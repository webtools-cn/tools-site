/**
 * 行为测试框架 - 用Node.js+jsdom模拟浏览器，验证工具功能
 * 
 * 测试层级：
 * L0 冒烟测试：页面能加载，JS无报错
 * L1 交互测试：输入→点击→有输出
 * L2 断言测试：输入→输出值正确
 * 
 * 用法：node tests/behavior_test.js [--level L0|L1|L2] [--sample N] [--tool name]
 */
const fs = require('fs');
const path = require('path');
const { JSDOM } = require('jsdom');

const SITE = path.resolve(__dirname, '..');
const results = { L0: { pass: 0, fail: 0 }, L1: { pass: 0, fail: 0 }, L2: { pass: 0, fail: 0 } };
const failures = [];

// ============ 工具行为定义 ============
// 每个工具定义：输入→预期输出
const TOOL_TESTS = {
  // === 编码/解码类 ===
  'base64-encode': {
    L1: { input: () => 'hello', action: 'encode', expectOutput: true },
    L2: { input: () => 'hello', action: 'encode', expectValue: 'aGVsbG8=' },
  },
  'base64-encoder-decoder': {
    L1: { input: () => 'test123', action: 'encode', expectOutput: true },
    L2: { input: () => 'test123', action: 'encode', expectValue: 'dGVzdDEyMw==' },
  },
  'url-encode-decode': {
    L1: { input: () => 'hello world', action: 'encode', expectOutput: true },
    L2: { input: () => 'hello world', action: 'encode', expectValue: 'hello%20world' },
  },
  'html-entity-encoder': {
    L1: { input: () => '<div>', action: 'encode', expectOutput: true },
    L2: { input: () => '<div>', action: 'encode', expectValue: '&lt;div&gt;' },
  },
  
  // === 文本转换类 ===
  'text-case': {
    L1: { input: () => 'hello world', action: 'uppercase', expectOutput: true },
    L2: { input: () => 'hello world', action: 'uppercase', expectValue: 'HELLO WORLD' },
  },
  'text-to-slug': {
    L1: { input: () => 'Hello World!', action: 'convert', expectOutput: true },
    L2: { input: () => 'Hello World!', action: 'convert', expectValue: 'hello-world' },
  },
  'backwards-text': {
    L1: { input: () => 'abc', action: 'reverse', expectOutput: true },
    L2: { input: () => 'abc', action: 'reverse', expectValue: 'cba' },
  },
  'word-counter': {
    L1: { input: () => 'hello world test', action: 'count', expectOutput: true },
    L2: { input: () => 'hello world test', action: 'count', expectContains: '3' },
  },
  'character-counter': {
    L1: { input: () => 'hello', action: 'count', expectOutput: true },
    L2: { input: () => 'hello', action: 'count', expectContains: '5' },
  },
  'reading-time': {
    L1: { input: () => 'This is a test paragraph with some words.', action: 'calculate', expectOutput: true },
  },
  'number-to-words': {
    L1: { input: () => '123', action: 'convert', expectOutput: true },
    L2: { input: () => '123', action: 'convert', expectContains: '一百' },
  },
  'number-base': {
    L1: { input: () => '255', action: 'convert', expectOutput: true },
    L2: { input: () => '255', action: 'convert', expectContains: 'FF' },
  },
  
  // === 计算器类 ===
  'percentage-calculator': {
    L1: { input: () => '50', input2: () => '200', action: 'calculate', expectOutput: true },
    L2: { input: () => '50', input2: () => '200', action: 'calculate', expectContains: '100' },
  },
  'bmi-calculator': {
    L1: { input: () => '70', input2: () => '175', action: 'calculate', expectOutput: true },
  },
  'age-calculator': {
    L1: { input: () => '2000-01-01', action: 'calculate', expectOutput: true },
  },
  'tip-calculator': {
    L1: { input: () => '100', input2: () => '15', action: 'calculate', expectOutput: true },
    L2: { input: () => '100', input2: () => '15', action: 'calculate', expectContains: '15' },
  },
  'discount-calculator': {
    L1: { input: () => '100', input2: () => '20', action: 'calculate', expectOutput: true },
    L2: { input: () => '100', input2: () => '20', action: 'calculate', expectContains: '80' },
  },
  
  // === 密码/安全类 ===
  'password-generator': {
    L1: { action: 'generate', expectOutput: true },
  },
  'password-strength-meter': {
    L1: { input: () => 'Test123!', action: 'check', expectOutput: true },
  },
  'hash-generator': {
    L1: { input: () => 'hello', action: 'generate', expectOutput: true },
  },
  
  // === JSON工具类 ===
  'json-formatter': {
    L1: { input: () => '{"a":1}', action: 'format', expectOutput: true },
    L2: { input: () => '{"a":1}', action: 'format', expectContains: '"a"' },
  },
  'json-to-csv': {
    L1: { input: () => '[{"name":"test","value":1}]', action: 'convert', expectOutput: true },
  },
  
  // === CSS生成器类 ===
  'css-box-shadow': {
    L1: { action: 'generate', expectOutput: true, expectContains: 'box-shadow' },
  },
  'css-gradient': {
    L1: { action: 'generate', expectOutput: true, expectContains: 'gradient' },
  },
  
  // === 颜色工具类 ===
  'color-picker': {
    L1: { action: 'pick', expectOutput: true },
  },
  'color-converter': {
    L1: { input: () => '#ff0000', action: 'convert', expectOutput: true },
    L2: { input: () => '#ff0000', action: 'convert', expectContains: '255' },
  },
};

// ============ 测试执行 ============

async function loadTool(toolName) {
  const htmlPath = path.join(SITE, toolName, 'index.html');
  if (!fs.existsSync(htmlPath)) return null;
  
  const html = fs.readFileSync(htmlPath, 'utf8');
  
  // 创建jsdom环境
  const dom = new JSDOM(html, {
    runScripts: 'dangerously',
    resources: 'usable',
    pretendToBeVisual: true,
    url: `https://free-toolbase.com/${toolName}/`,
  });
  
  // 模拟clipboard
  dom.window.navigator.clipboard = {
    writeText: () => Promise.resolve(),
    readText: () => Promise.resolve(''),
  };
  
  // 模拟gtag
  dom.window.dataLayer = [];
  dom.window.gtag = function() { dom.window.dataLayer.push(arguments); };
  
  return dom;
}

function findOutput(dom) {
  const doc = dom.window.document;
  // 常见输出区域选择器
  const selectors = [
    '#result', '#output', '#result-content', '#resultContent',
    '#output-text', '#outputText', '#result-text', '#resultText',
    '#result-section .output', '#result-value', '#resultValue',
    '.output', '.result', '.output-textarea',
    '#decoded-text', '#encoded-text', '#converted-text',
    '#generated', '#preview',
  ];
  
  for (const sel of selectors) {
    const el = doc.querySelector(sel);
    if (el && (el.textContent.trim() || el.value)) {
      return el.textContent.trim() || el.value;
    }
  }
  
  // 查找所有textarea（可能是输出）
  const textareas = doc.querySelectorAll('textarea[readonly], textarea.output');
  for (const ta of textareas) {
    if (ta.value.trim()) return ta.value.trim();
  }
  
  return null;
}

function findInput(dom) {
  const doc = dom.window.document;
  const input = doc.querySelector('textarea:not([readonly])') || 
                doc.querySelector('input[type="text"]') ||
                doc.querySelector('input[type="number"]');
  return input;
}

function findButton(dom, action) {
  const doc = dom.window.document;
  const buttons = doc.querySelectorAll('button');
  
  // 按action关键词找按钮
  const actionMap = {
    'encode': ['编码', 'Encode', '加密', 'Encrypt'],
    'decode': ['解码', 'Decode', '解密', 'Decrypt'],
    'convert': ['转换', 'Convert', '生成', 'Generate'],
    'calculate': ['计算', 'Calculate', 'Compute'],
    'format': ['格式化', 'Format', '美化', 'Beautify'],
    'generate': ['生成', 'Generate', 'Create'],
    'count': ['统计', 'Count', '计算', 'Calculate'],
    'check': ['检测', 'Check', '验证', 'Verify'],
    'reverse': ['反转', 'Reverse'],
    'uppercase': ['大写', 'Upper', 'UPPERCASE'],
    'pick': ['选择', 'Pick', 'Generate'],
  };
  
  const keywords = actionMap[action] || [action];
  
  for (const btn of buttons) {
    const text = btn.textContent.trim();
    for (const kw of keywords) {
      if (text.includes(kw)) return btn;
    }
  }
  
  // 没找到关键词匹配，返回第一个非clear/复制按钮
  for (const btn of buttons) {
    const text = btn.textContent.trim().toLowerCase();
    if (!text.includes('clear') && !text.includes('复制') && !text.includes('copy') && !text.includes('重置')) {
      return btn;
    }
  }
  
  return buttons[0] || null;
}

async function runTest(toolName, level) {
  const testDef = TOOL_TESTS[toolName];
  if (!testDef || !testDef[level]) return 'skip';
  
  let dom;
  try {
    dom = await loadTool(toolName);
    if (!dom) return 'skip';
    
    const test = testDef[level];
    const doc = dom.window.document;
    
    // L0: 页面加载无JS报错
    if (level === 'L0') {
      return dom.window.document.querySelector('h1') ? 'pass' : 'fail';
    }
    
    // L1/L2: 输入→操作→检查输出
    if (test.input) {
      const inputEl = findInput(dom);
      if (inputEl) {
        inputEl.value = test.input();
        inputEl.dispatchEvent(new dom.window.Event('input', { bubbles: true }));
      }
    }
    
    if (test.input2) {
      const inputs = doc.querySelectorAll('input[type="number"], input[type="text"]');
      if (inputs[1]) {
        inputs[1].value = test.input2();
        inputs[1].dispatchEvent(new dom.window.Event('input', { bubbles: true }));
      }
    }
    
    // 点击按钮
    const btn = findButton(dom, test.action);
    if (btn) {
      btn.click();
    } else {
      // 尝试直接调用函数
      const funcNames = [test.action, 'runTool', 'process', 'convert', 'calculate', 'generate'];
      for (const fn of funcNames) {
        if (typeof dom.window[fn] === 'function') {
          dom.window[fn]();
          break;
        }
      }
    }
    
    // 等待输出
    await new Promise(r => setTimeout(r, 100));
    
    const output = findOutput(dom);
    
    if (level === 'L1') {
      // L1: 只要有输出就行
      if (test.expectOutput && output && output.length > 0) return 'pass';
      if (test.expectContains && output && output.includes(test.expectContains)) return 'pass';
      if (!test.expectOutput && !test.expectContains) return 'pass';
      return 'fail';
    }
    
    if (level === 'L2') {
      // L2: 输出值必须正确
      if (test.expectValue && output === test.expectValue) return 'pass';
      if (test.expectContains && output && output.includes(test.expectContains)) return 'pass';
      return 'fail';
    }
    
  } catch (e) {
    return 'error: ' + e.message.slice(0, 100);
  } finally {
    if (dom) dom.window.close();
  }
  
  return 'fail';
}

// ============ 主流程 ============

async function main() {
  const args = process.argv.slice(2);
  let level = 'L1';
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
  } else {
    tools = Object.keys(TOOL_TESTS);
    if (sample > 0 && sample < tools.length) {
      // 随机抽样
      tools = tools.sort(() => Math.random() - 0.5).slice(0, sample);
    }
  }
  
  console.log(`\n🧪 行为测试 - Level ${level}`);
  console.log(`   工具数: ${tools.length}`);
  console.log('─'.repeat(50));
  
  for (const tool of tools) {
    const result = await runTest(tool, level);
    if (result === 'pass') {
      results[level].pass++;
      console.log(`  ✅ ${tool}`);
    } else if (result === 'skip') {
      console.log(`  ⏭️  ${tool} (无测试定义)`);
    } else {
      results[level].fail++;
      failures.push({ tool, level, result });
      console.log(`  ❌ ${tool}: ${result}`);
    }
  }
  
  console.log('─'.repeat(50));
  const total = results[level].pass + results[level].fail;
  const rate = total > 0 ? (results[level].pass / total * 100).toFixed(1) : 0;
  console.log(`\n结果: ${results[level].pass}/${total} 通过 (${rate}%)`);
  
  if (failures.length > 0) {
    console.log('\n失败列表:');
    for (const f of failures) {
      console.log(`  ${f.tool} [${f.level}]: ${f.result}`);
    }
  }
  
  // 输出JSON报告
  const report = { level, total, pass: results[level].pass, fail: results[level].fail, rate, failures, timestamp: new Date().toISOString() };
  const reportDir = path.join(SITE, 'quality-reports');
  if (!fs.existsSync(reportDir)) fs.mkdirSync(reportDir, { recursive: true });
  fs.writeFileSync(path.join(reportDir, 'behavior-test.json'), JSON.stringify(report, null, 2));
  
  process.exit(results[level].fail > 0 ? 1 : 0);
}

main().catch(e => { console.error(e); process.exit(2); });
