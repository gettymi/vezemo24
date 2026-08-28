/**
 * Розрахунок орієнтовної вартості перевезення.
 * Один транспорт — бус до 3,5 т. Логіку самоскида видалено: такої машини немає.
 * Формула бусу збережена без змін:
 *   виїзд + max(години, мінімум) × тариф/год + км × тариф/км
 */
(function (global) {
  "use strict";

  /** Виїзд (подача), грн. */
  var BUS_FEED_UAH = 799;
  /** Пальне на довгих маршрутах, грн/км. */
  var BUS_PRICE_PER_KM_UAH = 3;
  /** Мінімальна оплачувана кількість годин. */
  var BUS_MIN_HOURS = 2;

  /** Тариф за годину для кожної послуги, грн. */
  var BUS_SERVICE_CONFIG = {
    bus_taxi:       { hourlyRate: 799,  label: "Вантажне таксі" },
    bus_relocation: { hourlyRate: 1099, label: "Переїзд під ключ" },
    bus_delivery:   { hourlyRate: 859,  label: "Доставка меблів / техніки" },
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
    var breakdown =
      "Виїзд " + feed + " грн + " + roundedHours + " год × " + hourly +
      " грн + " + distanceKm.toFixed(1) + " км × " + perKm + " грн";

    if (total < minTotal) {
      total = minTotal;
      breakdown += " = " + total + " грн (мін. замовлення)";
    } else {
      breakdown += " = " + Math.round(total) + " грн";
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
    getBusServiceConfig: function () { return BUS_SERVICE_CONFIG; },
    constants: {
      BUS_FEED_UAH: BUS_FEED_UAH,
      BUS_MIN_HOURS: BUS_MIN_HOURS,
      BUS_PRICE_PER_KM_UAH: BUS_PRICE_PER_KM_UAH,
    },
  };
})(typeof window !== "undefined" ? window : typeof global !== "undefined" ? global : this);
