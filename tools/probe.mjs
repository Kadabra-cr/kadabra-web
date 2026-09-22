import { chromium } from 'playwright';
const b = await chromium.launch(); const p = await b.newPage({viewport:{width:1440,height:900}});
await p.goto('http://127.0.0.1:4173/',{waitUntil:'networkidle'}); await p.waitForTimeout(2500);
const r = await p.evaluate(()=>new Promise(res=>{const gs=[...document.querySelectorAll('#field g')];let prev=gs.map(g=>+g.getAttribute('opacity')),worst=[];let n=0;
 function f(){const cur=gs.map(g=>+g.getAttribute('opacity'));cur.forEach((o,k)=>{const j=Math.abs(o-prev[k]);if(j>.08)worst.push({k,from:prev[k],to:o,frame:n})});prev=cur;if(++n<240)requestAnimationFrame(f);else res(worst.slice(0,10));}
 requestAnimationFrame(f);}));
console.log(JSON.stringify(r));
// with pointer
p.mouse.move(400,700); const r2 = await p.evaluate(()=>new Promise(res=>{const gs=[...document.querySelectorAll('#field g')];let prev=gs.map(g=>+g.getAttribute('opacity')),worst=[];let n=0;
 function f(){const cur=gs.map(g=>+g.getAttribute('opacity'));cur.forEach((o,k)=>{const j=Math.abs(o-prev[k]);if(j>.08)worst.push({k,from:prev[k],to:o,frame:n})});prev=cur;if(++n<240)requestAnimationFrame(f);else res(worst.slice(0,10));}
 requestAnimationFrame(f);}));
for(let i=0;i<40;i++){await p.mouse.move(400+i*20,700-i*8);await p.waitForTimeout(30);}
console.log(JSON.stringify(r2));
await b.close();
