import { chromium } from 'playwright';
const BASE = 'http://127.0.0.1:4173';
const sleep = ms => new Promise(r => setTimeout(r, ms));
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 1440, height: 900 } });
await p.goto(BASE + '/'); await sleep(1500);
const H = await p.evaluate(() => { const s = document.getElementById('swipe'); return s.getBoundingClientRect().top + scrollY; });
console.log('swipe top', H);
for (let y = 0, i = 0; y <= H; y += 450, i++) {
  await p.evaluate(y => scrollTo(0, y), y); await sleep(700);
  await p.screenshot({ path: `shots/r11/scroll-${String(i).padStart(2, '0')}-${y}.png` });
}
await p.evaluate(() => scrollTo(0, 0)); await sleep(500);
await p.screenshot({ path: 'shots/r11/hdr.png', clip: { x: 0, y: 0, width: 400, height: 90 } });
const why = await p.evaluate(() => document.getElementById('why').getBoundingClientRect().top + scrollY);
await p.evaluate(y => scrollTo(0, y), why); await sleep(1500);
await p.screenshot({ path: 'shots/r11/why.png' });
const m = await b.newPage({ viewport: { width: 390, height: 844 }, hasTouch: true, isMobile: true });
await m.goto(BASE + '/'); await sleep(1200);
const sw = await m.evaluate(() => document.getElementById('swipe').getBoundingClientRect().top + scrollY);
await m.evaluate(y => scrollTo(0, y), sw); await sleep(1500);
await m.screenshot({ path: 'shots/r11/m-swipe0.png', fullPage: false });
await m.click('#bRight'); await sleep(900);
await m.screenshot({ path: 'shots/r11/m-swipe1.png' });
await m.click('#bLeft'); await sleep(900);
await m.evaluate(y => scrollTo(0, y + 400), sw); await sleep(500);
await m.screenshot({ path: 'shots/r11/m-swipe2.png' });
await b.close();
