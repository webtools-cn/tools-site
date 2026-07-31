const puppeteer = require('puppeteer');
(async () => {
  const browser = await puppeteer.launch({headless: true, args: ['--no-sandbox']});
  const page = await browser.newPage();
  page.on('pageerror', err => console.log('JS error:', err.message));
  page.on('console', msg => console.log('CONSOLE:', msg.type(), msg.text()));
  await page.goto('file:///home/chison/tools-site/json-formatter/index.html', {waitUntil: 'load', timeout: 10000});
  await new Promise(r=>setTimeout(r,1000));
  
  // Check if formatJSON exists globally
  const hasFn = await page.evaluate(() => {
    return {
      formatJSON: typeof formatJSON,
      getInput: typeof getInput,
      bindEvents: typeof bindEvents,
      btnFormat_onclick: document.getElementById('btnFormat').onclick,
      btnFormat_listeners: document.getElementById('btnFormat').getAttribute('onclick'),
      toastExists: !!document.getElementById('toast'),
    };
  });
  console.log('Functions check:', hasFn);
  
  // Directly call formatJSON
  await page.evaluate(() => {
    document.querySelector('textarea').value = '{"test":123}';
  });
  await page.evaluate(() => {
    try { formatJSON(); } catch(e) { console.log('formatJSON error:', e.message); }
  });
  await new Promise(r=>setTimeout(r,300));
  
  const output = await page.evaluate(() => {
    const el = document.getElementById('formattedOutput');
    return el ? 'value: "' + el.value + '"' : 'null';
  });
  console.log('After direct formatJSON:', output);
  
  // Check toast
  const toast = await page.evaluate(() => {
    const t = document.getElementById('toast');
    return t ? t.textContent + ' / classes:' + t.className : 'null';
  });
  console.log('Toast:', toast);
  
  await browser.close();
})().catch(e => console.error(e));