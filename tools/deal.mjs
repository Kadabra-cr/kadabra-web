import { chromium } from 'playwright';
const sleep = ms => new Promise(r => setTimeout(r, ms));
const b = await chromium.launch(); const errs = [];
const p = await (await b.newContext({ viewport: { width: 1440, height: 900 } })).newPage();
p.on('pageerror', e => errs.push(e.message));
await p.goto('http://127.0.0.1:4173/', { waitUntil: 'load' }); await sleep(900);
// card-to-graph handover timing
const mt = await p.evaluate(() => document.getElementById('morph').getBoundingClientRect().top + scrollY);
for (const [n, y] of [['a-cards', mt - 640], ['b-half', mt - 380], ['c-graph', mt - 90]]) {
  await p.evaluate(v => scrollTo(0, v), Math.round(y)); await sleep(900);
  console.log(n, 'r =', await p.evaluate(() => document.getElementById('morph').style.getPropertyValue('--r')));
  await p.screenshot({ path: `shots/r10/${n}.png` });
}
// the finish sequence, timed from the last card
await p.evaluate(() => document.getElementById('swipe').scrollIntoView()); await sleep(900);
await p.click('#bSkip');
await sleep(260 * 5 + 1500 + 300); await p.screenshot({ path: 'shots/r10/e-mark.png' });
await sleep(900); await p.screenshot({ path: 'shots/r10/f-deal1.png' });
await sleep(700); await p.screenshot({ path: 'shots/r10/g-deal2.png' });
await sleep(2500); await p.screenshot({ path: 'shots/r10/h-dealt.png' });
console.log('veils left over:', await p.evaluate(() => document.querySelectorAll('.veil').length));
// half-day, measured fresh now that the desk exists
const hs = await p.evaluate(() => { const e = document.getElementById('hstage-home'); return { top: e.getBoundingClientRect().top + scrollY, h: e.offsetHeight }; });
for (const [n, f] of [['j-half-start', -.45], ['k-half-grown', .4], ['l-half-exit', .95]]) {
  await p.evaluate(v => scrollTo(0, v), Math.round(hs.top - 72 + (hs.h - 828) * f)); await sleep(800);
  await p.screenshot({ path: `shots/r10/${n}.png` });
}
console.log('errors', errs); await b.close();
