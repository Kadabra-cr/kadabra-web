"""Round 15: the ask stays where it appears and only leans toward the hand;
'¿Interactuar?' alone; a slower difficulty ramp on the old base; shorter,
harder phrases; 'menos de la mitad' instead of 47%."""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..')
p = os.path.join(ROOT, 'src', 'app.src.js')
s = open(p, encoding='utf-8').read()


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:100])
    s = s.replace(a, b)


rep("""  var askEl = document.createElement('div'), askP = { x: 0, y: 0, placed: false, hover: false };
  askEl.className = 'ask';
  askEl.innerHTML = '<span>@@t.game.ask@@</span><button type="button" class="yes">@@t.game.ask.btn@@</button>' +""",
    """  var askEl = document.createElement('div'), askP = { x: 0, y: 0, placed: false, lx: 0, ly: 0, sc: 1 };
  askEl.className = 'ask';
  askEl.innerHTML = '<button type="button" class="yes">@@t.game.ask@@</button>' +""")
rep("""  askEl.addEventListener('pointerenter', function () { askP.hover = true; });
  askEl.addEventListener('pointerleave', function () { askP.hover = false; });
""", "")
rep("function unask() { askEl.classList.remove('on'); askP.hover = false; if",
    "function unask() { askEl.classList.remove('on'); if")
rep("""      else if (!askP.hover) {
        var sb = svg.getBoundingClientRect(), hb = host.getBoundingClientRect();
        var ks = Math.max(sb.width / W, sb.height / H);
        var hx = sb.left - hb.left + (sb.width - W * ks) / 2 + heart.x * ks, hy = sb.top - hb.top + (sb.height - H * ks) / 2 + heart.y * ks;
        var aw = askEl.offsetWidth, ah = askEl.offsetHeight, rr = hr * ks;
        var ax = Math.max(12, Math.min(hb.width - aw - 12, hx + rr * .7 + 14));
        var ay = Math.max(12, Math.min(hb.height - ah - 12, hy - rr * .7 - ah - 10));
        if (!askP.placed) { askP.x = ax; askP.y = ay; askP.placed = true; }
        askP.x += (ax - askP.x) * Math.min(1, 4.5 * dt); askP.y += (ay - askP.y) * Math.min(1, 4.5 * dt);
        askEl.style.transform = 'translate(' + askP.x.toFixed(1) + 'px,' + askP.y.toFixed(1) + 'px)';
      }""", """      else {
        var sb = svg.getBoundingClientRect(), hb = host.getBoundingClientRect();
        var ks = Math.max(sb.width / W, sb.height / H), aw = askEl.offsetWidth, ah = askEl.offsetHeight;
        if (!askP.placed) {
          /* it appears up and to the right of the heart, and stays there */
          var hx = sb.left - hb.left + (sb.width - W * ks) / 2 + heart.x * ks, hy = sb.top - hb.top + (sb.height - H * ks) / 2 + heart.y * ks;
          var rr = hr * ks;
          askP.x = Math.max(12, Math.min(hb.width - aw - 12, hx + rr * .7 + 14));
          askP.y = Math.max(12, Math.min(hb.height - ah - 12, hy - rr * .7 - ah - 10));
          askP.placed = true;
        }
        /* it only leans a few pixels toward the hand and swells as it nears */
        var pxl = sb.left - hb.left + (sb.width - W * ks) / 2 + ptr.x * ks - (askP.x + aw / 2);
        var pyl = sb.top - hb.top + (sb.height - H * ks) / 2 + ptr.y * ks - (askP.y + ah / 2);
        var pd = Math.hypot(pxl, pyl), near1 = ptr.on ? Math.max(0, 1 - pd / 260) : 0;
        var wl = near1 * 6 / (pd || 1);
        askP.lx += (pxl * wl - askP.lx) * Math.min(1, 8 * dt); askP.ly += (pyl * wl - askP.ly) * Math.min(1, 8 * dt);
        askP.sc += (1 + near1 * .06 - askP.sc) * Math.min(1, 8 * dt);
        askEl.style.transform = 'translate(' + (askP.x + askP.lx).toFixed(1) + 'px,' + (askP.y + askP.ly).toFixed(1) + 'px) scale(' + askP.sc.toFixed(3) + ')';
      }""")
# the old base, only a slower climb
rep("var seek = Math.min(2.4, .6 + game.wave * RAMP * .45);", "var seek = Math.min(2.4, 1 + game.wave * RAMP * .3);")
rep("var vmax = (500 + 280 * Math.min(1, age / .5))", "var vmax = (540 + 280 * Math.min(1, age / .5))")
rep("gap: Math.max(260, 520 - game.wave * RAMP * 40)", "gap: Math.max(260, 460 - game.wave * RAMP * 40)")
rep("              heart.hurt = 1; game.hits++; game.hitAge = age;", "              heart.hurt = 1; game.hits++;")
open(p, 'w', encoding='utf-8', newline='\n').write(s)
a = s.index('/* ==========================================================================\n   THE FIELD')
b = s.index('/* ==========================================================================\n   GRAPHS')
open(os.path.join(ROOT, 'src', 'field_r8.js'), 'w', encoding='utf-8', newline='\n').write(s[a:b].rstrip() + '\n')

cp = os.path.join(ROOT, 'src', 'copy.es.md')
t = open(cp, encoding='utf-8').read()


def crep(a, b):
    global t
    assert t.count(a) == 1, a
    t = t.replace(a, b)


crep("game.ask: Pruebe usar IA sin saber cómo.\ngame.ask.btn: Interactuar\n", "game.ask: ¿Interactuar?\n")
crep("viz.aside.pre: Y hoy solo al\n", "viz.aside.pre: Y hoy\n")
crep("viz.aside.fig: 47%\n", "viz.aside.fig: menos de la mitad\n")
crep("viz.cite2: 47% con capacitación &mdash;", "viz.cite2: Menos de la mitad con capacitación &mdash;")
old = [l for l in t.split('\n') if l.startswith('game.words:')][0]
t = t.replace(old, "game.words: La IA inventó cifras para la junta | ChatGPT citó una ley que no existe | "
              "Pegamos la planilla en un chat | Nadie revisó el pago de la IA | El bot prometió lo que no damos | "
              "Se filtraron las cédulas de clientes | Hacienda nos multó por la IA | El contrato traía una cláusula inventada | "
              "La PRODHAB abrió una investigación | Nos demandaron y la IA no responde")
open(cp, 'w', encoding='utf-8', newline='\n').write(t)

c = os.path.join(ROOT, 'site', 'styles.css')
t = open(c, encoding='utf-8').read()
a = ".ask{position:absolute;left:0;top:0;z-index:4;display:flex;align-items:center;gap:8px;padding:5px 5px 5px 15px;"
assert a in t
t = t.replace(a, ".ask{position:absolute;left:0;top:0;z-index:4;display:flex;align-items:center;gap:4px;padding:5px;transform-origin:50% 50%;")
open(c, 'w', encoding='utf-8', newline='\n').write(t)
print('ok')
