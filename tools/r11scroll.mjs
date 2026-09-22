import { chromium } from 'playwright';
const sleep = ms => new Promise(r => setTimeout(r, ms));
const [w, h, step, tag] = [+(process.argv[2] || 1440), +(process.argv[3] || 900), +(process.argv[4] || 400), process.argv[5] || 'd'];
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: w, height: h } });
const errs = []; p.on('pageerror', e => errs.push(e.message));
await p.goto('http://127.0.0.1:4173/'); await sleep(1200);
const end = await p.evaluate(() => document.getElementById('swipe').getBoundingClientRect().top + scrollY);
for (let y = 0, i = 0; y <= end + 200; y += step, i++) {
  await p.evaluate(y => scrollTo(0, y), y); await sleep(750);
  await p.screenshot({ path: `shots/r11/${tag}-${String(i).padStart(2, '0')}.png` });
}
console.log('end', end, 'errors', errs);
await b.close();
