/* Передає порахований маршрут і ціну у форму заявки.
   Раніше калькулятор був глухим кутом: людина бачила ціну і йшла геть. */
(function () {
  "use strict";

  var link = document.getElementById("order-this-route");
  if (!link) return;

  function textOf(id) {
    var el = document.getElementById(id);
    return el ? el.textContent.trim() : "";
  }

  link.addEventListener("click", function () {
    var inputs = document.querySelectorAll("#points-container .route-input");
    var points = [];
    inputs.forEach(function (i) { if (i.value.trim()) points.push(i.value.trim()); });

    var parts = [];
    if (points.length) parts.push("Маршрут: " + points.join(" → "));
    var dist = textOf("res-distance"); if (dist) parts.push("Відстань: " + dist);
    var dur = textOf("res-duration");  if (dur)  parts.push("Час у дорозі: " + dur);
    var svc = textOf("res-service");   if (svc && svc !== "—") parts.push("Послуга: " + svc);
    var price = textOf("res-price");   if (price && price !== "—") parts.push("Орієнтовна вартість: " + price);

    if (!parts.length) return;

    var msg = parts.join("\n");
    try { sessionStorage.setItem("vezemo_route", msg); } catch (e) { /* приватний режим */ }
    link.setAttribute("href", link.getAttribute("href").split("?")[0] + "?route=" + encodeURIComponent(msg));

    if (window.vezemoTrack) {
      window.vezemoTrack("calculator_order_click", { distance: dist, price: price, service: svc });
    }
  });
})();
