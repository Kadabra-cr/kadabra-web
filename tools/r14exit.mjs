import { chromium } from 'playwright';
const sleep = ms => new Promise(r => setTimeout(r, ms));
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 1440, height: 900 } });
const errs = []; p.on('pageerror', e => errs.push(e.message));
await p.goto('http://127.0.0.1:4173/'); await sleep(1000);
const box = await p.locator('#field').boundingBox();
const F = () => p.evaluate(() => { const f = document.getElementById('field').__field; return { phase: f.game.phase, mass: f.heart.mass, off: !!f.game.off }; });
let t0 = Date.now(), s;
while (Date.now() - t0 < 60000) { s = await F(); if (s.phase === 'asking') break; const a = Date.now() / 900; await p.mouse.move(box.x + 520 + Math.cos(a) * 60, box.y + 420 + Math.sin(a) * 45); await sleep(16); }
console.log('asked', s);
await p.click('#hero .ask .yes'); await sleep(1200);
console.log('after yes', await F());
await p.mouse.click(box.x + 300, box.y + 300); await sleep(100);
console.log('click shakes chip', await p.evaluate(() => document.querySelector('.mode').classList.contains('shake')));
await p.click('.mode button'); await sleep(2500);
console.log('after exit', await F(), 'chip on', await p.evaluate(() => document.querySelector('.mode').classList.contains('on')));
t0 = Date.now(); let asked = false;
while (Date.now() - t0 < 15000) { const q = await F(); if (q.phase === 'asking' || q.mass > 0) { asked = true; break; } const a = Date.now() / 900; await p.mouse.move(box.x + 520 + Math.cos(a) * 60, box.y + 420 + Math.sin(a) * 45); await sleep(30); }
console.log('gathers again after exit', asked);
await p.mouse.wheel(0, 700); await sleep(600);
console.log('scrolls after exit', await p.evaluate(() => scrollY), 'errors', errs);
await b.close();
