/**
 * Поле телефону для України — без зовнішніх бібліотек.
 * Замінює intl-tel-input (~200 КБ з CDN + власні стилі, які доводилось
 * перебивати двадцятьма !important).
 *
 * Приймає будь-який звичний формат вводу: 0671234567, +380671234567,
 * 380671234567, 067 123 45 67 — і показує як +380 67 123 45 67.
 * Остаточну перевірку все одно робить сервер (phonenumbers).
 */
(function (global) {
  "use strict";

  var NDC_LEN = 2;          // код оператора після 380 (напр. 67)
  var SUBSCRIBER_LEN = 7;   // решта номера
  var TOTAL = NDC_LEN + SUBSCRIBER_LEN; // 9 цифр після 380

  /** Лишає самі цифри національного номера (без 380). */
  function normalize(raw) {
    var d = (raw || "").replace(/\D/g, "");
    if (d.indexOf("380") === 0) d = d.slice(3);
    else if (d.indexOf("80") === 0) d = d.slice(2);
    else if (d.charAt(0) === "0") d = d.slice(1);
    return d.slice(0, TOTAL);
  }

  /** +380 67 123 45 67 */
  function format(digits) {
    if (!digits) return "";
    var out = "+380";
    if (digits.length) out += " " + digits.slice(0, 2);
    if (digits.length > 2) out += " " + digits.slice(2, 5);
    if (digits.length > 5) out += " " + digits.slice(5, 7);
    if (digits.length > 7) out += " " + digits.slice(7, 9);
    return out;
  }

  function isValid(digits) {
    return digits.length === TOTAL;
  }

  function e164(digits) {
    return "+380" + digits;
  }

  function attach(input) {
    if (!input) return null;

    input.setAttribute("inputmode", "tel");
    input.setAttribute("autocomplete", "tel");
    if (!input.placeholder) input.placeholder = "+380 67 123 45 67";

    var state = { digits: normalize(input.value) };

    function render(keepCaretAtEnd) {
      input.value = format(state.digits);
      if (keepCaretAtEnd) {
        var end = input.value.length;
        try { input.setSelectionRange(end, end); } catch (e) { /* не всі типи підтримують */ }
      }
    }

    input.addEventListener("focus", function () {
      if (!state.digits) render(true);
    });

    input.addEventListener("input", function () {
      state.digits = normalize(input.value);
      render(true);
      input.classList.remove("is-error");
      if (isValid(state.digits)) input.classList.add("is-valid");
      else input.classList.remove("is-valid");
    });

    input.addEventListener("blur", function () {
      if (!state.digits) { input.value = ""; input.classList.remove("is-valid", "is-error"); return; }
      render(false);
      input.classList.toggle("is-valid", isValid(state.digits));
      input.classList.toggle("is-error", !isValid(state.digits));
    });

    // Backspace на порожньому хвості не має залишати «+380 »
    input.addEventListener("keydown", function (e) {
      if (e.key === "Backspace" && normalize(input.value).length === 0) {
        input.value = "";
      }
    });

    return {
      isValid: function () { return isValid(state.digits); },
      getNumber: function () { return isValid(state.digits) ? e164(state.digits) : ""; },
      getDigits: function () { return state.digits; },
    };
  }

  global.PhoneField = { attach: attach, normalize: normalize, format: format, isValid: isValid, e164: e164 };
})(typeof window !== "undefined" ? window : this);
