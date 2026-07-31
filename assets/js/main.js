(function () {
  var toggle = document.querySelector(".menu-toggle");
  var nav = document.getElementById("primary-nav");
  var mq = window.matchMedia("(max-width: 1040px)");

  function isMobileNav() {
    return mq.matches;
  }

  function closeNav() {
    if (!nav || !toggle) return;
    nav.classList.remove("open");
    toggle.setAttribute("aria-expanded", "false");
    document.body.classList.remove("nav-open");
    nav.querySelectorAll(".nav-item.open").forEach(function (item) {
      item.classList.remove("open");
      var btn = item.querySelector("button");
      if (btn) btn.setAttribute("aria-expanded", "false");
    });
  }

  function openNav() {
    if (!nav || !toggle) return;
    nav.classList.add("open");
    toggle.setAttribute("aria-expanded", "true");
    document.body.classList.add("nav-open");
  }

  if (toggle && nav) {
    toggle.addEventListener("click", function (e) {
      e.preventDefault();
      e.stopPropagation();
      if (nav.classList.contains("open")) closeNav();
      else openNav();
    });

    // Accordion dropdowns on mobile
    nav.querySelectorAll(".nav-item > button").forEach(function (btn) {
      btn.addEventListener("click", function (e) {
        if (!isMobileNav()) return;
        e.preventDefault();
        e.stopPropagation();
        var item = btn.parentElement;
        var open = item.classList.toggle("open");
        btn.setAttribute("aria-expanded", open ? "true" : "false");
        // close siblings
        nav.querySelectorAll(".nav-item.open").forEach(function (other) {
          if (other !== item) {
            other.classList.remove("open");
            var ob = other.querySelector("button");
            if (ob) ob.setAttribute("aria-expanded", "false");
          }
        });
      });
    });

    // Close when a real link is tapped
    nav.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () {
        if (isMobileNav()) closeNav();
      });
    });

    // Close on resize to desktop
    if (mq.addEventListener) {
      mq.addEventListener("change", function (ev) {
        if (!ev.matches) closeNav();
      });
    } else if (mq.addListener) {
      mq.addListener(function (ev) {
        if (!ev.matches) closeNav();
      });
    }

    // Escape closes menu
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") closeNav();
    });
  }

  /* Mobile app bar active state */
  var path = (location.pathname || "/").replace(/\.html$/, "").replace(/\/+$/, "") || "/";
  var bar = document.querySelector(".mobile-app-bar");
  if (bar) {
    bar.querySelectorAll("a[data-nav]").forEach(function (a) {
      a.classList.remove("active");
      var key = a.getAttribute("data-nav");
      if (key === "home" && (path === "/" || path === "")) a.classList.add("active");
      if (
        key === "areas" &&
        (path.indexOf("/service-areas") !== -1 || path.indexOf("/areas") !== -1)
      ) {
        a.classList.add("active");
      }
    });
  }
})();
