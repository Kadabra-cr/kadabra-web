import { chromium } from 'playwright';
const sleep = ms => new Promise(r => setTimeout(r, ms));
const b = await chromium.launch();
const p = await (await b.newContext({ viewport: { width: 1440, height: 900 } })).newPage();
await p.goto('http://127.0.0.1:4173/', { waitUntil: 'load' }); await sleep(1500);
const box = await p.locator('#field').boundingBox();
const toPage = (fx, fy) => ({ x: box.x + box.width * (fx / 1600), y: box.y + box.height * (fy / 900) });
const st = () => p.evaluate(() => { const f = document.getElementById('field').__field, w = f.game.word;
  const fly = w ? w.letters.filter(l => l.st === 'fly').map(l => ({ x: l.x, y: l.y, vx: l.vx, vy: l.vy })) : [];
  return { mass: f.heart.mass, phase: f.game.phase, wave: f.game.wave, hx: f.heart.x, hy: f.heart.y, fly }; });
let mx = 500, my = 500, armedAt = 0, hits = 0, lastMass = 0;
const t0 = Date.now();
while (Date.now() - t0 < 90000) {
  const s = await st();
  if (!armedAt && s.phase === 'armed') { armedAt = Date.now(); console.log('armed at', ((armedAt - t0) / 1000).toFixed(1), 's, mass', s.mass); }
  if (s.phase === 'dead') { console.log('DEAD', armedAt ? ((Date.now() - armedAt) / 1000).toFixed(1) : '?', 's into danger, at wave', s.wave, 'after', hits, 'drops'); break; }
  if (s.mass < lastMass) hits++; lastMass = s.mass;
  if (s.phase !== 'armed') { const a = Date.now() / 900; mx = 500 + Math.cos(a) * 55; my = 520 + Math.sin(a) * 40; }
  else {
    // flee the nearest letter, keep inside the field
    let fx = 0, fy = 0;
    s.fly.forEach(l => { const dx = s.hx - l.x, dy = s.hy - l.y, d = Math.hypot(dx, dy) || 1; const w = Math.max(0, 1 - d / 700) / d; fx += dx * w; fy += dy * w; });
    const n = Math.hypot(fx, fy) || 1;
    mx = Math.max(120, Math.min(1480, s.hx + fx / n * 420));
    my = Math.max(120, Math.min(780, s.hy + fy / n * 420));
    if (!s.fly.length) { const a = Date.now() / 700; mx = 800 + Math.cos(a) * 480; my = 450 + Math.sin(a) * 260; }
  }
  const q = toPage(mx, my); await p.mouse.move(q.x, q.y); await sleep(16);
}
const end = await st(); if (end.phase !== 'dead') console.log('SURVIVED 90 s, wave', end.wave, 'mass', end.mass, 'drops', hits);
await b.close();
