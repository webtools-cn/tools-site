
var currentTab='css';
var isOpen=false;

function updatePreview(){
  var dir=document.getElementById('direction').value;
  var width=document.getElementById('sidebar-width').value;
  var duration=document.getElementById('duration').value;
  var easing=document.getElementById('easing').value;
  var overlayOpacity=document.getElementById('overlay-opacity').value;
  var bgColor=document.getElementById('sidebar-bg').value;
  var borderColor=document.getElementById('sidebar-border').value;
  var sidebar=document.getElementById('preview-sidebar');
  var overlay=document.getElementById('preview-overlay');
  document.getElementById('width-val').textContent=width+'px';
  document.getElementById('duration-val').textContent=duration+'ms';
  document.getElementById('overlay-val').textContent=overlayOpacity+'%';
  sidebar.className='preview-sidebar from-'+dir;
  if(isOpen)sidebar.classList.add('open');
  sidebar.style.width=width+'px';
  sidebar.style.transition='transform '+duration+'ms '+easing;
  sidebar.style.background=bgColor;
  sidebar.style.borderColor=borderColor;
  if(dir==='left'){sidebar.style.borderRight='1px solid '+borderColor;sidebar.style.borderLeft='none';}
  else{sidebar.style.borderLeft='1px solid '+borderColor;sidebar.style.borderRight='none';}
  overlay.style.background='rgba(0,0,0,'+(overlayOpacity/100)+')';
  overlay.style.transition='opacity '+duration+'ms '+easing;
  updateCode();
}

function updateCode(){
  var dir=document.getElementById('direction').value;
  var width=document.getElementById('sidebar-width').value;
  var duration=document.getElementById('duration').value;
  var easing=document.getElementById('easing').value;
  var overlayOpacity=document.getElementById('overlay-opacity').value;
  var bgColor=document.getElementById('sidebar-bg').value;
  var borderColor=document.getElementById('sidebar-border').value;
  var out=document.getElementById('code-output');
  var hideTransform=dir==='left'?'translateX(-100%)':'translateX(100%)';
  if(currentTab==='css'){
    var css='.sidebar {\n  position: fixed;\n  top: 0;\n  bottom: 0;\n  width: '+width+'px;\n  background: '+bgColor+';\n  border-'+(dir==='left'?'right':'left')+': 1px solid '+borderColor+';\n  '+(dir==='left'?'left':'right')+': 0;\n  transform: '+hideTransform+';\n  transition: transform '+duration+'ms '+easing+';\n  z-index: 1000;\n  padding: 20px;\n}\n\n.sidebar.open {\n  transform: translateX(0);\n}\n\n.sidebar-overlay {\n  position: fixed;\n  inset: 0;\n  background: rgba(0, 0, 0, '+(overlayOpacity/100)+');\n  opacity: 0;\n  pointer-events: none;\n  transition: opacity '+duration+'ms '+easing+';\n  z-index: 999;\n}\n\n.sidebar-overlay.show {\n  opacity: 1;\n  pointer-events: auto;\n}';
    out.textContent=css;
  } else if(currentTab==='html'){
    out.textContent='<button class="menu-btn" onclick="toggleSidebar()">☰</button>\n\n<div class="sidebar-overlay" id="sidebar-overlay" onclick="closeSidebar()"></div>\n\n<nav class="sidebar" id="sidebar">\n  <div class="sidebar-header">\n    <h3>Menu</h3>\n    <button onclick="closeSidebar()">✕</button>\n  </div>\n  <ul class="sidebar-menu">\n    <li>Home</li>\n    <li>Dashboard</li>\n    <li>Settings</li>\n    <li>Profile</li>\n  </ul>\n</nav>';
  } else {
    out.textContent='function openSidebar() {\n  document.getElementById(\'sidebar\').classList.add(\'open\');\n  document.getElementById(\'sidebar-overlay\').classList.add(\'show\');\n}\n\nfunction closeSidebar() {\n  document.getElementById(\'sidebar\').classList.remove(\'open\');\n  document.getElementById(\'sidebar-overlay\').classList.remove(\'show\');\n}\n\nfunction toggleSidebar() {\n  const sidebar = document.getElementById(\'sidebar\');\n  if (sidebar.classList.contains(\'open\')) {\n    closeSidebar();\n  } else {\n    openSidebar();\n  }\n}';
  }
}

function switchTab(tab){currentTab=tab;document.querySelectorAll('.tab-btn').forEach(function(b){b.classList.remove('active');});event.target.classList.add('active');updateCode();}
function copyCode(){var code=document.getElementById('code-output').textContent;if(!code){showToast('Generate code first');return;}navigator.clipboard.writeText(code).then(function(){showToast('✅ Copied to clipboard');});}
function resetParams(){document.getElementById('direction').value='left';document.getElementById('sidebar-width').value=280;document.getElementById('duration').value=300;document.getElementById('easing').value='ease';document.getElementById('overlay-opacity').value=50;document.getElementById('sidebar-bg').value='#0f172a';document.getElementById('sidebar-border').value='#1e293b';closeSidebar();updatePreview();}
function toggleFeedback(){var p=document.getElementById('feedback-panel');p.style.display=p.style.display==='none'?'block':'none';}
function showToast(msg){var t=document.getElementById('toast');t.textContent=msg;t.style.opacity='1';setTimeout(function(){t.style.opacity='0';},2000);}

window.addEventListener('load',function(){updatePreview();});
document.addEventListener('keydown',function(e){
  if(e.ctrlKey&&e.key==='Enter'){copyCode();e.preventDefault();}
  if(e.ctrlKey&&e.shiftKey&&e.key==='C'){copyCode();e.preventDefault();}
  if(e.key==='Escape')closeSidebar();
});
