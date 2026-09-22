import { chromium } from 'playwright';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const shotDir = path.join(__dirname, 'shots', 'r10');

const errors = [];

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
page.on('console', (msg) => { if (msg.type() === 'error') errors.push('console: ' + msg.text()); });
page.on('pageerror', (err) => errors.push('pageerror: ' + err.message));

await page.goto('http://127.0.0.1:4174/', { waitUntil: 'networkidle' });

// ---------- WHY-US: hover, height, clipping ----------
await page.locator('#why').scrollIntoViewIfNeeded();
await page.waitForTimeout(300);
await page.screenshot({ path: path.join(shotDir, 'why-rest.png') });

const bands = page.locator('.whyband');
const second = bands.nth(1);
const restBox = await second.boundingBox();

await second.hover();
await page.waitForTimeout(900);
await page.screenshot({ path: path.join(shotDir, 'why-hover.png') });

const hoverBox = await second.boundingBox();
const suitBox = await second.locator('svg.suit').boundingBox();

console.log('WHY-US ----------------------------------------');
console.log('suit bbox during hover:', JSON.stringify(suitBox));
console.log('suit left edge >= 0 (on screen):', suitBox.x >= 0);
console.log('band height rest:', restBox.height, ' hover:', hoverBox.height, ' equal:', Math.abs(restBox.height - hoverBox.height) < 0.5);

// click then move away: must not stay open
await second.click();
await page.mouse.move(5, 5);
await page.waitForTimeout(900);
const suitTransform = await second.locator('svg.suit').evaluate((el) => getComputedStyle(el).transform);
console.log('suit transform after click+move-away (must be none/identity):', suitTransform);

// ---------- HALF-DAY ----------
await page.locator('#halfday-home').scrollIntoViewIfNeeded();
await page.waitForTimeout(600);
await page.screenshot({ path: path.join(shotDir, 'halfday.png') });

const btn = page.locator('#halfday-home .btn.go.arrow.light');
const btnBox = await btn.boundingBox();
const btnStyle = await btn.evaluate((el) => {
  const cs = getComputedStyle(el);
  return { fontSize: cs.fontSize, backgroundColor: cs.backgroundColor };
});
console.log('HALFDAY ---------------------------------------');
console.log('button font-size:', btnStyle.fontSize, ' background-color:', btnStyle.backgroundColor);
console.log('button bbox:', JSON.stringify(btnBox));

const hcueStyle = await page.locator('#halfday-home .hcue').evaluate((el) => {
  const cs = getComputedStyle(el);
  return { fontSize: cs.fontSize, color: cs.color };
});
console.log('hcue font-size:', hcueStyle.fontSize, ' color:', hcueStyle.color);

// ---------- FOOTER ----------
await page.locator('footer').scrollIntoViewIfNeeded();
await page.waitForTimeout(400);
await page.screenshot({ path: path.join(shotDir, 'footer.png') });

const logoHeight = await page.locator('.footbrand svg').evaluate((el) => getComputedStyle(el).height);
console.log('FOOTER ----------------------------------------');
console.log('footer logo height:', logoHeight);

// noise grain presence
const hdrGrain = await page.locator('.hdr').evaluate((el) => {
  const cs = getComputedStyle(el, '::before');
  return { bg: cs.backgroundImage.slice(0, 40), opacity: cs.opacity, zIndex: cs.zIndex, pointerEvents: cs.pointerEvents };
});
console.log('NOISE -----------------------------------------');
console.log('.hdr::before background-image (truncated):', hdrGrain.bg, ' opacity:', hdrGrain.opacity, ' z-index:', hdrGrain.zIndex, ' pointer-events:', hdrGrain.pointerEvents);

const footerLinkCheck = await page.evaluate(() => {
  const a = document.querySelector('footer a');
  const r = a.getBoundingClientRect();
  const el = document.elementFromPoint(r.x + r.width / 2, r.y + r.height / 2);
  return { linkText: a.textContent.trim(), hitIsLinkOrDescendant: el === a || a.contains(el), hitTag: el ? el.tagName : null };
});
console.log('footer link clickable check:', JSON.stringify(footerLinkCheck));

console.log('ERRORS ------------------------------------------');
console.log(errors.length ? errors.join('\n') : '(none)');

await browser.close();
