/* Головна: поява блоку довіри.
   Тут був запуск hero-відео; відео з героя прибрано, лишилась фотографія. */
(function () {
  "use strict";

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
