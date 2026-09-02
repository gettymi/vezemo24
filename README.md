# Vezemo24

Website for a cargo-transport company in Kyiv: van deliveries around the
city and region, intercity runs across Ukraine, and international trips to
Europe. Commercial work for a client, published with their agreement.

**Status: in progress.** The rebuild lives on the `version2` branch and is
not deployed yet.

---

## What it does

- **32 pages in three languages** (Ukrainian, Russian, English) — 96
  indexable URLs with `hreflang`, canonical tags and a generated sitemap.
  Pages for 10 towns in the Kyiv region, 11 intercity routes and 5
  European destinations, each written about that specific place rather
  than from a template.
- **Price calculator** — hourly for the city and region, per kilometre
  for intercity, per kilometre of total mileage for Europe. Routes are
  measured with real road distance, not straight lines.
- **Lead capture** — a form at the foot of every page. Submissions are
  written to SQLite first and only then sent to Telegram, so a failing
  API cannot lose an enquiry.

## Stack

Flask 3 and Jinja2. **No build step and no frontend framework** — the
client has to be able to hand this project to any developer, and a
toolchain that rots in six months is a liability, not an asset.

| | |
|---|---|
| Backend | Flask, Jinja2, SQLite |
| Frontend | Vanilla JS, CSS with cascade layers |
| Maps | Leaflet, with Nominatim and OSRM proxied server-side |
| Images | AVIF / WebP generated from originals, content-hash cache busting |

## Decisions worth explaining

**CSS cascade layers.** `reset, tokens, base, layout, components, pages,
utilities`. Specificity conflicts are settled once by layer order instead
of by `!important` scattered through the file.

**Every price lives in one module.** `content/pricing.py` holds each rate;
templates interpolate `{rate}` and `{feed}`, and no figure is typed by
hand anywhere else. Changing a tariff is a one-line edit that cannot leave
a stale number behind in some page nobody remembers.

**Internationalisation without Flask-Babel.** Three Python dictionaries,
432 keys each, with a check that the key sets stay identical. No
compilation step, and a missing translation is a test failure rather than
a blank space on a page.

**Geocoding is proxied, not called from the browser.** `/api/geo/*` sits
in front of Nominatim and OSRM with a 30-day SQLite cache and a
one-request-per-second limit shared across workers, so the rate limit is
respected once rather than per visitor.

**The phone field is written, not imported.** 6 KB against 200 KB for
`intl-tel-input` from a CDN. Country names come from `Intl.DisplayNames`,
so three languages cost nothing and cannot drift apart from each other.

**Weight.** The home page is 360 KB over 13 requests before compression:
no framework, no icon font, no third-party CDN. The video block loads a
58 KB poster frame and no video at all until someone presses play.

## Running it locally

```bash
python3 -m venv myenv && source myenv/bin/activate
pip install -r requirements.txt
cp .env.example .env          # then fill in the values below
python3 app.py                # http://127.0.0.1:5001
```

Leaflet is vendored rather than loaded from a CDN:

```bash
bash scripts/vendor_leaflet.sh
```

### Environment

Nothing is required to start the site, but these change how it behaves:

| Variable | Purpose |
|---|---|
| `SECRET_KEY` | Session signing. Required in production. |
| `SITE_URL` | Absolute URLs in the sitemap and structured data |
| `PHONE_DISPLAY` | Phone number as shown on the page |
| `TELEGRAM_TOKEN`, `TELEGRAM_CHAT_ID` | Where new enquiries are sent |
| `TELEGRAM_URL`, `VIBER_URL` | Messenger buttons; hidden when unset |
| `GTM_CONTAINER_ID`, `GOOGLE_ADS_ID` | Analytics and conversion tracking |
| `SHOW_FLEET` | `1` publishes the vehicle page; off by default |
| `REDIS_URL` | Shared rate limiting across workers |

## Layout

```
app.py              application factory, template context
config.py           settings and business constants
content/            data the pages are built from
  pricing.py        every rate, single source of truth
  places.py         towns in the Kyiv region
  routes.py         intercity directions
  abroad.py         European destinations
  fleet.py          vehicles
routes/             blueprints: main, contact, geo
i18n/               uk.py, ru.py, en.py — 432 keys each
templates/          Jinja templates and partials
static/
  css/              app.css (design system), map.css (calculator only)
  js/               no bundler, no dependencies
  images/derived/   generated AVIF/WebP variants
scripts/            image, favicon and vendoring build scripts
```

## Not done yet

- Not deployed; the live domain still serves the previous version.
- The map's happy path is unverified — Nominatim and OSRM are unreachable
  from the development environment, so `/api/geo/*` is only proven to fail
  gracefully rather than to succeed.
- Vehicle specifications and photographs of the van in use are still
  outstanding from the client.
- No Content-Security-Policy header yet. There are no inline scripts
  anywhere, which is the easiest possible state to add one from.

## Licence

All rights reserved. See [LICENSE](LICENSE).
