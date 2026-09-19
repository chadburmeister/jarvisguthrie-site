(function () {
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("site-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
    nav.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", function () {
        nav.classList.remove("open");
        toggle.setAttribute("aria-expanded", "false");
      });
    });
  }

  document.querySelectorAll("[data-year]").forEach(function (el) {
    el.textContent = new Date().getFullYear();
  });

  var form = document.getElementById("reserve-form");
  if (form) {
    form.addEventListener("submit", function (e) {
      var status = form.querySelector("[data-form-status]");
      // Formspree (or similar) endpoint required — see README for setup.
      if (form.getAttribute("action").indexOf("YOUR_FORM_ID") !== -1) {
        e.preventDefault();
        if (status) {
          status.textContent = "Form isn't connected yet — add a Formspree endpoint in styles/build to go live.";
          status.style.color = "#A97632";
        }
      }
    });
  }
})();
