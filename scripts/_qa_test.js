const puppeteer = require('puppeteer');
const path = require('path');

const pages = process.argv.slice(2);
const results = {};

(async () => {
  const browser = await puppeteer.launch({
    executablePath: '/usr/bin/google-chrome-stable',
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  for (const p of pages) {
    const fileUrl = 'file://' + path.resolve(p);
    const page = await browser.newPage();
    await page.setViewport({ width: 1280, height: 900 });
    const errors = [];
    page.on('pageerror', e => errors.push('PAGEERROR: ' + e.message));
    page.on('console', m => { if (m.type() === 'error') errors.push('CONSOLE: ' + m.text()); });

    try {
      await page.goto(fileUrl, { waitUntil: 'networkidle0', timeout: 15000 });
    } catch (e) {
      errors.push('GOTO: ' + e.message);
    }

    const info = await page.evaluate(() => {
      const r = {};
      r.title = document.title;
      r.h1s = document.querySelectorAll('h1').length;
      r.mains = document.querySelectorAll('main').length;
      r.footers = document.querySelectorAll('footer').length;
      r.sections = document.querySelectorAll('section').length;
      r.divs = document.querySelectorAll('div').length;
      r.horizontalScroll = document.documentElement.scrollWidth > document.documentElement.clientWidth;
      r.langSwitch = !!document.querySelector('.lang-switch');
      r.langSwitchTop = (() => {
        const ls = document.querySelector('.lang-switch');
        if (!ls) return false;
        const h1 = document.querySelector('h1');
        if (!h1) return true;
        return ls.getBoundingClientRect().top <= h1.getBoundingClientRect().top;
      })();
      r.footerLast = (() => {
        const f = document.querySelector('footer');
        if (!f) return false;
        const els = Array.from(document.querySelectorAll('body > *')).filter(el => !['SCRIPT','STYLE','LINK','META'].includes(el.tagName));
        const last = els[els.length - 1];
        return last === f || last.contains(f);
      })();
      r.metaDesc = (document.querySelector('meta[name="description"]') || {}).content || '';
      r.ga = document.documentElement.innerHTML.includes('G-QVBQNJ3L5E');
      r.adsense = document.documentElement.innerHTML.includes('ca-pub-5527959372219623');
      r.canonical = !!document.querySelector('link[rel="canonical"]');
      r.hreflang = document.querySelectorAll('link[rel="alternate"][hreflang]').length;
      r.cssVars = !!document.querySelector('style') && document.documentElement.innerHTML.includes(':root');
      r.bodyBg = getComputedStyle(document.body).backgroundColor;
      r.bodyColor = getComputedStyle(document.body).color;
      r.lightBgResidual = (() => {
        const re = /background(?:-color)?\s*:\s*(#fff\b|#ffffff\b|#f8fafc|#EEF2FF|#E0E7FF|#f0fdf4|#f1f5f9|#e2e8f0\b)/gi;
        const m = document.documentElement.innerHTML.match(re) || [];
        return m;
      })();
      r.duplicateH1 = document.querySelectorAll('h1').length > 1;
      r.duplicateMain = document.querySelectorAll('main').length > 1;
      return r;
    });

    // mobile check
    await page.setViewport({ width: 375, height: 800 });
    const mobile = await page.evaluate(() => ({
      horizontalScroll: document.documentElement.scrollWidth > document.documentElement.clientWidth,
      bodyWidth: document.body.scrollWidth,
      viewport: document.documentElement.clientWidth
    }));

    results[p] = { errors, info, mobile };
    await page.close();
  }

  await browser.close();
  console.log(JSON.stringify(results, null, 2));
})();