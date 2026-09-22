import io, os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
SITE = '..'


def rd(p): return io.open(p, encoding='utf-8').read()
def wr(p, s): io.open(p, 'w', encoding='utf-8', newline='\n').write(s)
def sub1(s, old, new):
    assert s.count(old) == 1, ('anchor count %d: ' % s.count(old)) + old[:80]
    return s.replace(old, new)


# ============================ shell.html ====================================
# r10css scope: only the 4 .whyband divs lose tabindex (hover-only, no stuck-open
# band on click). Markup for halfday/hcue/footer/header is untouched here.
h = rd('shell.html')
for suit in ('smooth-spade', 'smooth-heart', 'smooth-diamond', 'smooth-club'):
    h = sub1(h, '<div class="whyband" data-suit="%s" tabindex="0">' % suit,
                 '<div class="whyband" data-suit="%s">' % suit)
wr('shell.html', h)


# ============================ styles.css ====================================
c = rd(os.path.join(SITE, 'styles.css'))

# --- 3. noise custom property, defined once in :root -------------------------
c = sub1(c, '''  --hdr:72px;

  /* ---- THE CHEVRON RULE (DESIGN.md "Chevron rule") -----------------------''',
'''  --hdr:72px;
  /* a faint film-grain filter, tiled as a background-image on carbon surfaces only */
  --noise:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='160' height='160'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");

  /* ---- THE CHEVRON RULE (DESIGN.md "Chevron rule") -----------------------''')

# --- 1. why-us: hover-only, no :focus-within stuck-open state ----------------
# the suit travels further, tilts, alternates direction per band; the text
# nudges right; height never changes (no new box-affecting properties touched).
c = sub1(c, '''/* hover: the suit leaves its cell, grows to the left, settles, breathes. Never a snap. */
.whyband:hover,.whyband:focus-within{background:var(--cream-2);z-index:2}
.whyband:hover .suit,.whyband:focus-within .suit{opacity:1;color:var(--gold-ink);
  transform:translateX(-14%) scale(2.15)}
.whyband:hover .suit path,.whyband:focus-within .suit path{animation:breathe 3.4s ease-in-out .75s infinite}
@keyframes breathe{0%,100%{transform:scale(1)}50%{transform:scale(1.045)}}
.bands:hover .whyband:not(:hover):not(:focus-within){opacity:.55}
.whyband{transition:opacity .5s var(--ease),background .4s var(--ease)}
.whyband .t{font-family:var(--title);font-weight:800;letter-spacing:-.035em;
  font-size:clamp(1.45rem,3.5vw,2.7rem);line-height:1.02;padding-bottom:.06em;transition:transform .7s var(--ease)}
.js .whyband .t{transform:translateY(12px)}
.js .whyband.on .t{transform:none}
.whyband .pf{margin-top:.45em;color:var(--ink-dim);font-size:clamp(.98rem,1.25vw,1.1rem)}
.whyband .rule{margin-top:.6em;color:var(--ink);opacity:.22;
  transition:opacity .5s linear,color .5s linear,clip-path .9s var(--ease)}
.js .whyband .rule{clip-path:inset(0 100% 0 0)}
.js .whyband.on .rule{clip-path:inset(0 0 0 0)}
.whyband:hover .rule,.whyband:focus-within .rule{opacity:.8;color:var(--gold-ink)}''',
'''/* hover only: the suit leaves its cell, grows to the left, tilts, settles, breathes.
   No :focus-within: a click must never leave a band stuck open (no tabindex any more). */
.whyband:hover{background:var(--cream-2);z-index:2}
.whyband>div{transition:transform .7s cubic-bezier(.16,1,.3,1)}
.whyband:hover>div{transform:translateX(10px)}
.whyband:hover .suit{opacity:1;color:var(--gold-ink);
  transform:translateX(-15%) rotate(-7deg) scale(2.1)}
.whyband:nth-child(2n):hover .suit{transform:translateX(-15%) rotate(7deg) scale(2.1)}
.whyband:hover .suit path{animation:breathe 3.4s ease-in-out .75s infinite}
@keyframes breathe{0%,100%{transform:scale(1)}50%{transform:scale(1.045)}}
.bands:hover .whyband:not(:hover){opacity:.55}
.whyband{transition:opacity .5s var(--ease),background .4s var(--ease)}
.whyband .t{font-family:var(--title);font-weight:800;letter-spacing:-.035em;
  font-size:clamp(1.45rem,3.5vw,2.7rem);line-height:1.02;padding-bottom:.06em;transition:transform .7s var(--ease)}
.js .whyband .t{transform:translateY(12px)}
.js .whyband.on .t{transform:none}
.whyband .pf{margin-top:.45em;color:var(--ink-dim);font-size:clamp(.98rem,1.25vw,1.1rem)}
.whyband .rule{margin-top:.6em;color:var(--ink);opacity:.22;
  transition:opacity .5s linear,color .5s linear,clip-path .9s var(--ease)}
.js .whyband .rule{clip-path:inset(0 100% 0 0)}
.js .whyband.on .rule{clip-path:inset(0 0 0 0)}
.whyband:hover .rule{opacity:.8;color:var(--gold-ink)}''')

# --- 2. footer logo, bigger --------------------------------------------------
c = sub1(c, '.footbrand svg{height:32px;width:auto;color:var(--white);display:block}',
             '.footbrand svg{height:52px;width:auto;color:var(--white);display:block}')

# --- 4. halfday CTA: the loudest thing on the card; hcue: quiet but alive ----
c = sub1(c, '''.btn.light{border:2px solid var(--gold);color:var(--gold);padding:calc(1.05em - 2px) 1.6em}
.btn.light:hover{background:var(--gold);color:var(--carbon);border-color:var(--gold)}''',
'''.btn.light{background:var(--gold);color:var(--carbon);border:2px solid var(--gold);
  font-size:clamp(1.15rem,1.6vw,1.25rem);padding:calc(1.15em - 2px) 2.2em;
  transition:background .25s var(--ease),color .25s var(--ease),border-color .25s var(--ease),
  transform .25s var(--ease),box-shadow .25s var(--ease)}
.btn.light:hover{background:var(--gold);color:var(--carbon);border-color:var(--gold);
  transform:translateY(-3px);box-shadow:0 16px 30px -12px rgba(201,162,39,.55)}''')
c = sub1(c, '''html.staged .hcue{display:grid;justify-items:center;gap:8px;margin-top:calc(var(--cell)*1.4);
  color:var(--gold);font-size:.74rem;letter-spacing:.16em;text-transform:uppercase;opacity:calc(var(--e)*8 - 7)}''',
'''html.staged .hcue{display:grid;justify-items:center;gap:8px;margin-top:calc(var(--cell)*1.4);
  color:var(--on-carbon-dim);font-size:.68rem;letter-spacing:.16em;text-transform:uppercase;opacity:calc(var(--e)*8 - 7)}''')

# --- 3. apply the grain: header, the carbon stat card, halfday, footer ------
# each gets its own stacking context so the overlay (z-index:-1) can never sit
# above real content/links; .hdr already has position+z-index from the sticky bar.
c = sub1(c, '.btn.light:hover{background:var(--gold);color:var(--carbon);border-color:var(--gold);\n  transform:translateY(-3px);box-shadow:0 16px 30px -12px rgba(201,162,39,.55)}',
'''.btn.light:hover{background:var(--gold);color:var(--carbon);border-color:var(--gold);
  transform:translateY(-3px);box-shadow:0 16px 30px -12px rgba(201,162,39,.55)}

/* ---------- film grain on carbon surfaces only (header, stat card, halfday, footer) --- */
.hdr{isolation:isolate}
footer,.pair .b,.halfday{position:relative;isolation:isolate}
.hdr::before,footer::before,.pair .b::before,.halfday::before{
  content:"";position:absolute;inset:0;z-index:-1;pointer-events:none;
  background-image:var(--noise);background-size:160px 160px;
  opacity:.04;mix-blend-mode:soft-light}
.halfday::before{border-radius:inherit}''')

wr(os.path.join(SITE, 'styles.css'), c)
print('patched r10css')
