import io, os, re
os.chdir(os.path.dirname(os.path.abspath(__file__)))
S = '..'

def cut(s, start_marker, end_marker, new, include_end=False):
    a = s.index(start_marker); b = s.index(end_marker, a)
    if include_end: b += len(end_marker)
    return s[:a] + new + s[b:]

# =========================== app.src.js ===========================
js = io.open('app.src.js', encoding='utf-8').read()

# --- hero anchors grow toward the pointer -------------------------------
js = js.replace("      s: size, depth: size / 40,            /* bigger = closer = more parallax */",
                "      s: size, sc: 1, depth: size / 40,     /* bigger = closer = more parallax */")
js = js.replace("      ') rotate(' + m.rot.toFixed(1) + ') scale(' + (m.s / 100).toFixed(4) + ') translate(-50 -50)');\n  }\n  marks.forEach(function (m) { m.g.setAttribute('opacity', m.o.toFixed(3)); place(m); });",
                "      ') rotate(' + m.rot.toFixed(1) + ') scale(' + (m.s * m.sc / 100).toFixed(4) + ') translate(-50 -50)');\n  }\n  marks.forEach(function (m) { m.g.setAttribute('opacity', m.o.toFixed(3)); place(m); });")
js = js.replace("      if (m.anchor) m.t = 1;                 /* a suit that never goes back */",
                "      if (m.anchor) {                        /* a suit that never goes back: it grows toward the hand */\n        m.t = 1;\n        var want = ptr.on && dp < R * 1.4 ? 1 + .75 * (1 - dp / (R * 1.4)) : 1;\n        m.sc += (want - m.sc) * Math.min(1, 5 * dt);\n      }")
js = js.replace("document.querySelectorAll('.rise,.viz')", "document.querySelectorAll('.rise')")
js = js.replace("  w: 1600, h: 900, n: 60, nm: 25, base: .20, peak: .84, r: 260, scroll: true,",
                "  w: 1600, h: 900, n: 60, nm: 25, base: .20, peak: .84, r: 260, scroll: true, anchors: 4,")
# anchors in the hero start a little dimmer than in the close field
js = js.replace("      base: anchor ? BASE * 1.25 : BASE, peak: PEAK, t: anchor ? 1 : 0,",
                "      base: anchor ? Math.min(.62, BASE * 2.2) : BASE, peak: PEAK, t: anchor ? 1 : 0,")
js = js.replace("      o: spare ? 0 : (anchor ? BASE * 1.25 : BASE),",
                "      o: spare ? 0 : (anchor ? Math.min(.62, BASE * 2.2) : BASE),")

# --- numbers: two bars of marks -------------------------------------------
a = js.index('   NUMBERS: 47 of 100 were taught')
a = js.rindex('/* ====', 0, a)
b = js.index('   SWIPE: "Can AI take this?"')
b = js.rindex('/* ====', 0, b)
js = js[:a] + r'''/* ==========================================================================
   NUMBERS: the same hundred people, twice. Taught first, they do 34% more.
   ========================================================================== */
(function () {
  var viz = document.getElementById('viz');
  if (!viz) return;
  var COLS = 10, CW = 20, CH = 21, SZ = 13, H = 14 * CH;
  function bar(svg, count, key) {
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
      cells.push({ g: g, p: p, row: row, n: n });
    }
    return cells;
  }
  var A = bar(document.getElementById('barA'), 100, null);
  var B = bar(document.getElementById('barB'), 134, 'smooth-spade');
  B.forEach(function (c) { if (c.n >= 100) c.g.classList.add('extra'); });
  if (reduce) {
    viz.classList.add('in', 'taught', 'more');
    B.forEach(function (c) { c.p.setAttribute('d', mix('smooth-spade', 1)); });
    return;
  }
  new IntersectionObserver(function (es, o) {
    if (!es[0].isIntersecting) return;
    o.disconnect();
    /* beat 1: the same hundred people, twice */
    A.concat(B.slice(0, 100)).forEach(function (c) { c.g.style.transitionDelay = (c.row * 55) + 'ms'; });
    viz.classList.add('in');
    /* beat 2: one group is taught: the squares become spades, bottom up */
    setTimeout(function () {
      viz.classList.add('taught');
      B.slice(0, 100).forEach(function (c) { morphPath(c.p, 'smooth-spade', 520, c.row * 60 + (c.n % COLS) * 12); });
    }, 1300);
    /* beat 3: and gets a third more done */
    setTimeout(function () {
      B.slice(100).forEach(function (c, i) {
        c.p.setAttribute('d', mix('smooth-spade', 1));
        c.g.style.transitionDelay = (i * 22) + 'ms';
      });
      viz.classList.add('more');
    }, 2900);
  }, { threshold: .35 }).observe(viz);
})();

''' + js[b:]

# --- swipe: one card, one element, all the way to the desk ----------------
a = js.index('  function mini(c, dir) {')
b = js.index('  var rz = 0;')
js = js[:a] + r'''  /* where the k-th card on a pile rests, relative to the deck */
  function pileSpot(dir, k) {
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
    el.dataset.fn = c.fn; el.dataset.dir = side; el.dataset.k = k;
    onPile[side].push(el);
    (dir > 0 ? pileR : pileL).classList.add('hot');
    el.style.zIndex = 40 + idx;
    el.style.pointerEvents = 'none';
    el.style.transition = reduce ? 'none' : 'transform .68s cubic-bezier(.16,1,.3,1)';
    el.style.transform = pileSpot(dir, k);
    el.classList.add('piled');
    idx++;
    restack();
    if (idx >= CARDS.length) { hint.textContent = ''; setTimeout(finish, reduce ? 0 : 1500); }
    else setHint();
  }

  /* --- the desk: the piles spread into two fanned columns ------------------ */
  var stage = document.getElementById('stage'), heads = document.getElementById('heads');
  var SLOT = { w: 0, h: 0, step: 0 };
  function slotFor(el, col, k) {
    var s = document.createElement('div');
    s.className = 'slot'; s.dataset.fn = el.dataset.fn; s.dataset.dir = el.dataset.dir;
    s.style.width = SLOT.w + 'px'; s.style.height = SLOT.h + 'px';
    s.style.top = (k * SLOT.step + 34) + 'px'; s.style.zIndex = 10 + k;
    col.appendChild(s);
    return s;
  }
  function finish() {
    if (done) return;
    done = true;
    stopNudge();
    var dr = deck.getBoundingClientRect();
    SLOT.w = Math.round(dr.width * .72); SLOT.h = Math.round(dr.height * .72); SLOT.step = Math.round(SLOT.h * .3);
    var sc = SLOT.w / dr.width;
    minis = [];
    notes.innerHTML = CARDS.map(function (c) {
      return '<div class="note" data-fn="' + c.fn + '" tabindex="0"><b aria-hidden="true">' + c.fn + '</b><div>' +
        '<p class="q">' + c.q + '</p><p class="a">' + c.a + '</p></div></div>';
    }).join('');
    /* first: where every card is on its pile */
    var first = els.map(function (el) { return el.getBoundingClientRect(); });
    /* swap the boards in place: same grid cell, nothing above moves */
    heads.classList.add('flip'); stage.classList.add('flip');
    btns.hidden = true; hint.hidden = true;
    colL.style.height = colR.style.height = (34 + SLOT.h + (Math.max(onPile.l.length, onPile.r.length) - 1) * SLOT.step) + 'px';
    ['l', 'r'].forEach(function (side) {
      onPile[side].forEach(function (el, k) {
        var s = slotFor(el, side === 'r' ? colR : colL, k);
        s.appendChild(el);
        el.classList.remove('piled'); el.classList.add('desk');
        el.style.zIndex = ''; el.style.pointerEvents = '';
        el.style.width = dr.width + 'px'; el.style.height = dr.height + 'px';
        var fm = document.createElement('span'); fm.className = 'fnmark'; fm.textContent = el.dataset.fn; el.appendChild(fm);
        el.style.transition = 'none';
        el.style.transform = 'scale(' + sc + ')';
        minis.push(s);
      });
    });
    /* last: where they are now, then play from first to last */
    els.forEach(function (el, i) {
      var l = el.getBoundingClientRect(), f = first[i];
      if (reduce) return;
      el.style.transform = 'translate(' + (f.left - l.left) + 'px,' + (f.top - l.top) + 'px) scale(' +
        (sc * f.width / l.width) + ')';
    });
    reveal.hidden = false;
    if (reduce) { drawCables(); return; }
    requestAnimationFrame(function () { requestAnimationFrame(function () {
      els.forEach(function (el, i) {
        el.style.transition = 'transform .85s cubic-bezier(.16,1,.3,1) ' + (i * 90) + 'ms';
        el.style.transform = 'scale(' + sc + ')';
      });
      setTimeout(drawCables, 850 + els.length * 90 + 250);
    }); });
  }

''' + js[b:]

# ropes anchor at the visible strip of each fanned card
a = js.index('  var rz = 0;')
b = js.index('  function reset() {')
js = js[:a] + r'''  var rz = 0;
  addEventListener('resize', function () {
    if (!done) return;
    clearTimeout(rz);
    rz = setTimeout(drawCables, 180);
  }, { passive: true });

''' + js[b:]
# insert the rope engine (from patch_ropes) before "var rz = 0;" if missing
if 'function stepRope' not in js:
    ropes = io.open('patch_ropes.py', encoding='utf-8').read()
    ra = ropes.index("ropes = r'''") + len("ropes = r'''"); rb = ropes.index("'''", ra)
    block = ropes[ra:rb]
    block = block.replace("        x1: a1.right - host.left - 6, y1: a1.top + a1.height * .5 - host.top,",
                          "        x1: a1.right - host.left - 4, y1: a1.top + Math.min(a1.height * .5, 30) - host.top,")
    js = js.replace('  var rz = 0;\n', block + '  var rz = 0;\n', 1)
    js = js.replace('''  function link() {
    function hot(fn, on) {
      desk.querySelectorAll('[data-fn]').forEach(function (el) {
        if (el.dataset.fn === fn) el.classList.toggle('hot', on);
      });
    }
''', '  function link() {\n')
# link() is called from the old finish(); call it once at setup instead
js = js.replace("  makeCards();\n  setHint();\n  new IntersectionObserver(", "  makeCards();\n  setHint();\n  link();\n  new IntersectionObserver(")

# reset: the cards fly back to the deck
a = js.index('  function reset() {')
b = js.index('  makeCards();\n  setHint();\n  link();')
js = js[:a] + r'''  function reset() {
    var first = els.map(function (el) { return el.getBoundingClientRect(); });
    ropes = []; grabbed = null; cables.innerHTML = ''; notes.innerHTML = '';
    reveal.hidden = true;
    heads.classList.remove('flip'); stage.classList.remove('flip');
    btns.hidden = false; hint.hidden = false;
    pileL.classList.remove('hot'); pileR.classList.remove('hot');
    els.forEach(function (el, i) {
      deck.appendChild(el);
      el.classList.remove('desk', 'piled');
      el.style.width = el.style.height = '';
      var fm = el.querySelector('.fnmark'); if (fm) fm.remove();
      el.style.zIndex = CARDS.length - i; el.style.pointerEvents = '';
      delete el.dataset.fn; delete el.dataset.dir; delete el.dataset.k;
      var rest = 'translateY(' + (i * 6) + 'px) scale(' + (1 - i * 0.02).toFixed(3) + ')';
      el.dataset.rest = rest; el.style.setProperty('--rest', rest);
      el.style.transition = 'none'; el.style.transform = rest;
      if (i) el.setAttribute('aria-hidden', 'true'); else el.removeAttribute('aria-hidden');
    });
    minis.forEach(function (s) { s.remove(); }); minis = [];
    colL.style.height = colR.style.height = '';
    onPile = { l: [], r: [] };
    if (!reduce) {
      els.forEach(function (el, i) {
        var l = el.getBoundingClientRect(), f = first[i];
        el.style.transform = 'translate(' + (f.left - l.left) + 'px,' + (f.top - l.top) + 'px) scale(' + (f.width / l.width) + ')';
      });
      requestAnimationFrame(function () { requestAnimationFrame(function () {
        els.forEach(function (el, i) {
          el.style.transition = 'transform .8s cubic-bezier(.16,1,.3,1) ' + ((els.length - i) * 60) + 'ms';
          el.style.transform = el.dataset.rest;
        });
      }); });
    }
    idx = 0; done = false; touched = false;
    setHint();
    armNudge();
  }

''' + js[b:]
# hint fixes: the skip button sends in a burst; keep it but with a pause per card
js = js.replace("    while (idx < CARDS.length && !done) send(idx % 2 ? -1 : 1);",
                "    (function step() { if (idx < CARDS.length && !done) { send(idx % 2 ? -1 : 1); setTimeout(step, 260); } })();")

# --- why us: no change in JS ---

# --- workshop: one continuous spine, one marker ----------------------------
a = js.index('  /* the three chevrons run down each spine as the reader passes it */')
b = js.index('  /* one visual per moment, built from the same square-to-suit path */')
js = js[:a] + r'''  /* one continuous line down the whole route; a single chevron rides it
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

''' + js[b:]
io.open('app.src.js', 'w', encoding='utf-8').write(js)

# =========================== shell.html ===========================
h = io.open('shell.html', encoding='utf-8').read()
# numbers
a = h.index('    <div class="viz" id="viz">'); b = h.index('<!-- ---------------------------- swipe, felt')
b = h.rindex('</section>', 0, b) + len('</section>')
h = h[:a] + '''    <div class="viz" id="viz">
      <h3>Taught teams get more done.</h3>
      <span class="rule ruledraw" aria-hidden="true"></span>
      <p class="lede">The same hundred people, twice. Teach one group first and it gets up to a third more done.</p>

      <div class="bars" id="bars" role="img" aria-label="Two bars made of marks. A hundred squares for people left to work it out. A hundred and thirty-four spades for people who were taught first: thirty-four percent more.">
        <figure class="barcol base">
          <svg id="barA" aria-hidden="true"></svg>
          <figcaption><b>100</b><span>Left to work it out</span></figcaption>
        </figure>
        <figure class="barcol taught">
          <p class="delta" aria-hidden="true">+34%</p>
          <svg id="barB" aria-hidden="true"></svg>
          <figcaption><b>134</b><span>Taught first</span></figcaption>
        </figure>
      </div>

      <p class="aside">And today only <b>47 of 100</b> people at work were ever taught to use AI at all.</p>

      <div class="cites">
        <p class="src">+34% for taught beginners &mdash; Brynjolfsson, Li &amp; Raymond, NBER 31161, 2023</p>
        <p class="src">47% trained &mdash; KPMG &times; Melbourne Business School, 2025</p>
      </div>
    </div>
  </div>
</section>''' + h[b:]

# swipe: heads and boards share a grid cell so the swap never shifts the page
a = h.index('    <div class="swipehead" id="swipehead">'); b = h.index('<!-- ---------------------------- why us, cream')
b = h.rindex('</section>', 0, b) + len('</section>')
h = h[:a] + '''    <div class="heads" id="heads">
      <div class="swipehead" id="swipehead">
        <h2 class="h2">Can AI<br>take this?</h2>
        <p class="lede">Five things that land on an office desk every week. Swipe right if AI can take it. Left if best not.</p>
      </div>
      <div class="deskhead" id="deskhead">
        <h3>Here's your desk.</h3>
        <p>Two piles. Every card on the right works, with a note. Every card on the left could work too, with the same note.</p>
      </div>
    </div>

    <div class="stage" id="stage">
      <div class="table" id="table">
        <div class="pile l" id="pileL">
          <p class="pile-h">Best not</p>
        </div>
        <div class="deck" id="deck" tabindex="0" role="group"
             aria-label="Five cards. Press the left arrow key for best not, the right arrow key for AI can take it."></div>
        <div class="pile r" id="pileR">
          <p class="pile-h">AI can take it</p>
        </div>
      </div>
      <div class="desk" id="desk">
        <div class="cables" id="cables" aria-hidden="true"></div>
        <div class="deskgrid">
          <div class="deskpiles">
            <div class="col" id="colL"><p class="colh">Best not</p></div>
            <div class="col" id="colR"><p class="colh">AI can take it</p></div>
          </div>
          <div class="notes" id="notes"></div>
        </div>
      </div>
    </div>

    <div class="btns" id="btns">
      <button class="btn" id="bLeft" type="button">Best not</button>
      <button class="btn" id="bRight" type="button">AI can take it</button>
      <button class="btn quiet" id="bSkip" type="button">Just show me the notes</button>
    </div>
    <p class="hint" id="hint" role="status" aria-live="polite"></p>

    <div id="reveal" hidden>
      <p class="workshopline">The asterisks are the workshop.</p>
      <div class="dealagain"><button class="btn" id="bAgain" type="button">Deal again</button></div>
    </div>
  </div>
</section>''' + h[b:]
assert 'id="swipehead"' in h

# workshop: one spine, per-moment cells stay empty
h = h.replace('<div class="spine"><span class="rule v" aria-hidden="true"></span></div>', '<div class="spine"></div>')
h = h.replace('<div class="spine"><span class="rule v dotted" aria-hidden="true"></span></div>', '<div class="spine"></div>')
h = h.replace('  <ol class="moments wrap" id="moments">\n', '''  <ol class="moments wrap" id="moments">
    <div class="spineline" id="spineline" aria-hidden="true"></div>
    <div class="spineline dotted" id="spinedots" aria-hidden="true"></div>
    <svg class="spinemark" id="spinemark" viewBox="0 0 64 28" aria-hidden="true"><use href="#chevron-down"/></svg>
''')
# footer: no cédula yet
h = h.replace('      <span>C&eacute;dula jur&iacute;dica: <span class="todo">TODO</span></span>\n', '')
io.open('shell.html', 'w', encoding='utf-8').write(h)

# sprites: a down-pointing chevron symbol
sp = io.open(os.path.join(S, 'sprites.svg'), encoding='utf-8').read()
if 'id="chevron-down"' not in sp:
    sp = sp.replace('<symbol id="chevron" viewBox="0 0 28 64">',
        '<symbol id="chevron-down" viewBox="0 0 64 28"><path fill="currentColor" d="M0,0l31.893,13.398l31.893,-13.398l0,14.12l-31.893,13.398l-31.893,-13.398l0,-14.12Z"/></symbol>\n<symbol id="chevron" viewBox="0 0 28 64">')
    io.open(os.path.join(S, 'sprites.svg'), 'w', encoding='utf-8').write(sp)

# =========================== build.py ===========================
bp = io.open('build.py', encoding='utf-8').read()
bp = bp.replace('    <span class="rule v point rise" aria-hidden="true"></span>\n', '')
io.open('build.py', 'w', encoding='utf-8').write(bp)

# =========================== styles.css ===========================
c = io.open(os.path.join(S, 'styles.css'), encoding='utf-8').read()
# the rule: a plain continuous line now. Thin. No cut-outs.
a = c.index('.rule{--rt:14px;'); b = c.index('.rule.drift{')
c = c[:a] + '''.rule{--rt:3px;display:block;width:100%;height:var(--rt);background:currentColor;color:inherit;flex:none}
.rule.thin{--rt:2px}
.rule.mid{--rt:2px}
.rule.v{--rt:3px;width:var(--rt);height:100%}
.rule.dotted{background:repeating-linear-gradient(to bottom,currentColor 0 6px,transparent 6px 14px)}
''' + c[b:]
c = c.replace('.rule.drift{animation:driftH 5.5s linear infinite;will-change:mask-position}\n', '').replace('.rule.drift{animation:driftH 9s cubic-bezier(.45,0,.55,1) infinite}\n', '')
c = re.sub(r'\.rule\.drift\{[^}]*\}\n?', '', c)
c = re.sub(r'\.rule\.v\.drift\{[^}]*\}\n?', '', c)
c = c.replace('.viz>.rule{--rt:14px;margin-top:.2em;color:var(--ink);opacity:.62}', '.viz>.rule{--rt:4px;margin-top:.25em;color:var(--ink);opacity:.9}')
c = c.replace('.closer .rule{--rt:14px;margin-top:.45em;color:var(--ink);opacity:.62}', '')
c = re.sub(r'\.close \.point\{[^}]*\}\n?', '', c)

# numbers graph
a = c.index('.legend{'); b = c.index('.liftrow,.viz .cites>div{')
b = c.index('}', b) + 1
c = c[:a] + '''.bars{display:grid;grid-template-columns:repeat(2,minmax(0,220px));gap:clamp(28px,6vw,90px);
  align-items:end;margin-top:calc(var(--cell)*1.3)}
.barcol{margin:0;display:grid;gap:.7em;justify-items:start}
.barcol svg{display:block;width:100%;height:auto;overflow:visible;color:var(--ink-dim)}
.barcol.taught svg{color:var(--gold-ink)}
.barcol figcaption{display:grid;line-height:1.15}
.barcol figcaption b{font-family:var(--title);font-weight:800;letter-spacing:-.04em;font-size:clamp(1.6rem,3vw,2.4rem);color:var(--ink)}
.barcol figcaption span{color:var(--ink-dim);font-size:.95rem}
.barcol.taught figcaption b{color:var(--gold-ink)}
.bars .mk{opacity:0;transition:opacity .38s linear}
.bars .mk path{transform-box:fill-box;transform-origin:center;transition:transform .5s cubic-bezier(.16,1,.3,1)}
.js .bars .mk path{transform:scale(.4)}
.viz.in .bars .mk:not(.extra){opacity:1}
.viz.in .bars .mk:not(.extra) path,.viz.more .bars .mk.extra path{transform:none}
.viz.more .bars .mk.extra{opacity:1}
.delta{font-family:var(--title);font-weight:800;letter-spacing:-.04em;line-height:1;
  font-size:clamp(2rem,4.2vw,3.4rem);color:var(--gold-ink);opacity:0;transform:translateY(10px);
  transition:opacity .5s linear .5s,transform .7s cubic-bezier(.16,1,.3,1) .5s}
.viz.more .delta{opacity:1;transform:none}
.aside{margin-top:calc(var(--cell)*1.1);color:var(--ink-dim);font-size:clamp(1.02rem,1.35vw,1.16rem);max-width:52ch}
.aside b{color:var(--ink)}
.viz .cites{margin-top:calc(var(--cell)*.9)}''' + c[b:]
c = c.replace('  .liftrow{grid-template-columns:minmax(0,1fr);gap:.3em}\n  .liftrow .val{justify-self:start}', '  .bars{grid-template-columns:repeat(2,minmax(0,1fr))}')
c = c.replace('  .liftrow .bar i{transform:scaleX(var(--v,1))!important}\n', '')

# swipe: shared cells, piled and desk cards, slots
c = c.replace('.table{display:grid;grid-template-columns:minmax(0,1fr) auto minmax(0,1fr);\n  gap:clamp(12px,2.4vw,36px);align-items:start;margin-top:calc(var(--cell)*1.4)}',
'''.heads,.stage{display:grid}
.heads>*,.stage>*{grid-area:1/1}
.heads .deskhead,.stage .desk{opacity:0;visibility:hidden;transition:opacity .6s linear .35s,visibility 0s .95s}
.heads .swipehead,.stage .table{transition:opacity .35s linear,visibility 0s .35s}
.heads.flip .swipehead,.stage.flip .table{opacity:0;visibility:hidden}
.heads.flip .deskhead,.stage.flip .desk{opacity:1;visibility:visible;transition:opacity .6s linear .3s,visibility 0s}
.stage.flip .table{pointer-events:none}
.table{display:grid;grid-template-columns:minmax(0,1fr) auto minmax(0,1fr);
  gap:clamp(12px,2.4vw,36px);align-items:start;margin-top:calc(var(--cell)*1.4)}''')
c = c.replace('.stack{display:flex;flex-direction:column;padding-top:14px;--ov:-78px}\n.stack .mini+.mini{margin-top:var(--ov)}\n', '')
c = c.replace('.card{position:absolute;inset:0;background:var(--cream);color:var(--ink);',
              '.card.piled{cursor:default;box-shadow:0 18px 36px -22px rgba(0,0,0,.95)}\n.card{position:absolute;inset:0;background:var(--cream);color:var(--ink);')
# the desk
a = c.index('.mini{background:var(--cream)'); b = c.index('/* --- the desk: two columns of cards, cables, notes --- */')
c = c[:a] + '''/* on the desk every card is the same element it was in the hand */
.slot{position:absolute;left:0;transition:transform .35s var(--ease)}
.slot .card{transform-origin:0 0;inset:auto;left:0;top:0;cursor:default}
.slot:hover,.slot:focus-within,.slot.hot{z-index:30!important;transform:translateY(-8px)}
.slot.hot .card{box-shadow:0 0 0 3px var(--gold),0 26px 52px -26px rgba(0,0,0,.95)}
.slot .fnmark{position:absolute;top:8px;right:10px;font-family:var(--body);font-weight:600;
  color:var(--gold-ink);font-size:2.4rem;line-height:1}

''' + c[b:]
c = c.replace('.deskpiles .col{display:grid;gap:14px;align-content:start}', '.deskpiles .col{position:relative}')
c = re.sub(r'\.deskpiles \.mini[^\n]*\n', '', c)
c = c.replace('.deskgrid{display:grid;position:relative;z-index:1;grid-template-columns:minmax(0,.95fr) minmax(0,1.15fr);',
              '.deskgrid{display:grid;position:relative;z-index:1;grid-template-columns:minmax(0,1fr) minmax(0,1fr);')
c = c.replace('.desk{position:relative;margin-top:calc(var(--cell)*1.2)}', '.desk{position:relative;margin-top:calc(var(--cell)*1.4)}')

# why us: bolder hover
c = c.replace('.whyband:hover .suit,.whyband:focus-within .suit{opacity:1;color:var(--gold-ink);\n  transform:scale(1.07) rotate(-2.2deg)}',
'''.whyband:hover .suit,.whyband:focus-within .suit{opacity:1;color:var(--gold-ink);
  animation:whyfloat 2.6s ease-in-out infinite;transform:scale(1.9) rotate(-6deg)}
@keyframes whyfloat{0%,100%{transform:scale(1.9) rotate(-6deg) translateY(0)}
  50%{transform:scale(2.05) rotate(4deg) translateY(-7px)}}''')
c = c.replace('.whyband{display:grid;grid-template-columns:clamp(48px,6vw,84px) minmax(0,1fr);',
              '.whyband{display:grid;overflow:visible;position:relative;z-index:0;grid-template-columns:clamp(48px,6vw,84px) minmax(0,1fr);')
c = c.replace('.whyband:hover,.whyband:focus-within{background:var(--cream-2)}', '.whyband:hover,.whyband:focus-within{background:var(--cream-2);z-index:2}')

# workshop spine: continuous
c = c.replace('.moment .spine{position:relative;height:100%;display:flex;justify-content:center;\n  color:var(--on-carbon);opacity:.15;transition:opacity .8s var(--ease),color .8s var(--ease)}\n.moment.on .spine{opacity:.85;color:var(--cream)}\n.moment.opt .spine{color:var(--gold)}',
'''.moments{position:relative}
.spineline{position:absolute;top:0;left:calc(clamp(14px,1.7vw,18px)/2 - 1.5px);width:3px;
  background:var(--on-carbon);opacity:.28;pointer-events:none}
.spineline.dotted{bottom:0;background:repeating-linear-gradient(to bottom,var(--gold) 0 6px,transparent 6px 14px);opacity:.7}
.spinemark{position:absolute;top:0;left:calc(clamp(14px,1.7vw,18px)/2 - 12px);width:24px;height:11px;
  color:var(--cream);filter:drop-shadow(0 0 8px rgba(243,238,228,.55));will-change:transform;
  transition:color .5s linear}
.spinemark.gold{color:var(--gold)}
.moment .spine{position:relative;height:100%}''')
c = c.replace('  .moment .spine{opacity:.7}\n', '')
c = c.replace('  .rule.drift,.cable .flow{animation:none!important}', '  .cable .flow,.whyband .suit{animation:none!important}')
io.open(os.path.join(S, 'styles.css'), 'w', encoding='utf-8').write(c)
print('r5 patched')
