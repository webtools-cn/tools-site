#!/usr/bin/env python3
"""Puppeteer验证password-generator页面功能"""
import subprocess, sys, json, time

def run_js(code):
    """在Puppeteer中执行JS并返回结果"""
    import subprocess
    result = subprocess.run([
        'node', '-e', f'''
const puppeteer = require('puppeteer');
(async () => {{
  const browser = await puppeteer.launch({{headless: 'new', args: ['--no-sandbox']}});
  const page = await browser.newPage();
  await page.goto('file:///home/chison/tools-site/password-generator/index.html', {{waitUntil: 'networkidle0'}});
  
  const results = [];
  
  // Test 1: Page loads
  const h1 = await page.$eval('h1', el => el.textContent);
  results.push({{test: 'Page H1', pass: h1.includes('密码生成器'), detail: h1}});
  
  // Test 2: Random mode generates passwords on load
  await page.waitForSelector('.password-item');
  const items = await page.$$('.password-item');
  results.push({{test: 'Initial password generation', pass: items.length > 0, detail: items.length + ' passwords'}});
  
  // Test 3: Copy button works
  const copyBtn = await page.$('.pw-btn');
  await copyBtn.click();
  await page.waitForTimeout(500);
  const toast = await page.$eval('#toast', el => el.textContent);
  results.push({{test: 'Copy button', pass: toast.includes('复制'), detail: toast}});
  
  // Test 4: Mode switch to passphrase
  await page.click('.mode-tab:nth-child(2)');
  await page.waitForTimeout(300);
  const passphraseVisible = await page.$eval('#passphraseSettings', el => el.style.display !== 'none');
  results.push({{test: 'Switch to passphrase mode', pass: passphraseVisible, detail: 'visible=' + passphraseVisible}});
  
  // Test 5: Mode switch to PIN
  await page.click('.mode-tab:nth-child(3)');
  await page.waitForTimeout(300);
  const pinVisible = await page.$eval('#pinSettings', el => el.style.display !== 'none');
  results.push({{test: 'Switch to PIN mode', pass: pinVisible, detail: 'visible=' + pinVisible}});
  
  // Test 6: Slider changes length display
  await page.click('.mode-tab:nth-child(1)');
  await page.waitForTimeout(200);
  await page.$eval('#pwLength', (el, v) => {{ el.value = v; el.dispatchEvent(new Event('input')); }}, 32);
  await page.waitForTimeout(200);
  const lenDisplay = await page.$eval('#lengthDisplay', el => el.textContent);
  results.push({{test: 'Length slider updates display', pass: lenDisplay === '32', detail: lenDisplay}});
  
  // Test 7: Generate button
  await page.click('#generateBtn');
  await page.waitForTimeout(300);
  const items2 = await page.$$('.password-item');
  results.push({{test: 'Generate button', pass: items2.length > 0, detail: items2.length + ' items'}});
  
  // Test 8: Download button exists
  const downloadBtn = await page.$('#downloadBtn');
  results.push({{test: 'Download button exists', pass: !!downloadBtn}});
  
  // Test 9: Preset - Hex 64
  await page.click('.mode-tab.shortcut:nth-child(4)');
  await page.waitForTimeout(300);
  const customCharsVal = await page.$eval('#customChars', el => el.value);
  results.push({{test: 'Hex64 preset sets custom chars', pass: customCharsVal === '0123456789abcdef', detail: customCharsVal}});
  
  // Test 10: Check strength bars
  const strengthBars = await page.$$('.pw-strength-bar');
  results.push({{test: 'Strength bars rendered', pass: strengthBars.length > 0, detail: strengthBars.length + ' bars'}});
  
  // Test 11: Stats bar
  const stats = await page.$eval('#statsBar', el => el.innerHTML);
  results.push({{test: 'Stats bar populated', pass: stats.includes('熵') || stats.includes('bit'), detail: 'has content'}});
  
  // Summary
  const passed = results.filter(r => r.pass).length;
  const total = results.length;
  console.log(JSON.stringify({{results, passed, total, allPass: passed === total}}));
  
  await browser.close();
}})();
    '''],
        capture_output=True, text=True, timeout=30
    )
    return result.stdout.strip()

if __name__ == '__main__':
    output = run_js('')
    print(output)
