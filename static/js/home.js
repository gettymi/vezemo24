/* Головна сторінка: відео лише там, де воно того варте + трекінг конверсій. */
(function () {
  "use strict";

  /* ── 1. Hero-відео: НЕ вантажимо на мобільних ───────────────────────────
     Раніше 4,5 МБ відео завантажувалось на всіх пристроях з autoplay.
     Тепер: широкий екран + не economy-режим + користувач не просив
     зменшити анімацію. На телефоні лишається лише poster (~250 КБ). */
  var video = document.getElementById("hero-video");
  if (video) {
    var conn = navigator.connection || navigator.mozConnection || navigator.webkitConnection;
    var saveData = !!(conn && (conn.saveData || /2g/.test(conn.effectiveType || "")));
    var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    var wide = window.matchMedia("(min-width: 900px)").matches;

    if (wide && !saveData && !reduced) {
      var src = video.getAttribute("data-src");
      if (src) {
        var start = function () {
          video.src = src;
          video.load();
          var p = video.play();
          if (p && p.catch) p.catch(function () { /* автоплей заблоковано — лишається poster */ });
        };
        if ("requestIdleCallback" in window) requestIdleCallback(start, { timeout: 2500 });
        else setTimeout(start, 1200);
      }
    }
  }

  /* ── 2. Поява блоку довіри ─────────────────────────────────────────────── */
  var trust = document.getElementById("trust-section");
  if (trust) {
    if ("IntersectionObserver" in window) {
      var obs = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
          if (e.isIntersecting) {
            e.target.classList.add("trust-section--visible");
            obs.unobserve(e.target);
          }
        });
      }, { threshold: 0.15, rootMargin: "0px 0px -40px 0px" });
      obs.observe(trust);
    } else {
      trust.classList.add("trust-section--visible");
    }
  }
})();
