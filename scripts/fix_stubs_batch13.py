#!/usr/bin/env python3
"""Fix stub functions in tool pages - Batch 13"""
import re

def fix_tool(path, fn_name, new_impl):
    content = open(path).read()
    pattern = rf'function\s+{fn_name}\s*\([^)]*\)\s*\{{\s*showToast\([^)]*coming soon[^)]*\);\s*\}}'
    new_content = re.sub(pattern, lambda m: new_impl, content, count=1)
    if new_content == content:
        print(f"  WARNING: Pattern not found for {fn_name} in {path}")
        return False
    open(path, 'w').write(new_content)
    return True

BASE = '/home/chison/tools-site'

# 1. xml-escape-unescape: autoDetect()
fix_tool(f'{BASE}/xml-escape-unescape/index.html', 'autoDetect', '''function autoDetect() {
  var input = document.getElementById('input').value;
  var output = document.getElementById('output');
  if (!input) { if (output) output.value = ''; return; }
  // Detect if input has XML entities to unescape, or special chars to escape
  var hasEntities = /&(amp|lt|gt|quot|apos|#\d+|#x[0-9a-fA-F]+);/.test(input);
  var hasSpecial = /[<>&"]/.test(input);
  
  if (hasEntities && !hasSpecial) {
    // Unescape
    var result = input
      .replace(/&amp;/g, '&')
      .replace(/&lt;/g, '<')
      .replace(/&gt;/g, '>')
      .replace(/&quot;/g, '"')
      .replace(/&apos;/g, "'")
      .replace(/&#(\d+);/g, function(m, c) { return String.fromCharCode(parseInt(c)); })
      .replace(/&#x([0-9a-fA-F]+);/g, function(m, c) { return String.fromCharCode(parseInt(c, 16)); });
    if (output) output.value = result;
  } else {
    // Escape
    var result = input
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&apos;');
    if (output) output.value = result;
  }
}''')

# 2. prime-number-checker: factorize()
fix_tool(f'{BASE}/prime-number-checker/index.html', 'factorize', '''function factorize() {
  var num = parseInt(document.getElementById('primeNum').value);
  var resultDiv = document.getElementById('primeFactorization');
  var resultText = resultDiv ? resultDiv.querySelector('pre') : null;
  if (!num || num < 2) { showToast('请输入大于1的数字'); return; }
  
  var factors = [];
  var n = num;
  for (var i = 2; i * i <= n; i++) {
    while (n % i === 0) {
      factors.push(i);
      n = n / i;
    }
  }
  if (n > 1) factors.push(n);
  
  var isPrime = factors.length === 1 && factors[0] === num;
  var html = '<div style="color:#94a3b8;font-size:.85rem;margin-bottom:8px">质因数分解:</div>';
  html += '<div style="color:#22d3ee;font-size:1.1rem;font-weight:600">' + num + ' = ' + factors.join(' \\u00d7 ') + '</div>';
  if (isPrime) {
    html += '<div style="color:#4ade80;margin-top:8px">\\u2b50 ' + num + ' 是质数！</div>';
  } else {
    html += '<div style="color:#94a3b8;margin-top:8px">' + num + ' 是合数，有 ' + factors.length + ' 个质因数</div>';
  }
  if (resultText) {
    resultText.innerHTML = html;
    resultDiv.style.display = 'block';
  }
  showToast(isPrime ? num + '是质数' : '分解完成');
}''')

# 3. csv-editor: parseCSV()
fix_tool(f'{BASE}/csv-editor/index.html', 'parseCSV', '''function parseCSV() {
  var input = document.getElementById('csvInput').value;
  var hasHeader = document.getElementById('hasHeader').checked;
  var trimSpaces = document.getElementById('trimSpaces').checked;
  var tableContainer = document.getElementById('tableContainer') || document.getElementById('csvTable');
  if (!input.trim()) { showToast('请输入CSV数据'); return; }
  
  var rows = parseCSVText(input, trimSpaces);
  if (rows.length === 0) { showToast('未解析到数据'); return; }
  
  var html = '<table style="width:100%;border-collapse:collapse;font-size:.85rem">';
  var startIdx = hasHeader ? 1 : 0;
  if (hasHeader && rows.length > 0) {
    html += '<thead><tr>';
    for (var c = 0; c < rows[0].length; c++) {
      html += '<th style="padding:6px 10px;border:1px solid #334155;background:#0f172a;color:#22d3ee;text-align:left">' + escapeHtml(rows[0][c]) + '</th>';
    }
    html += '</tr></thead>';
  }
  html += '<tbody>';
  for (var r = startIdx; r < rows.length; r++) {
    html += '<tr>';
    for (var c = 0; c < rows[r].length; c++) {
      html += '<td style="padding:6px 10px;border:1px solid rgba(148,163,184,.1);color:#e2e8f0" contenteditable="true">' + escapeHtml(rows[r][c]) + '</td>';
    }
    html += '</tr>';
  }
  html += '</tbody></table>';
  html += '<div style="margin-top:8px;color:#64748b;font-size:.8rem">' + (rows.length - startIdx) + ' 行 \\u00d7 ' + (rows[0] ? rows[0].length : 0) + ' 列</div>';
  if (tableContainer) {
    tableContainer.innerHTML = html;
    tableContainer.style.display = 'block';
  }
  showToast('解析完成，' + (rows.length - startIdx) + '行数据');
}
function parseCSVText(text, trim) {
  var rows = [];
  var current = [];
  var field = '';
  var inQuotes = false;
  for (var i = 0; i < text.length; i++) {
    var ch = text[i];
    if (inQuotes) {
      if (ch === '"') {
        if (text[i+1] === '"') { field += '"'; i++; }
        else inQuotes = false;
      } else { field += ch; }
    } else {
      if (ch === '"') inQuotes = true;
      else if (ch === ',') { current.push(trim ? field.trim() : field); field = ''; }
      else if (ch === '\\n') { current.push(trim ? field.trim() : field); rows.push(current); current = []; field = ''; }
      else if (ch === '\\r') { /* skip */ }
      else field += ch;
    }
  }
  if (field || current.length > 0) { current.push(trim ? field.trim() : field); rows.push(current); }
  return rows;
}
function escapeHtml(s) { var d=document.createElement('div'); d.textContent=s; return d.innerHTML; }''')

# 4. dot-grid-generator: updateGrid()
fix_tool(f'{BASE}/dot-grid-generator/index.html', 'updateGrid', '''function updateGrid() {
  var dotSize = parseInt(document.getElementById('dotSize').value) || 3;
  var hSpacing = parseInt(document.getElementById('hSpacing').value) || 30;
  var vSpacing = parseInt(document.getElementById('vSpacing').value) || 30;
  var dotColor = document.getElementById('dotColor').value;
  var bgColor = document.getElementById('bgColor').value;
  
  var preview = document.getElementById('gridPreview') || document.getElementById('preview');
  if (preview) {
    preview.style.backgroundImage = 'radial-gradient(circle, ' + dotColor + ' ' + dotSize + 'px, transparent ' + dotSize + 'px)';
    preview.style.backgroundSize = hSpacing + 'px ' + vSpacing + 'px';
    preview.style.backgroundColor = bgColor;
  }
  var codeEl = document.getElementById('gridCode');
  if (codeEl) {
    var code = '.dot-grid {\\n';
    code += '  background-color: ' + bgColor + ';\\n';
    code += '  background-image: radial-gradient(circle, ' + dotColor + ' ' + dotSize + 'px, transparent ' + dotSize + 'px);\\n';
    code += '  background-size: ' + hSpacing + 'px ' + vSpacing + 'px;\\n';
    code += '}';
    codeEl.textContent = code;
  }
  // Update labels
  var labels = document.querySelectorAll('[id$="Val"]');
  labels.forEach(function(l) {
    var inputId = l.id.replace('Val', '');
    var inp = document.getElementById(inputId);
    if (inp) l.textContent = inp.value + (inp.type === 'range' ? 'px' : '');
  });
}''')

# 5. font-previewer: filterFonts()
fix_tool(f'{BASE}/font-previewer/index.html', 'filterFonts', '''function filterFonts() {
  var search = (document.getElementById('searchInput').value || '').toLowerCase();
  var category = document.getElementById('categorySelect').value;
  var sort = document.getElementById('sortSelect').value;
  var container = document.getElementById('fontList') || document.getElementById('fontsContainer');
  if (!container) return;
  
  var fonts = container.querySelectorAll('.font-card');
  var visible = [];
  for (var i = 0; i < fonts.length; i++) {
    var name = (fonts[i].getAttribute('data-font') || fonts[i].querySelector('.font-name') || {}).textContent || '';
    name = name.toLowerCase();
    var cat = fonts[i].getAttribute('data-category') || '';
    var match = true;
    if (search && name.indexOf(search) === -1) match = false;
    if (category && category !== 'all' && cat !== category) match = false;
    fonts[i].style.display = match ? '' : 'none';
    if (match) visible.push(fonts[i]);
  }
  // Sort
  visible.sort(function(a, b) {
    var an = (a.getAttribute('data-font') || a.querySelector('.font-name').textContent).toLowerCase();
    var bn = (b.getAttribute('data-font') || b.querySelector('.font-name').textContent).toLowerCase();
    if (sort === 'name-desc') return bn.localeCompare(an);
    return an.localeCompare(bn);
  });
  for (var i = 0; i < visible.length; i++) {
    container.appendChild(visible[i]);
  }
  var countEl = document.getElementById('fontCount');
  if (countEl) countEl.textContent = visible.length;
}''')

# 6. octal-decimal-converter: setBase()
fix_tool(f'{BASE}/octal-decimal-converter/index.html', 'setBase', '''function setBase(base) {
  var input = document.getElementById('mainInput');
  if (!input) return;
  var val = input.value.trim();
  if (!val) return;
  var num;
  try {
    if (base === 2) num = parseInt(val, 2);
    else if (base === 8) num = parseInt(val, 8);
    else if (base === 10) num = parseInt(val, 10);
    else if (base === 16) num = parseInt(val, 16);
    else num = parseInt(val, 10);
  } catch(e) { showToast('无效输入'); return; }
  if (isNaN(num)) { showToast('无效的数值'); return; }
  document.getElementById('binResult').textContent = num.toString(2);
  document.getElementById('octResult').textContent = num.toString(8);
  document.getElementById('decResult').textContent = num.toString(10);
  document.getElementById('hexResult').textContent = num.toString(16).toUpperCase();
}''')

# 7. equation-grapher: plotGraph()
fix_tool(f'{BASE}/equation-grapher/index.html', 'plotGraph', '''function plotGraph() {
  var eq = document.getElementById('eqInput').value.trim();
  var xMin = parseFloat(document.getElementById('eqXMin').value) || -10;
  var xMax = parseFloat(document.getElementById('eqXMax').value) || 10;
  var yMin = parseFloat(document.getElementById('eqYMin').value) || -5;
  var yMax = parseFloat(document.getElementById('eqYMax').value) || 5;
  var canvas = document.getElementById('graphCanvas');
  if (!canvas || !eq) { if (!eq) showToast('请输入函数'); return; }
  
  // Parse equation - support sin, cos, tan, sqrt, abs, exp, log, pow, ^, *, /, +, -, x, pi, e
  var expr = eq.replace(/\\^/g, '**').replace(/\\bpi\\b/gi, 'Math.PI').replace(/\\be\\b/g, 'Math.E');
  expr = expr.replace(/\\bsin\\b/gi, 'Math.sin').replace(/\\bcos\\b/gi, 'Math.cos');
  expr = expr.replace(/\\btan\\b/gi, 'Math.tan').replace(/\\bsqrt\\b/gi, 'Math.sqrt');
  expr = expr.replace(/\\babs\\b/gi, 'Math.abs').replace(/\\bexp\\b/gi, 'Math.exp');
  expr = expr.replace(/\\blog\\b/gi, 'Math.log').replace(/\\bfloor\\b/gi, 'Math.floor');
  expr = expr.replace(/\\bceil\\b/gi, 'Math.ceil').replace(/\\bround\\b/gi, 'Math.round');
  expr = expr.replace(/\\bpow\\b/gi, 'Math.pow');
  
  var ctx = canvas.getContext('2d');
  var w = canvas.width, h = canvas.height;
  ctx.clearRect(0, 0, w, h);
  ctx.fillStyle = '#0f172a';
  ctx.fillRect(0, 0, w, h);
  
  // Draw grid
  ctx.strokeStyle = '#1e293b';
  ctx.lineWidth = 1;
  var xRange = xMax - xMin, yRange = yMax - yMin;
  for (var x = Math.ceil(xMin); x <= xMax; x++) {
    var px = (x - xMin) / xRange * w;
    ctx.beginPath(); ctx.moveTo(px, 0); ctx.lineTo(px, h); ctx.stroke();
  }
  for (var y = Math.ceil(yMin); y <= yMax; y++) {
    var py = h - (y - yMin) / yRange * h;
    ctx.beginPath(); ctx.moveTo(0, py); ctx.lineTo(w, py); ctx.stroke();
  }
  // Axes
  ctx.strokeStyle = '#334155';
  ctx.lineWidth = 2;
  var x0 = (0 - xMin) / xRange * w;
  var y0 = h - (0 - yMin) / yRange * h;
  ctx.beginPath(); ctx.moveTo(x0, 0); ctx.lineTo(x0, h); ctx.stroke();
  ctx.beginPath(); ctx.moveTo(0, y0); ctx.lineTo(w, y0); ctx.stroke();
  // Plot
  ctx.strokeStyle = '#22d3ee';
  ctx.lineWidth = 2;
  ctx.beginPath();
  var started = false;
  for (var px = 0; px <= w; px++) {
    var x = xMin + (px / w) * xRange;
    var y;
    try {
      y = eval('(function(x){return ' + expr + ';})(' + x + ')');
    } catch(e) { started = false; continue; }
    if (!isFinite(y) || isNaN(y)) { started = false; continue; }
    var py = h - (y - yMin) / yRange * h;
    if (py < -100 || py > h + 100) { started = false; continue; }
    if (!started) { ctx.moveTo(px, py); started = true; }
    else ctx.lineTo(px, py);
  }
  ctx.stroke();
  showToast('绘图完成');
}''')

# 8. redirect-tracer: switchMode()
fix_tool(f'{BASE}/redirect-tracer/index.html', 'switchMode', '''function switchMode(mode) {
  var singleMode = document.getElementById('single-mode') || document.querySelector('.single-mode');
  var batchMode = document.getElementById('batch-mode') || document.querySelector('.batch-mode');
  if (mode === 'batch') {
    if (singleMode) singleMode.style.display = 'none';
    if (batchMode) batchMode.style.display = '';
  } else {
    if (singleMode) singleMode.style.display = '';
    if (batchMode) batchMode.style.display = 'none';
  }
  // Update tab styles
  var tabs = document.querySelectorAll('.mode-tab');
  tabs.forEach(function(t) { t.classList.remove('active'); });
  var activeTab = document.querySelector('[data-mode="' + mode + '"]') || document.getElementById('tab-' + mode);
  if (activeTab) activeTab.classList.add('active');
}''')

# 9. webgpu-info: detectWebGPU()
fix_tool(f'{BASE}/webgpu-info/index.html', 'detectWebGPU', '''function detectWebGPU() {
  var resultDiv = document.getElementById('result') || document.getElementById('resultArea');
  if (!resultDiv) return;
  resultDiv.innerHTML = '<div style="text-align:center;padding:20px;color:#94a3b8">正在检测WebGPU支持...</div>';
  
  var info = {};
  info.userAgent = navigator.userAgent;
  info.platform = navigator.platform;
  
  if (navigator.gpu) {
    info.webgpuSupported = true;
    navigator.gpu.requestAdapter().then(function(adapter) {
      if (adapter) {
        info.adapterInfo = adapter.info || {};
        info.features = Array.from(adapter.features || []);
        info.limits = adapter.limits || {};
        displayWebGPUInfo(resultDiv, info);
      } else {
        info.webgpuSupported = false;
        info.error = 'No suitable GPU adapter found';
        displayWebGPUInfo(resultDiv, info);
      }
    }).catch(function(e) {
      info.webgpuSupported = false;
      info.error = e.message;
      displayWebGPUInfo(resultDiv, info);
    });
  } else {
    info.webgpuSupported = false;
    info.error = 'WebGPU not supported in this browser';
    displayWebGPUInfo(resultDiv, info);
  }
}
function displayWebGPUInfo(container, info) {
  var html = '<div style="display:grid;grid-template-columns:1fr 1fr;gap:12px">';
  html += gpuCard('WebGPU支持', info.webgpuSupported ? '\\u2705 支持' : '\\u274c 不支持');
  html += gpuCard('浏览器', info.userAgent.substring(0, 60) + '...');
  html += gpuCard('平台', info.platform || '-');
  if (info.error) html += gpuCard('错误', info.error);
  if (info.adapterInfo) {
    html += gpuCard('GPU厂商', info.adapterInfo.vendor || '-');
    html += gpuCard('GPU架构', info.adapterInfo.architecture || '-');
    html += gpuCard('设备描述', info.adapterInfo.description || '-');
  }
  if (info.features) html += gpuCard('特性数量', info.features.length);
  html += '</div>';
  if (info.features && info.features.length > 0) {
    html += '<div style="margin-top:12px;color:#94a3b8;font-size:.85rem">支持特性: ' + info.features.join(', ') + '</div>';
  }
  container.innerHTML = html;
  showToast(info.webgpuSupported ? 'WebGPU已支持' : 'WebGPU不支持');
}
function gpuCard(label, value) {
  return '<div style="background:#0f172a;padding:12px;border-radius:8px;border:1px solid rgba(148,163,184,.1)"><div style="color:#64748b;font-size:.8rem;margin-bottom:4px">' + label + '</div><div style="color:#e2e8f0;font-weight:500">' + value + '</div></div>';
}''')

# 10. interest-rate-calculator: updateLabels()
fix_tool(f'{BASE}/interest-rate-calculator/index.html', 'updateLabels', '''function updateLabels() {
  var type = document.getElementById('calcType') ? document.getElementById('calcType').value : 'simple';
  var labels = {
    'simple': ['本金', '年利率(%)', '期限(年)'],
    'compound': ['本金', '年利率(%)', '期限(年)'],
    'apr': ['贷款金额', '年利率(%)', '期限(月)'],
    'apy': ['初始金额', '年利率(%)', '复利次数/年']
  };
  var l = labels[type] || labels['simple'];
  var inputs = document.querySelectorAll('.form-group label');
  if (inputs.length >= 3) {
    inputs[0].textContent = l[0];
    inputs[1].textContent = l[1];
    inputs[2].textContent = l[2];
  }
  if (typeof calculate === 'function') calculate();
}''')

print("\nBatch 13 done.")
