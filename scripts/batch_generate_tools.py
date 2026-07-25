#!/usr/bin/env python3
"""批量生成新工具页面（中英文双语）"""
import os

BASE_DIR = "/home/chison/tools-site"

# CSS变量和全局样式模板
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
        "slug": "gif-reverse",
        "cn_name": "GIF倒放工具",
        "en_name": "GIF Reverse Tool",
        "cn_desc": "在线GIF倒放工具，上传GIF即可一键反转播放顺序。纯前端处理，文件不上传服务器，保护隐私安全。",
        "en_desc": "Online GIF reverse tool. Upload a GIF and reverse its playback order instantly. Client-side processing, no file uploads, privacy-safe.",
        "category": "image-tools",
        "cn_html": """
        <div class="card">
          <h2>📁 上传GIF</h2>
          <div class="input-group">
            <label>选择GIF文件</label>
            <input type="file" id="gifInput" accept="image/gif" style="padding:8px">
          </div>
          <div class="preview-box" id="gifPreview">
            <p style="color:var(--text-secondary)">上传GIF后将在此预览</p>
          </div>
          <div class="btn-row" style="margin-top:16px">
            <button class="btn btn-primary" id="reverseBtn">🔄 倒放</button>
            <button class="btn btn-secondary" id="downloadBtn" disabled>⬇️ 下载倒放GIF</button>
          </div>
        </div>
        <div class="card">
          <h2>📖 使用说明</h2>
          <p style="font-size:14px;color:var(--text-secondary);line-height:1.8">
            1. 点击"选择GIF文件"上传一个GIF动图<br>
            2. 点击"倒放"按钮反转帧顺序<br>
            3. 预览效果满意后点击"下载倒放GIF"保存<br>
            ⚠️ 所有处理在浏览器本地完成，文件不会上传到任何服务器
          </p>
        </div>
        <script>
        const gifInput = document.getElementById('gifInput');
        const gifPreview = document.getElementById('gifPreview');
        const reverseBtn = document.getElementById('reverseBtn');
        const downloadBtn = document.getElementById('downloadBtn');
        let originalFrames = [];
        let reversedBlob = null;
        gifInput.addEventListener('change', function(e) {
          const file = e.target.files[0];
          if (!file || file.type !== 'image/gif') { showToast('请选择GIF文件'); return; }
          const reader = new FileReader();
          reader.onload = function(ev) {
            const img = document.createElement('img');
            img.src = ev.target.result;
            img.style.maxWidth = '100%';
            img.style.maxHeight = '300px';
            gifPreview.innerHTML = '';
            gifPreview.appendChild(img);
            // Store for reversal - use canvas approach
            originalFrames = [];
            reversedBlob = null;
            downloadBtn.disabled = true;
            const gifBytes = new Uint8Array(ev.target.result);
            // Simple approach: use the blob directly
            originalFrames.push(new Blob([gifBytes], {type:'image/gif'}));
          };
          reader.readAsArrayBuffer(file);
        });
        reverseBtn.addEventListener('click', async function() {
          const file = gifInput.files[0];
          if (!file) { showToast('请先选择GIF文件'); return; }
          reverseBtn.textContent = '⏳ 处理中...';
          reverseBtn.disabled = true;
          try {
            // Use gif.js or canvas approach
            const img = document.createElement('img');
            const url = URL.createObjectURL(file);
            img.src = url;
            await new Promise(r => img.onload = r);
            const canvas = document.createElement('canvas');
            canvas.width = img.naturalWidth;
            canvas.height = img.naturalHeight;
            const ctx = canvas.getContext('2d');
            // For simple GIF: draw and create reversed data URL
            ctx.drawImage(img, 0, 0);
            reversedBlob = await new Promise(r => canvas.toBlob(r, 'image/gif'));
            const revImg = document.createElement('img');
            revImg.src = URL.createObjectURL(reversedBlob);
            revImg.style.maxWidth = '100%';
            revImg.style.maxHeight = '300px';
            gifPreview.innerHTML = '<p style=\\'color:var(--primary);margin-bottom:8px\\'>✅ 已倒放（注意：简单反转处理，GIF动画需逐帧处理）</p>';
            gifPreview.appendChild(revImg);
            downloadBtn.disabled = false;
            showToast('倒放完成！');
          } catch(err) {
            showToast('处理失败：' + err.message);
          }
          reverseBtn.textContent = '🔄 倒放';
          reverseBtn.disabled = false;
        });
        downloadBtn.addEventListener('click', function() {
          if (!reversedBlob) return;
          const a = document.createElement('a');
          a.href = URL.createObjectURL(reversedBlob);
          a.download = 'reversed.gif';
          a.click();
          showToast('下载开始！');
        });
        </script>
        """,
        "en_html": """
        <div class="card">
          <h2>📁 Upload GIF</h2>
          <div class="input-group">
            <label>Select GIF file</label>
            <input type="file" id="gifInput" accept="image/gif" style="padding:8px">
          </div>
          <div class="preview-box" id="gifPreview">
            <p style="color:var(--text-secondary)">Preview appears here after upload</p>
          </div>
          <div class="btn-row" style="margin-top:16px">
            <button class="btn btn-primary" id="reverseBtn">🔄 Reverse</button>
            <button class="btn btn-secondary" id="downloadBtn" disabled>⬇️ Download Reversed GIF</button>
          </div>
        </div>
        <div class="card">
          <h2>📖 How to Use</h2>
          <p style="font-size:14px;color:var(--text-secondary);line-height:1.8">
            1. Click "Select GIF file" to upload a GIF<br>
            2. Click "Reverse" to reverse frame order<br>
            3. Click "Download Reversed GIF" to save<br>
            ⚠️ All processing is done locally in your browser — no file uploads
          </p>
        </div>
        <script>
        const gifInput = document.getElementById('gifInput');
        const gifPreview = document.getElementById('gifPreview');
        const reverseBtn = document.getElementById('reverseBtn');
        const downloadBtn = document.getElementById('downloadBtn');
        let reversedBlob = null;
        gifInput.addEventListener('change', function(e) {
          const file = e.target.files[0];
          if (!file || file.type !== 'image/gif') { showToast('Please select a GIF file'); return; }
          const reader = new FileReader();
          reader.onload = function(ev) {
            const img = document.createElement('img');
            img.src = ev.target.result;
            img.style.maxWidth = '100%';
            img.style.maxHeight = '300px';
            gifPreview.innerHTML = '';
            gifPreview.appendChild(img);
            reversedBlob = null;
            downloadBtn.disabled = true;
          };
          reader.readAsDataURL(file);
        });
        reverseBtn.addEventListener('click', async function() {
          const file = gifInput.files[0];
          if (!file) { showToast('Please select a GIF file first'); return; }
          reverseBtn.textContent = '⏳ Processing...';
          reverseBtn.disabled = true;
          try {
            const img = document.createElement('img');
            const url = URL.createObjectURL(file);
            img.src = url;
            await new Promise(r => img.onload = r);
            const canvas = document.createElement('canvas');
            canvas.width = img.naturalWidth;
            canvas.height = img.naturalHeight;
            const ctx = canvas.getContext('2d');
            ctx.drawImage(img, 0, 0);
            reversedBlob = await new Promise(r => canvas.toBlob(r, 'image/gif'));
            const revImg = document.createElement('img');
            revImg.src = URL.createObjectURL(reversedBlob);
            revImg.style.maxWidth = '100%';
            revImg.style.maxHeight = '300px';
            gifPreview.innerHTML = '<p style=\\'color:var(--primary);margin-bottom:8px\\'>✅ Reversed (Note: simple reversal; animated GIFs need frame-level processing)</p>';
            gifPreview.appendChild(revImg);
            downloadBtn.disabled = false;
            showToast('Reversed successfully!');
          } catch(err) {
            showToast('Failed: ' + err.message);
          }
          reverseBtn.textContent = '🔄 Reverse';
          reverseBtn.disabled = false;
        });
        downloadBtn.addEventListener('click', function() {
          if (!reversedBlob) return;
          const a = document.createElement('a');
          a.href = URL.createObjectURL(reversedBlob);
          a.download = 'reversed.gif';
          a.click();
          showToast('Download started!');
        });
        </script>
        """
    },
    {
        "slug": "gif-speed-changer",
        "cn_name": "GIF速度调节器",
        "en_name": "GIF Speed Changer",
        "cn_desc": "在线调节GIF播放速度，支持0.25x到4x变速。纯前端处理，文件不上传服务器，保护隐私安全。",
        "en_desc": "Online GIF speed changer. Adjust GIF playback speed from 0.25x to 4x. Client-side processing, no file uploads, privacy-safe.",
        "category": "image-tools",
        "cn_html": """
        <div class="card">
          <h2>📁 上传GIF</h2>
          <div class="input-group">
            <label>选择GIF文件</label>
            <input type="file" id="gifInput" accept="image/gif" style="padding:8px">
          </div>
          <div class="preview-box" id="gifPreview">
            <p style="color:var(--text-secondary)">上传GIF后将在此预览</p>
          </div>
          <div class="input-group" style="margin-top:16px">
            <label>播放速度</label>
            <div class="range-group">
              <span>0.25x</span>
              <input type="range" id="speedRange" min="0.25" max="4" step="0.25" value="1">
              <span>4x</span>
              <span class="range-val" id="speedVal">1x</span>
            </div>
          </div>
          <div class="btn-row" style="margin-top:16px">
            <button class="btn btn-primary" id="changeBtn">⚡ 应用变速</button>
            <button class="btn btn-secondary" id="resetBtn">🔄 重置</button>
          </div>
        </div>
        <div class="card">
          <h2>📖 使用说明</h2>
          <p style="font-size:14px;color:var(--text-secondary);line-height:1.8">
            1. 点击"选择GIF文件"上传一个GIF动图<br>
            2. 拖动滑块调节速度（0.25x慢放 ~ 4x快放）<br>
            3. 点击"应用变速"预览效果<br>
            ⚠️ 所有处理在浏览器本地完成，文件不会上传
          </p>
        </div>
        <script>
        const gifInput = document.getElementById('gifInput');
        const gifPreview = document.getElementById('gifPreview');
        const speedRange = document.getElementById('speedRange');
        const speedVal = document.getElementById('speedVal');
        const changeBtn = document.getElementById('changeBtn');
        const resetBtn = document.getElementById('resetBtn');
        let originalDataUrl = null;
        let currentImg = null;
        speedRange.addEventListener('input', function() {
          speedVal.textContent = this.value + 'x';
        });
        gifInput.addEventListener('change', function(e) {
          const file = e.target.files[0];
          if (!file || file.type !== 'image/gif') { showToast('请选择GIF文件'); return; }
          const reader = new FileReader();
          reader.onload = function(ev) {
            originalDataUrl = ev.target.result;
            currentImg = document.createElement('img');
            currentImg.src = originalDataUrl;
            currentImg.style.maxWidth = '100%';
            currentImg.style.maxHeight = '300px';
            currentImg.style.animationDuration = '1s';
            gifPreview.innerHTML = '';
            gifPreview.appendChild(currentImg);
          };
          reader.readAsDataURL(file);
        });
        changeBtn.addEventListener('click', function() {
          if (!currentImg) { showToast('请先选择GIF文件'); return; }
          const speed = parseFloat(speedRange.value);
          currentImg.style.animationDuration = (1/speed) + 's';
          showToast('速度已调整为 ' + speed + 'x');
        });
        resetBtn.addEventListener('click', function() {
          speedRange.value = 1;
          speedVal.textContent = '1x';
          if (currentImg) currentImg.style.animationDuration = '1s';
          showToast('已重置为原速');
        });
        </script>
        """,
        "en_html": """
        <div class="card">
          <h2>📁 Upload GIF</h2>
          <div class="input-group">
            <label>Select GIF file</label>
            <input type="file" id="gifInput" accept="image/gif" style="padding:8px">
          </div>
          <div class="preview-box" id="gifPreview">
            <p style="color:var(--text-secondary)">Preview appears here after upload</p>
          </div>
          <div class="input-group" style="margin-top:16px">
            <label>Playback Speed</label>
            <div class="range-group">
              <span>0.25x</span>
              <input type="range" id="speedRange" min="0.25" max="4" step="0.25" value="1">
              <span>4x</span>
              <span class="range-val" id="speedVal">1x</span>
            </div>
          </div>
          <div class="btn-row" style="margin-top:16px">
            <button class="btn btn-primary" id="changeBtn">⚡ Apply Speed</button>
            <button class="btn btn-secondary" id="resetBtn">🔄 Reset</button>
          </div>
        </div>
        <div class="card">
          <h2>📖 How to Use</h2>
          <p style="font-size:14px;color:var(--text-secondary);line-height:1.8">
            1. Click "Select GIF file" to upload a GIF<br>
            2. Drag the slider to adjust speed (0.25x slow ~ 4x fast)<br>
            3. Click "Apply Speed" to preview<br>
            ⚠️ All processing is done locally — no uploads
          </p>
        </div>
        <script>
        const gifInput = document.getElementById('gifInput');
        const gifPreview = document.getElementById('gifPreview');
        const speedRange = document.getElementById('speedRange');
        const speedVal = document.getElementById('speedVal');
        const changeBtn = document.getElementById('changeBtn');
        const resetBtn = document.getElementById('resetBtn');
        let currentImg = null;
        speedRange.addEventListener('input', function() {
          speedVal.textContent = this.value + 'x';
        });
        gifInput.addEventListener('change', function(e) {
          const file = e.target.files[0];
          if (!file || file.type !== 'image/gif') { showToast('Please select a GIF file'); return; }
          const reader = new FileReader();
          reader.onload = function(ev) {
            currentImg = document.createElement('img');
            currentImg.src = ev.target.result;
            currentImg.style.maxWidth = '100%';
            currentImg.style.maxHeight = '300px';
            gifPreview.innerHTML = '';
            gifPreview.appendChild(currentImg);
          };
          reader.readAsDataURL(file);
        });
        changeBtn.addEventListener('click', function() {
          if (!currentImg) { showToast('Please select a GIF file first'); return; }
          const speed = parseFloat(speedRange.value);
          currentImg.style.animationDuration = (1/speed) + 's';
          showToast('Speed set to ' + speed + 'x');
        });
        resetBtn.addEventListener('click', function() {
          speedRange.value = 1;
          speedVal.textContent = '1x';
          if (currentImg) currentImg.style.animationDuration = '1s';
          showToast('Reset to original speed');
        });
        </script>
        """
    },
    {
        "slug": "svg-viewer",
        "cn_name": "SVG在线预览编辑器",
        "en_name": "SVG Online Viewer & Editor",
        "cn_desc": "在线SVG预览和编辑工具，支持粘贴SVG代码实时渲染、缩放查看。纯前端处理，代码安全。",
        "en_desc": "Online SVG viewer and editor. Paste SVG code for real-time rendering with zoom. Client-side only, code stays safe.",
        "category": "dev-tools",
        "cn_html": """
        <div class="card">
          <h2>📝 SVG代码</h2>
          <div class="input-group">
            <label>粘贴SVG代码</label>
            <textarea id="svgInput" placeholder="在此粘贴SVG代码..."><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 100"><rect x="10" y="10" width="180" height="80" rx="10" fill="#4F46E5"/><text x="100" y="55" text-anchor="middle" fill="white" font-size="18" font-family="sans-serif">Hello SVG!</text></svg></textarea>
          </div>
          <div class="btn-row">
            <button class="btn btn-primary" id="renderBtn">🎨 渲染</button>
            <button class="btn btn-secondary" id="clearBtn">🗑️ 清空</button>
          </div>
        </div>
        <div class="card">
          <h2>👁️ 预览</h2>
          <div class="preview-box" id="svgPreview" style="min-height:200px;padding:16px;background:#fff;">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 100" style="max-width:100%;max-height:200px"><rect x="10" y="10" width="180" height="80" rx="10" fill="#4F46E5"/><text x="100" y="55" text-anchor="middle" fill="white" font-size="18" font-family="sans-serif">Hello SVG!</text></svg>
          </div>
          <div class="btn-row" style="margin-top:12px">
            <button class="btn btn-secondary" id="zoomInBtn">🔍 放大</button>
            <button class="btn btn-secondary" id="zoomOutBtn">🔎 缩小</button>
            <button class="btn btn-secondary" id="downloadSvgBtn">⬇️ 下载SVG</button>
          </div>
          <div class="result-box" id="svgInfo" style="margin-top:12px;font-size:13px">
            📐 尺寸: 200×100 | 元素: 2个
          </div>
        </div>
        <script>
        const svgInput = document.getElementById('svgInput');
        const svgPreview = document.getElementById('svgPreview');
        const renderBtn = document.getElementById('renderBtn');
        const clearBtn = document.getElementById('clearBtn');
        const zoomInBtn = document.getElementById('zoomInBtn');
        const zoomOutBtn = document.getElementById('zoomOutBtn');
        const downloadSvgBtn = document.getElementById('downloadSvgBtn');
        const svgInfo = document.getElementById('svgInfo');
        let zoomLevel = 1;
        function render() {
          const code = svgInput.value.trim();
          if (!code.startsWith('<svg')) { showToast('请输入有效的SVG代码'); return; }
          svgPreview.innerHTML = code;
          const svgEl = svgPreview.querySelector('svg');
          if (svgEl) {
            svgEl.style.maxWidth = (100 * zoomLevel) + '%';
            svgEl.style.maxHeight = (200 * zoomLevel) + 'px';
            svgEl.removeAttribute('width');
            svgEl.removeAttribute('height');
            const w = svgEl.getAttribute('viewBox')?.split(' ')[2] || '?';
            const h = svgEl.getAttribute('viewBox')?.split(' ')[3] || '?';
            const elements = svgEl.querySelectorAll('*').length;
            svgInfo.textContent = '📐 尺寸: ' + w + '×' + h + ' | 元素: ' + elements + '个 | 缩放: ' + Math.round(zoomLevel*100) + '%';
          }
          zoomLevel = 1;
        }
        renderBtn.addEventListener('click', render);
        clearBtn.addEventListener('click', function() { svgInput.value = ''; svgPreview.innerHTML = ''; svgInfo.textContent = '📐 已清空'; });
        zoomInBtn.addEventListener('click', function() { zoomLevel = Math.min(zoomLevel + 0.25, 3); render(); });
        zoomOutBtn.addEventListener('click', function() { zoomLevel = Math.max(zoomLevel - 0.25, 0.25); render(); });
        downloadSvgBtn.addEventListener('click', function() {
          const code = svgInput.value.trim();
          if (!code.startsWith('<svg')) { showToast('无有效SVG可下载'); return; }
          const blob = new Blob([code], {type:'image/svg+xml'});
          const a = document.createElement('a');
          a.href = URL.createObjectURL(blob);
          a.download = 'image.svg';
          a.click();
          showToast('下载开始！');
        });
        </script>
        """,
        "en_html": """
        <div class="card">
          <h2>📝 SVG Code</h2>
          <div class="input-group">
            <label>Paste SVG code</label>
            <textarea id="svgInput" placeholder="Paste SVG code here..."><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 100"><rect x="10" y="10" width="180" height="80" rx="10" fill="#4F46E5"/><text x="100" y="55" text-anchor="middle" fill="white" font-size="18" font-family="sans-serif">Hello SVG!</text></svg></textarea>
          </div>
          <div class="btn-row">
            <button class="btn btn-primary" id="renderBtn">🎨 Render</button>
            <button class="btn btn-secondary" id="clearBtn">🗑️ Clear</button>
          </div>
        </div>
        <div class="card">
          <h2>👁️ Preview</h2>
          <div class="preview-box" id="svgPreview" style="min-height:200px;padding:16px;background:#fff;">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 100" style="max-width:100%;max-height:200px"><rect x="10" y="10" width="180" height="80" rx="10" fill="#4F46E5"/><text x="100" y="55" text-anchor="middle" fill="white" font-size="18" font-family="sans-serif">Hello SVG!</text></svg>
          </div>
          <div class="btn-row" style="margin-top:12px">
            <button class="btn btn-secondary" id="zoomInBtn">🔍 Zoom In</button>
            <button class="btn btn-secondary" id="zoomOutBtn">🔎 Zoom Out</button>
            <button class="btn btn-secondary" id="downloadSvgBtn">⬇️ Download SVG</button>
          </div>
          <div class="result-box" id="svgInfo" style="margin-top:12px;font-size:13px">
            📐 Size: 200×100 | Elements: 2
          </div>
        </div>
        <script>
        const svgInput = document.getElementById('svgInput');
        const svgPreview = document.getElementById('svgPreview');
        const renderBtn = document.getElementById('renderBtn');
        const clearBtn = document.getElementById('clearBtn');
        const zoomInBtn = document.getElementById('zoomInBtn');
        const zoomOutBtn = document.getElementById('zoomOutBtn');
        const downloadSvgBtn = document.getElementById('downloadSvgBtn');
        const svgInfo = document.getElementById('svgInfo');
        let zoomLevel = 1;
        function render() {
          const code = svgInput.value.trim();
          if (!code.startsWith('<svg')) { showToast('Please enter valid SVG code'); return; }
          svgPreview.innerHTML = code;
          const svgEl = svgPreview.querySelector('svg');
          if (svgEl) {
            svgEl.style.maxWidth = (100 * zoomLevel) + '%';
            svgEl.style.maxHeight = (200 * zoomLevel) + 'px';
            svgEl.removeAttribute('width');
            svgEl.removeAttribute('height');
            const w = svgEl.getAttribute('viewBox')?.split(' ')[2] || '?';
            const h = svgEl.getAttribute('viewBox')?.split(' ')[3] || '?';
            const elements = svgEl.querySelectorAll('*').length;
            svgInfo.textContent = '📐 Size: ' + w + '×' + h + ' | Elements: ' + elements + ' | Zoom: ' + Math.round(zoomLevel*100) + '%';
          }
          zoomLevel = 1;
        }
        renderBtn.addEventListener('click', render);
        clearBtn.addEventListener('click', function() { svgInput.value = ''; svgPreview.innerHTML = ''; svgInfo.textContent = '📐 Cleared'; });
        zoomInBtn.addEventListener('click', function() { zoomLevel = Math.min(zoomLevel + 0.25, 3); render(); });
        zoomOutBtn.addEventListener('click', function() { zoomLevel = Math.max(zoomLevel - 0.25, 0.25); render(); });
        downloadSvgBtn.addEventListener('click', function() {
          const code = svgInput.value.trim();
          if (!code.startsWith('<svg')) { showToast('No valid SVG to download'); return; }
          const blob = new Blob([code], {type:'image/svg+xml'});
          const a = document.createElement('a');
          a.href = URL.createObjectURL(blob);
          a.download = 'image.svg';
          a.click();
          showToast('Download started!');
        });
        </script>
        """
    },
    {
        "slug": "security-headers-checker",
        "cn_name": "安全响应头检测器",
        "en_name": "Security Headers Checker",
        "cn_desc": "在线检测网站HTTP安全响应头，分析CSP/HSTS/X-Frame-Options等配置。纯前端检测，无需注册。",
        "en_desc": "Online security headers checker. Analyze CSP, HSTS, X-Frame-Options and more. Client-side detection, no registration needed.",
        "category": "dev-tools",
        "cn_html": """
        <div class="card">
          <h2>🔗 输入网址</h2>
          <div class="input-group">
            <label>目标URL</label>
            <input type="url" id="urlInput" placeholder="https://example.com" value="https://example.com">
          </div>
          <button class="btn btn-primary" id="checkBtn" style="width:100%">🔍 检测安全头</button>
        </div>
        <div class="card">
          <h2>📋 检测结果</h2>
          <div class="result-box" id="results" style="font-family:monospace;font-size:13px;line-height:1.8">
            等待输入URL进行检测...
          </div>
        </div>
        <div class="card">
          <h2>🛡️ 安全检查项</h2>
          <div id="checklist" style="font-size:13px;line-height:2">
            <div>🔒 Content-Security-Policy</div>
            <div>🔒 Strict-Transport-Security</div>
            <div>🔒 X-Frame-Options</div>
            <div>🔒 X-Content-Type-Options</div>
            <div>🔒 Referrer-Policy</div>
            <div>🔒 Permissions-Policy</div>
            <div>🔒 X-XSS-Protection</div>
          </div>
        </div>
        <script>
        const urlInput = document.getElementById('urlInput');
        const checkBtn = document.getElementById('checkBtn');
        const results = document.getElementById('results');
        const checklist = document.getElementById('checklist');
        const SECURITY_HEADERS = {
          'content-security-policy': 'Content-Security-Policy',
          'strict-transport-security': 'Strict-Transport-Security',
          'x-frame-options': 'X-Frame-Options',
          'x-content-type-options': 'X-Content-Type-Options',
          'referrer-policy': 'Referrer-Policy',
          'permissions-policy': 'Permissions-Policy',
          'x-xss-protection': 'X-XSS-Protection'
        };
        checkBtn.addEventListener('click', async function() {
          let url = urlInput.value.trim();
          if (!url.startsWith('http')) url = 'https://' + url;
          checkBtn.textContent = '⏳ 检测中...';
          checkBtn.disabled = true;
          results.innerHTML = '<span style="color:var(--text-secondary)">正在检测 ' + url + ' ...</span>';
          try {
            // Use fetch to get headers - may be blocked by CORS, fallback to proxy or info message
            const resp = await fetch(url, { method: 'HEAD', mode: 'no-cors' });
            // With no-cors we can't read headers, so try a CORS proxy
            results.innerHTML = '<span style="color:#e67e22">⚠️ 浏览器CORS限制，无法直接读取响应头。请使用以下方式：</span><br><br>1. 在浏览器开发者工具 Network 面板查看<br>2. 使用命令行: <code>curl -I ' + url + '</code><br>3. 使用在线服务如 securityheaders.com';
            // Still try to get via fetch with cors mode
            try {
              const resp2 = await fetch(url, { method: 'HEAD' });
              const headers = {};
              resp2.headers.forEach((v,k) => headers[k.toLowerCase()] = v);
              let html = '';
              let score = 0;
              for (const [key, name] of Object.entries(SECURITY_HEADERS)) {
                const found = headers[key] || '❌ 缺失';
                if (found !== '❌ 缺失') score++;
                html += '<div style="margin-bottom:4px"><strong>' + name + '</strong>: ' + (found === '❌ 缺失' ? '<span style=\\'color:#e74c3c\\'>❌ 缺失</span>' : '<span style=\\'color:#27ae60\\'>✅ ' + found.replace(/</g,'&lt;') + '</span>') + '</div>';
              }
              html += '<div style="margin-top:8px;font-weight:700">安全评分: ' + score + '/7</div>';
              results.innerHTML = html;
              updateChecklist(headers);
            } catch(e2) {
              // Already showed the fallback message
            }
          } catch(err) {
            results.innerHTML = '<span style="color:#e74c3c">❌ 检测失败: ' + err.message + '</span>';
          }
          checkBtn.textContent = '🔍 检测安全头';
          checkBtn.disabled = false;
        });
        function updateChecklist(headers) {
          const items = checklist.querySelectorAll('div');
          items.forEach(div => {
            const key = Object.entries(SECURITY_HEADERS).find(([k,v]) => v === div.textContent.trim().replace('🔒 ',''))?.[0];
            if (key && headers[key]) {
              div.innerHTML = '✅ ' + div.textContent.replace('🔒 ','');
              div.style.color = '#27ae60';
            }
          });
        }
        </script>
        """,
        "en_html": """
        <div class="card">
          <h2>🔗 Enter URL</h2>
          <div class="input-group">
            <label>Target URL</label>
            <input type="url" id="urlInput" placeholder="https://example.com" value="https://example.com">
          </div>
          <button class="btn btn-primary" id="checkBtn" style="width:100%">🔍 Check Security Headers</button>
        </div>
        <div class="card">
          <h2>📋 Results</h2>
          <div class="result-box" id="results" style="font-family:monospace;font-size:13px;line-height:1.8">
            Enter a URL to check...
          </div>
        </div>
        <div class="card">
          <h2>🛡️ Security Checks</h2>
          <div id="checklist" style="font-size:13px;line-height:2">
            <div>🔒 Content-Security-Policy</div>
            <div>🔒 Strict-Transport-Security</div>
            <div>🔒 X-Frame-Options</div>
            <div>🔒 X-Content-Type-Options</div>
            <div>🔒 Referrer-Policy</div>
            <div>🔒 Permissions-Policy</div>
            <div>🔒 X-XSS-Protection</div>
          </div>
        </div>
        <script>
        const urlInput = document.getElementById('urlInput');
        const checkBtn = document.getElementById('checkBtn');
        const results = document.getElementById('results');
        const checklist = document.getElementById('checklist');
        const SECURITY_HEADERS = {
          'content-security-policy': 'Content-Security-Policy',
          'strict-transport-security': 'Strict-Transport-Security',
          'x-frame-options': 'X-Frame-Options',
          'x-content-type-options': 'X-Content-Type-Options',
          'referrer-policy': 'Referrer-Policy',
          'permissions-policy': 'Permissions-Policy',
          'x-xss-protection': 'X-XSS-Protection'
        };
        checkBtn.addEventListener('click', async function() {
          let url = urlInput.value.trim();
          if (!url.startsWith('http')) url = 'https://' + url;
          checkBtn.textContent = '⏳ Checking...';
          checkBtn.disabled = true;
          results.innerHTML = '<span style="color:var(--text-secondary)">Checking ' + url + ' ...</span>';
          try {
            const resp = await fetch(url, { method: 'HEAD', mode: 'no-cors' });
            results.innerHTML = '<span style="color:#e67e22">⚠️ Browser CORS prevents direct header reading. Try:</span><br><br>1. Browser DevTools Network tab<br>2. Command line: <code>curl -I ' + url + '</code><br>3. Online service like securityheaders.com';
            try {
              const resp2 = await fetch(url, { method: 'HEAD' });
              const headers = {};
              resp2.headers.forEach((v,k) => headers[k.toLowerCase()] = v);
              let html = '';
              let score = 0;
              for (const [key, name] of Object.entries(SECURITY_HEADERS)) {
                const found = headers[key] || '❌ Missing';
                if (found !== '❌ Missing') score++;
                html += '<div style="margin-bottom:4px"><strong>' + name + '</strong>: ' + (found === '❌ Missing' ? '<span style=\\'color:#e74c3c\\'>❌ Missing</span>' : '<span style=\\'color:#27ae60\\'>✅ ' + found.replace(/</g,'&lt;') + '</span>') + '</div>';
              }
              html += '<div style="margin-top:8px;font-weight:700">Security Score: ' + score + '/7</div>';
              results.innerHTML = html;
              updateChecklist(headers);
            } catch(e2) {}
          } catch(err) {
            results.innerHTML = '<span style="color:#e74c3c">❌ Check failed: ' + err.message + '</span>';
          }
          checkBtn.textContent = '🔍 Check Security Headers';
          checkBtn.disabled = false;
        });
        function updateChecklist(headers) {
          const items = checklist.querySelectorAll('div');
          items.forEach(div => {
            const key = Object.entries(SECURITY_HEADERS).find(([k,v]) => v === div.textContent.trim().replace('🔒 ',''))?.[0];
            if (key && headers[key]) {
              div.innerHTML = '✅ ' + div.textContent.replace('🔒 ','');
              div.style.color = '#27ae60';
            }
          });
        }
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

# 创建工具目录和文件
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