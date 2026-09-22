import io, re, os, shutil

os.chdir(os.path.dirname(os.path.abspath(__file__)))
SITE = '..'

# ---------------- shell.html ----------------
h = io.open('shell.html', encoding='utf-8').read()
h = h.replace('<a href="/sources/" data-nav="/sources/">Sources</a>', '<a href="/learn-more/" data-nav="/learn-more/">Learn more</a>')
h = h.replace('<li><a href="/sources/">Sources</a></li>', '<li><a href="/learn-more/">Learn more</a></li>')
# hero: a second, quieter button to the workshop
old = '''    <p><a class="cta rise" href="#TODO-whatsapp">Talk to us on WhatsApp</a></p>
    <p class="fine rise">Opens a WhatsApp chat. No form, nothing to buy.</p>'''
assert old in h
h = h.replace(old, '''    <p class="ctas rise"><a class="cta" href="#TODO-whatsapp">Talk to us on WhatsApp</a>
      <a class="btn go" href="/workshop/">See the workshop</a></p>
    <p class="fine rise">Opens a WhatsApp chat. No form, nothing to buy.</p>''')
# the learn-more route replaces the sources route
a = h.index('<!-- ROUTE: /sources/')
a = h.rindex('<!-- =====', 0, a)
b = h.index('</main>', a) + len('</main>')
h = h[:a] + '''<!-- ======================================================================= -->
<!-- ROUTE: /learn-more/                                                     -->
<!-- ======================================================================= -->
<main class="route" data-route="/learn-more/" @@HIDE_SRC@@>
<section class="band learn">
  <div class="wrap">
    <h2 class="h2 rise">The trick, with receipts.</h2>
    <p class="lede rise">Four numbers explain why we teach the way we do. Each one links to where it came from. Read them, then bring us your team's week.</p>
@@SOURCES@@
    <div class="learn-cta rise">
      <p class="big">Half a day. Your files. Nothing to buy afterwards.</p>
      <p class="ctas"><a class="cta" href="#TODO-whatsapp">Talk to us on WhatsApp</a>
        <a class="btn go dark" href="/workshop/">See the workshop</a></p>
    </div>
@@ALSO@@
  </div>
</section>
@@CLOSE_LEARN@@
</main>''' + h[b:]
io.open('shell.html', 'w', encoding='utf-8').write(h)

# ---------------- build.py ----------------
bp = io.open('build.py', encoding='utf-8').read()
bp = bp.replace('''    "/sources/": dict(
        file="sources/index.html",
        title="Sources. kadabra",
        desc="Every number on the kadabra site, with the figure as published, who published it, and what we took from it."),''',
'''    "/learn-more/": dict(
        file="learn-more/index.html",
        title="Learn more: the numbers behind the workshop. kadabra",
        desc="Four numbers explain why kadabra teaches the way it does. Each one links to the study it came from."),''')
bp = bp.replace('page = page.replace("@@HIDE_SRC@@", "" if route == "/sources/" else "hidden")',
                'page = page.replace("@@HIDE_SRC@@", "" if route == "/learn-more/" else "hidden")')
bp = bp.replace('''        page = page.replace("@@CLOSE_WORK@@", CLOSE.format(k="work"))''',
'''        page = page.replace("@@CLOSE_WORK@@", CLOSE.format(k="work", more=""))
        page = page.replace("@@CLOSE_LEARN@@", CLOSE.format(k="learn", more=MORE))
        page = page.replace("@@ALSO@@", also)''')
bp = bp.replace('''        page = page.replace("@@CLOSE_HOME@@", CLOSE.format(k="home"))''',
                '''        page = page.replace("@@CLOSE_HOME@@", CLOSE.format(k="home", more=MORE))''')
bp = bp.replace('''    <p class="fine rise">Opens a WhatsApp chat. Half a day, on your files, nothing to buy afterwards.</p>
  </div>
</section>"""''', '''    <p class="fine rise">Opens a WhatsApp chat. Half a day, on your files, nothing to buy afterwards.</p>{more}
  </div>
</section>"""

MORE = """
    <p class="more rise"><a class="btn go" href="/workshop/">See what a half-day looks like</a></p>"""''')
bp = bp.replace('    src = sources_markup()\n', '    src, also = sources_markup()\n')

a = bp.index('def sources_markup():')
b = bp.index('def whybands(page):')
bp = bp[:a] + '''MEANS = [
    "Your competitors' tech teams already save time with AI. The tools work. That part is not in question.",
    "Almost nobody has written down what may leave the building, or who checks what. That is the part we fix in an afternoon.",
    "More than half of the people using AI at work were never shown how. Ask around your office.",
    "The biggest gains go to beginners who get taught. That is your team. That is the half-day.",
]


def sources_markup():
    path = os.path.join(SITE, "sources.json")
    if not os.path.exists(path):
        sys.exit("sources.json missing: stopping rather than inventing citations.")
    data = json.load(open(path, encoding="utf-8"))
    out = []
    out.append('    <ol class="beats">')
    for i, r in enumerate(data["shown"]):
        out.append('      <li class="beat rise">')
        out.append('        <b class="fig">%s</b>' % esc(r["figure"]))
        out.append("        <div>")
        out.append('          <p class="claim">%s</p>' % esc(r["claim"]))
        out.append('          <p class="means">%s</p>' % esc(MEANS[i]))
        out.append('          <p class="meta"><a href="%s" rel="noopener noreferrer nofollow" target="_blank">%s, %s</a></p>'
                   % (esc(r["url"]), esc(r["source"]), esc(r["year"])))
        out.append("        </div>")
        out.append('        <span class="rule mid drift" aria-hidden="true"></span>')
        out.append("      </li>")
    out.append("    </ol>")

    also = []
    also.append('    <div class="also rise">')
    also.append("      <h3>Also worth a read</h3>")
    also.append('      <ul class="alsolist">')
    for r in data["alsoRead"]:
        also.append('        <li><a href="%s" rel="noopener noreferrer nofollow" target="_blank">%s</a> <span>%s, %s</span></li>'
                    % (esc(r["url"]), esc(r["claim"]), esc(r["source"]), esc(r["year"])))
    also.append("      </ul>")
    also.append("    </div>")
    return "\\n".join(out), "\\n".join(also)


''' + bp[b:]
io.open('build.py', 'w', encoding='utf-8').write(bp)

# ---------------- app.js (edit both the built file and the src copy) ----------------
for f in [os.path.join(SITE, 'app.js'), 'app.src.js']:
    s = io.open(f, encoding='utf-8').read()
    s = s.replace("    '/sources/': 'Sources. kadabra'", "    '/learn-more/': 'Learn more: the numbers behind the workshop. kadabra'")
    s = s.replace("    grabbed = nb; desk.style.cursor = 'grabbing';", "    grabbed = nb; desk.style.cursor = 'grabbing'; document.body.style.userSelect = 'none';")
    s = s.replace("  function drop() { grabbed = null; desk.style.cursor = ''; }", "  function drop() { grabbed = null; desk.style.cursor = ''; document.body.style.userSelect = ''; }")
    io.open(f, 'w', encoding='utf-8').write(s)

# ---------------- styles.css ----------------
c = io.open(os.path.join(SITE, 'styles.css'), encoding='utf-8').read()
old = '''.whyband:hover,.whyband:focus-within{background:var(--cream-2);
  padding-top:calc(var(--cell)*1.3);padding-bottom:calc(var(--cell)*1.3)}'''
assert old in c
c = c.replace(old, '.whyband:hover,.whyband:focus-within{background:var(--cream-2)}')
a = c.index('.sources{background:var(--cream)')
b = c.index('.srcgroup.also .fig{')
b = c.index('}', b) + 1
c = c[:a] + '''.learn{background:var(--cream);color:var(--ink);min-height:70svh}
.learn .h2{color:var(--ink)}
.learn .lede{color:var(--ink-dim);max-width:58ch}
.beats{list-style:none;margin:calc(var(--cell)*1.6) 0 0;padding:0;counter-reset:beat}
.beat{display:grid;grid-template-columns:minmax(0,9rem) minmax(0,1fr);gap:0 calc(var(--cell)*.9);
  padding:calc(var(--cell)*.9) 0 0}
.beat .fig{font-family:var(--title);font-weight:800;letter-spacing:-.05em;line-height:.9;
  font-size:clamp(3.4rem,8vw,7rem);color:var(--ink)}
.beat:nth-child(2) .fig,.beat:nth-child(4) .fig{color:var(--gold-ink)}
.beat .claim{font-family:var(--title);font-weight:800;letter-spacing:-.03em;line-height:1.05;
  font-size:clamp(1.35rem,2.6vw,2.1rem);color:var(--ink);padding-bottom:.06em}
.beat .means{margin-top:.55em;color:var(--ink-dim);font-size:clamp(1.02rem,1.35vw,1.18rem);max-width:56ch}
.beat .meta{margin-top:.7em;font-size:.92rem}
.beat .meta a{color:var(--ink);text-decoration:underline;text-underline-offset:3px;text-decoration-color:var(--gold-ink)}
.beat .meta a:hover{color:var(--gold-ink)}
.beat .rule{grid-column:1/-1;margin-top:calc(var(--cell)*.9);color:var(--ink);opacity:.22}
.learn-cta{margin-top:calc(var(--cell)*2);text-align:center}
.learn-cta .big{font-family:var(--title);font-weight:800;letter-spacing:-.035em;line-height:1;
  font-size:clamp(1.7rem,4vw,3.2rem);color:var(--ink);padding-bottom:.08em}
.ctas{display:flex;gap:14px;justify-content:center;align-items:center;flex-wrap:wrap;margin-top:calc(var(--cell)*.95)}
.btn.go{padding:.95em 1.5em;font-weight:600}
.btn.dark{border-color:var(--ink);color:var(--ink)}
.btn.dark:hover{background:var(--ink);color:var(--cream);border-color:var(--ink)}
.close .more{margin-top:calc(var(--cell)*.8)}
.also{margin-top:calc(var(--cell)*2.2);border-top:1px solid var(--cream-line);padding-top:calc(var(--cell)*.9)}
.also h3{font-size:clamp(1.1rem,1.8vw,1.4rem);color:var(--ink-dim);padding-bottom:.05em}
.alsolist{list-style:none;margin:calc(var(--cell)*.5) 0 0;padding:0;columns:2;column-gap:calc(var(--cell)*1.2)}
.alsolist li{break-inside:avoid;padding:.45em 0;font-size:.98rem;line-height:1.4}
.alsolist a{color:var(--ink);text-decoration:underline;text-underline-offset:3px;text-decoration-color:var(--gold-ink)}
.alsolist a:hover{color:var(--gold-ink)}
.alsolist span{display:block;color:var(--ink-dim);font-size:.88rem}''' + c[b:]
c = re.sub(r'\n  \.srcitem\{grid-template-columns:minmax\(0,1fr\);gap:\.4em\}', '\n  .beat{grid-template-columns:minmax(0,1fr);gap:.3em}\n  .alsolist{columns:1}', c)
io.open(os.path.join(SITE, 'styles.css'), 'w', encoding='utf-8').write(c)

# old route folder goes away
if os.path.isdir(os.path.join(SITE, 'sources')):
    shutil.rmtree(os.path.join(SITE, 'sources'))
print('patched')
