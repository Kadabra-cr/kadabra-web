import { chromium } from 'playwright';
const b = await chromium.launch();
for (const w of [320, 360, 390, 430, 700]) {
  const p = await (await b.newContext({ viewport: { width: w, height: 700 }, isMobile: true, hasTouch: true })).newPage();
  await p.goto('http://127.0.0.1:4173/learn-more/');
  const r = await p.evaluate(() => { const q = s => document.querySelector(s).getBoundingClientRect(); const n = q('.nav'); return { iw: innerWidth, brand: Math.round(q('.brand svg').width), nav: [Math.round(n.left), Math.round(n.right), Math.round(n.height)], wa: Math.round(q('.hdr .cta').right) }; });
  console.log(w, JSON.stringify(r));
  await p.screenshot({ path: `tools/shots/r16/hdr-${w}.png`, clip: { x: 0, y: 0, width: w, height: 80 } });
}
await b.close();
