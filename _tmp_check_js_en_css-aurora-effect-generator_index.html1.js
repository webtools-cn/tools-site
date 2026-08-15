
const presets = {
  classic: {c1:'#06b6d4',c2:'#8b5cf6',c3:'#22c55e',blur:80,opacity:50,speed:8,size:50,bg:'#0a0a1a'},
  sunset: {c1:'#f97316',c2:'#ec4899',c3:'#8b5cf6',blur:90,opacity:55,speed:10,size:55,bg:'#1a0a0a'},
  ocean: {c1:'#0ea5e9',c2:'#06b6d4',c3:'#14b8a6',blur:85,opacity:45,speed:12,size:60,bg:'#0a0f1a'},
  neon: {c1:'#d946ef',c2:'#8b5cf6',c3:'#6366f1',blur:75,opacity:60,speed:6,size:45,bg:'#0a0a1a'},
  forest: {c1:'#22c55e',c2:'#10b981',c3:'#84cc16',blur:95,opacity:40,speed:14,size:55,bg:'#0a1a0a'}
};

function applyPreset(name) {
  const p = presets[name];
  document.getElementById('color1').value = p.c1;
  document.getElementById('color2').value = p.c2;
  document.getElementById('color3').value = p.c3;
  document.getElementById('blur').value = p.blur;
  document.getElementById('opacity').value = p.opacity;
  document.getElementById('speed').value = p.speed;
  document.getElementById('size').value = p.size;
  document.getElementById('bg-color').value = p.bg;
  updatePreview();
}

function hexToRgba(hex, a) {
  const r = parseInt(hex.slice(1,3),16);
  const g = parseInt(hex.slice(3,5),16);
  const b = parseInt(hex.slice(5,7),16);
  return `rgba(${r},${g},${b},${a})`;
}

function updatePreview() {
  const c1 = document.getElementById('color1').value;
  const c2 = document.getElementById('color2').value;
  const c3 = document.getElementById('color3').value;
  const blur = document.getElementById('blur').value;
  const opacity = document.getElementById('opacity').value;
  const speed = document.getElementById('speed').value;
  const size = document.getElementById('size').value;
  const bgColor = document.getElementById('bg-color').value;

  document.getElementById('blur-val').textContent = blur + 'px';
  document.getElementById('opacity-val').textContent = opacity + '%';
  document.getElementById('speed-val').textContent = speed + 's';
  document.getElementById('size-val').textContent = size + '%';

  const preview = document.getElementById('aurora-preview');
  preview.style.background = bgColor;

  const al1 = document.getElementById('al1');
  const al2 = document.getElementById('al2');
  const al3 = document.getElementById('al3');

  al1.style.width = size + '%';
  al1.style.height = (parseInt(size) + 10) + '%';
  al1.style.background = `radial-gradient(circle,${hexToRgba(c1,0.8)},transparent)`;
  al1.style.filter = `blur(${blur}px)`;
  al1.style.opacity = opacity / 100;

  al2.style.width = (parseInt(size) - 10) + '%';
  al2.style.height = parseInt(size) + '%';
  al2.style.background = `radial-gradient(circle,${hexToRgba(c2,0.7)},transparent)`;
  al2.style.filter = `blur(${blur}px)`;
  al2.style.opacity = opacity / 100;

  al3.style.width = (parseInt(size) - 5) + '%';
  al3.style.height = (parseInt(size) + 5) + '%';
  al3.style.background = `radial-gradient(circle,${hexToRgba(c3,0.6)},transparent)`;
  al3.style.filter = `blur(${blur}px)`;
  al3.style.opacity = opacity / 100;

  // Update animation speed
  const dur = speed + 's';
  al1.style.animation = `aurora1 ${dur} ease-in-out infinite`;
  al2.style.animation = `aurora2 ${dur} ease-in-out infinite`;
  al3.style.animation = `aurora3 ${dur} ease-in-out infinite`;

  generateCSS(c1, c2, c3, blur, opacity, speed, size, bgColor);
}

function generateCSS(c1, c2, c3, blur, opacity, speed, size, bgColor) {
  const css = `.aurora-container {
  position: relative;
  width: 100%;
  height: 400px;
  background: ${bgColor};
  overflow: hidden;
  border-radius: 12px;
}

.aurora-layer {
  position: absolute;
  border-radius: 50%;
  filter: blur(${blur}px);
  opacity: ${opacity / 100};
  will-change: transform;
}

.aurora-1 {
  width: ${size}%;
  height: ${parseInt(size) + 10}%;
  top: 10%;
  left: 10%;
  background: radial-gradient(circle, ${hexToRgba(c1, 0.8)}, transparent);
  animation: aurora1 ${speed}s ease-in-out infinite;
}

.aurora-2 {
  width: ${parseInt(size) - 10}%;
  height: ${size}%;
  top: 20%;
  left: 40%;
  background: radial-gradient(circle, ${hexToRgba(c2, 0.7)}, transparent);
  animation: aurora2 ${speed}s ease-in-out infinite;
}

.aurora-3 {
  width: ${parseInt(size) - 5}%;
  height: ${parseInt(size) + 5}%;
  top: 30%;
  left: 55%;
  background: radial-gradient(circle, ${hexToRgba(c3, 0.6)}, transparent);
  animation: aurora3 ${speed}s ease-in-out infinite;
}

@keyframes aurora1 {
  0%, 100% { transform: translate(0, 0) scale(1); }
  33% { transform: translate(30px, -20px) scale(1.1); }
  66% { transform: translate(-20px, 15px) scale(0.9); }
}

@keyframes aurora2 {
  0%, 100% { transform: translate(0, 0) scale(1); }
  33% { transform: translate(-25px, 20px) scale(0.9); }
  66% { transform: translate(20px, -15px) scale(1.1); }
}

@keyframes aurora3 {
  0%, 100% { transform: translate(0, 0) scale(1); }
  33% { transform: translate(15px, 25px) scale(1.1); }
  66% { transform: translate(-30px, -10px) scale(0.95); }
}`;
  document.getElementById('css-output').textContent = css;
}

function copyCSS() {
  const css = document.getElementById('css-output').textContent;
  if (!css) { showToast('Please generate firstCSS'); return; }
  navigator.clipboard.writeText(css).then(() => showToast('✅ Copied to clipboard'));
}

function resetParams() {
  applyPreset('classic');
}

function toggleFeedback(){const p=document.getElementById('feedback-panel');p.style.display=p.style.display==='none'?'block':'none';}
function showToast(msg){const t=document.getElementById('toast')||(()=>{const d=document.createElement('div');d.id='toast';d.className='toast';document.body.appendChild(d);return d;})();t.textContent=msg;t.classList.add('show');setTimeout(()=>t.classList.remove('show'),2000);}

// Add animation keyframes dynamically
const style = document.createElement('style');
style.textContent = `
@keyframes aurora1{0%,100%{transform:translate(0,0) scale(1)}33%{transform:translate(30px,-20px) scale(1.1)}66%{transform:translate(-20px,15px) scale(0.9)}}
@keyframes aurora2{0%,100%{transform:translate(0,0) scale(1)}33%{transform:translate(-25px,20px) scale(0.9)}66%{transform:translate(20px,-15px) scale(1.1)}}
@keyframes aurora3{0%,100%{transform:translate(0,0) scale(1)}33%{transform:translate(15px,25px) scale(1.1)}66%{transform:translate(-30px,-10px) scale(0.95)}}
.toast{position:fixed;bottom:80px;left:50%;transform:translateX(-50%);background:#1e293b;color:#e2e8f0;padding:10px 20px;border-radius:8px;border:1px solid rgba(6,182,212,.3);z-index:9999;opacity:0;transition:opacity .3s;pointer-events:none;font-size:.9rem}
.toast.show{opacity:1}`;
document.head.appendChild(style);

window.addEventListener('load', updatePreview);
document.addEventListener('keydown', function(e) {
  if (e.ctrlKey && e.key === 'Enter') { copyCSS(); e.preventDefault(); }
});
