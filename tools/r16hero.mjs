import { chromium, devices } from 'playwright';
const sleep = ms => new Promise(r => setTimeout(r, ms));
const b = await chromium.launch();
for (const [d, n] of [[devices['iPhone 13'], 'ip'], [devices['Galaxy S9+'], 's9']]) {
  const p = await (await b.newContext({ ...d })).newPage();
  await p.goto('http://127.0.0.1:4173/'); await sleep(2600);
  await p.screenshot({ path: `tools/shots/r16/hero-${n}.png` });
}
await b.close();
