from datetime import date

from flask import Flask, jsonify, render_template, request
from werkzeug.middleware.proxy_fix import ProxyFix

import i18n
import os
from assets import assets
from config import Config
from content import abroad, places, pricing, routes as route_data
from extensions import csrf, limiter
from monitoring import init_sentry
from routes.contact import contact_bp
from routes.geo import geo_bp
from routes.main import main_bp
from utils import setup_logger



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1)

    setup_logger(app)
    # Одразу після логера: Sentry підхоплює саме logging, тож має бути
    # налаштований раніше, ніж застосунок почне щось писати.
    init_sentry(app)

    csrf.init_app(app)
    limiter.init_app(app)
    assets.init_app(app)
    i18n.init_app(app)

    app.register_blueprint(contact_bp)
    app.register_blueprint(geo_bp)
    app.register_blueprint(main_bp)

    # ─── Контакти доступні в кожному шаблоні ────────────────────────────────
    @app.context_processor
    def inject_site_context():
        c = app.config
        return {
            "PHONE_E164": c["PHONE_E164"],
            "PHONE_DISPLAY": c["PHONE_DISPLAY"],
            "PHONE_IS_PLACEHOLDER": c["PHONE_IS_PLACEHOLDER"],
            "VIBER_URL": c["VIBER_URL"],
            "TELEGRAM_URL": c["TELEGRAM_URL"],
            "EMAIL": c["EMAIL"],
            "HOURS_OPEN": c["HOURS_OPEN"],
            "HOURS_CLOSE": c["HOURS_CLOSE"],
            "HOURS_LABEL": c["HOURS_LABEL"],
            "HOURS_NOTE": c["HOURS_NOTE"],
            "CITY": c["CITY"],
            "REGION": c["REGION"],
            "SITE_URL": c["SITE_URL"].rstrip("/"),
            "GA4_MEASUREMENT_ID": c["GA4_MEASUREMENT_ID"],
            "GTM_CONTAINER_ID": c["GTM_CONTAINER_ID"],
            "YEAR": date.today().year,
            # Тарифи — з одного модуля, щоб цифра на головній не розійшлася
            # з тією, яку рахує калькулятор.
            "PRICING": pricing,
            # Список міст області потрібен і на сторінці послуг, і в підвалі.
            "PLACES": places.PLACES,
            # Напрямки в підвалі. Це не прикраса: 96 адрес мають отримувати
            # посилання з кожної сторінки, інакше половина з них лишається
            # глибоко в структурі, і Google доходить до них у останню чергу.
            "ROUTES": route_data.ROUTES,
            "ABROAD": abroad.DESTINATIONS,
        }

    # ─── Заголовки безпеки ──────────────────────────────────────────────────
    @app.after_request
    def security_headers(resp):
        resp.headers.setdefault("X-Content-Type-Options", "nosniff")
        resp.headers.setdefault("X-Frame-Options", "SAMEORIGIN")
        resp.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
        resp.headers.setdefault(
            "Permissions-Policy", "geolocation=(self), microphone=(), camera=()"
        )
        if not app.debug:
            resp.headers.setdefault(
                "Strict-Transport-Security", "max-age=31536000; includeSubDomains"
            )

        # Статика з відбитком вмісту (?v=...) ніколи не змінюється за тією
        # самою адресою, тому її можна кешувати назавжди. Без відбитка —
        # година, щоб випадкове пряме звернення не залипло зі старим файлом.
        if request.path.startswith("/static/") and resp.status_code == 200:
            if request.args.get("v"):
                resp.headers["Cache-Control"] = "public, max-age=31536000, immutable"
            else:
                resp.headers["Cache-Control"] = "public, max-age=3600"
        elif resp.mimetype == "text/html" and resp.status_code == 200:
            # У HTML немає відбитка в адресі: /services сьогодні й завтра —
            # та сама адреса з різним вмістом. Досі ми не казали браузеру
            # нічого, і кожен вирішував сам. Наслідок ловили 5 вересня: після
            # деплою сторінка віддавала новий вміст, а в браузері лишалася
            # вчорашня — і виглядало це як «кеш Cloudflare», хоча Cloudflare
            # HTML не кешує взагалі (cf-cache-status: DYNAMIC).
            #
            # max-age=0 + must-revalidate — це не «не кешуй». Копію лишити
            # можна, але показувати її без запиту до сервера не можна.
            #
            # private, а не public: у формі заявки їде CSRF-токен, привʼязаний
            # до сесії. Спільним кешам таку сторінку зберігати не можна, навіть
            # якщо сьогодні жоден цього й не робить.
            resp.headers.setdefault("Cache-Control", "private, max-age=0, must-revalidate")

            # ETag тут НЕ ставимо, і це навмисно.
            #
            # Спокуса очевидна: must-revalidate без валідатора означає, що
            # браузер щоразу тягне всю сторінку, а з ETag він отримував би
            # 304 без тіла. Ми це спробували — і воно не працює.
            #
            # Причина: форма заявки стоїть унизу КОЖНОЇ сторінки, а Flask-WTF
            # підписує csrf_token через URLSafeTimedSerializer, який вшиває
            # в підпис мітку часу. Токен різний у кожній відповіді, отже тіло
            # різне, отже ETag різний — If-None-Match не збігається ніколи,
            # і замість 304 завжди 200. Перевірено на живому сайті.
            #
            # Щоб ETag запрацював, довелося б винести токен із HTML і
            # підвантажувати його окремо скриптом. Це зламало б роботу форми
            # без JS, яку ми зберігаємо навмисно. Обмін невигідний.
            #
            # bfcache (кнопки «назад/вперед») лишається робочим: його вимикає
            # тільки no-store, якого тут немає.
        return resp

    # ─── Сторінки помилок ───────────────────────────────────────────────────
    @app.errorhandler(404)
    def not_found(e):
        return render_template("404.html"), 404

    @app.errorhandler(429)
    def too_many_requests(e):
        msg = "Забагато заявок. Спробуйте пізніше або зателефонуйте нам."
        if (
            request.path.startswith("/contact")
            or request.path.startswith("/api/")
            or request.accept_mimetypes.best == "application/json"
        ):
            # error_code — щоб фронт узяв переклад; error лишається для
            # випадку без JS (див. _error() у routes/contact.py).
            return jsonify({"error_code": "too_many", "error": msg}), 429
        return render_template("500.html"), 429

    @app.errorhandler(400)
    def bad_request(e):
        # Найчастіша причина 400 тут — протермінований CSRF-токен
        if request.path.startswith("/contact") and request.method == "POST":
            return jsonify({
                "error_code": "session_expired",
                "error": "Сесія застаріла. Оновіть сторінку і спробуйте ще раз.",
            }), 400
        return render_template("404.html"), 400

    @app.errorhandler(500)
    def server_error(e):
        app.logger.exception(e)
        return render_template("500.html"), 500

    @app.route("/health")
    def health():
        return {"status": "ok"}, 200

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=os.getenv("FLASK_DEBUG") == "1", port=5001, host="0.0.0.0")
