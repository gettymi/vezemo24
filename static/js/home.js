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
          // Проявляємо відео лише коли пішов реальний кадр, інакше поверх
          // постера блимне порожній прямокутник.
          video.addEventListener("playing", function () {
            video.classList.add("is-playing");
          }, { once: true });
          video.src = src;
          video.load();
          var p = video.play();
          if (p && p.catch) p.catch(function () { /* автоплей заблоковано — лишається постер */ });
        };
        if ("requestIdleCallback" in window) requestIdleCallback(start, { timeout: 2500 });
        else setTimeout(start, 1200);
      }
    }
  }

  var trust = document.getElementById("trust");
  if (trust && "IntersectionObserver" in window) {
    // Вмикаємо приховування аж тут: доти CSS нічого не ховає, тож збій
    // цього файлу не може лишити блок порожнім.
    trust.classList.add("is-armed");

    var reveal = function () { trust.classList.add("is-visible"); };

    var obs = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { reveal(); obs.unobserve(e.target); }
      });
    }, { threshold: 0.15, rootMargin: "0px 0px -40px 0px" });
    obs.observe(trust);

    var inView = function () {
      var b = trust.getBoundingClientRect();
      return b.top < window.innerHeight && b.bottom > 0;
    };

    // Блок може опинитись на екрані одразу: низьке вікно, перехід за якорем
    // або зсув верстки після довантаження картинок.
    if (inView()) reveal();
    window.addEventListener("load", function () {
      if (inView()) reveal();
    }, { once: true });

    // Таймера-страховки тут навмисно немає. Будь-яке його значення менше
    // за час, поки людина догортає до блоку, — а це кілька секунд, — просто
    // показувало б картки заздалегідь і скасовувало анімацію всім.
    // Якщо виконання дійшло сюди, IntersectionObserver існує і спрацює
    // при прокрутці; а якщо цей файл узагалі не завантажився, класу
    // .is-armed не буде і CSS нічого не сховає.
  }
})();
