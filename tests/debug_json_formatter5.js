const puppeteer = require('puppeteer');
(async () => {
  const browser = await puppeteer.launch({headless: true, args: ['--no-sandbox']});
  const page = await browser.newPage();
  const jsErrors = [];
  page.on('pageerror', err => jsErrors.push(err.message));
  page.on('console', msg => console.log('CONSOLE:', msg.type(), msg.text()));
  
  await page.goto('file:///home/chison/tools-site/json-formatter/index.html', {waitUntil: 'load', timeout: 10000});
  await new Promise(r=>setTimeout(r,500));
  
  // Method 1: test's approach (click+type)
  const input = await page.$('textarea');
  await input.click({clickCount: 3});
  await input.type('{"a":1}');
  
  const valAfterType = await page.evaluate(() => document.querySelector('textarea').value);
  console.log('textarea value after type:', valAfterType);
  
  // Method A: click via evaluateHandle
  const btnA = await page.evaluateHandle((text) => {
    const buttons = document.querySelectorAll('button');
    for (const b of buttons) { if (b.textContent.includes(text)) return b; }
    return null;
  }, '格式化');
  if (btnA && btnA.asElement()) {
    await btnA.asElement().click();
    await new Promise(r=>setTimeout(r,300));
  }
  const outA = await page.evaluate(() => document.getElementById('formattedOutput').value);
  console.log('Method A (evaluateHandle click):', outA.slice(0,50));
  
  // Reset
  await page.evaluate(() => { document.getElementById('formattedOutput').value = ''; });
  
  // Method B: page.click
  await page.click('#btnFormat');
  await new Promise(r=>setTimeout(r,300));
  const outB = await page.evaluate(() => document.getElementById('formattedOutput').value);
  console.log('Method B (page.click):', outB.slice(0,50));
  
  await browser.close();
})().catch(e => console.error(e));