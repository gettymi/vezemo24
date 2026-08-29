from datetime import date

from urllib.parse import urlencode

from flask import (
    Blueprint, abort, render_template, url_for, Response, redirect, current_app
)

import content.abroad as abroad_data
import content.routes as route_data
from content import pricing
from i18n import DEFAULT, LOCALES

main_bp = Blueprint("main", __name__)

# Кожна публічна сторінка живе за трьома адресами. Українська — в корені,
# без префікса: це основна мова, її URL уже проіндексовані й міняти їх
# заради симетрії було б шкідливо.
#
#   /            /ru/            /en/
#   /services    /ru/services    /en/services
#
# Другий декоратор ловить префікс, а defaults={"lang": DEFAULT} тримає
# українську версію в корені. Далі url_defaults (див. i18n/__init__.py)
# сам підставляє поточну мову в кожен url_for, тому в шаблонах посилання
# лишились без змін і не викидають людину з обраної мови.
LANG_RULE = "/<any(ru,en):lang>" 

# Публічні сторінки для sitemap (без /thank-you — це сторінка конверсії)
SITEMAP_PAGES = [
    {"endpoint": "main.index",        "priority": "1.0",  "priority_alt": "0.8",  "changefreq": "weekly"},
    {"endpoint": "main.services",     "priority": "0.9",  "priority_alt": "0.7",  "changefreq": "monthly"},
    {"endpoint": "main.mizhmiski",    "priority": "0.9",  "priority_alt": "0.7",  "changefreq": "monthly"},
    {"endpoint": "main.calculate_km", "priority": "0.85", "priority_alt": "0.65", "changefreq": "weekly"},
    {"endpoint": "main.abroad",       "priority": "0.9",  "priority_alt": "0.7",  "changefreq": "monthly"},
    {"endpoint": "contact.contact",   "priority": "0.8",  "priority_alt": "0.6",  "changefreq": "monthly"},
]


def _t(key):
    """t() з i18n, але доступний і поза шаблоном."""
    from i18n import t
    return t(key)


def _abs_url(endpoint, lang=None, **values):
    """Абсолютний URL на канонічному домені (а не на тому, з якого прийшов запит)."""
    base = current_app.config["SITE_URL"].rstrip("/")
    return base + (url_for(endpoint, lang=lang, **values) if lang
                   else url_for(endpoint, **values))


@main_bp.route("/", defaults={"lang": DEFAULT})
@main_bp.route(LANG_RULE + "/")
def index(lang=DEFAULT):
    return render_template("index.html")


@main_bp.route("/calculate-km", defaults={"lang": DEFAULT})
@main_bp.route(LANG_RULE + "/calculate-km")
def calculate_km(lang=DEFAULT):
    return render_template("calculate_km.html")


@main_bp.route("/thank-you", defaults={"lang": DEFAULT})
@main_bp.route(LANG_RULE + "/thank-you")
def thank_you(lang=DEFAULT):
    """Сторінка подяки — ціль конверсії для Google Ads / GA4."""
    return render_template("thank_you.html")


@main_bp.route("/services", defaults={"lang": DEFAULT})
@main_bp.route(LANG_RULE + "/services")
def services(lang=DEFAULT):
    return render_template("services.html")


# Сторінка на кожен напрямок. Людина шукає «перевезення Київ Львів», а не
# «вантажні перевезення» — загальна сторінка на такий запит не відповідає.
# Слаг латиницею і однаковий для всіх мов: адреса лишається стабільною,
# навіть якщо назва міста різна в кожній локалі.
@main_bp.route("/perevezennya/<slug>", defaults={"lang": DEFAULT})
@main_bp.route(LANG_RULE + "/perevezennya/<slug>")
def route_page(slug, lang=DEFAULT):
    route = route_data.get(slug)
    if route is None:
        abort(404)

    from flask import g
    locale = getattr(g, "locale", DEFAULT)
    city = _t(route["city"])

    # Калькулятор відкривається вже заповненим. Передаємо слаг, а не назви
    # міст: у map.js для цих напрямків є готові координати, тож розрахунок
    # відбувається миттєво й не витрачає ліміт геокодера.
    calc_url = url_for("main.calculate_km") + "?" + urlencode({"route": slug})

    # Ціну міжміського рейсу можна назвати чесно: вона залежить від
    # відстані, а відстань відома. Погодинну — ні, бо ніхто наперед не
    # знає, скільки триватиме завантаження.
    price = pricing.quote_intercity(route["km"])
    price_return = pricing.quote_intercity_return(route["km"])

    return render_template(
        "route.html",
        route=route,
        price=price,
        price_return=price_return,
        pricing=pricing,
        copy=route_data.copy_for(route, locale),
        via_names=[_t(k) for k in route.get("via", [])],
        # Показуємо не всі напрямки, а п'ять найближчих за відстанню. Дві
        # причини: список із десяти однакових рядків на кожній сторінці роздуває
        # частку шаблонного тексту (а це саме те, за чим Google визначає
        # дублікати), і читачеві корисніші сусідні плечі, а не повний перелік.
        others=sorted(
            (r for r in route_data.ROUTES if r["slug"] != slug),
            key=lambda r: abs(r["km"] - route["km"]),
        )[:5],
        calc_url=calc_url,
    )


@main_bp.route("/mizhmiski-perevezennya", defaults={"lang": DEFAULT})
@main_bp.route(LANG_RULE + "/mizhmiski-perevezennya")
def mizhmiski(lang=DEFAULT):
    """Міжміські перевезення по Україні."""
    # Напрямки з власними сторінками показуємо посиланнями, решту — просто
    # рядком. Так список не бреше: клікабельне те, що справді існує.
    return render_template("mizhmiski.html", routes=route_data.ROUTES)


@main_bp.route("/perevezennya-za-kordon", defaults={"lang": DEFAULT})
@main_bp.route(LANG_RULE + "/perevezennya-za-kordon")
def abroad(lang=DEFAULT):
    """Міжнародні перевезення. Ціна — ставка за км, суму рахує калькулятор."""
    return render_template("abroad.html", destinations=abroad_data.DESTINATIONS)


# ─── 301 зі старих URL ───────────────────────────────────────────────────────
# Стара адреса містила літеру з наголосом (/zakordón -> /zakord%C3%B3n),
# що псувало вигляд у видачі та в поширених посиланнях.
@main_bp.route("/zakordón")
@main_bp.route("/zakordon")
def zakordon_legacy():
    # Раніше вела на міжміські, бо закордонної послуги не було. Тепер є.
    return redirect(url_for("main.abroad"), code=301)



@main_bp.route("/robots.txt")
def robots():
    lines = [
        "User-agent: *",
        "Allow: /",
        "",
        "# Службові сторінки — не індексувати",
        "Disallow: /thank-you",
        "Disallow: /health",
        "",
        f"Sitemap: {_abs_url('main.sitemap')}",
    ]
    return Response("\n".join(lines) + "\n", mimetype="text/plain; charset=utf-8")


@main_bp.route("/sitemap.xml")
def sitemap():
    lastmod = date.today().isoformat()
    # Кожна сторінка потрапляє в мапу тричі — по разу на мову. Без цього
    # Google просто не дізнається, що російська та англійська версії існують.
    pages = [
        {
            "loc": _abs_url(item["endpoint"], lang),
            "lastmod": lastmod,
            "changefreq": item["changefreq"],
            "priority": item["priority"] if lang == DEFAULT else item["priority_alt"],
        }
        for item in SITEMAP_PAGES
        for lang in LOCALES
    ] + [
        {
            "loc": _abs_url("main.route_page", lang, slug=r["slug"]),
            "lastmod": lastmod,
            "changefreq": "monthly",
            "priority": "0.8" if lang == DEFAULT else "0.6",
        }
        for r in route_data.ROUTES
        for lang in LOCALES
    ]
    xml = render_template("sitemap_template.xml", pages=pages)
    return Response(xml, mimetype="application/xml; charset=utf-8")
