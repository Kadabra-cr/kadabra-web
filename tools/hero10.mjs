import { chromium } from 'playwright';
const sleep = ms => new Promise(r => setTimeout(r, ms));
const b = await chromium.launch();
for (const [w, h, tag] of [[1440, 900, '1440'], [1280, 800, '1280']]) {
  const p = await (await b.newContext({ viewport: { width: w, height: h } })).newPage();
  await p.goto('http://127.0.0.1:4173/', { waitUntil: 'load' }); await sleep(1200);
  await p.evaluate(() => scrollTo(0, 700)); await sleep(1200);
  console.log(tag, await p.evaluate(() => { const h1 = document.querySelector('.hero h1'), c = document.querySelector('.hero .ctas');
    return { h1font: getComputedStyle(h1).fontSize, h1w: Math.round(h1.getBoundingClientRect().width), lines: h1.getClientRects().length, ctasTop: Math.round(c.getBoundingClientRect().top), heroW: Math.round(document.querySelector('.hero').getBoundingClientRect().width) }; }));
  await p.screenshot({ path: `shots/r10/n-hero-${tag}.png` });
  await p.context().close();
}
await b.close();
