import { chromium } from 'playwright';
import fs from 'fs';

const sleep = (ms) => new Promise(r => setTimeout(r, ms));

fs.mkdirSync('shots/r9', { recursive: true });

const browser = await chromium.launch();
const context = await browser.newContext({ viewport: { width: 1440, height: 900 } });
const page = await context.newPage();
const errors = [];
page.on('pageerror', e => errors.push(e.message));
page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });

let fails = 0;
function report(ok, msg) { console.log((ok ? 'PASS' : 'FAIL') + ' ' + msg); if (!ok) fails++; }

await page.goto('http://127.0.0.1:4173/', { waitUntil: 'load' });
await page.evaluate(() => document.getElementById('swipe').scrollIntoView({ block: 'center' }));
await sleep(300);
await page.click('#bSkip');
await sleep(9000);

// --- 5 cable groups ---
const cableCount = await page.evaluate(() => document.querySelectorAll('#cables .cable').length);
report(cableCount === 5, `cables = ${cableCount} (expected 5)`);

// --- flip rows exist on both sides ---
const flipCounts = await page.evaluate(() => ({
  flip: document.querySelectorAll('#rows .row.flip').length,
  noflip: document.querySelectorAll('#rows .row:not(.flip)').length
}));
report(flipCounts.flip >= 1, `rows.flip = ${flipCounts.flip} (expected >= 1)`);
report(flipCounts.noflip >= 1, `rows:not(.flip) = ${flipCounts.noflip} (expected >= 1)`);

// --- ropes stay above the row below them ---
const geo = await page.evaluate(() => {
  const desk = document.getElementById('desk').getBoundingClientRect();
  const rows = [...document.querySelectorAll('#rows .row')].map(r => {
    const b = r.getBoundingClientRect();
    return { fn: r.dataset.fn, top: b.top - desk.top, flip: r.classList.contains('flip') };
  }).sort((a, b) => a.top - b.top);
  const ropes = [...document.querySelectorAll('#cables .cable')].map(g => ({
    fn: g.dataset.fn,
    d: g.querySelector('.rope').getAttribute('d')
  }));
  return { rows, ropes };
});
const rowIndex = new Map(geo.rows.map((r, i) => [r.fn, i]));
let ropeChecks = [];
for (const rope of geo.ropes) {
  const nums = (rope.d.match(/-?\d+\.?\d*/g) || []).map(Number);
  const ys = nums.filter((_, i) => i % 2 === 1);
  const maxY = Math.max(...ys);
  const i = rowIndex.get(rope.fn);
  const next = geo.rows[i + 1];
  if (!next) { ropeChecks.push({ fn: rope.fn, ok: true, note: 'last row, no row below' }); continue; }
  const limit = next.top - 4;
  ropeChecks.push({ fn: rope.fn, ok: maxY <= limit, note: `maxY=${maxY.toFixed(1)} limit=${limit.toFixed(1)}` });
}
ropeChecks.forEach(c => report(c.ok, `rope fn=${c.fn} clears next row (${c.note})`));

// --- finale card is big enough ---
// the finale folds in on arrival: measure it once it has settled
await page.evaluate(() => document.getElementById('reveal').scrollIntoView({ block: 'center' }));
await page.waitForFunction(() => { const f = document.querySelector('.finale'); return f && getComputedStyle(f).transform === 'none'; }, null, { timeout: 8000 });
await new Promise(r => setTimeout(r, 400));
const fcardBox = await page.locator('.fcard').boundingBox();
report(!!fcardBox && fcardBox.height >= 300, `fcard height = ${fcardBox ? fcardBox.height.toFixed(1) : 'null'} (expected >= 300)`);

// --- screenshots ---
await page.evaluate(() => document.getElementById('desk').scrollIntoView({ block: 'center' }));
await sleep(300);
await page.screenshot({ path: 'shots/r9/desk.png' });

await page.evaluate(() => document.getElementById('reveal').scrollIntoView({ block: 'center' }));
await sleep(300);
await page.screenshot({ path: 'shots/r9/finale.png' });

console.log('errors', errors);
report(errors.length === 0, `console/page errors = ${errors.length}`);

console.log(fails === 0 ? 'ALL PASS' : `${fails} CHECK(S) FAILED`);
await browser.close();
process.exit(fails === 0 ? 0 : 1);
