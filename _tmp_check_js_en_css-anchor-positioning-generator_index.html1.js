
function showToast(m){var t=document.getElementById("toast");t.textContent=m;t.classList.add("show");setTimeout(function(){t.classList.remove("show")},3000)}
function copyText(id){var el=document.getElementById(id);if(!el)return;var t=el.textContent||el.innerText;navigator.clipboard.writeText(t).then(function(){showToast("Copy")})["catch"](function(){showToast("CopyFailed")})}

let anchorPos = {x: 200, y: 120};
let isDragging = false;
let dragOffset = {x: 0, y: 0};

const anchorEl = document.getElementById('anchor');
const targetEl = document.getElementById('target');

anchorEl.addEventListener('mousedown', function(e) {
  isDragging = true;
  const rect = anchorEl.getBoundingClientRect();
  const previewRect = document.getElementById('preview').getBoundingClientRect();
  dragOffset.x = e.clientX - rect.left;
  dragOffset.y = e.clientY - rect.top;
  e.preventDefault();
});

document.addEventListener('mousemove', function(e) {
  if (!isDragging) return;
  const previewRect = document.getElementById('preview').getBoundingClientRect();
  anchorPos.x = e.clientX - previewRect.left - dragOffset.x;
  anchorPos.y = e.clientY - previewRect.top - dragOffset.y;
  anchorPos.x = Math.max(0, Math.min(anchorPos.x, previewRect.width - 120));
  anchorPos.y = Math.max(0, Math.min(anchorPos.y, previewRect.height - 50));
  anchorEl.style.left = anchorPos.x + 'px';
  anchorEl.style.top = anchorPos.y + 'px';
  updatePreview();
});

document.addEventListener('mouseup', function() { isDragging = false; });

function updatePreview() {
  const area = document.getElementById('position-area').value;
  const offsetX = parseInt(document.getElementById('offset-x').value) || 0;
  const offsetY = parseInt(document.getElementById('offset-y').value) || 0;
  const aW = 120, aH = 50;

  let tx, ty;
  switch(area) {
    case 'top':
      tx = anchorPos.x + aW/2 - 80;
      ty = anchorPos.y - 60 - offsetY;
      break;
    case 'bottom':
      tx = anchorPos.x + aW/2 - 80;
      ty = anchorPos.y + aH + offsetY;
      break;
    case 'left':
      tx = anchorPos.x - 170 - offsetX;
      ty = anchorPos.y + aH/2 - 25;
      break;
    case 'right':
      tx = anchorPos.x + aW + offsetX;
      ty = anchorPos.y + aH/2 - 25;
      break;
    case 'top left':
      tx = anchorPos.x - 160 - offsetX;
      ty = anchorPos.y - 60 - offsetY;
      break;
    case 'top right':
      tx = anchorPos.x + aW + offsetX;
      ty = anchorPos.y - 60 - offsetY;
      break;
    case 'bottom left':
      tx = anchorPos.x - 160 - offsetX;
      ty = anchorPos.y + aH + offsetY;
      break;
    case 'bottom right':
      tx = anchorPos.x + aW + offsetX;
      ty = anchorPos.y + aH + offsetY;
      break;
  }
  targetEl.style.left = tx + 'px';
  targetEl.style.top = ty + 'px';
}

window.updateCode = updateCode; function updateCode() {
  const anchorName = document.getElementById('anchor-name').value || '--my-anchor';
  const area = document.getElementById('position-area').value;
  const offsetX = parseInt(document.getElementById('offset-x').value) || 0;
  const offsetY = parseInt(document.getElementById('offset-y').value) || 0;
  const fallback = document.getElementById('fallback').value;
  const elType = document.getElementById('el-type').value;

  let css = `/* 锚点元素 */\n.anchor {\n  anchor-name: ${anchorName};\n}\n\n`;
  css += `/* 定位元素 */\n.${elType} {\n  position: fixed;\n  position-anchor: ${anchorName};\n  position-area: ${area};\n`;

  if (offsetX !== 0 || offsetY !== 0) {
    if (offsetY !== 0) css += `  margin-block-start: ${offsetY}px;\n`;
    if (offsetX !== 0) css += `  margin-inline-start: ${offsetX}px;\n`;
  }

  if (fallback !== 'none') {
    css += `  position-try-fallbacks: ${fallback};\n`;
  }

  css += `}`;

  const output = document.getElementById('code-output');
  output.innerHTML = `\x3Cbutton class="copy-btn" onclick="copyCode()">📋 Copy\x3C/button>${escapeHtml(css)}`;
}

function escapeHtml(text) {
  return text.replace(/&/g,'&amp;').replace(/\x3C/g,'&lt;').replace(/>/g,'&gt;');
}

function copyCode() {
  const code = document.getElementById('code-output').textContent.replace('📋 Copy','').trim();
  navigator.clipboard.writeText(code).then(() => {
    const btn = document.querySelector('.copy-btn');
    btn.textContent = '✅ Copy';
    setTimeout(() => btn.textContent = '📋 Copy', 2000);
  });
}

function toggleFeedback(){const p=document.getElementById('feedback-panel');p.style.display=p.style.display==='none'?'block':'none';}
function submitFeedback(){
const type=document.getElementById('feedback-type').value;
const typeLabel={feedback:'💡 功能建议',bug:'🐛 Bug报告',other:'💬 其他'}[type];
const title=encodeURIComponent(typeLabel+' - '+window.location.pathname);
const body=encodeURIComponent('**页面**: '+window.location.href+'\n**类型**: '+typeLabel+'\n\n'+text);
window.open('https://github.com/webtools-cn/tools-site/issues/new?title='+title+'&body='+body,'_blank');
document.getElementById('feedback-success').style.display='block';
}

updatePreview();
updateCode();
