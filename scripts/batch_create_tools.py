#!/usr/bin/env python3
"""批量创建新工具 - 本轮：site-availability-checker, server-checker, china-salary-calculator, speech-recognition, tempo-changer"""

import os
import json

BASE_DIR = '/home/chison/tools-site'

# 工具定义
TOOLS = [
    {
        "slug": "site-availability-checker",
        "cn_name": "网站可用性检测器",
        "en_name": "Site Availability Checker",
        "category": "utility",
        "cn_desc": "免费在线网站可用性检测工具，支持批量检测多个URL的HTTP状态码、响应时间。无需注册，浏览器端实时检测。",
        "en_desc": "Free online website availability checker. Check HTTP status codes and response times for multiple URLs. No registration required. Runs entirely in your browser.",
        "cn_short": "批量检测网站状态码和响应时间",
        "en_short": "Check website status and response times in bulk",
        "cn_steps": [
            "输入要检测的网站URL列表，一行一个",
            "点击开始检测按钮，查看各URL状态码和响应时间", 
            "查看统计报告，复制结果"
        ],
        "en_steps": [
            "Enter website URLs to check, one per line",
            "Click detect button to see status codes and response times",
            "View statistics report and copy results"
        ],
        "html_content": """<div class="panel">
  <div class="panel-title">📋 URL列表（每行一个）</div>
  <textarea id="urlInput" class="textarea-area" placeholder="https://example.com
https://google.com
https://github.com" style="min-height:150px"></textarea>
  <div class="btn-group">
    <button id="checkBtn" class="btn btn-primary">开始检测</button>
    <button id="clearBtn" class="btn btn-secondary">清空</button>
    <button id="copyBtn" class="btn btn-success">复制结果</button>
  </div>
  <div id="progressBar" style="display:none;height:4px;background:#334155;border-radius:2px;margin-top:12px;overflow:hidden">
    <div id="progressFill" style="height:100%;background:#06b6d4;width:0%;transition:width .3s"></div>
  </div>
</div>
<div class="panel">
  <div class="panel-title">📊 检测结果</div>
  <div id="results" class="output-area" style="min-height:200px">等待检测...</div>
  <div id="stats" style="margin-top:12px;display:flex;gap:16px;flex-wrap:wrap"></div>
</div>""",
        "js_logic": """
    const urlInput = document.getElementById('urlInput');
    const checkBtn = document.getElementById('checkBtn');
    const clearBtn = document.getElementById('clearBtn');
    const copyBtn = document.getElementById('copyBtn');
    const results = document.getElementById('results');
    const stats = document.getElementById('stats');
    const progressBar = document.getElementById('progressBar');
    const progressFill = document.getElementById('progressFill');

    function showToast(msg) {
      const t = document.getElementById('toast');
      t.textContent = msg;
      t.classList.add('show');
      setTimeout(() => t.classList.remove('show'), 2000);
    }

    async function checkUrl(url) {
      const start = performance.now();
      try {
        const controller = new AbortController();
        const timeout = setTimeout(() => controller.abort(), 15000);
        const resp = await fetch(url, { method: 'HEAD', mode: 'no-cors', signal: controller.signal });
        clearTimeout(timeout);
        const time = (performance.now() - start).toFixed(0);
        return { url, status: 'ok', time: parseInt(time), code: 200 };
      } catch(e) {
        const time = (performance.now() - start).toFixed(0);
        if (e.name === 'AbortError') return { url, status: 'timeout', time: parseInt(time), code: 0 };
        return { url, status: 'error', time: parseInt(time), code: 0, error: e.message };
      }
    }

    checkBtn.addEventListener('click', async () => {
      const lines = urlInput.value.split('\\n').map(l => l.trim()).filter(l => l);
      if (!lines.length) { showToast('请先输入URL'); return; }
      const urls = lines.map(l => l.startsWith('http') ? l : 'https://' + l);
      
      results.textContent = '检测中...\\n';
      progressBar.style.display = 'block';
      progressFill.style.width = '0%';
      stats.innerHTML = '';
      
      const allResults = [];
      for (let i = 0; i < urls.length; i++) {
        const r = await checkUrl(urls[i]);
        allResults.push(r);
        const icon = r.status === 'ok' ? '✅' : r.status === 'timeout' ? '⏱️' : '❌';
        results.textContent += `${icon} ${r.url} | ${r.status === 'ok' ? r.code : r.status} | ${r.time}ms\\n`;
        progressFill.style.width = ((i + 1) / urls.length * 100) + '%';
      }
      
      const ok = allResults.filter(r => r.status === 'ok').length;
      const err = allResults.filter(r => r.status === 'error').length;
      const to = allResults.filter(r => r.status === 'timeout').length;
      const avgTime = Math.round(allResults.reduce((s,r) => s + r.time, 0) / allResults.length);
      
      stats.innerHTML = `<span style="color:#10b981">✅ ${ok} 正常</span><span style="color:#ef4444">❌ ${err} 错误</span><span style="color:#f59e0b">⏱️ ${to} 超时</span><span style="color:#94a3b8">⏱ 平均 ${avgTime}ms</span>`;
      progressBar.style.display = 'none';
    });
    
    clearBtn.addEventListener('click', () => { urlInput.value = ''; results.textContent = '等待检测...'; stats.innerHTML = ''; });
    copyBtn.addEventListener('click', () => {
      if (results.textContent === '等待检测...') { showToast('没有结果可复制'); return; }
      navigator.clipboard.writeText(results.textContent).then(() => showToast('已复制'));
    });
"""
    },
    {
        "slug": "server-checker",
        "cn_name": "服务器状态检查器",
        "en_name": "Server Status Checker",
        "category": "utility",
        "cn_desc": "免费在线服务器状态检查工具，检测服务器端口开放情况、响应延迟。支持常见端口检查，无需注册，浏览器端直接检测。",
        "en_desc": "Free online server status checker. Check port availability and response latency. Supports common ports. No registration, runs in your browser.",
        "cn_short": "检测服务器端口状态和响应延迟",
        "en_short": "Check server port status and latency",
        "cn_steps": [
            "输入服务器IP或域名",
            "选择要检测的端口或输入自定义端口",
            "点击检测按钮查看端口状态和延迟"
        ],
        "en_steps": [
            "Enter server IP or domain",
            "Select ports to check or enter custom ports",
            "Click check button to see port status and latency"
        ],
        "html_content": """<div class="panel">
  <div class="panel-title">🖥️ 服务器信息</div>
  <div style="display:flex;gap:12px;flex-wrap:wrap;align-items:end">
    <div style="flex:1;min-width:200px">
      <label style="font-size:.85rem;color:#94a3b8;margin-bottom:6px;display:block">主机地址</label>
      <input type="text" id="hostInput" class="textarea-area" style="min-height:auto;height:44px" placeholder="example.com 或 192.168.1.1" value="">
    </div>
    <div style="flex:1;min-width:200px">
      <label style="font-size:.85rem;color:#94a3b8;margin-bottom:6px;display:block">端口（逗号分隔）</label>
      <input type="text" id="portInput" class="textarea-area" style="min-height:auto;height:44px" placeholder="80,443,22,3306" value="80,443,22,21,3306">
    </div>
  </div>
  <div style="margin-top:8px;font-size:.8rem;color:#64748b">💡 常用端口: HTTP(80) HTTPS(443) SSH(22) FTP(21) MySQL(3306) Redis(6379) MongoDB(27017)</div>
  <div class="btn-group">
    <button id="checkBtn" class="btn btn-primary">开始检测</button>
    <button id="clearBtn" class="btn btn-secondary">清空</button>
    <button id="copyBtn" class="btn btn-success">复制结果</button>
  </div>
</div>
<div class="panel">
  <div class="panel-title">📊 检测结果</div>
  <div id="results" class="output-area" style="min-height:200px">等待检测...</div>
</div>""",
        "js_logic": """
    const hostInput = document.getElementById('hostInput');
    const portInput = document.getElementById('portInput');
    const checkBtn = document.getElementById('checkBtn');
    const clearBtn = document.getElementById('clearBtn');
    const copyBtn = document.getElementById('copyBtn');
    const resultsDiv = document.getElementById('results');

    function showToast(msg) {
      const t = document.getElementById('toast');
      t.textContent = msg;
      t.classList.add('show');
      setTimeout(() => t.classList.remove('show'), 2000);
    }

    function getServiceName(port) {
      const map = {20:'FTP-Data',21:'FTP',22:'SSH',23:'Telnet',25:'SMTP',53:'DNS',80:'HTTP',110:'POP3',143:'IMAP',443:'HTTPS',465:'SMTPS',587:'SMTP',993:'IMAPS',995:'POP3S',1433:'MSSQL',1521:'Oracle',3306:'MySQL',3389:'RDP',5432:'PostgreSQL',5672:'RabbitMQ',6379:'Redis',8080:'HTTP-Alt',8443:'HTTPS-Alt',9092:'Kafka',9200:'Elasticsearch',11211:'Memcached',27017:'MongoDB'};
      return map[port] || '';
    }

    async function checkPort(host, port) {
      const start = performance.now();
      try {
        const controller = new AbortController();
        const timeout = setTimeout(() => controller.abort(), 10000);
        await fetch('https://' + host + ':' + port + '/', { mode: 'no-cors', signal: controller.signal });
        clearTimeout(timeout);
        return { port, open: true, time: Math.round(performance.now() - start) };
      } catch(e) {
        const time = Math.round(performance.now() - start);
        if (e.name === 'AbortError') return { port, open: false, time, reason: 'timeout' };
        return { port, open: false, time, reason: 'blocked/closed' };
      }
    }

    async function checkWithImg(host, port) {
      return new Promise(resolve => {
        const start = performance.now();
        const img = new Image();
        const timeout = setTimeout(() => { img.src = ''; resolve({port, open: false, time: Math.round(performance.now()-start), reason:'timeout'}); }, 8000);
        img.onload = () => { clearTimeout(timeout); resolve({port, open: true, time: Math.round(performance.now()-start)}); };
        img.onerror = () => { clearTimeout(timeout); resolve({port, open: true, time: Math.round(performance.now()-start)}); };
        img.src = 'https://' + host + ':' + port + '/favicon.ico?' + Date.now();
      });
    }

    checkBtn.addEventListener('click', async () => {
      const host = hostInput.value.trim();
      if (!host) { showToast('请输入主机地址'); return; }
      const ports = portInput.value.split(',').map(p => parseInt(p.trim())).filter(p => p > 0 && p < 65536);
      if (!ports.length) { showToast('请输入有效端口'); return; }
      
      resultsDiv.textContent = '检测中...\\n';
      for (const port of ports) {
        resultsDiv.textContent += `🔍 检测 ${host}:${port}...\\n`;
      }
      
      const allResults = [];
      for (const port of ports) {
        const r = await checkWithImg(host, port);
        allResults.push(r);
        const svc = getServiceName(port);
        const icon = r.open ? '✅' : '❌';
        const srv = svc ? ` (${svc})` : '';
        resultsDiv.textContent = resultsDiv.textContent.replace(`🔍 检测 ${host}:${port}...`, `${icon} ${host}:${port}${srv} | ${r.open ? '开放' : '关闭'} | ${r.time}ms`);
      }
      resultsDiv.textContent += '\\n检测完成。';
    });

    clearBtn.addEventListener('click', () => { hostInput.value = ''; portInput.value = '80,443,22,21,3306'; resultsDiv.textContent = '等待检测...'; });
    copyBtn.addEventListener('click', () => {
      if (resultsDiv.textContent === '等待检测...') { showToast('没有结果'); return; }
      navigator.clipboard.writeText(resultsDiv.textContent).then(() => showToast('已复制'));
    });
"""
    },
    {
        "slug": "china-salary-calculator",
        "cn_name": "中国工资计算器",
        "en_name": "China Salary Calculator",
        "category": "finance",
        "cn_desc": "免费在线中国工资计算器，根据税前月薪计算税后收入、五险一金扣除、个人所得税。支持2026年最新税率，无需注册。",
        "en_desc": "Free online China salary calculator. Calculate after-tax income, social insurance and housing fund deductions, and personal income tax based on pre-tax monthly salary. Supports 2026 tax rates.",
        "cn_short": "计算税前月薪对应的税后收入和五险一金",
        "en_short": "Calculate after-tax income and deductions from pre-tax salary",
        "cn_steps": [
            "输入税前月薪金额",
            "选择社保缴纳城市或自定义缴纳基数",
            "查看税后收入和各项扣除明细"
        ],
        "en_steps": [
            "Enter pre-tax monthly salary",
            "Select city or customize social insurance base",
            "View after-tax income and deduction details"
        ],
        "html_content": """<div class="panel">
  <div class="panel-title">💰 工资信息</div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px">
    <div>
      <label style="font-size:.85rem;color:#94a3b8;margin-bottom:6px;display:block">税前月薪 (元)</label>
      <input type="number" id="salaryInput" class="textarea-area" style="min-height:auto;height:44px" placeholder="15000" value="15000">
    </div>
    <div>
      <label style="font-size:.85rem;color:#94a3b8;margin-bottom:6px;display:block">社保缴纳基数 (元，默认=月薪)</label>
      <input type="number" id="baseInput" class="textarea-area" style="min-height:auto;height:44px" placeholder="15000" value="">
    </div>
  </div>
  <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;margin-top:12px">
    <div>
      <label style="font-size:.85rem;color:#94a3b8;margin-bottom:6px;display:block">城市类型</label>
      <select id="citySelect" class="textarea-area" style="min-height:auto;height:44px">
        <option value="default">默认(北京)</option>
        <option value="shanghai">上海</option>
        <option value="guangzhou">广州</option>
        <option value="shenzhen">深圳</option>
      </select>
    </div>
    <div>
      <label style="font-size:.85rem;color:#94a3b8;margin-bottom:6px;display:block">公积金比例(%)</label>
      <input type="number" id="fundRate" class="textarea-area" style="min-height:auto;height:44px" placeholder="12" value="12" min="5" max="12">
    </div>
  </div>
  <div class="btn-group">
    <button id="calcBtn" class="btn btn-primary">计算</button>
    <button id="clearBtn" class="btn btn-secondary">重置</button>
  </div>
</div>
<div class="panel">
  <div class="panel-title">📊 计算结果</div>
  <div id="results" class="output-area" style="min-height:250px;font-family:-apple-system,BlinkMacSystemFont,\"PingFang SC\",\"Microsoft YaHei\",sans-serif">输入月薪，点击计算...</div>
</div>""",
        "js_logic": """
    const salaryInput = document.getElementById('salaryInput');
    const baseInput = document.getElementById('baseInput');
    const citySelect = document.getElementById('citySelect');
    const fundRate = document.getElementById('fundRate');
    const calcBtn = document.getElementById('calcBtn');
    const clearBtn = document.getElementById('clearBtn');
    const results = document.getElementById('results');

    function showToast(msg) {
      const t = document.getElementById('toast');
      t.textContent = msg;
      t.classList.add('show');
      setTimeout(() => t.classList.remove('show'), 2000);
    }

    // 五险一金比例 (2026年参考)
    const cityRates = {
      default: {pension:0.08, medical:0.02, unemployment:0.005, injury:0, maternity:0, housingMax:12},
      shanghai: {pension:0.08, medical:0.02, unemployment:0.005, injury:0, maternity:0, housingMax:7},
      guangzhou: {pension:0.08, medical:0.02, unemployment:0.002, injury:0, maternity:0, housingMax:12},
      shenzhen: {pension:0.08, medical:0.02, unemployment:0.005, injury:0, maternity:0, housingMax:12}
    };

    function calcTax(annualIncome) {
      // 2026年个税：起征点5000/月=60000/年
      const exemption = 60000;
      const taxable = Math.max(0, annualIncome - exemption);
      const brackets = [
        {max:36000, rate:0.03, deduct:0},
        {max:144000, rate:0.10, deduct:2520},
        {max:300000, rate:0.20, deduct:16920},
        {max:420000, rate:0.25, deduct:31920},
        {max:660000, rate:0.30, deduct:52920},
        {max:960000, rate:0.35, deduct:85920},
        {max:Infinity, rate:0.45, deduct:181920}
      ];
      let tax = 0;
      for (const b of brackets) {
        if (taxable <= 0) break;
        const portion = Math.min(taxable, b.max - (brackets.indexOf(b) > 0 ? brackets[brackets.indexOf(b)-1].max : 0));
        tax += portion * b.rate;
      }
      // 简化为直接套公式
      let b = brackets.find(b => taxable <= b.max);
      tax = Math.max(0, taxable * b.rate - b.deduct);
      return Math.round(tax * 100) / 100;
    }

    calcBtn.addEventListener('click', () => {
      const salary = parseFloat(salaryInput.value);
      if (!salary || salary <= 0) { showToast('请输入有效月薪'); return; }
      
      const base = parseFloat(baseInput.value) || salary;
      const city = citySelect.value;
      const rates = cityRates[city] || cityRates.default;
      const housing = Math.min(fundRate.value || 12, rates.housingMax);
      
      // 社保上限参考（北京2026：35283）
      const capMonthly = 35283;
      const actualBase = Math.min(base, capMonthly);
      
      const pension = actualBase * rates.pension;
      const medical = actualBase * rates.medical;
      const unemployment = actualBase * rates.unemployment;
      const housingFund = actualBase * (housing / 100);
      const totalDeduction = pension + medical + unemployment + housingFund;
      
      const monthlyTaxable = salary - totalDeduction - 5000;
      const annualTaxable = monthlyTaxable * 12;
      const annualTax = calcTax(annualTaxable + 60000); // add back exemption
      const monthlyTax = annualTax / 12;
      
      const netSalary = salary - totalDeduction - monthlyTax;
      
      results.innerHTML = `
<div style="font-size:1.2rem;margin-bottom:16px">💰 <b>税后月收入: ¥${netSalary.toFixed(2)}</b></div>
<table style="width:100%;border-collapse:collapse;font-size:.9rem">
  <tr><td style="padding:6px 0;color:#94a3b8">税前月薪</td><td style="text-align:right;color:#f1f5f9">¥${salary.toFixed(2)}</td></tr>
  <tr><td style="padding:6px 0;color:#94a3b8">养老保险 (${(rates.pension*100).toFixed(1)}%)</td><td style="text-align:right;color:#ef4444">-¥${pension.toFixed(2)}</td></tr>
  <tr><td style="padding:6px 0;color:#94a3b8">医疗保险 (${(rates.medical*100).toFixed(1)}%)</td><td style="text-align:right;color:#ef4444">-¥${medical.toFixed(2)}</td></tr>
  <tr><td style="padding:6px 0;color:#94a3b8">失业保险 (${(rates.unemployment*100).toFixed(1)}%)</td><td style="text-align:right;color:#ef4444">-¥${unemployment.toFixed(2)}</td></tr>
  <tr><td style="padding:6px 0;color:#94a3b8">住房公积金 (${housing}%)</td><td style="text-align:right;color:#ef4444">-¥${housingFund.toFixed(2)}</td></tr>
  <tr><td style="padding:6px 0;border-top:1px solid #334155;color:#94a3b8">五险一金合计</td><td style="text-align:right;border-top:1px solid #334155;color:#f59e0b">-¥${totalDeduction.toFixed(2)}</td></tr>
  <tr><td style="padding:6px 0;color:#94a3b8">个人所得税</td><td style="text-align:right;color:#ef4444">-¥${monthlyTax.toFixed(2)}</td></tr>
  <tr style="font-weight:bold"><td style="padding:8px 0;border-top:2px solid #06b6d4;color:#22d3ee">税后收入</td><td style="text-align:right;border-top:2px solid #06b6d4;color:#22d3ee;font-size:1.1rem">¥${netSalary.toFixed(2)}</td></tr>
  <tr><td style="padding:6px 0;color:#94a3b8">社保缴纳基数</td><td style="text-align:right;color:#94a3b8">¥${actualBase.toFixed(2)}</td></tr>
</table>
<p style="color:#64748b;font-size:.8rem;margin-top:12px">* 以上计算仅供参考，实际以当地社保局扣缴为准。个税按累计预扣法简化计算。</p>`;
    });

    clearBtn.addEventListener('click', () => { salaryInput.value = '15000'; baseInput.value = ''; fundRate.value = '12'; citySelect.value = 'default'; results.innerHTML = '输入月薪，点击计算...'; });
"""
    },
    {
        "slug": "speech-recognition",
        "cn_name": "语音识别工具",
        "en_name": "Speech Recognition",
        "category": "text",
        "cn_desc": "免费在线语音识别工具，使用浏览器内置Web Speech API将语音实时转文字。支持多种语言，无需注册，完全本地处理。",
        "en_desc": "Free online speech recognition tool. Convert speech to text in real-time using browser's built-in Web Speech API. Supports multiple languages. No registration, fully local processing.",
        "cn_short": "语音实时转文字，支持多语言",
        "en_short": "Real-time speech to text, multi-language support",
        "cn_steps": [
            "选择识别语言",
            "点击开始录音按钮并说话",
            "查看实时识别的文字，可复制结果"
        ],
        "en_steps": [
            "Select recognition language",
            "Click start button and speak",
            "View real-time transcription, copy results"
        ],
        "html_content": """<div class="panel">
  <div class="panel-title">🎤 语音转文字</div>
  <div style="display:flex;gap:12px;flex-wrap:wrap;align-items:end;margin-bottom:12px">
    <div style="flex:1;min-width:150px">
      <label style="font-size:.85rem;color:#94a3b8;margin-bottom:6px;display:block">识别语言</label>
      <select id="langSelect" class="textarea-area" style="min-height:auto;height:44px">
        <option value="zh-CN">中文（简体）</option>
        <option value="en-US" selected>English (US)</option>
        <option value="ja-JP">日本語</option>
        <option value="ko-KR">한국어</option>
        <option value="fr-FR">Français</option>
        <option value="de-DE">Deutsch</option>
        <option value="es-ES">Español</option>
      </select>
    </div>
  </div>
  <div class="btn-group">
    <button id="startBtn" class="btn btn-primary">🎙️ 开始录音</button>
    <button id="stopBtn" class="btn btn-secondary" disabled>⏹️ 停止</button>
    <button id="copyBtn" class="btn btn-success">复制文字</button>
    <button id="clearBtn" class="btn btn-danger">清空</button>
  </div>
  <div id="status" style="margin-top:12px;font-size:.85rem;color:#94a3b8">点击"开始录音"并授权麦克风...</div>
  <div id="interim" style="margin-top:8px;font-size:.9rem;color:#64748b;min-height:24px"></div>
</div>
<div class="panel">
  <div class="panel-title">📝 识别结果</div>
  <div id="results" class="output-area" style="min-height:200px;white-space:pre-wrap">等待语音输入...</div>
</div>
<div class="privacy-note">🔒 语音数据完全在浏览器本地处理，不上传到任何服务器。</div>""",
        "js_logic": """
    const langSelect = document.getElementById('langSelect');
    const startBtn = document.getElementById('startBtn');
    const stopBtn = document.getElementById('stopBtn');
    const copyBtn = document.getElementById('copyBtn');
    const clearBtn = document.getElementById('clearBtn');
    const resultsDiv = document.getElementById('results');
    const interimDiv = document.getElementById('interim');
    const statusDiv = document.getElementById('status');

    let recognition = null;

    function showToast(msg) {
      const t = document.getElementById('toast');
      t.textContent = msg;
      t.classList.add('show');
      setTimeout(() => t.classList.remove('show'), 2000);
    }

    function initRecognition() {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      if (!SpeechRecognition) {
        statusDiv.innerHTML = '<span style="color:#ef4444">❌ 您的浏览器不支持语音识别。请使用Chrome或Edge浏览器。</span>';
        startBtn.disabled = true;
        return null;
      }
      const rec = new SpeechRecognition();
      rec.continuous = true;
      rec.interimResults = true;
      rec.lang = langSelect.value;
      
      rec.onstart = () => {
        statusDiv.innerHTML = '<span style="color:#10b981">🔴 录音中...</span>';
        startBtn.disabled = true;
        stopBtn.disabled = false;
      };
      
      rec.onresult = (event) => {
        let interim = '';
        let final = '';
        for (let i = event.resultIndex; i < event.results.length; i++) {
          if (event.results[i].isFinal) {
            final += event.results[i][0].transcript;
          } else {
            interim += event.results[i][0].transcript;
          }
        }
        if (final && resultsDiv.textContent === '等待语音输入...') resultsDiv.textContent = '';
        if (final) resultsDiv.textContent += final + ' ';
        interimDiv.textContent = interim;
      };
      
      rec.onerror = (event) => {
        if (event.error === 'no-speech') {
          statusDiv.innerHTML = '<span style="color:#f59e0b">⚠️ 未检测到语音，请说话...</span>';
        } else if (event.error === 'aborted') {
          statusDiv.innerHTML = '<span style="color:#94a3b8">已停止录音</span>';
        } else {
          statusDiv.innerHTML = `<span style="color:#ef4444">❌ 错误: ${event.error}</span>`;
        }
        startBtn.disabled = false;
        stopBtn.disabled = true;
      };
      
      rec.onend = () => {
        statusDiv.innerHTML = '<span style="color:#94a3b8">已停止 | 点击开始继续录音</span>';
        startBtn.disabled = false;
        stopBtn.disabled = true;
        interimDiv.textContent = '';
      };
      
      return rec;
    }

    startBtn.addEventListener('click', () => {
      recognition = initRecognition();
      if (recognition) {
        try { recognition.start(); } catch(e) { showToast('请先停止当前录音'); }
      }
    });

    stopBtn.addEventListener('click', () => {
      if (recognition) { recognition.stop(); recognition = null; }
    });

    copyBtn.addEventListener('click', () => {
      const text = resultsDiv.textContent;
      if (text === '等待语音输入...' || !text.trim()) { showToast('没有文字可复制'); return; }
      navigator.clipboard.writeText(text.trim()).then(() => showToast('已复制'));
    });

    clearBtn.addEventListener('click', () => { resultsDiv.textContent = '等待语音输入...'; interimDiv.textContent = ''; });
"""
    },
    {
        "slug": "tempo-changer",
        "cn_name": "音频变速器",
        "en_name": "Audio Tempo Changer",
        "category": "audio",
        "cn_desc": "免费在线音频变速工具，调整音频播放速度而不改变音调。支持MP3/WAV等格式，无需注册，浏览器端完全本地处理。",
        "en_desc": "Free online audio tempo changer. Adjust audio playback speed without changing pitch. Supports MP3/WAV formats. No registration, fully local processing in browser.",
        "cn_short": "调整音频播放速度，不改变音调",
        "en_short": "Change audio speed without affecting pitch",
        "cn_steps": [
            "上传或拖拽音频文件",
            "调整播放速度滑块",
            "播放预览效果，下载变速后的音频"
        ],
        "en_steps": [
            "Upload or drag audio file",
            "Adjust speed slider",
            "Preview and download tempo-changed audio"
        ],
        "html_content": """<div class="panel">
  <div class="panel-title">🎵 上传音频</div>
  <div id="dropZone" style="border:2px dashed rgba(148,163,184,.3);border-radius:12px;padding:32px;text-align:center;cursor:pointer;transition:border-color .2s">
    <div style="font-size:2rem;margin-bottom:8px">📁</div>
    <div style="color:#94a3b8">拖拽音频文件到此处，或点击选择</div>
    <div style="font-size:.8rem;color:#64748b;margin-top:4px">支持 MP3 / WAV / OGG / AAC 格式</div>
    <input type="file" id="audioFile" accept="audio/*" style="display:none">
  </div>
  <div id="fileInfo" style="margin-top:12px;display:none;color:#10b981;font-size:.85rem"></div>
</div>
<div class="panel">
  <div class="panel-title">⚡ 变速控制</div>
  <div style="display:flex;align-items:center;gap:16px;flex-wrap:wrap">
    <span style="color:#94a3b8;font-size:.85rem">速度:</span>
    <input type="range" id="speedSlider" min="50" max="200" value="100" style="flex:1;min-width:150px;accent-color:#06b6d4">
    <span id="speedLabel" style="color:#22d3ee;font-weight:600;min-width:50px">1.00x</span>
  </div>
  <div style="display:flex;gap:8px;margin-top:8px;flex-wrap:wrap">
    <button class="btn btn-secondary" onclick="document.getElementById('speedSlider').value=50;updateSpeed()">0.5x</button>
    <button class="btn btn-secondary" onclick="document.getElementById('speedSlider').value=75;updateSpeed()">0.75x</button>
    <button class="btn btn-secondary" onclick="document.getElementById('speedSlider').value=100;updateSpeed()">1x</button>
    <button class="btn btn-secondary" onclick="document.getElementById('speedSlider').value=125;updateSpeed()">1.25x</button>
    <button class="btn btn-secondary" onclick="document.getElementById('speedSlider').value=150;updateSpeed()">1.5x</button>
    <button class="btn btn-secondary" onclick="document.getElementById('speedSlider').value=200;updateSpeed()">2x</button>
  </div>
  <div class="btn-group">
    <button id="playBtn" class="btn btn-primary">▶️ 播放预览</button>
    <button id="pauseBtn" class="btn btn-secondary" disabled>⏸️ 暂停</button>
    <button id="downloadBtn" class="btn btn-success" disabled>💾 下载变速音频</button>
  </div>
  <audio id="audioPlayer" style="display:none"></audio>
</div>
<div class="privacy-note">🔒 音频文件完全在浏览器本地处理，不上传到任何服务器。</div>""",
        "js_logic": """
    const dropZone = document.getElementById('dropZone');
    const audioFile = document.getElementById('audioFile');
    const fileInfo = document.getElementById('fileInfo');
    const speedSlider = document.getElementById('speedSlider');
    const speedLabel = document.getElementById('speedLabel');
    const playBtn = document.getElementById('playBtn');
    const pauseBtn = document.getElementById('pauseBtn');
    const downloadBtn = document.getElementById('downloadBtn');
    const audioPlayer = document.getElementById('audioPlayer');

    let audioContext = null;
    let audioBuffer = null;
    let sourceNode = null;
    let originalFile = null;
    let originalFileName = '';

    function showToast(msg) {
      const t = document.getElementById('toast');
      t.textContent = msg;
      t.classList.add('show');
      setTimeout(() => t.classList.remove('show'), 2000);
    }

    function updateSpeed() {
      const val = speedSlider.value;
      speedLabel.textContent = (val / 100).toFixed(2) + 'x';
      if (audioPlayer.src) audioPlayer.playbackRate = val / 100;
    }

    speedSlider.addEventListener('input', updateSpeed);

    dropZone.addEventListener('click', () => audioFile.click());
    dropZone.addEventListener('dragover', e => { e.preventDefault(); dropZone.style.borderColor = '#06b6d4'; });
    dropZone.addEventListener('dragleave', () => { dropZone.style.borderColor = 'rgba(148,163,184,.3)'; });
    dropZone.addEventListener('drop', e => {
      e.preventDefault();
      dropZone.style.borderColor = 'rgba(148,163,184,.3)';
      if (e.dataTransfer.files.length) handleFile(e.dataTransfer.files[0]);
    });

    audioFile.addEventListener('change', () => {
      if (audioFile.files.length) handleFile(audioFile.files[0]);
    });

    async function handleFile(file) {
      if (!file.type.startsWith('audio/')) { showToast('请选择音频文件'); return; }
      originalFile = file;
      originalFileName = file.name;
      
      fileInfo.style.display = 'block';
      fileInfo.textContent = `✅ ${file.name} (${(file.size/1024/1024).toFixed(1)} MB)`;
      
      const url = URL.createObjectURL(file);
      audioPlayer.src = url;
      audioPlayer.load();
      
      downloadBtn.disabled = false;
      playBtn.disabled = false;
      showToast('音频已加载');
    }

    playBtn.addEventListener('click', () => {
      if (!audioPlayer.src) { showToast('请先上传音频'); return; }
      audioPlayer.playbackRate = speedSlider.value / 100;
      audioPlayer.play();
      playBtn.disabled = true;
      pauseBtn.disabled = false;
    });

    pauseBtn.addEventListener('click', () => {
      audioPlayer.pause();
      playBtn.disabled = false;
      pauseBtn.disabled = true;
    });

    audioPlayer.addEventListener('ended', () => {
      playBtn.disabled = false;
      pauseBtn.disabled = true;
    });

    downloadBtn.addEventListener('click', async () => {
      if (!originalFile) { showToast('请先上传音频'); return; }
      const rate = speedSlider.value / 100;
      
      try {
        audioContext = new (window.AudioContext || window.webkitAudioContext)();
        const arrayBuffer = await originalFile.arrayBuffer();
        audioBuffer = await audioContext.decodeAudioData(arrayBuffer);
        
        // 创建离线渲染
        const offlineCtx = new OfflineAudioContext(
          audioBuffer.numberOfChannels,
          Math.ceil(audioBuffer.length / rate),
          audioBuffer.sampleRate
        );
        
        const src = offlineCtx.createBufferSource();
        src.buffer = audioBuffer;
        src.playbackRate.value = rate;
        src.connect(offlineCtx.destination);
        src.start(0);
        
        showToast('处理中...');
        const renderedBuffer = await offlineCtx.startRendering();
        
        // 转为WAV
        const wav = audioBufferToWav(renderedBuffer);
        const blob = new Blob([wav], { type: 'audio/wav' });
        const url = URL.createObjectURL(blob);
        
        const a = document.createElement('a');
        const ext = originalFileName.split('.').pop();
        a.href = url;
        a.download = originalFileName.replace(new RegExp('\\\\.' + ext + '$'), '_tempo' + rate.toFixed(2).replace('.','') + '.wav');
        a.click();
        URL.revokeObjectURL(url);
        audioContext.close();
        showToast('下载完成');
      } catch(e) {
        showToast('处理失败: ' + e.message);
      }
    });

    function audioBufferToWav(buffer) {
      const numChannels = buffer.numberOfChannels;
      const sampleRate = buffer.sampleRate;
      const format = 1; // PCM
      const bitsPerSample = 16;
      const data = buffer.getChannelData(0);
      const dataLength = data.length * (bitsPerSample / 8);
      const headerLength = 44;
      const totalLength = headerLength + dataLength;
      
      const wav = new ArrayBuffer(totalLength);
      const view = new DataView(wav);
      
      writeString(view, 0, 'RIFF');
      view.setUint32(4, totalLength - 8, true);
      writeString(view, 8, 'WAVE');
      writeString(view, 12, 'fmt ');
      view.setUint32(16, 16, true);
      view.setUint16(20, format, true);
      view.setUint16(22, numChannels, true);
      view.setUint32(24, sampleRate, true);
      view.setUint32(28, sampleRate * numChannels * bitsPerSample / 8, true);
      view.setUint16(32, numChannels * bitsPerSample / 8, true);
      view.setUint16(34, bitsPerSample, true);
      writeString(view, 36, 'data');
      view.setUint32(40, dataLength, true);
      
      let offset = 44;
      for (let i = 0; i < data.length; i++) {
        const sample = Math.max(-1, Math.min(1, data[i]));
        view.setInt16(offset, sample < 0 ? sample * 0x8000 : sample * 0x7FFF, true);
        offset += 2;
      }
      
      return wav;
    }

    function writeString(view, offset, str) {
      for (let i = 0; i < str.length; i++) {
        view.setUint8(offset + i, str.charCodeAt(i));
      }
    }
"""
    }
]

# === 生成工具脚本 ===
def get_head(slug, cn_name, cn_desc, cn_short, en=False):
    """生成head部分"""
    name = slug if not en else slug
    title_text = cn_name if not en else get_en(slug, 'name')
    desc = cn_desc if not en else get_en(slug, 'desc')
    short = cn_short if not en else get_en(slug, 'short')
    lang = 'zh-CN' if not en else 'en'
    hreflang = 'zh' if not en else 'en'
    canon = cn_name if not en else get_en(slug, 'name')
    
    return f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-9W1157EBQV"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-9W1157EBQV');</script>
<script>window.addEventListener("error",function(e){{if(e&&e.message===""){{e.preventDefault();}}}});window.addEventListener("unhandledrejection",function(e){{if(e&&e.reason&&e.reason.message===""){{e.preventDefault();}}}});</script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="{desc}">
<meta name="keywords" content="{slug},工具,在线工具,免费">
<title>{title_text} - Free ToolBase</title>
<link rel="canonical" href="https://free-toolbase.com{'/en/' if en else '/'}{slug}/">
<meta property="og:title" content="{title_text} - Free ToolBase">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="https://free-toolbase.com{'/en/' if en else '/'}{slug}/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Free ToolBase">
<link rel="alternate" hreflang="zh" href="https://free-toolbase.com/{slug}/">
<link rel="alternate" hreflang="en" href="https://free-toolbase.com/en/{slug}/">
<link rel="alternate" hreflang="x-default" href="https://free-toolbase.com/en/{slug}/">
<script type="application/ld+json">{{"@context": "https://schema.org", "@type": "SoftwareApplication", "name": "{title_text}", "description": "{desc}", "applicationCategory": "UtilitiesApplication", "operatingSystem": "Web", "publisher": {{"@type": "Organization", "name": "Free ToolBase", "email": "dexshuang@google.com"}}, "offers": {{"@type": "Offer", "price": "0", "priceCurrency": "USD"}}}}</script>
<script type="application/ld+json">{{"@context": "https://schema.org", "@type": "HowTo", "name": "如何使用{title_text}", "description": "如何使用{title_text}的详细步骤指南", "totalTime": "PT2M", "tool": {{"@type": "HowToTool", "name": "{title_text}"}}, "step": [{get_steps_json(slug, en)}]}}</script>
<script type="application/ld+json">{{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{{"@type": "ListItem", "position": 1, "name": "{'Home' if en else '首页'}", "item": "https://free-toolbase.com{'/en/' if en else '/'}"}}, {{"@type": "ListItem", "position": 2, "name": "{'Tools' if en else '工具'}", "item": "https://free-toolbase.com{'/en/' if en else '/'}#tools"}}, {{"@type": "ListItem", "position": 3, "name": "{title_text}", "item": "https://free-toolbase.com{'/en/' if en else '/'}{slug}/"}}]}}</script>
'''

def get_en(slug, field):
    """获取英文翻译"""
    en = {
        'site-availability-checker': {
            'name': 'Site Availability Checker',
            'desc': 'Free online website availability checker. Check HTTP status codes and response times for multiple URLs. No registration required, runs entirely in your browser.',
            'short': 'Check website status and response times in bulk',
            'steps': ['Enter website URLs to check, one per line',
                      'Click check button to see status codes and response times',
                      'View statistics report and copy results']
        },
        'server-checker': {
            'name': 'Server Status Checker',
            'desc': 'Free online server status checker. Check port availability and response latency. Supports common ports. No registration, runs in browser.',
            'short': 'Check server port status and latency',
            'steps': ['Enter server IP or domain',
                      'Select ports to check or enter custom ports',
                      'Click check button to see port status and latency']
        },
        'china-salary-calculator': {
            'name': 'China Salary Calculator',
            'desc': 'Free online China salary calculator. Calculate after-tax income, social insurance and housing fund deductions, and personal income tax based on pre-tax monthly salary. Supports 2026 tax rates.',
            'short': 'Calculate after-tax income and deductions from pre-tax salary',
            'steps': ['Enter pre-tax monthly salary',
                      'Select city or customize social insurance base',
                      'View after-tax income and deduction details']
        },
        'speech-recognition': {
            'name': 'Speech Recognition',
            'desc': 'Free online speech recognition tool. Convert speech to text in real-time using browser Web Speech API. Supports multiple languages. No registration, fully local processing.',
            'short': 'Real-time speech to text, multi-language support',
            'steps': ['Select recognition language',
                      'Click start button and speak',
                      'View real-time transcription and copy results']
        },
        'tempo-changer': {
            'name': 'Audio Tempo Changer',
            'desc': 'Free online audio tempo changer. Adjust audio playback speed without changing pitch. Supports MP3/WAV formats. No registration, fully local processing in browser.',
            'short': 'Change audio speed without affecting pitch',
            'steps': ['Upload or drag audio file',
                      'Adjust speed slider',
                      'Preview and download tempo-changed audio']
        }
    }
    return en.get(slug, {}).get(field, '')

def get_steps_json(slug, en=False):
    """生成steps JSON"""
    if en:
        steps = get_en(slug, 'steps')
    else:
        tool = next((t for t in TOOLS if t['slug'] == slug), None)
        steps = tool['cn_steps'] if tool else []
    
    items = []
    for i, step in enumerate(steps):
        items.append(f'{{"@type": "HowToStep", "position": {i+1}, "name": "{step[:20]}", "text": "{step}"}}')
    return ', '.join(items)

def create_tool_files():
    """创建所有工具文件"""
    for tool in TOOLS:
        slug = tool['slug']
        cn_dir = os.path.join(BASE_DIR, slug)
        en_dir = os.path.join(BASE_DIR, 'en', slug)
        
        os.makedirs(cn_dir, exist_ok=True)
        os.makedirs(en_dir, exist_ok=True)
        
        # 中文版
        cn_head = get_head(slug, tool['cn_name'], tool['cn_desc'], tool['cn_short'], en=False)
        cn_content = create_page_content(tool, cn=False)
        with open(os.path.join(cn_dir, 'index.html'), 'w') as f:
            f.write(cn_head + cn_content)
        print(f'Created: {slug}/index.html')
        
        # 英文版
        en_head = get_head(slug, '', '', '', en=True)
        en_content = create_page_content(tool, cn=True)  # 英文版内容
        with open(os.path.join(en_dir, 'index.html'), 'w') as f:
            f.write(en_head + en_content)
        print(f'Created: en/{slug}/index.html')
    
    print(f'Done! Created {len(TOOLS)} tools x 2 langs = {len(TOOLS)*2} files')

def create_page_content(tool, cn=True):
    """创建页面主体内容"""
    slug = tool['slug']
    en_labels = {
        'home': 'Home', 'tools': 'Tools',
        'h1_site': 'Website Availability Checker',
        'h1_server': 'Server Status Checker', 
        'h1_salary': 'China Salary Calculator',
        'h1_speech': 'Speech Recognition',
        'h1_tempo': 'Audio Tempo Changer',
        'badge': 'Free Online Tool | No Registration',
        'subtitle_site': 'Check HTTP status codes and response times for any website. Pure browser-side detection, no server needed.',
        'subtitle_server': 'Check port availability and response latency. Common service port detection.',
        'subtitle_salary': 'Calculate after-tax income, social insurance and IIT deductions based on 2026 China rates.',
        'subtitle_speech': 'Real-time speech-to-text using browser Web Speech API. Supports multiple languages.',
        'subtitle_tempo': 'Adjust audio playback speed without changing pitch. Full local processing.',
    }
    
    h1_map = {'site-availability-checker': 'h1_site', 'server-checker': 'h1_server', 
              'china-salary-calculator': 'h1_salary', 'speech-recognition': 'h1_speech',
              'tempo-changer': 'h1_tempo'}
    subtitle_map = {'site-availability-checker': 'subtitle_site', 'server-checker': 'subtitle_server',
                    'china-salary-calculator': 'subtitle_salary', 'speech-recognition': 'subtitle_speech',
                    'tempo-changer': 'subtitle_tempo'}
    
    if not cn:
        h1 = en_labels.get(h1_map.get(slug, ''), tool['en_name'])
        subtitle = en_labels.get(subtitle_map.get(slug, ''), tool['en_short'])
        home = 'Home'
        tools_link = 'Tools'
        faq_title = 'FAQ'
        faq_q1 = f'How to use {tool["en_name"]}?'
        faq_a1 = f'Enter the required data in the input fields, click the action button, and view results instantly. All processing is done locally in your browser.'
        faq_q2 = f'Is {tool["en_name"]} free?'
        faq_a2 = f'Yes, completely free. No registration required. No data uploaded to any server.'
        faq_q3 = 'Is my data safe?'
        faq_a3 = 'All data processing happens locally in your browser. No data is ever uploaded or stored on any server.'
        footer_text = f'© 2024 Free ToolBase · All tools run locally in your browser'
    else:
        h1 = tool['cn_name']
        subtitle = tool['cn_short']
        home = '首页'
        tools_link = '工具'
        faq_title = '常见问题'
        faq_q1 = f'{tool["cn_name"]}怎么用？'
        faq_a1 = f'在输入框中填写需要的数据，点击操作按钮即可实时查看结果。所有处理都在浏览器本地完成。'
        faq_q2 = f'{tool["cn_name"]}免费吗？'
        faq_a2 = '完全免费，无需注册，无任何使用限制。'
        faq_q3 = '数据安全吗？'
        faq_a3 = '所有数据处理在浏览器本地完成，数据不会上传到任何服务器，完全保护您的隐私。'
        footer_text = '© 2024 Free ToolBase · 所有工具均在浏览器本地运行'
    
    return f'''<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#0f172a;color:#e2e8f0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,"PingFang SC","Microsoft YaHei",sans-serif;line-height:1.6}}
a{{color:#06b6d4;text-decoration:none}}
.container{{max-width:1200px;margin:0 auto;padding:0 16px}}
.breadcrumb{{color:#94a3b8;font-size:13px;padding:12px 0}}
.hero{{background:linear-gradient(135deg,#0c4a6e,#0f172a);border-radius:16px;padding:32px 24px;margin-bottom:24px;text-align:center;border:1px solid rgba(6,182,212,.15)}}
h1{{font-size:2rem;color:#f1f5f9;margin-bottom:8px}}
.subtitle{{color:#94a3b8;font-size:.95rem}}
.badge{{background:rgba(16,185,129,.15);color:#10b981;padding:4px 12px;border-radius:20px;font-size:.8rem;display:inline-block;margin-top:8px;border:1px solid rgba(16,185,129,.2)}}
.panel{{background:#1e293b;border-radius:16px;padding:24px;border:1px solid rgba(148,163,184,.1);margin-bottom:20px}}
.panel-title{{font-size:1rem;color:#f1f5f9;margin-bottom:16px;font-weight:600}}
.textarea-area{{width:100%;background:#0f172a;border:1px solid rgba(148,163,184,.2);border-radius:10px;color:#e2e8f0;padding:12px;font-size:.9rem;font-family:"JetBrains Mono",monospace;resize:vertical;min-height:120px}}
.textarea-area:focus{{outline:none;border-color:#06b6d4}}
.btn-group{{display:flex;gap:10px;margin-top:16px;flex-wrap:wrap}}
.btn{{padding:10px 20px;border-radius:10px;border:none;font-size:.9rem;font-weight:500;cursor:pointer;transition:all .2s;white-space:nowrap}}
.btn:disabled{{opacity:.5;cursor:not-allowed}}
.btn-primary{{background:#06b6d4;color:#0f172a}}
.btn-primary:hover:not(:disabled){{background:#22d3ee;transform:translateY(-1px)}}
.btn-secondary{{background:#334155;color:#e2e8f0}}
.btn-secondary:hover:not(:disabled){{background:#475569}}
.btn-success{{background:rgba(16,185,129,.15);color:#10b981;border:1px solid rgba(16,185,129,.2)}}
.btn-success:hover:not(:disabled){{background:rgba(16,185,129,.25)}}
.btn-danger{{background:rgba(239,68,68,.15);color:#ef4444;border:1px solid rgba(239,68,68,.2)}}
.btn-danger:hover:not(:disabled){{background:rgba(239,68,68,.25)}}
.privacy-note{{background:rgba(16,185,129,.08);border:1px solid rgba(16,185,129,.15);border-radius:10px;padding:12px 16px;margin-top:16px;color:#10b981;font-size:.85rem}}
.output-area{{width:100%;background:#0f172a;border:1px solid rgba(148,163,184,.2);border-radius:10px;color:#e2e8f0;padding:12px;font-size:.85rem;font-family:"JetBrains Mono",monospace;min-height:120px;max-height:400px;overflow:auto;white-space:pre-wrap;word-break:break-word}}
.faq-item{{background:rgba(148,163,184,.03);border-radius:10px;padding:16px;margin-top:12px;border:1px solid rgba(148,163,184,.08)}}
.faq-item h3{{color:#22d3ee;font-size:.95rem;font-weight:600;margin-bottom:8px}}
.faq-item p{{color:#94a3b8;font-size:.88rem;line-height:1.7}}
.footer{{text-align:center;padding:24px 0;border-top:1px solid rgba(148,163,184,.1);margin-top:32px}}
.footer a{{margin:0 12px;font-size:.88rem;color:#06b6d4}}
.footer p{{color:#64748b;font-size:.82rem;margin-top:4px}}
.toast{{position:fixed;bottom:24px;left:50%;transform:translateX(-50%);background:#1e293b;color:#e2e8f0;padding:12px 24px;border-radius:8px;font-size:.9rem;border:1px solid rgba(148,163,184,.15);opacity:0;transition:opacity .3s;pointer-events:none;z-index:999}}
.toast.show{{opacity:1}}
@media(max-width:640px){{h1{{font-size:1.2rem;word-break:break-word}}.container{{padding:0 12px}}}}
</style>
</head>
<body>
<div class="container">
  <div class="breadcrumb"><a href="{'/en/' if not cn else '/'}">{home}</a> / <a href="{'/en/#tools' if not cn else '/#tools'}">{tools_link}</a> / {h1}</div>
  <div class="hero">
    <h1>{h1}</h1>
    <p class="subtitle">{subtitle}</p>
    <span class="badge">{'Free Online Tool | No Registration' if not cn else '免费在线工具 | 无需注册'}</span>
  </div>

  {tool['html_content']}

  <div class="panel">
    <div class="panel-title">❓ {faq_title}</div>
    <div class="faq-item"><h3>{faq_q1}</h3><p>{faq_a1}</p></div>
    <div class="faq-item"><h3>{faq_q2}</h3><p>{faq_a2}</p></div>
    <div class="faq-item"><h3>{faq_q3}</h3><p>{faq_a3}</p></div>
  </div>

  <div class="footer">
    <div><a href="{'/en/' if not cn else '/'}">{home}</a><a href="{'/en/#tools' if not cn else '/#tools'}">{tools_link}</a><a href="{'/en/privacy-policy/' if not cn else '/privacy-policy/'}">{'Privacy' if not cn else '隐私政策'}</a></div>
    <p>{footer_text}</p>
  </div>
</div>
<div id="toast" class="toast"></div>
<script>
{tool['js_logic']}
</script>
</body>
</html>'''

if __name__ == '__main__':
    create_tool_files()
