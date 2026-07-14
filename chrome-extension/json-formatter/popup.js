/* ===================================================================
 * JSON 格式化工具 - Chrome 扩展 popup 逻辑
 * 复用工具站 free-toolbase.com/json-formatter/ 的核心算法
 * 纯前端，零依赖，数据完全本地处理
 * =================================================================== */
(function () {
'use strict';

const els = {
  jsonInput: document.getElementById('jsonInput'),
  formattedOutput: document.getElementById('formattedOutput'),
  treeOutput: document.getElementById('treeOutput'),
  messageBox: document.getElementById('messageBox'),
  statsBar: document.getElementById('statsBar'),
  statNodes: document.getElementById('statNodes'),
  statDepth: document.getElementById('statDepth'),
  statObjects: document.getElementById('statObjects'),
  statArrays: document.getElementById('statArrays'),
  statLength: document.getElementById('statLength'),
  inputCount: document.getElementById('inputCount'),
};

let currentOutputText = '';

// ========== HTML 转义 ==========
function escapeHtml(str) {
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');
}

// ========== JSON 解析 + 错误定位 (复用工具站逻辑) ==========
function parseJSONWithPosition(text) {
  try {
    return { data: JSON.parse(text), error: null };
  } catch (e) {
    const pos = extractErrorPosition(e, text);
    return { data: null, error: { message: e.message, line: pos.line, col: pos.col, snippet: pos.snippet } };
  }
}

function extractErrorPosition(e, text) {
  const m = e.message.match(/position (\d+)/);
  if (m) {
    return getLineCol(text, parseInt(m[1], 10));
  }
  const um = e.message.match(/Unexpected (token|character).*?at position (\d+)/i);
  if (um) {
    return getLineCol(text, parseInt(um[2], 10));
  }
  return getLineCol(text, 0);
}

function getLineCol(text, index) {
  let line = 1, col = 1;
  for (let i = 0; i < Math.min(index, text.length); i++) {
    if (text[i] === '\n') { line++; col = 1; } else { col++; }
  }
  const lines = text.split('\n');
  const start = Math.max(0, line - 2);
  const end = Math.min(lines.length, line + 1);
  const snippet = lines.slice(start, end).map((l, i) => {
    const num = start + i + 1;
    const isBad = num === line;
    return `<span class="${isBad ? 'line-bad' : ''}"><span class="line-num">${num}</span>${escapeHtml(l)}</span>`;
  }).join('\n');
  return { line, col, snippet };
}

// ========== 格式化 / 压缩 ==========
function formatJSON(text, indent) {
  const parsed = parseJSONWithPosition(text);
  if (parsed.error) return { success: false, error: parsed.error };
  return { success: true, data: parsed.data, formatted: JSON.stringify(parsed.data, null, indent || 2) };
}

function minifyJSON(text) {
  const parsed = parseJSONWithPosition(text);
  if (parsed.error) return { success: false, error: parsed.error };
  return { success: true, data: parsed.data, formatted: JSON.stringify(parsed.data) };
}

// ========== 统计 (复用工具站逻辑) ==========
function computeStats(obj) {
  const stats = { nodes: 0, depth: 0, objects: 0, arrays: 0, strings: 0, numbers: 0, bools: 0 };
  function walk(v, d) {
    stats.nodes++;
    stats.depth = Math.max(stats.depth, d);
    if (v === null || typeof v === 'boolean') { stats.bools++; }
    else if (typeof v === 'number') { stats.numbers++; }
    else if (typeof v === 'string') { stats.strings++; }
    else if (Array.isArray(v)) {
      stats.arrays++;
      v.forEach(item => walk(item, d + 1));
    } else if (typeof v === 'object') {
      stats.objects++;
      Object.values(v).forEach(item => walk(item, d + 1));
    }
  }
  walk(obj, 1);
  return stats;
}

function showStats(stats, len) {
  els.statNodes.textContent = stats.nodes;
  els.statDepth.textContent = stats.depth;
  els.statObjects.textContent = stats.objects;
  els.statArrays.textContent = stats.arrays;
  els.statLength.textContent = len;
  els.statsBar.classList.add('show');
}

// ========== 树状视图 (复用工具站逻辑，适配 popup 紧凑布局) ==========
function renderTreeView(obj) {
  let idCounter = 0;
  function build(value, key) {
    const id = 'tree_' + (idCounter++);
    const line = document.createElement('div');
    line.className = 'tree-line';

    if (value === null) {
      line.innerHTML = `${key ? '<span class="tree-key">' + escapeHtml(key) + ': </span>' : ''}<span class="tree-null">null</span><span class="tree-type">null</span>`;
      return line;
    }
    if (typeof value === 'boolean') {
      line.innerHTML = `${key ? '<span class="tree-key">' + escapeHtml(key) + ': </span>' : ''}<span class="tree-boolean">' + value + '</span><span class="tree-type">boolean</span>`;
      return line;
    }
    if (typeof value === 'number') {
      line.innerHTML = `${key ? '<span class="tree-key">' + escapeHtml(key) + ': </span>' : ''}<span class="tree-number">' + value + '</span><span class="tree-type">number</span>`;
      return line;
    }
    if (typeof value === 'string') {
      const short = value.length > 120 ? escapeHtml(value.slice(0, 120)) + '…' : escapeHtml(value);
      line.innerHTML = `${key ? '<span class="tree-key">' + escapeHtml(key) + ': </span>' : ''}<span class="tree-string">"' + short + '"</span><span class="tree-type">string(' + value.length + ')</span>`;
      return line;
    }

    const isArr = Array.isArray(value);
    const len = isArr ? value.length : Object.keys(value).length;
    const open = isArr ? '[' : '{';
    const close = isArr ? ']' : '}';

    if (len === 0) {
      line.innerHTML = `${key ? '<span class="tree-key">' + escapeHtml(key) + ': </span>' : ''}<span class="tree-bracket">${open}${close}</span><span class="tree-type">${isArr ? 'array(0)' : 'object(0)'}</span>`;
      return line;
    }

    const toggle = document.createElement('span');
    toggle.className = 'tree-toggle';
    toggle.textContent = '▼';
    toggle.dataset.target = id;
    toggle.onclick = function () {
      const target = document.getElementById(this.dataset.target);
      if (target.classList.toggle('collapsed')) {
        this.textContent = '▶';
      } else {
        this.textContent = '▼';
      }
    };

    line.appendChild(toggle);
    if (key) {
      line.innerHTML += '<span class="tree-key">' + escapeHtml(key) + ': </span>';
    }
    const bracket = document.createElement('span');
    bracket.className = 'tree-bracket';
    bracket.textContent = open + ' ' + len + ' items ' + close;
    line.appendChild(bracket);

    const children = document.createElement('div');
    children.className = 'tree-children';
    children.id = id;

    if (isArr) {
      value.forEach((item, i) => children.appendChild(build(item, '[' + i + ']')));
    } else {
      Object.keys(value).forEach(k => children.appendChild(build(value[k], k)));
    }

    const wrapper = document.createElement('div');
    wrapper.appendChild(line);
    wrapper.appendChild(children);
    return wrapper;
  }

  const root = document.createElement('div');
  root.appendChild(build(obj, null));
  return root;
}

// ========== 消息提示 ==========
function clearMessage() {
  els.messageBox.innerHTML = '';
}

function showError(err) {
  clearMessage();
  const div = document.createElement('div');
  div.className = 'msg msg-error';
  div.innerHTML =
    '<div class="err-title">❌ JSON 语法错误</div>' +
    '<div>' + escapeHtml(err.message) + '</div>' +
    '<div class="err-pos">行 ' + err.line + '，列 ' + err.col + '</div>' +
    '<div class="msg-error-context"><pre>' + err.snippet + '</pre></div>';
  els.messageBox.appendChild(div);
  els.statsBar.classList.remove('show');
}

function showSuccess(msg) {
  clearMessage();
  const div = document.createElement('div');
  div.className = 'msg msg-success';
  div.textContent = '✅ ' + msg;
  els.messageBox.appendChild(div);
}

function flashBtn(btn, text, isOk) {
  const orig = btn.textContent;
  btn.textContent = text;
  btn.classList.toggle('success', isOk);
  setTimeout(() => { btn.textContent = orig; btn.classList.remove('success'); }, 1500);
}

// ========== 输出更新 ==========
function updateOutputs(data, formatted) {
  currentOutputText = formatted;
  els.formattedOutput.value = formatted;
  els.treeOutput.innerHTML = '';
  els.treeOutput.appendChild(renderTreeView(data));
  const stats = computeStats(data);
  showStats(stats, formatted.length);
  clearMessage();
}

// ========== 输入字符计数 ==========
function updateInputCount() {
  const len = els.jsonInput.value.length;
  els.inputCount.textContent = len + ' 字符';
}

// ========== 事件绑定 ==========

// 格式化
document.getElementById('btnFormat').onclick = function () {
  const text = els.jsonInput.value;
  if (!text.trim()) { showSuccess('请先输入 JSON 数据'); return; }
  const res = formatJSON(text, 2);
  if (!res.success) { showError(res.error); return; }
  updateOutputs(res.data, res.formatted);
};

// 压缩
document.getElementById('btnMinify').onclick = function () {
  const text = els.jsonInput.value;
  if (!text.trim()) { showSuccess('请先输入 JSON 数据'); return; }
  const res = minifyJSON(text);
  if (!res.success) { showError(res.error); return; }
  updateOutputs(res.data, res.formatted);
};

// 验证
document.getElementById('btnValidate').onclick = function () {
  const text = els.jsonInput.value;
  if (!text.trim()) { showSuccess('请先输入 JSON 数据'); return; }
  const parsed = parseJSONWithPosition(text);
  if (parsed.error) {
    showError(parsed.error);
  } else {
    showSuccess('JSON 语法验证通过！数据格式正确。');
    const stats = computeStats(parsed.data);
    showStats(stats, text.length);
  }
};

// 复制结果
document.getElementById('btnCopy').onclick = async function () {
  const text = els.formattedOutput.value;
  if (!text) { flashBtn(this, '⚠️ 无内容', false); return; }
  let ok = false;
  try { await navigator.clipboard.writeText(text); ok = true; } catch (e) {}
  if (!ok) {
    // popup 中 execCommand 兜底
    const ta = document.createElement('textarea');
    ta.value = text;
    ta.style.position = 'fixed';
    ta.style.opacity = '0';
    document.body.appendChild(ta);
    ta.select();
    try { ok = document.execCommand('copy'); } catch (e) {}
    document.body.removeChild(ta);
  }
  flashBtn(this, ok ? '✅ 已复制' : '❌ 失败', ok);
};

// 清空
document.getElementById('btnClear').onclick = function () {
  els.jsonInput.value = '';
  els.formattedOutput.value = '';
  els.treeOutput.innerHTML = '';
  els.messageBox.innerHTML = '';
  els.statsBar.classList.remove('show');
  currentOutputText = '';
  updateInputCount();
  els.jsonInput.focus();
};

// 粘贴 (从剪贴板)
document.getElementById('btnPaste').onclick = async function () {
  let text = '';
  try { text = await navigator.clipboard.readText(); } catch (e) {}
  if (text) {
    els.jsonInput.value = text;
    updateInputCount();
    flashBtn(this, '✅ 已粘贴', true);
  } else {
    // 读取剪贴板在 popup 失焦时可能失败，提示手动粘贴
    flashBtn(this, '⚠️ 请用 Ctrl+V', false);
    els.jsonInput.focus();
  }
};

// Tab 切换
document.querySelectorAll('.tab-btn').forEach(btn => {
  btn.onclick = function () {
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
    this.classList.add('active');
    document.getElementById('tab-' + this.dataset.tab).classList.add('active');
  };
});

// 输入实时字符计数
els.jsonInput.addEventListener('input', updateInputCount);

// Ctrl+Enter 快捷格式化
els.jsonInput.addEventListener('keydown', function (e) {
  if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
    e.preventDefault();
    document.getElementById('btnFormat').click();
  }
});

// 底部链接：在新标签打开 (popup 中 a 标签 target=_blank 由浏览器处理)
// 额外提供 click 兜底，确保关闭 popup 后能打开
document.getElementById('siteLink').addEventListener('click', function (e) {
  const url = this.href;
  if (chrome && chrome.tabs && chrome.tabs.create) {
    e.preventDefault();
    chrome.tabs.create({ url: url });
  }
});

// ========== 初始化：载入示例数据并自动格式化 ==========
const SAMPLE = JSON.stringify({
  name: "在线小工具矩阵",
  version: "1.0.0",
  tools: [
    { id: "password-generator", name: "密码生成器", category: "安全工具" },
    { id: "qr-generator", name: "二维码生成器", category: "开发工具" }
  ],
  features: { offline: true, openSource: false, api: null },
  stats: { totalTools: 2, dailyUsers: 150 }
}, null, 2);

els.jsonInput.value = SAMPLE;
updateInputCount();
setTimeout(() => document.getElementById('btnFormat').click(), 50);

})();
