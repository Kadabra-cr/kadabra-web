import { chromium, devices } from 'playwright';
const sleep = ms => new Promise(r => setTimeout(r, ms));
const b = await chromium.launch();
const ctx = await b.newContext(devices['Pixel 7']);
const p = await ctx.newPage();
const cdp = await ctx.newCDPSession(p);
async function drag(x0, y0, x1, y1, steps) {
  await cdp.send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ x: x0, y: y0 }] });
  for (let i = 1; i <= steps; i++) { await cdp.send('Input.dispatchTouchEvent', { type: 'touchMove', touchPoints: [{ x: x0 + (x1 - x0) * i / steps, y: y0 + (y1 - y0) * i / steps }] }); await sleep(16); }
  await cdp.send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] });
}
const hint = () => p.evaluate(() => document.querySelector('#swipe').innerText.match(/Carta \d/)?.[0]);
const cardXY = () => p.evaluate(() => { const r = document.querySelector('#swipe .card:not(.gone)').getBoundingClientRect(); return { x: r.left + r.width / 2, y: r.top + r.height / 2 }; });
await p.goto('http://127.0.0.1:4173/'); await sleep(1000);
await p.evaluate(() => document.getElementById('swipe').scrollIntoView()); await sleep(1200);
let c = await cardXY(); await drag(c.x, c.y, c.x + 55, c.y, 10); await sleep(800);
console.log('slow 55px drag ->', await hint());
c = await cardXY(); await drag(c.x, c.y, c.x - 30, c.y, 3); await sleep(800);
console.log('quick 30px flick left ->', await hint());
c = await cardXY(); await drag(c.x, c.y, c.x + 35, c.y, 10); await sleep(800);
console.log('slow 35px drag (should stay) ->', await hint());
// frames: 4x slower CPU, hero idle then scrolling
await cdp.send('Emulation.setCPUThrottlingRate', { rate: 4 });
for (const [route, label] of [['/', 'home'], ['/workshop/', 'workshop']]) {
  await p.goto('http://127.0.0.1:4173' + route); await sleep(2500);
  const f = await p.evaluate(async () => {
    const d = []; let last = performance.now(), stop = false;
    requestAnimationFrame(function t(n) { d.push(n - last); last = n; if (!stop) requestAnimationFrame(t); });
    const H = document.documentElement.scrollHeight;
    for (let y = 0; y < H; y += 14) { scrollTo(0, y); await new Promise(r => requestAnimationFrame(r)); }
    stop = true; d.sort((a, b) => a - b);
    return { n: d.length, p50: d[d.length >> 1].toFixed(1), p95: d[Math.floor(d.length * .95)].toFixed(1), over33: d.filter(x => x > 33).length };
  });
  console.log(label, 'scroll frames @4x CPU', JSON.stringify(f));
}
await b.close();
