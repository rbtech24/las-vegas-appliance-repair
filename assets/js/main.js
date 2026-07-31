
(function () {
  var toggle = document.querySelector('.menu-toggle');
  var nav = document.getElementById('primary-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  /* Mobile app bar active state */
  var path = (location.pathname || '/').replace(/\.html$/, '').replace(/\/+$/, '') || '/';
  var bar = document.querySelector('.mobile-app-bar');
  if (bar) {
    bar.querySelectorAll('a[data-nav]').forEach(function (a) {
      a.classList.remove('active');
      var key = a.getAttribute('data-nav');
      if (key === 'home' && (path === '/' || path === '')) a.classList.add('active');
      if (key === 'schedule' && path.indexOf('/contact') !== -1) a.classList.add('active');
      if (key === 'areas' && (path.indexOf('/service-areas') !== -1 || path.indexOf('/areas') !== -1)) a.classList.add('active');
    });
  }
})();
