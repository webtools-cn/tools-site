const puppeteer = require('puppeteer');
(async () => {
  const browser = await puppeteer.launch({headless: true, args: ['--no-sandbox']});
  const page = await browser.newPage();
  const jsErrors = [];
  page.on('pageerror', err => jsErrors.push(err.message));
  await page.goto('file:///home/chison/tools-site/json-formatter/index.html', {waitUntil: 'load', timeout: 10000});
  await new Promise(r=>setTimeout(r,500));
  console.log('JS errors:', jsErrors);
  
  const btnExists = await page.evaluate(() => !!document.getElementById('btnFormat'));
  console.log('btnFormat exists:', btnExists);
  
  const textarea = await page.$('textarea');
  if (textarea) {
    await textarea.click({clickCount: 3});
    await textarea.type('{"test":123}');
  }
  console.log('Typed input');
  
  const btn = await page.evaluateHandle(() => {
    const buttons = document.querySelectorAll('button');
    for (const b of buttons) { if (b.textContent.includes('格式化')) return b; }
    return null;
  });
  console.log('Found button:', !!btn.asElement());
  if (btn.asElement()) {
    await btn.asElement().click();
    await new Promise(r=>setTimeout(r,300));
  }
  
  const output = await page.evaluate(() => {
    const el = document.getElementById('formattedOutput');
    if (el) return 'formattedOutput: ' + (el.value ? el.value.slice(0,100) : '(empty)');
    return 'no formattedOutput';
  });
  console.log('Output:', output);
  
  const allOutputs = await page.evaluate(() => {
    const results = [];
    document.querySelectorAll('[id*="Output"]').forEach(el => {
      results.push(el.id + ': ' + (el.value||el.textContent||'').slice(0,50));
    });
    return results;
  });
  console.log('All outputs:', allOutputs);

  // Check form elements
  const formEls = await page.evaluate(() => {
    return document.querySelectorAll('textarea,input,button').length;
  });
  console.log('Form elements count:', formEls);
  
  await browser.close();
})().catch(e => console.error(e));
