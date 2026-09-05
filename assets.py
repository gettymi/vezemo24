"""
Статика: хешовані URL + адаптивні <picture>.

Дві задачі:

1. static_url() додає до адреси відбиток вмісту файлу (?v=1a2b3c4d).
   Завдяки цьому Cloudflare і браузер можуть кешувати CSS/JS/зображення
   агресивно й надовго, але одразу бачать новий файл після деплою —
   без ручного скидання кешу і без «чому в клієнта стара верстка».

2. picture() будує <picture> з AVIF / WebP / оригінальним форматом і
   srcset за даними static/images/derived/manifest.json, який пише
   scripts/build_images.py.

   Якщо маніфесту немає (репозиторій щойно клонували й білд не запускали),
   picture() повертає звичайний <img> з оригіналом. Сайт лишається робочим,
   просто без економії трафіку — це навмисно, щоб забутий білд-крок
   не ламав сторінку.
"""

import hashlib
import json
import os

from flask import url_for
from markupsafe import Markup, escape

MANIFEST_REL = "images/derived/manifest.json"

# Порядок важливий: перший формат, який браузер розуміє, той і виграє.
_SOURCE_TYPES = [("avif", "image/avif"), ("webp", "image/webp")]


class Assets:
    def __init__(self, app=None):
        self.app = app
        self._fingerprints = {}   # filename -> (mtime, size, hash)
        self._manifest = None
        self._manifest_mtime = None
        if app is not None:
            self.init_app(app)

    # ── службове ────────────────────────────────────────────────────────────
    def _path(self, filename):
        return os.path.join(self.app.static_folder, filename.replace("/", os.sep))

    def _stat(self, filename):
        try:
            st = os.stat(self._path(filename))
            return st.st_mtime, st.st_size
        except OSError:
            return None

    # ── 1. хешовані URL ─────────────────────────────────────────────────────
    def fingerprint(self, filename):
        """Перші 8 символів sha256 вмісту або None, якщо файлу немає."""
        st = self._stat(filename)
        if st is None:
            return None
        cached = self._fingerprints.get(filename)
        if cached and cached[0] == st[0] and cached[1] == st[1]:
            return cached[2]
        h = hashlib.sha256()
        with open(self._path(filename), "rb") as fh:
            for chunk in iter(lambda: fh.read(131072), b""):
                h.update(chunk)
        digest = h.hexdigest()[:8]
        self._fingerprints[filename] = (st[0], st[1], digest)
        return digest

    def static_url(self, filename):
        url = url_for("static", filename=filename)
        fp = self.fingerprint(filename)
        return "%s?v=%s" % (url, fp) if fp else url

    def has_static(self, filename):
        return self._stat(filename) is not None

    # ── 2. адаптивні зображення ─────────────────────────────────────────────
    def manifest(self):
        st = self._stat(MANIFEST_REL)
        if st is None:
            return {}
        if self._manifest is None or self._manifest_mtime != st[0]:
            try:
                with open(self._path(MANIFEST_REL), encoding="utf-8") as fh:
                    self._manifest = json.load(fh)
            except (OSError, ValueError):
                self._manifest = {}
            self._manifest_mtime = st[0]
        return self._manifest

    def _srcset(self, stem, ext, widths):
        return ", ".join(
            "%s %dw" % (self.static_url("images/derived/%s-%d.%s" % (stem, w, ext)), w)
            for w in widths
        )

    def picture(
        self,
        name,
        alt="",
        sizes="100vw",
        loading="lazy",
        fetchpriority=None,
        img_class=None,
        picture_class=None,
        decoding="async",
    ):
        """
        <picture> з AVIF/WebP/запасним форматом.

        name — імʼя вихідного файлу в static/images (напр. "road-card.jpg").
        sizes — скільки місця зображення реально займе; від цього браузер
                обирає варіант, тож неправильний sizes зводить нанівець
                усю економію.
        """
        entry = self.manifest().get(name)
        img_attrs = []
        if img_class:
            img_attrs.append('class="%s"' % escape(img_class))

        if not entry:
            # Немає маніфесту — віддаємо оригінал, сторінка не ламається.
            img_attrs += [
                'src="%s"' % escape(self.static_url("images/" + name)),
                'alt="%s"' % escape(alt),
                'loading="%s"' % escape(loading),
                'decoding="%s"' % escape(decoding),
            ]
            if fetchpriority:
                img_attrs.append('fetchpriority="%s"' % escape(fetchpriority))
            return Markup("<img %s>" % " ".join(img_attrs))

        stem, widths = entry["stem"], entry["widths"]
        fallback_ext = entry["fallback"]

        sources = []
        for ext, mime in _SOURCE_TYPES:
            sources.append(
                '<source type="%s" srcset="%s" sizes="%s">'
                % (mime, escape(self._srcset(stem, ext, widths)), escape(sizes))
            )

        # src потрібен лише браузерам, які ігнорують srcset; беремо середній
        # варіант, щоб такому браузеру не поїхало найбільше зображення.
        default_w = min(widths, key=lambda w: abs(w - 800))
        img_attrs += [
            'src="%s"' % escape(
                self.static_url("images/derived/%s-%d.%s" % (stem, default_w, fallback_ext))),
            'srcset="%s"' % escape(self._srcset(stem, fallback_ext, widths)),
            'sizes="%s"' % escape(sizes),
            'width="%d"' % entry["w"],
            'height="%d"' % entry["h"],
            'alt="%s"' % escape(alt),
            'loading="%s"' % escape(loading),
            'decoding="%s"' % escape(decoding),
        ]
        if fetchpriority:
            img_attrs.append('fetchpriority="%s"' % escape(fetchpriority))

        cls = ' class="%s"' % escape(picture_class) if picture_class else ""
        return Markup(
            "<picture%s>%s<img %s></picture>" % (cls, "".join(sources), " ".join(img_attrs))
        )

    def preload_image(self, name, sizes="100vw", ext="avif"):
        """
        <link rel=preload> для головного зображення екрана (LCP).

        Браузер інакше знайде його лише після розбору CSS, бо це фон героя.
        type= гарантує, що браузери без AVIF просто проігнорують підказку
        і не викачають зайвого.
        """
        entry = self.manifest().get(name)
        if not entry:
            return Markup("")
        return Markup(
            '<link rel="preload" as="image" type="image/%s" href="%s" '
            'imagesrcset="%s" imagesizes="%s" fetchpriority="high">'
            % (
                escape(ext),
                escape(self.static_url(
                    "images/derived/%s-%d.%s"
                    % (entry["stem"], entry["widths"][0], ext))),
                escape(self._srcset(entry["stem"], ext, entry["widths"])),
                escape(sizes),
            )
        )

    # ── реєстрація ──────────────────────────────────────────────────────────
    def init_app(self, app):
        self.app = app
        app.jinja_env.globals["static_url"] = self.static_url
        app.jinja_env.globals["has_static"] = self.has_static
        app.jinja_env.globals["picture"] = self.picture
        app.jinja_env.globals["preload_image"] = self.preload_image


assets = Assets()
