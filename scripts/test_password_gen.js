#!/usr/bin/env node
const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch({headless: 'new', args: ['--no-sandbox']});
  const page = await browser.newPage();
  await page.setViewport({width: 1280, height: 800});
  await page.goto('file:///home/chison/tools-site/password-generator/index.html', {waitUntil: 'networkidle0'});
  
  const results = [];
  
  // Test 1: Page loads
  const h1 = await page.$eval('h1', el => el.textContent);
  results.push({test: 'Page H1', pass: h1.includes('密码生成器'), detail: h1});
  
  // Test 2: Random mode generates passwords on load
  await page.waitForSelector('.password-item', {timeout: 5000});
  const items = await page.$$('.password-item');
  results.push({test: 'Initial password generation', pass: items.length > 0, detail: items.length + ' passwords'});
  
  // Test 3: Copy button works
  const pwText = await page.$eval('.pw-text', el => el.textContent);
  const copyBtn = await page.$('.pw-btn');
  await copyBtn.click();
  await new Promise(r => setTimeout(r, 800));
  const toast = await page.$eval('#toast', el => el.textContent);
  results.push({test: 'Copy button', pass: toast.includes('复制'), detail: toast});
  
  // Test 4: Mode switch to passphrase
  const modeTabs = await page.$$('.mode-tab:not(.shortcut)');
  await modeTabs[1].click();
  await new Promise(r => setTimeout(r, 500));
  const passphraseVisible = await page.$eval('#passphraseSettings', el => el.style.display !== 'none');
  results.push({test: 'Switch to passphrase mode', pass: passphraseVisible, detail: 'visible=' + passphraseVisible});

  // verify passphrase generated
  const phraseItems = await page.$$('.password-item');
  const phraseText = await page.$eval('.pw-text', el => el.textContent);
  results.push({test: 'Passphrase generated', pass: phraseText.includes('-') || phraseText.includes(' ') || phraseText.length > 20, detail: phraseText.substring(0,30)});
  
  // Test 5: Mode switch to PIN
  await modeTabs[2].click();
  await new Promise(r => setTimeout(r, 500));
  const pinVisible = await page.$eval('#pinSettings', el => el.style.display !== 'none');
  results.push({test: 'Switch to PIN mode', pass: pinVisible, detail: 'visible=' + pinVisible});
  
  const pinText = await page.$eval('.pw-text', el => el.textContent);
  results.push({test: 'PIN generated', pass: /^\d/.test(pinText), detail: pinText});
  
  // Test 6: Slider changes length display (back to random)
  await modeTabs[0].click();
  await new Promise(r => setTimeout(r, 300));
  await page.$eval('#pwLength', (el, v) => { el.value = v; el.dispatchEvent(new Event('input')); }, 32);
  await new Promise(r => setTimeout(r, 300));
  const lenDisplay = await page.$eval('#lengthDisplay', el => el.textContent);
  results.push({test: 'Length slider updates', pass: lenDisplay === '32', detail: lenDisplay});
  
  // Test 7: Generate button
  await page.click('#generateBtn');
  await new Promise(r => setTimeout(r, 300));
  const items2 = await page.$$('.password-item');
  results.push({test: 'Generate button', pass: items2.length > 0, detail: items2.length + ' items'});
  
  // Test 8: Download button exists
  const downloadBtn = await page.$('#downloadBtn');
  results.push({test: 'Download button exists', pass: !!downloadBtn});
  
  // Test 9: Preset - Hex 64
  const shortcuts = await page.$$('.mode-tab.shortcut');
  await shortcuts[0].click();
  await new Promise(r => setTimeout(r, 500));
  const customCharsVal = await page.$eval('#customChars', el => el.value);
  results.push({test: 'Hex64 preset', pass: customCharsVal === '0123456789abcdef', detail: customCharsVal});
  
  // Test 10: Strength bars
  const strengthBars = await page.$$('.pw-strength-bar');
  results.push({test: 'Strength bars', pass: strengthBars.length > 0, detail: strengthBars.length + ' bars'});
  
  // Test 11: Stats bar
  const stats = await page.$eval('#statsBar', el => el.innerHTML);
  results.push({test: 'Stats bar', pass: stats.length > 10, detail: stats.substring(0, 60)});
  
  // Test 12: Check exclude similar
  await modeTabs[0].click();
  await new Promise(r => setTimeout(r, 200));
  await page.$eval('#chExcludeSimilar', el => { el.checked = true; el.dispatchEvent(new Event('change')); });
  await new Promise(r => setTimeout(r, 300));
  const pwsAfterExclude = await page.$$eval('.pw-text', els => els.map(e => e.textContent));
  const hasSimilar = pwsAfterExclude.some(p => /[0O1lI]/.test(p) && !/^请/.test(p));
  results.push({test: 'Exclude similar chars', pass: !hasSimilar, detail: 'no 0/O/1/l/I found'});
  
  // Test 13: Mobile viewport (375px)
  await page.setViewport({width: 375, height: 800});
  await new Promise(r => setTimeout(r, 500));
  const bodyWidth = await page.$eval('body', el => el.scrollWidth);
  results.push({test: 'Mobile 375px no horizontal scroll', pass: bodyWidth <= 375, detail: 'scrollWidth=' + bodyWidth});
  
  const passed = results.filter(r => r.pass).length;
  const total = results.length;
  console.log(JSON.stringify({results, passed, total, allPass: passed === total}, null, 2));
  
  await browser.close();
})();
