/* kadabra site checks.
   1. serve the site:   cd site && python -m http.server 4173 --bind 127.0.0.1
   2. playwright:       site/.check/node_modules is a junction to
                        mistral-study/prototypes/node_modules. Recreate with
                        New-Item -ItemType Junction -Path site\.check
ode_modules
                          -Target mistral-study\prototypes
ode_modules
                        (or `pnpm add -D playwright` in site/.check).
   3. run:              cd site/.check && BASE=http://127.0.0.1:4173 node shots.mjs
   Screenshots land in site/.check/shots/, the report is printed. */
import { chromium } from 'playwright';
import { mkdirSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const HERE = dirname(fileURLToPath(import.meta.url));
const SHOTS = join(HERE, 'shots');
mkdirSync(SHOTS, { recursive: true });
const BASE = process.env.BASE || 'http://localhost:4173';
const ROUTES = [['/', 'home'], ['/workshop/', 'workshop'], ['/learn-more/', 'sources']];
const DESK = { width: 1440, height: 900 };
const PHONE = { width: 390, height: 844 };

const results = [];
const ok = (n, pass, detail) => { results.push({ n, pass, detail }); console.log(`${pass ? 'PASS' : 'FAIL'}  ${n}  ${detail}`); };
const sleep = (ms) => new Promise(r => setTimeout(r, ms));

async function sweepScroll(page) {
  await page.evaluate(async () => {
    const h = document.body.scrollHeight;
    for (let y = 0; y < h; y += Math.round(innerHeight * 0.7)) {
      window.scrollTo(0, y);
      await new Promise(r => setTimeout(r, 140));
    }
    window.scrollTo(0, 0);
    await new Promise(r => setTimeout(r, 400));
  });
}

const browser = await chromium.launch();

/* ---------------------------------------------------------------- 3. console */
const consoleErrors = [];
async function newPage(viewport, opts = {}) {
  const ctx = await browser.newContext({ viewport, ...opts });
  const page = await ctx.newPage();
  page.on('console', m => { if (m.type() === 'error') consoleErrors.push(m.text()); });
  page.on('pageerror', e => consoleErrors.push('pageerror: ' + e.message));
  page.on('requestfailed', r => { if (r.url().startsWith(BASE)) consoleErrors.push('requestfailed: ' + r.url()); });
  return page;
}

/* ------------------------------------------------- 1. screenshots, both sizes */
for (const [route, name] of ROUTES) {
  for (const [vp, tag] of [[DESK, '1440'], [PHONE, '390']]) {
    const page = await newPage(vp);
    await page.goto(BASE + route, { waitUntil: 'load' });
    await sleep(700);
    await sweepScroll(page);
    await page.screenshot({ path: join(SHOTS, `${name}-${tag}.png`), fullPage: true });
    await page.context().close();
  }
}
ok('1 screenshots', true, `${ROUTES.length * 2} files in .check/shots/`);

/* ------------------------------------------------------ 2. gutter audit @1440 */
{
  const violations = [];
  let minLeft = 1e9, maxRight = -1e9, vw = 0;
  for (const [route, name] of ROUTES) {
    const page = await newPage(DESK);
    await page.goto(BASE + route, { waitUntil: 'load' });
    await sleep(500);
    await sweepScroll(page);
    const r = await page.evaluate(() => {
      const w = document.documentElement.clientWidth;
      const sel = 'h1,h2,h3,h4,p,li,a,button,kbd,b,span.fig,.card,.mini,.note,.cta';
      const bad = [];
      let lo = 1e9, hi = -1e9;
      for (const el of document.querySelectorAll(sel)) {
        if (el.closest('[aria-hidden="true"]') || el.getAttribute('aria-hidden') === 'true') continue;
        if (el.classList.contains('sr')) continue;
        const cs = getComputedStyle(el);
        if (cs.display === 'none' || cs.visibility === 'hidden' || +cs.opacity === 0) continue;
        const b = el.getBoundingClientRect();
        if (b.width < 1 || b.height < 1) continue;
        if (!el.textContent.trim() && el.tagName !== 'BUTTON' && el.tagName !== 'A') continue;
        lo = Math.min(lo, b.left); hi = Math.max(hi, b.right);
        if (b.left < 95 || b.right > w - 95) {
          bad.push({ tag: el.tagName, cls: el.className.toString().slice(0, 40), left: Math.round(b.left), right: Math.round(b.right) });
        }
      }
      return { w, lo, hi, bad: bad.slice(0, 8), n: bad.length };
    });
    vw = r.w; minLeft = Math.min(minLeft, r.lo); maxRight = Math.max(maxRight, r.hi);
    if (r.n) violations.push({ route: name, n: r.n, sample: r.bad });
    await page.context().close();
  }
  ok('2 gutters @1440', violations.length === 0,
    `viewport ${vw}px, min left ${minLeft.toFixed(1)}px, max right ${maxRight.toFixed(1)}px (limit ${(vw - 95).toFixed(0)}), violations ${violations.length}` +
    (violations.length ? ' ' + JSON.stringify(violations) : ''));
}

/* --------------------------------------------------------- 3. duplicate ids */
{
  const dupAll = [];
  for (const [route, name] of ROUTES) {
    const page = await newPage(DESK);
    await page.goto(BASE + route, { waitUntil: 'load' });
    await sleep(400);
    const d = await page.evaluate(() => {
      const seen = new Map();
      for (const el of document.querySelectorAll('[id]')) seen.set(el.id, (seen.get(el.id) || 0) + 1);
      return [...seen].filter(([, c]) => c > 1).map(([i, c]) => `${i} x${c}`);
    });
    if (d.length) dupAll.push(name + ': ' + d.join(', '));
    await page.context().close();
  }
  ok('3a duplicate ids', dupAll.length === 0, dupAll.length ? dupAll.join(' | ') : 'none on any route');
}

/* ------------------------------------------- 4. hero pointer + opacity ramp */
{
  const page = await newPage(DESK);
  await page.goto(BASE + '/', { waitUntil: 'load' });
  await sleep(700);
  const box = await page.locator('#field').boundingBox();
  for (let i = 0; i <= 24; i++) {
    await page.mouse.move(box.x + 120 + (box.width - 260) * (i / 24), box.y + box.height * (0.28 + 0.16 * Math.sin(i / 3)));
    await sleep(28);
  }
  await page.screenshot({ path: join(SHOTS, 'hero-trail-1440.png') });

  const samples = await page.evaluate(async () => {
    const gs = [...document.querySelectorAll('#field > g')];
    const out = [];
    for (let k = 0; k < 60; k++) {
      out.push(gs.map(g => +g.getAttribute('opacity')));
      await new Promise(r => setTimeout(r, 50));
    }
    return out;
  });
  let maxJump = 0, where = '';
  for (let k = 1; k < samples.length; k++) {
    for (let i = 0; i < samples[k].length; i++) {
      const d = Math.abs(samples[k][i] - samples[k - 1][i]);
      if (d > maxJump) { maxJump = d; where = `mark ${i} at sample ${k}`; }
    }
  }
  ok('4 hero pointer + no flash', maxJump < 0.15,
    `max opacity jump per 50 ms = ${maxJump.toFixed(4)} (${where || 'n/a'}), ${samples[0].length} marks`);
  await page.context().close();
}

/* --------------------------------------------------------- 5. swipe + cables */
{
  const page = await newPage(DESK);
  await page.goto(BASE + '/', { waitUntil: 'load' });
  await sleep(400);
  await page.locator('#deck').scrollIntoViewIfNeeded();
  await sleep(1200);
  await page.locator('#deck').focus();
  for (const k of ['ArrowRight', 'ArrowRight', 'ArrowRight', 'ArrowLeft', 'ArrowLeft']) {
    await page.keyboard.press(k);
    await sleep(700);
  }
  await sleep(8200);
  const cables = await page.locator('#cables .cable').count();
  const wired = await page.evaluate(() => new Set([...document.querySelectorAll('#cables .cable')].map(c => c.dataset.fn)).size);
  const notes = await page.locator('#rows .note').count();
  await page.locator('#desk').scrollIntoViewIfNeeded();
  await sleep(400);
  await page.screenshot({ path: join(SHOTS, 'swipe-reveal-1440.png'), fullPage: true });
  ok('5a swipe reveal', wired === 5 && cables === 5 && notes === 5,
    `${wired} hanging cables (${cables} rope groups), ${notes} notes`);

  await page.locator('#bAgain').click();
  await sleep(1200);
  const back = await page.locator('#deck .card').count();
  const revealHidden = await page.locator('#reveal').isHidden();
  await page.screenshot({ path: join(SHOTS, 'swipe-dealagain-1440.png'), fullPage: true });
  ok('5b deal again', back === 5 && revealHidden, `${back} cards restacked, reveal hidden ${revealHidden}`);
  await page.context().close();
}

/* ----------------------------------------------------- 6. why-us: no snap back */
{
  const page = await newPage(DESK);
  await page.goto(BASE + '/', { waitUntil: 'load' });
  await sleep(400);
  const band = page.locator('.whyband').first();
  await band.scrollIntoViewIfNeeded();
  await sleep(1800);                       /* the entry morph finishes */
  await band.hover();
  const trace = await page.evaluate(async () => {
    const p = document.querySelector('.whyband .suit path');
    const out = [];
    for (let k = 0; k < 30; k++) {
      out.push({ d: p.getAttribute('d'), o: +getComputedStyle(p.closest('svg')).opacity });
      await new Promise(r => setTimeout(r, 50));
    }
    return out;
  });
  const nums = s => (s.match(/-?[\d.]+/g) || []).map(Number);
  let maxShift = 0;
  for (let k = 1; k < trace.length; k++) {
    const a = nums(trace[k - 1].d), b = nums(trace[k].d);
    if (a.length !== b.length) { maxShift = 999; break; }
    for (let i = 0; i < a.length; i++) maxShift = Math.max(maxShift, Math.abs(a[i] - b[i]));
  }
  const first = nums(trace[0].d), last = nums(trace[trace.length - 1].d);
  const drift = Math.max(...first.map((v, i) => Math.abs(v - last[i])));
  ok('6 why-us never resets', maxShift < 0.6 && drift < 0.6,
    `max path move between 50 ms samples = ${maxShift.toFixed(3)}, start-to-end drift = ${drift.toFixed(3)}`);
  await page.screenshot({ path: join(SHOTS, 'whyus-hover-1440.png') });
  await page.context().close();
}

/* --------------------------------------------------------------- 7. routing */
{
  const page = await newPage(DESK);
  await page.goto(BASE + '/', { waitUntil: 'load' });
  await sleep(400);
  await page.evaluate(() => { window.__alive = 1; });
  await page.click('a[href="/workshop/"]');
  await sleep(700);
  const a = await page.evaluate(() => ({ url: location.pathname, title: document.title, alive: window.__alive, vis: document.querySelector('.route:not([hidden])').dataset.route }));
  await page.goBack();
  await sleep(700);
  const b = await page.evaluate(() => ({ url: location.pathname, title: document.title, alive: window.__alive, vis: document.querySelector('.route:not([hidden])').dataset.route }));
  ok('7a spa nav', a.url === '/workshop/' && a.alive === 1 && /taller/i.test(a.title) && a.vis === '/workshop/',
    `-> ${a.url} "${a.title}" alive=${a.alive} shown=${a.vis}`);
  ok('7b back', b.url === '/' && b.alive === 1 && b.vis === '/', `back to ${b.url} shown=${b.vis} alive=${b.alive}`);

  for (const [route, name] of [['/workshop/', 'Inteligencia Artificial sin humo'], ['/learn-more/', 'El truco, y de dónde lo sacamos.']]) {
    await page.goto(BASE + route, { waitUntil: 'load' });
    await sleep(400);
    const r = await page.evaluate(() => ({ vis: document.querySelector('.route:not([hidden])').dataset.route, h2: document.querySelector('.route:not([hidden]) h2').textContent.trim(), title: document.title }));
    ok('7c direct ' + route, r.vis === route && r.h2.includes(name), `shown=${r.vis} h2="${r.h2}"`);
  }
  await page.context().close();
}

/* ------------------------------------------- 9. chevron rule, 2x zoom shots */
{
  const ctx = await browser.newContext({ viewport: DESK, deviceScaleFactor: 2 });
  const page = await ctx.newPage();
  page.on('pageerror', e => consoleErrors.push('pageerror: ' + e.message));
  await page.goto(BASE + '/', { waitUntil: 'load' });
  await sleep(400);
  await page.locator('#viz').scrollIntoViewIfNeeded();
  await sleep(1600);
  const u = await page.locator('#viz > .rule').boundingBox();
  await page.screenshot({ path: join(SHOTS, 'zoom-underline-2x.png'),
    clip: { x: u.x - 8, y: u.y - 46, width: u.width + 16, height: u.height + 60 } });
  await page.goto(BASE + '/workshop/', { waitUntil: 'load' });
  await sleep(400);
  await page.locator('.moment').nth(1).scrollIntoViewIfNeeded();
  await sleep(1400);
  const sp = await page.locator('#spineline').boundingBox();
  await page.screenshot({ path: join(SHOTS, 'zoom-spine-2x.png'),
    clip: { x: sp.x - 26, y: 60, width: 74, height: 620 } });
  const spine = await page.evaluate(() => {
    const line = document.getElementById('spineline'), mark = document.getElementById('spinemark');
    const dots = document.getElementById('spinedots');
    return { lineH: Math.round(line.getBoundingClientRect().height), dotsH: Math.round(dots.getBoundingClientRect().height),
             mark: !!mark && getComputedStyle(mark).display !== 'none', rt: getComputedStyle(line).width };
  });
  ok('9 continuous spine', spine.lineH > 2000 && spine.dotsH > 200 && spine.mark,
    `solid line ${spine.lineH}px, dotted tail ${spine.dotsH}px, marker present ${spine.mark}, thickness ${spine.rt}`);
  await ctx.close();
}

/* ---------------------------------------------------------- 8. reduced motion */
{
  const page = await newPage(DESK, { reducedMotion: 'reduce' });
  await page.goto(BASE + '/', { waitUntil: 'load' });
  await sleep(700);
  await sweepScroll(page);
  await page.screenshot({ path: join(SHOTS, 'home-reduced-1440.png'), fullPage: true });
  const still = await page.evaluate(async () => {
    const gs = [...document.querySelectorAll('#field > g')];
    const a = gs.map(g => g.getAttribute('transform'));
    await new Promise(r => setTimeout(r, 800));
    const b = gs.map(g => g.getAttribute('transform'));
    return { n: gs.length, moved: a.filter((v, i) => v !== b[i]).length };
  });
  ok('8 reduced motion', still.moved === 0 && still.n > 0, `${still.n} marks, ${still.moved} moved in 800 ms`);
  await page.context().close();
}

/* console errors, collected across every page above */
ok('3b console errors', consoleErrors.length === 0,
  consoleErrors.length ? consoleErrors.slice(0, 6).join(' | ') : '0 errors');

await browser.close();
const failed = results.filter(r => !r.pass);
console.log(`\n${results.length - failed.length}/${results.length} checks passed`);
process.exit(failed.length ? 1 : 0);
