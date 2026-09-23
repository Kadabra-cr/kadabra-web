"""Round 14: the game asks first. A small pill floats by the heart; accepting
starts interactive mode, shown by a chip under the header that can end it.
While it runs, the page does not scroll and the chip shakes instead."""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..')
p = os.path.join(ROOT, 'src', 'app.src.js')
s = open(p, encoding='utf-8').read()


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:100])
    s = s.replace(a, b)


# ---- interactive mode: one chip for the page, owned by whichever field is playing ----
rep('''function makeField(svg, opt) {''', '''/* Interactive mode: while a field is being played the page holds still (the
   wheel, touch and scroll keys shake the chip instead), and the chip under
   the header is the way out. */
var Mode = (function () {
  var owner = null, chip = null;
  function build() {
    chip = document.createElement('div');
    chip.className = 'mode'; chip.setAttribute('role', 'status');
    chip.innerHTML = '<i class="dot" aria-hidden="true"></i><span>@@t.game.mode@@</span>' +
      '<button type="button">@@t.game.exit@@<svg viewBox="0 0 12 12" aria-hidden="true"><path d="M2 2l8 8M10 2l-8 8"/></svg></button>';
    chip.querySelector('button').addEventListener('click', function () { if (owner) owner.exit(); });
    document.body.appendChild(chip);
  }
  function shake() {
    if (!chip) return;
    chip.classList.remove('shake'); void chip.offsetWidth; chip.classList.add('shake');
  }
  function block(e) { if (owner) { e.preventDefault(); shake(); } }
  addEventListener('wheel', block, { passive: false });
  addEventListener('touchmove', block, { passive: false });
  addEventListener('keydown', function (e) {
    if (owner && /^( |PageUp|PageDown|ArrowUp|ArrowDown|Home|End)$/.test(e.key)) block(e);
  });
  return {
    on: function (who) {
      if (!chip) build();
      owner = who;
      chip.classList.add('on', 'fresh');
      setTimeout(function () { chip.classList.remove('fresh'); }, 1600);
    },
    off: function (who) { if (owner !== who) return; owner = null; if (chip) chip.classList.remove('on', 'fresh'); },
    shake: shake
  };
})();

function makeField(svg, opt) {''')

# ---- the ask ----
rep('''  function arm(now) {
    game.phase = 'armed'; game.armedAt = now; game.nextWord = now + 5000; game.wave = 0; game.hits = 0;
    host.classList.add('armed');
  }
  function disarm() { game.phase = 'calm'; host.classList.remove('armed'); endWord(); }''',
'''  /* never without asking: a small pill floats by the heart. Yes starts the
     words at once; the cross puts it away for good (until a reload). */
  var askEl = document.createElement('div'), askP = { x: 0, y: 0, placed: false, hover: false };
  askEl.className = 'ask';
  askEl.innerHTML = '<span>@@t.game.ask@@</span><button type="button" class="yes">@@t.game.ask.btn@@</button>' +
    '<button type="button" class="no" aria-label="@@t.game.ask.no@@"><svg viewBox="0 0 12 12" aria-hidden="true"><path d="M2 2l8 8M10 2l-8 8"/></svg></button>';
  host.appendChild(askEl);
  askEl.addEventListener('pointerenter', function () { askP.hover = true; });
  askEl.addEventListener('pointerleave', function () { askP.hover = false; });
  function ask() { game.phase = 'asking'; askP.placed = false; askEl.classList.add('on'); }
  function unask() { askEl.classList.remove('on'); askP.hover = false; if (game.phase === 'asking') game.phase = 'calm'; }
  askEl.querySelector('.yes').addEventListener('click', function () { unask(); arm(performance.now()); });
  askEl.querySelector('.no').addEventListener('click', function () { unask(); game.noAsk = true; });
  var ctl = { exit: exit };
  function arm(now) {
    game.phase = 'armed'; game.armedAt = now; game.nextWord = now + 900; game.wave = 0; game.hits = 0;
    host.classList.add('armed');
    Mode.on(ctl);
  }
  function disarm() { game.phase = 'calm'; host.classList.remove('armed'); endWord(); Mode.off(ctl); }
  /* out of interactive mode by choice: nothing lost, the heart just lets go,
     and this field does not gather again until the page is reloaded */
  function exit() {
    game.off = true;
    disarm();
    while (heart.held.length) release(performance.now(), 60, 180);
  }
  host.addEventListener('pointerdown', function (e) {
    if (game.phase === 'armed' && !e.target.closest('.ask')) Mode.shake();
  });''')
rep('''  function die(now) {
    game.phase = 'dead'; game.deadAt = now;''', '''  function die(now) {
    game.phase = 'dead'; game.deadAt = now;
    Mode.off(ctl);''')
rep('''    var feeding = ptr.on && !dead && (heart.mass === 0''', '''    var feeding = ptr.on && !dead && !game.off && (heart.mass === 0''')
rep('''          if (!armed && heart.mass >= CAP * .5 && !host.classList.contains('condensed')) arm(now);''',
    '''          if (game.phase === 'calm' && !game.noAsk && heart.mass >= CAP * .5 && !host.classList.contains('condensed')) ask();''')
# the pill rides up-right of the heart, loosely; it holds still under the hand
rep('''    if (heart.burst && heart.o < .02) heart.burst = 0;''', '''    if (heart.burst && heart.o < .02) heart.burst = 0;
    if (game.phase === 'asking') {
      if (!heart.mass || host.classList.contains('condensed')) unask();
      else if (!askP.hover) {
        var sb = svg.getBoundingClientRect(), hb = host.getBoundingClientRect();
        var ks = Math.max(sb.width / W, sb.height / H);
        var hx = sb.left - hb.left + (sb.width - W * ks) / 2 + heart.x * ks, hy = sb.top - hb.top + (sb.height - H * ks) / 2 + heart.y * ks;
        var aw = askEl.offsetWidth, ah = askEl.offsetHeight, rr = hr * ks;
        var ax = Math.max(12, Math.min(hb.width - aw - 12, hx + rr * .7 + 14));
        var ay = Math.max(12, Math.min(hb.height - ah - 12, hy - rr * .7 - ah - 10));
        if (!askP.placed) { askP.x = ax; askP.y = ay; askP.placed = true; }
        askP.x += (ax - askP.x) * Math.min(1, 4.5 * dt); askP.y += (ay - askP.y) * Math.min(1, 4.5 * dt);
        askEl.style.transform = 'translate(' + askP.x.toFixed(1) + 'px,' + askP.y.toFixed(1) + 'px)';
      }
    }''')
open(p, 'w', encoding='utf-8', newline='\n').write(s)
a = s.index('/* ==========================================================================\n   THE FIELD')
b = s.index('/* ==========================================================================\n   GRAPHS')
open(os.path.join(ROOT, 'src', 'field_r8.js'), 'w', encoding='utf-8', newline='\n').write(s[a:b].rstrip() + '\n')

# ---- copy ----
cp = os.path.join(ROOT, 'src', 'copy.es.md')
t = open(cp, encoding='utf-8').read()
a = '\n## Pie de página'
assert a in t and 'game.ask:' not in t
t = t.replace(a, '''
game.ask: Pruebe usar IA sin saber cómo.
game.ask.btn: Interactuar
game.ask.no: Ahora no
game.mode: Modo interactivo
game.exit: Salir
''' + a, 1)
open(cp, 'w', encoding='utf-8', newline='\n').write(t)

# ---- CSS ----
c = os.path.join(ROOT, 'site', 'styles.css')
t = open(c, encoding='utf-8').read()
a = '.swapping{opacity:0!important}'
assert t.count(a) == 1
t = t.replace(a, a + '''
/* the ask: a small pill by the heart */
.ask{position:absolute;left:0;top:0;z-index:4;display:flex;align-items:center;gap:8px;padding:5px 5px 5px 15px;
  border-radius:999px;background:rgba(28,26,23,.94);border:1px solid var(--carbon-line);color:var(--on-carbon);
  font-size:.88rem;line-height:1.2;white-space:nowrap;box-shadow:0 16px 32px -16px rgba(0,0,0,.95);
  opacity:0;scale:.9;pointer-events:none;transition:opacity .35s linear,scale .45s cubic-bezier(.16,1,.3,1)}
.ask.on{opacity:1;scale:1;pointer-events:auto}
.ask .yes{font:inherit;font-weight:600;background:var(--gold);color:var(--carbon);border:0;border-radius:999px;
  padding:.5em 1.05em;cursor:pointer;transition:background .2s var(--ease)}
.ask .yes:hover{background:#DDB437}
.ask .no,.mode button svg{flex:none}
.ask .no{display:grid;place-items:center;width:28px;height:28px;border-radius:50%;border:0;background:none;color:var(--on-carbon-dim);cursor:pointer}
.ask .no:hover{background:var(--carbon-2);color:var(--white)}
.ask svg,.mode svg{width:10px;height:10px;stroke:currentColor;stroke-width:1.8;stroke-linecap:round;fill:none}
/* interactive mode: a toast that drops in and settles into a chip */
.mode{position:fixed;top:calc(var(--hdr) + 14px);left:50%;z-index:58;display:flex;align-items:center;gap:10px;
  padding:5px 5px 5px 14px;border-radius:999px;background:var(--carbon);border:1px solid var(--carbon-line);
  color:var(--on-carbon);font-size:.86rem;line-height:1.2;white-space:nowrap;box-shadow:0 16px 32px -16px rgba(0,0,0,.95);
  opacity:0;transform:translate(-50%,-18px);pointer-events:none;
  transition:opacity .35s linear,transform .6s cubic-bezier(.16,1,.3,1),border-color .8s linear,box-shadow .8s linear,padding .6s var(--ease)}
.mode.on{opacity:1;transform:translate(-50%,0);pointer-events:auto}
.mode.fresh{padding:9px 7px 9px 18px;border-color:var(--gold);box-shadow:0 0 0 5px rgba(201,162,39,.16),0 16px 32px -16px rgba(0,0,0,.95)}
.mode .dot{width:8px;height:8px;border-radius:50%;background:var(--gold);animation:modeDot 1.6s ease-in-out infinite}
@keyframes modeDot{0%,100%{opacity:1}50%{opacity:.35}}
.mode button{display:flex;align-items:center;gap:7px;font:inherit;font-weight:600;color:var(--white);background:var(--carbon-2);
  border:1px solid var(--carbon-line);border-radius:999px;padding:.45em .9em;cursor:pointer;transition:background .2s var(--ease)}
.mode button:hover{background:var(--red)}
.mode.shake{animation:modeShake .45s cubic-bezier(.36,.07,.19,.97)}
@keyframes modeShake{15%{translate:-8px 0}35%{translate:7px 0}55%{translate:-5px 0}75%{translate:3px 0}90%{translate:-1px 0}}
.hero.armed .wrap,.close.armed .wrap{pointer-events:none}''', 1)
a = '  .cable .flow,.whyband .suit path,.pointing .cta .point{animation:none!important}'
assert a in t
t = t.replace(a, '  .cable .flow,.whyband .suit path,.pointing .cta .point,.mode .dot,.mode.shake{animation:none!important}')
open(c, 'w', encoding='utf-8', newline='\n').write(t)
print('ok')
