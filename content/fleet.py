"""
Автопарк.

Що тут можна писати, а що ні. Про кожну машину описуємо ЛИШЕ те, що
видно на фото й підтвердив власник: модель, колір, тип кузова. Рік,
вантажопідйомність, обʼєм і габарити відсіку тут свідомо відсутні —
поки їх ніхто не назвав, а вигадана цифра в оголошенні коштує довіри
дорожче, ніж порожнє місце.

Коли зʼявляться заміри — додати їх у `specs` і показати в картці.
"""

VEHICLES = [
    {
        "id": "v1",
        "image": "fleet-1.png",
        "name": "Volkswagen Crafter",
        "color": "fleet.color.white",
        "body": "fleet.body.panel",
        "note": "fleet.v1.note",
        "on_home": True,
        "specs": [],
    },
    {
        "id": "v2",
        "image": "fleet-2.png",
        "name": "Volkswagen Crafter",
        "color": "fleet.color.black",
        "body": "fleet.body.panel",
        "note": "fleet.v2.note",
        "on_home": True,
        "specs": [],
    },
    {
        "id": "v3",
        "image": "fleet-3.png",
        "name": "Volkswagen Crafter",
        "color": "fleet.color.grey",
        "body": "fleet.body.high",
        "note": "fleet.v3.note",
        "on_home": False,
        "specs": [],
    },
    {
        "id": "v4",
        "image": "fleet-4.png",
        "name": "Volkswagen Crafter",
        "color": "fleet.color.black",
        "body": "fleet.body.long",
        "note": "fleet.v4.note",
        "on_home": True,
        "specs": [],
    },
]

# Фото вантажного відсіку зсередини — окремо: воно відповідає на питання
# «а моє туди влізе?» краще, ніж будь-який опис зовні.
INTERIOR = {"image": "zad.png", "alt": "fleet.interior.alt"}


def home_vehicles():
    """Три машини для головної. Четверта живе на сторінці автопарку."""
    return [v for v in VEHICLES if v["on_home"]]
