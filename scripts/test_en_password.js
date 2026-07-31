#!/usr/bin/env node
const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch({headless: 'new', args: ['--no-sandbox']});
  const page = await browser.newPage();
  await page.setViewport({width: 1280, height: 800});
  await page.goto('file:///home/chison/tools-site/en/password-generator/index.html', {waitUntil: 'networkidle0'});
  
  const results = [];
  
  // Basic checks
  const h1 = await page.$eval('h1', el => el.textContent);
  results.push({test: 'EN H1', pass: h1.includes('Password Generator'), detail: h1});
  
  const pws = await page.$$('.pw-item');
  results.push({test: 'EN Passwords generated', pass: pws.length > 0, detail: pws.length + ' passwords'});
  
  // L5 features
  const memBadges = await page.$$('.mem-badge');
  results.push({test: 'EN Memorability badges', pass: memBadges.length > 0, detail: memBadges.length + ' badges'});
  
  const qrBtns = await page.$$eval('.pw-btn', btns => 
    btns.filter(b => b.textContent === '📱').length
  );
  results.push({test: 'EN QR buttons', pass: qrBtns > 0, detail: qrBtns + ' QR buttons'});
  
  // Mode switch
  const tabs = await page.$$('.mode-tab:not(.shortcut)');
  await tabs[1].click();
  await new Promise(r => setTimeout(r, 500));
  const memLabels = await page.$$eval('.mem-badge', els => els.map(e => e.textContent));
  results.push({test: 'EN Passphrase memorability = Easy', pass: memLabels.some(l => l === 'Easy'), detail: memLabels.join(',')});
  
  // Switch to PIN mode  
  await tabs[2].click();
  await new Promise(r => setTimeout(r, 500));
  const pinLabels = await page.$$eval('.mem-badge', els => els.map(e => e.textContent));
  results.push({test: 'EN PIN mode works', pass: pinLabels.length > 0, detail: pinLabels.join(',')});
  
  // Test QR overlay
  const firstQR = await page.$('.pw-btn');  // actually need to find QR button
  const allBtns = await page.$$('.pw-btn');
  let qrBtn = null;
  for (const btn of allBtns) {
    const text = await page.evaluate(el => el.textContent, btn);
    if (text === '📱') { qrBtn = btn; break; }
  }
  if (qrBtn) {
    await qrBtn.click();
    await new Promise(r => setTimeout(r, 500));
    const overlayVisible = await page.$eval('#qrOverlay', el => el.classList.contains('show'));
    results.push({test: 'EN QR modal opens', pass: overlayVisible});
    const canvasData = await page.$eval('#qrCanvas', el => {
      const ctx = el.getContext('2d');
      const data = ctx.getImageData(0, 0, el.width, el.height).data;
      for (let i = 0; i < data.length; i += 4) {
        if (data[i] < 200 || data[i+1] < 200 || data[i+2] < 200) return true;
      }
      return false;
    });
    results.push({test: 'EN QR canvas rendered', pass: canvasData});
  }
  
  // Stats bar
  const statsText = await page.$eval('#statsBar', el => el.textContent);
  results.push({test: 'EN Stats bar', pass: statsText.includes('Avg entropy') && statsText.includes('Easy'), detail: statsText.substring(0, 80)});
  
  const passed = results.filter(r => r.pass).length;
  const total = results.length;
  console.log(JSON.stringify({results, passed, total, allPass: passed === total}, null, 2));
  
  await browser.close();
})();