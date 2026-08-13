// Mouse Click Counter - app.js (EN)
(function() {
  const toolArea = document.getElementById('toolArea');
  const html = `
    <div class="stat-row">
      <div class="stat"><div class="stat-value" id="totalClicks">0</div><div class="stat-label">Total Clicks</div></div>
      <div class="stat"><div class="stat-value" id="cpsDisplay">0</div><div class="stat-label">CPS</div></div>
      <div class="stat"><div class="stat-value" id="timerDisplay">0s</div><div class="stat-label">Timer</div></div>
    </div>
    <div class="stat-row" style="margin-top:8px;">
      <div class="stat"><div class="stat-value" id="leftClicks">0</div><div class="stat-label">Left</div></div>
      <div class="stat"><div class="stat-value" id="rightClicks">0</div><div class="stat-label">Right</div></div>
      <div class="stat"><div class="stat-value" id="middleClicks">0</div><div class="stat-label">Middle</div></div>
    </div>
    <div class="card" style="margin-top:16px;text-align:center;">
      <div id="clickArea" style="padding:60px 20px;background:linear-gradient(135deg,#667eea,#764ba2);border-radius:12px;cursor:pointer;user-select:none;color:#fff;font-size:18px;font-weight:700;">
        🖱️ Click Here!
      </div>
    </div>
    <div class="input-group" style="margin-top:12px;justify-content:center;">
      <button class="btn-primary" id="btnStartTimer">Start Timer</button>
      <button class="btn-secondary" id="btnStopTimer">Stop</button>
      <button class="btn-secondary" id="btnResetClicks">Reset</button>
      <button class="btn-secondary" id="btnCopyResult">📋 Copy Result</button>
    </div>
    <div class="result" id="clickResult" style="text-align:center;color:var(--text2);">Click the area above to start counting (CPS calculated in timer mode only)</div>
    <div class="card" style="margin-top:12px;">
      <div style="font-size:13px;color:var(--text2);margin-bottom:8px;text-align:center;">📊 Click Distribution</div>
      <canvas id="clickChart" style="width:100%;height:140px;background:#0f172a;border:1px solid rgba(148,163,184,.1);border-radius:8px;"></canvas>
    </div>
  `;
  toolArea.innerHTML = html;

  let totalClicks = 0, leftClicks = 0, rightClicks = 0, middleClicks = 0;
  let timerRunning = false, timerInterval = null, startTime = null;

  function showToast(msg) {
    const t = document.getElementById('toast');
    t.textContent = msg; t.classList.add('show');
    setTimeout(() => t.classList.remove('show'), 2000);
  }

  function updateDisplay() {
    document.getElementById('totalClicks').textContent = totalClicks;
    document.getElementById('leftClicks').textContent = leftClicks;
    document.getElementById('rightClicks').textContent = rightClicks;
    document.getElementById('middleClicks').textContent = middleClicks;
    
    if (timerRunning && startTime) {
      const elapsed = (Date.now() - startTime) / 1000;
      const cps = elapsed > 0 ? (totalClicks / elapsed).toFixed(1) : 0;
      document.getElementById('cpsDisplay').textContent = cps;
      document.getElementById('timerDisplay').textContent = Math.round(elapsed) + 's';
    }
    drawChart();
  }

  function drawChart() {
    const canvas = document.getElementById('clickChart');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const dpr = window.devicePixelRatio || 1;
    const w = canvas.clientWidth;
    const h = canvas.clientHeight;
    canvas.width = w * dpr;
    canvas.height = h * dpr;
    ctx.scale(dpr, dpr);
    ctx.clearRect(0, 0, w, h);

    const data = [
      { label: 'Left', value: leftClicks, color: '#22d3ee' },
      { label: 'Right', value: rightClicks, color: '#f59e0b' },
      { label: 'Middle', value: middleClicks, color: '#10b981' }
    ];
    const max = Math.max(1, leftClicks, rightClicks, middleClicks);
    const barAreaH = h - 30;
    const barW = Math.min(80, (w - 40) / data.length);
    const gap = 12;

    ctx.font = '12px sans-serif';
    ctx.textAlign = 'center';
    data.forEach(function(d, i) {
      const barH = Math.max(2, (d.value / max) * barAreaH);
      const x = 20 + i * (barW + gap) + (w - 40 - data.length * (barW + gap)) / 2;
      const y = h - 20 - barH;
      ctx.fillStyle = d.color;
      ctx.fillRect(x, y, barW, barH);
      ctx.fillStyle = '#94a3b8';
      ctx.fillText(d.label, x + barW / 2, h - 6);
      ctx.fillStyle = '#e2e8f0';
      ctx.fillText(String(d.value), x + barW / 2, y - 4);
    });
  }

  function handleClick(e) {
    e.preventDefault();
    totalClicks++;
    if (e.button === 0) leftClicks++;
    else if (e.button === 2) rightClicks++;
    else if (e.button === 1) middleClicks++;
    updateDisplay();
  }

  document.getElementById('clickArea').addEventListener('mousedown', handleClick);
  document.getElementById('clickArea').addEventListener('contextmenu', e => e.preventDefault());

  document.getElementById('btnStartTimer').addEventListener('click', () => {
    if (timerRunning) return;
    timerRunning = true;
    totalClicks = leftClicks = rightClicks = middleClicks = 0;
    startTime = Date.now();
    document.getElementById('clickResult').textContent = 'Timer running... Click as fast as you can!';
    timerInterval = setInterval(updateDisplay, 100);
    updateDisplay();
    showToast('Timer started!');
  });

  document.getElementById('btnStopTimer').addEventListener('click', () => {
    if (!timerRunning) return;
    timerRunning = false;
    clearInterval(timerInterval);
    const elapsed = (Date.now() - startTime) / 1000;
    const cps = elapsed > 0 ? (totalClicks / elapsed).toFixed(1) : 0;
    document.getElementById('cpsDisplay').textContent = cps;
    document.getElementById('timerDisplay').textContent = Math.round(elapsed) + 's';
    document.getElementById('clickResult').innerHTML = 
      `⏱ Timer Stopped | Clicks: <b>${totalClicks}</b> | Time: <b>${Math.round(elapsed)}s</b> | CPS: <b>${cps}</b>`;
    showToast('Timer stopped!');
  });

  document.getElementById('btnResetClicks').addEventListener('click', () => {
    timerRunning = false;
    clearInterval(timerInterval);
    totalClicks = leftClicks = rightClicks = middleClicks = 0;
    startTime = null;
    document.getElementById('cpsDisplay').textContent = '0';
    document.getElementById('timerDisplay').textContent = '0s';
    document.getElementById('clickResult').textContent = 'Click the area above to start counting (CPS calculated in timer mode only)';
    updateDisplay();
  });

  document.getElementById('btnCopyResult').addEventListener('click', () => {
    const resultText = document.getElementById('clickResult').textContent;
    const report = 'Mouse Click Counter Report\nTotal: ' + totalClicks + '\nLeft: ' + leftClicks + '\nRight: ' + rightClicks + '\nMiddle: ' + middleClicks + '\nCPS: ' + document.getElementById('cpsDisplay').textContent + '\nTimer: ' + document.getElementById('timerDisplay').textContent + '\nStatus: ' + resultText;
    function ok() { showToast('Copied!'); }
    function fallback() {
      const ta = document.createElement('textarea');
      ta.value = report;
      ta.style.position = 'fixed';
      ta.style.opacity = '0';
      document.body.appendChild(ta);
      ta.select();
      try { document.execCommand('copy'); ok(); } catch (e) { showToast('Copy failed'); }
      document.body.removeChild(ta);
    }
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(report).then(ok).catch(fallback);
    } else { fallback(); }
  });

  drawChart();
})();