import { chromium, devices } from 'playwright';
const b = await chromium.launch();
const p = await (await b.newContext({ viewport:{width:320,height:640}, isMobile:true, hasTouch:true })).newPage();
for (const route of ['/', '/workshop/', '/learn-more/']) {
  await p.goto('http://127.0.0.1:4173' + route, { waitUntil: 'load' }); await new Promise(r => setTimeout(r, 800));
  const r = await p.evaluate(() => {
    const out = [];
    document.querySelectorAll('body *').forEach(el => { if (el.closest('svg')) return; const b = el.getBoundingClientRect(); if (b.right > 321 || el.scrollWidth > 321) out.push([Math.round(b.right), Math.round(b.width), el.scrollWidth, (el.id ? '#' + el.id : el.tagName.toLowerCase()) + '.' + [...el.classList].join('.'), getComputedStyle(el).minWidth, getComputedStyle(el).whiteSpace]); });
    out.sort((a, b) => b[0] - a[0]); return { iw: innerWidth, out: out.slice(0, 30) };
  });
  console.log(route, r.iw); r.out.forEach(x => console.log('  ', x.join(' | ')));
}
await b.close();
