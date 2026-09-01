# -*- coding: utf-8 -*-
"""
Сторінки населених пунктів Київської області.

Навіщо. «Вантажне таксі Бровари» — запит із набагато вищим наміром
купити, ніж «перевезення Київ Чернівці»: більшість роботи буса локальна.
У конкурентів таких сторінок 35+, у нас не було жодної. Це остання
велика прогалина проти них.

Чим ці сторінки відрізняються від сторінок напрямків (content/routes.py).
Там рахунок ПОКІЛОМЕТРОВИЙ, бо машина їде. Тут — ПОГОДИННИЙ, бо машина
стоїть і чекає на завантаженні: 799 грн/год + подача, мінімум 2 години.
Тому на цих сторінках немає ані кілометражу, ані готової суми — вона
чесно залежить від того, скільки триватиме завантаження.

Координати потрібні калькулятору: він рахує реальний маршрут через OSRM,
тож відстань ми не зашиваємо й не вигадуємо.

ВАЖЛИВО ПРО ТЕКСТИ. Кожен опис має бути ПРО ЦЕ МІСТО. Якщо взяти опис
Броварів і замінити назву, Google визнає сторінки дублікатами й не
покаже жодної — це гірше, ніж не мати їх узагалі. Пишемо про те, що
справді відрізняє: з якого боку Києва, через який міст чи трасу їхати,
який там забудований характер, що це означає для завантаження.

Чого тут НЕ пишемо: скільки замовлень ми туди возимо, які в нас там
клієнти, відгуки. Нічого з цього ніхто не підтверджував.
"""

PLACES = [
    {
        "slug": "brovary",
        "city": "city.brovary",
        "ll": [50.5111, 30.7900],
        "side": "place.side.left",
        "copy": {
            "uk": {
                "intro": "Бровари — лівий берег, за Дніпром, тож усе впирається в міст. "
                         "Виїзд із центру Києва в години пік через Північний або "
                         "Південний міст додає до дороги більше, ніж самі 20 кілометрів "
                         "траси, тому на ранок ми беремо запас часу й кажемо про це "
                         "заздалегідь, а не після того, як застрягли.",
                "work": "Уздовж броварської траси стоять склади й логістичні комплекси, "
                        "тому сюди часто везуть партії товару та обладнання. Друга "
                        "половина роботи — квартирні переїзди в нові житлові комплекси: "
                        "будинків тут побудували багато, і люди заїжджають цілий рік.",
                "note": "У нових ЖК майже завжди є вантажний ліфт і місце для машини "
                        "біля під'їзду — скажіть номер будинку, і ми одразу прикинемо, "
                        "де стати, щоб не носити речі через увесь двір.",
            },
            "ru": {
                "intro": "Бровары — левый берег, за Днепром, поэтому всё упирается в мост. "
                         "Выезд из центра Киева в час пик через Северный или Южный мост "
                         "добавляет к дороге больше, чем сами 20 километров трассы, "
                         "поэтому на утро мы берём запас времени и говорим об этом "
                         "заранее, а не после того, как застряли.",
                "work": "Вдоль броварской трассы стоят склады и логистические комплексы, "
                        "поэтому сюда часто везут партии товара и оборудование. Вторая "
                        "половина работы — квартирные переезды в новые жилые комплексы: "
                        "домов здесь построили много, и люди заезжают круглый год.",
                "note": "В новых ЖК почти всегда есть грузовой лифт и место для машины у "
                        "подъезда — назовите номер дома, и мы сразу прикинем, где стать, "
                        "чтобы не носить вещи через весь двор.",
            },
            "en": {
                "intro": "Brovary sits on the left bank, across the Dnipro, so everything "
                         "depends on the bridge. Leaving central Kyiv at rush hour over "
                         "the Northern or Southern bridge adds more to the trip than the "
                         "20 kilometres of road itself, so for morning jobs we build in "
                         "extra time and say so up front, not after we are stuck.",
                "work": "Warehouses and logistics parks line the Brovary highway, so "
                        "batches of stock and equipment go this way often. The other half "
                        "of the work is flat moves into the new residential blocks: a lot "
                        "of them have been built here and people move in all year round.",
                "note": "The newer blocks almost always have a goods lift and somewhere to "
                        "park by the entrance — give us the building number and we will "
                        "work out where to stand so nothing has to be carried across the "
                        "whole courtyard.",
            },
        },
    },
    {
        "slug": "irpin",
        "city": "city.irpin",
        "ll": [50.5218, 30.2506],
        "side": "place.side.west",
        "copy": {
            "uk": {
                "intro": "Ірпінь — захід від Києва, дорога через Житомирську трасу або "
                         "через Романівку. Місто досі відбудовується, і це видно на "
                         "маршруті: частина вулиць у ремонті, під'їзди до окремих "
                         "будинків змінюються. Тому адресу ми уточнюємо не «місто й "
                         "вулиця», а до під'їзду.",
                "work": "Найпомітніша частина роботи тут — перевезення будівельних "
                        "матеріалів, меблів і техніки у відновлені квартири й будинки. "
                        "Поруч із цим — звичайні переїзди й доставка товару для місцевих "
                        "магазинів.",
                "note": "Багато приватного сектору: вузькі вулиці, паркани, іноді "
                        "неможливо стати впритул. Скажіть заздалегідь, якщо під'їзд "
                        "складний, — це впливає на час завантаження, а отже й на суму.",
            },
            "ru": {
                "intro": "Ирпень — запад от Киева, дорога через Житомирскую трассу или "
                         "через Романовку. Город до сих пор отстраивается, и это видно на "
                         "маршруте: часть улиц в ремонте, подъезды к отдельным домам "
                         "меняются. Поэтому адрес мы уточняем не «город и улица», а до "
                         "подъезда.",
                "work": "Самая заметная часть работы здесь — перевозка строительных "
                        "материалов, мебели и техники в восстановленные квартиры и дома. "
                        "Рядом с этим — обычные переезды и доставка товара для местных "
                        "магазинов.",
                "note": "Много частного сектора: узкие улицы, заборы, иногда невозможно "
                        "стать вплотную. Скажите заранее, если подъезд сложный, — это "
                        "влияет на время загрузки, а значит и на сумму.",
            },
            "en": {
                "intro": "Irpin lies west of Kyiv, reached by the Zhytomyr highway or "
                         "through Romanivka. The town is still being rebuilt and it shows "
                         "on the route: some streets are under repair and the approaches "
                         "to individual buildings change. So we confirm the address down "
                         "to the entrance, not just the street.",
                "work": "The most visible part of the work here is carrying building "
                        "materials, furniture and appliances into restored flats and "
                        "houses. Alongside that are ordinary moves and deliveries for "
                        "local shops.",
                "note": "There is a lot of low-rise housing: narrow streets, fences, and "
                        "sometimes no way to park right at the door. Tell us in advance if "
                        "the approach is awkward — it affects loading time, and therefore "
                        "the total.",
            },
        },
    },
    {
        "slug": "bucha",
        "city": "city.bucha",
        "ll": [50.5486, 30.2119],
        "side": "place.side.west",
        "copy": {
            "uk": {
                "intro": "До Бучі їдемо через Ірпінь, тож обидва міста часто закриваються "
                         "одним виїздом. Забудова тут переважно низька — приватні будинки "
                         "й таунхауси, а не багатоповерхівки, — і це головне, що впливає "
                         "на роботу.",
                "work": "Найчастіше це переїзди в будинок або з будинку: меблі, побутова "
                        "техніка, речі з гаража й підвалу. Окрема історія — доставка "
                        "меблів і матеріалів на етапі ремонту, коли будинок ще не "
                        "заселений.",
                "note": "Приватний будинок довше вантажиться за квартиру: речі рознесені "
                        "по кімнатах, гаражу й дворі. Рахунок погодинний, тож зібрати все "
                        "в одне місце до приїзду машини — це прямо ваші зекономлені гроші.",
            },
            "ru": {
                "intro": "В Бучу едем через Ирпень, поэтому оба города часто закрываются "
                         "одним выездом. Застройка здесь в основном низкая — частные дома "
                         "и таунхаусы, а не многоэтажки, — и это главное, что влияет на "
                         "работу.",
                "work": "Чаще всего это переезды в дом или из дома: мебель, бытовая "
                        "техника, вещи из гаража и подвала. Отдельная история — доставка "
                        "мебели и материалов на этапе ремонта, когда дом ещё не заселён.",
                "note": "Частный дом грузится дольше квартиры: вещи разнесены по комнатам, "
                        "гаражу и двору. Счёт почасовой, поэтому собрать всё в одно место "
                        "до приезда машины — это прямо ваши сэкономленные деньги.",
            },
            "en": {
                "intro": "We reach Bucha through Irpin, so the two towns often fit into "
                         "one trip. The housing here is mostly low-rise — private houses "
                         "and townhouses rather than blocks of flats — and that is what "
                         "shapes the job.",
                "work": "Usually it is moving into or out of a house: furniture, "
                        "appliances, the contents of a garage or a basement. A separate "
                        "strand is delivering furniture and materials during renovation, "
                        "before anyone has moved in.",
                "note": "A house takes longer to load than a flat: things are spread across "
                        "rooms, the garage and the yard. The clock is what you pay for, so "
                        "gathering everything in one place before the van arrives is money "
                        "straight back in your pocket.",
            },
        },
    },
    {
        "slug": "vyshhorod",
        "city": "city.vyshhorod",
        "ll": [50.5847, 30.4894],
        "side": "place.side.north",
        "copy": {
            "uk": {
                "intro": "Вишгород — найближчий до Києва напрямок на північ, уздовж "
                         "Дніпра й Київського моря. Дорога одна й коротка, тож сюди "
                         "реально виїхати того ж дня, коли зателефонували, навіть у "
                         "другій половині дня.",
                "work": "Дві різні історії поруч. Перша — переїзди в житлові комплекси "
                        "вздовж набережної. Друга — сезонні перевезення на дачі й до "
                        "будинків біля води: навесні речі везуть туди, восени назад.",
                "note": "Через коротку дорогу тут особливо помітний мінімум у дві "
                        "години: сама поїздка займає менше, ніж завантаження. Якщо "
                        "перевезення дрібне, є сенс поєднати кілька справ за один виїзд.",
            },
            "ru": {
                "intro": "Вышгород — ближайшее к Киеву направление на север, вдоль Днепра "
                         "и Киевского моря. Дорога одна и короткая, поэтому сюда реально "
                         "выехать в тот же день, когда позвонили, даже во второй половине "
                         "дня.",
                "work": "Две разные истории рядом. Первая — переезды в жилые комплексы "
                        "вдоль набережной. Вторая — сезонные перевозки на дачи и к домам у "
                        "воды: весной вещи везут туда, осенью обратно.",
                "note": "Из-за короткой дороги здесь особенно заметен минимум в два часа: "
                        "сама поездка занимает меньше, чем загрузка. Если перевозка "
                        "мелкая, есть смысл объединить несколько дел за один выезд.",
            },
            "en": {
                "intro": "Vyshhorod is the closest destination north of Kyiv, along the "
                         "Dnipro and the Kyiv Reservoir. There is one short road, so a "
                         "same-day call-out is realistic here even in the afternoon.",
                "work": "Two different threads run side by side. One is moves into the "
                        "residential blocks along the waterfront. The other is seasonal "
                        "runs to summer houses near the water: things go out in spring and "
                        "come back in autumn.",
                "note": "Because the drive is short, the two-hour minimum is unusually "
                        "visible here: the journey itself takes less time than the loading. "
                        "For a small job it is worth combining several errands into one "
                        "call-out.",
            },
        },
    },
    {
        "slug": "boryspil",
        "city": "city.boryspil",
        "ll": [50.3527, 30.9550],
        "side": "place.side.left",
        "copy": {
            "uk": {
                "intro": "Бориспіль — це траса М03 і аеропорт. Дорога пряма й швидка, але "
                         "їхати через лівий берег, тому час у дорозі так само залежить від "
                         "мостів, як і в Броварах.",
                "work": "Крім звичайних переїздів і доставки товару в місто, окремий "
                        "напрямок — вантаж із карго-терміналу аеропорту та в нього. Це "
                        "коробки й піддони, які треба забрати за конкретним документом і "
                        "у конкретний час.",
                "note": "Вантаж із аеропорту — це завжди пропуск, оформлення й очікування. "
                        "Скажіть у розмові, що йдеться про карго-термінал: погодинний "
                        "рахунок тут стосується не тільки дороги, а й часу на території.",
            },
            "ru": {
                "intro": "Борисполь — это трасса М03 и аэропорт. Дорога прямая и быстрая, "
                         "но ехать через левый берег, поэтому время в пути так же зависит "
                         "от мостов, как и в Броварах.",
                "work": "Кроме обычных переездов и доставки товара в город, отдельное "
                        "направление — груз из карго-терминала аэропорта и в него. Это "
                        "коробки и паллеты, которые нужно забрать по конкретному документу "
                        "и в конкретное время.",
                "note": "Груз из аэропорта — это всегда пропуск, оформление и ожидание. "
                        "Скажите в разговоре, что речь о карго-терминале: почасовой счёт "
                        "здесь касается не только дороги, но и времени на территории.",
            },
            "en": {
                "intro": "Boryspil means the M03 highway and the airport. The road is "
                         "straight and quick, but it runs through the left bank, so travel "
                         "time depends on the bridges just as it does for Brovary.",
                "work": "Besides ordinary moves and deliveries into the town, there is a "
                        "separate strand: freight to and from the airport cargo terminal. "
                        "That means boxes and pallets to be collected against a specific "
                        "document at a specific time.",
                "note": "Airport freight always involves a pass, paperwork and waiting. Say "
                         "on the call that it is the cargo terminal: the hourly clock here "
                         "covers the time on site, not only the drive.",
            },
        },
    },
    {
        "slug": "vyshneve",
        "city": "city.vyshneve",
        "ll": [50.3866, 30.3706],
        "side": "place.side.west",
        "copy": {
            "uk": {
                "intro": "Вишневе практично зрослося з Києвом: із Святошина сюди їхати "
                         "стільки ж, скільки в інший район міста. За тарифом це область, "
                         "але за логістикою — майже місто, і виїхати сюди зазвичай можна "
                         "того ж дня.",
                "work": "Багато малого бізнесу: магазини, майстерні, невеликі склади. "
                        "Звідси й характер вантажу — регулярний розвіз товару невеликими "
                        "партіями, коли повна фура не потрібна, а «Нова пошта» вже незручна "
                        "за габаритами.",
                "note": "Якщо маршрут повторюється щотижня, скажіть про це одразу: "
                        "постійний графік зручніше рахувати наперед, ніж кожну поїздку "
                        "окремо.",
            },
            "ru": {
                "intro": "Вишнёвое практически срослось с Киевом: из Святошина сюда ехать "
                         "столько же, сколько в другой район города. По тарифу это область, "
                         "но по логистике — почти город, и выехать сюда обычно можно в тот "
                         "же день.",
                "work": "Много малого бизнеса: магазины, мастерские, небольшие склады. "
                        "Отсюда и характер груза — регулярный развоз товара небольшими "
                        "партиями, когда полная фура не нужна, а «Новая почта» уже неудобна "
                        "по габаритам.",
                "note": "Если маршрут повторяется каждую неделю, скажите об этом сразу: "
                        "постоянный график удобнее считать наперёд, чем каждую поездку "
                        "отдельно.",
            },
            "en": {
                "intro": "Vyshneve has effectively grown into Kyiv: from Sviatoshyn it is "
                         "no further than another district of the city. On the tariff it "
                         "counts as the region, but logistically it is almost the city, and "
                         "a same-day call-out is usually possible.",
                "work": "There is a lot of small business here: shops, workshops, small "
                        "warehouses. That shapes the loads — regular deliveries in modest "
                        "batches, where a full lorry is unnecessary and a parcel service is "
                        "already awkward for the dimensions.",
                "note": "If the route repeats every week, say so at the start: a standing "
                        "schedule is easier to price ahead than each trip on its own.",
            },
        },
    },
    {
        "slug": "vasylkiv",
        "city": "city.vasylkiv",
        "ll": [50.1848, 30.3103],
        "side": "place.side.south",
        "copy": {
            "uk": {
                "intro": "Васильків стоїть на Одеській трасі, і це найзручніший "
                         "напрямок з усієї області: виїзд із Києва через Голосіїв, "
                         "далі широка магістраль без світлофорів. Затори тут "
                         "трапляються не в будні вранці, а в п'ятницю ввечері й у "
                         "неділю, коли місто масово їде на дачі та назад.",
                "work": "Половина роботи — приватний сектор: у Василькові й довкола "
                        "багато власних будинків, а це означає меблі, будівельні "
                        "матеріали та техніку возять не в ліфт, а в двір. Друга "
                        "половина — товар із київських складів у місцеві магазини.",
                "note": "У приватному секторі головне питання не поверх, а заїзд: "
                        "чи пройде бус у ворота й чи розвернеться на вулиці. "
                        "Скажіть адресу — подивимось на карті до виїзду, а не "
                        "будемо здавати задом уздовж паркану.",
            },
            "ru": {
                "intro": "Васильков стоит на Одесской трассе, и это самое удобное "
                         "направление во всей области: выезд из Киева через "
                         "Голосеево, дальше широкая магистраль без светофоров. "
                         "Пробки здесь бывают не в будни утром, а в пятницу вечером "
                         "и в воскресенье, когда город массово едет на дачи и обратно.",
                "work": "Половина работы — частный сектор: в Василькове и вокруг "
                        "много своих домов, а это значит, что мебель, стройматериалы "
                        "и технику возят не в лифт, а во двор. Вторая половина — "
                        "товар с киевских складов в местные магазины.",
                "note": "В частном секторе главный вопрос не этаж, а заезд: пройдёт "
                        "ли бус в ворота и развернётся ли на улице. Скажите адрес — "
                        "посмотрим на карте до выезда, а не будем сдавать задом "
                        "вдоль забора.",
            },
            "en": {
                "intro": "Vasylkiv sits on the Odesa highway, which makes it the "
                         "easiest run in the whole region: out of Kyiv through "
                         "Holosiivo, then a wide road with no traffic lights. The "
                         "jams here are not weekday mornings but Friday evenings and "
                         "Sundays, when the city drives out to its dachas and back.",
                "work": "Half the work is the private housing sector: Vasylkiv and "
                        "the villages around it are mostly houses, so furniture, "
                        "building materials and appliances go into a yard rather "
                        "than a lift. The other half is stock from Kyiv warehouses "
                        "to local shops.",
                "note": "In a street of houses the question is never the floor, it "
                        "is the entrance: will the van fit through the gate and can "
                        "it turn around. Send the address and we will look at it on "
                        "the map beforehand, instead of reversing along your fence.",
            },
        },
    },
    {
        "slug": "obukhiv",
        "city": "city.obukhiv",
        "ll": [50.1069, 30.6214],
        "side": "place.side.south",
        "copy": {
            "uk": {
                "intro": "Обухів — південь, дорога вздовж Дніпра через Українку. "
                         "Траса тут вужча за Одеську й проходить через населені "
                         "пункти, тож середня швидкість нижча, ніж здається по "
                         "кілометрах на карті. Ми закладаємо це в час одразу, щоб "
                         "не переносити другу адресу на завтра.",
                "work": "Місто промислове, і поруч велике целюлозно-паперове "
                        "виробництво, тому сюди й звідси регулярно возять палети та "
                        "габаритні партії. Разом із цим — звичайні переїзди: "
                        "Обухів давно перестав бути тільки заводським містом.",
                "note": "Габаритний вантаж на палеті вимагає не тільки місця в "
                        "кузові, а й того, щоб його було чим завантажити з вашого "
                        "боку. Вантажників у нас немає — уточніть заздалегідь, чи є "
                        "на складі навантажувач і рампа.",
            },
            "ru": {
                "intro": "Обухов — юг, дорога вдоль Днепра через Украинку. Трасса "
                         "здесь уже Одесской и проходит через населённые пункты, "
                         "поэтому средняя скорость ниже, чем кажется по километрам "
                         "на карте. Мы закладываем это во время сразу, чтобы не "
                         "переносить второй адрес на завтра.",
                "work": "Город промышленный, рядом крупное целлюлозно-бумажное "
                        "производство, поэтому сюда и отсюда регулярно возят палеты "
                        "и габаритные партии. Вместе с этим — обычные переезды: "
                        "Обухов давно перестал быть только заводским городом.",
                "note": "Габаритный груз на палете требует не только места в кузове, "
                        "но и того, чем его загрузить с вашей стороны. Грузчиков у "
                        "нас нет — уточните заранее, есть ли на складе погрузчик и "
                        "рампа.",
            },
            "en": {
                "intro": "Obukhiv is south, along the Dnipro through Ukrainka. The "
                         "road is narrower than the Odesa highway and runs through "
                         "villages, so the average speed is lower than the map's "
                         "kilometres suggest. We build that into the time from the "
                         "start rather than pushing your second address to tomorrow.",
                "work": "It is an industrial town with a large pulp and paper works "
                        "next door, so pallets and bulky consignments move in and out "
                        "of here regularly. Alongside that, ordinary household moves: "
                        "Obukhiv stopped being only a factory town a long time ago.",
                "note": "A pallet needs more than room in the bay — it needs "
                        "something at your end to lift it. We have no loaders, so "
                        "check in advance whether the warehouse has a forklift and a "
                        "ramp.",
            },
        },
    },
    {
        "slug": "fastiv",
        "city": "city.fastiv",
        "ll": [50.0747, 29.9203],
        "side": "place.side.south",
        "copy": {
            "uk": {
                "intro": "Фастів — південний захід, приблизно година дороги від "
                         "Києва по Житомирській трасі з поворотом. Це вже та "
                         "відстань, на якій дорога туди й назад займає більшу "
                         "частину замовлення, тому одна поїздка з двома адресами "
                         "виходить розумніше, ніж дві окремі.",
                "work": "Фастів — великий залізничний вузол, і місто живе навколо "
                        "нього. Возять сюди переважно те, що не поїде вагоном: "
                        "меблі, побутову техніку, товар у роздрібні точки, речі при "
                        "переїзді до Києва й назад.",
                "note": "Якщо у вас дві адреси в один бік — скажіть про це відразу. "
                        "На такій відстані другу точку майже завжди вигідніше "
                        "зробити тим самим рейсом, ніж викликати машину вдруге.",
            },
            "ru": {
                "intro": "Фастов — юго-запад, примерно час дороги от Киева по "
                         "Житомирской трассе с поворотом. Это уже то расстояние, на "
                         "котором дорога туда и обратно занимает большую часть "
                         "заказа, поэтому одна поездка с двумя адресами выходит "
                         "разумнее, чем две отдельные.",
                "work": "Фастов — крупный железнодорожный узел, и город живёт вокруг "
                        "него. Возят сюда в основном то, что не поедет вагоном: "
                        "мебель, бытовую технику, товар в розничные точки, вещи при "
                        "переезде в Киев и обратно.",
                "note": "Если у вас два адреса в одну сторону — скажите об этом "
                        "сразу. На таком расстоянии вторую точку почти всегда "
                        "выгоднее сделать тем же рейсом, чем вызывать машину второй "
                        "раз.",
            },
            "en": {
                "intro": "Fastiv is south-west, about an hour from Kyiv on the "
                         "Zhytomyr road plus a turning. At this distance the drive "
                         "out and back takes up most of the job, which is why one "
                         "trip covering two addresses works out more sensibly than "
                         "two separate call-outs.",
                "work": "Fastiv is a major railway junction and the town lives around "
                        "it. What comes here by road is what will not go by wagon: "
                        "furniture, appliances, stock for shops, and belongings "
                        "moving to Kyiv and back.",
                "note": "If you have two addresses in the same direction, say so at "
                        "the start. At this distance the second stop is almost always "
                        "cheaper on the same run than as a second call-out.",
            },
        },
    },
    {
        "slug": "bila-tserkva",
        "city": "city.bilatserkva",
        "ll": [49.7950, 30.1310],
        "side": "place.side.south",
        "copy": {
            "uk": {
                "intro": "Біла Церква — найдальше місто з тих, що ми рахуємо як "
                         "область: близько 80 кілометрів по Одеській трасі. Дорога "
                         "хороша й швидка, але туди й назад це вже пів робочого дня, "
                         "і на таких замовленнях ми домовляємось про час і ціну "
                         "особливо ретельно — телефоном, а не листуванням.",
                "work": "Це велике самостійне місто з промисловою зоною, а не "
                        "передмістя, тому робота тут інша: не стільки дачі й "
                        "приватний сектор, скільки товар між складами, обладнання та "
                        "переїзди між Києвом і Білою Церквою в обидва боки.",
                "note": "На такій відстані порожній зворотний рейс — головна стаття "
                        "витрат. Якщо у вас є що відправити назад до Києва, скажіть: "
                        "рейс із вантажем в обидва боки завжди рахується інакше, ніж "
                        "рейс в один кінець.",
            },
            "ru": {
                "intro": "Белая Церковь — самый дальний город из тех, что мы считаем "
                         "областью: около 80 километров по Одесской трассе. Дорога "
                         "хорошая и быстрая, но туда и обратно это уже полдня, и на "
                         "таких заказах мы договариваемся о времени и цене особенно "
                         "тщательно — по телефону, а не перепиской.",
                "work": "Это большой самостоятельный город с промышленной зоной, а не "
                        "пригород, поэтому работа здесь другая: не столько дачи и "
                        "частный сектор, сколько товар между складами, оборудование и "
                        "переезды между Киевом и Белой Церковью в обе стороны.",
                "note": "На таком расстоянии пустой обратный рейс — главная статья "
                        "расходов. Если у вас есть что отправить назад в Киев, "
                        "скажите: рейс с грузом в обе стороны всегда считается иначе, "
                        "чем рейс в один конец.",
            },
            "en": {
                "intro": "Bila Tserkva is the furthest town we still count as the "
                         "region: about 80 kilometres down the Odesa highway. The "
                         "road is good and fast, but out and back is half a working "
                         "day, so on jobs like this we agree the time and the price "
                         "especially carefully — by phone, not by messages.",
                "work": "This is a large town in its own right with an industrial "
                        "zone, not a suburb, and the work reflects that: less dacha "
                        "and private-house traffic, more stock between warehouses, "
                        "equipment, and moves between Kyiv and Bila Tserkva in both "
                        "directions.",
                "note": "At this distance an empty return leg is the single biggest "
                        "cost. If you have something to send back to Kyiv, say so — a "
                        "run loaded both ways is always priced differently from a "
                        "one-way one.",
            },
        },
    },
]

BY_SLUG = {p["slug"]: p for p in PLACES}


def neighbours(slug, limit=3):
    """
    Сусідні напрямки для перелінковки.

    Спершу ті, що з того самого боку Києва: людині, яка дивиться Бучу,
    Ірпінь корисніший за Бориспіль.

    Список «решти» ПРОКРУЧУЄТЬСЯ від поточного міста, а не береться з
    початку файлу. Без цього перші міста в списку збирали всі посилання,
    а Вишгород — єдиний на півночі — не отримував жодного: на сторінку,
    на яку ніхто не веде, Google дивиться значно гірше. Тест перевіряє,
    що разом сторінки лінкують усі міста без винятку.
    """
    current = BY_SLUG.get(slug)
    if not current:
        return []
    i = PLACES.index(current)
    rotated = PLACES[i + 1:] + PLACES[:i]
    same = [p for p in rotated if p["side"] == current["side"]]
    other = [p for p in rotated if p["side"] != current["side"]]
    return (same + other)[:limit]
