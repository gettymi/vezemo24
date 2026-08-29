/**
 * Розрахунок орієнтовної вартості перевезення.
 * Один транспорт — бус до 3,5 т. Логіку самоскида видалено: такої машини немає.
 * Формула бусу збережена без змін:
 *   виїзд + max(години, мінімум) × тариф/год + км × тариф/км
 */
(function (global) {
  "use strict";

  var T = function (k, v) {
    return global.VZ && global.VZ.t ? global.VZ.t(k, v) : k;
  };

  /** Виїзд (подача), грн. */
  var BUS_FEED_UAH = 799;
  /** Пальне на довгих маршрутах, грн/км. */
  var BUS_PRICE_PER_KM_UAH = 3;
  /** Мінімальна оплачувана кількість годин. */
  var BUS_MIN_HOURS = 2;

  /** Тариф за годину для кожної послуги, грн. */
  /* Підписи більше не зашиті: беруться з i18n.js за поточною мовою.
     Тарифи однакові для всіх мов — ціна від мови не залежить. */
  var BUS_SERVICE_CONFIG = {
    bus_taxi:       { hourlyRate: 799,  labelKey: "svc.bus_taxi" },
    bus_relocation: { hourlyRate: 1099, labelKey: "svc.bus_relocation" },
    bus_delivery:   { hourlyRate: 859,  labelKey: "svc.bus_delivery" },
  };

  var METERS_PER_KM = 1000;
  var SECONDS_PER_HOUR = 3600;

  /**
   * @param {number} distanceInMeters   Довжина маршруту (з OSRM).
   * @param {number} durationInSeconds  Час у дорозі.
   * @param {string} [serviceType]      Лишений для сумісності — завжди "BUS".
   * @param {{ busServiceId?: string }} [options]
   * @returns {{total:number, breakdown:string, distanceKm:number, durationHours:number}}
   */
  function calculate(distanceInMeters, durationInSeconds, serviceType, options) {
    var distanceKm = (distanceInMeters || 0) / METERS_PER_KM;
    var durationHours = (durationInSeconds || 0) / SECONDS_PER_HOUR;
    var serviceId = (options && options.busServiceId) || "bus_taxi";
    return calculateBusByService(serviceId, distanceKm, durationHours);
  }

  function calculateBusByService(serviceId, distanceKm, durationHours) {
    var config = BUS_SERVICE_CONFIG[serviceId] || BUS_SERVICE_CONFIG.bus_taxi;
    var feed = BUS_FEED_UAH;
    var hourly = config.hourlyRate;
    var minH = BUS_MIN_HOURS;
    var perKm = BUS_PRICE_PER_KM_UAH;

    var billableHours = Math.max(durationHours, minH);
    var hoursPart = billableHours * hourly;
    var kmPart = distanceKm * perKm;
    var total = feed + hoursPart + kmPart;
    var minTotal = feed + minH * hourly;

    var roundedHours = Math.round(billableHours * 100) / 100;
    var uah = T("unit.uah");
    var breakdown =
      T("price.feed") + " " + feed + " " + uah + " + " +
      roundedHours + " " + T("unit.hour") + " × " + hourly + " " + uah + " + " +
      distanceKm.toFixed(1).replace(/\.0$/, "") + " " + T("unit.km") + " × " + perKm + " " + uah;

    if (total < minTotal) {
      total = minTotal;
      breakdown += " = " + total + " " + uah + " (" + T("price.min_order") + ")";
    } else {
      breakdown += " = " + Math.round(total) + " " + uah;
    }

    return {
      total: Math.round(total),
      breakdown: breakdown,
      distanceKm: distanceKm,
      durationHours: durationHours,
    };
  }

  /** Лишено для сумісності з map.js: транспорт тепер один. */
  function serviceTypeFromVehicle() {
    return "BUS";
  }

  function getHourlyRate(serviceType, serviceId) {
    var config = BUS_SERVICE_CONFIG[serviceId];
    return config ? config.hourlyRate : null;
  }

  global.PriceCalculator = {
    calculate: calculate,
    serviceTypeFromVehicle: serviceTypeFromVehicle,
    getHourlyRate: getHourlyRate,
    /* Підписи підставляються в момент виклику, а не при завантаженні файлу:
       так вони точно збігаються з мовою сторінки. */
    getBusServiceConfig: function () {
      var out = {};
      Object.keys(BUS_SERVICE_CONFIG).forEach(function (id) {
        var c = BUS_SERVICE_CONFIG[id];
        out[id] = { hourlyRate: c.hourlyRate, label: T(c.labelKey) };
      });
      return out;
    },
    constants: {
      BUS_FEED_UAH: BUS_FEED_UAH,
      BUS_MIN_HOURS: BUS_MIN_HOURS,
      BUS_PRICE_PER_KM_UAH: BUS_PRICE_PER_KM_UAH,
    },
  };
})(typeof window !== "undefined" ? window : typeof global !== "undefined" ? global : this);
