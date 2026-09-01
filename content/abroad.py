# -*- coding: utf-8 -*-
"""
Закордонні напрямки.

Тут координати, зона тарифу й тексти — але НЕ відстані. Відстань рахує
OSRM за реальним маршрутом. Це навмисно: для внутрішніх напрямків
кілометраж перевірений і зашитий у content/routes.py, а для європейських
точних цифр у нас немає, і вигадати їх заради красивої таблиці означало б
назвати неправильну ціну.

Тому ані ці сторінки, ані сторінка-хаб не показують готової суми:
показують СТАВКУ, а суму рахує калькулятор.

ПРО ТЕКСТИ. Те саме правило, що й у content/places.py: кожен опис має
бути про цей напрямок. Якщо взяти Варшаву й замінити назву на Прагу,
Google визнає сторінки дублікатами й не покаже жодної.

Чого тут НЕ пишемо: скільки рейсів туди зробили, які терміни гарантуємо,
через який саме пункт пропуску їдемо. Нічого з цього ніхто не підтверджував.
"""

DESTINATIONS = [
    {
        "slug": "kyiv-warszawa",
        "city": "city.warszawa",
        "country": "country.pl",
        "zone": "east",
        "ll": [52.2297, 21.0122],
        "copy": {
            "uk": {
                "intro": "Варшава — найближча столиця Євросоюзу, і дорога туди майже "
                         "вся йде однією трасою через західний кордон. Тривалість рейсу "
                         "тут визначають не кілометри, а черга на пункті пропуску: саме "
                         "вона перетворює добу на півтори.",
                "work": "Переважно це особисті речі й переїзди до родичів, а поруч із "
                        "ними — невеликі партії товару, яким невигідно чекати на збірну "
                        "машину. Ваш вантаж їде окремим рейсом і ніде не перевантажується.",
                "note": "У центрі Варшави вузькі вулиці й платна парковка, тож час "
                        "розвантаження краще узгодити заздалегідь. Скажіть точну "
                        "адресу — подивимось, де реально стане бус, до того як виїдемо.",
            },
            "ru": {
                "intro": "Варшава — ближайшая столица Евросоюза, и дорога туда почти вся "
                         "идёт одной трассой через западную границу. Длительность рейса "
                         "здесь определяют не километры, а очередь на пункте пропуска: "
                         "именно она превращает сутки в полтора.",
                "work": "В основном это личные вещи и переезды к родственникам, а рядом "
                        "с ними — небольшие партии товара, которым невыгодно ждать "
                        "сборную машину. Ваш груз едет отдельным рейсом и нигде не "
                        "перегружается.",
                "note": "В центре Варшавы узкие улицы и платная парковка, поэтому время "
                        "разгрузки лучше согласовать заранее. Скажите точный адрес — "
                        "посмотрим, где реально станет бус, до того как выедем.",
            },
            "en": {
                "intro": "Warsaw is the nearest EU capital, and almost the whole drive "
                         "runs on one road to the western border. What decides the length "
                         "of the trip is not the kilometres but the queue at the "
                         "crossing: that is what turns a day into a day and a half.",
                "work": "Mostly personal belongings and moves to family, and alongside "
                        "them small consignments that cannot afford to wait for a "
                        "groupage load. Your cargo travels on its own run and is never "
                        "transferred at a depot.",
                "note": "Central Warsaw has narrow streets and paid parking, so the "
                        "unloading time is worth agreeing in advance. Send the exact "
                        "address and we will work out where the van can actually stand "
                        "before we set off.",
            },
        },
    },
    {
        "slug": "kyiv-krakow",
        "city": "city.krakow",
        "country": "country.pl",
        "zone": "east",
        "ll": [50.0647, 19.9450],
        "copy": {
            "uk": {
                "intro": "Краків лежить на південь від Варшави, і дорога туди йде через "
                         "ті самі західні пункти пропуску, але далі повертає на "
                         "південний захід. Львів опиняється майже на шляху, тож "
                         "проміжна адреса в Україні додає до маршруту небагато.",
                "work": "Напрямок звичний для тих, хто переїжджає надовго: меблі, "
                        "техніка, речі цілої родини. Разом із цим — зворотні рейси до "
                        "України, коли людина повертається й везе все назад.",
                "note": "Старе місто закрите для транспорту, і розвантаження "
                        "відбувається на межі зони. Це нормально й вирішується "
                        "заздалегідь, але про це треба знати до виїзду, а не на місці.",
            },
            "ru": {
                "intro": "Краков лежит южнее Варшавы, и дорога туда идёт через те же "
                         "западные пункты пропуска, но дальше поворачивает на юго-запад. "
                         "Львов оказывается почти по пути, поэтому промежуточный адрес в "
                         "Украине добавляет к маршруту немного.",
                "work": "Направление привычное для тех, кто переезжает надолго: мебель, "
                        "техника, вещи целой семьи. Вместе с этим — обратные рейсы в "
                        "Украину, когда человек возвращается и везёт всё назад.",
                "note": "Старый город закрыт для транспорта, и разгрузка происходит на "
                        "границе зоны. Это нормально и решается заранее, но знать об "
                        "этом надо до выезда, а не на месте.",
            },
            "en": {
                "intro": "Krakow lies south of Warsaw. The road runs through the same "
                         "western crossings and then turns south-west, which puts Lviv "
                         "almost on the way — an intermediate address in Ukraine adds "
                         "very little to the route.",
                "work": "This is the familiar direction for people moving for good: "
                        "furniture, appliances, a whole household. And with it the "
                        "return runs, when someone comes back to Ukraine and brings it "
                        "all home again.",
                "note": "The old town is closed to traffic and unloading happens at the "
                        "edge of the zone. That is normal and easily arranged, but it is "
                        "something to know before setting off rather than on arrival.",
            },
        },
    },
    {
        "slug": "kyiv-praha",
        "city": "city.praha",
        "country": "country.cz",
        "zone": "east",
        "ll": [50.0755, 14.4378],
        "copy": {
            "uk": {
                "intro": "До Праги їдуть через усю Польщу, і це вже не одна ніч за "
                         "кермом, а два дні з обов'язковим відпочинком водія. Ми плануємо "
                         "рейс саме так — з відпочинком, а не «як вийде»: інакше це "
                         "питання безпеки, а не швидкості.",
                "work": "Здебільшого сімейні переїзди: меблі, побутова техніка, речі, "
                        "які не відправиш поштою. Ціна рахується за повний пробіг, тому "
                        "далекі напрямки виходять розумнішими, коли машина завантажена "
                        "нормально, а не наполовину.",
                "note": "Чеські платні дороги оплачуються віньєткою — вона вже в ставці "
                        "й окремо не додається, як і пальне з дозволами на всьому "
                        "маршруті.",
            },
            "ru": {
                "intro": "В Прагу едут через всю Польшу, и это уже не одна ночь за рулём, "
                         "а два дня с обязательным отдыхом водителя. Мы планируем рейс "
                         "именно так — с отдыхом, а не «как получится»: иначе это вопрос "
                         "безопасности, а не скорости.",
                "work": "В основном семейные переезды: мебель, бытовая техника, вещи, "
                        "которые не отправишь почтой. Цена считается за полный пробег, "
                        "поэтому дальние направления выходят разумнее, когда машина "
                        "загружена нормально, а не наполовину.",
                "note": "Чешские платные дороги оплачиваются виньеткой — она уже в ставке "
                        "и отдельно не добавляется, как и топливо с разрешениями на всём "
                        "маршруте.",
            },
            "en": {
                "intro": "Prague means crossing the whole of Poland: not one night at the "
                         "wheel but two days with a mandatory rest for the driver. We "
                         "plan the run that way on purpose — with the rest, not as it "
                         "comes out — because this is a safety question, not a speed one.",
                "work": "Mostly family moves: furniture, appliances, the things you "
                        "cannot put in the post. The price is calculated over the full "
                        "mileage, so long directions make more sense when the van goes "
                        "out properly loaded rather than half full.",
                "note": "Czech toll roads are paid by vignette. It is already in the rate "
                        "and never added afterwards, along with the fuel and the permits "
                        "for the whole route.",
            },
        },
    },
    {
        "slug": "kyiv-bratislava",
        "city": "city.bratislava",
        "country": "country.sk",
        "zone": "east",
        "ll": [48.1486, 17.1077],
        "copy": {
            "uk": {
                "intro": "Братислава ближча за Прагу, і дорога туди йде через Польщу або "
                         "Угорщину — вибір залежить від ситуації на кордонах у конкретний "
                         "день. Від Братислави до Відня менш як година, тож для "
                         "розрахунку це майже той самий рейс.",
                "work": "Словаччина рідше буває кінцевою точкою й частіше проміжною: сюди "
                        "везуть речі при переїзді й забирають назад до України. Через це "
                        "напрямок часто виходить завантаженим в обидва боки, а такий рейс "
                        "рахується інакше.",
                "note": "Якщо у вас є що відправити назад до Києва — скажіть одразу. "
                        "Порожній зворотний пробіг закладений у ставку, і коли машина йде "
                        "з вантажем в обидва боки, це видно в остаточній ціні.",
            },
            "ru": {
                "intro": "Братислава ближе Праги, и дорога туда идёт через Польшу или "
                         "Венгрию — выбор зависит от ситуации на границах в конкретный "
                         "день. От Братиславы до Вены меньше часа, поэтому для расчёта "
                         "это почти тот же рейс.",
                "work": "Словакия реже бывает конечной точкой и чаще промежуточной: сюда "
                        "везут вещи при переезде и забирают обратно в Украину. Из-за "
                        "этого направление часто выходит загруженным в обе стороны, а "
                        "такой рейс считается иначе.",
                "note": "Если у вас есть что отправить назад в Киев — скажите сразу. "
                        "Пустой обратный пробег заложен в ставку, и когда машина идёт с "
                        "грузом в обе стороны, это видно в окончательной цене.",
            },
            "en": {
                "intro": "Bratislava is closer than Prague, and the road there runs "
                         "through Poland or Hungary depending on how the borders look on "
                         "the day. Vienna is under an hour away, so for the purposes of a "
                         "quote it is nearly the same run.",
                "work": "Slovakia is less often the final stop and more often a point "
                        "along the way: things go out with a move and come back to "
                        "Ukraine later. That makes this direction one that is frequently "
                        "loaded both ways, and a run like that is priced differently.",
                "note": "If you have something to send back to Kyiv, say so at the start. "
                        "The empty return leg is built into the rate, and when the van "
                        "runs loaded in both directions it shows in the final price.",
            },
        },
    },
    {
        "slug": "kyiv-berlin",
        "city": "city.berlin",
        "country": "country.de",
        "zone": "west",
        "ll": [52.5200, 13.4050],
        "copy": {
            "uk": {
                "intro": "Берлін — уже західна зона, і ставка за кілометр тут вища. "
                         "Причина проста й перевіряється: далі на захід дорожче пальне й "
                         "більше платних автобанів. Ми показуємо це в тарифі відкрито, а "
                         "не дописуємо після рейсу.",
                "work": "Сюди частіше їдуть комерційні вантажі й великі переїзди, ніж "
                        "кілька коробок: на такій відстані має сенс везти багато за раз. "
                        "Вантажників у нас немає, тому завантаження й розвантаження — на "
                        "вашому боці з обох кінців.",
                "note": "У центрах німецьких міст діють зони з обмеженням викидів, і "
                        "в'їзд туди дозволений не всім. Скажіть точну адресу "
                        "розвантаження — перевіримо, чи потрапляє вона в таку зону, до "
                        "того як домовлятися про рейс.",
            },
            "ru": {
                "intro": "Берлин — уже западная зона, и ставка за километр здесь выше. "
                         "Причина простая и проверяемая: дальше на запад дороже топливо и "
                         "больше платных автобанов. Мы показываем это в тарифе открыто, а "
                         "не дописываем после рейса.",
                "work": "Сюда чаще едут коммерческие грузы и большие переезды, чем "
                        "несколько коробок: на таком расстоянии имеет смысл везти много "
                        "за раз. Грузчиков у нас нет, поэтому загрузка и разгрузка — на "
                        "вашей стороне с обоих концов.",
                "note": "В центрах немецких городов действуют зоны с ограничением "
                        "выбросов, и въезд туда разрешён не всем. Скажите точный адрес "
                        "разгрузки — проверим, попадает ли он в такую зону, до того как "
                        "договариваться о рейсе.",
            },
            "en": {
                "intro": "Berlin is already the western zone, where the rate per "
                         "kilometre is higher. The reason is simple and checkable: fuel "
                         "costs more the further west you go and there are more toll "
                         "motorways. We put that in the tariff openly rather than adding "
                         "it after the run.",
                "work": "This direction sees commercial freight and large moves more often "
                        "than a few boxes — at this distance it makes sense to carry a lot "
                        "at once. We bring no loaders, so loading and unloading are your "
                        "side of the job at both ends.",
                "note": "German city centres have low-emission zones and not every vehicle "
                        "may enter them. Give us the exact unloading address and we will "
                        "check whether it falls inside one before anything is agreed.",
            },
        },
    },
]

BY_SLUG = {d["slug"]: d for d in DESTINATIONS}


def neighbours(slug, limit=3):
    """
    Інші напрямки для перелінковки.

    Список прокручується від поточного, а не береться з початку файлу —
    та сама причина, що й у content/places.py: інакше перші напрямки
    збирають усі посилання, а останній не отримує жодного, і Google
    дивиться на нього як на сторінку, до якої нікому немає діла.

    Один слот завжди лишається «чужій» зоні/стороні, якщо вона є. Без цього
    напрямок, який єдиний у своїй зоні, не отримує ЖОДНОГО вхідного
    посилання: у решти той самий бік заповнює всі три місця, і сторінка
    залишається сиротою. Саме так загубився Берлін — єдиний у західній
    зоні, — і раніше Вишгород на півночі.
    """
    current = BY_SLUG.get(slug)
    if not current:
        return []
    i = DESTINATIONS.index(current)
    rotated = DESTINATIONS[i + 1:] + DESTINATIONS[:i]
    same = [d for d in rotated if d["zone"] == current["zone"]]
    other = [d for d in rotated if d["zone"] != current["zone"]]
    if other and len(same) >= limit:
        return same[:limit - 1] + other[:1]
    return (same + other)[:limit]
