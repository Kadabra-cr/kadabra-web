"""Round 11 game: pairs of letters, short homing then straight, three hits and out,
words mid-height from the sides, smaller, lighter to run."""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(HERE, '..', '..', 'src', 'app.src.js')
s = open(p, encoding='utf-8').read()


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:100])
    s = s.replace(a, b)


rep('''  var EXTRA = wide ? Math.round(COUNT * .6) : Math.round(COUNT * .2);   /* density near the pointer */''',
    '''  var EXTRA = wide ? Math.round(COUNT * .35) : Math.round(COUNT * .2);  /* density near the pointer */''')
rep('''  var REBIRTH = 10000;                       /* ms of reading after a defeat */''',
    '''  var REBIRTH = 20000;                       /* ms of reading after a defeat */
  var LIVES = 3;                             /* three hits and it is over, whatever the size */''')

# lives: three small diamonds riding above the heart
rep('''  heart.g.appendChild(heart.p); svg.appendChild(heart.g);''',
    '''  heart.g.appendChild(heart.p); svg.appendChild(heart.g);
  var lifeG = document.createElementNS(NS, 'g'), pips = [];
  lifeG.setAttribute('opacity', '0'); svg.appendChild(lifeG);
  for (var lv = 0; lv < LIVES; lv++) {
    var pp = document.createElementNS(NS, 'path');
    pp.setAttribute('d', 'M0 -9 L7 0 L0 9 L-7 0 Z'); pp.setAttribute('fill', '#FFFFFF');
    pp.setAttribute('transform', 'translate(' + ((lv - 1) * 22) + ' 0)');
    lifeG.appendChild(pp); pips.push(pp);
  }
  var lifeO = 0;
  function showLives() {
    pips.forEach(function (pp, k) {
      var lost = k >= LIVES - game.hits;
      pp.setAttribute('fill', lost ? 'none' : '#FFFFFF');
      pp.setAttribute('stroke', lost ? '#C9A227' : 'none'); pp.setAttribute('stroke-width', '2');
    });
  }''')

# a smaller pool of fuel: at most a handful of letters fly at once now
rep('''  for (var d = 0; d < 110; d++) {''', '''  for (var d = 0; d < 64; d++) {''')

rep('''  var game = { phase: 'calm', armedAt: 0, wave: 0, nextWord: 0, word: null, deadAt: 0, offAt: 0 };''',
    '''  var game = { phase: 'calm', armedAt: 0, wave: 0, nextWord: 0, word: null, deadAt: 0, offAt: 0, hits: 0 };''')

# smaller words, never wider than a fifth of the field
rep('''    var fs = lines.length > 1 ? 74 : (text.length <= 8 ? 92 : Math.max(64, 92 * 8 / text.length));
    var maxW = W * (lines.length > 1 ? .24 : .28), widest = 0;''',
    '''    var fs = lines.length > 1 ? 50 : (text.length <= 8 ? 62 : Math.max(46, 62 * 8 / text.length));
    var maxW = W * .2, widest = 0;''')

# words: mid-height, on the far side from the hand, sliding in from that edge
start = s.index('''  function newWord(now) {''')
end = s.index('''  function endWord() {''')
s = s[:start] + '''  function newWord(now) {
    var text = WORDS[game.wave % WORDS.length];
    var lay = layout(text);
    var refX = ptr.on ? ptr.x : heart.x;
    var side = refX < W / 2 ? 1 : -1;                 /* the far side from the hand */
    var cx = side > 0 ? Math.min(W * .84, W - 40 - lay.halfW) : Math.max(W * .16, 40 + lay.halfW);
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
''' + s[end:]

rep('''  function arm(now) {
    game.phase = 'armed'; game.armedAt = now; game.nextWord = now + 5000; game.wave = 0;
    host.classList.add('armed');
  }''', '''  function arm(now) {
    game.phase = 'armed'; game.armedAt = now; game.nextWord = now + 5000; game.wave = 0; game.hits = 0;
    host.classList.add('armed'); showLives();
  }''')
rep('''    t0 = now; game.phase = 'calm'; game.wave = 0; game.word = null;''',
    '''    t0 = now; game.phase = 'calm'; game.wave = 0; game.word = null; game.hits = 0; showLives();''')

# the lives ride above the heart, only while armed
rep('''    var col = pct < .75 ? lerpC(C_WHITE, C_PINK, pct / .75)''', '''    lifeO += ((armed && heart.mass ? .9 : 0) - lifeO) * Math.min(1, 4 * dt);
    lifeG.setAttribute('opacity', lifeO.toFixed(3));
    if (lifeO > .01) lifeG.setAttribute('transform', 'translate(' + heart.x.toFixed(1) + ' ' + (heart.y - hr - 24).toFixed(1) + ')');
    var col = pct < .75 ? lerpC(C_WHITE, C_PINK, pct / .75)''')

# launching: always a pair, a short beat apart
rep('''      var slide = Math.min(1, (now - w.at) / 620);
      w.x = w.cx + w.side * 300 * (1 - easeOut(slide));
      var canLaunch = now >= w.readAt && now - w.lastAt >= w.gap && w.launched < w.letters.length;
      if (canLaunch) {
        var left = w.letters.length - w.launched;
        var n = game.wave === 0 && left <= 4 ? left : Math.min(w.group, left);
        if (!w.mass) w.mass = Math.max(heart.mass, CAP);   /* a word always costs half a full heart */
        for (var q = 0; q < n; q++) {
          var L = w.letters[w.launched++];
          L.st = 'fly'; L.t0 = now; L.x = w.x + L.tx; L.y = w.cy + L.ty;
          L.vx = -w.side * 40 + rnd(-40, 40); L.vy = rnd(-70, 70);
        }
        w.lastAt = now;
      }''', '''      var slide = Math.min(1, (now - w.at) / 700);
      w.x = w.cx + w.side * 200 * (1 - easeOut(slide));
      var canLaunch = now >= w.readAt && now - w.lastAt >= w.gap && w.launched < w.letters.length;
      if (canLaunch) {
        var n = Math.min(2, w.letters.length - w.launched);
        for (var q = 0; q < n; q++) {
          var L = w.letters[w.launched++];
          L.st = 'fly'; L.t0 = now; L.x = w.x + L.tx; L.y = w.cy + L.ty;
          /* the two of a pair split a little, up and down, then close in */
          L.vx = -w.side * 120; L.vy = (q ? 1 : -1) * rnd(90, 140);
        }
        w.lastAt = now;
      }''')

# flight: home in for a moment, then fly straight on and off the field
start = s.index('''        } else if (L2.st === 'fly') {''')
end = s.index('''        } else if (L2.st === 'gone') {''')
s = s[:start] + '''        } else if (L2.st === 'fly') {
          /* homing for a moment only (longer each word), then it keeps its
             line and speeds up until it leaves the field: dodge at the right
             time and it is gone */
          var age = (now - L2.t0) / 1000;
          var seek = Math.min(2.4, 1.3 + game.wave * .25);
          var vmax = (620 + 280 * Math.min(1, age / .5)) * (1 + game.wave * .14);
          if (age < seek) {
            var adx = target.x - L2.x, ady = target.y - L2.y, ad = Math.hypot(adx, ady) || 1;
            var steer = Math.min(1, (3 + 5 * Math.min(1, age / .4)) * dt);
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
          if (dd < hitR || out || age > 6) {
            L2.st = 'gone'; L2.t0 = now; w.gone++;
            if (dd < hitR && heart.mass) {
              sparks(L2.x, L2.y, 7, '#C9A227');
              heart.hurt = 1; game.hits++; showLives();
              if (game.hits >= LIVES) { die(now); break; }
            }
          }
'''.rstrip('\n') + '\n' + s[end:]

# a spent letter is taken out of the page, not left at zero opacity
rep('''        } else if (L2.st === 'gone') {
          L2.o = Math.max(0, 1 - (now - L2.t0) / 450);
          L2.el.setAttribute('opacity', L2.o.toFixed(3));
        }''', '''        } else if (L2.st === 'gone') {
          if (!L2.el.parentNode) continue;
          L2.o = Math.max(0, 1 - (now - L2.t0) / 350);
          L2.el.setAttribute('opacity', L2.o.toFixed(3));
          if (!L2.o) ltrG.removeChild(L2.el);
        }''')
rep('''        else if (now - w.doneAt > Math.max(250, 1300 - game.wave * 300)) { endWord(); game.wave++; game.nextWord = now; }''',
    '''        else if (now - w.doneAt > Math.max(400, 1300 - game.wave * 250)) { endWord(); game.wave++; game.nextWord = now; }''')

# no per-mark glow filter in the field: the heart keeps its glow, the squares stay crisp
rep('''      var wantGlow = m.t > .86;
      if (wantGlow !== m.glow) { m.glow = wantGlow; m.g.classList.toggle('glow', wantGlow); }
      m.hs += Math.max(-2.4 * dt, Math.min(2.4 * dt, hush - m.hs));
      m.g.setAttribute('opacity', (m.o * m.hs * ent).toFixed(3));''', '''      m.hs += Math.max(-2.4 * dt, Math.min(2.4 * dt, hush - m.hs));
      m.g.setAttribute('opacity', (m.o * m.hs * ent).toFixed(3));''')

# both fields play by the same rules now: three hits, not one
rep('''  makeField(svg, { w: 1600, h: 620, n: 34, nm: 14, base: .16, peak: .8, r: 270, lethal: true,''',
    '''  makeField(svg, { w: 1600, h: 620, n: 34, nm: 14, base: .16, peak: .8, r: 270,''')
open(p, 'w', encoding='utf-8', newline='\n').write(s)
print('ok')
