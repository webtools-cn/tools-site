#!/usr/bin/env python3
"""Fix stub functions in tool pages - Batch 10"""
import os, re

def fix_tool(path, fn_name, new_impl):
    """Replace a stub function with real implementation"""
    content = open(path).read()
    # Match the stub function pattern
    pattern = rf'function\s+{fn_name}\s*\([^)]*\)\s*\{{\s*showToast\([^)]*coming soon[^)]*\);\s*\}}'
    # Use lambda to avoid escape processing in replacement
    new_content = re.sub(pattern, lambda m: new_impl, content, count=1)
    if new_content == content:
        print(f"  WARNING: Pattern not found for {fn_name} in {path}")
        return False
    open(path, 'w').write(new_content)
    return True

BASE = '/home/chison/tools-site'

# 1. cookie-parser: parseCookie()
fix_tool(f'{BASE}/cookie-parser/index.html', 'parseCookie', '''function parseCookie() {
  var input = document.getElementById('cookieInput').value.trim();
  if (!input) { showToast('请输入Cookie字符串'); return; }
  var urlDecode = document.getElementById('urlDecode').checked;
  var showRaw = document.getElementById('showRaw').checked;
  var result = document.getElementById('cookieResult');
  var cookies = [];
  var parts = input.split(';');
  for (var i = 0; i < parts.length; i++) {
    var part = parts[i].trim();
    if (!part) continue;
    var eqIdx = part.indexOf('=');
    if (eqIdx === -1) {
      cookies.push({name: part, value: '', attrs: []});
    } else {
      var name = part.substring(0, eqIdx).trim();
      var value = part.substring(eqIdx + 1).trim();
      if (urlDecode) {
        try { value = decodeURIComponent(value); } catch(e) {}
      }
      cookies.push({name: name, value: value, attrs: []});
    }
  }
  var attrNames = ['HttpOnly', 'Secure', 'SameSite', 'Max-Age', 'Expires', 'Domain', 'Path'];
  for (var ci = 0; ci < cookies.length; ci++) {
    var c = cookies[ci];
    for (var ai = 0; ai < attrNames.length; ai++) {
      var a = attrNames[ai];
      var re = new RegExp('\\\\b' + a + '=([^;]+)', 'i');
      var m = input.match(re);
      if (m) c.attrs.push(a + '=' + m[1].trim());
      else if (new RegExp('\\\\b' + a + '\\\\b', 'i').test(input) && c.name.toLowerCase() !== a.toLowerCase()) {
        if (c.attrs.indexOf(a) === -1) c.attrs.push(a);
      }
    }
  }
  if (cookies.length === 0) {
    result.innerHTML = '<span style="color:#f87171">未解析到Cookie</span>';
    return;
  }
  var html = '<table style="width:100%;border-collapse:collapse;font-size:.9rem">';
  html += '<thead><tr style="background:#0f172a"><th style="padding:8px;text-align:left;border-bottom:1px solid #334155">名称</th><th style="padding:8px;text-align:left;border-bottom:1px solid #334155">值</th><th style="padding:8px;text-align:left;border-bottom:1px solid #334155">属性</th></tr></thead><tbody>';
  for (var k = 0; k < cookies.length; k++) {
    var c = cookies[k];
    var displayVal = showRaw ? c.value : (c.value.length > 50 ? c.value.substring(0,50) + '...' : c.value);
    html += '<tr style="border-bottom:1px solid rgba(148,163,184,.1)">';
    html += '<td style="padding:8px;color:#22d3ee;font-weight:500">' + escapeHtml(c.name) + '</td>';
    html += '<td style="padding:8px;color:#e2e8f0;word-break:break-all">' + escapeHtml(displayVal) + '</td>';
    html += '<td style="padding:8px;color:#94a3b8;font-size:.8rem">' + (c.attrs.length ? c.attrs.join(', ') : '-') + '</td>';
    html += '</tr>';
  }
  html += '</tbody></table>';
  html += '<div style="margin-top:12px;color:#64748b;font-size:.85rem">共解析到 ' + cookies.length + ' 个Cookie</div>';
  result.innerHTML = html;
  showToast('解析完成，共' + cookies.length + '个Cookie');
}
function escapeHtml(s) { return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;'); }''')

# 2. text-to-hex: hexToText()
fix_tool(f'{BASE}/text-to-hex/index.html', 'hexToText', '''function hexToText() {
  var input = document.getElementById('hexInput').value.trim();
  var output = document.getElementById('textOutput');
  if (!input) { output.textContent = ''; return; }
  var hex = input.replace(/0x/gi, '').replace(/\\s+/g, '').replace(/,/g, '');
  if (!/^[0-9a-fA-F]*$/.test(hex) || hex.length % 2 !== 0) {
    output.innerHTML = '<span style="color:#f87171">无效的十六进制字符串</span>';
    return;
  }
  var text = '';
  for (var i = 0; i < hex.length; i += 2) {
    text += String.fromCharCode(parseInt(hex.substr(i, 2), 16));
  }
  try {
    text = decodeURIComponent(escape(text));
  } catch(e) {}
  output.textContent = text;
}''')

# 3. flip-text-generator: processFlip()
fix_tool(f'{BASE}/flip-text-generator/index.html', 'processFlip', '''function processFlip() {
  var input = document.getElementById('inputText').value;
  var resultArea = document.getElementById('resultArea');
  var resultText = document.getElementById('resultText');
  var previewBox = document.getElementById('previewBox');
  var previewText = document.getElementById('previewText');
  if (!input.trim()) {
    resultArea.style.display = 'none';
    previewBox.style.display = 'none';
    return;
  }
  var result = '';
  if (currentMode === 'vertical') {
    for (var i = 0; i < input.length; i++) {
      result += flipMap[input[i]] || input[i];
    }
  } else if (currentMode === 'horizontal') {
    for (var i = input.length - 1; i >= 0; i--) {
      result += input[i];
    }
  } else if (currentMode === 'full') {
    for (var i = input.length - 1; i >= 0; i--) {
      result += flipMap[input[i]] || input[i];
    }
  }
  resultText.textContent = result;
  resultArea.style.display = 'block';
  previewText.textContent = result;
  previewBox.style.display = 'block';
}
var flipMap = {'a':'\\u0250','b':'q','c':'\\u0254','d':'p','e':'\\u01DD','f':'\\u025F','g':'\\u0183','h':'\\u0265','i':'\\u0131','j':'\\u027E','k':'\\u029E','l':'l','m':'\\u026F','n':'u','o':'o','p':'d','q':'b','r':'\\u0279','s':'s','t':'\\u0287','u':'n','v':'\\u028C','w':'\\u028D','x':'x','y':'\\u028E','z':'z','A':'\\u0250','B':'Q','C':'\\u0186','D':'D','E':'\\u018E','F':'\\u2132','G':'\\u2141','H':'H','I':'I','J':'\\u017F','K':'\\u22CA','L':'\\u2142','M':'W','N':'N','O':'O','P':'\\u0500','Q':'\\u038C','R':'\\u1D1A','S':'S','T':'\\u22A5','U':'\\u2229','V':'\\u039B','W':'M','X':'X','Y':'\\u2144','Z':'Z','.':'\\u02D9',',':"'"  ,"'":',','!':'\\u00A1','?':'\\u00BF','(':')',')':'(','[':']',']':'[','{':'}','}':'{','<':'>','>':'<','1':'\\u21C2','6':'9','9':'6'};
var currentMode = 'vertical';
function setMode(m) {
  currentMode = m;
  document.querySelectorAll('.mode-card').forEach(function(c) { c.classList.remove('active'); });
  var el = document.getElementById('mode-' + m);
  if (el) el.classList.add('active');
  processFlip();
}''')

# 4. pig-latin: translate()
fix_tool(f'{BASE}/pig-latin/index.html', 'translate', '''function translate() {
  var input = document.getElementById('input').value;
  var output = document.getElementById('output');
  if (!input.trim()) { output.value = ''; return; }
  var suffix = currentSuffix || 'ay';
  var result = '';
  if (currentMode === 'encode') {
    result = input.replace(/\\b([a-zA-Z]+)\\b/g, function(word) {
      return encodeWord(word, suffix);
    });
  } else {
    result = input.replace(/\\b([a-zA-Z]+)\\b/g, function(word) {
      return decodeWord(word, suffix);
    });
  }
  output.value = result;
}
var currentMode = 'encode';
var currentSuffix = 'ay';
function setMode(m) {
  currentMode = m;
  document.querySelectorAll('.mode-tab').forEach(function(t) { t.classList.remove('active'); });
  if (event && event.target) event.target.classList.add('active');
  var il = document.getElementById('input-label');
  var ol = document.getElementById('output-label');
  if (il) il.textContent = m === 'encode' ? '输入英文文本' : '输入Pig Latin文本';
  if (ol) ol.textContent = m === 'encode' ? 'Pig Latin结果' : '英文结果';
}
function setSuffix(s, el) {
  currentSuffix = s;
  document.querySelectorAll('.suffix-option').forEach(function(o) { o.classList.remove('active'); });
  el.classList.add('active');
}
function encodeWord(word, suffix) {
  if (/^[aeiouAEIOU]/.test(word)) {
    return word + suffix;
  }
  var match = word.match(/^([^aeiouAEIOU]*)(.*)/);
  if (!match) return word + suffix;
  var consonants = match[1];
  var rest = match[2];
  var isCapital = word[0] === word[0].toUpperCase();
  var result = rest + consonants + 'ay';
  if (isCapital) {
    result = result.charAt(0).toUpperCase() + result.slice(1).toLowerCase();
  }
  return result;
}
function decodeWord(word, suffix) {
  var lower = word.toLowerCase();
  if (lower.endsWith(suffix)) {
    var stem = word.substring(0, word.length - suffix.length);
    if (suffix === 'way' || suffix === 'yay') {
      return stem;
    }
    var match = stem.match(/^(.+?)([aeiou].*)$/i);
    if (match) {
      var consonants = match[1];
      var rest = match[2];
      var isCapital = word[0] === word[0].toUpperCase();
      var result = consonants + rest;
      if (isCapital) {
        result = result.charAt(0).toUpperCase() + result.slice(1).toLowerCase();
      }
      return result;
    }
    return stem;
  }
  return word;
}''')

# 5. text-wrap-width: wrapText()
fix_tool(f'{BASE}/text-wrap-width/index.html', 'wrapText', '''function wrapText() {
  var input = document.getElementById('inputText').value;
  var lineWidth = parseInt(document.getElementById('lineWidth').value) || 80;
  var firstIndent = parseInt(document.getElementById('firstIndent').value) || 0;
  var hangIndent = parseInt(document.getElementById('hangIndent').value) || 0;
  var breakMode = document.getElementById('breakMode').value;
  var resultSection = document.getElementById('resultSection');
  var resultText = document.getElementById('resultText');
  
  if (!input.trim()) { showToast('请输入文本'); return; }
  
  var words = input.split(/\\s+/).filter(function(w) { return w.length > 0; });
  var lines = [];
  var currentLine = '';
  var currentWidth = 0;
  var isFirstLine = true;
  
  for (var i = 0; i < words.length; i++) {
    var word = words[i];
    var indent = isFirstLine ? firstIndent : hangIndent;
    var availableWidth = lineWidth - indent;
    var prefix = '';
    for (var j = 0; j < indent; j++) prefix += ' ';
    
    if (currentLine === '') {
      if (word.length > availableWidth) {
        if (breakMode === 'none') {
          lines.push(prefix + word);
          currentLine = '';
        } else {
          var broken = word;
          while (broken.length > availableWidth) {
            var part = broken.substring(0, availableWidth);
            if (breakMode === 'hyphen' && broken.length > availableWidth) {
              part = part.substring(0, availableWidth - 1) + '-';
            }
            lines.push(prefix + part);
            broken = broken.substring(breakMode === 'hyphen' ? availableWidth - 1 : availableWidth);
            prefix = '';
            for (var j2 = 0; j2 < hangIndent; j2++) prefix += ' ';
          }
          currentLine = prefix + broken;
          currentWidth = broken.length;
        }
      } else {
        currentLine = prefix + word;
        currentWidth = word.length;
      }
      isFirstLine = false;
    } else {
      if (currentWidth + 1 + word.length > lineWidth - (isFirstLine ? firstIndent : hangIndent)) {
        lines.push(currentLine);
        isFirstLine = false;
        var newPrefix = '';
        for (var j3 = 0; j3 < hangIndent; j3++) newPrefix += ' ';
        if (word.length > lineWidth - hangIndent) {
          if (breakMode === 'none') {
            lines.push(newPrefix + word);
            currentLine = '';
          } else {
            var broken = word;
            while (broken.length > lineWidth - hangIndent) {
              var part = broken.substring(0, lineWidth - hangIndent);
              if (breakMode === 'hyphen') {
                part = part.substring(0, part.length - 1) + '-';
              }
              lines.push(newPrefix + part);
              broken = broken.substring(breakMode === 'hyphen' ? part.length - 1 : part.length);
              newPrefix = '';
              for (var j4 = 0; j4 < hangIndent; j4++) newPrefix += ' ';
            }
            currentLine = newPrefix + broken;
            currentWidth = broken.length;
          }
        } else {
          currentLine = newPrefix + word;
          currentWidth = word.length;
        }
      } else {
        currentLine += ' ' + word;
        currentWidth += 1 + word.length;
      }
    }
  }
  if (currentLine) lines.push(currentLine);
  
  var result = lines.join('\\n');
  resultText.value = result;
  document.getElementById('lineCount').textContent = lines.length;
  document.getElementById('resultCharCount').textContent = result.length;
  resultSection.style.display = 'block';
  showToast('换行完成，共' + lines.length + '行');
}''')

# 6. text-rewriter: rewrite()
fix_tool(f'{BASE}/text-rewriter/index.html', 'rewrite', '''function rewrite() {
  var input = document.getElementById('input') || document.getElementById('inputText') || document.querySelector('textarea');
  var output = document.getElementById('output') || document.getElementById('result') || document.getElementById('outputText');
  if (!input || !input.value.trim()) { showToast('请输入文本'); return; }
  var text = input.value;
  var mode = 'synonym';
  var modeSelect = document.getElementById('mode') || document.getElementById('rewriteMode');
  if (modeSelect) mode = modeSelect.value;
  var modeEl = document.querySelector('.mode-tab.active, .mode-card.active');
  if (modeEl && modeEl.getAttribute('data-mode')) mode = modeEl.getAttribute('data-mode');
  
  var result = text;
  if (mode === 'uppercase' || mode === 'upper') {
    result = text.toUpperCase();
  } else if (mode === 'lowercase' || mode === 'lower') {
    result = text.toLowerCase();
  } else if (mode === 'capitalize' || mode === 'title') {
    result = text.replace(/\\b\\w/g, function(c) { return c.toUpperCase(); });
  } else if (mode === 'reverse') {
    result = text.split('').reverse().join('');
  } else {
    var synonyms = {
      'good': 'excellent', 'bad': 'poor', 'big': 'large', 'small': 'tiny',
      'fast': 'quick', 'slow': 'sluggish', 'happy': 'delighted', 'sad': 'sorrowful',
      'important': 'crucial', 'interesting': 'fascinating', 'difficult': 'challenging',
      'easy': 'simple', 'beautiful': 'gorgeous', 'ugly': 'unattractive'
    };
    result = text.replace(/\\b(\\w+)\\b/gi, function(word) {
      var lower = word.toLowerCase();
      if (synonyms[lower]) {
        if (word[0] === word[0].toUpperCase()) {
          return synonyms[lower].charAt(0).toUpperCase() + synonyms[lower].slice(1);
        }
        return synonyms[lower];
      }
      return word;
    });
  }
  if (output) {
    output.value = result;
    output.textContent = result;
  }
  showToast('改写完成');
}''')

# 7. text-similarity: compare()
fix_tool(f'{BASE}/text-similarity/index.html', 'compare', '''function compare() {
  var input1 = document.getElementById('text1') || document.getElementById('input1') || document.getElementById('source');
  var input2 = document.getElementById('text2') || document.getElementById('input2') || document.getElementById('target');
  var result = document.getElementById('result') || document.getElementById('output') || document.getElementById('resultArea');
  if (!input1 || !input2) { showToast('输入框未找到'); return; }
  var t1 = input1.value || input1.textContent;
  var t2 = input2.value || input2.textContent;
  if (!t1.trim() || !t2.trim()) { showToast('请输入两段文本'); return; }
  
  var matrix = [];
  for (var i = 0; i <= t1.length; i++) {
    matrix[i] = [i];
  }
  for (var j = 0; j <= t2.length; j++) {
    matrix[0][j] = j;
  }
  for (var i = 1; i <= t1.length; i++) {
    for (var j = 1; j <= t2.length; j++) {
      if (t1[i-1] === t2[j-1]) {
        matrix[i][j] = matrix[i-1][j-1];
      } else {
        matrix[i][j] = Math.min(matrix[i-1][j-1] + 1, matrix[i][j-1] + 1, matrix[i-1][j] + 1);
      }
    }
  }
  var distance = matrix[t1.length][t2.length];
  var maxLength = Math.max(t1.length, t2.length);
  var similarity = maxLength === 0 ? 100 : Math.round((1 - distance / maxLength) * 100);
  
  var words1 = new Set(t1.toLowerCase().split(/\\s+/));
  var words2 = new Set(t2.toLowerCase().split(/\\s+/));
  var intersection = 0;
  words1.forEach(function(w) { if (words2.has(w)) intersection++; });
  var union = words1.size + words2.size - intersection;
  var jaccardSim = union === 0 ? 0 : Math.round((intersection / union) * 100);
  
  var html = '<div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:16px">';
  html += '<div style="background:#0f172a;padding:16px;border-radius:8px;text-align:center">';
  html += '<div style="color:#94a3b8;font-size:.85rem;margin-bottom:4px">字符相似度</div>';
  html += '<div style="font-size:2rem;font-weight:700;color:' + (similarity >= 80 ? '#4ade80' : similarity >= 50 ? '#fbbf24' : '#f87171') + '">' + similarity + '%</div>';
  html += '</div>';
  html += '<div style="background:#0f172a;padding:16px;border-radius:8px;text-align:center">';
  html += '<div style="color:#94a3b8;font-size:.85rem;margin-bottom:4px">词汇相似度</div>';
  html += '<div style="font-size:2rem;font-weight:700;color:' + (jaccardSim >= 80 ? '#4ade80' : jaccardSim >= 50 ? '#fbbf24' : '#f87171') + '">' + jaccardSim + '%</div>';
  html += '</div></div>';
  html += '<div style="color:#94a3b8;font-size:.85rem">编辑距离: ' + distance + ' | 文本1长度: ' + t1.length + ' | 文本2长度: ' + t2.length + '</div>';
  
  if (result) {
    result.innerHTML = html;
    result.style.display = 'block';
  }
  showToast('比较完成');
}''')

# 8. json-lint: autoValidate()
fix_tool(f'{BASE}/json-lint/index.html', 'autoValidate', '''function autoValidate() {
  var input = document.getElementById('jsonInput') || document.getElementById('input') || document.querySelector('textarea');
  var output = document.getElementById('result') || document.getElementById('output') || document.getElementById('jsonOutput');
  if (!input || !input.value.trim()) { showToast('请输入JSON'); return; }
  var text = input.value.trim();
  try {
    var parsed = JSON.parse(text);
    var formatted = JSON.stringify(parsed, null, 2);
    if (output) {
      output.value = formatted;
      output.textContent = formatted;
    }
    showToast('JSON有效');
  } catch(e) {
    var msg = e.message;
    var posMatch = msg.match(/position (\\d+)/i);
    var posInfo = '';
    if (posMatch) {
      var pos = parseInt(posMatch[1]);
      var lines = text.substring(0, pos).split('\\n');
      posInfo = ' (行' + lines.length + ', 列' + (lines[lines.length-1].length+1) + ')';
    }
    if (output) {
      var d = document.createElement('div');
      d.style.color = '#f87171';
      d.textContent = 'JSON解析错误: ' + msg + posInfo;
      output.innerHTML = '';
      output.appendChild(d);
    }
    showToast('JSON无效: ' + msg);
  }
}''')

# 9. yaml-validator: yamlToJSON()
fix_tool(f'{BASE}/yaml-validator/index.html', 'yamlToJSON', '''function yamlToJSON() {
  var input = document.getElementById('yamlInput') || document.getElementById('input') || document.querySelector('textarea');
  var output = document.getElementById('result') || document.getElementById('output') || document.getElementById('jsonOutput');
  if (!input || !input.value.trim()) { showToast('请输入YAML'); return; }
  var yaml = input.value.trim();
  try {
    var result = parseYAML(yaml);
    var json = JSON.stringify(result, null, 2);
    if (output) {
      output.value = json;
      output.textContent = json;
    }
    showToast('YAML有效');
  } catch(e) {
    if (output) {
      var d = document.createElement('div');
      d.style.color = '#f87171';
      d.textContent = 'YAML解析错误: ' + e.message;
      output.innerHTML = '';
      output.appendChild(d);
    }
    showToast('YAML无效: ' + e.message);
  }
}
function parseYAML(text) {
  var result = {};
  var lines = text.split('\\n');
  var stack = [{indent: -1, obj: result}];
  
  for (var i = 0; i < lines.length; i++) {
    var line = lines[i];
    var trimmed = line.replace(/#.*$/, '').replace(/\\s+$/, '');
    if (!trimmed) continue;
    var indent = line.length - line.replace(/^\\s*/, '').length;
    var content = trimmed.trim();
    
    while (stack.length > 1 && stack[stack.length-1].indent >= indent) {
      stack.pop();
    }
    var parent = stack[stack.length-1];
    
    if (content.startsWith('- ')) {
      var itemValue = content.substring(2).trim();
      if (!parent.obj[parent._currentKey]) {
        parent.obj[parent._currentKey] = [];
      }
      if (itemValue.includes(':')) {
        var kv = itemValue.split(':', 2);
        var obj = {};
        obj[kv[0].trim()] = parseYAMLValue(kv[1].trim());
        parent.obj[parent._currentKey].push(obj);
      } else {
        parent.obj[parent._currentKey].push(parseYAMLValue(itemValue));
      }
    } else if (content.includes(':')) {
      var idx = content.indexOf(':');
      var key = content.substring(0, idx).trim();
      var val = content.substring(idx + 1).trim();
      if (val === '') {
        parent.obj[key] = {};
        parent._currentKey = key;
        stack.push({indent: indent, obj: parent.obj[key]});
      } else {
        parent.obj[key] = parseYAMLValue(val);
        parent._currentKey = key;
      }
    }
  }
  return result;
}
function parseYAMLValue(val) {
  if (val === 'true') return true;
  if (val === 'false') return false;
  if (val === 'null' || val === '~') return null;
  if (/^-?\\d+$/.test(val)) return parseInt(val);
  if (/^-?\\d+\\.\\d+$/.test(val)) return parseFloat(val);
  if ((val.startsWith('"') && val.endsWith('"')) || (val.startsWith("'") && val.endsWith("'"))) {
    return val.substring(1, val.length - 1);
  }
  if (val.startsWith('[') && val.endsWith(']')) {
    return val.substring(1, val.length-1).split(',').map(function(s) { return parseYAMLValue(s.trim()); });
  }
  return val;
}''')

# 10. binary-to-hex: autoConvert()
fix_tool(f'{BASE}/binary-to-hex/index.html', 'autoConvert', '''function autoConvert() {
  var input = document.getElementById('binaryInput') || document.getElementById('input') || document.querySelector('textarea');
  var hexOutput = document.getElementById('hexOutput') || document.getElementById('hex');
  var decOutput = document.getElementById('decOutput') || document.getElementById('decimal');
  var octOutput = document.getElementById('octOutput') || document.getElementById('octal');
  if (!input) return;
  var bin = input.value.trim().replace(/\\s+/g, '');
  if (!bin) { 
    if (hexOutput) hexOutput.textContent = '';
    if (decOutput) decOutput.textContent = '';
    if (octOutput) octOutput.textContent = '';
    return; 
  }
  if (!/^[01]+$/.test(bin)) {
    if (hexOutput) {
      var d = document.createElement('span');
      d.style.color = '#f87171';
      d.textContent = '无效的二进制';
      hexOutput.innerHTML = '';
      hexOutput.appendChild(d);
    }
    return;
  }
  var padded = bin;
  while (padded.length % 4 !== 0) padded = '0' + padded;
  var hex = '';
  for (var i = 0; i < padded.length; i += 4) {
    hex += parseInt(padded.substr(i, 4), 2).toString(16).toUpperCase();
  }
  var dec = '';
  try {
    if (typeof BigInt !== 'undefined') {
      dec = BigInt('0b' + bin).toString();
    } else {
      dec = parseInt(bin, 2).toString();
    }
  } catch(e) {
    dec = parseInt(bin, 2).toString();
  }
  var oct = '';
  try {
    if (typeof BigInt !== 'undefined') {
      oct = BigInt('0b' + bin).toString(8);
    } else {
      oct = parseInt(bin, 2).toString(8);
    }
  } catch(e) {
    oct = parseInt(bin, 2).toString(8);
  }
  if (hexOutput) hexOutput.textContent = hex;
  if (decOutput) decOutput.textContent = dec;
  if (octOutput) octOutput.textContent = oct;
}''')

print("\nAll 10 tools patched. Verifying...")
