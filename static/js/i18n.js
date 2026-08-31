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
      "quote.return_note": "Ціна, якщо машина везе вантаж і в зворотний бік. Дешевше, ніж два окремі рейси.",
      "quote.abroad": "Закордонний рейс",
      "quote.abroad_note": "Ціна за рейс туди й назад. Фіксуємо до виїзду.",
      "quote.intercity": "Міжміський рейс",
      "quote.intercity_note": "Ціна за доставку в один бік — зворотний пробіг уже враховано.",
      "quote.local": "По Києву та області",
      "quote.local_value": "від {rate} грн/год",
      "quote.local_note": "Плюс подача {feed} грн. Підсумок назвемо в розмові.",
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
      "calc.via_ph": "Проміжна точка",
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
      "quote.return_note": "Цена, если машина везёт груз и в обратную сторону. Дешевле, чем два отдельных рейса.",
      "quote.abroad": "Заграничный рейс",
      "quote.abroad_note": "Цена за рейс туда и обратно. Фиксируем до выезда.",
      "quote.intercity": "Междугородний рейс",
      "quote.intercity_note": "Цена за доставку в один конец — обратный пробег уже учтён.",
      "quote.local": "По Киеву и области",
      "quote.local_value": "от {rate} грн/час",
      "quote.local_note": "Плюс подача {feed} грн. Итог назовём в разговоре.",
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
      "calc.via_ph": "Промежуточная точка",
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
      "quote.return_note": "The price when the van carries a load back as well. Cheaper than two separate trips.",
      "quote.abroad": "International trip",
      "quote.abroad_note": "The price covers the trip out and back. Fixed before departure.",
      "quote.intercity": "Intercity trip",
      "quote.intercity_note": "The price covers the one-way delivery; the return leg is already in it.",
      "quote.local": "Kyiv and the region",
      "quote.local_value": "from {rate} UAH/hour",
      "quote.local_note": "Plus a {feed} UAH call-out fee. We name the total on the call.",
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
