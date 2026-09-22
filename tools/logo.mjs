import { chromium } from 'playwright';
import { readFileSync, writeFileSync } from 'fs';
const svg = readFileSync('C:/Users/david/Vault/Business/Startup/kadabra/logo/kadabra-third-edition.svg', 'utf8');
const b = await chromium.launch(); const p = await b.newPage();
await p.setContent('<html><body style="margin:0">' + svg.replace(/<\?xml[^>]*>|<!DOCTYPE[^>]*>/g, '') + '</body></html>');
const r = await p.evaluate(() => {
  const root = document.querySelector('svg');
  const all = root.getBBox();
  const mark = document.getElementById('Logo').getBBox();
  const paths = [...root.querySelectorAll('path')].map(x => ({ id: x.id, d: x.getAttribute('d'), style: x.getAttribute('style') || '', parent: x.parentElement.id }));
  return { all: [all.x, all.y, all.width, all.height], mark: [mark.x, mark.y, mark.width, mark.height], paths };
});
await b.close();
const f = n => (+n).toFixed(2);
const pad = 2;
const vbFull = `${f(r.all[0]-pad)} ${f(r.all[1]-pad)} ${f(r.all[2]+2*pad)} ${f(r.all[3]+2*pad)}`;
const vbMark = `${f(r.mark[0]-pad)} ${f(r.mark[1]-pad)} ${f(r.mark[2]+2*pad)} ${f(r.mark[3]+2*pad)}`;
const fr = s => /evenodd/.test(s) ? 'evenodd' : 'nonzero';
const full = `<symbol id="logo-full" viewBox="${vbFull}"><title>kadabra</title>` +
  r.paths.map(x => `<path d="${x.d}" fill="currentColor" fill-rule="${fr(x.style)}"/>`).join('') + '</symbol>';
const m = r.paths.find(x => x.id === 'Logo');
const mark = `<symbol id="logo-mark" viewBox="${vbMark}"><title>kadabra mark</title><path d="${m.d}" fill="currentColor" fill-rule="${fr(m.style)}"/></symbol>`;
let sp = readFileSync('../sprites.svg', 'utf8');
sp = sp.replace(/<symbol id="logo-full"[\s\S]*?<\/symbol>/, full).replace(/<symbol id="logo-mark"[\s\S]*?<\/symbol>/, mark);
writeFileSync('../sprites.svg', sp);
console.log('full', vbFull, 'mark', vbMark, 'paths', r.paths.length, r.paths.map(x=>x.id+'@'+x.parent).join(' '));
