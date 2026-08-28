/* Форма заявки: валідація телефону, підстановка маршруту з калькулятора,
   надсилання без перезавантаження. Без зовнішніх бібліотек. */
document.addEventListener("DOMContentLoaded", function () {
  var form = document.getElementById("contactForm");
  if (!form) return;

  var submitBtn = document.getElementById("submitBtn");
  var alertBox = document.getElementById("formAlert");
  var phoneInput = document.getElementById("phone");
  var messageInput = document.getElementById("message");

  var phone = window.PhoneField ? window.PhoneField.attach(phoneInput) : null;

  /* Маршрут із калькулятора — не змушуємо переписувати все заново. */
  (function prefillRoute() {
    var route = "";
    try {
      route = new URLSearchParams(window.location.search).get("route") || "";
      if (!route) route = sessionStorage.getItem("vezemo_route") || "";
    } catch (e) { /* приватний режим */ }
    if (route && messageInput && !messageInput.value.trim()) {
      messageInput.value = route;
      var extra = form.querySelector(".disclosure");
      if (extra) extra.open = true;
    }
  })();

  function showAlert(message) {
    alertBox.textContent = message;
    alertBox.className = "notice notice--error is-shown";
    alertBox.scrollIntoView({ behavior: "smooth", block: "nearest" });
  }

  function resetUI() {
    alertBox.classList.remove("is-shown");
    phoneInput.classList.remove("is-error");
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    resetUI();

    var valid = phone ? phone.isValid() : phoneInput.value.replace(/\D/g, "").length >= 9;
    if (!valid) {
      phoneInput.classList.add("is-error");
      phoneInput.focus();
      showAlert("Введіть коректний номер телефону — 9 цифр після +380.");
      return;
    }

    submitBtn.disabled = true;
    var btnLabel = submitBtn.querySelector("span");
    var original = btnLabel ? btnLabel.textContent : "";
    if (btnLabel) btnLabel.textContent = "Надсилаємо…";

    var data = new FormData(form);            // csrf_token їде разом із формою
    if (phone) data.set("phone", phone.getNumber());

    fetch(form.action, {
      method: "POST",
      body: data,
      headers: { "Accept": "application/json" }
    })
      .then(function (res) {
        return res.json().catch(function () { return {}; }).then(function (body) {
          return { ok: res.ok, body: body };
        });
      })
      .then(function (r) {
        if (!r.ok) {
          showAlert(r.body.error || "Не вдалося надіслати. Спробуйте ще раз або зателефонуйте.");
          return;
        }
        window.dataLayer = window.dataLayer || [];
        window.dataLayer.push({ event: "generate_lead", method: "form" });
        try { sessionStorage.removeItem("vezemo_route"); } catch (err) { /* ignore */ }
        window.location.href = "/thank-you";
      })
      .catch(function () {
        showAlert("Немає звʼязку з сервером. Спробуйте пізніше або зателефонуйте нам.");
      })
      .finally(function () {
        submitBtn.disabled = false;
        if (btnLabel) btnLabel.textContent = original;
      });
  });
});
