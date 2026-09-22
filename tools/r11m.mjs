import { chromium } from 'playwright';
const sleep = ms => new Promise(r => setTimeout(r, ms));
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: +(process.argv[2]||1440), height: +(process.argv[3]||900) } });
await p.goto('http://127.0.0.1:4173/'); await sleep(1000);
await p.evaluate(() => scrollTo(0, innerHeight * 1.2)); await sleep(800);
console.log(await p.evaluate(() => {
  const q = s => { const e = document.querySelector(s); const r = e.getBoundingClientRect(); return s + ' ' + Math.round(r.top) + '..' + Math.round(r.bottom) + ' h' + Math.round(r.height) + ' w' + Math.round(r.width); };
  return ['#morph .pin', '#morph .wrap', '#breaks .h2', '#policy', '#policy .vizgrid', '#pair', '#policy .bars', '#policy .story', '#polA'].map(q).join('\n');
}));
await b.close();
