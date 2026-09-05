/**
 * Надсилання заявки без перезавантаження сторінки.
 *
 * Форма тепер стоїть НЕ ЛИШЕ на сторінці контактів, а в блоці заклику
 * внизу кожної сторінки, тож на одній сторінці їх може бути дві. Тому
 * шукаємо всі [data-lead-form] і всередині кожної працюємо тільки з її
 * власними полями: раніше все трималось на getElementById, і друга форма
 * мовчки керувала б кнопкою першої.
 */
document.addEventListener("DOMContentLoaded", function () {
  var forms = document.querySelectorAll("[data-lead-form]");
  if (!forms.length) return;

  // Переклад дістаємо в момент виклику: i18n.js має defer.
  var VZT = function (k) { return window.VZ && window.VZ.t ? window.VZ.t(k) : k; };

  // Сервер віддає КОД помилки, а не готову фразу: інакше українська
  // відповідь показувалась би й на російській, і на англійській версії —
  // саме тоді, коли людина помилилась і намагається залишити заявку.
  // Білий список навмисно: на невідомий код падаємо назад на текст сервера,
  // а не показуємо відвідувачу назву ключа.
  var ERROR_KEYS = {
    "phone_required": "form.phone_required",
    "bad_phone": "form.bad_phone",
    "too_many": "form.too_many",
    "session_expired": "form.session_expired"
  };

  function errorText(body) {
    var key = body && body.error_code ? ERROR_KEYS[body.error_code] : null;
    return (key && VZT(key)) || (body && body.error) || VZT("form.send_failed");
  }

  Array.prototype.forEach.call(forms, function (form) {
    var submitBtn = form.querySelector("[data-lead-submit]");
    var alertBox = form.querySelector("[data-lead-alert]");
    var phoneInput = form.querySelector("[data-lead-phone]");
    var messageInput = form.querySelector("[data-lead-message]");
    if (!submitBtn || !alertBox || !phoneInput) return;

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
        showAlert(VZT("form.bad_phone"));
        return;
      }

      submitBtn.disabled = true;
      var btnLabel = submitBtn.querySelector("span");
      var original = btnLabel ? btnLabel.textContent : "";
      if (btnLabel) btnLabel.textContent = VZT("form.sending");

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
            showAlert(errorText(r.body));
            return;
          }
          window.dataLayer = window.dataLayer || [];
          window.dataLayer.push({
            event: "generate_lead",
            method: "form",
            cta_location: form.querySelector("[name=source]") ?
              form.querySelector("[name=source]").value : "unknown"
          });
          try { sessionStorage.removeItem("vezemo_route"); } catch (err) { /* ignore */ }
          window.location.href = "/thank-you";
        })
        .catch(function () {
          showAlert(VZT("form.no_connection"));
        })
        .finally(function () {
          submitBtn.disabled = false;
          if (btnLabel) btnLabel.textContent = original;
        });
    });
  });
});
