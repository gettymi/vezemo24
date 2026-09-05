import html
import json
import os
import sqlite3
from datetime import datetime, timedelta, timezone

import phonenumbers
import requests
from flask import Blueprint, current_app, jsonify, render_template, request

from i18n import DEFAULT

from extensions import limiter

contact_bp = Blueprint("contact", __name__)

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "leads.db")


# ─────────────────────────────────────────────────────────────────────────────
#  Збереження заявок
#  Раніше заявка існувала ЛИШЕ як повідомлення в Telegram: якщо API недоступне
#  або змінився токен — лід зникав назавжди. Тепер спочатку пишемо в базу,
#  і тільки потім намагаємось сповістити.
# ─────────────────────────────────────────────────────────────────────────────
def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS leads (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL,
                name       TEXT,
                phone      TEXT NOT NULL,
                email      TEXT,
                message    TEXT,
                ip         TEXT,
                user_agent TEXT,
                referer    TEXT,
                notified   INTEGER NOT NULL DEFAULT 0
            )
            """
        )
        # Індекс під перевірку дублів (find_duplicate). Без нього кожна
        # заявка читала б таблицю цілком — спершу непомітно, потім ні.
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_leads_dedupe "
            "ON leads (phone, created_at)"
        )
        conn.commit()


# Скільки часу вважаємо повторну відправку тією самою заявкою.
DEDUPE_WINDOW_SECONDS = 300


def find_duplicate(phone, ip, message):
    """id недавньої ІДЕНТИЧНОЇ заявки, якщо така вже є.

    Кнопку блокує contact.js, але це не рятує від сценарію, де JS відпрацював
    правильно: повільний зв'язок, запит відвалився за таймаутом, людина
    натиснула ще раз. Заявка при цьому вже лежить у базі, і власник отримує
    два однакових повідомлення.

    Збіг вимагаємо за трьома полями одразу — телефон, IP і текст. Тільки
    телефон брати не можна: людина цілком може дописати «а ще піаніно»
    другим повідомленням, і воно мусить дійти. Тут же збігається все, тобто
    це та сама відправка, а не нова думка.
    """
    cutoff = (datetime.now(timezone.utc)
              - timedelta(seconds=DEDUPE_WINDOW_SECONDS)).isoformat(timespec="seconds")
    try:
        init_db()
        with sqlite3.connect(DB_PATH) as conn:
            row = conn.execute(
                """SELECT id FROM leads
                   WHERE phone = ? AND ip = ? AND message = ? AND created_at >= ?
                   ORDER BY id DESC LIMIT 1""",
                (phone, ip, message, cutoff),
            ).fetchone()
        return row[0] if row else None
    except sqlite3.Error as exc:
        # Помилка перевірки не має коштувати заявки: краще зберегти двічі,
        # ніж не зберегти взагалі.
        current_app.logger.error("Перевірка дубля не вдалася: %s", exc)
        return None


def save_lead(data):
    try:
        init_db()
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.execute(
                """INSERT INTO leads
                   (created_at, name, phone, email, message, ip, user_agent, referer, notified)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, 0)""",
                (
                    datetime.now(timezone.utc).isoformat(timespec="seconds"),
                    data.get("name"),
                    data.get("phone"),
                    data.get("email"),
                    data.get("message"),
                    data.get("ip"),
                    data.get("user_agent"),
                    data.get("referer"),
                ),
            )
            conn.commit()
            return cur.lastrowid
    except sqlite3.Error as exc:
        current_app.logger.error("Не вдалося зберегти заявку в БД: %s", exc)
        # Останній рубіж: дописуємо в файл, щоб заявка не зникла взагалі
        try:
            with open(os.path.join(os.path.dirname(DB_PATH), "leads-fallback.jsonl"), "a", encoding="utf-8") as fh:
                fh.write(json.dumps(data, ensure_ascii=False) + "\n")
        except OSError:
            current_app.logger.exception("Не вдалося записати заявку навіть у файл")
        return None


def mark_notified(lead_id):
    if lead_id is None:
        return
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute("UPDATE leads SET notified = 1 WHERE id = ?", (lead_id,))
            conn.commit()
    except sqlite3.Error as exc:
        current_app.logger.error("Не вдалося оновити статус заявки %s: %s", lead_id, exc)


def get_client_ip():
    """IP відвідувача — рівно те, що бачить решта застосунку.

    Раніше тут вручну бралася ПЕРША адреса з X-Forwarded-For. Це помилка:
    Cloudflare ДОДАЄ справжній IP у кінець заголовка, а все, що стояло там
    до нього, прийшло від самого клієнта — тобто підробляється одним рядком
    у запиті. У базу лідів лягав би IP, який назвав відвідувач.

    ProxyFix(x_for=1) у create_app() уже розібрав заголовок правильно й
    поклав результат у request.remote_addr. Тим самим значенням оперує
    рейт-лімітер (key_func=get_remote_address), тож окрема логіка тут ще й
    розходилася з тим, за чим рахуються ліміти.
    """
    return request.remote_addr or "0.0.0.0"


def send_telegram(text):
    token = current_app.config.get("TELEGRAM_TOKEN")
    chat_id = current_app.config.get("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        current_app.logger.error("Telegram не налаштований — заявка лише в БД")
        return False
    resp = requests.post(
        f"https://api.telegram.org/bot{token}/sendMessage",
        data={"chat_id": chat_id, "text": text, "parse_mode": "HTML"},
        timeout=6,
    )
    resp.raise_for_status()
    return True


@contact_bp.route("/contact", methods=["GET"], defaults={"lang": DEFAULT})
@contact_bp.route("/<any(ru,en):lang>/contact", methods=["GET"])
def contact(lang=DEFAULT):
    return render_template("contact.html")


# POST лишається одним, спільним для всіх мов: форма шле дані, а не сторінку.
def _error(code, fallback, status=400):
    """Помилка форми — кодом, а не готовою фразою.

    Раніше сервер віддавав саме текст, і contact.js показував його першим:
    `showAlert(r.body.error || VZT("form.send_failed"))`. Через це
    російськомовний або англомовний відвідувач бачив український рядок —
    причому саме тоді, коли помилився й намагається залишити заявку.

    Тепер мову обирає фронт: у static/js/i18n.js ці фрази вже є трьома
    мовами. Поле `error` лишається для випадку без JS і для тих, хто читає
    відповідь напряму.
    """
    return jsonify({"error_code": code, "error": fallback}), status


@contact_bp.route("/contact", methods=["POST"])
@limiter.limit("5 per hour")   # реальний ліміт: 5 заявок/год з одного IP
def contact_submit():
    # Пастка для ботів: приховане поле, яке людина ніколи не заповнить
    if request.form.get("website", "").strip():
        current_app.logger.info("Honeypot спрацював, IP=%s", get_client_ip())
        return jsonify({"success": True}), 200  # тихо ігноруємо бота

    phone_raw = request.form.get("phone", "").strip()
    if not phone_raw:
        return _error("phone_required", "Введіть номер телефону.")

    try:
        # Номер приходить у міжнародному вигляді (+380…, +48…): у формі тепер
        # є вибір країни. Регіон "UA" лишається запасним варіантом для тих,
        # хто вставив «067…» без коду — а таких більшість.
        region = None if phone_raw.startswith("+") else "UA"
        parsed = phonenumbers.parse(phone_raw, region)
        if not phonenumbers.is_valid_number(parsed):
            return _error("bad_phone", "Введіть коректний номер телефону.")
        phone = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
    except phonenumbers.NumberParseException:
        return _error("bad_phone", "Введіть коректний номер телефону.")

    name = html.escape(request.form.get("name", "").strip()) or "Не вказано"
    email = html.escape(request.form.get("email", "").strip()) or "Не вказано"
    message = html.escape(request.form.get("message", "").strip()) or "Не вказано"
    # Звідки прийшла заявка. Форма стоїть унизу кожної сторінки, і без цього
    # поля неможливо сказати, які сторінки приносять клієнтів, а які просто
    # існують. Обрізаємо жорстко: поле наше, але приходить із браузера, тож
    # довіряти йому не можна.
    source = html.escape(request.form.get("source", "").strip())[:60] or "—"
    ip = get_client_ip()
    full_message = message + ("" if source == "—" else "\n[джерело: %s]" % source)

    # Та сама заявка вже прийшла хвилину тому — не зберігаємо вдруге й не
    # шлемо друге повідомлення. Відвідувачу однаково відповідаємо успіхом:
    # з його боку заявка справді залишена.
    duplicate_id = find_duplicate(phone, ip, full_message)
    if duplicate_id is not None:
        current_app.logger.info("Повторна відправка заявки №%s, пропускаємо", duplicate_id)
        return jsonify({"success": True}), 200

    lead_id = save_lead({
        "name": name,
        "phone": phone,
        "email": email,
        "message": full_message,
        "ip": ip,
        "user_agent": request.headers.get("User-Agent", "")[:400],
        "referer": request.headers.get("Referer", "")[:400],
    })

    text = (
        "<b>📩 Нова заявка</b>\n\n"
        f"<b>Телефон:</b> {phone}\n"
        f"<b>Імʼя:</b> {name}\n"
        f"<b>Email:</b> {email}\n\n"
        f"<b>Повідомлення:</b>\n{message}\n\n"
        f"<b>Звідки:</b> {source}\n\n"
        f"<i>IP: {ip} · №{lead_id if lead_id else '—'}</i>"
    )

    try:
        if send_telegram(text):
            mark_notified(lead_id)
    except (requests.RequestException, ValueError) as exc:
        # Заявка вже збережена — не змушуємо клієнта відправляти ще раз.
        current_app.logger.error("Telegram не прийняв заявку %s: %s", lead_id, exc)

    return jsonify({"success": True}), 200
