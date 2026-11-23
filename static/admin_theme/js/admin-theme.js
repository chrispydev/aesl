/* AESL Control Center — admin UI enhancements */
(function () {
  "use strict";

  /* Keep the admin permanently in the branded dark theme. */
  try {
    localStorage.setItem("theme", "dark");
  } catch (e) { /* storage can be unavailable in private mode */ }
  document.documentElement.dataset.theme = "dark";

  var body = document.body;
  var dateOptions = { weekday: "short", day: "2-digit", month: "short", year: "numeric" };

  function updateDates() {
    var now = new Date();
    var formatted = new Intl.DateTimeFormat("en-GB", dateOptions).format(now);
    var chip = document.getElementById("today-chip");
    var topbar = document.getElementById("topbar-date");
    if (chip) chip.textContent = formatted;
    if (topbar) {
      var time = new Intl.DateTimeFormat("en-GB", { hour: "2-digit", minute: "2-digit" }).format(now);
      topbar.textContent = formatted.replace(",", " ·") + "  " + time;
    }
  }

  function updateGreeting() {
    var prefix = document.getElementById("dash-greeting-prefix");
    if (!prefix) return;
    var hour = new Date().getHours();
    prefix.textContent =
      hour < 12 ? "Good morning" : hour < 17 ? "Good afternoon" : "Good evening";
  }

  /* --- Off-canvas navigation on small screens --- */
  var trigger = document.querySelector(".mobile-nav-trigger");
  var sidebar = document.getElementById("nav-sidebar");
  var overlay = document.querySelector(".sidebar-overlay");

  function setSidebar(open) {
    body.classList.toggle("sidebar-open", open);
    if (trigger) trigger.setAttribute("aria-expanded", String(open));
    if (overlay) overlay.hidden = !open;
    if (sidebar) sidebar.setAttribute("aria-hidden", String(!open && window.innerWidth <= 900));
  }

  if (trigger) {
    trigger.addEventListener("click", function () {
      setSidebar(!body.classList.contains("sidebar-open"));
    });
  }
  if (overlay) overlay.addEventListener("click", function () { setSidebar(false); });
  if (sidebar) {
    sidebar.addEventListener("click", function (event) {
      if (event.target.closest("a") && window.innerWidth <= 900) setSidebar(false);
    });
  }
  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape" && body.classList.contains("sidebar-open")) setSidebar(false);
    if (event.key === "/" && !/^(INPUT|TEXTAREA|SELECT)$/.test(event.target.tagName)) {
      var filter = document.getElementById("nav-filter");
      if (filter) {
        event.preventDefault();
        filter.focus();
      }
    }
  });
  window.addEventListener("resize", function () {
    if (window.innerWidth > 900 && body.classList.contains("sidebar-open")) setSidebar(false);
  });

  /* Smoothly flag the currently active sidebar model without reloading. */
  function markActiveModel() {
    if (!sidebar) return;
    var path = window.location.pathname;
    var links = sidebar.querySelectorAll("th[scope=row] a");
    links.forEach(function (link) {
      if (link.pathname === path && path !== "/admin/") {
        link.closest("tr").classList.add("current-model");
      }
    });
  }

  updateDates();
  updateGreeting();
  markActiveModel();
  setInterval(updateDates, 60000);
})();
