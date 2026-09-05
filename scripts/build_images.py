#!/usr/bin/env python3
"""
Генерує адаптивні варіанти зображень (AVIF / WebP / оригінальний формат)
для static/images/.

Запускати після того, як додали нові фото:

    python3 scripts/build_images.py          # тільки нове/змінене
    python3 scripts/build_images.py --force  # перегенерувати все

Результат кладеться в static/images/derived/, оригінали не чіпаються.
Шаблони підхоплюють варіанти через макрос picture() у
templates/partials/_media.html.
"""

import argparse
import json
import os

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(ROOT, "static", "images")
OUT_DIR = os.path.join(SRC_DIR, "derived")

# Ширини підібрані під реальні місця показу, а не «про запас»:
# немає сенсу класти 1920px у картку, яка ніколи не ширша за 400px.
SOURCES = {
    # Фон героя — на всю ширину екрана, тому потрібні великі варіанти.
    "video-poster.jpg": {"widths": [640, 960, 1280, 1920], "fallback": "JPEG"},
    # .split__media на /mizhmiski. Після перебудови головної (2 вересня) блок
    # став на всю ширину: sizes каже 1092px на десктопі, тобто 2184px на екрані
    # 2x. Старий максимум 1040 давав рівно вдвічі менше пікселів, ніж просить
    # браузер, — звідси й «розтягнуте, неякісне». Джерело НЕ вужче за 2100px.
    #
    # Кадр обрізаний одразу під 21:9 — саме таке aspect-ratio задане інлайном
    # у самому блоці, а не 13:9 із CSS. Раніше джерело було 13:9, і браузер
    # зрізав з нього верх і низ сам: фотографію готували під одну пропорцію,
    # а показували в іншій, тобто третина кадру просто не була видна.
    "road-wide.jpg": {"widths": [480, 720, 1040, 1560, 2080], "fallback": "JPEG"},
    # Смуга на /abroad. Блок такий самий, як у міжміських: на всю ширину
    # контейнера (1092px), тобто 2184px на екрані 2x. Джерело 2600 — із
    # запасом.
    "abroad-wide.jpg": {"widths": [480, 720, 1040, 1560, 2080], "fallback": "JPEG"},
    # Картки «Міжміські» і «Європа» на головній: те саме .card__media,
    # 540px на десктопі -> 1080px на екрані 2x.
    "intercity-card.jpg": {"widths": [400, 600, 800, 1080], "fallback": "JPEG"},
    "europe-card.jpg": {"widths": [400, 600, 800, 1080], "fallback": "JPEG"},
    # .card__media — 540px на десктопі, тобто 1080px на екрані 2x.
    "road-card.jpg": {"widths": [400, 600, 800, 1080], "fallback": "JPEG"},
    # Вантажний відсік зсередини. Ширше за 720 не робимо: у джерела саме
    # стільки, а домальовувати пікселі, яких немає, означає видати мило
    # за різкість.
    "cargo-card.jpg": {"widths": [400, 600, 720], "fallback": "JPEG"},
    # Фото буса з прозорим тлом — альфу треба зберегти.
    "busik.png": {"widths": [400, 600, 798], "fallback": "PNG"},
}

# AVIF дає найменший файл, WebP — сумісність із трохи старшими браузерами,
# оригінальний формат лишається як останній запасний варіант.
QUALITY = {"AVIF": 52, "WEBP": 76, "JPEG": 80, "PNG": None}
EXT = {"AVIF": "avif", "WEBP": "webp", "JPEG": "jpg", "PNG": "png"}


def newer(src, dst):
    """True, якщо dst треба (пере)генерувати."""
    if not os.path.exists(dst):
        return True
    return os.path.getmtime(src) > os.path.getmtime(dst)


def save(im, path, fmt):
    kwargs = {}
    q = QUALITY[fmt]
    if q is not None:
        kwargs["quality"] = q
    if fmt == "AVIF":
        kwargs["speed"] = 6
    elif fmt == "WEBP":
        kwargs["method"] = 5
    elif fmt == "JPEG":
        kwargs["progressive"] = True
        kwargs["optimize"] = True
        kwargs["subsampling"] = "4:2:0"
    elif fmt == "PNG":
        kwargs["optimize"] = True
    im.save(path, fmt, **kwargs)


def build(force=False):
    os.makedirs(OUT_DIR, exist_ok=True)
    total_src = 0
    total_best = 0
    made = 0
    manifest = {}

    for name, cfg in SOURCES.items():
        src = os.path.join(SRC_DIR, name)
        if not os.path.exists(src):
            print("  ПРОПУЩЕНО (немає файлу): %s" % name)
            continue

        stem = os.path.splitext(name)[0]
        original = Image.open(src)
        has_alpha = original.mode in ("RGBA", "LA") or (
            original.mode == "P" and "transparency" in original.info
        )
        base = original.convert("RGBA" if has_alpha else "RGB")

        src_kb = os.path.getsize(src) / 1024
        total_src += src_kb
        print("\n%s  (%dx%d, %.0f KB, alpha=%s)" % (
            name, base.width, base.height, src_kb, has_alpha))

        widths = [w for w in cfg["widths"] if w <= base.width]
        if base.width not in widths:
            widths.append(base.width)
        widths = sorted(set(widths))

        smallest_best = None
        fallback_fmt = cfg["fallback"]
        if has_alpha and fallback_fmt == "JPEG":
            fallback_fmt = "PNG"

        for w in widths:
            h = round(base.height * w / base.width)
            resized = base if w == base.width else base.resize(
                (w, h), Image.Resampling.LANCZOS)

            for fmt in ("AVIF", "WEBP", fallback_fmt):
                out = os.path.join(OUT_DIR, "%s-%d.%s" % (stem, w, EXT[fmt]))
                if force or newer(src, out):
                    frame = resized
                    if fmt == "JPEG" and frame.mode != "RGB":
                        frame = frame.convert("RGB")
                    if fmt == "PNG" and frame.mode == "RGBA":
                        # Без цього зменшений PNG важить БІЛЬШЕ за оригінал:
                        # джерело палітрове (P), а resize віддає 32-бітну RGBA.
                        frame = frame.quantize(
                            colors=256, method=Image.Quantize.FASTOCTREE)
                    save(frame, out, fmt)
                    made += 1
                kb = os.path.getsize(out) / 1024
                print("   %-5s %5dpx  %7.1f KB  %s" % (
                    fmt, w, kb, os.path.basename(out)))
                if w == widths[0] and fmt == "AVIF":
                    smallest_best = kb

        if smallest_best:
            total_best += smallest_best

        manifest[name] = {
            "stem": stem,
            "w": base.width,
            "h": base.height,
            "fallback": EXT[fallback_fmt],
            "widths": widths,
        }

    with open(os.path.join(OUT_DIR, "manifest.json"), "w") as fh:
        json.dump(manifest, fh, indent=2, ensure_ascii=False, sort_keys=True)
    print("\nМаніфест: static/images/derived/manifest.json (%d зображень)"
          % len(manifest))

    print("\n" + "=" * 60)
    print("Згенеровано/оновлено файлів: %d" % made)
    print("Оригінали разом:            %.0f KB" % total_src)
    print("Найменший AVIF-варіант:     %.0f KB  (те, що поїде на телефон)" % total_best)
    print("=" * 60)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--force", action="store_true")
    a = p.parse_args()
    build(force=a.force)
