"""Round 19b: a phrase that has not fired yet never lets the hand sit on it. If
the hand or the heart comes close, it slips out through its own edge and comes
back in through the opposite one, like a Pac-Man portal, and firing waits."""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..')
p = os.path.join(ROOT, 'src', 'app.src.js')
s = open(p, encoding='utf-8').read()


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:100])
    s = s.replace(a, b)


rep("""    var w = { side: side, cx: cx, cy: H / 2, x: cx + side * 200, at: now, letters: [], front: 0, back: lay.letters.length - 1,
              lastAt: 0, gap: Math.max(260, 460 - game.wave * RAMP * 40), gone: 0, doneAt: 0 };""",
    """    var w = { side: side, cx: cx, cy: H / 2, x: cx + side * 200, at: now, letters: [], front: 0, back: lay.letters.length - 1,
              lastAt: 0, gap: Math.max(260, 460 - game.wave * RAMP * 40), gone: 0, doneAt: 0,
              halfW: lay.halfW, halfH: lay.halfH, v0: v0, v1: v1, vw: vw, port: null, portAt: 0 };""")
rep("""  function endWord() {""", """  function sideCx(w, side) {
    return side > 0 ? Math.min(w.v0 + w.vw * .84, w.v1 - 30 - w.halfW) : Math.max(w.v0 + w.vw * .16, w.v0 + 30 + w.halfW);
  }
  function endWord() {""")
rep("""      w.x = w.cx + w.side * 200 * (1 - easeOut(slide));
""", """      w.x = w.cx + w.side * 200 * (1 - easeOut(slide));
      /* a phrase that has not fired yet never lets the hand sit on it: if the
         hand (or the heart) comes close, it slips out through its own edge and
         comes back in through the opposite one, and the firing waits for it */
      var nextFire = Math.max(w.readAt, w.lastAt + w.gap), waiting = false;
      for (var wi = 0; wi < w.letters.length; wi++) if (w.letters[wi].st === 'queued') { waiting = true; break; }
      if (!w.port && !waiting && w.front <= w.back && now < nextFire - 220 && now - w.portAt > 450 && slide >= 1) {
        var near2 = function (px, py) { return Math.abs(px - w.x) < w.halfW + 110 && Math.abs(py - w.cy) < w.halfH + 110; };
        if ((ptr.on && near2(ptr.x, ptr.y)) || (heart.mass && near2(heart.x, heart.y))) w.port = { t0: now, from: w.x, side: w.side };
      }
      var po = 1;
      if (w.port) {
        var pt = now - w.port.t0;
        if (pt < 170) { var e1 = pt / 170; w.x = w.port.from + w.port.side * 320 * e1 * e1; po = 1 - e1; }
        else {
          if (w.side === w.port.side) { w.side = -w.side; w.cx = sideCx(w, w.side); }
          var e2 = Math.min(1, (pt - 170) / 280); w.x = w.cx + w.side * 320 * (1 - easeOut(e2)); po = e2;
          if (e2 >= 1) { w.port = null; w.portAt = now; }
        }
        w.readAt = Math.max(w.readAt, now + 650); w.lastAt = Math.max(w.lastAt, now + 650 - w.gap);
      }
""")
rep("""          L2.el.setAttribute('opacity', L2.o.toFixed(3));
        } else if (L2.st === 'fly') {""", """          L2.el.setAttribute('opacity', (L2.o * po).toFixed(3));
        } else if (L2.st === 'fly') {""")
open(p, 'w', encoding='utf-8', newline='\n').write(s)
a = s.index('/* ==========================================================================\n   THE FIELD')
b = s.index('/* ==========================================================================\n   GRAPHS')
open(os.path.join(ROOT, 'src', 'field_r8.js'), 'w', encoding='utf-8', newline='\n').write(s[a:b].rstrip() + '\n')
print('ok')
