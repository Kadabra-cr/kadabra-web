import { chromium } from 'playwright';
const b = await chromium.launch(); const p = await (await b.newContext({viewport:{width:1440,height:900}})).newPage();
await p.goto('http://127.0.0.1:4173/', {waitUntil:'load'}); await new Promise(r=>setTimeout(r,1800));
await p.screenshot({path:'shots/r8-hero-before.png'});
const m = await p.evaluate(()=>{const h=document.querySelector('.hdr').getBoundingClientRect();const l=document.querySelector('.brand svg').getBoundingClientRect();const n=document.querySelector('.nav a');const cs=getComputedStyle(n);const c=document.querySelector('.hdr .cta').getBoundingClientRect();const h1=document.querySelector('.hero h1').getBoundingClientRect();return {hdr:h.height,logo:[l.width,l.height],nav:cs.fontSize,navH:n.getBoundingClientRect().height,cta:[c.width,c.height],h1:[h1.width,h1.height,h1.top]}});
console.log(JSON.stringify(m)); await b.close();
