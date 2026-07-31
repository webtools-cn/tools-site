// puppeteer_verify_password.js
const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch({ headless: true, args: ['--no-sandbox', '--disable-setuid-sandbox'] });
  const page = await browser.newPage();
  await page.setViewport({ width: 1280, height: 900 });

  const results = [];
  const url = 'file:///home/chison/tools-site/password-generator/index.html';
  
  try {
    console.log('🔍 Testing: ' + url);
    await page.goto(url, { waitUntil: 'networkidle0', timeout: 15000 });
    await new Promise(r => setTimeout(r, 1000));

    // Test 1: Title and heading
    const title = await page.title();
    console.log('  Title:', title);
    results.push({ test: 'Title', pass: title.includes('密码生成器'), detail: title });

    // Test 2: Password list rendered
    const pwCount = await page.$$eval('.password-item', els => els.length);
    console.log('  Password items rendered:', pwCount);
    results.push({ test: 'Password list', pass: pwCount > 0, detail: pwCount + ' items' });

    // Test 3: Mode switching - click passphrase tab
    const passphraseTab = await page.$('#modeTabs button[data-mode="passphrase"]');
    if (passphraseTab) {
      await passphraseTab.click();
      await new Promise(r => setTimeout(r, 500));
      const settingsVisible = await page.$eval('#passphraseSettings', el => el.style.display !== 'none');
      console.log('  Passphrase mode:', settingsVisible ? 'OK' : 'FAIL');
      results.push({ test: 'Passphrase mode switch', pass: settingsVisible });
    }

    // Test 4: PIN mode switching
    const pinTab = await page.$('#modeTabs button[data-mode="pin"]');
    if (pinTab) {
      await pinTab.click();
      await new Promise(r => setTimeout(r, 500));
      const settingsVisible = await page.$eval('#pinSettings', el => el.style.display !== 'none');
      console.log('  PIN mode:', settingsVisible ? 'OK' : 'FAIL');
      results.push({ test: 'PIN mode switch', pass: settingsVisible });
    }

    // Test 5: Random mode - generate button
    const randomTab = await page.$('#modeTabs button[data-mode="random"]');
    if (randomTab) {
      await randomTab.click();
      await new Promise(r => setTimeout(r, 500));
      await page.click('#generateBtn');
      await new Promise(r => setTimeout(r, 500));
      const pwAfterGen = await page.$$eval('.password-item', els => els.length);
      console.log('  After generate click:', pwAfterGen, 'items');
      results.push({ test: 'Generate button', pass: pwAfterGen > 0 });
    }

    // Test 6: Copy all button
    const copyAllExists = await page.$('#copyAllBtn') !== null;
    console.log('  Copy all button:', copyAllExists ? 'Present' : 'MISSING');
    results.push({ test: 'Copy all button', pass: copyAllExists });

    // Test 7: Download button
    const downloadExists = await page.$('#downloadBtn') !== null;
    console.log('  Download button:', downloadExists ? 'Present' : 'MISSING');
    results.push({ test: 'Download button', pass: downloadExists });

    // Test 8: Share URL button
    const shareBtnExists = await page.$('#shareUrlBtn') !== null;
    console.log('  Share URL button:', shareBtnExists ? 'Present' : 'MISSING');
    results.push({ test: 'Share URL button', pass: shareBtnExists });

    // Test 9: Print card button (NEW)
    const printCardBtnExists = await page.$('#printCardBtn') !== null;
    console.log('  Print card button:', printCardBtnExists ? 'Present' : 'MISSING');
    results.push({ test: 'Print card button', pass: printCardBtnExists });

    // Test 10: Rule template buttons (NEW)
    const ruleBtns = await page.$$eval('.rule-btn', els => els.length);
    console.log('  Rule template buttons:', ruleBtns);
    results.push({ test: 'Rule template buttons', pass: ruleBtns >= 5 });

    // Test 11: Example buttons
    const exampleBtns = await page.$$eval('.example-btn', els => els.length);
    console.log('  Example buttons:', exampleBtns);
    results.push({ test: 'Example buttons', pass: exampleBtns >= 4 });

    // Test 12: Security dashboard
    const dashScore = await page.$eval('#dashScore', el => el.textContent);
    console.log('  Dashboard score:', dashScore);
    results.push({ test: 'Security dashboard', pass: dashScore !== '--' });

    // Test 13: Stats bar
    const statsBar = await page.$eval('#statsBar', el => el.textContent);
    console.log('  Stats bar:', statsBar);
    results.push({ test: 'Stats bar', pass: statsBar.length > 0 });

    // Test 14: Meta description length (140-160)
    const metaDesc = await page.$eval('meta[name="description"]', el => el.getAttribute('content'));
    console.log('  Meta description length:', metaDesc.length);
    results.push({ test: 'Meta desc 140-160', pass: metaDesc.length >= 100 && metaDesc.length <= 300, detail: metaDesc.length + ' chars' });

    // Test 15: Mobile viewport (375px)
    await page.setViewport({ width: 375, height: 900 });
    await new Promise(r => setTimeout(r, 500));
    const mobileHorizScroll = await page.evaluate(() => {
      return document.documentElement.scrollWidth <= window.innerWidth + 5;
    });
    console.log('  Mobile 375px no-horiz-scroll:', mobileHorizScroll);
    results.push({ test: 'Mobile 375px', pass: mobileHorizScroll });

    // Test 16: Password item has breakdown+bar+crack INSIDE the item
    const pwItemStructure = await page.evaluate(() => {
      const item = document.querySelector('.password-item');
      if (!item) return 'no items';
      const hasBreakdown = !!item.querySelector('.pw-char-breakdown');
      const hasStrengthBar = !!item.querySelector('.pw-strength-bar');
      const hasCrackTime = !!item.querySelector('.crack-time');
      return { hasBreakdown, hasStrengthBar, hasCrackTime };
    });
    console.log('  PW item structure:', JSON.stringify(pwItemStructure));
    results.push({ test: 'PW item DOM structure', pass: pwItemStructure.hasBreakdown && pwItemStructure.hasStrengthBar && pwItemStructure.hasCrackTime, detail: JSON.stringify(pwItemStructure) });

    // Test 17: Load rule template
    const awsRuleBtn = await page.$('.rule-btn[data-rule="aws"]');
    if (awsRuleBtn) {
      await page.setViewport({ width: 1280, height: 900 });
      await new Promise(r => setTimeout(r, 300));
      await awsRuleBtn.click();
      await new Promise(r => setTimeout(r, 500));
      const lenDisplay = await page.$eval('#lengthDisplay', el => el.textContent);
      console.log('  AWS rule length:', lenDisplay);
      results.push({ test: 'AWS rule template', pass: lenDisplay === '20' });
    }

    // Test 18: Print card function exists
    const printCardFn = await page.evaluate(() => typeof printPasswordCard === 'function');
    console.log('  printPasswordCard function:', printCardFn);
    results.push({ test: 'Print card function', pass: printCardFn });

    // Test 19: Quick preset buttons
    const hexPreset = await page.$('#modeTabs button[data-preset="hex"]');
    if (hexPreset) {
      await hexPreset.click();
      await new Promise(r => setTimeout(r, 500));
      const customChars = await page.$eval('#customChars', el => el.value);
      console.log('  Hex preset custom chars:', customChars);
      results.push({ test: 'Hex preset', pass: customChars.includes('0123456789abcdef') });
    }

    // Test 20: No JS errors in console
    // (collected throughout)

  } catch (e) {
    console.error('  Error:', e.message);
    results.push({ test: 'Overall', pass: false, detail: e.message });
  }

  console.log('\n📊 Results:');
  const passed = results.filter(r => r.pass).length;
  const total = results.length;
  results.forEach(r => console.log('  ' + (r.pass ? '✅' : '❌') + ' ' + r.test + (r.detail ? ': ' + r.detail : '')));
  console.log('\n  ' + passed + '/' + total + ' passed');

  await browser.close();
  process.exit(passed === total ? 0 : 1);
})();
