import { chromium, devices } from 'playwright';
const sleep = ms => new Promise(r => setTimeout(r, ms));
const b = await chromium.launch();
const d = await b.newPage({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 2 });
await d.goto('http://127.0.0.1:4173/'); await sleep(800);
await d.screenshot({ path: 'tools/shots/r16/logo-hdr.png', clip: { x: 0, y: 0, width: 520, height: 72 } });
await d.evaluate(() => document.querySelector('footer').scrollIntoView()); await sleep(500);
const fb = await d.locator('footer .logo, footer svg').first().boundingBox();
await d.screenshot({ path: 'tools/shots/r16/logo-foot.png', clip: { x: fb.x - 10, y: fb.y - 10, width: fb.width + 20, height: fb.height + 20 } });
await d.setViewportSize({ width: 200, height: 240 }); await d.setContent('<body style="margin:0;background:#1c1a17"><img src="http://127.0.0.1:4173/favicon.svg" style="width:180px;margin:10px"></body>'); await sleep(400);

await d.screenshot({ path: 'tools/shots/r16/logo-fav.png' });
const m = await (await b.newContext({ viewport: { width: 320, height: 640 }, isMobile: true, deviceScaleFactor: 3 })).newPage();
await m.goto('http://127.0.0.1:4173/'); await sleep(600);
await m.screenshot({ path: 'tools/shots/r16/logo-320.png', clip: { x: 0, y: 0, width: 320, height: 72 } });
await b.close();
