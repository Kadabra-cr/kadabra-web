import { chromium } from 'playwright';
const b = await chromium.launch(); const p = await b.newPage({viewport:{width:1440,height:900}});
const errs=[]; p.on('pageerror',e=>errs.push(e.message)); p.on('console',m=>{if(m.type()==='error')errs.push(m.text())});
await p.goto('http://127.0.0.1:4173/',{waitUntil:'networkidle'});
const sw = await p.$('#swipe, .swipe'); await sw.scrollIntoViewIfNeeded(); await p.waitForTimeout(800);
const names = await p.evaluate(()=>[...document.querySelectorAll('section button')].map(b=>b.id+':'+b.textContent.trim()).slice(0,8)); console.log(names);
for (const t of ['AI can take it','AI can take it','Best not','AI can take it','Best not']) { await p.click(`button:has-text("${t}")`); await p.waitForTimeout(650); }
await p.waitForTimeout(3200); await p.screenshot({path:'shots/ropes-settled.png'});
const r = await p.$('.desk'); const bb = await r.boundingBox();
await p.mouse.move(bb.x+bb.width*0.45, bb.y+bb.height*0.4); await p.waitForTimeout(300);
await p.mouse.down(); await p.mouse.move(bb.x+bb.width*0.5, bb.y+bb.height*0.75, {steps:12}); await p.waitForTimeout(100); await p.screenshot({path:'shots/ropes-drag.png'}); await p.mouse.up();
await p.waitForTimeout(1500); await p.screenshot({path:'shots/ropes-after.png'});
const w = await p.$('#why, .why'); if (w) { await w.scrollIntoViewIfNeeded(); await p.waitForTimeout(1500); const hb=await (await p.$('.whyband')).boundingBox(); const h0=await p.evaluate(()=>document.querySelector('.whyband').offsetHeight); await p.mouse.move(hb.x+200,hb.y+40); await p.waitForTimeout(800); const h1=await p.evaluate(()=>document.querySelector('.whyband').offsetHeight); console.log('whyband height idle/hover',h0,h1); await p.screenshot({path:'shots/why-hover.png'}); }
console.log('errors',errs); await b.close();
