import { chromium } from 'playwright';
const sleep = ms => new Promise(r => setTimeout(r, ms));
const b = await chromium.launch(); const errs = [];
const p = await (await b.newContext({ viewport: { width: 1440, height: 900 } })).newPage();
p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
await p.goto('http://127.0.0.1:4173/', { waitUntil: 'load' }); await sleep(1400);
const g = await p.evaluate(() => { const o = id => { const e = document.getElementById(id); return { top: Math.round(e.getBoundingClientRect().top + scrollY), h: e.offsetHeight }; };
  return { morph: o('morph'), viz: o('viz'), swipe: o('swipe'), hstage: o('hstage-home'), doc: document.body.scrollHeight }; });
console.log(JSON.stringify(g));
for (const [n, y] of [['a-cards', g.morph.top - 500], ['b-mid', g.morph.top - 180], ['c-graph', g.morph.top + 120], ['d-taught', g.viz.top - 160]]) {
  await p.evaluate(v => scrollTo(0, v), Math.round(y)); await sleep(n === 'd-taught' ? 3000 : 900);
  console.log(n, 'r =', await p.evaluate(() => document.getElementById('morph').style.getPropertyValue('--r')));
  await p.screenshot({ path: `shots/r10/${n}.png` });
}
// the finish: mark, then the rows dealt
await p.evaluate(() => document.getElementById('swipe').scrollIntoView()); await sleep(1000);
await p.click('#bSkip'); await sleep(1500);
for (const [n, wait] of [['e-veil', 900], ['f-deal1', 500], ['g-deal2', 500], ['h-deal-done', 1400]]) { await sleep(wait); await p.screenshot({ path: `shots/r10/${n}.png` }); }
await sleep(2500);
await p.evaluate(() => document.getElementById('desk').scrollIntoView({ block: 'start' })); await sleep(600);
await p.screenshot({ path: 'shots/r10/i-desk.png' });
// half-day: grow then let the felt rise
const hs = g.hstage, ph = 828;
for (const [n, f] of [['j-half-start', -.5], ['k-half-grown', .35], ['l-half-exit', .95]]) { await p.evaluate(v => scrollTo(0, v), Math.round(hs.top - 72 + (hs.h - ph) * f)); await sleep(800); await p.screenshot({ path: `shots/r10/${n}.png` }); }
console.log('errors', errs); await b.close();
