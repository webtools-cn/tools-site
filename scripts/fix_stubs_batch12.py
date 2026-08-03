#!/usr/bin/env python3
"""Fix stub functions in tool pages - Batch 12"""
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

# 1. css-box-model: updateBoxModel()
fix_tool(f'{BASE}/css-box-model/index.html', 'updateBoxModel', '''function updateBoxModel() {
  var w = parseInt(document.getElementById('width').value) || 0;
  var h = parseInt(document.getElementById('height').value) || 0;
  var pt = parseInt(document.getElementById('paddingTop').value) || 0;
  var pr = parseInt(document.getElementById('paddingRight').value) || 0;
  var pb = parseInt(document.getElementById('paddingBottom').value) || 0;
  var pl = parseInt(document.getElementById('paddingLeft').value) || 0;
  var bt = parseInt(document.getElementById('borderTop').value) || 0;
  var br = parseInt(document.getElementById('borderRight').value) || 0;
  var bb = parseInt(document.getElementById('borderBottom').value) || 0;
  var bl = parseInt(document.getElementById('borderLeft').value) || 0;
  var mt = parseInt(document.getElementById('marginTop').value) || 0;
  var mr = parseInt(document.getElementById('marginRight').value) || 0;
  var mb = parseInt(document.getElementById('marginBottom').value) || 0;
  var ml = parseInt(document.getElementById('marginLeft').value) || 0;
  
  var boxSizing = document.querySelector('input[name="boxSizing"]:checked');
  var sizing = boxSizing ? boxSizing.value : 'content';
  
  var contentW = w, contentH = h;
  if (sizing === 'border') {
    contentW = Math.max(0, w - pl - pr - bl - br);
    contentH = Math.max(0, h - pt - pb - bt - bb);
  }
  
  var paddingBoxW = contentW + pl + pr;
  var paddingBoxH = contentH + pt + pb;
  var borderBoxW = paddingBoxW + bl + br;
  var borderBoxH = paddingBoxH + bt + bb;
  var marginBoxW = borderBoxW + ml + mr;
  var marginBoxH = borderBoxH + mt + mb;
  
  var preview = document.getElementById('boxPreview');
  if (preview) {
    preview.style.width = borderBoxW + 'px';
    preview.style.height = borderBoxH + 'px';
    preview.style.padding = pt + 'px ' + pr + 'px ' + pb + 'px ' + pl + 'px';
    preview.style.borderWidth = bt + 'px ' + br + 'px ' + bb + 'px ' + bl + 'px';
    preview.style.margin = mt + 'px ' + mr + 'px ' + mb + 'px ' + ml + 'px';
  }
  
  var codeEl = document.getElementById('cssCode');
  if (codeEl) {
    var code = '.box {\\n';
    code += '  width: ' + w + 'px;\\n';
    code += '  height: ' + h + 'px;\\n';
    code += '  padding: ' + pt + 'px ' + pr + 'px ' + pb + 'px ' + pl + 'px;\\n';
    code += '  border-width: ' + bt + 'px ' + br + 'px ' + bb + 'px ' + bl + 'px;\\n';
    code += '  margin: ' + mt + 'px ' + mr + 'px ' + mb + 'px ' + ml + 'px;\\n';
    code += '  box-sizing: ' + (sizing === 'border' ? 'border-box' : 'content-box') + ';\\n';
    code += '}';
    codeEl.textContent = code;
  }
  
  var sizesEl = document.getElementById('sizeInfo');
  if (sizesEl) {
    sizesEl.innerHTML = '<div>Content: ' + contentW + ' x ' + contentH + '</div>' +
      '<div>Padding Box: ' + paddingBoxW + ' x ' + paddingBoxH + '</div>' +
      '<div>Border Box: ' + borderBoxW + ' x ' + borderBoxH + '</div>' +
      '<div>Margin Box: ' + marginBoxW + ' x ' + marginBoxH + '</div>';
  }
}''')

# 2. pet-age-calculator: updateResult()
fix_tool(f'{BASE}/pet-age-calculator/index.html', 'updateResult', '''function updateResult() {
  var petType = document.getElementById('petType').value;
  var petAge = parseFloat(document.getElementById('petAge').value) || 0;
  var resultDiv = document.getElementById('result') || document.getElementById('resultArea');
  if (!resultDiv) return;
  
  var humanAge = 0, description = '';
  if (petType === 'dog') {
    if (petAge <= 0) humanAge = 0;
    else if (petAge <= 1) humanAge = petAge * 15;
    else if (petAge <= 2) humanAge = 15 + (petAge - 1) * 9;
    else if (petAge <= 5) humanAge = 24 + (petAge - 2) * 4;
    else humanAge = 24 + 12 + (petAge - 5) * 5;
    description = '狗狗年龄换算';
  } else if (petType === 'cat') {
    if (petAge <= 0) humanAge = 0;
    else if (petAge <= 1) humanAge = petAge * 15;
    else if (petAge <= 2) humanAge = 15 + (petAge - 1) * 9;
    else humanAge = 24 + (petAge - 2) * 4;
    description = '猫咪年龄换算';
  } else if (petType === 'rabbit') {
    humanAge = petAge * 8;
    description = '兔子年龄换算';
  } else if (petType === 'hamster') {
    humanAge = petAge * 25;
    description = '仓鼠年龄换算';
  } else if (petType === 'bird') {
    humanAge = petAge * 5;
    description = '鸟类年龄换算';
  } else {
    humanAge = petAge * 7;
    description = '通用年龄换算';
  }
  
  var html = '<div style="text-align:center;padding:20px">';
  html += '<div style="color:#94a3b8;font-size:.9rem;margin-bottom:8px">' + description + '</div>';
  html += '<div style="font-size:3rem;font-weight:700;color:#22d3ee">' + Math.round(humanAge) + '</div>';
  html += '<div style="color:#94a3b8;font-size:.85rem;margin-top:4px">相当于人类年龄</div>';
  html += '</div>';
  resultDiv.innerHTML = html;
}''')

# 3. fuzzy-string-matcher: search()
fix_tool(f'{BASE}/fuzzy-string-matcher/index.html', 'search', '''function search() {
  var query = document.getElementById('searchInput').value.trim();
  var candidatesText = document.getElementById('candidates').value.trim();
  var algorithm = document.getElementById('algorithm').value;
  var ngramSize = parseInt(document.getElementById('ngramSize').value) || 2;
  var maxResults = parseInt(document.getElementById('maxResults').value) || 10;
  var resultSection = document.getElementById('resultSection');
  
  if (!query) { showToast('请输入搜索字符串'); return; }
  if (!candidatesText) { showToast('请输入候选词'); return; }
  
  var candidates = candidatesText.split('\\n').map(function(s) { return s.trim(); }).filter(function(s) { return s; });
  var results = [];
  
  for (var i = 0; i < candidates.length; i++) {
    var score = 0;
    if (algorithm === 'levenshtein') {
      var dist = levenshtein(query.toLowerCase(), candidates[i].toLowerCase());
      var maxLen = Math.max(query.length, candidates[i].length);
      score = maxLen > 0 ? (1 - dist / maxLen) * 100 : 0;
    } else if (algorithm === 'ngram') {
      score = ngramSimilarity(query.toLowerCase(), candidates[i].toLowerCase(), ngramSize);
    } else if (algorithm === 'jaro') {
      score = jaroSimilarity(query.toLowerCase(), candidates[i].toLowerCase()) * 100;
    } else {
      // contains
      score = candidates[i].toLowerCase().includes(query.toLowerCase()) ? 100 : 0;
    }
    results.push({ word: candidates[i], score: Math.round(score) });
  }
  
  results.sort(function(a, b) { return b.score - a.score; });
  results = results.slice(0, maxResults);
  
  var html = '<div style="margin-bottom:12px;color:#94a3b8;font-size:.9rem">找到 ' + results.length + ' 个匹配结果</div>';
  for (var i = 0; i < results.length; i++) {
    var r = results[i];
    var color = r.score >= 80 ? '#4ade80' : r.score >= 50 ? '#fbbf24' : '#f87171';
    html += '<div style="display:flex;justify-content:space-between;align-items:center;padding:8px 12px;background:#0f172a;border-radius:8px;margin-bottom:6px;border:1px solid rgba(148,163,184,.1)">';
    html += '<span style="color:#e2e8f0">' + r.word.replace(/</g,'&lt;') + '</span>';
    html += '<span style="color:' + color + ';font-weight:600">' + r.score + '%</span>';
    html += '</div>';
  }
  resultSection.innerHTML = html;
  resultSection.style.display = 'block';
  showToast('搜索完成');
}
function levenshtein(a, b) {
  var m = [];
  for (var i = 0; i <= a.length; i++) m[i] = [i];
  for (var j = 0; j <= b.length; j++) m[0][j] = j;
  for (var i = 1; i <= a.length; i++) {
    for (var j = 1; j <= b.length; j++) {
      m[i][j] = a[i-1] === b[j-1] ? m[i-1][j-1] : Math.min(m[i-1][j-1]+1, m[i][j-1]+1, m[i-1][j]+1);
    }
  }
  return m[a.length][b.length];
}
function ngramSimilarity(a, b, n) {
  if (a.length < n || b.length < n) return a === b ? 100 : 0;
  var gramsA = {}, gramsB = {};
  for (var i = 0; i <= a.length - n; i++) { var g = a.substr(i, n); gramsA[g] = (gramsA[g]||0)+1; }
  for (var i = 0; i <= b.length - n; i++) { var g = b.substr(i, n); gramsB[g] = (gramsB[g]||0)+1; }
  var intersection = 0, union = 0;
  for (var g in gramsA) { intersection += Math.min(gramsA[g], gramsB[g]||0); union += gramsA[g]; }
  for (var g in gramsB) { if (!gramsA[g]) union += gramsB[g]; }
  return union > 0 ? (intersection / union) * 100 : 0;
}
function jaroSimilarity(a, b) {
  if (a === b) return 1;
  if (a.length === 0 || b.length === 0) return 0;
  var matchDist = Math.floor(Math.max(a.length, b.length) / 2) - 1;
  if (matchDist < 0) matchDist = 0;
  var aMatches = [], bMatches = [];
  var matches = 0;
  for (var i = 0; i < a.length; i++) {
    var start = Math.max(0, i - matchDist);
    var end = Math.min(i + matchDist + 1, b.length);
    for (var j = start; j < end; j++) {
      if (bMatches[j]) continue;
      if (a[i] !== b[j]) continue;
      aMatches[i] = true; bMatches[j] = true; matches++; break;
    }
  }
  if (matches === 0) return 0;
  var t = 0, k = 0;
  for (var i = 0; i < a.length; i++) {
    if (!aMatches[i]) continue;
    while (!bMatches[k]) k++;
    if (a[i] !== b[k]) t++;
    k++;
  }
  t = t / 2;
  return (matches/a.length + matches/b.length + (matches-t)/matches) / 3;
}''')

# 4. screen-resolution-simulator: rotateScreen()
fix_tool(f'{BASE}/screen-resolution-simulator/index.html', 'rotateScreen', '''function rotateScreen() {
  var w = document.getElementById('resW') || document.getElementById('width');
  var h = document.getElementById('resH') || document.getElementById('height');
  if (w && h) {
    var tmp = w.value;
    w.value = h.value;
    h.value = tmp;
    if (typeof updatePreview === 'function') updatePreview();
  }
  showToast('已旋转屏幕');
}''')

# 5. curl-builder: addHeader()
fix_tool(f'{BASE}/curl-builder/index.html', 'addHeader', '''function addHeader() {
  var container = document.getElementById('headersContainer');
  if (!container) return;
  var row = document.createElement('div');
  row.className = 'header-row';
  row.style.cssText = 'display:flex;gap:8px;margin-bottom:8px';
  row.innerHTML = '<input type="text" placeholder="Header名称，如 Content-Type" class="h-key" style="flex:1" oninput="updateCmd()"><input type="text" placeholder="Header值，如 application/json" class="h-val" style="flex:1" oninput="updateCmd()"><button class="btn btn-sm btn-danger" onclick="this.parentElement.remove();updateCmd()">\\u2715</button>';
  container.appendChild(row);
  showToast('已添加请求头');
}''')

# 6. html-breadcrumb-generator: addItem()
fix_tool(f'{BASE}/html-breadcrumb-generator/index.html', 'addItem', '''function addItem() {
  var container = document.getElementById('itemsContainer') || document.querySelector('.items-list');
  if (!container) { showToast('容器未找到'); return; }
  var count = container.querySelectorAll('.breadcrumb-item-row').length;
  var row = document.createElement('div');
  row.className = 'breadcrumb-item-row';
  row.style.cssText = 'display:flex;gap:8px;margin-bottom:8px;align-items:center';
  row.innerHTML = '<input type="text" placeholder="面包屑文本" class="crumb-text" value="页面' + (count+1) + '" style="flex:1" oninput="updatePreview()"><input type="text" placeholder="链接URL" class="crumb-url" value="#" style="flex:1" oninput="updatePreview()"><button class="btn btn-sm btn-danger" onclick="this.parentElement.remove();updatePreview()">\\u2715</button>';
  container.appendChild(row);
  if (typeof updatePreview === 'function') updatePreview();
  showToast('已添加面包屑项');
}''')

# 7. css-speech-bubble-generator: updateBubble()
fix_tool(f'{BASE}/css-speech-bubble-generator/index.html', 'updateBubble', '''function updateBubble() {
  var borderRadius = document.getElementById('borderRadius').value;
  var padding = document.getElementById('padding').value;
  var borderWidth = document.getElementById('borderWidth').value;
  var arrowSize = document.getElementById('arrowSize').value;
  var shadow = document.getElementById('shadow').value;
  var bubbleText = document.getElementById('bubbleText').value || '';
  var bgColor = document.getElementById('bgColor') ? document.getElementById('bgColor').value : '#1e293b';
  var textColor = document.getElementById('textColor') ? document.getElementById('textColor').value : '#e2e8f0';
  var borderColor = document.getElementById('borderColor') ? document.getElementById('borderColor').value : '#334155';
  var arrowPos = document.getElementById('arrowPos') ? document.getElementById('arrowPos').value : 'left';
  
  var preview = document.getElementById('bubblePreview');
  if (preview) {
    preview.style.borderRadius = borderRadius + 'px';
    preview.style.padding = padding + 'px';
    preview.style.borderWidth = borderWidth + 'px';
    preview.style.borderStyle = 'solid';
    preview.style.borderColor = borderColor;
    preview.style.background = bgColor;
    preview.style.color = textColor;
    preview.textContent = bubbleText;
    if (shadow === 'small') preview.style.boxShadow = '0 2px 8px rgba(0,0,0,.2)';
    else if (shadow === 'medium') preview.style.boxShadow = '0 4px 16px rgba(0,0,0,.3)';
    else if (shadow === 'large') preview.style.boxShadow = '0 8px 32px rgba(0,0,0,.4)';
    else preview.style.boxShadow = 'none';
  }
  
  var codeEl = document.getElementById('bubbleCode');
  if (codeEl) {
    var code = '.bubble {\\n';
    code += '  position: relative;\\n';
    code += '  background: ' + bgColor + ';\\n';
    code += '  color: ' + textColor + ';\\n';
    code += '  border: ' + borderWidth + 'px solid ' + borderColor + ';\\n';
    code += '  border-radius: ' + borderRadius + 'px;\\n';
    code += '  padding: ' + padding + 'px;\\n';
    if (shadow !== 'none') code += '  box-shadow: ' + preview.style.boxShadow + ';\\n';
    code += '}\\n\\n';
    code += '.bubble::' + (arrowPos === 'right' ? 'after' : 'before') + ' {\\n';
    code += '  content: "";\\n';
    code += '  position: absolute;\\n';
    if (arrowPos === 'left') {
      code += '  left: -' + arrowSize + 'px;\\n';
      code += '  top: 50%;\\n';
      code += '  transform: translateY(-50%);\\n';
      code += '  border: ' + arrowSize + 'px solid transparent;\\n';
      code += '  border-right-color: ' + borderColor + ';\\n';
    } else {
      code += '  right: -' + arrowSize + 'px;\\n';
      code += '  top: 50%;\\n';
      code += '  transform: translateY(-50%);\\n';
      code += '  border: ' + arrowSize + 'px solid transparent;\\n';
      code += '  border-left-color: ' + borderColor + ';\\n';
    }
    code += '}';
    codeEl.textContent = code;
  }
}''')

# 8. svg-path-editor: parsePath()
fix_tool(f'{BASE}/svg-path-editor/index.html', 'parsePath', '''function parsePath() {
  var input = document.getElementById('pathInput').value.trim();
  var parseText = document.getElementById('parseText');
  if (!input) { showToast('请输入SVG路径'); return; }
  
  var commands = [];
  var re = /([MmLlHhVvCcSsQqTtAaZz])([^MmLlHhVvCcSsQqTtAaZz]*)/g;
  var match;
  while ((match = re.exec(input)) !== null) {
    var cmd = match[1];
    var args = match[2].trim().split(/[\\s,]+/).filter(function(s) { return s; }).map(parseFloat);
    var desc = '';
    switch(cmd.toUpperCase()) {
      case 'M': desc = 'Move To'; break;
      case 'L': desc = 'Line To'; break;
      case 'H': desc = 'Horizontal Line'; break;
      case 'V': desc = 'Vertical Line'; break;
      case 'C': desc = 'Cubic Bezier'; break;
      case 'S': desc = 'Smooth Cubic'; break;
      case 'Q': desc = 'Quadratic Bezier'; break;
      case 'T': desc = 'Smooth Quadratic'; break;
      case 'A': desc = 'Arc'; break;
      case 'Z': desc = 'Close Path'; break;
    }
    commands.push({ cmd: cmd, desc: desc, args: args });
  }
  
  var html = '<div style="color:#94a3b8;font-size:.85rem;margin-bottom:8px">共 ' + commands.length + ' 条指令</div>';
  for (var i = 0; i < commands.length; i++) {
    var c = commands[i];
    html += '<div style="display:flex;gap:12px;padding:6px 8px;background:#0f172a;border-radius:6px;margin-bottom:4px;font-size:.8rem">';
    html += '<span style="color:#22d3ee;font-weight:600;min-width:24px">' + c.cmd + '</span>';
    html += '<span style="color:#94a3b8;min-width:100px">' + c.desc + '</span>';
    html += '<span style="color:#e2e8f0">' + (c.args.length ? c.args.join(', ') : '-') + '</span>';
    html += '</div>';
  }
  parseText.innerHTML = html;
  
  // Render SVG preview
  var svgEl = document.getElementById('svgPreview');
  if (svgEl) {
    var viewSize = parseInt(document.getElementById('viewSize').value) || 200;
    var stroke = document.getElementById('strokeColor').value;
    var fill = document.getElementById('fillColor').value;
    var sw = document.getElementById('strokeWidth').value;
    svgEl.innerHTML = '<svg viewBox="0 0 ' + viewSize + ' ' + viewSize + '" width="' + viewSize + '" height="' + viewSize + '"><path d="' + input.replace(/</g,'&lt;') + '" stroke="' + stroke + '" fill="' + fill + '" stroke-width="' + sw + '"/></svg>';
  }
  showToast('解析完成，共' + commands.length + '条指令');
}''')

# 9. data-uri-generator: processFile()
fix_tool(f'{BASE}/data-uri-generator/index.html', 'processFile', '''function processFile() {
  var fileInput = document.getElementById('fileInput');
  var resultArea = document.getElementById('resultArea');
  var resultData = document.getElementById('resultData');
  if (!fileInput || !fileInput.files || fileInput.files.length === 0) { showToast('请选择文件'); return; }
  var file = fileInput.files[0];
  if (file.size > 1024 * 1024) { showToast('文件过大，请选择小于1MB的文件'); return; }
  var reader = new FileReader();
  reader.onload = function(e) {
    var dataUri = e.target.result;
    resultData.textContent = dataUri;
    resultArea.style.display = 'block';
    var sizeInfo = document.getElementById('sizeInfo');
    if (sizeInfo) {
      var originalSize = file.size;
      var encodedSize = dataUri.length;
      var ratio = ((encodedSize / originalSize - 1) * 100).toFixed(1);
      sizeInfo.innerHTML = '原始大小: ' + originalSize + ' bytes | 编码后: ' + encodedSize + ' bytes | 增长: ' + ratio + '%';
    }
    showToast('文件编码完成');
  };
  reader.onerror = function() { showToast('文件读取失败'); };
  reader.readAsDataURL(file);
}''')

# 10. js-obfuscator: obfuscate()
fix_tool(f'{BASE}/js-obfuscator/index.html', 'obfuscate', '''function obfuscate() {
  var input = document.getElementById('inputCode').value;
  var output = document.getElementById('outputCode');
  if (!input.trim()) { showToast('请输入代码'); return; }
  
  var result = input;
  // Variable name obfuscation
  var varNames = {};
  var counter = 0;
  result = result.replace(/\\b(var|let|const)\\s+([a-zA-Z_$][a-zA-Z0-9_$]*)/g, function(match, keyword, name) {
    if (!varNames[name]) {
      varNames[name] = '_0x' + counter.toString(16).padStart(4, '0');
      counter++;
    }
    return keyword + ' ' + varNames[name];
  });
  // Replace all occurrences of obfuscated variable names
  for (var original in varNames) {
    var obf = varNames[original];
    result = result.replace(new RegExp('\\\\b' + original + '\\\\b', 'g'), obf);
  }
  // String encoding (hex)
  result = result.replace(/'([^'\\n]*)'/g, function(match, str) {
    if (str.length < 3) return match;
    var hex = str.split('').map(function(c) { return '\\\\x' + c.charCodeAt(0).toString(16).padStart(2, '0'); }).join('');
    return "'" + hex + "'";
  });
  result = result.replace(/"([^"\\n]*)"/g, function(match, str) {
    if (str.length < 3) return match;
    var hex = str.split('').map(function(c) { return '\\\\x' + c.charCodeAt(0).toString(16).padStart(2, '0'); }).join('');
    return '"' + hex + '"';
  });
  // Remove comments
  result = result.replace(/\\/\\/[^\n]*/g, '');
  result = result.replace(/\\/\\*[\\s\\S]*?\\*\\//g, '');
  // Remove extra whitespace
  result = result.replace(/\\n\\s*\\n/g, '\\n');
  result = result.trim();
  
  output.value = result;
  showToast('混淆完成');
}''')

print("\nBatch 12 done.")
