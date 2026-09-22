import { chromium } from 'playwright';
const sleep = ms => new Promise(r => setTimeout(r, ms));
const b = await chromium.launch();
const p = await (await b.newContext({ viewport: { width: 1440, height: 900 } })).newPage();
await p.goto('http://127.0.0.1:4173/', { waitUntil: 'load' }); await sleep(900);
await p.evaluate(() => document.getElementById('swipe').scrollIntoView()); await sleep(900);
await p.click('#bSkip');
await sleep(260 * 5 + 1500 + 700); await p.screenshot({ path: 'shots/r10/e-mark.png' });
console.log('veil opacity at hold:', await p.evaluate(() => { const v = document.querySelector('.veil'); return v ? getComputedStyle(v).opacity + ' pos ' + getComputedStyle(v).position : 'none'; }));
await sleep(3500); await p.screenshot({ path: 'shots/r10/h-dealt.png' });
const hs = await p.evaluate(() => { const e = document.getElementById('hstage-home'); return { top: e.getBoundingClientRect().top + scrollY, h: e.offsetHeight }; });
for (const [n, y] of [['k-half-grown', hs.top - 72 + (hs.h - 828) * .5], ['l-half-end', hs.top + hs.h - 900], ['m-after', hs.top + hs.h - 500]]) {
  await p.evaluate(v => scrollTo(0, v), Math.round(y)); await sleep(800); await p.screenshot({ path: `shots/r10/${n}.png` });
}
await b.close();
