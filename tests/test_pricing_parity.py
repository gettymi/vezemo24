# -*- coding: utf-8 -*-
"""
Ціни живуть у двох місцях: `content/pricing.py` на сервері й
`static/js/priceCalculator.js` у браузері. Дублювання свідоме — калькулятор
рахує без звернення до сервера, тому цифра зʼявляється миттєво, без
затримки й без ще одного способу зламатися.

Платня за це рішення — ризик, що два числа розійдуться. Тоді сторінка
напрямку назве одну ціну, калькулятор іншу, і НІЩО НЕ ВИГЛЯДАТИМЕ
ЗЛАМАНИМ: обидві сторінки відкриються, обидві покажуть цифру. Помилку
знайде клієнт, у розмові, коли платити доведеться більше, ніж він
прочитав.

Цей файл — і є та платня, внесена один раз.
"""
import pathlib
import re
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from _project import module, text          # noqa: E402

P = module("content/pricing.py")
JS = text("static/js/priceCalculator.js")


def js_number(pattern):
    """Дістати число з JS за виразом. Немає — це вже помилка."""
    m = re.search(pattern, JS)
    if m is None:
        raise AssertionError(
            "у priceCalculator.js не знайдено %r — константу перейменували "
            "або прибрали, і тест більше нічого не звіряє" % pattern
        )
    return float(m.group(1))


def js_zone_cc(zone):
    """Список кодів країн однієї зони з ZONE_CC у JS."""
    block = re.search(r"var ZONE_CC = \{(.*?)\};", JS, re.S)
    assert block, "у priceCalculator.js не знайдено ZONE_CC"
    arr = re.search(r"%s:\s*\[(.*?)\]" % zone, block.group(1), re.S)
    assert arr, "у ZONE_CC немає зони %r" % zone
    return re.findall(r'"([a-z]{2})"', arr.group(1))


class TestPricingParity(unittest.TestCase):

    def test_local_hourly(self):
        self.assertEqual(P.LOCAL_HOURLY, js_number(r"hourly:\s*([\d.]+)"))

    def test_local_feed(self):
        self.assertEqual(P.LOCAL_FEED, js_number(r"feed:\s*([\d.]+)"))

    def test_local_min_hours(self):
        self.assertEqual(P.LOCAL_MIN_HOURS, js_number(r"minHours:\s*([\d.]+)"))

    def test_intercity_per_km(self):
        self.assertEqual(P.INTERCITY_PER_KM, js_number(r"perKm:\s*([\d.]+)"))

    def test_return_share(self):
        self.assertEqual(P.RETURN_SHARE,
                         js_number(r"RETURN_SHARE\s*=\s*([\d.]+)"))

    def test_intercity_boundary(self):
        # 120 км — межа, за якою погодинний тариф перемикається на
        # покілометровий. Розійдеться — і той самий рейс порахується
        # двома різними способами залежно від того, хто рахує.
        self.assertEqual(P.INTERCITY_FROM_KM,
                         js_number(r"INTERCITY_FROM_KM\s*=\s*([\d.]+)"))

    def test_home_country(self):
        m = re.search(r'HOME_CC\s*=\s*"([a-z]{2})"', JS)
        self.assertIsNotNone(m, "у JS немає HOME_CC")
        self.assertEqual(P.HOME_CC, m.group(1))

    def test_abroad_rates(self):
        block = re.search(r"var ABROAD = \{(.*?)\};", JS, re.S)
        self.assertIsNotNone(block, "у JS немає ABROAD")
        for zone, data in P.ABROAD_ZONES.items():
            m = re.search(r"%s:\s*\{\s*perTotalKm:\s*([\d.]+)" % zone,
                          block.group(1))
            self.assertIsNotNone(m, "у JS немає зони %r" % zone)
            self.assertEqual(data["per_total_km"], float(m.group(1)),
                             "ставка зони %r розійшлася" % zone)

    def test_abroad_country_codes(self):
        # За цими кодами калькулятор визначає зону з адреси, яку людина
        # ввела сама. Країна, яка є лише в одному списку, або порахується
        # не за тим тарифом, або не порахується взагалі.
        for zone, data in P.ABROAD_ZONES.items():
            self.assertEqual(sorted(data["cc"]), sorted(js_zone_cc(zone)),
                             "коди країн зони %r розійшлися" % zone)

    def test_zones_do_not_overlap(self):
        east = set(P.ABROAD_ZONES["east"]["cc"])
        west = set(P.ABROAD_ZONES["west"]["cc"])
        self.assertEqual(east & west, set(),
                         "країна у двох зонах одразу: тариф залежатиме від "
                         "порядку перебору, тобто буде випадковим")

    def test_home_country_is_not_abroad(self):
        for zone, data in P.ABROAD_ZONES.items():
            self.assertNotIn(P.HOME_CC, data["cc"],
                             "Україна потрапила в закордонну зону %r" % zone)


if __name__ == "__main__":
    unittest.main(verbosity=2)
