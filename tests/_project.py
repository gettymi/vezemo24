# -*- coding: utf-8 -*-
"""
Спільний завантажувач для перевірок.

Модулі беруться ПРЯМО З ФАЙЛУ, а не через `import content.places`. Причина
проста: звичайний імпорт зачепив би `i18n/__init__.py`, а той тягне Flask.
Ці перевірки — про дані, а не про вебзастосунок, і мають запускатися
голим `python3` без жодного встановленого пакета. Перевірка, яку не можна
запустити однією командою, не запускається ніколи, а отже не існує.
"""
import importlib.util
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent


def module(relpath):
    """Завантажити модуль проєкту з файлу, не чіпаючи пакети."""
    path = ROOT / relpath
    name = "vz_" + path.stem
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def text(relpath):
    """Прочитати файл проєкту як текст."""
    return (ROOT / relpath).read_text(encoding="utf-8")
