/**
 * Leaflet + OpenStreetMap + OSRM — побудова маршруту (відстань і час).
 * Без цінника; вартість розраховується індивідуально.
 */
(function () {
  "use strict";

  var KYIV = [50.4501, 30.5234];

  /* Готові напрямки з зашитими координатами. Сенс не лише в зручності:
     пресет не робить ЖОДНОГО запиту до геокодера, тож найпопулярніші
     маршрути рахуються миттєво й не витрачають ліміт Nominatim. */
  var PRESETS = [
    { label: "Київ → Львів",  a: ["Київ", 50.4501, 30.5234], b: ["Львів", 49.8397, 24.0297] },
    { label: "Київ → Одеса",  a: ["Київ", 50.4501, 30.5234], b: ["Одеса", 46.4825, 30.7233] },
    { label: "Київ → Дніпро", a: ["Київ", 50.4501, 30.5234], b: ["Дніпро", 48.4647, 35.0462] },
    { label: "Київ → Харків", a: ["Київ", 50.4501, 30.5234], b: ["Харків", 49.9935, 36.2304] },
  ];

  var SERVICE_ORDER = ["bus_taxi", "bus_delivery", "bus_relocation"];
  var selectedService = "bus_taxi";
  /* Геосервіси більше не викликаються з браузера напряму: усе йде через
     власні /api/geo/*, де є кеш, коректний User-Agent і дотримання
     інтервалу між запитами (див. routes/geo.py). */
  var GEO_SEARCH = "/api/geo/search";
  var GEO_REVERSE = "/api/geo/reverse";
  var GEO_ROUTE = "/api/geo/route";

  /* alert() блокує сторінку, виглядає як помилка браузера і не показує
     контексту. Тепер повідомлення живе в самій панелі. */
  /* Шари існують лише разом із картою. Без цієї перевірки будь-яка дія,
     що чистить маршрут, падала з TypeError, коли Leaflet не завантажився —
     і разом із нею вмирала вся форма. */
  /* «540.0 км» і «6 год 0 хв» виглядають як вивід налагодження.
     В українській десятковий роздільник — кома, а нульові хвилини зайві. */
  function formatKm(meters) {
    var km = (meters || 0) / 1000;
    var txt = km >= 100 ? String(Math.round(km)) : km.toFixed(1).replace(".", ",");
    return txt.replace(",0", "") + " км";
  }

  function formatDuration(seconds) {
    var total = Math.round((seconds || 0) / 60);
    var h = Math.floor(total / 60);
    var m = total % 60;
    if (h && m) return h + " год " + m + " хв";
    if (h) return h + " год";
    return m + " хв";
  }

  function clearMapLayers() {
    if (markersLayer) markersLayer.clearLayers();
    if (routeLayer) routeLayer.clearLayers();
  }

  function notice(msg, kind) {
    var box = document.getElementById("map-notice");
    if (!box) return;
    if (!msg) { box.classList.remove("is-shown"); box.textContent = ""; return; }
    box.textContent = msg;
    box.className = "notice notice--" + (kind || "error") + " is-shown";
  }

  /* Через серверний геокодер із витримкою в секунду маршрут може рахуватись
     кілька секунд. Без цього стану сторінка виглядала так, ніби нічого не
     сталось, і люди тиснули кнопку повторно. */
  function setBusy(on) {
    var btn = document.getElementById("build-route");
    if (!btn) return;
    btn.disabled = !!on;
    btn.classList.toggle("is-busy", !!on);
    if (on) {
      if (!btn.getAttribute("data-label")) btn.setAttribute("data-label", btn.textContent);
      btn.textContent = "Рахуємо…";
    } else if (btn.getAttribute("data-label")) {
      btn.textContent = btn.getAttribute("data-label");
    }
  }

  function getJSON(url) {
    return fetch(url, { headers: { Accept: "application/json" } })
      .then(function (r) { return r.ok ? r.json() : null; });
  }

  var map = null;
  var routeLayer = null;
  var markersLayer = null;
  var mapClickMode = false;
  var mapClickHint = null;
  var autocompleteDropdown = null;
  var autocompleteTimer = null;
  var lastSearchAbort = null;
  var currentRouteData = null; // { distance: meters, duration: seconds }

  /* Раніше все — і карта, і кнопки — піднімалось в одній функції, яка
     починалась із L.map(). Якщо Leaflet не завантажився, кидався
     ReferenceError і разом із картою вмирали «Розрахувати», «Очистити»
     та підказки адрес. Тепер контроли не залежать від карти. */
  function wireControls() {
    renderPresets();

    document.getElementById("add-point")?.addEventListener("click", addWayPoint);
    document.getElementById("build-route")?.addEventListener("click", buildRoute);
    document.getElementById("clear-route")?.addEventListener("click", clearRoute);

    createAutocompleteDropdown();
    document.querySelectorAll("#points-container .point__input").forEach(function (inp) {
      if (!inp.readOnly) setupAutocomplete(inp);
    });
  }

  function renderPresets() {
    var host = document.getElementById("presets");
    if (!host) return;
    PRESETS.forEach(function (preset) {
      var b = document.createElement("button");
      b.type = "button";
      b.className = "preset";
      b.textContent = preset.label;
      b.addEventListener("click", function () { applyPreset(preset); });
      host.appendChild(b);
    });
  }

  function applyPreset(preset) {
    clearRoute();
    var rows = document.querySelectorAll("#points-container .point");
    [preset.a, preset.b].forEach(function (pt, i) {
      var row = rows[i];
      if (!row) return;
      var input = row.querySelector(".point__input");
      input.value = pt[0];
      row.setAttribute("data-lat", pt[1]);
      row.setAttribute("data-lng", pt[2]);
    });
    buildRoute();
  }

  function showMapFallback() {
    var fb = document.getElementById("map-fallback");
    if (fb) fb.hidden = false;
    var btn = document.getElementById("add-point-map");
    if (btn) btn.hidden = true;   // без карти в цій кнопці немає сенсу
  }

  function initMap() {
    if (map) return;
    var el = document.getElementById("map");
    if (!el) return;

    if (typeof L === "undefined") {
      showMapFallback();
      return;   // форма далі працює — карта тут не обов'язкова
    }

    document.getElementById("add-point-map")?.addEventListener("click", enableMapClickMode);

    map = L.map("map", {
      center: KYIV,
      zoom: 10,
      zoomControl: true,
    });
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
    }).addTo(map);

    markersLayer = L.layerGroup().addTo(map);
    routeLayer = L.layerGroup().addTo(map);

    map.on("click", onMapClick);
  }

  function createAutocompleteDropdown() {
    if (autocompleteDropdown) return;
    autocompleteDropdown = document.createElement("div");
    autocompleteDropdown.className = "suggest";
    autocompleteDropdown.setAttribute("role", "listbox");
    document.body.appendChild(autocompleteDropdown);
  }

  function searchAddresses(query) {
    if (!query || query.length < 2) return Promise.resolve([]);
    var params = new URLSearchParams({ q: query, limit: 6 });
    return getJSON(GEO_SEARCH + "?" + params)
      .then(function (data) {
        return data && Array.isArray(data.results) ? data.results : [];
      })
      .catch(function () { return []; });
  }

  function showAutocomplete(input, results) {
    if (!autocompleteDropdown) return;
    var rect = input.getBoundingClientRect();
    autocompleteDropdown.style.left = rect.left + "px";
    autocompleteDropdown.style.top = (rect.bottom + 2) + "px";
    autocompleteDropdown.style.width = Math.max(rect.width, 280) + "px";
    autocompleteDropdown.innerHTML = "";
    if (!results.length) {
      autocompleteDropdown.classList.add("suggest--empty");
      autocompleteDropdown.innerHTML = '<div class="suggest__item suggest__item--hint">Нічого не знайдено</div>';
    } else {
      autocompleteDropdown.classList.remove("suggest--empty");
      results.forEach(function (r) {
        var div = document.createElement("div");
        div.className = "suggest__item";
        div.setAttribute("role", "option");
        div.textContent = r.display;
        div.addEventListener("click", function () {
          selectAutocompleteItem(input, r);
        });
        autocompleteDropdown.appendChild(div);
      });
    }
    autocompleteDropdown.style.display = "block";
  }

  function selectAutocompleteItem(input, item) {
    input.value = item.display;
    var row = input.closest(".point");
    if (row && !row.classList.contains("point--map")) {
      row.setAttribute("data-lat", item.lat);
      row.setAttribute("data-lng", item.lng);
    }
    hideAutocomplete();
    input.blur();
  }

  function hideAutocomplete() {
    if (autocompleteDropdown) autocompleteDropdown.style.display = "none";
  }

  function setupAutocomplete(input) {
    if (input._autocompleteSetup) return;
    input._autocompleteSetup = true;

    input.addEventListener("input", function () {
      var row = input.closest(".point");
      if (row && row.getAttribute("data-lat") != null) {
        row.removeAttribute("data-lat");
        row.removeAttribute("data-lng");
        row.classList.remove("point--map");
        if (row._mapMarker && row._mapMarker.remove) row._mapMarker.remove();
        row._mapMarker = null;
      }
      if (row && row.classList.contains("point--map")) return;
      if (autocompleteTimer) clearTimeout(autocompleteTimer);
      var value = input.value.trim();
      if (value.length < 2) {
        hideAutocomplete();
        if (row) { row.removeAttribute("data-lat"); row.removeAttribute("data-lng"); }
        return;
      }
      autocompleteTimer = setTimeout(function () {
        autocompleteTimer = null;
        searchAddresses(value).then(function (results) {
          showAutocomplete(input, results);
        });
      }, 600);
    });

    input.addEventListener("focus", function () {
      var value = input.value.trim();
      if (value.length >= 2) searchAddresses(value).then(function (results) { showAutocomplete(input, results); });
    });

    input.addEventListener("blur", function () {
      setTimeout(hideAutocomplete, 220);
    });

    input.addEventListener("keydown", function (e) {
      if (e.key === "Escape") { hideAutocomplete(); return; }
      if (!autocompleteDropdown || autocompleteDropdown.style.display !== "block") return;

      var items = autocompleteDropdown.querySelectorAll(".suggest__item:not(.suggest__item--hint)");
      if (!items.length) return;
      var current = -1;
      items.forEach(function (el, i) { if (el.classList.contains("is-active")) current = i; });

      if (e.key === "ArrowDown" || e.key === "ArrowUp") {
        e.preventDefault();
        var next = e.key === "ArrowDown" ? current + 1 : current - 1;
        if (next < 0) next = items.length - 1;
        if (next >= items.length) next = 0;
        items.forEach(function (el) { el.classList.remove("is-active"); });
        items[next].classList.add("is-active");
        items[next].scrollIntoView({ block: "nearest" });
      } else if (e.key === "Enter" && current >= 0) {
        e.preventDefault();
        items[current].click();
      }
    });
  }

  function geocode(query) {
    var params = new URLSearchParams({ q: query, limit: 1 });
    return getJSON(GEO_SEARCH + "?" + params)
      .then(function (data) {
        var hit = data && data.results && data.results[0];
        return hit || null;
      })
      .catch(function () { return null; });
  }

  function reverseGeocode(lat, lng) {
    var params = new URLSearchParams({ lat: lat, lon: lng });
    return getJSON(GEO_REVERSE + "?" + params)
      .then(function (data) {
        return (data && data.display) || "Точка на карті";
      })
      .catch(function () { return "Точка на карті"; });
  }

  function enableMapClickMode() {
    mapClickMode = true;
    if (mapClickHint) mapClickHint.remove();
    mapClickHint = L.popup({ closeButton: true, autoClose: false })
      .setLatLng(map.getCenter())
      .setContent("<strong>Натисніть на карту</strong>, щоб додати точку маршруту.")
      .openOn(map);
    if (!map) return;
    map.getContainer().classList.add("map-picking");
  }

  function onMapClick(e) {
    if (!mapClickMode) return;
    mapClickMode = false;
    map.getContainer().classList.remove("map-picking");
    if (mapClickHint) {
      mapClickHint.remove();
      mapClickHint = null;
    }
    var lat = e.latlng.lat;
    var lng = e.latlng.lng;
    var container = document.getElementById("points-container");
    var rows = Array.from(container.querySelectorAll(".point"));
    if (rows.length === 0) return;
    var firstRow = rows[0];
    var lastRow = rows[rows.length - 1];
    function rowIsEmpty(row) {
      var inp = row.querySelector(".point__input");
      var hasCoords = row.getAttribute("data-lat") != null && row.getAttribute("data-lng") != null;
      var hasValue = inp && inp.value.trim().length > 0;
      return !hasCoords && !hasValue;
    }
    if (rowIsEmpty(firstRow)) {
      fillRowWithMapPoint(firstRow, lat, lng);
      return;
    }
    if (rows.length >= 2 && rowIsEmpty(lastRow)) {
      fillRowWithMapPoint(lastRow, lat, lng);
      return;
    }
    addRowFromMapClick(lat, lng);
  }

  function fillRowWithMapPoint(row, lat, lng) {
    if (row._mapMarker && row._mapMarker.remove) row._mapMarker.remove();
    row.setAttribute("data-lat", lat);
    row.setAttribute("data-lng", lng);
    row.classList.add("point--map");
    var inp = row.querySelector(".point__input");
    if (!inp) return;
    inp.value = "Точка на карті…";
    reverseGeocode(lat, lng).then(function (label) {
      inp.value = label;
    });
    var marker = L.marker([lat, lng]).addTo(markersLayer);
    marker.bindPopup(inp.value || "Точка на карті");
    row._mapMarker = marker;
  }

  function addRowFromMapClick(lat, lng) {
    var container = document.getElementById("points-container");
    var rows = container.querySelectorAll(".point");
    var lastRow = rows[rows.length - 1];

    var div = document.createElement("div");
    div.className = "point point--map";
    div.setAttribute("data-lat", lat);
    div.setAttribute("data-lng", lng);
    div.innerHTML =
      '<div class="point__pin point__pin--via">•</div>' +
      '<input type="text" class="point__input" placeholder="Точка на карті" readonly>' +
      '<button class="point__remove" title="Видалити">✕</button>';
    var inp = div.querySelector(".point__input");
    inp.value = "Точка на карті…";
    reverseGeocode(lat, lng).then(function (label) {
      inp.value = label;
    });
    var marker = L.marker([lat, lng]).addTo(markersLayer);
    marker.bindPopup(inp.value || "Точка на карті");
    div._mapMarker = marker;
    div.querySelector(".point__remove").addEventListener("click", function () {
      if (div._mapMarker && div._mapMarker.remove) div._mapMarker.remove();
      div.remove();
    });
    container.insertBefore(div, lastRow);

    inp.addEventListener("change", function () {
      marker.getPopup().setContent(inp.value || "Точка на карті");
    });
  }

  function clearRoute() {
    var container = document.getElementById("points-container");
    if (!container) return;
    var rows = Array.from(container.querySelectorAll(".point"));
    rows.forEach(function (row, i) {
      if (row._mapMarker && row._mapMarker.remove) row._mapMarker.remove();
      row._mapMarker = null;
      if (i > 1) row.remove();
    });
    var first = rows[0];
    var second = rows[1];
    if (first) {
      var inp1 = first.querySelector(".point__input");
      if (inp1) { inp1.value = ""; inp1.readOnly = false; }
      first.removeAttribute("data-lat");
      first.removeAttribute("data-lng");
      first.classList.remove("point--map");
    }
    if (second) {
      var inp2 = second.querySelector(".point__input");
      if (inp2) { inp2.value = ""; inp2.readOnly = false; }
      second.removeAttribute("data-lat");
      second.removeAttribute("data-lng");
      second.classList.remove("point--map");
    }
    clearMapLayers();
    currentRouteData = null;
    var resCard = document.getElementById("route-result");
    if (resCard) resCard.classList.remove("is-shown");
  }

  function addWayPoint() {
    var container = document.getElementById("points-container");
    var rows = container.querySelectorAll(".point");
    var lastRow = rows[rows.length - 1];

    var div = document.createElement("div");
    div.className = "point";
    div.innerHTML =
      '<div class="point__pin point__pin--via">•</div>' +
      '<input type="text" class="point__input" placeholder="Проміжна точка (місто або адреса)" autocomplete="off">' +
      '<button class="point__remove" title="Видалити">✕</button>';
    var inp = div.querySelector(".point__input");
    div.querySelector(".point__remove").addEventListener("click", function () {
      div.remove();
    });
    container.insertBefore(div, lastRow);
    setupAutocomplete(inp);
  }

  function getOrderedPoints() {
    var rows = Array.from(document.querySelectorAll("#points-container .point"));
    return rows.map(function (row) {
      var lat = row.getAttribute("data-lat");
      var lng = row.getAttribute("data-lng");
      var input = row.querySelector(".point__input");
      var value = input ? input.value.trim() : "";
      if (lat != null && lng != null) {
        return { type: "coords", lat: parseFloat(lat), lng: parseFloat(lng), label: value || "Точка на карті" };
      }
      return { type: "address", value: value, label: value };
    });
  }

  function resolvePoints(points) {
    var promises = points.map(function (p) {
      if (p.type === "coords") {
        return Promise.resolve({ lat: p.lat, lng: p.lng, display: p.label });
      }
      if (!p.value) return Promise.resolve(null);
      return geocode(p.value);
    });
    return Promise.all(promises);
  }

  function buildRoute() {
    var points = getOrderedPoints();
    var filled = points.filter(function (p) {
      return p.type === "coords" || (p.value && p.value.length > 0);
    });

    if (filled.length < 2) {
      notice("Вкажіть мінімум дві точки: звідки та куди.");
      return;
    }

    notice("");
    setBusy(true);
    var resCard = document.getElementById("route-result");
    resCard.classList.remove("is-shown");
    clearMapLayers();

    // Без цього прапорця не знайдена точка давала два alert поспіль:
    // спершу «точку не знайдено», а потім ще й «маршрут не знайдено».
    var aborted = false;

    resolvePoints(filled)
      .then(function (coords) {
        var missing = coords.findIndex(function (c) { return !c; });
        if (missing >= 0) {
          var label = filled[missing].label || filled[missing].value || "Точка " + (missing + 1);
          notice('Адресу «' + label + '» не знайдено. Уточніть написання або поставте точку на карті.');
          aborted = true;
          return;
        }

        if (map) {
          coords.forEach(function (c) {
            L.marker([c.lat, c.lng]).addTo(markersLayer).bindPopup(c.display);
          });
        }

        var coordsStr = coords.map(function (c) { return c.lng + "," + c.lat; }).join(";");
        return getJSON(GEO_ROUTE + "?coords=" + encodeURIComponent(coordsStr));
      })
      .then(function (route) {
        if (aborted) return;
        if (!route || !route.geometry) {
          notice("Маршрут не знайдено. Перевірте точки або спробуйте інші адреси.");
          return;
        }

        if (map) {
          var line = L.geoJSON(
            { type: "LineString", coordinates: route.geometry.coordinates },
            { style: { color: "#0ea5e9", weight: 5, opacity: 0.8 } }
          ).addTo(routeLayer);
          map.fitBounds(line.getBounds(), { padding: [40, 40] });
        }

        currentRouteData = { distance: route.distance, duration: route.duration };
        var distKm = formatKm(route.distance);
        var timeStr = formatDuration(route.duration);

        var labels = filled.map(function (p) { return p.label || p.value || ""; });
        var legs = route.legs || [];
        var legsHtml = legs
          .map(function (leg, i) {
            var a = (labels[i] || "Точка " + (i + 1)).split(",")[0].trim();
            var b = (labels[i + 1] || "Точка " + (i + 2)).split(",")[0].trim();
            var dist = formatKm(leg.distance);
            return '<div class="result__leg"><span>' + (i + 1) + ". " + a + " → " + b + "</span><strong>" + dist + "</strong></div>";
          })
          .join("");

        var resVehicle = document.getElementById("res-vehicle");
        if (resVehicle) resVehicle.textContent = "Бус до 3,5 т";
        document.getElementById("res-distance").textContent = distKm;
        document.getElementById("res-duration").textContent = timeStr;
        document.getElementById("legs-details").innerHTML = legsHtml || "";

        renderServicePrices(route.distance, route.duration);

        resCard.classList.add("is-shown");
      })
      .catch(function (err) {
        console.error(err);
        notice("Не вдалося побудувати маршрут. Перевірте адреси або спробуйте за хвилину.");
      })
      .then(function () { setBusy(false); });
  }

  /* Рахуємо ціну одразу за всіма послугами. Раніше треба було спершу
     обрати послугу й лише потім побачити цифру — тобто вибирати наосліп. */
  function renderServicePrices(distanceMeters, durationSeconds) {
    var host = document.getElementById("res-services");
    if (!host || typeof PriceCalculator === "undefined") return;

    var cfg = PriceCalculator.getBusServiceConfig();
    var priced = SERVICE_ORDER.map(function (id) {
      var r = PriceCalculator.calculate(distanceMeters, durationSeconds, "BUS", { busServiceId: id });
      return { id: id, label: (cfg[id] || {}).label || id, rate: (cfg[id] || {}).hourlyRate, res: r };
    });
    var cheapest = priced.reduce(function (a, b) { return b.res.total < a.res.total ? b : a; }).id;

    host.innerHTML = "";
    priced.forEach(function (item) {
      var btn = document.createElement("button");
      btn.type = "button";
      btn.className = "svc" + (item.id === cheapest ? " is-cheapest" : "");
      btn.setAttribute("data-service", item.id);
      btn.setAttribute("aria-pressed", "false");

      var name = document.createElement("span");
      name.className = "svc__name";
      name.textContent = item.label;

      var price = document.createElement("span");
      price.className = "svc__price";
      price.textContent = item.res.total + " грн";

      var rate = document.createElement("span");
      rate.className = "svc__rate";
      rate.textContent = item.rate ? item.rate + " грн/год" : "";
      if (item.id === cheapest) {
        var tag = document.createElement("b");
        tag.className = "svc__tag";
        tag.textContent = "найдешевше";
        rate.appendChild(document.createTextNode(" "));
        rate.appendChild(tag);
      }

      btn.appendChild(name);
      btn.appendChild(price);
      btn.appendChild(rate);
      btn.addEventListener("click", function () { selectService(item.id, priced); });
      host.appendChild(btn);
    });

    selectService(selectedService, priced);
  }

  function selectService(id, priced) {
    selectedService = id;
    var chosen = null;
    (priced || []).forEach(function (p) { if (p.id === id) chosen = p; });

    document.querySelectorAll("#res-services .svc").forEach(function (el) {
      var on = el.getAttribute("data-service") === id;
      el.classList.toggle("is-selected", on);
      el.setAttribute("aria-pressed", on ? "true" : "false");
    });

    var breakdown = document.getElementById("res-price-breakdown");
    if (breakdown && chosen) {
      breakdown.textContent = chosen.res.breakdown;
      breakdown.hidden = false;
    }
    // orderRoute.js бере звідси назву послуги для форми заявки.
    var hidden = document.getElementById("res-service");
    if (hidden && chosen) hidden.textContent = chosen.label;
  }

  function boot() { wireControls(); initMap(); }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
