import { chromium } from 'playwright';
const b = await chromium.launch(); const p = await b.newPage({viewport:{width:1440,height:900}});
const errs=[]; p.on('pageerror',e=>errs.push(e.message)); p.on('console',m=>{if(m.type()==='error')errs.push(m.text())});
let n=0; const shot=async(tag)=>{await p.screenshot({path:`shots/i${String(n++).padStart(2,'0')}-${tag}.png`});};
await p.goto('http://127.0.0.1:4173/',{waitUntil:'networkidle'}); await p.waitForTimeout(1500);
await p.screenshot({path:'shots/i00-header.png', clip:{x:80,y:0,width:260,height:64}}); n=1;
await p.mouse.move(300,720); for(let i=0;i<8;i++){await p.mouse.move(300+i*3,720); await p.waitForTimeout(350);} await p.mouse.move(1200,120); await p.waitForTimeout(900); await shot('heart-release');
const sw=await p.$('#swipe'); await sw.scrollIntoViewIfNeeded(); await p.evaluate(()=>scrollBy(0,-40)); await p.waitForTimeout(800);
for(const id of ['#bRight','#bLeft','#bRight','#bLeft','#bRight']){await p.click(id);await p.waitForTimeout(650);}
await p.waitForTimeout(4400); await p.evaluate(()=>scrollBy(0,330)); await p.waitForTimeout(600); await shot('desk-cables');
const rb=await (await p.$('.row:nth-child(2) .note')).boundingBox(); await p.mouse.move(rb.x+40, rb.y+40); await p.waitForTimeout(400); await shot('desk-hot');
const w=await p.$('.whyband:nth-child(2)'); await w.scrollIntoViewIfNeeded(); await p.evaluate(()=>scrollBy(0,-200)); await p.waitForTimeout(1500); const hb=await w.boundingBox(); await p.mouse.move(hb.x+400,hb.y+hb.height/2); await p.waitForTimeout(1100); await shot('why-settled');
await p.evaluate(()=>scrollTo(0,document.body.scrollHeight)); await p.waitForTimeout(800); await p.screenshot({path:'shots/i05-footer.png', clip:{x:80,y:520,width:400,height:200}});
console.log('errors',errs); await b.close();
