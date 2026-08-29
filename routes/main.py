from datetime import date

from flask import (
    Blueprint, render_template, url_for, Response, redirect, current_app
)

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
    {"endpoint": "contact.contact",   "priority": "0.8",  "priority_alt": "0.6",  "changefreq": "monthly"},
]


def _abs_url(endpoint, lang=None):
    """Абсолютний URL на канонічному домені (а не на тому, з якого прийшов запит)."""
    base = current_app.config["SITE_URL"].rstrip("/")
    return base + (url_for(endpoint, lang=lang) if lang else url_for(endpoint))


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


@main_bp.route("/mizhmiski-perevezennya", defaults={"lang": DEFAULT})
@main_bp.route(LANG_RULE + "/mizhmiski-perevezennya")
def mizhmiski(lang=DEFAULT):
    """Міжміські перевезення по Україні."""
    return render_template("mizhmiski.html")


# ─── 301 зі старих URL ───────────────────────────────────────────────────────
# Стара адреса містила літеру з наголосом (/zakordón -> /zakord%C3%B3n),
# що псувало вигляд у видачі та в поширених посиланнях.
@main_bp.route("/zakordón")
@main_bp.route("/zakordon")
def zakordon_legacy():
    return redirect(url_for("main.mizhmiski"), code=301)



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
    ]
    xml = render_template("sitemap_template.xml", pages=pages)
    return Response(xml, mimetype="application/xml; charset=utf-8")
