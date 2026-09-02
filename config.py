import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # ─── Secrets / integrations ──────────────────────────────────────────────
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_API")

    # ─── Rate limiting ───────────────────────────────────────────────────────
    # Порожній REDIS_URL -> Flask-Limiter працює в памʼяті (memory://).
    # Раніше цей ключ був відсутній взагалі, через що ліміт мовчки не працював.
    REDIS_URL = os.getenv("REDIS_URL", "")

    # ─── Analytics (заповнити реальними ID) ──────────────────────────────────
    GA4_MEASUREMENT_ID = os.getenv("GA4_MEASUREMENT_ID", "")   # напр. G-XXXXXXXXXX
    GTM_CONTAINER_ID = os.getenv("GTM_CONTAINER_ID", "")       # напр. GTM-XXXXXXX
    GOOGLE_ADS_ID = os.getenv("GOOGLE_ADS_ID", "")             # напр. AW-XXXXXXXXX
    GOOGLE_ADS_CONVERSION_LABEL = os.getenv("GOOGLE_ADS_CONVERSION_LABEL", "")

    # ─── Канонічний домен ────────────────────────────────────────────────────
    SITE_URL = os.getenv("SITE_URL", "https://vezemo24.com")

    # ══════════════════════════════════════════════════════════════════════════
    #  АВТОПАРК — ВИМКНЕНО ДО ЗАВЕРШЕННЯ ВЕРИФІКАЦІЇ
    #
    #  Сторінка /avtopark, блок на головній, посилання в підвалі й записи
    #  в sitemap.xml зникають усі разом, поки тут False. Код лишається на
    #  місці й перевіряється тестами — це прапорець, а не закоментований
    #  шматок, який через місяць ніхто не знайде.
    #
    #  Щоб увімкнути: FLEET_VISIBLE = True (або SHOW_FLEET=1 у .env).
    #  Сторінка тоді знову віддає 200 і повертається в мапу сайту.
    # ══════════════════════════════════════════════════════════════════════════
    FLEET_VISIBLE = os.getenv("SHOW_FLEET", "") == "1"

    # ══════════════════════════════════════════════════════════════════════════
    #  КОНТАКТИ — ЄДИНЕ МІСЦЕ ЗМІНИ
    #  ⚠️  ТИМЧАСОВИЙ НОМЕР-ЗАГЛУШКА. Замінити на реальний перед продакшеном:
    #      достатньо змінити PHONE_E164 та PHONE_DISPLAY тут — і номер
    #      оновиться в шапці, футері, мобільній панелі, schema.org та формі.
    # ══════════════════════════════════════════════════════════════════════════
    PHONE_E164 = os.getenv("PHONE_E164", "+380390000000")
    PHONE_DISPLAY = os.getenv("PHONE_DISPLAY", "+380 (39) 000-00-00")
    PHONE_IS_PLACEHOLDER = os.getenv("PHONE_E164") is None

    VIBER_URL = os.getenv("VIBER_URL", "")        # viber://chat?number=%2B380390000000
    # Кнопки месенджерів з'являються на сайті лише коли адреса задана —
    # порожнє посилання не малюється взагалі, щоб не вести в нікуди.
    TELEGRAM_URL = os.getenv("TELEGRAM_URL", "https://t.me/vezemo24")
    EMAIL = os.getenv("CONTACT_EMAIL", "info@vezemo24.com")

    # ─── Графік роботи ───────────────────────────────────────────────────────
    # Дзвінки 08:00–18:00, заявки через сайт — цілодобово.
    #
    # Ці два числа — єдине джерело. З них будується підпис під героєм,
    # текст переваги «виїзд у день звернення», відповідь у FAQ міст і
    # openingHoursSpecification у розмітці: Google бачить рівно те саме,
    # що й людина. У шаблонах і каталогах годин руками не писати —
    # підставляти {open} / {close}, інакше зміна графіка лишить у тексті
    # стару цифру, і жоден тест цього не помітить.
    HOURS_OPEN = "08:00"
    HOURS_CLOSE = "18:00"
    HOURS_LABEL = "Дзвінки 08:00 – 18:00"
    HOURS_NOTE = "Заявки на сайті — цілодобово"

    # ─── Зона обслуговування ─────────────────────────────────────────────────
    CITY = "Київ"
    REGION = "Київська область"
    AREAS_SERVED = ["Київ", "Київська область", "Україна"]
