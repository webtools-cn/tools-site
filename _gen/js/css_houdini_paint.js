function loadExample(){
document.getElementById('input').value='Hello World! This is a test text for the CSS Houdini Paint Worklet generator. It will create a custom paint effect.';
document.getElementById('paintType').value='checkerboard';
document.getElementById('color1').value='#06b6d4';
document.getElementById('color2').value='#1e293b';
document.getElementById('size').value='20';
execute();
}
function clearInput(){
document.getElementById('input').value='';
document.getElementById('paintType').value='checkerboard';
document.getElementById('output').textContent='等待生成...';
document.getElementById('preview').innerHTML='';
}
function execute(){
var type=document.getElementById('paintType').value;
var c1=document.getElementById('color1').value||'#06b6d4';
var c2=document.getElementById('color2').value||'#1e293b';
var size=document.getElementById('size').value||'20';
var code='// Paint Worklet: '+type+'\n';
code+='// Register in your main JS:\n';
code+='// CSS.paintWorklet.addModule("paint-'+type+'.js");\n\n';
code+='class '+capitalize(type)+'Painter {\n';
code+='  static get inputProperties() {\n';
code+='    return [];\n';
code+='  }\n\n';
code+='  paint(ctx, size, properties) {\n';
if(type==='checkerboard'){
code+='    const s = '+size+';\n';
code+='    const cols = Math.ceil(size.width / s);\n';
code+='    const rows = Math.ceil(size.height / s);\n';
code+='    for (let row = 0; row < rows; row++) {\n';
code+='      for (let col = 0; col < cols; col++) {\n';
code+='        ctx.fillStyle = (row + col) % 2 === 0 ? "'+c1+'" : "'+c2+'";\n';
code+='        ctx.fillRect(col * s, row * s, s, s);\n';
code+='      }\n';
code+='    }\n';
}else if(type==='dots'){
code+='    const s = '+size+';\n';
code+='    const r = s / 4;\n';
code+='    const cols = Math.ceil(size.width / s);\n';
code+='    const rows = Math.ceil(size.height / s);\n';
code+='    ctx.fillStyle = "'+c2+'";\n';
code+='    ctx.fillRect(0, 0, size.width, size.height);\n';
code+='    ctx.fillStyle = "'+c1+'";\n';
code+='    for (let row = 0; row < rows; row++) {\n';
code+='      for (let col = 0; col < cols; col++) {\n';
code+='        ctx.beginPath();\n';
code+='        ctx.arc(col * s + s/2, row * s + s/2, r, 0, Math.PI * 2);\n';
code+='        ctx.fill();\n';
code+='      }\n';
code+='    }\n';
}else if(type==='stripes'){
code+='    const s = '+size+';\n';
code+='    const count = Math.ceil(size.width / s) + Math.ceil(size.height / s);\n';
code+='    for (let i = 0; i < count; i++) {\n';
code+='      ctx.fillStyle = i % 2 === 0 ? "'+c1+'" : "'+c2+'";\n';
code+='      ctx.beginPath();\n';
code+='      ctx.moveTo(i * s, 0);\n';
code+='      ctx.lineTo(i * s + size.height, size.height);\n';
code+='      ctx.lineTo(i * s + size.height + s, size.height);\n';
code+='      ctx.lineTo(i * s + s, 0);\n';
code+='      ctx.fill();\n';
code+='    }\n';
}else if(type==='crosshatch'){
code+='    const s = '+size+';\n';
code+='    ctx.strokeStyle = "'+c1+'";\n';
code+='    ctx.lineWidth = 1;\n';
code+='    ctx.fillStyle = "'+c2+'";\n';
code+='    ctx.fillRect(0, 0, size.width, size.height);\n';
code+='    for (let i = -size.height; i < size.width; i += s) {\n';
code+='      ctx.beginPath();\n';
code+='      ctx.moveTo(i, 0);\n';
code+='      ctx.lineTo(i + size.height, size.height);\n';
code+='      ctx.stroke();\n';
code+='      ctx.beginPath();\n';
code+='      ctx.moveTo(i + size.height, 0);\n';
code+='      ctx.lineTo(i, size.height);\n';
code+='      ctx.stroke();\n';
code+='    }\n';
}else if(type==='waves'){
code+='    const s = '+size+';\n';
code+='    ctx.fillStyle = "'+c2+'";\n';
code+='    ctx.fillRect(0, 0, size.width, size.height);\n';
code+='    ctx.strokeStyle = "'+c1+'";\n';
code+='    ctx.lineWidth = 2;\n';
code+='    for (let y = 0; y < size.height; y += s) {\n';
code+='      ctx.beginPath();\n';
code+='      for (let x = 0; x <= size.width; x += 2) {\n';
code+='        ctx.lineTo(x, y + Math.sin(x / s * Math.PI) * s / 3);\n';
code+='      }\n';
code+='      ctx.stroke();\n';
code+='    }\n';
}
code+='  }\n';
code+='}\n\n';
code+='registerPaint("paint-'+type+'", '+capitalize(type)+'Painter);\n\n';
code+='/* CSS Usage:\n';
code+='  .element {\n';
code+='    background: paint(paint-'+type+');\n';
code+='  }\n';
code+='*/\n';
document.getElementById('output').textContent=code;
var preview=document.getElementById('preview');
var canvas=document.createElement('canvas');
canvas.width=280;canvas.height=180;
canvas.style.cssText='border-radius:8px;border:1px solid rgba(148,163,184,.1)';
var ctx=canvas.getContext('2d');
var s=parseInt(size)||20;
if(type==='checkerboard'){
var cols=Math.ceil(280/s),rows=Math.ceil(180/s);
for(var r=0;r<rows;r++)for(var c=0;c<cols;c++){ctx.fillStyle=(r+c)%2===0?c1:c2;ctx.fillRect(c*s,r*s,s,s)}
}else if(type==='dots'){
ctx.fillStyle=c2;ctx.fillRect(0,0,280,180);ctx.fillStyle=c1;
var cols=Math.ceil(280/s),rows=Math.ceil(180/s);
for(var r=0;r<rows;r++)for(var c=0;c<cols;c++){ctx.beginPath();ctx.arc(c*s+s/2,r*s+s/2,s/4,0,Math.PI*2);ctx.fill()}
}else if(type==='stripes'){
var count=Math.ceil(280/s)+Math.ceil(180/s);
for(var i=0;i<count;i++){ctx.fillStyle=i%2===0?c1:c2;ctx.beginPath();ctx.moveTo(i*s,0);ctx.lineTo(i*s+180,180);ctx.lineTo(i*s+180+s,180);ctx.lineTo(i*s+s,0);ctx.fill()}
}else if(type==='crosshatch'){
ctx.fillStyle=c2;ctx.fillRect(0,0,280,180);ctx.strokeStyle=c1;ctx.lineWidth=1;
for(var i=-180;i<280;i+=s){ctx.beginPath();ctx.moveTo(i,0);ctx.lineTo(i+180,180);ctx.stroke();ctx.beginPath();ctx.moveTo(i+180,0);ctx.lineTo(i,180);ctx.stroke()}
}else if(type==='waves'){
ctx.fillStyle=c2;ctx.fillRect(0,0,280,180);ctx.strokeStyle=c1;ctx.lineWidth=2;
for(var y=0;y<180;y+=s){ctx.beginPath();for(var x=0;x<=280;x+=2){ctx.lineTo(x,y+Math.sin(x/s*Math.PI)*s/3)}ctx.stroke()}
}
preview.innerHTML='';
preview.appendChild(canvas);
saveHistory('houdiniPaintHistory',type);
showToast('Paint Worklet生成完成');
}
function capitalize(s){return s.charAt(0).toUpperCase()+s.slice(1)}
function downloadOutput(){
var text=document.getElementById('output').textContent;
if(!text||text==='等待生成...'){showToast('请先生成代码');return}
downloadText('paint-'+document.getElementById('paintType').value+'.js',text);
}
