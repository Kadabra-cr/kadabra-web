import { chromium } from 'playwright';
const sleep = ms => new Promise(r => setTimeout(r, ms));
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 1440, height: 900 } });
await p.goto('http://127.0.0.1:4173/'); await sleep(1000);
const top = await p.evaluate(() => document.getElementById('swipe').getBoundingClientRect().top + scrollY);
let i = 0;
for (let y = top - 1000; y <= top; y += 125) {
  await p.evaluate(y => scrollTo(0, y), y); await sleep(500);
  await p.screenshot({ path: `shots/r11/f-${i++}.png` });
}
await b.close();
