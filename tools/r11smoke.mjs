import { chromium } from 'playwright';
const sleep = ms => new Promise(r => setTimeout(r, ms));
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 1440, height: 900 } });
const errs = []; p.on('pageerror', e => errs.push(e.message));
await p.goto('http://127.0.0.1:4173/workshop/'); await sleep(800);
await p.evaluate(() => document.querySelector('.moment').scrollIntoView({ block: 'center' })); await sleep(1500);
await p.screenshot({ path: 'shots/r11/smoke-0.png' });
const box = await p.evaluate(() => { const r = document.querySelector('.moment .m-vis svg').getBoundingClientRect(); return { x: r.left, y: r.top, w: r.width, h: r.height }; });
for (let i = 0; i < 40; i++) {
  const t = i / 40 * Math.PI * 4;
  await p.mouse.move(box.x + box.w / 2 + Math.cos(t) * box.w * .16, box.y + box.h / 2 + Math.sin(t) * box.h * .15); await sleep(40);
}
await sleep(300);
await p.screenshot({ path: 'shots/r11/smoke-1.png' });
await p.mouse.move(10, 10); await sleep(2500);
await p.screenshot({ path: 'shots/r11/smoke-2.png' });
console.log(box, errs);
await b.close();
