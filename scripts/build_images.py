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
    # .split__media — приблизно 560px на десктопі, на всю ширину на мобільному.
    "road-wide.jpg": {"widths": [480, 720, 1040], "fallback": "JPEG"},
    # .card__media у сітці з трьох колонок — максимум ~400px.
    "road-card.jpg": {"widths": [400, 600, 800], "fallback": "JPEG"},
    # Фото буса з прозорим тлом — альфу треба зберегти.
    "busik.png": {"widths": [400, 600, 798], "fallback": "PNG"},
    # Автопарк. Джерела готує scripts/prepare_fleet.py: він обрізає кожне
    # фото по самій машині й зводить усі до 4:3, інакше в сітці карток
    # буси виглядають різного розміру. Ширші за оригінал варіанти скрипт
    # не робить сам, тому fleet-3 (менше фото) лишиться меншим — це
    # чесніше, ніж домальовувати пікселі, яких у знімку немає.
    "fleet-1.png": {"widths": [400, 600, 800], "fallback": "PNG"},
    "fleet-2.png": {"widths": [400, 600, 800], "fallback": "PNG"},
    "fleet-3.png": {"widths": [400, 600, 800], "fallback": "PNG"},
    "fleet-4.png": {"widths": [400, 600, 800], "fallback": "PNG"},
    # Вантажний відсік зсередини — звичайне фото без прозорості.
    "zad.png": {"widths": [480, 720, 960], "fallback": "JPEG"},
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
