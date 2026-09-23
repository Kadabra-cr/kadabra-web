import { chromium } from 'playwright';
const sleep = ms => new Promise(r => setTimeout(r, ms));
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 1440, height: 900 } });
await p.goto('http://127.0.0.1:4173/'); await sleep(1000);
const box = await p.locator('#field').boundingBox();
const T0 = Date.now(); let last = -1;
while (Date.now() - T0 < 20000) {
  const a = Date.now() / 900; await p.mouse.move(box.x + 520 + Math.cos(a) * 60, box.y + 420 + Math.sin(a) * 45); await sleep(16);
  const m = await p.evaluate(() => document.getElementById('field').__field.heart.mass);
  if (m !== last) { process.stdout.write(`${m}@${((Date.now() - T0) / 1000).toFixed(1)}s `); last = m; }
}
await b.close();
