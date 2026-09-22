"""Round 11 CSS: the finish veil, phone piles, the phone desk, sideways indices."""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(HERE, '..', '..', 'site', 'styles.css')
s = open(p, encoding='utf-8').read()


def rep(a, b):
    global s
    assert s.count(a) == 1, a[:90]
    s = s.replace(a, b)


rep('''.veil{position:absolute;inset:0;z-index:6;display:grid;place-items:center;background:var(--felt-deep);
  opacity:0;transition:opacity .55s linear;pointer-events:none}
.veil.on{opacity:1}
.veil svg{width:min(360px,46vw);height:auto;color:var(--white);
  opacity:0;transform:translateY(14px) scale(.96);transition:opacity .6s linear .1s,transform .9s cubic-bezier(.16,1,.3,1) .1s}
.veil.on svg{opacity:1;transform:none}''',
'''/* the finish: the table fades, the mark holds the screen with a turning ring,
   then lets go. Under the header, over everything else (piled cards included). */
.swipe .wrap{transition:opacity .45s linear}
.swipe.clearing .wrap{opacity:0}
.veil{position:fixed;left:0;right:0;bottom:0;top:var(--hdr);z-index:59;display:grid;place-items:center;align-content:center;gap:34px;
  background:var(--felt-deep);opacity:0;transition:opacity .6s linear;pointer-events:none}
.veil.on{opacity:1;pointer-events:auto}
.veil.on.out{opacity:0;transition-duration:.9s}
.veil .mark{width:min(360px,62vw);height:auto;color:var(--white);
  opacity:0;transform:translateY(14px) scale(.96);transition:opacity .6s linear .15s,transform .9s cubic-bezier(.16,1,.3,1) .15s}
.veil.on .mark{opacity:1;transform:none}
.veil.out .mark{transform:translateY(-10px);transition-delay:0s}
.veil .ring{width:30px;height:30px;opacity:0;transition:opacity .5s linear .5s;animation:ring 1.1s linear infinite}
.veil.on .ring{opacity:.9}
.veil.out .ring{opacity:0;transition-delay:0s}
.veil .ring circle{fill:none;stroke:var(--gold);stroke-width:3;stroke-linecap:round;stroke-dasharray:62 101}
@keyframes ring{to{transform:rotate(1turn)}}''')

rep('''.row{display:grid;grid-template-columns:auto minmax(0,1fr);gap:clamp(140px,17vw,280px);align-items:center;''',
    '''.row{display:grid;grid-template-columns:auto minmax(0,1fr);gap:clamp(110px,12vw,200px);align-items:center;''')

# a card lying on its side: the indices and the pip turn with it
rep('''.card.desk .pip{width:34%}
.card.desk .ix{font-size:.95rem}''', '''.card.desk .pip{width:34%;transform:translate(-50%,-50%) rotate(90deg)}
.card.desk .ix{font-size:.95rem}
.card.desk .ix.ixa,.fcard .ix.ixa{top:14px;left:auto;right:15px;transform:rotate(90deg)}
.card.desk .ix.ixb,.fcard .ix.ixb{bottom:14px;right:auto;left:15px;transform:rotate(-90deg)}''')
rep('''.fcard .pip{position:absolute;top:50%;left:50%;width:36%;transform:translate(-50%,-50%);color:var(--ink);opacity:.07}''',
    '''.fcard .pip{position:absolute;top:50%;left:50%;width:36%;transform:translate(-50%,-50%) rotate(90deg);color:var(--ink);opacity:.07}''')

rep('''@media (max-width:900px){
  .table{grid-template-columns:minmax(0,1fr);justify-items:center}
  .pile{min-height:0;width:100%;max-width:340px;order:2}
  .pile.r{order:3}
  .deck{order:1;margin-inline:auto}
  .pile .stack{--ov:-84px}
  .row{gap:clamp(40px,8vw,70px)}
}''', '''.btn .tally{display:none}
/* phones: the deck alone on the table; the two answer buttons are the piles */
@media (max-width:900px){
  .table{display:flex;justify-content:center}
  .table .pile{display:none}
  .deck{width:min(74vw,300px)}
  .btns{display:grid;grid-template-columns:1fr 1fr;gap:10px;max-width:440px;margin-inline:auto;margin-top:calc(var(--cell)*1.1)}
  .btns #bSkip{grid-column:1/-1;justify-self:center}
  #bLeft,#bRight{position:relative;display:grid;align-content:space-between;gap:10px;min-height:92px;padding:.85em .95em;
    text-align:left;line-height:1.2;border-color:var(--felt-line);background:rgba(18,38,31,.45);
    transition:border-color .25s var(--ease),background .25s var(--ease),transform .25s var(--ease)}
  #bRight{text-align:right;justify-items:end}
  #bLeft:hover,#bRight:hover{background:rgba(18,38,31,.45);color:var(--on-felt)}
  #bLeft.hot,#bRight.hot{border-color:var(--white);color:var(--white)}
  #bLeft.nudge,#bRight.nudge{border-color:var(--gold);color:var(--gold)}
  #bLeft.landed,#bRight.landed{animation:landed .5s var(--ease)}
  @keyframes landed{0%{transform:scale(1)}35%{transform:scale(1.045)}100%{transform:scale(1)}}
  .btn .tally{display:flex;min-height:22px}
  #bRight .tally{flex-direction:row-reverse}
  .tally i{width:15px;height:21px;border-radius:2px;background:var(--cream);position:relative;overflow:hidden;
    box-shadow:0 3px 6px -3px rgba(0,0,0,.8);animation:tallyIn .45s cubic-bezier(.16,1,.3,1) both}
  .tally i+i{margin-left:-4px}
  #bRight .tally i+i{margin-left:0;margin-right:-4px}
  .tally i::after{content:"";position:absolute;left:0;right:0;top:38%;height:26%;background:var(--red)}
  .tally i:nth-child(odd){transform:rotate(-5deg)}
  .tally i:nth-child(even){transform:rotate(4deg)}
  @keyframes tallyIn{from{opacity:0;translate:0 -10px;scale:.6}to{opacity:1;translate:0 0;scale:1}}
  .hint{margin-top:calc(var(--cell)*.5)}
  /* the phone desk: one column, the note under its card, no cables */
  .cables{display:none}
  .rows{gap:calc(var(--cell)*1.6)}
  .row,.row.flip{grid-template-columns:minmax(0,1fr);gap:16px;justify-items:center;padding:0}
  .row .slot{max-width:100%}
  .row .note,.row.flip .note{text-align:left;width:100%}
  .row.flip .note .a{margin-left:0}
  .row.dealt,.row.dealt.flip{transform:translateY(24px)}
}''')
open(p, 'w', encoding='utf-8', newline='\n').write(s)
print('ok')
