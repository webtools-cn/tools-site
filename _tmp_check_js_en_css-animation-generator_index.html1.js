
var currentPreset='bounce';
var keyframesMap={
bounce:'@keyframes bounce {\n  0%, 20%, 50%, 80%, 100% {transform: translateY(0);}\n  40% {transform: translateY(-30px);}\n  60% {transform: translateY(-15px);}\n}',
fadeIn:'@keyframes fadeIn {\n  from {opacity: 0;}\n  to {opacity: 1;}\n}',
fadeOut:'@keyframes fadeOut {\n  from {opacity: 1;}\n  to {opacity: 0;}\n}',
rotate:'@keyframes rotate {\n  from {transform: rotate(0deg);}\n  to {transform: rotate(360deg);}\n}',
scale:'@keyframes scale {\n  0% {transform: scale(1);}\n  50% {transform: scale(1.3);}\n  100% {transform: scale(1);}\n}',
slideLeft:'@keyframes slideLeft {\n  from {transform: translateX(100%);opacity:0;}\n  to {transform: translateX(0);opacity:1;}\n}',
slideRight:'@keyframes slideRight {\n  from {transform: translateX(-100%);opacity:0;}\n  to {transform: translateX(0);opacity:1;}\n}',
slideUp:'@keyframes slideUp {\n  from {transform: translateY(100%);opacity:0;}\n  to {transform: translateY(0);opacity:1;}\n}',
shake:'@keyframes shake {\n  0%, 100% {transform: translateX(0);}\n  10%, 30%, 50%, 70%, 90% {transform: translateX(-5px);}\n  20%, 40%, 60%, 80% {transform: translateX(5px);}\n}',
pulse:'@keyframes pulse {\n  0% {transform: scale(1);opacity:1;}\n  50% {transform: scale(1.1);opacity:0.8;}\n  100% {transform: scale(1);opacity:1;}\n}',
swing:'@keyframes swing {\n  20% {transform: rotate(15deg);}\n  40% {transform: rotate(-10deg);}\n  60% {transform: rotate(5deg);}\n  80% {transform: rotate(-5deg);}\n  100% {transform: rotate(0deg);}\n}',
flip:'@keyframes flip {\n  0% {transform: perspective(400px) rotateY(0);}\n  100% {transform: perspective(400px) rotateY(360deg);}\n}'
};
function selectPreset(name,el){currentPreset=name;document.querySelectorAll('.preset-btn').forEach(function(b){b.classList.remove('active');});if(el)el.classList.add('active');updatePreview();}
function updatePreview(){
  var dur=document.getElementById('duration').value;
  var ease=document.getElementById('easing').value;
  var iter=document.getElementById('iteration').value;
  var delay=document.getElementById('delay').value;
  var dir=document.getElementById('direction').value;
  var el=document.getElementById('previewEl');
  el.style.animation='none';el.offsetHeight;
  el.style.animation=currentPreset+' '+dur+'s '+ease+' '+delay+'s '+iter+' '+dir;
  var kf=keyframesMap[currentPreset];
  var code=kf+'\n\n.animated-element {\n  animation: '+currentPreset+' '+dur+'s '+ease+' '+delay+'s '+iter+' '+dir+';\n}';
  document.getElementById('codeOutput').textContent=code;
}
function copyCode(){navigator.clipboard.writeText(document.getElementById('codeOutput').textContent);showToast('CSS code copied to clipboard');}
function showToast(msg){var t=document.getElementById('toast');t.textContent=msg;t.classList.add('show');setTimeout(function(){t.classList.remove('show');},2000);}
document.addEventListener('keydown',function(e){if(e.ctrlKey&&e.key==='Enter'){e.preventDefault();updatePreview();}if(e.ctrlKey&&e.shiftKey&&e.key==='C'){e.preventDefault();copyCode();}});
window.addEventListener('load',function(){updatePreview();});
