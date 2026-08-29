/* Передає порахований маршрут і ціну у форму заявки.
   Раніше калькулятор був глухим кутом: людина бачила ціну і йшла геть. */
(function () {
  "use strict";

  var VZT = function (k) { return window.VZ && window.VZ.t ? window.VZ.t(k) : k; };

  var link = document.getElementById("order-this-route");
  if (!link) return;

  function textOf(id) {
    var el = document.getElementById(id);
    return el ? el.textContent.trim() : "";
  }

  link.addEventListener("click", function () {
    var parts = [];
    var points = [];
    document.querySelectorAll("#points-container .point__input").forEach(function (i) {
      if (i.value.trim()) points.push(i.value.trim());
    });
    if (points.length) parts.push(VZT("route.label") + ": " + points.join(" → "));

    var dist = textOf("res-distance"); if (dist) parts.push(VZT("route.distance") + ": " + dist);
    var dur  = textOf("res-duration"); if (dur)  parts.push(VZT("route.duration") + ": " + dur);
    var svc  = textOf("res-service");  if (svc && svc !== "—") parts.push(VZT("route.service") + ": " + svc);

    // Ціна тепер живе в обраній картці послуги, а не в окремому рядку підсумку.
    var selected = document.querySelector("#res-services .svc.is-selected .svc__price");
    var price = selected ? selected.textContent.trim() : "";
    if (price) parts.push(VZT("route.price") + ": " + price);
    if (!parts.length) return;

    var msg = parts.join("\n");
    try { sessionStorage.setItem("vezemo_route", msg); } catch (e) { /* приватний режим */ }
    link.setAttribute("href", link.getAttribute("href").split("?")[0] + "?route=" + encodeURIComponent(msg));

    if (window.vezemoTrack) {
      window.vezemoTrack("calculator_order_click", { distance: dist, price: price, service: svc });
    }
  });
})();
