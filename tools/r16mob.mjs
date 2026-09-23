import { chromium } from 'playwright';
const sleep = ms => new Promise(r => setTimeout(r, ms));
const tag = process.argv[2] || 'm';
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 390, height: 844 }, hasTouch: true, isMobile: true, deviceScaleFactor: 2 });
const errs = []; p.on('pageerror', e => errs.push(e.message));
await p.goto('http://127.0.0.1:4173/'); await sleep(1000);
await p.evaluate(() => document.getElementById('swipe').scrollIntoView()); await sleep(1500);
await p.screenshot({ path: `shots/r16/${tag}-0.png` });
for (let i = 0; i < 5; i++) {
  await p.click(i % 2 ? '#bLeft' : '#bRight'); await sleep(250);
  if (i === 1) await p.screenshot({ path: `shots/r16/${tag}-mid.png` });
  await sleep(700);
  if (i === 2) await p.screenshot({ path: `shots/r16/${tag}-1.png` });
}
await sleep(600); await p.screenshot({ path: `shots/r16/${tag}-veil.png` });
await sleep(1500); await p.screenshot({ path: `shots/r16/${tag}-veil2.png` }); await sleep(3000);
await p.evaluate(() => document.getElementById('desk').scrollIntoView()); await sleep(900);
await p.screenshot({ path: `shots/r16/${tag}-desk.png` });
await p.evaluate(() => scrollBy(0, 700)); await sleep(900);
await p.screenshot({ path: `shots/r16/${tag}-desk2.png` });
console.log('errors', errs);
await b.close();
