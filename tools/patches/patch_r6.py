import io, os, re
os.chdir(os.path.dirname(os.path.abspath(__file__)))
S = '..'
js = io.open('app.src.js', encoding='utf-8').read()
h = io.open('shell.html', encoding='utf-8').read()
c = io.open(os.path.join(S, 'styles.css'), encoding='utf-8').read()
bp = io.open('build.py', encoding='utf-8').read()

def must(s, old, new, count=1):
    assert old in s, old[:80]
    return s.replace(old, new, count)

# ============================ 1. HERO: gather into a heart ============================
js = must(js, "  var WAKE_D = 220, FADE_UP = 880, HOLD = 1400, BACK = 640, FADE_DN = 1000;",
              "  var WAKE_D = 160, FADE_UP = 700, HOLD = 1300, BACK = 520, FADE_DN = 900;")
# the heart mark
js = must(js, "  svg.appendChild(frag);\n\n  var par = { x: 0, y: 0 };",
"""  svg.appendChild(frag);

  /* the gathering: hold the hand still and the marks that crowd it feed one
     heart. Let go and it gives them back. */
  var heart = { g: document.createElementNS(NS, 'g'), p: document.createElementNS(NS, 'path'),
                charge: 0, x: W / 2, y: H / 2 };
  heart.p.setAttribute('fill', 'currentColor'); heart.p.setAttribute('d', mix('smooth-heart', 1));
  heart.g.setAttribute('class', 'glow heartmark'); heart.g.setAttribute('opacity', '0');
  heart.g.appendChild(heart.p); svg.appendChild(heart.g);

  var par = { x: 0, y: 0 };""")
js = must(js, "    for (var i = 0; i < marks.length; i++) {\n      var m = marks[i];\n      if (!m.live) continue;\n      var ent =",
"""    /* how crowded is the hand? */
    var crowd = 0;
    if (ptr.on) for (var ci = 0; ci < marks.length; ci++) {
      var cm = marks[ci];
      if (cm.live && !cm.anchor && Math.hypot(cm.x - ptr.x, cm.y - ptr.y) < 64) crowd++;
    }
    if (ptr.on && crowd >= 2) heart.charge = Math.min(1, heart.charge + dt / 2.2 * Math.min(1, crowd / 3));
    else heart.charge = Math.max(0, heart.charge - dt / 1.7);
    if (ptr.on) { heart.x += (ptr.x - heart.x) * Math.min(1, 6 * dt); heart.y += (ptr.y - heart.y) * Math.min(1, 6 * dt); }
    var hs = 28 + heart.charge * 120;
    heart.g.setAttribute('opacity', Math.min(.94, heart.charge * 1.15).toFixed(3));
    heart.g.setAttribute('transform', 'translate(' + heart.x.toFixed(1) + ' ' + heart.y.toFixed(1) +
      ') scale(' + (hs / 100).toFixed(4) + ') translate(-50 -50)');

    for (var i = 0; i < marks.length; i++) {
      var m = marks[i];
      if (!m.live) continue;
      var ent =""")
js = must(js, """      if (near && dp > 36 && !m.anchor) {
        var pull = (1 - dp / R) * 240 * dt;""", """      if (near && dp > 30 && !m.anchor) {
        var pull = (1 - dp / R) * (380 + heart.charge * 500) * dt;""")
js = must(js, "      hush = 1 - .85 * Math.min(1, deepest);",
"""      hush = 1 - .85 * Math.min(1, deepest);
      /* a mark that feeds the heart fades into it */
      if (heart.charge > 0 && !m.anchor) {
        var dh = Math.hypot(m.x - heart.x, m.y - heart.y);
        if (dh < 96) hush *= 1 - heart.charge * (1 - dh / 96);
      }""")

# ============================ 2. GRAPH: hover influence + copy ============================
js = must(js, """  new IntersectionObserver(function (es, o) {
    if (!es[0].isIntersecting) return;
    o.disconnect();
    /* beat 1: the same hundred people, twice */""", """  /* the hand over the marks: spades swell, squares only shift a little */
  var bars = document.getElementById('bars'), live = false, braf = 0, bev = null;
  function influence() {
    braf = 0;
    if (!live) return;
    [[A, document.getElementById('barA'), false], [B, document.getElementById('barB'), true]].forEach(function (set) {
      var cells = set[0], svg = set[1], strong = set[2];
      var r = svg.getBoundingClientRect(), k = r.width / (COLS * CW);
      if (!bev) { cells.forEach(function (cc) { cc.p.style.transform = ''; }); return; }
      var px = (bev.clientX - r.left) / k, py = (bev.clientY - r.top) / k;
      cells.forEach(function (cc) {
        var cx = (cc.n % COLS) * CW + CW / 2, cy = H - cc.row * CH - CH / 2;
        var dx = cx - px, dy = cy - py, d = Math.hypot(dx, dy), RR = 95;
        if (d > RR) { if (cc.p.style.transform) cc.p.style.transform = ''; return; }
        var f = 1 - d / RR, sc = 1 + (strong ? .75 : .18) * f, sh = (strong ? 2.2 : 3.4) * f;
        cc.p.style.transform = 'translate(' + (dx / (d || 1) * sh).toFixed(2) + 'px,' + (dy / (d || 1) * sh).toFixed(2) +
          'px) scale(' + sc.toFixed(3) + ')';
      });
    });
  }
  bars.addEventListener('pointermove', function (e) { bev = e; if (!braf) braf = requestAnimationFrame(influence); }, { passive: true });
  bars.addEventListener('pointerleave', function () { bev = null; if (!braf) braf = requestAnimationFrame(influence); }, { passive: true });

  new IntersectionObserver(function (es, o) {
    if (!es[0].isIntersecting) return;
    o.disconnect();
    /* beat 1: the same hundred people, twice */""")
js = must(js, """      viz.classList.add('more');
    }, 2900);""", """      viz.classList.add('more');
      setTimeout(function () { live = true; viz.classList.add('live'); }, 1400);
    }, 2900);""")
js = must(js, """  if (reduce) {
    viz.classList.add('in', 'taught', 'more');
    B.forEach(function (c) { c.p.setAttribute('d', mix('smooth-spade', 1)); });
    return;
  }""", """  if (reduce) {
    viz.classList.add('in', 'taught', 'more');
    B.forEach(function (c) { c.p.setAttribute('d', mix('smooth-spade', 1)); });
  }""")
# guard: with reduced motion the observer block still runs; make it a no-op then
js = must(js, """  new IntersectionObserver(function (es, o) {
    if (!es[0].isIntersecting) return;
    o.disconnect();
    /* beat 1: the same hundred people, twice */""", """  if (!reduce) new IntersectionObserver(function (es, o) {
    if (!es[0].isIntersecting) return;
    o.disconnect();
    /* beat 1: the same hundred people, twice */""")

# ============================ 3. DESK: one row per card, two answers ============================
a = js.index("  var CARDS = ["); b = js.index("  ];", a) + 4
js = js[:a] + """  /* two answers per card: what to know if you hand it over, what to know if
     you keep it. Neither is wrong. Both come with a catch. */
  var CARDS = [
    { q: "Answer a client asking why their invoice is higher this month.", pip: "classic-spade",
      r: "It writes a convincing reply in seconds. If it doesn't have the numbers, it invents a reason. Give it the invoice, then read before sending.",
      l: "Fair. Then you are typing that reply yourself. It can still draft it: hand it the invoice, keep the decision and the send button." },
    { q: "Summarise the 40-page supplier contract.", pip: "classic-heart",
      r: "Good summary, and it will skip the one clause that matters. Ask for the clause list first, then read those pages yourself.",
      l: "Forty pages is a long afternoon. Let it list the clauses and where they sit, then read only those pages. The reading that counts stays yours." },
    { q: "Enter this stack of receipts into the system.", pip: "classic-diamond",
      r: "It reads receipts well. It is blind to duplicates and wrong dates. Spot-check one in ten.",
      l: "This is the one most teams hand over first. It reads receipts well. Keep the spot-check: one in ten, and anything that looks doubled." },
    { q: "Write the monthly report for the owner.", pip: "classic-club",
      r: "The structure in a minute. Every number needs a human check: numbers are where it sounds most sure and is most wrong.",
      l: "The structure it can do in a minute. The numbers are the part to guard: check every one, because it sounds most sure where it is most wrong." },
    { q: "Decide whether the new client gets 60-day payment terms.", pip: "classic-spade",
      r: "It can list the pros and cons. The decision, and the risk, stay with a person. If it says yes, it is still your yes.",
      l: "Right call to keep. It can still lay out the pros and cons in a minute. The decision, and the risk, stay with a person." }
  ];""" + js[b:]
js = must(js, "      colL = document.getElementById('colL'), colR = document.getElementById('colR'),\n", "      rows = document.getElementById('rows'),\n")
js = must(js, "    el.dataset.fn = c.fn; el.dataset.dir = side; el.dataset.k = k;", "    el.dataset.fn = String(idx + 1); el.dataset.dir = side; el.dataset.k = k;")
# finish: rows
a = js.index("  /* --- the desk: the piles spread into two fanned columns ------------------ */")
b = js.index("  /* Each card hangs a cable to its note.")
js = js[:a] + r"""  /* --- the desk: one row per card, the card on the left, its answer on the right --- */
  var stage = document.getElementById('stage'), heads = document.getElementById('heads');
  var SLOT = { w: 0, h: 0 };
  function finish() {
    if (done) return;
    done = true;
    stopNudge();
    var dr = deck.getBoundingClientRect();
    var narrow = innerWidth <= 900;
    SLOT.w = Math.round(dr.width * (narrow ? .42 : .5)); SLOT.h = Math.round(dr.height * (narrow ? .42 : .5));
    var sc = SLOT.w / dr.width;
    minis = [];
    /* first: where every card is on its pile */
    var first = els.map(function (el) { return el.getBoundingClientRect(); });
    heads.classList.add('flip'); stage.classList.add('flip');
    btns.hidden = true; hint.hidden = true;
    rows.innerHTML = '';
    els.forEach(function (el, i) {
      var cd = CARDS[i], right = el.dataset.dir === 'r';
      var row = document.createElement('div');
      row.className = 'row'; row.dataset.fn = el.dataset.fn;
      var slot = document.createElement('div');
      slot.className = 'slot'; slot.dataset.fn = el.dataset.fn;
      slot.style.width = SLOT.w + 'px'; slot.style.height = SLOT.h + 'px';
      row.appendChild(slot);
      var note = document.createElement('div');
      note.className = 'note'; note.dataset.fn = el.dataset.fn; note.tabIndex = 0;
      note.innerHTML = '<p class="said">You said: <b>' + (right ? 'AI can take it' : 'Best not') + '</b></p>' +
        '<p class="q">' + cd.q + '</p><p class="a">' + (right ? cd.r : cd.l) + '</p>';
      row.appendChild(note);
      rows.appendChild(row);
      slot.appendChild(el);
      el.classList.remove('piled'); el.classList.add('desk');
      el.style.zIndex = ''; el.style.pointerEvents = '';
      el.style.width = dr.width + 'px'; el.style.height = dr.height + 'px';
      el.style.transition = 'none';
      el.style.transform = 'scale(' + sc + ')';
      minis.push(slot);
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

""" + js[b:]
# cable anchors: card right-middle to the note's left edge, short and hanging
js = must(js, "        x1: a1.right - host.left - 4, y1: a1.top + Math.min(a1.height * .5, 30) - host.top,\n        x2: b1.left - host.left + 12, y2: b1.top + 26 - host.top };",
              "        x1: a1.right - host.left - 4, y1: a1.top + a1.height * .5 - host.top,\n        x2: b1.left - host.left - 6, y2: b1.top + 30 - host.top };")
js = must(js, "      var len = span * (1.10 + i * .045), seg = len / (N - 1), pts = [];",
              "      var len = span * 1.28, seg = len / (N - 1), pts = [];")
js = must(js, "    }).filter(Boolean).sort(function (p, q) { return p.y2 - q.y2; });", "    }).filter(Boolean);")
js = must(js, "    if (innerWidth <= 900) return;\n    var host = desk.getBoundingClientRect();", "    var host = desk.getBoundingClientRect();")
# reset: rows away, no fnmark
js = must(js, "    ropes = []; grabbed = null; cables.innerHTML = ''; notes.innerHTML = '';", "    ropes = []; grabbed = null; cables.innerHTML = '';")
js = must(js, "      var fm = el.querySelector('.fnmark'); if (fm) fm.remove();\n", "")
js = must(js, "    minis.forEach(function (s) { s.remove(); }); minis = [];\n    colL.style.height = colR.style.height = '';", "    minis = [];")
js = js.replace("    notes.innerHTML = CARDS.map(function (c) {", "    void 0; [].map(function (c) {")
js = js.replace("      notes = document.getElementById('notes'), cables = document.getElementById('cables'),", "      cables = document.getElementById('cables'),")
js = js.replace("      var note = notes.querySelector('.note[data-fn=\"' + m.dataset.fn + '\"]');", "      var note = rows.querySelector('.note[data-fn=\"' + m.dataset.fn + '\"]');")
# after the cards fly home, the rows must go after the FLIP measured them: remove at the end of reset
js = must(js, "    idx = 0; done = false; touched = false;\n    setHint();\n    armNudge();", "    rows.innerHTML = '';\n    idx = 0; done = false; touched = false;\n    setHint();\n    armNudge();")

io.open('app.src.js', 'w', encoding='utf-8').write(js)

# ============================ SHELL ============================
h = must(h, "<h3>Taught teams get more done.</h3>", "<h3>Teams taught to use AI get more done.</h3>")
h = must(h, "The same hundred people, twice. Teach one group first and it gets up to a third more done.",
            "The same hundred people, twice. Teach one group to use AI on its own work first, and that group gets up to a third more done.")
h = must(h, '<p class="delta" aria-hidden="true">+34%</p>',
            '<p class="delta" aria-hidden="true"><svg viewBox="0 0 100 100"><use href="#classic-spade"/></svg><span>+34%</span></p>')
# reveal
h = must(h, """        <p>Two piles. Every card on the right works, with a note. Every card on the left could work too, with the same note.</p>""",
            """        <p>Five calls, five catches. None of them wrong. Each one has a detail worth knowing before Monday.</p>""")
a = h.index('      <div class="desk" id="desk">'); b = h.index('    </div>\n\n    <div class="btns" id="btns">')
h = h[:a] + """      <div class="desk" id="desk">
        <div class="cables" id="cables" aria-hidden="true"></div>
        <div class="rows" id="rows"></div>
      </div>
""" + h[b:]
h = must(h, '<p class="workshopline">The asterisks are the workshop.</p>', '<p class="workshopline">Those catches are what we teach in half a day.</p>')
# why us: a wrapper class for the fade-the-others rule
h = must(h, '    <div style="margin-top:calc(var(--cell)*1.4)">\n      <div class="whyband" data-suit="smooth-spade"', '    <div class="bands">\n      <div class="whyband" data-suit="smooth-spade"')
# logo: third edition everywhere, always the real lockup when there are words
h = must(h, '           width="133" height="28"><use href="#logo-full" width="1694.24" height="358.08"/></svg>',
            '           width="125" height="32"><use href="#logo-full" width="1703.11" height="435.6"/></svg>')
h = h.replace('viewBox="112.88 359.73 1694.24 358.08"', 'viewBox="94.06 284.2 1703.11 435.6"')
h = must(h, """          <svg class="logo" viewBox="0 0 344.96 358.07" role="img" aria-label="kadabra"
               width="29" height="30"><use href="#logo-mark" width="344.96" height="358.07"/></svg>
          <span>kadabra</span>""", """          <svg class="logo" viewBox="94.06 284.2 1703.11 435.6" role="img" aria-label="kadabra"
               width="125" height="32"><use href="#logo-full" width="1703.11" height="435.6"/></svg>""")
h = must(h, "<span>&copy; 2026 kadabra. All rights reserved.</span>", "<span>&copy; 2026 kadabra CR. All rights reserved.</span>")
io.open('shell.html', 'w', encoding='utf-8').write(h)
# favicon from the new mark
sp = io.open(os.path.join(S, 'sprites.svg'), encoding='utf-8').read()
m = re.search(r'<symbol id="logo-mark" viewBox="([^"]+)"><title>[^<]*</title>(<path[^>]*/>)</symbol>', sp)
io.open(os.path.join(S, 'favicon.svg'), 'w', encoding='utf-8').write(
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="%s">%s</svg>' % (m.group(1), m.group(2).replace('currentColor', '#F3EEE4')))

# ============================ CSS ============================
# cables: one colour, gold only when hot
c = must(c, """.cable .rope{fill:none;stroke:var(--on-felt-dim);stroke-width:5;stroke-linecap:round;opacity:.5;""",
            """.cable .rope{fill:none;stroke:var(--on-felt);stroke-width:4;stroke-linecap:round;opacity:.55;""")
c = must(c, ".cable.in .flow{opacity:.32}", ".cable.in .flow{opacity:0}")
c = must(c, ".cable.hot .flow{opacity:.95;animation-duration:.8s;transition-delay:0s}", ".cable.hot .flow{opacity:.9;animation-duration:.8s;transition-delay:0s}")
c = must(c, ".cable .flow{fill:none;stroke:var(--gold);stroke-width:5;", ".cable .flow{fill:none;stroke:var(--gold);stroke-width:4;")
# desk rows
a = c.index('/* on the desk every card is the same element it was in the hand */'); b = c.index('.desk{touch-action:pan-y}')
c = c[:a] + """/* on the desk every card is the same element it was in the hand */
.rows{display:grid;gap:clamp(18px,2.4vw,30px);position:relative;z-index:1}
.row{display:grid;grid-template-columns:auto minmax(0,1fr);gap:clamp(90px,12vw,170px);align-items:center;
  padding:clamp(10px,1.4vw,18px) 0;border-top:1px solid var(--felt-line)}
.row:first-child{border-top:0}
.slot{position:relative;transition:transform .35s var(--ease)}
.slot .card{transform-origin:0 0;inset:auto;left:0;top:0;cursor:default;box-shadow:0 18px 36px -22px rgba(0,0,0,.95)}
.row.hot .slot{transform:translateY(-4px)}
.row.hot .card{box-shadow:0 0 0 3px var(--gold),0 26px 52px -26px rgba(0,0,0,.95)}
.note{outline:none;padding:.4em 0}
.note .said{font-size:.86rem;letter-spacing:.04em;color:var(--on-felt-dim);text-transform:uppercase}
.note .said b{color:var(--gold);font-weight:600}
.note .q{color:var(--white);font-weight:600;margin-top:.5em;font-size:clamp(1.05rem,1.4vw,1.25rem)}
.note .a{color:var(--on-felt);margin-top:.4em;font-size:clamp(.98rem,1.2vw,1.08rem);max-width:52ch}
.row.hot .note .q{color:var(--gold)}
.desk{position:relative;margin-top:calc(var(--cell)*1.4)}
.deskhead{text-align:center;max-width:52ch;margin-inline:auto}
.deskhead h3{font-size:clamp(2rem,4.6vw,3.4rem);padding-bottom:.06em}
.deskhead p{margin-top:.6em;color:var(--on-felt);font-size:clamp(1.02rem,1.3vw,1.16rem)}
/* the wiring runs behind the cards, never across their copy */
.cables{position:absolute;inset:0;pointer-events:none;z-index:0}
.ropes{position:absolute;inset:0;width:100%;height:100%;overflow:visible;display:block}
.cable .rope{fill:none;stroke:var(--on-felt);stroke-width:4;stroke-linecap:round;opacity:.55;
  stroke-dasharray:1;stroke-dashoffset:1;
  transition:opacity .3s var(--ease),stroke .3s var(--ease),stroke-dashoffset 1s var(--ease)}
.cable.in .rope{stroke-dashoffset:0}
.cable .flow{fill:none;stroke:var(--gold);stroke-width:4;stroke-linecap:round;opacity:0;
  stroke-dasharray:12 30;animation:ropeflow 1.4s linear infinite;transition:opacity .3s linear}
.cable.hot .rope{stroke:var(--gold);opacity:.95}
.cable.hot .flow{opacity:.9;animation-duration:.8s}
@keyframes ropeflow{from{stroke-dashoffset:42}to{stroke-dashoffset:0}}
""" + c[b:]
c = re.sub(r'\n  \.cables\{display:none\}', '', c)
c = c.replace("  .deskgrid{grid-template-columns:minmax(0,1fr);gap:calc(var(--cell)*1.2)}", "  .row{gap:clamp(40px,8vw,70px)}")
# graph delta with a spade
c = must(c, """.delta{font-family:var(--title);font-weight:800;letter-spacing:-.04em;line-height:1;
  font-size:clamp(2rem,4.2vw,3.4rem);color:var(--gold-ink);opacity:0;transform:translateY(10px);""",
""".delta{display:flex;align-items:center;gap:.18em;font-family:var(--title);font-weight:800;letter-spacing:-.04em;line-height:1;
  font-size:clamp(2rem,4.2vw,3.4rem);color:var(--gold-ink);opacity:0;transform:translateY(10px);""")
c = must(c, ".viz.more .delta{opacity:1;transform:none}", ".viz.more .delta{opacity:1;transform:none}\n.delta svg{width:1.15em;height:1.15em;flex:none}\n.viz.live .bars .mk path{transition:transform .22s cubic-bezier(.16,1,.3,1)}")
# why us: grow out of the list, smoothly, breathe, fade the others
a = c.index('.whyband .suit{width:100%;height:auto;color:var(--ink);opacity:.85;'); b = c.index('.whyband .t{')
c = c[:a] + """.whyband .suit{width:100%;height:auto;color:var(--ink);opacity:.85;overflow:visible;
  transform-origin:100% 50%;
  transition:opacity .6s var(--ease),transform .7s cubic-bezier(.16,1,.3,1),color .6s var(--ease)}
.js .whyband .suit{opacity:.2}
.js .whyband.on .suit{opacity:.85}
.whyband .suit path{transform-box:fill-box;transform-origin:center}
/* hover: the suit leaves its cell, grows to the left, settles, breathes. Never a snap. */
.whyband:hover,.whyband:focus-within{background:var(--cream-2);z-index:2}
.whyband:hover .suit,.whyband:focus-within .suit{opacity:1;color:var(--gold-ink);
  transform:translateX(-46%) scale(2.7)}
.whyband:hover .suit path,.whyband:focus-within .suit path{animation:breathe 3.4s ease-in-out .75s infinite}
@keyframes breathe{0%,100%{transform:scale(1)}50%{transform:scale(1.045)}}
.bands:hover .whyband:not(:hover):not(:focus-within){opacity:.55}
.whyband{transition:opacity .5s var(--ease),background .4s var(--ease)}
""" + c[b:]
c = c.replace("  .cable .flow,.whyband .suit{animation:none!important}", "  .cable .flow,.whyband .suit path{animation:none!important}")
# footer brand: the lockup itself, no typed word
c = must(c, ".footbrand svg{height:30px;width:auto;color:var(--white);display:block}", ".footbrand svg{height:32px;width:auto;color:var(--white);display:block}")
c = re.sub(r'\.footbrand span\{[^}]*\}\n?', '', c)
io.open(os.path.join(S, 'styles.css'), 'w', encoding='utf-8').write(c)
print('r6 patched')
