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


# ---- the copy: every visible string lives in src/copy.es.md ----------------
COPY_PATH = os.path.join(HERE, "copy.es.md")


def load_copy():
    out = {}
    for line in open(COPY_PATH, encoding="utf-8"):
        line = line.rstrip("\n")
        if line.startswith("#") or not line.strip() or ": " not in line:
            continue
        key, _, val = line.partition(": ")
        if re.match(r"^[a-z][A-Za-z0-9._]*$", key.strip()):
            out[key.strip()] = val.strip()
    return out


COPY = load_copy()
COPY["wa.link"] = "https://wa.me/" + re.sub(r"\D", "", COPY["foot.whatsapp.value"])
TOKEN = re.compile(r"@@t\.([A-Za-z0-9._]+)@@")


def tr(s, where):
    missing = [m.group(1) for m in TOKEN.finditer(s) if m.group(1) not in COPY]
    if missing:
        sys.exit("copy.es.md has no line for: %s (in %s)" % (", ".join(sorted(set(missing))), where))
    return TOKEN.sub(lambda m: COPY[m.group(1)], s)


DESC = "@@t.meta.home.desc@@"
ORIGIN = "https://kadabra.cr"

ROUTES = {
    "/": dict(
        file="index.html",
        title="@@t.meta.home.title@@",
        desc=DESC),
    "/workshop/": dict(
        file="workshop/index.html",
        title="@@t.meta.work.title@@",
        desc="@@t.meta.work.desc@@"),
    "/learn-more/": dict(
        file="learn-more/index.html",
        title="@@t.meta.learn.title@@",
        desc="@@t.meta.learn.desc@@"),
}

CLOSE = """<section class="close" id="close-{k}">
  <svg class="closefield" viewBox="0 0 1600 620" preserveAspectRatio="xMidYMid slice" aria-hidden="true"></svg>
  <div class="wrap">
    <h2 class="rise">@@t.close.h2@@</h2>
    <p><a class="cta rise" href="@@t.wa.link@@">@@t.cta.book@@</a></p>
    <p class="fine rise">@@t.close.fine@@</p>{more}
  </div>
</section>"""

HALF = """<div class="hstage" id="hstage-{k}"><div class="hpin">
<section class="band halfday" id="halfday-{k}">
  <div class="wrap">
    <h2 class="h2 rise">@@t.half.h2@@</h2>
    <p class="lede rise">@@t.half.lede@@</p>
    <p class="rise gorow"><a class="btn go arrow light" href="/workshop/">@@t.half.btn@@<svg class="arr" viewBox="0 0 64 28" aria-hidden="true"><use href="#arrow"/></svg></a></p>
    <div class="hcue" aria-hidden="true"><svg viewBox="0 0 64 28"><use href="#chevron-down"/></svg><span>@@t.half.cue@@</span></div>
  </div>
</section>
</div></div>
"""


def esc(s):
    return html.escape(str(s), quote=True)


def host(url):
    return urlsplit(url).netloc.replace("www.", "")


MEANS = ["@@t.learn.means1@@", "@@t.learn.means2@@", "@@t.learn.means3@@", "@@t.learn.means4@@"]


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
        out.append('          <p class="claim">@@t.learn.claim%d@@</p>' % (i + 1))
        out.append('          <p class="means">%s</p>' % esc(MEANS[i]))
        out.append('          <p class="meta"><a href="%s" rel="noopener noreferrer nofollow" target="_blank">%s, %s</a></p>'
                   % (esc(r["url"]), esc(r["source"]), esc(r["year"])))
        out.append("        </div>")
        out.append('        <span class="rule mid drift" aria-hidden="true"></span>')
        out.append("      </li>")
    out.append("    </ol>")

    also = []
    also.append('    <div class="also rise">')
    also.append("      <h3>@@t.learn.also.h3@@</h3>")
    also.append('      <ul class="alsolist">')
    for j, r in enumerate(data["alsoRead"]):
        also.append('        <li><a href="%s" rel="noopener noreferrer nofollow" target="_blank">@@t.also%d@@</a> <span>%s, %s</span></li>'
                    % (esc(r["url"]), j + 1, esc(r["source"]), esc(r["year"])))
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
    app = tr(app, "app.src.js")
    assert "@@" not in app, "unreplaced placeholder in app.src.js"
    with open(os.path.join(SITE, "app.js"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(app)
    print("%-22s %6d bytes" % ("app.js", len(app)))

    src, also = sources_markup()
    src, also = tr(src, "sources"), tr(also, "also")
    for route, meta in ROUTES.items():
        page = SHELL
        page = whybands(page)
        page = page.replace("@@SPRITES@@", SPRITES)
        page = page.replace("@@SOURCES@@", src)
        page = page.replace("@@CLOSE_HOME@@", HALF.format(k="home") + CLOSE.format(k="home", more=""))
        page = page.replace("@@CLOSE_WORK@@", CLOSE.format(k="work", more=""))
        page = page.replace("@@CLOSE_LEARN@@", HALF.format(k="learn") + CLOSE.format(k="learn", more=""))
        page = page.replace("@@ALSO@@", also)
        page = page.replace("@@TITLE@@", esc(tr(meta["title"], "title")))
        page = page.replace("@@DESC@@", esc(tr(meta["desc"], "desc")))
        page = page.replace("@@CANON@@", ORIGIN + route)
        page = page.replace("@@HIDE_HOME@@", "" if route == "/" else "hidden")
        page = page.replace("@@HIDE_WORK@@", "" if route == "/workshop/" else "hidden")
        page = page.replace("@@HIDE_SRC@@", "" if route == "/learn-more/" else "hidden")
        page = tr(page, route)
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
