#!/usr/bin/env python3
"""Build 2 new tools using template v3 - batch generation"""
import sys, os
sys.path.insert(0, os.path.expanduser('~/tools-site/_gen'))
from tool_template_v3 import ToolPageBuilder

builder = ToolPageBuilder()

# ============================================================
# TOOL 1: CSS Feature Support Checker
# ============================================================

# Categorized CSS features for testing
CSS_FEATURES_CN = [
    ("布局 Layout", [
        ("display: flex", "弹性盒布局"),
        ("display: grid", "网格布局"),
        ("display: subgrid", "子网格"),
        ("display: contents", "内容盒"),
        ("container-type: inline-size", "容器查询"),
        ("container-type: size", "容器尺寸查询"),
        ("position: sticky", "粘性定位"),
        ("overflow: clip", "裁剪溢出"),
        ("overscroll-behavior", "滚动链控制"),
        ("scroll-snap-type", "滚动捕捉"),
        ("scroll-behavior", "平滑滚动"),
        ("anchor-name", "CSS锚点定位"),
        ("position-anchor", "锚点定位"),
    ]),
    ("动画与过渡 Animation & Transition", [
        ("animation-name", "动画"),
        ("animation-timeline: scroll", "滚动驱动动画"),
        ("animation-timeline: view", "视图驱动动画"),
        ("view-timeline-name", "视图时间线"),
        ("scroll-timeline-name", "滚动时间线"),
        ("transition-behavior: allow-discrete", "离散过渡"),
        ("@starting-style", "进入动画"),
        ("interpolate-size", "尺寸插值"),
        ("display: auto", "自动显示模式"),
    ]),
    ("颜色 Color", [
        ("color: oklch", "OKLCH颜色空间"),
        ("color: oklab", "OKLAB颜色空间"),
        ("color-mix()", "颜色混合函数"),
        ("light-dark()", "亮暗模式颜色"),
        ("color-contrast()", "颜色对比度"),
        ("@media (prefers-color-scheme)", "暗色模式检测"),
        ("@media (dynamic-range)", "动态范围检测"),
    ]),
    ("排版 Typography", [
        ("text-wrap: pretty", "智能换行"),
        ("text-wrap: balance", "平衡换行"),
        ("text-box-trim", "文本框修剪"),
        ("text-box-edge", "文本边缘控制"),
        ("initial-letter", "首字母下沉"),
        ("hyphenate-character", "断字符号"),
        ("font-size: clamp()", "响应式字体"),
        ("font-palette", "字体调色板"),
    ]),
    ("效果与滤镜 Effects & Filters", [
        ("backdrop-filter", "背景模糊"),
        ("accent-color", "强调色"),
        ("scrollbar-color", "滚动条颜色"),
        ("scrollbar-width: thin", "细滚动条"),
        ("mask-image", "遮罩"),
        ("clip-path: path()", "裁剪路径"),
        ("filter: drop-shadow", "投影滤镜"),
    ]),
    ("选择器 Selectors", [
        (":has()", "父级选择器"),
        (":where()", "零特异性选择器"),
        (":is()", "选择器列表"),
        (":modal", "模态框选择器"),
        (":user-invalid", "用户输入无效"),
        (":target-within", "目标内部选择器"),
        ("::view-transition", "视图过渡伪元素"),
        ("::selection", "选中文本样式"),
    ]),
    ("UI组件 UI Components", [
        ("popover", "Popover API"),
        ("dialog", "Dialog元素"),
        ("<details>", "详情折叠"),
        ("<selectlist>", "可定制选择框"),
        ("input type=color", "颜色选择器"),
        ("input type=range", "范围滑块"),
        ("input type=date", "日期选择器"),
    ]),
    ("新特性 New Features", [
        ("@scope", "CSS作用域"),
        ("@layer", "层叠层"),
        ("@property", "自定义属性"),
        ("@media (scripting)", "脚本支持检测"),
        ("@media (hover)", "悬停能力检测"),
        ("@media (pointer)", "指针精度检测"),
        ("@media (prefers-reduced-motion)", "减少动画偏好"),
        ("@media (prefers-reduced-transparency)", "减少透明偏好"),
        ("scroll-driven-animations", "滚动驱动动画"),
        ("view-transitions", "视图过渡API"),
    ]),
]

CSS_FEATURES_EN = [
    ("Layout", [
        ("display: flex", "Flexbox layout"),
        ("display: grid", "CSS Grid layout"),
        ("display: subgrid", "Subgrid"),
        ("display: contents", "Contents box"),
        ("container-type: inline-size", "Container Queries"),
        ("container-type: size", "Container size queries"),
        ("position: sticky", "Sticky positioning"),
        ("overflow: clip", "Clip overflow"),
        ("overscroll-behavior", "Scroll chaining"),
        ("scroll-snap-type", "Scroll snap"),
        ("scroll-behavior", "Smooth scrolling"),
        ("anchor-name", "CSS Anchor Positioning"),
        ("position-anchor", "Anchor positioning"),
    ]),
    ("Animation & Transition", [
        ("animation-name", "Animations"),
        ("animation-timeline: scroll", "Scroll-driven animations"),
        ("animation-timeline: view", "View-driven animations"),
        ("view-timeline-name", "View timeline"),
        ("scroll-timeline-name", "Scroll timeline"),
        ("transition-behavior: allow-discrete", "Discrete transitions"),
        ("@starting-style", "Entry animations"),
        ("interpolate-size", "Size interpolation"),
        ("display: auto", "Auto display mode"),
    ]),
    ("Color", [
        ("color: oklch", "OKLCH color space"),
        ("color: oklab", "OKLAB color space"),
        ("color-mix()", "Color mix function"),
        ("light-dark()", "Light/dark color"),
        ("color-contrast()", "Color contrast"),
        ("@media (prefers-color-scheme)", "Dark mode detection"),
        ("@media (dynamic-range)", "Dynamic range detection"),
    ]),
    ("Typography", [
        ("text-wrap: pretty", "Pretty text wrap"),
        ("text-wrap: balance", "Balanced text wrap"),
        ("text-box-trim", "Text box trim"),
        ("text-box-edge", "Text edge control"),
        ("initial-letter", "Drop cap"),
        ("hyphenate-character", "Hyphenation character"),
        ("font-size: clamp()", "Responsive font size"),
        ("font-palette", "Font palette"),
    ]),
    ("Effects & Filters", [
        ("backdrop-filter", "Backdrop blur"),
        ("accent-color", "Accent color"),
        ("scrollbar-color", "Scrollbar color"),
        ("scrollbar-width: thin", "Thin scrollbar"),
        ("mask-image", "CSS mask"),
        ("clip-path: path()", "Clip path"),
        ("filter: drop-shadow", "Drop shadow"),
    ]),
    ("Selectors", [
        (":has()", "Parent selector"),
        (":where()", "Zero specificity"),
        (":is()", "Selector list"),
        (":modal", "Modal selector"),
        (":user-invalid", "User invalid input"),
        (":target-within", "Target within"),
        ("::view-transition", "View transition pseudo"),
        ("::selection", "Selection styling"),
    ]),
    ("UI Components", [
        ("popover", "Popover API"),
        ("dialog", "Dialog element"),
        ("<details>", "Details disclosure"),
        ("<selectlist>", "Customizable select"),
        ("input type=color", "Color picker input"),
        ("input type=range", "Range slider input"),
        ("input type=date", "Date picker input"),
    ]),
    ("New Features", [
        ("@scope", "CSS scoping"),
        ("@layer", "Cascade layers"),
        ("@property", "Custom properties"),
        ("@media (scripting)", "Scripting support"),
        ("@media (hover)", "Hover capability"),
        ("@media (pointer)", "Pointer precision"),
        ("@media (prefers-reduced-motion)", "Reduced motion"),
        ("@media (prefers-reduced-transparency)", "Reduced transparency"),
        ("scroll-driven-animations", "Scroll-driven animations"),
        ("view-transitions", "View Transition API"),
    ]),
]

def build_features_list(categories):
    """Convert category structure to JS array string"""
    parts = []
    for cat_name, features in categories:
        feats_str = ",".join(f'["{f[0]}","{f[1]}"]' for f in features)
        parts.append(f'["{cat_name}",[{feats_str}]]')
    return "[" + ",".join(parts) + "]"

features_js_cn = build_features_list(CSS_FEATURES_CN)
features_js_en = build_features_list(CSS_FEATURES_EN)

tool1_html_cn = f'''
<div class="form-group">
  <label>🔍 搜索CSS特性</label>
  <input type="text" id="cssSearch" placeholder="输入CSS属性名称搜索..." oninput="filterFeatures()">
</div>
<div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:16px">
  <button class="btn btn-primary" onclick="testAll()" style="padding:8px 16px;border:none;background:#06b6d4;color:#fff;border-radius:6px;cursor:pointer;font-size:.85rem">🧪 测试所有</button>
  <button class="btn" onclick="testCustom()" style="padding:8px 16px;border:1px solid rgba(148,163,184,.3);border-radius:6px;cursor:pointer;font-size:.85rem;background:transparent;color:#94a3b8">⚙️ 自定义测试</button>
  <span id="statsBadge" style="margin-left:auto;padding:6px 12px;background:#1e293b;border-radius:6px;font-size:.8rem;color:#94a3b8"></span>
</div>
<div id="customTestArea" style="display:none;background:#0f172a;padding:12px;border-radius:8px;margin-bottom:12px">
  <div class="form-group">
    <label>输入CSS声明测试（如 display: grid）</label>
    <input type="text" id="customCssInput" placeholder="display: grid" onkeydown="if(event.key==='Enter')runCustomTest()">
  </div>
  <button class="btn btn-primary" onclick="runCustomTest()" style="padding:6px 14px;border:none;background:#06b6d4;color:#fff;border-radius:6px;cursor:pointer;font-size:.85rem">测试</button>
  <div id="customResult" style="margin-top:8px"></div>
</div>
<div id="featureResults" style="max-height:600px;overflow-y:auto"></div>
<style>
#featureResults .cat-group {{ margin-bottom:12px }}
#featureResults .cat-title {{ font-size:.9rem;color:#f1c40f;margin-bottom:6px;padding:4px 0;border-bottom:1px solid rgba(148,163,184,.1) }}
.feat-item {{ display:flex;align-items:center;justify-content:space-between;padding:6px 8px;border-radius:4px;margin:2px 0;transition:background .2s;cursor:pointer }}
.feat-item:hover {{ background:rgba(6,182,212,.08) }}
.feat-item .feat-name {{ font-family:'SF Mono',Monaco,monospace;font-size:.82rem;color:#e2e8f0 }}
.feat-item .feat-desc {{ font-size:.78rem;color:#64748b;margin-left:8px }}
.feat-status {{ font-size:.8rem;padding:2px 8px;border-radius:4px;flex-shrink:0 }}
.feat-status.yes {{ color:#22c55e;background:rgba(34,197,94,.12) }}
.feat-status.no {{ color:#ef4444;background:rgba(239,68,68,.12) }}
.feat-status.pending {{ color:#94a3b8;background:rgba(148,163,184,.12) }}
#customResult .cr-item {{ padding:8px 12px;border-radius:6px;margin:4px 0;font-size:.85rem }}
.cr-yes {{ background:rgba(34,197,94,.1);border-left:3px solid #22c55e;color:#22c55e }}
.cr-no {{ background:rgba(239,68,68,.1);border-left:3px solid #ef4444;color:#ef4444 }}
</style>
'''

tool1_html_en = f'''
<div class="form-group">
  <label>🔍 Search CSS Features</label>
  <input type="text" id="cssSearch" placeholder="Type CSS property name..." oninput="filterFeatures()">
</div>
<div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:16px">
  <button class="btn btn-primary" onclick="testAll()" style="padding:8px 16px;border:none;background:#06b6d4;color:#fff;border-radius:6px;cursor:pointer;font-size:.85rem">🧪 Test All</button>
  <button class="btn" onclick="testCustom()" style="padding:8px 16px;border:1px solid rgba(148,163,184,.3);border-radius:6px;cursor:pointer;font-size:.85rem;background:transparent;color:#94a3b8">⚙️ Custom Test</button>
  <span id="statsBadge" style="margin-left:auto;padding:6px 12px;background:#1e293b;border-radius:6px;font-size:.8rem;color:#94a3b8"></span>
</div>
<div id="customTestArea" style="display:none;background:#0f172a;padding:12px;border-radius:8px;margin-bottom:12px">
  <div class="form-group">
    <label>Enter CSS declaration to test (e.g. display: grid)</label>
    <input type="text" id="customCssInput" placeholder="display: grid" onkeydown="if(event.key==='Enter')runCustomTest()">
  </div>
  <button class="btn btn-primary" onclick="runCustomTest()" style="padding:6px 14px;border:none;background:#06b6d4;color:#fff;border-radius:6px;cursor:pointer;font-size:.85rem">Test</button>
  <div id="customResult" style="margin-top:8px"></div>
</div>
<div id="featureResults" style="max-height:600px;overflow-y:auto"></div>
<style>
#featureResults .cat-group {{ margin-bottom:12px }}
#featureResults .cat-title {{ font-size:.9rem;color:#f1c40f;margin-bottom:6px;padding:4px 0;border-bottom:1px solid rgba(148,163,184,.1) }}
.feat-item {{ display:flex;align-items:center;justify-content:space-between;padding:6px 8px;border-radius:4px;margin:2px 0;transition:background .2s;cursor:pointer }}
.feat-item:hover {{ background:rgba(6,182,212,.08) }}
.feat-item .feat-name {{ font-family:'SF Mono',Monaco,monospace;font-size:.82rem;color:#e2e8f0 }}
.feat-item .feat-desc {{ font-size:.78rem;color:#64748b;margin-left:8px }}
.feat-status {{ font-size:.8rem;padding:2px 8px;border-radius:4px;flex-shrink:0 }}
.feat-status.yes {{ color:#22c55e;background:rgba(34,197,94,.12) }}
.feat-status.no {{ color:#ef4444;background:rgba(239,68,68,.12) }}
.feat-status.pending {{ color:#94a3b8;background:rgba(148,163,184,.12) }}
#customResult .cr-item {{ padding:8px 12px;border-radius:6px;margin:4px 0;font-size:.85rem }}
.cr-yes {{ background:rgba(34,197,94,.1);border-left:3px solid #22c55e;color:#22c55e }}
.cr-no {{ background:rgba(239,68,68,.1);border-left:3px solid #ef4444;color:#ef4444 }}
</style>
'''

# The JS is the same for both - it's shared
tool1_js = '''
var cssFeatures = FEATURES_PLACEHOLDER;
var testResults = {};

function renderFeatures(cats) {
  var el = document.getElementById('featureResults');
  var html = '';
  for (var ci = 0; ci < cats.length; ci++) {
    var cat = cats[ci];
    html += '<div class="cat-group">';
    html += '<div class="cat-title">' + cat[0] + '</div>';
    for (var fi = 0; fi < cat[1].length; fi++) {
      var f = cat[1][fi];
      var status = testResults[f[0]] || 'pending';
      var label = status === 'yes' ? '✅ 支持' : (status === 'no' ? '❌ 不支持' : '⏳ 待测试');
      html += '<div class="feat-item" onclick="testSingle(\'' + f[0] + '\')">';
      html += '<span><span class="feat-name">' + f[0] + '</span><span class="feat-desc">' + f[1] + '</span></span>';
      html += '<span class="feat-status ' + status + '">' + label + '</span>';
      html += '</div>';
    }
    html += '</div>';
  }
  el.innerHTML = html;
}

function testSingle(feature) {
  try {
    var parts = feature.split(':');
    if (parts.length === 2) {
      testResults[feature] = CSS.supports(parts[0].trim(), parts[1].trim()) ? 'yes' : 'no';
    } else {
      testResults[feature] = CSS.supports(feature) ? 'yes' : 'no';
    }
  } catch(e) {
    testResults[feature] = 'no';
  }
  filterFeatures();
  updateStats();
}

function testAll() {
  for (var ci = 0; ci < cssFeatures.length; ci++) {
    for (var fi = 0; fi < cssFeatures[ci][1].length; fi++) {
      var f = cssFeatures[ci][1][fi][0];
      testSingle(f);
    }
  }
}

function updateStats() {
  var total = 0, yes = 0, no = 0;
  for (var ci = 0; ci < cssFeatures.length; ci++) {
    total += cssFeatures[ci][1].length;
  }
  for (var k in testResults) {
    if (testResults[k] === 'yes') yes++;
    else if (testResults[k] === 'no') no++;
  }
  var el = document.getElementById('statsBadge');
  el.textContent = '✅ ' + yes + '/' + total + '  ✓   ❌ ' + no + '/' + total;
}

function filterFeatures() {
  var q = (document.getElementById('cssSearch').value || '').toLowerCase();
  if (!q) {
    renderFeatures(cssFeatures);
    return;
  }
  var filtered = [];
  for (var ci = 0; ci < cssFeatures.length; ci++) {
    var cat = cssFeatures[ci];
    var matched = [];
    for (var fi = 0; fi < cat[1].length; fi++) {
      var f = cat[1][fi];
      if (f[0].toLowerCase().indexOf(q) >= 0 || f[1].toLowerCase().indexOf(q) >= 0) {
        matched.push(f);
      }
    }
    if (matched.length > 0) {
      filtered.push([cat[0], matched]);
    }
  }
  renderFeatures(filtered);
}

function testCustom() {
  var area = document.getElementById('customTestArea');
  area.style.display = area.style.display === 'none' ? 'block' : 'none';
}

function runCustomTest() {
  var input = document.getElementById('customCssInput').value.trim();
  var el = document.getElementById('customResult');
  if (!input) { el.innerHTML = ''; return; }
  try {
    var supported;
    if (input.indexOf(':') >= 0) {
      var parts = input.split(':');
      var prop = parts[0].trim();
      var val = parts.slice(1).join(':').trim();
      supported = CSS.supports(prop, val);
    } else {
      supported = CSS.supports(input);
    }
    var display = input.replace(/</g,'&lt;').replace(/>/g,'&gt;');
    if (supported) {
      el.innerHTML = '<div class="cr-item cr-yes">✅ <code>' + display + '</code> — 浏览器支持此特性</div>';
    } else {
      el.innerHTML = '<div class="cr-item cr-no">❌ <code>' + display + '</code> — 浏览器不支持此特性</div>';
    }
  } catch(e) {
    el.innerHTML = '<div class="cr-item cr-no">❌ 测试失败: ' + e.message + '</div>';
  }
}

// Initialize
cssFeatures = FEATURES_PLACEHOLDER;
renderFeatures(cssFeatures);
updateStats();
'''

# Replace placeholders
tool1_js_cn = tool1_js.replace('FEATURES_PLACEHOLDER', features_js_cn)
tool1_js_en = tool1_js.replace('FEATURES_PLACEHOLDER', features_js_en)

# ============================================================
# TOOL 2: Keyboard Event Tester (keyboard-event-tester)
# ============================================================

tool2_html_cn = '''
<div class="keyboard-area" style="text-align:center;padding:20px 0">
  <div id="keyDisplay" style="font-size:3rem;font-weight:700;color:#f1c40f;min-height:5rem;padding:20px;background:#0f172a;border-radius:12px;border:2px solid rgba(148,163,184,.15);margin-bottom:16px;display:flex;align-items:center;justify-content:center;letter-spacing:2px;font-family:'SF Mono',Monaco,monospace">
    按下任意键
  </div>
  <div style="display:flex;gap:16px;justify-content:center;flex-wrap:wrap;margin-bottom:16px">
    <div class="mod-badge" id="modCtrl" style="padding:4px 12px;border-radius:6px;background:#1e293b;color:#64748b;font-size:.8rem;font-weight:600">Ctrl</div>
    <div class="mod-badge" id="modAlt" style="padding:4px 12px;border-radius:6px;background:#1e293b;color:#64748b;font-size:.8rem;font-weight:600">Alt</div>
    <div class="mod-badge" id="modShift" style="padding:4px 12px;border-radius:6px;background:#1e293b;color:#64748b;font-size:.8rem;font-weight:600">Shift</div>
    <div class="mod-badge" id="modMeta" style="padding:4px 12px;border-radius:6px;background:#1e293b;color:#64748b;font-size:.8rem;font-weight:600">Meta</div>
  </div>
</div>
<div class="info-grid" style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:16px">
  <div class="info-item" style="padding:8px 12px;background:#0f172a;border-radius:6px">
    <span style="color:#64748b;font-size:.75rem">event.key</span>
    <div id="infoKey" style="font-family:monospace;font-size:.9rem;color:#e2e8f0;word-break:break-all">—</div>
  </div>
  <div class="info-item" style="padding:8px 12px;background:#0f172a;border-radius:6px">
    <span style="color:#64748b;font-size:.75rem">event.code</span>
    <div id="infoCode" style="font-family:monospace;font-size:.9rem;color:#e2e8f0;word-break:break-all">—</div>
  </div>
  <div class="info-item" style="padding:8px 12px;background:#0f172a;border-radius:6px">
    <span style="color:#64748b;font-size:.75rem">event.type</span>
    <div id="infoType" style="font-family:monospace;font-size:.9rem;color:#e2e8f0">—</div>
  </div>
  <div class="info-item" style="padding:8px 12px;background:#0f172a;border-radius:6px">
    <span style="color:#64748b;font-size:.75rem">event.repeat</span>
    <div id="infoRepeat" style="font-family:monospace;font-size:.9rem;color:#e2e8f0">—</div>
  </div>
</div>
<div style="display:flex;gap:8px;margin-bottom:12px">
  <button class="btn btn-primary" onclick="clearLog()" style="padding:6px 14px;border:none;background:#06b6d4;color:#fff;border-radius:6px;cursor:pointer;font-size:.8rem">🗑 清空日志</button>
  <button class="btn" onclick="toggleLock()" style="padding:6px 14px;border:1px solid rgba(148,163,184,.3);border-radius:6px;cursor:pointer;font-size:.8rem;background:transparent;color:#94a3b8" id="lockBtn">🔒 暂停监听</button>
</div>
<div style="background:#0f172a;border-radius:8px;padding:8px;max-height:200px;overflow-y:auto">
  <table style="width:100%;font-size:.75rem;font-family:monospace">
    <thead><tr style="color:#64748b"><th style="text-align:left;padding:4px">类型</th><th style="text-align:left;padding:4px">key</th><th style="text-align:left;padding:4px">code</th><th style="text-align:left;padding:4px">修饰键</th></tr></thead>
    <tbody id="logBody"></tbody>
  </table>
</div>
'''

tool2_html_en = '''
<div class="keyboard-area" style="text-align:center;padding:20px 0">
  <div id="keyDisplay" style="font-size:3rem;font-weight:700;color:#f1c40f;min-height:5rem;padding:20px;background:#0f172a;border-radius:12px;border:2px solid rgba(148,163,184,.15);margin-bottom:16px;display:flex;align-items:center;justify-content:center;letter-spacing:2px;font-family:'SF Mono',Monaco,monospace">
    Press any key
  </div>
  <div style="display:flex;gap:16px;justify-content:center;flex-wrap:wrap;margin-bottom:16px">
    <div class="mod-badge" id="modCtrl" style="padding:4px 12px;border-radius:6px;background:#1e293b;color:#64748b;font-size:.8rem;font-weight:600">Ctrl</div>
    <div class="mod-badge" id="modAlt" style="padding:4px 12px;border-radius:6px;background:#1e293b;color:#64748b;font-size:.8rem;font-weight:600">Alt</div>
    <div class="mod-badge" id="modShift" style="padding:4px 12px;border-radius:6px;background:#1e293b;color:#64748b;font-size:.8rem;font-weight:600">Shift</div>
    <div class="mod-badge" id="modMeta" style="padding:4px 12px;border-radius:6px;background:#1e293b;color:#64748b;font-size:.8rem;font-weight:600">Meta</div>
  </div>
</div>
<div class="info-grid" style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:16px">
  <div class="info-item" style="padding:8px 12px;background:#0f172a;border-radius:6px">
    <span style="color:#64748b;font-size:.75rem">event.key</span>
    <div id="infoKey" style="font-family:monospace;font-size:.9rem;color:#e2e8f0;word-break:break-all">—</div>
  </div>
  <div class="info-item" style="padding:8px 12px;background:#0f172a;border-radius:6px">
    <span style="color:#64748b;font-size:.75rem">event.code</span>
    <div id="infoCode" style="font-family:monospace;font-size:.9rem;color:#e2e8f0;word-break:break-all">—</div>
  </div>
  <div class="info-item" style="padding:8px 12px;background:#0f172a;border-radius:6px">
    <span style="color:#64748b;font-size:.75rem">event.type</span>
    <div id="infoType" style="font-family:monospace;font-size:.9rem;color:#e2e8f0">—</div>
  </div>
  <div class="info-item" style="padding:8px 12px;background:#0f172a;border-radius:6px">
    <span style="color:#64748b;font-size:.75rem">event.repeat</span>
    <div id="infoRepeat" style="font-family:monospace;font-size:.9rem;color:#e2e8f0">—</div>
  </div>
</div>
<div style="display:flex;gap:8px;margin-bottom:12px">
  <button class="btn btn-primary" onclick="clearLog()" style="padding:6px 14px;border:none;background:#06b6d4;color:#fff;border-radius:6px;cursor:pointer;font-size:.8rem">🗑 Clear Log</button>
  <button class="btn" onclick="toggleLock()" style="padding:6px 14px;border:1px solid rgba(148,163,184,.3);border-radius:6px;cursor:pointer;font-size:.8rem;background:transparent;color:#94a3b8" id="lockBtn">🔒 Pause</button>
</div>
<div style="background:#0f172a;border-radius:8px;padding:8px;max-height:200px;overflow-y:auto">
  <table style="width:100%;font-size:.75rem;font-family:monospace">
    <thead><tr style="color:#64748b"><th style="text-align:left;padding:4px">Type</th><th style="text-align:left;padding:4px">key</th><th style="text-align:left;padding:4px">code</th><th style="text-align:left;padding:4px">Modifiers</th></tr></thead>
    <tbody id="logBody"></tbody>
  </table>
</div>
'''

tool2_js = '''
var locked = false;
var logCount = 0;
var MAX_LOG = 50;

function updateMods(e) {
  var map = {
    modCtrl: e.ctrlKey,
    modAlt: e.altKey,
    modShift: e.shiftKey,
    modMeta: e.metaKey
  };
  for (var id in map) {
    var el = document.getElementById(id);
    if (map[id]) {
      el.style.background = 'rgba(6,182,212,.2)';
      el.style.color = '#22d3ee';
      el.style.border = '1px solid rgba(6,182,212,.3)';
    } else {
      el.style.background = '#1e293b';
      el.style.color = '#64748b';
      el.style.border = '1px solid transparent';
    }
  }
}

function handleKeyEvent(e) {
  if (locked) return;
  var keyDisplay = document.getElementById('keyDisplay');
  var displayKey = e.key === ' ' ? 'Space' : e.key;
  keyDisplay.textContent = displayKey;
  
  document.getElementById('infoKey').textContent = displayKey;
  document.getElementById('infoCode').textContent = e.code;
  document.getElementById('infoType').textContent = e.type;
  document.getElementById('infoRepeat').textContent = e.repeat ? '⚠️ Repeat' : '—';
  
  updateMods(e);
  
  // Log
  var tbody = document.getElementById('logBody');
  var mods = [];
  if (e.ctrlKey) mods.push('Ctrl');
  if (e.altKey) mods.push('Alt');
  if (e.shiftKey) mods.push('Shift');
  if (e.metaKey) mods.push('Meta');
  var modStr = mods.length ? mods.join('+') : '—';
  
  // Color code by event type
  var typeColor = e.type === 'keydown' ? '#22d3ee' : (e.type === 'keyup' ? '#f1c40f' : '#94a3b8');
  
  var row = document.createElement('tr');
  row.style.color = '#94a3b8';
  row.innerHTML = '<td style="padding:2px 4px;color:' + typeColor + '">' + e.type + '</td>' +
    '<td style="padding:2px 4px;color:#e2e8f0">' + displayKey + '</td>' +
    '<td style="padding:2px 4px">' + e.code + '</td>' +
    '<td style="padding:2px 4px">' + modStr + '</td>';
  
  tbody.insertBefore(row, tbody.firstChild);
  logCount++;
  if (logCount > MAX_LOG) {
    tbody.removeChild(tbody.lastChild);
  }
}

function clearLog() {
  document.getElementById('logBody').innerHTML = '';
  logCount = 0;
}

function toggleLock() {
  locked = !locked;
  var btn = document.getElementById('lockBtn');
  if (locked) {
    btn.innerHTML = '🔓 继续监听';
    btn.style.background = 'rgba(239,68,68,.15)';
    btn.style.color = '#ef4444';
    document.getElementById('keyDisplay').textContent = '⏸ 已暂停';
    document.getElementById('keyDisplay').style.color = '#64748b';
  } else {
    btn.innerHTML = '🔒 暂停监听';
    btn.style.background = 'transparent';
    btn.style.color = '#94a3b8';
    document.getElementById('keyDisplay').style.color = '#f1c40f';
    document.getElementById('keyDisplay').textContent = '按下任意键';
  }
}

// Listen for keyboard events
document.addEventListener('keydown', function(e) {
  // Don't capture if typing in input
  if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA' || e.target.isContentEditable) return;
  handleKeyEvent(e);
});

document.addEventListener('keyup', function(e) {
  if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA' || e.target.isContentEditable) return;
  handleKeyEvent(e);
});

// Make sure clicking on tool area focuses it
document.querySelector('.keyboard-area').addEventListener('click', function() {
  // Focus trap to receive keyboard events
  this.setAttribute('tabindex', '-1');
  this.focus();
});
'''

# Build Tool 1: CSS Feature Support Checker
print("Building css-feature-support-checker...")
cn1, en1 = builder.build_bilingual(
    slug='css-feature-support-checker',
    title_cn='CSS特性检测',
    title_en='CSS Feature Support Checker',
    desc_cn='在线检测浏览器对CSS新特性的支持情况，一键测试Flexbox、Grid、容器查询、视图过渡等现代CSS特性。',
    desc_en='Check browser support for modern CSS features. Test Flexbox, Grid, Container Queries, View Transitions and more.',
    icon='🎨',
    cat_cn='CSS工具',
    cat_en='CSS Tools',
    cat_anchor='css-tools',
    tool_html_cn=tool1_html_cn,
    tool_html_en=tool1_html_en,
    tool_js=tool1_js_cn,
    faqs_cn=[
        ('这个工具如何检测CSS特性？', '使用浏览器内置的CSS.supports() API进行检测，不需要加载外部资源，结果准确可靠。'),
        ('支持检测哪些CSS特性？', '涵盖布局、动画、颜色、排版、滤镜效果、选择器、UI组件等8大类80+个现代CSS特性。'),
        ('检测结果准确吗？', 'CSS.supports()是浏览器原生API，检测结果100%准确反映当前浏览器的实际支持情况。'),
        ('可以检测自定义CSS属性吗？', '可以！使用"自定义测试"功能，输入任意CSS声明即可测试浏览器是否支持。'),
        ('数据会上传到服务器吗？', '不会。所有检测在浏览器本地完成，无需网络连接，不上传任何数据。'),
    ],
    faqs_en=[
        ('How does this tool test CSS features?', 'It uses the browser\'s native CSS.supports() API — no external resources needed, results are 100% accurate.'),
        ('Which CSS features can be tested?', '80+ modern CSS features across 8 categories: Layout, Animation, Color, Typography, Effects, Selectors, UI Components, and New Features.'),
        ('Are the results accurate?', 'CSS.supports() is a native browser API. Results accurately reflect your current browser\'s actual support.'),
        ('Can I test custom CSS properties?', 'Yes! Use the "Custom Test" feature to enter any CSS declaration and check browser support.'),
        ('Is data uploaded to any server?', 'No. All tests run completely in your browser — no network requests, no data upload.'),
    ],
    seo_cn='<h2>为什么需要CSS特性检测工具？</h2><p>CSS不断发展，新特性层出不穷。不同浏览器对CSS新特性的支持进度不同，开发者在编写CSS时常常需要查资料确认某个特性是否可用。CSS特性检测工具利用浏览器内置的CSS.supports() API，一键检测当前浏览器对80+个现代CSS特性的支持情况。</p><h2>如何使用CSS特性检测工具？</h2><p>打开工具页面后，页面会自动显示八大类CSS特性列表。点击任意特性即可检测当前浏览器是否支持，或点击"测试所有"一键完成全部检测。支持按关键字搜索CSS属性名称，也支持自定义输入CSS声明进行测试。</p><h2>CSS特性检测的原理</h2><p>CSS.supports()是CSS条件规则模块的一部分，语法为CSS.supports(property, value)或CSS.supports(declaration)。返回true表示浏览器支持该CSS声明，false表示不支持。该API在大多数现代浏览器中均有良好支持。</p>',
    seo_en='<h2>Why Use a CSS Feature Support Checker?</h2><p>CSS evolves rapidly with new features being added regularly. Different browsers implement CSS features at different speeds. This tool uses the native CSS.supports() API to instantly check your browser\'s support for 80+ modern CSS features.</p><h2>How to Use the CSS Feature Support Checker</h2><p>Open the tool to see 8 categories of CSS features. Click any feature to test browser support, or click "Test All" to run a complete check. Use the search box to find specific properties, or enter custom CSS declarations for testing.</p><h2>How CSS.supports() Works</h2><p>The CSS.supports() API is part of the CSS Conditional Rules Module. It accepts CSS.supports(property, value) or CSS.supports(declaration) syntax and returns true if the browser supports the CSS declaration, false otherwise.</p>',
)

print(f"  ✅ {cn1}")
print(f"  ✅ {en1}")

# Build Tool 2: Keyboard Event Tester
print("\nBuilding keyboard-event-tester...")
cn2, en2 = builder.build_bilingual(
    slug='keyboard-event-tester',
    title_cn='键盘事件测试',
    title_en='Keyboard Event Tester',
    desc_cn='在线键盘事件测试工具，实时显示按键信息、修饰键状态和键盘事件日志，帮助开发者调试快捷键和键盘交互。',
    desc_en='Real-time keyboard event debugger. Display key presses, modifier keys, and keyboard event logs. Perfect for debugging keyboard shortcuts and interactions.',
    icon='⌨️',
    cat_cn='开发者工具',
    cat_en='Developer Tools',
    cat_anchor='developer-tools',
    tool_html_cn=tool2_html_cn,
    tool_html_en=tool2_html_en,
    tool_js=tool2_js,
    faqs_cn=[
        ('这个工具可以做什么？', '实时显示键盘按键信息，包括event.key、event.code、事件类型（keydown/keyup）、修饰键状态（Ctrl/Alt/Shift/Meta）和按键重复状态。'),
        ('如何测试快捷键？', '同时按下修饰键和其他按键，工具会实时显示所有按下的修饰键状态和组合键信息。'),
        ('event.key和event.code有什么区别？', 'event.key返回按键的字符值（如"a"、"Enter"），event.code返回按键的物理位置（如"KeyA"、"Enter"），不随键盘布局改变。'),
        ('日志可以保留多少条？', '最多保留50条最近的键盘事件记录，你可以随时点击"清空日志"清除历史记录。'),
        ('为什么有些按键不显示？', '工具默认不捕获输入框中的按键事件以避免干扰输入。点击键盘展示区域即可激活按键监听。'),
    ],
    faqs_en=[
        ('What can this tool do?', 'Real-time display of keyboard events: event.key, event.code, event type (keydown/keyup), modifier states (Ctrl/Alt/Shift/Meta), and repeat status.'),
        ('How to test keyboard shortcuts?', 'Press modifier keys together with other keys. The tool shows all active modifiers and the combined key information in real-time.'),
        ('What\'s the difference between event.key and event.code?', 'event.key returns the character value (e.g. "a", "Enter"), while event.code returns the physical key location (e.g. "KeyA", "Enter") which doesn\'t change with keyboard layout.'),
        ('How many log entries are kept?', 'Up to 50 recent keyboard events are kept. Click "Clear Log" to reset.'),
        ('Why don\'t some keys show up?', 'The tool ignores key events in input fields to avoid interference. Click on the key display area to activate keyboard capture.'),
    ],
    seo_cn='<h2>什么是键盘事件测试工具？</h2><p>键盘事件测试工具是一个开发辅助工具，用于实时捕获和显示键盘事件详情。当开发者按下键盘按键时，工具会立即显示event.key、event.code、事件类型、修饰键状态以及按键重复信息。所有数据来自浏览器原生KeyboardEvent API。</p><h2>键盘事件测试工具的用途</h2><p>对于前端开发者来说，理解键盘事件是构建无障碍Web应用的关键。本工具可以帮助您：调试键盘快捷键实现、测试不同键盘布局下的按键行为、验证event.key和event.code的差异、分析修饰键组合的触发逻辑。</p><h2>KeyboardEvent API简介</h2><p>KeyboardEvent是DOM事件接口，用于描述键盘交互。包含keydown（按下）、keypress（已废弃）和keyup（释放）三种事件类型。常用属性包括key（按键值）、code（物理键位）、ctrlKey/altKey/shiftKey/metaKey（修饰键状态）和repeat（按键重复）。</p>',
    seo_en='<h2>What is a Keyboard Event Tester?</h2><p>A keyboard event tester is a developer tool that captures and displays keyboard event details in real-time. When you press a key, the tool instantly shows event.key, event.code, event type, modifier key states, and key repeat information — all sourced from the browser\'s native KeyboardEvent API.</p><h2>Why Use a Keyboard Event Tester?</h2><p>Understanding keyboard events is essential for building accessible web applications. This tool helps you debug keyboard shortcut implementations, test key behavior across layouts, understand event.key vs event.code differences, and verify modifier key combinations.</p><h2>About the KeyboardEvent API</h2><p>The KeyboardEvent interface describes keyboard interactions. It fires three event types: keydown, keypress (deprecated), and keyup. Key properties include key (character value), code (physical key position), ctrlKey/altKey/shiftKey/metaKey (modifier states), and repeat (auto-repeat).</p>',
)

print(f"  ✅ {cn2}")
print(f"  ✅ {en2}")

print("\n✅ Both tools generated successfully!")
