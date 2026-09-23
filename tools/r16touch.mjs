import { chromium, devices } from 'playwright';
const sleep = ms => new Promise(r => setTimeout(r, ms));
const b = await chromium.launch();
const ctx = await b.newContext({ ...devices['Pixel 7'] });
const p = await ctx.newPage();
const errs = []; p.on('pageerror', e => errs.push(e.message));
const cdp = await ctx.newCDPSession(p);
async function drag(x0, y0, x1, y1, steps = 12) {
  await cdp.send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ x: x0, y: y0 }] });
  for (let i = 1; i <= steps; i++) { await cdp.send('Input.dispatchTouchEvent', { type: 'touchMove', touchPoints: [{ x: x0 + (x1 - x0) * i / steps, y: y0 + (y1 - y0) * i / steps }] }); await sleep(16); }
  await cdp.send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] });
}
await p.goto('http://127.0.0.1:4173/'); await sleep(1200);
// hero: a swipe up scrolls the page (no game on phones)
let y0 = await p.evaluate(() => scrollY);
await drag(200, 600, 200, 250); await sleep(600);
console.log('hero swipe scrolls:', y0, '->', await p.evaluate(() => scrollY), 'ask pill exists:', await p.evaluate(() => !!document.querySelector('.ask')));
await p.evaluate(() => document.getElementById('swipe').scrollIntoView()); await sleep(1500);
const card = await p.evaluate(() => { const c = document.querySelector('#swipe .card:not(.gone)') || document.querySelector('.deck .card'); const r = c.getBoundingClientRect(); return { x: r.left + r.width / 2, y: r.top + r.height / 2, hint: document.querySelector('.hint, #hint') && (document.querySelector('.hint, #hint').textContent) }; });
console.log('card at', card);
y0 = await p.evaluate(() => scrollY);
const hint0 = await p.evaluate(() => document.querySelector('#swipe').innerText.match(/Carta \d/)?.[0]);
await drag(card.x, card.y + 60, card.x + 4, card.y - 200); await sleep(700);
const y1 = await p.evaluate(() => scrollY);
const hint1 = await p.evaluate(() => document.querySelector('#swipe').innerText.match(/Carta \d/)?.[0]);
console.log('vertical swipe on card scrolls page:', y0, '->', y1, '| card unchanged:', hint0, hint1);
await p.evaluate(() => document.getElementById('swipe').scrollIntoView()); await sleep(700);
const c2 = await p.evaluate(() => { const c = document.querySelector('#swipe .card:not(.gone)') || document.querySelector('.deck .card'); const r = c.getBoundingClientRect(); return { x: r.left + r.width / 2, y: r.top + r.height / 2 }; });
await drag(c2.x, c2.y, c2.x + 260, c2.y + 10, 14); await sleep(900);
console.log('horizontal drag deals the card:', await p.evaluate(() => document.querySelector('#swipe').innerText.match(/Carta \d/)?.[0]));
await p.screenshot({ path: 'tools/shots/r16/touch-swipe.png' });
console.log('errors', errs);
await b.close();
