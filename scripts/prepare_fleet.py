#!/usr/bin/env python3
"""
Готує фото автопарку до показу на сайті.

Знімки прийшли з різними полями: на одному бус займає весь кадр, на
іншому — третину, ще один взагалі вертикальний. У сітці карток це
виглядає так, ніби машини різного розміру. Тому кожне фото обрізаємо
по самому бусу (прозорий фон дає точну межу), додаємо однакове поле
і зводимо до спільного співвідношення 4:3.

    python3 scripts/prepare_fleet.py

Оригінали не чіпаються: результат — окремі файли fleet-N.png, які далі
підхоплює scripts/build_images.py.
"""

import os

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "static", "images")

# Поле навколо машини — щоб вона не впиралась у край картки.
PAD = 0.05
ASPECT = 4 / 3

SRC = [("crafter1.png", "fleet-1.png"),
       ("crafter2.png", "fleet-2.png"),
       ("crafter3.png", "fleet-3.png"),
       ("crafter4.png", "fleet-4.png")]


def prepare(src, dst):
    im = Image.open(os.path.join(IMG, src)).convert("RGBA")
    box = im.getchannel("A").getbbox()
    if box:
        im = im.crop(box)
    w, h = im.size
    pad = int(round(max(w, h) * PAD))
    w, h = w + pad * 2, h + pad * 2
    # Доводимо до 4:3, додаючи бракуюче з обох боків, а не розтягуючи.
    if w / h < ASPECT:
        w = int(round(h * ASPECT))
    else:
        h = int(round(w / ASPECT))
    canvas = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    canvas.paste(im, ((w - im.width) // 2, (h - im.height) // 2), im)
    out = os.path.join(IMG, dst)
    canvas.save(out, "PNG", optimize=True)
    print("%-16s -> %-14s %dx%d" % (src, dst, w, h))
    return canvas.size


if __name__ == "__main__":
    for a, b in SRC:
        prepare(a, b)
