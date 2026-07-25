// Text to Favicon - app.js
(function() {
  const toolArea = document.getElementById('toolArea');
  const html = `
    <div class="input-group">
      <input type="text" id="faviconText" placeholder="输入文字（1-3个字符最佳）" maxlength="5" value="A" style="flex:1;min-width:150px;">
    </div>
    <div class="input-group">
      <label style="font-size:13px;color:var(--text2);">背景色</label>
      <input type="color" id="bgColor" value="#4F46E5">
      <label style="font-size:13px;color:var(--text2);margin-left:8px;">文字色</label>
      <input type="color" id="textColor" value="#FFFFFF">
      <label style="font-size:13px;color:var(--text2);margin-left:8px;">字号</label>
      <input type="number" id="fontSize" value="80" min="20" max="180" style="width:65px;">
      <label style="font-size:13px;color:var(--text2);margin-left:8px;">圆角</label>
      <input type="number" id="borderRadius" value="8" min="0" max="64" style="width:65px;">
    </div>
    <div class="input-group">
      <button class="btn-primary" id="btnGenerate">生成Favicon</button>
      <button class="btn-secondary" id="btnDownloadPNG">下载PNG</button>
      <button class="btn-secondary" id="btnDownloadSVG">下载SVG</button>
    </div>
    <div style="text-align:center;margin-top:16px;">
      <canvas id="faviconCanvas" width="256" height="256" style="border-radius:8px;box-shadow:0 4px 12px rgba(0,0,0,0.1);max-width:256px;"></canvas>
    </div>
    <div class="result" id="faviconResult" style="text-align:center;color:var(--text2);margin-top:8px;">预览 256×256</div>
  `;
  toolArea.innerHTML = html;

  function showToast(msg) {
    const t = document.getElementById('toast');
    t.textContent = msg; t.classList.add('show');
    setTimeout(() => t.classList.remove('show'), 2000);
  }

  function generateFavicon() {
    const canvas = document.getElementById('faviconCanvas');
    const ctx = canvas.getContext('2d');
    const w = canvas.width, h = canvas.height;
    const text = document.getElementById('faviconText').value || 'A';
    const bgColor = document.getElementById('bgColor').value;
    const textColor = document.getElementById('textColor').value;
    const fontSize = parseInt(document.getElementById('fontSize').value) || 80;
    const borderRadius = parseInt(document.getElementById('borderRadius').value) || 8;

    // Clear
    ctx.clearRect(0, 0, w, h);

    // Rounded rect background
    const r = borderRadius * (w / 256);
    ctx.beginPath();
    ctx.moveTo(r, 0);
    ctx.lineTo(w - r, 0);
    ctx.quadraticCurveTo(w, 0, w, r);
    ctx.lineTo(w, h - r);
    ctx.quadraticCurveTo(w, h, w - r, h);
    ctx.lineTo(r, h);
    ctx.quadraticCurveTo(0, h, 0, h - r);
    ctx.lineTo(0, r);
    ctx.quadraticCurveTo(0, 0, r, 0);
    ctx.closePath();
    ctx.fillStyle = bgColor;
    ctx.fill();

    // Text
    ctx.fillStyle = textColor;
    ctx.font = `bold ${fontSize}px -apple-system, BlinkMacSystemFont, sans-serif`;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(text, w/2, h/2);

    document.getElementById('faviconResult').textContent = '预览 256×256 · 点击下载按钮保存';
  }

  function downloadPNG() {
    const canvas = document.getElementById('faviconCanvas');
    const link = document.createElement('a');
    link.download = 'favicon.png';
    link.href = canvas.toDataURL('image/png');
    link.click();
    showToast('PNG下载中...');
  }

  function downloadSVG() {
    const text = document.getElementById('faviconText').value || 'A';
    const bgColor = document.getElementById('bgColor').value;
    const textColor = document.getElementById('textColor').value;
    const fontSize = parseInt(document.getElementById('fontSize').value) || 80;
    const borderRadius = parseInt(document.getElementById('borderRadius').value) || 8;

    const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 256 256">
  <rect width="256" height="256" rx="${borderRadius}" fill="${bgColor}"/>
  <text x="128" y="128" text-anchor="middle" dominant-baseline="central" font-family="system-ui,sans-serif" font-weight="bold" font-size="${fontSize}" fill="${textColor}">${text}</text>
</svg>`;
    const blob = new Blob([svg], {type: 'image/svg+xml'});
    const link = document.createElement('a');
    link.download = 'favicon.svg';
    link.href = URL.createObjectURL(blob);
    link.click();
    URL.revokeObjectURL(link.href);
    showToast('SVG下载中...');
  }

  // Live preview on any change
  ['faviconText','bgColor','textColor','fontSize','borderRadius'].forEach(id => {
    document.getElementById(id).addEventListener('input', generateFavicon);
  });
  document.getElementById('btnGenerate').addEventListener('click', generateFavicon);
  document.getElementById('btnDownloadPNG').addEventListener('click', downloadPNG);
  document.getElementById('btnDownloadSVG').addEventListener('click', downloadSVG);

  generateFavicon();
})();