import io, os, re

os.chdir(os.path.dirname(os.path.abspath(__file__)))
SITE = '..'


def rd(p): return io.open(p, encoding='utf-8').read()
def wr(p, s): io.open(p, 'w', encoding='utf-8', newline='\n').write(s)
def sub1(s, old, new):
    assert s.count(old) == 1, ('anchor count %d: ' % s.count(old)) + old[:80]
    return s.replace(old, new)


# ============================ app.src.js ====================================
s = rd('app.src.js')

# one flag: the stage (pinned hero, scrubbed morph, fold, expanding card) is
# desktop-only and decided once.  ponytail: crossing 900px needs a reload.
s = sub1(s, "var NS = 'http://www.w3.org/2000/svg';",
            "var NS = 'http://www.w3.org/2000/svg';\nvar STAGE = !reduce && innerWidth > 900;\nif (STAGE) document.documentElement.classList.add('stage');")

# makeGraph: a graph can be driven by the scroll instead of timers
s = sub1(s, '''  new IntersectionObserver(function (es, o) {
    if (!es[0].isIntersecting) return;
    o.disconnect();
    var lastAt = 0;
    cfg.beats.forEach(function (bt) {
      lastAt = Math.max(lastAt, bt.at);
      setTimeout(function () { beatOn(bt.cls); bt.fn(A, B); }, bt.at);
    });
    setTimeout(function () { live = true; root.classList.add('live'); }, lastAt + 900);
  }, { threshold: .35 }).observe(root);
}''', '''  function beatOff(name) {
    root.classList.remove(name);
    var el = root.querySelector('.beat-l[data-beat="' + name + '"]');
    if (el) el.classList.remove('on');
  }
  if (cfg.drive && STAGE) {
    /* the scroll is the clock: each beat has a threshold in [0,1] and can go back */
    return { set: function (r) {
      cfg.beats.forEach(function (bt) {
        var on = r >= bt.r;
        if (on && !bt.on) { bt.on = true; beatOn(bt.cls); bt.fn(A, B); }
        else if (!on && bt.on) { bt.on = false; beatOff(bt.cls); if (bt.undo) bt.undo(A, B); }
      });
      var want = r > .92;
      if (want !== live) { live = want; root.classList.toggle('live', want); }
    } };
  }
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
}''')
s = sub1(s, '''makeGraph({ id: 'policy',
  a: { svg: document.getElementById('polA'), count: 100 }, b: { svg: document.getElementById('polB'), count: 100 },''',
'''var policyG = makeGraph({ id: 'policy', drive: true,
  a: { svg: document.getElementById('polA'), count: 100 }, b: { svg: document.getElementById('polB'), count: 100 },''')
s = sub1(s, '''    { at: 0, cls: 'in', fn: function (A, B) { A.concat(B).forEach(function (c) { c.g.style.transitionDelay = (c.row * 22) + 'ms'; }); } },
    { at: 650, cls: 'lit', fn: function (A) { A.forEach(function (c) { if (c.n < 93) c.p.style.transitionDelay = (c.row * 26 + c.col * 6) + 'ms'; }); } },
    { at: 1700, cls: 'rules', fn: function (A, B) {
      B.slice(0, 9).forEach(function (c, i) { c.p.style.transitionDelay = (i * 70) + 'ms'; morphPath(c.p, 'smooth-diamond', 520, i * 70); });
    } }
  ] });''',
'''    { at: 0, r: .16, cls: 'in', fn: function (A, B) { A.concat(B).forEach(function (c) { c.g.style.transitionDelay = (c.row * 22) + 'ms'; }); } },
    { at: 650, r: .42, cls: 'lit', fn: function (A) { A.forEach(function (c) { if (c.n < 93) c.p.style.transitionDelay = (c.row * 26 + c.col * 6) + 'ms'; }); } },
    { at: 1700, r: .76, cls: 'rules', fn: function (A, B) {
      B.slice(0, 9).forEach(function (c, i) { c.p.style.transitionDelay = (i * 70) + 'ms'; morphPath(c.p, 'smooth-diamond', 520, i * 70); });
    }, undo: function (A, B) { B.slice(0, 9).forEach(function (c) { c.p.setAttribute('d', PATHS.square); }); } }
  ] });''')

# the scene, rewritten
a = s.index('/* ==========================================================================\n   SCENE:')
b = s.rindex('})();')
s = s[:a] + r'''/* ==========================================================================
   THE STAGE: the hero shrinks to the left two fifths and stays; the numbers
   scroll on the right. The 93/9 cards sink into the graph as you scroll.
   The felt table folds down from behind; the half-day card fills the screen
   and lets go. Everything is scrubbed by the scroll: no timers, no snapping.
   ========================================================================== */
(function () {
  if (!STAGE) return;
  var stage = document.getElementById('stage2'), hero = document.getElementById('hero');
  var morph = document.getElementById('morph'), swipe = document.getElementById('swipe');
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
      if (morph) {
        var mr = morph.getBoundingClientRect();
        var r = clamp((HDR - mr.top) / (morph.offsetHeight - ph || 1));
        morph.style.setProperty('--r', r.toFixed(4));
        if (typeof policyG !== 'undefined' && policyG) policyG.set(r);
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
      var e = p < .38 ? p / .38 : p < .62 ? 1 : 1 - (p - .62) / .38;
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

''' + s[b:]
wr('app.src.js', s)


# ============================ shell.html ====================================
h = rd('shell.html')
h = sub1(h, '<div class="scene" id="scene"><div class="scene-pin">\n<section class="hero" id="hero">',
            '<div class="stage" id="stage2">\n<section class="hero" id="hero">')
h = sub1(h, '''    <p class="fine rise">Opens a WhatsApp chat. No form, nothing to buy.</p>
  </div>
</section>''', '''    <p class="fine rise">Opens a WhatsApp chat. No form, nothing to buy.</p>
  </div>
  <div class="cue" aria-hidden="true"><svg viewBox="0 0 64 28"><use href="#chevron-down"/></svg><span>Scroll</span></div>
</section>
<div class="stage-right">''')
old = h[h.index('<!-- ---------------------------- it works. until it doesn\'t. ------------- -->'):h.index('    <div class="viz" id="viz">')]
new = '''<!-- ---------------------------- it works. until it doesn't. ------------- -->
<section class="breaks" id="breaks">
  <div class="morph" id="morph">
    <div class="morph-pin">
      <div class="wrap">
        <h2 class="h2">It works. Until it doesn't.</h2>
        <div class="viz policy first" id="policy">
          <div class="vizgrid">
            <div class="bars" role="img" aria-label="Two bars of a hundred marks each. Ninety-three lit in the first: companies that save time with AI. Nine lit in the second: companies with any AI policy.">
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
      </div>
    </div>
  </div>
</section>

<!-- ---------------------------- numbers, cream --------------------------- -->
<section class="band numbers" id="numbers">
  <div class="wrap">
'''
h = h.replace(old, new)
h = sub1(h, '''    </div>
  </div>
</section>


<!-- ---------------------------- swipe, felt ------------------------------ -->''',
'''    </div>
  </div>
</section>
</div><!-- /stage-right -->
</div><!-- /stage -->


<!-- ---------------------------- swipe, felt ------------------------------ -->''')
wr('shell.html', h)


# ============================ build.py ======================================
bp = rd('build.py')
bp = sub1(bp, '''HALF = """<section class="band halfday" id="halfday-{k}">
  <div class="wrap">
    <p class="kicker rise">Before you book</p>
    <h2 class="h2 rise">See what half a day looks like.</h2>
    <p class="lede rise">Seven moments, your own work on the table, and a one-page plan the week after. Two minutes to read.</p>
    <p class="rise"><a class="btn go arrow light" href="/workshop/">See the workshop<svg class="arr" viewBox="0 0 64 28" aria-hidden="true"><use href="#arrow"/></svg></a></p>
  </div>
</section>
"""''', '''HALF = """<div class="hstage" id="hstage-{k}"><div class="hpin">
<section class="band halfday" id="halfday-{k}">
  <div class="wrap">
    <h2 class="h2 rise">See what half a day looks like.</h2>
    <p class="lede rise">Seven moments, your own work on the table, and a one-page plan the week after. Two minutes to read.</p>
    <p class="rise gorow"><a class="btn go arrow light" href="/workshop/">See the workshop<svg class="arr" viewBox="0 0 64 28" aria-hidden="true"><use href="#arrow"/></svg></a></p>
    <div class="hcue" aria-hidden="true"><svg viewBox="0 0 64 28"><use href="#chevron-down"/></svg><span>Keep scrolling to book with us</span></div>
  </div>
</section>
</div></div>
"""''')
wr('build.py', bp)


# ============================ styles.css ====================================
c = rd(os.path.join(SITE, 'styles.css'))
a = c.index('/* --- the scene: hero condenses left, the next screen rises from the right --- */')
b = c.index('.numbers .viz.first{margin-top:0;border-top:0;padding-top:0}')
c = c[:a] + r'''/* --- the stage: hero pinned left, numbers on the right, cards into graph --- */
.cue{position:absolute;left:50%;bottom:22px;transform:translateX(-50%);z-index:3;display:grid;justify-items:center;gap:6px;
  color:var(--gold);font-size:.7rem;letter-spacing:.18em;text-transform:uppercase;pointer-events:none}
.cue svg{width:38px;height:17px;animation:cue 1.9s var(--ease) infinite}
@keyframes cue{0%,100%{transform:translateY(0);opacity:.55}50%{transform:translateY(7px);opacity:1}}
.hero.armed .cue,.hero.condensed .cue{display:none}
.halfday .gorow{margin-top:calc(var(--cell)*.9)}
.halfday .h2{margin-top:0}
.stage{--q:0;--f:0;position:relative}
.breaks{background:var(--cream);color:var(--ink);padding:calc(var(--cell)*2.6) 0 0}
.breaks .h2{color:var(--ink)}
.policy{margin-top:calc(var(--cell)*1.4)!important;border-top:0!important;padding-top:0!important}
.policy .bars{position:relative}
.policy .pair{margin:0;max-width:none;grid-column:1/-1;order:-1;margin-bottom:calc(var(--cell)*1.2)}
.hcue{display:none}
html.stage .stage{display:grid;grid-template-columns:40% 60%;overflow-x:clip;align-items:start}
html.stage .hero{grid-column:1;position:sticky;top:var(--hdr);height:calc(100svh - var(--hdr));min-height:0;
  width:calc(100% + (1 - var(--q))*150%);z-index:2;
  transform:translateX(calc(var(--f)*-110%));will-change:transform,width}
html.stage .hero .wrap{padding:0}
html.stage .hero h1{font-size:calc(clamp(2.55rem,7.2vw,6.6rem)*(1 - var(--q)*.45))}
html.stage .hero .sub,html.stage .hero .fine{opacity:calc(1 - var(--q)*2.2);max-height:calc((1 - var(--q))*9em);overflow:hidden;
  margin-top:calc(var(--cell)*.5*(1 - var(--q)))}
html.stage .hero .ctas{margin-top:calc(var(--cell)*.9)}
html.stage .stage-right{grid-column:2;background:var(--cream);padding-top:calc((100svh - var(--hdr))*1.25);
  transform:translateX(calc((1 - var(--q))*40%));opacity:calc(var(--q)*1.5 + .1)}
html.stage .morph{height:calc((100svh - var(--hdr))*2.3);--r:0}
html.stage .morph-pin{position:sticky;top:var(--hdr);height:calc(100svh - var(--hdr));display:grid;align-content:center}
html.stage .breaks{padding:0}
html.stage .policy .vizgrid{grid-template-columns:minmax(0,auto) minmax(0,1fr);gap:clamp(24px,3vw,48px);align-items:end}
html.stage .policy .bars{grid-template-columns:repeat(2,minmax(0,200px));gap:clamp(18px,2.6vw,40px)}
html.stage .policy .barcol.base{grid-area:1/1}
html.stage .policy .barcol.rules{grid-area:1/2}
html.stage .policy .barcol{opacity:calc(var(--r)*3 - .5)}
html.stage .policy .pair{grid-area:1/1/2/3;order:0;margin:0;align-self:end;z-index:2;pointer-events:none;
  transform-origin:50% 100%;transform:scale(calc(1 - var(--r)*.55)) translateY(calc(var(--r)*-8%));opacity:calc(1.15 - var(--r)*2.1)}
html.stage .policy .pair>div{padding:calc(var(--cell)*.8) calc(var(--cell)*.7) calc(var(--cell)*.9)}
html.stage .policy .pair .fignum{font-size:clamp(2.6rem,5vw,4.4rem)}
html.stage .policy .pair p{font-size:.95rem;max-width:none}
html.stage .stage-right .viz{margin-top:0}
html.stage .stage-right .vizgrid{gap:clamp(24px,3vw,48px)}
html.stage #viz .vizgrid{grid-template-columns:minmax(0,1fr)}
html.stage #viz .bars{grid-template-columns:repeat(2,minmax(0,220px))}
html.stage .numbers{padding-top:calc(var(--cell)*2.2)}
/* the felt table folds down from behind the cream */
html.stage .swipe{position:relative;transform-origin:50% 0;
  transform:perspective(1300px) rotateX(calc((1 - var(--f))*68deg));opacity:calc(var(--f)*1.3 + .06)}
html.stage .swipe.flat{transform:none;opacity:1}
html.stage .swipe::before{content:"";position:absolute;inset:0;z-index:5;pointer-events:none;
  background:linear-gradient(to bottom,rgba(0,0,0,.75),rgba(0,0,0,0) 45%);opacity:calc(1 - var(--f))}
/* the half-day card fills the screen, then lets go */
html.stage .hstage{height:calc((100svh - var(--hdr))*2.6);background:var(--cream);--e:0}
html.stage .hpin{position:sticky;top:var(--hdr);height:calc(100svh - var(--hdr));display:grid;place-items:center;overflow:hidden}
html.stage .halfday{width:calc(72% + var(--e)*28%);height:calc(58% + var(--e)*42%);border-radius:calc((1 - var(--e))*10px);
  display:grid;align-content:center;padding:0;box-shadow:0 40px 80px -40px rgba(0,0,0,.6)}
html.stage .hcue{display:grid;justify-items:center;gap:8px;margin-top:calc(var(--cell)*1.4);
  color:var(--gold);font-size:.74rem;letter-spacing:.16em;text-transform:uppercase;opacity:calc(var(--e)*8 - 7)}
html.stage .hcue svg{width:38px;height:17px;animation:cue 1.9s var(--ease) infinite}
''' + c[b:]
c = sub1(c, '''.js .rise{opacity:0;transform:translateY(18px);
  transition:opacity .8s linear,transform .8s var(--ease)}''', '''.js .rise{opacity:0;transform-origin:50% 0;transform:perspective(900px) rotateX(-58deg) translateY(10px);
  transition:opacity .6s linear,transform .9s cubic-bezier(.16,1,.3,1)}''')
c = sub1(c, '  .btn .arr,.finale .guide svg{animation:none!important}', '  .btn .arr,.finale .guide svg,.cue svg,.hcue svg{animation:none!important}')
wr(os.path.join(SITE, 'styles.css'), c)
print('patched r9b')
