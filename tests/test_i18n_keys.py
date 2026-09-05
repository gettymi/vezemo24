# -*- coding: utf-8 -*-
"""
Три мови — три словники Python. Жодної компіляції, жодних .po: рядків
кілька сотень, і звичайний dict правиться простіше за бінарний .mo.

Слабке місце такого підходу одне. Ключ, доданий в українську й забутий у
двох інших, НІЧОГО НЕ ЛАМАЄ: сторінка відкриється, просто на місці тексту
буде порожнеча або службова назва ключа. Помітити це можна лише відкривши
саме ту сторінку саме тією мовою — а сторінок 32 і мов три.

Тому набори ключів звіряються тут. Українська — джерело істини.
"""
import pathlib
import re
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from _project import module          # noqa: E402

UK = module("i18n/uk.py").STRINGS
RU = module("i18n/ru.py").STRINGS
EN = module("i18n/en.py").STRINGS

OTHERS = {"ru": RU, "en": EN}

# Підстановки в рядку: "{rate} ₴/км". Якщо в перекладі їх менше, значення
# просто не підставиться; якщо більше — format() впаде вже у відвідувача.
PLACEHOLDER = re.compile(r"\{(\w+)\}")


def placeholders(value):
    return set(PLACEHOLDER.findall(value)) if isinstance(value, str) else set()


class TestTranslations(unittest.TestCase):

    def test_key_sets_are_identical(self):
        for lang, strings in OTHERS.items():
            missing = sorted(set(UK) - set(strings))
            extra = sorted(set(strings) - set(UK))
            self.assertEqual(missing, [],
                             "у %s.py немає ключів: %s" % (lang, missing[:10]))
            self.assertEqual(extra, [],
                             "у %s.py зайві ключі, яких немає в uk.py: %s"
                             % (lang, extra[:10]))

    def test_no_empty_values(self):
        # Порожній рядок проходить перевірку ключів і все одно лишає
        # порожнє місце на сторінці.
        for lang, strings in {"uk": UK, "ru": RU, "en": EN}.items():
            blank = sorted(k for k, v in strings.items()
                           if isinstance(v, str) and not v.strip())
            self.assertEqual(blank, [],
                             "порожні значення в %s.py: %s" % (lang, blank[:10]))

    def test_placeholders_match(self):
        # Ціни ніде не набираються руками: у текст іде "{rate}", "{feed}",
        # "{open}", "{close}". Переклад, що загубив підстановку, покаже
        # фразу без числа — і ніхто цього не помітить, поки не подзвонить
        # клієнт із чужою ціною.
        for lang, strings in OTHERS.items():
            for key, uk_value in UK.items():
                want = placeholders(uk_value)
                got = placeholders(strings.get(key))
                self.assertEqual(
                    want, got,
                    "%s.py, ключ %r: підстановки %s замість %s"
                    % (lang, key, sorted(got) or "—", sorted(want) or "—"))

    def test_value_types_match(self):
        for lang, strings in OTHERS.items():
            for key, uk_value in UK.items():
                self.assertIs(
                    type(strings.get(key)), type(uk_value),
                    "%s.py, ключ %r: інший тип значення" % (lang, key))


if __name__ == "__main__":
    unittest.main(verbosity=2)
