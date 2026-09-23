/* LinkedIn banners: brand/linkedin/copy.md + banners.html -> brand/linkedin/export/*.png
   Run from the project root: node tools/linkedin.mjs */
import { chromium } from 'playwright';
import { readFileSync, writeFileSync, mkdirSync } from 'fs';
import { tmpdir } from 'os';
import { join, resolve } from 'path';
import { pathToFileURL } from 'url';
const ROOT = resolve(import.meta.dirname, '..'), DIR = join(ROOT, 'brand', 'linkedin'), OUT = join(DIR, 'export');
const copy = {};
for (const line of readFileSync(join(DIR, 'copy.md'), 'utf8').split(/\r?\n/)) {
  const m = line.match(/^([a-z][a-z0-9.]*):\s*(.*)$/i);
  if (m) copy[m[1]] = m[2].trim();
}
const paths = JSON.parse(readFileSync(join(ROOT, 'src', 'suits-square-morph.json'), 'utf8')).paths;
const sprites = readFileSync(join(ROOT, 'site', 'sprites.svg'), 'utf8').replace(/<\?xml[^>]*>/, '');
const html = readFileSync(join(DIR, 'banners.html'), 'utf8')
  .replace('@@SPRITES@@', () => sprites).replace('@@COPY@@', () => JSON.stringify(copy)).replace('@@PATHS@@', () => JSON.stringify(paths));
const page = join(tmpdir(), 'kadabra-linkedin.html');
writeFileSync(page, html);
mkdirSync(OUT, { recursive: true });
const only = process.argv[2];
const jobs = [];
for (const [d, name] of [['carta', '1-carta'], ['humo', '2-sin-humo'], ['datos', '3-93-9']])
  for (const [s, w, h] of [['perfil', 1584, 396], ['empresa', 1128, 191]]) jobs.push({ d, s, w, h, scale: 2, file: `${name}_${s}_${w}x${h}@2x.png` });
jobs.push({ d: 'carta', s: 'avatar', w: 1080, h: 1080, scale: 1, file: 'perfil-icono-carbon_1080.png' });
jobs.push({ d: 'carta', s: 'avatar', w: 1080, h: 1080, scale: 400 / 1080, file: 'perfil-icono-carbon_400.png' });
const b = await chromium.launch();
for (const j of jobs) {
  if (only && !j.file.includes(only)) continue;
  const p = await b.newPage({ viewport: { width: j.w, height: j.h }, deviceScaleFactor: j.scale });
  const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto(pathToFileURL(page).href + `?d=${j.d}&s=${j.s}`);
  await p.waitForSelector('body[data-ready="1"]', { timeout: 20000 });
  await p.waitForTimeout(250);
  try { await p.locator('.art').screenshot({ path: join(OUT, j.file) }); console.log(errs.length ? 'ERR ' + errs : 'ok', j.file); }
  catch (e) { console.log('SKIPPED (file open elsewhere?)', j.file); }
  await p.close();
}
await b.close();
