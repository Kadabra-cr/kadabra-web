import { chromium, devices } from 'playwright';
const sleep = ms => new Promise(r => setTimeout(r, ms));
const b = await chromium.launch();
for (const [ctx, n] of [[{ viewport: { width: 1440, height: 900 } }, 'dt'], [devices['iPhone 13'], 'ph']]) {
  const p = await (await b.newContext(ctx)).newPage();
  await p.goto('http://127.0.0.1:4173/'); await sleep(900);
  await p.evaluate(() => { const el = document.getElementById('morph'); scrollTo(0, el.getBoundingClientRect().top + scrollY + (innerWidth > 900 ? el.offsetHeight * .62 : 380)); });
  await sleep(2800);
  const r = await p.evaluate(() => ['polA', 'polB'].map(id => Math.round(document.getElementById(id).getBoundingClientRect().top)));
  console.log(n, 'bar tops', r);
  await p.screenshot({ path: `tools/shots/r19/pol-${n}.png` });
}
await b.close();
