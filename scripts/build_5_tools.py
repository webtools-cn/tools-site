#!/usr/bin/env python3
"""批量创建5个新工具：diagram-generator, emojify, font-generator, utm-builder, car-loan-calculator"""

import os

BASE = "/home/chison/tools-site"

# ============================================================
# 工具1: diagram-generator - 手绘风格流程图
# ============================================================
DIAGRAM_CN = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>在线流程图生成器 - 手绘风格 | Free ToolBase</title>
  <meta name="description" content="免费在线流程图生成器，支持手绘风格，拖拽节点创建流程图、思维导图、组织架构图。无需注册，即开即用。">
  <meta property="og:title" content="在线流程图生成器 - 手绘风格 | Free ToolBase">
  <meta property="og:description" content="免费在线流程图生成器，支持手绘风格，拖拽节点创建流程图、思维导图、组织架构图。无需注册，即开即用。">
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://free-toolbase.com/diagram-generator/">
  <script type="application/ld+json">{"@context":"https://schema.org","@type":"SoftwareApplication","name":"流程图生成器","applicationCategory":"DeveloperApplication","operatingSystem":"Web Browser","description":"免费在线流程图生成器，支持手绘风格，拖拽节点创建流程图、思维导图、组织架构图。","url":"https://free-toolbase.com/diagram-generator/"}</script>
  <style>
    :root{--primary:#4F46E5;--primary-hover:#4338CA;--bg:#f8fafc;--surface:#fff;--text:#1e293b;--text-secondary:#64748b;--border:#e2e8f0;--radius:12px;--shadow:0 1px 3px rgba(0,0,0,.08)}
    *{margin:0;padding:0;box-sizing:border-box}
    body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;background:var(--bg);color:var(--text);min-height:100vh;display:flex;flex-direction:column}
    header{background:var(--surface);border-bottom:1px solid var(--border);padding:16px 24px;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px}
    header h1{font-size:1.25rem;font-weight:700}
    header a{color:var(--primary);text-decoration:none;font-size:.9rem}
    main{flex:1;padding:20px;max-width:1200px;margin:0 auto;width:100%}
    .toolbar{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:16px;align-items:center}
    .toolbar button{padding:8px 16px;border:1px solid var(--border);border-radius:8px;background:var(--surface);cursor:pointer;font-size:.875rem;transition:all .2s;display:flex;align-items:center;gap:6px}
    .toolbar button:hover{border-color:var(--primary);color:var(--primary)}
    .toolbar button.active{background:var(--primary);color:#fff;border-color:var(--primary)}
    .canvas-container{background:var(--surface);border:2px dashed var(--border);border-radius:var(--radius);min-height:500px;position:relative;overflow:auto;cursor:crosshair}
    .node{position:absolute;background:var(--surface);border:2px solid var(--primary);border-radius:8px;padding:12px 16px;min-width:120px;text-align:center;cursor:move;font-size:.9rem;user-select:none;box-shadow:var(--shadow);transform:rotate(-1deg);transition:box-shadow .2s}
    .node:hover{box-shadow:0 4px 12px rgba(79,70,229,.2)}
    .node.selected{border-color:#ef4444;box-shadow:0 0 0 3px rgba(239,68,68,.2)}
    .node .delete-btn{position:absolute;top:-10px;right:-10px;width:22px;height:22px;background:#ef4444;color:#fff;border:none;border-radius:50%;cursor:pointer;font-size:12px;display:none;line-height:22px;text-align:center}
    .node:hover .delete-btn{display:block}
    footer{background:var(--surface);border-top:1px solid var(--border);padding:16px 24px;text-align:center;font-size:.8rem;color:var(--text-secondary)}
    @media(max-width:600px){header{padding:12px 16px}main{padding:12px}.node{min-width:80px;padding:8px 12px;font-size:.8rem}}
  </style>
</head>
<body>
<header>
  <h1>📐 流程图生成器</h1>
  <a href="/">← 返回首页</a>
</header>
<main>
  <div class="toolbar">
    <button class="active" onclick="setMode('rect')" id="btn-rect">⬜ 矩形节点</button>
    <button onclick="setMode('diamond')" id="btn-diamond">🔷 菱形节点</button>
    <button onclick="setMode('circle')" id="btn-circle">⭕ 圆形节点</button>
    <button onclick="clearAll()" style="margin-left:auto">🗑️ 清空画布</button>
  </div>
  <div class="canvas-container" id="canvas"></div>
  <p style="margin-top:12px;font-size:.85rem;color:var(--text-secondary)">💡 点击画布空白处添加节点，拖拽移动节点，点击节点可选中，按Delete键删除选中节点。</p>
</main>
<footer>© 2025 Free ToolBase · 免费在线工具</footer>
<script>
let mode='rect',nodeId=0,nodes=[],selectedNode=null,dragging=null,offsetX=0,offsetY=0;
const canvas=document.getElementById('canvas');
function setMode(m){mode=m;document.querySelectorAll('.toolbar button').forEach(b=>b.classList.remove('active'));document.getElementById('btn-'+mode)?.classList.add('active')}
function addNode(x,y,text){
  const id=++nodeId;const el=document.createElement('div');el.className='node';el.id='node-'+id;
  el.style.left=x+'px';el.style.top=y+'px';
  if(mode==='diamond')el.style.transform='rotate(45deg) scale(.85)';
  else if(mode==='circle')el.style.borderRadius='50%';
  else el.style.transform='rotate(-1deg)';
  el.innerHTML='<span class="node-text">'+text+'</span><button class="delete-btn" onclick="event.stopPropagation();removeNode('+id+')">×</button>';
  el.addEventListener('mousedown',e=>startDrag(e,id));
  el.addEventListener('click',e=>{e.stopPropagation();selectNode(id)});
  canvas.appendChild(el);nodes.push({id,el,x,y,text,mode});
  makeEditable(el,id);
}
function makeEditable(el,id){
  const span=el.querySelector('.node-text');
  span.addEventListener('dblclick',e=>{e.stopPropagation();const t=span.textContent;const input=document.createElement('input');
    input.value=t;input.style.cssText='border:none;background:transparent;text-align:center;font-size:.9rem;width:100%;outline:none';
    span.textContent='';span.appendChild(input);input.focus();
    input.addEventListener('blur',()=>{span.textContent=input.value||'双击编辑';const n=nodes.find(n=>n.id===id);if(n)n.text=span.textContent});
    input.addEventListener('keydown',ev=>{if(ev.key==='Enter')input.blur()});
  });
}
function startDrag(e,id){if(e.target.tagName==='BUTTON'||e.target.tagName==='INPUT')return;e.preventDefault();
  dragging=nodes.find(n=>n.id===id);if(!dragging)return;
  const rect=dragging.el.getBoundingClientRect();offsetX=e.clientX-rect.left;offsetY=e.clientY-rect.top;selectNode(id)}
function selectNode(id){if(selectedNode)selectedNode.el.classList.remove('selected');
  selectedNode=nodes.find(n=>n.id===id);if(selectedNode)selectedNode.el.classList.add('selected')}
function removeNode(id){const n=nodes.find(n=>n.id===id);if(n){n.el.remove();nodes=nodes.filter(n=>n.id!==id);if(selectedNode&&selectedNode.id===id)selectedNode=null}}
function clearAll(){nodes.forEach(n=>n.el.remove());nodes=[];selectedNode=null;nodeId=0}
canvas.addEventListener('click',e=>{if(e.target===canvas){const rect=canvas.getBoundingClientRect();
  addNode(e.clientX-rect.left-60,e.clientY-rect.top-20,'双击编辑')}});
document.addEventListener('mousemove',e=>{if(!dragging)return;const rect=canvas.getBoundingClientRect();
  dragging.el.style.left=(e.clientX-rect.left-offsetX)+'px';dragging.el.style.top=(e.clientY-rect.top-offsetY)+'px';
  dragging.x=parseInt(dragging.el.style.left);dragging.y=parseInt(dragging.el.style.top)});
document.addEventListener('mouseup',()=>{dragging=null});
document.addEventListener('keydown',e=>{if(e.key==='Delete'&&selectedNode){removeNode(selectedNode.id)}});
setMode('rect');
</script>
</body>
</html>
"""

DIAGRAM_EN = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Flowchart Generator - Hand-drawn Style | Free ToolBase</title>
  <meta name="description" content="Free online flowchart generator with hand-drawn style. Drag and drop nodes to create flowcharts, mind maps, and org charts. No sign-up required.">
  <meta property="og:title" content="Flowchart Generator - Hand-drawn Style | Free ToolBase">
  <meta property="og:description" content="Free online flowchart generator with hand-drawn style. Drag and drop nodes to create flowcharts, mind maps, and org charts. No sign-up required.">
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://free-toolbase.com/en/diagram-generator/">
  <script type="application/ld+json">{"@context":"https://schema.org","@type":"SoftwareApplication","name":"Flowchart Generator","applicationCategory":"DeveloperApplication","operatingSystem":"Web Browser","description":"Free online flowchart generator with hand-drawn style. Drag and drop nodes to create flowcharts, mind maps, and org charts.","url":"https://free-toolbase.com/en/diagram-generator/"}</script>
  <style>
    :root{--primary:#4F46E5;--primary-hover:#4338CA;--bg:#f8fafc;--surface:#fff;--text:#1e293b;--text-secondary:#64748b;--border:#e2e8f0;--radius:12px;--shadow:0 1px 3px rgba(0,0,0,.08)}
    *{margin:0;padding:0;box-sizing:border-box}
    body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;background:var(--bg);color:var(--text);min-height:100vh;display:flex;flex-direction:column}
    header{background:var(--surface);border-bottom:1px solid var(--border);padding:16px 24px;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px}
    header h1{font-size:1.25rem;font-weight:700}
    header a{color:var(--primary);text-decoration:none;font-size:.9rem}
    main{flex:1;padding:20px;max-width:1200px;margin:0 auto;width:100%}
    .toolbar{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:16px;align-items:center}
    .toolbar button{padding:8px 16px;border:1px solid var(--border);border-radius:8px;background:var(--surface);cursor:pointer;font-size:.875rem;transition:all .2s;display:flex;align-items:center;gap:6px}
    .toolbar button:hover{border-color:var(--primary);color:var(--primary)}
    .toolbar button.active{background:var(--primary);color:#fff;border-color:var(--primary)}
    .canvas-container{background:var(--surface);border:2px dashed var(--border);border-radius:var(--radius);min-height:500px;position:relative;overflow:auto;cursor:crosshair}
    .node{position:absolute;background:var(--surface);border:2px solid var(--primary);border-radius:8px;padding:12px 16px;min-width:120px;text-align:center;cursor:move;font-size:.9rem;user-select:none;box-shadow:var(--shadow);transform:rotate(-1deg);transition:box-shadow .2s}
    .node:hover{box-shadow:0 4px 12px rgba(79,70,229,.2)}
    .node.selected{border-color:#ef4444;box-shadow:0 0 0 3px rgba(239,68,68,.2)}
    .node .delete-btn{position:absolute;top:-10px;right:-10px;width:22px;height:22px;background:#ef4444;color:#fff;border:none;border-radius:50%;cursor:pointer;font-size:12px;display:none;line-height:22px;text-align:center}
    .node:hover .delete-btn{display:block}
    footer{background:var(--surface);border-top:1px solid var(--border);padding:16px 24px;text-align:center;font-size:.8rem;color:var(--text-secondary)}
    @media(max-width:600px){header{padding:12px 16px}main{padding:12px}.node{min-width:80px;padding:8px 12px;font-size:.8rem}}
  </style>
</head>
<body>
<header>
  <h1>📐 Flowchart Generator</h1>
  <a href="/en/">← Back to Home</a>
</header>
<main>
  <div class="toolbar">
    <button class="active" onclick="setMode('rect')" id="btn-rect">⬜ Rectangle</button>
    <button onclick="setMode('diamond')" id="btn-diamond">🔷 Diamond</button>
    <button onclick="setMode('circle')" id="btn-circle">⭕ Circle</button>
    <button onclick="clearAll()" style="margin-left:auto">🗑️ Clear Canvas</button>
  </div>
  <div class="canvas-container" id="canvas"></div>
  <p style="margin-top:12px;font-size:.85rem;color:var(--text-secondary)">💡 Click empty canvas to add a node. Drag to move. Click to select. Press Delete to remove selected node.</p>
</main>
<footer>© 2025 Free ToolBase · Free Online Tools</footer>
<script>
let mode='rect',nodeId=0,nodes=[],selectedNode=null,dragging=null,offsetX=0,offsetY=0;
const canvas=document.getElementById('canvas');
function setMode(m){mode=m;document.querySelectorAll('.toolbar button').forEach(b=>b.classList.remove('active'));document.getElementById('btn-'+mode)?.classList.add('active')}
function addNode(x,y,text){
  const id=++nodeId;const el=document.createElement('div');el.className='node';el.id='node-'+id;
  el.style.left=x+'px';el.style.top=y+'px';
  if(mode==='diamond')el.style.transform='rotate(45deg) scale(.85)';
  else if(mode==='circle')el.style.borderRadius='50%';
  else el.style.transform='rotate(-1deg)';
  el.innerHTML='<span class="node-text">'+text+'</span><button class="delete-btn" onclick="event.stopPropagation();removeNode('+id+')">×</button>';
  el.addEventListener('mousedown',e=>startDrag(e,id));
  el.addEventListener('click',e=>{e.stopPropagation();selectNode(id)});
  canvas.appendChild(el);nodes.push({id,el,x,y,text,mode});
  makeEditable(el,id);
}
function makeEditable(el,id){
  const span=el.querySelector('.node-text');
  span.addEventListener('dblclick',e=>{e.stopPropagation();const t=span.textContent;const input=document.createElement('input');
    input.value=t;input.style.cssText='border:none;background:transparent;text-align:center;font-size:.9rem;width:100%;outline:none';
    span.textContent='';span.appendChild(input);input.focus();
    input.addEventListener('blur',()=>{span.textContent=input.value||'Double-click to edit';const n=nodes.find(n=>n.id===id);if(n)n.text=span.textContent});
    input.addEventListener('keydown',ev=>{if(ev.key==='Enter')input.blur()});
  });
}
function startDrag(e,id){if(e.target.tagName==='BUTTON'||e.target.tagName==='INPUT')return;e.preventDefault();
  dragging=nodes.find(n=>n.id===id);if(!dragging)return;
  const rect=dragging.el.getBoundingClientRect();offsetX=e.clientX-rect.left;offsetY=e.clientY-rect.top;selectNode(id)}
function selectNode(id){if(selectedNode)selectedNode.el.classList.remove('selected');
  selectedNode=nodes.find(n=>n.id===id);if(selectedNode)selectedNode.el.classList.add('selected')}
function removeNode(id){const n=nodes.find(n=>n.id===id);if(n){n.el.remove();nodes=nodes.filter(n=>n.id!==id);if(selectedNode&&selectedNode.id===id)selectedNode=null}}
function clearAll(){nodes.forEach(n=>n.el.remove());nodes=[];selectedNode=null;nodeId=0}
canvas.addEventListener('click',e=>{if(e.target===canvas){const rect=canvas.getBoundingClientRect();
  addNode(e.clientX-rect.left-60,e.clientY-rect.top-20,'Double-click to edit')}});
document.addEventListener('mousemove',e=>{if(!dragging)return;const rect=canvas.getBoundingClientRect();
  dragging.el.style.left=(e.clientX-rect.left-offsetX)+'px';dragging.el.style.top=(e.clientY-rect.top-offsetY)+'px';
  dragging.x=parseInt(dragging.el.style.left);dragging.y=parseInt(dragging.el.style.top)});
document.addEventListener('mouseup',()=>{dragging=null});
document.addEventListener('keydown',e=>{if(e.key==='Delete'&&selectedNode){removeNode(selectedNode.id)}});
setMode('rect');
</script>
</body>
</html>
"""

# ============================================================
# 工具2: emojify - 文字转Emoji
# ============================================================
EMOJIFY_CN = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>文字转Emoji - 在线Emojify工具 | Free ToolBase</title>
  <meta name="description" content="免费在线文字转Emoji工具，将普通文字转换为表情符号。支持字母、数字、符号到emoji的一键转换，让文字更有趣。">
  <meta property="og:title" content="文字转Emoji - 在线Emojify工具 | Free ToolBase">
  <meta property="og:description" content="免费在线文字转Emoji工具，将普通文字转换为表情符号。支持字母、数字、符号到emoji的一键转换，让文字更有趣。">
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://free-toolbase.com/emojify/">
  <script type="application/ld+json">{"@context":"https://schema.org","@type":"SoftwareApplication","name":"文字转Emoji","applicationCategory":"UtilityApplication","operatingSystem":"Web Browser","description":"免费在线文字转Emoji工具，将普通文字转换为表情符号。","url":"https://free-toolbase.com/emojify/"}</script>
  <style>
    :root{--primary:#4F46E5;--primary-hover:#4338CA;--bg:#f8fafc;--surface:#fff;--text:#1e293b;--text-secondary:#64748b;--border:#e2e8f0;--radius:12px}
    *{margin:0;padding:0;box-sizing:border-box}
    body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;background:var(--bg);color:var(--text);min-height:100vh;display:flex;flex-direction:column}
    header{background:var(--surface);border-bottom:1px solid var(--border);padding:16px 24px;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px}
    header h1{font-size:1.25rem;font-weight:700}
    header a{color:var(--primary);text-decoration:none;font-size:.9rem}
    main{flex:1;padding:24px;max-width:800px;margin:0 auto;width:100%}
    .card{background:var(--surface);border-radius:var(--radius);padding:24px;box-shadow:0 1px 3px rgba(0,0,0,.08);margin-bottom:16px}
    textarea{width:100%;min-height:120px;border:1px solid var(--border);border-radius:8px;padding:12px;font-size:1rem;resize:vertical;font-family:inherit}
    textarea:focus{outline:none;border-color:var(--primary);box-shadow:0 0 0 3px rgba(79,70,229,.1)}
    .btn-row{display:flex;gap:8px;flex-wrap:wrap;margin-top:12px}
    button{padding:10px 20px;border:none;border-radius:8px;cursor:pointer;font-size:.9rem;font-weight:600;transition:all .2s}
    .btn-primary{background:var(--primary);color:#fff}.btn-primary:hover{background:var(--primary-hover)}
    .btn-outline{background:var(--surface);color:var(--primary);border:1px solid var(--primary)}.btn-outline:hover{background:rgba(79,70,229,.05)}
    .btn-sm{padding:6px 12px;font-size:.8rem}
    .output-box{background:#f1f5f9;border-radius:8px;padding:16px;min-height:60px;font-size:1.2rem;word-break:break-all;line-height:1.8}
    .mode-tabs{display:flex;gap:4px;margin-bottom:12px;flex-wrap:wrap}
    .mode-tab{padding:6px 14px;border:1px solid var(--border);border-radius:20px;cursor:pointer;font-size:.85rem;background:var(--surface);transition:all .2s}
    .mode-tab.active{background:var(--primary);color:#fff;border-color:var(--primary)}
    footer{background:var(--surface);border-top:1px solid var(--border);padding:16px 24px;text-align:center;font-size:.8rem;color:var(--text-secondary)}
    @media(max-width:600px){main{padding:12px}.card{padding:16px}textarea{min-height:100px}}
  </style>
</head>
<body>
<header>
  <h1>😀 文字转Emoji</h1>
  <a href="/">← 返回首页</a>
</header>
<main>
  <div class="card">
    <div class="mode-tabs">
      <span class="mode-tab active" data-mode="letter">🔤 字母→Emoji</span>
      <span class="mode-tab" data-mode="word">📝 单词→Emoji</span>
      <span class="mode-tab" data-mode="custom">✨ 自定义映射</span>
    </div>
    <textarea id="input" placeholder="输入要转换的文字...&#10;例如：Hello World 或 I love coding"></textarea>
    <div class="btn-row">
      <button class="btn-primary" onclick="emojify()">🎨 转换为Emoji</button>
      <button class="btn-outline" onclick="copyOutput()">📋 复制结果</button>
      <button class="btn-outline btn-sm" onclick="clearAll()">🗑️ 清空</button>
    </div>
  </div>
  <div class="card">
    <h3 style="margin-bottom:8px;font-size:.95rem;color:var(--text-secondary)">转换结果</h3>
    <div class="output-box" id="output">等待输入...</div>
  </div>
</main>
<footer>© 2025 Free ToolBase · 免费在线工具</footer>
<script>
const letterMap={a:'🅰️',b:'🅱️',c:'©️',d:'↩️',e:'📧',f:'🎏',g:'🌀',h:'♓',i:'ℹ️',j:'🕹️',k:'🎋',l:'👢',m:'Ⓜ️',n:'♑',o:'⭕',p:'🅿️',q:'👑',r:'®️',s:'💲',t:'✝️',u:'⛎',v:'✌️',w:'〰️',x:'❌',y:'🍸',z:'💤'};
const wordMap={hello:'👋',hi:'👋',love:'❤️',happy:'😊',sad:'😢',cool:'😎',fire:'🔥',star:'⭐',sun:'☀️',moon:'🌙',heart:'💖',music:'🎵',food:'🍕',pizza:'🍕',coffee:'☕',beer:'🍺',cat:'🐱',dog:'🐶',laugh:'😂',cry:'😭',angry:'😡',money:'💰',time:'⏰',ok:'👌',yes:'✅',no:'❌',thanks:'🙏','thank':'🙏',good:'👍',bad:'👎',great:'👏',wow:'😮',party:'🎉',birthday:'🎂',gift:'🎁',phone:'📱',computer:'💻',book:'📖',car:'🚗',home:'🏠',run:'🏃',sleep:'😴',eat:'🍽️',dance:'💃',rain:'🌧️',snow:'❄️',lol:'😂',omg:'😱',coding:'👨‍💻'};
let currentMode='letter';
document.querySelectorAll('.mode-tab').forEach(t=>{t.addEventListener('click',function(){document.querySelectorAll('.mode-tab').forEach(x=>x.classList.remove('active'));this.classList.add('active');currentMode=this.dataset.mode})});
function emojify(){const input=document.getElementById('input').value.trim();const output=document.getElementById('output');
  if(!input){output.textContent='请输入文字';return}
  let result;
  if(currentMode==='letter'){result=input.toLowerCase().split('').map(c=>letterMap[c]||c).join(' ')}
  else if(currentMode==='word'){result=input.split(/\s+/).map(w=>{const clean=w.replace(/[^a-zA-Z]/g,'').toLowerCase();return wordMap[clean]||w}).join(' ')}
  else{result=input}
  output.textContent=result||'转换完成'}
function copyOutput(){const t=document.getElementById('output').textContent;if(!t||t==='等待输入...')return;
  navigator.clipboard.writeText(t).then(()=>showToast('✅ 已复制')).catch(()=>showToast('❌ 复制失败'))}
function clearAll(){document.getElementById('input').value='';document.getElementById('output').textContent='等待输入...'}
function showToast(msg){const t=document.createElement('div');t.style.cssText='position:fixed;bottom:20px;right:20px;background:#333;color:#fff;padding:12px 20px;border-radius:8px;z-index:9999;font-size:.9rem;animation:fadeIn .3s';
  t.textContent=msg;document.body.appendChild(t);setTimeout(()=>{t.style.opacity='0';t.style.transition='opacity .3s';setTimeout(()=>t.remove(),300)},2000)}
</script>
</body>
</html>
"""

EMOJIFY_EN = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Text to Emoji - Online Emojify Tool | Free ToolBase</title>
  <meta name="description" content="Free online text to emoji converter. Turn plain text into fun emoji symbols. Supports letter, word, and custom mapping. No sign-up needed.">
  <meta property="og:title" content="Text to Emoji - Online Emojify Tool | Free ToolBase">
  <meta property="og:description" content="Free online text to emoji converter. Turn plain text into fun emoji symbols. Supports letter, word, and custom mapping. No sign-up needed.">
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://free-toolbase.com/en/emojify/">
  <script type="application/ld+json">{"@context":"https://schema.org","@type":"SoftwareApplication","name":"Text to Emoji","applicationCategory":"UtilityApplication","operatingSystem":"Web Browser","description":"Free online text to emoji converter. Turn plain text into fun emoji symbols.","url":"https://free-toolbase.com/en/emojify/"}</script>
  <style>
    :root{--primary:#4F46E5;--primary-hover:#4338CA;--bg:#f8fafc;--surface:#fff;--text:#1e293b;--text-secondary:#64748b;--border:#e2e8f0;--radius:12px}
    *{margin:0;padding:0;box-sizing:border-box}
    body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;background:var(--bg);color:var(--text);min-height:100vh;display:flex;flex-direction:column}
    header{background:var(--surface);border-bottom:1px solid var(--border);padding:16px 24px;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px}
    header h1{font-size:1.25rem;font-weight:700}
    header a{color:var(--primary);text-decoration:none;font-size:.9rem}
    main{flex:1;padding:24px;max-width:800px;margin:0 auto;width:100%}
    .card{background:var(--surface);border-radius:var(--radius);padding:24px;box-shadow:0 1px 3px rgba(0,0,0,.08);margin-bottom:16px}
    textarea{width:100%;min-height:120px;border:1px solid var(--border);border-radius:8px;padding:12px;font-size:1rem;resize:vertical;font-family:inherit}
    textarea:focus{outline:none;border-color:var(--primary);box-shadow:0 0 0 3px rgba(79,70,229,.1)}
    .btn-row{display:flex;gap:8px;flex-wrap:wrap;margin-top:12px}
    button{padding:10px 20px;border:none;border-radius:8px;cursor:pointer;font-size:.9rem;font-weight:600;transition:all .2s}
    .btn-primary{background:var(--primary);color:#fff}.btn-primary:hover{background:var(--primary-hover)}
    .btn-outline{background:var(--surface);color:var(--primary);border:1px solid var(--primary)}.btn-outline:hover{background:rgba(79,70,229,.05)}
    .btn-sm{padding:6px 12px;font-size:.8rem}
    .output-box{background:#f1f5f9;border-radius:8px;padding:16px;min-height:60px;font-size:1.2rem;word-break:break-all;line-height:1.8}
    .mode-tabs{display:flex;gap:4px;margin-bottom:12px;flex-wrap:wrap}
    .mode-tab{padding:6px 14px;border:1px solid var(--border);border-radius:20px;cursor:pointer;font-size:.85rem;background:var(--surface);transition:all .2s}
    .mode-tab.active{background:var(--primary);color:#fff;border-color:var(--primary)}
    footer{background:var(--surface);border-top:1px solid var(--border);padding:16px 24px;text-align:center;font-size:.8rem;color:var(--text-secondary)}
    @media(max-width:600px){main{padding:12px}.card{padding:16px}textarea{min-height:100px}}
  </style>
</head>
<body>
<header>
  <h1>😀 Text to Emoji</h1>
  <a href="/en/">← Back to Home</a>
</header>
<main>
  <div class="card">
    <div class="mode-tabs">
      <span class="mode-tab active" data-mode="letter">🔤 Letter→Emoji</span>
      <span class="mode-tab" data-mode="word">📝 Word→Emoji</span>
      <span class="mode-tab" data-mode="custom">✨ Custom Mapping</span>
    </div>
    <textarea id="input" placeholder="Enter text to convert...&#10;Example: Hello World or I love coding"></textarea>
    <div class="btn-row">
      <button class="btn-primary" onclick="emojify()">🎨 Convert to Emoji</button>
      <button class="btn-outline" onclick="copyOutput()">📋 Copy Result</button>
      <button class="btn-outline btn-sm" onclick="clearAll()">🗑️ Clear</button>
    </div>
  </div>
  <div class="card">
    <h3 style="margin-bottom:8px;font-size:.95rem;color:var(--text-secondary)">Result</h3>
    <div class="output-box" id="output">Waiting for input...</div>
  </div>
</main>
<footer>© 2025 Free ToolBase · Free Online Tools</footer>
<script>
const letterMap={a:'🅰️',b:'🅱️',c:'©️',d:'↩️',e:'📧',f:'🎏',g:'🌀',h:'♓',i:'ℹ️',j:'🕹️',k:'🎋',l:'👢',m:'Ⓜ️',n:'♑',o:'⭕',p:'🅿️',q:'👑',r:'®️',s:'💲',t:'✝️',u:'⛎',v:'✌️',w:'〰️',x:'❌',y:'🍸',z:'💤'};
const wordMap={hello:'👋',hi:'👋',love:'❤️',happy:'😊',sad:'😢',cool:'😎',fire:'🔥',star:'⭐',sun:'☀️',moon:'🌙',heart:'💖',music:'🎵',food:'🍕',pizza:'🍕',coffee:'☕',beer:'🍺',cat:'🐱',dog:'🐶',laugh:'😂',cry:'😭',angry:'😡',money:'💰',time:'⏰',ok:'👌',yes:'✅',no:'❌',thanks:'🙏','thank':'🙏',good:'👍',bad:'👎',great:'👏',wow:'😮',party:'🎉',birthday:'🎂',gift:'🎁',phone:'📱',computer:'💻',book:'📖',car:'🚗',home:'🏠',run:'🏃',sleep:'😴',eat:'🍽️',dance:'💃',rain:'🌧️',snow:'❄️',lol:'😂',omg:'😱',coding:'👨‍💻'};
let currentMode='letter';
document.querySelectorAll('.mode-tab').forEach(t=>{t.addEventListener('click',function(){document.querySelectorAll('.mode-tab').forEach(x=>x.classList.remove('active'));this.classList.add('active');currentMode=this.dataset.mode})});
function emojify(){const input=document.getElementById('input').value.trim();const output=document.getElementById('output');
  if(!input){output.textContent='Please enter some text';return}
  let result;
  if(currentMode==='letter'){result=input.toLowerCase().split('').map(c=>letterMap[c]||c).join(' ')}
  else if(currentMode==='word'){result=input.split(/\s+/).map(w=>{const clean=w.replace(/[^a-zA-Z]/g,'').toLowerCase();return wordMap[clean]||w}).join(' ')}
  else{result=input}
  output.textContent=result||'Conversion complete'}
function copyOutput(){const t=document.getElementById('output').textContent;if(!t||t==='Waiting for input...')return;
  navigator.clipboard.writeText(t).then(()=>showToast('✅ Copied')).catch(()=>showToast('❌ Copy failed'))}
function clearAll(){document.getElementById('input').value='';document.getElementById('output').textContent='Waiting for input...'}
function showToast(msg){const t=document.createElement('div');t.style.cssText='position:fixed;bottom:20px;right:20px;background:#333;color:#fff;padding:12px 20px;border-radius:8px;z-index:9999;font-size:.9rem;animation:fadeIn .3s';
  t.textContent=msg;document.body.appendChild(t);setTimeout(()=>{t.style.opacity='0';t.style.transition='opacity .3s';setTimeout(()=>t.remove(),300)},2000)}
</script>
</body>
</html>
"""

# ============================================================
# 工具3: font-generator - 花体字生成器
# ============================================================
FONT_CN = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>花体字生成器 - Unicode风格字体转换 | Free ToolBase</title>
  <meta name="description" content="免费在线花体字生成器，将普通文字转换为多种Unicode风格字体：粗体、斜体、手写体、花体、双线体等。一键复制，支持社交媒体。">
  <meta property="og:title" content="花体字生成器 - Unicode风格字体转换 | Free ToolBase">
  <meta property="og:description" content="免费在线花体字生成器，将普通文字转换为多种Unicode风格字体：粗体、斜体、手写体、花体、双线体等。">
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://free-toolbase.com/font-generator/">
  <script type="application/ld+json">{"@context":"https://schema.org","@type":"SoftwareApplication","name":"花体字生成器","applicationCategory":"UtilityApplication","operatingSystem":"Web Browser","description":"免费在线花体字生成器，将普通文字转换为多种Unicode风格字体。","url":"https://free-toolbase.com/font-generator/"}</script>
  <style>
    :root{--primary:#4F46E5;--primary-hover:#4338CA;--bg:#f8fafc;--surface:#fff;--text:#1e293b;--text-secondary:#64748b;--border:#e2e8f0;--radius:12px}
    *{margin:0;padding:0;box-sizing:border-box}
    body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;background:var(--bg);color:var(--text);min-height:100vh;display:flex;flex-direction:column}
    header{background:var(--surface);border-bottom:1px solid var(--border);padding:16px 24px;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px}
    header h1{font-size:1.25rem;font-weight:700}
    header a{color:var(--primary);text-decoration:none;font-size:.9rem}
    main{flex:1;padding:24px;max-width:900px;margin:0 auto;width:100%}
    .card{background:var(--surface);border-radius:var(--radius);padding:24px;box-shadow:0 1px 3px rgba(0,0,0,.08);margin-bottom:16px}
    textarea{width:100%;min-height:80px;border:1px solid var(--border);border-radius:8px;padding:12px;font-size:1rem;resize:vertical;font-family:inherit}
    textarea:focus{outline:none;border-color:var(--primary);box-shadow:0 0 0 3px rgba(79,70,229,.1)}
    .font-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:12px;margin-top:16px}
    .font-item{background:#f8fafc;border:1px solid var(--border);border-radius:8px;padding:12px;cursor:pointer;transition:all .2s;text-align:center}
    .font-item:hover{border-color:var(--primary);box-shadow:0 2px 8px rgba(79,70,229,.1)}
    .font-label{font-size:.75rem;color:var(--text-secondary);margin-bottom:4px}
    .font-preview{font-size:1.1rem;word-break:break-all;line-height:1.5;min-height:24px}
    .copy-btn{padding:6px 12px;background:var(--primary);color:#fff;border:none;border-radius:6px;cursor:pointer;font-size:.8rem;margin-top:8px;transition:all .2s}
    .copy-btn:hover{background:var(--primary-hover)}
    footer{background:var(--surface);border-top:1px solid var(--border);padding:16px 24px;text-align:center;font-size:.8rem;color:var(--text-secondary)}
    @media(max-width:600px){main{padding:12px}.card{padding:16px}.font-grid{grid-template-columns:repeat(auto-fill,minmax(150px,1fr))}}
  </style>
</head>
<body>
<header>
  <h1>✨ 花体字生成器</h1>
  <a href="/">← 返回首页</a>
</header>
<main>
  <div class="card">
    <textarea id="input" placeholder="输入文字，即时预览各种字体风格..."></textarea>
  </div>
  <div class="font-grid" id="font-grid"></div>
</main>
<footer>© 2025 Free ToolBase · 免费在线工具</footer>
<script>
const fonts=[
  {name:'粗体 Bold',map:'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789',to:'𝗔𝗕𝗖𝗗𝗘𝗙𝗚𝗛𝗜𝗝𝗞𝗟𝗠𝗡𝗢𝗣𝗤𝗥𝗦𝗧𝗨𝗩𝗪𝗫𝗬𝗭𝗮𝗯𝗰𝗱𝗲𝗳𝗴𝗵𝗶𝗷𝗸𝗹𝗺𝗻𝗼𝗽𝗾𝗿𝘀𝘁𝘂𝘃𝘄𝘅𝘆𝘇𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵'},
  {name:'斜体 Italic',map:'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789',to:'𝘈𝘉𝘊𝘋𝘌𝘍𝘎𝘏𝘐𝘑𝘒𝘓𝘔𝘕𝘖𝘗𝘘𝘙𝘚𝘛𝘜𝘝𝘞𝘟𝘠𝘡𝘢𝘣𝘤𝘥𝘦𝘧𝘨𝘩𝘪𝘫𝘬𝘭𝘮𝘯𝘰𝘱𝘲𝘳𝘴𝘵𝘶𝘷𝘸𝘹𝘺𝘻0123456789'},
  {name:'粗斜体 Bold Italic',map:'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789',to:'𝘼𝘽𝘾𝘿𝙀𝙁𝙂𝙃𝙄𝙅𝙆𝙇𝙈𝙉𝙊𝙋𝙌𝙍𝙎𝙏𝙐𝙑𝙒𝙓𝙔𝙕𝙖𝙗𝙘𝙙𝙚𝙛𝙜𝙝𝙞𝙟𝙠𝙡𝙢𝙣𝙤𝙥𝙦𝙧𝙨𝙩𝙪𝙫𝙬𝙭𝙮𝙯0123456789'},
  {name:'手写体 Script',map:'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz',to:'𝒜𝐵𝒞𝒟𝐸𝐹𝒢𝐻𝐼𝒥𝒦𝐿𝑀𝒩𝒪𝒫𝒬𝑅𝒮𝒯𝒰𝒱𝒲𝒳𝒴𝒵𝒶𝒷𝒸𝒹𝑒𝒻𝑔𝒽𝒾𝒿𝓀𝓁𝓂𝓃𝑜𝓅𝓆𝓇𝓈𝓉𝓊𝓋𝓌𝓍𝓎𝓏'},
  {name:'花体 Fraktur',map:'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz',to:'𝔄𝔅ℭ𝔇𝔈𝔉𝔊ℌℑ𝔍𝔎𝔏𝔐𝔑𝔒𝔓𝔔ℜ𝔖𝔗𝔘𝔙𝔚𝔛𝔜ℨ𝔞𝔟𝔠𝔡𝔢𝔣𝔤𝔥𝔦𝔧𝔨𝔩𝔪𝔫𝔬𝔭𝔮𝔯𝔰𝔱𝔲𝔳𝔴𝔵𝔶𝔷'},
  {name:'双线 Double-struck',map:'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789',to:'𝔸𝔹ℂ𝔻𝔼𝔽𝔾ℍ𝕀𝕁𝕂𝕃𝕄ℕ𝕆ℙℚℝ𝕊𝕋𝕌𝕍𝕎𝕏𝕐ℤ𝕒𝕓𝕔𝕕𝕖𝕗𝕘𝕙𝕚𝕛𝕜𝕝𝕞𝕟𝕠𝕡𝕢𝕣𝕤𝕥𝕦𝕧𝕨𝕩𝕪𝕫𝟘𝟙𝟚𝟛𝟜𝟝𝟞𝟟𝟠𝟡'},
  {name:'无衬线 Sans-serif',map:'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789',to:'𝖠𝖡𝖢𝖣𝖤𝖥𝖦𝖧𝖨𝖩𝖪𝖫𝖬𝖭𝖮𝖯𝖰𝖱𝖲𝖳𝖴𝖵𝖶𝖷𝖸𝖹𝖺𝖻𝖼𝖽𝖾𝖿𝗀𝗁𝗂𝗃𝗄𝗅𝗆𝗇𝗈𝗉𝗊𝗋𝗌𝗍𝗎𝗏𝗐𝗑𝗒𝗓𝟢𝟣𝟤𝟥𝟦𝟧𝟨𝟩𝟪𝟫'},
  {name:'无衬线粗体',map:'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789',to:'𝗔𝗕𝗖𝗗𝗘𝗙𝗚𝗛𝗜𝗝𝗞𝗟𝗠𝗡𝗢𝗣𝗤𝗥𝗦𝗧𝗨𝗩𝗪𝗫𝗬𝗭𝗮𝗯𝗰𝗱𝗲𝗳𝗴𝗵𝗶𝗷𝗸𝗹𝗺𝗻𝗼𝗽𝗾𝗿𝘀𝘁𝘂𝘃𝘄𝘅𝘆𝘇𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵'},
  {name:'小号大写 Small Caps',map:'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz',to:'ᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘǫʀꜱᴛᴜᴠᴡxʏᴢᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘǫʀꜱᴛᴜᴠᴡxʏᴢ'},
  {name:'圈字 Circled',map:'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789',to:'🄐🄑🄒🄓🄔🄕🄖🄗🄘🄙🄚🄛🄜🄝🄞🄟🄠🄡🄢🄣🄤🄥🄦🄧🄨🄩ⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩ⓪①②③④⑤⑥⑦⑧⑨'},
  {name:'上下颠倒 Upside Down',map:'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789',to:'∀𐐒Ɔ◖ƎℲ⅁HIſ⋊⅂WNOԀΌᴚS⊥∩ΛMX⅄Zɐqɔpǝɟɓɥıɾʞlɯuodbɹsʇnʌʍxʎz0⇂ᘔ⇂456789'},
  {name:'划线 Strikethrough',map:'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789',to:'A̶B̶C̶D̶E̶F̶G̶H̶I̶J̶K̶L̶M̶N̶O̶P̶Q̶R̶S̶T̶U̶V̶W̶X̶Y̶Z̶a̶b̶c̶d̶e̶f̶g̶h̶i̶j̶k̶l̶m̶n̶o̶p̶q̶r̶s̶t̶u̶v̶w̶x̶y̶z̶0̶1̶2̶3̶4̶5̶6̶7̶8̶9̶'},
];
function convert(text,font){
  let result='';
  for(const ch of text){
    const idx=font.map.indexOf(ch);
    result+=idx>=0?font.to[idx]:ch;
  }
  return result;
}
function renderFonts(){
  const input=document.getElementById('input').value||'Hello World';
  const grid=document.getElementById('font-grid');
  grid.innerHTML=fonts.map((f,i)=>`<div class="font-item">
    <div class="font-label">${f.name}</div>
    <div class="font-preview">${convert(input,f)}</div>
    <button class="copy-btn" onclick="copyFont(${i})">📋 复制</button>
  </div>`).join('');
}
function copyFont(i){
  const input=document.getElementById('input').value||'Hello World';
  const result=convert(input,fonts[i]);
  navigator.clipboard.writeText(result).then(()=>showToast('✅ 已复制')).catch(()=>showToast('❌ 复制失败'));
}
document.getElementById('input').addEventListener('input',renderFonts);
renderFonts();
function showToast(msg){const t=document.createElement('div');t.style.cssText='position:fixed;bottom:20px;right:20px;background:#333;color:#fff;padding:12px 20px;border-radius:8px;z-index:9999;font-size:.9rem';
  t.textContent=msg;document.body.appendChild(t);setTimeout(()=>{t.style.opacity='0';t.style.transition='opacity .3s';setTimeout(()=>t.remove(),300)},2000)}
</script>
</body>
</html>
"""

FONT_EN = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Font Generator - Unicode Style Text Converter | Free ToolBase</title>
  <meta name="description" content="Free online font generator. Convert plain text into multiple Unicode font styles: bold, italic, script, fraktur, double-struck, and more. One-click copy for social media.">
  <meta property="og:title" content="Font Generator - Unicode Style Text Converter | Free ToolBase">
  <meta property="og:description" content="Free online font generator. Convert plain text into multiple Unicode font styles: bold, italic, script, fraktur, double-struck, and more.">
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://free-toolbase.com/en/font-generator/">
  <script type="application/ld+json">{"@context":"https://schema.org","@type":"SoftwareApplication","name":"Font Generator","applicationCategory":"UtilityApplication","operatingSystem":"Web Browser","description":"Free online font generator. Convert plain text into multiple Unicode font styles.","url":"https://free-toolbase.com/en/font-generator/"}</script>
  <style>
    :root{--primary:#4F46E5;--primary-hover:#4338CA;--bg:#f8fafc;--surface:#fff;--text:#1e293b;--text-secondary:#64748b;--border:#e2e8f0;--radius:12px}
    *{margin:0;padding:0;box-sizing:border-box}
    body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;background:var(--bg);color:var(--text);min-height:100vh;display:flex;flex-direction:column}
    header{background:var(--surface);border-bottom:1px solid var(--border);padding:16px 24px;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px}
    header h1{font-size:1.25rem;font-weight:700}
    header a{color:var(--primary);text-decoration:none;font-size:.9rem}
    main{flex:1;padding:24px;max-width:900px;margin:0 auto;width:100%}
    .card{background:var(--surface);border-radius:var(--radius);padding:24px;box-shadow:0 1px 3px rgba(0,0,0,.08);margin-bottom:16px}
    textarea{width:100%;min-height:80px;border:1px solid var(--border);border-radius:8px;padding:12px;font-size:1rem;resize:vertical;font-family:inherit}
    textarea:focus{outline:none;border-color:var(--primary);box-shadow:0 0 0 3px rgba(79,70,229,.1)}
    .font-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:12px;margin-top:16px}
    .font-item{background:#f8fafc;border:1px solid var(--border);border-radius:8px;padding:12px;cursor:pointer;transition:all .2s;text-align:center}
    .font-item:hover{border-color:var(--primary);box-shadow:0 2px 8px rgba(79,70,229,.1)}
    .font-label{font-size:.75rem;color:var(--text-secondary);margin-bottom:4px}
    .font-preview{font-size:1.1rem;word-break:break-all;line-height:1.5;min-height:24px}
    .copy-btn{padding:6px 12px;background:var(--primary);color:#fff;border:none;border-radius:6px;cursor:pointer;font-size:.8rem;margin-top:8px;transition:all .2s}
    .copy-btn:hover{background:var(--primary-hover)}
    footer{background:var(--surface);border-top:1px solid var(--border);padding:16px 24px;text-align:center;font-size:.8rem;color:var(--text-secondary)}
    @media(max-width:600px){main{padding:12px}.card{padding:16px}.font-grid{grid-template-columns:repeat(auto-fill,minmax(150px,1fr))}}
  </style>
</head>
<body>
<header>
  <h1>✨ Font Generator</h1>
  <a href="/en/">← Back to Home</a>
</header>
<main>
  <div class="card">
    <textarea id="input" placeholder="Type your text to preview different font styles..."></textarea>
  </div>
  <div class="font-grid" id="font-grid"></div>
</main>
<footer>© 2025 Free ToolBase · Free Online Tools</footer>
<script>
const fonts=[
  {name:'Bold',map:'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789',to:'𝗔𝗕𝗖𝗗𝗘𝗙𝗚𝗛𝗜𝗝𝗞𝗟𝗠𝗡𝗢𝗣𝗤𝗥𝗦𝗧𝗨𝗩𝗪𝗫𝗬𝗭𝗮𝗯𝗰𝗱𝗲𝗳𝗴𝗵𝗶𝗷𝗸𝗹𝗺𝗻𝗼𝗽𝗾𝗿𝘀𝘁𝘂𝘃𝘄𝘅𝘆𝘇𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵'},
  {name:'Italic',map:'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789',to:'𝘈𝘉𝘊𝘋𝘌𝘍𝘎𝘏𝘐𝘑𝘒𝘓𝘔𝘕𝘖𝘗𝘘𝘙𝘚𝘛𝘜𝘝𝘞𝘟𝘠𝘡𝘢𝘣𝘤𝘥𝘦𝘧𝘨𝘩𝘪𝘫𝘬𝘭𝘮𝘯𝘰𝘱𝘲𝘳𝘴𝘵𝘶𝘷𝘸𝘹𝘺𝘻0123456789'},
  {name:'Bold Italic',map:'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789',to:'𝘼𝘽𝘾𝘿𝙀𝙁𝙂𝙃𝙄𝙅𝙆𝙇𝙈𝙉𝙊𝙋𝙌𝙍𝙎𝙏𝙐𝙑𝙒𝙓𝙔𝙕𝙖𝙗𝙘𝙙𝙚𝙛𝙜𝙝𝙞𝙟𝙠𝙡𝙢𝙣𝙤𝙥𝙦𝙧𝙨𝙩𝙪𝙫𝙬𝙭𝙮𝙯0123456789'},
  {name:'Script',map:'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz',to:'𝒜𝐵𝒞𝒟𝐸𝐹𝒢𝐻𝐼𝒥𝒦𝐿𝑀𝒩𝒪𝒫𝒬𝑅𝒮𝒯𝒰𝒱𝒲𝒳𝒴𝒵𝒶𝒷𝒸𝒹𝑒𝒻𝑔𝒽𝒾𝒿𝓀𝓁𝓂𝓃𝑜𝓅𝓆𝓇𝓈𝓉𝓊𝓋𝓌𝓍𝓎𝓏'},
  {name:'Fraktur',map:'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz',to:'𝔄𝔅ℭ𝔇𝔈𝔉𝔊ℌℑ𝔍𝔎𝔏𝔐𝔑𝔒𝔓𝔔ℜ𝔖𝔗𝔘𝔙𝔚𝔛𝔜ℨ𝔞𝔟𝔠𝔡𝔢𝔣𝔤𝔥𝔦𝔧𝔨𝔩𝔪𝔫𝔬𝔭𝔮𝔯𝔰𝔱𝔲𝔳𝔴𝔵𝔶𝔷'},
  {name:'Double-struck',map:'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789',to:'𝔸𝔹ℂ𝔻𝔼𝔽𝔾ℍ𝕀𝕁𝕂𝕃𝕄ℕ𝕆ℙℚℝ𝕊𝕋𝕌𝕍𝕎𝕏𝕐ℤ𝕒𝕓𝕔𝕕𝕖𝕗𝕘𝕙𝕚𝕛𝕜𝕝𝕞𝕟𝕠𝕡𝕢𝕣𝕤𝕥𝕦𝕧𝕨𝕩𝕪𝕫𝟘𝟙𝟚𝟛𝟜𝟝𝟞𝟟𝟠𝟡'},
  {name:'Sans-serif',map:'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789',to:'𝖠𝖡𝖢𝖣𝖤𝖥𝖦𝖧𝖨𝖩𝖪𝖫𝖬𝖭𝖮𝖯𝖰𝖱𝖲𝖳𝖴𝖵𝖶𝖷𝖸𝖹𝖺𝖻𝖼𝖽𝖾𝖿𝗀𝗁𝗂𝗃𝗄𝗅𝗆𝗇𝗈𝗉𝗊𝗋𝗌𝗍𝗎𝗏𝗐𝗑𝗒𝗓𝟢𝟣𝟤𝟥𝟦𝟧𝟨𝟩𝟪𝟫'},
  {name:'Sans-serif Bold',map:'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789',to:'𝗔𝗕𝗖𝗗𝗘𝗙𝗚𝗛𝗜𝗝𝗞𝗟𝗠𝗡𝗢𝗣𝗤𝗥𝗦𝗧𝗨𝗩𝗪𝗫𝗬𝗭𝗮𝗯𝗰𝗱𝗲𝗳𝗴𝗵𝗶𝗷𝗸𝗹𝗺𝗻𝗼𝗽𝗾𝗿𝘀𝘁𝘂𝘃𝘄𝘅𝘆𝘇𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵'},
  {name:'Small Caps',map:'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz',to:'ᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘǫʀꜱᴛᴜᴠᴡxʏᴢᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘǫʀꜱᴛᴜᴠᴡxʏᴢ'},
  {name:'Circled',map:'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789',to:'🄐🄑🄒🄓🄔🄕🄖🄗🄘🄙🄚🄛🄜🄝🄞🄟🄠🄡🄢🄣🄤🄥🄦🄧🄨🄩ⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩ⓪①②③④⑤⑥⑦⑧⑨'},
  {name:'Upside Down',map:'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789',to:'∀𐐒Ɔ◖ƎℲ⅁HIſ⋊⅂WNOԀΌᴚS⊥∩ΛMX⅄Zɐqɔpǝɟɓɥıɾʞlɯuodbɹsʇnʌʍxʎz0⇂ᘔ⇂456789'},
  {name:'Strikethrough',map:'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789',to:'A̶B̶C̶D̶E̶F̶G̶H̶I̶J̶K̶L̶M̶N̶O̶P̶Q̶R̶S̶T̶U̶V̶W̶X̶Y̶Z̶a̶b̶c̶d̶e̶f̶g̶h̶i̶j̶k̶l̶m̶n̶o̶p̶q̶r̶s̶t̶u̶v̶w̶x̶y̶z̶0̶1̶2̶3̶4̶5̶6̶7̶8̶9̶'},
];
function convert(text,font){
  let result='';
  for(const ch of text){
    const idx=font.map.indexOf(ch);
    result+=idx>=0?font.to[idx]:ch;
  }
  return result;
}
function renderFonts(){
  const input=document.getElementById('input').value||'Hello World';
  const grid=document.getElementById('font-grid');
  grid.innerHTML=fonts.map((f,i)=>`<div class="font-item">
    <div class="font-label">${f.name}</div>
    <div class="font-preview">${convert(input,f)}</div>
    <button class="copy-btn" onclick="copyFont(${i})">📋 Copy</button>
  </div>`).join('');
}
function copyFont(i){
  const input=document.getElementById('input').value||'Hello World';
  const result=convert(input,fonts[i]);
  navigator.clipboard.writeText(result).then(()=>showToast('✅ Copied')).catch(()=>showToast('❌ Copy failed'));
}
document.getElementById('input').addEventListener('input',renderFonts);
renderFonts();
function showToast(msg){const t=document.createElement('div');t.style.cssText='position:fixed;bottom:20px;right:20px;background:#333;color:#fff;padding:12px 20px;border-radius:8px;z-index:9999;font-size:.9rem';
  t.textContent=msg;document.body.appendChild(t);setTimeout(()=>{t.style.opacity='0';t.style.transition='opacity .3s';setTimeout(()=>t.remove(),300)},2000)}
</script>
</body>
</html>
"""

# ============================================================
# 工具4: utm-builder - UTM参数构建器
# ============================================================
UTM_CN = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>UTM参数构建器 - 在线URL追踪链接生成 | Free ToolBase</title>
  <meta name="description" content="免费在线UTM参数构建器，可视化生成带UTM追踪参数的URL。支持Google Analytics、百度统计等。批量生成、一键复制。">
  <meta property="og:title" content="UTM参数构建器 - 在线URL追踪链接生成 | Free ToolBase">
  <meta property="og:description" content="免费在线UTM参数构建器，可视化生成带UTM追踪参数的URL。支持Google Analytics、百度统计等。">
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://free-toolbase.com/utm-builder/">
  <script type="application/ld+json">{"@context":"https://schema.org","@type":"SoftwareApplication","name":"UTM参数构建器","applicationCategory":"BusinessApplication","operatingSystem":"Web Browser","description":"免费在线UTM参数构建器，可视化生成带UTM追踪参数的URL。","url":"https://free-toolbase.com/utm-builder/"}</script>
  <style>
    :root{--primary:#4F46E5;--primary-hover:#4338CA;--bg:#f8fafc;--surface:#fff;--text:#1e293b;--text-secondary:#64748b;--border:#e2e8f0;--radius:12px}
    *{margin:0;padding:0;box-sizing:border-box}
    body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;background:var(--bg);color:var(--text);min-height:100vh;display:flex;flex-direction:column}
    header{background:var(--surface);border-bottom:1px solid var(--border);padding:16px 24px;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px}
    header h1{font-size:1.25rem;font-weight:700}
    header a{color:var(--primary);text-decoration:none;font-size:.9rem}
    main{flex:1;padding:24px;max-width:800px;margin:0 auto;width:100%}
    .card{background:var(--surface);border-radius:var(--radius);padding:24px;box-shadow:0 1px 3px rgba(0,0,0,.08);margin-bottom:16px}
    .form-group{margin-bottom:14px}
    .form-group label{display:block;font-size:.85rem;font-weight:600;margin-bottom:4px;color:var(--text-secondary)}
    .form-group label .req{color:#ef4444}
    .form-group input,.form-group select{width:100%;padding:10px 12px;border:1px solid var(--border);border-radius:8px;font-size:.9rem;font-family:inherit}
    .form-group input:focus,.form-group select:focus{outline:none;border-color:var(--primary);box-shadow:0 0 0 3px rgba(79,70,229,.1)}
    .form-row{display:grid;grid-template-columns:1fr 1fr;gap:12px}
    .btn-row{display:flex;gap:8px;flex-wrap:wrap;margin-top:16px}
    button{padding:10px 20px;border:none;border-radius:8px;cursor:pointer;font-size:.9rem;font-weight:600;transition:all .2s}
    .btn-primary{background:var(--primary);color:#fff}.btn-primary:hover{background:var(--primary-hover)}
    .btn-outline{background:var(--surface);color:var(--primary);border:1px solid var(--primary)}.btn-outline:hover{background:rgba(79,70,229,.05)}
    .output-box{background:#f1f5f9;border-radius:8px;padding:16px;font-family:monospace;font-size:.9rem;word-break:break-all;line-height:1.6}
    .param-list{margin-top:12px}
    .param-item{display:flex;justify-content:space-between;align-items:center;padding:6px 0;border-bottom:1px solid var(--border);font-size:.85rem}
    .param-item code{background:#f1f5f9;padding:2px 6px;border-radius:4px;font-size:.8rem}
    footer{background:var(--surface);border-top:1px solid var(--border);padding:16px 24px;text-align:center;font-size:.8rem;color:var(--text-secondary)}
    @media(max-width:600px){main{padding:12px}.card{padding:16px}.form-row{grid-template-columns:1fr}}
  </style>
</head>
<body>
<header>
  <h1>🔗 UTM参数构建器</h1>
  <a href="/">← 返回首页</a>
</header>
<main>
  <div class="card">
    <div class="form-group">
      <label>网站URL <span class="req">*</span></label>
      <input type="url" id="base-url" placeholder="https://example.com/landing-page" value="">
    </div>
    <div class="form-group">
      <label>流量来源 (utm_source) <span class="req">*</span></label>
      <input type="text" id="utm-source" placeholder="例如: google, newsletter, facebook" value="">
    </div>
    <div class="form-group">
      <label>流量媒介 (utm_medium) <span class="req">*</span></label>
      <select id="utm-medium">
        <option value="">-- 选择媒介 --</option>
        <option value="cpc">CPC (付费点击)</option>
        <option value="social">Social (社交媒体)</option>
        <option value="email">Email (邮件)</option>
        <option value="banner">Banner (横幅广告)</option>
        <option value="affiliate">Affiliate (联盟营销)</option>
        <option value="referral">Referral (推荐)</option>
        <option value="display">Display (展示广告)</option>
        <option value="organic">Organic (自然流量)</option>
      </select>
    </div>
    <div class="form-group">
      <label>广告系列 (utm_campaign) <span class="req">*</span></label>
      <input type="text" id="utm-campaign" placeholder="例如: summer-sale-2025, product-launch" value="">
    </div>
    <div class="form-row">
      <div class="form-group">
        <label>广告内容 (utm_content)</label>
        <input type="text" id="utm-content" placeholder="例如: cta-button, hero-banner" value="">
      </div>
      <div class="form-group">
        <label>关键词 (utm_term)</label>
        <input type="text" id="utm-term" placeholder="例如: buy+shoes, free+tools" value="">
      </div>
    </div>
    <div class="btn-row">
      <button class="btn-primary" onclick="buildUTM()">🔨 生成UTM链接</button>
      <button class="btn-outline" onclick="copyUTM()">📋 复制链接</button>
      <button class="btn-outline" onclick="clearForm()" style="border-color:var(--border);color:var(--text-secondary)">🗑️ 清空</button>
    </div>
  </div>
  <div class="card">
    <h3 style="margin-bottom:8px;font-size:.95rem;color:var(--text-secondary)">生成的UTM链接</h3>
    <div class="output-box" id="output">请填写URL和必填参数...</div>
    <div class="param-list" id="param-list" style="display:none">
      <h4 style="font-size:.85rem;color:var(--text-secondary);margin-top:8px">参数明细</h4>
    </div>
  </div>
</main>
<footer>© 2025 Free ToolBase · 免费在线工具</footer>
<script>
function buildUTM(){
  const base=document.getElementById('base-url').value.trim();
  const source=document.getElementById('utm-source').value.trim();
  const medium=document.getElementById('utm-medium').value;
  const campaign=document.getElementById('utm-campaign').value.trim();
  const content=document.getElementById('utm-content').value.trim();
  const term=document.getElementById('utm-term').value.trim();
  const output=document.getElementById('output');
  const paramList=document.getElementById('param-list');
  if(!base||!source||!medium||!campaign){
    output.textContent='❌ 请填写URL、来源、媒介和广告系列名称';
    paramList.style.display='none';return;
  }
  try{new URL(base)}catch(e){output.textContent='❌ 请输入有效的URL（以http://或https://开头）';paramList.style.display='none';return}
  const params=new URLSearchParams();
  params.set('utm_source',source);params.set('utm_medium',medium);params.set('utm_campaign',campaign);
  if(content)params.set('utm_content',content);
  if(term)params.set('utm_term',term);
  const sep=base.includes('?')?'&':'?';
  const finalURL=base+sep+params.toString();
  output.textContent=finalURL;
  paramList.style.display='block';
  paramList.innerHTML='<h4 style="font-size:.85rem;color:var(--text-secondary);margin:8px 0">参数明细</h4>'+Array.from(params.entries()).map(([k,v])=>`<div class="param-item"><span>${k}</span><code>${v}</code></div>`).join('');
}
function copyUTM(){
  const t=document.getElementById('output').textContent;
  if(!t||t.startsWith('❌')||t.startsWith('请'))return;
  navigator.clipboard.writeText(t).then(()=>showToast('✅ 已复制')).catch(()=>showToast('❌ 复制失败'));
}
function clearForm(){
  document.querySelectorAll('input').forEach(i=>i.value='');
  document.getElementById('utm-medium').value='';
  document.getElementById('output').textContent='请填写URL和必填参数...';
  document.getElementById('param-list').style.display='none';
}
function showToast(msg){const t=document.createElement('div');t.style.cssText='position:fixed;bottom:20px;right:20px;background:#333;color:#fff;padding:12px 20px;border-radius:8px;z-index:9999;font-size:.9rem';
  t.textContent=msg;document.body.appendChild(t);setTimeout(()=>{t.style.opacity='0';t.style.transition='opacity .3s';setTimeout(()=>t.remove(),300)},2000)}
</script>
</body>
</html>
"""

UTM_EN = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>UTM Builder - Online URL Tracking Link Generator | Free ToolBase</title>
  <meta name="description" content="Free online UTM parameter builder. Visually generate URLs with UTM tracking parameters for Google Analytics, campaign tracking. One-click copy.">
  <meta property="og:title" content="UTM Builder - Online URL Tracking Link Generator | Free ToolBase">
  <meta property="og:description" content="Free online UTM parameter builder. Visually generate URLs with UTM tracking parameters for Google Analytics, campaign tracking.">
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://free-toolbase.com/en/utm-builder/">
  <script type="application/ld+json">{"@context":"https://schema.org","@type":"SoftwareApplication","name":"UTM Builder","applicationCategory":"BusinessApplication","operatingSystem":"Web Browser","description":"Free online UTM parameter builder. Visually generate URLs with UTM tracking parameters.","url":"https://free-toolbase.com/en/utm-builder/"}</script>
  <style>
    :root{--primary:#4F46E5;--primary-hover:#4338CA;--bg:#f8fafc;--surface:#fff;--text:#1e293b;--text-secondary:#64748b;--border:#e2e8f0;--radius:12px}
    *{margin:0;padding:0;box-sizing:border-box}
    body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;background:var(--bg);color:var(--text);min-height:100vh;display:flex;flex-direction:column}
    header{background:var(--surface);border-bottom:1px solid var(--border);padding:16px 24px;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px}
    header h1{font-size:1.25rem;font-weight:700}
    header a{color:var(--primary);text-decoration:none;font-size:.9rem}
    main{flex:1;padding:24px;max-width:800px;margin:0 auto;width:100%}
    .card{background:var(--surface);border-radius:var(--radius);padding:24px;box-shadow:0 1px 3px rgba(0,0,0,.08);margin-bottom:16px}
    .form-group{margin-bottom:14px}
    .form-group label{display:block;font-size:.85rem;font-weight:600;margin-bottom:4px;color:var(--text-secondary)}
    .form-group label .req{color:#ef4444}
    .form-group input,.form-group select{width:100%;padding:10px 12px;border:1px solid var(--border);border-radius:8px;font-size:.9rem;font-family:inherit}
    .form-group input:focus,.form-group select:focus{outline:none;border-color:var(--primary);box-shadow:0 0 0 3px rgba(79,70,229,.1)}
    .form-row{display:grid;grid-template-columns:1fr 1fr;gap:12px}
    .btn-row{display:flex;gap:8px;flex-wrap:wrap;margin-top:16px}
    button{padding:10px 20px;border:none;border-radius:8px;cursor:pointer;font-size:.9rem;font-weight:600;transition:all .2s}
    .btn-primary{background:var(--primary);color:#fff}.btn-primary:hover{background:var(--primary-hover)}
    .btn-outline{background:var(--surface);color:var(--primary);border:1px solid var(--primary)}.btn-outline:hover{background:rgba(79,70,229,.05)}
    .output-box{background:#f1f5f9;border-radius:8px;padding:16px;font-family:monospace;font-size:.9rem;word-break:break-all;line-height:1.6}
    .param-list{margin-top:12px}
    .param-item{display:flex;justify-content:space-between;align-items:center;padding:6px 0;border-bottom:1px solid var(--border);font-size:.85rem}
    .param-item code{background:#f1f5f9;padding:2px 6px;border-radius:4px;font-size:.8rem}
    footer{background:var(--surface);border-top:1px solid var(--border);padding:16px 24px;text-align:center;font-size:.8rem;color:var(--text-secondary)}
    @media(max-width:600px){main{padding:12px}.card{padding:16px}.form-row{grid-template-columns:1fr}}
  </style>
</head>
<body>
<header>
  <h1>🔗 UTM Builder</h1>
  <a href="/en/">← Back to Home</a>
</header>
<main>
  <div class="card">
    <div class="form-group">
      <label>Website URL <span class="req">*</span></label>
      <input type="url" id="base-url" placeholder="https://example.com/landing-page" value="">
    </div>
    <div class="form-group">
      <label>Traffic Source (utm_source) <span class="req">*</span></label>
      <input type="text" id="utm-source" placeholder="e.g. google, newsletter, facebook" value="">
    </div>
    <div class="form-group">
      <label>Medium (utm_medium) <span class="req">*</span></label>
      <select id="utm-medium">
        <option value="">-- Select Medium --</option>
        <option value="cpc">CPC (Paid Click)</option>
        <option value="social">Social</option>
        <option value="email">Email</option>
        <option value="banner">Banner</option>
        <option value="affiliate">Affiliate</option>
        <option value="referral">Referral</option>
        <option value="display">Display</option>
        <option value="organic">Organic</option>
      </select>
    </div>
    <div class="form-group">
      <label>Campaign (utm_campaign) <span class="req">*</span></label>
      <input type="text" id="utm-campaign" placeholder="e.g. summer-sale-2025, product-launch" value="">
    </div>
    <div class="form-row">
      <div class="form-group">
        <label>Content (utm_content)</label>
        <input type="text" id="utm-content" placeholder="e.g. cta-button, hero-banner" value="">
      </div>
      <div class="form-group">
        <label>Keyword (utm_term)</label>
        <input type="text" id="utm-term" placeholder="e.g. buy+shoes, free+tools" value="">
      </div>
    </div>
    <div class="btn-row">
      <button class="btn-primary" onclick="buildUTM()">🔨 Generate UTM Link</button>
      <button class="btn-outline" onclick="copyUTM()">📋 Copy Link</button>
      <button class="btn-outline" onclick="clearForm()" style="border-color:var(--border);color:var(--text-secondary)">🗑️ Clear</button>
    </div>
  </div>
  <div class="card">
    <h3 style="margin-bottom:8px;font-size:.95rem;color:var(--text-secondary)">Generated UTM Link</h3>
    <div class="output-box" id="output">Fill in the URL and required parameters...</div>
    <div class="param-list" id="param-list" style="display:none">
      <h4 style="font-size:.85rem;color:var(--text-secondary);margin-top:8px">Parameter Details</h4>
    </div>
  </div>
</main>
<footer>© 2025 Free ToolBase · Free Online Tools</footer>
<script>
function buildUTM(){
  const base=document.getElementById('base-url').value.trim();
  const source=document.getElementById('utm-source').value.trim();
  const medium=document.getElementById('utm-medium').value;
  const campaign=document.getElementById('utm-campaign').value.trim();
  const content=document.getElementById('utm-content').value.trim();
  const term=document.getElementById('utm-term').value.trim();
  const output=document.getElementById('output');
  const paramList=document.getElementById('param-list');
  if(!base||!source||!medium||!campaign){
    output.textContent='❌ Please fill in URL, Source, Medium, and Campaign name';
    paramList.style.display='none';return;
  }
  try{new URL(base)}catch(e){output.textContent='❌ Please enter a valid URL (starting with http:// or https://)';paramList.style.display='none';return}
  const params=new URLSearchParams();
  params.set('utm_source',source);params.set('utm_medium',medium);params.set('utm_campaign',campaign);
  if(content)params.set('utm_content',content);
  if(term)params.set('utm_term',term);
  const sep=base.includes('?')?'&':'?';
  const finalURL=base+sep+params.toString();
  output.textContent=finalURL;
  paramList.style.display='block';
  paramList.innerHTML='<h4 style="font-size:.85rem;color:var(--text-secondary);margin:8px 0">Parameter Details</h4>'+Array.from(params.entries()).map(([k,v])=>`<div class="param-item"><span>${k}</span><code>${v}</code></div>`).join('');
}
function copyUTM(){
  const t=document.getElementById('output').textContent;
  if(!t||t.startsWith('❌')||t.startsWith('Fill'))return;
  navigator.clipboard.writeText(t).then(()=>showToast('✅ Copied')).catch(()=>showToast('❌ Copy failed'));
}
function clearForm(){
  document.querySelectorAll('input').forEach(i=>i.value='');
  document.getElementById('utm-medium').value='';
  document.getElementById('output').textContent='Fill in the URL and required parameters...';
  document.getElementById('param-list').style.display='none';
}
function showToast(msg){const t=document.createElement('div');t.style.cssText='position:fixed;bottom:20px;right:20px;background:#333;color:#fff;padding:12px 20px;border-radius:8px;z-index:9999;font-size:.9rem';
  t.textContent=msg;document.body.appendChild(t);setTimeout(()=>{t.style.opacity='0';t.style.transition='opacity .3s';setTimeout(()=>t.remove(),300)},2000)}
</script>
</body>
</html>
"""

# ============================================================
# 工具5: car-loan-calculator - 车贷计算器
# ============================================================
CAR_LOAN_CN = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>车贷计算器 - 在线汽车贷款月供计算 | Free ToolBase</title>
  <meta name="description" content="免费在线车贷计算器，计算汽车贷款月供、总利息和还款总额。支持等额本息和等额本金两种方式，可视化还款明细。">
  <meta property="og:title" content="车贷计算器 - 在线汽车贷款月供计算 | Free ToolBase">
  <meta property="og:description" content="免费在线车贷计算器，计算汽车贷款月供、总利息和还款总额。支持等额本息和等额本金两种方式。">
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://free-toolbase.com/car-loan-calculator/">
  <script type="application/ld+json">{"@context":"https://schema.org","@type":"SoftwareApplication","name":"车贷计算器","applicationCategory":"FinanceApplication","operatingSystem":"Web Browser","description":"免费在线车贷计算器，计算汽车贷款月供、总利息和还款总额。","url":"https://free-toolbase.com/car-loan-calculator/"}</script>
  <style>
    :root{--primary:#4F46E5;--primary-hover:#4338CA;--bg:#f8fafc;--surface:#fff;--text:#1e293b;--text-secondary:#64748b;--border:#e2e8f0;--radius:12px}
    *{margin:0;padding:0;box-sizing:border-box}
    body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;background:var(--bg);color:var(--text);min-height:100vh;display:flex;flex-direction:column}
    header{background:var(--surface);border-bottom:1px solid var(--border);padding:16px 24px;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px}
    header h1{font-size:1.25rem;font-weight:700}
    header a{color:var(--primary);text-decoration:none;font-size:.9rem}
    main{flex:1;padding:24px;max-width:900px;margin:0 auto;width:100%}
    .card{background:var(--surface);border-radius:var(--radius);padding:24px;box-shadow:0 1px 3px rgba(0,0,0,.08);margin-bottom:16px}
    .form-row{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:14px;margin-bottom:16px}
    .form-group label{display:block;font-size:.85rem;font-weight:600;margin-bottom:4px;color:var(--text-secondary)}
    .form-group input,.form-group select{width:100%;padding:10px 12px;border:1px solid var(--border);border-radius:8px;font-size:.9rem;font-family:inherit}
    .form-group input:focus,.form-group select:focus{outline:none;border-color:var(--primary);box-shadow:0 0 0 3px rgba(79,70,229,.1)}
    .input-with-suffix{position:relative}
    .input-with-suffix input{padding-right:40px}
    .input-with-suffix .suffix{position:absolute;right:12px;top:50%;transform:translateY(-50%);color:var(--text-secondary);font-size:.85rem}
    .btn-row{display:flex;gap:8px;flex-wrap:wrap}
    button{padding:10px 20px;border:none;border-radius:8px;cursor:pointer;font-size:.9rem;font-weight:600;transition:all .2s}
    .btn-primary{background:var(--primary);color:#fff}.btn-primary:hover{background:var(--primary-hover)}
    .btn-outline{background:var(--surface);color:var(--primary);border:1px solid var(--primary)}.btn-outline:hover{background:rgba(79,70,229,.05)}
    .results{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:12px;margin-top:16px}
    .result-item{background:linear-gradient(135deg,#f0f4ff,#e8ecff);border-radius:10px;padding:16px;text-align:center}
    .result-value{font-size:1.5rem;font-weight:700;color:var(--primary);margin-top:4px}
    .result-label{font-size:.8rem;color:var(--text-secondary)}
    .schedule-table{width:100%;border-collapse:collapse;margin-top:12px;font-size:.85rem}
    .schedule-table th{background:#f1f5f9;padding:8px 10px;text-align:right;font-weight:600;font-size:.8rem;color:var(--text-secondary)}
    .schedule-table td{padding:8px 10px;text-align:right;border-bottom:1px solid var(--border)}
    .schedule-table td:first-child{text-align:center}
    .schedule-scroll{max-height:400px;overflow-y:auto;border-radius:8px;border:1px solid var(--border)}
    footer{background:var(--surface);border-top:1px solid var(--border);padding:16px 24px;text-align:center;font-size:.8rem;color:var(--text-secondary)}
    @media(max-width:600px){main{padding:12px}.card{padding:16px}.results{grid-template-columns:1fr 1fr}}
  </style>
</head>
<body>
<header>
  <h1>🚗 车贷计算器</h1>
  <a href="/">← 返回首页</a>
</header>
<main>
  <div class="card">
    <div class="form-row">
      <div class="form-group">
        <label>车辆价格</label>
        <div class="input-with-suffix"><input type="number" id="car-price" placeholder="200000" value="200000"><span class="suffix">元</span></div>
      </div>
      <div class="form-group">
        <label>首付比例</label>
        <div class="input-with-suffix"><input type="number" id="down-payment-percent" placeholder="30" value="30" min="0" max="100"><span class="suffix">%</span></div>
      </div>
      <div class="form-group">
        <label>贷款年限</label>
        <select id="loan-years">
          <option value="1">1年 (12期)</option>
          <option value="2">2年 (24期)</option>
          <option value="3" selected>3年 (36期)</option>
          <option value="4">4年 (48期)</option>
          <option value="5">5年 (60期)</option>
        </select>
      </div>
      <div class="form-group">
        <label>年利率</label>
        <div class="input-with-suffix"><input type="number" id="annual-rate" placeholder="4.5" value="4.5" step="0.01"><span class="suffix">%</span></div>
      </div>
      <div class="form-group">
        <label>还款方式</label>
        <select id="repay-method">
          <option value="equal-installment">等额本息</option>
          <option value="equal-principal">等额本金</option>
        </select>
      </div>
    </div>
    <div class="btn-row">
      <button class="btn-primary" onclick="calculate()">💰 计算</button>
      <button class="btn-outline" onclick="clearForm()">🗑️ 重置</button>
    </div>
  </div>
  <div class="card" id="result-card" style="display:none">
    <h3 style="margin-bottom:12px;font-size:.95rem;color:var(--text-secondary)">计算结果</h3>
    <div class="results" id="results"></div>
    <div class="schedule-scroll" style="margin-top:16px">
      <table class="schedule-table" id="schedule"><thead><tr><th>期数</th><th>月供</th><th>本金</th><th>利息</th><th>剩余本金</th></tr></thead><tbody></tbody></table>
    </div>
  </div>
</main>
<footer>© 2025 Free ToolBase · 免费在线工具</footer>
<script>
function formatMoney(n){return n.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g,',')}
function calculate(){
  const price=parseFloat(document.getElementById('car-price').value)||0;
  const dpPct=parseFloat(document.getElementById('down-payment-percent').value)||0;
  const years=parseInt(document.getElementById('loan-years').value)||3;
  const annualRate=parseFloat(document.getElementById('annual-rate').value)||0;
  const method=document.getElementById('repay-method').value;
  if(price<=0||dpPct<0||dpPct>100||annualRate<0){alert('请填写有效数值');return}
  const downPayment=price*dpPct/100;
  const loanAmount=price-downPayment;
  const months=years*12;
  const monthlyRate=annualRate/100/12;
  let monthlyPayment,totalPayment,totalInterest,schedule=[];
  if(method==='equal-installment'){
    if(monthlyRate===0){monthlyPayment=loanAmount/months;totalInterest=0}
    else{monthlyPayment=loanAmount*monthlyRate*Math.pow(1+monthlyRate,months)/(Math.pow(1+monthlyRate,months)-1)}
    totalPayment=monthlyPayment*months;totalInterest=totalPayment-loanAmount;
    let remaining=loanAmount;
    for(let i=1;i<=months;i++){const interest=remaining*monthlyRate;const principal=monthlyPayment-interest;remaining-=principal;
      schedule.push({period:i,payment:monthlyPayment,principal:Math.max(0,principal),interest:Math.max(0,interest),remaining:Math.max(0,remaining)})}
  }else{
    const monthlyPrincipal=loanAmount/months;totalPayment=0;totalInterest=0;let remaining=loanAmount;
    for(let i=1;i<=months;i++){const interest=remaining*monthlyRate;const payment=monthlyPrincipal+interest;remaining-=monthlyPrincipal;
      totalPayment+=payment;totalInterest+=interest;
      schedule.push({period:i,payment,principal:monthlyPrincipal,interest,remaining:Math.max(0,remaining)})}
    monthlyPayment=schedule[0]?.payment||0;
  }
  document.getElementById('result-card').style.display='block';
  document.getElementById('results').innerHTML=`
    <div class="result-item"><div class="result-label">贷款金额</div><div class="result-value">¥${formatMoney(loanAmount)}</div></div>
    <div class="result-item"><div class="result-label">首付金额</div><div class="result-value">¥${formatMoney(downPayment)}</div></div>
    <div class="result-item"><div class="result-label">${method==='equal-installment'?'月供':'首月月供'}</div><div class="result-value">¥${formatMoney(monthlyPayment)}</div></div>
    <div class="result-item"><div class="result-label">总利息</div><div class="result-value">¥${formatMoney(totalInterest)}</div></div>
    <div class="result-item"><div class="result-label">还款总额</div><div class="result-value">¥${formatMoney(totalPayment)}</div></div>
  `;
  const tbody=document.querySelector('#schedule tbody');
  const show=schedule.length>48?schedule.slice(0,48):schedule;
  tbody.innerHTML=show.map(s=>`<tr><td>${s.period}</td><td>¥${formatMoney(s.payment)}</td><td>¥${formatMoney(s.principal)}</td><td>¥${formatMoney(s.interest)}</td><td>¥${formatMoney(s.remaining)}</td></tr>`).join('');
  if(schedule.length>48){tbody.innerHTML+='<tr><td colspan="5" style="text-align:center;color:var(--text-secondary)">... 仅显示前48期，共'+schedule.length+'期</td></tr>'}
}
function clearForm(){document.getElementById('car-price').value='200000';document.getElementById('down-payment-percent').value='30';
  document.getElementById('loan-years').value='3';document.getElementById('annual-rate').value='4.5';
  document.getElementById('repay-method').value='equal-installment';document.getElementById('result-card').style.display='none'}
calculate();
</script>
</body>
</html>
"""

CAR_LOAN_EN = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Car Loan Calculator - Online Auto Loan Payment Calculator | Free ToolBase</title>
  <meta name="description" content="Free online car loan calculator. Calculate monthly payments, total interest, and total cost for auto loans. Supports equal installment and equal principal methods.">
  <meta property="og:title" content="Car Loan Calculator - Online Auto Loan Payment Calculator | Free ToolBase">
  <meta property="og:description" content="Free online car loan calculator. Calculate monthly payments, total interest, and total cost for auto loans. Supports equal installment and equal principal methods.">
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://free-toolbase.com/en/car-loan-calculator/">
  <script type="application/ld+json">{"@context":"https://schema.org","@type":"SoftwareApplication","name":"Car Loan Calculator","applicationCategory":"FinanceApplication","operatingSystem":"Web Browser","description":"Free online car loan calculator. Calculate monthly payments, total interest, and total cost for auto loans.","url":"https://free-toolbase.com/en/car-loan-calculator/"}</script>
  <style>
    :root{--primary:#4F46E5;--primary-hover:#4338CA;--bg:#f8fafc;--surface:#fff;--text:#1e293b;--text-secondary:#64748b;--border:#e2e8f0;--radius:12px}
    *{margin:0;padding:0;box-sizing:border-box}
    body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;background:var(--bg);color:var(--text);min-height:100vh;display:flex;flex-direction:column}
    header{background:var(--surface);border-bottom:1px solid var(--border);padding:16px 24px;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px}
    header h1{font-size:1.25rem;font-weight:700}
    header a{color:var(--primary);text-decoration:none;font-size:.9rem}
    main{flex:1;padding:24px;max-width:900px;margin:0 auto;width:100%}
    .card{background:var(--surface);border-radius:var(--radius);padding:24px;box-shadow:0 1px 3px rgba(0,0,0,.08);margin-bottom:16px}
    .form-row{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:14px;margin-bottom:16px}
    .form-group label{display:block;font-size:.85rem;font-weight:600;margin-bottom:4px;color:var(--text-secondary)}
    .form-group input,.form-group select{width:100%;padding:10px 12px;border:1px solid var(--border);border-radius:8px;font-size:.9rem;font-family:inherit}
    .form-group input:focus,.form-group select:focus{outline:none;border-color:var(--primary);box-shadow:0 0 0 3px rgba(79,70,229,.1)}
    .input-with-suffix{position:relative}
    .input-with-suffix input{padding-right:40px}
    .input-with-suffix .suffix{position:absolute;right:12px;top:50%;transform:translateY(-50%);color:var(--text-secondary);font-size:.85rem}
    .btn-row{display:flex;gap:8px;flex-wrap:wrap}
    button{padding:10px 20px;border:none;border-radius:8px;cursor:pointer;font-size:.9rem;font-weight:600;transition:all .2s}
    .btn-primary{background:var(--primary);color:#fff}.btn-primary:hover{background:var(--primary-hover)}
    .btn-outline{background:var(--surface);color:var(--primary);border:1px solid var(--primary)}.btn-outline:hover{background:rgba(79,70,229,.05)}
    .results{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:12px;margin-top:16px}
    .result-item{background:linear-gradient(135deg,#f0f4ff,#e8ecff);border-radius:10px;padding:16px;text-align:center}
    .result-value{font-size:1.5rem;font-weight:700;color:var(--primary);margin-top:4px}
    .result-label{font-size:.8rem;color:var(--text-secondary)}
    .schedule-table{width:100%;border-collapse:collapse;margin-top:12px;font-size:.85rem}
    .schedule-table th{background:#f1f5f9;padding:8px 10px;text-align:right;font-weight:600;font-size:.8rem;color:var(--text-secondary)}
    .schedule-table td{padding:8px 10px;text-align:right;border-bottom:1px solid var(--border)}
    .schedule-table td:first-child{text-align:center}
    .schedule-scroll{max-height:400px;overflow-y:auto;border-radius:8px;border:1px solid var(--border)}
    footer{background:var(--surface);border-top:1px solid var(--border);padding:16px 24px;text-align:center;font-size:.8rem;color:var(--text-secondary)}
    @media(max-width:600px){main{padding:12px}.card{padding:16px}.results{grid-template-columns:1fr 1fr}}
  </style>
</head>
<body>
<header>
  <h1>🚗 Car Loan Calculator</h1>
  <a href="/en/">← Back to Home</a>
</header>
<main>
  <div class="card">
    <div class="form-row">
      <div class="form-group">
        <label>Car Price</label>
        <div class="input-with-suffix"><input type="number" id="car-price" placeholder="30000" value="30000"><span class="suffix">$</span></div>
      </div>
      <div class="form-group">
        <label>Down Payment</label>
        <div class="input-with-suffix"><input type="number" id="down-payment-percent" placeholder="20" value="20" min="0" max="100"><span class="suffix">%</span></div>
      </div>
      <div class="form-group">
        <label>Loan Term</label>
        <select id="loan-years">
          <option value="1">1 Year (12 mo)</option>
          <option value="2">2 Years (24 mo)</option>
          <option value="3" selected>3 Years (36 mo)</option>
          <option value="4">4 Years (48 mo)</option>
          <option value="5">5 Years (60 mo)</option>
        </select>
      </div>
      <div class="form-group">
        <label>Annual Interest Rate</label>
        <div class="input-with-suffix"><input type="number" id="annual-rate" placeholder="5.5" value="5.5" step="0.01"><span class="suffix">%</span></div>
      </div>
      <div class="form-group">
        <label>Repayment Method</label>
        <select id="repay-method">
          <option value="equal-installment">Equal Installment</option>
          <option value="equal-principal">Equal Principal</option>
        </select>
      </div>
    </div>
    <div class="btn-row">
      <button class="btn-primary" onclick="calculate()">💰 Calculate</button>
      <button class="btn-outline" onclick="clearForm()">🗑️ Reset</button>
    </div>
  </div>
  <div class="card" id="result-card" style="display:none">
    <h3 style="margin-bottom:12px;font-size:.95rem;color:var(--text-secondary)">Results</h3>
    <div class="results" id="results"></div>
    <div class="schedule-scroll" style="margin-top:16px">
      <table class="schedule-table" id="schedule"><thead><tr><th>Period</th><th>Payment</th><th>Principal</th><th>Interest</th><th>Balance</th></tr></thead><tbody></tbody></table>
    </div>
  </div>
</main>
<footer>© 2025 Free ToolBase · Free Online Tools</footer>
<script>
function formatMoney(n){return n.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g,',')}
function calculate(){
  const price=parseFloat(document.getElementById('car-price').value)||0;
  const dpPct=parseFloat(document.getElementById('down-payment-percent').value)||0;
  const years=parseInt(document.getElementById('loan-years').value)||3;
  const annualRate=parseFloat(document.getElementById('annual-rate').value)||0;
  const method=document.getElementById('repay-method').value;
  if(price<=0||dpPct<0||dpPct>100||annualRate<0){alert('Please enter valid values');return}
  const downPayment=price*dpPct/100;
  const loanAmount=price-downPayment;
  const months=years*12;
  const monthlyRate=annualRate/100/12;
  let monthlyPayment,totalPayment,totalInterest,schedule=[];
  if(method==='equal-installment'){
    if(monthlyRate===0){monthlyPayment=loanAmount/months;totalInterest=0}
    else{monthlyPayment=loanAmount*monthlyRate*Math.pow(1+monthlyRate,months)/(Math.pow(1+monthlyRate,months)-1)}
    totalPayment=monthlyPayment*months;totalInterest=totalPayment-loanAmount;
    let remaining=loanAmount;
    for(let i=1;i<=months;i++){const interest=remaining*monthlyRate;const principal=monthlyPayment-interest;remaining-=principal;
      schedule.push({period:i,payment:monthlyPayment,principal:Math.max(0,principal),interest:Math.max(0,interest),remaining:Math.max(0,remaining)})}
  }else{
    const monthlyPrincipal=loanAmount/months;totalPayment=0;totalInterest=0;let remaining=loanAmount;
    for(let i=1;i<=months;i++){const interest=remaining*monthlyRate;const payment=monthlyPrincipal+interest;remaining-=monthlyPrincipal;
      totalPayment+=payment;totalInterest+=interest;
      schedule.push({period:i,payment,principal:monthlyPrincipal,interest,remaining:Math.max(0,remaining)})}
    monthlyPayment=schedule[0]?.payment||0;
  }
  document.getElementById('result-card').style.display='block';
  document.getElementById('results').innerHTML=`
    <div class="result-item"><div class="result-label">Loan Amount</div><div class="result-value">$${formatMoney(loanAmount)}</div></div>
    <div class="result-item"><div class="result-label">Down Payment</div><div class="result-value">$${formatMoney(downPayment)}</div></div>
    <div class="result-item"><div class="result-label">${method==='equal-installment'?'Monthly Payment':'First Payment'}</div><div class="result-value">$${formatMoney(monthlyPayment)}</div></div>
    <div class="result-item"><div class="result-label">Total Interest</div><div class="result-value">$${formatMoney(totalInterest)}</div></div>
    <div class="result-item"><div class="result-label">Total Payment</div><div class="result-value">$${formatMoney(totalPayment)}</div></div>
  `;
  const tbody=document.querySelector('#schedule tbody');
  const show=schedule.length>48?schedule.slice(0,48):schedule;
  tbody.innerHTML=show.map(s=>`<tr><td>${s.period}</td><td>$${formatMoney(s.payment)}</td><td>$${formatMoney(s.principal)}</td><td>$${formatMoney(s.interest)}</td><td>$${formatMoney(s.remaining)}</td></tr>`).join('');
  if(schedule.length>48){tbody.innerHTML+='<tr><td colspan="5" style="text-align:center;color:var(--text-secondary)">... Showing first 48 of '+schedule.length+' periods</td></tr>'}
}
function clearForm(){document.getElementById('car-price').value='30000';document.getElementById('down-payment-percent').value='20';
  document.getElementById('loan-years').value='3';document.getElementById('annual-rate').value='5.5';
  document.getElementById('repay-method').value='equal-installment';document.getElementById('result-card').style.display='none'}
calculate();
</script>
</body>
</html>
"""

# ============================================================
# 写入文件
# ============================================================
files = {
    "diagram-generator/index.html": DIAGRAM_CN,
    "en/diagram-generator/index.html": DIAGRAM_EN,
    "emojify/index.html": EMOJIFY_CN,
    "en/emojify/index.html": EMOJIFY_EN,
    "font-generator/index.html": FONT_CN,
    "en/font-generator/index.html": FONT_EN,
    "utm-builder/index.html": UTM_CN,
    "en/utm-builder/index.html": UTM_EN,
    "car-loan-calculator/index.html": CAR_LOAN_CN,
    "en/car-loan-calculator/index.html": CAR_LOAN_EN,
}

for path, content in files.items():
    full_path = os.path.join(BASE, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ {path}")

print(f"\n总计: {len(files)} 个文件")