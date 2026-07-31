/**
 * Puppeteer行为测试 - 用真实Chrome验证工具功能
 * 
 * 测试层级：
 * L0 冒烟：页面加载无JS报错
 * L1 交互：输入→点击→有输出
 * L2 断言：输入→输出值正确
 * 
 * 用法：node tests/puppeteer_test.js [--level L0|L1|L2] [--sample N] [--tool name]
 */
const puppeteer = require('puppeteer-core');
const fs = require('fs');
const path = require('path');

const SITE = path.resolve(__dirname, '..');
const CHROME_PATH = '/opt/google/chrome/chrome';
const results = { pass: 0, fail: 0, skip: 0, error: 0 };
const failures = [];

// ============ 工具行为定义 ============
const TOOL_TESTS = {
  'base64-encoder-decoder': {
    L1: { selector: 'textarea', input: 'hello', btnText: '编码', outputSelector: '#result,.result,.output,textarea[readonly],.output-textarea' },
    L2: { selector: 'textarea', input: 'hello', btnText: '编码', outputContains: 'aGVsbG8=' },
  },
  'url-encode-decode': {
    L1: { selector: 'textarea', input: 'hello world', btnText: '编码', outputSelector: '#result,.result,.output,textarea[readonly]' },
    L2: { selector: 'textarea', input: 'hello world', btnText: '编码', outputContains: 'hello%20world' },
  },
  'percentage-calculator': {
    L1: { selector: 'input[type="number"],input[type="text"]', input: '50', btnText: '计算', outputSelector: '#result,.result,.output' },
  },
  'bmi-calculator': {
    L1: { selector: 'input[type="number"]', input: '70', btnText: '计算', outputSelector: '#result,.result,.output' },
  },
  'password-generator': {
    L1: { btnText: '生成', outputSelector: '#result,.result,.output,input[readonly],textarea[readonly]' },
  },
  'json-formatter': {
    L1: { selector: 'textarea', input: '{"a":1}', btnText: '格式化', outputSelector: '#formattedOutput,#rawOutput,.raw-output,textarea[readonly]' },
  },
  'color-converter': {
    L1: { selector: 'input[type="text"],input[type="color"]', input: '#ff0000', btnText: '转换', outputSelector: '#result,.result,.output' },
  },
  'hash-generator': {
    L1: { selector: 'textarea,input[type="text"]', input: 'hello', btnText: '计算', outputSelector: '#text_md5,#text_sha256,.hash-value' },
  },
  'word-counter': {
    L1: { selector: 'textarea', input: 'hello world test', noButton: true, outputSelector: '#wc-chars,#wc-words,#wc-sentences', outputContains: 'hello world test' },
  },
  'character-counter': {
    L1: { selector: 'textarea', input: 'hello', outputSelector: '#result,.result,.output' },
  },
  'tip-calculator': {
    L1: { selector: 'input[type="number"]', input: '100', btnText: '计算', outputSelector: '#result,.result,.output' },
  },
  'discount-calculator': {
    L1: { selector: 'input[type="number"]', input: '100', btnText: '计算', outputSelector: '#result,.result,.output' },
  },
  'age-calculator': {
    L1: { selector: 'input[type="date"],input[type="text"]', input: '2000-01-01', btnText: '计算', outputSelector: '#result,.result,.output' },
  },
  'css-box-shadow': {
    L1: { skip: true },
  },
  'css-gradient': {
    L1: { skip: true },
  },
};

// ============ 通用L0测试 ============
async function testL0(page, toolName) {
  const filePath = `file://${SITE}/${toolName}/index.html`;
  
  // 收集JS错误
  const jsErrors = [];
  page.on('pageerror', err => jsErrors.push(err.message));
  
  // 收集console错误
  const consoleErrors = [];
  page.on('console', msg => {
    if (msg.type() === 'error') consoleErrors.push(msg.text());
  });
  
  try {
    await page.goto(filePath, { waitUntil: 'load', timeout: 10000 });
  } catch (e) {
    return { result: 'fail', reason: `加载失败: ${e.message.slice(0, 80)}` };
  }
  
  // 检查h1
  const h1 = await page.$('h1');
  if (!h1) return { result: 'fail', reason: '缺少h1' };
  
  // 检查JS错误
  if (jsErrors.length > 0) {
    const err = jsErrors[0].slice(0, 100);
    return { result: 'fail', reason: `JS错误: ${err}` };
  }
  
  // L0.5: 检测onclick/oninput绑定的函数是否存在
  try {
    const missingFns = await page.evaluate(() => {
      const missing = [];
      // 检查所有onclick
      document.querySelectorAll('[onclick]').forEach(el => {
        const onclick = el.getAttribute('onclick');
        const fnMatch = onclick.match(/(\w+)\s*\(/);
        // SKIP: 'this.xxx.method()' patterns — these are DOM API calls, not global functions
        const onclickRaw = onclick.trim();
        const isThisMethod = /^this\.\w+\.\w+\s*\(/.test(onclickRaw);
        if (fnMatch && !isThisMethod && typeof window[fnMatch[1]] !== 'function') {
          // 排除DOM API和内置对象
          const domApis = ['document','window','navigator','console','Math','JSON','parseInt','parseFloat','isNaN','alert','confirm','prompt','this','true','false','null','undefined',
            'event','stopPropagation','preventDefault','toggle'];
          if (!domApis.includes(fnMatch[1]) && !fnMatch[1].startsWith('get') && !fnMatch[1].startsWith('set') && !fnMatch[1].startsWith('create') && !fnMatch[1].startsWith('remove')) {
            missing.push(fnMatch[1]);
          }
        }
      });
      // 检查所有oninput
      document.querySelectorAll('[oninput]').forEach(el => {
        const oninput = el.getAttribute('oninput');
        const fnMatch = oninput.match(/(\w+)\s*\(/);
        const oninputRaw = oninput.trim();
        const isThisMethod = /^this\.\w+\.\w+\s*\(/.test(oninputRaw);
        if (fnMatch && !isThisMethod && typeof window[fnMatch[1]] !== 'function') {
          const domApis = ['document','window','navigator','console','Math','JSON','parseInt','parseFloat','isNaN','alert','confirm','prompt','this','true','false','null','undefined',
            'event','stopPropagation','preventDefault','toggle'];
          if (!domApis.includes(fnMatch[1]) && !fnMatch[1].startsWith('get') && !fnMatch[1].startsWith('set') && !fnMatch[1].startsWith('create') && !fnMatch[1].startsWith('remove')) {
            missing.push(fnMatch[1]);
          }
        }
      });
      // 检查所有onchange
      document.querySelectorAll('[onchange]').forEach(el => {
        const onchange = el.getAttribute('onchange');
        const fnMatch = onchange.match(/(\w+)\s*\(/);
        const onchangeRaw = onchange.trim();
        const isThisMethod = /^this\.\w+\.\w+\s*\(/.test(onchangeRaw);
        if (fnMatch && !isThisMethod && typeof window[fnMatch[1]] !== 'function') {
          const domApis = ['document','window','navigator','console','Math','JSON','parseInt','parseFloat','isNaN','alert','confirm','prompt','this','true','false','null','undefined',
            'event','stopPropagation','preventDefault','toggle'];
          if (!domApis.includes(fnMatch[1]) && !fnMatch[1].startsWith('get') && !fnMatch[1].startsWith('set') && !fnMatch[1].startsWith('create') && !fnMatch[1].startsWith('remove')) {
            missing.push(fnMatch[1]);
          }
        }
      });
      return [...new Set(missing)];
    });
    if (missingFns.length > 0) {
      return { result: 'fail', reason: `JS错误: ${missingFns[0]} is not defined (event handler)` };
    }
  } catch(e) {
    // 检测失败不影响L0结果
  }
  
  return { result: 'pass' };
}

// ============ 通用L1测试（自动，无需手动定义） ============
async function testGenericL1(page, toolName) {
  const filePath = `file://${SITE}/${toolName}/index.html`;
  const jsErrors = [];
  page.on('pageerror', err => jsErrors.push(err.message));
  
  try {
    await page.goto(filePath, { waitUntil: 'load', timeout: 10000 });
  } catch (e) {
    return { result: 'fail', reason: '加载失败' };
  }
  
  // 1. 找第一个输入框，填测试值
  const hasInput = await page.evaluate(() => {
    const inputs = document.querySelectorAll('input[type="text"], input[type="number"], input:not([type]), textarea, select');
    return inputs.length > 0;
  });
  
  if (!hasInput) {
    return { result: 'skip', reason: '无输入框' };
  }
  
  // 填入测试值
  await page.evaluate(() => {
    const inputs = document.querySelectorAll('input[type="text"], input[type="number"], input:not([type]), textarea');
    inputs.forEach(el => {
      if (el.tagName === 'TEXTAREA') {
        el.value = 'test input';
        el.dispatchEvent(new Event('input', { bubbles: true }));
      } else if (el.type === 'number') {
        el.value = '42';
        el.dispatchEvent(new Event('input', { bubbles: true }));
      } else {
        el.value = 'test';
        el.dispatchEvent(new Event('input', { bubbles: true }));
      }
    });
    // select选第一个非空选项
    document.querySelectorAll('select').forEach(sel => {
      if (sel.options.length > 1) {
        sel.selectedIndex = 1;
        sel.dispatchEvent(new Event('change', { bubbles: true }));
      }
    });
  });
  
  await new Promise(r => setTimeout(r, 300));
  
  // 2. 点击主按钮
  const btnClicked = await page.evaluate(() => {
    const btns = document.querySelectorAll('button');
    // 优先找"计算/生成/转换/编码/解码/分析"类按钮
    const actionBtn = Array.from(btns).find(b => 
      /计算|生成|转换|编码|解码|分析|处理|开始|运行|执行|提交|generate|convert|calculate|encode|decode|analyze|process|run|start|submit/i.test(b.textContent)
    );
    if (actionBtn) { actionBtn.click(); return true; }
    // 没找到就点第一个非reset非copy按钮
    const firstBtn = Array.from(btns).find(b => 
      !/reset|clear|copy|复制|重置|清空/i.test(b.textContent)
    );
    if (firstBtn) { firstBtn.click(); return true; }
    return false;
  });
  
  await new Promise(r => setTimeout(r, 500));
  
  // 3. 检查JS错误
  if (jsErrors.length > 0) {
    return { result: 'fail', reason: `交互JS错误: ${jsErrors[0].slice(0, 80)}` };
  }
  
  // 4. 检查输出
  const hasOutput = await page.evaluate(() => {
    // 找输出区域
    const outputEls = document.querySelectorAll(
      '[id*="result"],[id*="output"],[id*="display"],[id*="preview"],[id*="code"],[class*="result"],[class*="output"],textarea[readonly],.result-box,.output-box'
    );
    for (const el of outputEls) {
      const text = (el.textContent || el.value || '').trim();
      if (text && text.length > 0 && text !== '结果将显示在这里' && text !== 'Results will appear here') {
        return true;
      }
    }
    return false;
  });
  
  if (!hasOutput && btnClicked) {
    return { result: 'fail', reason: '点击按钮后无输出' };
  }
  
  return { result: 'pass' };
}

// ============ 通用L1/L2测试 ============
async function testBehavior(page, toolName, level) {
  const testDef = TOOL_TESTS[toolName];
  
  // 通用L1：没有手动定义的工具也能测
  if (!testDef || !testDef[level]) {
    if (level === 'L1') {
      return await testGenericL1(page, toolName);
    }
    return { result: 'skip' };
  }
  
  const test = testDef[level];
  
  // Skip check
  if (test.skip) {
    return { result: 'skip', reason: '配置跳过' };
  }
  
  const filePath = `file://${SITE}/${toolName}/index.html`;
  
  const jsErrors = [];
  page.on('pageerror', err => jsErrors.push(err.message));
  
  try {
    await page.goto(filePath, { waitUntil: 'load', timeout: 10000 });
  } catch (e) {
    return { result: 'fail', reason: `加载失败` };
  }
  
  // 输入
  if (test.selector && test.input) {
    const input = await page.$(test.selector);
    if (input) {
      await input.click({ clickCount: 3 });
      // Clear existing content before typing for accuracy
      await input.evaluate(el => el.value = '');
      await input.type(test.input);
    }
  }
  
  // 点击按钮
  if (test.btnText) {
    const btn = await page.evaluateHandle((text) => {
      const buttons = document.querySelectorAll('button');
      for (const b of buttons) {
        if (b.textContent.includes(text)) return b;
      }
      return null;
    }, test.btnText);
    
    if (btn && btn.asElement()) {
      await btn.asElement().click();
      await await new Promise(r=>setTimeout(r,200));
    }
  }
  
  // 检查JS错误
  if (jsErrors.length > 0) {
    return { result: 'fail', reason: `JS错误: ${jsErrors[0].slice(0, 80)}` };
  }
  
  // 检查输出
  if (test.outputSelector) {
    const output = await page.$(test.outputSelector);
    if (!output) {
      // 尝试更宽泛的选择器
      const anyOutput = await page.evaluate(() => {
        const els = document.querySelectorAll('[id*="result"],[id*="output"],[class*="result"],[class*="output"],textarea[readonly]');
        for (const el of els) {
          const text = el.textContent.trim() || el.value;
          if (text && text.length > 0) return text.slice(0, 200);
        }
        return null;
      });
      
      if (!anyOutput) {
        return { result: 'fail', reason: '无输出' };
      }
      
      if (level === 'L2' && test.outputContains && !anyOutput.includes(test.outputContains)) {
        return { result: 'fail', reason: `输出不含"${test.outputContains}"` };
      }
    } else {
      const outputText = await page.evaluate(el => (el.textContent.trim() || el.value || '').slice(0, 200), output);
      if (!outputText) {
        return { result: 'fail', reason: '输出为空' };
      }
      if (level === 'L2' && test.outputContains && !outputText.includes(test.outputContains)) {
        return { result: 'fail', reason: `输出不含"${test.outputContains}"` };
      }
    }
  }
  
  return { result: 'pass' };
}

// ============ 主流程 ============
async function main() {
  const args = process.argv.slice(2);
  let level = 'L0';
  let sample = 0;
  let singleTool = null;
  
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--level') level = args[++i];
    if (args[i] === '--sample') sample = parseInt(args[++i]);
    if (args[i] === '--tool') singleTool = args[++i];
  }
  
  // 获取工具列表
  let tools;
  if (singleTool) {
    tools = [singleTool];
  } else if (level === 'L0') {
    // L0测所有非noindex/非重定向页面
    tools = fs.readdirSync(SITE).filter(d => {
      const f = path.join(SITE, d, 'index.html');
      if (!fs.existsSync(f)) return false;
      const c = fs.readFileSync(f, 'utf8');
      return !c.includes('noindex') && !c.includes('http-equiv="refresh"') && 
             !['about','blog','contact','privacy','terms','css','data'].includes(d);
    });
  } else {
    tools = Object.keys(TOOL_TESTS);
  }
  
  if (sample > 0 && sample < tools.length) {
    tools = tools.sort(() => Math.random() - 0.5).slice(0, sample);
  }
  
  console.log(`\n🧪 Puppeteer行为测试 - Level ${level}`);
  console.log(`   工具数: ${tools.length}`);
  console.log('─'.repeat(50));
  
  const browser = await puppeteer.launch({
    executablePath: CHROME_PATH,
    headless: 'new',
    args: [
      '--no-sandbox', '--disable-setuid-sandbox', '--disable-gpu', '--disable-dev-shm-usage'
    ]
  });
  
  let tested = 0;
  for (const tool of tools) {
    let res;
    let page;
    try {
      page = await browser.newPage();
      await page.setViewport({ width: 1280, height: 720 });
      if (level === 'L0') {
        res = await testL0(page, tool);
      } else {
        res = await testBehavior(page, tool, level);
      }
    } catch (e) {
      res = { result: 'error', reason: e.message.slice(0, 80) };
    }
    
    // 关闭page防止detached frame
    try { await page.close(); } catch(e) {}
    
    tested++;
    results[res.result]++;
    
    if (res.result === 'pass') {
      console.log(`  ✅ ${tool}`);
    } else if (res.result === 'skip') {
      console.log(`  ⏭️  ${tool} (无测试定义)`);
    } else {
      failures.push({ tool, level, reason: res.reason || res.result });
      console.log(`  ❌ ${tool}: ${res.reason || res.result}`);
    }
  }
  
  await browser.close();
  
  console.log('─'.repeat(50));
  const total = results.pass + results.fail + results.error;
  const rate = total > 0 ? (results.pass / total * 100).toFixed(1) : 0;
  console.log(`\n结果: ${results.pass}/${total} 通过 (${rate}%) | skip: ${results.skip}`);
  
  if (failures.length > 0 && failures.length <= 50) {
    console.log('\n失败列表:');
    for (const f of failures) {
      console.log(`  ${f.tool}: ${f.reason}`);
    }
  } else if (failures.length > 50) {
    console.log(`\n失败列表(前50/${failures.length}):`);
    for (const f of failures.slice(0, 50)) {
      console.log(`  ${f.tool}: ${f.reason}`);
    }
  }
  
  // 保存报告
  const report = { level, total: tested, pass: results.pass, fail: results.fail, error: results.error, skip: results.skip, rate, failures, timestamp: new Date().toISOString() };
  const reportDir = path.join(SITE, 'quality-reports');
  if (!fs.existsSync(reportDir)) fs.mkdirSync(reportDir, { recursive: true });
  fs.writeFileSync(path.join(reportDir, `puppeteer-${level}.json`), JSON.stringify(report, null, 2));
  
  process.exit(results.fail > 0 ? 1 : 0);
}

main().catch(e => { console.error(e); process.exit(2); });
