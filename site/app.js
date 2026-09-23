/* ============================================================================
   kadabra — one script, no framework.
   Source of truth: site/.check/app.src.js  ->  site/app.js  (python .check/build.py)
   ========================================================================== */
(function () {
"use strict";

var mq = matchMedia('(prefers-reduced-motion: reduce)');
var reduce = mq.matches;
var NS = 'http://www.w3.org/2000/svg';
var STAGE = !reduce && innerWidth > 900;
if (STAGE) document.documentElement.classList.add('staged');
var SUITS = ['spade', 'heart', 'diamond', 'club'];

/* ---- the one owned asset: one path, lerped number for number -------------- */
var PATHS = {
  "square": "M50 20 C53.33 20 56.67 20 60 20 C63.33 20 66.67 20 70 20 C73.33 20 76.67 20 80 20 C80 23.33 80 26.67 80 30 C80 33.33 80 36.67 80 40 C80 43.33 80 46.67 80 50 C80 53.33 80 56.67 80 60 C80 63.33 80 66.67 80 70 C80 73.33 80 76.67 80 80 C76.67 80 73.33 80 70 80 C66.67 80 63.33 80 60 80 C56.67 80 53.33 80 50 80 C46.67 80 43.33 80 40 80 C36.67 80 33.33 80 30 80 C26.67 80 23.33 80 20 80 C20 76.67 20 73.34 20 70.01 C20 66.68 20 63.36 20 60.03 C20 56.7 20 53.37 20 50.04 C20 46.71 20 43.38 20 40.05 C20 36.72 20 33.4 20 30.07 C20 26.74 20 23.41 20 20.08 C23.32 20.05 26.63 20.03 29.95 20 C33.29 20 36.63 20 39.97 20 C43.32 20 46.66 20 50 20 Z",
  "smooth-spade": "M50 9 C53.28 12.93 56.56 16.86 59.84 20.79 C63.12 24.71 66.4 28.64 69.69 32.56 C72.98 36.48 76.75 40.13 79.57 44.31 C82.4 48.5 86.31 53.19 86.62 57.68 C86.94 62.18 84.79 68.85 81.47 71.3 C78.14 73.76 71.01 73.9 66.68 72.43 C62.36 70.96 59.23 65.81 55.5 62.5 C56.17 65.87 56.4 69.4 57.5 72.61 C58.61 75.83 60.15 79.07 62.15 81.8 C64.15 84.53 67.05 86.6 69.5 89 C65.17 89 60.83 89 56.5 89 C52.17 89 47.83 89 43.5 89 C39.17 89 34.83 89 30.5 89 C32.95 86.6 35.85 84.53 37.85 81.8 C39.85 79.07 41.39 75.83 42.5 72.61 C43.6 69.4 43.83 65.87 44.5 62.5 C41.36 65.57 38.85 69.97 35.09 71.71 C31.34 73.45 25.59 74.33 21.99 72.95 C18.39 71.56 14.52 67.16 13.5 63.41 C12.48 59.67 14.09 54.38 15.86 50.46 C17.63 46.55 21.32 43.38 24.14 39.91 C26.95 36.44 29.9 33.05 32.77 29.62 C35.65 26.19 38.52 22.75 41.39 19.31 C44.26 15.88 47.13 12.44 50 9 Z",
  "smooth-heart": "M50 27 C52 24.53 53.51 21.35 56.01 19.6 C58.51 17.86 61.94 16.71 64.99 16.53 C68.04 16.34 71.54 17.14 74.31 18.48 C77.08 19.83 79.75 22.14 81.61 24.62 C83.48 27.09 84.82 30.3 85.48 33.35 C86.15 36.4 86.09 39.81 85.58 42.91 C85.08 46.02 83.8 49.1 82.45 51.99 C81.1 54.87 79.3 57.59 77.46 60.21 C75.62 62.83 73.55 65.3 71.42 67.7 C69.3 70.11 67.04 72.39 64.73 74.62 C62.42 76.84 60.02 78.98 57.57 81.05 C55.11 83.11 52.52 85.02 50 87 C47.48 85.02 44.89 83.11 42.44 81.05 C39.98 78.99 37.58 76.84 35.27 74.62 C32.96 72.4 30.7 70.11 28.58 67.7 C26.45 65.3 24.38 62.83 22.54 60.21 C20.7 57.59 18.9 54.87 17.55 51.99 C16.2 49.11 14.92 46.02 14.42 42.91 C13.91 39.81 13.85 36.4 14.52 33.35 C15.18 30.3 16.52 27.09 18.39 24.62 C20.25 22.14 22.92 19.83 25.69 18.48 C28.46 17.14 31.96 16.34 35.01 16.53 C38.06 16.71 41.49 17.86 43.99 19.6 C46.49 21.35 48 24.53 50 27 Z",
  "smooth-diamond": "M50 7 C51.5 9.63 52.92 12.3 54.49 14.88 C56.06 17.46 57.71 20 59.43 22.49 C61.14 24.98 62.93 27.42 64.78 29.81 C66.63 32.2 68.55 34.54 70.52 36.83 C72.5 39.13 74.53 41.37 76.61 43.56 C78.69 45.75 80.87 47.85 83 50 C80.87 52.15 78.69 54.25 76.61 56.44 C74.53 58.63 72.5 60.87 70.52 63.17 C68.55 65.46 66.63 67.8 64.78 70.19 C62.93 72.58 61.14 75.02 59.43 77.51 C57.71 80 56.06 82.54 54.49 85.12 C52.92 87.7 51.5 90.37 50 93 C48.5 90.37 47.08 87.7 45.51 85.12 C43.94 82.54 42.29 80 40.57 77.51 C38.86 75.02 37.07 72.58 35.22 70.19 C33.37 67.8 31.45 65.46 29.48 63.17 C27.5 60.87 25.47 58.63 23.39 56.44 C21.31 54.25 19.13 52.15 17 50 C19.13 47.85 21.31 45.75 23.39 43.56 C25.47 41.37 27.5 39.13 29.48 36.83 C31.45 34.54 33.37 32.2 35.22 29.81 C37.07 27.42 38.86 24.98 40.57 22.49 C42.29 20 43.94 17.46 45.51 14.88 C47.08 12.3 48.5 9.63 50 7 Z",
  "smooth-club": "M50 8.5 C53.86 9.77 58.48 10.02 61.59 12.32 C64.7 14.61 67.51 18.58 68.64 22.27 C69.78 25.96 68.48 30.41 68.4 34.47 C72.17 35.78 76.67 36.12 79.7 38.4 C82.74 40.68 85.48 44.55 86.62 48.18 C87.75 51.8 87.71 56.54 86.51 60.15 C85.31 63.75 82.51 67.58 79.43 69.8 C76.35 72.03 71.84 73.49 68.05 73.5 C64.25 73.51 60.45 71.07 56.65 69.86 C57.96 73.52 58.53 77.67 60.59 80.86 C62.64 84.05 66.2 86.29 69 89 C64.78 89 60.56 89 56.33 89 C52.11 89 47.89 89 43.67 89 C39.44 89 35.22 89 31 89 C33.8 86.29 37.36 84.05 39.41 80.86 C41.47 77.67 42.04 73.52 43.35 69.86 C38.75 71.02 33.92 73.9 29.54 73.35 C25.15 72.79 19.87 69.9 17.03 66.5 C14.2 63.11 12.29 57.4 12.53 52.98 C12.76 48.56 15.25 43.08 18.42 40 C21.6 36.92 27.19 36.34 31.57 34.5 C31.5 30.44 30.21 26 31.35 22.3 C32.48 18.6 35.29 14.62 38.4 12.32 C41.51 10.02 46.13 9.77 50 8.5 Z",
  "sharp-spade": "M50 6 C53.11 9.46 56.23 12.92 59.34 16.38 C62.45 19.84 65.57 23.3 68.68 26.76 C71.79 30.22 74.91 33.68 78.02 37.14 C80.68 40.77 83.34 44.4 86 48.04 C86 52.69 86 57.35 86 62 C83.33 63.33 80.67 64.67 78 66 C75.33 67.33 72.67 68.67 70 70 C65.33 67.33 60.67 64.67 56 62 C58 66.67 60 71.33 62 76 C64 80.67 66 85.33 68 90 C64 90 60 90 56 90 C52 90 48 90 44 90 C40 90 36 90 32 90 C34 85.33 36 80.67 38 76 C40 71.33 42 66.67 44 62 C41.67 63.33 39.33 64.67 37 66 C34.67 67.33 32.33 68.67 30 70 C27.33 68.67 24.67 67.33 22 66 C19.33 64.67 16.67 63.33 14 62 C14 57.35 14 52.69 14 48.04 C16.66 44.4 19.32 40.77 21.98 37.14 C25.09 33.68 28.21 30.22 31.32 26.76 C34.43 23.3 37.55 19.84 40.66 16.38 C43.77 12.92 46.89 9.46 50 6 Z",
  "sharp-heart": "M50 30.3 C51.58 28.4 53.17 26.5 54.75 24.6 C56.33 22.7 57.92 20.8 59.5 18.9 C62.92 18.9 66.34 18.9 69.76 18.9 C72.54 20.53 75.32 22.17 78.1 23.8 C80.61 26.13 83.12 28.45 85.63 30.77 C85.79 34.12 85.94 37.47 86.1 40.83 C85.09 43.88 84.09 46.93 83.08 49.98 C80.87 52.6 78.67 55.21 76.46 57.83 C74.26 60.44 72.05 63.06 69.85 65.67 C67.64 68.28 65.44 70.9 63.23 73.51 C61.03 76.13 58.82 78.74 56.62 81.36 C54.41 83.97 52.21 86.59 50 89.2 C47.79 86.59 45.59 83.97 43.38 81.36 C41.18 78.74 38.97 76.13 36.77 73.51 C34.56 70.9 32.36 68.28 30.15 65.67 C27.95 63.06 25.74 60.44 23.54 57.83 C21.33 55.21 19.13 52.6 16.92 49.98 C15.91 46.93 14.91 43.88 13.9 40.83 C14.06 37.47 14.21 34.12 14.37 30.77 C16.88 28.45 19.39 26.13 21.9 23.8 C24.68 22.17 27.46 20.53 30.24 18.9 C33.66 18.9 37.08 18.9 40.5 18.9 C42.08 20.8 43.67 22.7 45.25 24.6 C46.83 26.5 48.42 28.4 50 30.3 Z",
  "sharp-diamond": "M50 6 C51.89 8.44 53.78 10.89 55.67 13.33 C57.56 15.78 59.44 18.22 61.33 20.67 C63.22 23.11 65.11 25.56 67 28 C68.89 30.44 70.78 32.89 72.67 35.33 C74.56 37.78 76.44 40.22 78.33 42.67 C80.22 45.11 82.11 47.56 84 50 C82.11 52.44 80.22 54.89 78.33 57.33 C76.44 59.78 74.56 62.22 72.67 64.67 C70.78 67.11 68.89 69.56 67 72 C65.11 74.44 63.22 76.89 61.33 79.33 C59.44 81.78 57.56 84.22 55.67 86.67 C53.78 89.11 51.89 91.56 50 94 C48.11 91.56 46.22 89.11 44.33 86.67 C42.44 84.22 40.56 81.78 38.67 79.33 C36.78 76.89 34.89 74.44 33 72 C31.11 69.56 29.22 67.11 27.33 64.67 C25.44 62.22 23.56 59.78 21.67 57.33 C19.78 54.89 17.89 52.44 16 50 C17.89 47.56 19.78 45.11 21.67 42.67 C23.56 40.22 25.44 37.78 27.33 35.33 C29.22 32.89 31.11 30.44 33 28 C34.89 25.56 36.78 23.11 38.67 20.67 C40.56 18.22 42.44 15.78 44.33 13.33 C46.22 10.89 48.11 8.44 50 6 Z",
  "sharp-club": "M50 12 C52.83 13.67 55.67 15.33 58.5 17 C61.33 18.67 64.17 20.33 67 22 C67 26.25 67.01 30.51 67.01 34.76 C70.34 35.55 73.67 36.33 77 37.12 C80.34 39.08 83.67 41.04 87 43 C87 47.67 87 52.33 87 57 C84.17 58.67 81.33 60.33 78.5 62 C75.67 63.67 72.83 65.33 70 67 C66.44 64.91 62.88 62.81 59.32 60.72 C60.1 65.6 60.88 70.48 61.66 75.36 C62.44 80.24 63.22 85.12 64 90 C59.33 90 54.67 90 50 90 C45.33 90 40.67 90 36 90 C36.78 85.12 37.56 80.24 38.34 75.36 C39.12 70.48 39.9 65.6 40.68 60.72 C37.12 62.81 33.56 64.91 30 67 C27.17 65.33 24.33 63.67 21.5 62 C18.67 60.33 15.83 58.67 13 57 C13 52.33 13 47.67 13 43 C16.33 41.04 19.66 39.08 23 37.12 C26.33 36.33 29.66 35.55 32.99 34.76 C32.99 30.51 33 26.25 33 22 C35.83 20.33 38.67 18.67 41.5 17 C44.33 15.33 47.17 13.67 50 12 Z"
};
var TMPL = PATHS.square.split(/-?[\d.]+/);
var SQ = PATHS.square.match(/-?[\d.]+/g).map(Number);
var NUM = {};
Object.keys(PATHS).forEach(function (k) {
  NUM[k] = PATHS[k].match(/-?[\d.]+/g).map(Number);
});
function mix(key, t) {
  var n = NUM[key], s = '';
  for (var i = 0; i < TMPL.length; i++) {
    s += TMPL[i];
    if (i < SQ.length) s += (SQ[i] + (n[i] - SQ[i]) * t).toFixed(2);
  }
  return s;
}
var easeOut = function (t) { return 1 - Math.pow(1 - t, 3); };
var easeIO = function (t) { return t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; };
function rnd(a, b) { return a + Math.random() * (b - a); }
function suit() { return 'smooth-' + SUITS[(Math.random() * 4) | 0]; }

/* run a square -> suit morph on a single <path>, once */
function morphPath(el, key, dur, delay) {
  if (reduce) { el.setAttribute('d', mix(key, 1)); return; }
  el.setAttribute('d', PATHS.square);
  var t0 = 0;
  setTimeout(function () {
    requestAnimationFrame(function step(now) {
      if (!t0) t0 = now;
      var u = Math.min(1, (now - t0) / dur);
      el.setAttribute('d', mix(key, easeOut(u)));
      if (u < 1) requestAnimationFrame(step);
    });
  }, delay || 0);
}

/* ---- shared entrance observer -------------------------------------------- */
var seen = new IntersectionObserver(function (es) {
  es.forEach(function (e) {
    if (e.isIntersecting) { e.target.classList.add('in'); seen.unobserve(e.target); }
  });
}, { threshold: .18, rootMargin: '0px 0px -5% 0px' });
document.querySelectorAll('.rise').forEach(function (el) { seen.observe(el); });

var pair = document.getElementById('pair');
if (pair) new IntersectionObserver(function (es, o) {
  es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); o.unobserve(e.target); } });
}, { threshold: .35 }).observe(pair);

/* ---- numbers count once --------------------------------------------------- */
var nio = new IntersectionObserver(function (es) {
  es.forEach(function (e) {
    if (!e.isIntersecting) return;
    nio.unobserve(e.target);
    var el = e.target, end = +el.dataset.count, t0 = 0;
    requestAnimationFrame(function step(now) {
      if (!t0) t0 = now;
      var u = Math.min(1, (now - t0) / 1100);
      el.textContent = Math.round(end * easeOut(u)) + '%';
      if (u < 1) requestAnimationFrame(step);
    });
  });
}, { threshold: .6 });
document.querySelectorAll('[data-count]').forEach(function (el) {
  if (reduce) { el.textContent = el.dataset.count + '%'; }
  else { el.textContent = '0%'; if (!STAGE) nio.observe(el); }   /* staged: the scroll counts */
});

/* ==========================================================================
   ROUTER: three real pages, one shell. No reload, no framework.
   ========================================================================== */
(function () {
  var TITLES = {
    '/': 'kadabra. Talleres prácticos de IA para equipos en Costa Rica',
    '/workshop/': 'El taller: IA sin cortina de humo. kadabra',
    '/learn-more/': 'Más información: los números detrás del taller. kadabra'
  };
  var routes = Array.prototype.slice.call(document.querySelectorAll('.route'));
  var navs = Array.prototype.slice.call(document.querySelectorAll('[data-nav]'));
  var sweep = document.getElementById('sweep');

  function norm(p) {
    p = p.split('#')[0].split('?')[0];
    if (p.length > 1 && p.charAt(p.length - 1) !== '/') p += '/';
    return TITLES[p] ? p : '/';
  }
  function paint(path) {
    routes.forEach(function (r) { r.hidden = r.dataset.route !== path; });
    document.title = TITLES[path];
    navs.forEach(function (a) {
      if (a.dataset.nav === path) a.setAttribute('aria-current', 'page');
      else a.removeAttribute('aria-current');
    });
    window.scrollTo(0, 0);
  }
  function wipe() {
    if (reduce || !sweep) return;
    var main = document.getElementById('main');
    main.classList.remove('routing-in');
    void main.offsetWidth;
    main.classList.add('routing-in');
    sweep.classList.remove('go');
    void sweep.offsetWidth;
    sweep.classList.add('go');
  }
  function go(path, push) {
    path = norm(path);
    if (push) history.pushState({ p: path }, '', path);
    if (!reduce && document.startViewTransition) {
      document.startViewTransition(function () { paint(path); });
    } else {
      paint(path);
      wipe();
    }
  }
  document.addEventListener('click', function (e) {
    if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    var a = e.target.closest ? e.target.closest('a') : null;
    if (!a || a.target || a.hasAttribute('download')) return;
    var href = a.getAttribute('href') || '';
    if (href.charAt(0) !== '/' || href.indexOf('//') === 0) return;
    var path = norm(href);
    e.preventDefault();
    if (path === norm(location.pathname)) { window.scrollTo(0, 0); return; }
    go(path, true);
  });
  window.addEventListener('popstate', function () { go(location.pathname, false); });
  history.replaceState({ p: norm(location.pathname) }, '', location.pathname);
  paint(norm(location.pathname));
})();

/* ==========================================================================
   THE FIELD: sparse drifting squares that wake, morph and gather into a
   heart made of them. Grow it and the words come for it. Used by the hero
   and the closing CTA: one engine, same rules, top and bottom.
   ========================================================================== */
/* Interactive mode: while a field is being played the page holds still (the
   wheel, touch and scroll keys shake the chip instead), and the chip under
   the header is the way out. */
var Mode = (function () {
  var owner = null, chip = null;
  function build() {
    chip = document.createElement('div');
    chip.className = 'mode'; chip.setAttribute('role', 'status');
    chip.innerHTML = '<i class="dot" aria-hidden="true"></i><span>Modo interactivo</span>' +
      '<button type="button">Salir<svg viewBox="0 0 12 12" aria-hidden="true"><path d="M2 2l8 8M10 2l-8 8"/></svg></button>';
    chip.querySelector('button').addEventListener('click', function () { if (owner) owner.exit(); });
    document.body.appendChild(chip);
  }
  function shake() {
    if (!chip) return;
    chip.classList.remove('shake'); void chip.offsetWidth; chip.classList.add('shake');
  }
  function block(e) { if (owner) { e.preventDefault(); shake(); } }
  addEventListener('wheel', block, { passive: false });
  addEventListener('touchmove', block, { passive: false });
  addEventListener('keydown', function (e) {
    if (owner && /^( |PageUp|PageDown|ArrowUp|ArrowDown|Home|End)$/.test(e.key)) block(e);
  });
  return {
    on: function (who) {
      if (!chip) build();
      owner = who;
      chip.classList.add('on', 'fresh');
      setTimeout(function () { chip.classList.remove('fresh'); }, 1600);
    },
    off: function (who) { if (owner !== who) return; owner = null; if (chip) chip.classList.remove('on', 'fresh'); },
    shake: shake
  };
})();

function makeField(svg, opt) {
  var W = opt.w, H = opt.h;
  var wide = innerWidth > 860;
  var COUNT = wide ? opt.n : Math.min(opt.n, opt.nm);
  var EXTRA = wide ? Math.round(COUNT * .35) : Math.round(COUNT * .2);  /* density near the pointer */
  var BASE = opt.base, PEAK = opt.peak;
  var R = opt.r;
  /* shape is immediate (most of the way at 100 ms); the opacity ramp is slow
     on purpose: never 0.15 of opacity inside 50 ms, anywhere. */
  var WAKE_D = 160, FADE_UP = 700, HOLD = 1300, BACK = 520, FADE_DN = 900;
  var SPAWN = 620, BORN = 900;
  var CAP = 40;                              /* marks in a full heart: 100% */
  var REBIRTH = 20000;                       /* ms of reading after a defeat */
  var RAMP = .4;                             /* difficulty per phrase: the sixth plays like the old third */
  var LIVES = 3;                             /* three hits and it is over, whatever the size */
  var marks = [], frag = document.createDocumentFragment();
  var host = svg.parentNode;

  /* quiet zones hug the real text: one box per rendered line of copy, read
     from the DOM and mapped into field units, so squares can come close to
     the words without ever sitting on them. Falls back to opt.quiet. */
  var zones = [];
  function measure() {
    var b = svg.getBoundingClientRect();
    var sc = Math.max(b.width / W, b.height / H);
    var ox = (b.width - W * sc) / 2, oy = (b.height - H * sc) / 2;
    zones = [];
    (opt.text || []).forEach(function (el) {
      var rects = el.getClientRects();
      for (var i = 0; i < rects.length; i++) {
        var r = rects[i]; if (!r.width) continue;
        var pad = 26 / sc;
        zones.push({ x0: (r.left - b.left - ox) / sc - pad, x1: (r.right - b.left - ox) / sc + pad,
                     y0: (r.top - b.top - oy) / sc - pad, y1: (r.bottom - b.top - oy) / sc + pad });
      }
    });
    if (!zones.length && opt.quiet) zones = [opt.quiet];
  }
  measure();
  function inQuiet(x, y, m) {
    m = m || 0;
    for (var i = 0; i < zones.length; i++) {
      var z = zones[i];
      if (x > z.x0 - m && x < z.x1 + m && y > z.y0 - m && y < z.y1 + m) return z;
    }
    return null;
  }
  /* a spot that is never on the copy, nor on the copy's doorstep */
  function spot() {
    for (var k = 0; k < 40; k++) {
      var x = rnd(40, W - 40), y = rnd(40, H - 40);
      if (!inQuiet(x, y, 70)) return { x: x, y: y };
    }
    return { x: rnd(40, W - 40), y: 40 };
  }
  function seed(m) {
    var at = spot();
    m.x = at.x; m.y = at.y;
    m.vx = m.vx0 = rnd(-11, 11); m.vy = m.vy0 = rnd(-8, 8);
    m.rot = Math.random() * 360; m.vr = rnd(-7, 7);
    m.t = 0; m.o = 0; m.phase = 'idle'; m.at = 0; m.held = false; m.live = !m.spare; m.freeTil = 0; m.hs = 1;
    m.born = Math.hypot(at.x - W / 2, at.y - H / 2) / Math.hypot(W / 2, H / 2) * 1100 + rnd(0, 260);
    m.p.setAttribute('d', PATHS.square);
    if (m.glow) { m.glow = false; m.g.classList.remove('glow'); }
    m.g.setAttribute('opacity', '0');
  }

  for (var i = 0; i < COUNT + EXTRA; i++) {
    var g = document.createElementNS(NS, 'g'), p = document.createElementNS(NS, 'path');
    p.setAttribute('fill', 'currentColor');
    p.setAttribute('d', PATHS.square);
    g.appendChild(p);
    if (i % 6 === 4) g.setAttribute('fill', '#A81A2C');
    frag.appendChild(g);
    var spare = i >= COUNT, size = rnd(14, 40);
    var m = { g: g, p: p, s: size, sc: 1, depth: size / 40, base: BASE, peak: PEAK,
              suit: suit(), spare: spare, glow: false };
    seed(m);
    if (!spare) m.o = BASE;
    marks.push(m);
  }
  svg.appendChild(frag);

  /* the gathering: the marks the hand draws in are swallowed one by one into
     a heart that is made of them. It pulses with every one, reddens as it
     fills, and follows the hand: never glued to it, never left behind. */
  var heart = { g: document.createElementNS(NS, 'g'), p: document.createElementNS(NS, 'path'),
                mass: 0, held: [], x: W / 2, y: H / 2, vx: 0, vy: 0, sc: 0, o: 0, relAt: 0, eatAt: 0,
                pulse: 0, hurt: 0, debt: 0, burst: 0, fill: '' };
  heart.p.setAttribute('fill', '#FFFFFF'); heart.p.setAttribute('d', mix('smooth-heart', 1));
  heart.g.setAttribute('class', 'glow heartmark'); heart.g.setAttribute('opacity', '0');
  heart.g.appendChild(heart.p); svg.appendChild(heart.g);
  /* the war layer: fuel and sparks under the letters, letters over everything */
  var war = document.createElementNS(NS, 'g'); war.setAttribute('class', 'war'); svg.appendChild(war);
  var fuelG = document.createElementNS(NS, 'g'); war.appendChild(fuelG);
  var ltrG = document.createElementNS(NS, 'g'); war.appendChild(ltrG);
  var dots = [];
  for (var d = 0; d < 64; d++) {
    var c = document.createElementNS(NS, 'circle');
    c.setAttribute('r', '0'); c.setAttribute('opacity', '0'); fuelG.appendChild(c);
    dots.push({ el: c, on: false, x: 0, y: 0, vx: 0, vy: 0, t: 0, ttl: 1, r: 4, o: .5, fill: '' });
  }
  function puff(x, y, vx, vy, ttl, r, o, fill) {
    for (var i = 0; i < dots.length; i++) {
      var q = dots[i]; if (q.on) continue;
      q.on = true; q.x = x; q.y = y; q.vx = vx; q.vy = vy; q.t = 0; q.ttl = ttl; q.r = r; q.o = o;
      if (q.fill !== fill) { q.fill = fill; q.el.setAttribute('fill', fill); }
      return;
    }
  }
  function sparks(x, y, n, fill) {
    for (var i = 0; i < n; i++) {
      var a = Math.random() * Math.PI * 2, s = rnd(120, 360);
      puff(x, y, Math.cos(a) * s, Math.sin(a) * s, rnd(.35, .6), rnd(3, 6), .9, fill);
    }
  }

  var game = { phase: 'calm', armedAt: 0, wave: 0, nextWord: 0, word: null, deadAt: 0, offAt: 0, hits: 0 };
  svg.__field = { heart: heart, game: game, marks: marks, opt: opt };   /* for the checks */
  var WORDS = 'La IA inventó cifras para la junta | ChatGPT citó una ley que no existe | Pegamos la planilla en un chat | Nadie revisó el pago de la IA | El bot prometió lo que no damos | Se filtraron las cédulas de clientes | Hacienda nos multó por la IA | El contrato traía una cláusula inventada | La PRODHAB abrió una investigación | Nos demandaron y la IA no responde'.split(' | ');
  var cv = document.createElement('canvas').getContext('2d');
  function fontReady() { return !document.fonts || document.fonts.check('800 100px Gabarito'); }
  if (document.fonts && document.fonts.load) document.fonts.load('800 100px Gabarito');

  /* a word laid out letter by letter, from real glyph widths, so it reads as
     one word before it comes apart */
  function layout(text) {
    /* a phrase wraps into short lines, about fifteen characters each */
    var lines = [], cur = '';
    text.split(' ').forEach(function (wd) {
      if (cur && (cur + ' ' + wd).length > 15) { lines.push(cur); cur = wd; } else cur = cur ? cur + ' ' + wd : wd;
    });
    if (cur) lines.push(cur);
    var fs = lines.length > 2 ? 42 : lines.length > 1 ? 48 : 58;
    var maxW = W * .24, widest = 0;
    cv.font = '800 ' + fs + 'px Gabarito, sans-serif';
    lines.forEach(function (ln) { widest = Math.max(widest, cv.measureText(ln).width); });
    if (widest > maxW) fs *= maxW / widest;
    cv.font = '800 ' + fs + 'px Gabarito, sans-serif';
    var out = [], maxTx = 0;
    lines.forEach(function (ln, li) {
      var lw = cv.measureText(ln).width, y = (li - (lines.length - 1) / 2) * fs * .98;
      for (var i = 0; i < ln.length; i++) {
        var ch = ln.charAt(i); if (ch === ' ') continue;
        var x = -lw / 2 + cv.measureText(ln.slice(0, i)).width + cv.measureText(ch).width / 2;
        out.push({ ch: ch, tx: x, ty: y });
        maxTx = Math.max(maxTx, Math.abs(x));
      }
    });
    /* box half-extents, for placing the word clear of the copy */
    return { letters: out, fs: fs, halfW: maxTx + fs * .6, halfH: fs * (lines.length * .5 + .1) };
  }
  function newWord(now) {
    var text = WORDS[game.wave % WORDS.length];
    var lay = layout(text);
    var refX = ptr.on ? ptr.x : heart.x;
    var side = refX < W / 2 ? 1 : -1;                 /* the far side from the hand */
    /* the field is cropped to the screen: place the word in what is seen */
    var bb = svg.getBoundingClientRect(), vw = bb.width / Math.max(bb.width / W, bb.height / H);
    var v0 = (W - vw) / 2, v1 = v0 + vw;
    var cx = side > 0 ? Math.min(v0 + vw * .84, v1 - 30 - lay.halfW) : Math.max(v0 + vw * .16, v0 + 30 + lay.halfW);
    var w = { side: side, cx: cx, cy: H / 2, x: cx + side * 200, at: now, letters: [], front: 0, back: lay.letters.length - 1,
              lastAt: 0, gap: Math.max(260, 460 - game.wave * RAMP * 40), gone: 0, doneAt: 0 };
    w.readAt = now + 700 + Math.max(300, 650 - game.wave * RAMP * 90) + 55 * lay.letters.length;
    lay.letters.forEach(function (l, i) {
      var t = document.createElementNS(NS, 'text');
      t.setAttribute('font-size', lay.fs.toFixed(1)); t.setAttribute('text-anchor', 'middle');
      t.setAttribute('dominant-baseline', 'central'); t.setAttribute('opacity', '0');
      t.textContent = l.ch; ltrG.appendChild(t);
      w.letters.push({ el: t, ch: l.ch, tx: l.tx, ty: l.ty, x: 0, y: 0, vx: 0, vy: 0, st: 'held', t0: 0, o: 0, i: i, fuelAt: 0 });
    });
    game.word = w;
  }
  function endWord() {
    if (!game.word) return;
    game.word.letters.forEach(function (l) { if (l.el.parentNode) ltrG.removeChild(l.el); });
    game.word = null;
  }
  /* never without asking: a small pill floats by the heart. Yes starts the
     words at once; the cross puts it away for good (until a reload). */
  var askEl = document.createElement('div'), askP = { x: 0, y: 0, placed: false, lx: 0, ly: 0, sc: 1 };
  askEl.className = 'ask';
  askEl.innerHTML = '<button type="button" class="yes">¿Jugar?</button>' +
    '<button type="button" class="no" aria-label="Ahora no"><svg viewBox="0 0 12 12" aria-hidden="true"><path d="M2 2l8 8M10 2l-8 8"/></svg></button>';
  host.appendChild(askEl);
  function ask() { game.phase = 'asking'; askP.placed = false; askEl.classList.add('on'); }
  function unask() { askEl.classList.remove('on'); if (game.phase === 'asking') game.phase = 'calm'; }
  askEl.querySelector('.yes').addEventListener('click', function () { unask(); arm(performance.now()); });
  askEl.querySelector('.no').addEventListener('click', function () { unask(); game.noAsk = true; });
  var ctl = { exit: exit };
  function arm(now) {
    game.phase = 'armed'; game.armedAt = now; game.nextWord = now + 900; game.wave = 0; game.hits = 0;
    host.classList.add('armed');
    Mode.on(ctl);
  }
  function disarm() { game.phase = 'calm'; host.classList.remove('armed'); endWord(); Mode.off(ctl); }
  /* out of interactive mode by choice: nothing lost, the heart just lets go,
     and this field does not gather again until the page is reloaded */
  function exit() {
    game.off = true;
    disarm();
    while (heart.held.length) release(performance.now(), 60, 180);
  }
  host.addEventListener('pointerdown', function (e) {
    if (game.phase === 'armed' && !e.target.closest('.ask')) Mode.shake();
  });
  var LIVE = opt.copy ? opt.copy.els.map(function (el) { return el.textContent; }) : null;
  function setCopy(lines) {
    if (!opt.copy) return;
    opt.copy.els.forEach(function (el, i) {
      if (el.textContent === lines[i]) return;
      el.classList.add('swapping');
      setTimeout(function () { el.textContent = lines[i]; el.classList.remove('swapping'); measure(); }, 320);
    });
    setTimeout(measure, 500);
  }
  var pointT = 0;
  function die(now) {
    game.phase = 'dead'; game.deadAt = now;
    Mode.off(ctl);
    clearTimeout(pointT);
    pointT = setTimeout(function () { if (game.phase === 'dead') host.classList.add('pointing'); }, 3000);
    host.classList.remove('armed'); host.classList.add('dead');
    endWord();
    sparks(heart.x, heart.y, 28, '#FFFFFF');
    while (heart.held.length) release(now, 520, 940);
    for (var i = 0; i < marks.length; i++) {
      var m = marks[i]; if (!m.live) continue;
      var dx = m.x - heart.x, dy = m.y - heart.y, dd = Math.hypot(dx, dy) || 1, s = rnd(520, 940);
      m.vx = dx / dd * s; m.vy = dy / dd * s; m.phase = 'gone'; m.freeTil = now + 3000;
      /* the visible keep their strength and fade out; the ones just let out
         of the heart rise briefly into view first: no flash either way */
      m.gt = m.o > .02 ? .3 : 0; m.go = m.o > .02 ? m.o : .55;
    }
    heart.burst = 1;
    setCopy(opt.copy ? opt.copy.dead : []);
  }
  function reborn(now) {
    clearTimeout(pointT);
    host.classList.remove('dead', 'pointing');
    if (LIVE) setCopy(LIVE);
    t0 = now; game.phase = 'calm'; game.wave = 0; game.word = null; game.hits = 0;
    heart.mass = 0; heart.held = []; heart.o = 0; heart.sc = 0; heart.burst = 0; heart.debt = 0;
    measure();
    marks.forEach(function (m) { seed(m); });
  }

  var par = { x: 0, y: 0 };                 /* pointer parallax, eased */
  function place(m) {
    var px = m.x + par.x * 26 * m.depth, py = m.y + par.y * 18 * m.depth;
    m.g.setAttribute('transform', 'translate(' + px.toFixed(1) + ' ' + py.toFixed(1) +
      ') rotate(' + m.rot.toFixed(1) + ') scale(' + (m.s * m.sc / 100).toFixed(4) + ') translate(-50 -50)');
  }
  marks.forEach(function (m) { m.g.setAttribute('opacity', m.o.toFixed(3)); place(m); });
  if (reduce) return;                       /* a static sparse set of squares */

  /* staged arrival: the field ripples outward from the copy on first sight */
  marks.forEach(function (m) { m.g.setAttribute('opacity', '0'); });

  var ptr = { x: -9e3, y: -9e3, on: false };
  function local(e) {
    var b = svg.getBoundingClientRect();
    var sc = Math.max(b.width / W, b.height / H);
    return { x: (e.clientX - b.left - (b.width - W * sc) / 2) / sc,
             y: (e.clientY - b.top - (b.height - H * sc) / 2) / sc };
  }
  host.addEventListener('pointermove', function (e) {
    var l = local(e); ptr.x = l.x; ptr.y = l.y; ptr.on = true;
  }, { passive: true });
  host.addEventListener('pointerleave', function () { ptr.on = false; ptr.x = ptr.y = -9e3; }, { passive: true });
  addEventListener('resize', measure, { passive: true });
  /* the copy moves (condensed / armed / dead): re-measure now and once the
     transition has had time to settle */
  new MutationObserver(function () {
    measure(); setTimeout(measure, 500); setTimeout(measure, 1200);
  }).observe(host, { attributes: true, attributeFilter: ['class'] });
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(measure);

  var running = false, t0 = 0;
  new IntersectionObserver(function (es) { running = es[0].isIntersecting; }, { threshold: 0 }).observe(host);

  /* one held mark climbs back out of the heart */
  function release(now, s0, s1) {
    var mr = heart.held.pop(); if (!mr) return;
    heart.mass--; heart.relAt = now;
    var hr = 16 + Math.sqrt(heart.mass + 1) * 11;
    var ang = Math.random() * Math.PI * 2, sp0 = rnd(s0, s1);
    mr.x = heart.x + Math.cos(ang) * hr * .45; mr.y = heart.y + Math.sin(ang) * hr * .45;
    mr.vx = Math.cos(ang) * sp0 + heart.vx * .4; mr.vy = Math.sin(ang) * sp0 + heart.vy * .4;
    mr.live = true; mr.held = false; mr.phase = 'spawn'; mr.at = now; mr.o = 0; mr.born = 0; mr.t = 0;
    mr.freeTil = now + 500;
    mr.p.setAttribute('d', PATHS.square);
    if (mr.glow) { mr.glow = false; mr.g.classList.remove('glow'); }
  }
  function hex(c) { return [parseInt(c.slice(1, 3), 16), parseInt(c.slice(3, 5), 16), parseInt(c.slice(5, 7), 16)]; }
  var C_WHITE = hex('#FFFFFF'), C_PINK = hex('#DC6F7C'), C_RED = hex('#A81A2C'), C_GOLD = hex('#C9A227');
  function lerpC(a, b, t) { return [a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, a[2] + (b[2] - a[2]) * t]; }
  function css(c) { return 'rgb(' + Math.round(c[0]) + ',' + Math.round(c[1]) + ',' + Math.round(c[2]) + ')'; }

  var last = 0, spawnAt = 0;

  requestAnimationFrame(function tick(now) {
    requestAnimationFrame(tick);
    if (!running || document.hidden) { last = now; return; }
    var dt = last ? Math.min(.05, (now - last) / 1000) : 0; last = now;
    if (!t0) t0 = now;
    var armed = game.phase === 'armed', dead = game.phase === 'dead';

    /* the whole field leans a little against the pointer, more for the near
       (large) marks: depth without a single blurred pixel */
    var tx = ptr.on ? (ptr.x - W / 2) / W : 0, ty = ptr.on ? (ptr.y - H / 2) / H : 0;
    par.x += (tx - par.x) * Math.min(1, 3 * dt); par.y += (ty - par.y) * Math.min(1, 3 * dt);

    /* density: wake a spare square into the pointer's neighbourhood, fading in */
    if (ptr.on && !dead && now - spawnAt > (armed ? 160 + game.wave * RAMP * 50 : 170)) {
      for (var s = 0; s < marks.length; s++) {
        var sp = marks[s];
        if (sp.spare && !sp.live && !sp.held) {
          var sx = ptr.x + rnd(-R * .8, R * .8), syy = ptr.y + rnd(-R * .8, R * .8);
          sx = Math.max(24, Math.min(W - 24, sx)); syy = Math.max(24, Math.min(H - 24, syy));
          if (!armed && inQuiet(sx, syy, 30)) break;   /* never born on the copy */
          sp.live = true; sp.at = now; sp.phase = 'spawn'; sp.o = 0; sp.born = 0;
          sp.x = sx; sp.y = syy;
          spawnAt = now;
          break;
        }
      }
    }

    /* ---- the heart: weight, follow, pulse, colour ---- */
    var hr = heart.mass ? 16 + Math.sqrt(heart.mass) * 11 : 0;
    var pct = heart.mass / CAP;
    if (heart.mass === 0) {
      /* an empty heart only moves while it is invisible: a fading one stays put */
      if (heart.o < .02 && ptr.on) { heart.x = ptr.x; heart.y = ptr.y; heart.vx = heart.vy = 0; }
    } else {
      /* calm, it follows a hand that stays with it; armed, it follows any hand.
         A far hand, calm, gets nothing: the heart stays and comes apart. */
      var near0 = Math.hypot(ptr.x - heart.x, ptr.y - heart.y) < 300;
      var k = armed ? 95 : 62, drag = armed ? 12 : 9.5, chase = ptr.on && (armed || near0);
      var ax = chase ? (ptr.x - heart.x) * k : 0, ay = chase ? (ptr.y - heart.y) * k : 0;
      heart.vx += (ax - heart.vx * drag) * dt; heart.vy += (ay - heart.vy * drag) * dt;
      var hv = Math.hypot(heart.vx, heart.vy), HV = armed ? 1050 : 650;
      if (hv > HV) { heart.vx *= HV / hv; heart.vy *= HV / hv; }
      heart.x += heart.vx * dt; heart.y += heart.vy * dt;
      heart.x = Math.max(hr, Math.min(W - hr, heart.x)); heart.y = Math.max(hr, Math.min(H - hr, heart.y));
    }
    var far = Math.hypot(ptr.x - heart.x, ptr.y - heart.y);
    var feeding = ptr.on && !dead && !game.off && (heart.mass === 0 ? (heart.o < .02 || far < 120) : (armed || far < 300));
    /* a hand that leaves (or, before it is armed, runs off) lets it come apart */
    if (!ptr.on) { if (!game.offAt) game.offAt = now; } else game.offAt = 0;
    var letGo = heart.mass > 0 && !dead && (armed ? (!ptr.on && now - game.offAt > 1500) : !feeding);
    if (letGo && now - heart.relAt > 110) release(now, 26, 54);
    if (armed && heart.mass === 0 && !heart.held.length) disarm();

    heart.pulse -= heart.pulse * Math.min(1, 7 * dt);
    heart.hurt -= heart.hurt * Math.min(1, 3.5 * dt);
    var wantSc = heart.mass ? hr * 2 * (1 + .24 * heart.pulse) : 0;
    if (heart.burst) { heart.burst = Math.max(0, heart.burst - dt * 1.7); wantSc = heart.sc * (1 + 1.6 * dt); }
    heart.sc += (wantSc - heart.sc) * Math.min(1, (heart.burst ? 1 : 9) * dt);
    var wantO = heart.mass && !heart.burst ? .94 : 0;
    heart.o += (wantO - heart.o) * Math.min(1, (wantO ? 2.2 : 3.2) * dt);   /* never a flash */
    if (heart.burst && heart.o < .02) heart.burst = 0;
    if (game.phase === 'asking') {
      if (!heart.mass || host.classList.contains('condensed')) unask();
      else {
        var sb = svg.getBoundingClientRect(), hb = host.getBoundingClientRect();
        var ks = Math.max(sb.width / W, sb.height / H), aw = askEl.offsetWidth, ah = askEl.offsetHeight;
        if (!askP.placed) {
          /* it appears up and to the right of the heart, and stays there */
          var hx = sb.left - hb.left + (sb.width - W * ks) / 2 + heart.x * ks, hy = sb.top - hb.top + (sb.height - H * ks) / 2 + heart.y * ks;
          var rr = hr * ks;
          askP.x = Math.max(12, Math.min(hb.width - aw - 12, hx + rr * .7 + 14));
          askP.y = Math.max(12, Math.min(hb.height - ah - 12, hy - rr * .7 - ah - 10));
          askP.placed = true;
        }
        /* it only leans a few pixels toward the hand and swells as it nears */
        var pxl = sb.left - hb.left + (sb.width - W * ks) / 2 + ptr.x * ks - (askP.x + aw / 2);
        var pyl = sb.top - hb.top + (sb.height - H * ks) / 2 + ptr.y * ks - (askP.y + ah / 2);
        var pd = Math.hypot(pxl, pyl), near1 = ptr.on ? Math.max(0, 1 - pd / 260) : 0;
        var wl = near1 * 6 / (pd || 1);
        askP.lx += (pxl * wl - askP.lx) * Math.min(1, 8 * dt); askP.ly += (pyl * wl - askP.ly) * Math.min(1, 8 * dt);
        askP.sc += (1 + near1 * .06 - askP.sc) * Math.min(1, 8 * dt);
        askEl.style.transform = 'translate(' + (askP.x + askP.lx).toFixed(1) + 'px,' + (askP.y + askP.ly).toFixed(1) + 'px) scale(' + askP.sc.toFixed(3) + ')';
      }
    }
    heart.g.setAttribute('opacity', heart.o.toFixed(3));
    heart.g.setAttribute('transform', 'translate(' + heart.x.toFixed(1) + ' ' + heart.y.toFixed(1) +
      ') scale(' + (heart.sc / 100).toFixed(4) + ') translate(-50 -50)');
    var col = pct < .75 ? lerpC(C_WHITE, C_PINK, pct / .75) : lerpC(C_PINK, C_RED, Math.min(1, (pct - .75) / .25));
    if (heart.hurt > .01) col = lerpC(col, C_GOLD, heart.hurt);
    var fill = css(col);
    if (fill !== heart.fill) { heart.fill = fill; heart.p.setAttribute('fill', fill); }
    var tx0 = heart.mass ? heart.x : ptr.x, ty0 = heart.mass ? heart.y : ptr.y;   /* what pulls */
    var RR = armed ? R * 1.5 : R, VMAX = armed ? 190 : 90;

    /* ---- the words ---- */
    var w = game.word;
    if (armed && !w && now >= game.nextWord && fontReady()) { newWord(now); w = game.word; }
    if (w) {
      var slide = Math.min(1, (now - w.at) / 700);
      w.x = w.cx + w.side * 200 * (1 - easeOut(slide));
      /* never more than three pairs in the air: the rest wait their turn */
      var flying = 0;
      for (var fi = 0; fi < w.letters.length; fi++) if (w.letters[fi].st === 'fly' || w.letters[fi].st === 'queued') flying++;
      var canLaunch = now >= w.readAt && now - w.lastAt >= w.gap && w.front <= w.back && flying <= 4;
      if (canLaunch) {
        /* two threads: from the front of the phrase a pair fires, from the
           back two letters just dissolve. Half the phrase ever flies. */
        var arc0 = Math.random() < .5 ? 1 : -1;
        for (var q = 0; q < 2 && w.front <= w.back; q++) {
          var L = w.letters[w.front++];
          /* the two of a pair take opposite arcs, the second a beat later */
          L.st = 'queued'; L.go = now + q * rnd(340, 480); L.arc = q ? -arc0 : arc0;
        }
        for (var q2 = 0; q2 < 2 && w.front <= w.back; q2++) {
          var Lf = w.letters[w.back--];
          Lf.st = 'gone'; Lf.t0 = now + q2 * 140; Lf.fadeMs = 900; w.gone++;
        }
        w.lastAt = now;
      }
      var target = heart;   /* the heart is the mark, never the hand */
      for (var li = 0; li < w.letters.length; li++) {
        var L2 = w.letters[li];
        if (L2.st === 'queued' && now >= L2.go) {
          L2.st = 'fly'; L2.t0 = now;
          var ux = target.x - L2.x, uy = target.y - L2.y, ul = Math.hypot(ux, uy) || 1;
          ux /= ul; uy /= ul;
          L2.ux = ux; L2.uy = uy;
          L2.vx = ux * 140 - uy * L2.arc * 460; L2.vy = uy * 140 + ux * L2.arc * 460;
        }
        if (L2.st === 'held' || L2.st === 'queued') {
          L2.x = w.x + L2.tx; L2.y = w.cy + L2.ty;
          if (now - w.at > 60 * L2.i) L2.o = Math.min(1, L2.o + dt / .5);
          L2.el.setAttribute('transform', 'translate(' + L2.x.toFixed(1) + ' ' + L2.y.toFixed(1) + ')');
          L2.el.setAttribute('opacity', L2.o.toFixed(3));
        } else if (L2.st === 'fly') {
          /* homing for a moment only (longer each word), then it keeps its
             line and speeds up until it leaves the field: dodge at the right
             time and it is gone */
          var age = (now - L2.t0) / 1000;
          var seek = Math.min(2.4, 1 + game.wave * RAMP * .3);
          var vmax = (540 + 280 * Math.min(1, age / .5)) * (1 + game.wave * RAMP * .2);
          if (age < seek) {
            /* early on it aims wide of the heart, on its own side, and the
               offset closes: a curve in, not a straight line */
            var off = Math.max(0, 1 - age / .75) * 240 * L2.arc;
            var adx = target.x - L2.uy * off - L2.x, ady = target.y + L2.ux * off - L2.y, ad = Math.hypot(adx, ady) || 1;
            var steer = Math.min(1, (2.6 + 4.4 * Math.min(1, age / .4)) * (1 + game.wave * RAMP * .15) * dt);
            L2.vx += (adx / ad * vmax - L2.vx) * steer; L2.vy += (ady / ad * vmax - L2.vy) * steer;
          } else {
            var vs0 = Math.hypot(L2.vx, L2.vy) || 1, acc = 1 + 1.4 * dt;
            if (vs0 < vmax * 1.6) { L2.vx *= acc; L2.vy *= acc; }
          }
          var vs = Math.hypot(L2.vx, L2.vy);
          L2.x += L2.vx * dt; L2.y += L2.vy * dt;
          var dd = Math.hypot(target.x - L2.x, target.y - L2.y) || 1;
          if (now - L2.fuelAt > 55 && vs > 60) {
            L2.fuelAt = now;
            puff(L2.x - L2.vx / vs * 14, L2.y - L2.vy / vs * 14, -L2.vx * .1 + rnd(-24, 24), -L2.vy * .1 + rnd(-24, 24),
                 .4, rnd(3.5, 6), .45, '#E38A3C');
          }
          L2.el.setAttribute('transform', 'translate(' + L2.x.toFixed(1) + ' ' + L2.y.toFixed(1) + ') rotate(' +
            (Math.atan2(L2.vy, L2.vx) * 180 / Math.PI).toFixed(1) + ')');
          var hitR = heart.mass ? Math.max(26, hr * .7) : 30;
          var out = L2.x < -80 || L2.x > W + 80 || L2.y < -80 || L2.y > H + 80;
          if (dd < hitR || out || age > 3.4) {
            L2.st = 'gone'; L2.t0 = now; w.gone++;
            if (dd < hitR && heart.mass) {
              sparks(L2.x, L2.y, 7, '#C9A227');
              heart.hurt = 1; game.hits++;
              if (game.hits >= LIVES) { die(now); break; }
            }
          }
        } else if (L2.st === 'gone') {
          if (!L2.el.parentNode) continue;
          L2.o = Math.max(0, Math.min(1, 1 - (now - L2.t0) / (L2.fadeMs || 350)));
          L2.el.setAttribute('opacity', L2.o.toFixed(3));
          if (!L2.o) ltrG.removeChild(L2.el);
        }
      }
      if (game.word === w && w.gone >= w.letters.length) {
        if (!w.doneAt) w.doneAt = now;
        else if (now - w.doneAt > Math.max(400, 1300 - game.wave * RAMP * 250)) { endWord(); game.wave++; game.nextWord = now; }
      }
    }
    /* the reading time after a defeat, or the moment the hero steps aside */
    if (dead && (now - game.deadAt > REBIRTH || host.classList.contains('condensed'))) reborn(now);

    /* ---- fuel and sparks ---- */
    for (var di = 0; di < dots.length; di++) {
      var qd = dots[di]; if (!qd.on) continue;
      qd.t += dt;
      if (qd.t >= qd.ttl) { qd.on = false; qd.el.setAttribute('opacity', '0'); continue; }
      var u = qd.t / qd.ttl;
      qd.vx *= 1 - 2.2 * dt; qd.vy *= 1 - 2.2 * dt;
      qd.x += qd.vx * dt; qd.y += qd.vy * dt;
      qd.el.setAttribute('cx', qd.x.toFixed(1)); qd.el.setAttribute('cy', qd.y.toFixed(1));
      qd.el.setAttribute('r', (qd.r * (1 - u * .7)).toFixed(2));
      qd.el.setAttribute('opacity', (qd.o * (1 - u)).toFixed(3));
    }

    /* ---- the marks ---- */
    for (var i = 0; i < marks.length; i++) {
      var m = marks[i];
      if (!m.live) continue;
      var ent = Math.min(1, Math.max(0, (now - t0 - m.born) / BORN));  /* arrival */
      if (ent <= 0) continue;

      var dpx = ptr.x - m.x, dpy = ptr.y - m.y, dp = Math.hypot(dpx, dpy);
      var near = ptr.on && dp < RR;
      var free = m.freeTil > now;

      if (m.phase === 'gone') {
        m.x += m.vx * dt; m.y += m.vy * dt; m.rot += m.vr * 3 * dt;
        m.gt += dt;
        var env = m.gt < .3 ? m.gt / .3 : Math.max(0, 1 - (m.gt - .3) / 1.3);
        m.o = m.go * env;
        m.g.setAttribute('opacity', m.o.toFixed(3)); place(m);
        if (m.gt >= 1.6) { m.live = false; m.phase = 'idle'; m.o = 0; }
        continue;
      }

      /* the pointer pulls: near marks lean in, so the hand is felt at once.
         Once a heart exists, it is the heart that pulls. */
      var dhx = tx0 - m.x, dhy = ty0 - m.y, dh = Math.hypot(dhx, dhy) || 1;
      if (near && dh > 4 && !dead) {
        var pull = (1 - Math.min(1, dh / RR)) * (armed ? 1100 : 520 + heart.mass * 20) * dt;
        m.vx += dhx / dh * pull; m.vy += dhy / dh * pull;
      }
      /* and everything relaxes back to its own drift */
      m.vx += (m.vx0 - m.vx) * Math.min(1, 1.6 * dt);
      m.vy += (m.vy0 - m.vy) * Math.min(1, 1.6 * dt);

      var hush = 1, deepest = 0;
      /* the marks are scared of the words: they get out of their way */
      if (w) for (var lj = 0; lj < w.letters.length; lj++) {
        var LL = w.letters[lj]; if (LL.st === 'gone') continue;
        var rad = LL.st === 'held' ? 120 : 64;
        var ex = m.x - LL.x, ey = m.y - LL.y, ed = Math.hypot(ex, ey);
        if (ed < rad && ed > 0) {
          var f = (1 - ed / rad) * (LL.st === 'held' ? 620 : 900) * dt;
          m.vx += ex / ed * f; m.vy += ey / ed * f;
          if (LL.st === 'held') hush = Math.min(hush, .15 + .85 * ed / rad);
        }
      }

      m.x += m.vx * dt; m.y += m.vy * dt; m.rot += m.vr * dt;
      if (m.x < 20 || m.x > W - 20) { m.vx *= -1; m.vx0 *= -1; m.x = Math.max(20, Math.min(W - 20, m.x)); }
      if (m.y < 20 || m.y > H - 20) { m.vy *= -1; m.vy0 *= -1; m.y = Math.max(20, Math.min(H - 20, m.y)); }

      /* the quiet zones: the copy is never covered. A mark that drifts onto a
         line is eased out and dims on the way in, so nothing ever sits on a
         word at strength. (Armed, the copy has stepped back: the field is open.) */
      if (!armed) {
        for (var q2 = 0; q2 < zones.length; q2++) {
          var z = zones[q2];
          if (!(m.x > z.x0 && m.x < z.x1 && m.y > z.y0 && m.y < z.y1)) continue;
          var cx = (z.x0 + z.x1) / 2, cy = (z.y0 + z.y1) / 2;
          var dx = m.x - cx, dy = (m.y - cy) * 2.2, d2 = Math.hypot(dx, dy) || 1;
          m.vx += (dx / d2) * 150 * dt; m.vy += (dy / d2) * 150 * dt;
          var deep = Math.min(m.x - z.x0, z.x1 - m.x, m.y - z.y0, z.y1 - m.y) / 60;
          if (deep > deepest) deepest = deep;
        }
        hush *= 1 - .85 * Math.min(1, deepest);
      }
      /* a mark on its way into the heart dims as it arrives, then is swallowed:
         it is gone from the field and the heart grows by one. One at a time,
         at a pace: growing is deliberate work. */
      if (feeding && m.phase !== 'spawn') {
        var eat = Math.max(34, hr * .7), band = 48;
        if (dh < eat + band) hush *= Math.max(0, Math.min(1, (dh - eat * .35) / (eat * .65 + band)));
        /* swallowed only once it has all but faded: never a flash */
        if (dh < eat && m.o * m.hs * ent < .06 && now - heart.eatAt > (armed ? 70 + game.wave * RAMP * 25 : 110)) {
          m.live = false; m.held = true; m.o = 0; m.g.setAttribute('opacity', '0');
          heart.held.push(m); heart.mass++; heart.eatAt = now; heart.pulse = 1;
          if (game.phase === 'calm' && !game.noAsk && heart.mass >= CAP * .5 && !host.classList.contains('condensed')) ask();
          continue;
        }
      }
      var spd = Math.hypot(m.vx, m.vy);
      if (spd > VMAX && !free) { m.vx *= VMAX / spd; m.vy *= VMAX / spd; }

      var el = now - m.at;
      if (m.phase === 'spawn') {
        m.o = m.base * Math.min(1, el / SPAWN);
        if (el >= SPAWN) { m.phase = 'idle'; m.o = m.base; }
      }
      if (m.phase === 'idle' && near) {
        m.phase = 'wake'; m.at = now; el = 0;
        m.suit = suit();
      }

      if (m.phase === 'wake') {
        m.t = easeOut(Math.min(1, el / WAKE_D));
        m.o = m.base + (m.peak - m.base) * Math.min(1, el / FADE_UP);  /* never a flash */
        if (el >= FADE_UP) { m.phase = 'hold'; m.at = now; }
      } else if (m.phase === 'hold') {
        m.t = 1; m.o = m.peak;
        if (near) m.at = now - Math.min(el, HOLD * .45);
        else if (el >= HOLD) { m.phase = 'back'; m.at = now; }
      } else if (m.phase === 'back') {
        m.t = 1 - easeIO(Math.min(1, el / BACK));
        var floor = m.spare ? 0 : m.base;    /* a spare fades all the way out */
        m.o = m.peak - (m.peak - floor) * Math.min(1, el / FADE_DN);
        if (el >= FADE_DN) {
          m.phase = 'idle'; m.t = 0; m.o = floor;
          if (m.spare) m.live = false;
        }
      }

      if (m.phase !== 'idle' || m.t > 0) m.p.setAttribute('d', mix(m.suit, m.t));
      m.hs += Math.max(-2.4 * dt, Math.min(2.4 * dt, hush - m.hs));
      m.g.setAttribute('opacity', (m.o * m.hs * ent).toFixed(3));
      place(m);
    }
  });
}

var heroField = document.getElementById('field');
if (heroField) makeField(heroField, {
  w: 1600, h: 900, n: 66, nm: 24, base: .20, peak: .84, r: 260,
  text: [].slice.call(document.querySelectorAll('.hero .wrap > *')),
  quiet: { x0: 330, x1: 1270, y0: 215, y1: 700 },
  copy: { els: [document.querySelector('.hero h1'), document.querySelector('.hero .sub')],
          dead: ['Sin ayuda, tarde o temprano se paga.', 'La tabla de excel con datos falsos, la factura inexistente, la falla oculta. No es qué pueda pasar, sino cuándo. Medio día con nosotros y su equipo deja de adivinar.'] }
});
document.querySelectorAll('.closefield').forEach(function (svg) {
  var sec = svg.parentNode;
  makeField(svg, { w: 1600, h: 620, n: 34, nm: 14, base: .16, peak: .8, r: 270,
    text: [].slice.call(sec.querySelectorAll('.wrap > *')),
    quiet: { x0: 450, x1: 1150, y0: 130, y1: 510 },
    copy: { els: [sec.querySelector('h2'), sec.querySelector('.fine')],
            dead: ['Es peligroso sin ayuda.', 'Medio día, con sus archivos, y sus herramientas.'] } });
});

/* ==========================================================================
   GRAPHS: a hundred marks per bar, twice. Who uses AI and who wrote a rule
   for it; who is taught and what it earns. Same style, same hand.
   ========================================================================== */
function makeGraph(cfg) {
  var root = document.getElementById(cfg.id);
  if (!root) return;
  var COLS = 10, CW = 22, CH = 23, SZ = 19, H = 14 * CH;
  function bar(svg, count) {
    svg.setAttribute('viewBox', '0 0 ' + (COLS * CW) + ' ' + H);
    var cells = [];
    for (var n = 0; n < count; n++) {
      var col = n % COLS, row = (n / COLS) | 0;
      var cx = col * CW + CW / 2, cy = H - row * CH - CH / 2;
      var g = document.createElementNS(NS, 'g');
      g.setAttribute('class', 'mk');
      g.setAttribute('transform', 'translate(' + cx + ' ' + cy + ') scale(' + (SZ / 100) + ') translate(-50 -50)');
      var p = document.createElementNS(NS, 'path');
      p.setAttribute('fill', 'currentColor'); p.setAttribute('d', PATHS.square);
      g.appendChild(p); svg.appendChild(g);
      cells.push({ g: g, p: p, row: row, col: col, n: n, cx: cx, cy: cy, strong: false, fo: 1, svg: svg });
    }
    return cells;
  }
  var A = bar(cfg.a.svg, cfg.a.count), B = bar(cfg.b.svg, cfg.b.count);
  cfg.setup(A, B);
  function beatOn(name) {
    root.classList.add(name);
    var el = root.querySelector('.beat-l[data-beat="' + name + '"]');
    if (el) el.classList.add('on');
  }
  if (reduce) { cfg.beats.forEach(function (bt) { beatOn(bt.cls); }); cfg.still(A, B); return; }

  /* the hand over the marks: strong marks swell, the rest only lose transparency */
  var live = false, braf = 0, bev = null;
  var bars = root.querySelector('.bars'), big = root.querySelector('.delta svg');
  function influence() {
    braf = 0;
    if (!live) return;
    [A, B].forEach(function (cells) {
      var r = cells[0].svg.getBoundingClientRect(), k = r.width / (COLS * CW);
      var px = bev ? (bev.clientX - r.left) / k : -1e4, py = bev ? (bev.clientY - r.top) / k : -1e4;
      cells.forEach(function (cc) {
        var dx = cc.cx - px, dy = cc.cy - py, d = Math.hypot(dx, dy), RR = 95;
        if (d > RR) { if (cc.p.style.transform) cc.p.style.transform = ''; if (cc.p.style.fillOpacity) cc.p.style.fillOpacity = ''; return; }
        var f = 1 - d / RR;
        if (!cc.strong) { if (cc.fo < 1) cc.p.style.fillOpacity = (cc.fo + (1 - cc.fo) * f).toFixed(3); return; }
        var sc = 1 + .75 * f, sh = 2.2 * f;
        cc.p.style.transform = 'translate(' + (dx / (d || 1) * sh).toFixed(2) + 'px,' + (dy / (d || 1) * sh).toFixed(2) +
          'px) scale(' + sc.toFixed(3) + ')';
      });
    });
    if (big) {
      if (!bev) big.style.transform = '';
      else {
        var rb = big.getBoundingClientRect(), db = Math.hypot(bev.clientX - (rb.left + rb.width / 2), bev.clientY - (rb.top + rb.height / 2));
        var fb = Math.max(0, 1 - db / 150);
        big.style.transform = fb ? 'scale(' + (1 + .6 * fb).toFixed(3) + ')' : '';
      }
    }
  }
  bars.addEventListener('pointermove', function (e) { bev = e; if (!braf) braf = requestAnimationFrame(influence); }, { passive: true });
  bars.addEventListener('pointerleave', function () { bev = null; if (!braf) braf = requestAnimationFrame(influence); }, { passive: true });

  function beatOff(name) {
    root.classList.remove(name);
    var el = root.querySelector('.beat-l[data-beat="' + name + '"]');
    if (el) el.classList.remove('on');
  }
  function play() {
    var lastAt = 0;
    root.querySelectorAll('.beat-l').forEach(function (el) { el.classList.add('on'); });
    cfg.beats.forEach(function (bt) {
      lastAt = Math.max(lastAt, bt.at);
      setTimeout(function () { beatOn(bt.cls); bt.fn(A, B); }, bt.at);
    });
    setTimeout(function () { live = true; root.classList.add('live'); }, lastAt + 900);
  }
  if (cfg.drive && STAGE) {
    /* staged: the scroll decides when it starts, the clock plays it, once */
    var played = false;
    return { play: function () { if (!played) { played = true; play(); } } };
  }
  new IntersectionObserver(function (es, o) {
    if (!es[0].isIntersecting) return;
    o.disconnect();
    play();
  }, { threshold: .35 }).observe(root);
}

/* it works, until it doesn't: 93 of 100 save time with AI, 9 of 100 have a rule */
var policyG = makeGraph({ id: 'policy', drive: true,
  a: { svg: document.getElementById('polA'), count: 100 }, b: { svg: document.getElementById('polB'), count: 100 },
  setup: function (A, B) {
    A.forEach(function (c) { c.fo = .14; if (c.n < 93) { c.g.classList.add('lit'); c.fo = 1; } });
    B.forEach(function (c) { c.fo = .14; if (c.n < 9) { c.g.classList.add('lit'); c.strong = true; } });
  },
  still: function (A, B) { B.slice(0, 9).forEach(function (c) { c.p.setAttribute('d', mix('smooth-diamond', 1)); }); },
  beats: [
    { at: 150, cls: 'in', fn: function (A, B) { A.concat(B).forEach(function (c) { c.g.style.transitionDelay = (c.row * 9) + 'ms'; }); } },
    { at: 400, cls: 'lit', fn: function (A) { A.forEach(function (c) { if (c.n < 93) c.p.style.transitionDelay = (c.row * 9 + c.col * 3) + 'ms'; }); } },
    { at: 750, cls: 'rules', fn: function (A, B) {
      B.slice(0, 9).forEach(function (c, i) { c.p.style.transitionDelay = (i * 35) + 'ms'; morphPath(c.p, 'smooth-diamond', 420, i * 35); });
    } }
  ] });

/* taught first: the same hundred people, twice. Taught, they do 34% more */
var vizG = makeGraph({ id: 'viz', drive: true,
  a: { svg: document.getElementById('barA'), count: 100 }, b: { svg: document.getElementById('barB'), count: 134 },
  setup: function (A, B) {
    A.forEach(function (c) { c.fo = .42; });
    B.forEach(function (c) { c.strong = true; if (c.n >= 100) c.g.classList.add('extra'); });
  },
  still: function (A, B) { B.forEach(function (c) { c.p.setAttribute('d', mix('smooth-spade', 1)); }); },
  beats: [
    { at: 0, cls: 'in', fn: function (A, B) { A.concat(B.slice(0, 100)).forEach(function (c) { c.g.style.transitionDelay = (c.row * 9) + 'ms'; }); } },
    { at: 300, cls: 'taught', fn: function (A, B) { B.slice(0, 100).forEach(function (c) { morphPath(c.p, 'smooth-spade', 380, c.row * 10 + c.col * 3); }); } },
    { at: 800, cls: 'more', fn: function (A, B) {
      B.slice(100).forEach(function (c, i) { c.p.setAttribute('d', mix('smooth-spade', 1)); c.g.style.transitionDelay = (i * 6) + 'ms'; });
    } }
  ] });

/* ==========================================================================
   SWIPE: "Can AI take this?"  Five cards, two piles, then the desk.
   ========================================================================== */
(function () {
  var deck = document.getElementById('deck');
  if (!deck) return;
  /* two answers per card: what to know if you hand it over, what to know if
     you keep it. Neither is wrong. Both come with a catch. */
  var CARDS = [
    { q: "Responderle a un cliente que pregunta por qué su factura salió más alta este mes.", pip: "classic-spade",
      r: "La IA puede escribir una respuesta convincente en segundos, pero si no tiene los números, se inventa una razón. Déle la factura y léala antes de enviar.",
      l: "El toque humano es importante, pero la IA puede repetir la forma en la que usted se comunica con sus clientes, es cuestión de saber darle esa información." },
    { q: "Resumir el contrato de 40 páginas del proveedor.", pip: "classic-heart",
      r: "La IA hace un buen resumen, pero puede que se salte la cláusula que importa. Pídale primero lo que necesita su atención y lea esas páginas usted antes que la IA.",
      l: "Cuarenta páginas son una tarde entera. Déjela listar las cláusulas y dónde están, y lea solo páginas que sean importantes revisar a mano." },
    { q: "Digitar este montón de facturas en el sistema.", pip: "classic-diamond",
      r: "La IA lee bien las facturas, pero es probable que no vea los duplicados ni las fechas equivocadas por sí sola, hay que mantenerla supervisada.",
      l: "Esta es la que más equipos entregan de primero. La IA lee bien las facturas, aunque sí se debe mantener una revisión, al menos una de cada diez." },
    { q: "Escribir el informe mensual para la gerencia.", pip: "classic-club",
      r: "La IA arma la estructura en un minuto, pero cada número necesita revisión de una persona, pues en los números es donde suena más confiada y más se equivoca.",
      l: "La IA puede hacerle la estructura en un minuto, no hay que perder tiempo en eso ya, pero los números son la parte que hay que cuidar, porque ahí es donde suena más segura y más se equivoca." },
    { q: "Decidir si al cliente nuevo se le dan 60 días de plazo de pago.", pip: "classic-spade",
      r: "La IA puede listar los pros y los contras, pero la decisión, y el riesgo, deben quedar en manos de una persona. Una IA no se hace responsable.",
      l: "Bien hecho en no dejarla decidir. Igual puede armar los pros y los contras en un minuto, puede ayudar solo que la decisión y el riesgo debe tomarla una persona informada." }
  ];
  var hint = document.getElementById('hint'),
      table = document.getElementById('table'),
      btns = document.getElementById('btns'),
      head = document.getElementById('swipehead'),
      pileL = document.getElementById('pileL'), pileR = document.getElementById('pileR'),
      stackL = document.getElementById('stackL'), stackR = document.getElementById('stackR'),
      rows = document.getElementById('rows'),
      cables = document.getElementById('cables'),
      desk = document.getElementById('desk'), reveal = document.getElementById('reveal');
  var idx = 0, els = [], minis = [], drag = null, done = false, touched = false, nudgeTimer = 0, nudgeBack = 0, nudgeSide = 1;
  /* phones get their own table: no piles beside the deck, the two answer
     buttons are the piles. A sent card flies into its button and leaves a
     small card in it. */
  var phone = matchMedia('(max-width:900px)');
  var bL = document.getElementById('bLeft'), bR = document.getElementById('bRight');
  [bL, bR].forEach(function (b) { b.insertAdjacentHTML('beforeend', '<span class="tally" aria-hidden="true"></span>'); });
  function pileOf(dir) { return phone.matches ? (dir > 0 ? bR : bL) : (dir > 0 ? pileR : pileL); }
  var HINT = 'de 5. Arrastre la carta, use los botones o presione ';

  function setHint() {
    hint.innerHTML = 'Carta ' + Math.min(idx + 1, 5) + ' ' + HINT +
      '<span class="kbd"><kbd>&larr;</kbd><kbd>&rarr;</kbd></span>.';
  }

  function makeCards() {
    deck.innerHTML = '';
    els = [];
    CARDS.forEach(function (c, i) {
      var el = document.createElement('article');
      el.className = 'card' + (/heart|diamond/.test(c.pip) ? ' red' : '');
      el.style.zIndex = CARDS.length - i;
      el.dataset.rest = 'translateY(' + (i * 6) + 'px) scale(' + (1 - i * 0.02).toFixed(3) + ')';
      el.style.setProperty('--rest', el.dataset.rest);
      el.innerHTML =
        '<svg class="pip" viewBox="0 0 100 100" aria-hidden="true"><use href="#' + c.pip + '"/></svg>' +
        '<span class="ix ixa">' + (i + 1) + '<svg viewBox="0 0 100 100" aria-hidden="true"><use href="#' + c.pip + '"/></svg></span>' +
        '<div class="top"></div>' +
        '<div class="cband"><p>' + c.q + '</p></div>' +
        '<div class="bot"></div>' +
        '<span class="ix ixb">' + (i + 1) + '<svg viewBox="0 0 100 100" aria-hidden="true"><use href="#' + c.pip + '"/></svg></span>';
      if (i) el.setAttribute('aria-hidden', 'true');
      el.style.transform = reduce ? el.dataset.rest : 'translateY(46px) scale(.94)';
      if (!reduce) el.style.opacity = '0';
      deck.appendChild(el);
      els.push(el);
    });
    deck.insertAdjacentHTML('beforeend',
      '<svg class="hintarrow" viewBox="0 0 28 64" aria-hidden="true"><use href="#chevron"/></svg>' +
      '<svg class="hintarrow l" viewBox="0 0 28 64" aria-hidden="true"><use href="#chevron"/></svg>');
  }

  function deal() {
    els.forEach(function (el, i) {
      setTimeout(function () {
        el.style.transition = 'opacity .5s linear, transform .7s var(--ease)';
        el.style.opacity = '1';
        el.style.transform = el.dataset.rest;
      }, reduce ? 0 : i * 90);
    });
    armNudge();
  }

  /* the visitor does not know what to do: show the gesture after a beat */
  function armNudge() {
    clearTimeout(nudgeTimer);
    if (reduce || touched || done) return;
    nudgeTimer = setTimeout(function () {
      if (touched || done || idx >= CARDS.length) return;
      var el = els[idx];
      if (!el) return;
      el.style.transition = '';
      var right = nudgeSide > 0; nudgeSide = -nudgeSide;   /* one side, then the other */
      el.classList.add(right ? 'nudging' : 'nudging-l');
      deck.classList.add(right ? 'hinting' : 'hinting-l');
      pileOf(right ? 1 : -1).classList.add('nudge');
      nudgeBack = setTimeout(function () {
        el.classList.remove('nudging', 'nudging-l');
        deck.classList.remove('hinting', 'hinting-l');
        [pileR, pileL, bL, bR].forEach(function (p) { p.classList.remove('nudge'); });
        if (el.classList.contains('piled')) return;
        el.style.transition = 'transform .45s var(--ease)';
        el.style.transform = el.dataset.rest;
        armNudge();
      }, 1600);
    }, 2000);
  }
  function stopNudge() {
    touched = true;
    clearTimeout(nudgeTimer); clearTimeout(nudgeBack);
    deck.classList.remove('hinting', 'hinting-l');
    [pileR, pileL, bL, bR].forEach(function (p) { p.classList.remove('nudge'); });
    els.forEach(function (el) { el.classList.remove('nudging', 'nudging-l'); });
  }

  function restack() {
    els.forEach(function (el, i) {
      if (i < idx) return;
      var k = i - idx;
      el.style.zIndex = CARDS.length - k;
      el.style.transition = 'transform .5s var(--ease)';
      el.style.transform = 'translateY(' + (k * 6) + 'px) scale(' + (1 - k * 0.02).toFixed(3) + ')';
      el.style.setProperty('--rest', 'translateY(' + (k * 6) + 'px) scale(' + (1 - k * 0.02).toFixed(3) + ')');
      el.dataset.rest = 'translateY(' + (k * 6) + 'px) scale(' + (1 - k * 0.02).toFixed(3) + ')';
      if (k) el.setAttribute('aria-hidden', 'true'); else el.removeAttribute('aria-hidden');
    });
  }

  /* where the k-th card on a pile rests, relative to the deck */
  function pileSpot(dir, k) {
    if (phone.matches) {
      /* into the button: small, turned, gone */
      var bt = pileOf(dir).getBoundingClientRect(), dk = deck.getBoundingClientRect();
      return 'translate(' + (bt.left + bt.width / 2 - dk.left - dk.width / 2).toFixed(1) + 'px,' +
        (bt.top + bt.height / 2 - dk.top - dk.height / 2).toFixed(1) + 'px) rotate(' + (dir * 24) + 'deg) scale(.14)';
    }
    var pile = (dir > 0 ? pileR : pileL).getBoundingClientRect();
    var here = deck.getBoundingClientRect();
    var sc = .44;
    var dx = (pile.left + pile.width / 2) - (here.left + here.width / 2);
    var dy = (pile.top + 40 + k * 16) - here.top - here.height * (1 - sc) / 2;
    return 'translate(' + dx.toFixed(1) + 'px,' + dy.toFixed(1) + 'px) rotate(' +
      (dir * (3 + k * 1.6)).toFixed(1) + 'deg) scale(' + sc + ')';
  }
  var onPile = { l: [], r: [] };
  function send(dir) {
    if (done || idx >= CARDS.length) return;
    stopNudge();
    var el = els[idx], c = CARDS[idx], side = dir > 0 ? 'r' : 'l';
    var k = onPile[side].length;
    el.dataset.fn = String(idx + 1); el.dataset.dir = side; el.dataset.k = k;
    onPile[side].push(el);
    pileOf(dir).classList.add('hot');
    el.style.zIndex = 40 + idx;
    el.style.pointerEvents = 'none';
    if (phone.matches) {
      var b = pileOf(dir);
      el.style.transition = reduce ? 'none' : 'transform .5s cubic-bezier(.5,0,.75,0), opacity .22s linear .3s';
      el.style.opacity = '0';
      setTimeout(function () {
        b.querySelector('.tally').insertAdjacentHTML('beforeend', '<i></i>');
        b.classList.remove('landed'); void b.offsetWidth; b.classList.add('landed');
      }, reduce ? 0 : 460);
    } else el.style.transition = reduce ? 'none' : 'transform .68s cubic-bezier(.16,1,.3,1)';
    el.style.transform = pileSpot(dir, k);
    el.classList.add('piled');
    idx++;
    restack();
    if (idx >= CARDS.length) { hint.textContent = ''; setTimeout(finish, reduce ? 0 : 1500); }
    else setHint();
  }

  /* --- the desk: one row per card, the card on the left, its answer on the right --- */
  var stage = document.getElementById('stage'), heads = document.getElementById('heads');
  var SLOT = { w: 0, h: 0 };
  /* The hand is played. The table fades, the mark holds the screen for a
     moment (with a small turning ring, so the wait reads as work), and the
     desk is laid out behind it, unseen. Then the mark lets go and the rows
     are dealt one after another. */
  var swipeSec = document.getElementById('swipe');
  function finish() {
    if (done) return;
    done = true;
    stopNudge();
    var narrow = phone.matches;
    minis = [];

    function lay() {
      var wrapW = desk.getBoundingClientRect().width;
      SLOT.w = Math.round(narrow ? Math.min(wrapW, 420) : Math.min(420, wrapW * .42)); SLOT.h = Math.round(SLOT.w * .6);
      btns.hidden = true; hint.hidden = true;
      heads.classList.add('flip'); stage.classList.add('flip');
      rows.innerHTML = '';
      els.forEach(function (el) {
        var cd = CARDS[els.indexOf(el)], right = el.dataset.dir === 'r';
        /* the card and its note swap sides row by row, whatever was answered */
        var flip = !narrow && +el.dataset.fn % 2 === 0;
        var row = document.createElement('div');
        row.className = 'row' + (flip ? ' flip' : '') + (reduce ? '' : ' dealt');
        row.dataset.fn = el.dataset.fn;
        var slot = document.createElement('div');
        slot.className = 'slot'; slot.dataset.fn = el.dataset.fn;
        slot.style.width = SLOT.w + 'px'; slot.style.height = SLOT.h + 'px';
        var note = document.createElement('div');
        note.className = 'note'; note.dataset.fn = el.dataset.fn; note.tabIndex = 0;
        note.innerHTML = '<p class="said">Usted dijo: <b>' + (right ? 'La IA puede' : 'Mejor una persona') + '</b></p>' +
          '<p class="q">' + cd.q + '</p><p class="a">' + (right ? cd.r : cd.l) + '</p>';
        if (flip) { row.appendChild(note); row.appendChild(slot); } else { row.appendChild(slot); row.appendChild(note); }
        rows.appendChild(row);
        slot.appendChild(el);
        el.classList.remove('piled'); el.classList.add('desk');
        el.style.zIndex = ''; el.style.pointerEvents = ''; el.style.transition = 'none'; el.style.transform = 'none';
        el.style.opacity = '';
        el.style.width = SLOT.w + 'px'; el.style.height = SLOT.h + 'px';
        minis.push(slot);
      });
      reveal.hidden = false;
    }
    function dealRows() {
      var list = [].slice.call(rows.querySelectorAll('.row'));
      list.forEach(function (r, i) { setTimeout(function () { r.classList.remove('dealt'); }, 120 + i * 190); });
      if (!narrow) setTimeout(drawCables, 120 + list.length * 190 + 600);
    }

    if (reduce) { lay(); rows.querySelectorAll('.row').forEach(function (r) { r.classList.remove('dealt'); }); if (!narrow) drawCables(); return; }
    swipeSec.classList.add('clearing');                  /* the table fades first */
    var veil = document.createElement('div');
    veil.className = 'veil';
    veil.innerHTML = '<svg class="mark" viewBox="0 0 1703.11 435.6" aria-hidden="true"><use href="#logo-full" width="1703.11" height="435.6"/></svg>' +
      '<svg class="ring" viewBox="0 0 40 40" aria-hidden="true"><circle cx="20" cy="20" r="16"/></svg>';
    document.body.appendChild(veil);
    setTimeout(function () { veil.classList.add('on'); }, 380);
    /* opaque from ~1s: only now is the page rebuilt, so the work is never seen */
    setTimeout(function () {
      lay();
      swipeSec.classList.remove('clearing');
      var hdr = parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--hdr')) || 72;
      window.scrollTo(0, heads.getBoundingClientRect().top + scrollY - hdr - 24);
    }, 1150);
    setTimeout(function () { veil.classList.add('out'); dealRows(); }, 4000);
    setTimeout(function () { if (veil.parentNode) veil.parentNode.removeChild(veil); }, 5000);
  }

  /* Each card hangs a cable to its note. Real slack, real gravity: the
     cables settle, dangle, and can be brushed or dragged by the pointer.
     A verlet rope per card, drawn as one smooth path, with a gold current
     running toward the note. */
  var ropes = [], ropeSvg = null, grabbed = null, ropeRun = false, ropeLast = 0;
  var N = 30, GRAV = 1500, DAMP = .985, ITER = 4;

  function ropePath(pts) {
    var d = 'M' + pts[0].x.toFixed(1) + ' ' + pts[0].y.toFixed(1);
    for (var i = 0; i < pts.length - 1; i++) {
      var p0 = pts[i ? i - 1 : 0], p1 = pts[i], p2 = pts[i + 1],
          p3 = pts[i + 2 < pts.length ? i + 2 : i + 1];
      d += 'C' + (p1.x + (p2.x - p0.x) / 6).toFixed(1) + ' ' + (p1.y + (p2.y - p0.y) / 6).toFixed(1) +
           ' ' + (p2.x - (p3.x - p1.x) / 6).toFixed(1) + ' ' + (p2.y - (p3.y - p1.y) / 6).toFixed(1) +
           ' ' + p2.x.toFixed(1) + ' ' + p2.y.toFixed(1);
    }
    return d;
  }

  function drawCables() {
    cables.innerHTML = ''; ropes = []; grabbed = null;
    var host = desk.getBoundingClientRect();
    ropeSvg = document.createElementNS(NS, 'svg');
    ropeSvg.setAttribute('class', 'ropes');
    ropeSvg.setAttribute('width', host.width); ropeSvg.setAttribute('height', host.height);
    ropeSvg.setAttribute('viewBox', '0 0 ' + host.width + ' ' + host.height);
    cables.appendChild(ropeSvg);

    var wires = minis.map(function (m) {
      var note = rows.querySelector('.note[data-fn="' + m.dataset.fn + '"]');
      if (!note) return null;
      var band = m.querySelector('.cband') || m, said = note.querySelector('.q') || note;
      var a1 = band.getBoundingClientRect(), b1 = said.getBoundingClientRect();
      var rowEl = m.closest('.row'), flip = !!(rowEl && rowEl.classList.contains('flip'));
      return flip ? { fn: m.dataset.fn,
        x1: a1.left - host.left + 2, y1: a1.top + a1.height * .5 - host.top,
        x2: b1.right - host.left + 10, y2: b1.top + b1.height * .5 - host.top } : { fn: m.dataset.fn,
        x1: a1.right - host.left - 2, y1: a1.top + a1.height * .5 - host.top,
        x2: b1.left - host.left - 10, y2: b1.top + b1.height * .5 - host.top };
    }).filter(Boolean);

    wires.forEach(function (r, i) {
      var g = document.createElementNS(NS, 'g');
      g.setAttribute('class', 'cable'); g.dataset.fn = r.fn;
      var base = document.createElementNS(NS, 'path'), flow = document.createElementNS(NS, 'path');
      base.setAttribute('class', 'rope'); base.setAttribute('pathLength', '1');
      flow.setAttribute('class', 'flow');
      g.appendChild(base); g.appendChild(flow); ropeSvg.appendChild(g);

      /* slack grows with the index so no two cables hang on the same curve */
      var span = Math.hypot(r.x2 - r.x1, r.y2 - r.y1);
      var len = span * 1.07 + 10, seg = len / (N - 1), pts = [];
      for (var k = 0; k < N; k++) {
        var t = k / (N - 1);
        var x = r.x1 + (r.x2 - r.x1) * t, y = r.y1 + (r.y2 - r.y1) * t + Math.sin(t * Math.PI) * 8;
        pts.push({ x: x, y: y, px: x, py: y });
      }
      var rope = { g: g, base: base, flow: flow, pts: pts, seg: seg, a: r, fn: r.fn };
      ropes.push(rope);
      if (reduce) { for (var w = 0; w < 240; w++) stepRope(rope, 1 / 60, true); render(rope); g.classList.add('in'); }
      else setTimeout(function () { g.classList.add('in'); }, 120 + i * 140);
    });
    if (!reduce) startRopes();
  }

  function stepRope(rope, dt, still) {
    var pts = rope.pts, n = pts.length;
    for (var i = 1; i < n - 1; i++) {
      var p = pts[i];
      if (grabbed && grabbed.rope === rope && grabbed.i === i) continue;
      var vx = (p.x - p.px) * DAMP, vy = (p.y - p.py) * DAMP;
      p.px = p.x; p.py = p.y;
      p.x += vx; p.y += vy + GRAV * dt * dt;
    }
    for (var it = 0; it < ITER; it++) {
      for (var j = 0; j < n - 1; j++) {
        var q = pts[j], r = pts[j + 1];
        var dx = r.x - q.x, dy = r.y - q.y, d = Math.hypot(dx, dy) || 1e-4;
        var diff = (d - rope.seg) / d * .5;
        var qFixed = j === 0 || (grabbed && grabbed.rope === rope && grabbed.i === j);
        var rFixed = j + 1 === n - 1 || (grabbed && grabbed.rope === rope && grabbed.i === j + 1);
        if (!qFixed) { q.x += dx * diff * (rFixed ? 2 : 1); q.y += dy * diff * (rFixed ? 2 : 1); }
        if (!rFixed) { r.x -= dx * diff * (qFixed ? 2 : 1); r.y -= dy * diff * (qFixed ? 2 : 1); }
      }
    }
    if (still) for (var z = 1; z < n - 1; z++) { pts[z].px = pts[z].x; pts[z].py = pts[z].y; }
  }
  function render(rope) {
    var d = ropePath(rope.pts);
    rope.base.setAttribute('d', d); rope.flow.setAttribute('d', d);
  }

  var ptrR = { x: -1e4, y: -1e4, on: false, down: false };
  function ropeLocal(e) {
    var b = cables.getBoundingClientRect();
    return { x: e.clientX - b.left, y: e.clientY - b.top };
  }
  function nearest(x, y, within) {
    var best = null, bd = within;
    ropes.forEach(function (rope) {
      for (var i = 1; i < rope.pts.length - 1; i++) {
        var d = Math.hypot(rope.pts[i].x - x, rope.pts[i].y - y);
        if (d < bd) { bd = d; best = { rope: rope, i: i, d: d }; }
      }
    });
    return best;
  }
  /* one owner for the highlight: whatever the pointer is over (a card, a
     note) or close to (a cable). A cable once lit stays lit until the pointer
     is well clear of it, and letting go waits a beat: no flicker. */
  var hotFn = null, coolT = 0;
  function setHot(fn) {
    if (fn) { clearTimeout(coolT); coolT = 0; }
    if (fn === hotFn) return;
    if (!fn) { if (!coolT) coolT = setTimeout(function () { coolT = 0; if (hotFn) hot(hotFn, false); hotFn = null; }, 220); return; }
    if (hotFn) hot(hotFn, false);
    hot(fn, true); hotFn = fn;
  }
  desk.addEventListener('pointermove', function (e) {
    var l = ropeLocal(e); ptrR.x = l.x; ptrR.y = l.y; ptrR.on = true;
    if (grabbed) { grabbed.rope.pts[grabbed.i].x = l.x; grabbed.rope.pts[grabbed.i].y = l.y; return; }
    var el = e.target.closest ? e.target.closest('[data-fn]') : null;
    var nb = ropes.length ? nearest(l.x, l.y, 34) : null;
    if (!nb && hotFn && ropes.length) { var keep = nearest(l.x, l.y, 80); if (keep && keep.rope.fn === hotFn) nb = keep; }
    setHot(el ? el.dataset.fn : nb ? nb.rope.fn : null);
    desk.style.cursor = nb && !el ? 'grab' : '';
  }, { passive: true });
  desk.addEventListener('pointerleave', function () {
    ptrR.on = false; ptrR.x = ptrR.y = -1e4;
    setHot(null);
    desk.style.cursor = '';
  }, { passive: true });
  desk.addEventListener('pointerdown', function (e) {
    if (!ropes.length || e.button) return;
    var l = ropeLocal(e), nb = nearest(l.x, l.y, 30);
    if (!nb) return;
    grabbed = nb; desk.style.cursor = 'grabbing';
    try { desk.setPointerCapture(e.pointerId); } catch (_) {}
    e.preventDefault();
  });
  function drop() { grabbed = null; desk.style.cursor = ''; }
  desk.addEventListener('pointerup', drop, { passive: true });
  desk.addEventListener('pointercancel', drop, { passive: true });

  function startRopes() {
    if (ropeRun) return;
    ropeRun = true; ropeLast = 0;
    requestAnimationFrame(function tick(now) {
      if (!ropes.length) { ropeRun = false; return; }
      requestAnimationFrame(tick);
      if (document.hidden) { ropeLast = now; return; }
      var dt = ropeLast ? Math.min(.033, (now - ropeLast) / 1000) : 1 / 60; ropeLast = now;
      ropes.forEach(function (rope) {
        /* a pointer passing close brushes the cable aside */
        if (ptrR.on && !grabbed) {
          for (var i = 1; i < rope.pts.length - 1; i++) {
            var p = rope.pts[i], dx = p.x - ptrR.x, dy = p.y - ptrR.y, d = Math.hypot(dx, dy);
            if (d < 40 && d > 0) { var f = (1 - d / 40) * 1.1; p.x += dx / d * f; p.y += dy / d * f; }
          }
        }
        stepRope(rope, dt, false);
        render(rope);
      });
    });
  }

  function hot(fn, on) {
    desk.querySelectorAll('[data-fn]').forEach(function (el) {
      if (el.dataset.fn === fn) el.classList.toggle('hot', on);
    });
  }

  function link() {
    function fnOf(e) { var el = e.target.closest ? e.target.closest('[data-fn]') : null; return el && el.dataset.fn; }
    desk.addEventListener('focusin', function (e) { setHot(fnOf(e)); });
    desk.addEventListener('focusout', function () { setHot(null); });
  }

  var rz = 0;
  addEventListener('resize', function () {
    if (!done) return;
    clearTimeout(rz);
    rz = setTimeout(function () { if (phone.matches) { cables.innerHTML = ''; ropes = []; } else drawCables(); }, 180);
  }, { passive: true });

  function reset() {
    var first = els.map(function (el) { return el.getBoundingClientRect(); });
    ropes = []; grabbed = null; cables.innerHTML = '';
    reveal.hidden = true;
    heads.classList.remove('flip'); stage.classList.remove('flip');
    btns.hidden = false; hint.hidden = false;
    [pileL, pileR, bL, bR].forEach(function (p) { p.classList.remove('hot', 'landed'); });
    [bL, bR].forEach(function (b) { b.querySelector('.tally').innerHTML = ''; });
    els.forEach(function (el, i) {
      deck.appendChild(el);
      el.classList.remove('desk', 'piled');
      el.style.width = el.style.height = '';
      el.style.zIndex = CARDS.length - i; el.style.pointerEvents = '';
      delete el.dataset.fn; delete el.dataset.dir; delete el.dataset.k;
      var rest = 'translateY(' + (i * 6) + 'px) scale(' + (1 - i * 0.02).toFixed(3) + ')';
      el.dataset.rest = rest; el.style.setProperty('--rest', rest);
      el.style.transition = 'none'; el.style.transform = reduce ? rest : 'none'; el.style.opacity = '';
      if (i) el.setAttribute('aria-hidden', 'true'); else el.removeAttribute('aria-hidden');
    });
    minis = [];
    onPile = { l: [], r: [] };
    if (!reduce) {
      var dk = deck.getBoundingClientRect();
      els.forEach(function (el, i) {
        var l = el.getBoundingClientRect(), f = first[i];
        el.style.width = f.width + 'px'; el.style.height = f.height + 'px';
        el.style.transform = 'translate(' + (f.left - l.left) + 'px,' + (f.top - l.top) + 'px)';
      });
      requestAnimationFrame(function () { requestAnimationFrame(function () {
        els.forEach(function (el, i) {
          var d = ((els.length - i) * 60) + 'ms', e = ' .8s cubic-bezier(.16,1,.3,1) ';
          el.style.transition = 'transform' + e + d + ', width' + e + d + ', height' + e + d;
          el.style.transform = el.dataset.rest;
          el.style.width = dk.width + 'px'; el.style.height = dk.height + 'px';
        });
        setTimeout(function () { els.forEach(function (el) { el.style.width = el.style.height = ''; }); }, 1400);
      }); });
    }
    rows.innerHTML = '';
    document.querySelectorAll('.veil').forEach(function (v) { v.parentNode.removeChild(v); });
    idx = 0; done = false; touched = false;
    setHint();
    armNudge();
    var sec = document.getElementById('swipe');
    if (sec) sec.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' });
  }

  makeCards();
  setHint();
  link();
  new IntersectionObserver(function (es, o) {
    if (!es[0].isIntersecting) return;
    o.disconnect();
    deal();
  }, { threshold: .25 }).observe(deck);

  document.getElementById('bLeft').onclick = function () { send(-1); };
  document.getElementById('bRight').onclick = function () { send(1); };
  document.getElementById('bSkip').onclick = function () {
    (function step() { if (idx < CARDS.length && !done) { send(idx % 2 ? -1 : 1); setTimeout(step, 260); } })();
  };
  document.getElementById('bAgain').onclick = function () { reset(); };
  deck.addEventListener('keydown', function (e) {
    if (e.key === 'ArrowLeft') { e.preventDefault(); send(-1); }
    if (e.key === 'ArrowRight') { e.preventDefault(); send(1); }
  });
  deck.addEventListener('pointerdown', function (e) {
    if (done || idx >= CARDS.length) return;
    stopNudge();
    var el = els[idx];
    drag = { id: e.pointerId, x: e.clientX, el: el, dx: 0 };
    el.style.transition = 'none';
    deck.setPointerCapture(e.pointerId);
  });
  deck.addEventListener('pointermove', function (e) {
    if (!drag || e.pointerId !== drag.id) return;
    var dx = e.clientX - drag.x;
    drag.dx = dx;
    drag.el.style.transform = 'translate(' + dx + 'px,0) rotate(' + (dx * 0.045) + 'deg)';
    pileOf(dx > 0 ? 1 : -1).classList.toggle('hot', Math.abs(dx) > 30);
    pileOf(dx > 0 ? -1 : 1).classList.remove('hot');
  });
  function endDrag(e) {
    if (!drag || (e && e.pointerId !== drag.id)) return;
    var dx = drag.dx || 0, el = drag.el;
    drag = null;
    if (Math.abs(dx) > 90) { el.style.transition = 'none'; send(dx > 0 ? 1 : -1); }
    else {
      el.style.transition = 'transform .45s var(--ease)';
      el.style.transform = el.dataset.rest;
      armNudge();
    }
  }
  deck.addEventListener('pointerup', endDrag);
  deck.addEventListener('pointercancel', endDrag);
})();

/* ==========================================================================
   WHY US: the square becomes the band's suit once. Hover never resets it.
   ========================================================================== */
document.querySelectorAll('.whyband').forEach(function (band) {
  var path = band.querySelector('.suit path');
  var key = band.dataset.suit;
  path.setAttribute('d', PATHS.square);
  if (reduce) { path.setAttribute('d', mix(key, 1)); band.classList.add('on', 'open'); return; }
  new IntersectionObserver(function (es, o) {
    if (!es[0].isIntersecting) return;
    o.disconnect();
    band.classList.add('on');
    morphPath(path, key, 900, 120);
  }, { threshold: .5 }).observe(band);
});

/* ==========================================================================
   WORKSHOP: seven moments, one vertical chevron spine, one visual each.
   ========================================================================== */
(function () {
  var moments = document.querySelectorAll('.moment');
  if (!moments.length) return;

  var mo = new IntersectionObserver(function (es) {
    es.forEach(function (e) { e.target.classList.toggle('on', e.isIntersecting); });
  }, { rootMargin: '-34% 0px -34% 0px' });
  moments.forEach(function (m) { mo.observe(m); });

  /* one continuous line down the whole route; a single chevron rides it
     with the reader, and the last stretch (the optional week after) is dotted */
  var list = document.getElementById('moments');
  var line = document.getElementById('spineline'), dots = document.getElementById('spinedots'),
      mark = document.getElementById('spinemark');
  var opt = list.querySelector('.moment.opt');
  function layout() {
    var top = list.getBoundingClientRect().top + scrollY;
    var oTop = opt ? opt.getBoundingClientRect().top + scrollY - top + opt.offsetHeight * .18 : list.offsetHeight;
    line.style.height = oTop + 'px';
    dots.style.top = oTop + 'px';
  }
  layout();
  addEventListener('resize', layout, { passive: true });
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(layout);
  if (!reduce) {
    var raf = 0;
    var run = function () {
      raf = 0;
      var r = list.getBoundingClientRect(), vh = innerHeight;
      var p = (vh * .5 - r.top) / r.height;
      p = p < 0 ? 0 : p > 1 ? 1 : p;
      mark.style.transform = 'translateY(' + (p * (r.height - 40)).toFixed(1) + 'px)';
      mark.classList.toggle('gold', opt && p * r.height > parseFloat(line.style.height));
    };
    addEventListener('scroll', function () { if (!raf) raf = requestAnimationFrame(run); }, { passive: true });
    addEventListener('resize', function () { if (!raf) raf = requestAnimationFrame(run); }, { passive: true });
    run();
  } else mark.hidden = true;

  /* one visual per moment, built from the same square-to-suit path */
  function vis(m) {
    var kind = m.dataset.vis, svg = m.querySelector('.m-vis svg');
    if (!svg) return;
    if (kind === 'smoke') {
      /* a thick, slow cloud of the brand squares, softened, rising. The hand
         parts it; behind it a square that turns into a spade the clearer the
         middle gets. Left alone, it closes again. With no hand for a while, a
         slow ghost hand passes through, so phones see it too. */
      var defs = document.createElementNS(NS, 'defs');
      defs.innerHTML = '<filter id="smokeblur" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="2.6"/></filter>';
      svg.appendChild(defs);
      var symG = document.createElementNS(NS, 'g'), symP = document.createElementNS(NS, 'path');
      symP.setAttribute('fill', '#C9A227'); symP.setAttribute('d', PATHS.square);
      symG.setAttribute('transform', 'translate(160 110) scale(1.15) translate(-50 -50)');
      symG.setAttribute('opacity', '0'); symG.appendChild(symP); svg.appendChild(symG);
      var cloud = document.createElementNS(NS, 'g');
      cloud.setAttribute('filter', 'url(#smokeblur)'); svg.appendChild(cloud);
      var puffs = [];
      for (var i = 0; i < 76; i++) {
        var g = document.createElementNS(NS, 'g'), p = document.createElementNS(NS, 'path');
        p.setAttribute('fill', 'currentColor'); p.setAttribute('d', PATHS.square);
        g.appendChild(p); cloud.appendChild(g);
        var a = Math.random() * Math.PI * 2, rr = Math.pow(Math.random(), .7);
        puffs.push({ g: g, hx: 160 + Math.cos(a) * rr * 120, hy: 30 + Math.random() * 170, s: rnd(26, 62),
          o: rnd(.16, .34), rot: rnd(0, 90), vr: rnd(-9, 9), rise: rnd(5, 12), ph: rnd(0, 6.3), ox: 0, oy: 0 });
      }
      var hand = { x: -1e3, y: -1e3, at: -1e4 }, clear = 0, smokeOn = false, last = 0;
      function toLocal(e) {
        var b = svg.getBoundingClientRect(), k = 320 / b.width;
        hand.x = (e.clientX - b.left) * k; hand.y = (e.clientY - b.top) * k; hand.at = performance.now();
      }
      svg.addEventListener('pointermove', toLocal, { passive: true });
      svg.addEventListener('pointerdown', toLocal, { passive: true });
      svg.addEventListener('pointerleave', function () { hand.x = hand.y = -1e3; }, { passive: true });
      function draw(now) {
        var dt = last ? Math.min(.05, (now - last) / 1000) : 0; last = now;
        var hx = hand.x, hy = hand.y, push = 520;
        if (now - hand.at > 3200) {
          push = 240;                 /* the ghost hand */
          var u = now / 1000;
          hx = 160 + Math.sin(u * .55) * 70; hy = 110 + Math.sin(u * 1.1) * 38;
        }
        var near = 0;
        for (var i = 0; i < puffs.length; i++) {
          var q = puffs[i];
          q.hy -= q.rise * dt;
          if (q.hy < 18) { q.hy = 205; q.hx = 160 + rnd(-120, 120); }
          q.rot += q.vr * dt;
          var x = q.hx + Math.sin(now / 1900 + q.ph) * 9 + q.ox, y = q.hy + q.oy;
          var dx = x - hx, dy = y - hy, d = Math.hypot(dx, dy) || 1;
          if (d < 78) { var f = (1 - d / 78) * push * dt; q.ox += dx / d * f; q.oy += dy / d * f; }
          q.ox -= q.ox * Math.min(1, .9 * dt); q.oy -= q.oy * Math.min(1, .9 * dt);   /* closes back, slowly */
          x = q.hx + Math.sin(now / 1900 + q.ph) * 9 + q.ox; y = q.hy + q.oy;
          if (Math.hypot(x - 160, y - 110) < 62) near += q.s / 40;
          var edge = Math.min(1, (q.hy - 18) / 40, (205 - q.hy) / 30);
          q.g.setAttribute('opacity', (q.o * Math.max(0, edge)).toFixed(3));
          q.g.setAttribute('transform', 'translate(' + x.toFixed(1) + ' ' + y.toFixed(1) + ') rotate(' + q.rot.toFixed(1) +
            ') scale(' + (q.s / 100).toFixed(3) + ') translate(-50 -50)');
        }
        /* the fewer (and smaller) puffs over the middle, the clearer it is */
        var want = Math.max(0, Math.min(1, 1 - (near - 2.5) / 8));
        clear += (want - clear) * Math.min(1, 2.4 * dt);
        symG.setAttribute('opacity', (.12 + clear * .88).toFixed(3));
        symP.setAttribute('d', mix('smooth-spade', easeOut(clear)));
        if (clear > .85) symG.classList.add('glow'); else symG.classList.remove('glow');
      }
      if (reduce) { draw(0); symG.setAttribute('opacity', '1'); symP.setAttribute('d', mix('smooth-spade', 1)); }
      else {
        new IntersectionObserver(function (es) {
          smokeOn = es[0].isIntersecting;
          if (smokeOn) { last = 0; requestAnimationFrame(function step(now) { if (!smokeOn) return; draw(now); requestAnimationFrame(step); }); }
        }).observe(svg);
      }
    } else if (kind === 'desk') {
      var keys = ['smooth-spade', 'smooth-heart', 'smooth-diamond'];
      var ps = keys.map(function (k, i) {
        var g = document.createElementNS(NS, 'g');
        var p = document.createElementNS(NS, 'path');
        p.setAttribute('fill', 'currentColor');
        p.setAttribute('d', PATHS.square);
        g.appendChild(p);
        g.setAttribute('transform', 'translate(' + (68 + i * 92) + ' 110) scale(.62) translate(-50 -50)');
        g.setAttribute('opacity', '.85');
        svg.appendChild(g);
        return p;
      });
      once(m, function (on) { if (on) ps.forEach(function (p, i) { morphPath(p, keys[i], 820, i * 180); }); });
    } else if (kind === 'magic') {
      var g2 = document.createElementNS(NS, 'g');
      var p2 = document.createElementNS(NS, 'path');
      p2.setAttribute('fill', 'currentColor');
      p2.setAttribute('d', PATHS.square);
      g2.appendChild(p2);
      g2.setAttribute('transform', 'translate(160 110) scale(1.7) translate(-50 -50)');
      g2.setAttribute('opacity', '.92');
      svg.appendChild(g2);
      once(m, function (on) {
        if (!on) return;
        morphPath(p2, 'smooth-spade', 950, 150);
        setTimeout(function () { g2.classList.add('glow'); }, 1000);
      });
    } else if (kind === 'break') {
      var hps = svg.querySelectorAll('.host path');
      hps.forEach(function (hp) {
        hp.setAttribute('d', PATHS.square);
        hp.parentNode.setAttribute('transform', 'translate(160 108) scale(1.5) translate(-50 -50)');
      });
      once(m, function (on) { if (on) hps.forEach(function (hp) { morphPath(hp, 'smooth-diamond', 820, 100); }); });
    }
  }
  function once(m, fn) {
    if (reduce) { fn(true); return; }
    var fired = false;
    new IntersectionObserver(function (es) {
      if (es[0].isIntersecting && !fired) { fired = true; fn(true); }
    }, { threshold: .25 }).observe(m);
    fn(false);
  }
  moments.forEach(vis);
})();

/* ==========================================================================
   THE STAGE: the hero shrinks to the left two fifths and stays; the numbers
   scroll on the right. The 93/9 cards sink into the graph as you scroll.
   The felt table folds down from behind; the half-day card fills the screen
   and lets go. Everything is scrubbed by the scroll: no timers, no snapping.
   ========================================================================== */
(function () {
  if (!STAGE) return;
  var stage = document.getElementById('stage2'), hero = document.getElementById('hero');
  var morph = document.getElementById('morph'), swipe = document.getElementById('swipe');
  var vscr = document.getElementById('vizscr');
  var counts = [].slice.call(document.querySelectorAll('.split [data-count]'));
  var hst = [].slice.call(document.querySelectorAll('.hstage'));
  var HDR = parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--hdr')) || 72;
  function clamp(v) { return Math.max(0, Math.min(1, v)); }
  function smooth(v) { return v * v * (3 - 2 * v); }
  var raf = 0;
  function run() {
    raf = 0;
    var ph = innerHeight - HDR;
    if (stage && hero) {
      var q = smooth(clamp(scrollY / (ph * .55)));
      stage.style.setProperty('--q', q.toFixed(4));
      hero.classList.toggle('condensed', q > .5);
      stage.classList.toggle('rest', q < .01);   /* the right column waits out of sight */
      counts.forEach(function (el) { el.textContent = Math.round(+el.dataset.count * q) + '%'; });
      /* each screen holds still while the scroll plays it: a pillow of scroll,
         the animation, and a longer pillow before it lets go */
      if (morph) {
        /* the two cards hold for a breath (a gold rule fills under them),
           then the graph takes over and plays on its own */
        var ms = HDR - morph.getBoundingClientRect().top, mEnd = morph.offsetHeight - ph;
        var g = ms >= ph * 1.4;
        morph.style.setProperty('--p', (g ? clamp((ms - ph * 1.4) / (mEnd - ph * 1.4)) : clamp((ms - ph * .55) / (ph * .85))).toFixed(4));
        morph.classList.toggle('graph', g);
        if (g && policyG) policyG.play();
      }
      if (vscr) {
        var vt = vscr.getBoundingClientRect().top;
        vscr.style.setProperty('--p', clamp((HDR - vt) / (vscr.offsetHeight - ph)).toFixed(4));
        if (vizG && vt <= HDR + ph * .25) vizG.play();
      }
      if (swipe) {
        var sr = swipe.getBoundingClientRect();
        var f = smooth(clamp(1 - (sr.top - HDR) / ph));
        stage.style.setProperty('--f', f.toFixed(4));
        swipe.style.setProperty('--f', f.toFixed(4));
        swipe.classList.toggle('flat', f >= .999 || f <= 0);
      }
    }
    hst.forEach(function (h) {
      if (h.closest('.route').hidden) return;
      var hr = h.getBoundingClientRect();
      var p = clamp((HDR - hr.top) / (h.offsetHeight - ph || 1));
      var e = p / .45;
      e = smooth(clamp(e));
      h.style.setProperty('--e', e.toFixed(4));
      h.classList.toggle('full', e > .97);
    });
  }
  function ask() { if (!raf) raf = requestAnimationFrame(run); }
  addEventListener('scroll', ask, { passive: true });
  addEventListener('resize', ask, { passive: true });
  run();
})();

})();
