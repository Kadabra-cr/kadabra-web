import { chromium, devices } from 'playwright';
const sleep = ms => new Promise(r => setTimeout(r, ms));
const b = await chromium.launch();
const ctx = await b.newContext(devices['Pixel 7']);
const p = await ctx.newPage();
const cdp = await ctx.newCDPSession(p);
await cdp.send('Emulation.setCPUThrottlingRate', { rate: 4 });
await p.goto('http://127.0.0.1:4173/'); await sleep(2500);
const r = await p.evaluate(async () => {
  const out = []; const H = document.documentElement.scrollHeight; let last = performance.now();
  for (let y = 0; y < H; y += 14) {
    scrollTo(0, y); const n = await new Promise(r => requestAnimationFrame(r)); const d = n - last; last = n;
    if (d > 33) { const el = document.elementFromPoint(innerWidth / 2, innerHeight / 2); const sec = el && el.closest('section'); out.push(Math.round(d) + '@' + y + ':' + (sec ? (sec.id || sec.className) : '?')); }
  }
  return out;
});
console.log(r.join('  '));
await b.close();
