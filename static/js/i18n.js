/**
 * Рядки для скриптів, три мови.
 *
 * Чому не віддаємо переклади з сервера інлайновим <script>: сторінка тоді
 * не кешується цілком, а інлайновий скрипт заважає ввести сувору CSP
 * (див. Phase 6). Тут рядків небагато, тому дешевше покласти всі три мови
 * в один статичний файл — він кешується назавжди за хешем у ?v=.
 *
 * Мова береться з <html lang>, який ставить сервер.
 */
(function (global) {
  "use strict";

  var STRINGS = {
    uk: {
      "calc.busy": "Рахуємо…",
      "calc.need_two": "Вкажіть мінімум дві точки: звідки та куди.",
      "calc.not_found": "Адресу «{label}» не знайдено. Уточніть написання або поставте точку на карті.",
      "calc.no_route": "Маршрут не знайдено. Перевірте точки або спробуйте інші адреси.",
      "calc.failed": "Не вдалося побудувати маршрут. Перевірте адреси або спробуйте за хвилину.",
      "calc.nothing": "Нічого не знайдено",
      "calc.map_point": "Точка на карті",
      "calc.cheapest": "найдешевше",
      "calc.vehicle": "Бус до 3,5 т",
      "unit.km": "км",
      "unit.hour": "год",
      "unit.min": "хв",
      "unit.uah": "грн",
      "unit.uah_hour": "грн/год",
      "quote.return": "Туди й назад",
      "quote.return_note": "Зворотний рейс із вантажем — чверть від ціни «туди»: машина однаково їде цим шляхом.",
      "quote.abroad": "Закордонний рейс",
      "quote.abroad_note": "{km} км повного пробігу × {rate} € — це {oneway} €/км, якщо рахувати відстань в один бік.",
      "price.abroad_note": "{km} км туди й назад × {rate} € ({oneway} €/км за відстань в один бік)",
      "quote.intercity": "Міжміський рейс",
      "quote.intercity_note": "{rate} грн/км · ціна за доставку в один бік, порожній зворотний пробіг уже враховано",
      "quote.local": "По Києву та області",
      "quote.local_value": "від {rate} грн/год",
      "quote.local_note": "Мінімум {hours} год + подача {feed} грн. Підсумок залежить від того, скільки триватиме завантаження — назвемо його в розмові.",
      "price.hourly_note": "Подача {feed} грн + від {hours} год × {rate} грн/год",
      "price.feed": "Виїзд",
      "form.bad_phone": "Введіть коректний номер телефону — 9 цифр після +380.",
      "form.sending": "Надсилаємо…",
      "form.send_failed": "Не вдалося надіслати. Спробуйте ще раз або зателефонуйте.",
      "form.no_connection": "Немає звʼязку з сервером. Спробуйте пізніше або зателефонуйте нам.",
      "route.label": "Маршрут",
      "route.distance": "Відстань",
      "route.duration": "Час у дорозі",
      "route.service": "Послуга",
      "route.price": "Орієнтовна вартість",
      "calc.click_hint": "<strong>Натисніть на карту</strong>, щоб додати точку маршруту.",
      "calc.pending": "Точка на карті…",
      "calc.remove": "Видалити",
      "calc.via_ph": "Проміжна точка (місто або адреса)",
      "city.zhytomyr": "Житомир",
      "city.cherkasy": "Черкаси",
      "city.vinnytsia": "Вінниця",
      "city.rivne": "Рівне",
      "city.poltava": "Полтава",
      "city.zapor": "Запоріжжя",
      "city.chernivtsi": "Чернівці",
      "city.warszawa": "Варшава",
      "city.krakow": "Краків",
      "city.praha": "Прага",
      "city.bratislava": "Братислава",
      "city.berlin": "Берлін",
      "city.kyiv": "Київ", "city.lviv": "Львів", "city.odesa": "Одеса",
      "city.dnipro": "Дніпро", "city.kharkiv": "Харків"
    },
    ru: {
      "calc.busy": "Считаем…",
      "calc.need_two": "Укажите минимум две точки: откуда и куда.",
      "calc.not_found": "Адрес «{label}» не найден. Уточните написание или поставьте точку на карте.",
      "calc.no_route": "Маршрут не найден. Проверьте точки или попробуйте другие адреса.",
      "calc.failed": "Не удалось построить маршрут. Проверьте адреса или попробуйте через минуту.",
      "calc.nothing": "Ничего не найдено",
      "calc.map_point": "Точка на карте",
      "calc.cheapest": "дешевле всего",
      "calc.vehicle": "Бус до 3,5 т",
      "unit.km": "км",
      "unit.hour": "ч",
      "unit.min": "мин",
      "unit.uah": "грн",
      "unit.uah_hour": "грн/час",
      "quote.return": "Туда и обратно",
      "quote.return_note": "Обратный рейс с грузом — четверть от цены «туда»: машина всё равно едет этим путём.",
      "quote.abroad": "Заграничный рейс",
      "quote.abroad_note": "{km} км полного пробега × {rate} € — это {oneway} €/км, если считать расстояние в один конец.",
      "price.abroad_note": "{km} км туда и обратно × {rate} € ({oneway} €/км за расстояние в один конец)",
      "quote.intercity": "Междугородний рейс",
      "quote.intercity_note": "{rate} грн/км · цена за доставку в один конец, порожний обратный пробег уже учтён",
      "quote.local": "По Киеву и области",
      "quote.local_value": "от {rate} грн/час",
      "quote.local_note": "Минимум {hours} ч + подача {feed} грн. Итог зависит от того, сколько продлится загрузка — назовём его в разговоре.",
      "price.hourly_note": "Подача {feed} грн + от {hours} ч × {rate} грн/час",
      "price.feed": "Подача",
      "form.bad_phone": "Введите корректный номер телефона — 9 цифр после +380.",
      "form.sending": "Отправляем…",
      "form.send_failed": "Не удалось отправить. Попробуйте ещё раз или позвоните.",
      "form.no_connection": "Нет связи с сервером. Попробуйте позже или позвоните нам.",
      "route.label": "Маршрут",
      "route.distance": "Расстояние",
      "route.duration": "Время в дороге",
      "route.service": "Услуга",
      "route.price": "Примерная стоимость",
      "calc.click_hint": "<strong>Нажмите на карту</strong>, чтобы добавить точку маршрута.",
      "calc.pending": "Точка на карте…",
      "calc.remove": "Удалить",
      "calc.via_ph": "Промежуточная точка (город или адрес)",
      "city.zhytomyr": "Житомир",
      "city.cherkasy": "Черкассы",
      "city.vinnytsia": "Винница",
      "city.rivne": "Ровно",
      "city.poltava": "Полтава",
      "city.zapor": "Запорожье",
      "city.chernivtsi": "Черновцы",
      "city.warszawa": "Варшава",
      "city.krakow": "Краков",
      "city.praha": "Прага",
      "city.bratislava": "Братислава",
      "city.berlin": "Берлин",
      "city.kyiv": "Киев", "city.lviv": "Львов", "city.odesa": "Одесса",
      "city.dnipro": "Днепр", "city.kharkiv": "Харьков"
    },
    en: {
      "calc.busy": "Calculating…",
      "calc.need_two": "Enter at least two points: where from and where to.",
      "calc.not_found": "We could not find “{label}”. Check the spelling or place a point on the map.",
      "calc.no_route": "No route found. Check the points or try different addresses.",
      "calc.failed": "We could not build the route. Check the addresses or try again in a minute.",
      "calc.nothing": "Nothing found",
      "calc.map_point": "Point on the map",
      "calc.cheapest": "cheapest",
      "calc.vehicle": "Van up to 3.5 t",
      "unit.km": "km",
      "unit.hour": "h",
      "unit.min": "min",
      "unit.uah": "UAH",
      "unit.uah_hour": "UAH/hour",
      "quote.return": "There and back",
      "quote.return_note": "A loaded return leg costs a quarter of the outbound price — the van is making that journey anyway.",
      "quote.abroad": "International trip",
      "quote.abroad_note": "{km} km of total mileage × €{rate} — that is €{oneway}/km if you count the distance one way.",
      "price.abroad_note": "{km} km there and back × €{rate} (€{oneway}/km on the one-way distance)",
      "quote.intercity": "Intercity trip",
      "quote.intercity_note": "{rate} UAH/km · price for the delivery one way; the empty return leg is already included",
      "quote.local": "Kyiv and the region",
      "quote.local_value": "from {rate} UAH/hour",
      "quote.local_note": "Minimum {hours} hours + {feed} UAH callout. The total depends on how long loading takes — we confirm it on the call.",
      "price.hourly_note": "{feed} UAH callout + from {hours} h × {rate} UAH/hour",
      "price.feed": "Callout",
      "form.bad_phone": "Enter a valid phone number — 9 digits after +380.",
      "form.sending": "Sending…",
      "form.send_failed": "We could not send that. Try again, or give us a call.",
      "form.no_connection": "No connection to the server. Try again later, or give us a call.",
      "route.label": "Route",
      "route.distance": "Distance",
      "route.duration": "Driving time",
      "route.service": "Service",
      "route.price": "Estimated cost",
      "calc.click_hint": "<strong>Click the map</strong> to add a point to your route.",
      "calc.pending": "Point on the map…",
      "calc.remove": "Remove",
      "calc.via_ph": "Stop along the way (city or address)",
      "city.zhytomyr": "Zhytomyr",
      "city.cherkasy": "Cherkasy",
      "city.vinnytsia": "Vinnytsia",
      "city.rivne": "Rivne",
      "city.poltava": "Poltava",
      "city.zapor": "Zaporizhzhia",
      "city.chernivtsi": "Chernivtsi",
      "city.warszawa": "Warsaw",
      "city.krakow": "Kraków",
      "city.praha": "Prague",
      "city.bratislava": "Bratislava",
      "city.berlin": "Berlin",
      "city.kyiv": "Kyiv", "city.lviv": "Lviv", "city.odesa": "Odesa",
      "city.dnipro": "Dnipro", "city.kharkiv": "Kharkiv"
    }
  };

  // <html lang> — "uk-UA" / "ru-UA" / "en"; нам потрібні лише перші дві літери.
  var lang = (document.documentElement.getAttribute("lang") || "uk").slice(0, 2);
  if (!STRINGS[lang]) lang = "uk";

  global.VZ = global.VZ || {};
  global.VZ.lang = lang;

  /** t("calc.not_found", { label: "Броварі" }) */
  global.VZ.t = function (key, vars) {
    var s = STRINGS[lang][key];
    if (s === undefined) s = STRINGS.uk[key];
    if (s === undefined) return key;   // помітна поломка краща за порожнє місце
    if (vars) {
      Object.keys(vars).forEach(function (k) {
        s = s.replace("{" + k + "}", vars[k]);
      });
    }
    return s;
  };
})(window);
