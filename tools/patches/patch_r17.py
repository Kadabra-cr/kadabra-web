"""Round 17 (phones first): the calm felt becomes composited HTML layers that
keep well clear of the copy; the smoke clears by itself on touch screens, with
no blur; the workshop chevron rides with position:sticky (no scroll script);
a shorter swipe deals a card."""
import os, re
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..')
p = os.path.join(ROOT, 'src', 'app.src.js')
s = open(p, encoding='utf-8').read()


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:100])
    s = s.replace(a, b)


# ---- the calm felt, rebuilt ----
a = s.index("/* Phones and touch screens get a calm felt instead of the game:")
b = s.index("function makeField(svg, opt) {")
s = s[:a] + r"""/* Phones and touch screens get a calm felt instead of the game: the suits lie
   scattered on the open felt, well clear of every block of copy, and only
   drift. Each suit is its own small layer moved by CSS, so the browser can
   float them without repainting the section; now and then one folds back
   into a square and comes up a new suit. */
var CALM = matchMedia('(hover: none), (max-width: 760px)').matches;
function calmField(svg, opt) {
  var host = svg.parentNode, marks = [], lastW = 0;
  var felt = document.createElement('div');
  felt.className = 'felt'; felt.setAttribute('aria-hidden', 'true');
  svg.style.display = 'none';
  host.insertBefore(felt, svg);
  function lay() {
    var b = host.getBoundingClientRect(), W = Math.round(b.width), H = Math.round(b.height);
    if (!W || !H || W === lastW) return;
    lastW = W;
    /* every block of copy, whole (not line by line), measured at rest */
    var blocks = [];
    (opt.text || []).concat([].slice.call(host.querySelectorAll('.cue'))).forEach(function (el) {
      var tf = el.style.transform; el.style.transform = 'none';
      var r = el.getBoundingClientRect();
      el.style.transform = tf;
      if (r.width) blocks.push({ x0: r.left - b.left, x1: r.right - b.left, y0: r.top - b.top, y1: r.bottom - b.top });
    });
    var want = Math.max(8, Math.min(18, Math.round(W * H / 14000))), got = [];
    for (var k = 0; k < 1200 && got.length < want; k++) {
      var sz = rnd(16, 38), x = rnd(sz * .7, W - sz * .7), y = rnd(sz * .7, H - sz * .7);
      var m = sz / 2 + 34, ok = true;        /* half the suit, its drift, and a wide berth */
      blocks.forEach(function (z) { if (x > z.x0 - m && x < z.x1 + m && y > z.y0 - m && y < z.y1 + m) ok = false; });
      got.forEach(function (o) { if (Math.hypot(o.x - x, o.y - y) < (o.s + sz) * .8 + 22) ok = false; });
      if (ok) got.push({ x: x, y: y, s: sz });
    }
    felt.innerHTML = ''; marks = [];
    var reach = Math.hypot(W / 2, H / 2);
    got.forEach(function (q, i) {
      var el = document.createElement('i'), key = suit(), depth = (q.s - 16) / 22;
      el.className = 'm' + (i % 6 === 4 ? ' red' : '');
      el.innerHTML = '<svg viewBox="0 0 100 100" style="transform:rotate(' + rnd(-24, 24).toFixed(1) + 'deg)"><path fill="currentColor"/></svg>';
      el.style.cssText = 'left:' + (q.x - q.s / 2).toFixed(1) + 'px;top:' + (q.y - q.s / 2).toFixed(1) + 'px;width:' + q.s.toFixed(1) +
        'px;height:' + q.s.toFixed(1) + 'px;--o:' + (.3 + depth * .45).toFixed(2) +
        ';--in:' + Math.round(Math.hypot(q.x - W / 2, q.y - H / 2) / reach * 900 + rnd(0, 250)) +
        'ms;--d:' + rnd(6, 11).toFixed(1) + 's;--dl:-' + rnd(0, 10).toFixed(1) + 's;--dx:' + rnd(-6, 6).toFixed(1) + 'px;--dy:' +
        (-(4 + depth * 6)).toFixed(1) + 'px;--dr:' + rnd(-9, 9).toFixed(1) + 'deg';
      var path = el.querySelector('path');
      path.setAttribute('d', mix(key, 1));
      felt.appendChild(el);
      marks.push({ p: path, key: key });
    });
  }
  lay();
  function again() { lastW = 0; lay(); }
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(again);
  addEventListener('load', again);
  var rz = 0;
  addEventListener('resize', function () { clearTimeout(rz); rz = setTimeout(lay, 200); });
  if (reduce) { felt.classList.add('lit'); return; }
  function turn() {
    var m = marks[(Math.random() * marks.length) | 0], t0 = 0;
    if (!m) return;
    requestAnimationFrame(function fold(now) {
      if (!t0) t0 = now;
      var u = Math.min(1, (now - t0) / 380);
      m.p.setAttribute('d', mix(m.key, 1 - easeOut(u)));
      if (u < 1) return requestAnimationFrame(fold);
      m.key = suit(); morphPath(m.p, m.key, 700, 160);
    });
  }
  var timer = 0;
  new IntersectionObserver(function (es) {
    clearInterval(timer);
    var on = es[0].isIntersecting;
    felt.classList.toggle('run', on);
    if (!on) return;
    felt.classList.add('lit');
    timer = setInterval(function () { if (!document.hidden) turn(); }, 2600);
  }, { threshold: .15 }).observe(host);
}

""" + s[b:]

# ---- the smoke: phones get it cleared for them, crisp, no blur ----
rep("""      var defs = document.createElementNS(NS, 'defs');
      defs.innerHTML = '<filter id="smokeblur" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="2.6"/></filter>';
      svg.appendChild(defs);""", """      /* touch screens: no hand to part it, so it parts itself when the
         moment comes into view, and the blur (costly to repaint) is dropped */
      var defs = document.createElementNS(NS, 'defs');
      if (!CALM) defs.innerHTML = '<filter id="smokeblur" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="2.6"/></filter>';
      svg.appendChild(defs);""")
rep("""      cloud.setAttribute('filter', 'url(#smokeblur)'); svg.appendChild(cloud);
      var puffs = [];
      for (var i = 0; i < 76; i++) {""", """      if (!CALM) cloud.setAttribute('filter', 'url(#smokeblur)');
      svg.appendChild(cloud);
      var puffs = [], onAt = 0;
      for (var i = 0; i < (CALM ? 44 : 76); i++) {""")
rep("""          o: rnd(.16, .34), rot""", """          o: CALM ? rnd(.08, .2) : rnd(.16, .34), rot""")
rep("""        var near = 0;
        for (var i = 0; i < puffs.length; i++) {""", """        /* the self-clearing (touch): the middle opens over a second and a half */
        var auto = CALM && onAt ? easeIO(Math.min(1, Math.max(0, (now - onAt - 500) / 1500))) : 0, rad = 88 * auto;
        var near = 0;
        for (var i = 0; i < puffs.length; i++) {""")
rep("""          x = q.hx + Math.sin(now / 1900 + q.ph) * 9 + q.ox; y = q.hy + q.oy;
          if (Math.hypot(x - 160, y - 110) < 62) near += q.s / 40;""", """          x = q.hx + Math.sin(now / 1900 + q.ph) * 9 + q.ox; y = q.hy + q.oy;
          if (rad) {
            var cdx = x - 160, cdy = y - 110, cd = Math.hypot(cdx, cdy) || 1, lim = rad * 1.3;
            if (cd < lim) { var nd = cd + (lim - cd) * .77; x = 160 + cdx / cd * nd; y = 110 + cdy / cd * nd; }
          }
          if (Math.hypot(x - 160, y - 110) < 62) near += q.s / 40;""")
rep("""        new IntersectionObserver(function (es) {
          smokeOn = es[0].isIntersecting;""", """        new IntersectionObserver(function (es) {
          smokeOn = es[0].isIntersecting;
          onAt = smokeOn ? performance.now() : 0;""")
# on touch the ghost hand stays home: the self-clearing does its work
rep("""        if (now - hand.at > 3200) {""", """        if (CALM) hx = hy = -1e3;
        else if (now - hand.at > 3200) {""")

# ---- the chevron rides with CSS (sticky); the script only colours it ----
rep("""      var r = list.getBoundingClientRect(), vh = innerHeight;
      var p = (vh * .5 - r.top) / r.height;
      p = p < 0 ? 0 : p > 1 ? 1 : p;
      mark.style.transform = 'translateY(' + (p * (r.height - 40)).toFixed(1) + 'px)';
      mark.classList.toggle('gold', opt && p * r.height > parseFloat(line.style.height));""",
    """      var at = mark.getBoundingClientRect().top - list.getBoundingClientRect().top;
      mark.classList.toggle('gold', !!opt && at > parseFloat(line.style.height));""")

# ---- a shorter swipe deals the card; a quick flick does too ----
rep("""    drag = { id: e.pointerId, x: e.clientX, el: el, dx: 0 };""",
    """    drag = { id: e.pointerId, x: e.clientX, el: el, dx: 0, vx: 0, t: e.timeStamp };""")
rep("""    var dx = e.clientX - drag.x;
    drag.dx = dx;""", """    var dx = e.clientX - drag.x, dt = e.timeStamp - drag.t;
    if (dt > 0) drag.vx = drag.vx * .5 + (dx - drag.dx) / dt * .5;   /* px per ms, smoothed */
    drag.dx = dx; drag.t = e.timeStamp;""")
rep("""    var dx = drag.dx || 0, el = drag.el;
    drag = null;
    if (Math.abs(dx) > 90) {""", """    var dx = drag.dx || 0, el = drag.el, flick = Math.abs(drag.vx) > .45 && drag.vx * dx > 0;
    drag = null;
    if (Math.abs(dx) > 45 || (flick && Math.abs(dx) > 20)) {""")

open(p, 'w', encoding='utf-8', newline='\n').write(s)
a = s.index('/* ==========================================================================\n   THE FIELD')
b = s.index('/* ==========================================================================\n   GRAPHS')
open(os.path.join(ROOT, 'src', 'field_r8.js'), 'w', encoding='utf-8', newline='\n').write(s[a:b].rstrip() + '\n')

# ---- markup: the chevron lives in a track the height of the route ----
h = os.path.join(ROOT, 'src', 'shell.html')
t = open(h, encoding='utf-8').read()
a = '''    <svg class="spinemark" id="spinemark" viewBox="0 0 64 28" aria-hidden="true"><use href="#chevron-down"/></svg>'''
assert t.count(a) == 1
t = t.replace(a, '''    <div class="spinetrack" aria-hidden="true"><svg class="spinemark" id="spinemark" viewBox="0 0 64 28"><use href="#chevron-down"/></svg></div>''')
open(h, 'w', encoding='utf-8', newline='\n').write(t)

# ---- CSS ----
c = os.path.join(ROOT, 'site', 'styles.css')
t = open(c, encoding='utf-8').read()


def srep(a, b):
    global t
    assert t.count(a) == 1, a[:90]
    t = t.replace(a, b)


srep("""/* the calm felt (phones): scattered suits that drift, lit outward from the copy */
.calm .m{opacity:0;transform-box:fill-box;transform-origin:50% 50%;transition:opacity 1.4s linear var(--in);
  animation:drift var(--d) ease-in-out var(--dl) infinite}
.calm.lit .m{opacity:var(--o)}
@keyframes drift{50%{transform:translate(var(--dx),var(--dy)) rotate(var(--dr))}}""",
"""/* the calm felt (phones): scattered suits, each its own layer, drifting on the compositor */
.felt{position:absolute;inset:0;z-index:1;pointer-events:none;overflow:hidden;color:var(--white);contain:strict}
.felt .m{position:absolute;display:block;opacity:0;will-change:transform,opacity;
  transition:opacity 1.4s linear var(--in);animation:drift var(--d) ease-in-out var(--dl) infinite paused}
.felt .m.red{color:#A81A2C}
.felt .m svg{display:block;width:100%;height:100%}
.felt.run .m{animation-play-state:running}
.felt.lit .m{opacity:var(--o)}
@keyframes drift{50%{transform:translate3d(var(--dx),var(--dy),0) rotate(var(--dr))}}""")
srep(".calm .m{animation:none!important}", ".felt .m{animation:none!important}")
srep(""".spinemark{position:absolute;top:0;left:calc(clamp(14px,1.7vw,18px)/2 - 12px);width:24px;height:11px;
  color:var(--cream);filter:drop-shadow(0 0 8px rgba(243,238,228,.55));will-change:transform;
  transition:color .5s linear}""", """/* the chevron rides the middle of the screen by itself (sticky), clamped to the route */
.spinetrack{position:absolute;top:0;bottom:0;left:calc(clamp(14px,1.7vw,18px)/2 - 12px);width:24px;pointer-events:none}
.spinemark{position:sticky;top:50svh;display:block;width:24px;height:11px;
  color:var(--cream);filter:drop-shadow(0 0 8px rgba(243,238,228,.55));
  transition:color .5s linear}""")
open(c, 'w', encoding='utf-8', newline='\n').write(t)
print('ok')
