"""
Проксі до геосервісів (Nominatim, OSRM) з кешем на боці сервера.

Навіщо це взагалі: раніше браузер ходив у nominatim.openstreetmap.org
напряму. Три проблеми, які так не вирішуються:

1. Політика використання Nominatim вимагає осмисленого User-Agent, а
   браузерам заборонено його виставляти — заголовок мовчки ігнорувався.
2. Кешу не було взагалі: десять людей, які шукають «Хрещатик», давали
   десять однакових запитів до безкоштовного сервісу.
3. Обмеження «не більше запиту в секунду» ніяк не дотримувалось.

Тепер усе йде через власні /api/geo/*: є кеш у SQLite, є нормальний
User-Agent і є дотримання інтервалу між запитами — спільне для всіх
воркерів gunicorn, бо мітка часу лежить у тій самій базі, а не в памʼяті
процесу.

ВІДОМЕ ОБМЕЖЕННЯ. Nominatim прямо просить не використовувати його для
пошуку «за кожним натисканням клавіші». Кеш і збільшений дебаунс роблять
навантаження помірним, але сам патерн лишається небажаним. Правильний
наступний крок — Photon (photon.komoot.io): ті самі дані OSM, але сервіс
створений саме під автодоповнення. Завдяки цьому модулю така заміна — це
правка одного місця, а не переписування фронтенду.
"""

import json
import os
import sqlite3
import threading
import time

import requests
from flask import Blueprint, current_app, jsonify, request

from extensions import limiter

geo_bp = Blueprint("geo", __name__, url_prefix="/api/geo")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE_DB = os.path.join(BASE_DIR, "geocache.db")

NOMINATIM_SEARCH = "https://nominatim.openstreetmap.org/search"
NOMINATIM_REVERSE = "https://nominatim.openstreetmap.org/reverse"
OSRM_ROUTE = "https://router.project-osrm.org/route/v1/driving"

# Адреси не переїжджають, тому кеш можна тримати довго.
TTL_SECONDS = 30 * 24 * 3600
MIN_INTERVAL = 1.1          # вимога Nominatim: не частіше ніж раз на секунду
MAX_WAIT = 3.0              # довше не чекаємо — краще чесно віддати 503
HTTP_TIMEOUT = 8

_init_lock = threading.Lock()
_initialised = False


# ── кеш ─────────────────────────────────────────────────────────────────────
def _connect():
    conn = sqlite3.connect(CACHE_DB, timeout=10)
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def _init_db():
    global _initialised
    if _initialised:
        return
    with _init_lock:
        if _initialised:
            return
        conn = _connect()
        try:
            conn.execute(
                "CREATE TABLE IF NOT EXISTS geo_cache ("
                " key TEXT PRIMARY KEY,"
                " payload TEXT NOT NULL,"
                " created_at REAL NOT NULL)"
            )
            conn.execute(
                "CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT)"
            )
            conn.commit()
        finally:
            conn.close()
        _initialised = True


def _cache_get(key):
    _init_db()
    conn = _connect()
    try:
        row = conn.execute(
            "SELECT payload, created_at FROM geo_cache WHERE key = ?", (key,)
        ).fetchone()
    finally:
        conn.close()
    if not row:
        return None
    if time.time() - row[1] > TTL_SECONDS:
        return None
    try:
        return json.loads(row[0])
    except ValueError:
        return None


def _cache_put(key, value):
    _init_db()
    conn = _connect()
    try:
        conn.execute(
            "INSERT OR REPLACE INTO geo_cache (key, payload, created_at) VALUES (?, ?, ?)",
            (key, json.dumps(value, ensure_ascii=False), time.time()),
        )
        conn.commit()
    except sqlite3.Error as exc:
        current_app.logger.warning("Кеш геокодера недоступний: %s", exc)
    finally:
        conn.close()


# ── дотримання інтервалу між запитами ───────────────────────────────────────
def _reserve_slot():
    """
    Резервує наступний дозволений момент запиту і повертає, скільки чекати.

    Мітка часу зберігається в базі, а не в памʼяті процесу: інакше кожен
    воркер gunicorn дотримувався б інтервалу окремо, і разом вони все одно
    перевищували б ліміт.
    """
    _init_db()
    conn = _connect()
    try:
        conn.isolation_level = None
        conn.execute("BEGIN IMMEDIATE")
        row = conn.execute("SELECT value FROM meta WHERE key = 'last_req'").fetchone()
        last = float(row[0]) if row else 0.0
        slot = max(time.time(), last + MIN_INTERVAL)
        conn.execute(
            "INSERT OR REPLACE INTO meta (key, value) VALUES ('last_req', ?)",
            (str(slot),),
        )
        conn.execute("COMMIT")
    except sqlite3.Error:
        # Якщо з базою щось не так — краще пропустити запит, ніж впасти.
        return 0.0
    finally:
        conn.close()
    return max(0.0, slot - time.time())


def _user_agent():
    site = current_app.config.get("SITE_URL", "").rstrip("/")
    email = current_app.config.get("EMAIL", "")
    return "Vezemo24/1.0 (+%s; %s)" % (site or "https://vezemo24.com", email)


def _upstream_get(url, params, throttle=True):
    if throttle:
        wait = _reserve_slot()
        if wait > MAX_WAIT:
            return None, "busy"
        if wait > 0:
            time.sleep(wait)
    try:
        resp = requests.get(
            url,
            params=params,
            headers={"User-Agent": _user_agent(), "Accept": "application/json"},
            timeout=HTTP_TIMEOUT,
        )
        resp.raise_for_status()
        return resp.json(), None
    except (requests.RequestException, ValueError) as exc:
        current_app.logger.warning("Геосервіс недоступний (%s): %s", url, exc)
        return None, "upstream"


def _fail(reason):
    if reason == "busy":
        return jsonify({"error": "Забагато запитів. Спробуйте за мить."}), 503
    return jsonify({"error": "Сервіс адрес тимчасово недоступний."}), 502


# ── ендпойнти ───────────────────────────────────────────────────────────────
@geo_bp.route("/search")
@limiter.limit("90 per minute")
def search():
    query = (request.args.get("q") or "").strip()
    if len(query) < 2:
        return jsonify({"results": []})
    try:
        limit = min(max(int(request.args.get("limit", 6)), 1), 10)
    except ValueError:
        limit = 6

    key = "s:%d:%s" % (limit, query.lower())
    cached = _cache_get(key)
    if cached is not None:
        return jsonify({"results": cached, "cached": True})

    data, err = _upstream_get(
        NOMINATIM_SEARCH,
        {
            "q": query,
            "format": "json",
            "limit": limit,
            "countrycodes": "ua",
            # Без цього Nominatim віддає назви не українською.
            "accept-language": "uk",
        },
    )
    if err:
        return _fail(err)

    results = [
        {
            "lat": float(d["lat"]),
            "lng": float(d["lon"]),
            "display": d.get("display_name", ""),
        }
        for d in (data or [])
        if d.get("lat") and d.get("lon")
    ]
    _cache_put(key, results)
    return jsonify({"results": results})


@geo_bp.route("/reverse")
@limiter.limit("60 per minute")
def reverse():
    try:
        lat = float(request.args["lat"])
        lng = float(request.args["lon"])
    except (KeyError, ValueError):
        return jsonify({"error": "Потрібні координати lat і lon."}), 400

    # Округлення до ~11 м: без нього кожен піксель кліку по карті давав би
    # власний ключ і кеш ніколи б не спрацьовував.
    key = "r:%.4f:%.4f" % (lat, lng)
    cached = _cache_get(key)
    if cached is not None:
        return jsonify({"display": cached, "cached": True})

    data, err = _upstream_get(
        NOMINATIM_REVERSE,
        {"lat": lat, "lon": lng, "format": "json", "accept-language": "uk"},
    )
    if err:
        return _fail(err)

    display = (data or {}).get("display_name") or "Точка на карті"
    _cache_put(key, display)
    return jsonify({"display": display})


@geo_bp.route("/route")
@limiter.limit("40 per minute")
def route():
    coords = (request.args.get("coords") or "").strip()
    if not coords or ";" not in coords:
        return jsonify({"error": "Потрібні щонайменше дві точки."}), 400
    # Пропускаємо далі лише те, що справді схоже на координати.
    try:
        pairs = [p.split(",") for p in coords.split(";")]
        cleaned = ";".join(
            "%.6f,%.6f" % (float(lng), float(lat)) for lng, lat in pairs
        )
    except (ValueError, TypeError):
        return jsonify({"error": "Некоректні координати."}), 400

    key = "o:%s" % cleaned
    cached = _cache_get(key)
    if cached is not None:
        return jsonify(dict(cached, cached=True))

    # OSRM — окремий сервіс зі своїм лімітом, спільну чергу з Nominatim
    # йому нав'язувати не треба.
    data, err = _upstream_get(
        "%s/%s" % (OSRM_ROUTE, cleaned),
        {"overview": "full", "geometries": "geojson"},
        throttle=False,
    )
    if err:
        return _fail(err)
    if not data or data.get("code") != "Ok" or not data.get("routes"):
        return jsonify({"error": "Маршрут не знайдено."}), 404

    r = data["routes"][0]
    payload = {
        "distance": r.get("distance"),
        "duration": r.get("duration"),
        "geometry": r.get("geometry"),
        "legs": [
            {"distance": leg.get("distance"), "duration": leg.get("duration")}
            for leg in r.get("legs", [])
        ],
    }
    _cache_put(key, payload)
    return jsonify(payload)
