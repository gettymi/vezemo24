/* Головна: відео лише там, де воно того варте, і поява блоку довіри. */
(function () {
  "use strict";

  /* Hero-відео НЕ вантажимо на мобільних: раніше 4,5 МБ їхало на кожен
     телефон з autoplay. Тепер широкий екран + не economy + без reduced-motion.
     На телефоні лишається тільки poster. */
  var video = document.getElementById("js-hero-video");
  if (video) {
    var conn = navigator.connection || navigator.mozConnection || navigator.webkitConnection;
    var saveData = !!(conn && (conn.saveData || /(^|[^4])2g/.test(conn.effectiveType || "")));
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

  var trust = document.getElementById("trust");
  if (trust) {
    if ("IntersectionObserver" in window) {
      var obs = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
          if (e.isIntersecting) { e.target.classList.add("is-visible"); obs.unobserve(e.target); }
        });
      }, { threshold: 0.2, rootMargin: "0px 0px -40px 0px" });
      obs.observe(trust);
      // Страховка: якщо observer чомусь не спрацював, текст усе одно зʼявиться.
      setTimeout(function () { trust.classList.add("is-visible"); }, 1500);
    } else {
      trust.classList.add("is-visible");
    }
  }
})();
