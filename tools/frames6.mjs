import { chromium } from 'playwright';
const b = await chromium.launch(); const p = await b.newPage({viewport:{width:1440,height:900}});
const errs=[]; p.on('pageerror',e=>errs.push(e.message)); p.on('console',m=>{if(m.type()==='error')errs.push(m.text())});
let n=0; const shot=async(tag)=>{await p.screenshot({path:`shots/h${String(n++).padStart(2,'0')}-${tag}.png`});};
await p.goto('http://127.0.0.1:4173/',{waitUntil:'networkidle'}); await p.waitForTimeout(2000);
await shot('header');
// heart: hold the pointer still over a crowded spot for 3s
await p.mouse.move(300,720); await p.waitForTimeout(300); for(let i=0;i<8;i++){await p.mouse.move(300+i*3,720); await p.waitForTimeout(350);} await shot('heart-3s');
await p.mouse.move(1200,120); await p.waitForTimeout(900); await shot('heart-release');
const vz=await p.$('#viz'); await vz.scrollIntoViewIfNeeded(); await p.waitForTimeout(4600); const vb=await (await p.$('#barB')).boundingBox(); await p.mouse.move(vb.x+vb.width*0.5, vb.y+vb.height*0.5); await p.waitForTimeout(400); await shot('viz-hover');
const sw=await p.$('#swipe'); await sw.scrollIntoViewIfNeeded(); await p.evaluate(()=>scrollBy(0,-40)); await p.waitForTimeout(800);
for(const id of ['#bRight','#bLeft','#bRight','#bLeft','#bRight']){await p.click(id);await p.waitForTimeout(650);}
await p.waitForTimeout(4400); await shot('desk-top'); await p.evaluate(()=>scrollBy(0,700)); await p.waitForTimeout(500); await shot('desk-mid');
const rb=await (await p.$('.row:nth-child(2) .note')).boundingBox(); await p.mouse.move(rb.x+40, rb.y+40); await p.waitForTimeout(400); await shot('desk-hot');
await p.evaluate(()=>scrollBy(0,700)); await p.waitForTimeout(400); await shot('desk-end');
const w=await p.$('.whyband:nth-child(2)'); await w.scrollIntoViewIfNeeded(); await p.evaluate(()=>scrollBy(0,-200)); await p.waitForTimeout(1500); const hb=await w.boundingBox(); await p.mouse.move(hb.x+400,hb.y+hb.height/2); await p.waitForTimeout(250); await shot('why-250ms'); await p.waitForTimeout(900); await shot('why-settled');
await p.mouse.move(hb.x+400,hb.y-300); await p.waitForTimeout(400); await shot('why-leave-400');
await p.evaluate(()=>scrollTo(0,document.body.scrollHeight)); await p.waitForTimeout(800); await shot('footer');
console.log('errors',errs); await b.close();
