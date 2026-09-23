import { chromium, devices } from 'playwright';
const sleep = ms => new Promise(r => setTimeout(r, ms));
const b = await chromium.launch();
const ctx = await b.newContext(devices['Pixel 7']);
const p = await ctx.newPage();
const cdp = await ctx.newCDPSession(p);
async function drag(x0, y0, x1, y1, steps) {
  await cdp.send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ x: x0, y: y0 }] });
  for (let i = 1; i <= steps; i++) { await cdp.send('Input.dispatchTouchEvent', { type: 'touchMove', touchPoints: [{ x: x0 + (x1 - x0) * i / steps, y: y0 + (y1 - y0) * i / steps }] }); await sleep(12); }
  await cdp.send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] });
}
await p.goto('http://127.0.0.1:4173/'); await sleep(1000);
await p.evaluate(() => { document.getElementById('swipe').scrollIntoView(); const d = document.getElementById('deck'); ['pointerdown', 'pointermove', 'pointerup', 'pointercancel'].forEach(t => d.addEventListener(t, e => (window.L = window.L || []).push(t[7] + Math.round(e.clientX) + '@' + Math.round(e.timeStamp)))); });
await sleep(1200);
const c = await p.evaluate(() => { const r = document.querySelector('#swipe .card:not(.gone)').getBoundingClientRect(); return { x: r.left + r.width / 2, y: r.top + r.height / 2 }; });
await drag(c.x, c.y, c.x - 32, c.y, 3); await sleep(800);
console.log(await p.evaluate(() => window.L.join(' ')), '->', await p.evaluate(() => document.querySelector('#swipe').innerText.match(/Carta \d/)?.[0]));
await b.close();
