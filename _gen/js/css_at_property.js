function loadExample(){
document.getElementById('propertyName').value='--gradient-angle';
document.getElementById('syntax').value='<angle>';
document.getElementById('initialValue').value='0deg';
document.getElementById('inherits').value='false';
document.getElementById('animValue1').value='0deg';
document.getElementById('animValue2').value='360deg';
document.getElementById('animDuration').value='3';
document.getElementById('animTiming').value='linear';
document.getElementById('animIteration').value='infinite';
execute();
}
function clearInput(){
document.getElementById('propertyName').value='';
document.getElementById('syntax').value='';
document.getElementById('initialValue').value='';
document.getElementById('inherits').value='false';
document.getElementById('output').textContent='等待生成...';
document.getElementById('preview').innerHTML='';
}
function execute(){
var name=document.getElementById('propertyName').value.trim();
var syntax=document.getElementById('syntax').value.trim();
var initial=document.getElementById('initialValue').value.trim();
var inherits=document.getElementById('inherits').value;
var anim1=document.getElementById('animValue1').value.trim();
var anim2=document.getElementById('animValue2').value.trim();
var dur=document.getElementById('animDuration').value.trim()||'3';
var timing=document.getElementById('animTiming').value;
var iter=document.getElementById('animIteration').value;
if(!name){showToast('请输入属性名称');return}
if(!syntax){showToast('请输入语法类型');return}
if(!initial){showToast('请输入初始值');return}
var code='@property '+name+' {\n';
code+='  syntax: "'+syntax+'";\n';
code+='  inherits: '+inherits+';\n';
code+='  initial-value: '+initial+';\n';
code+='}\n';
if(anim1&&anim2){
code+='\n@keyframes '+name.replace(/^--/,'')+'-anim {\n';
code+='  from { '+name+': '+anim1+'; }\n';
code+='  to { '+name+': '+anim2+'; }\n';
code+='}\n';
code+='\n.animated-element {\n';
code+='  animation: '+name.replace(/^--/,'')+'-anim '+dur+'s '+timing+' '+iter+';\n';
code+='}\n';
}
document.getElementById('output').textContent=code;
var preview=document.getElementById('preview');
if(name==='--gradient-angle'&&anim1==='0deg'&&anim2==='360deg'){
preview.innerHTML='<div style="width:200px;height:200px;border-radius:12px;background:linear-gradient(var(--gradient-angle),#06b6d4,#8b5cf6,#ec4899);animation:gradient-rotate '+dur+'s '+timing+' '+iter+'"></div><style>@property --gradient-angle{syntax:"<angle>";inherits:false;initial-value:0deg}@keyframes gradient-rotate{from{--gradient-angle:0deg}to{--gradient-angle:360deg}}</style>';
}else{
preview.innerHTML='<div style="padding:16px;background:#1e293b;border-radius:8px;color:#94a3b8;font-size:.85rem">预览仅支持渐变角度动画示例，其他属性请复制代码到本地测试</div>';
}
saveHistory('cssAtPropertyHistory',name);
showToast('CSS @property生成完成');
}
function downloadOutput(){
var text=document.getElementById('output').textContent;
if(!text||text==='等待生成...'){showToast('请先生成代码');return}
downloadText('custom-property.css',text);
}
