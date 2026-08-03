#!/usr/bin/env python3
"""批量修复空壳工具 - 第十三轮"""
import os, re

site_dir = '/home/chison/tools-site'
fixes = {}

# === css-variables-generator ===
fixes['css-variables-generator/index.html'] = {
    'addVariable': '''function addVariable() {
  var container = document.getElementById('variables') || document.querySelector('.variables-list');
  if (!container) { showToast('未找到变量容器'); return; }
  var div = document.createElement('div');
  div.className = 'var-item';
  div.style.cssText = 'display:flex;gap:8px;align-items:center;margin-bottom:8px;padding:8px;background:#1e293b;border-radius:6px';
  div.innerHTML = '<input type="text" placeholder="--my-color" style="width:140px;background:#0f172a;color:#e2e8f0;border:1px solid #334155;border-radius:4px;padding:6px" class="var-name"><input type="color" value="#22d3ee" style="width:40px;height:32px;border:none;border-radius:4px" class="var-value-color"><input type="text" placeholder="#22d3ee" style="width:100px;background:#0f172a;color:#e2e8f0;border:1px solid #334155;border-radius:4px;padding:6px" class="var-value-text"><button onclick="this.parentElement.remove();updateVarOutput();" style="padding:4px 8px;background:#ef4444;color:#fff;border:none;border-radius:4px;cursor:pointer">✕</button>';
  container.appendChild(div);
  div.querySelector('.var-value-color').addEventListener('input', function() { div.querySelector('.var-value-text').value = this.value; updateVarOutput(); });
  div.querySelector('.var-value-text').addEventListener('input', function() { updateVarOutput(); });
  div.querySelector('.var-name').addEventListener('input', function() { updateVarOutput(); });
  updateVarOutput();
  showToast('已添加CSS变量');
}

function updateVarOutput() {
  var items = document.querySelectorAll('.var-item');
  var css = ':root {\\n';
  items.forEach(function(item) {
    var name = item.querySelector('.var-name').value;
    var val = item.querySelector('.var-value-text').value || item.querySelector('.var-value-color').value;
    if (name && val) css += '  ' + name + ': ' + val + ';\\n';
  });
  css += '}';
  var code = document.getElementById('outputCode') || document.getElementById('code');
  if (code) code.textContent = css;
  var preview = document.getElementById('preview') || document.querySelector('.preview');
  if (preview) {
    var style = document.getElementById('dynamicVars');
    if (!style) { style = document.createElement('style'); style.id = 'dynamicVars'; document.head.appendChild(style); }
    style.textContent = css;
  }
}''',
    'importJSON': '''function importJSON() {
  var input = document.getElementById('jsonInput') || document.querySelector('textarea[name="json"]');
  if (!input || !input.value.trim()) { showToast('请输入JSON'); return; }
  try {
    var data = JSON.parse(input.value);
    var container = document.getElementById('variables') || document.querySelector('.variables-list');
    if (!container) { showToast('未找到变量容器'); return; }
    container.innerHTML = '';
    Object.keys(data).forEach(function(key) {
      var div = document.createElement('div');
      div.className = 'var-item';
      div.style.cssText = 'display:flex;gap:8px;align-items:center;margin-bottom:8px;padding:8px;background:#1e293b;border-radius:6px';
      div.innerHTML = '<input type="text" value="--' + key + '" style="width:140px;background:#0f172a;color:#e2e8f0;border:1px solid #334155;border-radius:4px;padding:6px" class="var-name"><input type="color" value="#22d3ee" style="width:40px;height:32px;border:none;border-radius:4px" class="var-value-color"><input type="text" value="' + data[key] + '" style="width:100px;background:#0f172a;color:#e2e8f0;border:1px solid #334155;border-radius:4px;padding:6px" class="var-value-text"><button onclick="this.parentElement.remove();updateVarOutput();" style="padding:4px 8px;background:#ef4444;color:#fff;border:none;border-radius:4px;cursor:pointer">✕</button>';
      container.appendChild(div);
    });
    updateVarOutput();
    showToast('已导入JSON变量');
  } catch(e) {
    showToast('JSON格式错误');
  }
}'''
}

# === css-keyframe-animation-generator ===
fixes['css-keyframe-animation-generator/index.html'] = {
    'stopAnimation': '''function stopAnimation() {
  var preview = document.getElementById('preview') || document.querySelector('.preview, .animation-preview');
  if (preview) {
    preview.style.animationPlayState = 'paused';
    showToast('动画已暂停');
  }
}''',
    'updateCode': '''function updateCode() {
  var name = (document.getElementById('animName') || document.querySelector('input[name="name"]'));
  var nameVal = name ? name.value : 'myAnimation';
  var duration = (document.getElementById('duration') || document.querySelector('input[name="duration"]'));
  var durVal = duration ? duration.value : '2';
  var timing = (document.getElementById('timing') || document.querySelector('select[name="timing"]'));
  var timingVal = timing ? timing.value : 'ease';
  var iter = (document.getElementById('iteration') || document.querySelector('select[name="iteration"]'));
  var iterVal = iter ? iter.value : 'infinite';
  var direction = (document.getElementById('direction') || document.querySelector('select[name="direction"]'));
  var dirVal = direction ? direction.value : 'normal';
  
  var fromX = (document.getElementById('fromX') || {}).value || '0';
  var fromY = (document.getElementById('fromY') || {}).value || '0';
  var toX = (document.getElementById('toX') || {}).value || '100';
  var toY = (document.getElementById('toY') || {}).value || '0';
  var fromOpacity = (document.getElementById('fromOpacity') || {}).value || '1';
  var toOpacity = (document.getElementById('toOpacity') || {}).value || '0.5';
  
  var css = '@keyframes ' + nameVal + ' {\\n';
  css += '  from {\\n';
  css += '    transform: translate(' + fromX + 'px, ' + fromY + 'px);\\n';
  css += '    opacity: ' + fromOpacity + ';\\n';
  css += '  }\\n';
  css += '  to {\\n';
  css += '    transform: translate(' + toX + 'px, ' + toY + 'px);\\n';
  css += '    opacity: ' + toOpacity + ';\\n';
  css += '  }\\n';
  css += '}\\n\\n';
  css += '.element {\\n';
  css += '  animation: ' + nameVal + ' ' + durVal + 's ' + timingVal + ' ' + iterVal + ' ' + dirVal + ';\\n';
  css += '}';
  
  var code = document.getElementById('outputCode') || document.getElementById('code');
  if (code) code.textContent = css;
  
  var preview = document.getElementById('preview') || document.querySelector('.preview, .animation-preview');
  if (preview) {
    var style = document.getElementById('dynamicAnim');
    if (!style) { style = document.createElement('style'); style.id = 'dynamicAnim'; document.head.appendChild(style); }
    style.textContent = css;
    preview.style.animation = nameVal + ' ' + durVal + 's ' + timingVal + ' ' + iterVal + ' ' + dirVal;
  }
  showToast('代码已更新');
}'''
}

# === css-noise-texture-generator ===
fixes['css-noise-texture-generator/index.html'] = {
    'updateNoise': '''function updateNoise() {
  var opacity = parseFloat((document.getElementById('opacity') || document.querySelector('input[name="opacity"]')).value) || 0.5;
  var scale = parseInt((document.getElementById('scale') || document.querySelector('input[name="scale"]')).value) || 100;
  var color1 = (document.getElementById('color1') || document.querySelectorAll('input[type="color"]')[0] || {}).value || '#000000';
  var color2 = (document.getElementById('color2') || document.querySelectorAll('input[type="color"]')[1] || {}).value || '#ffffff';
  
  // Generate SVG noise
  var svg = '<svg xmlns="http://www.w3.org/2000/svg" width="' + scale + '" height="' + scale + '">';
  svg += '<filter id="n"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="4" stitchTiles="stitch"/></filter>';
  svg += '<rect width="100%" height="100%" filter="url(#n)" opacity="' + opacity + '"/>';
  svg += '</svg>';
  var dataUri = 'data:image/svg+xml,' + encodeURIComponent(svg);
  
  var preview = document.getElementById('preview') || document.querySelector('.preview');
  if (preview) preview.style.backgroundImage = 'url("' + dataUri + '")';
  
  var code = document.getElementById('outputCode') || document.getElementById('code');
  if (code) code.textContent = '.noise-bg {\\n  background-image: url("' + dataUri + '");\\n  background-size: ' + scale + 'px ' + scale + 'px;\\n  opacity: ' + opacity + ';\\n}';
  showToast('噪点纹理已更新');
}'''
}

# === css-view-transition-generator ===
fixes['css-view-transition-generator/index.html'] = {
    'playPreview': '''function playPreview() {
  var preview = document.getElementById('preview') || document.querySelector('.preview');
  if (!preview) { showToast('未找到预览区域'); return; }
  preview.style.viewTransitionName = 'preview-transition';
  preview.style.opacity = '0';
  preview.style.transform = 'scale(0.8)';
  setTimeout(function() {
    preview.style.transition = 'all 0.5s ease';
    preview.style.opacity = '1';
    preview.style.transform = 'scale(1)';
  }, 50);
  showToast('播放过渡动画');
}''',
    'selectType': '''function selectType() {
  var sel = document.getElementById('transitionType') || document.querySelector('select[name="type"]');
  if (!sel) { showToast('请选择过渡类型'); return; }
  var type = sel.value;
  var code = document.getElementById('outputCode') || document.getElementById('code');
  var css = '';
  if (type === 'fade') {
    css = '::view-transition-old(root) {\\n  animation: fade-out 0.3s ease forwards;\\n}\\n::view-transition-new(root) {\\n  animation: fade-in 0.3s ease forwards;\\n}';
  } else if (type === 'slide') {
    css = '::view-transition-old(root) {\\n  animation: slide-out-left 0.3s ease forwards;\\n}\\n::view-transition-new(root) {\\n  animation: slide-in-right 0.3s ease forwards;\\n}';
  } else if (type === 'zoom') {
    css = '::view-transition-old(root) {\\n  animation: zoom-out 0.3s ease forwards;\\n}\\n::view-transition-new(root) {\\n  animation: zoom-in 0.3s ease forwards;\\n}';
  } else {
    css = '::view-transition-old(root) {\\n  animation: fade-out 0.3s ease forwards;\\n}\\n::view-transition-new(root) {\\n  animation: fade-in 0.3s ease forwards;\\n}';
  }
  if (code) code.textContent = css;
  showToast('已选择' + type + '过渡');
}''',
    'updateConfig': '''function updateConfig() {
  var duration = (document.getElementById('duration') || document.querySelector('input[name="duration"]')).value || '0.3';
  var easing = (document.getElementById('easing') || document.querySelector('select[name="easing"]')).value || 'ease';
  var code = document.getElementById('outputCode') || document.getElementById('code');
  if (code) {
    var txt = code.textContent;
    txt = txt.replace(/\\d+\\.?\\d*s/g, duration + 's');
    txt = txt.replace(/ease[a-z-]*|linear|cubic-bezier\\([^)]+\\)/g, easing);
    code.textContent = txt;
  }
  showToast('配置已更新');
}'''
}

# === css-clip-path-animation ===
fixes['css-clip-path-animation/index.html'] = {
    'stopAnimation': '''function stopAnimation() {
  var preview = document.getElementById('preview') || document.querySelector('.preview');
  if (preview) {
    preview.style.animationPlayState = 'paused';
    showToast('动画已暂停');
  }
}''',
    'updateCode': '''function updateCode() {
  var fromShape = (document.getElementById('fromShape') || document.querySelectorAll('select')[0] || {}).value || 'circle(50%)';
  var toShape = (document.getElementById('toShape') || document.querySelectorAll('select')[1] || {}).value || 'polygon(50% 0%, 100% 100%, 0% 100%)';
  var duration = (document.getElementById('duration') || document.querySelector('input[name="duration"]') || {}).value || '2';
  
  var css = '@keyframes clipAnim {\\n';
  css += '  0% { clip-path: ' + fromShape + '; }\\n';
  css += '  100% { clip-path: ' + toShape + '; }\\n';
  css += '}\\n\\n';
  css += '.element {\\n  animation: clipAnim ' + duration + 's ease infinite alternate;\\n}';
  
  var code = document.getElementById('outputCode') || document.getElementById('code');
  if (code) code.textContent = css;
  
  var preview = document.getElementById('preview') || document.querySelector('.preview');
  if (preview) {
    var style = document.getElementById('dynamicClip');
    if (!style) { style = document.createElement('style'); style.id = 'dynamicClip'; document.head.appendChild(style); }
    style.textContent = css;
    preview.style.animation = 'clipAnim ' + duration + 's ease infinite alternate';
  }
  showToast('代码已更新');
}'''
}

# === css-grid-inspector ===
fixes['css-grid-inspector/index.html'] = {
    'renderGrid': '''function renderGrid() {
  var cols = parseInt((document.getElementById('cols') || document.querySelector('input[name="cols"]')).value) || 3;
  var rows = parseInt((document.getElementById('rows') || document.querySelector('input[name="rows"]')).value) || 3;
  var gap = parseInt((document.getElementById('gap') || document.querySelector('input[name="gap"]')).value) || 10;
  var colTemplate = (document.getElementById('colTemplate') || document.querySelector('input[name="colTemplate"]'));
  
  var preview = document.getElementById('preview') || document.querySelector('.preview, .grid-preview');
  if (!preview) { showToast('未找到预览区域'); return; }
  preview.innerHTML = '';
  preview.style.display = 'grid';
  preview.style.gridTemplateColumns = colTemplate && colTemplate.value ? colTemplate.value : 'repeat(' + cols + ', 1fr)';
  preview.style.gridTemplateRows = 'repeat(' + rows + ', 1fr)';
  preview.style.gap = gap + 'px';
  
  for (var i = 0; i < cols * rows; i++) {
    var cell = document.createElement('div');
    cell.style.cssText = 'background:rgba(34,211,238,0.15);border:1px solid rgba(34,211,238,0.3);display:flex;align-items:center;justify-content:center;color:#22d3ee;font-size:0.85rem;min-height:40px';
    cell.textContent = i + 1;
    preview.appendChild(cell);
  }
  
  var code = document.getElementById('outputCode') || document.getElementById('code');
  if (code) {
    code.textContent = '.grid-container {\\n  display: grid;\\n  grid-template-columns: ' + (colTemplate && colTemplate.value ? colTemplate.value : 'repeat(' + cols + ', 1fr)') + ';\\n  grid-template-rows: repeat(' + rows + ', 1fr);\\n  gap: ' + gap + 'px;\\n}';
  }
  showToast('网格已渲染: ' + cols + '×' + rows);
}'''
}

# === git-command-generator ===
fixes['git-command-generator/index.html'] = {
    'onOperationChange': '''function onOperationChange() {
  var sel = document.getElementById('operation') || document.querySelector('select[name="operation"]');
  if (!sel) return;
  var op = sel.value;
  var panels = document.querySelectorAll('.op-panel');
  panels.forEach(function(p) { p.style.display = 'none'; });
  var active = document.getElementById('panel-' + op);
  if (active) active.style.display = 'block';
  generateCommand();
  showToast('已切换到: ' + op);
}

function generateCommand() {
  var sel = document.getElementById('operation') || document.querySelector('select[name="operation"]');
  if (!sel) return;
  var op = sel.value;
  var cmd = 'git ' + op;
  var output = document.getElementById('output') || document.getElementById('commandOutput') || document.querySelector('.output');
  if (output) output.textContent = cmd;
}'''
}

# === git-diff-viewer ===
fixes['git-diff-viewer/index.html'] = {
    'renderDiff': '''function renderDiff() {
  var input1 = document.getElementById('text1') || document.querySelectorAll('textarea')[0];
  var input2 = document.getElementById('text2') || document.querySelectorAll('textarea')[1];
  if (!input1 || !input2) { showToast('未找到输入区域'); return; }
  var lines1 = input1.value.split('\\n');
  var lines2 = input2.value.split('\\n');
  var output = document.getElementById('diffOutput') || document.querySelector('.diff-output, #output');
  if (!output) { showToast('未找到输出区域'); return; }
  
  var html = '';
  var maxLen = Math.max(lines1.length, lines2.length);
  for (var i = 0; i < maxLen; i++) {
    var l1 = lines1[i] || '';
    var l2 = lines2[i] || '';
    if (l1 === l2) {
      html += '<div style="color:#94a3b8;padding:2px 8px">  ' + escapeHtml(l1) + '</div>';
    } else {
      if (l1) html += '<div style="color:#ef4444;padding:2px 8px;background:rgba(239,68,68,0.1)">- ' + escapeHtml(l1) + '</div>';
      if (l2) html += '<div style="color:#22c55e;padding:2px 8px;background:rgba(34,197,94,0.1)">+ ' + escapeHtml(l2) + '</div>';
    }
  }
  output.innerHTML = html;
  showToast('差异已渲染');
}

function escapeHtml(s) {
  return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}''',
    'switchMode': '''function switchMode() {
  var sel = document.getElementById('diffMode') || document.querySelector('select[name="mode"]');
  if (!sel) return;
  var mode = sel.value;
  var output = document.getElementById('diffOutput') || document.querySelector('.diff-output, #output');
  if (output) {
    if (mode === 'unified') output.style.fontFamily = 'monospace';
    else if (mode === 'split') output.style.display = 'flex';
  }
  renderDiff();
  showToast('已切换到' + mode + '模式');
}'''
}

# === http-to-curl ===
fixes['http-to-curl/index.html'] = {
    'addHeader': '''function addHeader() {
  var container = document.getElementById('headers') || document.querySelector('.headers-list');
  if (!container) { showToast('未找到头部容器'); return; }
  var div = document.createElement('div');
  div.className = 'header-item';
  div.style.cssText = 'display:flex;gap:8px;margin-bottom:8px';
  div.innerHTML = '<input type="text" placeholder="Header名称" style="flex:1;background:#0f172a;color:#e2e8f0;border:1px solid #334155;border-radius:4px;padding:6px" class="h-key"><input type="text" placeholder="Header值" style="flex:1;background:#0f172a;color:#e2e8f0;border:1px solid #334155;border-radius:4px;padding:6px" class="h-val"><button onclick="this.parentElement.remove();generateCurl();" style="padding:6px 10px;background:#ef4444;color:#fff;border:none;border-radius:4px;cursor:pointer">✕</button>';
  container.appendChild(div);
  showToast('已添加Header');
}''',
    'addQueryParam': '''function addQueryParam() {
  var container = document.getElementById('queryParams') || document.querySelector('.params-list');
  if (!container) { showToast('未找到参数容器'); return; }
  var div = document.createElement('div');
  div.className = 'param-item';
  div.style.cssText = 'display:flex;gap:8px;margin-bottom:8px';
  div.innerHTML = '<input type="text" placeholder="参数名" style="flex:1;background:#0f172a;color:#e2e8f0;border:1px solid #334155;border-radius:4px;padding:6px" class="p-key"><input type="text" placeholder="参数值" style="flex:1;background:#0f172a;color:#e2e8f0;border:1px solid #334155;border-radius:4px;padding:6px" class="p-val"><button onclick="this.parentElement.remove();generateCurl();" style="padding:6px 10px;background:#ef4444;color:#fff;border:none;border-radius:4px;cursor:pointer">✕</button>';
  container.appendChild(div);
  showToast('已添加查询参数');
}''',
    'parseCurl': '''function parseCurl() {
  var input = document.getElementById('curlInput') || document.querySelector('textarea');
  if (!input || !input.value.trim()) { showToast('请输入curl命令'); return; }
  var curl = input.value.trim();
  
  var method = 'GET';
  var url = '';
  var headers = [];
  var body = '';
  
  var m = curl.match(/-X\\s+(\\w+)/);
  if (m) method = m[1].toUpperCase();
  
  m = curl.match(/curl\\s+['"]?(https?:\\/\\/[^'\"\\s]+)/);
  if (m) url = m[1];
  
  var headerMatches = curl.matchAll(/-H\\s+['"]([^'"]+)['"]/g);
  for (var hm of headerMatches) {
    var parts = hm[1].split(':\\s*');
    if (parts.length >= 2) headers.push({key: parts[0], val: parts.slice(1).join(': ')});
  }
  
  m = curl.match(/-d\\s+['"]([^'"]+)['"]/);
  if (m) { body = m[1]; if (method === 'GET') method = 'POST'; }
  
  if (document.getElementById('method')) document.getElementById('method').value = method;
  if (document.getElementById('url')) document.getElementById('url').value = url;
  if (document.getElementById('body')) document.getElementById('body').value = body;
  
  showToast('已解析curl命令: ' + method + ' ' + url);
}'''
}

# === code-playground ===
fixes['code-playground/index.html'] = {
    'autoRun': '''function autoRun() {
  var checkbox = document.getElementById('autoRun') || document.querySelector('input[type="checkbox"]');
  if (checkbox) {
    if (checkbox.checked) {
      runCode();
      showToast('自动运行已开启');
    } else {
      showToast('自动运行已关闭');
    }
  }
}''',
    'runCode': '''function runCode() {
  var html = (document.getElementById('htmlCode') || document.querySelectorAll('textarea')[0] || {}).value || '';
  var css = (document.getElementById('cssCode') || document.querySelectorAll('textarea')[1] || {}).value || '';
  var js = (document.getElementById('jsCode') || document.querySelectorAll('textarea')[2] || {}).value || '';
  
  var iframe = document.getElementById('preview') || document.querySelector('iframe');
  if (!iframe) { showToast('未找到预览区域'); return; }
  
  var doc = iframe.contentDocument || iframe.contentWindow.document;
  doc.open();
  doc.write('<html><head><style>' + css + '</style></head><body>' + html + '<script>' + js + '<\\/script></body></html>');
  doc.close();
  showToast('代码已运行');
}'''
}

# === flowchart-generator ===
fixes['flowchart-generator/index.html'] = {
    'adjustZoom': '''function adjustZoom(delta) {
  var canvas = document.getElementById('canvas') || document.querySelector('.canvas, svg');
  if (!canvas) { showToast('未找到画布'); return; }
  var currentZoom = parseFloat(canvas.dataset.zoom || '1');
  var newZoom = Math.max(0.25, Math.min(4, currentZoom + (delta || 0.1)));
  canvas.dataset.zoom = newZoom;
  canvas.style.transform = 'scale(' + newZoom + ')';
  canvas.style.transformOrigin = 'center center';
  showToast('缩放: ' + Math.round(newZoom * 100) + '%');
}''',
    'renderChart': '''function renderChart() {
  var input = document.getElementById('chartData') || document.querySelector('textarea');
  var canvas = document.getElementById('canvas') || document.querySelector('.canvas, svg');
  if (!input || !canvas) { showToast('未找到输入或画布'); return; }
  
  var lines = input.value.trim().split('\\n');
  var svg = '<svg width="100%" height="400" xmlns="http://www.w3.org/2000/svg" style="background:#0f172a">';
  var y = 40;
  var x = 50;
  
  lines.forEach(function(line, i) {
    line = line.trim();
    if (!line) return;
    var parts = line.split('->');
    if (parts.length >= 2) {
      // Draw arrow
      svg += '<line x1="' + (x + 120) + '" y1="' + y + '" x2="' + (x + 180) + '" y2="' + y + '" stroke="#22d3ee" stroke-width="2" marker-end="url(#arrowhead)"/>';
      svg += '<rect x="' + x + '" y="' + (y - 20) + '" width="120" height="40" rx="8" fill="#1e293b" stroke="#22d3ee" stroke-width="1.5"/>';
      svg += '<text x="' + (x + 60) + '" y="' + y + '" fill="#e2e8f0" text-anchor="middle" dy=".35em" font-size="13">' + escapeXml(parts[0].trim()) + '</text>';
      x += 180;
      svg += '<rect x="' + x + '" y="' + (y - 20) + '" width="120" height="40" rx="8" fill="#1e293b" stroke="#22d3ee" stroke-width="1.5"/>';
      svg += '<text x="' + (x + 60) + '" y="' + y + '" fill="#e2e8f0" text-anchor="middle" dy=".35em" font-size="13">' + escapeXml(parts[1].trim()) + '</text>';
      y += 60;
      x = 50;
    } else {
      svg += '<rect x="' + x + '" y="' + (y - 20) + '" width="120" height="40" rx="8" fill="#1e293b" stroke="#22d3ee" stroke-width="1.5"/>';
      svg += '<text x="' + (x + 60) + '" y="' + y + '" fill="#e2e8f0" text-anchor="middle" dy=".35em" font-size="13">' + escapeXml(line) + '</text>';
      y += 60;
    }
  });
  
  svg += '<defs><marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0, 10 3.5, 0 7" fill="#22d3ee"/></marker></defs>';
  svg += '</svg>';
  canvas.innerHTML = svg;
  showToast('流程图已渲染');
}

function escapeXml(s) {
  return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}'''
}

# === sql-query-builder ===
fixes['sql-query-builder/index.html'] = {
    'switchType': '''function switchType() {
  var sel = document.getElementById('queryType') || document.querySelector('select[name="type"]');
  if (!sel) return;
  var type = sel.value;
  var panels = document.querySelectorAll('.query-panel');
  panels.forEach(function(p) { p.style.display = 'none'; });
  var active = document.getElementById('panel-' + type);
  if (active) active.style.display = 'block';
  buildSQL();
  showToast('已切换到' + type.toUpperCase() + '查询');
}''',
    'addWhere': '''function addWhere() {
  addClauseRow('where', 'WHERE条件');
}''',
    'addDeleteWhere': '''function addDeleteWhere() {
  addClauseRow('deleteWhere', 'DELETE条件');
}''',
    'addUpdateWhere': '''function addUpdateWhere() {
  addClauseRow('updateWhere', 'UPDATE条件');
}''',
    'addUpdateField': '''function addUpdateField() {
  addClauseRow('updateField', 'SET字段');
}''',
    'addGroupBy': '''function addGroupBy() {
  addClauseRow('groupBy', 'GROUP BY字段');
}''',
    'addHaving': '''function addHaving() {
  addClauseRow('having', 'HAVING条件');
}''',
    'addInsertField': '''function addInsertField() {
  addClauseRow('insertField', 'INSERT字段');
}''',
    'addJoin': '''function addJoin() {
  addClauseRow('join', 'JOIN表');
}''',
    'addOrderBy': '''function addOrderBy() {
  addClauseRow('orderBy', 'ORDER BY字段');
}''',
    'addUpdateField': '''function addUpdateField() {
  addClauseRow('updateField', 'SET字段');
}''',
    'buildSQL': '''function buildSQL() {
  var type = (document.getElementById('queryType') || document.querySelector('select[name="type"]') || {}).value || 'select';
  var table = (document.getElementById('tableName') || document.querySelector('input[name="table"]') || {}).value || 'my_table';
  var sql = '';
  
  if (type === 'select') {
    var fields = getClauseValues('selectField');
    var fieldStr = fields.length ? fields.join(', ') : '*';
    sql = 'SELECT ' + fieldStr + ' FROM ' + table;
    var joins = getClauseValues('join');
    joins.forEach(function(j) { sql += ' JOIN ' + j; });
    var wheres = getClauseValues('where');
    if (wheres.length) sql += ' WHERE ' + wheres.join(' AND ');
    var groupBys = getClauseValues('groupBy');
    if (groupBys.length) sql += ' GROUP BY ' + groupBys.join(', ');
    var havings = getClauseValues('having');
    if (havings.length) sql += ' HAVING ' + havings.join(' AND ');
    var orderBys = getClauseValues('orderBy');
    if (orderBys.length) sql += ' ORDER BY ' + orderBys.join(', ');
  } else if (type === 'insert') {
    var fields = getClauseValues('insertField');
    var vals = getClauseValues('insertValue');
    sql = 'INSERT INTO ' + table;
    if (fields.length) sql += ' (' + fields.join(', ') + ')';
    if (vals.length) sql += ' VALUES (' + vals.join(', ') + ')';
  } else if (type === 'update') {
    var sets = getClauseValues('updateField');
    var wheres = getClauseValues('updateWhere');
    sql = 'UPDATE ' + table;
    if (sets.length) sql += ' SET ' + sets.join(', ');
    if (wheres.length) sql += ' WHERE ' + wheres.join(' AND ');
  } else if (type === 'delete') {
    var wheres = getClauseValues('deleteWhere');
    sql = 'DELETE FROM ' + table;
    if (wheres.length) sql += ' WHERE ' + wheres.join(' AND ');
  }
  
  var output = document.getElementById('sqlOutput') || document.getElementById('output') || document.querySelector('.output');
  if (output) output.textContent = sql + ';';
  showToast('SQL已生成');
}

function addClauseRow(clauseType, label) {
  var container = document.getElementById(clauseType + 'Container') || document.querySelector('.' + clauseType + '-list');
  if (!container) { showToast('未找到' + label + '容器'); return; }
  var div = document.createElement('div');
  div.className = clauseType + '-row';
  div.style.cssText = 'display:flex;gap:8px;margin-bottom:8px';
  div.innerHTML = '<input type="text" placeholder="' + label + '" style="flex:1;background:#0f172a;color:#e2e8f0;border:1px solid #334155;border-radius:4px;padding:6px" data-clause="' + clauseType + '"><button onclick="this.parentElement.remove();buildSQL();" style="padding:6px 10px;background:#ef4444;color:#fff;border:none;border-radius:4px;cursor:pointer">✕</button>';
  container.appendChild(div);
  div.querySelector('input').addEventListener('input', buildSQL);
  showToast('已添加' + label);
}

function getClauseValues(clauseType) {
  var vals = [];
  document.querySelectorAll('[data-clause="' + clauseType + '"]').forEach(function(input) {
    if (input.value.trim()) vals.push(input.value.trim());
  });
  return vals;
}''',
    'importSQL': '''function importSQL() {
  var input = document.getElementById('sqlInput') || document.querySelector('textarea[name="sql"]');
  if (!input || !input.value.trim()) { showToast('请输入SQL'); return; }
  var sql = input.value.trim();
  var output = document.getElementById('sqlOutput') || document.getElementById('output') || document.querySelector('.output');
  if (output) output.textContent = sql;
  showToast('已导入SQL');
}'''
}

# Process
for relpath, func_fixes in fixes.items():
    fpath = os.path.join(site_dir, relpath)
    if not os.path.exists(fpath):
        print(f'SKIP (not found): {relpath}')
        continue
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    for func_name, new_impl in func_fixes.items():
        pattern = r'function\s+' + re.escape(func_name) + r'\s*\([^)]*\)\s*\{[^}]*(?:\{[^}]*\}[^}]*)*coming soon[^}]*\}'
        match = re.search(pattern, content, re.DOTALL)
        if not match:
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

print('\nDone!')
