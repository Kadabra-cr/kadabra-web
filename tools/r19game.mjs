import { chromium } from 'playwright';
const sleep = ms => new Promise(r => setTimeout(r, ms));
const b = await chromium.launch();
const ctx = await b.newContext({ viewport: { width: 1440, height: 900 } });
const p = await ctx.newPage();
const errs = []; p.on('pageerror', e => errs.push(e.message));
await p.goto('http://127.0.0.1:4173/'); await sleep(1200);
const box = await p.locator('#field').boundingBox();
const F = () => p.evaluate(() => document.getElementById('field').__field.game.phase);
let t0 = Date.now();
while (Date.now() - t0 < 40000 && await F() !== 'asking') { const a = Date.now() / 900; await p.mouse.move(box.x + 520 + Math.cos(a) * 60, box.y + 420 + Math.sin(a) * 45); await sleep(16); }
// force :hover on the yes button through the devtools protocol
const cdp = await ctx.newCDPSession(p);
await cdp.send('DOM.enable'); await cdp.send('CSS.enable');
const { root } = await cdp.send('DOM.getDocument');
const { nodeId } = await cdp.send('DOM.querySelector', { nodeId: root.nodeId, selector: '#hero .ask .yes' });
await cdp.send('CSS.forcePseudoState', { nodeId, forcedPseudoClasses: ['hover'] });
await sleep(160);
const yes = await p.locator('#hero .ask .yes').boundingBox();
await p.screenshot({ path: 'tools/shots/r19/ask-jump.png', clip: { x: yes.x - 40, y: yes.y - 30, width: yes.width + 120, height: yes.height + 60 } });
console.log('hovered marks:', await p.evaluate(() => [...document.querySelectorAll('#hero .ask .yes .pm i')].map(i => i.textContent + ':' + getComputedStyle(i).visibility + ':' + getComputedStyle(i).transform).join('  ')));
await cdp.send('CSS.forcePseudoState', { nodeId, forcedPseudoClasses: [] });
await p.evaluate(() => document.querySelector('#hero .ask .yes').click()); await sleep(200);
console.log('scrollY', await p.evaluate(() => scrollY), 'phase', await F());
let w = null; t0 = Date.now();
while (Date.now() - t0 < 6000) { w = await p.evaluate(() => { const w = document.getElementById('field').__field.game.word; return w && { side: w.side, cx: w.cx, cy: w.cy }; }); if (w) break; await p.mouse.move(box.x + 700, box.y + 420); await sleep(50); }
await sleep(750);
const toScr = await p.evaluate(({ cx, cy }) => { const s = document.getElementById('field'), b = s.getBoundingClientRect(), k = Math.max(b.width / 1600, b.height / 900); return { x: b.left + (b.width - 1600 * k) / 2 + cx * k, y: b.top + (b.height - 900 * k) / 2 + cy * k }; }, w);
const sides = [];
for (let i = 1; i <= 14; i++) { await p.mouse.move(box.x + 700 + (toScr.x - box.x - 700) * i / 14, box.y + 420 + (toScr.y - box.y - 420) * i / 14); await sleep(30); }
for (let k = 0; k < 20; k++) { sides.push(await p.evaluate(() => { const w = document.getElementById('field').__field.game.word; return w ? (w.port ? 'P' : w.side) : '-'; })); if (k === 3) await p.screenshot({ path: 'tools/shots/r19/portal-mid.png' }); await sleep(60); }
console.log('word at', w, 'side over time:', sides.join(' '));
await p.screenshot({ path: 'tools/shots/r19/portal.png' });
console.log('errors', errs);
await b.close();
