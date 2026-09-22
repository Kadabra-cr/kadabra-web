import { chromium } from 'playwright';
const sleep = ms => new Promise(r => setTimeout(r, ms));
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 1440, height: 900 } });
const errs = []; p.on('pageerror', e => errs.push(e.message));
await p.goto('http://127.0.0.1:4173/'); await sleep(800);
const top = await p.evaluate(() => document.getElementById('swipe').getBoundingClientRect().top + scrollY);
await p.evaluate(y => scrollTo(0, y), top); await sleep(1500);
await p.click('#bSkip');
const t0 = Date.now();
for (const t of [1700, 2300, 3000, 4200, 5300, 6000, 8500]) {
  await sleep(t - (Date.now() - t0));
  await p.screenshot({ path: `shots/r11/fin-${t}.png` });
}
// long frame check during the veil: measure rAF gaps
await p.evaluate(() => document.getElementById('desk').scrollIntoView({ block: 'start' })); await sleep(800);
await p.screenshot({ path: 'shots/r11/fin-desk.png' });
// hover a rope's middle and hold still: count hot toggles
const toggles = await p.evaluate(async () => {
  const g = document.querySelector('.cable'); const path = g.querySelector('.rope');
  const L = path.getTotalLength(), mid = path.getPointAtLength(L / 2), svg = path.ownerSVGElement.getBoundingClientRect();
  const x = svg.left + mid.x, y = svg.top + mid.y; let n = 0;
  const row = document.querySelector('.row[data-fn="' + g.dataset.fn + '"]');
  new MutationObserver(() => n++).observe(row, { attributes: true, attributeFilter: ['class'] });
  const desk = document.getElementById('desk');
  for (let i = 0; i < 60; i++) { desk.dispatchEvent(new PointerEvent('pointermove', { clientX: x + Math.sin(i / 3) * 8, clientY: y + Math.cos(i / 4) * 6, bubbles: true })); await new Promise(r => setTimeout(r, 30)); }
  return { n, hot: row.classList.contains('hot') };
});
await p.screenshot({ path: 'shots/r11/fin-hover.png' });
console.log('hover toggles', toggles, 'errors', errs);
await b.close();
