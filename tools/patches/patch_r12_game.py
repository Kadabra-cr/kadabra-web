"""Round 12 game: no lives shown, no invulnerability; each pair splits and comes
at the heart from two angles, the second a beat after the first. A little spade
points at the WhatsApp button three seconds after a defeat."""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(HERE, '..', '..', 'src', 'app.src.js')
s = open(p, encoding='utf-8').read()


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:100])
    s = s.replace(a, b)


# ---- lives: counted, never shown ----
start = s.index('  var lifeG = document.createElementNS(NS, \'g\'), pips = [];')
end = s.index('  /* the war layer')
s = s[:start] + s[end:]
rep("    host.classList.add('armed'); showLives();", "    host.classList.add('armed');")
rep("game.word = null; game.hits = 0; showLives();", "game.word = null; game.hits = 0;")
rep("""    lifeO += ((armed && heart.mass ? .9 : 0) - lifeO) * Math.min(1, 1.8 * dt);
    lifeG.setAttribute('opacity', lifeO.toFixed(3));
    if (lifeO > .01) lifeG.setAttribute('transform', 'translate(' + heart.x.toFixed(1) + ' ' + (heart.y - hr - 24).toFixed(1) + ')');
""", "")
# ---- no invulnerability ----
rep("    heart.g.setAttribute('opacity', (heart.o * (now < heart.safeTil ? .45 + .55 * (Math.floor(now / 90) % 2) : 1)).toFixed(3));",
    "    heart.g.setAttribute('opacity', heart.o.toFixed(3));")
rep(", fill: '', safeTil: 0 };", ", fill: '' };")
rep("""            /* a hit leaves the heart untouchable for a beat: a pair counts once */
            if (dd < hitR && heart.mass && now < heart.safeTil) sparks(L2.x, L2.y, 4, '#FFFFFF');
            else if (dd < hitR && heart.mass) {
              sparks(L2.x, L2.y, 7, '#C9A227');
              heart.hurt = 1; heart.safeTil = now + 800; game.hits++; showLives();""",
    """            if (dd < hitR && heart.mass) {
              sparks(L2.x, L2.y, 7, '#C9A227');
              heart.hurt = 1; game.hits++;""")

# ---- the pincer: a pair splits wide and closes from two sides, one a beat late ----
rep("""      for (var fi = 0; fi < w.letters.length; fi++) if (w.letters[fi].st === 'fly') flying++;""",
    """      for (var fi = 0; fi < w.letters.length; fi++) if (w.letters[fi].st === 'fly' || w.letters[fi].st === 'queued') flying++;""")
rep("""        for (var q = 0; q < n; q++) {
          var L = w.letters[w.launched++];
          L.st = 'fly'; L.t0 = now; L.x = w.x + L.tx; L.y = w.cy + L.ty;
          /* the two of a pair split a little, up and down, then close in */
          L.vx = -w.side * 120; L.vy = (q ? 1 : -1) * rnd(90, 140);
        }""", """        var arc0 = Math.random() < .5 ? 1 : -1;
        for (var q = 0; q < n; q++) {
          var L = w.letters[w.launched++];
          /* the two of a pair take opposite arcs, the second a beat later */
          L.st = 'queued'; L.go = now + q * rnd(150, 260); L.arc = q ? -arc0 : arc0;
        }""")
rep("""        var L2 = w.letters[li];
        if (L2.st === 'held') {""", """        var L2 = w.letters[li];
        if (L2.st === 'queued' && now >= L2.go) {
          L2.st = 'fly'; L2.t0 = now;
          var ux = target.x - L2.x, uy = target.y - L2.y, ul = Math.hypot(ux, uy) || 1;
          ux /= ul; uy /= ul;
          L2.ux = ux; L2.uy = uy;
          L2.vx = ux * 160 - uy * L2.arc * 520; L2.vy = uy * 160 + ux * L2.arc * 520;
        }
        if (L2.st === 'held' || L2.st === 'queued') {""")
rep("""          if (age < seek) {
            var adx = target.x - L2.x, ady = target.y - L2.y, ad = Math.hypot(adx, ady) || 1;""",
    """          if (age < seek) {
            /* early on it aims wide of the heart, on its own side, and the
               offset closes: a curve in, not a straight line */
            var off = Math.max(0, 1 - age / .75) * 240 * L2.arc;
            var adx = target.x - L2.uy * off - L2.x, ady = target.y + L2.ux * off - L2.y, ad = Math.hypot(adx, ady) || 1;""")

# ---- after a defeat, a little spade points at the button ----
rep("""  function die(now) {
    game.phase = 'dead'; game.deadAt = now;""", """  var pointT = 0;
  function die(now) {
    game.phase = 'dead'; game.deadAt = now;
    clearTimeout(pointT);
    pointT = setTimeout(function () { if (game.phase === 'dead') host.classList.add('pointing'); }, 3000);""")
rep("""  function reborn(now) {
    host.classList.remove('dead');""", """  function reborn(now) {
    clearTimeout(pointT);
    host.classList.remove('dead', 'pointing');""")

# ---- graphs: the scroll only starts them; they play on their own clock ----
rep("""  if (cfg.drive && STAGE) {
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
  }""", """  function play() {
    var lastAt = 0;
    cfg.beats.forEach(function (bt) {
      lastAt = Math.max(lastAt, bt.at);
      setTimeout(function () { beatOn(bt.cls); bt.fn(A, B); }, bt.at);
    });
    setTimeout(function () { live = true; root.classList.add('live'); }, lastAt + 900);
  }
  if (cfg.drive && STAGE) {
    /* staged: the scroll decides when it starts, the clock plays it, once */
    var played = false;
    return { play: function () { if (!played) { played = true; play(); } } };
  }""")
rep("""  new IntersectionObserver(function (es, o) {
    if (!es[0].isIntersecting) return;
    o.disconnect();
    var lastAt = 0;
    cfg.beats.forEach(function (bt) {
      lastAt = Math.max(lastAt, bt.at);
      setTimeout(function () { beatOn(bt.cls); bt.fn(A, B); }, bt.at);
    });
    setTimeout(function () { live = true; root.classList.add('live'); }, lastAt + 900);
  }, { threshold: .35 }).observe(root);""", """  new IntersectionObserver(function (es, o) {
    if (!es[0].isIntersecting) return;
    o.disconnect();
    play();
  }, { threshold: .35 }).observe(root);""")
rep("""      if (morph) {
        var r = clamp((HDR - morph.getBoundingClientRect().top - ph * .7) / (ph * 1.3));
        morph.style.setProperty('--r', r.toFixed(4));
        if (policyG) policyG.set(r);
      }
      if (vscr && vizG) vizG.set(clamp((HDR - vscr.getBoundingClientRect().top - ph * .2) / (ph * 1.3)));""",
    """      if (morph) {
        /* the two cards hold for a breath (a gold rule fills under them),
           then the graph takes over and plays on its own */
        var ms = HDR - morph.getBoundingClientRect().top;
        morph.style.setProperty('--p', clamp((ms - ph * .55) / (ph * .85)).toFixed(4));
        var g = ms >= ph * 1.4;
        morph.classList.toggle('graph', g);
        if (g && policyG) policyG.play();
      }
      if (vscr && vizG && vscr.getBoundingClientRect().top <= HDR + ph * .25) vizG.play();""")
open(p, 'w', encoding='utf-8', newline='\n').write(s)
print('ok')
