
(function(){
const $=s=>document.getElementById(s);
function fmt(v){return '$'+v.toLocaleString('en-US',{minimumFractionDigits:0,maximumFractionDigits:0})}
function calc(){
const income=+$('annualIncome').value,expense=+$('annualExpense').value,
nw=+$('currentNetWorth').value,age=+$('currentAge').value,
ret=+$('annualReturn').value/100,swr=+$('withdrawalRate').value/100;
if(income<=0||expense<=0){showToast('请填写有效数值');return}
const savings=income-expense;
const fireNumber=expense/swr;
const leanFire=expense*20,fatFire=expense*35;
let years=0;let bal=nw;
while(bal<fireNumber&&years<100){bal=bal*(1+ret)+savings;years++}
const fireAge=age+years;
const coastBal=nw*Math.pow(1+ret,65-age);
const coastFire=(coastBal>=fireNumber)?age:65;
const pct=Math.min(100,(nw/fireNumber*100));
$('fireNumber').textContent=fmt(fireNumber);
$('fireAge').textContent=fireAge>age?fireAge+'岁':'已达成!';
$('fireYears').textContent=fireAge>age?'还需 '+years+' 年':'恭喜!';
$('annualSavings').textContent=fmt(savings);
$('savingsRate').textContent='储蓄率: '+(savings/income*100).toFixed(1)+'%';
$('coastFireAge').textContent=(coastFire>=65||nw>=fireNumber)?'已达Coast!':(65-coastFire>0?'还需存'+(65-coastFire)+'年':'已达');
$('leanFire').textContent=fmt(leanFire);
$('fatFire').textContent=fmt(fatFire);
$('progressPct').textContent=pct.toFixed(1)+'%';
$('progressFill').style.width=pct+'%';
drawChart(nw,savings,fireNumber,years,ret);
}
function drawChart(start,savings,target,years,ret){
const canvas=$('fireChart'),ctx=canvas.getContext('2d');
const dpr=window.devicePixelRatio||1;
const w=canvas.parentElement.clientWidth-32,h=280;
canvas.width=w*dpr;canvas.height=h*dpr;
canvas.style.width=w+'px';canvas.style.height=h+'px';
ctx.scale(dpr,dpr);ctx.clearRect(0,0,w,h);
const maxY=Math.max(target*1.1,start);
const scaleY=h/(maxY*1.05);
ctx.strokeStyle='rgba(148,163,184,.3)';ctx.fillStyle='#64748b';ctx.font='10px sans-serif';
for(let i=0;i<=5;i++){const y=h-(maxY/5*i*scaleY);ctx.beginPath();ctx.moveTo(40,y);ctx.lineTo(w-20,y);ctx.stroke();ctx.fillText('$'+(maxY/5*i).toFixed(0),2,y+4)}
ctx.strokeStyle='rgba(239,68,68,.3)';ctx.setLineDash([5,5]);
const ty=h-target*scaleY;ctx.beginPath();ctx.moveTo(40,ty);ctx.lineTo(w-20,ty);ctx.stroke();
ctx.fillStyle='#f87171';ctx.fillText('FIRE数字',w-100,ty-5);
ctx.setLineDash([]);
ctx.beginPath();ctx.strokeStyle='#22c55e';ctx.lineWidth=2;
let bal=start;ctx.moveTo(40,h-bal*scaleY);
const pts=Math.min(years+10,50);
for(let i=0;i<=pts;i++){const x=40+(w-60)*(i/pts);const y=h-bal*scaleY;ctx.lineTo(x,y);bal=bal*(1+ret)+savings}
ctx.stroke();
}
function reset(){
$('annualIncome').value=100000;$('annualExpense').value=40000;
$('currentNetWorth').value=50000;$('currentAge').value=30;
$('annualReturn').value=7;$('withdrawalRate').value=4;
['fireNumber','fireAge','annualSavings','coastFireAge','leanFire','fatFire'].forEach(id=>$(id).textContent='-');
$('fireYears').textContent='-';$('savingsRate').textContent='储蓄率: -';
$('progressPct').textContent='0%';$('progressFill').style.width='0%';
const c=$('fireChart'),ctx=c.getContext('2d');ctx.clearRect(0,0,c.width,c.height)
}
function copyResult(){
navigator.clipboard.writeText(['=== FIRE分析结果 ===',
'FIRE数字: '+$('fireNumber').textContent,'达到FIRE: '+$('fireAge').textContent+' ('+$('fireYears').textContent+')',
'年储蓄: '+$('annualSavings').textContent+' ('+$('savingsRate').textContent+')',
'Coast FIRE: '+$('coastFireAge').textContent,
'Lean FIRE: '+$('leanFire').textContent,'Fat FIRE: '+$('fatFire').textContent].join('\n'))
.then(()=>showToast('✅ 已复制')).catch(()=>showToast('复制失败'))
}
function showToast(msg){const t=$('toast');t.textContent=msg;t.classList.add('show');setTimeout(()=>t.classList.remove('show'),2000)}
$('calcBtn').addEventListener('click',calc);
$('resetBtn').addEventListener('click',reset);
$('copyBtn').addEventListener('click',copyResult);
calc();
})();
