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
      "svc.bus_taxi": "Вантажне таксі",
      "svc.bus_relocation": "Переїзд під ключ",
      "svc.bus_delivery": "Доставка меблів / техніки",
      "price.feed": "Виїзд",
      "price.min_order": "мін. замовлення",
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
      "svc.bus_taxi": "Грузовое такси",
      "svc.bus_relocation": "Переезд под ключ",
      "svc.bus_delivery": "Доставка мебели / техники",
      "price.feed": "Подача",
      "price.min_order": "мин. заказ",
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
      "svc.bus_taxi": "Van with driver",
      "svc.bus_relocation": "Full removal",
      "svc.bus_delivery": "Furniture & appliance delivery",
      "price.feed": "Callout",
      "price.min_order": "minimum booking",
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
