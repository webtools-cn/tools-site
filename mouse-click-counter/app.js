// Mouse Click Counter - app.js
(function() {
  const toolArea = document.getElementById('toolArea');
  const html = `
    <div class="stat-row">
      <div class="stat"><div class="stat-value" id="totalClicks">0</div><div class="stat-label">总点击数</div></div>
      <div class="stat"><div class="stat-value" id="cpsDisplay">0</div><div class="stat-label">CPS</div></div>
      <div class="stat"><div class="stat-value" id="timerDisplay">0s</div><div class="stat-label">计时</div></div>
    </div>
    <div class="stat-row" style="margin-top:8px;">
      <div class="stat"><div class="stat-value" id="leftClicks">0</div><div class="stat-label">左键</div></div>
      <div class="stat"><div class="stat-value" id="rightClicks">0</div><div class="stat-label">右键</div></div>
      <div class="stat"><div class="stat-value" id="middleClicks">0</div><div class="stat-label">中键</div></div>
    </div>
    <div class="card" style="margin-top:16px;text-align:center;">
      <div id="clickArea" style="padding:60px 20px;background:linear-gradient(135deg,#667eea,#764ba2);border-radius:12px;cursor:pointer;user-select:none;color:#fff;font-size:18px;font-weight:700;">
        🖱️ 在这里点击！
      </div>
    </div>
    <div class="input-group" style="margin-top:12px;justify-content:center;">
      <button class="btn-primary" id="btnStartTimer">开始计时</button>
      <button class="btn-secondary" id="btnStopTimer">停止</button>
      <button class="btn-secondary" id="btnResetClicks">重置计数</button>
    </div>
    <div class="result" id="clickResult" style="text-align:center;color:var(--text2);">点击上方区域开始计数（计时模式下才计算CPS）</div>
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
    document.getElementById('clickResult').textContent = '计时中... 疯狂点击吧！';
    timerInterval = setInterval(updateDisplay, 100);
    updateDisplay();
    showToast('计时开始！');
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
      `⏱ 计时结束 | 总点击: <b>${totalClicks}</b> | 用时: <b>${Math.round(elapsed)}s</b> | CPS: <b>${cps}</b>`;
    showToast('计时结束！');
  });

  document.getElementById('btnResetClicks').addEventListener('click', () => {
    timerRunning = false;
    clearInterval(timerInterval);
    totalClicks = leftClicks = rightClicks = middleClicks = 0;
    startTime = null;
    document.getElementById('cpsDisplay').textContent = '0';
    document.getElementById('timerDisplay').textContent = '0s';
    document.getElementById('clickResult').textContent = '点击上方区域开始计数（计时模式下才计算CPS）';
    updateDisplay();
  });
})();