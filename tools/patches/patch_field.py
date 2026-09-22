import io
p='app.js'; s=io.open(p,encoding='utf-8').read()
start=s.index('function makeField(svg, opt) {'); end=s.index('var heroField = document.getElementById')
new=r'''function makeField(svg, opt) {
  var W = opt.w, H = opt.h;
  var wide = innerWidth > 860;
  var COUNT = wide ? opt.n : Math.min(opt.n, opt.nm);
  var EXTRA = wide ? Math.round(COUNT * .25) : 0;   /* density near the pointer */
  var BASE = opt.base, PEAK = opt.peak;
  var R = opt.r;
  /* shape is immediate (most of the way at 100 ms); the opacity ramp is slow
     on purpose: never 0.15 of opacity inside 50 ms, anywhere. */
  var WAKE_D = 220, FADE_UP = 880, HOLD = 1400, BACK = 640, FADE_DN = 1000;
  var SPAWN = 620, BORN = 900;
  var marks = [], frag = document.createDocumentFragment();

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

  var ANCH = opt.anchors || 0;              /* suits that live in the field */
  for (var i = 0; i < COUNT + EXTRA; i++) {
    var g = document.createElementNS(NS, 'g'), p = document.createElementNS(NS, 'path');
    p.setAttribute('fill', 'currentColor');
    p.setAttribute('d', PATHS.square);
    g.appendChild(p);
    if (i % 6 === 4) g.setAttribute('fill', '#A81A2C');
    frag.appendChild(g);
    var spare = i >= COUNT;
    var anchor = i < ANCH;                  /* one of each classic suit */
    if (anchor) {
      g.removeAttribute('fill');
      p.setAttribute('d', PATHS['smooth-' + SUITS[i]]);
    }
    var at = spot();
    var vx = rnd(-11, 11) * (anchor ? .45 : 1), vy = rnd(-8, 8) * (anchor ? .45 : 1);
    var size = anchor ? rnd(58, 78) : rnd(14, 40);
    marks.push({
      g: g, p: p, x: at.x, y: at.y, vx: vx, vy: vy, vx0: vx, vy0: vy,
      s: size, depth: size / 40,            /* bigger = closer = more parallax */
      rot: anchor ? rnd(-9, 9) : Math.random() * 360, vr: rnd(-7, 7) * (anchor ? .3 : 1),
      base: anchor ? BASE * 1.25 : BASE, peak: PEAK, t: anchor ? 1 : 0,
      o: spare ? 0 : (anchor ? BASE * 1.25 : BASE),
      born: Math.hypot(at.x - W / 2, at.y - H / 2) / Math.hypot(W / 2, H / 2) * 1100 + rnd(0, 260),
      phase: 'idle', at: 0, suit: anchor ? 'smooth-' + SUITS[i] : suit(),
      spare: spare, live: !spare, glow: false, anchor: anchor
    });
  }
  svg.appendChild(frag);

  var par = { x: 0, y: 0 };                 /* pointer parallax, eased */
  function place(m) {
    var px = m.x + par.x * 26 * m.depth, py = m.y + par.y * 18 * m.depth;
    m.g.setAttribute('transform', 'translate(' + px.toFixed(1) + ' ' + py.toFixed(1) +
      ') rotate(' + m.rot.toFixed(1) + ') scale(' + (m.s / 100).toFixed(4) + ') translate(-50 -50)');
  }
  marks.forEach(function (m) { m.g.setAttribute('opacity', m.o.toFixed(3)); place(m); });
  if (reduce) return;                       /* a static sparse set of squares */

  /* staged arrival: the field ripples outward from the copy on first sight */
  marks.forEach(function (m) { m.g.setAttribute('opacity', '0'); });

  var ptr = { x: -9e3, y: -9e3, on: false };
  var host = svg.parentNode;
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
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(measure);

  var running = false, t0 = 0;
  new IntersectionObserver(function (es) { running = es[0].isIntersecting; }, { threshold: 0 }).observe(host);

  var last = 0, spawnAt = 0, sy = 0;
  if (opt.scroll) addEventListener('scroll', function () { sy = scrollY; }, { passive: true });

  requestAnimationFrame(function tick(now) {
    requestAnimationFrame(tick);
    if (!running || document.hidden) { last = now; return; }
    var dt = last ? Math.min(.05, (now - last) / 1000) : 0; last = now;
    if (!t0) t0 = now;

    /* the whole field leans a little against the pointer, more for the near
       (large) marks: depth without a single blurred pixel */
    var tx = ptr.on ? (ptr.x - W / 2) / W : 0, ty = ptr.on ? (ptr.y - H / 2) / H : 0;
    par.x += (tx - par.x) * Math.min(1, 3 * dt); par.y += (ty - par.y) * Math.min(1, 3 * dt);
    if (opt.scroll) svg.style.transform = 'translate3d(0,' + (Math.min(sy, H) * .28).toFixed(1) + 'px,0)';

    /* density: wake a spare square into the pointer's neighbourhood, fading in */
    if (ptr.on && now - spawnAt > 200) {
      for (var s = 0; s < marks.length; s++) {
        var sp = marks[s];
        if (sp.spare && !sp.live) {
          var sx = ptr.x + rnd(-R * .7, R * .7), syy = ptr.y + rnd(-R * .7, R * .7);
          sx = Math.max(24, Math.min(W - 24, sx)); syy = Math.max(24, Math.min(H - 24, syy));
          if (inQuiet(sx, syy, 30)) break;   /* never born on the copy */
          sp.live = true; sp.at = now; sp.phase = 'spawn'; sp.o = 0; sp.born = 0;
          sp.x = sx; sp.y = syy;
          spawnAt = now;
          break;
        }
      }
    }

    for (var i = 0; i < marks.length; i++) {
      var m = marks[i];
      if (!m.live) continue;
      var ent = Math.min(1, Math.max(0, (now - t0 - m.born) / BORN));  /* arrival */
      if (ent <= 0) continue;

      var dpx = ptr.x - m.x, dpy = ptr.y - m.y, dp = Math.hypot(dpx, dpy);
      var near = ptr.on && dp < R;

      /* the pointer pulls: near marks lean in, so the hand is felt at once */
      if (near && dp > 36 && !m.anchor) {
        var pull = (1 - dp / R) * 240 * dt;
        m.vx += dpx / dp * pull; m.vy += dpy / dp * pull;
      }
      /* and everything relaxes back to its own drift */
      m.vx += (m.vx0 - m.vx) * Math.min(1, 1.6 * dt);
      m.vy += (m.vy0 - m.vy) * Math.min(1, 1.6 * dt);

      m.x += m.vx * dt; m.y += m.vy * dt; m.rot += m.vr * dt;
      if (m.x < 20 || m.x > W - 20) { m.vx *= -1; m.vx0 *= -1; }
      if (m.y < 20 || m.y > H - 20) { m.vy *= -1; m.vy0 *= -1; }

      /* the quiet zones: the copy is never covered. A mark that drifts onto a
         line is eased out and dims on the way in, so nothing ever sits on a
         word at strength. */
      var hush = 1, z = inQuiet(m.x, m.y);
      if (z) {
        var cx = (z.x0 + z.x1) / 2, cy = (z.y0 + z.y1) / 2;
        var dx = m.x - cx, dy = (m.y - cy) * 2.2, d = Math.hypot(dx, dy) || 1;
        m.vx += (dx / d) * 150 * dt; m.vy += (dy / d) * 150 * dt;
        var deep = Math.min(m.x - z.x0, z.x1 - m.x, m.y - z.y0, z.y1 - m.y) / 60;
        hush = 1 - .85 * Math.min(1, Math.max(0, deep));
      }
      var spd = Math.hypot(m.vx, m.vy);
      if (spd > 60) { m.vx *= 60 / spd; m.vy *= 60 / spd; }

      var el = now - m.at;
      if (m.phase === 'spawn') {
        m.o = m.base * Math.min(1, el / SPAWN);
        if (el >= SPAWN) { m.phase = 'idle'; m.o = m.base; }
      }
      if (m.phase === 'idle' && near) {
        m.phase = 'wake'; m.at = now; el = 0;
        if (!m.anchor) m.suit = suit();
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
        m.o = m.peak - (m.peak - m.base) * Math.min(1, el / FADE_DN);
        if (el >= FADE_DN) {
          m.phase = 'idle'; m.t = 0; m.o = m.base;
          if (m.spare) { m.live = false; m.o = 0; }
        }
      }

      if (m.anchor) m.t = 1;                 /* a suit that never goes back */
      else if (m.phase !== 'idle' || m.t > 0) m.p.setAttribute('d', mix(m.suit, m.t));
      var wantGlow = m.t > .86;
      if (wantGlow !== m.glow) { m.glow = wantGlow; m.g.classList.toggle('glow', wantGlow); }
      m.g.setAttribute('opacity', (m.o * hush * ent).toFixed(3));
      place(m);
    }
  });
}

'''
s=s[:start]+new+s[end:]
old_hero='''  w: 1600, h: 900, n: 60, nm: 25, base: .20, peak: .84, r: 235,
  quiet: { x0: 330, x1: 1270, y0: 215, y1: 700 }
});'''
assert old_hero in s
s=s.replace(old_hero,'''  w: 1600, h: 900, n: 60, nm: 25, base: .20, peak: .84, r: 260, scroll: true,
  text: [].slice.call(document.querySelectorAll('.hero .wrap > *')),
  quiet: { x0: 330, x1: 1270, y0: 215, y1: 700 }
});''')
old_close='''    anchors: 4, quiet: { x0: 450, x1: 1150, y0: 130, y1: 510 } });'''
assert old_close in s
s=s.replace(old_close,'''    anchors: 4, text: [].slice.call(svg.parentNode.querySelectorAll('.wrap > *')),
    quiet: { x0: 450, x1: 1150, y0: 130, y1: 510 } });''')
io.open(p,'w',encoding='utf-8').write(s)
print('patched')
