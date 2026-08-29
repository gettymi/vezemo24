/**
 * Розрахунок вартості. Дві моделі, бо це справді дві різні послуги.
 *
 * ПО КИЄВУ Й ОБЛАСТІ машина не стільки їде, скільки СТОЇТЬ: чекає, поки
 * завантажать і розвантажать. Тому рахунок за годинами. Скільки триватиме
 * завантаження, сайт знати не може — тому підсумок тут НЕ вигадується.
 * Показуємо ставку й мінімум, точну суму називають у розмові. Раніше
 * калькулятор брав час у дорозі з OSRM і видавав його за тривалість
 * роботи — для переїзду це просто неправда.
 *
 * МІЖМІСЬКИЙ РЕЙС — це кілометри: машина їде, а не чекає. Відстань відома,
 * тому підсумок рахується чесно й показується цифрою.
 *
 * Ціна міжміського — за відстань В ОДИН БІК. Порожній зворотний пробіг уже
 * закладений у ставку, окремо він не додається.
 */
(function (global) {
  "use strict";

  var T = function (k, v) {
    return global.VZ && global.VZ.t ? global.VZ.t(k, v) : k;
  };

  /** Погодинно: Київ і область. */
  var LOCAL = {
    hourly: 799,      // грн/год
    feed: 799,        // подача, грн
    minHours: 2,      // мінімальна оплачувана кількість годин
  };

  /** Покілометрово: міжміські рейси по Україні. */
  var INTERCITY = {
    // Єдина ставка на будь-яку відстань. Мінімального замовлення НЕМАЄ.
    perKm: 37,        // грн/км, за відстань в один бік
  };

  /* Зворотний рейс із вантажем — чверть від ціни «туди»: машина однаково
     їде цим шляхом, платити повну ціну двічі не за що. */
  var RETURN_SHARE = 0.25;

  /* Закордон: євро за кілометр ПОВНОГО пробігу (туди й назад). Через
     кордон порожній зворотний рейс не окупається нічим, тому платним є
     весь пробіг. Захід Європи дорожчий: пальне й платні автобани. */
  var ABROAD = {
    east: { perTotalKm: 0.60 },   // Польща, Чехія, Словаччина
    west: { perTotalKm: 0.70 },   // Німеччина, Франція, Італія, Іспанія
  };

  /**
   * Межа між «область» і «міжмісто». Київська область закінчується
   * приблизно тут, тож далі погодинна модель втрачає сенс: ніхто не
   * наймає бус погодинно, щоб поїхати за 300 км.
   */
  var INTERCITY_FROM_KM = 120;

  var METERS_PER_KM = 1000;

  /**
   * @param {number} distanceInMeters відстань в один бік (з OSRM)
   * @returns {{mode:string, distanceKm:number, ...}}
   */
  function quote(distanceInMeters, zone) {
    if (zone) return quoteAbroad(distanceInMeters, zone);
    var km = (distanceInMeters || 0) / METERS_PER_KM;

    if (km < INTERCITY_FROM_KM) {
      return {
        mode: "hourly",
        distanceKm: km,
        hourly: LOCAL.hourly,
        feed: LOCAL.feed,
        minHours: LOCAL.minHours,
        // Найменше, що взагалі може вийти: подача + мінімальні години.
        floor: LOCAL.feed + LOCAL.minHours * LOCAL.hourly,
      };
    }

    var total = Math.round(km * INTERCITY.perKm);
    return {
      mode: "intercity",
      distanceKm: km,
      perKm: INTERCITY.perKm,
      total: total,
      totalReturn: Math.round(total * (1 + RETURN_SHARE)),
      returnShare: RETURN_SHARE,
    };
  }

  /**
   * Закордонний рейс. km — відстань В ОДИН БІК; платним є подвійний
   * пробіг, бо машина повертається.
   */
  function quoteAbroad(distanceInMeters, zone) {
    var km = (distanceInMeters || 0) / METERS_PER_KM;
    var z = ABROAD[zone] || ABROAD.east;
    var totalKm = km * 2;
    return {
      mode: "abroad",
      distanceKm: km,
      totalKm: Math.round(totalKm),
      perTotalKm: z.perTotalKm,
      perOneWayKm: Math.round(z.perTotalKm * 200) / 100,
      eur: Math.round(totalKm * z.perTotalKm),
      zone: zone || "east",
    };
  }

  /** Рядок-пояснення, звідки взялася сума. */
  function explain(q) {
    if (q.mode === "abroad") {
      return T("price.abroad_note", {
        km: q.totalKm, rate: q.perTotalKm.toFixed(2).replace(".", ","),
        oneway: q.perOneWayKm.toFixed(2).replace(".", ","),
      });
    }
    if (q.mode === "intercity") {
      var uah = T("unit.uah");
      var money = function (n) {
        return String(Math.round(n)).replace(/\B(?=(\d{3})+(?!\d))/g, "\u00a0");
      };
      var base = Math.round(q.distanceKm) + " " + T("unit.km") + " × " +
                 q.perKm + " " + uah;
      return base + " = " + money(q.total) + " " + uah;
    }
    return T("price.hourly_note", {
      feed: q.feed, hours: q.minHours, rate: q.hourly,
    });
  }

  global.PriceCalculator = {
    quote: quote,
    explain: explain,
    quoteAbroad: quoteAbroad,
    constants: {
      LOCAL: LOCAL,
      INTERCITY: INTERCITY,
      INTERCITY_FROM_KM: INTERCITY_FROM_KM,
      RETURN_SHARE: RETURN_SHARE,
      ABROAD: ABROAD,
    },
  };
})(typeof window !== "undefined" ? window : typeof global !== "undefined" ? global : this);
