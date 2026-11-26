// Footer year
var y = document.getElementById('year');
if (y) y.textContent = new Date().getFullYear();

// Mobile menu
var toggle = document.querySelector('.nav-toggle');
var nav = document.getElementById('site-nav');
if (toggle && nav) {
  toggle.addEventListener('click', function () {
    var open = nav.classList.toggle('open');
    toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
  });
  nav.addEventListener('click', function (e) {
    if (e.target.tagName === 'A') {
      nav.classList.remove('open');
      toggle.setAttribute('aria-expanded', 'false');
    }
  });
}

// Body map demo: switch example sites
var tabs = document.querySelectorAll('.map-tabs button');
var mapImg = document.getElementById('map-img');
var mapLabel = document.getElementById('map-label');
var mapView = document.getElementById('map-view');
tabs.forEach(function (btn) {
  btn.addEventListener('click', function () {
    tabs.forEach(function (b) { b.setAttribute('aria-selected', b === btn ? 'true' : 'false'); });
    mapImg.src = btn.dataset.img;
    mapImg.alt = btn.dataset.alt;
    mapLabel.textContent = 'Selected: ' + btn.dataset.label;
    mapView.textContent = btn.dataset.view;
  });
});

// Clinical photo: blurred until the visitor chooses to see it
var reveal = document.getElementById('wound-reveal');
if (reveal) {
  reveal.querySelector('.reveal-btn').addEventListener('click', function () { reveal.classList.add('shown'); });
}

// Hero showcase loop: fade in one by one, hold, fade out up / up-right, repeat while visible
(function () {
  var stage = document.querySelector('.hero-stage');
  if (!stage) return;
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  stage.classList.add('js-loop');
  var order = ['.stage-back', '.stage-front', '.card-map', '.card-review', '.card-flow']
    .map(function (s) { return stage.querySelector(s); }).filter(Boolean);
  var inAt = [300, 1300, 2300, 3100, 3800];      // fade-in times (ms)
  var holdUntil = 9500;                           // start fading out
  var outGap = 350;                               // stagger between fade-outs
  var cycle = holdUntil + outGap * order.length + 1200;
  var timers = [], running = false;

  function clear() { timers.forEach(clearTimeout); timers = []; }
  function at(ms, fn) { timers.push(setTimeout(fn, ms)); }
  function reset() {
    stage.classList.add('no-anim');
    order.forEach(function (el) { el.classList.remove('is-in', 'is-out'); });
    void stage.offsetWidth;                       // apply the hidden state instantly
    stage.classList.remove('no-anim');
  }
  function run() {
    clear(); reset();
    order.forEach(function (el, i) { at(inAt[i], function () { el.classList.add('is-in'); }); });
    order.slice().reverse().forEach(function (el, i) {
      at(holdUntil + i * outGap, function () { el.classList.add('is-out'); el.classList.remove('is-in'); });
    });
    at(cycle, function () { if (running) run(); });
  }
  function showAll() { clear(); order.forEach(function (el) { el.classList.remove('is-out'); el.classList.add('is-in'); }); }

  if ('IntersectionObserver' in window) {
    new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting && !running) { running = true; run(); }
        else if (!e.isIntersecting && running) { running = false; showAll(); }
      });
    }, { threshold: 0.35 }).observe(stage);
  } else { running = true; run(); }
})();

// "Who it's for" dropdown
document.querySelectorAll('.nav-drop').forEach(function (d) {
  var b = d.querySelector('button');
  b.addEventListener('click', function (e) {
    e.stopPropagation();
    var open = d.classList.toggle('open');
    b.setAttribute('aria-expanded', open ? 'true' : 'false');
  });
});
document.addEventListener('click', function () {
  document.querySelectorAll('.nav-drop.open').forEach(function (d) {
    d.classList.remove('open'); d.querySelector('button').setAttribute('aria-expanded', 'false');
  });
});
document.addEventListener('keydown', function (e) {
  if (e.key === 'Escape') document.querySelectorAll('.nav-drop.open').forEach(function (d) {
    d.classList.remove('open'); var b = d.querySelector('button'); b.setAttribute('aria-expanded', 'false'); b.focus();
  });
});
