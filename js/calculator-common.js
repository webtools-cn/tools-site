// Free ToolBase - Calculator Common Utilities v1.0
// Shared by all calculator tools

function showToast(msg) {
    const t = document.getElementById('toast');
    if (!t) return;
    t.textContent = msg;
    t.classList.add('show');
    setTimeout(() => t.classList.remove('show'), 2000);
}

function copyResult() {
    const card = document.getElementById('result-card');
    if (!card || card.style.display === 'none') { showToast('请先计算'); return; }
    const items = card.querySelectorAll('.result-item');
    let text = '';
    items.forEach(item => {
        const label = item.querySelector('.result-label')?.textContent?.trim() || '';
        const value = item.querySelector('.result-value')?.textContent?.trim() || '';
        if (label && value) text += label + ': ' + value + '\n';
    });
    if (text) {
        navigator.clipboard.writeText(text.trim()).then(() => showToast('已复制到剪贴板')).catch(() => showToast('复制失败'));
    }
}

function resetForm() {
    document.querySelectorAll('#input-area input').forEach(el => {
        if (el.type === 'number' || el.type === 'text') {
            el.value = el.dataset.default || '';
        }
    });
    document.getElementById('result-card').style.display = 'none';
    document.getElementById('chart-container').style.display = 'none';
    if (window.chart) { window.chart.destroy(); window.chart = null; }
}

function formatNum(n, decimals) {
    if (decimals === undefined) decimals = 2;
    if (typeof n !== 'number' || isNaN(n)) return '0.00';
    return n.toLocaleString('en-US', { minimumFractionDigits: decimals, maximumFractionDigits: decimals });
}

function formatUSD(n) {
    if (typeof n !== 'number' || isNaN(n)) return '$0.00';
    return '$' + n.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

function drawBarChart(canvasId, labels, datasets, title) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;
    if (window.chart) window.chart.destroy();
    
    const ctx = canvas.getContext('2d');
    const w = canvas.parentElement.clientWidth - 40;
    const h = 220;
    canvas.width = w * 2;
    canvas.height = h * 2;
    canvas.style.width = w + 'px';
    canvas.style.height = h + 'px';
    ctx.scale(2, 2);
    
    const padding = { top: 30, right: 20, bottom: 50, left: 70 };
    const chartW = w - padding.left - padding.right;
    const chartH = h - padding.top - padding.bottom;
    
    // Find max value
    let maxVal = 0;
    datasets.forEach(ds => ds.data.forEach(v => { if (v > maxVal) maxVal = v; }));
    maxVal = Math.ceil(maxVal * 1.15);
    
    // Draw grid
    ctx.strokeStyle = 'rgba(148,163,184,0.15)';
    ctx.lineWidth = 0.5;
    const gridLines = 5;
    for (let i = 0; i <= gridLines; i++) {
        const y = padding.top + (chartH / gridLines) * i;
        ctx.beginPath();
        ctx.moveTo(padding.left, y);
        ctx.lineTo(w - padding.right, y);
        ctx.stroke();
        
        ctx.fillStyle = '#94a3b8';
        ctx.font = '11px sans-serif';
        ctx.textAlign = 'right';
        ctx.fillText('$' + formatNum(maxVal * (1 - i / gridLines), 0), padding.left - 8, y + 4);
    }
    
    // Draw bars
    const barWidth = chartW / labels.length / (datasets.length + 1);
    const barGap = barWidth * 0.3;
    
    datasets.forEach((ds, di) => {
        ds.data.forEach((val, i) => {
            const barH = (val / maxVal) * chartH;
            const x = padding.left + (chartW / labels.length) * i + barWidth * di + barWidth * 0.5;
            const y = padding.top + chartH - barH;
            
            ctx.fillStyle = ds.color || COLORS[di % COLORS.length];
            ctx.fillRect(x - barWidth / 2 + barGap / 2, y, barWidth - barGap, barH);
            
            // Value on top
            ctx.fillStyle = '#e2e8f0';
            ctx.font = 'bold 10px sans-serif';
            ctx.textAlign = 'center';
            ctx.fillText('$' + formatNum(val, 0), x, y - 4);
        });
    });
    
    // X-axis labels
    ctx.fillStyle = '#94a3b8';
    ctx.font = '11px sans-serif';
    ctx.textAlign = 'center';
    labels.forEach((label, i) => {
        const x = padding.left + (chartW / labels.length) * i + chartW / labels.length / 2;
        ctx.fillText(label, x, h - padding.bottom + 20);
    });
    
    // Legend
    if (datasets.length > 1) {
        let lx = padding.left;
        datasets.forEach((ds, i) => {
            ctx.fillStyle = ds.color || COLORS[i % COLORS.length];
            ctx.fillRect(lx, 8, 12, 12);
            ctx.fillStyle = '#94a3b8';
            ctx.font = '11px sans-serif';
            ctx.textAlign = 'left';
            ctx.fillText(ds.label, lx + 16, 18);
            lx += ctx.measureText(ds.label).width + 40;
        });
    }
}

function drawLineChart(canvasId, labels, datasets) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;
    if (window.chart) window.chart.destroy();
    
    const ctx = canvas.getContext('2d');
    const w = canvas.parentElement.clientWidth - 40;
    const h = 250;
    canvas.width = w * 2;
    canvas.height = h * 2;
    canvas.style.width = w + 'px';
    canvas.style.height = h + 'px';
    ctx.scale(2, 2);
    
    const padding = { top: 30, right: 20, bottom: 50, left: 70 };
    const chartW = w - padding.left - padding.right;
    const chartH = h - padding.top - padding.bottom;
    
    let maxVal = 0;
    datasets.forEach(ds => ds.data.forEach(v => { if (v > maxVal) maxVal = v; }));
    maxVal = Math.ceil(maxVal * 1.15);
    
    // Grid
    ctx.strokeStyle = 'rgba(148,163,184,0.15)';
    ctx.lineWidth = 0.5;
    const gridLines = 5;
    for (let i = 0; i <= gridLines; i++) {
        const y = padding.top + (chartH / gridLines) * i;
        ctx.beginPath();
        ctx.moveTo(padding.left, y);
        ctx.lineTo(w - padding.right, y);
        ctx.stroke();
        
        ctx.fillStyle = '#94a3b8';
        ctx.font = '11px sans-serif';
        ctx.textAlign = 'right';
        const val = maxVal * (1 - i / gridLines);
        ctx.fillText(val >= 1000 ? '$' + formatNum(val, 0) : '$' + formatNum(val, 2), padding.left - 8, y + 4);
    }
    
    // Lines
    datasets.forEach((ds, di) => {
        ctx.strokeStyle = ds.color || COLORS[di % COLORS.length];
        ctx.lineWidth = 2.5;
        ctx.beginPath();
        ds.data.forEach((val, i) => {
            const x = padding.left + (chartW / (ds.data.length - 1)) * i;
            const y = padding.top + chartH - (val / maxVal) * chartH;
            if (i === 0) ctx.moveTo(x, y);
            else ctx.lineTo(x, y);
        });
        ctx.stroke();
        
        // Dots
        ds.data.forEach((val, i) => {
            const x = padding.left + (chartW / (ds.data.length - 1)) * i;
            const y = padding.top + chartH - (val / maxVal) * chartH;
            ctx.fillStyle = ds.color || COLORS[di % COLORS.length];
            ctx.beginPath();
            ctx.arc(x, y, 4, 0, Math.PI * 2);
            ctx.fill();
        });
    });
    
    // X-axis
    ctx.fillStyle = '#94a3b8';
    ctx.font = '11px sans-serif';
    ctx.textAlign = 'center';
    const step = Math.max(1, Math.floor(labels.length / 12));
    labels.forEach((label, i) => {
        if (i % step === 0 || i === labels.length - 1) {
            const x = padding.left + (chartW / (labels.length - 1)) * i;
            ctx.fillText(label, x, h - padding.bottom + 20);
        }
    });
    
    // Legend
    let lx = padding.left;
    datasets.forEach((ds, i) => {
        ctx.fillStyle = ds.color || COLORS[i % COLORS.length];
        ctx.fillRect(lx, 8, 12, 12);
        ctx.fillStyle = '#94a3b8';
        ctx.font = '11px sans-serif';
        ctx.textAlign = 'left';
        ctx.fillText(ds.label, lx + 16, 18);
        lx += ctx.measureText(ds.label).width + 40;
    });
}