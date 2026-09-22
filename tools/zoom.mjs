import { chromium } from 'playwright';
const b = await chromium.launch(); const p = await b.newPage({viewport:{width:1440,height:900},deviceScaleFactor:2});
await p.goto('http://127.0.0.1:4173/',{waitUntil:'networkidle'});
const H = await p.evaluate(()=>document.body.scrollHeight);
for(let y=0;y<H;y+=450){await p.evaluate(v=>scrollTo(0,v),y);await p.waitForTimeout(150);}
const el = await p.$('.closer .rule'); await el.scrollIntoViewIfNeeded(); await p.waitForTimeout(1500);
const bb = await el.boundingBox(); await p.screenshot({path:'shots/zoom-underline.png',clip:{x:bb.x-10,y:bb.y-60,width:700,height:bb.height+80}});
await p.goto('http://127.0.0.1:4173/workshop/',{waitUntil:'networkidle'}); await p.evaluate(()=>scrollTo(0,1200)); await p.waitForTimeout(800);
await p.screenshot({path:'shots/zoom-spine.png',clip:{x:60,y:0,width:220,height:900}});
await p.evaluate(()=>scrollTo(0,document.body.scrollHeight-1600)); await p.waitForTimeout(800);
await p.screenshot({path:'shots/workshop-end.png'});
await p.goto('http://127.0.0.1:4173/',{waitUntil:'networkidle'});
const s = await p.$('#swipe, .swipe, section.swipe'); if(s){await s.scrollIntoViewIfNeeded(); await p.waitForTimeout(3000); await p.screenshot({path:'shots/swipe-idle.png'});}
for(const k of ['ArrowRight','ArrowRight','ArrowLeft','ArrowRight','ArrowLeft']){await p.keyboard.press(k);await p.waitForTimeout(700);}
await p.waitForTimeout(2500); await p.screenshot({path:'shots/reveal-zoom.png'});
await b.close();
