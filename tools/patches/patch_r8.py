import io, os, re

os.chdir(os.path.dirname(os.path.abspath(__file__)))
SITE = '..'


def rd(p): return io.open(p, encoding='utf-8').read()
def wr(p, s): io.open(p, 'w', encoding='utf-8', newline='\n').write(s)
def sub1(s, old, new):
    assert s.count(old) == 1, ('anchor count %d: ' % s.count(old)) + old[:70]
    return s.replace(old, new)


# ============================ app.src.js ====================================
s = rd('app.src.js')

# --- the field: whole engine replaced (game) ---
a = s.index('/* ==========================================================================\n   THE FIELD:')
b = s.index('/* ==========================================================================\n   NUMBERS:')
s = s[:a] + rd('field_r8.js').rstrip('\n') + '\n\n' + s[b:]

# --- graphs: one function, two graphs ---
a = s.index('/* ==========================================================================\n   NUMBERS:')
b = s.index('/* ==========================================================================\n   SWIPE:')
s = s[:a] + r'''/* ==========================================================================
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

  new IntersectionObserver(function (es, o) {
    if (!es[0].isIntersecting) return;
    o.disconnect();
    var lastAt = 0;
    cfg.beats.forEach(function (bt) {
      lastAt = Math.max(lastAt, bt.at);
      setTimeout(function () { beatOn(bt.cls); bt.fn(A, B); }, bt.at);
    });
    setTimeout(function () { live = true; root.classList.add('live'); }, lastAt + 900);
  }, { threshold: .35 }).observe(root);
}

/* it works, until it doesn't: 93 of 100 save time with AI, 9 of 100 have a rule */
makeGraph({ id: 'policy',
  a: { svg: document.getElementById('polA'), count: 100 }, b: { svg: document.getElementById('polB'), count: 100 },
  setup: function (A, B) {
    A.forEach(function (c) { c.fo = .14; if (c.n < 93) { c.g.classList.add('lit'); c.fo = 1; } });
    B.forEach(function (c) { c.fo = .14; if (c.n < 9) { c.g.classList.add('lit'); c.strong = true; } });
  },
  still: function (A, B) { B.slice(0, 9).forEach(function (c) { c.p.setAttribute('d', mix('smooth-diamond', 1)); }); },
  beats: [
    { at: 0, cls: 'in', fn: function (A, B) { A.concat(B).forEach(function (c) { c.g.style.transitionDelay = (c.row * 22) + 'ms'; }); } },
    { at: 650, cls: 'lit', fn: function (A) { A.forEach(function (c) { if (c.n < 93) c.p.style.transitionDelay = (c.row * 26 + c.col * 6) + 'ms'; }); } },
    { at: 1700, cls: 'rules', fn: function (A, B) {
      B.slice(0, 9).forEach(function (c, i) { c.p.style.transitionDelay = (i * 70) + 'ms'; morphPath(c.p, 'smooth-diamond', 520, i * 70); });
    } }
  ] });

/* taught first: the same hundred people, twice. Taught, they do 34% more */
makeGraph({ id: 'viz',
  a: { svg: document.getElementById('barA'), count: 100 }, b: { svg: document.getElementById('barB'), count: 134 },
  setup: function (A, B) {
    A.forEach(function (c) { c.fo = .42; });
    B.forEach(function (c) { c.strong = true; if (c.n >= 100) c.g.classList.add('extra'); });
  },
  still: function (A, B) { B.forEach(function (c) { c.p.setAttribute('d', mix('smooth-spade', 1)); }); },
  beats: [
    { at: 0, cls: 'in', fn: function (A, B) { A.concat(B.slice(0, 100)).forEach(function (c) { c.g.style.transitionDelay = (c.row * 22) + 'ms'; }); } },
    { at: 650, cls: 'taught', fn: function (A, B) { B.slice(0, 100).forEach(function (c) { morphPath(c.p, 'smooth-spade', 420, c.row * 28 + c.col * 7); }); } },
    { at: 1600, cls: 'more', fn: function (A, B) {
      B.slice(100).forEach(function (c, i) { c.p.setAttribute('d', mix('smooth-spade', 1)); c.g.style.transitionDelay = (i * 16) + 'ms'; });
    } }
  ] });

''' + s[b:]

# --- swipe: the nudge's return timer must die with the nudge (it was flying a
#     dealt card back into the deck) ---
s = sub1(s, "nudgeTimer = 0, nudgeSide = 1;", "nudgeTimer = 0, nudgeBack = 0, nudgeSide = 1;")
s = sub1(s, '''      (right ? pileR : pileL).classList.add('nudge');
      setTimeout(function () {''', '''      (right ? pileR : pileL).classList.add('nudge');
      nudgeBack = setTimeout(function () {''')
s = sub1(s, '''        pileL.classList.remove('nudge');
        el.style.transition = 'transform .45s var(--ease)';
        el.style.transform = el.dataset.rest;
        armNudge();''', '''        pileL.classList.remove('nudge');
        if (el.classList.contains('piled')) return;
        el.style.transition = 'transform .45s var(--ease)';
        el.style.transform = el.dataset.rest;
        armNudge();''')
s = sub1(s, '''    touched = true;
    clearTimeout(nudgeTimer);''', '''    touched = true;
    clearTimeout(nudgeTimer); clearTimeout(nudgeBack);''')

# --- cables: thick, long, from the band's middle to the note's middle ---
s = sub1(s, "var N = 26, GRAV = 1500, DAMP = .985, ITER = 4;", "var N = 30, GRAV = 1500, DAMP = .985, ITER = 4;")
s = sub1(s, '''      var a1 = m.getBoundingClientRect(), b1 = note.getBoundingClientRect();
      return { fn: m.dataset.fn,
        x1: a1.right - host.left - 4, y1: a1.top + a1.height * .5 - host.top,
        x2: b1.left - host.left - 6, y2: b1.top + 30 - host.top };''',
'''      var band = m.querySelector('.cband') || m, said = note.querySelector('.said') || note;
      var a1 = band.getBoundingClientRect(), b1 = said.getBoundingClientRect();
      return { fn: m.dataset.fn,
        x1: a1.right - host.left - 2, y1: a1.top + a1.height * .5 - host.top,
        x2: b1.left - host.left - 10, y2: b1.top + b1.height * .5 - host.top };''')
s = sub1(s, "var len = span * 1.28, seg = len / (N - 1), pts = [];", "var len = span * 1.5 + 60, seg = len / (N - 1), pts = [];")

# --- the star breaks in two ---
s = sub1(s, '''      var hp = svg.querySelector('.host path');
      hp.setAttribute('d', PATHS.square);
      hp.parentNode.setAttribute('transform', 'translate(160 108) scale(1.5) translate(-50 -50)');
      once(m, function (on) { if (on) morphPath(hp, 'smooth-diamond', 820, 100); });''',
'''      var hps = svg.querySelectorAll('.host path');
      hps.forEach(function (hp) {
        hp.setAttribute('d', PATHS.square);
        hp.parentNode.setAttribute('transform', 'translate(160 108) scale(1.5) translate(-50 -50)');
      });
      once(m, function (on) { if (on) hps.forEach(function (hp) { morphPath(hp, 'smooth-diamond', 820, 100); }); });''')

# --- the scene: scroll condenses the hero to the left while the next screen
#     rises from the bottom right. Scrubbed by the scroll, never on a timer. ---
assert s.rstrip().endswith('})();')
s = s.rstrip()[:-len('})();')] + r'''/* ==========================================================================
   SCENE: the hero condenses to the left as "It works. Until it doesn't."
   rises from the bottom right into a full screen. The scroll is the scrub.
   ========================================================================== */
(function () {
  var scene = document.getElementById('scene');
  if (!scene) return;
  var pin = scene.querySelector('.scene-pin'), narrow = matchMedia('(max-width: 900px)');
  var raf = 0;
  function run() {
    raf = 0;
    if (reduce || narrow.matches) { scene.classList.remove('live'); scene.style.removeProperty('--q'); return; }
    scene.classList.add('live');
    var top = scene.getBoundingClientRect().top + scrollY;
    var track = scene.offsetHeight - pin.offsetHeight;
    var p = Math.max(0, Math.min(1, (scrollY - top) / (track || 1)));
    var q = Math.max(0, Math.min(1, (p - .12) / .66));
    q = q * q * (3 - 2 * q);
    scene.style.setProperty('--q', q.toFixed(4));
    scene.classList.toggle('past', q > .55);
  }
  function ask() { if (!raf) raf = requestAnimationFrame(run); }
  addEventListener('scroll', ask, { passive: true });
  addEventListener('resize', ask, { passive: true });
  if (narrow.addEventListener) narrow.addEventListener('change', ask);
  run();
})();

})();
'''
wr('app.src.js', s)


# ============================ shell.html ====================================
h = rd('shell.html')
# hero button: seen, with an arrow that moves
h = sub1(h, '''      <a class="btn go" href="/workshop/">See the workshop</a></p>
    <p class="fine rise">Opens a WhatsApp chat. No form, nothing to buy.</p>''',
'''      <a class="btn go arrow" href="/workshop/">See the workshop<svg class="arr" viewBox="0 0 64 28" aria-hidden="true"><use href="#arrow"/></svg></a></p>
    <p class="fine rise">Opens a WhatsApp chat. No form, nothing to buy.</p>''')
# the scene wraps the hero and the breaks screen
h = sub1(h, '<section class="hero" id="hero">', '<div class="scene" id="scene"><div class="scene-pin">\n<section class="hero" id="hero">')
old_numbers_head = '''<!-- ---------------------------- numbers, cream --------------------------- -->
<section class="band numbers" id="numbers">
  <div class="wrap">
    <h2 class="h2">It works. Until it doesn't.</h2>

    <div class="pair" id="pair">
      <div class="a">
        <b class="fignum" data-count="93">93%</b>
        <p>of Costa Rican tech companies save time on repetitive tasks with AI.</p>
        <p class="src">PROCOMER, 2025</p>
      </div>
      <div class="b">
        <b class="fignum" data-count="9">9%</b>
        <p>of them have any formal AI policy.</p>
        <p class="src">PROCOMER, 2025</p>
      </div>
    </div>
    <p class="pairnote">The same companies. The same year.</p>

    <div class="viz" id="viz">'''
new_numbers_head = '''<!-- ---------------------------- it works. until it doesn't. ------------- -->
<section class="breaks" id="breaks">
  <div class="wrap">
    <h2 class="h2">It works. Until it doesn't.</h2>
    <div class="pair" id="pair">
      <div class="a">
        <b class="fignum" data-count="93">93%</b>
        <p>of Costa Rican tech companies save time on repetitive tasks with AI.</p>
        <p class="src">PROCOMER, 2025</p>
      </div>
      <div class="b">
        <b class="fignum" data-count="9">9%</b>
        <p>of them have any formal AI policy.</p>
        <p class="src">PROCOMER, 2025</p>
      </div>
    </div>
    <p class="pairnote">The same companies. The same year.</p>
  </div>
</section>
</div></div>

<!-- ---------------------------- numbers, cream --------------------------- -->
<section class="band numbers" id="numbers">
  <div class="wrap">
    <div class="viz policy first" id="policy">
      <h3>Nearly everyone uses it. Almost no one has a rule for it.</h3>
      <span class="rule ruledraw" aria-hidden="true"></span>
      <p class="lede">A hundred Costa Rican tech companies. Ninety-three already save time with AI. Nine have written down a single rule about it.</p>

      <div class="vizgrid">
        <div class="bars" role="img" aria-label="Two bars of a hundred marks each. Ninety-three lit in the first: companies that save time with AI. Nine lit in the second: companies with any AI policy.">
          <figure class="barcol base">
            <svg id="polA" aria-hidden="true"></svg>
            <figcaption><b>93%</b><span>Save time with AI</span></figcaption>
          </figure>
          <figure class="barcol rules">
            <svg id="polB" aria-hidden="true"></svg>
            <figcaption><b>9%</b><span>Have any AI policy</span></figcaption>
          </figure>
        </div>
        <div class="story">
          <p class="beat-l" data-beat="in">A hundred Costa Rican tech companies.</p>
          <p class="beat-l" data-beat="lit">Ninety-three of them already save time with AI.</p>
          <p class="beat-l" data-beat="rules">Nine of them have any rule about it.</p>
          <p class="aside">The other eighty-four are running on luck. Same companies, same year.</p>
          <div class="cites">
            <p class="src">93% save time, 9% have a policy &mdash; PROCOMER, Caracterizaci&oacute;n del Sector TIC, 2025</p>
          </div>
        </div>
      </div>
    </div>

    <div class="viz" id="viz">'''
h = sub1(h, old_numbers_head, new_numbers_head)

# the finale: a card of its own, tilted, with the eye led to it
h = sub1(h, '''    <div id="reveal" hidden>
      <p class="workshopline">Those catches are what we teach in half a day.</p>
      <div class="dealagain"><button class="btn" id="bAgain" type="button">Deal again</button></div>
    </div>''',
'''    <div id="reveal" hidden>
      <div class="finale rise">
        <span class="guide l" aria-hidden="true"><svg viewBox="0 0 28 64"><use href="#chevron"/></svg><svg viewBox="0 0 28 64"><use href="#chevron"/></svg><svg viewBox="0 0 28 64"><use href="#chevron"/></svg></span>
        <article class="fcard">
          <svg class="pip" viewBox="0 0 100 100" aria-hidden="true"><use href="#classic-heart"/></svg>
          <span class="ix ixa">6<svg viewBox="0 0 100 100" aria-hidden="true"><use href="#classic-heart"/></svg></span>
          <div class="top"></div>
          <div class="cband"><p class="workshopline">Those catches are what we teach in half a day.</p></div>
          <div class="bot"></div>
          <span class="ix ixb">6<svg viewBox="0 0 100 100" aria-hidden="true"><use href="#classic-heart"/></svg></span>
        </article>
        <span class="guide r" aria-hidden="true"><svg viewBox="0 0 28 64"><use href="#chevron"/></svg><svg viewBox="0 0 28 64"><use href="#chevron"/></svg><svg viewBox="0 0 28 64"><use href="#chevron"/></svg></span>
      </div>
      <p class="ctas rise"><a class="cta" href="/workshop/">See the workshop</a>
        <button class="btn" id="bAgain" type="button">Deal again</button></p>
    </div>''')

# the star breaks in two
h = sub1(h, '''      <div class="m-vis"><svg class="vis-break" viewBox="0 0 320 220" aria-hidden="true">
        <g class="host"><path fill="currentColor" opacity=".8"/></g>
        <rect class="slash" x="20" y="104" width="280" height="9" fill="currentColor"/>
      </svg></div>''',
'''      <div class="m-vis"><svg class="vis-break" viewBox="0 0 320 220" aria-hidden="true">
        <clipPath id="crackL"><polygon points="0,0 176,0 150,58 178,104 146,150 170,220 0,220"/></clipPath>
        <clipPath id="crackR"><polygon points="176,0 320,0 320,220 170,220 146,150 178,104 150,58"/></clipPath>
        <g class="half l" clip-path="url(#crackL)"><g class="host"><path fill="currentColor" opacity=".8"/></g></g>
        <g class="half r" clip-path="url(#crackR)"><g class="host"><path fill="currentColor" opacity=".8"/></g></g>
      </svg></div>''')
wr('shell.html', h)


# ============================ build.py ======================================
bp = rd('build.py')
bp = sub1(bp, '''MORE = """
    <p class="more rise"><a class="btn go" href="/workshop/">See what a half-day looks like</a></p>"""''',
'''HALF = """<section class="band halfday" id="halfday-{k}">
  <div class="wrap">
    <p class="kicker rise">Before you book</p>
    <h2 class="h2 rise">See what half a day looks like.</h2>
    <p class="lede rise">Seven moments, your own work on the table, and a one-page plan the week after. Two minutes to read.</p>
    <p class="rise"><a class="btn go arrow light" href="/workshop/">See the workshop<svg class="arr" viewBox="0 0 64 28" aria-hidden="true"><use href="#arrow"/></svg></a></p>
  </div>
</section>
"""''')
bp = sub1(bp, 'page = page.replace("@@CLOSE_HOME@@", CLOSE.format(k="home", more=MORE))',
              'page = page.replace("@@CLOSE_HOME@@", HALF.format(k="home") + CLOSE.format(k="home", more=""))')
bp = sub1(bp, 'page = page.replace("@@CLOSE_LEARN@@", CLOSE.format(k="learn", more=MORE))',
              'page = page.replace("@@CLOSE_LEARN@@", HALF.format(k="learn") + CLOSE.format(k="learn", more=""))')
wr('build.py', bp)


# ============================ sprites.svg ===================================
sp = rd(os.path.join(SITE, 'sprites.svg'))
if 'id="arrow"' not in sp:
    sp = sub1(sp, '<symbol id="chevron-down"',
              '<symbol id="arrow" viewBox="0 0 64 28"><path fill="currentColor" d="M0 11.5h46v5H0zM44.5 0 64 14 44.5 28l-3.4-3.6L55 14 41.1 3.6z"/></symbol>\n<symbol id="chevron-down"')
    wr(os.path.join(SITE, 'sprites.svg'), sp)


# ============================ styles.css ====================================
c = rd(os.path.join(SITE, 'styles.css'))
# header: a little more presence
c = sub1(c, '  --hdr:64px;', '  --hdr:72px;')
c = sub1(c, '.brand svg{height:28px;width:auto;color:var(--white);display:block}',
            '.brand svg{height:34px;width:auto;color:var(--white);display:block}')
c = sub1(c, '.nav{display:flex;gap:clamp(14px,2.4vw,34px);margin-left:auto;font-size:.95rem}',
            '.nav{display:flex;gap:clamp(14px,2.4vw,34px);margin-left:auto;font-size:1rem}')
# the old slash rules go
c = sub1(c, '''.vis-break .slash{transform-origin:50% 50%;color:var(--red-lift);
  transition:transform .8s var(--ease) .5s}
.js .vis-break .slash{transform:scaleX(0)}
.js .moment.on .vis-break .slash{transform:scaleX(1)}
''', '''.vis-break .half{transition:transform 1.1s cubic-bezier(.16,1,.3,1) .95s}
.vis-break .half.l{transform-origin:150px 108px}
.vis-break .half.r{transform-origin:170px 108px}
.js .moment.on .vis-break .half.l{transform:translate(-13px,7px) rotate(-7deg)}
.js .moment.on .vis-break .half.r{transform:translate(13px,-5px) rotate(6deg)}
''')
# cables: thicker, cream, gold only with current
c = sub1(c, '''.cable .rope{fill:none;stroke:var(--on-felt);stroke-width:4;stroke-linecap:round;opacity:.55;''',
            '''.cable .rope{fill:none;stroke:var(--cream-2);stroke-width:9;stroke-linecap:round;opacity:.92;''')
c = sub1(c, '''.cable .flow{fill:none;stroke:var(--gold);stroke-width:4;stroke-linecap:round;opacity:0;''',
            '''.cable .flow{fill:none;stroke:var(--gold);stroke-width:9;stroke-linecap:round;opacity:0;''')
c = sub1(c, '.row{display:grid;grid-template-columns:auto minmax(0,1fr);gap:clamp(70px,9vw,130px);align-items:center;',
            '.row{display:grid;grid-template-columns:auto minmax(0,1fr);gap:clamp(140px,17vw,280px);align-items:center;')
c = sub1(c, '.viz.live .bars .mk path{transition:transform .22s cubic-bezier(.16,1,.3,1)}',
            '.viz.live .bars .mk path{transition:transform .22s cubic-bezier(.16,1,.3,1),fill-opacity .2s linear}')
c = sub1(c, '.viz.in .beat-l[data-beat=in],.viz.taught .beat-l[data-beat=taught],.viz.more .beat-l[data-beat=more]{opacity:1;transform:none}',
            '.beat-l.on{opacity:1;transform:none}')
c = sub1(c, '.beat-l[data-beat=more]{color:var(--gold-ink)}', '.beat-l[data-beat=more],.beat-l[data-beat=rules]{color:var(--gold-ink)}')
c = sub1(c, '.close .more{margin-top:calc(var(--cell)*.8)}\n', '')
c = sub1(c, '''.workshopline{margin-top:calc(var(--cell)*1.4);font-family:var(--title);font-weight:800;
  letter-spacing:-.035em;font-size:clamp(1.6rem,4vw,3rem);color:var(--white);
  padding-bottom:.1em}
.dealagain{margin-top:calc(var(--cell)*1.1);display:flex;justify-content:center}
''', '')

c += r'''

/* ============================ ROUND 8 ==================================== */
/* --- the hero button that is seen, with an arrow that moves --- */
.btn.arrow{display:inline-flex;align-items:center;gap:.55em}
.btn .arr{width:1.25em;height:.55em;flex:none;transition:transform .35s var(--ease);animation:arrIdle 2.8s var(--ease) infinite}
.btn.arrow:hover .arr{transform:translateX(6px);animation:none}
@keyframes arrIdle{0%,100%{transform:translateX(0)}50%{transform:translateX(5px)}}
.hero .btn.go{border:2px solid var(--gold);color:var(--gold);padding:calc(1.05em - 2px) 1.5em}
.hero .btn.go:hover{background:var(--gold);color:var(--carbon);border-color:var(--gold)}

/* --- the field at war --- */
.hero .wrap,.close .wrap{transition:opacity 1.1s linear}
.hero.armed .wrap,.close.armed .wrap{opacity:.28}
.hero.dead .wrap,.close.dead .wrap{opacity:1}
.war text{font-family:var(--title);font-weight:800;fill:var(--white);
  paint-order:stroke;stroke:rgba(18,38,31,.55);stroke-width:6px;stroke-linejoin:round}
.war{filter:drop-shadow(0 0 9px rgba(255,255,255,.35))}
.hero h1,.hero .sub,.close h2,.close .fine{transition:opacity .4s linear}

/* --- the scene: hero condenses left, the next screen rises from the right --- */
.scene{--q:0;position:relative}
.breaks{background:var(--cream);color:var(--ink);padding:calc(var(--cell)*2.6) 0}
.breaks .h2{color:var(--ink)}
@media (min-width:901px){
  .js .scene.live{height:calc((100svh - var(--hdr))*2.6)}
  .js .scene.live .scene-pin{position:sticky;top:var(--hdr);height:calc(100svh - var(--hdr));overflow:hidden;background:var(--felt-deep)}
  .js .scene.live .hero{position:absolute;inset:0;min-height:0;transform-origin:0 50%;
    transform:translateX(calc(var(--q)*-36%)) scale(calc(1 - var(--q)*.4));opacity:calc(1 - var(--q)*.94);
    will-change:transform,opacity}
  .js .scene.live.past .hero{pointer-events:none}
  .js .scene.live .breaks{position:absolute;inset:0;display:grid;align-items:center;padding:0;
    transform-origin:100% 100%;
    transform:translate(calc((1 - var(--q))*62%),calc((1 - var(--q))*100%)) scale(calc(.84 + var(--q)*.16));
    opacity:calc(var(--q)*2.2);will-change:transform,opacity;
    box-shadow:-40px -20px 90px -40px rgba(0,0,0,.55)}
  .js .scene.live .breaks .wrap{padding:calc(var(--cell)*1.2) 0}
  .js .scene.live .pair>div{min-height:calc(var(--q)*(100svh - var(--hdr))*.42);display:grid;align-content:end;
    transition:none}
}
.numbers .viz.first{margin-top:0;border-top:0;padding-top:0}

/* --- the policy graph: ninety-three lit, nine with a rule --- */
.policy .barcol svg{color:var(--ink)}
.policy .barcol.rules .mk.lit{color:var(--gold-ink)}
.policy .bars .mk path{fill-opacity:.14;transition:transform .5s cubic-bezier(.16,1,.3,1),fill-opacity .45s linear}
.policy.lit .barcol.base .mk.lit path{fill-opacity:1}
.policy.rules .barcol.rules .mk.lit path{fill-opacity:1}
.policy .barcol.rules figcaption b,.policy .barcol.rules figcaption span{color:var(--gold-ink)}

/* --- the desk's last card: tilted, large, the eye led to it --- */
.finale{margin-top:calc(var(--cell)*2);display:grid;grid-template-columns:1fr auto 1fr;align-items:center;
  gap:clamp(18px,3vw,44px)}
.finale .guide{display:flex;gap:12px;justify-content:flex-end;color:var(--gold)}
.finale .guide.r{justify-content:flex-start}
.finale .guide svg{width:18px;height:42px;animation:guideL 1.9s var(--ease) infinite}
.finale .guide.r svg{transform:rotate(180deg);animation-name:guideR}
.finale .guide svg:nth-child(2){animation-delay:.18s}
.finale .guide svg:nth-child(3){animation-delay:.36s}
@keyframes guideL{0%,100%{transform:translateX(0);opacity:.45}50%{transform:translateX(9px);opacity:1}}
@keyframes guideR{0%,100%{transform:rotate(180deg) translateX(0);opacity:.45}50%{transform:rotate(180deg) translateX(9px);opacity:1}}
.fcard{position:relative;width:min(780px,72vw);min-height:clamp(230px,26vw,330px);background:var(--cream);color:var(--ink);
  border-radius:6px;overflow:hidden;box-shadow:0 30px 60px -28px rgba(0,0,0,.95);
  display:grid;grid-template-rows:1fr auto 1fr;transform:rotate(-2.4deg);user-select:none}
.fcard .pip{position:absolute;top:50%;left:50%;width:36%;transform:translate(-50%,-50%);color:var(--ink);opacity:.07}
.fcard .ix{position:absolute;display:grid;justify-items:center;gap:3px;font-family:var(--body);font-weight:600;font-size:1.05rem;line-height:1;color:var(--ink)}
.fcard .ix svg{width:14px;height:14px}
.fcard .ix.ixa{top:16px;left:18px}
.fcard .ix.ixb{bottom:16px;right:18px;transform:rotate(180deg)}
.fcard .cband{background:var(--red);color:var(--white);padding:1.1em 1.6em;position:relative;z-index:2}
.workshopline{margin:0;font-family:var(--title);font-weight:800;letter-spacing:-.035em;line-height:1.02;
  font-size:clamp(1.5rem,3.4vw,2.9rem);color:var(--white);padding-bottom:.08em}
#reveal .ctas{margin-top:calc(var(--cell)*1.5)}
@media (max-width:900px){
  .finale{grid-template-columns:1fr}
  .finale .guide{display:none}
  .fcard{width:100%;transform:rotate(-1.4deg)}
}

/* --- before you book: half a day, seen --- */
.halfday{background:var(--carbon);color:var(--on-carbon);text-align:center}
.halfday .kicker{font-size:.8rem;letter-spacing:.14em;text-transform:uppercase;color:var(--gold)}
.halfday .h2{color:var(--white);margin-top:.35em}
.halfday .lede{margin-inline:auto;color:var(--on-carbon-dim)}
.halfday .rise:last-child{margin-top:calc(var(--cell)*.9)}
.btn.light{border:2px solid var(--gold);color:var(--gold);padding:calc(1.05em - 2px) 1.6em}
.btn.light:hover{background:var(--gold);color:var(--carbon);border-color:var(--gold)}

@media (prefers-reduced-motion:reduce){
  .btn .arr,.finale .guide svg{animation:none!important}
}
'''
wr(os.path.join(SITE, 'styles.css'), c)
print('patched r8')
