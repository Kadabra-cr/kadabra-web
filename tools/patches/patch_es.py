"""Turn the hard-coded English copy into tokens read from src/copy.es.md."""
import io, os, re

os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))


def rd(p): return io.open(p, encoding='utf-8').read()
def wr(p, s): io.open(p, 'w', encoding='utf-8', newline='\n').write(s)


def swap(path, pairs, exact=True):
    s = rd(path)
    for old, key in pairs:
        tok = '@@t.%s@@' % key
        n = s.count(old)
        assert n == (1 if exact else n) and n >= 1, 'in %s, %d hits for: %s' % (path, n, old[:70])
        s = s.replace(old, tok)
    wr(path, s)


SHELL = [
    ('>Skip to content<', '>@@t.nav.skip@@<'),
]

# ---------------------------------------------------------------- shell.html
s = rd('src/shell.html')
pairs = [
    ('Skip to content', 'nav.skip'),
    ('<a href="/workshop/" data-nav="/workshop/">The workshop</a>', None),
]
# straightforward one-for-one text swaps
text_keys = [
    ('Skip to content', 'nav.skip'),
    ('>The workshop</a>\n      <a href="/learn-more/"', '>@@t.nav.workshop@@</a>\n      <a href="/learn-more/"'),
]
s = s.replace('Skip to content', '@@t.nav.skip@@')
s = s.replace('data-nav="/workshop/">The workshop<', 'data-nav="/workshop/">@@t.nav.workshop@@<')
s = s.replace('data-nav="/learn-more/">Learn more<', 'data-nav="/learn-more/">@@t.nav.learn@@<')
s = s.replace('>Talk to us on WhatsApp<', '>@@t.cta.whatsapp@@<')
s = s.replace('The trick is teaching, not tools.', '@@t.hero.h1@@')
s = s.replace('Half-day, hands-on AI workshops for teams in Costa Rica. Your real work, your tools, nothing to buy afterwards.', '@@t.hero.sub@@')
s = s.replace('See the workshop<svg class="arr"', '@@t.hero.btn@@<svg class="arr"')
s = s.replace('Opens a WhatsApp chat. No form, nothing to buy.', '@@t.hero.fine@@')
s = s.replace('<span>Scroll</span>', '<span>@@t.hero.cue@@</span>')
s = s.replace("It works. Until it doesn't.", '@@t.breaks.h2@@')
s = s.replace('of Costa Rican tech companies save time on repetitive tasks with AI.', '@@t.breaks.a.text@@')
s = s.replace('of them have any formal AI policy.', '@@t.breaks.b.text@@')
s = s.replace('>PROCOMER, 2025<', '>@@t.breaks.src@@<')
s = s.replace('aria-label="Two bars of a hundred marks each. Ninety-three lit in the first: companies that save time with AI. Nine lit in the second: companies with any AI policy."',
              'aria-label="@@t.policy.aria@@"')
s = s.replace('<figcaption><b>93%</b><span>Save time with AI</span></figcaption>',
              '<figcaption><b>@@t.policy.capA.fig@@</b><span>@@t.policy.capA.label@@</span></figcaption>')
s = s.replace('<figcaption><b>9%</b><span>Have any AI policy</span></figcaption>',
              '<figcaption><b>@@t.policy.capB.fig@@</b><span>@@t.policy.capB.label@@</span></figcaption>')
s = s.replace('A hundred Costa Rican tech companies.', '@@t.policy.beat1@@')
s = s.replace('Ninety-three of them already save time with AI.', '@@t.policy.beat2@@')
s = s.replace('Nine of them have any rule about it.', '@@t.policy.beat3@@')
s = s.replace('The other eighty-four are running on luck. Same companies, same year.', '@@t.policy.aside@@')
s = s.replace('93% save time, 9% have a policy &mdash; PROCOMER, Caracterizaci&oacute;n del Sector TIC, 2025', '@@t.policy.cite@@')
s = s.replace('Teams taught to use AI get more done.', '@@t.viz.h3@@')
s = s.replace('The same hundred people, twice. Teach one group to use AI on its own work first, and that group gets up to a third more done.', '@@t.viz.lede@@')
s = s.replace('aria-label="Two bars made of marks. Squares for people working it out alone, spades for people taught first. The spade bar is thirty-four percent taller."',
              'aria-label="@@t.viz.aria@@"')
s = s.replace('<span>Working it out alone</span>', '<span>@@t.viz.capA@@</span>')
s = s.replace('<span>Taught first</span>', '<span>@@t.viz.capB@@</span>')
s = s.replace('<span>+34%</span>', '<span>@@t.viz.delta@@</span>')
s = s.replace('The same hundred people, twice.<', '@@t.viz.beat1@@<')
s = s.replace('One group is taught to use AI on its own work first.', '@@t.viz.beat2@@')
s = s.replace('That group gets up to a third more done.', '@@t.viz.beat3@@')
s = s.replace('And today only <b>47%</b> of people at work were ever taught to use AI at all.',
              '@@t.viz.aside.pre@@ <b>@@t.viz.aside.fig@@</b> @@t.viz.aside.post@@')
s = s.replace('+34% for taught beginners &mdash; Brynjolfsson, Li &amp; Raymond, NBER 31161, 2023', '@@t.viz.cite1@@')
s = s.replace('47% trained &mdash; KPMG &times; Melbourne Business School, 2025', '@@t.viz.cite2@@')
s = s.replace('Can AI<br>take this?', '@@t.swipe.h2.a@@<br>@@t.swipe.h2.b@@')
s = s.replace('Can AI', '@@t.swipe.h2.a@@').replace('take this?', '@@t.swipe.h2.b@@')
s = s.replace('Five things that land on an office desk every week. Swipe right if AI can take it. Left if best not.', '@@t.swipe.sub@@')
s = s.replace("Here's your desk.", '@@t.swipe.desk.h3@@')
s = s.replace('Five calls, five catches. None of them wrong. Each one has a detail worth knowing before Monday.', '@@t.swipe.desk.sub@@')
s = s.replace('<span>Best not</span>', '<span>@@t.swipe.pileL@@</span>')
s = s.replace('<span>AI can take it</span>', '<span>@@t.swipe.pileR@@</span>')
s = s.replace('id="bLeft" type="button">Best not<', 'id="bLeft" type="button">@@t.swipe.btnL@@<')
s = s.replace('id="bRight" type="button">AI can take it<', 'id="bRight" type="button">@@t.swipe.btnR@@<')
s = s.replace('Just show me the notes', '@@t.swipe.skip@@')
s = s.replace('Those catches are what we teach in half a day.', '@@t.swipe.line@@')
s = s.replace('href="/workshop/">See the workshop</a>', 'href="/workshop/">@@t.half.btn@@</a>')
s = s.replace('id="bAgain" type="button">Deal again<', 'id="bAgain" type="button">@@t.swipe.again@@<')
s = s.replace('<h2 class="h2">Why us</h2>', '<h2 class="h2">@@t.why.h2@@</h2>')
for i, (t_, pf) in enumerate([
        ('Your real work, not slides.', 'We open your files, not a template.'),
        ('First in, not catching up.', 'Daily users, not certified presenters.'),
        ('The risks, not just the hype.', 'We make it fail in front of you on purpose.'),
        ('Nothing to sell you afterwards.', 'No licences, no platform, no upsell.')], 1):
    s = s.replace(t_, '@@t.why%d.t@@' % i).replace(pf, '@@t.why%d.pf@@' % i)
s = s.replace('AI without the smoke screen', '@@t.work.h2@@')
s = s.replace('The main workshop. Half a day, seven moments, your own work on the table.', '@@t.work.lede@@')
for i, (h3, p) in enumerate([
        ('The smoke.', 'What your team has been told AI does. We clear it in ten minutes, using your own examples.'),
        ('Your desk.', "Three real tasks from your team's week. Not ours. Yours."),
        ('Hands on.', 'Everyone at a keyboard or a phone, with the tools they already have. We bring our own tools for teaching, tailored to your team.'),
        ('Teaching magic.', 'One task, done with AI, in front of everyone.'),
        ('Where it breaks.', 'We make it fail on purpose, so you see it before a client does.'),
        ('House rules.', 'What never leaves the building. Who checks what. Three lines, written together.'),
        ('Next week.', 'A one-page plan in your inbox: what to automate first, what to guard, what to ignore. Yours to use, no second session needed.')], 1):
    s = s.replace('<h3>%s</h3>' % h3, '<h3>@@t.work%d.h3@@</h3>' % i).replace(p, '@@t.work%d.p@@' % i)
s = s.replace('<span class="optflag">Optional</span>', '<span class="optflag">@@t.work7.flag@@</span>')
s = s.replace('The trick, with receipts.', '@@t.learn.h2@@')
s = s.replace("Four numbers explain why we teach the way we do. Each one links to where it came from. Read them, then bring us your team's week.", '@@t.learn.lede@@')
s = s.replace('Half a day. Your files. Nothing to buy afterwards.', '@@t.learn.cta.big@@')
s = s.replace('>See the workshop</a>', '>@@t.half.btn@@</a>')
s = s.replace('Hands-on AI workshops for teams in Costa Rica.', '@@t.foot.tag@@')
s = s.replace('<h3>Site</h3>', '<h3>@@t.foot.site@@</h3>')
s = s.replace('>Home</a>', '>@@t.foot.home@@</a>')
s = s.replace('<li><a href="/workshop/">The workshop</a></li>', '<li><a href="/workshop/">@@t.nav.workshop@@</a></li>')
s = s.replace('<li><a href="/learn-more/">Learn more</a></li>', '<li><a href="/learn-more/">@@t.nav.learn@@</a></li>')
s = s.replace('<h3>Contact</h3>', '<h3>@@t.foot.contact@@</h3>')
s = s.replace('WhatsApp <span class="todo">TODO number</span>', '@@t.foot.whatsapp@@ <span class="todo">@@t.foot.whatsapp.todo@@</span>')
s = s.replace('Email <span class="todo">TODO address</span>', '@@t.foot.email@@ <span class="todo">@@t.foot.email.todo@@</span>')
s = s.replace('LinkedIn <span class="todo">TODO url</span>', '@@t.foot.linkedin@@ <span class="todo">@@t.foot.linkedin.todo@@</span>')
s = s.replace('<span class="todo">TODO city</span>, Costa Rica', '<span class="todo">@@t.foot.city.todo@@</span>@@t.foot.country@@')
s = s.replace('&copy; 2026 kadabra CR. All rights reserved.', '@@t.foot.legal@@')
wr('src/shell.html', s)

# ---------------------------------------------------------------- app.src.js
a = rd('src/app.src.js')
a = a.replace("'/': 'kadabra. Hands-on AI workshops for teams in Costa Rica',", "'/': '@@t.meta.home.title@@',")
a = a.replace("'/workshop/': 'The workshop: AI without the smoke screen. kadabra',", "'/workshop/': '@@t.meta.work.title@@',")
a = a.replace("'/learn-more/': 'Learn more: the numbers behind the workshop. kadabra'", "'/learn-more/': '@@t.meta.learn.title@@'")
a = a.replace("""  var WORDS = ['wrong invoice', 'fake numbers', 'bad advice', 'breach', 'wrong price',
               'data leak', 'made-up quote', 'client data', 'leaked contract', 'lawsuit'];""",
              "  var WORDS = '@@t.game.words@@'.split(', ');")
a = a.replace("""          dead: ['On your own, it bites back.',
                 'The leak, the made-up number, the prompt nobody saw coming: not if, when. Half a day with us and your team sees them first.'] }""",
              "          dead: ['@@t.hero.dead.h1@@', '@@t.hero.dead.sub@@'] }")
a = a.replace("""            dead: ['It bit back. Ready when you are.', 'Half a day, on your files, and your team sees it coming.'] } });""",
              "            dead: ['@@t.close.dead.h2@@', '@@t.close.dead.fine@@'] } });")
cards = [
    ("Answer a client asking why their invoice is higher this month.", 'card1.q'),
    ("It writes a convincing reply in seconds. If it doesn't have the numbers, it invents a reason. Give it the invoice, then read before sending.", 'card1.r'),
    ("Fair. Then you are typing that reply yourself. It can still draft it: hand it the invoice, keep the decision and the send button.", 'card1.l'),
    ("Summarise the 40-page supplier contract.", 'card2.q'),
    ("Good summary, and it will skip the one clause that matters. Ask for the clause list first, then read those pages yourself.", 'card2.r'),
    ("Forty pages is a long afternoon. Let it list the clauses and where they sit, then read only those pages. The reading that counts stays yours.", 'card2.l'),
    ("Enter this stack of receipts into the system.", 'card3.q'),
    ("It reads receipts well. It is blind to duplicates and wrong dates. Spot-check one in ten.", 'card3.r'),
    ("This is the one most teams hand over first. It reads receipts well. Keep the spot-check: one in ten, and anything that looks doubled.", 'card3.l'),
    ("Write the monthly report for the owner.", 'card4.q'),
    ("The structure in a minute. Every number needs a human check: numbers are where it sounds most sure and is most wrong.", 'card4.r'),
    ("The structure it can do in a minute. The numbers are the part to guard: check every one, because it sounds most sure where it is most wrong.", 'card4.l'),
    ("Decide whether the new client gets 60-day payment terms.", 'card5.q'),
    ("It can list the pros and cons. The decision, and the risk, stay with a person. If it says yes, it is still your yes.", 'card5.r'),
    ("Right call to keep. It can still lay out the pros and cons in a minute. The decision, and the risk, stay with a person.", 'card5.l'),
]
for txt, key in cards:
    assert a.count(txt) == 1, 'card string missing: ' + txt[:50]
    a = a.replace(txt, '@@t.%s@@' % key)
a = a.replace("var HINT = 'Drag the card, use the buttons, or press ';", "var HINT = '@@t.swipe.hint.mid@@ ';")
a = a.replace("hint.innerHTML = 'Card ' + Math.min(idx + 1, 5) + ' of 5. ' + HINT +",
              "hint.innerHTML = '@@t.swipe.hint.pre@@ ' + Math.min(idx + 1, 5) + ' ' + HINT +")
a = a.replace("""note.innerHTML = '<p class="said">You said: <b>' + (right ? 'AI can take it' : 'Best not') + '</b></p>' +""",
              """note.innerHTML = '<p class="said">@@t.swipe.said@@ <b>' + (right ? '@@t.swipe.pileR@@' : '@@t.swipe.pileL@@') + '</b></p>' +""")
wr('src/app.src.js', a)

# ---------------------------------------------------------------- build.py
b = rd('src/build.py')
b = b.replace('DESC = "Half-day, hands-on AI workshops for teams in Costa Rica. Your real work, your tools, nothing to buy afterwards."',
              'DESC = "@@t.meta.home.desc@@"')
b = b.replace('title="kadabra. Hands-on AI workshops for teams in Costa Rica",', 'title="@@t.meta.home.title@@",')
b = b.replace('title="The workshop: AI without the smoke screen. kadabra",', 'title="@@t.meta.work.title@@",')
b = b.replace('desc="Half a day, seven moments, your own work on the table. What actually happens in a kadabra workshop."),',
              'desc="@@t.meta.work.desc@@"),')
b = b.replace('title="Learn more: the numbers behind the workshop. kadabra",', 'title="@@t.meta.learn.title@@",')
b = b.replace('desc="Four numbers explain why kadabra teaches the way it does. Each one links to the study it came from."),',
              'desc="@@t.meta.learn.desc@@"),')
b = b.replace('<h2 class="rise">Ready when you are.</h2>', '<h2 class="rise">@@t.close.h2@@</h2>')
b = b.replace('href="#TODO-whatsapp">Book a half-day</a>', 'href="#TODO-whatsapp">@@t.cta.book@@</a>')
b = b.replace('<p class="fine rise">Opens a WhatsApp chat. Half a day, on your files, nothing to buy afterwards.</p>',
              '<p class="fine rise">@@t.close.fine@@</p>')
b = b.replace('<h2 class="h2 rise">See what half a day looks like.</h2>', '<h2 class="h2 rise">@@t.half.h2@@</h2>')
b = b.replace('<p class="lede rise">Seven moments, your own work on the table, and a one-page plan the week after. Two minutes to read.</p>',
              '<p class="lede rise">@@t.half.lede@@</p>')
b = b.replace('>See the workshop<svg class="arr"', '>@@t.half.btn@@<svg class="arr"')
b = b.replace('<span>Keep scrolling to book with us</span>', '<span>@@t.half.cue@@</span>')
b = b.replace('<h3>Also worth a read</h3>', '<h3>@@t.learn.also.h3@@</h3>')
old_means = b[b.index('MEANS = ['):b.index(']\n\n\ndef sources_markup')+1]
b = b.replace(old_means, 'MEANS = ["@@t.learn.means1@@", "@@t.learn.means2@@", "@@t.learn.means3@@", "@@t.learn.means4@@"]')
b = b.replace("out.append('          <p class=\"claim\">%s</p>' % esc(r[\"claim\"]))",
              "out.append('          <p class=\"claim\">@@t.learn.claim%d@@</p>' % (i + 1))")
b = b.replace("""        also.append('        <li><a href="%s" rel="noopener noreferrer nofollow" target="_blank">%s</a> <span>%s, %s</span></li>'
                    % (esc(r["url"]), esc(r["claim"]), esc(r["source"]), esc(r["year"])))""",
              """        also.append('        <li><a href="%s" rel="noopener noreferrer nofollow" target="_blank">@@t.also%d@@</a> <span>%s, %s</span></li>'
                    % (esc(r["url"]), j + 1, esc(r["source"]), esc(r["year"])))""")
b = b.replace('    for r in data["alsoRead"]:', '    for j, r in enumerate(data["alsoRead"]):')

# the copy file is the source of every visible string
loader = '''

# ---- the copy: every visible string lives in src/copy.es.md ----------------
COPY_PATH = os.path.join(HERE, "copy.es.md")


def load_copy():
    out = {}
    for line in open(COPY_PATH, encoding="utf-8"):
        line = line.rstrip("\\n")
        if line.startswith("#") or not line.strip() or ": " not in line:
            continue
        key, _, val = line.partition(": ")
        if re.match(r"^[a-z][a-z0-9._]*$", key.strip()):
            out[key.strip()] = val.strip()
    return out


COPY = load_copy()
TOKEN = re.compile(r"@@t\\.([a-z0-9._]+)@@")


def tr(s, where):
    missing = [m.group(1) for m in TOKEN.finditer(s) if m.group(1) not in COPY]
    if missing:
        sys.exit("copy.es.md has no line for: %s (in %s)" % (", ".join(sorted(set(missing))), where))
    return TOKEN.sub(lambda m: COPY[m.group(1)], s)

'''
b = b.replace('\nDESC = ', loader + '\nDESC = ')
b = b.replace('''    app = APPSRC.replace("@@PATHS@@", json.dumps(MORPH, indent=2, ensure_ascii=False))''',
              '''    app = APPSRC.replace("@@PATHS@@", json.dumps(MORPH, indent=2, ensure_ascii=False))
    app = tr(app, "app.src.js")''')
b = b.replace('''        assert "@@" not in page, "unreplaced placeholder in " + route''',
              '''        page = tr(page, route)
        assert "@@" not in page, "unreplaced placeholder in " + route''')
b = b.replace('    src, also = sources_markup()', '    src, also = sources_markup()\n    src, also = tr(src, "sources"), tr(also, "also")')
b = b.replace('page = page.replace("@@TITLE@@", esc(meta["title"]))', 'page = page.replace("@@TITLE@@", esc(tr(meta["title"], "title")))')
b = b.replace('page = page.replace("@@DESC@@", esc(meta["desc"]))', 'page = page.replace("@@DESC@@", esc(tr(meta["desc"], "desc")))')
b = b.replace('page = page.replace("@@CANON@@"', 'page = page.replace("@@CANON@@"')
wr('src/build.py', b)
print('tokenised')
