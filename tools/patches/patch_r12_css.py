"""Round 12 CSS: the breath before the graph, timed graphs, corner indices on
sideways cards (equal margins, red suits red), no text selection at the table,
the defeat pointer, the WhatsApp mark on every WhatsApp button."""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..')
p = os.path.join(ROOT, 'site', 'styles.css')
s = open(p, encoding='utf-8').read()


def rep(a, b):
    global s
    assert s.count(a) == 1, a[:90]
    s = s.replace(a, b)


rep('html.staged #morph{--len:3.4;--r:0}', 'html.staged #morph{--len:4.1;--p:0}')
rep('html.staged #vizscr{--len:2.9}', 'html.staged #vizscr{--len:2.5}')
rep('html.staged .policy .barcol{opacity:calc(var(--r)*6 - .5)}',
    '''html.staged .policy .barcol{opacity:0;transition:opacity .6s linear .25s}
html.staged .graph .policy .barcol{opacity:1}''')
rep('''html.staged .policy .pair{grid-area:1/1/2/3;order:0;margin:0;align-self:stretch;z-index:2;pointer-events:none;
  transform-origin:0 100%;transform:scale(calc(1 - var(--r)*.5));opacity:calc(1.15 - var(--r)*5.5)}''',
    '''html.staged .policy .pair{grid-area:1/1/2/3;order:0;margin:0;align-self:stretch;z-index:2;pointer-events:none;position:relative;
  transform-origin:0 100%;transform:scale(calc(1 - var(--p)*.035));
  transition:transform .8s cubic-bezier(.16,1,.3,1),opacity .45s linear}
/* the breath: a gold rule fills under the two cards as the scroll carries on */
html.staged .policy .pair::after{content:"";position:absolute;left:0;bottom:-14px;height:3px;width:100%;background:var(--gold-ink);
  transform-origin:0 50%;transform:scaleX(var(--p))}
html.staged .graph .policy .pair{transform:scale(.5);opacity:0}''')

# sideways cards: the indices sit in the corners with the same margin on every
# side (the box is turned about its own corner), red suits in red
rep('''.card.desk .ix.ixa,.fcard .ix.ixa{top:14px;left:auto;right:15px;transform:rotate(90deg)}
.card.desk .ix.ixb,.fcard .ix.ixb{bottom:14px;right:auto;left:15px;transform:rotate(-90deg)}''',
    '''.card.desk .ix.ixa,.fcard .ix.ixa{top:14px;right:14px;left:auto;bottom:auto;transform-origin:100% 0;transform:rotate(90deg) translateX(100%)}
.card.desk .ix.ixb,.fcard .ix.ixb{bottom:14px;left:14px;right:auto;top:auto;transform-origin:0 100%;transform:rotate(-90deg) translateY(100%)}
.card.red .ix,.fcard.red .ix{color:var(--red)}''')
# the finale card's own corner rules came later and pulled the indices to the middle
rep('''.fcard .ix.ixa{top:16px;left:18px}
.fcard .ix.ixb{bottom:16px;right:18px;transform:rotate(180deg)}''', '')
rep('''.fcard .ix{position:absolute;display:grid;justify-items:center;gap:3px;font-family:var(--body);font-weight:600;font-size:1.05rem;line-height:1;color:var(--ink)}''',
    '''.fcard .ix{position:absolute;display:grid;justify-items:center;gap:3px;font-family:var(--body);font-weight:600;font-size:1.15rem;line-height:1;color:var(--ink)}
.fcard .ix.ixa{top:18px;right:18px}
.fcard .ix.ixb{bottom:18px;left:18px}''')

# the table and the desk are for dragging, not selecting
rep('''.swipe{background:var(--felt)}''', '''.swipe{background:var(--felt);-webkit-user-select:none;user-select:none}''')

# the defeat pointer: a small spade beside the button, nudging toward it
rep('''.swapping{opacity:0!important}''', '''.swapping{opacity:0!important}
.cta{position:relative}
.cta .point{position:absolute;right:calc(100% + 14px);top:50%;width:30px;height:30px;margin-top:-15px;color:var(--gold);
  opacity:0;transform:rotate(90deg);transition:opacity .35s linear;pointer-events:none}
.pointing .cta .point{opacity:1;animation:point 1.1s cubic-bezier(.45,0,.2,1) infinite}
@keyframes point{0%,100%{transform:translateX(-8px) rotate(90deg)}50%{transform:translateX(2px) rotate(90deg)}}''')

# the WhatsApp mark, left of the words
rep('''.cta:hover{background:var(--red-lift);''', '''.cta.wa{display:inline-flex;align-items:center;gap:.6em}
.cta .wamark{width:1.2em;height:1.2em;flex:none;display:block}
.cta:hover{background:var(--red-lift);''')
rep('''  .cable .flow,.whyband .suit path{animation:none!important}''',
    '''  .cable .flow,.whyband .suit path,.pointing .cta .point{animation:none!important}''')
open(p, 'w', encoding='utf-8', newline='\n').write(s)

# ---- markup: the mark in every WhatsApp button, the pointer in the game ones ----
WA = '<svg class="wamark" viewBox="0 0 24 24" aria-hidden="true"><use href="#whatsapp"/></svg>'
PT = '<svg class="point" viewBox="0 0 100 100" aria-hidden="true"><use href="#classic-spade"/></svg>'
sh = os.path.join(ROOT, 'src', 'shell.html')
t = open(sh, encoding='utf-8').read()
a = '<a class="cta" href="@@t.wa.link@@">@@t.cta.whatsapp@@</a>'
assert t.count(a) == 3
t = t.replace('<p class="ctas rise">' + a, '<p class="ctas rise"><a class="cta wa" href="@@t.wa.link@@">' + PT + WA + '@@t.cta.whatsapp@@</a>', 1)
t = t.replace(a, '<a class="cta wa" href="@@t.wa.link@@">' + WA + '@@t.cta.whatsapp@@</a>')
open(sh, 'w', encoding='utf-8', newline='\n').write(t)
bp = os.path.join(ROOT, 'src', 'build.py')
t = open(bp, encoding='utf-8').read()
a = '<p><a class="cta rise" href="@@t.wa.link@@">@@t.cta.book@@</a></p>'
assert a in t
t = t.replace(a, '<p><a class="cta wa rise" href="@@t.wa.link@@">' + PT + WA + '@@t.cta.book@@</a></p>')
open(bp, 'w', encoding='utf-8', newline='\n').write(t)

# the WhatsApp glyph joins the sprite sheet (Simple Icons, CC0)
sp = os.path.join(ROOT, 'site', 'sprites.svg')
t = open(sp, encoding='utf-8').read()
if 'id="whatsapp"' not in t:
    sym = ('<symbol id="whatsapp" viewBox="0 0 24 24"><title>WhatsApp</title><path fill="currentColor" d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/></symbol>')
    i = t.rindex('</svg>')
    t = t[:i] + sym + '\n' + t[i:]
    open(sp, 'w', encoding='utf-8', newline='\n').write(t)
print('ok')
