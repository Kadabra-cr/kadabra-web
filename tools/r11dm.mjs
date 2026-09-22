import { chromium } from 'playwright';
const sleep = ms => new Promise(r => setTimeout(r, ms));
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 390, height: 844 }, hasTouch: true, isMobile: true });
await p.goto('http://127.0.0.1:4173/'); await sleep(800);
await p.evaluate(() => document.getElementById('swipe').scrollIntoView()); await sleep(1200);
await p.click('#bSkip'); await sleep(6500);
console.log(await p.evaluate(() => {
  const r = document.querySelector('.row'), c = r.querySelector('.card');
  const f = e => { const b = e.getBoundingClientRect(); return Math.round(b.top) + '..' + Math.round(b.bottom) + ' w' + Math.round(b.width); };
  const hits = [];
  const walk = rs => { for (const x of rs) { if (x.cssRules && !x.selectorText) walk(x.cssRules); else if (x.selectorText && x.style.position && c.matches(x.selectorText)) hits.push(x.selectorText + ' ' + x.style.position); } };
  for (const sh of document.styleSheets) { try { walk(sh.cssRules); } catch (e) {} }
  return [hits.join(' | '), getComputedStyle(c).position, 'slot ' + f(r.querySelector('.slot')), 'card ' + f(c), 'note ' + f(r.querySelector('.note'))].join('\n');
}));
await b.close();
