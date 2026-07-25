// Polygon Area Calculator - app.js
(function() {
  const toolArea = document.getElementById('toolArea');
  
  const html = `
    <h2>输入顶点坐标</h2>
    <div class="input-group">
      <textarea id="vertexInput" placeholder="每行一个顶点，格式：x,y&#10;例如：&#10;0,0&#10;4,0&#10;4,3&#10;0,3" rows="6"></textarea>
    </div>
    <div class="input-group">
      <button class="btn-primary" id="btnCalc">计算面积</button>
      <button class="btn-secondary" id="btnClear">清空</button>
      <button class="btn-secondary" id="btnExample">加载示例</button>
    </div>
    <div class="result" id="areaResult">输入顶点坐标后点击"计算面积"</div>
    <canvas id="polyCanvas" width="600" height="400" style="width:100%;height:auto;border:1px solid #e2e8f0;margin-top:12px;"></canvas>
  `;
  toolArea.innerHTML = html;

  function showToast(msg) {
    const t = document.getElementById('toast');
    t.textContent = msg; t.classList.add('show');
    setTimeout(() => t.classList.remove('show'), 2000);
  }

  function parseVertices(text) {
    const vertices = [];
    const lines = text.trim().split('\n');
    for (const line of lines) {
      const parts = line.trim().split(/[\s,]+/);
      if (parts.length >= 2) {
        const x = parseFloat(parts[0]);
        const y = parseFloat(parts[1]);
        if (!isNaN(x) && !isNaN(y)) vertices.push({x, y});
      }
    }
    return vertices;
  }

  function shoelaceArea(vertices) {
    const n = vertices.length;
    if (n < 3) return 0;
    let area = 0;
    for (let i = 0; i < n; i++) {
      const j = (i + 1) % n;
      area += vertices[i].x * vertices[j].y;
      area -= vertices[j].x * vertices[i].y;
    }
    return Math.abs(area) / 2;
  }

  function drawPolygon(vertices) {
    const canvas = document.getElementById('polyCanvas');
    const ctx = canvas.getContext('2d');
    const w = canvas.width, h = canvas.height;
    ctx.clearRect(0, 0, w, h);
    if (vertices.length < 2) return;

    // Find bounds
    let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
    vertices.forEach(v => {
      if (v.x < minX) minX = v.x;
      if (v.y < minY) minY = v.y;
      if (v.x > maxX) maxX = v.x;
      if (v.y > maxY) maxY = v.y;
    });
    
    const pad = 40;
    const rangeX = maxX - minX || 1;
    const rangeY = maxY - minY || 1;
    const scale = Math.min((w - 2*pad) / rangeX, (h - 2*pad) / rangeY);
    
    function tx(x) { return pad + (x - minX) * scale; }
    function ty(y) { return h - pad - (y - minY) * scale; }

    // Draw grid
    ctx.strokeStyle = '#e2e8f0';
    ctx.lineWidth = 0.5;
    for (let i = 0; i <= 10; i++) {
      const x = pad + i * (w - 2*pad) / 10;
      ctx.beginPath(); ctx.moveTo(x, pad); ctx.lineTo(x, h - pad); ctx.stroke();
      const y = pad + i * (h - 2*pad) / 10;
      ctx.beginPath(); ctx.moveTo(pad, y); ctx.lineTo(w - pad, y); ctx.stroke();
    }

    // Draw axes
    ctx.strokeStyle = '#94a3b8';
    ctx.lineWidth = 1;
    ctx.beginPath(); ctx.moveTo(pad, h-pad); ctx.lineTo(w-pad, h-pad); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(pad, pad); ctx.lineTo(pad, h-pad); ctx.stroke();

    // Draw polygon
    if (vertices.length >= 2) {
      ctx.beginPath();
      ctx.moveTo(tx(vertices[0].x), ty(vertices[0].y));
      for (let i = 1; i < vertices.length; i++) {
        ctx.lineTo(tx(vertices[i].x), ty(vertices[i].y));
      }
      if (vertices.length >= 3) ctx.closePath();
      ctx.fillStyle = 'rgba(79, 70, 229, 0.15)';
      ctx.fill();
      ctx.strokeStyle = '#4F46E5';
      ctx.lineWidth = 2;
      ctx.stroke();
    }

    // Draw vertices
    vertices.forEach((v, i) => {
      ctx.beginPath();
      ctx.arc(tx(v.x), ty(v.y), 5, 0, Math.PI * 2);
      ctx.fillStyle = '#4F46E5';
      ctx.fill();
      ctx.fillStyle = '#1e293b';
      ctx.font = '12px monospace';
      ctx.fillText(`(${v.x},${v.y})`, tx(v.x) + 8, ty(v.y) - 8);
    });
  }

  function calculate() {
    const text = document.getElementById('vertexInput').value;
    const vertices = parseVertices(text);
    if (vertices.length < 3) {
      document.getElementById('areaResult').textContent = '❌ 至少需要3个顶点才能计算面积';
      drawPolygon(vertices);
      return;
    }
    const area = shoelaceArea(vertices);
    const vertexNames = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P'];
    const names = vertices.map((v,i) => `${vertexNames[i]||'V'+(i+1)}(${v.x},${v.y})`).join(' → ');
    document.getElementById('areaResult').textContent = 
      `顶点序列: ${names}\n多边形面积: ${area.toFixed(4)} 平方单位\n顶点数: ${vertices.length}`;
    drawPolygon(vertices);
    showToast('面积计算完成');
  }

  document.getElementById('btnCalc').addEventListener('click', calculate);
  document.getElementById('btnClear').addEventListener('click', () => {
    document.getElementById('vertexInput').value = '';
    document.getElementById('areaResult').textContent = '输入顶点坐标后点击"计算面积"';
    const canvas = document.getElementById('polyCanvas');
    canvas.getContext('2d').clearRect(0, 0, canvas.width, canvas.height);
  });
  document.getElementById('btnExample').addEventListener('click', () => {
    document.getElementById('vertexInput').value = '0,0\n4,0\n5,2\n4,4\n0,4\n-1,2';
    calculate();
  });
})();