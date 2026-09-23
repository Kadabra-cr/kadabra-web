import { chromium, devices } from 'playwright';
const sleep = ms => new Promise(r => setTimeout(r, ms));
const tag = process.argv[2] || 'before';
const b = await chromium.launch();
for (const [dev, name] of [[devices['iPhone 13'], 'ip13'], [{ ...devices['Galaxy S9+'] }, 's9'], [{ viewport: { width: 320, height: 640 }, isMobile: true, hasTouch: true, deviceScaleFactor: 2 }, 'w320']]) {
  const ctx = await b.newContext({ ...dev });
  const p = await ctx.newPage();
  const errs = []; p.on('pageerror', e => errs.push(e.message)); p.on('console', m => m.type() === 'error' && errs.push(m.text()));
  for (const route of ['/', '/workshop/', '/learn-more/']) {
    await p.goto('http://127.0.0.1:4173' + route, { waitUntil: 'load' }); await sleep(900);
    const H = await p.evaluate(() => document.documentElement.scrollHeight);
    const vh = p.viewportSize().height;
    // scroll through to trigger reveals
    for (let y = 0; y < H; y += vh * .6) { await p.evaluate(y => scrollTo(0, y), y); await sleep(120); }
    await sleep(600);
    const r = await p.evaluate(() => {
      const vw = innerWidth, out = [];
      document.querySelectorAll('body *').forEach(el => {
        const b = el.getBoundingClientRect(); if (!b.width) return;
        if (b.right > vw + 1 || b.left < -1) {
          // skip if an ancestor clips
          let a = el.parentElement, clipped = false;
          while (a && a !== document.body) { const o = getComputedStyle(a); if (/(hidden|clip)/.test(o.overflowX) ) { const ab = a.getBoundingClientRect(); if (ab.right <= vw + 1 && ab.left >= -1) { clipped = true; break; } } a = a.parentElement; }
          if (!clipped) out.push((el.id ? '#' + el.id : el.tagName.toLowerCase() + '.' + [...el.classList].join('.')) + ' L' + Math.round(b.left) + ' R' + Math.round(b.right));
        }
      });
      return { vw, sw: document.documentElement.scrollWidth, bw: document.body.scrollWidth, out: out.slice(0, 25) };
    });
    console.log(name, route, JSON.stringify(r));
    if (name === 'ip13') {
      const slug = route.replace(/\//g, '') || 'home';
      for (let i = 0, y = 0; y < H && i < 30; y += vh, i++) { await p.evaluate(y => scrollTo(0, y), y); await sleep(350); await p.screenshot({ path: `shots/r16/${tag}-${slug}-${String(i).padStart(2, '0')}.png` }); }
    }
  }
  if (errs.length) console.log(name, 'ERRORS', errs);
  await ctx.close();
}
await b.close();
