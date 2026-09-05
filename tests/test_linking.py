# -*- coding: utf-8 -*-
"""
Перелінковка між сторінками міст і напрямків.

Сторінка, на яку не веде жодне внутрішнє посилання, — сирота. Вона є в
sitemap.xml, вона відкривається за прямою адресою, і саме тому помилку
неможливо побачити очима: сайт виглядає цілим. Але для Google сторінка,
до якої не веде ніхто зі свого ж сайту, не варта уваги, і в пошук вона
або не потрапить узагалі, або потрапить останньою.

Ця вада траплялася ДВІЧІ й обидва рази з тієї самої причини: `neighbours()`
віддавав усі три слоти сторінкам своєї ж зони, тож напрямок, єдиний у
своїй зоні, не отримував нічого. Спершу так загубився Вишгород — єдиний на
півночі. Виправили в `places.py`, а через тиждень той самий рядок
повторили в `abroad.py`, і так само загубився Берлін — єдиний у західній
зоні.

Тому перевіряються обидва файли, тим самим набором умов.
"""
import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from _project import module          # noqa: E402

PLACES = module("content/places.py")
ABROAD = module("content/abroad.py")

# (назва для повідомлення, модуль, список записів, поле зони)
SETS = [
    ("міста області", PLACES, PLACES.PLACES, "side"),
    ("закордонні напрямки", ABROAD, ABROAD.DESTINATIONS, "zone"),
]


class TestInternalLinking(unittest.TestCase):

    def test_no_orphan_pages(self):
        for name, mod, items, _field in SETS:
            inbound = {i["slug"]: 0 for i in items}
            for item in items:
                for neighbour in mod.neighbours(item["slug"]):
                    inbound[neighbour["slug"]] += 1
            orphans = sorted(s for s, n in inbound.items() if n == 0)
            self.assertEqual(
                orphans, [],
                "%s: на ці сторінки не веде жодне посилання: %s"
                % (name, orphans))

    def test_page_does_not_link_to_itself(self):
        for name, mod, items, _field in SETS:
            for item in items:
                slugs = [n["slug"] for n in mod.neighbours(item["slug"])]
                self.assertNotIn(item["slug"], slugs,
                                 "%s: %s посилається сама на себе"
                                 % (name, item["slug"]))

    def test_block_is_always_full(self):
        # Блок «сусідні напрямки» розрахований на три картки. Дві замість
        # трьох — це діра в макеті, яку помітно лише на одній сторінці.
        for name, mod, items, _field in SETS:
            want = min(3, len(items) - 1)
            for item in items:
                self.assertEqual(
                    len(mod.neighbours(item["slug"])), want,
                    "%s: у %s не %d сусідів" % (name, item["slug"], want))

    def test_no_duplicates_in_block(self):
        for name, mod, items, _field in SETS:
            for item in items:
                slugs = [n["slug"] for n in mod.neighbours(item["slug"])]
                self.assertEqual(len(slugs), len(set(slugs)),
                                 "%s: %s посилається двічі на те саме"
                                 % (name, item["slug"]))

    def test_lonely_zone_still_gets_a_link(self):
        # Суть виправлення: якщо запис єдиний у своїй зоні, посилання на
        # нього можуть дати ЛИШЕ сторінки з інших зон. Саме цей випадок
        # ламався обидва рази.
        for name, mod, items, field in SETS:
            for item in items:
                alone = [i for i in items if i[field] == item[field]]
                if len(alone) > 1:
                    continue
                linkers = [o["slug"] for o in items
                           if item["slug"] in
                           [n["slug"] for n in mod.neighbours(o["slug"])]]
                self.assertNotEqual(
                    linkers, [],
                    "%s: %s — єдиний у зоні %r і лишився без посилань"
                    % (name, item["slug"], item[field]))

    def test_slugs_are_unique(self):
        for name, _mod, items, _field in SETS:
            slugs = [i["slug"] for i in items]
            self.assertEqual(len(slugs), len(set(slugs)),
                             "%s: однакові slug — одна сторінка перекриє іншу"
                             % name)

    def test_unknown_slug_returns_nothing(self):
        # Шаблон викликає neighbours() з тим, що прийшло з адреси.
        for name, mod, _items, _field in SETS:
            self.assertEqual(mod.neighbours("no-such-page"), [], name)


if __name__ == "__main__":
    unittest.main(verbosity=2)
