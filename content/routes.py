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
    {
        "slug": "kyiv-zhytomyr",
        "city": "city.zhytomyr",
        "km": 140,
        "hours": "2",
        "via": [],
        "copy": {
            "uk": {
                "intro": "Найближчий із міжміських напрямків — 140 км по трасі М06. За часом "
                         "це ближче до подовженого міського рейсу, ніж до справжнього "
                         "міжміського: туди й назад укладаємось в один день без поспіху.",
                "cargo": "Через коротке плече цей напрямок найкраще підходить для регулярних "
                         "рейсів: постачання магазинів і кафе, розвіз замовлень, дрібні "
                         "партії товару за графіком. Разові переїзди теж возимо, але саме "
                         "тут найчастіше домовляються про постійний маршрут.",
                "note": "Якщо возити треба щотижня, рахуємо не за годинами, а за маршрутом — "
                        "виходить помітно дешевше.",
            },
            "ru": {
                "intro": "Ближайшее из междугородних направлений — 140 км по трассе М06. По "
                         "времени это ближе к удлинённому городскому рейсу, чем к настоящему "
                         "междугороднему: туда и обратно укладываемся в один день без спешки.",
                "cargo": "Из-за короткого плеча это направление лучше всего подходит для "
                         "регулярных рейсов: поставки в магазины и кафе, развоз заказов, "
                         "мелкие партии товара по графику. Разовые переезды тоже возим, но "
                         "именно здесь чаще всего договариваются о постоянном маршруте.",
                "note": "Если возить нужно еженедельно, считаем не по часам, а по маршруту — "
                        "выходит заметно дешевле.",
            },
            "en": {
                "intro": "The shortest of the intercity routes — 140 km on the M06. In "
                         "practice this is closer to an extended city run than a long-haul "
                         "trip: there and back fits comfortably into one day.",
                "cargo": "The short distance makes this the best route for regular runs: "
                         "resupplying shops and cafes, delivering orders, small batches on a "
                         "schedule. We do one-off moves too, but this is the direction where "
                         "people most often set up a standing route.",
                "note": "If you need this weekly, we price the route rather than the hours — "
                        "it works out noticeably cheaper.",
            },
        },
    },
    {
        "slug": "kyiv-cherkasy",
        "city": "city.cherkasy",
        "km": 190,
        "hours": "2–3",
        "via": [],
        "copy": {
            "uk": {
                "intro": "190 км на південний схід. Дорога спокійна, без затяжних підйомів, "
                         "тож туди й назад за день — звична справа, а не подвиг.",
                "cargo": "Меблі й техніка при переїзді, товар для магазинів, обладнання. "
                         "Черкаси близько, тому сюди часто просять забрати щось терміново — "
                         "і ми встигаємо в той самий день.",
                "note": "Терміновий виїзд у день звернення на цьому напрямку реальний, якщо "
                        "подзвонити до обіду.",
            },
            "ru": {
                "intro": "190 км на юго-восток. Дорога спокойная, без затяжных подъёмов, "
                         "поэтому туда и обратно за день — обычное дело, а не подвиг.",
                "cargo": "Мебель и техника при переезде, товар для магазинов, оборудование. "
                         "Черкассы близко, поэтому сюда часто просят забрать что-то срочно — "
                         "и мы успеваем в тот же день.",
                "note": "Срочный выезд в день обращения на этом направлении реален, если "
                        "позвонить до обеда.",
            },
            "en": {
                "intro": "190 km to the south-east. An easy road with no long climbs, so a "
                         "same-day return trip is routine rather than ambitious.",
                "cargo": "Furniture and appliances for people moving, shop stock, equipment. "
                         "Cherkasy is close enough that urgent collections come up often — "
                         "and we can usually manage them the same day.",
                "note": "Same-day departure is realistic on this route if you call before "
                        "midday.",
            },
        },
    },
    {
        "slug": "kyiv-vinnytsia",
        "city": "city.vinnytsia",
        "km": 265,
        "hours": "3–4",
        "via": [],
        "copy": {
            "uk": {
                "intro": "265 км трасою М12. Одне з тих плечей, де ще можна встигнути туди й "
                         "назад за день, якщо вирушити зранку і не мати довгого вивантаження.",
                "cargo": "Товар для роздрібу, обладнання для закладів, меблі. Вінниця — "
                         "великий обласний центр із живим бізнесом, тож звідси регулярно "
                         "їдуть партії товару в обидва боки.",
                "note": "Якщо у вас є що везти назад до Києва, скажіть одразу — зворотний "
                        "рейс здешевлює обидва.",
            },
            "ru": {
                "intro": "265 км по трассе М12. Одно из тех плеч, где ещё можно успеть туда "
                         "и обратно за день, если выехать утром и не иметь долгой выгрузки.",
                "cargo": "Товар для розницы, оборудование для заведений, мебель. Винница — "
                         "крупный областной центр с живым бизнесом, поэтому отсюда регулярно "
                         "едут партии товара в обе стороны.",
                "note": "Если у вас есть что везти обратно в Киев, скажите сразу — обратный "
                        "рейс удешевляет оба.",
            },
            "en": {
                "intro": "265 km on the M12. This is one of the routes where a return trip "
                         "in a single day still works, if we set off early and unloading is "
                         "not drawn out.",
                "cargo": "Retail stock, equipment for bars and restaurants, furniture. "
                         "Vinnytsia is a substantial regional centre with active business, "
                         "so consignments run in both directions regularly.",
                "note": "If you have something to send back to Kyiv, mention it up front — a "
                        "return leg brings the price down on both.",
            },
        },
    },
    {
        "slug": "kyiv-rivne",
        "city": "city.rivne",
        "km": 330,
        "hours": "4–5",
        "via": ["city.zhytomyr"],
        "copy": {
            "uk": {
                "intro": "330 км тією ж трасою М06, що веде на Львів. Рівне стоїть якраз по "
                         "дорозі, тож цей напрямок часто вдається поєднати з львівським "
                         "рейсом.",
                "cargo": "Будматеріали в упаковці, меблі, товар для магазинів, обладнання. "
                         "Через розташування на трасі сюди зручно завозити партії дорогою "
                         "далі на захід.",
                "note": "Якщо ваш вантаж їде в Рівне, а в нас того тижня є рейс на Львів — "
                        "вийде дешевше. Спитайте при дзвінку.",
            },
            "ru": {
                "intro": "330 км по той же трассе М06, что ведёт на Львов. Ровно стоит как "
                         "раз по дороге, поэтому это направление часто удаётся совместить со "
                         "львовским рейсом.",
                "cargo": "Стройматериалы в упаковке, мебель, товар для магазинов, "
                         "оборудование. Из-за расположения на трассе сюда удобно завозить "
                         "партии по дороге дальше на запад.",
                "note": "Если ваш груз едет в Ровно, а у нас на той неделе есть рейс на "
                        "Львов — выйдет дешевле. Спросите при звонке.",
            },
            "en": {
                "intro": "330 km along the same M06 that runs to Lviv. Rivne sits directly "
                         "on that road, so this route can often be combined with a Lviv trip.",
                "cargo": "Packaged building materials, furniture, shop stock, equipment. "
                         "Being on the main westbound road makes it convenient to drop a "
                         "consignment here on the way further west.",
                "note": "If your load is going to Rivne and we have a Lviv run that week, it "
                        "comes out cheaper. Ask when you call.",
            },
        },
    },
    {
        "slug": "kyiv-poltava",
        "city": "city.poltava",
        "km": 340,
        "hours": "4–5",
        "via": [],
        "copy": {
            "uk": {
                "intro": "340 км трасою М03 — тією самою, що веде на Харків. Дорога хороша, "
                         "рух рівний, без ділянок, де доводиться повзти.",
                "cargo": "Харчове й торгове обладнання, товар для магазинів і кафе, меблі. "
                         "Полтава — сильний аграрний і харчовий регіон, тому часто везуть "
                         "обладнання для виробництв і закладів.",
                "note": "Полтава лежить по дорозі на Харків і Дніпро — якщо вантаж їде далі, "
                        "проміжна точка тут майже нічого не додає до вартості.",
            },
            "ru": {
                "intro": "340 км по трассе М03 — той самой, что ведёт на Харьков. Дорога "
                         "хорошая, движение ровное, без участков, где приходится ползти.",
                "cargo": "Пищевое и торговое оборудование, товар для магазинов и кафе, "
                         "мебель. Полтава — сильный аграрный и пищевой регион, поэтому часто "
                         "везут оборудование для производств и заведений.",
                "note": "Полтава лежит по дороге на Харьков и Днепр — если груз едет дальше, "
                        "промежуточная точка здесь почти ничего не добавляет к стоимости.",
            },
            "en": {
                "intro": "340 km on the M03, the same road that continues to Kharkiv. Good "
                         "surface and steady traffic, with no stretches where a loaded van "
                         "has to crawl.",
                "cargo": "Catering and retail equipment, stock for shops and cafes, "
                         "furniture. Poltava sits in a strong agricultural and food-producing "
                         "region, so production and hospitality equipment moves here often.",
                "note": "Poltava is on the way to both Kharkiv and Dnipro — if your load is "
                        "going further, adding a stop here costs almost nothing.",
            },
        },
    },
    {
        "slug": "kyiv-zaporizhzhia",
        "city": "city.zapor",
        "km": 520,
        "hours": "7–9",
        "via": ["city.poltava", "city.dnipro"],
        "copy": {
            "uk": {
                "intro": "520 км через Полтаву й Дніпро. Один із довших рейсів: виїзд "
                         "зазвичай рано вранці, щоб вивантажитись того самого дня.",
                "cargo": "Промислове обладнання, метал у пакуванні, запчастини, товар на "
                         "склади. Запоріжжя — індустріальне місто, і вантажі тут відповідні: "
                         "важчі й габаритніші за середні.",
                "note": "Скажіть вагу й габарити при дзвінку: на цьому напрямку частіше, ніж "
                        "деінде, буває, що вантаж просто не влазить у бус до 3,5 т — краще "
                        "зʼясувати це заздалегідь, ніж на місці.",
            },
            "ru": {
                "intro": "520 км через Полтаву и Днепр. Один из более длинных рейсов: выезд "
                         "обычно рано утром, чтобы выгрузиться в тот же день.",
                "cargo": "Промышленное оборудование, металл в упаковке, запчасти, товар на "
                         "склады. Запорожье — индустриальный город, и грузы здесь "
                         "соответствующие: тяжелее и габаритнее средних.",
                "note": "Скажите вес и габариты при звонке: на этом направлении чаще, чем "
                        "где-либо, бывает, что груз просто не влезает в бус до 3,5 т — лучше "
                        "выяснить это заранее, чем на месте.",
            },
            "en": {
                "intro": "520 km via Poltava and Dnipro. One of the longer runs: we normally "
                         "leave early so we can unload the same day.",
                "cargo": "Industrial equipment, packaged metal, spare parts, stock for "
                         "warehouses. Zaporizhzhia is an industrial city and the loads "
                         "reflect that — heavier and bulkier than average.",
                "note": "Tell us the weight and dimensions when you call. More often than on "
                        "other routes, a load here simply will not fit a 3.5-tonne van — far "
                        "better to establish that in advance than on the day.",
            },
        },
    },
    {
        "slug": "kyiv-chernivtsi",
        "city": "city.chernivtsi",
        "km": 540,
        "hours": "8–10",
        "via": ["city.vinnytsia"],
        "copy": {
            "uk": {
                "intro": "540 км на південний захід через Вінницю. За кілометрами це як "
                         "Львів, але часу треба більше: остання третина дороги вужча й "
                         "повільніша, тож ми не обіцяємо львівських строків.",
                "cargo": "Меблі й особисті речі при переїзді, товар для магазинів, "
                         "обладнання. Чернівці — не найчастіший напрямок, тому рейс сюди "
                         "майже завжди планується під конкретне замовлення.",
                "note": "Через відстань і дорогу тут майже завжди ночівля в дорозі або "
                        "вивантаження наступного ранку. Це закладено в розрахунок, ніяких "
                        "доплат «за ніч» потім не зʼявляється.",
            },
            "ru": {
                "intro": "540 км на юго-запад через Винницу. По километрам это как Львов, но "
                         "времени нужно больше: последняя треть дороги уже и медленнее, "
                         "поэтому мы не обещаем львовских сроков.",
                "cargo": "Мебель и личные вещи при переезде, товар для магазинов, "
                         "оборудование. Черновцы — не самое частое направление, поэтому рейс "
                         "сюда почти всегда планируется под конкретный заказ.",
                "note": "Из-за расстояния и дороги здесь почти всегда ночёвка в пути или "
                        "выгрузка на следующее утро. Это заложено в расчёт, никаких доплат "
                        "«за ночь» потом не появляется.",
            },
            "en": {
                "intro": "540 km to the south-west via Vinnytsia. The same distance as Lviv, "
                         "but it takes longer: the last third of the road is narrower and "
                         "slower, so we do not promise Lviv timings here.",
                "cargo": "Furniture and personal belongings for people relocating, shop "
                         "stock, equipment. Chernivtsi is not a frequent destination, so a "
                         "run here is almost always planned around a specific booking.",
                "note": "Given the distance and the road, this usually means an overnight "
                        "stop or unloading the following morning. That is built into the "
                        "quote — no overnight surcharge appears afterwards.",
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
