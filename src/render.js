const puppeteer = require('puppeteer-core');
const path = require('path');
(async () => {
  const [,, htmlPath, outPath, mode] = process.argv;
  const browser = await puppeteer.launch({
    executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
    args: ['--no-sandbox','--disable-dev-shm-usage','--font-render-hinting=none'],
  });
  const page = await browser.newPage();
  await page.setViewport({width: 1100, height: 1400, deviceScaleFactor: 2});
  await page.goto('file://' + path.resolve(htmlPath), {waitUntil: 'networkidle0', timeout: 120000});
  try {
    await page.waitForFunction('window.MJDONE === true', {timeout: 90000});
    console.log('MathJax typeset complete');
  } catch (e) { console.log('WARN: MathJax flag not seen -', e.message); }
  await new Promise(r => setTimeout(r, 700));
  if (mode === 'png') {
    await page.screenshot({path: outPath, fullPage: true});
  } else {
    await page.pdf({
      path: outPath, format: 'A4', printBackground: true,
      margin: {top: '19mm', bottom: '20mm', left: '18mm', right: '18mm'},
      displayHeaderFooter: true,
      headerTemplate: '<div style="width:100%;font-family:Georgia,serif;font-size:7.5pt;color:#8a8a8a;padding:0 18mm;display:flex;justify-content:space-between;"><span>Graph Theory &mdash; Problem Set Solutions</span><span></span></div>',
      footerTemplate: '<div style="width:100%;font-family:Georgia,serif;font-size:8pt;color:#6b6b6b;padding:0 18mm;text-align:center;"><span class="pageNumber"></span> / <span class="totalPages"></span></div>',
    });
  }
  const n = await page.evaluate(() => document.body.scrollHeight);
  console.log('rendered', outPath, 'body height', n);
  await browser.close();
})();
