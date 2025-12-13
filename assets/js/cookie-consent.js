document.addEventListener("DOMContentLoaded", function () {
  const banner = document.getElementById("cookie-consent");
  const button = document.getElementById("accept-cookies");

  function getCookie(name) {
    return document.cookie
      .split("; ")
      .find(row => row.startsWith(name + "="))
      ?.split("=")[1];
  }

  function setCookie(name, value, days) {
    const date = new Date();
    date.setTime(date.getTime() + days * 24 * 60 * 60 * 1000);
    document.cookie = `${name}=${value}; expires=${date.toUTCString()}; path=/; SameSite=Lax`;
  }

  if (!getCookie("cookie_consent")) {
    banner.style.display = "flex";
  }

  button.addEventListener("click", function () {
    setCookie("cookie_consent", "true", 365);
    banner.style.display = "none";
  });
});

