import io, os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
SITE = '..'


def rd(p): return io.open(p, encoding='utf-8').read()
def wr(p, s): io.open(p, 'w', encoding='utf-8', newline='\n').write(s)
def sub1(s, old, new):
    assert s.count(old) == 1, ('anchor count %d: ' % s.count(old)) + old[:80]
    return s.replace(old, new)


# ============================ app.src.js ====================================
s = rd('app.src.js')

# --- the deal is over: the table clears to the mark, then the rows are dealt ---
a = s.index('  function finish() {')
b = s.index('  /* Each card hangs a cable to its note.')
s = s[:a] + '''  /* The hand is played. The table clears to the mark, and while it holds the
     screen the desk is laid out behind it: one row dealt after another. */
  function finish() {
    if (done) return;
    done = true;
    stopNudge();
    var narrow = innerWidth <= 900;
    var wrapW = desk.getBoundingClientRect().width;
    SLOT.w = Math.round(Math.min(narrow ? wrapW : 420, wrapW * (narrow ? 1 : .42))); SLOT.h = Math.round(SLOT.w * .6);
    minis = [];
    btns.hidden = true; hint.hidden = true;

    function lay() {
      heads.classList.add('flip'); stage.classList.add('flip');
      rows.innerHTML = '';
      els.forEach(function (el) {
        var cd = CARDS[els.indexOf(el)], right = el.dataset.dir === 'r', flip = !right;
        var row = document.createElement('div');
        row.className = 'row' + (flip ? ' flip' : '') + (reduce ? '' : ' dealt');
        row.dataset.fn = el.dataset.fn;
        var slot = document.createElement('div');
        slot.className = 'slot'; slot.dataset.fn = el.dataset.fn;
        slot.style.width = SLOT.w + 'px'; slot.style.height = SLOT.h + 'px';
        var note = document.createElement('div');
        note.className = 'note'; note.dataset.fn = el.dataset.fn; note.tabIndex = 0;
        note.innerHTML = '<p class="said">You said: <b>' + (right ? 'AI can take it' : 'Best not') + '</b></p>' +
          '<p class="q">' + cd.q + '</p><p class="a">' + (right ? cd.r : cd.l) + '</p>';
        if (flip) { row.appendChild(note); row.appendChild(slot); } else { row.appendChild(slot); row.appendChild(note); }
        rows.appendChild(row);
        slot.appendChild(el);
        el.classList.remove('piled'); el.classList.add('desk');
        el.style.zIndex = ''; el.style.pointerEvents = ''; el.style.transition = 'none'; el.style.transform = 'none';
        el.style.width = SLOT.w + 'px'; el.style.height = SLOT.h + 'px';
        minis.push(slot);
      });
      reveal.hidden = false;
      if (reduce) { rows.querySelectorAll('.row').forEach(function (r) { r.classList.remove('dealt'); }); drawCables(); return; }
      /* dealt one after another, each from its own side of the table */
      var list = [].slice.call(rows.querySelectorAll('.row'));
      list.forEach(function (r, i) { setTimeout(function () { r.classList.remove('dealt'); }, 120 + i * 170); });
      setTimeout(drawCables, 120 + list.length * 170 + 700);
    }

    if (reduce) { lay(); return; }
    /* the mark holds the screen while the desk is laid out behind it */
    var veil = document.createElement('div');
    veil.className = 'veil';
    veil.innerHTML = '<svg viewBox="0 0 1703.11 435.6" aria-hidden="true"><use href="#logo-full" width="1703.11" height="435.6"/></svg>';
    desk.parentNode.insertBefore(veil, desk);
    requestAnimationFrame(function () { veil.classList.add('on'); });
    setTimeout(lay, 900);
    setTimeout(function () { veil.classList.remove('on'); }, 1500);
    setTimeout(function () { if (veil.parentNode) veil.parentNode.removeChild(veil); }, 2400);
  }

''' + s[b:]

# the rows are gone on a new deal
s = sub1(s, "    rows.innerHTML = '';\n    idx = 0; done = false; touched = false;",
            "    rows.innerHTML = '';\n    document.querySelectorAll('#swipe .veil').forEach(function (v) { v.parentNode.removeChild(v); });\n    idx = 0; done = false; touched = false;")

# --- the stage: the numbers read at full size, so no screen is pinned ---
s = sub1(s, '''      if (morph) {
        var mr = morph.getBoundingClientRect();
        var r = clamp((HDR - mr.top) / (morph.offsetHeight - ph || 1));
        morph.style.setProperty('--r', r.toFixed(4));
        if (typeof policyG !== 'undefined' && policyG) policyG.set(r);
      }''',
'''      if (morph) {
        /* the cards become the graph as the block crosses the screen */
        var mr = morph.getBoundingClientRect();
        var r = clamp((ph * .86 - mr.top) / (ph * .52));
        morph.style.setProperty('--r', r.toFixed(4));
        if (typeof policyG !== 'undefined' && policyG) policyG.set(r);
      }''')
# the half-day card grows and stays: carbon gives way to the felt below it
s = sub1(s, "      var e = p < .38 ? p / .38 : p < .62 ? 1 : 1 - (p - .62) / .38;",
            "      var e = p / .45;")
wr('app.src.js', s)


# ============================ styles.css ====================================
c = rd(os.path.join(SITE, 'styles.css'))

# the hero keeps its voice when it steps aside
c = sub1(c, "html.staged .hero h1{font-size:calc(clamp(2.55rem,7.2vw,6.6rem)*(1 - var(--q)*.45))}",
            "html.staged .hero h1{font-size:calc(clamp(2.55rem,7.2vw,6.6rem)*(1 - var(--q)*.2))}")
c = sub1(c, "html.staged .split{display:grid;grid-template-columns:40% 60%;",
            "html.staged .split{display:grid;grid-template-columns:36% 64%;")
c = sub1(c, "html.staged .hero{grid-column:1;position:sticky;top:var(--hdr);height:calc(100svh - var(--hdr));min-height:0;\n  width:calc(100% + (1 - var(--q))*150%);",
            "html.staged .hero{grid-column:1;position:sticky;top:var(--hdr);height:calc(100svh - var(--hdr));min-height:0;\n  width:calc(100% + (1 - var(--q))*178%);")
# copy that changes, changes by fading
c = sub1(c, ".hero h1,.hero .sub,.close h2,.close .fine{transition:opacity .4s linear}",
            ".hero h1,.hero .sub,.close h2,.close .fine{transition:opacity .35s linear}\n.swapping{opacity:0!important}")

# the numbers: one block, read at the size of the taught graph, nothing pinned
old = c[c.index("html.staged .morph{height:"):c.index("html.staged .stage-right .viz{margin-top:0}")]
new = '''html.staged .morph{--r:0}
html.staged .morph-pin{display:block}
html.staged .breaks{padding:calc(var(--cell)*2.2) 0 0}
html.staged .policy .vizgrid{grid-template-columns:minmax(0,1fr);gap:clamp(20px,2.4vw,36px)}
html.staged .policy .bars{grid-template-columns:repeat(2,minmax(0,220px));gap:clamp(20px,2.6vw,44px)}
html.staged .policy .barcol.base{grid-area:1/1}
html.staged .policy .barcol.rules{grid-area:1/2}
html.staged .policy .barcol{opacity:calc(var(--r)*5 - .6)}
html.staged .policy .pair{grid-area:1/1/2/3;order:0;margin:0;align-self:end;z-index:2;pointer-events:none;
  transform-origin:50% 100%;transform:scale(calc(1 - var(--r)*.35));opacity:calc(1.35 - var(--r)*4.4)}
html.staged .policy .pair>div{padding:calc(var(--cell)*.75) calc(var(--cell)*.6) calc(var(--cell)*.85);
  min-height:290px;display:grid;align-content:end}
html.staged .policy .pair .fignum{font-size:clamp(3rem,5.4vw,4.8rem)}
html.staged .policy .pair p{font-size:.96rem;max-width:none}
html.staged .policy .story{margin-top:calc(var(--cell)*1.1)}
'''
c = c.replace(old, new)
# the smaller type the pinned screen needed is no longer wanted
for dead in ["html.staged .policy .beat-l{font-size:clamp(1.15rem,1.6vw,1.5rem)}\n",
             "html.staged .policy .aside{margin-top:calc(var(--cell)*.5);font-size:1rem}\n",
             "html.staged .policy .cites{margin-top:calc(var(--cell)*.5)}\n",
             "html.staged .stage-right .h2{font-size:clamp(2.2rem,3.8vw,3.6rem)}\n",
             "html.staged .stage-right .viz h3{font-size:clamp(2rem,3.6vw,3.4rem)}\n",
             "html.staged .policy{margin-top:calc(var(--cell)*.9)!important}\n"]:
    if dead in c: c = sub1(c, dead, '')   # some lived inside the block above
c = sub1(c, "html.staged #viz .bars{grid-template-columns:repeat(2,minmax(0,220px))}",
            "html.staged #viz .bars{grid-template-columns:repeat(2,minmax(0,220px))}\nhtml.staged .stage-right .h2{font-size:clamp(2.4rem,4.4vw,4rem)}")

# the desk: the mark holds the screen, then the rows are dealt
c = sub1(c, '''.rows{display:grid;''', '''.veil{position:absolute;inset:0;z-index:6;display:grid;place-items:center;background:var(--felt-deep);
  opacity:0;transition:opacity .55s linear;pointer-events:none}
.veil.on{opacity:1}
.veil svg{width:min(360px,46vw);height:auto;color:var(--white);
  opacity:0;transform:translateY(14px) scale(.96);transition:opacity .6s linear .1s,transform .9s cubic-bezier(.16,1,.3,1) .1s}
.veil.on svg{opacity:1;transform:none}
.row{transition:opacity .5s linear,transform .8s cubic-bezier(.16,1,.3,1)}
.row.dealt{opacity:0;transform:translateX(-7%) rotate(-1.4deg)}
.row.dealt.flip{transform:translateX(7%) rotate(1.4deg)}
.rows{display:grid;''')
c = sub1(c, ".desk{position:relative;margin-top:calc(var(--cell)*1.4)}", ".desk{position:relative;margin-top:calc(var(--cell)*1.4)}\n.swipe .wrap{position:relative}")

# the half-day card grows and holds; the felt below rises over it
c = sub1(c, "html.staged .hstage{height:calc((100svh - var(--hdr))*2.6);background:var(--cream);--e:0}",
            "html.staged .hstage{height:calc((100svh - var(--hdr))*2);background:var(--cream);--e:0}")
wr(os.path.join(SITE, 'styles.css'), c)
print('patched r10')
