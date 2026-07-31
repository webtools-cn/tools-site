const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage']
  });

  const page = await browser.newPage();
  let passed = 0;
  let failed = 0;

  const results = [];

  function check(name, condition, detail) {
    if (condition) {
      passed++;
      results.push(`✅ ${name}: ${detail || 'OK'}`);
    } else {
      failed++;
      results.push(`❌ ${name}: ${detail || 'FAILED'}`);
    }
  }

  try {
    // L0: Page load tests
    await page.goto('file:///home/chison/tools-site/sketch-pad/index.html', { waitUntil: 'networkidle0', timeout: 15000 });

    // 1. Title check
    const title = await page.title();
    check('Page title', title.includes('素描板') || title.includes('Sketch'), title);

    // 2. Canvas element exists
    const canvasExists = await page.$('#sketchCanvas');
    check('Canvas element exists', !!canvasExists);

    // 3. Pencil buttons exist (7 levels)
    const pencilBtns = await page.$$('.pencil-btn');
    check('Pencil hardness buttons', pencilBtns.length === 7, `${pencilBtns.length} buttons found`);

    // 4. Action buttons
    const undoBtn = await page.$('#undoBtn');
    check('Undo button', !!undoBtn);
    const clearBtn = await page.$('#clearBtn');
    check('Clear button', !!clearBtn);
    const downloadBtn = await page.$('#downloadBtn');
    check('Download button', !!downloadBtn);

    // 5. Size slider
    const sizeSlider = await page.$('#sizeSlider');
    check('Size slider', !!sizeSlider);

    // 6. Toast element
    const toast = await page.$('#toast');
    check('Toast element', !!toast);

    // 7. Check no JS errors in console
    const errors = [];
    page.on('pageerror', err => errors.push(err.message));
    // Trigger a resize
    await page.setViewport({ width: 800, height: 600 });
    await new Promise(r => setTimeout(r, 500));
    check('No JS errors on load', errors.length === 0, errors.join(', '));

    // 8. Canvas has dimensions
    const canvasDim = await page.evaluate(() => {
      const c = document.getElementById('sketchCanvas');
      return { w: c.width, h: c.height };
    });
    check('Canvas has dimensions', canvasDim.w > 0 && canvasDim.h > 0, `${canvasDim.w}x${canvasDim.h}`);

    // 9. Active pencil button
    const activePencil = await page.evaluate(() => {
      const active = document.querySelector('.pencil-btn.active');
      return active ? active.getAttribute('data-pencil') : null;
    });
    check('Default active pencil is 2B', activePencil === '2B', activePencil);

    // L1: Interaction tests

    // L1.1: Click pencil button to change active
    await page.click('.pencil-btn[data-pencil="6B"]');
    const newActive = await page.evaluate(() => {
      const active = document.querySelector('.pencil-btn.active');
      return active ? active.getAttribute('data-pencil') : null;
    });
    check('Click 6B button changes active', newActive === '6B', newActive);

    // L1.2: Change size slider
    await page.evaluate(() => {
      const slider = document.getElementById('sizeSlider');
      slider.value = '4';
      slider.dispatchEvent(new Event('input'));
    });
    const sizeDisplay = await page.$eval('#sizeDisplay', el => el.textContent);
    check('Size slider changes display', sizeDisplay === '4px', sizeDisplay);

    // L1.3: Draw on canvas and check undo stack
    await page.evaluate(() => {
      const canvas = document.getElementById('sketchCanvas');
      const rect = canvas.getBoundingClientRect();
      // Simulate a mousedown-move-mouseup sequence
      canvas.dispatchEvent(new MouseEvent('mousedown', { clientX: rect.left + 100, clientY: rect.top + 100, bubbles: true }));
      canvas.dispatchEvent(new MouseEvent('mousemove', { clientX: rect.left + 150, clientY: rect.top + 150, bubbles: true }));
      canvas.dispatchEvent(new MouseEvent('mouseup', { clientX: rect.left + 150, clientY: rect.top + 150, bubbles: true }));
    });
    await new Promise(r => setTimeout(r, 200));
    const undoStackLen = await page.evaluate(() => {
      // Access the undoStack inside the IIFE closure via a hack: we'll check if undo works
      return true; // We'll verify via undo action below
    });

    // L1.4: Click undo
    await page.click('#undoBtn');
    await new Promise(r => setTimeout(r, 200));
    const toastText = await page.evaluate(() => {
      const t = document.getElementById('toast');
      return t.textContent;
    });
    check('Undo shows toast', toastText.includes('撤销') || toastText.includes('Undone'), toastText);

    // L1.5: Click clear
    await page.click('#clearBtn');
    await new Promise(r => setTimeout(r, 200));
    const clearToast = await page.evaluate(() => document.getElementById('toast').textContent);
    check('Clear shows toast', clearToast.includes('清空') || clearToast.includes('cleared'), clearToast);

    // L1.6: Click download (doesn't actually download, just triggers)
    await page.click('#downloadBtn');
    await new Promise(r => setTimeout(r, 200));
    const dlToast = await page.evaluate(() => document.getElementById('toast').textContent);
    check('Download shows toast', dlToast.includes('下载') || dlToast.includes('Downloaded'), dlToast);

  } catch (e) {
    results.push(`💥 CRASH: ${e.message}`);
    failed++;
  }

  console.log('\n=== Sketch Pad Test Results ===');
  results.forEach(r => console.log(r));
  console.log(`\nPassed: ${passed}, Failed: ${failed}`);
  console.log(failed === 0 ? '🎉 ALL TESTS PASSED!' : '❌ SOME TESTS FAILED');

  await browser.close();
  process.exit(failed > 0 ? 1 : 0);
})();