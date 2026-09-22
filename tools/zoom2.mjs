import { chromium } from 'playwright';
const b = await chromium.launch(); const p = await b.newPage({viewport:{width:1440,height:900}});
const errs=[]; p.on('pageerror',e=>errs.push(e.message)); p.on('console',m=>{if(m.type()==='error')errs.push(m.text())});
await p.goto('http://127.0.0.1:4173/',{waitUntil:'networkidle'});
await p.waitForTimeout(150); await p.screenshot({path:'shots/hero-t0.png'});
await p.waitForTimeout(1800); await p.screenshot({path:'shots/hero-t2.png'});
// pointer sweep + opacity probe
let maxJ=0, prev=null;
for(let i=0;i<60;i++){ await p.mouse.move(300+i*12, 700-i*6); await p.waitForTimeout(50);
  const os = await p.evaluate(()=>[...document.querySelectorAll('#field g')].map(g=>+g.getAttribute('opacity')));
  if(prev) os.forEach((o,k)=>{maxJ=Math.max(maxJ,Math.abs(o-prev[k]))}); prev=os; }
await p.screenshot({path:'shots/hero-trail2.png'});
// overlap audit: any mark with opacity>0.25 whose centre lies inside a text rect?
const bad = await p.evaluate(()=>{const rs=[...document.querySelectorAll('.hero .wrap > *')].flatMap(e=>[...e.getClientRects()]);let n=0;
 document.querySelectorAll('#field g').forEach(g=>{const o=+g.getAttribute('opacity');if(o<.25)return;const r=g.getBoundingClientRect();const cx=r.x+r.width/2,cy=r.y+r.height/2;if(rs.some(t=>cx>t.left&&cx<t.right&&cy>t.top&&cy<t.bottom))n++});return n});
console.log('maxJump',maxJ.toFixed(3),'marksOnText',bad,'errors',errs);
const v = await p.$('#viz'); await v.scrollIntoViewIfNeeded(); await p.waitForTimeout(2500);
await p.screenshot({path:'shots/viz2.png'});
await b.close();
