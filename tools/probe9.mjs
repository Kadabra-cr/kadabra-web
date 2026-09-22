import { chromium } from 'playwright';
const b = await chromium.launch(); const p = await (await b.newContext({ viewport: { width: 1440, height: 900 } })).newPage();
await p.goto('http://127.0.0.1:4173/', { waitUntil: 'load' }); await new Promise(r => setTimeout(r, 1200));
const top = await p.evaluate(() => document.getElementById('swipe').getBoundingClientRect().top + scrollY);
await p.evaluate(y => scrollTo(0, y), Math.round(top - 72 - 828 * .3)); await new Promise(r => setTimeout(r, 700));
console.log(await p.evaluate(() => [[720, 850], [300, 800], [1300, 880]].map(([x, y]) => { const e = document.elementFromPoint(x, y); return x + ',' + y + ' ' + e.tagName + '#' + e.id + '.' + e.className + ' bg=' + getComputedStyle(e).backgroundColor; })));
await b.close();
