import io, re

# ---------------- app.js: rope physics replaces the elbow legs ----------------
p = 'app.js'; s = io.open(p, encoding='utf-8').read()
a = s.index('  /* Each card is wired to its note with an orthogonal elbow')
b = s.index('  function link() {')
ropes = r'''  /* Each card hangs a cable to its note. Real slack, real gravity: the
     cables settle, dangle, and can be brushed or dragged by the pointer.
     A verlet rope per card, drawn as one smooth path, with a gold current
     running toward the note. */
  var ropes = [], ropeSvg = null, grabbed = null, ropeRun = false, ropeLast = 0;
  var N = 26, GRAV = 1500, DAMP = .985, ITER = 4;

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
    if (innerWidth <= 900) return;
    var host = desk.getBoundingClientRect();
    ropeSvg = document.createElementNS(NS, 'svg');
    ropeSvg.setAttribute('class', 'ropes');
    ropeSvg.setAttribute('width', host.width); ropeSvg.setAttribute('height', host.height);
    ropeSvg.setAttribute('viewBox', '0 0 ' + host.width + ' ' + host.height);
    cables.appendChild(ropeSvg);

    var rows = minis.map(function (m) {
      var note = notes.querySelector('.note[data-fn="' + m.dataset.fn + '"]');
      if (!note) return null;
      var a1 = m.getBoundingClientRect(), b1 = note.getBoundingClientRect();
      return { fn: m.dataset.fn,
        x1: a1.right - host.left - 6, y1: a1.top + a1.height * .5 - host.top,
        x2: b1.left - host.left + 12, y2: b1.top + 26 - host.top };
    }).filter(Boolean).sort(function (p, q) { return p.y2 - q.y2; });

    rows.forEach(function (r, i) {
      var g = document.createElementNS(NS, 'g');
      g.setAttribute('class', 'cable'); g.dataset.fn = r.fn;
      var base = document.createElementNS(NS, 'path'), flow = document.createElementNS(NS, 'path');
      base.setAttribute('class', 'rope'); base.setAttribute('pathLength', '1');
      flow.setAttribute('class', 'flow');
      g.appendChild(base); g.appendChild(flow); ropeSvg.appendChild(g);

      /* slack grows with the index so no two cables hang on the same curve */
      var span = Math.hypot(r.x2 - r.x1, r.y2 - r.y1);
      var len = span * (1.10 + i * .045), seg = len / (N - 1), pts = [];
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
  var hotRope = null;
  desk.addEventListener('pointermove', function (e) {
    if (!ropes.length) return;
    var l = ropeLocal(e); ptrR.x = l.x; ptrR.y = l.y; ptrR.on = true;
    if (grabbed) { grabbed.rope.pts[grabbed.i].x = l.x; grabbed.rope.pts[grabbed.i].y = l.y; return; }
    var nb = nearest(l.x, l.y, 30);
    var fn = nb ? nb.rope.fn : null;
    if (fn !== hotRope) { if (hotRope) hot(hotRope, false); if (fn) hot(fn, true); hotRope = fn; }
    desk.style.cursor = nb ? 'grab' : '';
  }, { passive: true });
  desk.addEventListener('pointerleave', function () {
    ptrR.on = false; ptrR.x = ptrR.y = -1e4;
    if (hotRope) { hot(hotRope, false); hotRope = null; }
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
            if (d < 44 && d > 0) { var f = (1 - d / 44) * 2.2; p.x += dx / d * f; p.y += dy / d * f; }
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

'''
s = s[:a] + ropes + s[b:]
old_link = '''  function link() {
    function hot(fn, on) {
      desk.querySelectorAll('[data-fn]').forEach(function (el) {
        if (el.dataset.fn === fn) el.classList.toggle('hot', on);
      });
    }
'''
assert old_link in s
s = s.replace(old_link, '  function link() {\n')
s = s.replace("    notes.innerHTML = ''; cables.innerHTML = '';", "    notes.innerHTML = ''; cables.innerHTML = ''; ropes = []; grabbed = null;")
io.open(p, 'w', encoding='utf-8').write(s)

# ---------------- styles.css ----------------
c = io.open('styles.css', encoding='utf-8').read()
old_c = c[c.index('.cables{position:absolute;inset:0;pointer-events:none;z-index:0}'):c.index('.cable.hot{opacity:1;color:var(--gold)}') + len('.cable.hot{opacity:1;color:var(--gold)}')]
new_c = '''.cables{position:absolute;inset:0;pointer-events:none;z-index:0}
.deskgrid{position:relative;z-index:1}
.ropes{position:absolute;inset:0;width:100%;height:100%;overflow:visible;display:block}
.cable .rope{fill:none;stroke:var(--on-felt-dim);stroke-width:5;stroke-linecap:round;opacity:.5;
  stroke-dasharray:1;stroke-dashoffset:1;
  transition:opacity .3s var(--ease),stroke .3s var(--ease),stroke-dashoffset 1s var(--ease)}
.cable.in .rope{stroke-dashoffset:0}
.cable .flow{fill:none;stroke:var(--gold);stroke-width:5;stroke-linecap:round;opacity:0;
  stroke-dasharray:12 30;animation:ropeflow 1.4s linear infinite;
  transition:opacity .6s linear .7s}
.cable.in .flow{opacity:.32}
.cable.hot .rope{stroke:var(--gold);opacity:.9}
.cable.hot .flow{opacity:.95;animation-duration:.8s;transition-delay:0s}
@keyframes ropeflow{from{stroke-dashoffset:42}to{stroke-dashoffset:0}}
.desk{touch-action:pan-y}'''
c = c.replace(old_c, new_c)
c = c.replace('.rule.drift,.cable{animation:none!important}', '.rule.drift,.cable .flow{animation:none!important}')

# why-us: nothing grows on hover. Proof line and rule are always there.
old_w = c[c.index('.whyband .pf{margin-top:.35em'):c.index('.note.hot{')]
new_w = '''.whyband .pf{margin-top:.45em;color:var(--ink-dim);font-size:clamp(.98rem,1.25vw,1.1rem)}
.whyband .rule{margin-top:.6em;color:var(--ink);opacity:.22;
  transition:opacity .5s linear,color .5s linear,clip-path .9s var(--ease)}
.js .whyband .rule{clip-path:inset(0 100% 0 0)}
.js .whyband.on .rule{clip-path:inset(0 0 0 0)}
.whyband:hover .rule,.whyband:focus-within .rule{opacity:.8;color:var(--gold-ink)}

'''
c = c.replace(old_w, new_w)
c = c.replace('  .whyband .pf{max-height:none;opacity:1;margin-top:.5em}\n', '')
io.open('styles.css', 'w', encoding='utf-8').write(c)
print('ok')
