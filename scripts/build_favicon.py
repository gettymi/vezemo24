#!/usr/bin/env python3
"""
Збирає весь набір іконок із одного SVG: static/brand/favicon.svg.

    python3 scripts/build_favicon.py

Потрібен Playwright (він і так стоїть для перевірок):

    pip install playwright && playwright install chromium

Чому браузер, а не бібліотека: рендер SVG у Chromium — той самий, який
побачить користувач, і не тягне cairo/librsvg у залежності проєкту.

ЩО ВАЖЛИВО В САМОМУ SVG. Він має бути КВАДРАТОМ НА ВСЮ ПЛОЩУ, без
прозорих кутів. Google обрізає фавікон у коло й підкладає біле тло, тому
іконка, яка сама намальована колом, показується у видачі як коло
всередині білого кола — з видимим білим обідком.
"""

import os
import pathlib
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "static", "brand", "favicon.svg")
OUT = os.path.join(ROOT, "static", "images")

# 48px — мінімум, який приймає Google; решта кратні йому або 16.
ICO_SIZES = [16, 32, 48]
PNG_SIZES = {
    "apple-touch-icon.png": 180,   # iOS накладає свою маску сам
    "icon-192.png": 192,           # Android / веб-маніфест
    "icon-512.png": 512,           # сплеш-екран PWA
}


def render(svg_text, size, path):
    from playwright.sync_api import sync_playwright
    html = ("<style>html,body{margin:0;padding:0}"
            "svg{display:block;width:%dpx;height:%dpx}</style>%s"
            % (size, size, svg_text))
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": size, "height": size},
                        device_scale_factor=1)
        pg.set_content(html)
        pg.wait_for_timeout(120)
        pg.screenshot(path=path)
        b.close()


def main():
    from PIL import Image
    svg = pathlib.Path(SRC).read_text(encoding="utf-8")
    os.makedirs(OUT, exist_ok=True)
    tmp = os.path.join(OUT, "_favicon-tmp.png")

    frames = []
    for s in ICO_SIZES:
        render(svg, s, tmp)
        frames.append(Image.open(tmp).convert("RGBA").copy())
    frames[-1].save(os.path.join(OUT, "favicon.ico"), format="ICO",
                    sizes=[(s, s) for s in ICO_SIZES])
    print("favicon.ico  %s" % ICO_SIZES)

    for name, size in PNG_SIZES.items():
        render(svg, size, os.path.join(OUT, name))
        print("%-22s %dpx" % (name, size))

    # SVG кладемо поруч: сучасні браузери беруть саме його й малюють
    # різко на будь-якому масштабі.
    pathlib.Path(os.path.join(OUT, "favicon.svg")).write_text(svg, encoding="utf-8")
    print("favicon.svg")

    if os.path.exists(tmp):
        os.remove(tmp)


if __name__ == "__main__":
    sys.exit(main())
