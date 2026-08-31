/**
 * Режим «Київ та область» у калькуляторі: години → ціна.
 *
 * Чому окремий файл, а не всередині map.js. По місту й області маршрут не
 * потрібен узагалі — платять за час, а не за кілометри. Тримати цей режим
 * поруч із картою означало б, що впала Leaflet — і людина не може порахувати
 * навіть найпростіше. Тут немає жодної залежності від карти, а перемикач
 * режимів працює, навіть якщо map.js не завантажився.
 *
 * Ціну на два (мінімальні) години вже намалював сервер, тому вона видна ще
 * до виконання цього скрипта. Тут лише перерахунок на кліку.
 */
(function () {
  "use strict";

  var local = document.getElementById("mode-local");
  var route = document.getElementById("mode-route");
  var btnLocal = document.getElementById("mode-btn-local");
  var btnRoute = document.getElementById("mode-btn-route");
  if (!local || !route || !btnLocal || !btnRoute) return;

  /* ── Перемикач режимів ─────────────────────────────────────────────── */
  function show(which) {
    var isLocal = which === "local";
    local.hidden = !isLocal;
    route.hidden = isLocal;
    btnLocal.classList.toggle("is-active", isLocal);
    btnRoute.classList.toggle("is-active", !isLocal);
    btnLocal.setAttribute("aria-selected", String(isLocal));
    btnRoute.setAttribute("aria-selected", String(!isLocal));
    // Карті треба сказати, що її контейнер змінив розмір, інакше після
    // перемикання вона малює тайли в старих межах і лишає сірі смуги.
    if (!isLocal) window.dispatchEvent(new Event("resize"));
  }
  btnLocal.addEventListener("click", function () { show("local"); });
  btnRoute.addEventListener("click", function () { show("route"); });

  /* Зі сторінок міст і напрямків приходять із готовим маршрутом — тоді
     показуємо саме його, а не погодинний режим. */
  var q = new URLSearchParams(window.location.search);
  if (q.get("route") || q.get("lat")) show("route");

  /* ── Години → ціна ─────────────────────────────────────────────────── */
  var out = document.getElementById("hours-value");
  var total = document.getElementById("local-total");
  var minus = document.getElementById("hours-minus");
  var plus = document.getElementById("hours-plus");
  if (!out || !total || !minus || !plus) return;

  var L = (window.PriceCalculator && window.PriceCalculator.constants &&
           window.PriceCalculator.constants.LOCAL) || null;
  if (!L) return;   // без тарифів рахувати нічого — лишаємо те, що віддав сервер

  var MIN = L.minHours;
  var MAX = 12;     // довше за робочий день — це вже інша розмова, не калькулятор
  var hours = parseInt(out.textContent, 10) || MIN;

  function money(n) {
    // Нерозривний пробіл між тисячами: інакше «3 200 грн» переноситься
    // посеред числа.
    return String(Math.round(n)).replace(/\B(?=(\d{3})+(?!\d))/g, " ");
  }

  function uah() {
    var el = total.textContent.match(/[^\d\s ]+\s*$/);
    return el ? el[0].trim() : "";
  }
  var UNIT = uah();

  function render() {
    out.textContent = hours;
    total.textContent = money(L.feed + hours * L.hourly) + " " + UNIT;
    minus.disabled = hours <= MIN;
    plus.disabled = hours >= MAX;
  }

  minus.addEventListener("click", function () {
    if (hours > MIN) { hours -= 1; render(); }
  });
  plus.addEventListener("click", function () {
    if (hours < MAX) { hours += 1; render(); }
  });

  render();
})();
