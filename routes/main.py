from datetime import date

from flask import (
    Blueprint, render_template, url_for, Response, redirect, current_app
)

main_bp = Blueprint("main", __name__)

# Публічні сторінки для sitemap (без /thank-you — це сторінка конверсії)
SITEMAP_PAGES = [
    {"endpoint": "main.index",        "priority": "1.0",  "changefreq": "weekly"},
    {"endpoint": "main.services",     "priority": "0.9",  "changefreq": "monthly"},
    {"endpoint": "main.mizhmiski",    "priority": "0.9",  "changefreq": "monthly"},
    {"endpoint": "main.calculate_km", "priority": "0.85", "changefreq": "weekly"},
    {"endpoint": "contact.contact",   "priority": "0.8",  "changefreq": "monthly"},
]


def _abs_url(endpoint):
    """Абсолютний URL на канонічному домені (а не на тому, з якого прийшов запит)."""
    base = current_app.config["SITE_URL"].rstrip("/")
    return base + url_for(endpoint)


@main_bp.route("/")
def index():
    return render_template("index.html")


@main_bp.route("/calculate-km")
def calculate_km():
    return render_template("calculate_km.html")


@main_bp.route("/thank-you")
def thank_you():
    """Сторінка подяки — ціль конверсії для Google Ads / GA4."""
    return render_template("thank_you.html")


@main_bp.route("/services")
def services():
    return render_template("services.html")


@main_bp.route("/mizhmiski-perevezennya")
def mizhmiski():
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
    pages = [
        {
            "loc": _abs_url(item["endpoint"]),
            "lastmod": lastmod,
            "changefreq": item["changefreq"],
            "priority": item["priority"],
        }
        for item in SITEMAP_PAGES
    ]
    xml = render_template("sitemap_template.xml", pages=pages)
    return Response(xml, mimetype="application/xml; charset=utf-8")
