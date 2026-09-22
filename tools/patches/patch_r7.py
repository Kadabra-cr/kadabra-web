import io, os, re
os.chdir(os.path.dirname(os.path.abspath(__file__)))
S = '..'
js = io.open('app.src.js', encoding='utf-8').read()
h = io.open('shell.html', encoding='utf-8').read()
c = io.open(os.path.join(S, 'styles.css'), encoding='utf-8').read()

def must(s, old, new, count=1):
    assert old in s, old[:90]
    return s.replace(old, new, count)

# ======================= A. the heart is made of the marks it swallows =======================
js = must(js, """  var heart = { g: document.createElementNS(NS, 'g'), p: document.createElementNS(NS, 'path'),
                charge: 0, x: W / 2, y: H / 2 };""",
"""  var heart = { g: document.createElementNS(NS, 'g'), p: document.createElementNS(NS, 'path'),
                mass: 0, held: [], x: W / 2, y: H / 2, vx: 0, vy: 0, sc: 0, o: 0, relAt: 0 };""")
a = js.index("    /* how crowded is the hand? */"); b = js.index("    for (var i = 0; i < marks.length; i++) {\n      var m = marks[i];\n      if (!m.live) continue;\n      var ent =")
js = js[:a] + r"""    /* the gathering: the marks the hand draws in are swallowed one by one into a
       heart that is made of them. A hand that leaves, or moves faster than the
       heart can follow, lets it come apart: each mark climbs back out. */
    var hr = heart.mass ? 16 + Math.sqrt(heart.mass) * 14 : 0;      /* heart radius, field units */
    var far = Math.hypot(ptr.x - heart.x, ptr.y - heart.y);
    var feeding = ptr.on && (heart.mass === 0 || far < 170);
    if (heart.mass === 0) { heart.x = ptr.on ? ptr.x : heart.x; heart.y = ptr.on ? ptr.y : heart.y; heart.vx = heart.vy = 0; }
    else {
      /* a heavier heart follows the hand more slowly: spring and drag, so a
         quick hand simply gets away from it */
      var k = 30 / (1 + heart.mass * .14), drag = 5.5;
      var ax = feeding ? (ptr.x - heart.x) * k : 0, ay = feeding ? (ptr.y - heart.y) * k : 0;
      heart.vx += (ax - heart.vx * drag) * dt; heart.vy += (ay - heart.vy * drag) * dt;
      heart.x += heart.vx * dt; heart.y += heart.vy * dt;
    }
    if (heart.mass > 0 && !feeding && now - heart.relAt > 110) {
      var mr = heart.held.pop(); heart.mass--; heart.relAt = now;
      var ang = Math.random() * Math.PI * 2, sp0 = rnd(26, 54);
      mr.x = heart.x + Math.cos(ang) * hr * .45; mr.y = heart.y + Math.sin(ang) * hr * .45;
      mr.vx = Math.cos(ang) * sp0 + heart.vx * .4; mr.vy = Math.sin(ang) * sp0 + heart.vy * .4;
      mr.live = true; mr.held = false; mr.phase = 'spawn'; mr.at = now; mr.o = 0; mr.born = 0; mr.t = 0;
      mr.p.setAttribute('d', PATHS.square);
      if (mr.glow) { mr.glow = false; mr.g.classList.remove('glow'); }
    }
    heart.sc += ((heart.mass ? hr * 2 : 0) - heart.sc) * Math.min(1, 4 * dt);
    heart.o += ((heart.mass ? .94 : 0) - heart.o) * Math.min(1, 2.2 * dt);   /* never a flash */
    heart.g.setAttribute('opacity', heart.o.toFixed(3));
    heart.g.setAttribute('transform', 'translate(' + heart.x.toFixed(1) + ' ' + heart.y.toFixed(1) +
      ') scale(' + (heart.sc / 100).toFixed(4) + ') translate(-50 -50)');
    var tx0 = heart.mass ? heart.x : ptr.x, ty0 = heart.mass ? heart.y : ptr.y;   /* what pulls */

""" + js[b:]
js = must(js, """      /* the pointer pulls: near marks lean in, so the hand is felt at once */
      if (near && dp > 30 && !m.anchor) {
        var pull = (1 - dp / R) * (380 + heart.charge * 500) * dt;
        m.vx += dpx / dp * pull; m.vy += dpy / dp * pull;
      }""", """      /* the pointer pulls: near marks lean in, so the hand is felt at once.
         Once a heart exists, it is the heart that pulls. */
      var dhx = tx0 - m.x, dhy = ty0 - m.y, dh = Math.hypot(dhx, dhy) || 1;
      if (near && !m.anchor && dh > 4) {
        var pull = (1 - Math.min(1, dh / R)) * (380 + heart.mass * 60) * dt;
        m.vx += dhx / dh * pull; m.vy += dhy / dh * pull;
      }""")
js = must(js, """      /* a mark that feeds the heart fades into it */
      if (heart.charge > 0 && !m.anchor) {
        var dh = Math.hypot(m.x - heart.x, m.y - heart.y);
        if (dh < 96) hush *= 1 - heart.charge * (1 - dh / 96);
      }""", """      /* a mark on its way into the heart dims as it arrives, then is swallowed:
         it is gone from the field and the heart grows by one */
      if (feeding && !m.anchor && heart.mass < 14 && m.phase !== 'spawn') {
        var eat = Math.max(22, hr * .55);
        if (dh < eat + 44) hush *= Math.max(0, Math.min(1, (dh - eat) / 44));
        if (dh < eat) {
          m.live = false; m.held = true; m.o = 0; m.g.setAttribute('opacity', '0');
          heart.held.push(m); heart.mass++;
          continue;
        }
      }""")

# ======================= B. graph: quicker, bigger, percentages, a story on the right =======================
js = must(js, "  var COLS = 10, CW = 20, CH = 21, SZ = 16, H = 14 * CH;", "  var COLS = 10, CW = 22, CH = 23, SZ = 19, H = 14 * CH;")
js = must(js, "    A.concat(B.slice(0, 100)).forEach(function (c) { c.g.style.transitionDelay = (c.row * 55) + 'ms'; });",
              "    A.concat(B.slice(0, 100)).forEach(function (c) { c.g.style.transitionDelay = (c.row * 22) + 'ms'; });")
js = must(js, "      B.slice(0, 100).forEach(function (c) { morphPath(c.p, 'smooth-spade', 520, c.row * 60 + (c.n % COLS) * 12); });\n    }, 1300);",
              "      B.slice(0, 100).forEach(function (c) { morphPath(c.p, 'smooth-spade', 420, c.row * 28 + (c.n % COLS) * 7); });\n    }, 650);")
js = must(js, "        c.g.style.transitionDelay = (i * 22) + 'ms';\n      });\n      viz.classList.add('more');\n      setTimeout(function () { live = true; viz.classList.add('live'); }, 1400);\n    }, 2900);",
              "        c.g.style.transitionDelay = (i * 16) + 'ms';\n      });\n      viz.classList.add('more');\n      setTimeout(function () { live = true; viz.classList.add('live'); }, 900);\n    }, 1600);")
# hover: squares only lose their transparency; spades swell; the big spade too
js = must(js, """      if (!bev) { cells.forEach(function (cc) { cc.p.style.transform = ''; }); return; }""",
"""      if (!bev) { cells.forEach(function (cc) { cc.p.style.transform = ''; cc.p.style.fillOpacity = ''; }); return; }""")
js = must(js, """        if (d > RR) { if (cc.p.style.transform) cc.p.style.transform = ''; return; }
        var f = 1 - d / RR, sc = 1 + (strong ? .75 : .18) * f, sh = (strong ? 2.2 : 3.4) * f;
        cc.p.style.transform = 'translate(' + (dx / (d || 1) * sh).toFixed(2) + 'px,' + (dy / (d || 1) * sh).toFixed(2) +
          'px) scale(' + sc.toFixed(3) + ')';""",
"""        if (d > RR) { if (cc.p.style.transform) cc.p.style.transform = ''; if (cc.p.style.fillOpacity) cc.p.style.fillOpacity = ''; return; }
        var f = 1 - d / RR;
        if (!strong) { cc.p.style.fillOpacity = (.42 + .58 * f).toFixed(3); return; }
        var sc = 1 + .75 * f, sh = 2.2 * f;
        cc.p.style.transform = 'translate(' + (dx / (d || 1) * sh).toFixed(2) + 'px,' + (dy / (d || 1) * sh).toFixed(2) +
          'px) scale(' + sc.toFixed(3) + ')';""")
js = must(js, """  bars.addEventListener('pointermove', function (e) { bev = e; if (!braf) braf = requestAnimationFrame(influence); }, { passive: true });""",
"""  var bigSpade = document.querySelector('.delta svg');
  function influenceBig() {
    if (!bigSpade) return;
    if (!bev) { bigSpade.style.transform = ''; return; }
    var r = bigSpade.getBoundingClientRect(), d = Math.hypot(bev.clientX - (r.left + r.width / 2), bev.clientY - (r.top + r.height / 2));
    var f = Math.max(0, 1 - d / 150);
    bigSpade.style.transform = f ? 'scale(' + (1 + .6 * f).toFixed(3) + ')' : '';
  }
  var influence0 = influence;
  influence = function () { influence0(); influenceBig(); };
  bars.addEventListener('pointermove', function (e) { bev = e; if (!braf) braf = requestAnimationFrame(influence); }, { passive: true });""")

# ======================= C. the nudge shows both sides =======================
js = must(js, "    deck.insertAdjacentHTML('beforeend',\n      '<svg class=\"hintarrow\" viewBox=\"0 0 28 64\" aria-hidden=\"true\"><use href=\"#chevron\"/></svg>');",
              "    deck.insertAdjacentHTML('beforeend',\n      '<svg class=\"hintarrow\" viewBox=\"0 0 28 64\" aria-hidden=\"true\"><use href=\"#chevron\"/></svg>' +\n      '<svg class=\"hintarrow l\" viewBox=\"0 0 28 64\" aria-hidden=\"true\"><use href=\"#chevron\"/></svg>');")
js = must(js, "  var idx = 0, els = [], minis = [], drag = null, done = false, touched = false, nudgeTimer = 0;",
              "  var idx = 0, els = [], minis = [], drag = null, done = false, touched = false, nudgeTimer = 0, nudgeSide = 1;")
js = must(js, """      el.style.transition = '';
      el.classList.add('nudging');
      deck.classList.add('hinting');
      pileR.classList.add('nudge');
      pileL.classList.add('nudge');
      setTimeout(function () {
        el.classList.remove('nudging');
        deck.classList.remove('hinting');
        pileR.classList.remove('nudge');
        pileL.classList.remove('nudge');""", """      el.style.transition = '';
      var right = nudgeSide > 0; nudgeSide = -nudgeSide;   /* one side, then the other */
      el.classList.add(right ? 'nudging' : 'nudging-l');
      deck.classList.add(right ? 'hinting' : 'hinting-l');
      (right ? pileR : pileL).classList.add('nudge');
      setTimeout(function () {
        el.classList.remove('nudging', 'nudging-l');
        deck.classList.remove('hinting', 'hinting-l');
        pileR.classList.remove('nudge');
        pileL.classList.remove('nudge');""")
js = must(js, """    deck.classList.remove('hinting');
    pileR.classList.remove('nudge');
    pileL.classList.remove('nudge');
    els.forEach(function (el) { el.classList.remove('nudging'); });""", """    deck.classList.remove('hinting', 'hinting-l');
    pileR.classList.remove('nudge');
    pileL.classList.remove('nudge');
    els.forEach(function (el) { el.classList.remove('nudging', 'nudging-l'); });""")

# ======================= D. the desk: cards turn landscape =======================
js = must(js, """    SLOT.w = Math.round(dr.width * (narrow ? .42 : .5)); SLOT.h = Math.round(dr.height * (narrow ? .42 : .5));
    var sc = SLOT.w / dr.width;""", """    var wrapW = desk.getBoundingClientRect().width;
    SLOT.w = Math.round(Math.min(narrow ? wrapW : 420, wrapW * (narrow ? 1 : .42))); SLOT.h = Math.round(SLOT.w * .6);
    var sc = SLOT.w / dr.width;""")
js = must(js, """      el.style.width = dr.width + 'px'; el.style.height = dr.height + 'px';
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
    }); });""", """      el.style.transition = 'none';
      el.style.transform = 'none';
      if (reduce) { el.style.width = SLOT.w + 'px'; el.style.height = SLOT.h + 'px'; }
      else { el.style.width = dr.width + 'px'; el.style.height = dr.height + 'px'; }
      minis.push(slot);
    });
    /* last: where they are now (still portrait, at the slot's corner), then play
       from the pile to the row while the card turns landscape */
    els.forEach(function (el, i) {
      if (reduce) return;
      var l = el.getBoundingClientRect(), f = first[i];
      el.style.transform = 'translate(' + (f.left - l.left) + 'px,' + (f.top - l.top) + 'px) scale(' +
        (f.width / l.width) + ')';
    });
    reveal.hidden = false;
    if (reduce) { drawCables(); return; }
    requestAnimationFrame(function () { requestAnimationFrame(function () {
      els.forEach(function (el, i) {
        var d = (i * 90) + 'ms', e = ' .9s cubic-bezier(.16,1,.3,1) ';
        el.style.transition = 'transform' + e + d + ', width' + e + d + ', height' + e + d;
        el.style.transform = 'none';
        el.style.width = SLOT.w + 'px'; el.style.height = SLOT.h + 'px';
      });
      setTimeout(drawCables, 900 + els.length * 90 + 250);
    }); });""")
js = must(js, """      var rest = 'translateY(' + (i * 6) + 'px) scale(' + (1 - i * 0.02).toFixed(3) + ')';
      el.dataset.rest = rest; el.style.setProperty('--rest', rest);
      el.style.transition = 'none'; el.style.transform = rest;""", """      var rest = 'translateY(' + (i * 6) + 'px) scale(' + (1 - i * 0.02).toFixed(3) + ')';
      el.dataset.rest = rest; el.style.setProperty('--rest', rest);
      el.style.transition = 'none'; el.style.transform = reduce ? rest : 'none';""")
js = must(js, """      els.forEach(function (el, i) {
        var l = el.getBoundingClientRect(), f = first[i];
        el.style.transform = 'translate(' + (f.left - l.left) + 'px,' + (f.top - l.top) + 'px) scale(' + (f.width / l.width) + ')';
      });
      requestAnimationFrame(function () { requestAnimationFrame(function () {
        els.forEach(function (el, i) {
          el.style.transition = 'transform .8s cubic-bezier(.16,1,.3,1) ' + ((els.length - i) * 60) + 'ms';
          el.style.transform = el.dataset.rest;
        });
      }); });""", """      var dk = deck.getBoundingClientRect();
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
      }); });""")
io.open('app.src.js', 'w', encoding='utf-8').write(js)

# ======================= SHELL =======================
a = h.index('      <div class="bars" id="bars"'); b = h.index('    </div>\n  </div>\n</section>', a)
h = h[:a] + """      <div class="vizgrid">
        <div class="bars" id="bars" role="img" aria-label="Two bars made of marks. Squares for people working it out alone, spades for people taught first. The spade bar is thirty-four percent taller.">
          <figure class="barcol base">
            <svg id="barA" aria-hidden="true"></svg>
            <figcaption><span>Working it out alone</span></figcaption>
          </figure>
          <figure class="barcol taught">
            <p class="delta" aria-hidden="true"><svg viewBox="0 0 100 100"><use href="#classic-spade"/></svg><span>+34%</span></p>
            <svg id="barB" aria-hidden="true"></svg>
            <figcaption><span>Taught first</span></figcaption>
          </figure>
        </div>
        <div class="story">
          <p class="beat-l" data-beat="in">The same hundred people, twice.</p>
          <p class="beat-l" data-beat="taught">One group is taught to use AI on its own work first.</p>
          <p class="beat-l" data-beat="more">That group gets up to a third more done.</p>
          <p class="aside">And today only <b>47%</b> of people at work were ever taught to use AI at all.</p>
          <div class="cites">
            <p class="src">+34% for taught beginners &mdash; Brynjolfsson, Li &amp; Raymond, NBER 31161, 2023</p>
            <p class="src">47% trained &mdash; KPMG &times; Melbourne Business School, 2025</p>
          </div>
        </div>
      </div>
""" + h[b:]
h = must(h, "<p class=\"t\">We grew up with these tools.</p>", "<p class=\"t\">First in, not catching up.</p>")
io.open('shell.html', 'w', encoding='utf-8').write(h)

# ======================= CSS =======================
c = must(c, ".viz>.rule{--rt:4px;margin-top:.25em;color:var(--ink);opacity:.9}\n.viz .lede{color:var(--ink-dim);margin-top:.5em}",
            ".viz>.rule{--rt:4px;margin-top:.35em;color:var(--ink);opacity:.9}\n.viz .lede{color:var(--ink-dim);margin-top:1.3em;max-width:54ch}")
c = must(c, ".bars{display:grid;grid-template-columns:repeat(2,minmax(0,220px));gap:clamp(28px,6vw,90px);\n  align-items:end;margin-top:calc(var(--cell)*1.3)}",
            ".vizgrid{display:grid;grid-template-columns:minmax(0,1.05fr) minmax(0,1fr);gap:clamp(40px,7vw,120px);align-items:end;margin-top:calc(var(--cell)*1.4)}\n.bars{display:grid;grid-template-columns:repeat(2,minmax(0,260px));gap:clamp(24px,4vw,60px);align-items:end}")
c = must(c, ".barcol figcaption{display:grid;line-height:1.15}", ".barcol figcaption{display:grid;line-height:1.15;font-weight:600;color:var(--ink)}")
c = must(c, ".barcol figcaption span{color:var(--ink-dim);font-size:.95rem}", ".barcol figcaption span{font-size:1rem}\n.barcol.taught figcaption span{color:var(--gold-ink)}\n.barcol.base .mk path{fill-opacity:.42;transition:fill-opacity .2s linear}")
c = must(c, ".delta svg{width:1.15em;height:1.15em;flex:none}", ".delta svg{width:1.15em;height:1.15em;flex:none;transition:transform .25s cubic-bezier(.16,1,.3,1);transform-origin:center}")
c = must(c, ".aside{margin-top:calc(var(--cell)*1.1);color:var(--ink-dim);font-size:clamp(1.02rem,1.35vw,1.16rem);max-width:52ch}",
""".story{display:grid;gap:.7em;align-content:end}
.beat-l{font-family:var(--title);font-weight:800;letter-spacing:-.03em;line-height:1.08;
  font-size:clamp(1.35rem,2.4vw,2rem);color:var(--ink);opacity:.18;transform:translateY(8px);
  transition:opacity .6s linear,transform .7s cubic-bezier(.16,1,.3,1)}
.viz.in .beat-l[data-beat=in],.viz.taught .beat-l[data-beat=taught],.viz.more .beat-l[data-beat=more]{opacity:1;transform:none}
.beat-l[data-beat=more]{color:var(--gold-ink)}
.aside{margin-top:calc(var(--cell)*.9);color:var(--ink-dim);font-size:clamp(1.02rem,1.35vw,1.16rem);max-width:52ch}""")
c = c.replace("  .bars{grid-template-columns:repeat(2,minmax(0,1fr))}", "  .bars{grid-template-columns:repeat(2,minmax(0,1fr))}\n  .vizgrid{grid-template-columns:minmax(0,1fr)}")
# nudge: both sides
c = must(c, ".card.nudging{animation:nudgeR 1.5s var(--ease) both}",
""".card.nudging{animation:nudgeR 1.5s var(--ease) both}
@keyframes nudgeL{0%{transform:var(--rest)}
  45%{transform:translateX(-38px) rotate(-3.4deg)}100%{transform:var(--rest)}}
.card.nudging-l{animation:nudgeL 1.5s var(--ease) both}""")
c = must(c, ".deck.hinting .hintarrow{opacity:.95;transform:translateY(-50%) translateX(0)}",
""".deck.hinting .hintarrow:not(.l){opacity:.95;transform:translateY(-50%) translateX(0)}
.hintarrow.l{right:auto;left:-46px;transform:translateY(-50%) rotate(180deg) translateX(-10px)}
.deck.hinting-l .hintarrow.l{opacity:.95;transform:translateY(-50%) rotate(180deg) translateX(0)}""")
# landscape desk cards
c = must(c, ".slot .card{transform-origin:0 0;inset:auto;left:0;top:0;cursor:default;box-shadow:0 18px 36px -22px rgba(0,0,0,.95)}",
""".slot .card{transform-origin:0 0;inset:auto;left:0;top:0;cursor:default;box-shadow:0 18px 36px -22px rgba(0,0,0,.95)}
.card.desk .cband{font-size:clamp(1rem,1.25vw,1.12rem);padding:1.1em 1.4em;font-weight:600}
.card.desk .pip{width:34%}
.card.desk .ix{font-size:.95rem}""")
c = must(c, ".row{display:grid;grid-template-columns:auto minmax(0,1fr);gap:clamp(90px,12vw,170px);align-items:center;",
            ".row{display:grid;grid-template-columns:auto minmax(0,1fr);gap:clamp(70px,9vw,130px);align-items:center;")
io.open(os.path.join(S, 'styles.css'), 'w', encoding='utf-8').write(c)
print('r7 patched')
