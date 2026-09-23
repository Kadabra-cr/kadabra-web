"""Round 19: the marks of '¿Jugar?' jump into '¡Jugar!'; a side-panel cue on the
staged hero; LinkedIn in the footer; a smoke the hand really clears, with no
cut edges and no blur; a house-rules sheet; the policy graph tells 93 -> 84 red
+ 9 gold in percentages; the taught graph speaks of two groups, with less text."""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..')
p = os.path.join(ROOT, 'src', 'app.src.js')
s = open(p, encoding='utf-8').read()


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:100])
    s = s.replace(a, b)


# ---- the ask: only the marks change, and they jump ----
rep("""  askEl.innerHTML = '<button type="button" class="yes"><span>@@t.game.ask@@</span><span aria-hidden="true">@@t.game.ask.hover@@</span></button>' +""",
    """  /* '¿Jugar?' becomes '¡Jugar!' under the hand: the word stays put, only the
     marks swap, at once, and jump. Other copy falls back to swapping the whole label. */
  function askLabel(a, b) {
    var re = /^([¿¡]*)([\\s\\S]*?)([?!]*)$/, x = a.match(re), y = b.match(re);
    function pm(u, v) { return u || v ? '<span class="pm"><i>' + u + '</i><i class="alt" aria-hidden="true">' + v + '</i></span>' : ''; }
    if (x[2] !== y[2]) return '<span class="pm whole"><i>' + a + '</i><i class="alt" aria-hidden="true">' + b + '</i></span>';
    return pm(x[1], y[1]) + '<span>' + x[2] + '</span>' + pm(x[3], y[3]);
  }
  askEl.innerHTML = '<button type="button" class="yes">' + askLabel('@@t.game.ask@@', '@@t.game.ask.hover@@') + '</button>' +""")

# ---- the smoke: the hand is a real repellent, the edges fade, no blur ----
rep("""      var defs = document.createElementNS(NS, 'defs');
      if (!CALM) defs.innerHTML = '<filter id="smokeblur" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="2.6"/></filter>';
      svg.appendChild(defs);
""", "")
rep("""      if (!CALM) cloud.setAttribute('filter', 'url(#smokeblur)');
      svg.appendChild(cloud);""", """      svg.appendChild(cloud);""")
rep("""          o: CALM ? rnd(.08, .2) : rnd(.16, .34), rot""", """          o: CALM ? rnd(.08, .2) : rnd(.1, .26), rot""")
rep("""        var hx = hand.x, hy = hand.y, push = 520;""", """        var hx = hand.x, hy = hand.y, push = 3400, reach = 118;""")
rep("""          push = 240;                 /* the ghost hand */""", """          push = 380; reach = 80;     /* the ghost hand */""")
rep("""          if (d < 78) { var f = (1 - d / 78) * push * dt; q.ox += dx / d * f; q.oy += dy / d * f; }
          q.ox -= q.ox * Math.min(1, .9 * dt); q.oy -= q.oy * Math.min(1, .9 * dt);   /* closes back, slowly */""",
    """          /* the hand throws the smoke well out of its way; it drifts back only slowly */
          if (d < reach) { var f = (1 - d / reach) * push * dt; q.ox += dx / d * f; q.oy += dy / d * f; }
          q.ox -= q.ox * Math.min(1, .2 * dt); q.oy -= q.oy * Math.min(1, .2 * dt);""")
rep("""          var edge = Math.min(1, (q.hy - 18) / 40, (205 - q.hy) / 30);""",
    """          /* every puff fades out before it could touch the drawing's border */
          var half = q.s * .72;
          var edge = Math.min(1, (q.hy - 18) / 40, (205 - q.hy) / 30,
            (x - half) / 34, (320 - half - x) / 34, (y - half) / 30, (220 - half - y) / 30);""")
rep("""        clear += (want - clear) * Math.min(1, 2.4 * dt);
        symG.setAttribute('opacity', (.12 + clear * .88).toFixed(3));
        symP.setAttribute('d', mix('smooth-spade', easeOut(clear)));
        if (clear > .85) symG.classList.add('glow'); else symG.classList.remove('glow');""",
    """        clear += (want - clear) * Math.min(1, 5 * dt);
        symG.setAttribute('opacity', (.12 + clear * .88).toFixed(3));
        /* the spade is whole early; its glow comes up gradually, never at once */
        symP.setAttribute('d', mix('smooth-spade', easeOut(Math.min(1, clear * 1.7))));
        var gl = Math.max(0, Math.min(1, (clear - .45) / .55)); gl = gl * gl * (3 - 2 * gl);
        if (Math.abs(gl - glowAt) > .01 || (gl === 0) !== (glowAt === 0)) {
          glowAt = gl;
          symG.style.filter = gl ? 'drop-shadow(0 0 ' + (11 * gl).toFixed(1) + 'px rgba(201,162,39,' + (.6 * gl).toFixed(3) + '))' : '';
        }""")
rep("""      var hand = { x: -1e3, y: -1e3, at: -1e4 }, clear = 0, smokeOn = false, last = 0;""",
    """      var hand = { x: -1e3, y: -1e3, at: -1e4 }, clear = 0, smokeOn = false, last = 0, glowAt = 0;""")

# ---- house rules: a sheet, three suited rules, everyone's signature, a seal ----
rep("""    } else if (kind === 'break') {""", """    } else if (kind === 'rules') {
      var rk = ['smooth-spade', 'smooth-heart', 'smooth-diamond'];
      var rps = [].map.call(svg.querySelectorAll('.rmark path'), function (rp) { rp.setAttribute('d', PATHS.square); return rp; });
      var seal = svg.querySelector('.seal path');
      if (seal) seal.setAttribute('d', PATHS.square);
      once(m, function (on) {
        if (!on) return;
        rps.forEach(function (rp, i) { morphPath(rp, rk[i], 620, 250 + i * 330); });
        if (seal) morphPath(seal, 'smooth-club', 700, 1900);
      });
    } else if (kind === 'break') {""")

# ---- the policy graph: the same 93, 84 red without a rule, 9 gold with one ----
rep("""/* it works, until it doesn't: 93 of 100 save time with AI, 9 of 100 have a rule */
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
  ] });""", """/* it works, until it doesn't: 93% save time with AI. The second bar is those
   same 93: 84% use it without a rule (red), and at the bottom, the 9% with one (gold) */
var policyG = makeGraph({ id: 'policy', drive: true,
  a: { svg: document.getElementById('polA'), count: 100 }, b: { svg: document.getElementById('polB'), count: 93 },
  setup: function (A, B) {
    A.forEach(function (c) { c.fo = .14; if (c.n < 93) { c.g.classList.add('lit'); c.fo = 1; } });
    B.forEach(function (c) { c.fo = 1; c.g.classList.add('lit', c.n < 9 ? 'gold' : 'risk'); if (c.n < 9) c.strong = true; });
  },
  still: function (A, B) { B.slice(0, 9).forEach(function (c) { c.p.setAttribute('d', mix('smooth-diamond', 1)); }); },
  beats: [
    { at: 150, cls: 'in', fn: function (A, B) { A.concat(B).forEach(function (c) { c.g.style.transitionDelay = (c.row * 9) + 'ms'; }); } },
    { at: 400, cls: 'lit', fn: function (A, B) { A.concat(B).forEach(function (c) { if (c.n < 93) c.p.style.transitionDelay = (c.row * 9 + c.col * 3) + 'ms'; }); } },
    { at: 900, cls: 'risk', fn: function (A, B) { B.slice(9).forEach(function (c) { c.g.style.transitionDelay = ((c.row - 1) * 30 + c.col * 4) + 'ms'; }); } },
    { at: 1450, cls: 'rules', fn: function (A, B) {
      B.slice(0, 9).forEach(function (c, i) { morphPath(c.p, 'smooth-diamond', 420, i * 40); });
    } }
  ] });""")
rep("""/* taught first: the same hundred people, twice. Taught, they do 34% more */""",
    """/* two groups: the one taught first does 34% more */""")

open(p, 'w', encoding='utf-8', newline='\n').write(s)
a = s.index('/* ==========================================================================\n   THE FIELD')
b = s.index('/* ==========================================================================\n   GRAPHS')
open(os.path.join(ROOT, 'src', 'field_r8.js'), 'w', encoding='utf-8', newline='\n').write(s[a:b].rstrip() + '\n')

# ---- markup ----
h = os.path.join(ROOT, 'src', 'shell.html')
t = open(h, encoding='utf-8').read()


def hrep(a, b):
    global t
    assert t.count(a) == 1, a[:90]
    t = t.replace(a, b)


hrep("""  <div class="cue" aria-hidden="true"><svg viewBox="0 0 64 28"><use href="#chevron-down"/></svg><span>@@t.hero.cue@@</span></div>""",
     """  <div class="cue" aria-hidden="true"><svg viewBox="0 0 64 28"><use href="#chevron-down"/></svg><span>@@t.hero.cue@@</span></div>
  <div class="side-cue" aria-hidden="true"><svg viewBox="0 0 28 64"><use href="#chevron"/></svg><i></i></div>""")
hrep("""          <li>@@t.foot.linkedin@@ @@t.foot.linkedin.value@@</li>""",
     """          <li>@@t.foot.linkedin@@ <a href="@@t.foot.linkedin.link@@" rel="noopener">@@t.foot.linkedin.value@@</a></li>""")
hrep("""      <div class="m-vis vis-rules">
        <span class="rule mid drift" aria-hidden="true"></span>
        <span class="rule mid drift" aria-hidden="true"></span>
        <span class="rule mid drift" aria-hidden="true"></span>
      </div>""", """      <div class="m-vis"><svg class="vis-rules" viewBox="0 0 320 220" aria-hidden="true">
        <rect class="sheet" x="62" y="14" width="196" height="192" rx="5"/>
        <rect class="ttl" x="84" y="36" width="78" height="9" rx="1"/>
        <g class="rrow"><g class="rmark" transform="translate(94 78) scale(.2) translate(-50 -50)"><path/></g><rect class="ln" x="114" y="74" width="118" height="7" rx="1"/></g>
        <g class="rrow"><g class="rmark red" transform="translate(94 110) scale(.2) translate(-50 -50)"><path/></g><rect class="ln" x="114" y="106" width="96" height="7" rx="1"/></g>
        <g class="rrow"><g class="rmark red" transform="translate(94 142) scale(.2) translate(-50 -50)"><path/></g><rect class="ln" x="114" y="138" width="108" height="7" rx="1"/></g>
        <path class="sig" pathLength="1" d="M84 184c6-9 10-10 11-3s4 7 9-2 7-6 8 1 5 5 10-3"/>
        <path class="sig" pathLength="1" d="M136 186c4-10 9-12 10-4s2 6 7-1c3-4 6-3 7 2s5 4 11-4"/>
        <path class="sig" pathLength="1" d="M190 183c7-8 10-8 10-1s5 6 9-1 6-6 7 0"/>
        <g class="seal"><circle cx="236" cy="42" r="18"/><g transform="translate(236 42) scale(.19) translate(-50 -50)"><path/></g></g>
      </svg></div>""")
# the policy graph: B's caption carries both parts; the ledger drops the hundred
hrep("""                <figcaption><b>@@t.policy.capB.fig@@</b><span>@@t.policy.capB.label@@</span></figcaption>""",
     """                <figcaption><b>@@t.policy.capB.fig@@</b><span>@@t.policy.capB.label@@</span><span class="gold">@@t.policy.capB.gold@@</span></figcaption>""")
hrep("""                <p class="beat-l" data-beat="in"><b>@@t.policy.beat1.fig@@</b><span>@@t.policy.beat1@@</span></p>
                <p class="beat-l" data-beat="lit"><b>@@t.policy.beat2.fig@@</b><span>@@t.policy.beat2@@</span></p>
                <p class="beat-l" data-beat="rules"><b>@@t.policy.beat3.fig@@</b><span>@@t.policy.beat3@@</span></p>
                <p class="beat-l risk" data-beat="rules"><b>@@t.policy.aside.fig@@</b><span>@@t.policy.aside@@</span></p>""",
     """                <p class="beat-l" data-beat="lit"><b>@@t.policy.beat1.fig@@</b><span>@@t.policy.beat1@@</span></p>
                <p class="beat-l risk" data-beat="risk"><b>@@t.policy.beat2.fig@@</b><span>@@t.policy.beat2@@</span></p>
                <p class="beat-l gold" data-beat="rules"><b>@@t.policy.beat3.fig@@</b><span>@@t.policy.beat3@@</span></p>""")
# the taught graph: the beats tell it, the lede goes
hrep("""      <p class="lede">@@t.viz.lede@@</p>
""", "")
open(h, 'w', encoding='utf-8', newline='\n').write(t)

# ---- copy ----
cp = os.path.join(ROOT, 'src', 'copy.es.md')
t = open(cp, encoding='utf-8').read()


def crep(a, b):
    global t
    assert t.count(a) == 1, a
    t = t.replace(a, b)


def setkey(k, v):
    global t
    lines = t.split('\n')
    hit = [i for i, l in enumerate(lines) if l.startswith(k + ':')]
    assert len(hit) == 1, k
    lines[hit[0]] = k + ': ' + v
    t = '\n'.join(lines)


def dropkey(k):
    global t
    lines = t.split('\n')
    t = '\n'.join(l for l in lines if not l.startswith(k + ':'))


setkey('policy.aria', 'Dos barras. En la primera, 93 de cada 100 empresas ahorran tiempo con IA. La segunda son esas mismas 93, con 84 en rojo que la usan sin reglas y 9 en dorado que tienen una política de IA.')
setkey('policy.capB.fig', '84%')
setkey('policy.capB.label', 'La usan sin reglas')
crep('policy.capB.label: La usan sin reglas\n', 'policy.capB.label: La usan sin reglas\npolicy.capB.gold: 9% con política de IA\n')
setkey('policy.beat1.fig', '93%')
setkey('policy.beat1', 'de las empresas tecnológicas del país ya ahorran tiempo con IA.')
setkey('policy.beat2.fig', '84%')
setkey('policy.beat2', 'la usan sin ninguna regla. Están tentando la suerte.')
setkey('policy.beat3.fig', '9%')
setkey('policy.beat3', 'tienen una política de IA. Ahí es donde queremos ver a su empresa.')
dropkey('policy.aside.fig')
dropkey('policy.aside')
dropkey('viz.lede')
setkey('viz.beat1', 'Dos grupos hacen el mismo trabajo.')
setkey('viz.beat2', 'A uno se le enseña primero a usar IA.')
setkey('viz.beat3', 'Ese grupo aprendido logra 1/3 más de trabajo.')
setkey('foot.linkedin.value', 'kadabracr')
crep('foot.linkedin.value: kadabracr\n', 'foot.linkedin.value: kadabracr\nfoot.linkedin.link: https://www.linkedin.com/company/kadabracr\n')
open(cp, 'w', encoding='utf-8', newline='\n').write(t)

# ---- CSS ----
c = os.path.join(ROOT, 'site', 'styles.css')
t = open(c, encoding='utf-8').read()


def srep(a, b):
    global t
    assert t.count(a) == 1, a[:90]
    t = t.replace(a, b)


srep(""".ask .yes{font:inherit;font-size:1rem;font-weight:700;background:var(--gold);color:var(--carbon);border:0;border-radius:999px;
  min-height:40px;padding:.55em 1.3em;cursor:pointer;display:grid;transition:background .2s var(--ease)}
/* the two words share one cell, so the pill never changes width */
.ask .yes span{grid-area:1/1;transition:opacity .18s linear,translate .3s cubic-bezier(.16,1,.3,1)}
.ask .yes span+span{opacity:0;translate:0 5px}
.ask .yes:is(:hover,:focus-visible) span:first-child{opacity:0;translate:0 -5px}
.ask .yes:is(:hover,:focus-visible) span+span{opacity:1;translate:0 0}""",
""".ask .yes{font:inherit;font-size:1rem;font-weight:700;background:var(--gold);color:var(--carbon);border:0;border-radius:999px;
  min-height:40px;padding:.55em 1.3em;cursor:pointer;display:inline-flex;align-items:baseline;justify-content:center;
  transition:background .2s var(--ease)}
/* the marks swap at once (no fade) and the new ones jump, then keep growing a touch */
.ask .yes .pm{display:inline-grid}
.ask .yes .pm i{grid-area:1/1;font-style:normal;display:inline-block;transform-origin:50% 85%}
.ask .yes .pm .alt,.ask .yes:is(:hover,:focus-visible) .pm i:first-child{visibility:hidden}
.ask .yes:is(:hover,:focus-visible) .pm .alt{visibility:visible;animation:markJump .9s cubic-bezier(.2,.9,.3,1) both}
@keyframes markJump{0%{transform:translateY(0) scale(1)}18%{transform:translateY(-5px) scale(1.16)}100%{transform:translateY(-1px) scale(1.32)}}
.ask .yes .pm.whole .alt{transform-origin:50% 60%}""")
srep(".hero.armed .cue,.hero.condensed .cue{display:none}",
     """.hero.armed .cue,.hero.condensed .cue{display:none}
/* the staged hero scrolls a panel in from the right, so the cue says that: the
   panel's cream edge peeks at the right border, a chevron nudges left */
.side-cue{display:none}
html.staged .cue{display:none}
html.staged .side-cue{position:absolute;right:0;top:50%;z-index:3;display:flex;align-items:center;gap:14px;
  transform:translateY(-50%);pointer-events:none;opacity:calc(1 - var(--q)*5)}
html.staged .side-cue svg{width:10px;height:22px;color:var(--gold);transform:scaleX(-1);animation:sideCue 2.4s var(--ease) infinite}
html.staged .side-cue i{display:block;width:5px;height:clamp(90px,16svh,150px);background:var(--cream);border-radius:3px 0 0 3px;
  opacity:.9;animation:sidePeek 2.4s var(--ease) infinite}
@keyframes sideCue{0%,100%{translate:0 0;opacity:.45}50%{translate:-7px 0;opacity:1}}
@keyframes sidePeek{0%,100%{width:5px}50%{width:9px}}
html.staged .hero.armed .side-cue,html.staged .hero.condensed .side-cue{display:none}""")
srep("  .btn .arr,.finale .guide svg,.cue svg,.hcue svg{animation:none!important}",
     "  .btn .arr,.finale .guide svg,.cue svg,.hcue svg,.side-cue svg,.side-cue i,.ask .yes .pm .alt{animation:none!important}")
# house rules sheet
srep(""".vis-rules{display:grid;gap:clamp(14px,2vw,24px)}""",
""".vis-rules .sheet{fill:none;stroke:currentColor;stroke-width:3;opacity:.5}
.vis-rules .ttl,.vis-rules .ln{fill:currentColor;opacity:.8;transform-box:fill-box;transform-origin:0 50%;transition:transform .7s var(--ease)}
.vis-rules .ttl{opacity:.95}
.vis-rules .rmark path{fill:currentColor}
.vis-rules .rmark.red path{fill:#C24A5A}
.vis-rules .sig{fill:none;stroke:currentColor;stroke-width:2.2;stroke-linecap:round;stroke-linejoin:round;opacity:.6;
  stroke-dasharray:1;stroke-dashoffset:1;transition:stroke-dashoffset .9s var(--ease)}
.vis-rules .seal circle{fill:none;stroke:var(--gold);stroke-width:2.5}
.vis-rules .seal path{fill:var(--gold)}
.vis-rules .seal{transform-box:fill-box;transform-origin:50% 50%;opacity:0;transform:scale(1.5) rotate(-14deg);
  transition:opacity .35s linear 1.9s,transform .6s cubic-bezier(.2,1.5,.4,1) 1.9s}
.js .vis-rules .ttl,.js .vis-rules .ln{transform:scaleX(0)}
.js .moment.on .vis-rules .ttl,.js .moment.on .vis-rules .ln{transform:scaleX(1)}
.moment.on .vis-rules .rrow:nth-of-type(1) .ln{transition-delay:.35s}
.moment.on .vis-rules .rrow:nth-of-type(2) .ln{transition-delay:.68s}
.moment.on .vis-rules .rrow:nth-of-type(3) .ln{transition-delay:1.01s}
.moment.on .vis-rules .sig{stroke-dashoffset:0}
.moment.on .vis-rules .sig:nth-of-type(1){transition-delay:1.3s}
.moment.on .vis-rules .sig:nth-of-type(2){transition-delay:1.5s}
.moment.on .vis-rules .sig:nth-of-type(3){transition-delay:1.7s}
.moment.on .vis-rules .seal{opacity:1;transform:rotate(-10deg)}
@media (prefers-reduced-motion:reduce){.vis-rules .ttl,.vis-rules .ln{transform:none!important}.vis-rules .sig{stroke-dashoffset:0!important}
  .vis-rules .seal{opacity:1!important;transform:rotate(-10deg)!important}}""")
# the policy graph: red for the 84, gold for the 9, the ledger in three
srep(""".policy .barcol.rules .mk.lit{color:var(--gold-ink)}
.policy .bars .mk path{fill-opacity:.14;transition:transform .5s cubic-bezier(.16,1,.3,1),fill-opacity .45s linear}
.policy.lit .barcol.base .mk.lit path{fill-opacity:1}
.policy.rules .barcol.rules .mk.lit path{fill-opacity:1}""",
""".policy .bars .mk{transition:opacity .38s linear,color .5s linear}
.policy .bars .mk path{fill-opacity:.14;transition:transform .5s cubic-bezier(.16,1,.3,1),fill-opacity .45s linear}
.policy.lit .bars .mk.lit path{fill-opacity:1}
.policy.risk .barcol.rules .mk.risk{color:var(--red)}
.policy.rules .barcol.rules .mk.gold{color:var(--gold-ink)}
.policy .barcol.rules figcaption b{color:var(--red)}
.policy .barcol.rules figcaption span:not(.gold){color:var(--red)}
.policy .barcol.rules figcaption .gold{color:var(--gold-ink);font-weight:700;margin-top:.35em}""")
srep(".policy .barcol.rules figcaption b,.policy .barcol.rules figcaption span{color:var(--gold-ink)}", "")
srep(".ledger .beat-l[data-beat=in]{color:var(--ink-dim)}", ".ledger .beat-l.gold{color:var(--gold-ink)}")
open(c, 'w', encoding='utf-8', newline='\n').write(t)
print('ok')
