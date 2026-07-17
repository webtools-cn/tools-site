var benchRunning=false;
var benchResults=[];
function loadExample(){
document.getElementById('codeA').value='// Array.map\nconst result = Array.from({length: 10000}, (_, i) => i).map(x => x * 2);';
document.getElementById('codeB').value='// For loop\nconst arr = Array.from({length: 10000}, (_, i) => i);\nconst result = [];\nfor (let i = 0; i < arr.length; i++) {\n  result.push(arr[i] * 2);\n}';
document.getElementById('iterations').value='1000';
document.getElementById('warmup').value='10';
}
function clearInput(){
document.getElementById('codeA').value='';
document.getElementById('codeB').value='';
document.getElementById('iterations').value='1000';
document.getElementById('warmup').value='10';
document.getElementById('output').textContent='等待测试...';
document.getElementById('chartArea').innerHTML='';
benchResults=[];
}
function runSingle(code,iterations){
var start=performance.now();
for(var i=0;i<iterations;i++){
try{new Function(code)()}catch(e){return{error:e.message}}
}
var end=performance.now();
return{time:end-start,opsPerSec:iterations/((end-start)/1000)};
}
async function execute(){
if(benchRunning){showToast('测试进行中，请等待');return}
var codeA=document.getElementById('codeA').value.trim();
var codeB=document.getElementById('codeB').value.trim();
var iterations=parseInt(document.getElementById('iterations').value)||1000;
var warmup=parseInt(document.getElementById('warmup').value)||10;
if(!codeA){showToast('请输入代码A');return}
benchRunning=true;
document.getElementById('output').textContent='预热中...';
await new Promise(r=>setTimeout(r,50));
for(var w=0;w<warmup;w++){
try{new Function(codeA)()}catch(e){}
if(codeB)try{new Function(codeB)()}catch(e){}
}
var resultsA=[];
var resultsB=[];
var rounds=5;
for(var r=0;r<rounds;r++){
document.getElementById('output').textContent='测试中... 第'+(r+1)+'/'+rounds+'轮';
await new Promise(resolve=>setTimeout(resolve,100));
var resA=runSingle(codeA,iterations);
if(resA.error){document.getElementById('output').textContent='代码A错误: '+resA.error;benchRunning=false;return}
resultsA.push(resA.time);
if(codeB){
var resB=runSingle(codeB,iterations);
if(resB.error){document.getElementById('output').textContent='代码B错误: '+resB.error;benchRunning=false;return}
resultsB.push(resB.time);
}
}
var avgA=resultsA.reduce(function(a,b){return a+b},0)/resultsA.length;
var minA=Math.min.apply(null,resultsA);
var maxA=Math.max.apply(null,resultsA);
var opsA=Math.round(iterations/(avgA/1000));
var output='=== 性能基准测试结果 ===\n\n';
output+='代码A:\n';
output+='  平均耗时: '+avgA.toFixed(3)+' ms ('+iterations+'次迭代)\n';
output+='  最快: '+minA.toFixed(3)+' ms | 最慢: '+maxA.toFixed(3)+' ms\n';
output+='  吞吐量: '+formatNumber(opsA)+' ops/sec\n';
output+='  各轮: '+resultsA.map(function(t){return t.toFixed(2)+'ms'}).join(', ')+'\n';
if(codeB){
var avgB=resultsB.reduce(function(a,b){return a+b},0)/resultsB.length;
var minB=Math.min.apply(null,resultsB);
var maxB=Math.max.apply(null,resultsB);
var opsB=Math.round(iterations/(avgB/1000));
output+='\n代码B:\n';
output+='  平均耗时: '+avgB.toFixed(3)+' ms ('+iterations+'次迭代)\n';
output+='  最快: '+minB.toFixed(3)+' ms | 最慢: '+maxB.toFixed(3)+' ms\n';
output+='  吞吐量: '+formatNumber(opsB)+' ops/sec\n';
output+='  各轮: '+resultsB.map(function(t){return t.toFixed(2)+'ms'}).join(', ')+'\n';
output+='\n=== 对比 ===\n';
var speedup=avgA/avgB;
if(speedup>1){
output+='代码B 快 '+speedup.toFixed(2)+'x ('+((speedup-1)*100).toFixed(1)+'% 更快)';
}else{
output+='代码A 快 '+(1/speedup).toFixed(2)+'x ('+((1/speedup-1)*100).toFixed(1)+'% 更快)';
}
drawChart(resultsA,resultsB);
}else{
drawChart(resultsA,null);
}
document.getElementById('output').textContent=output;
benchRunning=false;
showToast('基准测试完成');
}
function formatNumber(n){
if(n>=1e6)return(n/1e6).toFixed(1)+'M';
if(n>=1e3)return(n/1e3).toFixed(1)+'K';
return n.toString();
}
function drawChart(a,b){
var html='<div style="display:flex;gap:16px;align-items:flex-end;height:120px;padding:8px 0">';
var maxVal=Math.max.apply(null,a.concat(b||[0]));
a.forEach(function(v,i){
var h=Math.max(4,(v/maxVal)*100);
html+='<div style="display:flex;flex-direction:column;align-items:center;gap:2px">';
html+='<span style="color:#94a3b8;font-size:.7rem">'+v.toFixed(1)+'ms</span>';
html+='<div style="width:30px;height:'+h+'px;background:rgba(6,182,212,.6);border-radius:3px 3px 0 0"></div>';
html+='<span style="color:#64748b;font-size:.65rem">A'+(i+1)+'</span>';
html+='</div>';
});
if(b){
b.forEach(function(v,i){
var h=Math.max(4,(v/maxVal)*100);
html+='<div style="display:flex;flex-direction:column;align-items:center;gap:2px">';
html+='<span style="color:#94a3b8;font-size:.7rem">'+v.toFixed(1)+'ms</span>';
html+='<div style="width:30px;height:'+h+'px;background:rgba(168,85,247,.6);border-radius:3px 3px 0 0"></div>';
html+='<span style="color:#64748b;font-size:.65rem">B'+(i+1)+'</span>';
html+='</div>';
});
}
html+='</div>';
html+='<div style="display:flex;gap:16px;margin-top:4px;font-size:.75rem">';
html+='<span style="color:#06b6d4">■ 代码A</span>';
if(b)html+='<span style="color:#a855f7">■ 代码B</span>';
html+='</div>';
document.getElementById('chartArea').innerHTML=html;
}
