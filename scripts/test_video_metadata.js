const puppeteer = require('puppeteer');
const path = require('path');

(async () => {
  const htmlPath = 'file://' + path.resolve('/home/chison/tools-site/video-metadata/index.html');
  console.log('Loading:', htmlPath);

  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-web-security']
  });

  const page = await browser.newPage();

  let errors = [];

  // Collect console errors
  page.on('pageerror', err => {
    errors.push('PAGE ERROR: ' + err.message);
  });
  page.on('console', msg => {
    if (msg.type() === 'error') {
      errors.push('CONSOLE ERROR: ' + msg.text());
    }
  });

  await page.goto(htmlPath, { waitUntil: 'networkidle0', timeout: 30000 });
  console.log('Page loaded');

  // L0: Check key elements exist
  const checks = [
    { name: 'File Input', sel: '#fileInput' },
    { name: 'Drop Zone', sel: '#dropZone' },
    { name: 'Result Section', sel: '#resultSection' },
    { name: 'Meta Grid', sel: '#metaGrid' },
    { name: 'Loading Spinner', sel: '#loadingSpinner' },
    { name: 'Clear Button', sel: 'button' }, // at least one button
    { name: 'Video Preview', sel: '#previewVideo' },
    { name: 'Toast', sel: '#toast' },
    { name: 'Title H1', sel: 'h1' },
    { name: 'FAQ Section', sel: '.faq-item' },
  ];

  let l0Passed = 0;
  let l0Failed = 0;
  for (const check of checks) {
    const el = await page.$(check.sel);
    if (el) {
      console.log('  [PASS] L0:', check.name);
      l0Passed++;
    } else {
      console.log('  [FAIL] L0:', check.name, '- NOT FOUND');
      l0Failed++;
    }
  }

  // L1: Check that JS functions are defined globally
  console.log('\n--- L1: JS Function Tests ---');
  const functions = ['showToast', 'handleFileSelect', 'processFile', 'clearAll', 'formatFileSize', 'formatDuration', 'formatBitrate'];
  let l1Passed = 0;
  let l1Failed = 0;

  for (const fn of functions) {
    const exists = await page.evaluate((name) => {
      return typeof window[name] === 'function';
    }, fn);
    if (exists) {
      console.log('  [PASS] L1:', fn, 'is defined globally');
      l1Passed++;
    } else {
      console.log('  [FAIL] L1:', fn, 'is NOT defined globally');
      l1Failed++;
    }
  }

  // L1: Test file input exists and has accept attribute
  const acceptAttr = await page.$eval('#fileInput', el => el.getAttribute('accept'));
  console.log('  [INFO] File input accept:', acceptAttr);
  if (acceptAttr === 'video/*') {
    console.log('  [PASS] L1: accept="video/*" correct');
    l1Passed++;
  } else {
    console.log('  [FAIL] L1: accept attribute wrong:', acceptAttr);
    l1Failed++;
  }

  // L1: Test that toast function works
  await page.evaluate(() => { showToast('Test toast', false); });
  const toastVisible = await page.$eval('#toast', el => el.classList.contains('show'));
  console.log('  [INFO] Toast visible after call:', toastVisible);
  if (toastVisible) {
    console.log('  [PASS] L1: Toast notification works');
    l1Passed++;
  } else {
    console.log('  [FAIL] L1: Toast not showing');
    l1Failed++;
  }

  // L1: Check that the clearAll function resets properly
  await page.evaluate(() => { clearAll(); });
  const resultHidden = await page.$eval('#resultSection', el => !el.classList.contains('visible'));
  console.log('  [INFO] Result section hidden after clear:', resultHidden);
  if (resultHidden) {
    console.log('  [PASS] L1: clearAll works');
    l1Passed++;
  } else {
    console.log('  [FAIL] L1: clearAll did not hide results');
    l1Failed++;
  }

  // L1: Test utility functions
  const formatTests = [
    { fn: 'formatFileSize', args: [1048576], expected: '1.00 MB' },
    { fn: 'formatFileSize', args: [0], expected: '0 B' },
    { fn: 'formatDuration', args: [65], expected: '1分5秒' },
    { fn: 'formatDuration', args: [3661], expected: '1时1分1秒' },
    { fn: 'formatBitrate', args: [1000000], expected: '1.00 Mbps' },
  ];

  for (const test of formatTests) {
    const result = await page.evaluate((name, args) => {
      return window[name].apply(null, args);
    }, test.fn, test.args);
    const pass = result === test.expected;
    if (pass) {
      console.log('  [PASS] L1:', test.fn + '(' + test.args.join(',') + ') = "' + result + '"');
      l1Passed++;
    } else {
      console.log('  [FAIL] L1:', test.fn + '(' + test.args.join(',') + ') = "' + result + '" (expected "' + test.expected + '")');
      l1Failed++;
    }
  }

  // Summary
  console.log('\n==========================');
  console.log('L0 Results:', l0Passed + '/' + (l0Passed + l0Failed) + ' passed');
  console.log('L1 Results:', l1Passed + '/' + (l1Passed + l1Failed) + ' passed');
  console.log('Page Errors:', errors.length);
  if (errors.length > 0) {
    console.log('Errors:', errors);
  }
  console.log('==========================');

  const allPassed = (l0Failed === 0 && l1Failed === 0 && errors.length === 0);
  console.log(allPassed ? 'ALL TESTS PASSED' : 'SOME TESTS FAILED');

  await browser.close();
  process.exit(allPassed ? 0 : 1);
})();
