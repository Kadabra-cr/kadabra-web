import { chromium } from 'playwright';
const sleep = ms => new Promise(r => setTimeout(r, ms));
const b = await chromium.launch(); const errs = [];
const p = await (await b.newContext({ viewport: { width: 1440, height: 900 } })).newPage();
p.on('pageerror', e => errs.push(e.message));
await p.goto('http://127.0.0.1:4173/', { waitUntil: 'load' }); await sleep(1500);
const box = await p.locator('#field').boundingBox();
const cx = box.x + box.width * .32, cy = box.y + box.height * .6;
const st = () => p.evaluate(() => { const f = document.getElementById('field').__field, w = f.game.word;
  const fly = w ? w.letters.filter(l => l.st === 'fly') : [];
  return { mass: f.heart.mass, phase: f.game.phase, wave: f.game.wave, hx: f.heart.x, hy: f.heart.y,
    flyN: fly.length, minToHeart: fly.length ? Math.min(...fly.map(l => Math.hypot(l.x - f.heart.x, l.y - f.heart.y))) : -1,
    vmax: fly.length ? Math.max(...fly.map(l => Math.hypot(l.vx, l.vy))) : 0, h1: document.querySelector('.hero h1').textContent }; });
let t0 = Date.now(), armed = 0, dead = 0, dodged = 0, flying = 0;
// phase 1: gather with small slow circles; phase 2: dodge with big fast sweeps
while (Date.now() - t0 < 75000) {
  const s = await st();
  const gather = s.phase !== 'armed';
  for (let k = 0; k < 10; k++) {
    const a = (Date.now() / (gather ? 900 : 260)) % (Math.PI * 2);
    const rx = gather ? 55 : box.width * .33, ry = gather ? 40 : box.height * .3;
    await p.mouse.move(cx + Math.cos(a) * rx, cy + Math.sin(a) * ry); await sleep(16);
  }
  if (!armed && s.phase === 'armed') { armed = Date.now(); console.log('armed', ((armed - t0) / 1000).toFixed(1), 's'); }
  if (s.flyN) { flying++; if (s.minToHeart > 60) dodged++; }
  if (s.phase === 'dead') { dead = Date.now(); console.log('DEAD after', ((dead - armed) / 1000).toFixed(1), 's of danger, wave', s.wave); break; }
}
if (!dead) console.log('SURVIVED the whole run while dodging; wave', (await st()).wave);
console.log('samples with letters in the air:', flying, 'of which farther than 60 units from the heart:', dodged);
// the copy goes back when the hero steps aside
await p.evaluate(() => scrollTo(0, 700)); await sleep(2200);
const after = await st();
console.log('after shrinking: h1 =', JSON.stringify(after.h1), '| phase', after.phase);
console.log('errors', errs);
await b.close();
