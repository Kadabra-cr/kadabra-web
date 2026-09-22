import { chromium } from 'playwright';
const sleep = (ms) => new Promise(r => setTimeout(r, ms));
const browser = await chromium.launch();
const p = await (await browser.newContext({ viewport: { width: 1440, height: 900 } })).newPage();
await p.goto('http://127.0.0.1:4173/', { waitUntil: 'load' }); await sleep(1500);
const box = await p.locator('#field').boundingBox(); const cx = box.x + box.width * .3, cy = box.y + box.height * .62;
for (let t = 0; t < 260; t++) { const a = t * .05; await p.mouse.move(cx + Math.cos(a) * 55, cy + Math.sin(a) * 40); await sleep(16); }
await p.evaluate(() => { const f = document.getElementById('field').__field; window.__tr = []; const h = f.heart;
  (function loop() { window.__tr.push([performance.now() | 0, h.x | 0, h.y | 0, h.mass, +h.o.toFixed(2), h.vx | 0, h.vy | 0]); if (window.__tr.length < 200) requestAnimationFrame(loop); })(); });
await p.mouse.move(box.x + box.width * .92, box.y + box.height * .12);
await sleep(1200);
const tr = await p.evaluate(() => window.__tr);
let prev = tr[0]; for (const r of tr) { if (Math.abs(r[1] - prev[1]) > 40 || Math.abs(r[2] - prev[2]) > 40) console.log('JUMP', prev, '->', r); prev = r; }
console.log(tr.slice(0, 6).map(r => r.join(',')).join(' | '));
console.log(tr.slice(-3).map(r => r.join(',')).join(' | '));
await browser.close();
