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
