// Typing Race - app.js (EN)
(function() {
  const toolArea = document.getElementById('toolArea');
  const paragraphs = [
    "The quick brown fox jumps over the lazy dog near the river bank on a sunny afternoon.",
    "In the heart of the bustling city, people hurried along crowded streets while neon lights flickered overhead.",
    "Science has revealed that regular exercise improves both physical health and mental clarity significantly.",
    "Mountains stood tall against the horizon, their peaks covered in snow even during the summer months.",
    "Technology continues to reshape how we communicate, work, and interact with the world around us.",
    "A gentle breeze carried the scent of blooming flowers through the open window of the quiet cottage.",
    "Learning a new skill requires patience, practice, and the willingness to make mistakes along the way.",
    "The ancient library contained thousands of manuscripts that had survived through centuries of careful preservation.",
    "Music has the remarkable ability to evoke memories and emotions that words alone cannot express.",
    "Deep beneath the ocean surface, creatures of extraordinary beauty thrive in complete darkness and extreme pressure."
  ];

  const html = `
    <div class="stat-row">
      <div class="stat"><div class="stat-value" id="wpmDisplay">0</div><div class="stat-label">WPM</div></div>
      <div class="stat"><div class="stat-value" id="accuracyDisplay">100%</div><div class="stat-label">Accuracy</div></div>
      <div class="stat"><div class="stat-value" id="timeDisplay">0s</div><div class="stat-label">Time</div></div>
    </div>
    <div class="card" style="margin-top:16px;">
      <div id="targetText" style="font-size:18px;line-height:1.8;color:#64748b;padding:12px;background:#f8fafc;border-radius:8px;min-height:80px;"></div>
      <textarea id="userInput" placeholder="Type the text above here..." style="margin-top:12px;font-size:16px;" rows="3" disabled></textarea>
    </div>
    <div class="input-group" style="margin-top:8px;">
      <button class="btn-primary" id="btnStart">Start Race</button>
      <button class="btn-secondary" id="btnReset">New Text</button>
    </div>
    <div id="result" style="background:#1e293b;border:1px solid rgba(148,163,184,.1);border-radius:12px;padding:16px;margin-top:16px;">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;flex-wrap:wrap;gap:8px">
        <span style="color:#f1f5f9;font-weight:600;font-size:.95rem">📊 Race Result &amp; History</span>
        <button id="copyResult" style="padding:6px 14px;border:1px solid rgba(6,182,212,.3);background:rgba(6,182,212,.2);color:#22d3ee;border-radius:6px;cursor:pointer;font-size:.8rem">📋 Copy Result</button>
      </div>
      <div id="raceResult" style="text-align:center;color:#94a3b8;background:#0f172a;border-radius:8px;padding:12px;">Click "Start Race" to challenge your typing speed</div>
      <canvas id="historyChart" width="600" height="200" style="width:100%;height:auto;margin-top:12px;background:#0f172a;border-radius:8px;display:none"></canvas>
    </div>
  `;
  toolArea.innerHTML = html;

  let targetText = '';
  let startTime = null;
  let timerInterval = null;
  let racing = false;
  let lastResult = '';
  let history = [];
  try { history = JSON.parse(localStorage.getItem('typingRaceHistory') || '[]'); } catch (e) { history = []; }

  function copyTextFb(t) {
    if (navigator.clipboard) {
      navigator.clipboard.writeText(t).then(() => showToast('Result copied'), () => showToast('Copy failed'));
    } else {
      const ta = document.createElement('textarea');
      ta.value = t; ta.style.position = 'fixed'; ta.style.left = '-9999px';
      document.body.appendChild(ta); ta.select();
      document.execCommand('copy');
      document.body.removeChild(ta);
      showToast('Result copied');
    }
  }

  function renderChart() {
    const c = document.getElementById('historyChart');
    if (!c || history.length === 0) return;
    c.style.display = 'block';
    const ctx = c.getContext('2d');
    const W = c.width, H = c.height, pad = 30;
    ctx.fillStyle = '#0f172a'; ctx.fillRect(0, 0, W, H);
    const max = Math.max(20, ...history.map(h => h.wpm));
    const n = history.length, bw = (W - pad * 2) / Math.max(n, 1);
    history.forEach(function(h, i) {
      const hh = (h.wpm / max) * (H - pad * 2);
      ctx.fillStyle = 'rgba(6,182,212,.85)';
      ctx.fillRect(pad + i * bw + 4, H - pad - hh, bw - 8, hh);
      ctx.fillStyle = '#94a3b8'; ctx.font = '10px monospace'; ctx.textAlign = 'center';
      ctx.fillText(h.wpm, pad + i * bw + bw / 2, H - pad - hh - 4);
    });
    ctx.fillStyle = '#64748b'; ctx.textAlign = 'left'; ctx.font = '10px monospace';
    ctx.fillText('WPM per race (last ' + n + ')', 8, 14);
  }

  function showToast(msg) {
    const t = document.getElementById('toast');
    t.textContent = msg; t.classList.add('show');
    setTimeout(() => t.classList.remove('show'), 2000);
  }

  function pickParagraph() {
    return paragraphs[Math.floor(Math.random() * paragraphs.length)];
  }

  function renderTarget(text, userText) {
    let html = '';
    for (let i = 0; i < text.length; i++) {
      if (i < userText.length) {
        html += text[i] === userText[i] 
          ? `<span style="color:#10B981;">${text[i]}</span>` 
          : `<span style="color:#EF4444;background:#FEE2E2;">${text[i]}</span>`;
      } else {
        html += `<span>${text[i]}</span>`;
      }
    }
    return html;
  }

  function updateStats() {
    if (!startTime) return;
    const elapsed = (Date.now() - startTime) / 1000;
    const userText = document.getElementById('userInput').value;
    const wordsTyped = userText.trim().split(/\s+/).length;
    const wpm = elapsed > 0 ? Math.round((wordsTyped / elapsed) * 60) : 0;
    
    let correct = 0;
    for (let i = 0; i < Math.min(userText.length, targetText.length); i++) {
      if (userText[i] === targetText[i]) correct++;
    }
    const accuracy = userText.length > 0 ? Math.round((correct / userText.length) * 100) : 100;

    document.getElementById('wpmDisplay').textContent = wpm;
    document.getElementById('accuracyDisplay').textContent = accuracy + '%';
    document.getElementById('timeDisplay').textContent = Math.round(elapsed) + 's';
    document.getElementById('targetText').innerHTML = renderTarget(targetText, userText);

    if (userText.length >= targetText.length && racing) {
      racing = false;
      clearInterval(timerInterval);
      document.getElementById('userInput').disabled = true;
      const finalWPM = wpm;
      const rating = finalWPM > 80 ? '🏆 Elite' : finalWPM > 60 ? '🥇 Excellent' : finalWPM > 40 ? '🥈 Good' : finalWPM > 20 ? '🥉 Average' : '💪 Keep Practicing';
      document.getElementById('raceResult').innerHTML = `🎉 Complete! WPM: <b>${finalWPM}</b> | Accuracy: <b>${accuracy}%</b> | Rating: <b>${rating}</b>`;
      lastResult = `Typing Race Result | WPM: ${finalWPM} | Accuracy: ${accuracy}% | Time: ${Math.round(elapsed)}s | Rating: ${rating}`;
      history.unshift({ wpm: finalWPM, accuracy, rating });
      history = history.slice(0, 10);
      localStorage.setItem('typingRaceHistory', JSON.stringify(history));
      renderChart();
      showToast('Race complete!');
    }
  }

  document.getElementById('btnStart').addEventListener('click', () => {
    if (racing) return;
    racing = true;
    document.getElementById('userInput').disabled = false;
    document.getElementById('userInput').value = '';
    document.getElementById('userInput').focus();
    document.getElementById('raceResult').textContent = 'Racing...';
    startTime = Date.now();
    timerInterval = setInterval(updateStats, 200);
  });

  document.getElementById('btnReset').addEventListener('click', () => {
    racing = false;
    clearInterval(timerInterval);
    targetText = pickParagraph();
    document.getElementById('targetText').innerHTML = targetText;
    document.getElementById('userInput').value = '';
    document.getElementById('userInput').disabled = true;
    document.getElementById('wpmDisplay').textContent = '0';
    document.getElementById('accuracyDisplay').textContent = '100%';
    document.getElementById('timeDisplay').textContent = '0s';
    document.getElementById('raceResult').textContent = 'Click "Start Race" to challenge your typing speed';
    startTime = null;
  });

  document.getElementById('userInput').addEventListener('input', updateStats);

  document.getElementById('copyResult').addEventListener('click', () => {
    if (!lastResult) { showToast('Finish a race first'); return; }
    copyTextFb(lastResult);
  });

  targetText = pickParagraph();
  document.getElementById('targetText').innerHTML = targetText;
  renderChart();
})();