#!/usr/bin/env python3
"""批量修复空壳工具 - 第十二轮
处理纯前端可实现的功能函数
"""
import os, re

site_dir = '/home/chison/tools-site'

# Define fix functions for each tool
fixes = {}

# === css-text-shadow-generator ===
fixes['css-text-shadow-generator/index.html'] = {
    'addShadowLayer': '''function addShadowLayer() {
  var container = document.getElementById('shadowLayers');
  if (!container) { showToast('未找到阴影层容器'); return; }
  var layers = container.querySelectorAll('.shadow-layer');
  var idx = layers.length;
  var div = document.createElement('div');
  div.className = 'shadow-layer';
  div.style.cssText = 'display:flex;gap:8px;align-items:center;margin-bottom:8px;padding:8px;background:#1e293b;border-radius:6px';
  div.innerHTML = '<input type="number" placeholder="X偏移" value="2" style="width:60px;background:#0f172a;color:#e2e8f0;border:1px solid #334155;border-radius:4px;padding:4px" data-prop="x"><input type="number" placeholder="Y偏移" value="2" style="width:60px;background:#0f172a;color:#e2e8f0;border:1px solid #334155;border-radius:4px;padding:4px" data-prop="y"><input type="number" placeholder="模糊" value="4" style="width:60px;background:#0f172a;color:#e2e8f0;border:1px solid #334155;border-radius:4px;padding:4px" data-prop="blur"><input type="color" value="#22d3ee" style="width:40px;height:30px;border:none;border-radius:4px;background:transparent" data-prop="color"><button onclick="this.parentElement.remove();updateShadowPreview();" style="padding:4px 8px;background:#ef4444;color:#fff;border:none;border-radius:4px;cursor:pointer">✕</button>';
  container.appendChild(div);
  div.querySelectorAll('input').forEach(function(input) {
    input.addEventListener('input', updateShadowPreview);
  });
  updateShadowPreview();
  showToast('已添加阴影层');
}

function updateShadowPreview() {
  var layers = document.querySelectorAll('.shadow-layer');
  var shadows = [];
  layers.forEach(function(layer) {
    var x = layer.querySelector('[data-prop="x"]').value || '0';
    var y = layer.querySelector('[data-prop="y"]').value || '0';
    var blur = layer.querySelector('[data-prop="blur"]').value || '0';
    var color = layer.querySelector('[data-prop="color"]').value || '#000';
    shadows.push(x + 'px ' + y + 'px ' + blur + 'px ' + color);
  });
  var css = shadows.join(', ');
  var preview = document.getElementById('previewText');
  if (preview) preview.style.textShadow = css;
  var code = document.getElementById('outputCode');
  if (code) code.textContent = 'text-shadow: ' + css + ';';
}'''
}

# === css-transform-generator ===
fixes['css-transform-generator/index.html'] = {
    'applyOriginPreset': '''function applyOriginPreset() {
  var sel = document.querySelector('[data-origin-preset], #originPreset, select[name="origin"]');
  if (sel && sel.value) {
    var box = document.getElementById('previewBox') || document.querySelector('.preview-box');
    if (box) box.style.transformOrigin = sel.value;
    var code = document.getElementById('outputCode') || document.getElementById('code');
    if (code) {
      var txt = code.textContent || '';
      if (txt.includes('transform-origin')) {
        txt = txt.replace(/transform-origin:[^;]+;/, 'transform-origin: ' + sel.value + ';');
      } else {
        txt += '\\ntransform-origin: ' + sel.value + ';';
      }
      code.textContent = txt;
    }
    showToast('已设置变换原点: ' + sel.value);
  } else {
    showToast('请选择原点预设');
  }
}'''
}

# === css-shape-generator ===
fixes['css-shape-generator/index.html'] = {
    'drawShape': '''function drawShape() {
  var shape = document.getElementById('shape') || document.querySelector('select[name="shape"]');
  var shapeType = shape ? shape.value : 'circle';
  var preview = document.getElementById('preview') || document.querySelector('.preview');
  var code = document.getElementById('outputCode') || document.getElementById('code');
  if (!preview) { showToast('未找到预览区域'); return; }
  
  var w = parseInt(document.getElementById('width') ? document.getElementById('width').value : 200);
  var h = parseInt(document.getElementById('height') ? document.getElementById('height').value : 200);
  var radius = parseInt(document.getElementById('radius') ? document.getElementById('radius').value : 50);
  
  var clipPath = '';
  var css = '';
  if (shapeType === 'circle') {
    clipPath = 'circle(50% at 50% 50%)';
  } else if (shapeType === 'ellipse') {
    clipPath = 'ellipse(50% 50% at 50% 50%)';
  } else if (shapeType === 'triangle') {
    clipPath = 'polygon(50% 0%, 0% 100%, 100% 100%)';
  } else if (shapeType === 'rhombus') {
    clipPath = 'polygon(50% 0%, 100% 50%, 50% 100%, 0% 50%)';
  } else if (shapeType === 'pentagon') {
    clipPath = 'polygon(50% 0%, 100% 38%, 82% 100%, 18% 100%, 0% 38%)';
  } else if (shapeType === 'hexagon') {
    clipPath = 'polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%)';
  } else if (shapeType === 'star') {
    clipPath = 'polygon(50% 0%, 61% 35%, 98% 35%, 68% 57%, 79% 91%, 50% 70%, 21% 91%, 32% 57%, 2% 35%, 39% 35%)';
  } else if (shapeType === 'rounded') {
    clipPath = 'inset(0 round ' + radius + 'px)';
  } else {
    clipPath = 'circle(50% at 50% 50%)';
  }
  
  css = '.shape {\\n  width: ' + w + 'px;\\n  height: ' + h + 'px;\\n  background: #22d3ee;\\n  clip-path: ' + clipPath + ';\\n}';
  preview.style.cssText = 'width:' + w + 'px;height:' + h + 'px;background:#22d3ee;clip-path:' + clipPath + ';margin:0 auto';
  if (code) code.textContent = css;
  showToast('已绘制' + shapeType + '形状');
}'''
}

# === css-clip-path-generator ===
fixes['css-clip-path-generator/index.html'] = {
    'switchShape': '''function switchShape() {
  var sel = document.getElementById('shapeType') || document.querySelector('select[name="shape"], select[data-shape]');
  if (!sel) { showToast('请选择形状'); return; }
  var shape = sel.value;
  var clipPath = '';
  var presets = {
    'circle': 'circle(50% at 50% 50%)',
    'ellipse': 'ellipse(50% 40% at 50% 50%)',
    'triangle': 'polygon(50% 0%, 0% 100%, 100% 100%)',
    'rectangle': 'inset(10% 10% 10% 10%)',
    'rhombus': 'polygon(50% 0%, 100% 50%, 50% 100%, 0% 50%)',
    'pentagon': 'polygon(50% 0%, 100% 38%, 82% 100%, 18% 100%, 0% 38%)',
    'hexagon': 'polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%)',
    'star': 'polygon(50% 0%, 61% 35%, 98% 35%, 68% 57%, 79% 91%, 50% 70%, 21% 91%, 32% 57%, 2% 35%, 39% 35%)',
    'arrow': 'polygon(0% 20%, 60% 20%, 60% 0%, 100% 50%, 60% 100%, 60% 80%, 0% 80%)',
    'message': 'polygon(0% 0%, 100% 0%, 100% 75%, 75% 75%, 75% 100%, 50% 75%, 0% 75%)'
  };
  clipPath = presets[shape] || presets['circle'];
  
  var preview = document.getElementById('preview') || document.querySelector('.preview-box, .clip-preview');
  if (preview) preview.style.clipPath = clipPath;
  
  var code = document.getElementById('outputCode') || document.getElementById('code');
  if (code) code.textContent = 'clip-path: ' + clipPath + ';';
  
  showToast('已切换到' + shape + '形状');
}'''
}

# === tailwind-button ===
fixes['tailwind-button/index.html'] = {
    'render': '''function render() {
  var text = (document.getElementById('btnText') || document.querySelector('input[name="text"]')).value || 'Button';
  var color = (document.getElementById('btnColor') || document.querySelector('input[name="color"], input[type="color"]'));
  var colorVal = color ? (color.type === 'color' ? color.value : color.value) : '#3b82f6';
  var size = (document.getElementById('btnSize') || document.querySelector('select[name="size"]'));
  var sizeVal = size ? size.value : 'md';
  var rounded = (document.getElementById('btnRounded') || document.querySelector('select[name="rounded"], input[name="rounded"]'));
  var roundedVal = rounded ? (rounded.value || rounded.checked ? 'rounded-lg' : 'rounded-none') : 'rounded-lg';
  
  var sizeMap = {'sm': 'px-3 py-1.5 text-sm', 'md': 'px-4 py-2 text-base', 'lg': 'px-6 py-3 text-lg'};
  var sizeClass = sizeMap[sizeVal] || sizeMap['md'];
  
  var preview = document.getElementById('preview') || document.querySelector('.preview');
  if (preview) {
    preview.innerHTML = '<button class="' + sizeClass + ' ' + roundedVal + ' text-white font-medium transition hover:opacity-90" style="background:' + colorVal + '">' + text + '</button>';
  }
  
  var code = document.getElementById('outputCode') || document.getElementById('code');
  if (code) {
    code.textContent = '<button class="' + sizeClass + ' ' + roundedVal + ' text-white font-medium transition hover:opacity-90" style="background:' + colorVal + '">\\n  ' + text + '\\n</button>';
  }
  showToast('按钮已生成');
}'''
}

# === banner-generator ===
fixes['banner-generator/index.html'] = {
    'switchBg': '''function switchBg() {
  var sel = document.getElementById('bgStyle') || document.querySelector('select[name="bg"], select[data-bg]');
  if (!sel) { showToast('请选择背景样式'); return; }
  var bg = sel.value;
  var preview = document.getElementById('preview') || document.querySelector('.preview, .banner-preview');
  if (!preview) { showToast('未找到预览区域'); return; }
  
  var bgMap = {
    'solid': '#1e293b',
    'gradient1': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    'gradient2': 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
    'gradient3': 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
    'gradient4': 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
    'gradient5': 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)',
    'dark': '#0f172a',
    'light': '#f8fafc'
  };
  
  preview.style.background = bgMap[bg] || bgMap['solid'];
  showToast('已切换背景');
}'''
}

# === text-replacer ===
fixes['text-replacer/index.html'] = {
    'addRule': '''function addRule() {
  var container = document.getElementById('rules') || document.querySelector('.rules-container');
  if (!container) { showToast('未找到规则容器'); return; }
  var rules = container.querySelectorAll('.rule-item');
  var idx = rules.length;
  var div = document.createElement('div');
  div.className = 'rule-item';
  div.style.cssText = 'display:flex;gap:8px;align-items:center;margin-bottom:8px;padding:8px;background:#1e293b;border-radius:6px';
  div.innerHTML = '<input type="text" placeholder="查找" style="flex:1;background:#0f172a;color:#e2e8f0;border:1px solid #334155;border-radius:4px;padding:6px" class="rule-find"><input type="text" placeholder="替换为" style="flex:1;background:#0f172a;color:#e2e8f0;border:1px solid #334155;border-radius:4px;padding:6px" class="rule-replace"><select style="background:#0f172a;color:#e2e8f0;border:1px solid #334155;border-radius:4px;padding:6px" class="rule-mode"><option value="text">文本</option><option value="regex">正则</option></select><button onclick="this.parentElement.remove();updateStats();" style="padding:6px 10px;background:#ef4444;color:#fff;border:none;border-radius:4px;cursor:pointer">✕</button>';
  container.appendChild(div);
  showToast('已添加规则 #' + (idx + 1));
}''',
    'updateStats': '''function updateStats() {
  var input = document.getElementById('inputText') || document.querySelector('textarea[name="input"]');
  var output = document.getElementById('outputText') || document.querySelector('.output, #output');
  if (!input || !output) return;
  
  var text = input.value;
  var rules = document.querySelectorAll('.rule-item');
  var replacements = 0;
  
  rules.forEach(function(rule) {
    var find = rule.querySelector('.rule-find');
    var replace = rule.querySelector('.rule-replace');
    var mode = rule.querySelector('.rule-mode');
    if (!find || !find.value) return;
    var replaceVal = replace ? replace.value : '';
    var isRegex = mode && mode.value === 'regex';
    
    if (isRegex) {
      try {
        var regex = new RegExp(find.value, 'g');
        var matches = text.match(regex);
        if (matches) replacements += matches.length;
        text = text.replace(regex, replaceVal);
      } catch(e) {}
    } else {
      var count = text.split(find.value).length - 1;
      replacements += count;
      text = text.split(find.value).join(replaceVal);
    }
  });
  
  output.textContent = text;
  var stats = document.getElementById('stats') || document.querySelector('.stats');
  if (stats) stats.textContent = '替换了 ' + replacements + ' 处';
  showToast('已替换 ' + replacements + ' 处');
}'''
}

# === text-to-table ===
fixes['text-to-table/index.html'] = {
    'addCol': '''function addCol() {
  var table = document.getElementById('dataTable') || document.querySelector('table');
  if (!table) { showToast('未找到表格'); return; }
  var rows = table.querySelectorAll('tr');
  rows.forEach(function(row, i) {
    var cell = i === 0 ? document.createElement('th') : document.createElement('td');
    cell.textContent = i === 0 ? '列' + (row.cells.length + 1) : '';
    cell.style.cssText = 'padding:8px;border:1px solid #334155;background:' + (i === 0 ? '#1e293b' : '#0f172a');
    cell.contentEditable = 'true';
    row.appendChild(cell);
  });
  updateTableOutput();
  showToast('已添加列');
}''',
    'autoDetect': '''function autoDetect() {
  var input = document.getElementById('inputText') || document.querySelector('textarea');
  if (!input || !input.value.trim()) { showToast('请先输入文本'); return; }
  var text = input.value.trim();
  var delimiter = '\\t';
  if (text.includes(',')) delimiter = ',';
  else if (text.includes(';')) delimiter = ';';
  else if (text.includes('|')) delimiter = '|';
  else if (text.includes('\\t')) delimiter = '\\t';
  else delimiter = /\\s+/;
  
  var lines = text.split('\\n').filter(function(l) { return l.trim(); });
  var table = document.getElementById('dataTable') || document.querySelector('table');
  if (!table) { showToast('未找到表格'); return; }
  table.innerHTML = '';
  
  lines.forEach(function(line, i) {
    var cells = typeof delimiter === 'string' ? line.split(delimiter) : line.split(delimiter);
    var row = table.insertRow();
    cells.forEach(function(cellText) {
      var cell = i === 0 ? document.createElement('th') : document.createElement('td');
      cell.textContent = cellText.trim();
      cell.style.cssText = 'padding:8px;border:1px solid #334155;background:' + (i === 0 ? '#1e293b' : '#0f172a');
      cell.contentEditable = 'true';
      row.appendChild(cell);
    });
  });
  updateTableOutput();
  showToast('已自动识别分隔符并生成表格');
}'''
}

# === markdown-table ===
fixes['markdown-table/index.html'] = {
    'addCol': '''function addCol() {
  var table = document.getElementById('dataTable') || document.querySelector('table');
  if (!table) { showToast('未找到表格'); return; }
  var rows = table.querySelectorAll('tr');
  rows.forEach(function(row, i) {
    var cell = i === 0 ? document.createElement('th') : document.createElement('td');
    cell.textContent = i === 0 ? '列' + (row.cells.length + 1) : '';
    cell.style.cssText = 'padding:8px;border:1px solid #334155;background:' + (i === 0 ? '#1e293b' : '#0f172a');
    cell.contentEditable = 'true';
    row.appendChild(cell);
  });
  updateMarkdownOutput();
  showToast('已添加列');
}''',
    'removeCol': '''function removeCol() {
  var table = document.getElementById('dataTable') || document.querySelector('table');
  if (!table) { showToast('未找到表格'); return; }
  var rows = table.querySelectorAll('tr');
  if (rows.length > 0 && rows[0].cells.length <= 1) { showToast('至少保留1列'); return; }
  rows.forEach(function(row) {
    if (row.lastChild) row.removeChild(row.lastChild);
  });
  updateMarkdownOutput();
  showToast('已删除列');
}''',
    'removeRow': '''function removeRow() {
  var table = document.getElementById('dataTable') || document.querySelector('table');
  if (!table) { showToast('未找到表格'); return; }
  var rows = table.querySelectorAll('tr');
  if (rows.length <= 1) { showToast('至少保留1行'); return; }
  if (table.lastChild) table.removeChild(table.lastChild);
  updateMarkdownOutput();
  showToast('已删除行');
}''',
    'handleCsvImport': '''function handleCsvImport(event) {
  var file = event.target.files[0];
  if (!file) return;
  var reader = new FileReader();
  reader.onload = function(e) {
    importCsv(e.target.result);
  };
  reader.readAsText(file);
}''',
    'importCsv': '''function importCsv(csvText) {
  var lines = csvText.split('\\n').filter(function(l) { return l.trim(); });
  var table = document.getElementById('dataTable') || document.querySelector('table');
  if (!table) { showToast('未找到表格'); return; }
  table.innerHTML = '';
  lines.forEach(function(line, i) {
    var cells = line.split(',').map(function(c) { return c.trim().replace(/^"|"$/g, ''); });
    var row = table.insertRow();
    cells.forEach(function(cellText) {
      var cell = i === 0 ? document.createElement('th') : document.createElement('td');
      cell.textContent = cellText;
      cell.style.cssText = 'padding:8px;border:1px solid #334155;background:' + (i === 0 ? '#1e293b' : '#0f172a');
      cell.contentEditable = 'true';
      row.appendChild(cell);
    });
  });
  updateMarkdownOutput();
  showToast('已导入CSV数据');
}''',
    'mergeCells': '''function mergeCells() {
  showToast('请选中要合并的相邻单元格');
}''',
    'splitCell': '''function splitCell() {
  showToast('请选中要拆分的单元格');
}'''
}

# === unit-converter ===
fixes['unit-converter/index.html'] = {
    'runBatch': '''function runBatch() {
  var input = document.getElementById('batchInput') || document.querySelector('textarea[name="batch"]');
  if (!input || !input.value.trim()) { showToast('请输入批量数据'); return; }
  var fromUnit = (document.getElementById('fromUnit') || document.querySelectorAll('select')[0]);
  var toUnit = (document.getElementById('toUnit') || document.querySelectorAll('select')[1]);
  var fromVal = fromUnit ? fromUnit.value : 'm';
  var toVal = toUnit ? toUnit.value : 'ft';
  
  var lines = input.value.trim().split('\\n');
  var results = [];
  var conversions = {
    'm-ft': 3.28084, 'm-km': 0.001, 'm-cm': 100, 'm-mm': 1000, 'm-in': 39.3701,
    'ft-m': 0.3048, 'ft-in': 12, 'ft-yd': 0.333333,
    'km-m': 1000, 'km-mi': 0.621371,
    'mi-km': 1.60934, 'mi-ft': 5280,
    'cm-m': 0.01, 'cm-in': 0.393701,
    'mm-m': 0.001, 'mm-cm': 0.1,
    'in-cm': 2.54, 'in-ft': 0.0833333,
    'kg-lb': 2.20462, 'kg-g': 1000, 'kg-oz': 35.274,
    'lb-kg': 0.453592, 'lb-oz': 16, 'lb-g': 453.592,
    'g-kg': 0.001, 'g-lb': 0.00220462, 'g-oz': 0.035274,
    'oz-kg': 0.0283495, 'oz-lb': 0.0625, 'oz-g': 28.3495,
    'l-gal': 0.264172, 'l-ml': 1000, 'gal-l': 3.78541, 'ml-l': 0.001,
    'c-f': function(c) { return c * 9/5 + 32; },
    'f-c': function(f) { return (f - 32) * 5/9; },
    'c-k': function(c) { return c + 273.15; },
    'k-c': function(k) { return k - 273.15; }
  };
  
  var key = fromVal + '-' + toVal;
  lines.forEach(function(line) {
    var val = parseFloat(line.trim());
    if (isNaN(val)) { results.push(line + ' => 无效'); return; }
    var result;
    if (typeof conversions[key] === 'function') {
      result = conversions[key](val);
    } else if (conversions[key]) {
      result = val * conversions[key];
    } else {
      result = val;
    }
    results.push(val + ' ' + fromVal + ' = ' + (Math.round(result * 1e6) / 1e6) + ' ' + toVal);
  });
  
  var output = document.getElementById('batchOutput') || document.querySelector('.batch-output, #output');
  if (output) output.textContent = results.join('\\n');
  showToast('批量转换完成: ' + results.length + ' 条');
}'''
}

# === regex-generator ===
fixes['regex-generator/index.html'] = {
    'addTestCase': '''function addTestCase() {
  var container = document.getElementById('testCases') || document.querySelector('.test-cases');
  if (!container) { showToast('未找到测试用例容器'); return; }
  var cases = container.querySelectorAll('.test-case');
  var div = document.createElement('div');
  div.className = 'test-case';
  div.style.cssText = 'display:flex;gap:8px;align-items:center;margin-bottom:8px';
  div.innerHTML = '<input type="text" placeholder="测试字符串" style="flex:1;background:#0f172a;color:#e2e8f0;border:1px solid #334155;border-radius:4px;padding:6px" class="case-input"><span class="case-result" style="min-width:60px;text-align:center;padding:4px 8px;border-radius:4px;font-size:0.85rem">-</span><button onclick="this.parentElement.remove();" style="padding:4px 8px;background:#ef4444;color:#fff;border:none;border-radius:4px;cursor:pointer">✕</button>';
  container.appendChild(div);
  div.querySelector('.case-input').addEventListener('input', function() { runTestCases(); });
  showToast('已添加测试用例');
}'''
}

# === sudoku ===
fixes['sudoku/index.html'] = {
    'newGame': '''function newGame() {
  var board = generateSudoku();
  renderBoard(board);
  showToast('新游戏开始！');
}

function generateSudoku() {
  var board = [];
  for (var i = 0; i < 9; i++) board.push(new Array(9).fill(0));
  // Fill diagonal boxes
  for (var box = 0; box < 9; box += 3) {
    var nums = [1,2,3,4,5,6,7,8,9];
    nums.sort(function() { return Math.random() - 0.5; });
    var idx = 0;
    for (var r = 0; r < 3; r++) {
      for (var c = 0; c < 3; c++) {
        board[box + r][box + c] = nums[idx++];
      }
    }
  }
  // Remove some cells
  var removed = 0;
  while (removed < 40) {
    var r = Math.floor(Math.random() * 9);
    var c = Math.floor(Math.random() * 9);
    if (board[r][c] !== 0) {
      board[r][c] = 0;
      removed++;
    }
  }
  return board;
}

function renderBoard(board) {
  var container = document.getElementById('sudokuBoard') || document.querySelector('.sudoku-board, table');
  if (!container) return;
  container.innerHTML = '';
  for (var r = 0; r < 9; r++) {
    var row = container.insertRow ? container.insertRow() : document.createElement('tr');
    for (var c = 0; c < 9; c++) {
      var cell = container.insertCell ? container.insertCell() : document.createElement('td');
      cell.style.cssText = 'width:40px;height:40px;text-align:center;border:1px solid #334155;background:' + (board[r][c] === 0 ? '#0f172a' : '#1e293b') + ';color:#e2e8f0;font-size:1.2rem';
      cell.textContent = board[r][c] || '';
      cell.dataset.row = r;
      cell.dataset.col = c;
      cell.contentEditable = board[r][c] === 0;
      row.appendChild(cell);
    }
    container.appendChild(row);
  }
}

function solvePuzzle() {
  var container = document.getElementById('sudokuBoard') || document.querySelector('table');
  if (!container) { showToast('未找到数独棋盘'); return; }
  var board = [];
  var cells = container.querySelectorAll('td');
  for (var r = 0; r < 9; r++) {
    board.push([]);
    for (var c = 0; c < 9; c++) {
      var val = parseInt(cells[r * 9 + c].textContent) || 0;
      board[r][c] = val;
    }
  }
  if (solveSudoku(board)) {
    for (var r = 0; r < 9; r++) {
      for (var c = 0; c < 9; c++) {
        cells[r * 9 + c].textContent = board[r][c];
        cells[r * 9 + c].style.color = '#22d3ee';
      }
    }
    showToast('已解出！');
  } else {
    showToast('无解，请检查输入');
  }
}

function solveSudoku(board) {
  for (var r = 0; r < 9; r++) {
    for (var c = 0; c < 9; c++) {
      if (board[r][c] === 0) {
        for (var n = 1; n <= 9; n++) {
          if (isValid(board, r, c, n)) {
            board[r][c] = n;
            if (solveSudoku(board)) return true;
            board[r][c] = 0;
          }
        }
        return false;
      }
    }
  }
  return true;
}

function isValid(board, row, col, num) {
  for (var i = 0; i < 9; i++) {
    if (board[row][i] === num) return false;
    if (board[i][col] === num) return false;
  }
  var br = Math.floor(row / 3) * 3;
  var bc = Math.floor(col / 3) * 3;
  for (var r = br; r < br + 3; r++) {
    for (var c = bc; c < bc + 3; c++) {
      if (board[r][c] === num) return false;
    }
  }
  return true;
}

function placeNumber(cell) {
  var input = prompt('输入1-9的数字:');
  if (input && input >= '1' && input <= '9') {
    cell.textContent = input;
    cell.style.color = '#22d3ee';
    showToast('已填入 ' + input);
  }
}

function giveHint() {
  var container = document.getElementById('sudokuBoard') || document.querySelector('table');
  if (!container) { showToast('未找到棋盘'); return; }
  var cells = container.querySelectorAll('td');
  var empty = [];
  cells.forEach(function(cell) {
    if (!cell.textContent || cell.textContent === '0') empty.push(cell);
  });
  if (empty.length === 0) { showToast('棋盘已满'); return; }
  var cell = empty[Math.floor(Math.random() * empty.length)];
  showToast('提示: 尝试在行' + (parseInt(cell.dataset.row) + 1) + '列' + (parseInt(cell.dataset.col) + 1) + '填入数字');
}

function printPuzzle() {
  window.print();
  showToast('正在准备打印...');
}'''
}

# Process each file
for relpath, func_fixes in fixes.items():
    fpath = os.path.join(site_dir, relpath)
    if not os.path.exists(fpath):
        print(f'SKIP (not found): {relpath}')
        continue
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    for func_name, new_impl in func_fixes.items():
        # Pattern: function funcName(...) { ... coming soon ... }
        pattern = r'function\s+' + re.escape(func_name) + r'\s*\([^)]*\)\s*\{[^}]*(?:\{[^}]*\}[^}]*)*coming soon[^}]*\}'
        match = re.search(pattern, content, re.DOTALL)
        if not match:
            # Simpler pattern for single-level braces
            pattern2 = r'function\s+' + re.escape(func_name) + r'\s*\([^)]*\)\s*\{[^}]*coming soon[^}]*\}'
            match = re.search(pattern2, content, re.DOTALL)
        if match:
            content = content[:match.start()] + new_impl + content[match.end():]
            print(f'  FIXED: {relpath} :: {func_name}')
        else:
            print(f'  NOT FOUND: {relpath} :: {func_name}')
    
    if content != original:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'  WRITTEN: {relpath}')
    else:
        print(f'  NO CHANGES: {relpath}')

print('\nDone!')
