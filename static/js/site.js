/* Каркас сайту: стан шапки, мобільне меню, відстеження конверсій.
   Раніше це були два окремі файли (main.js + analytics.js). */
(function () {
  "use strict";

  /* ── Шапка при скролі ───────────────────────────────────────────────── */
  var header = document.getElementById("js-header");
  if (header) {
    var ticking = false;
    var onScroll = function () {
      header.classList.toggle("is-scrolled", (window.scrollY || window.pageYOffset) > 16);
      ticking = false;
    };
    window.addEventListener("scroll", function () {
      if (!ticking) { ticking = true; requestAnimationFrame(onScroll); }
    }, { passive: true });
    onScroll();
  }

  /* ── Мобільне меню ──────────────────────────────────────────────────── */
  var nav = document.getElementById("js-nav");
  var burger = document.getElementById("js-burger");
  if (nav && burger) {
    var setOpen = function (open) {
      nav.classList.toggle("is-open", open);
      burger.setAttribute("aria-expanded", open ? "true" : "false");
    };
    burger.addEventListener("click", function () {
      setOpen(!nav.classList.contains("is-open"));
    });
    document.addEventListener("click", function (e) {
      if (nav.classList.contains("is-open") && !nav.contains(e.target) && !burger.contains(e.target)) {
        setOpen(false);
      }
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && nav.classList.contains("is-open")) { setOpen(false); burger.focus(); }
    });
  }

  /* ── Конверсії ──────────────────────────────────────────────────────────
     Дзвінок — головна конверсія в цій ніші, тому кожен клік по телефону,
     месенджеру чи формі йде в dataLayer. */
  window.dataLayer = window.dataLayer || [];
  function track(name, params) {
    var payload = { event: name };
    for (var k in params) if (Object.prototype.hasOwnProperty.call(params, k)) payload[k] = params[k];
    window.dataLayer.push(payload);
  }
  window.vezemoTrack = track;

  document.addEventListener("click", function (e) {
    var el = e.target && e.target.closest ? e.target.closest("[data-cta]") : null;
    if (!el) return;
    var href = el.getAttribute("href") || "";
    var kind = "other";
    if (href.indexOf("tel:") === 0) kind = "phone_call";
    else if (href.indexOf("viber") > -1) kind = "viber";
    else if (href.indexOf("t.me") > -1 || href.indexOf("tg:") === 0) kind = "telegram";
    else if (href.indexOf("/contact") > -1) kind = "form_open";

    track(kind, { cta_location: el.getAttribute("data-cta") || "unknown", link_url: href });
    track("contact_intent", { method: kind, cta_location: el.getAttribute("data-cta") || "unknown" });
  }, { passive: true });
})();
