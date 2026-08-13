// Text to Favicon - app.js (EN)
(function() {
  const toolArea = document.getElementById('toolArea');
  const html = `
    <div class="input-group">
      <input type="text" id="faviconText" placeholder="Enter text (1-3 chars best)" maxlength="5" value="A" style="flex:1;min-width:150px;">
    </div>
    <div class="input-group">
      <label style="font-size:13px;color:var(--text2);">Background</label>
      <input type="color" id="bgColor" value="#4F46E5">
      <label style="font-size:13px;color:var(--text2);margin-left:8px;">Text Color</label>
      <input type="color" id="textColor" value="#FFFFFF">
      <label style="font-size:13px;color:var(--text2);margin-left:8px;">Font Size</label>
      <input type="number" id="fontSize" value="80" min="20" max="180" style="width:65px;">
      <label style="font-size:13px;color:var(--text2);margin-left:8px;">Radius</label>
      <input type="number" id="borderRadius" value="8" min="0" max="64" style="width:65px;">
    </div>
    <div class="input-group">
      <button class="btn-primary" id="btnGenerate">Generate</button>
      <button class="btn-secondary" id="btnRandom">🎲 Random</button>
      <button class="btn-secondary" id="btnCopyPNG">📋 Copy PNG</button>
      <button class="btn-secondary" id="btnDownloadPNG">Download PNG</button>
      <button class="btn-secondary" id="btnDownloadSVG">Download SVG</button>
    </div>
    <div style="text-align:center;margin-top:16px;">
      <canvas id="faviconCanvas" width="256" height="256" style="border-radius:8px;box-shadow:0 4px 12px rgba(0,0,0,0.1);max-width:256px;"></canvas>
    </div>
    <div class="result" id="faviconResult" style="text-align:center;color:var(--text2);margin-top:8px;">Preview 256×256</div>
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

    ctx.clearRect(0, 0, w, h);

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

    ctx.fillStyle = textColor;
    ctx.font = `bold ${fontSize}px -apple-system, BlinkMacSystemFont, sans-serif`;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(text, w/2, h/2);

    document.getElementById('faviconResult').textContent = 'Preview 256×256 · Click download button to save';
  }

  function downloadPNG() {
    const canvas = document.getElementById('faviconCanvas');
    const link = document.createElement('a');
    link.download = 'favicon.png';
    link.href = canvas.toDataURL('image/png');
    link.click();
    showToast('Downloading PNG...');
  }

  const RANDOM_TEXTS = ['AB', 'FT', '🧡', '☀', 'OK', '88', 'Hi', '★'];

  function randomText() {
    const input = document.getElementById('faviconText');
    input.value = RANDOM_TEXTS[Math.floor(Math.random() * RANDOM_TEXTS.length)];
    generateFavicon();
    showToast('Random sample filled');
  }

  function copyPNG() {
    const canvas = document.getElementById('faviconCanvas');
    canvas.toBlob((blob) => {
      if (!blob) { showToast('Copy not supported'); return; }
      const item = new ClipboardItem({'image/png': blob});
      navigator.clipboard.write([item]).then(() => {
        showToast('PNG copied to clipboard');
      }).catch(() => {
        showToast('Copy blocked — use Download PNG instead');
      });
    }, 'image/png');
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
    showToast('Downloading SVG...');
  }

  ['faviconText','bgColor','textColor','fontSize','borderRadius'].forEach(id => {
    document.getElementById(id).addEventListener('input', generateFavicon);
  });
  document.getElementById('btnGenerate').addEventListener('click', generateFavicon);
  document.getElementById('btnRandom').addEventListener('click', randomText);
  document.getElementById('btnCopyPNG').addEventListener('click', copyPNG);
  document.getElementById('btnDownloadPNG').addEventListener('click', downloadPNG);
  document.getElementById('btnDownloadSVG').addEventListener('click', downloadSVG);

  generateFavicon();
})();