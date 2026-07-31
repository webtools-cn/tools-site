#!/usr/bin/env node
const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch({headless: 'new', args: ['--no-sandbox']});
  const page = await browser.newPage();
  await page.setViewport({width: 1280, height: 800});
  await page.goto('file:///home/chison/tools-site/password-generator/index.html', {waitUntil: 'networkidle0'});
  
  const results = [];
  
  // Test L5-1: Memorability badges visible
  const memBadges = await page.$$('.mem-badge');
  results.push({test: 'L5: Memorability badges', pass: memBadges.length > 0, detail: memBadges.length + ' badges'});
  
  // Test L5-2: QR buttons visible
  const qrBtns = await page.$$('.pw-btn');
  const qrBtnCount = await page.$$eval('.pw-btn', btns => 
    btns.filter(b => b.textContent === '📱').length
  );
  results.push({test: 'L5: QR buttons exist', pass: qrBtnCount > 0, detail: qrBtnCount + ' QR buttons'});
  
  // Test L5-3: QR modal exists in DOM
  const qrOverlay = await page.$('#qrOverlay');
  results.push({test: 'L5: QR overlay exists', pass: !!qrOverlay});
  
  // Test L5-4: Click QR button opens modal
  const firstQRBtn = await page.$('.pw-btn');
  // Find the actual QR button
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
    results.push({test: 'L5: QR modal opens', pass: overlayVisible, detail: 'overlay visible=' + overlayVisible});
    
    // Test QR canvas has content
    const canvasData = await page.$eval('#qrCanvas', el => {
      const ctx = el.getContext('2d');
      const data = ctx.getImageData(0, 0, el.width, el.height).data;
      // Check if any pixel is black (non-white)
      for (let i = 0; i < data.length; i += 4) {
        if (data[i] < 200 || data[i+1] < 200 || data[i+2] < 200) return true;
      }
      return false;
    });
    results.push({test: 'L5: QR canvas has content', pass: canvasData, detail: 'has black pixels=' + canvasData});
    
    // Close modal
    await page.$eval('.qr-close', el => el.click());
    await new Promise(r => setTimeout(r, 300));
  }
  
  // Test L5-5: Stats bar shows memorability
  const statsText = await page.$eval('#statsBar', el => el.textContent);
  results.push({test: 'L5: Stats bar has memorability', pass: statsText.includes('易记') || statsText.includes('中等') || statsText.includes('难记'), detail: statsText.substring(0, 80)});
  
  // Test L5-6: Switch to passphrase mode, check memorability = "易记"
  const modeTabs = await page.$$('.mode-tab:not(.shortcut)');
  await modeTabs[1].click();
  await new Promise(r => setTimeout(r, 500));
  const memLabels = await page.$$eval('.mem-badge', els => els.map(e => e.textContent));
  const hasEasy = memLabels.some(l => l === '易记');
  results.push({test: 'L5: Passphrase memorability = 易记', pass: hasEasy, detail: memLabels.join(',')});
  
  // Test L5-7: QR code generated in overlay displays password
  const pwText = await page.$eval('.pw-text', el => el.textContent);
  // Find QR button and click
  const qrBtns2 = await page.$$('.pw-btn');
  let qrBtn2 = null;
  for (const btn of qrBtns2) {
    const text = await page.evaluate(el => el.textContent, btn);
    if (text === '📱') { qrBtn2 = btn; break; }
  }
  if (qrBtn2) {
    await qrBtn2.click();
    await new Promise(r => setTimeout(r, 500));
    const qrPass = await page.$eval('#qrPassDisplay', el => el.textContent);
    results.push({test: 'L5: QR displays correct password', pass: qrPass === pwText, detail: 'QR=' + qrPass.substring(0,15) + ' PW=' + pwText.substring(0,15)});
  }
  
  // Test L5-8: FAQ count increased (new QR + memorability FAQs)
  const faqCount = await page.$$eval('.info-section h3', els => 
    els.filter(e => e.textContent && e.textContent.includes('?') && !e.textContent.includes('模式')).length
  );
  results.push({test: 'L5: FAQ questions count', pass: faqCount >= 8, detail: faqCount + ' FAQs'});
  
  const passed = results.filter(r => r.pass).length;
  const total = results.length;
  console.log(JSON.stringify({results, passed, total, allPass: passed === total}, null, 2));
  
  await browser.close();
})();