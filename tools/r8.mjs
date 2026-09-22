/* round-8 frame checks: the game, the scene, the swipe fix, cables, finale, half-day, broken star */
import { chromium } from 'playwright';
import { mkdirSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';
const HERE = dirname(fileURLToPath(import.meta.url));
const OUT = join(HERE, 'shots', 'r8'); mkdirSync(OUT, { recursive: true });
const BASE = process.env.BASE || 'http://127.0.0.1:4173';
const sleep = (ms) => new Promise(r => setTimeout(r, ms));
const browser = await chromium.launch();
const errors = [];
async function page(vp = { width: 1440, height: 900 }) {
  const ctx = await browser.newContext({ viewport: vp });
  const p = await ctx.newPage();
  p.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
  p.on('pageerror', e => errors.push('pageerror: ' + e.message));
  return p;
}
const log = (...a) => console.log(...a);

/* ---------------- 1. hero + game ---------------- */
{
  const p = await page();
  await p.goto(BASE + '/', { waitUntil: 'load' }); await sleep(1800);
  await p.screenshot({ path: join(OUT, '01-hero.png') });
  const box = await p.locator('#field').boundingBox();
  const cx = box.x + box.width * .3, cy = box.y + box.height * .62;
  // gather: small slow circles around one spot
  const heartState = () => p.evaluate(() => {
    const h = document.querySelector('#field .heartmark');
    const m = /translate\(([-\d.]+) ([-\d.]+)\) scale\(([-\d.]+)\)/.exec(h.getAttribute('transform') || '');
    return { o: +h.getAttribute('opacity'), x: m ? +m[1] : 0, y: m ? +m[2] : 0, sc: m ? +m[3] : 0, fill: h.firstChild.getAttribute('fill'),
      armed: document.querySelector('.hero').classList.contains('armed'), dead: document.querySelector('.hero').classList.contains('dead'),
      letters: document.querySelectorAll('#field .war text').length, h1: document.querySelector('.hero h1').textContent };
  });
  let t = 0, armedAt = 0, shots = { heart: false, armed: false, word: false, fly: false, dead: false };
  const start = Date.now();
  while (Date.now() - start < 42000) {
    const a = t * .16;
    await p.mouse.move(cx + Math.cos(a) * 70, cy + Math.sin(a) * 50);
    await sleep(16); t++;
    if (t % 12 === 0) {
      const s = await heartState();
      if (!shots.heart && s.sc > .5) { shots.heart = true; log('heart formed at', ((Date.now() - start) / 1000).toFixed(1), 's', JSON.stringify(s)); await p.screenshot({ path: join(OUT, '02-heart.png') }); }
      if (!shots.armed && s.armed) { shots.armed = true; armedAt = Date.now(); log('armed at', ((Date.now() - start) / 1000).toFixed(1), 's', JSON.stringify(s)); await p.screenshot({ path: join(OUT, '03-armed.png') }); }
      if (!shots.word && s.letters > 0) { shots.word = true; log('word at', ((Date.now() - start) / 1000).toFixed(1), 's'); await sleep(900); await p.screenshot({ path: join(OUT, '04-word.png') }); }
      if (shots.word && !shots.fly && Date.now() - armedAt > 8500) { shots.fly = true; await p.screenshot({ path: join(OUT, '05-fly.png') }); await sleep(600); await p.screenshot({ path: join(OUT, '05b-fly.png') }); }
      if (!shots.dead && s.dead) { shots.dead = true; log('dead at', ((Date.now() - start) / 1000).toFixed(1), 's', s.h1); await sleep(300); await p.screenshot({ path: join(OUT, '06-dead.png') }); await sleep(1500); await p.screenshot({ path: join(OUT, '06b-dead.png') }); }
      if (shots.dead && !s.dead) { log('reborn at', ((Date.now() - start) / 1000).toFixed(1), 's'); await sleep(1500); await p.screenshot({ path: join(OUT, '07-reborn.png') }); break; }
    }
  }
  log('game shots', JSON.stringify(shots));
  await p.context().close();
}

/* ---------------- 2. no teleport: a fading heart stays put ---------------- */
{
  const p = await page();
  await p.goto(BASE + '/', { waitUntil: 'load' }); await sleep(1500);
  const box = await p.locator('#field').boundingBox();
  const cx = box.x + box.width * .3, cy = box.y + box.height * .62;
  for (let t = 0; t < 240; t++) { const a = t * .16; await p.mouse.move(cx + Math.cos(a) * 70, cy + Math.sin(a) * 50); await sleep(16); }
  const before = await p.evaluate(() => document.querySelector('#field .heartmark').getAttribute('transform'));
  // teleport the hand far away and sample the heart's position while it fades
  await p.mouse.move(box.x + box.width * .9, box.y + box.height * .15);
  const trace = await p.evaluate(async () => {
    const h = document.querySelector('#field .heartmark'); const out = [];
    for (let k = 0; k < 70; k++) {
      const m = /translate\(([-\d.]+) ([-\d.]+)\)/.exec(h.getAttribute('transform'));
      out.push({ x: +m[1], y: +m[2], o: +h.getAttribute('opacity') });
      await new Promise(r => setTimeout(r, 40));
    }
    return out;
  });
  let maxStep = 0;
  for (let k = 1; k < trace.length; k++) if (trace[k - 1].o > .02) maxStep = Math.max(maxStep, Math.hypot(trace[k].x - trace[k - 1].x, trace[k].y - trace[k - 1].y));
  log('teleport check: before', before, 'max step while visible =', maxStep.toFixed(1), 'units / 40 ms, final o', trace[trace.length - 1].o);
  await p.context().close();
}

/* ---------------- 3. the scene ---------------- */
{
  const p = await page();
  await p.goto(BASE + '/', { waitUntil: 'load' }); await sleep(1200);
  const h = await p.evaluate(() => ({ scene: document.getElementById('scene').offsetHeight, pin: document.querySelector('.scene-pin').offsetHeight, live: document.getElementById('scene').classList.contains('live') }));
  log('scene', JSON.stringify(h));
  const track = h.scene - h.pin;
  for (const [f, name] of [[.1, 'q0'], [.3, 'q-early'], [.45, 'q-mid'], [.62, 'q-late'], [.85, 'q-hold'], [1.15, 'past']]) {
    await p.evaluate((y) => window.scrollTo(0, y), Math.round(track * f)); await sleep(500);
    const q = await p.evaluate(() => getComputedStyle(document.getElementById('scene')).getPropertyValue('--q'));
    await p.screenshot({ path: join(OUT, `10-scene-${name}.png`) });
    log('scene', name, 'q=', q.trim());
  }
  await p.evaluate(() => document.getElementById('numbers').scrollIntoView()); await sleep(3200);
  await p.screenshot({ path: join(OUT, '11-policy.png') });
  await p.evaluate(() => document.getElementById('viz').scrollIntoView()); await sleep(3200);
  await p.screenshot({ path: join(OUT, '12-taught.png') });
  await p.context().close();
}

/* ---------------- 4. swipe: dealt card stays dealt even mid-nudge ---------------- */
{
  const p = await page();
  await p.goto(BASE + '/', { waitUntil: 'load' }); await sleep(600);
  await p.evaluate(() => document.getElementById('swipe').scrollIntoView({ block: 'start' })); await sleep(1400);
  // wait for the nudge to be mid-flight, then drag the card away
  await p.waitForFunction(() => document.querySelector('#deck .card.nudging, #deck .card.nudging-l'), null, { timeout: 6000 });
  const d = await p.locator('#deck').boundingBox();
  await p.mouse.move(d.x + d.width / 2, d.y + d.height / 2); await p.mouse.down();
  for (let i = 1; i <= 10; i++) { await p.mouse.move(d.x + d.width / 2 + i * 22, d.y + d.height / 2); await sleep(16); }
  await p.mouse.up();
  await sleep(2600);
  const st = await p.evaluate(() => { const c = document.querySelector('#deck .card[data-fn="1"]'); return { piled: c.classList.contains('piled'), tf: c.style.transform, hint: document.getElementById('hint').textContent }; });
  log('swipe after drag mid-nudge:', JSON.stringify(st));
  await p.screenshot({ path: join(OUT, '20-swipe-dealt.png') });
  // finish the deal, see the desk
  await p.click('#bSkip'); await sleep(1500 + 1500 + 3000);
  const cab = await p.evaluate(() => { const r = [...document.querySelectorAll('#cables .cable')]; return { n: r.length, sw: r.length ? getComputedStyle(r[0].querySelector('.rope')).strokeWidth : null, stroke: r.length ? getComputedStyle(r[0].querySelector('.rope')).stroke : null }; });
  log('cables', JSON.stringify(cab));
  await p.evaluate(() => document.getElementById('desk').scrollIntoView({ block: 'start' })); await sleep(900);
  await p.screenshot({ path: join(OUT, '21-desk.png') });
  await p.evaluate(() => document.getElementById('reveal').scrollIntoView({ block: 'center' })); await sleep(1200);
  await p.screenshot({ path: join(OUT, '22-finale.png') });
  await p.evaluate(() => document.getElementById('halfday-home').scrollIntoView({ block: 'start' })); await sleep(1200);
  await p.screenshot({ path: join(OUT, '23-halfday.png') });
  await p.context().close();
}

/* ---------------- 5. workshop: the star breaks ---------------- */
{
  const p = await page();
  await p.goto(BASE + '/workshop/', { waitUntil: 'load' }); await sleep(600);
  await p.evaluate(() => document.querySelector('[data-vis=break]').scrollIntoView({ block: 'center' })); await sleep(2800);
  await p.screenshot({ path: join(OUT, '30-break.png') });
  await p.context().close();
}

/* ---------------- 6. phone: scene inert, everything stacked ---------------- */
{
  const p = await page({ width: 390, height: 844 });
  await p.goto(BASE + '/', { waitUntil: 'load' }); await sleep(900);
  const live = await p.evaluate(() => document.getElementById('scene').classList.contains('live'));
  log('phone scene live =', live);
  await p.evaluate(() => document.getElementById('breaks').scrollIntoView()); await sleep(900);
  await p.screenshot({ path: join(OUT, '40-phone-breaks.png') });
  await p.context().close();
}

log('console errors:', errors.length, errors.slice(0, 5));
await browser.close();
