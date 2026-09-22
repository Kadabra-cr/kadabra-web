import { chromium } from 'playwright';
import { mkdirSync } from 'node:fs';
const OUT = 'shots/r8'; mkdirSync(OUT, { recursive: true });
const sleep = (ms) => new Promise(r => setTimeout(r, ms));
const browser = await chromium.launch();
const p = await (await browser.newContext({ viewport: { width: 1440, height: 900 } })).newPage();
const errors = []; p.on('pageerror', e => errors.push(e.message)); p.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
await p.goto('http://127.0.0.1:4173/', { waitUntil: 'load' }); await sleep(1500);
const box = await p.locator('#field').boundingBox();
const cx = box.x + box.width * .3, cy = box.y + box.height * .62;
const state = () => p.evaluate(() => { const f = document.getElementById('field').__field; const h = document.querySelector('.hero');
  return { mass: f.heart.mass, phase: f.game.phase, wave: f.game.wave, word: f.game.word ? f.game.word.letters.map(l => l.ch + ':' + l.st[0]).join('') : '', armed: h.classList.contains('armed'), dead: h.classList.contains('dead'), h1: h.querySelector('h1').textContent, fill: f.heart.fill, sc: f.heart.sc.toFixed(0) }; });
let t = 0; const start = Date.now(); let last = ''; const seen = {};
const SPEED = +(process.env.SPEED || .05);
while (Date.now() - start < 60000) {
  const a = t * SPEED; await p.mouse.move(cx + Math.cos(a) * 55, cy + Math.sin(a) * 40); await sleep(16); t++;
  if (t % 10 === 0) {
    const s = await state(); const key = s.phase + s.wave;
    const line = `${((Date.now() - start) / 1000).toFixed(1)}s mass=${s.mass} sc=${s.sc} ${s.phase} w${s.wave} ${s.fill} ${s.word}`;
    if (line.slice(6) !== last.slice(6)) console.log(line); last = line;
    if (!seen.heart && s.mass >= 3) { seen.heart = 1; await p.screenshot({ path: OUT + '/02-heart.png' }); }
    if (!seen.armed && s.armed) { seen.armed = 1; await p.screenshot({ path: OUT + '/03-armed.png' }); }
    if (!seen.word && s.word && s.word.indexOf(':f') < 0 && s.word.length > 8) { seen.word = 1; await sleep(800); await p.screenshot({ path: OUT + '/04-word.png' }); }
    if (!seen.fly && s.word.indexOf(':f') >= 0) { seen.fly = 1; await sleep(350); await p.screenshot({ path: OUT + '/05-fly.png' }); await sleep(500); await p.screenshot({ path: OUT + '/05b-fly.png' }); }
    if (!seen.dead && s.dead) { seen.dead = 1; await sleep(250); await p.screenshot({ path: OUT + '/06-dead.png' }); await sleep(1800); await p.screenshot({ path: OUT + '/06b-dead.png' }); console.log('DEAD copy:', s.h1); }
    if (seen.dead && !s.dead) { await sleep(1600); await p.screenshot({ path: OUT + '/07-reborn.png' }); console.log('reborn'); break; }
  }
}
console.log('seen', JSON.stringify(seen), 'errors', errors);
await browser.close();
