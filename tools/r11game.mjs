/* Round 11 game check: words mid-height from a side, letters in pairs, homing
   then straight, three hits and out, restart after ~20 s, frame times.
   node r11game.mjs [dodge|still] [/|close] */
import { chromium } from 'playwright';
const sleep = ms => new Promise(r => setTimeout(r, ms));
const mode = process.argv[2] || 'dodge', where = process.argv[3] || 'hero';
const b = await chromium.launch();
const p = await (await b.newContext({ viewport: { width: 1440, height: 900 } })).newPage();
const errs = []; p.on('pageerror', e => errs.push(e.message));
await p.goto('http://127.0.0.1:4173/', { waitUntil: 'load' }); await sleep(1200);
const sel = where === 'close' ? '#close-home .closefield' : '#field';
if (where === 'close') { await p.evaluate(() => document.querySelector('#close-home').scrollIntoView({ block: 'center' })); await sleep(1200); }
const box = await p.locator(sel).boundingBox();
const FH = where === 'close' ? 620 : 900;
/* the field is "slice"-scaled: map field units to the page */
const sc = Math.max(box.width / 1600, box.height / FH), ox = (box.width - 1600 * sc) / 2, oy = (box.height - FH * sc) / 2;
const toPage = (fx, fy) => ({ x: box.x + ox + fx * sc, y: box.y + oy + fy * sc });
await p.evaluate(s => {
  window.__ft = []; let l = 0;
  requestAnimationFrame(function f(t) { if (l) window.__ft.push(t - l); l = t; requestAnimationFrame(f); });
  window.__F = document.querySelector(s).__field;
}, sel);
const st = () => p.evaluate(() => { const f = window.__F, w = f.game.word;
  const fly = w ? w.letters.filter(l => l.st === 'fly').map(l => ({ x: l.x, y: l.y })) : [];
  return { mass: f.heart.mass, phase: f.game.phase, wave: f.game.wave, hits: f.game.hits, hx: f.heart.x, hy: f.heart.y, fly,
    word: w ? { cy: w.cy, cx: w.cx, n: w.letters.length, fs: +w.letters[0].el.getAttribute('font-size') } : null,
    texts: document.querySelectorAll('.war text').length }; });
let mx = 500, my = 450, armedAt = 0, maxFly = 0, maxTexts = 0, words = [], shot = 0;
const t0 = Date.now();
let s, lastHits = 0;
while (Date.now() - t0 < 120000) {
  s = await st();
  if (!armedAt && s.phase === 'armed') { armedAt = Date.now(); await p.evaluate(() => { window.__ft = []; }); console.log('armed at', ((armedAt - t0) / 1000).toFixed(1), 's, mass', s.mass); }
  if (s.word && !words.find(w => w.cx === s.word.cx && w.wave === s.wave)) { words.push({ ...s.word, wave: s.wave }); }
  maxFly = Math.max(maxFly, s.fly.length); maxTexts = Math.max(maxTexts, s.texts);
  if (s.fly.length >= 2 && shot < 2) { await p.screenshot({ path: `shots/r11/game-${where}-${shot++}.png` }); }
  if (s.hits > lastHits) { lastHits = s.hits; console.log('hit', s.hits, ((Date.now() - armedAt) / 1000).toFixed(2), 's heart', s.hx.toFixed(0), s.hy.toFixed(0), 'mouse-target', mx.toFixed(0), my.toFixed(0), 'fly', s.fly.length); }
  if (s.phase === 'asking') {
    if (!s.askShot) { await sleep(900); await p.screenshot({ path: `shots/r11/ask-${where}.png` }); s.askShot = 1; }
    await p.click((where === 'close' ? '#close-home' : '#hero') + ' .ask .yes'); await sleep(900);
    await p.screenshot({ path: `shots/r11/mode-${where}.png` });
    await p.mouse.wheel(0, 600); await sleep(120);
    console.log('scrollY after wheel', await p.evaluate(() => scrollY), 'chip shaking', await p.evaluate(() => document.querySelector('.mode').classList.contains('shake')));
    continue;
  }
  if (s.phase === 'dead') break;
  if (s.phase !== 'armed') { const a = Date.now() / 900; mx = 520 + Math.cos(a) * 60; my = 450 + Math.sin(a) * 45; }
  else if (mode === 'dodge') {
    let fx = 0, fy = 0;
    s.fly.forEach(l => { const dx = s.hx - l.x, dy = s.hy - l.y, d = Math.hypot(dx, dy) || 1; const w = Math.max(0, 1 - d / 600) / d; fx += (dx * w) - dy * w * .8; fy += (dy * w) + dx * w * .8; });
    const n = Math.hypot(fx, fy) || 1;
    mx = Math.max(200, Math.min(1400, s.hx + fx / n * 380 + (800 - s.hx) * .35)); my = Math.max(160, Math.min(FH - 160, s.hy + fy / n * 380 + (FH / 2 - s.hy) * .35));
    if (!s.fly.length) { const a = Date.now() / 700; mx = 800 + Math.cos(a) * 260; my = FH / 2 + Math.sin(a) * FH * .28; }
  } else if (mode === 'circle') { const a = Date.now() / 380; mx = 800 + Math.cos(a) * 330; my = FH / 2 + Math.sin(a) * FH * .3;
  } else { const a = Date.now() / 1500; mx = 800 + Math.cos(a) * 150; my = FH / 2 + Math.sin(a) * 90; }
  const q = toPage(mx, my); await p.mouse.move(q.x, q.y); await sleep(16);
}
const ft = await p.evaluate(() => window.__ft.slice().sort((a, b) => a - b));
const pct = k => ft.length ? ft[Math.min(ft.length - 1, Math.floor(ft.length * k))].toFixed(1) : '-';
console.log(mode, where, s.phase === 'dead' ? `DEAD ${((Date.now() - armedAt) / 1000).toFixed(1)} s into danger, wave ${s.wave}, hits ${s.hits}` : `alive, wave ${s.wave}, hits ${s.hits}`);
console.log('words', words.map(w => `${w.n}L fs${w.fs.toFixed(0)} cx${w.cx.toFixed(0)} cy${w.cy}`).join(' | '));
console.log('max letters flying', maxFly, 'max text nodes', maxTexts, 'frames', ft.length, 'p50', pct(.5), 'p95', pct(.95), 'p99', pct(.99), 'max', ft.length ? ft[ft.length - 1].toFixed(1) : '-');
if (s.phase === 'dead') {
  const d0 = Date.now(); let back = 0;
  await p.mouse.move(box.x + 20, box.y + 20);
  await sleep(3900); await p.screenshot({ path: `shots/r11/dead-${where}.png` });
  console.log('pointing', await p.evaluate(s => document.querySelector(s).parentNode.classList.contains('pointing'), sel));
  while (Date.now() - d0 < 26000) { const q = await st(); if (q.phase !== 'dead') { back = Date.now() - d0; break; } await sleep(250); }
  console.log('restart after', (back / 1000).toFixed(1), 's');
}
console.log('errors', errs);
await b.close();
