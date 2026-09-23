import { chromium } from 'playwright';
const sleep = ms => new Promise(r => setTimeout(r, ms));
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 1440, height: 900 } });
await p.goto('http://127.0.0.1:4173/'); await sleep(1000);
const T0 = Date.now(); const box = await p.locator('#field').boundingBox();
const F = () => p.evaluate(() => document.getElementById('field').__field.game.phase);
let t0 = Date.now();
while (Date.now() - t0 < 60000 && await F() !== 'asking') { const a = Date.now() / 900; await p.mouse.move(box.x + 520 + Math.cos(a) * 60, box.y + 420 + Math.sin(a) * 45); await sleep(16); }
p.on('pageerror', e => console.log('ERR', e.message));
console.log('asked after ms', Date.now() - T0); await sleep(700);
console.log(await p.evaluate(() => { const a = document.querySelector('#hero .ask'); return a.className + ' | ' + a.style.transform + ' | ' + JSON.stringify(a.getBoundingClientRect()); }));
const r0 = await p.locator('#hero .ask').boundingBox();
const tgt = { x: r0.x + r0.width / 2, y: r0.y + r0.height / 2 };
const cur = { x: box.x + 520, y: box.y + 420 };
for (let i = 1; i <= 20; i++) { await p.mouse.move(cur.x + (tgt.x - cur.x) * i / 20, cur.y + (tgt.y - cur.y) * i / 20); await sleep(40); }
await sleep(300);
const r1 = await p.locator('#hero .ask').boundingBox();
await p.screenshot({ path: 'shots/r16/ask-hover.png', clip: { x: Math.max(0, r1.x - 260), y: Math.max(0, r1.y - 170), width: 700, height: 340 } });
console.log('pill moved by', (r1.x - r0.x).toFixed(1), (r1.y - r0.y).toFixed(1), 'size', r0.width.toFixed(0), 'x', r0.height.toFixed(0));
console.log('hover text:', await p.evaluate(() => [...document.querySelectorAll('#hero .ask .yes span')].map(s => s.textContent + '=' + getComputedStyle(s).opacity).join(' ')));
await p.click('#hero .ask .yes'); await sleep(300);
console.log('phase after click', await F());
await p.evaluate(() => document.querySelector('#viz .aside').scrollIntoView({ block: 'center' }));
console.log(await p.evaluate(() => document.querySelector('#viz .aside').textContent.trim() + ' || ' + document.querySelectorAll('#viz .cites .src')[1].textContent));
await b.close();
