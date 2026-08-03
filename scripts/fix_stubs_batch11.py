#!/usr/bin/env python3
"""Fix stub functions in tool pages - Batch 11"""
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

# 1. morse-decoder: playMorse()
fix_tool(f'{BASE}/morse-decoder/index.html', 'playMorse', '''function playMorse() {
  var result = document.getElementById('resultOutput');
  if (!result || !result.value.trim()) { showToast('请先转换摩尔斯码'); return; }
  var morse = result.value.trim();
  var freq = parseInt(document.getElementById('freq').value) || 700;
  var wpm = parseInt(document.getElementById('speed').value) || 15;
  var unit = 1.2 / wpm; // seconds per dot
  try {
    var ctx = new (window.AudioContext || window.webkitAudioContext)();
    var time = ctx.currentTime;
    for (var i = 0; i < morse.length; i++) {
      var ch = morse[i];
      if (ch === '.') {
        playTone(ctx, freq, time, unit);
        time += unit * 2;
      } else if (ch === '-') {
        playTone(ctx, freq, time, unit * 3);
        time += unit * 4;
      } else if (ch === ' ') {
        time += unit * 3;
      } else if (ch === '/') {
        time += unit * 7;
      }
    }
    showToast('正在播放摩尔斯码');
  } catch(e) {
    showToast('音频播放不支持');
  }
}
function playTone(ctx, freq, startTime, duration) {
  var osc = ctx.createOscillator();
  var gain = ctx.createGain();
  osc.frequency.value = freq;
  osc.type = 'sine';
  gain.gain.setValueAtTime(0, startTime);
  gain.gain.linearRampToValueAtTime(0.3, startTime + 0.01);
  gain.gain.setValueAtTime(0.3, startTime + duration - 0.01);
  gain.gain.linearRampToValueAtTime(0, startTime + duration);
  osc.connect(gain);
  gain.connect(ctx.destination);
  osc.start(startTime);
  osc.stop(startTime + duration);
}''')

# 2. punycode-converter: usePreset()
fix_tool(f'{BASE}/punycode-converter/index.html', 'usePreset', '''function usePreset() {
  var presets = ['\\u4e2d\\u56fd.cn', 'm\\u00fcnchen.de', '\\u65e5\\u672c.jp', 'r\\u00e9sum\\u00e9.com', '\\u4e16\\u754c.com'];
  var input = document.getElementById('pInput');
  if (input) {
    input.value = presets[Math.floor(Math.random() * presets.length)];
    if (typeof convert === 'function') convert();
  }
  showToast('已加载预设');
}''')

# 3. ip-lookup: lookupMyIP()
fix_tool(f'{BASE}/ip-lookup/index.html', 'lookupMyIP', '''function lookupMyIP() {
  var resultArea = document.getElementById('resultArea');
  if (resultArea) {
    resultArea.innerHTML = '<div style="text-align:center;padding:20px;color:#94a3b8">正在查询本机IP地址...</div>';
  }
  fetch('https://api.ipify.org?format=json')
    .then(function(r) { return r.json(); })
    .then(function(data) {
      var ip = data.ip;
      document.getElementById('ipInput').value = ip;
      if (typeof lookup === 'function') lookup();
      else lookupIPInfo(ip);
    })
    .catch(function() {
      fetch('https://api.ipify.org?format=text')
        .then(function(r) { return r.text(); })
        .then(function(ip) {
          document.getElementById('ipInput').value = ip;
          if (typeof lookup === 'function') lookup();
          else lookupIPInfo(ip);
        })
        .catch(function() {
          if (resultArea) resultArea.innerHTML = '<div style="color:#f87171">查询失败，请检查网络连接</div>';
          showToast('查询失败');
        });
    });
}
function lookupIPInfo(ip) {
  var resultArea = document.getElementById('resultArea');
  if (!resultArea) return;
  resultArea.innerHTML = '<div style="text-align:center;padding:20px;color:#94a3b8">正在查询IP信息...</div>';
  fetch('https://ipapi.co/' + ip + '/json/')
    .then(function(r) { return r.json(); })
    .then(function(data) {
      var html = '<div style="display:grid;grid-template-columns:1fr 1fr;gap:12px">';
      html += ipInfoCard('IP地址', ip);
      html += ipInfoCard('城市', data.city || '-');
      html += ipInfoCard('地区', data.region || '-');
      html += ipInfoCard('国家', data.country_name || '-');
      html += ipInfoCard('运营商', data.org || '-');
      html += ipInfoCard('时区', data.timezone || '-');
      html += ipInfoCard('经度', data.longitude || '-');
      html += ipInfoCard('纬度', data.latitude || '-');
      html += '</div>';
      resultArea.innerHTML = html;
      showToast('查询完成');
    })
    .catch(function() {
      resultArea.innerHTML = '<div style="color:#f87171">IP信息查询失败</div>';
      showToast('查询失败');
    });
}
function ipInfoCard(label, value) {
  return '<div style="background:#0f172a;padding:12px;border-radius:8px;border:1px solid rgba(148,163,184,.1)"><div style="color:#64748b;font-size:.8rem;margin-bottom:4px">' + label + '</div><div style="color:#e2e8f0;font-weight:500">' + value + '</div></div>';
}''')

# 4. jsonpath-tester: executeQuery()
fix_tool(f'{BASE}/jsonpath-tester/index.html', 'executeQuery', '''function executeQuery() {
  var jsonInput = document.getElementById('jsonInput').value.trim();
  var pathInput = document.getElementById('jsonPathInput').value.trim();
  var resultBox = document.getElementById('resultBox');
  var resultStats = document.getElementById('resultStats');
  if (!jsonInput) { showToast('请输入JSON数据'); return; }
  if (!pathInput) { showToast('请输入JSONPath表达式'); return; }
  
  var data;
  try {
    data = JSON.parse(jsonInput);
  } catch(e) {
    resultBox.innerHTML = '<span style="color:#f87171">JSON解析错误: ' + e.message + '</span>';
    return;
  }
  
  try {
    var results = jsonPath(data, pathInput);
    if (results.length === 0) {
      resultStats.textContent = '0 个匹配';
      resultBox.innerHTML = '<span style="color:#94a3b8">没有匹配的结果</span>';
    } else {
      resultStats.textContent = results.length + ' 个匹配';
      var html = '<pre style="background:#0f172a;padding:12px;border-radius:8px;overflow-x:auto;color:#7ee787;font-size:.85rem">' + JSON.stringify(results, null, 2) + '</pre>';
      resultBox.innerHTML = html;
    }
    showToast('查询完成');
  } catch(e) {
    resultBox.innerHTML = '<span style="color:#f87171">JSONPath错误: ' + e.message + '</span>';
  }
}
function jsonPath(obj, path) {
  if (!path.startsWith('$')) path = '$' + path;
  path = path.substring(1);
  var tokens = [];
  var current = '';
  var inBracket = false;
  for (var i = 0; i < path.length; i++) {
    var ch = path[i];
    if (ch === '.' && !inBracket) {
      if (current) tokens.push(current);
      current = '';
    } else if (ch === '[') {
      if (current) tokens.push(current);
      current = '';
      inBracket = true;
    } else if (ch === ']') {
      tokens.push(current);
      current = '';
      inBracket = false;
    } else {
      current += ch;
    }
  }
  if (current) tokens.push(current);
  
  var results = [obj];
  for (var t = 0; t < tokens.length; t++) {
    var token = tokens[t];
    var newResults = [];
    for (var r = 0; r < results.length; r++) {
      var item = results[r];
      if (token === '*') {
        if (Array.isArray(item)) {
          for (var k = 0; k < item.length; k++) newResults.push(item[k]);
        } else if (item && typeof item === 'object') {
          for (var key in item) newResults.push(item[key]);
        }
      } else if (/^\\d+$/.test(token)) {
        var idx = parseInt(token);
        if (Array.isArray(item) && idx < item.length) newResults.push(item[idx]);
      } else {
        if (item && typeof item === 'object' && item[token] !== undefined) {
          newResults.push(item[token]);
        }
      }
    }
    results = newResults;
  }
  return results;
}''')

# 5. file-hash-checker: compareAll()
fix_tool(f'{BASE}/file-hash-checker/index.html', 'compareAll', '''function compareAll() {
  var compareHash = document.getElementById('compareHash').value.trim();
  var resultsSection = document.getElementById('resultsSection');
  if (!compareHash) { showToast('请输入对比哈希值'); return; }
  if (!resultsSection) return;
  var hashElements = resultsSection.querySelectorAll('[data-hash]');
  if (hashElements.length === 0) { showToast('请先计算文件哈希'); return; }
  var matchCount = 0;
  var compareLower = compareHash.toLowerCase().trim();
  for (var i = 0; i < hashElements.length; i++) {
    var el = hashElements[i];
    var fileHash = (el.getAttribute('data-hash') || '').toLowerCase().trim();
    var algo = el.getAttribute('data-algo') || '';
    var statusEl = el.querySelector('.compare-status') || document.createElement('span');
    statusEl.className = 'compare-status';
    if (fileHash === compareLower) {
      statusEl.innerHTML = ' \\u2705 匹配';
      statusEl.style.color = '#4ade80';
      matchCount++;
    } else {
      statusEl.innerHTML = ' \\u274c 不匹配';
      statusEl.style.color = '#f87171';
    }
    if (!statusEl.parentElement) el.appendChild(statusEl);
  }
  showToast(matchCount > 0 ? matchCount + '个哈希匹配' : '无匹配');
}''')

# 6. margin-calculator: sm()
fix_tool(f'{BASE}/margin-calculator/index.html', 'sm', '''function sm() {
  var mode = document.getElementById('mode').value;
  var v1 = parseFloat(document.getElementById('v1').value) || 0;
  var v2 = parseFloat(document.getElementById('v2').value) || 0;
  var cost, revenue, profit, margin, markup;
  
  if (mode === 'cr') {
    cost = v1; revenue = v2;
    profit = revenue - cost;
    margin = revenue > 0 ? (profit / revenue * 100) : 0;
    markup = cost > 0 ? (profit / cost * 100) : 0;
  } else if (mode === 'cm') {
    cost = v1; margin = v2;
    revenue = cost / (1 - margin / 100);
    profit = revenue - cost;
    markup = cost > 0 ? (profit / cost * 100) : 0;
  } else if (mode === 'rm') {
    revenue = v1; margin = v2;
    cost = revenue * (1 - margin / 100);
    profit = revenue - cost;
    markup = cost > 0 ? (profit / cost * 100) : 0;
  } else if (mode === 'cp') {
    cost = v1; markup = v2;
    revenue = cost * (1 + markup / 100);
    profit = revenue - cost;
    margin = revenue > 0 ? (profit / revenue * 100) : 0;
  } else {
    cost = v1; revenue = v2;
    profit = revenue - cost;
    margin = revenue > 0 ? (profit / revenue * 100) : 0;
    markup = cost > 0 ? (profit / cost * 100) : 0;
  }
  
  document.getElementById('rM').textContent = margin.toFixed(2) + '%';
  document.getElementById('rMP').textContent = markup.toFixed(2) + '%';
  document.getElementById('rP').textContent = profit.toFixed(2);
  document.getElementById('rC').textContent = cost.toFixed(2);
  document.getElementById('rR').textContent = revenue.toFixed(2);
  
  // Update labels based on mode
  var fg1 = document.getElementById('fg1');
  var fg2 = document.getElementById('fg2');
  if (fg1 && fg2) {
    var labels = {
      'cr': ['成本价', '售价/收入'],
      'cm': ['成本价', '毛利率(%)'],
      'rm': ['售价/收入', '毛利率(%)'],
      'cp': ['成本价', '加价率(%)']
    };
    var l = labels[mode] || labels['cr'];
    fg1.querySelector('label').textContent = l[0];
    fg2.querySelector('label').textContent = l[1];
  }
}''')

# 7. text-indentation-fixer: fixIndent()
fix_tool(f'{BASE}/text-indentation-fixer/index.html', 'fixIndent', '''function fixIndent() {
  var input = document.getElementById('inputText').value;
  var output = document.getElementById('outputText');
  if (!input.trim()) { showToast('请输入文本'); return; }
  var lines = input.split('\\n');
  var fixedLines = [];
  var indentLevel = 0;
  var indentStr = '  '; // 2 spaces
  
  for (var i = 0; i < lines.length; i++) {
    var line = lines[i];
    var trimmed = line.trim();
    if (!trimmed) { fixedLines.push(''); continue; }
    
    // Decrease indent for closing brackets
    if (/^[}\\]\\)]/.test(trimmed)) {
      indentLevel = Math.max(0, indentLevel - 1);
    }
    
    var indent = '';
    for (var j = 0; j < indentLevel; j++) indent += indentStr;
    fixedLines.push(indent + trimmed);
    
    // Increase indent for opening brackets
    var opens = (trimmed.match(/[\\{\\[\\(]/g) || []).length;
    var closes = (trimmed.match(/[}\\]\\)]/g) || []).length;
    if (opens > closes) {
      indentLevel += opens - closes;
    } else if (closes > opens && /^[}\\]\\)]/.test(trimmed)) {
      // Already decreased above
    }
  }
  output.value = fixedLines.join('\\n');
  showToast('缩进修复完成');
}''')

# 8. text-chunk-splitter: splitText()
fix_tool(f'{BASE}/text-chunk-splitter/index.html', 'splitText', '''function splitText() {
  var input = document.getElementById('inputText').value;
  var strategy = document.getElementById('strategy').value;
  var chunkSize = parseInt(document.getElementById('chunkSize').value) || 500;
  var overlap = parseInt(document.getElementById('overlapSize').value) || 0;
  var resultSection = document.getElementById('resultSection');
  if (!input.trim()) { showToast('请输入文本'); return; }
  
  var chunks = [];
  if (strategy === 'char') {
    for (var i = 0; i < input.length; i += chunkSize - overlap) {
      chunks.push(input.substring(i, i + chunkSize));
      if (i + chunkSize >= input.length) break;
    }
  } else if (strategy === 'word') {
    var words = input.split(/\\s+/);
    for (var i = 0; i < words.length; i += chunkSize - overlap) {
      chunks.push(words.slice(i, i + chunkSize).join(' '));
      if (i + chunkSize >= words.length) break;
    }
  } else if (strategy === 'sentence') {
    var sentences = input.match(/[^.!?]+[.!?]+|[^.!?]+$/g) || [input];
    var current = '';
    var count = 0;
    for (var i = 0; i < sentences.length; i++) {
      if (count + 1 > chunkSize && current) {
        chunks.push(current);
        if (overlap > 0 && overlap < sentences.length) {
          var overlapSentences = sentences.slice(Math.max(0, i - overlap), i);
          current = overlapSentences.join('') + sentences[i];
          count = overlapSentences.length + 1;
        } else {
          current = sentences[i];
          count = 1;
        }
      } else {
        current += sentences[i];
        count++;
      }
    }
    if (current) chunks.push(current);
  } else if (strategy === 'line') {
    var lines = input.split('\\n');
    for (var i = 0; i < lines.length; i += chunkSize - overlap) {
      chunks.push(lines.slice(i, i + chunkSize).join('\\n'));
      if (i + chunkSize >= lines.length) break;
    }
  } else {
    // paragraph
    var paras = input.split(/\\n\\s*\\n/);
    var currentP = '';
    var countP = 0;
    for (var i = 0; i < paras.length; i++) {
      if (countP + 1 > chunkSize && currentP) {
        chunks.push(currentP);
        currentP = paras[i];
        countP = 1;
      } else {
        currentP += (currentP ? '\\n\\n' : '') + paras[i];
        countP++;
      }
    }
    if (currentP) chunks.push(currentP);
  }
  
  var html = '<div style="margin-bottom:12px;color:#94a3b8;font-size:.9rem">共分成 ' + chunks.length + ' 个文本块</div>';
  for (var i = 0; i < chunks.length; i++) {
    html += '<div style="background:#0f172a;border-radius:8px;padding:12px;margin-bottom:8px;border:1px solid rgba(148,163,184,.1)">';
    html += '<div style="display:flex;justify-content:space-between;margin-bottom:8px"><span style="color:#22d3ee;font-size:.85rem">块 #' + (i+1) + '</span><span style="color:#64748b;font-size:.8rem">' + chunks[i].length + ' 字符</span></div>';
    html += '<pre style="white-space:pre-wrap;color:#e2e8f0;font-size:.85rem;margin:0;max-height:200px;overflow-y:auto">' + chunks[i].replace(/</g,'&lt;').replace(/>/g,'&gt;') + '</pre>';
    html += '</div>';
  }
  resultSection.innerHTML = html;
  resultSection.style.display = 'block';
  showToast('分块完成，共' + chunks.length + '块');
}''')

# 9. shipping-calculator: addPackage()
fix_tool(f'{BASE}/shipping-calculator/index.html', 'addPackage', '''function addPackage() {
  var container = document.getElementById('packages') || document.querySelector('.packages-container');
  if (!container) { showToast('包裹容器未找到'); return; }
  var count = container.querySelectorAll('.package-item').length;
  var newIdx = count;
  var html = '<div class="package-item" style="border:1px solid rgba(148,163,184,.2);border-radius:8px;padding:12px;margin-bottom:8px">';
  html += '<div class="form-row" style="display:flex;gap:8px;flex-wrap:wrap">';
  html += '<div class="form-group" style="flex:1;min-width:120px"><label>重量 (kg)</label><input type="number" id="pkg_w_' + newIdx + '" step="0.1" min="0" placeholder="0" oninput="calcShipping()"></div>';
  html += '<div class="form-group" style="flex:1;min-width:120px"><label>运输距离</label><select id="pkg_d_' + newIdx + '" onchange="calcShipping()"><option value="local">同城</option><option value="domestic">国内</option><option value="international">国际</option></select></div>';
  html += '<div class="form-group" style="flex:1;min-width:120px"><label>包裹类型</label><select id="pkg_t_' + newIdx + '" onchange="calcShipping()"><option value="standard">标准</option><option value="express">快递</option><option value="fragile">易碎</option></select></div>';
  html += '<button class="btn btn-danger" style="align-self:flex-end" onclick="this.closest(\\'.package-item\\').remove();calcShipping()">删除</button>';
  html += '</div></div>';
  container.insertAdjacentHTML('beforeend', html);
  showToast('已添加包裹 #' + (newIdx + 1));
  if (typeof calcShipping === 'function') calcShipping();
}''')

# 10. resolution-calculator: calcRes()
fix_tool(f'{BASE}/resolution-calculator/index.html', 'calcRes', '''function calcRes() {
  var w = parseInt(document.getElementById('width').value) || 0;
  var h = parseInt(document.getElementById('height').value) || 0;
  var diagonal = parseFloat(document.getElementById('diagonal').value) || 0;
  if (w <= 0 || h <= 0) { showToast('请输入有效的宽度和高度'); return; }
  
  // Aspect ratio (simplified)
  function gcd(a, b) { return b === 0 ? a : gcd(b, a % b); }
  var g = gcd(w, h);
  var aspectW = w / g, aspectH = h / g;
  // Simplify common ratios
  if (aspectW > 50 || aspectH > 50) {
    var ratio = w / h;
    var common = [[16,9],[4,3],[21,9],[16,10],[3,2],[5,4],[1,1]];
    var bestDiff = Infinity, bestW = aspectW, bestH = aspectH;
    for (var i = 0; i < common.length; i++) {
      var diff = Math.abs(ratio - common[i][0] / common[i][1]);
      if (diff < bestDiff) { bestDiff = diff; bestW = common[i][0]; bestH = common[i][1]; }
    }
    aspectW = bestW; aspectH = bestH;
  }
  document.getElementById('rAspect').textContent = aspectW + ':' + aspectH;
  
  // Total pixels
  var pixels = w * h;
  document.getElementById('rPixels').textContent = pixels.toLocaleString();
  document.getElementById('rMP').textContent = (pixels / 1000000).toFixed(2);
  
  // PPI and diagonal
  var diagPixels = Math.sqrt(w * w + h * h);
  if (diagonal > 0) {
    var ppi = diagPixels / diagonal;
    document.getElementById('rPPI').textContent = Math.round(ppi) + ' PPI';
    document.getElementById('rDiag').textContent = diagonal + '"';
  } else {
    document.getElementById('rPPI').textContent = '- 需输入对角线';
    document.getElementById('rDiag').textContent = diagPixels + ' px';
  }
  showToast('计算完成');
}''')

print("\nBatch 11 done. Verifying...")
