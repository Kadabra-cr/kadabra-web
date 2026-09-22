import { chromium } from 'playwright';
const sleep = (ms) => new Promise(r => setTimeout(r, ms));
const browser = await chromium.launch();
const p = await (await browser.newContext({ viewport: { width: 1440, height: 900 } })).newPage();
await p.goto('http://127.0.0.1:4173/', { waitUntil: 'load' }); await sleep(1500);
const box = await p.locator('#field').boundingBox(); const cx = box.x + box.width * .3, cy = box.y + box.height * .62;
for (let t = 0; t < 200; t++) { const a = t * .05; await p.mouse.move(cx + Math.cos(a) * 55, cy + Math.sin(a) * 40); await sleep(16); }
await p.evaluate(() => { const h = document.getElementById('field').__field.heart; window.__tr = [];
  (function loop() { window.__tr.push([h.x | 0, h.y | 0, h.mass, +h.o.toFixed(3)]); if (window.__tr.length < 300) requestAnimationFrame(loop); })(); });
await p.mouse.move(box.x + box.width * .92, box.y + box.height * .12);
await sleep(5200);
const tr = await p.evaluate(() => window.__tr);
let prev = tr[0]; for (let i = 1; i < tr.length; i++) { const r = tr[i]; if (Math.abs(r[0] - prev[0]) > 30) console.log('move at frame', i, 'from', prev, 'to', r); prev = r; }
console.log('start', tr[0], 'end', tr[tr.length - 1]);
await browser.close();
