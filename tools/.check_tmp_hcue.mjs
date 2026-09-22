import { chromium } from 'playwright';
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
await page.goto('http://127.0.0.1:4174/', { waitUntil: 'networkidle' });
await page.locator('#hstage-home').scrollIntoViewIfNeeded();
await page.waitForTimeout(300);
// scroll down within the pinned stage to push --e toward 1
for (let i=0;i<6;i++){ await page.mouse.wheel(0, 400); await page.waitForTimeout(200); }
await page.waitForTimeout(500);
const e = await page.locator('.hstage').evaluate(el => getComputedStyle(el).getPropertyValue('--e'));
console.log('--e:', e);
const hcue = await page.locator('#halfday-home .hcue').evaluate(el => {
  const cs = getComputedStyle(el);
  return {opacity: cs.opacity, display: cs.display, color: cs.color, fontSize: cs.fontSize};
});
console.log('hcue:', JSON.stringify(hcue));
await page.screenshot({ path: 'shots/r10/halfday-pinned.png' });
await browser.close();
