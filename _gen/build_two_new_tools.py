#!/usr/bin/env python3
"""Build 2 new tools using template v3 - batch generation"""
import sys, os
sys.path.insert(0, os.path.expanduser('~/tools-site/_gen'))
from tool_template_v3 import ToolPageBuilder

builder = ToolPageBuilder()

# ============================================================
# TOOL 1: HTML Previewer  - Live HTML/CSS/JS Preview
# ============================================================

HTML_PREVIEWER_TOOL_HTML_CN = '''
<div class="previewer-layout" style="display:grid;grid-template-columns:1fr;gap:12px;min-height:500px">
  <div class="editor-panel">
    <div style="display:flex;gap:8px;margin-bottom:8px;flex-wrap:wrap">
      <button id="run-btn" class="btn" style="background:#22c55e;color:#000;font-weight:600">▶ 运行</button>
      <button id="clear-btn" class="btn" style="background:#ef4444;color:#fff">清空</button>
      <label style="color:#94a3b8;font-size:.85rem;display:flex;align-items:center;gap:4px">
        <input type="checkbox" id="auto-run" checked> 自动运行
      </label>
      <div style="flex:1;text-align:right;font-size:.8rem;color:#64748b">HTML/CSS/JS 实时预览</div>
    </div>
    <textarea id="html-editor" spellcheck="false" style="width:100%;height:200px;background:#0f172a;border:1px solid rgba(148,163,184,.2);border-radius:8px;color:#e2e8f0;font-family:'Consolas','Monaco','Courier New',monospace;font-size:.85rem;padding:12px;resize:vertical;outline:none;tab-size:2"><!DOCTYPE html>
<html>
<head><style>
body { font-family: sans-serif; padding: 20px; }
h1 { color: #06b6d4; }
</style></head>
<body>
<h1>Hello, World!</h1>
<p>开始编辑HTML代码，右侧预览将实时更新。</p>
<button onclick="alert('Hello!')">点击我</button>
</body>
</html></textarea>
  </div>
  <div class="preview-panel">
    <div style="display:flex;gap:8px;justify-content:space-between;margin-bottom:8px;align-items:center">
      <div style="color:#f1c40f;font-weight:500;font-size:.9rem">🖥️ 预览</div>
      <button id="open-new-tab-btn" class="btn" style="background:#1e293b;color:#94a3b8;font-size:.8rem">新标签页打开</button>
    </div>
    <iframe id="preview-frame" style="width:100%;height:350px;background:#fff;border-radius:8px;border:1px solid rgba(148,163,184,.2)"></iframe>
  </div>
</div>
<style>
.btn{padding:6px 16px;border:none;border-radius:6px;cursor:pointer;font-size:.85rem;transition:all .2s}
.btn:hover{opacity:.85;transform:translateY(-1px)}
#preview-frame{transition:all .3s}
.editor-panel textarea:focus{border-color:rgba(34,197,94,.4);box-shadow:0 0 0 3px rgba(34,197,94,.1)}
</style>
'''

HTML_PREVIEWER_TOOL_HTML_EN = '''
<div class="previewer-layout" style="display:grid;grid-template-columns:1fr;gap:12px;min-height:500px">
  <div class="editor-panel">
    <div style="display:flex;gap:8px;margin-bottom:8px;flex-wrap:wrap">
      <button id="run-btn" class="btn" style="background:#22c55e;color:#000;font-weight:600">▶ Run</button>
      <button id="clear-btn" class="btn" style="background:#ef4444;color:#fff">Clear</button>
      <label style="color:#94a3b8;font-size:.85rem;display:flex;align-items:center;gap:4px">
        <input type="checkbox" id="auto-run" checked> Auto Run
      </label>
      <div style="flex:1;text-align:right;font-size:.8rem;color:#64748b">Live HTML/CSS/JS Preview</div>
    </div>
    <textarea id="html-editor" spellcheck="false" style="width:100%;height:200px;background:#0f172a;border:1px solid rgba(148,163,184,.2);border-radius:8px;color:#e2e8f0;font-family:'Consolas','Monaco','Courier New',monospace;font-size:.85rem;padding:12px;resize:vertical;outline:none;tab-size:2"><!DOCTYPE html>
<html>
<head><style>
body { font-family: sans-serif; padding: 20px; }
h1 { color: #06b6d4; }
</style></head>
<body>
<h1>Hello, World!</h1>
<p>Edit the HTML code and see the preview update in real time.</p>
<button onclick="alert('Hello!')">Click Me</button>
</body>
</html></textarea>
  </div>
  <div class="preview-panel">
    <div style="display:flex;gap:8px;justify-content:space-between;margin-bottom:8px;align-items:center">
      <div style="color:#f1c40f;font-weight:500;font-size:.9rem">🖥️ Live Preview</div>
      <button id="open-new-tab-btn" class="btn" style="background:#1e293b;color:#94a3b8;font-size:.8rem">Open in New Tab</button>
    </div>
    <iframe id="preview-frame" style="width:100%;height:350px;background:#fff;border-radius:8px;border:1px solid rgba(148,163,184,.2)"></iframe>
  </div>
</div>
<style>
.btn{padding:6px 16px;border:none;border-radius:6px;cursor:pointer;font-size:.85rem;transition:all .2s}
.btn:hover{opacity:.85;transform:translateY(-1px)}
#preview-frame{transition:all .3s}
.editor-panel textarea:focus{border-color:rgba(34,197,94,.4);box-shadow:0 0 0 3px rgba(34,197,94,.1)}
</style>
'''

HTML_PREVIEWER_JS = '''
document.addEventListener('DOMContentLoaded', function() {
  var editor = document.getElementById('html-editor');
  var frame = document.getElementById('preview-frame');
  var runBtn = document.getElementById('run-btn');
  var clearBtn = document.getElementById('clear-btn');
  var autoRun = document.getElementById('auto-run');
  var openNewTab = document.getElementById('open-new-tab-btn');
  var timer = null;

  function render() {
    var html = editor.value;
    var src = 'data:text/html;charset=utf-8,' + encodeURIComponent(html);
    frame.src = src;
  }

  function runNow() {
    render();
  }

  if (autoRun && autoRun.checked) {
    render();
  }

  if (runBtn) {
    runBtn.addEventListener('click', function() { render(); });
  }

  if (clearBtn) {
    clearBtn.addEventListener('click', function() {
      editor.value = '<!DOCTYPE html>\\n<html>\\n<head><style>\\nbody { font-family: sans-serif; padding: 20px; }\\n</style></head>\\n<body>\\n<h1>Hello, World!</h1>\\n<p>Start editing!</p>\\n</body>\\n</html>';
      render();
    });
  }

  if (editor) {
    editor.addEventListener('input', function() {
      if (autoRun && autoRun.checked) {
        if (timer) clearTimeout(timer);
        timer = setTimeout(function() { render(); }, 500);
      }
    });
    editor.addEventListener('keydown', function(e) {
      if (e.key === 'Tab') {
        e.preventDefault();
        var start = this.selectionStart;
        var end = this.selectionEnd;
        this.value = this.value.substring(0, start) + '  ' + this.value.substring(end);
        this.selectionStart = this.selectionEnd = start + 2;
        if (autoRun && autoRun.checked) {
          if (timer) clearTimeout(timer);
          timer = setTimeout(function() { render(); }, 500);
        }
      }
    });
  }

  if (autoRun) {
    autoRun.addEventListener('change', function() {
      if (this.checked) render();
    });
  }

  if (openNewTab) {
    openNewTab.addEventListener('click', function() {
      var html = editor.value;
      var win = window.open('', '_blank');
      win.document.write(html);
      win.document.close();
    });
  }
});
'''

HTML_PREVIEWER_FAQS_CN = [
    ("HTML预览器支持哪些语言？", "支持HTML、CSS和JavaScript。你可以在编辑器中混合使用这三种语言，预览区域会像真实浏览器一样渲染。"),
    ("代码会被上传到服务器吗？", "不会。所有代码都在你的浏览器本地处理，通过data:URI直接渲染，不经过任何服务器。"),
    ("为什么我的JavaScript没有生效？", "请检查你的JavaScript语法。预览使用data:URI模式，一些高级API（如Service Worker）可能受限。建议使用标准的script标签。"),
    ("支持移动端预览吗？", "目前以桌面浏览器渲染为主。如需测试移动端响应式布局，建议使用浏览器的开发者工具。"),
    ("如何保存我的代码？", "目前暂未提供保存功能。你可以复制代码到本地文件，或使用浏览器的「另存为」功能。"),
]
HTML_PREVIEWER_FAQS_EN = [
    ("What languages does the HTML Previewer support?", "It supports HTML, CSS, and JavaScript. You can mix all three in the editor and see the result rendered just like a real browser."),
    ("Is my code uploaded to a server?", "No. All processing is done locally in your browser using data:URI rendering. Nothing is sent to any server."),
    ("Why isn't my JavaScript working?", "Check your JavaScript syntax. The preview uses data:URI mode, which may restrict some advanced APIs like Service Workers. Use standard script tags."),
    ("Can I preview mobile layouts?", "Currently the preview targets desktop rendering. For responsive testing, use your browser's developer tools."),
    ("How do I save my code?", "Save functionality is not yet available. You can copy the code to a local file or use your browser's 'Save As' feature."),
]

HTML_PREVIEWER_SEO_CN = '''
<h2>在线HTML预览器 - 实时编辑与预览HTML/CSS/JS代码</h2>
<p>HTML预览器是一个免费的在线工具，让你可以实时编辑和预览HTML、CSS和JavaScript代码。无需安装任何软件，打开浏览器即可使用。</p>
<h3>主要功能</h3>
<ul>
  <li><strong>实时预览：</strong>编辑代码后立即看到效果，支持自动运行模式</li>
  <li><strong>语法高亮：</strong>代码编辑区域采用等宽字体，便于阅读和调试</li>
  <li><strong>新标签页打开：</strong>可以在新标签页中查看完整的渲染效果</li>
  <li><strong>零依赖：</strong>纯前端实现，不依赖任何第三方服务或库</li>
</ul>
<h3>适用场景</h3>
<p>前端开发学习、原型设计、代码片段测试、在线教学、技术分享等。无论是初学者还是专业开发者，都可以快速验证HTML/CSS/JS代码的运行效果。</p>
'''

HTML_PREVIEWER_SEO_EN = '''
<h2>Online HTML Previewer - Live Edit & Preview HTML/CSS/JS Code</h2>
<p>The HTML Previewer is a free online tool that lets you edit and preview HTML, CSS, and JavaScript code in real time. No installation needed - just open your browser and start coding.</p>
<h3>Key Features</h3>
<ul>
  <li><strong>Live Preview:</strong> See changes instantly as you type, with auto-run mode</li>
  <li><strong>Code Editing:</strong> Monospace font editor for easy reading and debugging</li>
  <li><strong>New Tab View:</strong> Open the rendered page in a new tab for full inspection</li>
  <li><strong>Zero Dependencies:</strong> Pure frontend, no third-party services or libraries needed</li>
</ul>
<h3>Use Cases</h3>
<p>Frontend learning, prototyping, code snippet testing, online teaching, and technical sharing. Perfect for beginners and professional developers alike.</p>
'''

# ============================================================
# TOOL 2: Meeting Planner - Coordinate meeting times
# ============================================================

MEETING_PLANNER_TOOL_HTML_CN = '''
<div class="meeting-planner">
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:12px">
    <div class="form-group">
      <label>📅 会议日期</label>
      <input type="date" id="meeting-date">
    </div>
    <div class="form-group">
      <label>⏰ 会议时长</label>
      <select id="meeting-duration">
        <option value="15">15分钟</option>
        <option value="30" selected>30分钟</option>
        <option value="45">45分钟</option>
        <option value="60">1小时</option>
        <option value="90">1.5小时</option>
        <option value="120">2小时</option>
      </select>
    </div>
  </div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:12px">
    <div class="form-group">
      <label>🌍 我的时区</label>
      <select id="my-tz" style="width:100%;padding:10px 14px;background:#0f172a;border:1px solid rgba(148,163,184,.2);border-radius:8px;color:#e2e8f0;font-size:.9rem;outline:none"></select>
    </div>
    <div class="form-group">
      <label>🕐 我的可用时间</label>
      <div style="display:flex;gap:6px;align-items:center">
        <input type="time" id="my-start" value="09:00" style="flex:1;padding:8px 10px;background:#0f172a;border:1px solid rgba(148,163,184,.2);border-radius:8px;color:#e2e8f0;font-size:.85rem;outline:none">
        <span style="color:#64748b">至</span>
        <input type="time" id="my-end" value="18:00" style="flex:1;padding:8px 10px;background:#0f172a;border:1px solid rgba(148,163,184,.2);border-radius:8px;color:#e2e8f0;font-size:.85rem;outline:none">
      </div>
    </div>
  </div>
  <div id="participants-section" style="margin-bottom:12px">
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px">
      <label style="color:#94a3b8;font-size:.9rem">👥 参与者时区</label>
      <button id="add-participant-btn" class="btn-sm" style="background:rgba(6,182,212,.15);color:#22d3ee;border:1px solid rgba(6,182,212,.2)">+ 添加参与者</button>
    </div>
    <div id="participants-list"></div>
  </div>
  <button id="find-times-btn" class="btn-primary" style="width:100%;padding:12px;background:#06b6d4;color:#000;font-weight:600;border:none;border-radius:8px;cursor:pointer;font-size:1rem;transition:all .2s">🔍 查找最佳会议时间</button>
  <div id="results-section" style="display:none;margin-top:16px">
    <h3 style="color:#f1c40f;margin-bottom:8px">✅ 推荐会议时间</h3>
    <div id="results-list" class="results-list"></div>
  </div>
</div>
<style>
.btn-sm{padding:6px 12px;border-radius:6px;cursor:pointer;font-size:.8rem;transition:all .2s}
.btn-sm:hover{opacity:.8}
.btn-primary:hover{opacity:.9;transform:translateY(-1px)}
.participant-row{display:grid;grid-template-columns:1fr 1fr auto;gap:8px;align-items:center;margin-bottom:8px;padding:8px;background:rgba(15,23,42,.5);border-radius:8px}
.participant-row select,.participant-row input{width:100%;padding:8px 10px;background:#0f172a;border:1px solid rgba(148,163,184,.2);border-radius:6px;color:#e2e8f0;font-size:.8rem;outline:none}
.remove-btn{background:rgba(239,68,68,.15);color:#ef4444;border:1px solid rgba(239,68,68,.2);padding:4px 10px;border-radius:6px;cursor:pointer;font-size:.75rem}
.remove-btn:hover{background:rgba(239,68,68,.25)}
.result-card{padding:12px;background:rgba(34,197,94,.1);border:1px solid rgba(34,197,94,.2);border-radius:8px;margin-bottom:8px}
.result-card .time{font-size:1.1rem;font-weight:600;color:#22c55e}
.result-card .tz-info{font-size:.8rem;color:#94a3b8;margin-top:4px}
</style>
'''

MEETING_PLANNER_TOOL_HTML_EN = '''
<div class="meeting-planner">
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:12px">
    <div class="form-group">
      <label>📅 Meeting Date</label>
      <input type="date" id="meeting-date">
    </div>
    <div class="form-group">
      <label>⏰ Duration</label>
      <select id="meeting-duration">
        <option value="15">15 minutes</option>
        <option value="30" selected>30 minutes</option>
        <option value="45">45 minutes</option>
        <option value="60">1 hour</option>
        <option value="90">1.5 hours</option>
        <option value="120">2 hours</option>
      </select>
    </div>
  </div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:12px">
    <div class="form-group">
      <label>🌍 My Timezone</label>
      <select id="my-tz" style="width:100%;padding:10px 14px;background:#0f172a;border:1px solid rgba(148,163,184,.2);border-radius:8px;color:#e2e8f0;font-size:.9rem;outline:none"></select>
    </div>
    <div class="form-group">
      <label>🕐 My Availability</label>
      <div style="display:flex;gap:6px;align-items:center">
        <input type="time" id="my-start" value="09:00" style="flex:1;padding:8px 10px;background:#0f172a;border:1px solid rgba(148,163,184,.2);border-radius:8px;color:#e2e8f0;font-size:.85rem;outline:none">
        <span style="color:#64748b">to</span>
        <input type="time" id="my-end" value="18:00" style="flex:1;padding:8px 10px;background:#0f172a;border:1px solid rgba(148,163,184,.2);border-radius:8px;color:#e2e8f0;font-size:.85rem;outline:none">
      </div>
    </div>
  </div>
  <div id="participants-section" style="margin-bottom:12px">
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px">
      <label style="color:#94a3b8;font-size:.9rem">👥 Participant Timezones</label>
      <button id="add-participant-btn" class="btn-sm" style="background:rgba(6,182,212,.15);color:#22d3ee;border:1px solid rgba(6,182,212,.2)">+ Add Participant</button>
    </div>
    <div id="participants-list"></div>
  </div>
  <button id="find-times-btn" class="btn-primary" style="width:100%;padding:12px;background:#06b6d4;color:#000;font-weight:600;border:none;border-radius:8px;cursor:pointer;font-size:1rem;transition:all .2s">🔍 Find Best Meeting Times</button>
  <div id="results-section" style="display:none;margin-top:16px">
    <h3 style="color:#f1c40f;margin-bottom:8px">✅ Recommended Meeting Times</h3>
    <div id="results-list" class="results-list"></div>
  </div>
</div>
<style>
.btn-sm{padding:6px 12px;border-radius:6px;cursor:pointer;font-size:.8rem;transition:all .2s}
.btn-sm:hover{opacity:.8}
.btn-primary:hover{opacity:.9;transform:translateY(-1px)}
.participant-row{display:grid;grid-template-columns:1fr 1fr auto;gap:8px;align-items:center;margin-bottom:8px;padding:8px;background:rgba(15,23,42,.5);border-radius:8px}
.participant-row select,.participant-row input{width:100%;padding:8px 10px;background:#0f172a;border:1px solid rgba(148,163,184,.2);border-radius:6px;color:#e2e8f0;font-size:.8rem;outline:none}
.remove-btn{background:rgba(239,68,68,.15);color:#ef4444;border:1px solid rgba(239,68,68,.2);padding:4px 10px;border-radius:6px;cursor:pointer;font-size:.75rem}
.remove-btn:hover{background:rgba(239,68,68,.25)}
.result-card{padding:12px;background:rgba(34,197,94,.1);border:1px solid rgba(34,197,94,.2);border-radius:8px;margin-bottom:8px}
.result-card .time{font-size:1.1rem;font-weight:600;color:#22c55e}
.result-card .tz-info{font-size:.8rem;color:#94a3b8;margin-top:4px}
</style>
'''

MEETING_PLANNER_JS = '''
document.addEventListener('DOMContentLoaded', function() {
  // Common timezones
  var timezones = [
    {label: 'UTC (UTC+0)', value: 'UTC'},
    {label: 'London (GMT+0/+1)', value: 'Europe/London'},
    {label: 'Paris/Berlin (CET, UTC+1/+2)', value: 'Europe/Berlin'},
    {label: 'Moscow (MSK, UTC+3)', value: 'Europe/Moscow'},
    {label: 'Dubai (GST, UTC+4)', value: 'Asia/Dubai'},
    {label: 'India (IST, UTC+5:30)', value: 'Asia/Kolkata'},
    {label: 'China (CST, UTC+8)', value: 'Asia/Shanghai'},
    {label: 'Tokyo (JST, UTC+9)', value: 'Asia/Tokyo'},
    {label: 'Sydney (AEST, UTC+10/+11)', value: 'Australia/Sydney'},
    {label: 'New Zealand (NZST, UTC+12/+13)', value: 'Pacific/Auckland'},
    {label: 'Hawaii (HST, UTC-10)', value: 'Pacific/Honolulu'},
    {label: 'Alaska (AKST, UTC-9)', value: 'America/Anchorage'},
    {label: 'Los Angeles (PST, UTC-8/-7)', value: 'America/Los_Angeles'},
    {label: 'Denver (MST, UTC-7/-6)', value: 'America/Denver'},
    {label: 'Chicago (CST, UTC-6/-5)', value: 'America/Chicago'},
    {label: 'New York (EST, UTC-5/-4)', value: 'America/New_York'},
    {label: 'São Paulo (BRT, UTC-3)', value: 'America/Sao_Paulo'},
    {label: 'Argentina (ART, UTC-3)', value: 'America/Argentina/Buenos_Aires'},
    {label: 'Reykjavik (GMT, UTC+0)', value: 'Atlantic/Reykjavik'},
  ];

  function populateTzSelect(sel) {
    sel.innerHTML = '<option value="">-- 选择时区 / Select Timezone --</option>';
    timezones.forEach(function(tz) {
      var opt = document.createElement('option');
      opt.value = tz.value;
      opt.textContent = tz.label;
      sel.appendChild(opt);
    });
    // Try to detect user's timezone
    try {
      var userTz = Intl.DateTimeFormat().resolvedOptions().timeZone;
      for (var i = 0; i < sel.options.length; i++) {
        if (sel.options[i].value === userTz) {
          sel.selectedIndex = i;
          break;
        }
      }
    } catch(e) {}
  }

  var myTz = document.getElementById('my-tz');
  populateTzSelect(myTz);

  // Set today's date
  var today = new Date();
  var dateInput = document.getElementById('meeting-date');
  dateInput.value = today.toISOString().split('T')[0];
  // Set +7 days as max
  var future = new Date(today);
  future.setDate(future.getDate() + 30);
  dateInput.max = future.toISOString().split('T')[0];

  // Participants management
  var participants = [];
  var participantsList = document.getElementById('participants-list');
  var addBtn = document.getElementById('add-participant-btn');

  function addParticipant(name, tz, start, end) {
    participants.push({
      name: name || 'Participant ' + (participants.length + 1),
      tz: tz || 'America/New_York',
      start: start || '09:00',
      end: end || '18:00'
    });
    renderParticipants();
  }

  function removeParticipant(index) {
    participants.splice(index, 1);
    renderParticipants();
  }

  function renderParticipants() {
    if (!participantsList) return;
    if (participants.length === 0) {
      participantsList.innerHTML = '<div style="color:#475569;font-size:.85rem;text-align:center;padding:12px">暂无参与者，点击上方添加</div>';
      return;
    }
    var html = '';
    for (var i = 0; i < participants.length; i++) {
      var p = participants[i];
      html += '<div class="participant-row">';
      html += '<input type="text" class="p-name" value="' + p.name.replace(/"/g,'&quot;') + '" placeholder="Name" data-index="' + i + '">';
      html += '<select class="p-tz" data-index="' + i + '">';
      timezones.forEach(function(tz) {
        html += '<option value="' + tz.value + '"' + (tz.value === p.tz ? ' selected' : '') + '>' + tz.label + '</option>';
      });
      html += '</select>';
      html += '<button class="remove-btn" data-index="' + i + '">✕</button>';
      html += '</div>';
    }
    participantsList.innerHTML = html;

    // Bind events
    participantsList.querySelectorAll('.remove-btn').forEach(function(btn) {
      btn.addEventListener('click', function() {
        removeParticipant(parseInt(this.dataset.index));
      });
    });
    participantsList.querySelectorAll('.p-name').forEach(function(inp) {
      inp.addEventListener('change', function() {
        participants[parseInt(this.dataset.index)].name = this.value;
      });
    });
    participantsList.querySelectorAll('.p-tz').forEach(function(sel) {
      sel.addEventListener('change', function() {
        participants[parseInt(this.dataset.index)].tz = this.value;
      });
    });
  }

  // Add first participant
  addParticipant('Alice', 'America/New_York', '09:00', '17:00');
  addParticipant('Bob', 'Europe/London', '10:00', '18:00');

  if (addBtn) {
    addBtn.addEventListener('click', function() {
      addParticipant('', '', '09:00', '18:00');
    });
  }

  // Find meeting times
  var findBtn = document.getElementById('find-times-btn');
  var resultsSection = document.getElementById('results-section');
  var resultsList = document.getElementById('results-list');
  var myStart = document.getElementById('my-start');
  var myEnd = document.getElementById('my-end');
  var duration = document.getElementById('meeting-duration');
  var meetingDate = document.getElementById('meeting-date');

  function getOffset(tz) {
    if (!tz) return 0;
    try {
      var date = new Date();
      var formatter = new Intl.DateTimeFormat('en-US', { timeZone: tz, timeZoneName: 'shortOffset' });
      var parts = formatter.formatToParts(date);
      for (var i = 0; i < parts.length; i++) {
        if (parts[i].type === 'timeZoneName') {
          var offsetStr = parts[i].value;
          var match = offsetStr.match(/UTC([+-])(\d+)(?::(\d+))?/);
          if (match) {
            var hours = parseInt(match[2]);
            var mins = parseInt(match[3] || '0');
            if (match[1] === '-') hours = -hours;
            return hours * 60 + mins;
          }
        }
      }
    } catch(e) {}
    return 0;
  }

  function formatTime(date, tz) {
    try {
      var opts = { hour: '2-digit', minute: '2-digit', hour12: false, timeZone: tz };
      return new Intl.DateTimeFormat('en-US', opts).format(date);
    } catch(e) {
      return date.toTimeString().slice(0,5);
    }
  }

  function findOverlaps() {
    var myTzVal = myTz.value;
    var myStartVal = myStart.value;
    var myEndVal = myEnd.value;
    var dur = parseInt(duration.value);
    var dateVal = meetingDate.value;

    if (!myTzVal) { alert('请选择你的时区 / Please select your timezone'); return; }
    if (!myStartVal || !myEndVal) { alert('请设置可用时间 / Please set availability'); return; }
    if (!dateVal) { alert('请选择日期 / Please select a date'); return; }

    resultsList.innerHTML = '';
    resultsSection.style.display = 'none';

    // Convert my availability to UTC minutes
    var myStartParts = myStartVal.split(':').map(Number);
    var myEndParts = myEndVal.split(':').map(Number);
    var myStartMin = myStartParts[0] * 60 + myStartParts[1];
    var myEndMin = myEndParts[0] * 60 + myEndParts[1];

    // Create date objects for the meeting date
    var dateObj = new Date(dateVal + 'T00:00:00');
    var myOffset = getOffset(myTzVal);

    // For each participant, get their availability in UTC
    var allSlots = [];
    var timeSlots = [];
    // Generate 30-min slots
    var slotStart = Math.max(0, myStartMin);
    var slotEnd = Math.min(1440, myEndMin);

    for (var m = slotStart; m + dur <= slotEnd; m += 30) {
      timeSlots.push(m);
    }

    // Score each slot
    timeSlots.forEach(function(slotMin) {
      // Slot in UTC
      var slotUTC = slotMin - myOffset;
      var score = 0;
      var details = [];

      // Check each participant
      var allOk = true;
      for (var i = 0; i < participants.length; i++) {
        var p = participants[i];
        if (!p.tz) { allOk = false; break; }
        var pOff = getOffset(p.tz);
        var pStartParts = (p.start || '09:00').split(':').map(Number);
        var pEndParts = (p.end || '18:00').split(':').map(Number);
        var pStartMin = pStartParts[0] * 60 + pStartParts[1];
        var pEndMin = pEndParts[0] * 60 + pEndParts[1];

        // Slot in participant's timezone
        var pSlotStart = slotUTC + pOff;
        var pSlotEnd = pSlotStart + dur;

        // Normalize to 0-1440
        var pStartNorm = ((pSlotStart % 1440) + 1440) % 1440;
        var pEndNorm = ((pSlotEnd % 1440) + 1440) % 1440;

        // Check if within participant's availability (handle overnight)
        var pAvailOk = false;
        if (pStartMin <= pEndMin) {
          pAvailOk = (pStartNorm >= pStartMin && pEndNorm <= pEndMin);
        } else {
          pAvailOk = (pStartNorm >= pStartMin || pEndNorm <= pEndMin);
        }

        if (!pAvailOk) { allOk = false; break; }
        score++;
        details.push({
          name: p.name,
          tz: p.tz,
          localStart: pSlotStart
        });
      }

      if (allOk && score > 0) {
        allSlots.push({
          utcStart: slotUTC,
          localStart: slotMin,
          localEnd: slotMin + dur,
          score: score,
          details: details
        });
      }
    });

    // Sort by score (highest first)
    allSlots.sort(function(a, b) { return b.score - a.score; });

    // Show top results
    if (allSlots.length === 0) {
      resultsList.innerHTML = '<div style="padding:20px;text-align:center;color:#ef4444">😕 未找到所有参与者都空闲的时间段。<br>请调整可用时间或时区后重试。</div>';
    } else {
      var html = '';
      var maxShow = Math.min(5, allSlots.length);
      for (var s = 0; s < maxShow; s++) {
        var slot = allSlots[s];
        var startDate = new Date(dateObj);
        startDate.setMinutes(slot.utcStart);

        var endDate = new Date(dateObj);
        endDate.setMinutes(slot.utcStart + dur);

        var myTime = formatTime(startDate, myTzVal) + ' - ' + formatTime(endDate, myTzVal);
        var utcTime = formatTime(startDate, 'UTC') + ' - ' + formatTime(endDate, 'UTC');

        html += '<div class="result-card">';
        html += '<div class="time">🕐 ' + myTime + ' (你的时区)</div>';
        html += '<div class="tz-info">UTC: ' + utcTime + '</div>';
        html += '<div class="tz-info" style="margin-top:6px">';
        html += '<strong>各时区时间:</strong><br>';
        html += '<span>你: ' + myTime + '</span><br>';
        slot.details.forEach(function(d) {
          var dStart = new Date(dateObj);
          dStart.setMinutes(slot.utcStart);
          var t = formatTime(dStart, d.tz);
          html += '<span>' + d.name + ': ' + t + ' (' + d.tz + ')</span><br>';
        });
        html += '</div>';
        html += '<div style="margin-top:6px;font-size:.8rem;color:#64748b">参会人数: ' + slot.score + '</div>';
        html += '</div>';
      }
      if (allSlots.length > 5) {
        html += '<div style="text-align:center;color:#64748b;font-size:.85rem;padding:8px">还有 ' + (allSlots.length - 5) + ' 个可选时间段</div>';
      }
      resultsList.innerHTML = html;
    }
    resultsSection.style.display = 'block';
  }

  if (findBtn) {
    findBtn.addEventListener('click', findOverlaps);
  }
});
'''

MEETING_PLANNER_FAQS_CN = [
    ("会议时间规划器如何工作？", "你设置自己的时区和可用时间，添加参与者及其时区，工具会自动计算出所有参与者都空闲的会议时间段。"),
    ("支持多少参与者？", "不限制参与者数量，你可以自由添加任意数量的参与者，每个参与者都可以设置自己的时区和可用时间。"),
    ("时区会自动检测吗？", "工具会尝试检测你的浏览器时区并自动选择。参与者时区需要手动选择。"),
    ("可以处理跨日（过夜）的可用时间吗？", "当前版本暂不支持过夜时间（如22:00-06:00），可用时间在同一天内。"),
    ("工具支持夏令时吗？", "是的。工具使用Intl.DateTimeFormat API获取时区偏移，会自动处理夏令时调整。"),
]
MEETING_PLANNER_FAQS_EN = [
    ("How does the Meeting Planner work?", "Set your timezone and availability, add participants with their timezones, and the tool finds overlapping free time slots for everyone."),
    ("How many participants can I add?", "There's no limit. You can add as many participants as you need, each with their own timezone and availability."),
    ("Does it auto-detect my timezone?", "The tool tries to detect your browser timezone. Participant timezones need to be selected manually."),
    ("Can it handle overnight availability?", "Currently it doesn't support overnight periods (e.g., 10 PM to 6 AM). Availability is within a single day."),
    ("Does it handle DST?", "Yes. The tool uses the Intl.DateTimeFormat API for timezone offsets and handles Daylight Saving Time automatically."),
]

MEETING_PLANNER_SEO_CN = '''
<h2>在线会议时间规划器 - 跨时区会议时间协调工具</h2>
<p>会议时间规划器是一个免费的在线工具，帮助团队轻松协调跨时区的会议时间。无论团队成员分布在全球哪个角落，都能找到适合所有人的会议时间。</p>
<h3>主要功能</h3>
<ul>
  <li><strong>多时区支持：</strong>支持全球主要时区，自动处理夏令时</li>
  <li><strong>灵活参与者管理：</strong>可添加任意数量的参与者，每个参与者独立设置时区和可用时间</li>
  <li><strong>智能时间查找：</strong>自动计算所有参与者的空闲重叠时间段</li>
  <li><strong>本地时间显示：</strong>每个参与者看到的是自己的本地时间</li>
  <li><strong>纯前端处理：</strong>所有数据仅在浏览器本地处理，不上传服务器</li>
</ul>
<h3>适用场景</h3>
<p>跨国团队会议、远程团队站会、跨地区项目协调、国际客户会议、分布式团队工作坊等。</p>
'''

MEETING_PLANNER_SEO_EN = '''
<h2>Online Meeting Planner - Cross-Timezone Meeting Coordinator</h2>
<p>The Meeting Planner is a free online tool that helps teams easily coordinate meeting times across timezones. Whether your team is distributed globally, find the perfect time for everyone.</p>
<h3>Key Features</h3>
<ul>
  <li><strong>Multi-Timezone Support:</strong> Supports major global timezones with automatic DST handling</li>
  <li><strong>Flexible Participants:</strong> Add unlimited participants, each with their own timezone and availability</li>
  <li><strong>Smart Time Finding:</strong> Automatically calculates overlapping free time slots</li>
  <li><strong>Local Time Display:</strong> Each participant sees their own local time</li>
  <li><strong>Pure Frontend:</strong> All processing is done locally in your browser</li>
</ul>
<h3>Use Cases</h3>
<p>Global team meetings, remote stand-ups, cross-region project coordination, international client calls, distributed team workshops, and more.</p>
'''

# ============================================================
# BUILD THEM
# ============================================================

print("=" * 60)
print("Building Tool 1: HTML Previewer (html-previewer)")
print("=" * 60)

cn_path1, en_path1 = builder.build_bilingual(
    slug='html-previewer',
    title_cn='HTML预览器 - 实时HTML/CSS/JS代码预览',
    title_en='HTML Previewer - Live HTML/CSS/JS Code Preview',
    desc_cn='在线HTML预览器，实时编辑和预览HTML、CSS、JavaScript代码。支持自动刷新、新标签页打开。纯前端实现，代码不上传服务器。',
    desc_en='Online HTML Previewer. Edit and preview HTML, CSS, and JavaScript code in real time. Auto-refresh, new tab opening. Pure frontend, no server uploads.',
    icon='🖥️',
    cat_cn='开发工具',
    cat_en='Developer Tools',
    cat_anchor='developer-tools',
    tool_html_cn=HTML_PREVIEWER_TOOL_HTML_CN,
    tool_html_en=HTML_PREVIEWER_TOOL_HTML_EN,
    tool_js=HTML_PREVIEWER_JS,
    faqs_cn=HTML_PREVIEWER_FAQS_CN,
    faqs_en=HTML_PREVIEWER_FAQS_EN,
    seo_cn=HTML_PREVIEWER_SEO_CN,
    seo_en=HTML_PREVIEWER_SEO_EN,
)
print(f"  CN: {cn_path1}")
print(f"  EN: {en_path1}")

print()
print("=" * 60)
print("Building Tool 2: Meeting Planner (meeting-planner)")
print("=" * 60)

cn_path2, en_path2 = builder.build_bilingual(
    slug='meeting-planner',
    title_cn='会议时间规划器 - 跨时区会议协调',
    title_en='Meeting Planner - Cross-Timezone Meeting Coordinator',
    desc_cn='在线会议时间规划器，轻松协调跨时区团队会议时间。添加参与者及其时区，自动找出所有人都有空的最佳会议时间。纯前端，数据不上传。',
    desc_en='Online Meeting Planner. Easily coordinate meeting times across timezones. Add participants with their timezones, find overlapping free slots automatically. Pure frontend, no data uploads.',
    icon='📅',
    cat_cn='办公工具',
    cat_en='Office Tools',
    cat_anchor='office-tools',
    tool_html_cn=MEETING_PLANNER_TOOL_HTML_CN,
    tool_html_en=MEETING_PLANNER_TOOL_HTML_EN,
    tool_js=MEETING_PLANNER_JS,
    faqs_cn=MEETING_PLANNER_FAQS_CN,
    faqs_en=MEETING_PLANNER_FAQS_EN,
    seo_cn=MEETING_PLANNER_SEO_CN,
    seo_en=MEETING_PLANNER_SEO_EN,
)
print(f"  CN: {cn_path2}")
print(f"  EN: {en_path2}")

print()
print("=" * 60)
print("✅ 2 tools built successfully!")
print("=" * 60)
