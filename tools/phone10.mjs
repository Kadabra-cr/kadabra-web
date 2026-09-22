import { chromium } from 'playwright';
const sleep = ms => new Promise(r => setTimeout(r, ms));
const b = await chromium.launch();
const m = await (await b.newContext({ viewport: { width: 390, height: 844 } })).newPage();
await m.goto('http://127.0.0.1:4173/', { waitUntil: 'load' }); await sleep(800);
await m.evaluate(() => document.getElementById('breaks').scrollIntoView()); await sleep(2200);
console.log('phone shows the 93/9 cards?', await m.evaluate(() => getComputedStyle(document.getElementById('pair')).display));
await m.screenshot({ path: 'shots/r10/p-phone-breaks.png' });
await b.close();
