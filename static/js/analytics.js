/* Відстеження конверсій. Дзвінок — головна конверсія в цій ніші,
   тому кожен клік по телефону/месенджеру/формі йде в dataLayer. */
(function () {
  "use strict";
  window.dataLayer = window.dataLayer || [];

  function track(name, params) {
    var payload = { event: name };
    for (var k in params) if (Object.prototype.hasOwnProperty.call(params, k)) payload[k] = params[k];
    window.dataLayer.push(payload);
  }

  document.addEventListener("click", function (e) {
    var el = e.target && e.target.closest ? e.target.closest("[data-cta]") : null;
    if (!el) return;

    var cta = el.getAttribute("data-cta") || "unknown";
    var href = el.getAttribute("href") || "";
    var kind = "other";
    if (href.indexOf("tel:") === 0) kind = "phone_call";
    else if (href.indexOf("viber:") === 0 || href.indexOf("viber.click") > -1) kind = "viber";
    else if (href.indexOf("t.me") > -1 || href.indexOf("tg:") === 0) kind = "telegram";
    else if (href.indexOf("/contact") > -1) kind = "form_open";

    track(kind, { cta_location: cta, link_url: href });
    track("contact_intent", { method: kind, cta_location: cta });
  }, { passive: true });

  window.vezemoTrack = track;
})();
