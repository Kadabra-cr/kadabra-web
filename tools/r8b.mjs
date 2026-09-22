import { chromium } from 'playwright';
const sleep = (ms) => new Promise(r => setTimeout(r, ms));
const browser = await chromium.launch();
const errors = [];
async function page(vp = { width: 1440, height: 900 }) { const p = await (await browser.newContext({ viewport: vp })).newPage(); p.on('pageerror', e => errors.push(e.message)); p.on('console', m => { if (m.type() === 'error') errors.push(m.text()); }); return p; }
/* a: a fading heart stays put when the hand teleports away (calm phase) */
{
  const p = await page(); await p.goto('http://127.0.0.1:4173/', { waitUntil: 'load' }); await sleep(1500);
  const box = await p.locator('#field').boundingBox(); const cx = box.x + box.width * .3, cy = box.y + box.height * .62;
  for (let t = 0; t < 260; t++) { const a = t * .05; await p.mouse.move(cx + Math.cos(a) * 55, cy + Math.sin(a) * 40); await sleep(16); }
  const m0 = await p.evaluate(() => document.getElementById('field').__field.heart.mass);
  await p.mouse.move(box.x + box.width * .92, box.y + box.height * .12);
  const trace = await p.evaluate(async () => { const f = document.getElementById('field').__field; const out = [];
    for (let k = 0; k < 90; k++) { out.push({ x: f.heart.x, y: f.heart.y, o: f.heart.o, mass: f.heart.mass }); await new Promise(r => setTimeout(r, 40)); } return out; });
  let maxStep = 0; for (let k = 1; k < trace.length; k++) if (trace[k - 1].o > .02) maxStep = Math.max(maxStep, Math.hypot(trace[k].x - trace[k - 1].x, trace[k].y - trace[k - 1].y));
  const last = trace[trace.length - 1];
  console.log(`teleport: mass before ${m0}, max step while visible ${maxStep.toFixed(1)} u/40ms, end mass ${last.mass} o ${last.o.toFixed(3)} at (${last.x.toFixed(0)},${last.y.toFixed(0)}) start (${trace[0].x.toFixed(0)},${trace[0].y.toFixed(0)})`);
  await p.context().close();
}
/* b: the same engine at the bottom: arm and get a word on "Ready when you are" */
{
  const p = await page(); await p.goto('http://127.0.0.1:4173/', { waitUntil: 'load' }); await sleep(600);
  await p.evaluate(() => document.getElementById('close-home').scrollIntoView({ block: 'center' })); await sleep(1600);
  const box = await p.locator('#close-home .closefield').boundingBox(); const cx = box.x + box.width * .25, cy = box.y + box.height * .5;
  let s = null; const start = Date.now();
  for (let t = 0; Date.now() - start < 30000; t++) { const a = t * .05; await p.mouse.move(cx + Math.cos(a) * 55, cy + Math.sin(a) * 40); await sleep(16);
    if (t % 20 === 0) { s = await p.evaluate(() => { const f = document.querySelector('#close-home .closefield').__field; return { mass: f.heart.mass, phase: f.game.phase, letters: f.game.word ? f.game.word.letters.length : 0 }; }); if (s.letters) break; } }
  console.log('close field:', JSON.stringify(s), 'after', ((Date.now() - start) / 1000).toFixed(1), 's');
  await sleep(900); await p.screenshot({ path: 'shots/r8/08-close-word.png' });
  await p.context().close();
}
/* c: learn more has the half-day band */
{
  const p = await page(); await p.goto('http://127.0.0.1:4173/learn-more/', { waitUntil: 'load' }); await sleep(600);
  const ok = await p.evaluate(() => !!document.getElementById('halfday-learn') && document.getElementById('halfday-learn').compareDocumentPosition(document.getElementById('close-learn')) & Node.DOCUMENT_POSITION_FOLLOWING);
  console.log('learn-more half-day band before close:', ok);
  await p.context().close();
}
console.log('errors', errors);
await browser.close();
