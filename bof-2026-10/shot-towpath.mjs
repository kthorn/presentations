import { chromium } from 'playwright';
const browser = await chromium.launch({ executablePath: `${process.env.HOME}/.cache/ms-playwright/chromium-1234/chrome-linux64/chrome` });
const page = await browser.newPage({ viewport: { width: 1400, height: 1400 }, deviceScaleFactor: 2 });
await page.goto('https://towpath.thornlab.dev', { waitUntil: 'networkidle' });
await page.waitForTimeout(6000);
const map = page.locator('.gm-style').first();
await map.screenshot({ path: 'assets/towpath-map.png' });
console.log(await map.boundingBox());
await browser.close();
