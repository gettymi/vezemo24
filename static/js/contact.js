document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("contactForm");
  const submitBtn = document.getElementById("submitBtn");
  const alertBox = document.getElementById("formAlert");
  const phoneInput = document.getElementById("phone");
  const messageInput = document.getElementById("message");
  if (!form || !phoneInput) return;

  /* ── Підставляємо маршрут із калькулятора ────────────────────────────────
     Людина порахувала ціну — не змушуємо її переписувати все заново. */
  (function prefillRoute() {
    let route = "";
    try {
      route = new URLSearchParams(window.location.search).get("route") || "";
      if (!route) route = sessionStorage.getItem("vezemo_route") || "";
    } catch (e) { /* приватний режим */ }
    if (route && messageInput && !messageInput.value.trim()) {
      messageInput.value = route;
      const extra = document.querySelector(".form-extra");
      if (extra) extra.open = true;
    }
  })();

  const iti = window.intlTelInput(phoneInput, {
    initialCountry: "ua",
    separateDialCode: true,
    preferredCountries: ["ua", "pl", "de"],
    utilsScript: "https://cdn.jsdelivr.net/npm/intl-tel-input@18.2.1/build/js/utils.js",
  });

  const validatePhone = () => {
    if (!phoneInput.value.trim()) return false;
    const ok = iti.isValidNumber();
    phoneInput.classList.toggle("valid", ok);
    phoneInput.classList.toggle("error", !ok);
    return ok;
  };

  phoneInput.addEventListener("blur", validatePhone);
  phoneInput.addEventListener("change", validatePhone);

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    resetUI();

    if (!validatePhone()) {
      showAlert("Введіть коректний номер телефону.", "error");
      phoneInput.classList.add("error");
      alertBox.scrollIntoView({ behavior: "smooth", block: "nearest" });
      return;
    }

    submitBtn.disabled = true;
    submitBtn.querySelector("span").textContent = "Надсилаємо…";

    const formData = new FormData(form);           // csrf_token їде разом із формою
    formData.set("phone", iti.getNumber());

    try {
      const res = await fetch(form.action, {
        method: "POST",
        body: formData,
        headers: { "Accept": "application/json" },
      });
      const data = await res.json().catch(() => ({}));

      if (!res.ok) {
        showAlert(data.error || "Не вдалося надіслати. Спробуйте ще раз або зателефонуйте.", "error");
        alertBox.scrollIntoView({ behavior: "smooth", block: "nearest" });
        return;
      }

      window.dataLayer = window.dataLayer || [];
      window.dataLayer.push({ event: "generate_lead", method: "form" });
      window.dataLayer.push({ event: "form_submission" });
      try { sessionStorage.removeItem("vezemo_route"); } catch (err) { /* ignore */ }
      window.location.href = "/thank-you";

    } catch (err) {
      showAlert("Немає звʼязку з сервером. Спробуйте пізніше або зателефонуйте нам.", "error");
      alertBox.scrollIntoView({ behavior: "smooth", block: "nearest" });
    } finally {
      submitBtn.disabled = false;
      submitBtn.querySelector("span").textContent = "Передзвоніть мені";
    }
  });

  function showAlert(message, type) {
    alertBox.textContent = message;
    alertBox.className = `alert ${type}`;
    alertBox.style.display = "block";
  }

  function resetUI() {
    alertBox.style.display = "none";
    form.querySelectorAll(".form-input, .iti input").forEach((el) => el.classList.remove("error"));
  }
});
