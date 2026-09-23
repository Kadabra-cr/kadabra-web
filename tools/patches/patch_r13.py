"""Round 13: phrases instead of words (half the letters fire, half dissolve),
fast graphs with every sentence at once, a progress rule per screen, the ledger."""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..')
p = os.path.join(ROOT, 'src', 'app.src.js')
s = open(p, encoding='utf-8').read()


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:100])
    s = s.replace(a, b)


# ---- phrases ----
rep("var WORDS = '@@t.game.words@@'.split(', ');", "var WORDS = '@@t.game.words@@'.split(' | ');")
rep("""    var lines = text.indexOf(' ') > 0 && text.length > 9 ? text.split(' ') : [text];
    var fs = lines.length > 1 ? 50 : (text.length <= 8 ? 62 : Math.max(46, 62 * 8 / text.length));
    var maxW = W * .2, widest = 0;""", """    /* a phrase wraps into short lines, about fifteen characters each */
    var lines = [], cur = '';
    text.split(' ').forEach(function (wd) {
      if (cur && (cur + ' ' + wd).length > 15) { lines.push(cur); cur = wd; } else cur = cur ? cur + ' ' + wd : wd;
    });
    if (cur) lines.push(cur);
    var fs = lines.length > 2 ? 42 : lines.length > 1 ? 48 : 58;
    var maxW = W * .24, widest = 0;""")
rep("""    return { letters: out, fs: fs, halfW: maxTx + fs * .6, halfH: fs * (lines.length > 1 ? 1.1 : .6) };""",
    """    return { letters: out, fs: fs, halfW: maxTx + fs * .6, halfH: fs * (lines.length * .5 + .1) };""")
rep("""    var w = { side: side, cx: cx, cy: H / 2, x: cx + side * 200, at: now, letters: [], launched: 0, lastAt: 0,
              gap: Math.max(200, 380 - game.wave * 40), gone: 0, doneAt: 0 };
    w.readAt = now + 700 + Math.max(300, 650 - game.wave * 90) + 40 * lay.letters.length;""",
    """    var w = { side: side, cx: cx, cy: H / 2, x: cx + side * 200, at: now, letters: [], front: 0, back: lay.letters.length - 1,
              lastAt: 0, gap: Math.max(260, 460 - game.wave * 40), gone: 0, doneAt: 0 };
    w.readAt = now + 700 + Math.max(300, 650 - game.wave * 90) + 55 * lay.letters.length;""")
rep("""      var canLaunch = now >= w.readAt && now - w.lastAt >= w.gap && w.launched < w.letters.length && flying <= 4;
      if (canLaunch) {
        var n = Math.min(2, w.letters.length - w.launched);
        var arc0 = Math.random() < .5 ? 1 : -1;
        for (var q = 0; q < n; q++) {
          var L = w.letters[w.launched++];
          /* the two of a pair take opposite arcs, the second a beat later */
          L.st = 'queued'; L.go = now + q * rnd(340, 480); L.arc = q ? -arc0 : arc0;
        }
        w.lastAt = now;
      }""", """      var canLaunch = now >= w.readAt && now - w.lastAt >= w.gap && w.front <= w.back && flying <= 4;
      if (canLaunch) {
        /* two threads: from the front of the phrase a pair fires, from the
           back two letters just dissolve. Half the phrase ever flies. */
        var arc0 = Math.random() < .5 ? 1 : -1;
        for (var q = 0; q < 2 && w.front <= w.back; q++) {
          var L = w.letters[w.front++];
          /* the two of a pair take opposite arcs, the second a beat later */
          L.st = 'queued'; L.go = now + q * rnd(340, 480); L.arc = q ? -arc0 : arc0;
        }
        for (var q2 = 0; q2 < 2 && w.front <= w.back; q2++) {
          var Lf = w.letters[w.back--];
          Lf.st = 'gone'; Lf.t0 = now + q2 * 140; Lf.fadeMs = 900; w.gone++;
        }
        w.lastAt = now;
      }""")
rep("""          L2.o = Math.max(0, 1 - (now - L2.t0) / 350);""",
    """          L2.o = Math.max(0, Math.min(1, 1 - (now - L2.t0) / (L2.fadeMs || 350)));""")

# ---- graphs: fast, every sentence at once ----
rep("""  function play() {
    var lastAt = 0;""", """  function play() {
    var lastAt = 0;
    root.querySelectorAll('.beat-l').forEach(function (el) { el.classList.add('on'); });""")
rep("""    { at: 350, cls: 'in', fn: function (A, B) { A.concat(B).forEach(function (c) { c.g.style.transitionDelay = (c.row * 22) + 'ms'; }); } },
    { at: 1150, cls: 'lit', fn: function (A) { A.forEach(function (c) { if (c.n < 93) c.p.style.transitionDelay = (c.row * 26 + c.col * 6) + 'ms'; }); } },
    { at: 2300, cls: 'rules', fn: function (A, B) {
      B.slice(0, 9).forEach(function (c, i) { c.p.style.transitionDelay = (i * 70) + 'ms'; morphPath(c.p, 'smooth-diamond', 520, i * 70); });""",
    """    { at: 150, cls: 'in', fn: function (A, B) { A.concat(B).forEach(function (c) { c.g.style.transitionDelay = (c.row * 9) + 'ms'; }); } },
    { at: 400, cls: 'lit', fn: function (A) { A.forEach(function (c) { if (c.n < 93) c.p.style.transitionDelay = (c.row * 9 + c.col * 3) + 'ms'; }); } },
    { at: 750, cls: 'rules', fn: function (A, B) {
      B.slice(0, 9).forEach(function (c, i) { c.p.style.transitionDelay = (i * 35) + 'ms'; morphPath(c.p, 'smooth-diamond', 420, i * 35); });""")
rep("""    { at: 0, cls: 'in', fn: function (A, B) { A.concat(B.slice(0, 100)).forEach(function (c) { c.g.style.transitionDelay = (c.row * 22) + 'ms'; }); } },
    { at: 800, cls: 'taught', fn: function (A, B) { B.slice(0, 100).forEach(function (c) { morphPath(c.p, 'smooth-spade', 420, c.row * 28 + c.col * 7); }); } },
    { at: 1900, cls: 'more', fn: function (A, B) {
      B.slice(100).forEach(function (c, i) { c.p.setAttribute('d', mix('smooth-spade', 1)); c.g.style.transitionDelay = (i * 16) + 'ms'; });""",
    """    { at: 0, cls: 'in', fn: function (A, B) { A.concat(B.slice(0, 100)).forEach(function (c) { c.g.style.transitionDelay = (c.row * 9) + 'ms'; }); } },
    { at: 300, cls: 'taught', fn: function (A, B) { B.slice(0, 100).forEach(function (c) { morphPath(c.p, 'smooth-spade', 380, c.row * 10 + c.col * 3); }); } },
    { at: 800, cls: 'more', fn: function (A, B) {
      B.slice(100).forEach(function (c, i) { c.p.setAttribute('d', mix('smooth-spade', 1)); c.g.style.transitionDelay = (i * 6) + 'ms'; });""")

# ---- the progress rule: fills per phase; full means the screen lets go ----
rep("""        var ms = HDR - morph.getBoundingClientRect().top;
        morph.style.setProperty('--p', clamp((ms - ph * .55) / (ph * .85)).toFixed(4));
        var g = ms >= ph * 1.4;
        morph.classList.toggle('graph', g);
        if (g && policyG) policyG.play();
      }
      if (vscr && vizG && vscr.getBoundingClientRect().top <= HDR + ph * .25) vizG.play();""",
    """        var ms = HDR - morph.getBoundingClientRect().top, mEnd = morph.offsetHeight - ph;
        var g = ms >= ph * 1.4;
        morph.style.setProperty('--p', (g ? clamp((ms - ph * 1.4) / (mEnd - ph * 1.4)) : clamp((ms - ph * .55) / (ph * .85))).toFixed(4));
        morph.classList.toggle('graph', g);
        if (g && policyG) policyG.play();
      }
      if (vscr) {
        var vt = vscr.getBoundingClientRect().top;
        vscr.style.setProperty('--p', clamp((HDR - vt) / (vscr.offsetHeight - ph)).toFixed(4));
        if (vizG && vt <= HDR + ph * .25) vizG.play();
      }""")
open(p, 'w', encoding='utf-8', newline='\n').write(s)
a = s.index('/* ==========================================================================\n   THE FIELD')
b = s.index('/* ==========================================================================\n   GRAPHS')
open(os.path.join(ROOT, 'src', 'field_r8.js'), 'w', encoding='utf-8', newline='\n').write(s[a:b].rstrip() + '\n')

# ---- CSS ----
c = os.path.join(ROOT, 'site', 'styles.css')
t = open(c, encoding='utf-8').read()


def crep(a, b):
    global t
    assert t.count(a) == 1, a[:90]
    t = t.replace(a, b)


crep('html.staged #morph{--len:4.1;--p:0}', 'html.staged #morph{--len:3.4;--p:0}')
crep('html.staged #vizscr{--len:2.5}', 'html.staged #vizscr{--len:2.2;--p:0}')
crep('''/* the breath: a gold rule fills under the two cards as the scroll carries on */
html.staged .policy .pair::after{content:"";position:absolute;left:0;bottom:-14px;height:3px;width:100%;background:var(--gold-ink);
  transform-origin:0 50%;transform:scaleX(var(--p))}
''', '''/* the progress rule: fills as the scroll carries on; full, the screen lets go */
.prog{display:none}
html.staged .prog{display:block;height:3px;margin-top:clamp(20px,3.4svh,36px);background:var(--cream-line)}
html.staged .prog i{display:block;height:100%;background:var(--gold-ink);transform-origin:0 50%;transform:scaleX(var(--p))}
''')
crep('''.aside{margin-top:calc(var(--cell)*.9);''', '''/* the ledger: the figure leads, the sentence follows */
.ledger{display:grid;gap:clamp(8px,1.6svh,16px)}
.ledger .beat-l{display:grid;grid-template-columns:3.1ch minmax(0,1fr);gap:.55em;align-items:baseline;
  font-family:var(--body);font-weight:600;letter-spacing:0;font-size:clamp(1rem,1.25vw,1.15rem);line-height:1.3}
.ledger .beat-l b{font-family:var(--title);font-weight:800;letter-spacing:-.04em;font-variant-numeric:tabular-nums;
  text-align:right;font-size:2.1em;line-height:.9}
.ledger .beat-l[data-beat=in]{color:var(--ink-dim)}
.ledger .beat-l.risk{color:var(--red)}
html.staged .stage-right .ledger .beat-l{font-size:clamp(1rem,1.2vw,1.12rem)}
.aside{margin-top:calc(var(--cell)*.9);''')
open(c, 'w', encoding='utf-8', newline='\n').write(t)
print('ok')
