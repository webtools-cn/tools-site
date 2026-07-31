const puppeteer = require('puppeteer');
(async () => {
  const browser = await puppeteer.launch({headless: true, args: ['--no-sandbox']});
  const page = await browser.newPage();
  page.on('pageerror', err => console.log('JS error:', err.message));
  page.on('console', msg => console.log('CONSOLE:', msg.type(), msg.text()));
  await page.goto('file:///home/chison/tools-site/json-formatter/index.html', {waitUntil: 'load', timeout: 10000});
  await new Promise(r=>setTimeout(r,1000));
  
  // Check if clicking the button works
  await page.evaluate(() => {
    document.querySelector('textarea').value = '{"test":123}';
  });
  
  // Click via Puppeteer
  await page.click('#btnFormat');
  await new Promise(r=>setTimeout(r,500));
  
  const output = await page.evaluate(() => {
    const el = document.getElementById('formattedOutput');
    return el ? 'value: "' + el.value + '"' : 'null';
  });
  console.log('After click btnFormat:', output);
  
  // Check if event listener was added
  const listeners = await page.evaluate(() => {
    // Check if clicking the button directly dispatches
    const btn = document.getElementById('btnFormat');
    const orig = btn.onclick;
    // Use getEventListeners equivalent - try triggering manually
    btn.dispatchEvent(new MouseEvent('click', {bubbles: true}));
    return 'dispatched';
  });
  console.log('Manual dispatch result:', listeners);
  
  const output2 = await page.evaluate(() => {
    const el = document.getElementById('formattedOutput');
    return el ? 'value: "' + el.value + '"' : 'null';
  });
  console.log('After dispatchEvent:', output2);
  
  await browser.close();
})().catch(e => console.error(e));