import { chromium, devices } from 'playwright';
const sleep = ms => new Promise(r => setTimeout(r, ms));
const b = await chromium.launch();
const p = await (await b.newContext(devices['iPhone 13'])).newPage();
await p.goto('http://127.0.0.1:4173/workshop/'); await sleep(2500);
await p.screenshot({ path: 'tools/shots/r16/sm-0-load.png' });
await p.evaluate(() => document.querySelector('[data-vis=smoke] .m-vis').scrollIntoView({ block: 'center' }));
for (const [t, n] of [[200, 1], [900, 2], [1800, 3]]) { await sleep(t === 200 ? 200 : t - 200); await p.screenshot({ path: `tools/shots/r16/sm-${n}.png` }); }
await b.close();
