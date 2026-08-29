# -*- coding: utf-8 -*-
"""
Сторінки напрямків — по одній на маршрут із Києва.

Навіщо окремі сторінки: людина шукає не «вантажні перевезення», а
«перевезення Київ Львів». Одна загальна сторінка про міжміські рейси на
такий запит не відповідає, а сторінка саме про цей маршрут — відповідає.
Конкуренти мають 40+ сторінок, ми мали 5.

Увесь текст маршруту лежить ТУТ, а не в i18n/*.py. Так додати новий
напрямок — це правка одного файлу, а не чотирьох. У каталогах лишаються
тільки підписи інтерфейсу, спільні для всіх маршрутів.

Щоб додати напрямок: скопіюйте будь-який запис, змініть дані й напишіть
власний текст трьома мовами. Порожній `copy` для якоїсь мови — сторінка
все одно збереться, просто без описової частини.

ВАЖЛИВО: тексти мають бути різні. Якщо скопіювати опис Львова й
замінити назву міста, Google побачить дублікати й не покаже жодної
сторінки — це гірше, ніж не мати їх узагалі.
"""

ROUTES = [
    {
        "slug": "kyiv-lviv",
        "city": "city.lviv",
        "km": 540,
        "hours": "7–9",
        "via": ["city.zhytomyr", "city.rivne"],
        "copy": {
            "uk": {
                "intro": "Один із найзавантаженіших напрямків із Києва. Траса М06 через "
                         "Житомир і Рівне — дорога рівна, тож 540 км ми проходимо за "
                         "звичайний робочий день без нічної їзди.",
                "cargo": "Найчастіше це товар для львівських магазинів і кафе, меблі та "
                         "техніка при переїзді, обладнання для офісів. Львів давно "
                         "приймає компанії, що переїжджають із інших міст, тож офісні "
                         "переїзди в цьому напрямку — регулярна історія.",
                "note": "Виїзд зазвичай зранку, вивантаження — того ж дня ввечері або "
                        "наступного ранку, як вам зручніше.",
            },
            "ru": {
                "intro": "Одно из самых загруженных направлений из Киева. Трасса М06 через "
                         "Житомир и Ровно — дорога ровная, поэтому 540 км проходим за "
                         "обычный рабочий день, без ночной езды.",
                "cargo": "Чаще всего это товар для львовских магазинов и кафе, мебель и "
                         "техника при переезде, оборудование для офисов. Львов давно "
                         "принимает компании, переезжающие из других городов, поэтому "
                         "офисные переезды в этом направлении — регулярная история.",
                "note": "Выезд обычно утром, выгрузка — в тот же день вечером или на "
                        "следующее утро, как вам удобнее.",
            },
            "en": {
                "intro": "One of the busiest routes out of Kyiv. The M06 runs through "
                         "Zhytomyr and Rivne and the road is in good shape, so we cover "
                         "the 540 km within a normal working day — no night driving.",
                "cargo": "Usually stock for shops and cafes in Lviv, furniture and "
                         "appliances for people relocating, and office equipment. Lviv has "
                         "taken in a lot of companies moving from elsewhere, so office "
                         "relocations in this direction come up regularly.",
                "note": "We normally set off in the morning and unload the same evening or "
                        "the next morning, whichever suits you.",
            },
        },
    },
    {
        "slug": "kyiv-odesa",
        "city": "city.odesa",
        "km": 475,
        "hours": "6–8",
        "via": ["city.vinnytsia"],
        "copy": {
            "uk": {
                "intro": "Траса М05 через Умань — найшвидший із довгих напрямків: 475 км "
                         "здебільшого доброю дорогою, без гірських ділянок і об'їздів.",
                "cargo": "Одеса — порт і торгівля, тому звідси й сюди часто їде товар для "
                         "рітейлу, обладнання для закладів, виставкові конструкції. Влітку "
                         "додається сезонне: меблі й техніка для оренди, обладнання для "
                         "літніх майданчиків.",
                "note": "Влітку на цьому напрямку варто бронювати дату заздалегідь — "
                        "бажаючих більше, ніж машин.",
            },
            "ru": {
                "intro": "Трасса М05 через Умань — самое быстрое из длинных направлений: "
                         "475 км в основном хорошей дорогой, без горных участков и объездов.",
                "cargo": "Одесса — порт и торговля, поэтому отсюда и сюда часто едет товар "
                         "для ритейла, оборудование для заведений, выставочные конструкции. "
                         "Летом добавляется сезонное: мебель и техника для аренды, "
                         "оборудование для летних площадок.",
                "note": "Летом на этом направлении дату стоит бронировать заранее — "
                        "желающих больше, чем машин.",
            },
            "en": {
                "intro": "The M05 through Uman is the quickest of the long routes: 475 km "
                         "on mostly good road, with no mountain sections or detours.",
                "cargo": "Odesa is a port and a trading city, so retail stock, equipment for "
                         "bars and restaurants, and exhibition fittings move in both "
                         "directions. Summer adds seasonal work — furniture and appliances "
                         "for rentals, and kit for open-air venues.",
                "note": "In summer it is worth booking a date in advance on this route — "
                        "demand outstrips the vans available.",
            },
        },
    },
    {
        "slug": "kyiv-dnipro",
        "city": "city.dnipro",
        "km": 480,
        "hours": "6–8",
        "via": ["city.poltava"],
        "copy": {
            "uk": {
                "intro": "Дорога М03 через Полтаву й Кременчук. 480 км, які проходяться "
                         "рівно — без вузьких ділянок, де доводиться повзти з вантажем.",
                "cargo": "Дніпро — промислове місто, тож тут переважає не побут, а робота: "
                         "обладнання, запчастини, комплектуючі, товар на склади. Часто "
                         "просять забрати з кількох адрес у Києві й привезти на одну.",
                "note": "Кілька точок завантаження на цьому напрямку — звична річ, "
                        "додайте їх у калькуляторі, і ціна перерахується.",
            },
            "ru": {
                "intro": "Дорога М03 через Полтаву и Кременчуг. 480 км, которые проходятся "
                         "ровно — без узких участков, где приходится ползти с грузом.",
                "cargo": "Днепр — промышленный город, поэтому здесь преобладает не быт, а "
                         "работа: оборудование, запчасти, комплектующие, товар на склады. "
                         "Часто просят забрать с нескольких адресов в Киеве и привезти на одну.",
                "note": "Несколько точек загрузки на этом направлении — обычное дело, "
                        "добавьте их в калькуляторе, и цена пересчитается.",
            },
            "en": {
                "intro": "The M03 through Poltava and Kremenchuk. 480 km that run smoothly — "
                         "no narrow stretches where a loaded van has to crawl.",
                "cargo": "Dnipro is an industrial city, so this is mostly work rather than "
                         "household goods: machinery, spare parts, components, stock for "
                         "warehouses. Collections from several Kyiv addresses into one "
                         "delivery are common here.",
                "note": "Multiple pickup points are normal on this route — add them in the "
                        "calculator and the price updates.",
            },
        },
    },
    {
        "slug": "kyiv-kharkiv",
        "city": "city.kharkiv",
        "km": 480,
        "hours": "6–8",
        "via": ["city.poltava"],
        "copy": {
            "uk": {
                "intro": "Траса М03 через Полтаву. 480 км від Києва — за відстанню це "
                         "звичайний денний рейс.",
                "cargo": "Товар для магазинів, обладнання, речі при переїзді. Возимо і "
                         "туди, і назад — зворотний рейс часто вигідніший, якщо дати "
                         "збігаються.",
                # Свідомо без обіцянок щодо строків: на цьому напрямку графік
                # залежить від обстановки й комендантської години, і обіцяти
                # «один день» наперед було б нечесно.
                "note": "Дату й час виїзду на цьому напрямку узгоджуємо індивідуально — "
                        "плануємо під поточну ситуацію на дорозі. Зателефонуйте, і ми "
                        "чесно скажемо, коли зможемо поїхати.",
            },
            "ru": {
                "intro": "Трасса М03 через Полтаву. 480 км от Киева — по расстоянию это "
                         "обычный дневной рейс.",
                "cargo": "Товар для магазинов, оборудование, вещи при переезде. Возим и "
                         "туда, и обратно — обратный рейс часто выгоднее, если даты "
                         "совпадают.",
                "note": "Дату и время выезда на этом направлении согласовываем "
                        "индивидуально — планируем под текущую ситуацию на дороге. "
                        "Позвоните, и мы честно скажем, когда сможем поехать.",
            },
            "en": {
                "intro": "The M03 through Poltava. At 480 km from Kyiv this is, by distance, "
                         "an ordinary day trip.",
                "cargo": "Shop stock, equipment, belongings for people relocating. We run in "
                         "both directions — a return leg often works out cheaper if the "
                         "dates line up.",
                "note": "We agree the departure date and time individually on this route and "
                        "plan around current road conditions. Call us and we will tell you "
                        "honestly when we can go.",
            },
        },
    },
]

BY_SLUG = {r["slug"]: r for r in ROUTES}


def get(slug):
    return BY_SLUG.get(slug)


def copy_for(route, locale, default="uk"):
    """Текст маршруту потрібною мовою; якщо його немає — українською."""
    c = route.get("copy", {})
    return c.get(locale) or c.get(default) or {}
