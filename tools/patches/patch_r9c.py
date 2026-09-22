import io, os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
SITE = '..'


def rd(p): return io.open(p, encoding='utf-8').read()
def wr(p, s): io.open(p, 'w', encoding='utf-8', newline='\n').write(s)
def sub1(s, old, new):
    assert s.count(old) == 1, ('anchor count %d: ' % s.count(old)) + old[:70]
    return s.replace(old, new)


# ============================ app.src.js ====================================
s = rd('app.src.js')

# --- A: rows alternate sides by answer (finish()) ---
s = sub1(s, r"""      var row = document.createElement('div');
      row.className = 'row'; row.dataset.fn = el.dataset.fn;
      var slot = document.createElement('div');
      slot.className = 'slot'; slot.dataset.fn = el.dataset.fn;
      slot.style.width = SLOT.w + 'px'; slot.style.height = SLOT.h + 'px';
      row.appendChild(slot);
      var note = document.createElement('div');
      note.className = 'note'; note.dataset.fn = el.dataset.fn; note.tabIndex = 0;
      note.innerHTML = '<p class="said">You said: <b>' + (right ? 'AI can take it' : 'Best not') + '</b></p>' +
        '<p class="q">' + cd.q + '</p><p class="a">' + (right ? cd.r : cd.l) + '</p>';
      row.appendChild(note);""", r"""      var row = document.createElement('div');
      row.className = 'row'; row.dataset.fn = el.dataset.fn;
      var flip = el.dataset.dir !== 'r';
      if (flip) row.classList.add('flip');
      var slot = document.createElement('div');
      slot.className = 'slot'; slot.dataset.fn = el.dataset.fn;
      slot.style.width = SLOT.w + 'px'; slot.style.height = SLOT.h + 'px';
      var note = document.createElement('div');
      note.className = 'note'; note.dataset.fn = el.dataset.fn; note.tabIndex = 0;
      note.innerHTML = '<p class="said">You said: <b>' + (right ? 'AI can take it' : 'Best not') + '</b></p>' +
        '<p class="q">' + cd.q + '</p><p class="a">' + (right ? cd.r : cd.l) + '</p>';
      if (flip) { row.appendChild(note); row.appendChild(slot); } else { row.appendChild(slot); row.appendChild(note); }""")

# --- B: cables follow the flip (drawCables()) ---
s = sub1(s, r"""    var wires = minis.map(function (m) {
      var note = rows.querySelector('.note[data-fn="' + m.dataset.fn + '"]');
      if (!note) return null;
      var band = m.querySelector('.cband') || m, said = note.querySelector('.said') || note;
      var a1 = band.getBoundingClientRect(), b1 = said.getBoundingClientRect();
      return { fn: m.dataset.fn,
        x1: a1.right - host.left - 2, y1: a1.top + a1.height * .5 - host.top,
        x2: b1.left - host.left - 10, y2: b1.top + b1.height * .5 - host.top };
    }).filter(Boolean);""", r"""    var wires = minis.map(function (m) {
      var note = rows.querySelector('.note[data-fn="' + m.dataset.fn + '"]');
      if (!note) return null;
      var band = m.querySelector('.cband') || m, said = note.querySelector('.said') || note;
      var a1 = band.getBoundingClientRect(), b1 = said.getBoundingClientRect();
      var rowEl = m.closest('.row'), flip = !!(rowEl && rowEl.classList.contains('flip'));
      return flip ? { fn: m.dataset.fn,
        x1: a1.left - host.left + 2, y1: a1.top + a1.height * .5 - host.top,
        x2: b1.right - host.left + 10, y2: b1.top + b1.height * .5 - host.top } : { fn: m.dataset.fn,
        x1: a1.right - host.left - 2, y1: a1.top + a1.height * .5 - host.top,
        x2: b1.left - host.left - 10, y2: b1.top + b1.height * .5 - host.top };
    }).filter(Boolean);""")

# --- B: less slack in the hang ---
s = sub1(s,
    "var len = span * 1.5 + 60, seg = len / (N - 1), pts = [];",
    "var len = span * 1.16 + 24, seg = len / (N - 1), pts = [];")

wr('app.src.js', s)


# ============================ styles.css =====================================
s = rd(f'{SITE}/styles.css')

# --- A/B: .rows gap, drop the divider border, .row.flip columns ---
s = sub1(s, """.rows{display:grid;gap:clamp(18px,2.4vw,30px);position:relative;z-index:1}
.row{display:grid;grid-template-columns:auto minmax(0,1fr);gap:clamp(140px,17vw,280px);align-items:center;
  padding:clamp(10px,1.4vw,18px) 0;border-top:1px solid var(--felt-line)}
.row:first-child{border-top:0}""", """.rows{display:grid;gap:clamp(34px,4vw,56px);position:relative;z-index:1}
.row{display:grid;grid-template-columns:auto minmax(0,1fr);gap:clamp(140px,17vw,280px);align-items:center;
  padding:clamp(10px,1.4vw,18px) 0}
.row.flip{grid-template-columns:minmax(0,1fr) auto}""")

# --- A: right-align the note in flipped rows ---
s = sub1(s,
    ".note .a{color:var(--on-felt);margin-top:.4em;font-size:clamp(.98rem,1.2vw,1.08rem);max-width:52ch}",
    ".note .a{color:var(--on-felt);margin-top:.4em;font-size:clamp(.98rem,1.2vw,1.08rem);max-width:52ch}\n"
    ".row.flip .note{text-align:right}\n"
    ".row.flip .note .a{margin-left:auto}")

# --- C: the finale card, bigger, taller, lower, guides spread ---
s = sub1(s,
    ".finale{margin-top:calc(var(--cell)*2);display:grid;grid-template-columns:1fr auto 1fr;align-items:center;\n"
    "  gap:clamp(18px,3vw,44px)}",
    ".finale{margin-top:calc(var(--cell)*4.2);display:grid;grid-template-columns:1fr auto 1fr;align-items:center;\n"
    "  gap:clamp(30px,5vw,80px)}")

s = sub1(s,
    ".finale .guide{display:flex;gap:12px;justify-content:flex-end;color:var(--gold)}",
    ".finale .guide{display:flex;gap:26px;justify-content:flex-end;color:var(--gold)}")

s = sub1(s,
    ".finale .guide svg{width:18px;height:42px;animation:guideL 1.9s var(--ease) infinite}",
    ".finale .guide svg{width:26px;height:60px;animation:guideL 1.9s var(--ease) infinite}")

s = sub1(s,
    ".fcard{position:relative;width:min(780px,72vw);min-height:clamp(230px,26vw,330px);background:var(--cream);color:var(--ink);",
    ".fcard{position:relative;width:min(980px,80vw);min-height:clamp(320px,36vw,480px);background:var(--cream);color:var(--ink);")

s = sub1(s,
    ".fcard .cband{background:var(--red);color:var(--white);padding:1.1em 1.6em;position:relative;z-index:2}",
    ".fcard .cband{background:var(--red);color:var(--white);padding:1.3em 1.8em;position:relative;z-index:2}")

s = sub1(s,
    ".workshopline{margin:0;font-family:var(--title);font-weight:800;letter-spacing:-.035em;line-height:1.02;\n"
    "  font-size:clamp(1.5rem,3.4vw,2.9rem);color:var(--white);padding-bottom:.08em}",
    ".workshopline{margin:0;font-family:var(--title);font-weight:800;letter-spacing:-.035em;line-height:1.02;\n"
    "  font-size:clamp(1.8rem,4.2vw,3.6rem);color:var(--white);padding-bottom:.08em}")

wr(f'{SITE}/styles.css', s)

print('patch_r9c applied.')
