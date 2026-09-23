import { chromium, devices } from 'playwright';
const sleep = ms => new Promise(r => setTimeout(r, ms));
const b = await chromium.launch();
for (const [ctxo, n] of [[devices['iPhone 13'], 'ip'], [{ viewport: { width: 1440, height: 900 } }, 'dt']]) {
  const p = await (await b.newContext(ctxo)).newPage();
  const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto('http://127.0.0.1:4173/workshop/'); await sleep(900);
  await p.evaluate(() => document.querySelector('[data-vis=smoke] .m-vis').scrollIntoView({ block: 'center' }));
  await sleep(300); await p.screenshot({ path: `tools/shots/r16/smoke-${n}-a.png` });
  await sleep(2600); await p.screenshot({ path: `tools/shots/r16/smoke-${n}-b.png` });
  // chevron: viewport position across the route
  const top = await p.evaluate(() => document.getElementById('moments').getBoundingClientRect().top + scrollY);
  const out = [];
  for (let y = top - 300; y < top + 5200; y += 350) {
    await p.evaluate(y => scrollTo(0, y), y); await sleep(60);
    out.push(await p.evaluate(() => Math.round(document.getElementById('spinemark').getBoundingClientRect().top) + (document.getElementById('spinemark').classList.contains('gold') ? 'g' : '')));
  }
  console.log(n, 'vh', await p.evaluate(() => innerHeight), 'chevron top by scroll:', out.join(' '), 'errors', errs);
}
await b.close();
