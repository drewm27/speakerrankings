document.addEventListener("DOMContentLoaded", function () {
  const banner = document.getElementById("cookie-consent");
  const button = document.getElementById("accept-cookies");

  if (!localStorage.getItem("cookieConsent")) {
    banner.style.display = "flex";
  }

  button.addEventListener("click", function () {
    localStorage.setItem("cookieConsent", "true");
    banner.style.display = "none";
  });
});

