/**
 * Поле телефону з вибором країни — без зовнішніх бібліотек.
 *
 * Чому не intl-tel-input: ~200 КБ із CDN, власні стилі, які доводилось
 * перебивати двадцятьма !important, і ще один зовнішній домен у критичному
 * шляху. Тут те саме поводження в 6 КБ і без жодного запиту.
 *
 * НАЗВИ КРАЇН НЕ ЗБЕРІГАЄМО. Їх дає Intl.DisplayNames, який є в браузері:
 * "PL" → «Польща» українською, «Польша» російською, «Poland» англійською.
 * Тому в даних лише код країни й телефонний префікс, а переклад трьома
 * мовами не коштує жодного байта й не може розійтися сам із собою.
 *
 * ПОРЯДОК У СПИСКУ. Спершу країни, куди ми справді їздимо і звідки нам
 * дзвонять, — це не географія, а робота: Україна, Польща, Чехія,
 * Словаччина, Німеччина, Молдова, Румунія, Угорщина. Далі решта за
 * абеткою мовою сторінки (Intl.Collator сортує «Ї» і «Є» правильно, чого
 * звичайний sort() не робить).
 *
 * ПЕРЕВІРКА. Клієнт стежить лише за довжиною: 6–15 цифр — стільки
 * дозволяє E.164. Справжню перевірку робить сервер бібліотекою
 * phonenumbers, бо правил у кожної країни свої й тягнути їх у браузер
 * означало б повернутися до тих самих 200 КБ.
 */
(function (global) {
  "use strict";

  /* Код країни → телефонний префікс. Тільки Європа та кілька країн, звідки
     реально бувають замовлення; повний світовий список — це ще 200 рядків
     заради випадків, яких не буває. */
  var DIAL = {
    UA: "380", PL: "48", CZ: "420", SK: "421", DE: "49", MD: "373", RO: "40", HU: "36",
    AT: "43", BE: "32", BG: "359", HR: "385", CY: "357", DK: "45", EE: "372", FI: "358",
    FR: "33", GB: "44", GR: "30", IE: "353", IT: "39", LV: "371", LT: "370", LU: "352",
    MT: "356", NL: "31", NO: "47", PT: "351", SI: "386", ES: "34", SE: "46", CH: "41",
    RS: "381", BA: "387", ME: "382", MK: "389", AL: "355", TR: "90", GE: "995", IS: "354",
    US: "1", CA: "1", IL: "972", AE: "971", KZ: "7"
  };
  /* Білорусі й росії у списку немає — це рішення власника, а не недогляд.

     Щоб відсутність країни в списку нікого не замикала, є режим RAW: номер,
     що починається з «+» і не збігається з жодним відомим префіксом,
     лишається як є, а перевіряє його сервер бібліотекою phonenumbers, яка
     знає всі країни світу. Тобто ми не пропонуємо — але й не блокуємо. */

  /* Показуються першими, у цьому порядку. */
  var TOP = ["UA", "PL", "CZ", "SK", "DE", "MD", "RO", "HU"];

  var DEFAULT_ISO = "UA";
  var STORE_KEY = "vezemo_phone_iso";

  /* ── Дрібні помічники ─────────────────────────────────────────────────── */

  function lang() {
    return (document.documentElement.getAttribute("lang") || "uk").slice(0, 2);
  }

  var displayNames = null;
  function countryName(iso) {
    if (displayNames === null) {
      try { displayNames = new Intl.DisplayNames([lang()], { type: "region" }); }
      catch (e) { displayNames = false; }
    }
    if (!displayNames) return iso;
    try { return displayNames.of(iso) || iso; } catch (e) { return iso; }
  }

  /* Прапорець — два «regional indicator» символи з коду країни. На Windows
     емодзі-прапорців немає, і там видно самі літери «UA». Це не поломка:
     саме тому поруч завжди стоїть префікс «+380», і зрозуміло без картинки. */
  function flag(iso) {
    return String.fromCodePoint.apply(null, iso.toUpperCase().split("").map(function (c) {
      return 0x1F1E6 + c.charCodeAt(0) - 65;
    }));
  }

  function remember(iso) {
    if (iso === RAW) return;      // «інша країна» запамʼятовувати нічого
    try { localStorage.setItem(STORE_KEY, iso); } catch (e) {}
  }
  function recall() {
    try { return DIAL[localStorage.getItem(STORE_KEY)] ? localStorage.getItem(STORE_KEY) : null; }
    catch (e) { return null; }
  }

  function sortedList() {
    var rest = Object.keys(DIAL).filter(function (i) { return TOP.indexOf(i) < 0; });
    try {
      var coll = new Intl.Collator(lang());
      rest.sort(function (a, b) { return coll.compare(countryName(a), countryName(b)); });
    } catch (e) { rest.sort(); }
    return { top: TOP.slice(), rest: rest };
  }

  /* ── Розбір і формат ──────────────────────────────────────────────────── */

  function digitsOf(raw) { return (raw || "").replace(/\D/g, ""); }

  /* Якщо людина вставила повний міжнародний номер — визначаємо країну самі,
     а не змушуємо шукати її в списку. Довші префікси перевіряємо першими,
     інакше "380" сплутається з "38". */
  var BY_DIAL = Object.keys(DIAL)
    .sort(function (a, b) { return DIAL[b].length - DIAL[a].length; });

  var RAW = "__raw";       // країна невідома, номер лишаємо як набрали

  function looksInternational(raw) {
    return (raw || "").charAt(0) === "+" || digitsOf(raw).indexOf("00") === 0;
  }

  function detect(raw) {
    if (!looksInternational(raw)) return null;
    var d = digitsOf(raw);
    if (d.indexOf("00") === 0) d = d.slice(2);
    for (var i = 0; i < BY_DIAL.length; i++) {
      if (d.indexOf(DIAL[BY_DIAL[i]]) === 0) return BY_DIAL[i];
    }
    return RAW;
  }

  /* Український номер розбиваємо групами — так його читають і диктують.
     Для решти країн правила різні, і вигадувати їх було б гірше, ніж
     лишити цифри як є. */
  function group(iso, d) {
    if (iso !== "UA") return d;
    var out = "";
    if (d.length) out += d.slice(0, 2);
    if (d.length > 2) out += " " + d.slice(2, 5);
    if (d.length > 5) out += " " + d.slice(5, 7);
    if (d.length > 7) out += " " + d.slice(7, 9);
    return out;
  }

  function maxLen(iso) {
    if (iso === RAW) return 15;
    return iso === "UA" ? 9 : 15 - DIAL[iso].length;
  }
  function minLen(iso) {
    if (iso === RAW) return 8;   // коротших міжнародних номерів не буває
    return iso === "UA" ? 9 : 6;
  }

  /* ── Побудова поля ────────────────────────────────────────────────────── */

  function attach(input) {
    if (!input || input.__phoneField) return input ? input.__phoneField : null;

    var T = function (k, fb) {
      return (global.VZ && global.VZ.t && global.VZ.t(k) !== k) ? global.VZ.t(k) : fb;
    };

    var iso = detect(input.value) || recall() || DEFAULT_ISO;
    var digits = digitsOf(input.value);
    if (iso !== RAW && digits.indexOf(DIAL[iso]) === 0) digits = digits.slice(DIAL[iso].length);
    digits = digits.slice(0, maxLen(iso));

    /* Обгортка навколо наявного input, щоб розмітка форми не змінювалась і
       все, що вже вміє форма (label for, автозаповнення), лишилось живим. */
    var wrap = document.createElement("div");
    wrap.className = "phone";
    input.parentNode.insertBefore(wrap, input);

    var btn = document.createElement("button");
    btn.type = "button";
    btn.className = "phone__country";
    btn.setAttribute("aria-haspopup", "listbox");
    btn.setAttribute("aria-expanded", "false");
    btn.setAttribute("aria-label", T("form.country", "Код країни"));

    var pop = document.createElement("div");
    pop.className = "phone__pop";
    pop.hidden = true;

    var search = document.createElement("input");
    search.type = "text";
    search.className = "phone__search";
    search.setAttribute("autocomplete", "off");
    search.placeholder = T("form.country_search", "Пошук країни");

    var list = document.createElement("ul");
    list.className = "phone__list";
    list.setAttribute("role", "listbox");

    pop.appendChild(search);
    pop.appendChild(list);
    wrap.appendChild(btn);
    wrap.appendChild(input);
    wrap.appendChild(pop);

    input.setAttribute("inputmode", "tel");
    input.setAttribute("autocomplete", "tel");
    input.classList.add("phone__input");

    function renderButton() {
      btn.innerHTML = "";
      var f = document.createElement("span");
      f.className = "phone__flag";
      f.textContent = iso === RAW ? "\uD83C\uDF10" : flag(iso);   // глобус
      var d = document.createElement("span");
      d.className = "phone__dial";
      d.textContent = iso === RAW ? "+" : "+" + DIAL[iso];
      btn.appendChild(f);
      btn.appendChild(d);
      input.placeholder = iso === "UA" ? "67 123 45 67" : T("form.phone_ph2", "номер");
      btn.title = iso === RAW ? T("form.country_other", "Інша країна") : countryName(iso);
    }

    function renderInput(caretEnd) {
      input.value = group(iso, digits);
      if (caretEnd) {
        try { input.setSelectionRange(input.value.length, input.value.length); } catch (e) {}
      }
      input.classList.toggle("is-valid", valid());
      if (valid()) input.classList.remove("is-error");
    }

    function valid() { return digits.length >= minLen(iso) && digits.length <= maxLen(iso); }
    function e164() {
      if (!valid()) return "";
      return iso === RAW ? "+" + digits : "+" + DIAL[iso] + digits;
    }

    /* ── Список країн ───────────────────────────────────────────────────── */
    function renderList(query) {
      var q = (query || "").trim().toLowerCase();
      list.innerHTML = "";
      var data = sortedList();

      function row(code, isTop) {
        var li = document.createElement("li");
        li.className = "phone__opt" + (code === iso ? " is-current" : "");
        li.setAttribute("role", "option");
        li.setAttribute("data-iso", code);
        li.setAttribute("aria-selected", code === iso ? "true" : "false");
        li.tabIndex = -1;
        li.innerHTML = '<span class="phone__flag">' + flag(code) + "</span>" +
                       '<span class="phone__name"></span>' +
                       '<span class="phone__dial">+' + DIAL[code] + "</span>";
        li.querySelector(".phone__name").textContent = countryName(code);
        if (isTop) li.classList.add("is-top");
        return li;
      }

      function matches(code) {
        if (!q) return true;
        return countryName(code).toLowerCase().indexOf(q) === 0 ||
               countryName(code).toLowerCase().indexOf(" " + q) > -1 ||
               code.toLowerCase().indexOf(q) === 0 ||
               ("+" + DIAL[code]).indexOf(q) === 0 ||
               DIAL[code].indexOf(q.replace("+", "")) === 0;
      }

      var top = data.top.filter(matches);
      var rest = data.rest.filter(matches);

      /* Підпис «Куди возимо» показуємо лише поки не шукають: у результатах
         пошуку групування тільки заважає. */
      if (top.length && !q) {
        var h = document.createElement("li");
        h.className = "phone__group";
        h.setAttribute("role", "presentation");
        h.textContent = T("form.country_top", "Популярні");
        list.appendChild(h);
      }
      top.forEach(function (c) { list.appendChild(row(c, true)); });
      if (rest.length && !q) {
        var h2 = document.createElement("li");
        h2.className = "phone__group";
        h2.setAttribute("role", "presentation");
        h2.textContent = T("form.country_all", "Усі країни");
        list.appendChild(h2);
      }
      rest.forEach(function (c) { list.appendChild(row(c, false)); });

      if (!top.length && !rest.length) {
        var none = document.createElement("li");
        none.className = "phone__group";
        none.textContent = T("form.country_none", "Нічого не знайшли");
        list.appendChild(none);
      }
    }

    function open() {
      renderList("");
      search.value = "";
      pop.hidden = false;
      btn.setAttribute("aria-expanded", "true");
      var cur = list.querySelector(".is-current");
      if (cur) cur.scrollIntoView({ block: "nearest" });
      search.focus();
    }

    function close(focusInput) {
      pop.hidden = true;
      btn.setAttribute("aria-expanded", "false");
      if (focusInput) input.focus();
    }

    function choose(code) {
      if (!DIAL[code]) return;
      iso = code;
      remember(iso);
      digits = digits.slice(0, maxLen(iso));
      renderButton();
      renderInput(true);
      close(true);          // фокус одразу в номер — на один клік менше
    }

    /* ── Події ──────────────────────────────────────────────────────────── */
    btn.addEventListener("click", function () { pop.hidden ? open() : close(false); });

    search.addEventListener("input", function () { renderList(search.value); });

    search.addEventListener("keydown", function (e) {
      if (e.key === "Escape") { e.preventDefault(); close(true); return; }
      if (e.key === "ArrowDown") {
        e.preventDefault();
        var first = list.querySelector(".phone__opt");
        if (first) first.focus();
        return;
      }
      if (e.key === "Enter") {
        e.preventDefault();
        var only = list.querySelector(".phone__opt");
        if (only) choose(only.getAttribute("data-iso"));
      }
    });

    list.addEventListener("click", function (e) {
      var li = e.target.closest ? e.target.closest(".phone__opt") : null;
      if (li) choose(li.getAttribute("data-iso"));
    });

    list.addEventListener("keydown", function (e) {
      var li = e.target.closest ? e.target.closest(".phone__opt") : null;
      if (!li) return;
      if (e.key === "Enter" || e.key === " ") { e.preventDefault(); choose(li.getAttribute("data-iso")); }
      else if (e.key === "ArrowDown") { e.preventDefault(); var n = li.nextElementSibling; while (n && !n.classList.contains("phone__opt")) n = n.nextElementSibling; if (n) n.focus(); }
      else if (e.key === "ArrowUp") { e.preventDefault(); var p = li.previousElementSibling; while (p && !p.classList.contains("phone__opt")) p = p.previousElementSibling; if (p) p.focus(); else search.focus(); }
      else if (e.key === "Escape") { e.preventDefault(); close(true); }
    });

    document.addEventListener("click", function (e) {
      if (!pop.hidden && !wrap.contains(e.target)) close(false);
    });

    input.addEventListener("input", function () {
      /* Вставили повний міжнародний номер — перемикаємо країну самі. */
      var guess = detect(input.value);
      if (guess) {
        iso = guess;
        remember(iso);
        var d = digitsOf(input.value);
        if (d.indexOf("00") === 0) d = d.slice(2);
        digits = iso === RAW ? d.slice(0, 15)
                             : d.slice(DIAL[iso].length, DIAL[iso].length + maxLen(iso));
        renderButton();
      } else {
        var raw = digitsOf(input.value);
        /* 0671234567 → 671234567: український нуль перед кодом оператора. */
        if (iso === "UA" && raw.charAt(0) === "0") raw = raw.slice(1);
        if (iso === "UA" && raw.indexOf("380") === 0) raw = raw.slice(3);
        digits = raw.slice(0, maxLen(iso));
      }
      input.classList.remove("is-error");
      renderInput(true);
    });

    input.addEventListener("blur", function () {
      if (!digits) { input.value = ""; input.classList.remove("is-valid", "is-error"); return; }
      input.classList.toggle("is-valid", valid());
      input.classList.toggle("is-error", !valid());
    });

    renderButton();
    renderInput(false);

    var api = {
      isValid: valid,
      getNumber: e164,
      getDigits: function () { return digits; },
      getCountry: function () { return iso; },
    };
    input.__phoneField = api;
    return api;
  }

  global.PhoneField = { attach: attach, DIAL: DIAL, TOP: TOP };
})(typeof window !== "undefined" ? window : this);
