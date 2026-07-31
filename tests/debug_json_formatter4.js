const puppeteer = require('puppeteer');
(async () => {
  const browser = await puppeteer.launch({headless: true, args: ['--no-sandbox']});
  const page = await browser.newPage();
  const jsErrors = [];
  page.on('pageerror', err => jsErrors.push(err.message));
  
  await page.goto('file:///home/chison/tools-site/json-formatter/index.html', {waitUntil: 'load', timeout: 10000});
  await new Promise(r=>setTimeout(r,500));
  
  // Simulate test: find textarea, click, type
  const input = await page.$('textarea');
  if (input) {
    await input.click({clickCount: 3});
    await input.type('{"a":1}');
  }
  
  // Find button with "格式化"
  const btn = await page.evaluateHandle((text) => {
    const buttons = document.querySelectorAll('button');
    for (const b of buttons) {
      if (b.textContent.includes(text)) return b;
    }
    return null;
  }, '格式化');
  
  if (btn && btn.asElement()) {
    console.log('Clicking button...');
    await btn.asElement().click();
    await new Promise(r=>setTimeout(r,500));
  } else {
    console.log('Button not found!');
  }
  
  console.log('JS errors:', jsErrors);
  
  // Check outputSelector: #formattedOutput,#rawOutput,.raw-output,textarea[readonly]
  const outputCheck = await page.evaluate(() => {
    const selector = '#formattedOutput,#rawOutput,.raw-output,textarea[readonly]';
    const els = document.querySelectorAll(selector);
    const results = [];
    els.forEach(el => {
      results.push(el.id + '/' + el.tagName + ': ' + (el.value||el.textContent||'').slice(0,100));
    });
    return results;
  });
  console.log('Output selector results:', outputCheck);
  
  // Check anyOutput fallback
  const anyOutput = await page.evaluate(() => {
    const els = document.querySelectorAll('[id*="result"],[id*="output"],[class*="result"],[class*="output"],textarea[readonly]');
    for (const el of els) {
      const text = (el.textContent||'').trim() || (el.value||'').trim();
      if (text && text.length > 0) return el.id + ': ' + text.slice(0, 200);
    }
    return null;
  });
  console.log('anyOutput:', anyOutput);
  
  await browser.close();
})().catch(e => console.error(e));