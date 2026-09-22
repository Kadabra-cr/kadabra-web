#!/usr/bin/env python3
"""Generate the three route shells from src/shell.html + site/sprites.svg + site/sources.json.

Not a required build step: the output is committed plain HTML and the site runs
without it. It exists so the three shells cannot drift apart by hand.

    python src/build.py
"""
import html, json, os, re, sys
from urllib.parse import urlsplit

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(os.path.dirname(HERE), "site")

SHELL = open(os.path.join(HERE, "shell.html"), encoding="utf-8").read()
SPRITES = open(os.path.join(SITE, "sprites.svg"), encoding="utf-8").read().strip()
APPSRC = open(os.path.join(HERE, "app.src.js"), encoding="utf-8").read()
MORPH = json.load(open(os.path.join(HERE, "suits-square-morph.json"), encoding="utf-8"))["paths"]

DESC = "Half-day, hands-on AI workshops for teams in Costa Rica. Your real work, your tools, nothing to buy afterwards."
ORIGIN = "https://kadabra.cr"

ROUTES = {
    "/": dict(
        file="index.html",
        title="kadabra. Hands-on AI workshops for teams in Costa Rica",
        desc=DESC),
    "/workshop/": dict(
        file="workshop/index.html",
        title="The workshop: AI without the smoke screen. kadabra",
        desc="Half a day, seven moments, your own work on the table. What actually happens in a kadabra workshop."),
    "/learn-more/": dict(
        file="learn-more/index.html",
        title="Learn more: the numbers behind the workshop. kadabra",
        desc="Four numbers explain why kadabra teaches the way it does. Each one links to the study it came from."),
}

CLOSE = """<section class="close" id="close-{k}">
  <svg class="closefield" viewBox="0 0 1600 620" preserveAspectRatio="xMidYMid slice" aria-hidden="true"></svg>
  <div class="wrap">
    <h2 class="rise">Ready when you are.</h2>
    <p><a class="cta rise" href="#TODO-whatsapp">Book a half-day</a></p>
    <p class="fine rise">Opens a WhatsApp chat. Half a day, on your files, nothing to buy afterwards.</p>{more}
  </div>
</section>"""

HALF = """<div class="hstage" id="hstage-{k}"><div class="hpin">
<section class="band halfday" id="halfday-{k}">
  <div class="wrap">
    <h2 class="h2 rise">See what half a day looks like.</h2>
    <p class="lede rise">Seven moments, your own work on the table, and a one-page plan the week after. Two minutes to read.</p>
    <p class="rise gorow"><a class="btn go arrow light" href="/workshop/">See the workshop<svg class="arr" viewBox="0 0 64 28" aria-hidden="true"><use href="#arrow"/></svg></a></p>
    <div class="hcue" aria-hidden="true"><svg viewBox="0 0 64 28"><use href="#chevron-down"/></svg><span>Keep scrolling to book with us</span></div>
  </div>
</section>
</div></div>
"""


def esc(s):
    return html.escape(str(s), quote=True)


def host(url):
    return urlsplit(url).netloc.replace("www.", "")


MEANS = [
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
    return "\n".join(out), "\n".join(also)


def whybands(page):
    """No-JS readers still see the suit: the final path is inline, JS resets it
    to the square and morphs it once when the band arrives."""
    def fill(m):
        return m.group(0).replace('<path fill="currentColor"/>',
                                  '<path fill="currentColor" d="%s"/>' % MORPH[m.group(1)])
    return re.sub(r'data-suit="([^"]+)"[\s\S]*?<path fill="currentColor"/>', fill, page)


def main():
    # app.js: the morph paths are embedded so the hero never waits on a fetch.
    app = APPSRC.replace("@@PATHS@@", json.dumps(MORPH, indent=2, ensure_ascii=False))
    assert "@@" not in app, "unreplaced placeholder in app.src.js"
    with open(os.path.join(SITE, "app.js"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(app)
    print("%-22s %6d bytes" % ("app.js", len(app)))

    src, also = sources_markup()
    for route, meta in ROUTES.items():
        page = SHELL
        page = whybands(page)
        page = page.replace("@@SPRITES@@", SPRITES)
        page = page.replace("@@SOURCES@@", src)
        page = page.replace("@@CLOSE_HOME@@", HALF.format(k="home") + CLOSE.format(k="home", more=""))
        page = page.replace("@@CLOSE_WORK@@", CLOSE.format(k="work", more=""))
        page = page.replace("@@CLOSE_LEARN@@", HALF.format(k="learn") + CLOSE.format(k="learn", more=""))
        page = page.replace("@@ALSO@@", also)
        page = page.replace("@@TITLE@@", esc(meta["title"]))
        page = page.replace("@@DESC@@", esc(meta["desc"]))
        page = page.replace("@@CANON@@", ORIGIN + route)
        page = page.replace("@@HIDE_HOME@@", "" if route == "/" else "hidden")
        page = page.replace("@@HIDE_WORK@@", "" if route == "/workshop/" else "hidden")
        page = page.replace("@@HIDE_SRC@@", "" if route == "/learn-more/" else "hidden")
        assert "@@" not in page, "unreplaced placeholder in " + route
        dest = os.path.join(SITE, meta["file"])
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        open(dest, "w", encoding="utf-8", newline="\n").write(page)
        print("%-22s %6d bytes" % (meta["file"], len(page)))

    # duplicate-id self-check: the three routes live in one document.
    ids = re.findall(r'\sid="([^"]+)"', page)
    dupes = {i for i in ids if ids.count(i) > 1}
    assert not dupes, "duplicate ids: %s" % dupes
    print("ids unique:", len(ids))


if __name__ == "__main__":
    main()
