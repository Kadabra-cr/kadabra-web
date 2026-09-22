import { chromium } from 'playwright';
const sleep = ms => new Promise(r => setTimeout(r, ms));
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 2 });
await p.goto('http://127.0.0.1:4173/'); await sleep(800);
await p.evaluate(() => document.getElementById('swipe').scrollIntoView()); await sleep(1200);
await p.click('#bSkip'); await sleep(9000);
const sel = await p.evaluate(() => { const r = document.createRange(); r.selectNodeContents(document.querySelector('.note .a')); const s = getSelection(); s.removeAllRanges(); s.addRange(r); return getComputedStyle(document.querySelector('.note .a')).userSelect; });
for (const [i, q] of [[0, '.row[data-fn="2"] .card'], [1, '.row[data-fn="3"] .card'], [2, '.fcard']]) {
  await p.locator(q).scrollIntoViewIfNeeded(); await sleep(600);
  await p.locator(q).screenshot({ path: `shots/r11/card-${i}.png` });
  console.log(q, await p.evaluate(q => { const c = document.querySelector(q).getBoundingClientRect(); return [...document.querySelector(q).querySelectorAll('.ix')].map(e => { const r = e.getBoundingClientRect(); return `L${(r.left - c.left).toFixed(0)} T${(r.top - c.top).toFixed(0)} R${(c.right - r.right).toFixed(0)} B${(c.bottom - r.bottom).toFixed(0)} ${getComputedStyle(e).color}`; }).join(' | '); }, q));
}
await p.evaluate(() => scrollTo(0, 0)); await sleep(500);
await p.locator('.hero .cta').screenshot({ path: 'shots/r11/wa.png' });
console.log('user-select', sel);
await b.close();
