#!/usr/bin/env python3
"""Build list-diff tool - Compare two lists and find differences"""
import sys, os
sys.path.insert(0, os.path.expanduser('~/tools-site/_gen'))
from tool_template_v3 import ToolPageBuilder

builder = ToolPageBuilder()

# Tool HTML - CN
tool_html_cn = '''
<div class="diff-layout">
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:12px">
    <div class="form-group">
      <label>列表 A（每行一项）</label>
      <textarea id="listA" class="diff-input" placeholder="输入列表A，每行一个项目&#10;例如：&#10;苹果&#10;香蕉&#10;橙子" rows="8">苹果
香蕉
橙子
葡萄
西瓜</textarea>
    </div>
    <div class="form-group">
      <label>列表 B（每行一项）</label>
      <textarea id="listB" class="diff-input" placeholder="输入列表B，每行一个项目&#10;例如：&#10;苹果&#10;橙子&#10;草莓&#10;芒果" rows="8">苹果
橙子
草莓
芒果
香蕉</textarea>
    </div>
  </div>
  <div style="display:flex;gap:8px;margin-bottom:16px;flex-wrap:wrap">
    <button class="btn btn-primary" onclick="compareLists()">🔍 比较列表</button>
    <button class="btn" style="background:#1e293b;color:#94a3b8" onclick="swapLists()">⇄ 交换</button>
    <button class="btn" style="background:#ef4444;color:#fff" onclick="clearLists()">清空</button>
    <label style="color:#94a3b8;font-size:.85rem;display:flex;align-items:center;gap:4px;margin-left:8px">
      <input type="checkbox" id="ignoreCase" checked> 忽略大小写
    </label>
    <label style="color:#94a3b8;font-size:.85rem;display:flex;align-items:center;gap:4px">
      <input type="checkbox" id="trimWhitespace" checked> 去除首尾空格
    </label>
  </div>
  <div class="results-grid" style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px">
    <div class="result-panel" style="background:rgba(16,185,129,.1);border:1px solid rgba(16,185,129,.3);border-radius:8px;padding:12px">
      <h3 style="color:#10b981;font-size:.9rem;margin-bottom:8px">✅ 共同项（交集）</h3>
      <div id="commonItems" class="result-list" style="font-size:.85rem;color:#e2e8f0;min-height:60px;max-height:200px;overflow-y:auto">等待比较...</div>
      <div style="margin-top:8px;color:#64748b;font-size:.8rem">共 <span id="commonCount">0</span> 项</div>
    </div>
    <div class="result-panel" style="background:rgba(239,68,68,.1);border:1px solid rgba(239,68,68,.3);border-radius:8px;padding:12px">
      <h3 style="color:#ef4444;font-size:.9rem;margin-bottom:8px">➖ 仅 A 有（差集）</h3>
      <div id="onlyAItems" class="result-list" style="font-size:.85rem;color:#e2e8f0;min-height:60px;max-height:200px;overflow-y:auto">等待比较...</div>
      <div style="margin-top:8px;color:#64748b;font-size:.8rem">共 <span id="onlyACount">0</span> 项</div>
    </div>
    <div class="result-panel" style="background:rgba(59,130,246,.1);border:1px solid rgba(59,130,246,.3);border-radius:8px;padding:12px">
      <h3 style="color:#3b82f6;font-size:.9rem;margin-bottom:8px">➕ 仅 B 有（新增）</h3>
      <div id="onlyBItems" class="result-list" style="font-size:.85rem;color:#e2e8f0;min-height:60px;max-height:200px;overflow-y:auto">等待比较...</div>
      <div style="margin-top:8px;color:#64748b;font-size:.8rem">共 <span id="onlyBCount">0</span> 项</div>
    </div>
  </div>
  <div style="margin-top:16px;display:flex;gap:8px;flex-wrap:wrap">
    <button class="btn" style="background:#1e293b;color:#94a3b8;font-size:.8rem" onclick="exportResults()">📥 导出结果</button>
    <button class="btn" style="background:#1e293b;color:#94a3b8;font-size:.8rem" onclick="copyResults()">📋 复制结果</button>
  </div>
</div>
<style>
.diff-input{width:100%;padding:10px 14px;background:#0f172a;border:1px solid rgba(148,163,184,.2);border-radius:8px;color:#e2e8f0;font-size:.85rem;font-family:'Consolas','Monaco','Courier New',monospace;outline:none;resize:vertical;transition:all .2s}
.diff-input:focus{border-color:rgba(6,182,212,.4);box-shadow:0 0 0 3px rgba(6,182,212,.1)}
.result-list{font-family:'Consolas','Monaco','Courier New',monospace;line-height:1.7}
.result-list div{padding:2px 0}
.btn{padding:8px 20px;border:none;border-radius:6px;cursor:pointer;font-size:.85rem;transition:all .2s}
.btn:hover{opacity:.85;transform:translateY(-1px)}
.result-panel h3{margin:0}
@media(max-width:600px){.results-grid{grid-template-columns:1fr!important}}
</style>
'''

# Tool HTML - EN
tool_html_en = '''
<div class="diff-layout">
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:12px">
    <div class="form-group">
      <label>List A（one per line）</label>
      <textarea id="listA" class="diff-input" placeholder="Enter list A, one per line&#10;e.g.:&#10;Apple&#10;Banana&#10;Orange" rows="8">Apple
Banana
Orange
Grape
Watermelon</textarea>
    </div>
    <div class="form-group">
      <label>List B（one per line）</label>
      <textarea id="listB" class="diff-input" placeholder="Enter list B, one per line&#10;e.g.:&#10;Apple&#10;Orange&#10;Strawberry&#10;Mango" rows="8">Apple
Orange
Strawberry
Mango
Banana</textarea>
    </div>
  </div>
  <div style="display:flex;gap:8px;margin-bottom:16px;flex-wrap:wrap">
    <button class="btn btn-primary" onclick="compareLists()">🔍 Compare Lists</button>
    <button class="btn" style="background:#1e293b;color:#94a3b8" onclick="swapLists()">⇄ Swap</button>
    <button class="btn" style="background:#ef4444;color:#fff" onclick="clearLists()">Clear</button>
    <label style="color:#94a3b8;font-size:.85rem;display:flex;align-items:center;gap:4px;margin-left:8px">
      <input type="checkbox" id="ignoreCase" checked> Ignore Case
    </label>
    <label style="color:#94a3b8;font-size:.85rem;display:flex;align-items:center;gap:4px">
      <input type="checkbox" id="trimWhitespace" checked> Trim Whitespace
    </label>
  </div>
  <div class="results-grid" style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px">
    <div class="result-panel" style="background:rgba(16,185,129,.1);border:1px solid rgba(16,185,129,.3);border-radius:8px;padding:12px">
      <h3 style="color:#10b981;font-size:.9rem;margin-bottom:8px">✅ Common（Intersection）</h3>
      <div id="commonItems" class="result-list" style="font-size:.85rem;color:#e2e8f0;min-height:60px;max-height:200px;overflow-y:auto">Waiting...</div>
      <div style="margin-top:8px;color:#64748b;font-size:.8rem">Total: <span id="commonCount">0</span></div>
    </div>
    <div class="result-panel" style="background:rgba(239,68,68,.1);border:1px solid rgba(239,68,68,.3);border-radius:8px;padding:12px">
      <h3 style="color:#ef4444;font-size:.9rem;margin-bottom:8px">➖ Only in A（Difference）</h3>
      <div id="onlyAItems" class="result-list" style="font-size:.85rem;color:#e2e8f0;min-height:60px;max-height:200px;overflow-y:auto">Waiting...</div>
      <div style="margin-top:8px;color:#64748b;font-size:.8rem">Total: <span id="onlyACount">0</span></div>
    </div>
    <div class="result-panel" style="background:rgba(59,130,246,.1);border:1px solid rgba(59,130,246,.3);border-radius:8px;padding:12px">
      <h3 style="color:#3b82f6;font-size:.9rem;margin-bottom:8px">➕ Only in B（Added）</h3>
      <div id="onlyBItems" class="result-list" style="font-size:.85rem;color:#e2e8f0;min-height:60px;max-height:200px;overflow-y:auto">Waiting...</div>
      <div style="margin-top:8px;color:#64748b;font-size:.8rem">Total: <span id="onlyBCount">0</span></div>
    </div>
  </div>
  <div style="margin-top:16px;display:flex;gap:8px;flex-wrap:wrap">
    <button class="btn" style="background:#1e293b;color:#94a3b8;font-size:.8rem" onclick="exportResults()">📥 Export</button>
    <button class="btn" style="background:#1e293b;color:#94a3b8;font-size:.8rem" onclick="copyResults()">📋 Copy Results</button>
  </div>
</div>
<style>
.diff-input{width:100%;padding:10px 14px;background:#0f172a;border:1px solid rgba(148,163,184,.2);border-radius:8px;color:#e2e8f0;font-size:.85rem;font-family:'Consolas','Monaco','Courier New',monospace;outline:none;resize:vertical;transition:all .2s}
.diff-input:focus{border-color:rgba(6,182,212,.4);box-shadow:0 0 0 3px rgba(6,182,212,.1)}
.result-list{font-family:'Consolas','Monaco','Courier New',monospace;line-height:1.7}
.result-list div{padding:2px 0}
.btn{padding:8px 20px;border:none;border-radius:6px;cursor:pointer;font-size:.85rem;transition:all .2s}
.btn:hover{opacity:.85;transform:translateY(-1px)}
.result-panel h3{margin:0}
@media(max-width:600px){.results-grid{grid-template-columns:1fr!important}}
</style>
'''

# Tool JS
tool_js = '''
function getList(id) {
  var val = document.getElementById(id).value;
  var trim = document.getElementById('trimWhitespace').checked;
  var lines = val.split('\\n');
  var result = [];
  for (var i = 0; i < lines.length; i++) {
    var line = trim ? lines[i].trim() : lines[i];
    if (line !== '') result.push(line);
  }
  return result;
}
function normalize(str) {
  var ignoreCase = document.getElementById('ignoreCase').checked;
  return ignoreCase ? str.toLowerCase() : str;
}
function compareLists() {
  var listA = getList('listA');
  var listB = getList('listB');
  var normA = listA.map(normalize);
  var normB = listB.map(normalize);
  var common = [], onlyA = [], onlyB = [];
  var aUsed = {}, bUsed = {};
  for (var i = 0; i < normA.length; i++) {
    var found = false;
    for (var j = 0; j < normB.length; j++) {
      if (!bUsed[j] && normA[i] === normB[j]) {
        bUsed[j] = true;
        found = true;
        break;
      }
    }
    if (found) {
      common.push(listA[i]);
    } else {
      onlyA.push(listA[i]);
    }
  }
  for (var j = 0; j < normB.length; j++) {
    if (!bUsed[j]) {
      onlyB.push(listB[j]);
    }
  }
  renderResults(common, onlyA, onlyB);
}
function renderResults(common, onlyA, onlyB) {
  var render = function(arr, id, countId) {
    var html = '';
    for (var i = 0; i < arr.length; i++) {
      html += '<div>' + escapeHtml(arr[i]) + '</div>';
    }
    if (arr.length === 0) html = '<div style="color:#64748b">(empty)</div>';
    document.getElementById(id).innerHTML = html;
    document.getElementById(countId).textContent = arr.length;
  };
  render(common, 'commonItems', 'commonCount');
  render(onlyA, 'onlyAItems', 'onlyACount');
  render(onlyB, 'onlyBItems', 'onlyBCount');
}
function swapLists() {
  var a = document.getElementById('listA').value;
  var b = document.getElementById('listB').value;
  document.getElementById('listA').value = b;
  document.getElementById('listB').value = a;
  compareLists();
}
function clearLists() {
  document.getElementById('listA').value = '';
  document.getElementById('listB').value = '';
  document.getElementById('commonItems').innerHTML = '<div style="color:#64748b">Waiting...</div>';
  document.getElementById('onlyAItems').innerHTML = '<div style="color:#64748b">Waiting...</div>';
  document.getElementById('onlyBItems').innerHTML = '<div style="color:#64748b">Waiting...</div>';
  document.getElementById('commonCount').textContent = '0';
  document.getElementById('onlyACount').textContent = '0';
  document.getElementById('onlyBCount').textContent = '0';
}
function escapeHtml(str) {
  var div = document.createElement('div');
  div.textContent = str;
  return div.innerHTML;
}
function exportResults() {
  var common = document.getElementById('commonItems').innerText;
  var onlyA = document.getElementById('onlyAItems').innerText;
  var onlyB = document.getElementById('onlyBItems').innerText;
  if (common === 'Waiting...' || common === '(empty)') common = '';
  if (onlyA === 'Waiting...' || onlyA === '(empty)') onlyA = '';
  if (onlyB === 'Waiting...' || onlyB === '(empty)') onlyB = '';
  var text = '=== Common Items ===\\n' + common + '\\n\\n=== Only in A ===\\n' + onlyA + '\\n\\n=== Only in B ===\\n' + onlyB;
  var blob = new Blob([text], {type: 'text/plain'});
  var a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'list-diff-result.txt';
  a.click();
  URL.revokeObjectURL(a.href);
  showToast('Exported');
}
function copyResults() {
  var common = document.getElementById('commonItems').innerText;
  var onlyA = document.getElementById('onlyAItems').innerText;
  var onlyB = document.getElementById('onlyBItems').innerText;
  if (common === 'Waiting...' || common === '(empty)') common = '';
  if (onlyA === 'Waiting...' || onlyA === '(empty)') onlyA = '';
  if (onlyB === 'Waiting...' || onlyB === '(empty)') onlyB = '';
  var text = '=== Common Items ===\\n' + common + '\\n\\n=== Only in A ===\\n' + onlyA + '\\n\\n=== Only in B ===\\n' + onlyB;
  navigator.clipboard.writeText(text).then(function() {
    showToast('Copied!');
  }).catch(function() {
    showToast('Copy failed');
  });
}
'''

# FAQs CN
faqs_cn = [
    ('列表比较工具支持哪些格式？', '支持按行分隔的文本列表。每行一个项目，支持中英文、数字、符号等任意字符。结果自动分为共同项、仅A有、仅B有三类展示。'),
    ('可以比较大型列表吗？', '支持比较数千项的列表。但由于纯前端处理，超大列表（超过1万项）可能会有性能影响。建议分批次比较。'),
    ('忽略大小写和空格功能有什么用？', '忽略大小写：比较时"A"和"a"视为相同。去除首尾空格：自动清除每行前后的空格，避免因格式差异导致的误判。'),
    ('数据会上传到服务器吗？', '不会。所有比较操作在浏览器本地完成，数据不会上传任何服务器，保障你的数据隐私安全。'),
    ('比较结果可以导出吗？', '可以。点击"导出结果"按钮可以下载TXT文件，点击"复制结果"可以将比较结果复制到剪贴板。'),
]

faqs_en = [
    ('What formats does the list comparison tool support?', 'Supports line-separated text lists. One item per line. Supports Chinese, English, numbers, symbols and any characters. Results are categorized into Common Items, Only in A, and Only in B.'),
    ('Can I compare large lists?', 'Supports comparing lists with thousands of items. For very large lists (over 10,000 items), there may be performance impact since processing is done in the browser.'),
    ('What do Ignore Case and Trim Whitespace options do?', 'Ignore Case: treats "A" and "a" as the same during comparison. Trim Whitespace: automatically removes leading/trailing spaces from each line to avoid false mismatches due to formatting differences.'),
    ('Is my data uploaded to a server?', 'No. All comparison operations are performed locally in the browser. Your data never leaves your device.'),
    ('Can I export the comparison results?', 'Yes. Click "Export" to download a TXT file, or click "Copy Results" to copy the results to your clipboard.'),
]

# SEO CN
seo_cn = '''
<h2>在线列表比较工具 - 免费快速对比两个列表的差异</h2>
<p>列表比较工具（List Diff Checker）是一款免费在线的列表差异对比工具，帮助你快速找出两个列表之间的共同项、差集和新增项。适用于数据分析、内容比对、版本差异检查、文件清单对比等场景。纯前端本地处理，保障数据隐私。</p>
<h3>核心功能</h3>
<ul>
<li>双列对比：左右两个文本区分别输入列表A和列表B</li>
<li>自动分类：结果自动分为共同项（交集）、仅A有（差集）、仅B有（新增）</li>
<li>智能选项：支持忽略大小写、去除首尾空格，避免误判</li>
<li>一键交换：点击交换按钮快速切换两个列表的位置</li>
<li>导出结果：支持导出为文本文件和复制到剪贴板</li>
</ul>
<h3>适用场景</h3>
<ul>
<li>数据清洗：比较两个数据集找出差异记录</li>
<li>内容审核：对比新旧版本内容变更</li>
<li>文件比对：检查两个文件清单的差异</li>
<li>名单管理：对比参会名单、客户名单等</li>
</ul>
'''

seo_en = '''
<h2>Online List Comparison Tool - Free List Diff Checker</h2>
<p>List Diff Checker is a free online tool for comparing two lists and finding differences. Quickly identify common items, items only in list A, and items only in list B. Perfect for data analysis, content comparison, version diff checking, and inventory comparison. Pure frontend processing, no data upload.</p>
<h3>Key Features</h3>
<ul>
<li>Side-by-side comparison: Enter List A and List B in two text areas</li>
<li>Auto-categorization: Results organized into Common, Only in A, Only in B</li>
<li>Smart options: Ignore case, trim whitespace for accurate comparison</li>
<li>One-click swap: Quickly swap the two lists</li>
<li>Export results: Download as text file or copy to clipboard</li>
</ul>
'''

cn_path, en_path = builder.build_bilingual(
    slug='list-diff',
    title_cn='列表比较工具',
    title_en='List Diff Checker',
    desc_cn='免费在线列表比较工具，快速对比两个列表的差异。自动找出共同项、差集和新增项。支持忽略大小写、去除空格。纯前端本地处理，数据隐私安全。',
    desc_en='Free online list diff checker. Compare two lists and find common items, items only in A, and items only in B. Supports ignore case and trim whitespace. Pure frontend, private & secure.',
    icon='📋',
    cat_cn='开发工具',
    cat_en='Developer Tools',
    cat_anchor='developer-tools',
    tool_html_cn=tool_html_cn,
    tool_html_en=tool_html_en,
    tool_js=tool_js,
    faqs_cn=faqs_cn,
    faqs_en=faqs_en,
    seo_cn=seo_cn,
    seo_en=seo_en,
)

print(f"✅ Created: {cn_path}")
print(f"✅ Created: {en_path}")
