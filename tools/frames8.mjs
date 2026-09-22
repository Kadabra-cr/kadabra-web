import { chromium } from 'playwright';
const b = await chromium.launch(); const p = await b.newPage({viewport:{width:1440,height:900}});
const errs=[]; p.on('pageerror',e=>errs.push(e.message)); p.on('console',m=>{if(m.type()==='error')errs.push(m.text())});
let n=0; const shot=async(tag)=>{await p.screenshot({path:`shots/j${String(n++).padStart(2,'0')}-${tag}.png`});};
await p.goto('http://127.0.0.1:4173/',{waitUntil:'networkidle'}); await p.waitForTimeout(1600);
// feed the heart at a crowded spot for 3s
await p.mouse.move(280,740); for(let i=0;i<9;i++){await p.mouse.move(280+(i%2)*4,740); await p.waitForTimeout(330);} await shot('heart-fed');
const mass = await p.evaluate(()=>document.querySelectorAll('#field g').length);
// quick move away: heart should lag then come apart
await p.mouse.move(900,200,{steps:6}); await p.waitForTimeout(250); await shot('heart-lag'); await p.waitForTimeout(700); await shot('heart-breaking'); await p.waitForTimeout(1400); await shot('heart-gone');
// graph timing: 0.4s, 1.0s, 2.0s after entering
const vz=await p.$('#viz'); await vz.scrollIntoViewIfNeeded(); await p.waitForTimeout(400); await shot('viz-04'); await p.waitForTimeout(700); await shot('viz-11'); await p.waitForTimeout(1200); await shot('viz-23');
const bb=await (await p.$('#barA')).boundingBox(); await p.mouse.move(bb.x+bb.width*0.5, bb.y+bb.height*0.5); await p.waitForTimeout(400); await shot('viz-hover-squares');
const ds=await (await p.$('.delta svg')).boundingBox(); await p.mouse.move(ds.x+ds.width/2+10, ds.y+ds.height/2+10); await p.waitForTimeout(400); await shot('viz-hover-bigspade');
// nudge both sides
const sw=await p.$('#swipe'); await sw.scrollIntoViewIfNeeded(); await p.evaluate(()=>scrollBy(0,-40)); await p.mouse.move(10,10); await p.waitForTimeout(2900); await shot('nudge-1'); await p.waitForTimeout(3600); await shot('nudge-2');
for(const id of ['#bRight','#bLeft','#bRight','#bLeft','#bRight']){await p.click(id);await p.waitForTimeout(650);}
await p.waitForTimeout(2200); await shot('desk-turning'); await p.waitForTimeout(2600); await p.evaluate(()=>scrollBy(0,300)); await p.waitForTimeout(500); await shot('desk-landscape');
await p.evaluate(()=>document.getElementById('bAgain').scrollIntoView()); await p.waitForTimeout(300); await p.click('#bAgain'); await p.waitForTimeout(500); await shot('again-mid'); await p.waitForTimeout(1600); await shot('again-end');
console.log('errors',errs); await b.close();
