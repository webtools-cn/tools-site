#!/usr/bin/env python3
"""生成 css-loader-generator 和 progress-bar-generator 两个工具"""

import sys, os, json
sys.path.insert(0, os.path.expanduser('~/tools-site/_gen'))
from tool_template_v3 import ToolPageBuilder

builder = ToolPageBuilder()

# ============================================================
# 1. css-loader-generator
# ============================================================

CUSTOM_CSS_LOADER = '''
.loader-preview{background:#1e293b;border-radius:12px;padding:40px;display:flex;justify-content:center;align-items:center;min-height:200px;margin-bottom:20px;border:1px solid rgba(148,163,184,.1)}
.loader-controls{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.loader-controls .form-group{margin-bottom:0}
.code-output{background:#0f172a;border-radius:8px;padding:16px;font-family:"SF Mono","Cascadia Code",monospace;font-size:.82rem;white-space:pre-wrap;word-break:break-all;max-height:300px;overflow:auto;border:1px solid rgba(148,163,184,.1)}
.copy-btn{margin-top:8px;padding:8px 20px;background:rgba(6,182,212,.2);color:#22d3ee;border:1px solid rgba(6,182,212,.3);border-radius:6px;cursor:pointer;font-size:.85rem}
.copy-btn:hover{background:rgba(6,182,212,.3)}
/* Loader animations */
.loader-spinner{width:var(--l-size);height:var(--l-size);border:var(--l-border) solid rgba(255,255,255,.1);border-top-color:var(--l-color);border-radius:50%;animation:lspin var(--l-speed) linear infinite}
@keyframes lspin{to{transform:rotate(360deg)}}
.loader-dots{display:flex;gap:calc(var(--l-size)/3);align-items:center}
.loader-dots span{width:calc(var(--l-size)/3);height:calc(var(--l-size)/3);background:var(--l-color);border-radius:50%;animation:ldot var(--l-speed) ease-in-out infinite}
.loader-dots span:nth-child(2){animation-delay:.15s}
.loader-dots span:nth-child(3){animation-delay:.3s}
@keyframes ldot{0%,100%{transform:scale(.6);opacity:.4}50%{transform:scale(1);opacity:1}}
.loader-bars{display:flex;gap:4px;align-items:center;height:var(--l-size)}
.loader-bars span{width:calc(var(--l-size)/4);height:var(--l-size);background:var(--l-color);border-radius:3px;animation:lbar var(--l-speed) ease-in-out infinite}
.loader-bars span:nth-child(2){animation-delay:.1s;height:calc(var(--l-size)*.8)}
.loader-bars span:nth-child(3){animation-delay:.2s;height:calc(var(--l-size)*.6)}
.loader-bars span:nth-child(4){animation-delay:.3s;height:calc(var(--l-size)*.8)}
@keyframes lbar{0%,100%{transform:scaleY(.5);opacity:.5}50%{transform:scaleY(1);opacity:1}}
.loader-ring{width:var(--l-size);height:var(--l-size);display:flex;justify-content:center;align-items:center}
.loader-ring::after{content:"";display:block;width:var(--l-size);height:var(--l-size);border-radius:50%;border:var(--l-border) solid rgba(255,255,255,.1);border-top-color:var(--l-color);border-bottom-color:var(--l-color);animation:lring var(--l-speed) linear infinite}
@keyframes lring{to{transform:rotate(360deg)}}
.loader-pulse{width:var(--l-size);height:var(--l-size);background:var(--l-color);border-radius:50%;animation:lpulse var(--l-speed) ease-in-out infinite}
@keyframes lpulse{0%,100%{transform:scale(.8);opacity:.6}50%{transform:scale(1.2);opacity:1}}
.preview-grid{display:grid;grid-template-columns:repeat(5,1fr);gap:8px;margin-bottom:16px}
.preview-grid .type-btn{padding:8px 4px;text-align:center;border-radius:6px;cursor:pointer;font-size:.75rem;border:1px solid rgba(148,163,184,.15);background:#0f172a;color:#94a3b8;transition:all .2s}
.preview-grid .type-btn:hover{border-color:rgba(6,182,212,.3);color:#22d3ee}
.preview-grid .type-btn.active{background:rgba(6,182,212,.2);border-color:#22d3ee;color:#22d3ee}
.range-value{color:#22d3ee;font-weight:600}
input[type="color"]{width:100%;height:40px;padding:2px;border-radius:8px;cursor:pointer;background:#0f172a;border:1px solid rgba(148,163,184,.2)}
'''

TOOL_JS_LOADER = '''
var ls_types=['spinner','dots','bars','ring','pulse'];
var ls_type='spinner',ls_color='#22d3ee',ls_size=48,ls_speed=1,ls_border=4;

function updateLoader(){
  var p=document.getElementById('loader-preview');
  if(!p)return;
  var inner='';
  if(ls_type==='spinner') inner='<div class="loader-spinner"></div>';
  else if(ls_type==='dots') inner='<div class="loader-dots"><span></span><span></span><span></span></div>';
  else if(ls_type==='bars') inner='<div class="loader-bars"><span></span><span></span><span></span><span></span></div>';
  else if(ls_type==='ring') inner='<div class="loader-ring"></div>';
  else if(ls_type==='pulse') inner='<div class="loader-pulse"></div>';
  p.innerHTML=inner;
  p.style.setProperty('--l-color',ls_color);
  p.style.setProperty('--l-size',ls_size+'px');
  p.style.setProperty('--l-speed',ls_speed+'s');
  p.style.setProperty('--l-border',ls_border+'px');
  updateLoaderCode();
}

function setLoaderType(t){
  ls_type=t;
  document.querySelectorAll('.type-btn').forEach(function(b){b.classList.toggle('active',b.dataset.type===t)});
  updateLoader();
}

function updateLoaderCode(){
  var css='/* CSS Loader - '+ls_type+' */\\n';
  var lsize=ls_size,bd=ls_border,spd=ls_speed,clr=ls_color;
  if(ls_type==='spinner'){
    css+='.my-loader {\\n  width: '+lsize+'px;\\n  height: '+lsize+'px;\\n  border: '+bd+'px solid rgba(255,255,255,.1);\\n  border-top-color: '+clr+';\\n  border-radius: 50%;\\n  animation: lspin '+spd+'s linear infinite;\\n}\\n\\n@keyframes lspin {\\n  to { transform: rotate(360deg); }\\n}';
  }else if(ls_type==='dots'){
    var ds=Math.round(lsize/3);
    css+='.my-loader {\\n  display: flex;\\n  gap: '+ds+'px;\\n  align-items: center;\\n}\\n.my-loader span {\\n  width: '+ds+'px;\\n  height: '+ds+'px;\\n  background: '+clr+';\\n  border-radius: 50%;\\n  animation: ldot '+spd+'s ease-in-out infinite;\\n}\\n.my-loader span:nth-child(2) { animation-delay: .15s; }\\n.my-loader span:nth-child(3) { animation-delay: .3s; }\\n\\n@keyframes ldot {\\n  0%, 100% { transform: scale(.6); opacity: .4; }\\n  50% { transform: scale(1); opacity: 1; }\\n}';
  }else if(ls_type==='bars'){
    var bw=Math.round(lsize/4);
    css+='.my-loader {\\n  display: flex;\\n  gap: 4px;\\n  align-items: center;\\n  height: '+lsize+'px;\\n}\\n.my-loader span {\\n  width: '+bw+'px;\\n  background: '+clr+';\\n  border-radius: 3px;\\n  animation: lbar '+spd+'s ease-in-out infinite;\\n}\\n.my-loader span:nth-child(1) { height: '+lsize+'px; }\\n.my-loader span:nth-child(2) { height: '+Math.round(lsize*.8)+'px; animation-delay: .1s; }\\n.my-loader span:nth-child(3) { height: '+Math.round(lsize*.6)+'px; animation-delay: .2s; }\\n.my-loader span:nth-child(4) { height: '+Math.round(lsize*.8)+'px; animation-delay: .3s; }\\n\\n@keyframes lbar {\\n  0%, 100% { transform: scaleY(.5); opacity: .5; }\\n  50% { transform: scaleY(1); opacity: 1; }\\n}';
  }else if(ls_type==='ring'){
    css+='.my-loader {\\n  width: '+lsize+'px;\\n  height: '+lsize+'px;\\n  border-radius: 50%;\\n  border: '+bd+'px solid rgba(255,255,255,.1);\\n  border-top-color: '+clr+';\\n  border-bottom-color: '+clr+';\\n  animation: lring '+spd+'s linear infinite;\\n}\\n\\n@keyframes lring {\\n  to { transform: rotate(360deg); }\\n}';
  }else if(ls_type==='pulse'){
    css+='.my-loader {\\n  width: '+lsize+'px;\\n  height: '+lsize+'px;\\n  background: '+clr+';\\n  border-radius: 50%;\\n  animation: lpulse '+spd+'s ease-in-out infinite;\\n}\\n\\n@keyframes lpulse {\\n  0%, 100% { transform: scale(.8); opacity: .6; }\\n  50% { transform: scale(1.2); opacity: 1; }\\n}';
  }
  document.getElementById('loader-code').textContent=css;
}

function copyLoaderCode(){
  var code=document.getElementById('loader-code').textContent;
  navigator.clipboard.writeText(code).then(function(){showToast('Copied')}).catch(function(){showToast('Copy failed')});
}
'''

TOOL_HTML_LOADER_CN = '''
<div>
  <div class="loader-preview" id="loader-preview"><div class="loader-spinner"></div></div>
  <div class="preview-grid" id="type-grid">
    <div class="type-btn active" data-type="spinner" onclick="setLoaderType('spinner')">Spinner</div>
    <div class="type-btn" data-type="dots" onclick="setLoaderType('dots')">Dots</div>
    <div class="type-btn" data-type="bars" onclick="setLoaderType('bars')">Bars</div>
    <div class="type-btn" data-type="ring" onclick="setLoaderType('ring')">Ring</div>
    <div class="type-btn" data-type="pulse" onclick="setLoaderType('pulse')">Pulse</div>
  </div>
  <div class="loader-controls">
    <div class="form-group">
      <label>颜色</label>
      <input type="color" id="loader-color" value="#22d3ee" onchange="ls_color=this.value;updateLoader()">
    </div>
    <div class="form-group">
      <label>大小: <span class="range-value" id="size-val">48px</span></label>
      <input type="range" min="20" max="100" value="48" oninput="ls_size=parseInt(this.value);document.getElementById('size-val').textContent=this.value+'px';updateLoader()">
    </div>
    <div class="form-group">
      <label>速度: <span class="range-value" id="speed-val">1s</span></label>
      <input type="range" min="0.2" max="3" step="0.1" value="1" oninput="ls_speed=parseFloat(this.value);document.getElementById('speed-val').textContent=this.value+'s';updateLoader()">
    </div>
    <div class="form-group">
      <label>边框: <span class="range-value" id="border-val">4px</span></label>
      <input type="range" min="2" max="12" value="4" oninput="ls_border=parseInt(this.value);document.getElementById('border-val').textContent=this.value+'px';updateLoader()">
    </div>
  </div>
  <div style="margin-top:16px">
    <label>CSS 代码</label>
    <div class="code-output" id="loader-code">/* CSS Loader - spinner */</div>
    <button class="copy-btn" onclick="copyLoaderCode()">📋 复制代码</button>
  </div>
</div>
'''

TOOL_HTML_LOADER_EN = '''
<div>
  <div class="loader-preview" id="loader-preview"><div class="loader-spinner"></div></div>
  <div class="preview-grid" id="type-grid">
    <div class="type-btn active" data-type="spinner" onclick="setLoaderType('spinner')">Spinner</div>
    <div class="type-btn" data-type="dots" onclick="setLoaderType('dots')">Dots</div>
    <div class="type-btn" data-type="bars" onclick="setLoaderType('bars')">Bars</div>
    <div class="type-btn" data-type="ring" onclick="setLoaderType('ring')">Ring</div>
    <div class="type-btn" data-type="pulse" onclick="setLoaderType('pulse')">Pulse</div>
  </div>
  <div class="loader-controls">
    <div class="form-group">
      <label>Color</label>
      <input type="color" id="loader-color" value="#22d3ee" onchange="ls_color=this.value;updateLoader()">
    </div>
    <div class="form-group">
      <label>Size: <span class="range-value" id="size-val">48px</span></label>
      <input type="range" min="20" max="100" value="48" oninput="ls_size=parseInt(this.value);document.getElementById('size-val').textContent=this.value+'px';updateLoader()">
    </div>
    <div class="form-group">
      <label>Speed: <span class="range-value" id="speed-val">1s</span></label>
      <input type="range" min="0.2" max="3" step="0.1" value="1" oninput="ls_speed=parseFloat(this.value);document.getElementById('speed-val').textContent=this.value+'s';updateLoader()">
    </div>
    <div class="form-group">
      <label>Border: <span class="range-value" id="border-val">4px</span></label>
      <input type="range" min="2" max="12" value="4" oninput="ls_border=parseInt(this.value);document.getElementById('border-val').textContent=this.value+'px';updateLoader()">
    </div>
  </div>
  <div style="margin-top:16px">
    <label>CSS Code</label>
    <div class="code-output" id="loader-code">/* CSS Loader - spinner */</div>
    <button class="copy-btn" onclick="copyLoaderCode()">📋 Copy Code</button>
  </div>
</div>
'''

SEOCN_LOADER = '''
<h2>CSS加载动画生成器 - 在线创建自定义Loader</h2>
<p>CSS加载动画生成器是一款免费在线工具，帮助开发者快速创建自定义CSS loading动画。无需编写代码，可视化选择动画类型、颜色、大小和速度，一键复制生成的CSS代码。</p>
<h3>支持的加载动画类型</h3>
<ul>
  <li><strong>Spinner</strong> - 经典旋转加载圈，适合通用加载场景</li>
  <li><strong>Dots</strong> - 弹跳圆点动画，适合社交应用和内容加载</li>
  <li><strong>Bars</strong> - 伸缩条动画，适合进度指示</li>
  <li><strong>Ring</strong> - 双色旋转环，视觉效果丰富</li>
  <li><strong>Pulse</strong> - 脉冲动画，适合按钮加载状态</li>
</ul>
<h3>使用场景</h3>
<ul>
  <li>网页异步加载时的等待提示</li>
  <li>表单提交按钮的加载状态</li>
  <li>图片或内容延迟加载时的占位动画</li>
  <li>API请求等待反馈</li>
</ul>
'''

SEOEN_LOADER = '''
<h2>CSS Loader Generator - Create Custom Loading Animations Online</h2>
<p>The CSS Loader Generator is a free online tool that helps developers quickly create custom CSS loading animations. No coding required - visually select animation type, color, size and speed, then copy the generated CSS code with one click.</p>
<h3>Supported Loader Types</h3>
<ul>
  <li><strong>Spinner</strong> - Classic rotating loader, ideal for general loading scenarios</li>
  <li><strong>Dots</strong> - Bouncing dots animation, great for social apps and content loading</li>
  <li><strong>Bars</strong> - Stretching bar animation, perfect for progress indication</li>
  <li><strong>Ring</strong> - Dual-color rotating ring with rich visual effects</li>
  <li><strong>Pulse</strong> - Pulse animation, suitable for button loading states</li>
</ul>
<h3>Use Cases</h3>
<ul>
  <li>Waiting indicators during async page loading</li>
  <li>Button loading states in forms</li>
  <li>Placeholder animations for lazy-loaded content</li>
  <li>API request waiting feedback</li>
</ul>
'''

FAQS_LOADER_CN = [
    ("CSS加载动画会影响页面性能吗？", "CSS动画使用GPU加速，性能开销很小。适当使用不会对页面性能产生明显影响。"),
    ("如何修改生成的CSS代码？", "复制代码后可直接在CSS文件中修改。动画名称、时长、颜色等都可以自定义。"),
    ("支持所有浏览器吗？", "CSS @keyframes动画支持所有现代浏览器，包括Chrome、Firefox、Safari和Edge。"),
    ("生成的代码可以直接使用吗？", "可以直接使用。复制CSS代码到你的样式文件中，然后在HTML中使用对应的类名即可。"),
]
FAQS_LOADER_EN = [
    ("Do CSS loaders affect page performance?", "CSS animations use GPU acceleration with minimal overhead. Proper use won't significantly impact page performance."),
    ("How can I modify the generated CSS code?", "After copying, you can modify the code directly in your CSS file. Animation names, duration, colors, etc. are all customizable."),
    ("Is it compatible with all browsers?", "CSS @keyframes animations work in all modern browsers including Chrome, Firefox, Safari and Edge."),
    ("Can I use the generated code directly?", "Yes. Copy the CSS code to your stylesheet and use the corresponding class name in your HTML."),
]


# ============================================================
# 2. progress-bar-generator
# ============================================================

CUSTOM_CSS_PROGRESS = '''
.preview-area{background:#1e293b;border-radius:12px;padding:32px 24px;min-height:200px;margin-bottom:20px;border:1px solid rgba(148,163,184,.1);display:flex;flex-direction:column;justify-content:center;gap:16px}
.preview-bar-wrapper{width:100%;background:rgba(255,255,255,.08);border-radius:var(--pb-radius);overflow:hidden;position:relative;height:var(--pb-height)}
.preview-bar-fill{height:100%;width:var(--pb-pct);background:var(--pb-color);border-radius:var(--pb-radius);transition:width .5s ease;position:relative}
.preview-bar-fill.striped{background-image:linear-gradient(45deg,rgba(255,255,255,.15) 25%,transparent 25%,transparent 50%,rgba(255,255,255,.15) 50%,rgba(255,255,255,.15) 75%,transparent 75%,transparent);background-size:var(--pb-stripe-size) var(--pb-stripe-size)}
.preview-bar-fill.animated{animation:pb-stripe 1s linear infinite}
@keyframes pb-stripe{from{background-position:var(--pb-stripe-size) 0}to{background-position:0 0}}
.preview-bar-label{position:absolute;right:8px;top:50%;transform:translateY(-50%);font-size:.75rem;color:#fff;font-weight:600;text-shadow:0 1px 2px rgba(0,0,0,.5)}
.preview-bar-label.left{left:8px;right:auto;text-align:left}
.progress-controls{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.progress-controls .form-group{margin-bottom:0}
.code-output{background:#0f172a;border-radius:8px;padding:16px;font-family:"SF Mono","Cascadia Code",monospace;font-size:.82rem;white-space:pre-wrap;word-break:break-all;max-height:250px;overflow:auto;border:1px solid rgba(148,163,184,.1)}
.copy-btn{margin-top:8px;padding:8px 20px;background:rgba(6,182,212,.2);color:#22d3ee;border:1px solid rgba(6,182,212,.3);border-radius:6px;cursor:pointer;font-size:.85rem}
.copy-btn:hover{background:rgba(6,182,212,.3)}
input[type="color"]{width:100%;height:40px;padding:2px;border-radius:8px;cursor:pointer;background:#0f172a;border:1px solid rgba(148,163,184,.2)}
.checkbox-group{display:flex;gap:16px;flex-wrap:wrap}
.checkbox-group label{display:flex;align-items:center;gap:6px;color:#94a3b8;font-size:.85rem;cursor:pointer}
.checkbox-group input[type="checkbox"]{width:auto;accent-color:#22d3ee}
'''

TOOL_JS_PROGRESS = '''
var pb_pct=65,pb_color='#22d3ee',pb_height=24,pb_radius=6,pb_striped=false,pb_animated=false,pb_label='65%',pb_label_pos='right';

function updateProgress(){
  var p=document.getElementById('progress-preview');
  if(!p)return;
  var fill=p.querySelector('.preview-bar-fill');
  if(!fill)return;
  fill.style.setProperty('--pb-pct',pb_pct+'%');
  fill.style.width=pb_pct+'%';
  fill.style.setProperty('--pb-color',pb_color);
  fill.style.background=pb_color;
  p.style.setProperty('--pb-height',pb_height+'px');
  p.style.setProperty('--pb-radius',pb_radius+'px');
  fill.style.borderRadius=pb_radius+'px';
  fill.className='preview-bar-fill'+(pb_striped?' striped':'')+(pb_animated?' animated':'');
  if(pb_striped){
    var ss=Math.round(pb_height*1.5);
    fill.style.setProperty('--pb-stripe-size',ss+'px');
    fill.style.background='linear-gradient(45deg,rgba(255,255,255,.15) 25%,transparent 25%,transparent 50%,rgba(255,255,255,.15) 50%,rgba(255,255,255,.15) 75%,transparent 75%,transparent), '+pb_color;
    fill.style.backgroundSize=ss+'px '+ss+'px';
  }else{
    fill.style.background=pb_color;
    fill.style.backgroundImage='none';
  }
  // label
  var label=p.querySelector('.preview-bar-label');
  if(!label){label=document.createElement('span');label.className='preview-bar-label';fill.appendChild(label)}
  label.textContent=pb_label;
  label.className='preview-bar-label'+(pb_label_pos==='left'?' left':'');
  updateProgressCode();
}

function setProgressPct(v){
  pb_pct=Math.min(100,Math.max(0,parseInt(v)||0));
  document.getElementById('pct-val').textContent=pb_pct+'%';
  pb_label=pb_pct+'%';
  updateProgress();
}

function setProgressHeight(v){
  pb_height=parseInt(v)||24;
  document.getElementById('height-val').textContent=pb_height+'px';
  updateProgress();
}

function setProgressRadius(v){
  pb_radius=parseInt(v)||6;
  document.getElementById('radius-val').textContent=pb_radius+'px';
  updateProgress();
}

function updateProgressCode(){
  var css='/* Progress Bar - Generated */\\n';
  css+='.progress-bar {\\n';
  css+='  width: 100%;\\n';
  css+='  height: '+pb_height+'px;\\n';
  css+='  background: rgba(255,255,255,.08);\\n';
  css+='  border-radius: '+pb_radius+'px;\\n';
  css+='  overflow: hidden;\\n';
  css+='  position: relative;\\n';
  css+='}\\n';
  css+='.progress-bar-fill {\\n';
  css+='  height: 100%;\\n';
  css+='  width: '+pb_pct+'%;\\n';
  css+='  background: '+pb_color+';\\n';
  css+='  border-radius: '+pb_radius+'px;\\n';
  css+='  transition: width .5s ease;\\n';
  if(pb_striped){
    css+='  background-image: linear-gradient(45deg, rgba(255,255,255,.15) 25%, transparent 25%, transparent 50%, rgba(255,255,255,.15) 50%, rgba(255,255,255,.15) 75%, transparent 75%, transparent);\\n';
    css+='  background-size: '+(pb_height*1.5)+'px '+(pb_height*1.5)+'px;\\n';
  }
  if(pb_animated) css+='  animation: progress-stripes 1s linear infinite;\\n';
  css+='}\\n';
  if(pb_animated){
    css+='\\n@keyframes progress-stripes {\\n';
    css+='  from { background-position: '+(pb_height*1.5)+'px 0; }\\n';
    css+='  to { background-position: 0 0; }\\n';
    css+='}\\n';
  }
  document.getElementById('progress-code').textContent=css;
}

function copyProgressCode(){
  var code=document.getElementById('progress-code').textContent;
  navigator.clipboard.writeText(code).then(function(){showToast('Copied')}).catch(function(){showToast('Copy failed')});
}
'''

TOOL_HTML_PROGRESS_CN = '''
<div>
  <div class="preview-area" id="progress-preview">
    <div class="preview-bar-wrapper" style="height:24px;border-radius:6px">
      <div class="preview-bar-fill" style="width:65%;background:#22d3ee;border-radius:6px;transition:width .5s ease;position:relative">
        <span class="preview-bar-label" style="position:absolute;right:8px;top:50%;transform:translateY(-50%);font-size:.75rem;color:#fff;font-weight:600">65%</span>
      </div>
    </div>
  </div>
  <div class="progress-controls">
    <div class="form-group">
      <label>进度: <span class="range-value" id="pct-val">65%</span></label>
      <input type="range" min="0" max="100" value="65" oninput="setProgressPct(this.value)">
    </div>
    <div class="form-group">
      <label>颜色</label>
      <input type="color" value="#22d3ee" onchange="pb_color=this.value;updateProgress()">
    </div>
    <div class="form-group">
      <label>高度: <span class="range-value" id="height-val">24px</span></label>
      <input type="range" min="8" max="48" value="24" oninput="setProgressHeight(this.value)">
    </div>
    <div class="form-group">
      <label>圆角: <span class="range-value" id="radius-val">6px</span></label>
      <input type="range" min="0" max="24" value="6" oninput="setProgressRadius(this.value)">
    </div>
    <div class="form-group" style="grid-column:1/-1">
      <div class="checkbox-group">
        <label><input type="checkbox" onchange="pb_striped=this.checked;updateProgress()"> 条纹效果</label>
        <label><input type="checkbox" onchange="pb_animated=this.checked;updateProgress()"> 动画条纹</label>
        <label style="margin-left:8px">标签位置:
          <select style="width:auto;padding:4px 8px;background:#0f172a;border:1px solid rgba(148,163,184,.2);border-radius:4px;color:#e2e8f0;font-size:.8rem" onchange="pb_label_pos=this.value;updateProgress()">
            <option value="right">右侧</option>
            <option value="left">左侧</option>
          </select>
        </label>
      </div>
    </div>
  </div>
  <div style="margin-top:16px">
    <label>CSS 代码</label>
    <div class="code-output" id="progress-code">/* Progress Bar - Generated */</div>
    <button class="copy-btn" onclick="copyProgressCode()">📋 复制代码</button>
  </div>
</div>
'''

TOOL_HTML_PROGRESS_EN = '''
<div>
  <div class="preview-area" id="progress-preview">
    <div class="preview-bar-wrapper" style="height:24px;border-radius:6px">
      <div class="preview-bar-fill" style="width:65%;background:#22d3ee;border-radius:6px;transition:width .5s ease;position:relative">
        <span class="preview-bar-label" style="position:absolute;right:8px;top:50%;transform:translateY(-50%);font-size:.75rem;color:#fff;font-weight:600">65%</span>
      </div>
    </div>
  </div>
  <div class="progress-controls">
    <div class="form-group">
      <label>Progress: <span class="range-value" id="pct-val">65%</span></label>
      <input type="range" min="0" max="100" value="65" oninput="setProgressPct(this.value)">
    </div>
    <div class="form-group">
      <label>Color</label>
      <input type="color" value="#22d3ee" onchange="pb_color=this.value;updateProgress()">
    </div>
    <div class="form-group">
      <label>Height: <span class="range-value" id="height-val">24px</span></label>
      <input type="range" min="8" max="48" value="24" oninput="setProgressHeight(this.value)">
    </div>
    <div class="form-group">
      <label>Radius: <span class="range-value" id="radius-val">6px</span></label>
      <input type="range" min="0" max="24" value="6" oninput="setProgressRadius(this.value)">
    </div>
    <div class="form-group" style="grid-column:1/-1">
      <div class="checkbox-group">
        <label><input type="checkbox" onchange="pb_striped=this.checked;updateProgress()"> Striped</label>
        <label><input type="checkbox" onchange="pb_animated=this.checked;updateProgress()"> Animated</label>
        <label style="margin-left:8px">Label:
          <select style="width:auto;padding:4px 8px;background:#0f172a;border:1px solid rgba(148,163,184,.2);border-radius:4px;color:#e2e8f0;font-size:.8rem" onchange="pb_label_pos=this.value;updateProgress()">
            <option value="right">Right</option>
            <option value="left">Left</option>
          </select>
        </label>
      </div>
    </div>
  </div>
  <div style="margin-top:16px">
    <label>CSS Code</label>
    <div class="code-output" id="progress-code">/* Progress Bar - Generated */</div>
    <button class="copy-btn" onclick="copyProgressCode()">📋 Copy Code</button>
  </div>
</div>
'''

SEOCN_PROGRESS = '''
<h2>CSS进度条生成器 - 在线创建自定义进度条</h2>
<p>CSS进度条生成器是一款免费在线工具，帮助开发者快速创建美观的自定义CSS进度条。可视化配置进度、颜色、高度、圆角和条纹效果，一键复制代码。</p>
<h3>功能特性</h3>
<ul>
  <li>可视化调节进度百分比</li>
  <li>自定义颜色、高度和圆角</li>
  <li>条纹背景和动画效果</li>
  <li>进度标签位置可选</li>
  <li>一键复制CSS代码</li>
</ul>
<h3>使用场景</h3>
<ul>
  <li>文件上传进度展示</li>
  <li>表单填写进度指示</li>
  <li>技能水平可视化</li>
  <li>数据加载进度条</li>
  <li>问卷调查进度</li>
</ul>
'''

SEOEN_PROGRESS = '''
<h2>CSS Progress Bar Generator - Create Custom Progress Bars Online</h2>
<p>The CSS Progress Bar Generator is a free online tool that helps developers create beautiful custom CSS progress bars. Visually configure progress percentage, color, height, border radius and stripe effects, then copy the code with one click.</p>
<h3>Features</h3>
<ul>
  <li>Visual progress percentage adjustment</li>
  <li>Custom color, height and border radius</li>
  <li>Stripe background and animation effects</li>
  <li>Configurable label position</li>
  <li>One-click CSS code copy</li>
</ul>
<h3>Use Cases</h3>
<ul>
  <li>File upload progress display</li>
  <li>Form completion progress indicator</li>
  <li>Skill level visualization</li>
  <li>Data loading progress bars</li>
  <li>Survey completion progress</li>
</ul>
'''

FAQS_PROGRESS_CN = [
    ("进度条支持动画过渡效果吗？", "支持。进度条宽度变化自带0.5秒平滑过渡效果，条纹动画也支持连续滚动。"),
    ("如何将进度条嵌入我的网页？", "复制生成的CSS代码到样式文件，然后在HTML中使用对应的类名即可。生成器提供完整的示例代码。"),
    ("支持响应式设计吗？", "进度条宽度默认100%，自适应容器尺寸。移动端和桌面端都能完美显示。"),
    ("条纹动画的兼容性如何？", "CSS条纹动画使用background-position动画，支持所有现代浏览器。"),
]
FAQS_PROGRESS_EN = [
    ("Does the progress bar support animated transitions?", "Yes. The progress bar width change has a built-in 0.5s smooth transition, and the stripe animation supports continuous scrolling."),
    ("How do I embed the progress bar in my webpage?", "Copy the generated CSS code to your stylesheet and use the corresponding class names in your HTML. The generator provides complete example code."),
    ("Is it responsive?", "The progress bar width defaults to 100% and adapts to the container size automatically. It works perfectly on both mobile and desktop."),
    ("What about stripe animation compatibility?", "CSS stripe animation uses background-position animation and works in all modern browsers."),
]


# ============================================================
# 构建并保存
# ============================================================

print("=" * 60)
print("Building css-loader-generator...")
cn_path, en_path = builder.build_bilingual(
    slug='css-loader-generator',
    title_cn='CSS加载动画生成器',
    title_en='CSS Loader Generator',
    desc_cn='在线创建自定义CSS加载动画，支持5种动画类型：Spinner、Dots、Bars、Ring、Pulse',
    desc_en='Create custom CSS loading animations online. Supports 5 types: Spinner, Dots, Bars, Ring, Pulse',
    icon='⏳',
    cat_cn='开发工具',
    cat_en='Developer Tools',
    cat_anchor='developer-tools',
    tool_html_cn=TOOL_HTML_LOADER_CN,
    tool_html_en=TOOL_HTML_LOADER_EN,
    tool_js=TOOL_JS_LOADER,
    faqs_cn=FAQS_LOADER_CN,
    faqs_en=FAQS_LOADER_EN,
    seo_cn=SEOCN_LOADER,
    seo_en=SEOEN_LOADER,
    custom_css=CUSTOM_CSS_LOADER,
)
print(f"  CN: {cn_path}")
print(f"  EN: {en_path}")

print("\nBuilding progress-bar-generator...")
cn_path2, en_path2 = builder.build_bilingual(
    slug='progress-bar-generator',
    title_cn='CSS进度条生成器',
    title_en='CSS Progress Bar Generator',
    desc_cn='在线创建自定义CSS进度条，可调节进度、颜色、高度、圆角，支持条纹和动画效果',
    desc_en='Create custom CSS progress bars online. Adjust progress, color, height, radius, with stripe and animation support',
    icon='📊',
    cat_cn='开发工具',
    cat_en='Developer Tools',
    cat_anchor='developer-tools',
    tool_html_cn=TOOL_HTML_PROGRESS_CN,
    tool_html_en=TOOL_HTML_PROGRESS_EN,
    tool_js=TOOL_JS_PROGRESS,
    faqs_cn=FAQS_PROGRESS_CN,
    faqs_en=FAQS_PROGRESS_EN,
    seo_cn=SEOCN_PROGRESS,
    seo_en=SEOEN_PROGRESS,
    custom_css=CUSTOM_CSS_PROGRESS,
)
print(f"  CN: {cn_path2}")
print(f"  EN: {en_path2}")

print("\n✅ Done! Both tools generated.")
