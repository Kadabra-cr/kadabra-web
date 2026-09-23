"""Round 16: '¿Jugar?' asks sooner, is easier to hit and answers the hover
('¡Jugar!'); phones get a calm felt (scattered suits that drift, one turning
now and then) instead of the game; a touch hint for the deck."""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..')
p = os.path.join(ROOT, 'src', 'app.src.js')
s = open(p, encoding='utf-8').read()


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:100])
    s = s.replace(a, b)


# ---- the ask: sooner, bigger, and it answers the hover ----
rep("""  askEl.innerHTML = '<button type="button" class="yes">@@t.game.ask@@</button>' +""",
    """  askEl.innerHTML = '<button type="button" class="yes"><span>@@t.game.ask@@</span><span aria-hidden="true">@@t.game.ask.hover@@</span></button>' +""")
rep("""heart.mass >= CAP * .5 && !host.classList.contains('condensed')) ask();""",
    """heart.mass >= CAP * .2 && !host.classList.contains('condensed')) ask();""")
rep("""          askP.x = Math.max(12, Math.min(hb.width - aw - 12, hx + rr * .7 + 14));
          askP.y = Math.max(12, Math.min(hb.height - ah - 12, hy - rr * .7 - ah - 10));""",
    """          askP.x = Math.max(12, Math.min(hb.width - aw - 12, hx + rr * .6 + 10));
          askP.y = Math.max(12, Math.min(hb.height - ah - 12, hy - rr * .6 - ah - 6));""")

# ---- phones: the calm felt ----
rep("""function makeField(svg, opt) {
  var W = opt.w, H = opt.h;""", """/* Phones and touch screens get a calm felt instead of the game: the suits lie
   scattered where a hand would have woken them, clear of the copy, and only
   drift. CSS does the floating; now and then one folds back into a square
   and comes up a new suit. No loop runs while nothing turns. */
var CALM = matchMedia('(hover: none), (max-width: 760px)').matches;
function calmField(svg, opt) {
  var host = svg.parentNode, marks = [], lastW = 0;
  svg.classList.add('calm');
  function lay() {
    var b = svg.getBoundingClientRect(), W = Math.round(b.width), H = Math.round(b.height);
    if (!W || !H || W === lastW) return;
    lastW = W;
    svg.setAttribute('viewBox', '0 0 ' + W + ' ' + H);
    var zones = [];
    (opt.text || []).forEach(function (el) {
      [].forEach.call(el.getClientRects(), function (r) {
        if (r.width) zones.push({ x0: r.left - b.left, x1: r.right - b.left, y0: r.top - b.top, y1: r.bottom - b.top });
      });
    });
    var want = Math.max(9, Math.min(20, Math.round(W * H / 15000))), got = [];
    for (var k = 0; k < 900 && got.length < want; k++) {
      var sz = rnd(15, 34), x = rnd(sz, W - sz), y = rnd(sz, H - sz), m = sz * .7 + 10, ok = true;
      zones.forEach(function (z) { if (x > z.x0 - m && x < z.x1 + m && y > z.y0 - m && y < z.y1 + m) ok = false; });
      got.forEach(function (o) { if (Math.hypot(o.x - x, o.y - y) < (o.s + sz) * .8 + 22) ok = false; });
      if (ok) got.push({ x: x, y: y, s: sz });
    }
    svg.innerHTML = ''; marks = [];
    var reach = Math.hypot(W / 2, H / 2);
    got.forEach(function (q, i) {
      var g = document.createElementNS(NS, 'g'), inner = document.createElementNS(NS, 'g'), path = document.createElementNS(NS, 'path');
      var key = suit(), depth = (q.s - 15) / 19;
      path.setAttribute('d', mix(key, 1)); path.setAttribute('fill', 'currentColor');
      if (i % 6 === 4) inner.setAttribute('fill', '#A81A2C');
      inner.setAttribute('transform', 'translate(' + q.x.toFixed(1) + ' ' + q.y.toFixed(1) + ') rotate(' + rnd(-24, 24).toFixed(1) +
        ') scale(' + (q.s / 100).toFixed(4) + ') translate(-50 -50)');
      inner.appendChild(path); g.appendChild(inner);
      g.setAttribute('class', 'm');
      /* bigger ones sit nearer: brighter, and they travel further */
      g.style.cssText = '--o:' + (.3 + depth * .45).toFixed(2) + ';--in:' + Math.round(Math.hypot(q.x - W / 2, q.y - H / 2) / reach * 900 + rnd(0, 250)) +
        'ms;--d:' + rnd(6, 11).toFixed(1) + 's;--dl:-' + rnd(0, 10).toFixed(1) + 's;--dx:' + rnd(-7, 7).toFixed(1) + 'px;--dy:' +
        (-(5 + depth * 7)).toFixed(1) + 'px;--dr:' + rnd(-9, 9).toFixed(1) + 'deg';
      svg.appendChild(g);
      marks.push({ p: path, key: key });
    });
  }
  lay();
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { lastW = 0; lay(); });
  var rz = 0;
  addEventListener('resize', function () { clearTimeout(rz); rz = setTimeout(lay, 200); });
  if (reduce) { svg.classList.add('lit'); return; }
  /* one turn: the suit folds into its square and opens as another */
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
    if (!es[0].isIntersecting) return;
    svg.classList.add('lit');
    timer = setInterval(function () { if (!document.hidden) turn(); }, 2600);
  }, { threshold: .15 }).observe(host);
}

function makeField(svg, opt) {
  if (CALM) return calmField(svg, opt);
  var W = opt.w, H = opt.h;""")

# ---- the deck's hint says what a thumb can do ----
rep("""  var HINT = '@@t.swipe.hint.mid@@ ';

  function setHint() {
    hint.innerHTML = '@@t.swipe.hint.pre@@ ' + Math.min(idx + 1, 5) + ' ' + HINT +
      '<span class="kbd"><kbd>&larr;</kbd><kbd>&rarr;</kbd></span>.';
  }""", """  var HINT = '@@t.swipe.hint.mid@@ ', THUMB = matchMedia('(hover: none)').matches;

  function setHint() {
    hint.innerHTML = '@@t.swipe.hint.pre@@ ' + Math.min(idx + 1, 5) + ' ' + (THUMB ? '@@t.swipe.hint.touch@@' :
      HINT + '<span class="kbd"><kbd>&larr;</kbd><kbd>&rarr;</kbd></span>.');
  }""")

open(p, 'w', encoding='utf-8', newline='\n').write(s)
a = s.index('/* ==========================================================================\n   THE FIELD')
b = s.index('/* ==========================================================================\n   GRAPHS')
open(os.path.join(ROOT, 'src', 'field_r8.js'), 'w', encoding='utf-8', newline='\n').write(s[a:b].rstrip() + '\n')

# ---- copy ----
cp = os.path.join(ROOT, 'src', 'copy.es.md')
t = open(cp, encoding='utf-8').read()


def crep(a, b):
    global t
    assert t.count(a) == 1, a
    t = t.replace(a, b)


crep("game.ask: ¿Jugar?\n", "game.ask: ¿Jugar?\ngame.ask.hover: ¡Jugar!\n")
crep("swipe.hint.mid: de 5. Arrastre la carta, use los botones o presione\n",
     "swipe.hint.mid: de 5. Arrastre la carta, use los botones o presione\nswipe.hint.touch: de 5. Deslice la carta o toque un botón.\n")
open(cp, 'w', encoding='utf-8', newline='\n').write(t)

# ---- CSS ----
c = os.path.join(ROOT, 'site', 'styles.css')
t = open(c, encoding='utf-8').read()


def srep(a, b):
    global t
    assert t.count(a) == 1, a[:90]
    t = t.replace(a, b)


srep(""".ask .yes{font:inherit;font-weight:600;background:var(--gold);color:var(--carbon);border:0;border-radius:999px;
  padding:.5em 1.05em;cursor:pointer;transition:background .2s var(--ease)}
.ask .yes:hover{background:#DDB437}""", """.ask .yes{font:inherit;font-size:1rem;font-weight:700;background:var(--gold);color:var(--carbon);border:0;border-radius:999px;
  min-height:40px;padding:.55em 1.3em;cursor:pointer;display:grid;transition:background .2s var(--ease)}
/* the two words share one cell, so the pill never changes width */
.ask .yes span{grid-area:1/1;transition:opacity .18s linear,translate .3s cubic-bezier(.16,1,.3,1)}
.ask .yes span+span{opacity:0;translate:0 5px}
.ask .yes:is(:hover,:focus-visible) span:first-child{opacity:0;translate:0 -5px}
.ask .yes:is(:hover,:focus-visible) span+span{opacity:1;translate:0 0}
.ask .yes:hover{background:#DDB437}""")
srep(".ask .no{display:grid;place-items:center;width:28px;height:28px;",
     ".ask .no{display:grid;place-items:center;width:34px;height:34px;")
srep("""#field{position:absolute;inset:0;width:100%;height:100%;display:block;
  color:var(--white);pointer-events:none}""", """#field{position:absolute;inset:0;width:100%;height:100%;display:block;
  color:var(--white);pointer-events:none}
/* the calm felt (phones): scattered suits that drift, lit outward from the copy */
.calm .m{opacity:0;transform-box:fill-box;transform-origin:50% 50%;transition:opacity 1.4s linear var(--in);
  animation:drift var(--d) ease-in-out var(--dl) infinite}
.calm.lit .m{opacity:var(--o)}
@keyframes drift{50%{transform:translate(var(--dx),var(--dy)) rotate(var(--dr))}}""")
a = '  .cable .flow,.whyband .suit path,.pointing .cta .point,.mode .dot,.mode.shake{animation:none!important}'
srep(a, '  .cable .flow,.whyband .suit path,.pointing .cta .point,.mode .dot,.mode.shake,.calm .m{animation:none!important}')
open(c, 'w', encoding='utf-8', newline='\n').write(t)
print('ok')
