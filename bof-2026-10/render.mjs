// Render slide SVGs to PNG via headless Chromium.
//   node render.mjs slide3            -> slide3.png
//   node render.mjs --shot URL out.png [WxH] [waitMs]
import { chromium } from 'playwright';
import { readFileSync, writeFileSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const W = 1600, H = 900, SCALE = 2;

const fontFaces = ['Regular:400', 'Medium:500', 'SemiBold:600', 'Bold:700', 'ExtraBold:800']
  .map(s => s.split(':'))
  .map(([name, weight]) => `@font-face{font-family:Montserrat;font-weight:${weight};` +
    `src:url(${pathToFileURL(resolve(here, `fonts/Montserrat-${name}.ttf`))})}`)
  .join('\n');

const browser = await chromium.launch({
  executablePath: process.env.CHROME ?? `${process.env.HOME}/.cache/ms-playwright/chromium-1234/chrome-linux64/chrome`,
});
const args = process.argv.slice(2);

if (args[0] === '--shot') {
  const [, url, out, size = '1600x1000', wait = '4000'] = args;
  const [w, h] = size.split('x').map(Number);
  const page = await browser.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: SCALE });
  await page.goto(url, { waitUntil: 'networkidle' });
  await page.waitForTimeout(Number(wait));
  await page.screenshot({ path: resolve(here, out) });
} else {
  for (const name of args) {
    const svg = readFileSync(resolve(here, `${name}.svg`), 'utf8');
    const html = `<!doctype html><html><head><style>${fontFaces}
      html,body{margin:0;padding:0;width:${W}px;height:${H}px;overflow:hidden}</style></head>
      <body>${svg}</body></html>`;
    const page = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: SCALE });
    // Write next to the SVG so relative asset hrefs (assets/...) resolve.
    const tmp = resolve(here, `.${name}.html`);
    writeFileSync(tmp, html);
    await page.goto(pathToFileURL(tmp).href, { waitUntil: 'load' });
    await page.evaluate(() => document.fonts.ready);
    await page.screenshot({ path: resolve(here, `${name}.png`) });
    console.log(`${name}.png`);
  }
}
await browser.close();
