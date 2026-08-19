
function formatCurrency(n){return new Intl.NumberFormat('zh-CN',{style:'currency',currency:'CNY',minimumFractionDigits:0,maximumFractionDigits:0}).format(n)}
function formatPct(n){return n.toFixed(1)+'%'}

function calculate(){
const nw=parseFloat(document.getElementById('netWorth').value)||0;
const ae=parseFloat(document.getElementById('annualExpense').value)||0;
const ai=parseFloat(document.getElementById('annualIncome').value)||0;
const rr=parseFloat(document.getElementById('returnRate').value)||7;
const age=parseInt(document.getElementById('currentAge').value)||0;
if(ae<=0){showToast('请输入年支出金额');return}
if(nw<0||ai<0){showToast('请输入有效金额');return}

const fireTarget=ae*25;
const progress=nw/fireTarget*100;
const annualSavings=ai-ae;
const savingsRate=ai>0?(annualSavings/ai*100):0;
let yearsToFire=999;
if(annualSavings>0&&rr>0){
const r=rr/100;
yearsToFire=Math.log(1+(fireTarget-nw)*(r/annualSavings))/Math.log(1+r);
}
const fireAge=age+Math.ceil(yearsToFire);

document.getElementById('results').style.display='block';
document.getElementById('fireTarget').textContent=formatCurrency(fireTarget);
document.getElementById('currentProgress').textContent=formatPct(Math.min(progress,9999));
document.getElementById('annualSavings').textContent=formatCurrency(Math.max(0,annualSavings));
document.getElementById('savingsRate').textContent=formatPct(Math.max(0,Math.min(savingsRate,100)));
document.getElementById('yearsToFire').textContent=yearsToFire<999?Math.ceil(yearsToFire)+' 年':'需增加储蓄';
document.getElementById('fireAge').textContent=yearsToFire<999?fireAge+' 岁':'—';

const bar=document.getElementById('progressBar');
bar.style.width=Math.min(progress,100)+'%';
bar.textContent=formatPct(Math.min(progress,100));

const milestones=[
{pct:25,label:'FIRE起步',desc:'达到目标25%'},
{pct:50,label:'FIRE中点',desc:'实现一半自由'},
{pct:75,label:'FIRE冲刺',desc:'距自由一步之遥'},
{pct:100,label:'FIRE达成!',desc:'恭喜财务自由'}
];
const ml=document.getElementById('milestones');
ml.innerHTML=milestones.map(m=>`<li class="${progress>=m.pct?'reached':''}"><span>🏁 ${m.label}</span><span>${m.desc}</span><span class="pct">${m.pct}%</span></li>`).join('');
}

function copyResults(){
const items=[
'FIRE目标金额: '+document.getElementById('fireTarget').textContent,
'当前进度: '+document.getElementById('currentProgress').textContent,
'年储蓄: '+document.getElementById('annualSavings').textContent,
'储蓄率: '+document.getElementById('savingsRate').textContent,
'预计FIRE年数: '+document.getElementById('yearsToFire').textContent,
'预计FIRE年龄: '+document.getElementById('fireAge').textContent
];
navigator.clipboard.writeText('🔥 FIRE进度追踪结果\n'+items.join('\n')).then(()=>showToast('✅ 已复制'));
}

function resetForm(){
['netWorth','annualExpense','annualIncome','returnRate','currentAge'].forEach(id=>document.getElementById(id).value='');
document.getElementById('returnRate').value='7';
document.getElementById('results').style.display='none';
showToast('🔄 已清空');
}

function showToast(msg){
const t=document.getElementById('toast');
t.textContent=msg;t.classList.add('show');
setTimeout(()=>t.classList.remove('show'),2000);
}

function fillExample(){
  var vals = [["netWorth", "500000"], ["annualExpense", "120000"], ["annualIncome", "200000"], ["returnRate", "7"], ["currentAge", "30"]];
  for(var i=0;i<vals.length;i++){
    var el = document.getElementById(vals[i][0]);
    if(el){el.value = vals[i][1];}
  }
  calculate();
  var t=document.getElementById('toast');
  if(t){t.textContent='已填入示例并计算';t.classList.add('show');setTimeout(function(){t.classList.remove('show')},2000)}
}
