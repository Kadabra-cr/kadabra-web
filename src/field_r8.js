/* ==========================================================================
   THE FIELD: sparse drifting squares that wake, morph and gather into a
   heart made of them. Grow it and the words come for it. Used by the hero
   and the closing CTA: one engine, same rules, top and bottom.
   ========================================================================== */
function makeField(svg, opt) {
  var W = opt.w, H = opt.h;
  var wide = innerWidth > 860;
  var COUNT = wide ? opt.n : Math.min(opt.n, opt.nm);
  var EXTRA = wide ? Math.round(COUNT * .35) : Math.round(COUNT * .2);  /* density near the pointer */
  var BASE = opt.base, PEAK = opt.peak;
  var R = opt.r;
  /* shape is immediate (most of the way at 100 ms); the opacity ramp is slow
     on purpose: never 0.15 of opacity inside 50 ms, anywhere. */
  var WAKE_D = 160, FADE_UP = 700, HOLD = 1300, BACK = 520, FADE_DN = 900;
  var SPAWN = 620, BORN = 900;
  var CAP = 40;                              /* marks in a full heart: 100% */
  var REBIRTH = 20000;                       /* ms of reading after a defeat */
  var LIVES = 3;                             /* three hits and it is over, whatever the size */
  var marks = [], frag = document.createDocumentFragment();
  var host = svg.parentNode;

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
  function seed(m) {
    var at = spot();
    m.x = at.x; m.y = at.y;
    m.vx = m.vx0 = rnd(-11, 11); m.vy = m.vy0 = rnd(-8, 8);
    m.rot = Math.random() * 360; m.vr = rnd(-7, 7);
    m.t = 0; m.o = 0; m.phase = 'idle'; m.at = 0; m.held = false; m.live = !m.spare; m.freeTil = 0; m.hs = 1;
    m.born = Math.hypot(at.x - W / 2, at.y - H / 2) / Math.hypot(W / 2, H / 2) * 1100 + rnd(0, 260);
    m.p.setAttribute('d', PATHS.square);
    if (m.glow) { m.glow = false; m.g.classList.remove('glow'); }
    m.g.setAttribute('opacity', '0');
  }

  for (var i = 0; i < COUNT + EXTRA; i++) {
    var g = document.createElementNS(NS, 'g'), p = document.createElementNS(NS, 'path');
    p.setAttribute('fill', 'currentColor');
    p.setAttribute('d', PATHS.square);
    g.appendChild(p);
    if (i % 6 === 4) g.setAttribute('fill', '#A81A2C');
    frag.appendChild(g);
    var spare = i >= COUNT, size = rnd(14, 40);
    var m = { g: g, p: p, s: size, sc: 1, depth: size / 40, base: BASE, peak: PEAK,
              suit: suit(), spare: spare, glow: false };
    seed(m);
    if (!spare) m.o = BASE;
    marks.push(m);
  }
  svg.appendChild(frag);

  /* the gathering: the marks the hand draws in are swallowed one by one into
     a heart that is made of them. It pulses with every one, reddens as it
     fills, and follows the hand: never glued to it, never left behind. */
  var heart = { g: document.createElementNS(NS, 'g'), p: document.createElementNS(NS, 'path'),
                mass: 0, held: [], x: W / 2, y: H / 2, vx: 0, vy: 0, sc: 0, o: 0, relAt: 0, eatAt: 0,
                pulse: 0, hurt: 0, debt: 0, burst: 0, fill: '' };
  heart.p.setAttribute('fill', '#FFFFFF'); heart.p.setAttribute('d', mix('smooth-heart', 1));
  heart.g.setAttribute('class', 'glow heartmark'); heart.g.setAttribute('opacity', '0');
  heart.g.appendChild(heart.p); svg.appendChild(heart.g);
  /* the war layer: fuel and sparks under the letters, letters over everything */
  var war = document.createElementNS(NS, 'g'); war.setAttribute('class', 'war'); svg.appendChild(war);
  var fuelG = document.createElementNS(NS, 'g'); war.appendChild(fuelG);
  var ltrG = document.createElementNS(NS, 'g'); war.appendChild(ltrG);
  var dots = [];
  for (var d = 0; d < 64; d++) {
    var c = document.createElementNS(NS, 'circle');
    c.setAttribute('r', '0'); c.setAttribute('opacity', '0'); fuelG.appendChild(c);
    dots.push({ el: c, on: false, x: 0, y: 0, vx: 0, vy: 0, t: 0, ttl: 1, r: 4, o: .5, fill: '' });
  }
  function puff(x, y, vx, vy, ttl, r, o, fill) {
    for (var i = 0; i < dots.length; i++) {
      var q = dots[i]; if (q.on) continue;
      q.on = true; q.x = x; q.y = y; q.vx = vx; q.vy = vy; q.t = 0; q.ttl = ttl; q.r = r; q.o = o;
      if (q.fill !== fill) { q.fill = fill; q.el.setAttribute('fill', fill); }
      return;
    }
  }
  function sparks(x, y, n, fill) {
    for (var i = 0; i < n; i++) {
      var a = Math.random() * Math.PI * 2, s = rnd(120, 360);
      puff(x, y, Math.cos(a) * s, Math.sin(a) * s, rnd(.35, .6), rnd(3, 6), .9, fill);
    }
  }

  var game = { phase: 'calm', armedAt: 0, wave: 0, nextWord: 0, word: null, deadAt: 0, offAt: 0, hits: 0 };
  svg.__field = { heart: heart, game: game, marks: marks, opt: opt };   /* for the checks */
  var WORDS = '@@t.game.words@@'.split(', ');
  var cv = document.createElement('canvas').getContext('2d');
  function fontReady() { return !document.fonts || document.fonts.check('800 100px Gabarito'); }
  if (document.fonts && document.fonts.load) document.fonts.load('800 100px Gabarito');

  /* a word laid out letter by letter, from real glyph widths, so it reads as
     one word before it comes apart */
  function layout(text) {
    var lines = text.indexOf(' ') > 0 && text.length > 9 ? text.split(' ') : [text];
    var fs = lines.length > 1 ? 50 : (text.length <= 8 ? 62 : Math.max(46, 62 * 8 / text.length));
    var maxW = W * .2, widest = 0;
    cv.font = '800 ' + fs + 'px Gabarito, sans-serif';
    lines.forEach(function (ln) { widest = Math.max(widest, cv.measureText(ln).width); });
    if (widest > maxW) fs *= maxW / widest;
    cv.font = '800 ' + fs + 'px Gabarito, sans-serif';
    var out = [], maxTx = 0;
    lines.forEach(function (ln, li) {
      var lw = cv.measureText(ln).width, y = (li - (lines.length - 1) / 2) * fs * .98;
      for (var i = 0; i < ln.length; i++) {
        var ch = ln.charAt(i); if (ch === ' ') continue;
        var x = -lw / 2 + cv.measureText(ln.slice(0, i)).width + cv.measureText(ch).width / 2;
        out.push({ ch: ch, tx: x, ty: y });
        maxTx = Math.max(maxTx, Math.abs(x));
      }
    });
    /* box half-extents, for placing the word clear of the copy */
    return { letters: out, fs: fs, halfW: maxTx + fs * .6, halfH: fs * (lines.length > 1 ? 1.1 : .6) };
  }
  function newWord(now) {
    var text = WORDS[game.wave % WORDS.length];
    var lay = layout(text);
    var refX = ptr.on ? ptr.x : heart.x;
    var side = refX < W / 2 ? 1 : -1;                 /* the far side from the hand */
    /* the field is cropped to the screen: place the word in what is seen */
    var bb = svg.getBoundingClientRect(), vw = bb.width / Math.max(bb.width / W, bb.height / H);
    var v0 = (W - vw) / 2, v1 = v0 + vw;
    var cx = side > 0 ? Math.min(v0 + vw * .84, v1 - 30 - lay.halfW) : Math.max(v0 + vw * .16, v0 + 30 + lay.halfW);
    var w = { side: side, cx: cx, cy: H / 2, x: cx + side * 200, at: now, letters: [], launched: 0, lastAt: 0,
              gap: Math.max(200, 380 - game.wave * 40), gone: 0, doneAt: 0 };
    w.readAt = now + 700 + Math.max(300, 650 - game.wave * 90) + 40 * lay.letters.length;
    lay.letters.forEach(function (l, i) {
      var t = document.createElementNS(NS, 'text');
      t.setAttribute('font-size', lay.fs.toFixed(1)); t.setAttribute('text-anchor', 'middle');
      t.setAttribute('dominant-baseline', 'central'); t.setAttribute('opacity', '0');
      t.textContent = l.ch; ltrG.appendChild(t);
      w.letters.push({ el: t, ch: l.ch, tx: l.tx, ty: l.ty, x: 0, y: 0, vx: 0, vy: 0, st: 'held', t0: 0, o: 0, i: i, fuelAt: 0 });
    });
    game.word = w;
  }
  function endWord() {
    if (!game.word) return;
    game.word.letters.forEach(function (l) { if (l.el.parentNode) ltrG.removeChild(l.el); });
    game.word = null;
  }
  function arm(now) {
    game.phase = 'armed'; game.armedAt = now; game.nextWord = now + 5000; game.wave = 0; game.hits = 0;
    host.classList.add('armed');
  }
  function disarm() { game.phase = 'calm'; host.classList.remove('armed'); endWord(); }
  var LIVE = opt.copy ? opt.copy.els.map(function (el) { return el.textContent; }) : null;
  function setCopy(lines) {
    if (!opt.copy) return;
    opt.copy.els.forEach(function (el, i) {
      if (el.textContent === lines[i]) return;
      el.classList.add('swapping');
      setTimeout(function () { el.textContent = lines[i]; el.classList.remove('swapping'); measure(); }, 320);
    });
    setTimeout(measure, 500);
  }
  var pointT = 0;
  function die(now) {
    game.phase = 'dead'; game.deadAt = now;
    clearTimeout(pointT);
    pointT = setTimeout(function () { if (game.phase === 'dead') host.classList.add('pointing'); }, 3000);
    host.classList.remove('armed'); host.classList.add('dead');
    endWord();
    sparks(heart.x, heart.y, 28, '#FFFFFF');
    while (heart.held.length) release(now, 520, 940);
    for (var i = 0; i < marks.length; i++) {
      var m = marks[i]; if (!m.live) continue;
      var dx = m.x - heart.x, dy = m.y - heart.y, dd = Math.hypot(dx, dy) || 1, s = rnd(520, 940);
      m.vx = dx / dd * s; m.vy = dy / dd * s; m.phase = 'gone'; m.freeTil = now + 3000;
      /* the visible keep their strength and fade out; the ones just let out
         of the heart rise briefly into view first: no flash either way */
      m.gt = m.o > .02 ? .3 : 0; m.go = m.o > .02 ? m.o : .55;
    }
    heart.burst = 1;
    setCopy(opt.copy ? opt.copy.dead : []);
  }
  function reborn(now) {
    clearTimeout(pointT);
    host.classList.remove('dead', 'pointing');
    if (LIVE) setCopy(LIVE);
    t0 = now; game.phase = 'calm'; game.wave = 0; game.word = null; game.hits = 0;
    heart.mass = 0; heart.held = []; heart.o = 0; heart.sc = 0; heart.burst = 0; heart.debt = 0;
    measure();
    marks.forEach(function (m) { seed(m); });
  }

  var par = { x: 0, y: 0 };                 /* pointer parallax, eased */
  function place(m) {
    var px = m.x + par.x * 26 * m.depth, py = m.y + par.y * 18 * m.depth;
    m.g.setAttribute('transform', 'translate(' + px.toFixed(1) + ' ' + py.toFixed(1) +
      ') rotate(' + m.rot.toFixed(1) + ') scale(' + (m.s * m.sc / 100).toFixed(4) + ') translate(-50 -50)');
  }
  marks.forEach(function (m) { m.g.setAttribute('opacity', m.o.toFixed(3)); place(m); });
  if (reduce) return;                       /* a static sparse set of squares */

  /* staged arrival: the field ripples outward from the copy on first sight */
  marks.forEach(function (m) { m.g.setAttribute('opacity', '0'); });

  var ptr = { x: -9e3, y: -9e3, on: false };
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
  /* the copy moves (condensed / armed / dead): re-measure now and once the
     transition has had time to settle */
  new MutationObserver(function () {
    measure(); setTimeout(measure, 500); setTimeout(measure, 1200);
  }).observe(host, { attributes: true, attributeFilter: ['class'] });
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(measure);

  var running = false, t0 = 0;
  new IntersectionObserver(function (es) { running = es[0].isIntersecting; }, { threshold: 0 }).observe(host);

  /* one held mark climbs back out of the heart */
  function release(now, s0, s1) {
    var mr = heart.held.pop(); if (!mr) return;
    heart.mass--; heart.relAt = now;
    var hr = 16 + Math.sqrt(heart.mass + 1) * 11;
    var ang = Math.random() * Math.PI * 2, sp0 = rnd(s0, s1);
    mr.x = heart.x + Math.cos(ang) * hr * .45; mr.y = heart.y + Math.sin(ang) * hr * .45;
    mr.vx = Math.cos(ang) * sp0 + heart.vx * .4; mr.vy = Math.sin(ang) * sp0 + heart.vy * .4;
    mr.live = true; mr.held = false; mr.phase = 'spawn'; mr.at = now; mr.o = 0; mr.born = 0; mr.t = 0;
    mr.freeTil = now + 500;
    mr.p.setAttribute('d', PATHS.square);
    if (mr.glow) { mr.glow = false; mr.g.classList.remove('glow'); }
  }
  function hex(c) { return [parseInt(c.slice(1, 3), 16), parseInt(c.slice(3, 5), 16), parseInt(c.slice(5, 7), 16)]; }
  var C_WHITE = hex('#FFFFFF'), C_PINK = hex('#DC6F7C'), C_RED = hex('#A81A2C'), C_GOLD = hex('#C9A227');
  function lerpC(a, b, t) { return [a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, a[2] + (b[2] - a[2]) * t]; }
  function css(c) { return 'rgb(' + Math.round(c[0]) + ',' + Math.round(c[1]) + ',' + Math.round(c[2]) + ')'; }

  var last = 0, spawnAt = 0;

  requestAnimationFrame(function tick(now) {
    requestAnimationFrame(tick);
    if (!running || document.hidden) { last = now; return; }
    var dt = last ? Math.min(.05, (now - last) / 1000) : 0; last = now;
    if (!t0) t0 = now;
    var armed = game.phase === 'armed', dead = game.phase === 'dead';

    /* the whole field leans a little against the pointer, more for the near
       (large) marks: depth without a single blurred pixel */
    var tx = ptr.on ? (ptr.x - W / 2) / W : 0, ty = ptr.on ? (ptr.y - H / 2) / H : 0;
    par.x += (tx - par.x) * Math.min(1, 3 * dt); par.y += (ty - par.y) * Math.min(1, 3 * dt);

    /* density: wake a spare square into the pointer's neighbourhood, fading in */
    if (ptr.on && !dead && now - spawnAt > (armed ? 160 + game.wave * 50 : 170)) {
      for (var s = 0; s < marks.length; s++) {
        var sp = marks[s];
        if (sp.spare && !sp.live && !sp.held) {
          var sx = ptr.x + rnd(-R * .8, R * .8), syy = ptr.y + rnd(-R * .8, R * .8);
          sx = Math.max(24, Math.min(W - 24, sx)); syy = Math.max(24, Math.min(H - 24, syy));
          if (!armed && inQuiet(sx, syy, 30)) break;   /* never born on the copy */
          sp.live = true; sp.at = now; sp.phase = 'spawn'; sp.o = 0; sp.born = 0;
          sp.x = sx; sp.y = syy;
          spawnAt = now;
          break;
        }
      }
    }

    /* ---- the heart: weight, follow, pulse, colour ---- */
    var hr = heart.mass ? 16 + Math.sqrt(heart.mass) * 11 : 0;
    var pct = heart.mass / CAP;
    if (heart.mass === 0) {
      /* an empty heart only moves while it is invisible: a fading one stays put */
      if (heart.o < .02 && ptr.on) { heart.x = ptr.x; heart.y = ptr.y; heart.vx = heart.vy = 0; }
    } else {
      /* calm, it follows a hand that stays with it; armed, it follows any hand.
         A far hand, calm, gets nothing: the heart stays and comes apart. */
      var near0 = Math.hypot(ptr.x - heart.x, ptr.y - heart.y) < 300;
      var k = armed ? 95 : 62, drag = armed ? 12 : 9.5, chase = ptr.on && (armed || near0);
      var ax = chase ? (ptr.x - heart.x) * k : 0, ay = chase ? (ptr.y - heart.y) * k : 0;
      heart.vx += (ax - heart.vx * drag) * dt; heart.vy += (ay - heart.vy * drag) * dt;
      var hv = Math.hypot(heart.vx, heart.vy), HV = armed ? 1050 : 650;
      if (hv > HV) { heart.vx *= HV / hv; heart.vy *= HV / hv; }
      heart.x += heart.vx * dt; heart.y += heart.vy * dt;
      heart.x = Math.max(hr, Math.min(W - hr, heart.x)); heart.y = Math.max(hr, Math.min(H - hr, heart.y));
    }
    var far = Math.hypot(ptr.x - heart.x, ptr.y - heart.y);
    var feeding = ptr.on && !dead && (heart.mass === 0 ? (heart.o < .02 || far < 120) : (armed || far < 300));
    /* a hand that leaves (or, before it is armed, runs off) lets it come apart */
    if (!ptr.on) { if (!game.offAt) game.offAt = now; } else game.offAt = 0;
    var letGo = heart.mass > 0 && !dead && (armed ? (!ptr.on && now - game.offAt > 1500) : !feeding);
    if (letGo && now - heart.relAt > 110) release(now, 26, 54);
    if (armed && heart.mass === 0 && !heart.held.length) disarm();

    heart.pulse -= heart.pulse * Math.min(1, 7 * dt);
    heart.hurt -= heart.hurt * Math.min(1, 3.5 * dt);
    var wantSc = heart.mass ? hr * 2 * (1 + .24 * heart.pulse) : 0;
    if (heart.burst) { heart.burst = Math.max(0, heart.burst - dt * 1.7); wantSc = heart.sc * (1 + 1.6 * dt); }
    heart.sc += (wantSc - heart.sc) * Math.min(1, (heart.burst ? 1 : 9) * dt);
    var wantO = heart.mass && !heart.burst ? .94 : 0;
    heart.o += (wantO - heart.o) * Math.min(1, (wantO ? 2.2 : 3.2) * dt);   /* never a flash */
    if (heart.burst && heart.o < .02) heart.burst = 0;
    heart.g.setAttribute('opacity', heart.o.toFixed(3));
    heart.g.setAttribute('transform', 'translate(' + heart.x.toFixed(1) + ' ' + heart.y.toFixed(1) +
      ') scale(' + (heart.sc / 100).toFixed(4) + ') translate(-50 -50)');
    var col = pct < .75 ? lerpC(C_WHITE, C_PINK, pct / .75) : lerpC(C_PINK, C_RED, Math.min(1, (pct - .75) / .25));
    if (heart.hurt > .01) col = lerpC(col, C_GOLD, heart.hurt);
    var fill = css(col);
    if (fill !== heart.fill) { heart.fill = fill; heart.p.setAttribute('fill', fill); }
    var tx0 = heart.mass ? heart.x : ptr.x, ty0 = heart.mass ? heart.y : ptr.y;   /* what pulls */
    var RR = armed ? R * 1.5 : R, VMAX = armed ? 190 : 90;

    /* ---- the words ---- */
    var w = game.word;
    if (armed && !w && now >= game.nextWord && fontReady()) { newWord(now); w = game.word; }
    if (w) {
      var slide = Math.min(1, (now - w.at) / 700);
      w.x = w.cx + w.side * 200 * (1 - easeOut(slide));
      /* never more than three pairs in the air: the rest wait their turn */
      var flying = 0;
      for (var fi = 0; fi < w.letters.length; fi++) if (w.letters[fi].st === 'fly' || w.letters[fi].st === 'queued') flying++;
      var canLaunch = now >= w.readAt && now - w.lastAt >= w.gap && w.launched < w.letters.length && flying <= 4;
      if (canLaunch) {
        var n = Math.min(2, w.letters.length - w.launched);
        var arc0 = Math.random() < .5 ? 1 : -1;
        for (var q = 0; q < n; q++) {
          var L = w.letters[w.launched++];
          /* the two of a pair take opposite arcs, the second a beat later */
          L.st = 'queued'; L.go = now + q * rnd(340, 480); L.arc = q ? -arc0 : arc0;
        }
        w.lastAt = now;
      }
      var target = heart;   /* the heart is the mark, never the hand */
      for (var li = 0; li < w.letters.length; li++) {
        var L2 = w.letters[li];
        if (L2.st === 'queued' && now >= L2.go) {
          L2.st = 'fly'; L2.t0 = now;
          var ux = target.x - L2.x, uy = target.y - L2.y, ul = Math.hypot(ux, uy) || 1;
          ux /= ul; uy /= ul;
          L2.ux = ux; L2.uy = uy;
          L2.vx = ux * 140 - uy * L2.arc * 460; L2.vy = uy * 140 + ux * L2.arc * 460;
        }
        if (L2.st === 'held' || L2.st === 'queued') {
          L2.x = w.x + L2.tx; L2.y = w.cy + L2.ty;
          if (now - w.at > 60 * L2.i) L2.o = Math.min(1, L2.o + dt / .5);
          L2.el.setAttribute('transform', 'translate(' + L2.x.toFixed(1) + ' ' + L2.y.toFixed(1) + ')');
          L2.el.setAttribute('opacity', L2.o.toFixed(3));
        } else if (L2.st === 'fly') {
          /* homing for a moment only (longer each word), then it keeps its
             line and speeds up until it leaves the field: dodge at the right
             time and it is gone */
          var age = (now - L2.t0) / 1000;
          var seek = Math.min(2.4, 1 + game.wave * .3);
          var vmax = (540 + 280 * Math.min(1, age / .5)) * (1 + game.wave * .2);
          if (age < seek) {
            /* early on it aims wide of the heart, on its own side, and the
               offset closes: a curve in, not a straight line */
            var off = Math.max(0, 1 - age / .75) * 240 * L2.arc;
            var adx = target.x - L2.uy * off - L2.x, ady = target.y + L2.ux * off - L2.y, ad = Math.hypot(adx, ady) || 1;
            var steer = Math.min(1, (2.6 + 4.4 * Math.min(1, age / .4)) * (1 + game.wave * .15) * dt);
            L2.vx += (adx / ad * vmax - L2.vx) * steer; L2.vy += (ady / ad * vmax - L2.vy) * steer;
          } else {
            var vs0 = Math.hypot(L2.vx, L2.vy) || 1, acc = 1 + 1.4 * dt;
            if (vs0 < vmax * 1.6) { L2.vx *= acc; L2.vy *= acc; }
          }
          var vs = Math.hypot(L2.vx, L2.vy);
          L2.x += L2.vx * dt; L2.y += L2.vy * dt;
          var dd = Math.hypot(target.x - L2.x, target.y - L2.y) || 1;
          if (now - L2.fuelAt > 55 && vs > 60) {
            L2.fuelAt = now;
            puff(L2.x - L2.vx / vs * 14, L2.y - L2.vy / vs * 14, -L2.vx * .1 + rnd(-24, 24), -L2.vy * .1 + rnd(-24, 24),
                 .4, rnd(3.5, 6), .45, '#E38A3C');
          }
          L2.el.setAttribute('transform', 'translate(' + L2.x.toFixed(1) + ' ' + L2.y.toFixed(1) + ') rotate(' +
            (Math.atan2(L2.vy, L2.vx) * 180 / Math.PI).toFixed(1) + ')');
          var hitR = heart.mass ? Math.max(26, hr * .7) : 30;
          var out = L2.x < -80 || L2.x > W + 80 || L2.y < -80 || L2.y > H + 80;
          if (dd < hitR || out || age > 3.4) {
            L2.st = 'gone'; L2.t0 = now; w.gone++;
            if (dd < hitR && heart.mass) {
              sparks(L2.x, L2.y, 7, '#C9A227');
              heart.hurt = 1; game.hits++;
              if (game.hits >= LIVES) { die(now); break; }
            }
          }
        } else if (L2.st === 'gone') {
          if (!L2.el.parentNode) continue;
          L2.o = Math.max(0, 1 - (now - L2.t0) / 350);
          L2.el.setAttribute('opacity', L2.o.toFixed(3));
          if (!L2.o) ltrG.removeChild(L2.el);
        }
      }
      if (game.word === w && w.gone >= w.letters.length) {
        if (!w.doneAt) w.doneAt = now;
        else if (now - w.doneAt > Math.max(400, 1300 - game.wave * 250)) { endWord(); game.wave++; game.nextWord = now; }
      }
    }
    /* the reading time after a defeat, or the moment the hero steps aside */
    if (dead && (now - game.deadAt > REBIRTH || host.classList.contains('condensed'))) reborn(now);

    /* ---- fuel and sparks ---- */
    for (var di = 0; di < dots.length; di++) {
      var qd = dots[di]; if (!qd.on) continue;
      qd.t += dt;
      if (qd.t >= qd.ttl) { qd.on = false; qd.el.setAttribute('opacity', '0'); continue; }
      var u = qd.t / qd.ttl;
      qd.vx *= 1 - 2.2 * dt; qd.vy *= 1 - 2.2 * dt;
      qd.x += qd.vx * dt; qd.y += qd.vy * dt;
      qd.el.setAttribute('cx', qd.x.toFixed(1)); qd.el.setAttribute('cy', qd.y.toFixed(1));
      qd.el.setAttribute('r', (qd.r * (1 - u * .7)).toFixed(2));
      qd.el.setAttribute('opacity', (qd.o * (1 - u)).toFixed(3));
    }

    /* ---- the marks ---- */
    for (var i = 0; i < marks.length; i++) {
      var m = marks[i];
      if (!m.live) continue;
      var ent = Math.min(1, Math.max(0, (now - t0 - m.born) / BORN));  /* arrival */
      if (ent <= 0) continue;

      var dpx = ptr.x - m.x, dpy = ptr.y - m.y, dp = Math.hypot(dpx, dpy);
      var near = ptr.on && dp < RR;
      var free = m.freeTil > now;

      if (m.phase === 'gone') {
        m.x += m.vx * dt; m.y += m.vy * dt; m.rot += m.vr * 3 * dt;
        m.gt += dt;
        var env = m.gt < .3 ? m.gt / .3 : Math.max(0, 1 - (m.gt - .3) / 1.3);
        m.o = m.go * env;
        m.g.setAttribute('opacity', m.o.toFixed(3)); place(m);
        if (m.gt >= 1.6) { m.live = false; m.phase = 'idle'; m.o = 0; }
        continue;
      }

      /* the pointer pulls: near marks lean in, so the hand is felt at once.
         Once a heart exists, it is the heart that pulls. */
      var dhx = tx0 - m.x, dhy = ty0 - m.y, dh = Math.hypot(dhx, dhy) || 1;
      if (near && dh > 4 && !dead) {
        var pull = (1 - Math.min(1, dh / RR)) * (armed ? 1100 : 520 + heart.mass * 20) * dt;
        m.vx += dhx / dh * pull; m.vy += dhy / dh * pull;
      }
      /* and everything relaxes back to its own drift */
      m.vx += (m.vx0 - m.vx) * Math.min(1, 1.6 * dt);
      m.vy += (m.vy0 - m.vy) * Math.min(1, 1.6 * dt);

      var hush = 1, deepest = 0;
      /* the marks are scared of the words: they get out of their way */
      if (w) for (var lj = 0; lj < w.letters.length; lj++) {
        var LL = w.letters[lj]; if (LL.st === 'gone') continue;
        var rad = LL.st === 'held' ? 120 : 64;
        var ex = m.x - LL.x, ey = m.y - LL.y, ed = Math.hypot(ex, ey);
        if (ed < rad && ed > 0) {
          var f = (1 - ed / rad) * (LL.st === 'held' ? 620 : 900) * dt;
          m.vx += ex / ed * f; m.vy += ey / ed * f;
          if (LL.st === 'held') hush = Math.min(hush, .15 + .85 * ed / rad);
        }
      }

      m.x += m.vx * dt; m.y += m.vy * dt; m.rot += m.vr * dt;
      if (m.x < 20 || m.x > W - 20) { m.vx *= -1; m.vx0 *= -1; m.x = Math.max(20, Math.min(W - 20, m.x)); }
      if (m.y < 20 || m.y > H - 20) { m.vy *= -1; m.vy0 *= -1; m.y = Math.max(20, Math.min(H - 20, m.y)); }

      /* the quiet zones: the copy is never covered. A mark that drifts onto a
         line is eased out and dims on the way in, so nothing ever sits on a
         word at strength. (Armed, the copy has stepped back: the field is open.) */
      if (!armed) {
        for (var q2 = 0; q2 < zones.length; q2++) {
          var z = zones[q2];
          if (!(m.x > z.x0 && m.x < z.x1 && m.y > z.y0 && m.y < z.y1)) continue;
          var cx = (z.x0 + z.x1) / 2, cy = (z.y0 + z.y1) / 2;
          var dx = m.x - cx, dy = (m.y - cy) * 2.2, d2 = Math.hypot(dx, dy) || 1;
          m.vx += (dx / d2) * 150 * dt; m.vy += (dy / d2) * 150 * dt;
          var deep = Math.min(m.x - z.x0, z.x1 - m.x, m.y - z.y0, z.y1 - m.y) / 60;
          if (deep > deepest) deepest = deep;
        }
        hush *= 1 - .85 * Math.min(1, deepest);
      }
      /* a mark on its way into the heart dims as it arrives, then is swallowed:
         it is gone from the field and the heart grows by one. One at a time,
         at a pace: growing is deliberate work. */
      if (feeding && m.phase !== 'spawn') {
        var eat = Math.max(34, hr * .7), band = 48;
        if (dh < eat + band) hush *= Math.max(0, Math.min(1, (dh - eat * .35) / (eat * .65 + band)));
        /* swallowed only once it has all but faded: never a flash */
        if (dh < eat && m.o * m.hs * ent < .06 && now - heart.eatAt > (armed ? 70 + game.wave * 25 : 110)) {
          m.live = false; m.held = true; m.o = 0; m.g.setAttribute('opacity', '0');
          heart.held.push(m); heart.mass++; heart.eatAt = now; heart.pulse = 1;
          if (!armed && heart.mass >= CAP * .5 && !host.classList.contains('condensed')) arm(now);
          continue;
        }
      }
      var spd = Math.hypot(m.vx, m.vy);
      if (spd > VMAX && !free) { m.vx *= VMAX / spd; m.vy *= VMAX / spd; }

      var el = now - m.at;
      if (m.phase === 'spawn') {
        m.o = m.base * Math.min(1, el / SPAWN);
        if (el >= SPAWN) { m.phase = 'idle'; m.o = m.base; }
      }
      if (m.phase === 'idle' && near) {
        m.phase = 'wake'; m.at = now; el = 0;
        m.suit = suit();
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
        var floor = m.spare ? 0 : m.base;    /* a spare fades all the way out */
        m.o = m.peak - (m.peak - floor) * Math.min(1, el / FADE_DN);
        if (el >= FADE_DN) {
          m.phase = 'idle'; m.t = 0; m.o = floor;
          if (m.spare) m.live = false;
        }
      }

      if (m.phase !== 'idle' || m.t > 0) m.p.setAttribute('d', mix(m.suit, m.t));
      m.hs += Math.max(-2.4 * dt, Math.min(2.4 * dt, hush - m.hs));
      m.g.setAttribute('opacity', (m.o * m.hs * ent).toFixed(3));
      place(m);
    }
  });
}

var heroField = document.getElementById('field');
if (heroField) makeField(heroField, {
  w: 1600, h: 900, n: 66, nm: 24, base: .20, peak: .84, r: 260,
  text: [].slice.call(document.querySelectorAll('.hero .wrap > *')),
  quiet: { x0: 330, x1: 1270, y0: 215, y1: 700 },
  copy: { els: [document.querySelector('.hero h1'), document.querySelector('.hero .sub')],
          dead: ['@@t.hero.dead.h1@@', '@@t.hero.dead.sub@@'] }
});
document.querySelectorAll('.closefield').forEach(function (svg) {
  var sec = svg.parentNode;
  makeField(svg, { w: 1600, h: 620, n: 34, nm: 14, base: .16, peak: .8, r: 270,
    text: [].slice.call(sec.querySelectorAll('.wrap > *')),
    quiet: { x0: 450, x1: 1150, y0: 130, y1: 510 },
    copy: { els: [sec.querySelector('h2'), sec.querySelector('.fine')],
            dead: ['@@t.close.dead.h2@@', '@@t.close.dead.fine@@'] } });
});
