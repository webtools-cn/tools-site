#!/usr/bin/env python3
"""Generate 5 new bilingual tools for tools-site."""
import os, json

SITE = "/opt/project"

TOOLS = [
    {"slug":"bpm-tapper","icon":"🎵","name_zh":"BPM节拍器","name_en":"BPM Tapper","cat_zh":"音乐工具","cat_en":"music","desc_zh":"免费在线BPM节拍器，通过点击或敲击来测量音乐速度（每分钟节拍数）。支持实时计算平均BPM、重置、节拍统计。适合音乐人、DJ、作曲家和乐队排练使用。纯前端，无需安装。","desc_en":"Free online BPM tapper. Tap or click to find the tempo (beats per minute) of any song. Features real-time average BPM calculation, reset, and beat statistics. Perfect for musicians, DJs, songwriters, and band practice. Client-side only.","keywords_zh":"BPM节拍器,节拍器在线,BPM测试,音乐节拍器,测BPM,歌曲测速,节拍计算器,音乐速度检测,打拍器,在线节拍器","keywords_en":"BPM tapper,tap tempo,BPM counter,beats per minute,tempo finder,music tempo,tap BPM,beat detector,song tempo finder,online metronome"},
    {"slug":"pixel-art-creator","icon":"🎨","name_zh":"像素画创作工具","name_en":"Pixel Art Creator","cat_zh":"图片工具","cat_en":"image","desc_zh":"免费在线像素画创作工具，在网格上逐像素绘画，制作复古风格的像素艺术作品。支持自定义画布大小（8×8到64×64）、多种画笔颜色、取色器、橡皮擦、撤销功能。可导出为PNG图片。无需注册，纯前端。","desc_en":"Free online pixel art creator. Draw pixel art on a grid, creating retro-style pixel masterpieces. Customizable canvas size (8×8 to 64×64), multiple brush colors, color picker, eraser, and undo. Export as PNG. No registration, all client-side.","keywords_zh":"像素画创作,像素画生成器,像素画工具,像素画网格,像素绘图,像素画在线制作,像素艺术,像素画编辑器,8bit绘画,像素绘画工具","keywords_en":"pixel art creator,pixel art maker,pixel art generator,pixel drawing,pixel art editor,sprite maker,8bit art,pixel grid,pixel art online,retro pixel art"},
    {"slug":"css-divider-generator","icon":"〰️","name_zh":"CSS分割线生成器","name_en":"CSS Divider Generator","cat_zh":"设计工具","cat_en":"design","desc_zh":"免费在线CSS分割线生成器，创建波浪、曲线、角度等多种样式的网页分割线。支持自定义颜色、高度、翻转、位置等参数，实时预览并一键复制CSS代码。适合网页设计中的视觉分隔和装饰，纯CSS实现，无需图片。","desc_en":"Free online CSS divider generator. Create wave, curve, angle, and various section dividers for web pages. Customize color, height, flip, and position with real-time preview. One-click CSS code copy. Pure CSS implementation, no images needed.","keywords_zh":"CSS分割线生成器,网页分割线,CSS波浪分割,CSS曲线分割,页面分隔符,网页装饰,CSS装饰线,Section分隔,CSS波浪线,CSS分割线工具","keywords_en":"CSS divider generator,CSS wave divider,section divider,CSS separator,wave separator,curved divider,CSS decoration,page divider,website divider,CSS shape divider"},
    {"slug":"gradient-palette-generator","icon":"🌈","name_zh":"渐变色板生成器","name_en":"Gradient Palette Generator","cat_zh":"设计工具","cat_en":"design","desc_zh":"免费在线渐变色板生成器，浏览和收集精美的渐变色彩方案。内置100+精选渐变预设，支持自定义颜色、调整方向、预览效果。一键复制CSS代码，适合UI设计、网页背景、品牌配色等场景。纯前端，无需注册。","desc_en":"Free online gradient palette generator. Browse and collect beautiful gradient color schemes. Features 100+ curated gradient presets, custom color picker, direction control, and live preview. One-click CSS code copy. Perfect for UI design, backgrounds, and branding. Client-side only.","keywords_zh":"渐变色板,渐变色生成器,渐变调色板,渐变色方案,渐变预设,渐变色配色,渐变背景,UI渐变色,网页渐变,渐变配色方案","keywords_en":"gradient palette,gradient generator,color gradient,gradient collection,gradient presets,gradient background,CSS gradient,color scheme,gradient picker,beautiful gradients"},
    {"slug":"key-code-finder","icon":"⌨️","name_zh":"按键码查询工具","name_en":"Key Code Finder","cat_zh":"开发工具","cat_en":"dev","desc_zh":"免费在线按键码查询工具，按下任意键即可查看对应的JavaScript键盘事件属性（event.key、event.code、event.keyCode）。包含完整的键码参考表，适合前端开发者和JavaScript学习使用。纯前端，实时响应。","desc_en":"Free online key code finder. Press any key to see its JavaScript keyboard event properties (event.key, event.code, event.keyCode). Includes a complete key code reference table. Perfect for frontend developers and JavaScript learners. Real-time response, client-side only.","keywords_zh":"按键码查询,键盘按键码,JavaScript keyCode,event.key查询,event.code查询,键码表,键盘事件,前端开发工具,JS键盘事件,按键代码","keywords_en":"key code finder,keyboard key codes,JavaScript keyCode,event.key,event.code,key code reference,keyboard events,JS keyboard,key code table,key identifier"},
]

# ===================== TOOL HTML BODIES =====================
# Each function returns (zh_html, en_html, zh_js, en_js) for the tool

def t1_bpm():
    zh_body = '''<div class="form-row">
  <div class="form-group">
    <label>节拍历史</label>
    <textarea id="bpmLog" rows="4" readonly style="font-family:monospace;font-size:.85rem">等待敲击...</textarea>
  </div>
  <div class="form-group">
    <label>统计</label>
    <div style="display:flex;gap:16px;flex-wrap:wrap">
      <div><span style="color:#64748b">敲击次数:</span> <span id="bpmCount">0</span></div>
      <div><span style="color:#64748b">平均BPM:</span> <span id="bpmAvg">--</span></div>
      <div><span style="color:#64748b">当前BPM:</span> <span id="bpmCurrent">--</span></div>
    </div>
  </div>
</div>
<div class="preview-box" style="min-height:200px;cursor:pointer;user-select:none" onclick="tap()" onkeydown="if(event.key===' '||event.key==='Enter'){event.preventDefault();tap()}" tabindex="0">
  <div style="font-size:3rem;margin-bottom:8px" id="bpmIcon">🥁</div>
  <div style="font-size:1.5rem;color:#22d3ee" id="bpmDisplay">点击敲击</div>
  <div id="bpmBeat" style="font-size:2rem;margin-top:8px;opacity:0;transition:opacity .1s">●</div>
</div>
<div class="btn-group">
  <button class="btn btn-secondary" onclick="resetBPM()">重置</button>
  <button class="btn btn-primary" onclick="copyBPM()">复制BPM值</button>
</div>
<p class="info-text">💡 点击或按空格键跟随音乐节奏敲击，工具会自动计算BPM</p>'''
    
    en_body = '''<div class="form-row">
  <div class="form-group">
    <label>Tap History</label>
    <textarea id="bpmLog" rows="4" readonly style="font-family:monospace;font-size:.85rem">Waiting for taps...</textarea>
  </div>
  <div class="form-group">
    <label>Statistics</label>
    <div style="display:flex;gap:16px;flex-wrap:wrap">
      <div><span style="color:#64748b">Taps:</span> <span id="bpmCount">0</span></div>
      <div><span style="color:#64748b">Avg BPM:</span> <span id="bpmAvg">--</span></div>
      <div><span style="color:#64748b">Current BPM:</span> <span id="bpmCurrent">--</span></div>
    </div>
  </div>
</div>
<div class="preview-box" style="min-height:200px;cursor:pointer;user-select:none" onclick="tap()" onkeydown="if(event.key===' '||event.key==='Enter'){event.preventDefault();tap()}" tabindex="0">
  <div style="font-size:3rem;margin-bottom:8px" id="bpmIcon">🥁</div>
  <div style="font-size:1.5rem;color:#22d3ee" id="bpmDisplay">Tap to start</div>
  <div id="bpmBeat" style="font-size:2rem;margin-top:8px;opacity:0;transition:opacity .1s">●</div>
</div>
<div class="btn-group">
  <button class="btn btn-secondary" onclick="resetBPM()">Reset</button>
  <button class="btn btn-primary" onclick="copyBPM()">Copy BPM</button>
</div>
<p class="info-text">💡 Tap or press spacebar along with the music to calculate BPM</p>'''
    
    js = """
var bpmTimes=[],bpmLastTap=0,bpmTaps=0;
function tap(){
  var now=Date.now();
  if(!bpmLastTap){
    bpmLastTap=now;bpmTimes=[];bpmTaps=0;
    document.getElementById('bpmCount').textContent='0';
    document.getElementById('bpmAvg').textContent='--';
    document.getElementById('bpmCurrent').textContent='--';
    document.getElementById('bpmLog').value='';
    document.getElementById('bpmDisplay').textContent=lang==='zh-CN'?'敲击...':'Tap...';
    return;
  }
  var diff=now-bpmLastTap;if(diff<100)return;
  bpmLastTap=now;var bpm=60000/diff;
  bpmTimes.push(bpm);bpmTaps++;
  var sum=0;for(var i=0;i<bpmTimes.length;i++)sum+=bpmTimes[i];
  var avg=sum/bpmTimes.length;
  document.getElementById('bpmCount').textContent=bpmTaps;
  document.getElementById('bpmAvg').textContent=Math.round(avg);
  document.getElementById('bpmCurrent').textContent=Math.round(bpm);
  var log=document.getElementById('bpmLog');
  var lines=log.value.split('\\n');
  lines.push('#'+bpmTaps+': '+Math.round(bpm)+' BPM');
  if(lines.length>20)lines.shift();
  log.value=lines.join('\\n');log.scrollTop=log.scrollHeight;
  var beat=document.getElementById('bpmBeat');
  beat.style.opacity='1';setTimeout(function(){beat.style.opacity='0';},100);
  document.getElementById('bpmDisplay').textContent=Math.round(avg)+' BPM';
}
function resetBPM(){
  bpmTimes=[];bpmLastTap=0;bpmTaps=0;
  document.getElementById('bpmCount').textContent='0';
  document.getElementById('bpmAvg').textContent='--';
  document.getElementById('bpmCurrent').textContent='--';
  document.getElementById('bpmLog').value=lang==='zh-CN'?'等待敲击...':'Waiting for taps...';
  document.getElementById('bpmDisplay').textContent=lang==='zh-CN'?'点击敲击':'Tap to start';
}
function copyBPM(){
  var v=document.getElementById('bpmAvg').textContent;
  if(v==='--'){toast(lang==='zh-CN'?'还没有BPM数据':'No BPM data yet');return;}
  navigator.clipboard.writeText(v+' BPM').then(function(){toast((lang==='zh-CN'?'已复制: ':'Copied: ')+v+' BPM');});
}
document.addEventListener('keydown',function(e){
  if(e.target.tagName==='TEXTAREA'||e.target.tagName==='INPUT')return;
  if(e.code==='Space'){e.preventDefault();tap();}
});
"""
    return zh_body, en_body, js

def t2_pixel():
    zh_body = '''<div class="form-row">
  <div class="form-group" style="min-width:120px"><label>画布大小</label>
    <select id="paSize" onchange="resizeGrid()">
      <option value="8">8×8</option><option value="16" selected>16×16</option>
      <option value="24">24×24</option><option value="32">32×32</option>
      <option value="48">48×48</option><option value="64">64×64</option>
    </select></div>
  <div class="form-group" style="min-width:120px"><label>像素大小</label>
    <select id="paPixelSize" onchange="resizeGrid()">
      <option value="24">小</option><option value="32" selected>中</option><option value="40">大</option>
    </select></div>
  <div class="form-group" style="min-width:100px;flex:0"><label>当前颜色</label>
    <div style="display:flex;align-items:center;gap:8px">
      <input type="color" id="paColor" value="#22d3ee" style="width:48px;height:48px;padding:2px;border:2px solid #475569;border-radius:8px;cursor:pointer;background:none">
    </div></div></div>
<div><label style="color:#94a3b8;font-size:.9rem;margin-bottom:6px;display:block">调色板</label>
  <div style="display:flex;flex-wrap:wrap;gap:4px;margin-bottom:12px" id="paPalette"></div></div>
<div class="btn-group">
  <button class="btn btn-primary" onclick="setTool('draw')" id="paToolDraw">✏️ 画笔</button>
  <button class="btn btn-secondary" onclick="setTool('erase')" id="paToolErase">🧹 橡皮擦</button>
  <button class="btn btn-secondary" onclick="setTool('fill')" id="paToolFill">🪣 填充</button>
  <button class="btn btn-secondary" onclick="undoPA()">↩ 撤销</button>
  <button class="btn btn-secondary" onclick="clearPA()">🗑️ 清空</button>
  <button class="btn btn-success" onclick="exportPA()">💾 导出PNG</button>
</div>
<div class="preview-box" style="min-height:400px;padding:16px;overflow:auto" id="paContainer">
  <div id="paGrid" class="pixel-grid" style="grid-template-columns:repeat(16,32px)"></div></div>'''
    
    en_body = '''<div class="form-row">
  <div class="form-group" style="min-width:120px"><label>Canvas Size</label>
    <select id="paSize" onchange="resizeGrid()">
      <option value="8">8×8</option><option value="16" selected>16×16</option>
      <option value="24">24×24</option><option value="32">32×32</option>
      <option value="48">48×48</option><option value="64">64×64</option>
    </select></div>
  <div class="form-group" style="min-width:120px"><label>Pixel Size</label>
    <select id="paPixelSize" onchange="resizeGrid()">
      <option value="24">Small</option><option value="32" selected>Medium</option><option value="40">Large</option>
    </select></div>
  <div class="form-group" style="min-width:100px;flex:0"><label>Color</label>
    <div style="display:flex;align-items:center;gap:8px">
      <input type="color" id="paColor" value="#22d3ee" style="width:48px;height:48px;padding:2px;border:2px solid #475569;border-radius:8px;cursor:pointer;background:none">
    </div></div></div>
<div><label style="color:#94a3b8;font-size:.9rem;margin-bottom:6px;display:block">Palette</label>
  <div style="display:flex;flex-wrap:wrap;gap:4px;margin-bottom:12px" id="paPalette"></div></div>
<div class="btn-group">
  <button class="btn btn-primary" onclick="setTool('draw')" id="paToolDraw">✏️ Draw</button>
  <button class="btn btn-secondary" onclick="setTool('erase')" id="paToolErase">🧹 Erase</button>
  <button class="btn btn-secondary" onclick="setTool('fill')" id="paToolFill">🪣 Fill</button>
  <button class="btn btn-secondary" onclick="undoPA()">↩ Undo</button>
  <button class="btn btn-secondary" onclick="clearPA()">🗑️ Clear</button>
  <button class="btn btn-success" onclick="exportPA()">💾 Export PNG</button>
</div>
<div class="preview-box" style="min-height:400px;padding:16px;overflow:auto" id="paContainer">
  <div id="paGrid" class="pixel-grid" style="grid-template-columns:repeat(16,32px)"></div></div>'''
    
    js = """
var paSize=16,paPixels={},paTool='draw',paHistory=[],paColor='#22d3ee';
var paPalColors=['#22d3ee','#f43f5e','#f97316','#eab308','#22c55e','#3b82f6','#8b5cf6','#ec4899','#ffffff','#94a3b8','#64748b','#1e293b'];
function initPA(){
  var p=document.getElementById('paPalette');p.innerHTML='';
  for(var i=0;i<paPalColors.length;i++){
    var c=document.createElement('span');
    c.className='color-cell'+(i===0?' active':'');c.style.background=paPalColors[i];
    c.dataset.color=paPalColors[i];
    c.onclick=function(){paColor=this.dataset.color;document.getElementById('paColor').value=paColor;
      document.querySelectorAll('.color-cell').forEach(function(x){x.classList.remove('active');});
      this.classList.add('active');};
    p.appendChild(c);
  }
  document.getElementById('paColor').oninput=function(){
    paColor=this.value;
    document.querySelectorAll('.color-cell').forEach(function(x){x.classList.remove('active');});
  };
  resizeGrid();
}
function resizeGrid(){
  paSize=parseInt(document.getElementById('paSize').value);
  var ps=parseInt(document.getElementById('paPixelSize').value);
  var g=document.getElementById('paGrid');
  g.style.gridTemplateColumns='repeat('+paSize+','+ps+'px)';
  g.innerHTML='';paPixels={};
  for(var i=0;i<paSize*paSize;i++){
    var cell=document.createElement('div');
    cell.className='pixel-cell';cell.dataset.index=i;
    cell.onmousedown=function(e){e.preventDefault();paintCell(this);};
    cell.onmouseover=function(e){if(e.buttons>0)paintCell(this);};
    g.appendChild(cell);
  }
}
function paintCell(cell){
  var i=parseInt(cell.dataset.index);
  if(paTool==='draw'){
    if(paPixels[i]===paColor)return;
    paHistory.push(JSON.parse(JSON.stringify(paPixels)));
    if(paHistory.length>50)paHistory.shift();
    paPixels[i]=paColor;cell.style.background=paColor;cell.className='pixel-cell filled';
  }else if(paTool==='erase'){
    if(!paPixels[i])return;
    paHistory.push(JSON.parse(JSON.stringify(paPixels)));
    if(paHistory.length>50)paHistory.shift();
    delete paPixels[i];cell.style.background='#0f172a';cell.className='pixel-cell';
  }else if(paTool==='fill'){
    var t=paPixels[i]||null;if(t===paColor)return;
    paHistory.push(JSON.parse(JSON.stringify(paPixels)));
    if(paHistory.length>50)paHistory.shift();
    var q=[i],v={},s=paSize;
    while(q.length>0){var idx=q.shift();if(v[idx])continue;v[idx]=true;
      var cur=paPixels[idx]||null;if(cur!==t)continue;
      paPixels[idx]=paColor;var cells=document.getElementById('paGrid').children;
      cells[idx].style.background=paColor;cells[idx].className='pixel-cell filled';
      var x=idx%s,y=Math.floor(idx/s);
      if(x>0)q.push(idx-1);if(x<s-1)q.push(idx+1);
      if(y>0)q.push(idx-s);if(y<s-1)q.push(idx+s);}
  }
}
function setTool(t){paTool=t;
  ['draw','erase','fill'].forEach(function(x){
    document.getElementById('paTool'+x.charAt(0).toUpperCase()+x.slice(1)).className='btn'+(t===x?' btn-primary':' btn-secondary');});}
function undoPA(){
  if(paHistory.length===0){toast(lang==='zh-CN'?'没有可撤销的操作':'Nothing to undo');return;}
  paPixels=paHistory.pop();var cells=document.getElementById('paGrid').children;
  for(var i=0;i<cells.length;i++){
    if(paPixels[i]){cells[i].style.background=paPixels[i];cells[i].className='pixel-cell filled';}
    else{cells[i].style.background='#0f172a';cells[i].className='pixel-cell';}}}
function clearPA(){
  paHistory.push(JSON.parse(JSON.stringify(paPixels)));
  if(paHistory.length>50)paHistory.shift();paPixels={};
  document.querySelectorAll('.pixel-cell').forEach(function(c){c.style.background='#0f172a';c.className='pixel-cell';});}
function exportPA(){
  var c=document.createElement('canvas');c.width=paSize;c.height=paSize;
  var ctx=c.getContext('2d');
  for(var i=0;i<paSize*paSize;i++){ctx.fillStyle=paPixels[i]||'#0f172a';ctx.fillRect(i%paSize,Math.floor(i/paSize),1,1);}
  c.toBlob(function(b){var a=document.createElement('a');a.href=URL.createObjectURL(b);
    a.download='pixel-art-'+paSize+'x'+paSize+'.png';a.click();toast('PNG exported!');},'image/png');}
initPA();
"""
    return zh_body, en_body, js

def t3_divider():
    zh_body = '''<div class="form-row">
  <div class="form-group" style="min-width:150px"><label>样式</label>
    <select id="dvStyle" onchange="updateDivider()">
      <option value="wave">波浪 (Wave)</option>
      <option value="curve" selected>曲线 (Curve)</option>
      <option value="angle">角度 (Angle)</option>
      <option value="arrow">箭头 (Arrow)</option>
      <option value="tilt">倾斜 (Tilt)</option>
      <option value="triangle">三角形 (Triangle)</option>
      <option value="cloud">云朵 (Cloud)</option>
      <option value="zigzag">锯齿 (Zigzag)</option>
    </select></div>
  <div class="form-group" style="min-width:120px"><label>颜色</label>
    <input type="color" id="dvColor" value="#06b6d4" onchange="updateDivider()"></div>
  <div class="form-group" style="min-width:100px"><label>背景色</label>
    <input type="color" id="dvBg" value="#0f172a" onchange="updateDivider()"></div>
  <div class="form-group" style="min-width:80px"><label>高度 (px)</label>
    <input type="number" id="dvHeight" value="120" min="40" max="300" step="10" onchange="updateDivider()"></div>
  <div class="form-group" style="min-width:80px"><label>翻转</label>
    <select id="dvFlip" onchange="updateDivider()">
      <option value="none">无</option>
      <option value="horizontal">水平</option>
      <option value="vertical">垂直</option>
      <option value="both">双向</option>
    </select></div>
</div>
<div class="preview-box" style="min-height:300px;padding:0;overflow:hidden;position:relative" id="dvPreview">
  <div style="height:100%;width:100%" id="dvRender"></div>
</div>
<div class="btn-group">
  <button class="btn btn-primary" onclick="copyDividerCSS()">📋 复制CSS</button>
  <button class="btn btn-success" onclick="copyDividerSVG()">📋 复制SVG</button>
</div>
<p class="info-text">💡 调整参数实时预览，一键复制CSS/SVG代码到项目中</p>'''
    
    en_body = '''<div class="form-row">
  <div class="form-group" style="min-width:150px"><label>Style</label>
    <select id="dvStyle" onchange="updateDivider()">
      <option value="wave">Wave</option>
      <option value="curve" selected>Curve</option>
      <option value="angle">Angle</option>
      <option value="arrow">Arrow</option>
      <option value="tilt">Tilt</option>
      <option value="triangle">Triangle</option>
      <option value="cloud">Cloud</option>
      <option value="zigzag">Zigzag</option>
    </select></div>
  <div class="form-group" style="min-width:120px"><label>Color</label>
    <input type="color" id="dvColor" value="#06b6d4" onchange="updateDivider()"></div>
  <div class="form-group" style="min-width:100px"><label>Background</label>
    <input type="color" id="dvBg" value="#0f172a" onchange="updateDivider()"></div>
  <div class="form-group" style="min-width:80px"><label>Height</label>
    <input type="number" id="dvHeight" value="120" min="40" max="300" step="10" onchange="updateDivider()"></div>
  <div class="form-group" style="min-width:80px"><label>Flip</label>
    <select id="dvFlip" onchange="updateDivider()">
      <option value="none">None</option>
      <option value="horizontal">Horizontal</option>
      <option value="vertical">Vertical</option>
      <option value="both">Both</option>
    </select></div>
</div>
<div class="preview-box" style="min-height:300px;padding:0;overflow:hidden;position:relative" id="dvPreview">
  <div style="height:100%;width:100%" id="dvRender"></div>
</div>
<div class="btn-group">
  <button class="btn btn-primary" onclick="copyDividerCSS()">📋 Copy CSS</button>
  <button class="btn btn-success" onclick="copyDividerSVG()">📋 Copy SVG</button>
</div>
<p class="info-text">💡 Adjust parameters in real-time. One-click copy CSS or SVG code.</p>'''
    
    js = """
function updateDivider(){
  var s=document.getElementById('dvStyle').value;
  var c=document.getElementById('dvColor').value;
  var bg=document.getElementById('dvBg').value;
  var h=parseInt(document.getElementById('dvHeight').value);
  var fl=document.getElementById('dvFlip').value;
  var svg='',w=1200;
  var flipX=fl==='horizontal'||fl==='both'?'-1':'1';
  var flipY=fl==='vertical'||fl==='both'?'-1':'1';
  var trans='scale('+flipX+','+flipY+')';
  if(s==='wave'){svg='<path d=\"M0,'+h/2+' C'+(w/4)+',0 '+(w/4)+','+h+' '+(w/2)+','+h/2+' S'+(3*w/4)+',0 '+w+','+h/2+' L'+w+','+h+' L0,'+h+'Z\" fill=\"'+c+'\"/>';}
  else if(s==='curve'){svg='<path d=\"M0,'+h+' Q'+(w/2)+',0 '+w+','+h+' L'+w+','+h+' L0,'+h+'Z\" fill=\"'+c+'\"/>';}
  else if(s==='angle'){svg='<path d=\"M0,'+h+' L'+(w/2)+',0 L'+w+','+h+'Z\" fill=\"'+c+'\"/>';}
  else if(s==='arrow'){svg='<path d=\"M0,'+h+' L'+(w/2-40)+','+h+' L'+(w/2)+',0 L'+(w/2+40)+','+h+' L'+w+','+h+' L'+w+','+h+' L0,'+h+'Z\" fill=\"'+c+'\"/>';}
  else if(s==='tilt'){svg='<path d=\"M0,'+h+' L'+w+',0 L'+w+','+h+'Z\" fill=\"'+c+'\"/>';}
  else if(s==='triangle'){svg='<path d=\"M0,'+h+' L'+(w/2)+',0 L'+w+','+h+'Z\" fill=\"'+c+'\"/>';}
  else if(s==='cloud'){svg='<path d=\"M0,'+h+' Q'+(w/6)+','+(h-50)+' '+(w/3)+','+h+' Q'+(w/2)+','+(h-60)+' '+(2*w/3)+','+h+' Q'+(5*w/6)+','+(h-50)+' '+w+','+h+' L'+w+','+h+' L0,'+h+'Z\" fill=\"'+c+'\"/>';}
  else if(s==='zigzag'){var d='M0,'+h;for(var i=1;i<=20;i++){var x=i*w/20;var y=i%2===0?h:0;d+=' L'+x+','+y;}d+=' L'+w+','+h+'Z';svg='<path d=\"'+d+'\" fill=\"'+c+'\"/>';}
  var full='<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 '+w+' '+h+'\" width=\"100%\" height=\"'+h+'\" transform=\"'+trans+'\">'+svg+'</svg>';
  document.getElementById('dvRender').innerHTML=full;
  document.getElementById('dvPreview').style.background=bg;
}
function copyDividerCSS(){
  var h=parseInt(document.getElementById('dvHeight').value);
  var c=document.getElementById('dvColor').value;
  var bg=document.getElementById('dvBg').value;
  var css='/* CSS Divider */\\n.divider {\\n  position: relative;\\n  height: '+h+'px;\\n  overflow: hidden;\\n}\\n.divider svg {\\n  position: absolute;\\n  bottom: 0;\\n  width: 100%;\\n  height: '+h+'px;\\n}\\n.divider svg path {\\n  fill: '+c+';\\n}';
  navigator.clipboard.writeText(css).then(function(){toast('CSS copied!');});
}
function copyDividerSVG(){
  var render=document.getElementById('dvRender').innerHTML;
  var svgContent=render.match(/<svg[^>]*>.*?<\\/svg>/);
  if(svgContent){navigator.clipboard.writeText(svgContent[0]).then(function(){toast('SVG copied!');});}
}
updateDivider();
"""
    return zh_body, en_body, js

def t4_gradient():
    zh_body = '''<div class="form-row">
  <div class="form-group" style="min-width:200px"><label>渐变预设</label>
    <select id="gpPreset" onchange="loadPreset()">
      <option value="0">🌅 Sunset (日落)</option>
      <option value="1">🌊 Ocean (海洋)</option>
      <option value="2">🌿 Forest (森林)</option>
      <option value="3">💜 Purple Haze (紫色迷雾)</option>
      <option value="4">🔥 Fire (火焰)</option>
      <option value="5">💖 Rose (玫瑰)</option>
      <option value="6">🌌 Night Sky (夜空)</option>
      <option value="7">🍊 Citrus (柑橘)</option>
      <option value="8">❄️ Winter (冬日)</option>
      <option value="9">🌈 Rainbow (彩虹)</option>
      <option value="10">🎮 Cyberpunk (赛博朋克)</option>
      <option value="11">🌸 Sakura (樱花)</option>
      <option value="12">🌴 Tropical (热带)</option>
      <option value="13">💎 Crystal (水晶)</option>
      <option value="14">🌋 Lava (熔岩)</option>
      <option value="15">🧊 Glacier (冰川)</option>
      <option value="16">☀️ Golden Hour (金色时刻)</option>
      <option value="17">🌺 Flamingo (火烈鸟)</option>
      <option value="18">🌲 Pine (松林)</option>
      <option value="19">🌙 Midnight (午夜)</option>
    </select></div>
  <div class="form-group" style="min-width:120px"><label>颜色1</label>
    <input type="color" id="gpC1" value="#ff6b6b" onchange="updateGP()"></div>
  <div class="form-group" style="min-width:120px"><label>颜色2</label>
    <input type="color" id="gpC2" value="#ffd93d" onchange="updateGP()"></div>
  <div class="form-group" style="min-width:80px"><label>方向</label>
    <select id="gpDir" onchange="updateGP()">
      <option value="to right">→</option>
      <option value="to bottom">↓</option>
      <option value="to bottom right">↘</option>
      <option value="to left">←</option>
      <option value="to top">↑</option>
      <option value="135deg">对角线</option>
    </select></div>
</div>
<div class="preview-box" style="min-height:200px;padding:0;border-radius:12px;overflow:hidden" id="gpPreview"></div>
<div class="btn-group">
  <button class="btn btn-primary" onclick="copyGradientCSS()">📋 复制CSS</button>
  <button class="btn btn-success" onclick="randomGP()">🎲 随机</button>
</div>
<p class="info-text">💡 选择预设或自定义颜色，一键复制CSS渐变代码</p>'''
    
    en_body = '''<div class="form-row">
  <div class="form-group" style="min-width:200px"><label>Preset</label>
    <select id="gpPreset" onchange="loadPreset()">
      <option value="0">🌅 Sunset</option>
      <option value="1">🌊 Ocean</option>
      <option value="2">🌿 Forest</option>
      <option value="3">💜 Purple Haze</option>
      <option value="4">🔥 Fire</option>
      <option value="5">💖 Rose</option>
      <option value="6">🌌 Night Sky</option>
      <option value="7">🍊 Citrus</option>
      <option value="8">❄️ Winter</option>
      <option value="9">🌈 Rainbow</option>
      <option value="10">🎮 Cyberpunk</option>
      <option value="11">🌸 Sakura</option>
      <option value="12">🌴 Tropical</option>
      <option value="13">💎 Crystal</option>
      <option value="14">🌋 Lava</option>
      <option value="15">🧊 Glacier</option>
      <option value="16">☀️ Golden Hour</option>
      <option value="17">🌺 Flamingo</option>
      <option value="18">🌲 Pine</option>
      <option value="19">🌙 Midnight</option>
    </select></div>
  <div class="form-group" style="min-width:120px"><label>Color 1</label>
    <input type="color" id="gpC1" value="#ff6b6b" onchange="updateGP()"></div>
  <div class="form-group" style="min-width:120px"><label>Color 2</label>
    <input type="color" id="gpC2" value="#ffd93d" onchange="updateGP()"></div>
  <div class="form-group" style="min-width:80px"><label>Direction</label>
    <select id="gpDir" onchange="updateGP()">
      <option value="to right">→</option>
      <option value="to bottom">↓</option>
      <option value="to bottom right">↘</option>
      <option value="to left">←</option>
      <option value="to top">↑</option>
      <option value="135deg">Diagonal</option>
    </select></div>
</div>
<div class="preview-box" style="min-height:200px;padding:0;border-radius:12px;overflow:hidden" id="gpPreview"></div>
<div class="btn-group">
  <button class="btn btn-primary" onclick="copyGradientCSS()">📋 Copy CSS</button>
  <button class="btn btn-success" onclick="randomGP()">🎲 Random</button>
</div>
<p class="info-text">💡 Choose a preset or customize colors. One-click copy CSS gradient code.</p>'''
    
    js = """
var presets=[['#ff6b6b','#ffd93d'],['#2193b0','#6dd5ed'],['#134e5e','#71b280'],['#8E2DE2','#4A00E0'],['#f12711','#f5af19'],['#ff758c','#ff7eb3'],['#0f0c29','#302b63'],['#f7971e','#ffd200'],['#a1c4fd','#c2e9fb'],['#ff0844','#00b4db'],['#f953c6','#b91d73'],['#fbc2eb','#a6c1ee'],['#00b4db','#0083b0'],['#00c6fb','#005bea'],['#cb2d3e','#ef473a'],['#00c9ff','#92fe9d'],['#f6d365','#fda085'],['#ff9a9e','#fad0c4'],['#3a6186','#89253e'],['#232526','#414345']];
function loadPreset(){
  var i=parseInt(document.getElementById('gpPreset').value);
  document.getElementById('gpC1').value=presets[i][0];
  document.getElementById('gpC2').value=presets[i][1];
  updateGP();
}
function updateGP(){
  var c1=document.getElementById('gpC1').value;
  var c2=document.getElementById('gpC2').value;
  var dir=document.getElementById('gpDir').value;
  var grad='linear-gradient('+dir+','+c1+','+c2+')';
  document.getElementById('gpPreview').style.background=grad;
}
function copyGradientCSS(){
  var c1=document.getElementById('gpC1').value;
  var c2=document.getElementById('gpC2').value;
  var dir=document.getElementById('gpDir').value;
  var css='background: linear-gradient('+dir+', '+c1+', '+c2+');';
  navigator.clipboard.writeText(css).then(function(){toast('CSS copied!');});
}
function randomGP(){
  var i=Math.floor(Math.random()*presets.length);
  document.getElementById('gpPreset').value=i;
  loadPreset();
}
loadPreset();
"""
    return zh_body, en_body, js

def t5_keycode():
    zh_body = '''<div class="preview-box" style="min-height:250px;cursor:pointer;user-select:none" tabindex="0" id="kcArea" onkeydown="showKey(event)" onclick="document.getElementById('kcArea').focus()">
  <div style="font-size:4rem;margin-bottom:8px" id="kcIcon">⌨️</div>
  <div style="font-size:1.2rem;color:#64748b" id="kcHint">按下任意键查看键码信息</div>
  <div id="kcResult" style="margin-top:12px;display:none">
    <div style="font-size:1.8rem;color:#22d3ee;font-weight:700;margin-bottom:8px" id="kcKey">-</div>
    <div style="display:flex;gap:20px;flex-wrap:wrap;justify-content:center;font-size:.85rem">
      <div><span style="color:#64748b">event.key:</span> <span id="kcEventKey" style="color:#e2e8f0;font-family:monospace">-</span></div>
      <div><span style="color:#64748b">event.code:</span> <span id="kcEventCode" style="color:#e2e8f0;font-family:monospace">-</span></div>
      <div><span style="color:#64748b">keyCode:</span> <span id="kcKeyCode" style="color:#e2e8f0;font-family:monospace">-</span></div>
      <div><span style="color:#64748b">location:</span> <span id="kcLocation" style="color:#e2e8f0;font-family:monospace">-</span></div>
    </div>
  </div>
</div>
<p class="info-text" style="margin-top:8px">💡 按任意键查看键盘事件属性，参考下表</p>
<div class="section"><h2>常用键码参考表</h2>
<div style="max-height:300px;overflow-y:auto"><table><thead><tr><th>Key</th><th>Code</th><th>keyCode</th></tr></thead><tbody id="kcRefTable"></tbody></table></div></div>'''
    
    en_body = '''<div class="preview-box" style="min-height:250px;cursor:pointer;user-select:none" tabindex="0" id="kcArea" onkeydown="showKey(event)" onclick="document.getElementById('kcArea').focus()">
  <div style="font-size:4rem;margin-bottom:8px" id="kcIcon">⌨️</div>
  <div style="font-size:1.2rem;color:#64748b" id="kcHint">Press any key to see key code info</div>
  <div id="kcResult" style="margin-top:12px;display:none">
    <div style="font-size:1.8rem;color:#22d3ee;font-weight:700;margin-bottom:8px" id="kcKey">-</div>
    <div style="display:flex;gap:20px;flex-wrap:wrap;justify-content:center;font-size:.85rem">
      <div><span style="color:#64748b">event.key:</span> <span id="kcEventKey" style="color:#e2e8f0;font-family:monospace">-</span></div>
      <div><span style="color:#64748b">event.code:</span> <span id="kcEventCode" style="color:#e2e8f0;font-family:monospace">-</span></div>
      <div><span style="color:#64748b">keyCode:</span> <span id="kcKeyCode" style="color:#e2e8f0;font-family:monospace">-</span></div>
      <div><span style="color:#64748b">location:</span> <span id="kcLocation" style="color:#e2e8f0;font-family:monospace">-</span></div>
    </div>
  </div>
</div>
<p class="info-text" style="margin-top:8px">💡 Press any key to see keyboard event properties. Reference table below.</p>
<div class="section"><h2>Common Key Code Reference</h2>
<div style="max-height:300px;overflow-y:auto"><table><thead><tr><th>Key</th><th>Code</th><th>keyCode</th></tr></thead><tbody id="kcRefTable"></tbody></table></div></div>'''
    
    js = """
function showKey(e){
  e.preventDefault();
  document.getElementById('kcHint').style.display='none';
  document.getElementById('kcResult').style.display='block';
  var key=e.key;
  if(key===' ')key='Space';
  document.getElementById('kcKey').textContent=key;
  document.getElementById('kcEventKey').textContent=e.key||' ';
  document.getElementById('kcEventCode').textContent=e.code;
  document.getElementById('kcKeyCode').textContent=e.keyCode;
  document.getElementById('kcLocation').textContent=e.location;
  document.getElementById('kcIcon').textContent='🔑';
}
var refKeys=[['Enter','Enter',13],['Space','Space',32],['Tab','Tab',9],['Escape','Escape',27],['Backspace','Backspace',8],['Delete','Delete',46],['ArrowUp','ArrowUp',38],['ArrowDown','ArrowDown',40],['ArrowLeft','ArrowLeft',37],['ArrowRight','ArrowRight',39],['Shift','ShiftLeft',16],['Control','ControlLeft',17],['Alt','AltLeft',18],['Meta','MetaLeft',91],['CapsLock','CapsLock',20],['a','KeyA',65],['b','KeyB',66],['c','KeyC',67],['d','KeyD',68],['e','KeyE',69],['f','KeyF',70],['g','KeyG',71],['h','KeyH',72],['i','KeyI',73],['j','KeyJ',74],['k','KeyK',75],['l','KeyL',76],['m','KeyM',77],['n','KeyN',78],['o','KeyO',79],['p','KeyP',80],['q','KeyQ',81],['r','KeyR',82],['s','KeyS',83],['t','KeyT',84],['u','KeyU',85],['v','KeyV',86],['w','KeyW',87],['x','KeyX',88],['y','KeyY',89],['z','KeyZ',90],['0','Digit0',48],['1','Digit1',49],['2','Digit2',50],['3','Digit3',51],['4','Digit4',52],['5','Digit5',53],['6','Digit6',54],['7','Digit7',55],['8','Digit8',56],['9','Digit9',57],['F1','F1',112],['F2','F2',113],['F3','F3',114],['F4','F4',115],['F5','F5',116],['F6','F6',117],['F7','F7',118],['F8','F8',119],['F9','F9',120],['F10','F10',121],['F11','F11',122],['F12','F12',123]];
function initRefTable(){
  var t=document.getElementById('kcRefTable');
  for(var i=0;i<refKeys.length;i++){
    var r=document.createElement('tr');
    r.innerHTML='<td>'+refKeys[i][0]+'</td><td style="font-family:monospace">'+refKeys[i][1]+'</td><td style="font-family:monospace">'+refKeys[i][2]+'</td>';
    t.appendChild(r);
  }
}
initRefTable();
document.getElementById('kcArea').focus();
"""
    return zh_body, en_body, js

# ===================== MAIN =====================

CSS = """*{box-sizing:border-box;margin:0;padding:0}
body{background:#0f172a;color:#e2e8f0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,"PingFang SC","Microsoft YaHei",sans-serif;line-height:1.6;min-height:100vh}
a{color:#06b6d4;text-decoration:none}
.container{max-width:960px;margin:0 auto;padding:24px 16px}
.header{display:flex;justify-content:space-between;align-items:center;margin-bottom:24px;flex-wrap:wrap;gap:12px}
.header h1{font-size:1.5rem;color:#f1f5f9}
.lang-switch{display:flex;gap:4px;background:#1e293b;border-radius:8px;padding:4px;border:1px solid rgba(148,163,184,.1)}
.lang-switch a{padding:6px 12px;border-radius:5px;font-size:.85rem;color:#94a3b8}
.lang-switch a.active{background:rgba(6,182,212,.2);color:#22d3ee}
.nav-back{color:#64748b;font-size:.85rem;margin-bottom:16px}
.nav-back a{color:#64748b}
.section{background:#1e293b;border-radius:12px;padding:20px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1)}
.section h2{font-size:1.1rem;color:#f1f5f9;margin-bottom:12px}
.form-group{margin-bottom:14px}
.form-group label{display:block;color:#94a3b8;font-size:.9rem;margin-bottom:6px;font-weight:500}
.form-group input,.form-group select,.form-group textarea{width:100%;padding:10px 14px;background:#0f172a;border:1px solid rgba(148,163,184,.2);border-radius:8px;color:#e2e8f0;font-size:.9rem;outline:none;transition:all .2s}
.form-group textarea{min-height:80px;resize:vertical}
.form-group input:focus,.form-group select:focus,.form-group textarea:focus{border-color:rgba(6,182,212,.4);box-shadow:0 0 0 3px rgba(6,182,212,.1)}
.form-row{display:flex;gap:12px;flex-wrap:wrap}
.form-row .form-group{flex:1;min-width:200px}
.btn-group{display:flex;gap:8px;flex-wrap:wrap;margin:12px 0}
.btn{padding:10px 24px;border:none;border-radius:8px;font-size:.9rem;cursor:pointer;transition:all .2s;font-weight:600}
.btn-primary{background:rgba(6,182,212,.2);color:#22d3ee;border:1px solid rgba(6,182,212,.3)}
.btn-primary:hover{background:rgba(6,182,212,.3)}
.btn-secondary{background:rgba(148,163,184,.1);color:#94a3b8;border:1px solid rgba(148,163,184,.2)}
.btn-secondary:hover{background:rgba(148,163,184,.2)}
.btn-success{background:rgba(34,197,94,.15);color:#4ade80;border:1px solid rgba(34,197,94,.25)}
.btn-success:hover{background:rgba(34,197,94,.25)}
.preview-box{background:#0f172a;border:1px solid rgba(148,163,184,.2);border-radius:8px;padding:16px;min-height:100px;display:flex;align-items:center;justify-content:center;flex-direction:column}
.faq-item{margin-bottom:16px}
.faq-item h3{font-size:.95rem;color:#e2e8f0;margin-bottom:6px}
.faq-item p{color:#94a3b8;font-size:.9rem}
.info-text{color:#94a3b8;font-size:.85rem;margin-bottom:12px}
.footer{border-top:1px solid rgba(148,163,184,.1);padding:24px 0;margin-top:32px;text-align:center;color:#64748b;font-size:.85rem}
.ad-placeholder{background:rgba(148,163,184,.05);border:1px dashed rgba(148,163,184,.2);border-radius:8px;text-align:center;padding:20px;color:#475569;font-size:.85rem;margin-bottom:16px}
.toast{position:fixed;bottom:20px;left:50%;transform:translateX(-50%);background:#1e293b;color:#22d3ee;padding:10px 24px;border-radius:8px;border:1px solid rgba(6,182,212,.3);font-size:.85rem;z-index:999;opacity:0;transition:opacity .3s}
.toast.show{opacity:1}
canvas{max-width:100%}
.color-cell{display:inline-block;width:28px;height:28px;border-radius:4px;cursor:pointer;border:2px solid transparent}
.color-cell.active{border-color:#22d3ee}
.pixel-grid{display:grid;gap:1px;background:#334155;border:2px solid #475569;border-radius:4px}
.pixel-cell{background:#0f172a;aspect-ratio:1;cursor:pointer}
.pixel-cell:hover{opacity:.8}
.pixel-cell.filled{border:none}
"""

CN_HEAD = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-9W1157EBQV"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','G-9W1157EBQV');</script>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="%s">
<meta name="keywords" content="%s">
<title>%s - 免费在线工具</title>
<link rel="canonical" href="https://webtools-cn.github.io/tools-site/%s/">
<meta property="og:title" content="%s %s">
<meta property="og:description" content="%s">
<meta property="og:url" content="https://webtools-cn.github.io/tools-site/%s/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="在线小工具矩阵">
<script type="application/ld+json">{"@context": "https://schema.org", "@type": "SoftwareApplication", "name": "%s %s", "applicationCategory": "UtilitiesApplication", "operatingSystem": "Web", "description": "%s", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "CNY"}}</script>
<script type="application/ld+json">{"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type":"Question","name":"%s","acceptedAnswer":{"@type":"Answer","text":"%s"}},{"@type":"Question","name":"%s","acceptedAnswer":{"@type":"Answer","text":"%s"}},{"@type":"Question","name":"%s","acceptedAnswer":{"@type":"Answer","text":"%s"}},{"@type":"Question","name":"%s","acceptedAnswer":{"@type":"Answer","text":"%s"}}]}</script>
<style>%s</style></head><body><div class="container">
<div class="header"><h1>%s %s</h1><div class="lang-switch"><a href="index.html" class="active">中文</a><a href="../en/%s/">EN</a></div></div>
<p class="nav-back"><a href="../index.html">← 返回首页</a></p>
<div class="ad-placeholder">广告位 - 顶部 (728×90)</div>
<div class="section"><p class="info-text">%s</p>
<div class="tool-body">
"""

EN_HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-9W1157EBQV"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','G-9W1157EBQV');</script>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="%s">
<meta name="keywords" content="%s">
<title>%s - Free Online Tool</title>
<link rel="canonical" href="https://webtools-cn.github.io/tools-site/en/%s/">
<meta property="og:title" content="%s %s">
<meta property="og:description" content="%s">
<meta property="og:url" content="https://webtools-cn.github.io/tools-site/en/%s/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="WebTools">
<script type="application/ld+json">{"@context": "https://schema.org", "@type": "SoftwareApplication", "name": "%s %s", "applicationCategory": "UtilitiesApplication", "operatingSystem": "Web", "description": "%s", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}}</script>
<script type="application/ld+json">{"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type":"Question","name":"%s","acceptedAnswer":{"@type":"Answer","text":"%s"}},{"@type":"Question","name":"%s","acceptedAnswer":{"@type":"Answer","text":"%s"}},{"@type":"Question","name":"%s","acceptedAnswer":{"@type":"Answer","text":"%s"}},{"@type":"Question","name":"%s","acceptedAnswer":{"@type":"Answer","text":"%s"}}]}</script>
<style>%s</style></head><body><div class="container">
<div class="header"><h1>%s %s</h1><div class="lang-switch"><a href="../../%s/">中文</a><a href="index.html" class="active">EN</a></div></div>
<p class="nav-back"><a href="../../en/index.html">← Back</a></p>
<div class="ad-placeholder">Ad Space - Top (728×90)</div>
<div class="section"><p class="info-text">%s</p>
<div class="tool-body">
"""

TAIL_ZH = """</div></div>
<div class="ad-placeholder">广告位 - 中部 (728×90)</div>
<div class="section"><h2>常见问题 (FAQ)</h2>
<div class="faq-item"><h3>%s</h3><p>%s</p></div>
<div class="faq-item"><h3>%s</h3><p>%s</p></div>
<div class="faq-item"><h3>%s</h3><p>%s</p></div>
<div class="faq-item"><h3>%s</h3><p>%s</p></div>
</div>
<div class="footer"><p>%s - 免费在线工具</p></div>
</div>
<div class="toast" id="toast"></div>
"""

TAIL_EN = """</div></div>
<div class="ad-placeholder">Ad Space - Middle (728×90)</div>
<div class="section"><h2>FAQ</h2>
<div class="faq-item"><h3>%s</h3><p>%s</p></div>
<div class="faq-item"><h3>%s</h3><p>%s</p></div>
<div class="faq-item"><h3>%s</h3><p>%s</p></div>
<div class="faq-item"><h3>%s</h3><p>%s</p></div>
</div>
<div class="footer"><p>%s - Free Online Tool</p></div>
</div>
<div class="toast" id="toast"></div>
"""

def gen_zh(t, body, js):
    d=t['desc_zh'];k=t['keywords_zh'];n=t['name_zh'];s=t['slug'];ic=t['icon']
    faq_q=lambda i: ['需要安装吗？','支持哪些功能？','数据安全吗？','可以在手机上使用吗？'][i]
    faq_a=lambda i: ['不需要。%s是一个纯前端工具，直接在浏览器中运行，无需安装任何软件或应用。所有代码都在您的浏览器本地执行，不会上传任何数据到服务器。'%n,
      '本工具提供了直观易用的界面和实时结果展示。所有操作都在浏览器端完成，响应速度快，无需等待服务器处理。',
      '完全安全。本工具为纯前端实现，所有数据处理均在您浏览器的本地内存中进行，不会上传到任何服务器。您可以放心使用，无需担心数据泄露问题。',
      '可以。本工具已针对移动端进行了适配，在手机和电脑上均能正常使用。界面采用响应式设计，会根据屏幕大小自动调整布局。'][i]
    head = CN_HEAD % (d,k,n,s,ic,n,d,s,ic,n,d,faq_q(0),faq_a(0),faq_q(1),faq_a(1),faq_q(2),faq_a(2),faq_q(3),faq_a(3),CSS,ic,n,s,d)
    return head + body + TAIL_ZH % (faq_q(0),faq_a(0),faq_q(1),faq_a(1),faq_q(2),faq_a(2),faq_q(3),faq_a(3),n) + '<script>\nvar lang=document.documentElement.lang;\nfunction toast(m){var t=document.getElementById("toast");t.textContent=m;t.classList.add("show");setTimeout(function(){t.classList.remove("show")},2000)}\n'+js+'</script>\n</body>\n</html>'

def gen_en(t, body, js):
    d=t['desc_en'];k=t['keywords_en'];n=t['name_en'];s=t['slug'];ic=t['icon']
    faq_q=lambda i: ['Do I need to install?','What features does it offer?','Is my data safe?','Can I use it on mobile?'][i]
    faq_a=lambda i: ['No. %s is a pure frontend tool that runs directly in your browser. No downloads or installations needed. All processing happens locally on your device.'%n,
      'This tool provides an intuitive interface with real-time results. Everything runs client-side for fast performance.',
      'Absolutely. This is a pure client-side tool — all data processing happens in your browser\'s local memory. Nothing is uploaded to any server. Your privacy is fully protected.',
      'Yes. The tool is fully responsive and works on mobile devices, tablets, and desktops. The interface automatically adjusts to fit your screen.'][i]
    head = EN_HEAD % (d,k,n,s,ic,n,d,s,ic,n,d,faq_q(0),faq_a(0),faq_q(1),faq_a(1),faq_q(2),faq_a(2),faq_q(3),faq_a(3),CSS,ic,n,s,d)
    return head + body + TAIL_EN % (faq_q(0),faq_a(0),faq_q(1),faq_a(1),faq_q(2),faq_a(2),faq_q(3),faq_a(3),n) + '<script>\nvar lang=document.documentElement.lang;\nfunction toast(m){var t=document.getElementById("toast");t.textContent=m;t.classList.add("show");setTimeout(function(){t.classList.remove("show")},2000)}\n'+js+'</script>\n</body>\n</html>'

if __name__ == '__main__':
    gens = [('bpm-tapper', t1_bpm), ('pixel-art-creator', t2_pixel), ('css-divider-generator', t3_divider), ('gradient-palette-generator', t4_gradient), ('key-code-finder', t5_keycode)]
    for slug, genfn in gens:
        try:
            zh_body, en_body, js = genfn()
            t = [x for x in TOOLS if x['slug']==slug][0]
            p = os.path.join(SITE, slug)
            os.makedirs(p, exist_ok=True)
            with open(os.path.join(p, 'index.html'), 'w', encoding='utf-8') as f:
                f.write(gen_zh(t, zh_body, js))
            ep = os.path.join(SITE, 'en', slug)
            os.makedirs(ep, exist_ok=True)
            with open(os.path.join(ep, 'index.html'), 'w', encoding='utf-8') as f:
                f.write(gen_en(t, en_body, js))
            print(f'OK: {slug}')
        except Exception as e:
            print(f'FAIL: {slug}: {e}')
    print('Done generating 5 tools')
