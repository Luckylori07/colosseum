/* Colosseum Azzate - comportamento della pagina. Nessuna dipendenza, nessun tracking. */
(function () {
  'use strict';

  var doc = document;
  var root = doc.documentElement;
  var body = doc.body;

  /* ---------------------------------------------------------------------
     0. Modalità demo: se data-demo non è "on" tolgo anche noindex e prefisso titolo
        (il modo completo di pubblicare è go-live.sh, vedi README)
     ------------------------------------------------------------------ */
  if (body.getAttribute('data-demo') !== 'on') {
    var robots = doc.getElementById('demo-robots');
    if (robots && robots.parentNode) robots.parentNode.removeChild(robots);
    doc.title = doc.title.replace(/^\[DEMO\]\s*/, '');
  }

  /* ---------------------------------------------------------------------
     1. Altezza della barra fissa (demo + header) per gli scroll alle ancore
     ------------------------------------------------------------------ */
  var top = doc.querySelector('.top');
  function setTopHeight() {
    if (top) root.style.setProperty('--top-h', top.offsetHeight + 'px');
  }
  setTopHeight();
  window.addEventListener('resize', setTopHeight);
  if (window.ResizeObserver && top) new ResizeObserver(setTopHeight).observe(top);

  var style = doc.createElement('style');
  style.textContent = '[id]{scroll-margin-top:calc(var(--top-h) + 8px)}';
  doc.head.appendChild(style);

  /* ---------------------------------------------------------------------
     2. Menu mobile
     ------------------------------------------------------------------ */
  var burger = doc.querySelector('.header__burger');
  var nav = doc.getElementById('menu');
  function setMenu(open) {
    if (!burger || !nav) return;
    nav.classList.toggle('is-open', open);
    burger.setAttribute('aria-expanded', open ? 'true' : 'false');
    burger.setAttribute('aria-label', open ? 'Chiudi il menu' : 'Apri il menu');
    burger.querySelector('use').setAttribute('href', open ? '#i-close' : '#i-menu');
  }
  if (burger && nav) {
    burger.addEventListener('click', function () {
      setMenu(burger.getAttribute('aria-expanded') !== 'true');
    });
    nav.addEventListener('click', function (e) {
      if (e.target.closest('a')) setMenu(false);
    });
    doc.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && nav.classList.contains('is-open')) {
        setMenu(false);
        burger.focus();
      }
    });
  }

  /* ---------------------------------------------------------------------
     3. Aperto ora / Chiuso (fuso Europe/Rome)
        Orari: Lun-Ven 7:00-22:00, Sab 9:00-18:00, Dom 9:00-13:00
     ------------------------------------------------------------------ */
  var SCHEDULE = {            // giorno (0 = domenica) -> [apertura, chiusura] in minuti dalla mezzanotte
    0: [9 * 60, 13 * 60],
    1: [7 * 60, 22 * 60],
    2: [7 * 60, 22 * 60],
    3: [7 * 60, 22 * 60],
    4: [7 * 60, 22 * 60],
    5: [7 * 60, 22 * 60],
    6: [9 * 60, 18 * 60]
  };
  var WEEKDAY_INDEX = { Sun: 0, Mon: 1, Tue: 2, Wed: 3, Thu: 4, Fri: 5, Sat: 6 };

  function fmt(min) {
    var h = Math.floor(min / 60), m = min % 60;
    return h + ':' + (m < 10 ? '0' : '') + m;
  }

  function romeNow(date) {
    var parts = new Intl.DateTimeFormat('en-GB', {
      timeZone: 'Europe/Rome', weekday: 'short', hour: '2-digit', minute: '2-digit', hourCycle: 'h23'
    }).formatToParts(date);
    var out = {};
    parts.forEach(function (p) { out[p.type] = p.value; });
    return { day: WEEKDAY_INDEX[out.weekday], minutes: parseInt(out.hour, 10) * 60 + parseInt(out.minute, 10) };
  }

  function getStatus(date) {
    var now = romeNow(date);
    var today = SCHEDULE[now.day];
    if (now.minutes >= today[0] && now.minutes < today[1]) {
      return { open: true, label: 'Aperto ora', detail: 'Fino alle ' + fmt(today[1]), day: now.day };
    }
    if (now.minutes < today[0]) {
      return { open: false, label: 'Chiuso', detail: 'Apre oggi alle ' + fmt(today[0]), day: now.day };
    }
    var next = (now.day + 1) % 7;
    return { open: false, label: 'Chiuso', detail: 'Riapre domani alle ' + fmt(SCHEDULE[next][0]), day: now.day };
  }

  function renderStatus() {
    var s;
    try { s = getStatus(new Date()); } catch (err) { return; }
    doc.querySelectorAll('[data-status]').forEach(function (el) {
      el.classList.toggle('is-open', s.open);
      var l = el.querySelector('[data-status-label]');
      var d = el.querySelector('[data-status-detail]');
      if (l) l.textContent = s.label;
      if (d) d.textContent = s.detail;
    });
    doc.querySelectorAll('.hours__item').forEach(function (li) {
      var days = li.getAttribute('data-days').split(',').map(Number);
      var isToday = days.indexOf(s.day) !== -1;
      li.classList.toggle('is-today', isToday);
      if (isToday) li.setAttribute('aria-current', 'date'); else li.removeAttribute('aria-current');
    });
  }
  renderStatus();
  setInterval(renderStatus, 60 * 1000);

  /* ---------------------------------------------------------------------
     4. Presentazione foto nell'hero (cambio ogni ~3,5 s; pausa con il pulsante, al passaggio del mouse o a scheda nascosta)
     ------------------------------------------------------------------ */
  var slides = doc.querySelectorAll('.hero__slides img');
  var pauseBtn = doc.querySelector('.hero__pause');
  var motionOff = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (slides.length > 1 && !motionOff) {
    var cur = 0, timer = null, userPaused = false, hovering = false;
    Array.prototype.forEach.call(slides, function (im, i) { im.setAttribute('aria-hidden', i === 0 ? 'false' : 'true'); });
    var go = function () {
      slides[cur].classList.remove('is-active'); slides[cur].setAttribute('aria-hidden', 'true');
      cur = (cur + 1) % slides.length;
      slides[cur].classList.add('is-active'); slides[cur].setAttribute('aria-hidden', 'false');
    };
    var sync = function () {
      var shouldRun = !userPaused && !hovering && !doc.hidden;
      if (shouldRun && !timer) timer = setInterval(go, 3500);
      if (!shouldRun && timer) { clearInterval(timer); timer = null; }
    };
    var figure = doc.querySelector('.hero__photo');
    if (figure) {
      figure.addEventListener('mouseenter', function () { hovering = true; sync(); });
      figure.addEventListener('mouseleave', function () { hovering = false; sync(); });
    }
    doc.addEventListener('visibilitychange', sync);
    if (pauseBtn) {
      pauseBtn.addEventListener('click', function () {
        userPaused = !userPaused;
        pauseBtn.setAttribute('aria-pressed', userPaused ? 'true' : 'false');
        pauseBtn.setAttribute('aria-label', userPaused ? 'Riprendi la presentazione delle foto' : 'Metti in pausa la presentazione delle foto');
        sync();
      });
    }
    sync();
  } else if (pauseBtn) {
    pauseBtn.parentNode.removeChild(pauseBtn);
  }

  /* ---------------------------------------------------------------------
     5. Reveal sobrio allo scroll (solo gruppi numerati; disattivo con prefers-reduced-motion)
     ------------------------------------------------------------------ */
  var reveals = doc.querySelectorAll('[data-reveal]');
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reveals.length && 'IntersectionObserver' in window && !reduce) {
    reveals.forEach(function (group) {
      Array.prototype.forEach.call(group.children, function (child, i) { child.style.setProperty('--n', i); });
    });
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting || en.boundingClientRect.top < 0) { en.target.classList.add('is-in'); io.unobserve(en.target); }
      });
    }, { threshold: 0.15 });
    reveals.forEach(function (g) { io.observe(g); });
  } else {
    reveals.forEach(function (g) { g.classList.add('is-in'); });
  }
})();
