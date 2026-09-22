import { chromium } from 'playwright';
const sleep = (ms) => new Promise(r => setTimeout(r, ms));
const B = 'http://127.0.0.1:4173';
const browser = await chromium.launch();
const errors = [];
async function page(vp) { const p = await (await browser.newContext({ viewport: vp })).newPage(); p.on('pageerror', e => errors.push(e.message)); p.on('console', m => { if (m.type() === 'error') errors.push(m.text()); }); return p; }
const p = await page({ width: 1440, height: 900 });
await p.goto(B + '/', { waitUntil: 'load' }); await sleep(1500);
const geo = await p.evaluate(() => { const g = id => { const e = document.getElementById(id); const r = e.getBoundingClientRect(); return { top: Math.round(r.top + scrollY), h: e.offsetHeight }; };
  return { stage: g('stage2'), morph: g('morph'), numbers: g('numbers'), viz: g('viz'), swipe: g('swipe'), hstage: g('hstage-home'), docH: document.body.scrollHeight, cls: document.documentElement.className }; });
console.log(JSON.stringify(geo));
const ph = 900 - 72;
const shots = [
  ['a-hero', 0], ['b-q50', ph * .28], ['c-q100', ph * .6], ['d-content-rise', ph * 1.0],
  ['e-morph-r0', geo.morph.top - 72], ['f-morph-r30', geo.morph.top - 72 + (geo.morph.h - ph) * .3], ['g-morph-r55', geo.morph.top - 72 + (geo.morph.h - ph) * .55], ['h-morph-r90', geo.morph.top - 72 + (geo.morph.h - ph) * .92],
  ['i-viz', geo.viz.top - 140], ['j-fold30', geo.swipe.top - 72 - ph * .7], ['k-fold70', geo.swipe.top - 72 - ph * .3], ['l-swipe', geo.swipe.top - 72],
];
for (const [n, y] of shots) { await p.evaluate(y => window.scrollTo(0, y), Math.round(y)); await sleep(n === 'i-viz' ? 3000 : 700);
  const v = await p.evaluate(() => { const s = document.getElementById('stage2'); return { q: s.style.getPropertyValue('--q'), f: s.style.getPropertyValue('--f'), r: document.getElementById('morph').style.getPropertyValue('--r'), cond: document.getElementById('hero').classList.contains('condensed') }; });
  console.log(n, JSON.stringify(v)); await p.screenshot({ path: `shots/r9/${n}.png` }); }
const hs = geo.hstage;
for (const [n, f] of [['m-half-e0', -0.6], ['n-half-e50', .19], ['o-half-full', .5], ['p-half-out', .85]]) { await p.evaluate(y => window.scrollTo(0, y), Math.round(hs.top - 72 + (hs.h - ph) * f)); await sleep(900); await p.screenshot({ path: `shots/r9/${n}.png` }); }
const m = await page({ width: 390, height: 844 });
await m.goto(B + '/', { waitUntil: 'load' }); await sleep(900); await m.screenshot({ path: 'shots/r9/z-phone-hero.png' });
await m.evaluate(() => document.getElementById('breaks').scrollIntoView()); await sleep(2500); await m.screenshot({ path: 'shots/r9/z-phone-breaks.png' });
await m.evaluate(() => document.getElementById('halfday-home').scrollIntoView()); await sleep(1500); await m.screenshot({ path: 'shots/r9/z-phone-half.png' });
console.log('errors', errors);
await browser.close();
