import html
import json
import os
import sqlite3
from datetime import datetime, timezone

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
        conn.commit()


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
    xff = request.headers.get("X-Forwarded-For")
    if xff:
        return xff.split(",")[0].strip()
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
@contact_bp.route("/contact", methods=["POST"])
@limiter.limit("5 per hour")   # реальний ліміт: 5 заявок/год з одного IP
def contact_submit():
    # Пастка для ботів: приховане поле, яке людина ніколи не заповнить
    if request.form.get("website", "").strip():
        current_app.logger.info("Honeypot спрацював, IP=%s", get_client_ip())
        return jsonify({"success": True}), 200  # тихо ігноруємо бота

    phone_raw = request.form.get("phone", "").strip()
    if not phone_raw:
        return jsonify({"error": "Введіть номер телефону."}), 400

    try:
        parsed = phonenumbers.parse(phone_raw, "UA")
        if not phonenumbers.is_valid_number(parsed):
            return jsonify({"error": "Введіть коректний номер телефону."}), 400
        phone = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
    except phonenumbers.NumberParseException:
        return jsonify({"error": "Введіть коректний номер телефону."}), 400

    name = html.escape(request.form.get("name", "").strip()) or "Не вказано"
    email = html.escape(request.form.get("email", "").strip()) or "Не вказано"
    message = html.escape(request.form.get("message", "").strip()) or "Не вказано"
    ip = get_client_ip()

    lead_id = save_lead({
        "name": name,
        "phone": phone,
        "email": email,
        "message": message,
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
        f"<i>IP: {ip} · №{lead_id if lead_id else '—'}</i>"
    )

    try:
        if send_telegram(text):
            mark_notified(lead_id)
    except (requests.RequestException, ValueError) as exc:
        # Заявка вже збережена — не змушуємо клієнта відправляти ще раз.
        current_app.logger.error("Telegram не прийняв заявку %s: %s", lead_id, exc)

    return jsonify({"success": True}), 200
