import { chromium } from 'playwright';
const sleep = ms => new Promise(r => setTimeout(r, ms));
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 1440, height: 900 } });
const errs = []; p.on('pageerror', e => errs.push(e.message)); p.on('console', m => m.type() === 'error' && errs.push(m.text()));
await p.goto('http://127.0.0.1:4173/'); await sleep(1200);
await p.screenshot({ path: 'tools/shots/r19/hero-cue.png' });
// gather until asked
const box = await p.locator('#field').boundingBox();
const F = () => p.evaluate(() => document.getElementById('field').__field.game.phase);
let t0 = Date.now();
while (Date.now() - t0 < 40000 && await F() !== 'asking') { const a = Date.now() / 900; await p.mouse.move(box.x + 520 + Math.cos(a) * 60, box.y + 420 + Math.sin(a) * 45); await sleep(16); }
const yes = await p.locator('#hero .ask .yes').boundingBox();
await p.mouse.move(yes.x + yes.width / 2, yes.y + yes.height / 2); await sleep(120);
await p.screenshot({ path: 'tools/shots/r19/ask-jump.png', clip: { x: yes.x - 40, y: yes.y - 30, width: yes.width + 120, height: yes.height + 60 } });
console.log('marks visible on hover:', await p.evaluate(() => [...document.querySelectorAll('#hero .ask .yes .pm i')].map(i => i.textContent + ':' + getComputedStyle(i).visibility).join(' ')));
await p.click('#hero .ask .yes'); await sleep(200);
// wait for a phrase, then walk the hand onto it and watch the side switch
let w = null; t0 = Date.now();
while (Date.now() - t0 < 6000) { w = await p.evaluate(() => { const w = document.getElementById('field').__field.game.word; return w && { side: w.side, cx: w.cx, cy: w.cy }; }); if (w) break; await sleep(50); }
await sleep(750);
const toScr = await p.evaluate(({ cx, cy }) => { const s = document.getElementById('field'), b = s.getBoundingClientRect(), k = Math.max(b.width / 1600, b.height / 900); return { x: b.left + (b.width - 1600 * k) / 2 + cx * k, y: b.top + (b.height - 900 * k) / 2 + cy * k }; }, w);
for (let i = 1; i <= 12; i++) { await p.mouse.move(box.x + 520 + (toScr.x - box.x - 520) * i / 12, box.y + 420 + (toScr.y - box.y - 420) * i / 12); await sleep(30); }
await sleep(700);
const w2 = await p.evaluate(() => { const w = document.getElementById('field').__field.game.word; return w && { side: w.side, fired: w.front }; });
console.log('phrase side before', w.side, 'after hand on it', w2 && w2.side, 'letters fired', w2 && w2.fired);
await p.screenshot({ path: 'tools/shots/r19/portal.png' });
// exit the game and look at the rest
await p.click('.mode button'); await sleep(400);
for (const [id, name, pre] of [['morph', 'policy', 0.62], ['vizscr', 'viz', 0.5]]) {
  await p.evaluate(({ id, pre }) => { const el = document.getElementById(id); scrollTo(0, el.getBoundingClientRect().top + scrollY + el.offsetHeight * pre); }, { id, pre });
  await sleep(2600); await p.screenshot({ path: `tools/shots/r19/${name}.png` });
}
await p.evaluate(() => document.querySelector('footer').scrollIntoView()); await sleep(500);
console.log('footer linkedin:', await p.evaluate(() => { const a = [...document.querySelectorAll('footer a')].find(a => /linkedin/.test(a.href)); return a && a.textContent + ' -> ' + a.href; }));
await p.goto('http://127.0.0.1:4173/workshop/'); await sleep(900);
const sm = p.locator('[data-vis=smoke] .m-vis svg');
await sm.scrollIntoViewIfNeeded(); await sleep(600);
const sb = await sm.boundingBox();
await p.screenshot({ path: 'tools/shots/r19/smoke-0.png', clip: { x: sb.x - 30, y: sb.y - 30, width: sb.width + 60, height: sb.height + 60 } });
for (let k = 0; k < 40; k++) { const a = k / 40 * Math.PI * 4; await p.mouse.move(sb.x + sb.width / 2 + Math.cos(a) * sb.width * .18, sb.y + sb.height / 2 + Math.sin(a) * sb.height * .18); await sleep(25); }
await sleep(300);
await p.screenshot({ path: 'tools/shots/r19/smoke-1.png', clip: { x: sb.x - 30, y: sb.y - 30, width: sb.width + 60, height: sb.height + 60 } });
await p.mouse.move(5, 300); await sleep(2500);
await p.screenshot({ path: 'tools/shots/r19/smoke-2.png', clip: { x: sb.x - 30, y: sb.y - 30, width: sb.width + 60, height: sb.height + 60 } });
await p.evaluate(() => document.querySelector('[data-vis=rules]').scrollIntoView({ block: 'center' })); await sleep(3000);
await p.screenshot({ path: 'tools/shots/r19/rules.png' });
console.log('errors', errs);
await b.close();
