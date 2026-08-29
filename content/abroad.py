# -*- coding: utf-8 -*-
"""
Закордонні напрямки.

Тут лише координати й зона тарифу — відстань РАХУЄ OSRM, а не ми.
Це навмисно: для внутрішніх маршрутів кілометраж перевірений і зашитий
у content/routes.py, а для європейських точних цифр у нас немає, і
вигадувати їх заради красивої таблиці означало б назвати неправильну ціну.

Тому сторінка закордону показує СТАВКУ, а конкретну суму рахує
калькулятор за реальним маршрутом.
"""

DESTINATIONS = [
    {"slug": "kyiv-warszawa",   "city": "city.warszawa",   "country": "country.pl",
     "zone": "east", "ll": [52.2297, 21.0122]},
    {"slug": "kyiv-krakow",     "city": "city.krakow",     "country": "country.pl",
     "zone": "east", "ll": [50.0647, 19.9450]},
    {"slug": "kyiv-praha",      "city": "city.praha",      "country": "country.cz",
     "zone": "east", "ll": [50.0755, 14.4378]},
    {"slug": "kyiv-bratislava", "city": "city.bratislava", "country": "country.sk",
     "zone": "east", "ll": [48.1486, 17.1077]},
    {"slug": "kyiv-berlin",     "city": "city.berlin",     "country": "country.de",
     "zone": "west", "ll": [52.5200, 13.4050]},
]

BY_SLUG = {d["slug"]: d for d in DESTINATIONS}
