"""
Три мови без зайвої машинерії.

Чому не Flask-Babel: він тягне залежність, .po-файли і крок компіляції
перед кожним деплоєм. Проєкт свідомо тримається без збірки (див. рішення
щодо фронтенду), а рядків тут кілька сотень — звичайні словники Python
читаються й правляться простіше, ніж бінарні .mo.

Адреси:
    /                     українська (типова, без префікса)
    /ru/  /en/            російська та англійська

Українська лишається в корені навмисно: це основна мова сайту, і її URL
не повинні змінюватись — там уже є посилання й дані Search Console.

Кожен маршрут оголошується двічі:

    @main_bp.route("/services", defaults={"lang": DEFAULT})
    @main_bp.route("/<any(ru,en):lang>/services")

Далі url_defaults сам підставляє поточну мову в кожен url_for(), тому
в шаблонах нічого міняти не треба — посилання самі лишаються в межах
обраної мови.
"""

from flask import g, request, url_for

from . import en, ru, uk

DEFAULT = "uk"
LOCALES = ("uk", "ru", "en")

# Підписи для перемикача. Своя мова завжди називається своєю мовою.
LOCALE_NAMES = {"uk": "Українська", "ru": "Русский", "en": "English"}
LOCALE_SHORT = {"uk": "UA", "ru": "RU", "en": "EN"}

# hreflang хоче код мови, а не наш внутрішній ключ.
HREFLANG = {"uk": "uk-UA", "ru": "ru-UA", "en": "en"}

# Open Graph користується власним записом локалі, не тим, що hreflang.
OG_LOCALE = {"uk": "uk_UA", "ru": "ru_UA", "en": "en_US"}

CATALOGS = {"uk": uk.STRINGS, "ru": ru.STRINGS, "en": en.STRINGS}


def current_locale():
    return getattr(g, "locale", DEFAULT)


def t(key, **kwargs):
    """
    Переклад за ключем.

    Якщо рядка немає в поточній мові — беремо український, щоб сторінка
    лишалась читабельною. Якщо немає й там, повертаємо сам ключ: помітна
    поломка краща за порожнє місце, яке ніхто не зауважить.
    """
    lang = current_locale()
    value = CATALOGS.get(lang, {}).get(key)
    if value is None:
        value = CATALOGS[DEFAULT].get(key, key)
    if kwargs:
        try:
            return value.format(**kwargs)
        except (KeyError, IndexError):
            return value
    return value


def locale_url(lang, endpoint=None, **values):
    """Адреса поточної (або вказаної) сторінки іншою мовою."""
    if endpoint is None:
        endpoint = request.endpoint
        values = dict(request.view_args or {}, **values)
    values.pop("lang", None)
    try:
        return url_for(endpoint, lang=lang, **values)
    except Exception:
        # Сторінка без мовних версій (robots.txt тощо) — лишаємось на місці.
        return url_for("main.index", lang=lang)


def alternates():
    """
    Усі мовні версії поточної сторінки — для hreflang.

    Повертає список (код_hreflang, абсолютний_URL). x-default додається
    окремо в шаблоні і вказує на українську.
    """
    return [(HREFLANG[l], locale_url(l)) for l in LOCALES]


def init_app(app):
    @app.url_value_preprocessor
    def _pull_lang(endpoint, values):
        # lang живе в URL, але у в'ю-функції він не потрібен — забираємо.
        g.locale = (values or {}).pop("lang", None) or DEFAULT

    @app.url_defaults
    def _push_lang(endpoint, values):
        if "lang" in values:
            return
        if app.url_map.is_endpoint_expecting(endpoint, "lang"):
            values["lang"] = getattr(g, "locale", DEFAULT)

    # Дозволяє перекладати список ключів прямо в шаблоні:
    #   {{ ['country.pl','country.cz'] | map('t_pass') | join(' · ') }}
    app.jinja_env.filters["t_pass"] = t

    @app.context_processor
    def _inject():
        lang = current_locale()
        return {
            "t": t,
            "LOCALE": lang,
            "LOCALES": LOCALES,
            "LOCALE_NAMES": LOCALE_NAMES,
            "LOCALE_SHORT": LOCALE_SHORT,
            "HREFLANG": HREFLANG,
            "OG_LOCALE": OG_LOCALE,
            "locale_url": locale_url,
            "alternates": alternates,
            "DEFAULT_LOCALE": DEFAULT,
        }
