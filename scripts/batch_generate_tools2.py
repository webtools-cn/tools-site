#!/usr/bin/env python3
"""批量生成新工具页面（中英文双语）- 第二批"""
import os

BASE_DIR = "/home/chison/tools-site"

STYLE = """:root {
  --primary: #4F46E5;
  --primary-light: #EEF2FF;
  --bg: #f8fafc;
  --card-bg: #ffffff;
  --text: #1e293b;
  --text-secondary: #64748b;
  --border: #e2e8f0;
  --radius: 12px;
  --shadow: 0 1px 3px rgba(0,0,0,0.08);
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  background: var(--bg);
  color: var(--text);
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}
header {
  background: var(--card-bg);
  border-bottom: 1px solid var(--border);
  padding: 16px 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: sticky;
  top: 0;
  z-index: 10;
}
header a {
  text-decoration: none;
  color: var(--primary);
  font-weight: 700;
  font-size: 18px;
}
.lang-switch {
  display: flex;
  gap: 8px;
}
.lang-switch a {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 13px;
  color: var(--text-secondary);
  background: var(--bg);
  border: 1px solid var(--border);
}
.lang-switch a.active {
  background: var(--primary);
  color: #fff;
  border-color: var(--primary);
}
main {
  flex: 1;
  max-width: 800px;
  margin: 32px auto;
  padding: 0 16px;
}
.tool-header {
  text-align: center;
  margin-bottom: 32px;
}
.tool-header h1 {
  font-size: 28px;
  margin-bottom: 8px;
}
.tool-header p {
  color: var(--text-secondary);
  font-size: 15px;
}
.card {
  background: var(--card-bg);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  padding: 24px;
  margin-bottom: 20px;
}
.card h2 {
  font-size: 18px;
  margin-bottom: 16px;
  color: var(--primary);
}
.input-group {
  margin-bottom: 16px;
}
.input-group label {
  display: block;
  font-size: 13px;
  font-weight: 600;
  color: var(--text-secondary);
  margin-bottom: 6px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}
textarea, input[type="text"], input[type="url"], input[type="number"], select {
  width: 100%;
  padding: 10px 14px;
  border: 2px solid var(--border);
  border-radius: 8px;
  font-size: 14px;
  font-family: inherit;
  transition: border-color 0.2s;
  background: #fff;
}
textarea:focus, input:focus, select:focus {
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 3px var(--primary-light);
}
textarea { min-height: 120px; resize: vertical; }
.btn-row {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}
.btn {
  padding: 10px 20px;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 6px;
}
.btn-primary {
  background: var(--primary);
  color: #fff;
}
.btn-primary:hover { opacity: 0.9; transform: translateY(-1px); }
.btn-secondary {
  background: var(--bg);
  color: var(--text);
  border: 1px solid var(--border);
}
.btn-secondary:hover { background: var(--border); }
.result-box {
  margin-top: 16px;
  padding: 16px;
  background: #f1f5f9;
  border-radius: 8px;
  font-size: 14px;
  word-break: break-all;
  min-height: 48px;
}
.preview-box {
  margin-top: 16px;
  border: 2px dashed var(--border);
  border-radius: 8px;
  min-height: 120px;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: auto;
}
.range-group {
  display: flex;
  align-items: center;
  gap: 12px;
}
.range-group input[type="range"] {
  flex: 1;
}
.range-group .range-val {
  min-width: 40px;
  text-align: center;
  font-weight: 700;
  color: var(--primary);
}
.color-preview {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  border: 2px solid var(--border);
}
.toast {
  position: fixed;
  bottom: 24px;
  left: 50%;
  transform: translateX(-50%);
  background: #1e293b;
  color: #fff;
  padding: 10px 24px;
  border-radius: 8px;
  font-size: 14px;
  z-index: 999;
  opacity: 0;
  transition: opacity 0.3s;
  pointer-events: none;
}
.toast.show { opacity: 1; }
footer {
  text-align: center;
  padding: 24px;
  color: var(--text-secondary);
  font-size: 13px;
  border-top: 1px solid var(--border);
  margin-top: 40px;
}
@media (max-width: 600px) {
  main { margin: 16px auto; }
  .tool-header h1 { font-size: 22px; }
}
"""

TOOLS = [
    {
        "slug": "hsl-color-picker",
        "cn_name": "HSL颜色选择器",
        "en_name": "HSL Color Picker",
        "cn_desc": "在线HSL颜色选择器，可视化调节色相/饱和度/亮度，实时预览并一键复制CSS色值。纯前端工具。",
        "en_desc": "Online HSL color picker. Visual adjustment of hue/saturation/lightness with real-time preview and CSS copy. Client-side tool.",
        "category": "design-tools",
        "cn_html": """
        <div class="card">
          <h2>🎨 HSL 颜色调节</h2>
          <div class="input-group">
            <label>色相 Hue (0-360)</label>
            <div class="range-group">
              <input type="range" id="hueRange" min="0" max="360" value="240">
              <span class="range-val" id="hueVal">240</span>
            </div>
          </div>
          <div class="input-group">
            <label>饱和度 Saturation (0-100%)</label>
            <div class="range-group">
              <input type="range" id="satRange" min="0" max="100" value="70">
              <span class="range-val" id="satVal">70%</span>
            </div>
          </div>
          <div class="input-group">
            <label>亮度 Lightness (0-100%)</label>
            <div class="range-group">
              <input type="range" id="lightRange" min="0" max="100" value="50">
              <span class="range-val" id="lightVal">50%</span>
            </div>
          </div>
          <div style="display:flex;align-items:center;gap:16px;margin-top:16px">
            <div class="color-preview" id="colorPreview" style="width:80px;height:80px;border-radius:12px;"></div>
            <div>
              <div class="result-box" id="hslValue" style="font-size:18px;font-weight:700">hsl(240, 70%, 50%)</div>
              <div class="result-box" id="hexValue" style="font-size:16px;margin-top:4px">#2b2bd4</div>
            </div>
          </div>
          <div class="btn-row" style="margin-top:16px">
            <button class="btn btn-primary" id="copyHslBtn">📋 复制 HSL</button>
            <button class="btn btn-secondary" id="copyHexBtn">📋 复制 HEX</button>
          </div>
        </div>
        <script>
        const hueRange = document.getElementById('hueRange');
        const satRange = document.getElementById('satRange');
        const lightRange = document.getElementById('lightRange');
        const hueVal = document.getElementById('hueVal');
        const satVal = document.getElementById('satVal');
        const lightVal = document.getElementById('lightVal');
        const colorPreview = document.getElementById('colorPreview');
        const hslValue = document.getElementById('hslValue');
        const hexValue = document.getElementById('hexValue');
        function hslToHex(h, s, l) {
          s /= 100; l /= 100;
          const a = s * Math.min(l, 1 - l);
          const f = n => { const k = (n + h/30) % 12; const c = l - a * Math.max(Math.min(k-3,9-k,1),-1); return Math.round(c*255).toString(16).padStart(2,'0'); };
          return '#' + f(0) + f(8) + f(4);
        }
        function update() {
          const h = parseInt(hueRange.value);
          const s = parseInt(satRange.value);
          const l = parseInt(lightRange.value);
          hueVal.textContent = h;
          satVal.textContent = s + '%';
          lightVal.textContent = l + '%';
          const hsl = 'hsl(' + h + ', ' + s + '%, ' + l + '%)';
          const hex = hslToHex(h, s, l);
          colorPreview.style.background = hsl;
          hslValue.textContent = hsl;
          hexValue.textContent = hex;
        }
        [hueRange, satRange, lightRange].forEach(r => r.addEventListener('input', update));
        document.getElementById('copyHslBtn').addEventListener('click', function() {
          navigator.clipboard.writeText(hslValue.textContent);
          showToast('HSL已复制！');
        });
        document.getElementById('copyHexBtn').addEventListener('click', function() {
          navigator.clipboard.writeText(hexValue.textContent);
          showToast('HEX已复制！');
        });
        update();
        </script>
        """,
        "en_html": """
        <div class="card">
          <h2>🎨 HSL Color Adjustment</h2>
          <div class="input-group">
            <label>Hue (0-360)</label>
            <div class="range-group">
              <input type="range" id="hueRange" min="0" max="360" value="240">
              <span class="range-val" id="hueVal">240</span>
            </div>
          </div>
          <div class="input-group">
            <label>Saturation (0-100%)</label>
            <div class="range-group">
              <input type="range" id="satRange" min="0" max="100" value="70">
              <span class="range-val" id="satVal">70%</span>
            </div>
          </div>
          <div class="input-group">
            <label>Lightness (0-100%)</label>
            <div class="range-group">
              <input type="range" id="lightRange" min="0" max="100" value="50">
              <span class="range-val" id="lightVal">50%</span>
            </div>
          </div>
          <div style="display:flex;align-items:center;gap:16px;margin-top:16px">
            <div class="color-preview" id="colorPreview" style="width:80px;height:80px;border-radius:12px;"></div>
            <div>
              <div class="result-box" id="hslValue" style="font-size:18px;font-weight:700">hsl(240, 70%, 50%)</div>
              <div class="result-box" id="hexValue" style="font-size:16px;margin-top:4px">#2b2bd4</div>
            </div>
          </div>
          <div class="btn-row" style="margin-top:16px">
            <button class="btn btn-primary" id="copyHslBtn">📋 Copy HSL</button>
            <button class="btn btn-secondary" id="copyHexBtn">📋 Copy HEX</button>
          </div>
        </div>
        <script>
        const hueRange = document.getElementById('hueRange');
        const satRange = document.getElementById('satRange');
        const lightRange = document.getElementById('lightRange');
        const hueVal = document.getElementById('hueVal');
        const satVal = document.getElementById('satVal');
        const lightVal = document.getElementById('lightVal');
        const colorPreview = document.getElementById('colorPreview');
        const hslValue = document.getElementById('hslValue');
        const hexValue = document.getElementById('hexValue');
        function hslToHex(h, s, l) {
          s /= 100; l /= 100;
          const a = s * Math.min(l, 1 - l);
          const f = n => { const k = (n + h/30) % 12; const c = l - a * Math.max(Math.min(k-3,9-k,1),-1); return Math.round(c*255).toString(16).padStart(2,'0'); };
          return '#' + f(0) + f(8) + f(4);
        }
        function update() {
          const h = parseInt(hueRange.value);
          const s = parseInt(satRange.value);
          const l = parseInt(lightRange.value);
          hueVal.textContent = h;
          satVal.textContent = s + '%';
          lightVal.textContent = l + '%';
          const hsl = 'hsl(' + h + ', ' + s + '%, ' + l + '%)';
          const hex = hslToHex(h, s, l);
          colorPreview.style.background = hsl;
          hslValue.textContent = hsl;
          hexValue.textContent = hex;
        }
        [hueRange, satRange, lightRange].forEach(r => r.addEventListener('input', update));
        document.getElementById('copyHslBtn').addEventListener('click', function() {
          navigator.clipboard.writeText(hslValue.textContent);
          showToast('HSL copied!');
        });
        document.getElementById('copyHexBtn').addEventListener('click', function() {
          navigator.clipboard.writeText(hexValue.textContent);
          showToast('HEX copied!');
        });
        update();
        </script>
        """
    },
    {
        "slug": "xml-viewer",
        "cn_name": "XML在线查看器",
        "en_name": "XML Online Viewer",
        "cn_desc": "在线XML格式化查看工具，支持粘贴XML代码自动美化高亮、树形结构展示。纯前端处理，代码安全。",
        "en_desc": "Online XML viewer and formatter. Paste XML for auto-beautify with syntax highlighting and tree view. Client-side, code stays safe.",
        "category": "dev-tools",
        "cn_html": """
        <div class="card">
          <h2>📝 XML代码</h2>
          <div class="input-group">
            <label>粘贴XML代码</label>
            <textarea id="xmlInput" placeholder="在此粘贴XML代码...">&lt;?xml version="1.0"?&gt;
&lt;catalog&gt;
  &lt;book id="1"&gt;
    &lt;title&gt;The Great Gatsby&lt;/title&gt;
    &lt;author&gt;F. Scott Fitzgerald&lt;/author&gt;
    &lt;year&gt;1925&lt;/year&gt;
  &lt;/book&gt;
  &lt;book id="2"&gt;
    &lt;title&gt;1984&lt;/title&gt;
    &lt;author&gt;George Orwell&lt;/author&gt;
    &lt;year&gt;1949&lt;/year&gt;
  &lt;/book&gt;
&lt;/catalog&gt;</textarea>
          </div>
          <div class="btn-row">
            <button class="btn btn-primary" id="formatBtn">✨ 格式化</button>
            <button class="btn btn-secondary" id="minifyBtn">🗜️ 压缩</button>
            <button class="btn btn-secondary" id="clearBtn">🗑️ 清空</button>
          </div>
        </div>
        <div class="card">
          <h2>👁️ 预览</h2>
          <div class="result-box" id="xmlOutput" style="font-family:monospace;font-size:13px;white-space:pre-wrap;max-height:500px;overflow:auto;line-height:1.6">
          </div>
          <div class="btn-row" style="margin-top:12px">
            <button class="btn btn-secondary" id="copyBtn">📋 复制结果</button>
            <button class="btn btn-secondary" id="downloadBtn">⬇️ 下载XML</button>
          </div>
        </div>
        <script>
        const xmlInput = document.getElementById('xmlInput');
        const xmlOutput = document.getElementById('xmlOutput');
        function formatXml(xml) {
          let formatted = '';
          let indent = '';
          xml.split(/>\s*</).forEach(function(node) {
            if (node.match(/^\/\w/)) indent = indent.substring(2);
            formatted += indent + '<' + node + '>\\n';
            if (node.match(/^<?\w[^>]*[^/]$/) && !node.startsWith('?')) indent += '  ';
          });
          return formatted.substring(0, formatted.length-1);
        }
        function highlightXml(xml) {
          return xml
            .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
            .replace(/(&lt;\/?)([\\w.-]+)/g, '$1<span style="color:#d63384">$2</span>')
            .replace(/(\\w+)=(".*?")/g, '<span style="color:#0d6efd">$1</span>=<span style="color:#198754">$2</span>');
        }
        document.getElementById('formatBtn').addEventListener('click', function() {
          try {
            const xml = xmlInput.value.trim();
            const formatted = formatXml(xml);
            xmlOutput.innerHTML = highlightXml(formatted);
          } catch(e) {
            xmlOutput.innerHTML = '<span style="color:#e74c3c">格式化失败: ' + e.message + '</span>';
          }
        });
        document.getElementById('minifyBtn').addEventListener('click', function() {
          const minified = xmlInput.value.replace(/>\\s+</g, '><').replace(/\\s+/g, ' ').trim();
          xmlOutput.textContent = minified;
        });
        document.getElementById('clearBtn').addEventListener('click', function() {
          xmlInput.value = '';
          xmlOutput.innerHTML = '';
        });
        document.getElementById('copyBtn').addEventListener('click', function() {
          const text = xmlOutput.textContent;
          if (!text) { showToast('无内容可复制'); return; }
          navigator.clipboard.writeText(text);
          showToast('已复制！');
        });
        document.getElementById('downloadBtn').addEventListener('click', function() {
          const xml = xmlInput.value.trim();
          if (!xml) { showToast('无内容可下载'); return; }
          const blob = new Blob([xml], {type:'application/xml'});
          const a = document.createElement('a');
          a.href = URL.createObjectURL(blob);
          a.download = 'output.xml';
          a.click();
          showToast('下载开始！');
        });
        // Auto format on load
        document.getElementById('formatBtn').click();
        </script>
        """,
        "en_html": """
        <div class="card">
          <h2>📝 XML Code</h2>
          <div class="input-group">
            <label>Paste XML code</label>
            <textarea id="xmlInput" placeholder="Paste XML code here...">&lt;?xml version="1.0"?&gt;
&lt;catalog&gt;
  &lt;book id="1"&gt;
    &lt;title&gt;The Great Gatsby&lt;/title&gt;
    &lt;author&gt;F. Scott Fitzgerald&lt;/author&gt;
    &lt;year&gt;1925&lt;/year&gt;
  &lt;/book&gt;
  &lt;book id="2"&gt;
    &lt;title&gt;1984&lt;/title&gt;
    &lt;author&gt;George Orwell&lt;/author&gt;
    &lt;year&gt;1949&lt;/year&gt;
  &lt;/book&gt;
&lt;/catalog&gt;</textarea>
          </div>
          <div class="btn-row">
            <button class="btn btn-primary" id="formatBtn">✨ Format</button>
            <button class="btn btn-secondary" id="minifyBtn">🗜️ Minify</button>
            <button class="btn btn-secondary" id="clearBtn">🗑️ Clear</button>
          </div>
        </div>
        <div class="card">
          <h2>👁️ Preview</h2>
          <div class="result-box" id="xmlOutput" style="font-family:monospace;font-size:13px;white-space:pre-wrap;max-height:500px;overflow:auto;line-height:1.6">
          </div>
          <div class="btn-row" style="margin-top:12px">
            <button class="btn btn-secondary" id="copyBtn">📋 Copy Result</button>
            <button class="btn btn-secondary" id="downloadBtn">⬇️ Download XML</button>
          </div>
        </div>
        <script>
        const xmlInput = document.getElementById('xmlInput');
        const xmlOutput = document.getElementById('xmlOutput');
        function formatXml(xml) {
          let formatted = '';
          let indent = '';
          xml.split(/>\s*</).forEach(function(node) {
            if (node.match(/^\/\w/)) indent = indent.substring(2);
            formatted += indent + '<' + node + '>\\n';
            if (node.match(/^<?\w[^>]*[^/]$/) && !node.startsWith('?')) indent += '  ';
          });
          return formatted.substring(0, formatted.length-1);
        }
        function highlightXml(xml) {
          return xml
            .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
            .replace(/(&lt;\/?)([\\w.-]+)/g, '$1<span style="color:#d63384">$2</span>')
            .replace(/(\\w+)=(".*?")/g, '<span style="color:#0d6efd">$1</span>=<span style="color:#198754">$2</span>');
        }
        document.getElementById('formatBtn').addEventListener('click', function() {
          try {
            const xml = xmlInput.value.trim();
            const formatted = formatXml(xml);
            xmlOutput.innerHTML = highlightXml(formatted);
          } catch(e) {
            xmlOutput.innerHTML = '<span style="color:#e74c3c">Format failed: ' + e.message + '</span>';
          }
        });
        document.getElementById('minifyBtn').addEventListener('click', function() {
          const minified = xmlInput.value.replace(/>\\s+</g, '><').replace(/\\s+/g, ' ').trim();
          xmlOutput.textContent = minified;
        });
        document.getElementById('clearBtn').addEventListener('click', function() {
          xmlInput.value = '';
          xmlOutput.innerHTML = '';
        });
        document.getElementById('copyBtn').addEventListener('click', function() {
          const text = xmlOutput.textContent;
          if (!text) { showToast('Nothing to copy'); return; }
          navigator.clipboard.writeText(text);
          showToast('Copied!');
        });
        document.getElementById('downloadBtn').addEventListener('click', function() {
          const xml = xmlInput.value.trim();
          if (!xml) { showToast('Nothing to download'); return; }
          const blob = new Blob([xml], {type:'application/xml'});
          const a = document.createElement('a');
          a.href = URL.createObjectURL(blob);
          a.download = 'output.xml';
          a.click();
          showToast('Download started!');
        });
        document.getElementById('formatBtn').click();
        </script>
        """
    },
    {
        "slug": "text-deduplicator",
        "cn_name": "文本去重工具",
        "en_name": "Text Deduplicator",
        "cn_desc": "在线文本去重工具，按行去重或整体去重，支持保留/移除重复项，一键复制结果。纯前端处理，数据安全。",
        "en_desc": "Online text deduplicator. Remove duplicate lines or whole-text duplicates. Keep or remove duplicates with one-click copy. Client-side, data safe.",
        "category": "text-tools",
        "cn_html": """
        <div class="card">
          <h2>📝 输入文本</h2>
          <div class="input-group">
            <label>粘贴文本（每行一条）</label>
            <textarea id="textInput" placeholder="在此粘贴文本...
每行一条数据
重复的行将被移除">苹果
香蕉
苹果
橘子
香蕉
葡萄
苹果</textarea>
          </div>
          <div class="input-group">
            <label>去重模式</label>
            <select id="modeSelect">
              <option value="unique">保留唯一值（移除重复）</option>
              <option value="duplicates">保留重复值（出现>1次的）</option>
              <option value="count">统计出现次数</option>
            </select>
          </div>
          <div class="btn-row">
            <button class="btn btn-primary" id="dedupBtn">🔍 去重</button>
            <button class="btn btn-secondary" id="clearBtn">🗑️ 清空</button>
            <button class="btn btn-secondary" id="copyBtn">📋 复制结果</button>
          </div>
        </div>
        <div class="card">
          <h2>📊 结果</h2>
          <div class="result-box" id="statsBox" style="margin-bottom:12px">
            原始: 7行 | 去重后: 4行 | 重复: 3行
          </div>
          <textarea id="outputText" readonly style="min-height:150px;background:#f8fafc"></textarea>
        </div>
        <script>
        const textInput = document.getElementById('textInput');
        const modeSelect = document.getElementById('modeSelect');
        const statsBox = document.getElementById('statsBox');
        const outputText = document.getElementById('outputText');
        document.getElementById('dedupBtn').addEventListener('click', function() {
          const lines = textInput.value.split('\\n').filter(l => l.trim());
          const total = lines.length;
          const mode = modeSelect.value;
          let result = [];
          if (mode === 'unique') {
            result = [...new Set(lines)];
            statsBox.textContent = '原始: ' + total + '行 | 去重后: ' + result.length + '行 | 移除: ' + (total - result.length) + '行';
          } else if (mode === 'duplicates') {
            const count = {};
            lines.forEach(l => count[l] = (count[l]||0)+1);
            result = Object.entries(count).filter(([k,v]) => v > 1).map(([k]) => k);
            statsBox.textContent = '原始: ' + total + '行 | 重复项: ' + result.length + '个';
          } else {
            const count = {};
            lines.forEach(l => count[l] = (count[l]||0)+1);
            result = Object.entries(count).sort((a,b) => b[1]-a[1]).map(([k,v]) => k + ' (' + v + '次)');
            statsBox.textContent = '原始: ' + total + '行 | 唯一项: ' + Object.keys(count).length + '个';
          }
          outputText.value = result.join('\\n');
        });
        document.getElementById('clearBtn').addEventListener('click', function() {
          textInput.value = '';
          outputText.value = '';
          statsBox.textContent = '已清空';
        });
        document.getElementById('copyBtn').addEventListener('click', function() {
          if (!outputText.value) { showToast('无结果可复制'); return; }
          navigator.clipboard.writeText(outputText.value);
          showToast('结果已复制！');
        });
        document.getElementById('dedupBtn').click();
        </script>
        """,
        "en_html": """
        <div class="card">
          <h2>📝 Input Text</h2>
          <div class="input-group">
            <label>Paste text (one item per line)</label>
            <textarea id="textInput" placeholder="Paste text here...
One item per line
Duplicates will be handled">Apple
Banana
Apple
Orange
Banana
Grape
Apple</textarea>
          </div>
          <div class="input-group">
            <label>Dedup Mode</label>
            <select id="modeSelect">
              <option value="unique">Keep Unique (remove duplicates)</option>
              <option value="duplicates">Keep Duplicates (appear >1 time)</option>
              <option value="count">Count Occurrences</option>
            </select>
          </div>
          <div class="btn-row">
            <button class="btn btn-primary" id="dedupBtn">🔍 Deduplicate</button>
            <button class="btn btn-secondary" id="clearBtn">🗑️ Clear</button>
            <button class="btn btn-secondary" id="copyBtn">📋 Copy Result</button>
          </div>
        </div>
        <div class="card">
          <h2>📊 Result</h2>
          <div class="result-box" id="statsBox" style="margin-bottom:12px">
            Original: 7 lines | Unique: 4 | Removed: 3
          </div>
          <textarea id="outputText" readonly style="min-height:150px;background:#f8fafc"></textarea>
        </div>
        <script>
        const textInput = document.getElementById('textInput');
        const modeSelect = document.getElementById('modeSelect');
        const statsBox = document.getElementById('statsBox');
        const outputText = document.getElementById('outputText');
        document.getElementById('dedupBtn').addEventListener('click', function() {
          const lines = textInput.value.split('\\n').filter(l => l.trim());
          const total = lines.length;
          const mode = modeSelect.value;
          let result = [];
          if (mode === 'unique') {
            result = [...new Set(lines)];
            statsBox.textContent = 'Original: ' + total + ' lines | Unique: ' + result.length + ' | Removed: ' + (total - result.length);
          } else if (mode === 'duplicates') {
            const count = {};
            lines.forEach(l => count[l] = (count[l]||0)+1);
            result = Object.entries(count).filter(([k,v]) => v > 1).map(([k]) => k);
            statsBox.textContent = 'Original: ' + total + ' lines | Duplicates: ' + result.length;
          } else {
            const count = {};
            lines.forEach(l => count[l] = (count[l]||0)+1);
            result = Object.entries(count).sort((a,b) => b[1]-a[1]).map(([k,v]) => k + ' (' + v + ' times)');
            statsBox.textContent = 'Original: ' + total + ' lines | Unique items: ' + Object.keys(count).length;
          }
          outputText.value = result.join('\\n');
        });
        document.getElementById('clearBtn').addEventListener('click', function() {
          textInput.value = '';
          outputText.value = '';
          statsBox.textContent = 'Cleared';
        });
        document.getElementById('copyBtn').addEventListener('click', function() {
          if (!outputText.value) { showToast('No result to copy'); return; }
          navigator.clipboard.writeText(outputText.value);
          showToast('Result copied!');
        });
        document.getElementById('dedupBtn').click();
        </script>
        """
    },
    {
        "slug": "decision-wheel",
        "cn_name": "决策转盘",
        "en_name": "Decision Wheel",
        "cn_desc": "在线决策转盘工具，自定义选项列表，旋转转盘随机选择。帮你快速做决定，告别选择困难。",
        "en_desc": "Online decision wheel tool. Customize option list, spin the wheel for random selection. Helps you make quick decisions.",
        "category": "fun-tools",
        "cn_html": """
        <div class="card">
          <h2>📝 选项列表</h2>
          <div class="input-group">
            <label>输入选项（每行一个）</label>
            <textarea id="optionInput" placeholder="披萨
寿司
汉堡
沙拉
面条
饺子
咖喱饭">披萨
寿司
汉堡
沙拉
面条
饺子
咖喱饭</textarea>
          </div>
          <div class="btn-row">
            <button class="btn btn-primary" id="spinBtn">🎰 开始旋转</button>
            <button class="btn btn-secondary" id="updateBtn">🔄 更新选项</button>
          </div>
        </div>
        <div class="card" style="text-align:center">
          <h2>🎯 转盘</h2>
          <canvas id="wheelCanvas" width="400" height="400" style="max-width:100%"></canvas>
          <div class="result-box" id="wheelResult" style="font-size:20px;font-weight:700;margin-top:12px">
            🎉 结果: --
          </div>
        </div>
        <script>
        const canvas = document.getElementById('wheelCanvas');
        const ctx = canvas.getContext('2d');
        const optionInput = document.getElementById('optionInput');
        const wheelResult = document.getElementById('wheelResult');
        let options = [];
        let spinning = false;
        let currentAngle = 0;
        const COLORS = ['#FF6384','#36A2EB','#FFCE56','#4BC0C0','#9966FF','#FF9F40','#C9CBCF','#7BC8A4','#E8C3B9','#B8A9C9'];
        function drawWheel() {
          options = optionInput.value.split('\\n').filter(l => l.trim());
          if (options.length < 2) { ctx.clearRect(0,0,400,400); ctx.fillText('至少2个选项', 150, 200); return; }
          const sliceAngle = (2 * Math.PI) / options.length;
          ctx.clearRect(0, 0, 400, 400);
          for (let i = 0; i < options.length; i++) {
            const startAngle = currentAngle + i * sliceAngle;
            const endAngle = startAngle + sliceAngle;
            ctx.beginPath();
            ctx.moveTo(200, 200);
            ctx.arc(200, 200, 190, startAngle, endAngle);
            ctx.fillStyle = COLORS[i % COLORS.length];
            ctx.fill();
            ctx.strokeStyle = '#fff';
            ctx.lineWidth = 2;
            ctx.stroke();
            ctx.save();
            ctx.translate(200, 200);
            ctx.rotate(startAngle + sliceAngle / 2);
            ctx.fillStyle = '#fff';
            ctx.font = 'bold 13px sans-serif';
            ctx.textAlign = 'right';
            ctx.fillText(options[i].substring(0, 15), 170, 5);
            ctx.restore();
          }
          // Center circle
          ctx.beginPath();
          ctx.arc(200, 200, 25, 0, 2*Math.PI);
          ctx.fillStyle = '#fff';
          ctx.fill();
          ctx.fillStyle = '#333';
          ctx.font = 'bold 14px sans-serif';
          ctx.textAlign = 'center';
          ctx.fillText('GO', 200, 206);
        }
        document.getElementById('updateBtn').addEventListener('click', function() {
          currentAngle = 0;
          drawWheel();
          wheelResult.textContent = '🎉 结果: --';
        });
        document.getElementById('spinBtn').addEventListener('click', function() {
          options = optionInput.value.split('\\n').filter(l => l.trim());
          if (options.length < 2) { showToast('至少需要2个选项！'); return; }
          if (spinning) return;
          spinning = true;
          const spinBtn = document.getElementById('spinBtn');
          spinBtn.disabled = true;
          const spins = 5 + Math.random() * 5;
          const targetAngle = currentAngle + spins * 2 * Math.PI + Math.random() * 2 * Math.PI;
          const duration = 3000;
          const startTime = Date.now();
          const startAngle = currentAngle;
          function animate() {
            const elapsed = Date.now() - startTime;
            const progress = Math.min(elapsed / duration, 1);
            const eased = 1 - Math.pow(1 - progress, 3);
            currentAngle = startAngle + (targetAngle - startAngle) * eased;
            drawWheel();
            if (progress < 1) {
              requestAnimationFrame(animate);
            } else {
              const sliceAngle = (2 * Math.PI) / options.length;
              const normalizedAngle = (currentAngle % (2 * Math.PI) + 2 * Math.PI) % (2 * Math.PI);
              const winnerIndex = Math.floor(((2 * Math.PI - normalizedAngle + sliceAngle/2) % (2 * Math.PI)) / sliceAngle);
              const winner = options[winnerIndex % options.length];
              wheelResult.textContent = '🎉 结果: ' + winner;
              spinning = false;
              spinBtn.disabled = false;
            }
          }
          requestAnimationFrame(animate);
        });
        drawWheel();
        </script>
        """,
        "en_html": """
        <div class="card">
          <h2>📝 Options</h2>
          <div class="input-group">
            <label>Enter options (one per line)</label>
            <textarea id="optionInput" placeholder="Pizza
Sushi
Burger
Salad
Noodles
Dumplings
Curry Rice">Pizza
Sushi
Burger
Salad
Noodles
Dumplings
Curry Rice</textarea>
          </div>
          <div class="btn-row">
            <button class="btn btn-primary" id="spinBtn">🎰 Spin!</button>
            <button class="btn btn-secondary" id="updateBtn">🔄 Update Options</button>
          </div>
        </div>
        <div class="card" style="text-align:center">
          <h2>🎯 Wheel</h2>
          <canvas id="wheelCanvas" width="400" height="400" style="max-width:100%"></canvas>
          <div class="result-box" id="wheelResult" style="font-size:20px;font-weight:700;margin-top:12px">
            🎉 Result: --
          </div>
        </div>
        <script>
        const canvas = document.getElementById('wheelCanvas');
        const ctx = canvas.getContext('2d');
        const optionInput = document.getElementById('optionInput');
        const wheelResult = document.getElementById('wheelResult');
        let options = [];
        let spinning = false;
        let currentAngle = 0;
        const COLORS = ['#FF6384','#36A2EB','#FFCE56','#4BC0C0','#9966FF','#FF9F40','#C9CBCF','#7BC8A4','#E8C3B9','#B8A9C9'];
        function drawWheel() {
          options = optionInput.value.split('\\n').filter(l => l.trim());
          if (options.length < 2) { ctx.clearRect(0,0,400,400); ctx.fillText('Need at least 2 options', 130, 200); return; }
          const sliceAngle = (2 * Math.PI) / options.length;
          ctx.clearRect(0, 0, 400, 400);
          for (let i = 0; i < options.length; i++) {
            const startAngle = currentAngle + i * sliceAngle;
            const endAngle = startAngle + sliceAngle;
            ctx.beginPath();
            ctx.moveTo(200, 200);
            ctx.arc(200, 200, 190, startAngle, endAngle);
            ctx.fillStyle = COLORS[i % COLORS.length];
            ctx.fill();
            ctx.strokeStyle = '#fff';
            ctx.lineWidth = 2;
            ctx.stroke();
            ctx.save();
            ctx.translate(200, 200);
            ctx.rotate(startAngle + sliceAngle / 2);
            ctx.fillStyle = '#fff';
            ctx.font = 'bold 13px sans-serif';
            ctx.textAlign = 'right';
            ctx.fillText(options[i].substring(0, 15), 170, 5);
            ctx.restore();
          }
          ctx.beginPath();
          ctx.arc(200, 200, 25, 0, 2*Math.PI);
          ctx.fillStyle = '#fff';
          ctx.fill();
          ctx.fillStyle = '#333';
          ctx.font = 'bold 14px sans-serif';
          ctx.textAlign = 'center';
          ctx.fillText('GO', 200, 206);
        }
        document.getElementById('updateBtn').addEventListener('click', function() {
          currentAngle = 0;
          drawWheel();
          wheelResult.textContent = '🎉 Result: --';
        });
        document.getElementById('spinBtn').addEventListener('click', function() {
          options = optionInput.value.split('\\n').filter(l => l.trim());
          if (options.length < 2) { showToast('Need at least 2 options!'); return; }
          if (spinning) return;
          spinning = true;
          const spinBtn = document.getElementById('spinBtn');
          spinBtn.disabled = true;
          const spins = 5 + Math.random() * 5;
          const targetAngle = currentAngle + spins * 2 * Math.PI + Math.random() * 2 * Math.PI;
          const duration = 3000;
          const startTime = Date.now();
          const startAngle = currentAngle;
          function animate() {
            const elapsed = Date.now() - startTime;
            const progress = Math.min(elapsed / duration, 1);
            const eased = 1 - Math.pow(1 - progress, 3);
            currentAngle = startAngle + (targetAngle - startAngle) * eased;
            drawWheel();
            if (progress < 1) {
              requestAnimationFrame(animate);
            } else {
              const sliceAngle = (2 * Math.PI) / options.length;
              const normalizedAngle = (currentAngle % (2 * Math.PI) + 2 * Math.PI) % (2 * Math.PI);
              const winnerIndex = Math.floor(((2 * Math.PI - normalizedAngle + sliceAngle/2) % (2 * Math.PI)) / sliceAngle);
              const winner = options[winnerIndex % options.length];
              wheelResult.textContent = '🎉 Result: ' + winner;
              spinning = false;
              spinBtn.disabled = false;
            }
          }
          requestAnimationFrame(animate);
        });
        drawWheel();
        </script>
        """
    },
    {
        "slug": "dice-roll-simulator",
        "cn_name": "骰子模拟器",
        "en_name": "Dice Roll Simulator",
        "cn_desc": "在线骰子模拟器，支持多面骰(D4/D6/D8/D10/D12/D20/D100)和多骰同掷，含历史记录。",
        "en_desc": "Online dice roll simulator. Support multi-sided dice (D4/D6/D8/D10/D12/D20/D100) and multiple dice at once with history.",
        "category": "fun-tools",
        "cn_html": """
        <div class="card">
          <h2>🎲 骰子设置</h2>
          <div class="input-group">
            <label>骰子类型</label>
            <select id="diceType">
              <option value="4">D4 (四面骰)</option>
              <option value="6" selected>D6 (六面骰)</option>
              <option value="8">D8 (八面骰)</option>
              <option value="10">D10 (十面骰)</option>
              <option value="12">D12 (十二面骰)</option>
              <option value="20">D20 (二十面骰)</option>
              <option value="100">D100 (百分骰)</option>
            </select>
          </div>
          <div class="input-group">
            <label>骰子数量</label>
            <input type="number" id="diceCount" min="1" max="20" value="1">
          </div>
          <div class="btn-row">
            <button class="btn btn-primary" id="rollBtn">🎲 掷骰子!</button>
            <button class="btn btn-secondary" id="clearHistoryBtn">🗑️ 清除历史</button>
          </div>
        </div>
        <div class="card">
          <h2>📊 结果</h2>
          <div class="result-box" id="rollResult" style="font-size:28px;font-weight:700;text-align:center;min-height:60px;display:flex;align-items:center;justify-content:center">
            点击掷骰子!
          </div>
          <div class="result-box" id="rollDetails" style="margin-top:8px;font-size:14px;color:var(--text-secondary)">
            单次结果详情
          </div>
        </div>
        <div class="card">
          <h2>📜 历史记录</h2>
          <div id="history" style="max-height:200px;overflow-y:auto;font-size:13px">
          </div>
        </div>
        <script>
        const diceType = document.getElementById('diceType');
        const diceCount = document.getElementById('diceCount');
        const rollResult = document.getElementById('rollResult');
        const rollDetails = document.getElementById('rollDetails');
        const history = document.getElementById('history');
        let historyData = [];
        document.getElementById('rollBtn').addEventListener('click', function() {
          const sides = parseInt(diceType.value);
          const count = parseInt(diceCount.value);
          const results = [];
          for (let i = 0; i < count; i++) {
            results.push(Math.floor(Math.random() * sides) + 1);
          }
          const total = results.reduce((a,b) => a+b, 0);
          rollResult.innerHTML = '🎯 <span style="font-size:36px">' + total + '</span>';
          if (count === 1) {
            rollDetails.textContent = 'D' + sides + ' = ' + results[0];
          } else {
            rollDetails.textContent = count + '×D' + sides + ' = [' + results.join(', ') + '] 总和=' + total;
          }
          // Add to history
          const entry = { time: new Date().toLocaleTimeString(), sides, count, results, total };
          historyData.unshift(entry);
          if (historyData.length > 50) historyData.pop();
          renderHistory();
          // Animate
          rollResult.style.transform = 'scale(1.2)';
          setTimeout(() => rollResult.style.transform = 'scale(1)', 150);
        });
        function renderHistory() {
          history.innerHTML = historyData.map((h,i) => 
            '<div style="padding:4px 0;border-bottom:1px solid var(--border)">' +
            '<span style="color:var(--text-secondary)">' + h.time + '</span> ' +
            h.count + '×D' + h.sides + ' = <strong>' + h.total + '</strong>' +
            (h.count > 1 ? ' [' + h.results.join(',') + ']' : '') +
            '</div>'
          ).join('');
        }
        document.getElementById('clearHistoryBtn').addEventListener('click', function() {
          historyData = [];
          history.innerHTML = '';
        });
        </script>
        """,
        "en_html": """
        <div class="card">
          <h2>🎲 Dice Settings</h2>
          <div class="input-group">
            <label>Dice Type</label>
            <select id="diceType">
              <option value="4">D4 (4-sided)</option>
              <option value="6" selected>D6 (6-sided)</option>
              <option value="8">D8 (8-sided)</option>
              <option value="10">D10 (10-sided)</option>
              <option value="12">D12 (12-sided)</option>
              <option value="20">D20 (20-sided)</option>
              <option value="100">D100 (Percentile)</option>
            </select>
          </div>
          <div class="input-group">
            <label>Number of Dice</label>
            <input type="number" id="diceCount" min="1" max="20" value="1">
          </div>
          <div class="btn-row">
            <button class="btn btn-primary" id="rollBtn">🎲 Roll!</button>
            <button class="btn btn-secondary" id="clearHistoryBtn">🗑️ Clear History</button>
          </div>
        </div>
        <div class="card">
          <h2>📊 Result</h2>
          <div class="result-box" id="rollResult" style="font-size:28px;font-weight:700;text-align:center;min-height:60px;display:flex;align-items:center;justify-content:center">
            Click to roll!
          </div>
          <div class="result-box" id="rollDetails" style="margin-top:8px;font-size:14px;color:var(--text-secondary)">
            Details
          </div>
        </div>
        <div class="card">
          <h2>📜 History</h2>
          <div id="history" style="max-height:200px;overflow-y:auto;font-size:13px">
          </div>
        </div>
        <script>
        const diceType = document.getElementById('diceType');
        const diceCount = document.getElementById('diceCount');
        const rollResult = document.getElementById('rollResult');
        const rollDetails = document.getElementById('rollDetails');
        const history = document.getElementById('history');
        let historyData = [];
        document.getElementById('rollBtn').addEventListener('click', function() {
          const sides = parseInt(diceType.value);
          const count = parseInt(diceCount.value);
          const results = [];
          for (let i = 0; i < count; i++) {
            results.push(Math.floor(Math.random() * sides) + 1);
          }
          const total = results.reduce((a,b) => a+b, 0);
          rollResult.innerHTML = '🎯 <span style="font-size:36px">' + total + '</span>';
          if (count === 1) {
            rollDetails.textContent = 'D' + sides + ' = ' + results[0];
          } else {
            rollDetails.textContent = count + '×D' + sides + ' = [' + results.join(', ') + '] Sum=' + total;
          }
          const entry = { time: new Date().toLocaleTimeString(), sides, count, results, total };
          historyData.unshift(entry);
          if (historyData.length > 50) historyData.pop();
          renderHistory();
          rollResult.style.transform = 'scale(1.2)';
          setTimeout(() => rollResult.style.transform = 'scale(1)', 150);
        });
        function renderHistory() {
          history.innerHTML = historyData.map((h,i) => 
            '<div style="padding:4px 0;border-bottom:1px solid var(--border)">' +
            '<span style="color:var(--text-secondary)">' + h.time + '</span> ' +
            h.count + '×D' + h.sides + ' = <strong>' + h.total + '</strong>' +
            (h.count > 1 ? ' [' + h.results.join(',') + ']' : '') +
            '</div>'
          ).join('');
        }
        document.getElementById('clearHistoryBtn').addEventListener('click', function() {
          historyData = [];
          history.innerHTML = '';
        });
        </script>
        """
    },
    {
        "slug": "clipboard-formatter",
        "cn_name": "剪贴板格式化工具",
        "en_name": "Clipboard Formatter",
        "cn_desc": "在线剪贴板格式化工具，一键粘贴文本并自动去除多余空格、格式化大小写、清理特殊字符。纯前端处理。",
        "en_desc": "Online clipboard formatter. One-click paste and auto-clean: trim spaces, format case, remove special characters. Client-side processing.",
        "category": "text-tools",
        "cn_html": """
        <div class="card">
          <h2>📋 输入文本</h2>
          <div class="input-group">
            <label>粘贴文本（或点击下方按钮自动读取剪贴板）</label>
            <textarea id="textInput" placeholder="在此粘贴文本..."></textarea>
          </div>
          <div class="btn-row">
            <button class="btn btn-primary" id="pasteBtn">📋 读取剪贴板</button>
            <button class="btn btn-secondary" id="clearBtn">🗑️ 清空</button>
          </div>
        </div>
        <div class="card">
          <h2>⚙️ 格式化选项</h2>
          <div class="input-group">
            <label>去除多余空格</label>
            <label style="display:flex;align-items:center;gap:8px;font-weight:400;text-transform:none">
              <input type="checkbox" id="trimSpaces" checked> 将连续空格合并为单个空格
            </label>
          </div>
          <div class="input-group">
            <label>去除空行</label>
            <label style="display:flex;align-items:center;gap:8px;font-weight:400;text-transform:none">
              <input type="checkbox" id="removeEmptyLines" checked> 移除空白行
            </label>
          </div>
          <div class="input-group">
            <label>去除首尾空格</label>
            <label style="display:flex;align-items:center;gap:8px;font-weight:400;text-transform:none">
              <input type="checkbox" id="trimEdges" checked> 去除每行首尾空白
            </label>
          </div>
          <div class="btn-row" style="margin-top:16px">
            <button class="btn btn-primary" id="formatBtn">✨ 格式化</button>
            <button class="btn btn-secondary" id="copyBtn">📋 复制结果</button>
          </div>
        </div>
        <div class="card">
          <h2>📊 结果</h2>
          <textarea id="outputText" readonly style="min-height:150px;background:#f8fafc"></textarea>
          <div class="result-box" id="statsBox" style="margin-top:8px;font-size:13px">
            等待格式化...
          </div>
        </div>
        <script>
        const textInput = document.getElementById('textInput');
        const outputText = document.getElementById('outputText');
        const statsBox = document.getElementById('statsBox');
        document.getElementById('pasteBtn').addEventListener('click', async function() {
          try {
            const text = await navigator.clipboard.readText();
            textInput.value = text;
            showToast('已读取剪贴板内容！');
          } catch(e) {
            showToast('无法读取剪贴板，请手动粘贴');
          }
        });
        document.getElementById('clearBtn').addEventListener('click', function() {
          textInput.value = '';
          outputText.value = '';
          statsBox.textContent = '已清空';
        });
        document.getElementById('formatBtn').addEventListener('click', function() {
          let text = textInput.value;
          if (!text) { showToast('请先输入文本'); return; }
          const origLen = text.length;
          const origLines = text.split('\\n').length;
          if (document.getElementById('trimEdges').checked) {
            text = text.split('\\n').map(l => l.trim()).join('\\n');
          }
          if (document.getElementById('trimSpaces').checked) {
            text = text.replace(/[ \\t]+/g, ' ');
          }
          if (document.getElementById('removeEmptyLines').checked) {
            text = text.split('\\n').filter(l => l.trim()).join('\\n');
          }
          text = text.trim();
          outputText.value = text;
          const newLines = text.split('\\n').length;
          statsBox.textContent = '原始: ' + origLen + '字符/' + origLines + '行 → 格式化后: ' + text.length + '字符/' + newLines + '行';
        });
        document.getElementById('copyBtn').addEventListener('click', function() {
          if (!outputText.value) { showToast('无结果可复制'); return; }
          navigator.clipboard.writeText(outputText.value);
          showToast('结果已复制到剪贴板！');
        });
        </script>
        """,
        "en_html": """
        <div class="card">
          <h2>📋 Input Text</h2>
          <div class="input-group">
            <label>Paste text (or click button to read clipboard)</label>
            <textarea id="textInput" placeholder="Paste text here..."></textarea>
          </div>
          <div class="btn-row">
            <button class="btn btn-primary" id="pasteBtn">📋 Read Clipboard</button>
            <button class="btn btn-secondary" id="clearBtn">🗑️ Clear</button>
          </div>
        </div>
        <div class="card">
          <h2>⚙️ Format Options</h2>
          <div class="input-group">
            <label>Collapse Spaces</label>
            <label style="display:flex;align-items:center;gap:8px;font-weight:400;text-transform:none">
              <input type="checkbox" id="trimSpaces" checked> Merge consecutive spaces into one
            </label>
          </div>
          <div class="input-group">
            <label>Remove Empty Lines</label>
            <label style="display:flex;align-items:center;gap:8px;font-weight:400;text-transform:none">
              <input type="checkbox" id="removeEmptyLines" checked> Strip blank lines
            </label>
          </div>
          <div class="input-group">
            <label>Trim Line Edges</label>
            <label style="display:flex;align-items:center;gap:8px;font-weight:400;text-transform:none">
              <input type="checkbox" id="trimEdges" checked> Remove leading/trailing whitespace per line
            </label>
          </div>
          <div class="btn-row" style="margin-top:16px">
            <button class="btn btn-primary" id="formatBtn">✨ Format</button>
            <button class="btn btn-secondary" id="copyBtn">📋 Copy Result</button>
          </div>
        </div>
        <div class="card">
          <h2>📊 Result</h2>
          <textarea id="outputText" readonly style="min-height:150px;background:#f8fafc"></textarea>
          <div class="result-box" id="statsBox" style="margin-top:8px;font-size:13px">
            Waiting to format...
          </div>
        </div>
        <script>
        const textInput = document.getElementById('textInput');
        const outputText = document.getElementById('outputText');
        const statsBox = document.getElementById('statsBox');
        document.getElementById('pasteBtn').addEventListener('click', async function() {
          try {
            const text = await navigator.clipboard.readText();
            textInput.value = text;
            showToast('Clipboard content read!');
          } catch(e) {
            showToast('Cannot read clipboard, please paste manually');
          }
        });
        document.getElementById('clearBtn').addEventListener('click', function() {
          textInput.value = '';
          outputText.value = '';
          statsBox.textContent = 'Cleared';
        });
        document.getElementById('formatBtn').addEventListener('click', function() {
          let text = textInput.value;
          if (!text) { showToast('Please enter text first'); return; }
          const origLen = text.length;
          const origLines = text.split('\\n').length;
          if (document.getElementById('trimEdges').checked) {
            text = text.split('\\n').map(l => l.trim()).join('\\n');
          }
          if (document.getElementById('trimSpaces').checked) {
            text = text.replace(/[ \\t]+/g, ' ');
          }
          if (document.getElementById('removeEmptyLines').checked) {
            text = text.split('\\n').filter(l => l.trim()).join('\\n');
          }
          text = text.trim();
          outputText.value = text;
          const newLines = text.split('\\n').length;
          statsBox.textContent = 'Original: ' + origLen + ' chars/' + origLines + ' lines → Formatted: ' + text.length + ' chars/' + newLines + ' lines';
        });
        document.getElementById('copyBtn').addEventListener('click', function() {
          if (!outputText.value) { showToast('No result to copy'); return; }
          navigator.clipboard.writeText(outputText.value);
          showToast('Result copied to clipboard!');
        });
        </script>
        """
    },
]

def make_page(slug, cn_name, en_name, cn_desc, en_desc, category, cn_html, en_html, lang="cn"):
    is_cn = lang == "cn"
    title = cn_name if is_cn else en_name
    desc = cn_desc if is_cn else en_desc
    lang_tag = "zh-CN" if is_cn else "en"
    canonical = f"https://free-toolbase.com/{slug}/" if is_cn else f"https://free-toolbase.com/en/{slug}/"
    alt_href = f"/en/{slug}/" if is_cn else f"/{slug}/"
    alt_lang = "en" if is_cn else "zh-CN"
    active_cn = "active" if is_cn else ""
    active_en = "active" if not is_cn else ""
    body_html = cn_html if is_cn else en_html

    return f"""<!DOCTYPE html>
<html lang="{lang_tag}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} - Free ToolBase</title>
  <meta name="description" content="{desc}">
  <meta property="og:title" content="{title} - Free ToolBase">
  <meta property="og:description" content="{desc}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{canonical}">
  <link rel="canonical" href="{canonical}">
  <link rel="alternate" hreflang="{alt_lang}" href="https://free-toolbase.com{alt_href}">
  <link rel="alternate" hreflang="{lang_tag}" href="{canonical}">
  <link rel="alternate" hreflang="x-default" href="https://free-toolbase.com/{slug}/">
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "SoftwareApplication",
    "name": "{title}",
    "description": "{desc}",
    "applicationCategory": "DeveloperApplication",
    "operatingSystem": "Any",
    "url": "{canonical}",
    "offers": {{"@type": "Offer", "price": "0"}}
  }}
  </script>
  <style>
{STYLE}
  </style>
</head>
<body>
  <header>
    <a href="{'/' if is_cn else '/en/'}">🧰 Free ToolBase</a>
    <div class="lang-switch">
      <a href="/{slug}/" class="{active_cn}">中文</a>
      <a href="/en/{slug}/" class="{active_en}">English</a>
    </div>
  </header>
  <main>
    <div class="tool-header">
      <h1>{title}</h1>
      <p>{desc}</p>
    </div>
{body_html}
  </main>
  <footer>
    <p>&copy; 2026 Free ToolBase · {'纯前端处理，数据不上传服务器' if is_cn else 'Client-side processing · No data uploads'}</p>
  </footer>
  <div class="toast" id="toast"></div>
  <script>
  function showToast(msg) {{
    const t = document.getElementById('toast');
    t.textContent = msg;
    t.classList.add('show');
    setTimeout(function() {{ t.classList.remove('show'); }}, 2000);
  }}
  </script>
</body>
</html>"""

for tool in TOOLS:
    slug = tool["slug"]
    cn_dir = os.path.join(BASE_DIR, slug)
    en_dir = os.path.join(BASE_DIR, "en", slug)
    os.makedirs(cn_dir, exist_ok=True)
    os.makedirs(en_dir, exist_ok=True)

    cn_page = make_page(slug, tool["cn_name"], tool["en_name"], tool["cn_desc"], tool["en_desc"],
                        tool["category"], tool["cn_html"], tool["en_html"], "cn")
    en_page = make_page(slug, tool["cn_name"], tool["en_name"], tool["cn_desc"], tool["en_desc"],
                        tool["category"], tool["cn_html"], tool["en_html"], "en")

    with open(os.path.join(cn_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(cn_page)
    with open(os.path.join(en_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(en_page)
    print(f"✅ {slug} (中英文)")

print(f"\n共生成 {len(TOOLS)} 个工具")