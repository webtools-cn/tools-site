

function update(){
  var blur=document.getElementById('blur').value;
  var brightness=document.getElementById('brightness').value;
  var contrast=document.getElementById('contrast').value;
  var saturate=document.getElementById('saturate').value;
  var grayscale=document.getElementById('grayscale').value;
  var sepia=document.getElementById('sepia').value;
  var hueRotate=document.getElementById('hueRotate').value;
  var gc=document.getElementById('glassColor').value;
  var op=document.getElementById('glassOpacity').value;
  
  document.getElementById('blurVal').textContent=blur+'px';
  document.getElementById('brightnessVal').textContent=brightness+'%';
  document.getElementById('contrastVal').textContent=contrast+'%';
  document.getElementById('saturateVal').textContent=saturate+'%';
  document.getElementById('grayscaleVal').textContent=grayscale+'%';
  document.getElementById('sepiaVal').textContent=sepia+'%';
  document.getElementById('hueRotateVal').textContent=hueRotate+'deg';
  document.getElementById('glassOpacityVal').textContent=(op/100).toFixed(2);
  
  var filters='blur('+blur+'px) brightness('+brightness+'%) contrast('+contrast+'%) saturate('+saturate+'%) grayscale('+grayscale+'%) sepia('+sepia+'%) hue-rotate('+hueRotate+'deg)';
  var p=document.getElementById('glassPreview');
  p.style.backdropFilter=filters;
  p.style.background='rgba('+hexToRgb(gc)+','+(op/100)+')';
  
  document.getElementById('codeBox1').textContent='.glass-element {\n  backdrop-filter: '+filters+';\n  background: rgba('+hexToRgb(gc)+', '+(op/100)+');\n  border: 1px solid rgba(255,255,255,0.2);\n  border-radius: 12px;\n}';
}
function hexToRgb(h){var r=0,g=0,b=0;if(h.length==7){r=parseInt(h[1]+h[2],16);g=parseInt(h[3]+h[4],16);b=parseInt(h[5]+h[6],16)}return r+','+g+','+b}
function copyCode(){navigator.clipboard.writeText(document.getElementById('codeBox1').textContent).then(function(){showToast('CSS code copied ✅')}).catch(function(){showToast('Copy failed')})}
update();

