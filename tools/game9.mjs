import { chromium } from 'playwright';
const sleep = (ms) => new Promise(r => setTimeout(r, ms));
const browser = await chromium.launch(); const errors = [];
async function page() { const p = await (await browser.newContext({ viewport: { width: 1440, height: 900 } })).newPage(); p.on('pageerror', e => errors.push(e.message)); return p; }
async function play(p, sel, tag, fx, fy) {
  const box = await p.locator(sel).boundingBox(); const cx = box.x + box.width * fx, cy = box.y + box.height * fy;
  const st = () => p.evaluate(s => { const f = document.querySelector(s).__field; const host = document.querySelector(s).parentNode;
    const w = f.game.word; let overlap = 0;
    if (w) { const zs = [...host.querySelectorAll('.wrap > *')].flatMap(e => [...e.getClientRects()]); w.letters.forEach(l => { if (l.st !== 'held') return; const r = l.el.getBoundingClientRect(); if (zs.some(z => r.right > z.left && r.left < z.right && r.bottom > z.top && r.top < z.bottom && getComputedStyle(host.querySelector('.wrap')).opacity > .5)) overlap++; }); }
    return { mass: f.heart.mass, phase: f.game.phase, wave: f.game.wave, word: w ? w.letters.map(l => l.ch).join('') : '', fly: w ? w.letters.filter(l => l.st === 'fly').length : 0, overlap, h1: (host.querySelector('h1,h2') || {}).textContent }; }, sel);
  const t0 = Date.now(); let armedAt = 0, deadAt = 0, maxOverlap = 0, lastWord = '', shot = 0;
  for (let t = 0; Date.now() - t0 < 70000; t++) {
    const a = t * .05; await p.mouse.move(cx + Math.cos(a) * 55, cy + Math.sin(a) * 40); await sleep(16);
    if (t % 10) continue;
    const s = await st(); maxOverlap = Math.max(maxOverlap, s.overlap);
    if (!armedAt && s.phase === 'armed') { armedAt = Date.now(); console.log(tag, 'armed at', ((armedAt - t0) / 1000).toFixed(1), 's'); }
    if (s.word && s.word !== lastWord) { lastWord = s.word; console.log(tag, 'word', s.word, 'wave', s.wave, 'mass', s.mass); if (!shot) { shot = 1; await sleep(900); await p.screenshot({ path: `shots/r9/${tag}-word.png` }); } }
    if (s.fly && shot === 1) { shot = 2; await sleep(250); await p.screenshot({ path: `shots/r9/${tag}-fly.png` }); }
    if (s.phase === 'dead') { deadAt = Date.now(); console.log(tag, 'DEAD', ((deadAt - armedAt) / 1000).toFixed(1), 's after arming; copy:', s.h1); await sleep(1800); await p.screenshot({ path: `shots/r9/${tag}-dead.png` }); break; }
  }
  console.log(tag, 'max letters over live copy:', maxOverlap);
}
const p = await page(); await p.goto('http://127.0.0.1:4173/', { waitUntil: 'load' }); await sleep(1500);
await play(p, '#field', 'hero', .3, .62);
// the hero's cue: hidden while armed, shown after
console.log('cue display while dead:', await p.evaluate(() => getComputedStyle(document.querySelector('.hero .cue')).display));
const q = await page(); await q.goto('http://127.0.0.1:4173/', { waitUntil: 'load' }); await sleep(500);
await q.evaluate(() => document.getElementById('close-home').scrollIntoView({ block: 'center' })); await sleep(1500);
await play(q, '#close-home .closefield', 'close', .25, .5);
// condensed hero must not arm: scroll to split, gather
const c = await page(); await c.goto('http://127.0.0.1:4173/', { waitUntil: 'load' }); await sleep(800);
await c.evaluate(() => scrollTo(0, 600)); await sleep(800);
const bx = await c.locator('#field').boundingBox();
for (let t = 0; t < 900; t++) { const a = t * .05; await c.mouse.move(bx.x + bx.width * .5 + Math.cos(a) * 40, bx.y + bx.height * .8 + Math.sin(a) * 30); await sleep(16); }
console.log('condensed hero after 15 s of gathering:', JSON.stringify(await c.evaluate(() => { const f = document.getElementById('field').__field; return { mass: f.heart.mass, phase: f.game.phase }; })));
console.log('errors', errors); await browser.close();
