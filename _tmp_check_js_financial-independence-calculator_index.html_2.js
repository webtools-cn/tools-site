
function showToast(m){var t=document.getElementById("toast");t.textContent=m;t.classList.add("show");setTimeout(function(){t.classList.remove("show")},3000)}
function copyText(id){var el=document.getElementById(id);if(!el)return;var t=el.textContent||el.innerText;navigator.clipboard.writeText(t).then(function(){showToast("已复制")})["catch"](function(){showToast("复制失败")})}

(function(){var app=document.getElementById('app');
app.innerHTML='<div class="input-section"><h2>👤 基本信息</h2><div class="row"><div class="field"><label>当前年龄</label><input type="number" id="currentAge" value="30" min="18" max="80"></div><div class="field"><label>年支出 (¥)</label><input type="number" id="annualExpense" value="120000"></div></div><div class="row"><div class="field"><label>当前储蓄 (¥)</label><input type="number" id="savings" value="200000"></div><div class="field"><label>每月存款 (¥)</label><input type="number" id="monthlyCont" value="8000"></div></div><div class="row"><div class="field"><label>预期年回报率 (%)</label><input type="number" id="returnRate" value="7" step="0.5"></div><div class="field"><label>提款策略</label><select id="strategy"><option value="4">4%规则</option><option value="3">3%保守</option><option value="5">5%激进</option></select></div></div><div class="btn-row"><button class="btn btn-primary" id="calcBtn">计算</button><button class="btn btn-secondary" id="resetBtn">重置</button></div></div><div class="result-section" id="resultSection"><h2>📊 财务独立分析</h2><div class="grid grid-cols-3" id="summaryCards"></div><h2 style="margin-top:16px">📅 时间线</h2><div class="grid grid-cols-2" id="timelineCards"></div><div id="assessment" style="color:#94a3b8;font-size:.9rem;margin-top:8px"></div></div>';

function formatMoney(v){return '¥'+Math.round(v).toLocaleString('zh-CN');}
function calc(){
var cAge=parseInt(document.getElementById('currentAge').value)||30;
var expense=parseFloat(document.getElementById('annualExpense').value)||0;
var savings=parseFloat(document.getElementById('savings').value)||0;
var monthly=parseFloat(document.getElementById('monthlyCont').value)||0;
var ret=parseFloat(document.getElementById('returnRate').value)||7;
var strategy=parseFloat(document.getElementById('strategy').value)||4;
var wr=strategy/100;
var neededSavings=expense/wr;
var fiRatio=savings/neededSavings*100;
var mr=ret/100/12;
var total=savings;
var years=0;
while(total<neededSavings&&years<100){total=total*(1+mr)+monthly;years++;}
var monthlyPassive=total*wr/12;
var retireAge=cAge+years;
document.getElementById('summaryCards').innerHTML='<div style="background:#0f172a;border-radius:8px;padding:16px;text-align:center"><div style="color:#64748b;font-size:.8rem">FI Ratio</div><div style="color:'+(fiRatio>=100?'#22d3ee':'#f87171')+';font-size:1.8rem;font-weight:700;margin-top:4px">'+fiRatio.toFixed(1)+'%</div></div><div style="background:#0f172a;border-radius:8px;padding:16px;text-align:center"><div style="color:#64748b;font-size:.8rem">目标储蓄</div><div style="color:#f1f5f9;font-size:1.2rem;font-weight:700;margin-top:4px">'+formatMoney(neededSavings)+'</div></div><div style="background:#0f172a;border-radius:8px;padding:16px;text-align:center"><div style="color:#64748b;font-size:.8rem">每月被动收入</div><div style="color:#fbbf24;font-size:1.4rem;font-weight:700;margin-top:4px">'+formatMoney(monthlyPassive)+'</div></div>';
document.getElementById('timelineCards').innerHTML='<div style="background:#0f172a;border-radius:8px;padding:16px;text-align:center"><div style="color:#64748b;font-size:.8rem">达到FI所需年数</div><div style="color:#22d3ee;font-size:1.4rem;font-weight:700;margin-top:4px">'+years+' 年</div></div><div style="background:#0f172a;border-radius:8px;padding:16px;text-align:center"><div style="color:#64748b;font-size:.8rem">财务独立年龄</div><div style="color:#4ade80;font-size:1.2rem;font-weight:700;margin-top:4px">'+retireAge+' 岁</div></div>';
var msg=years<=0?'<p style="color:#22d3ee">🎉 恭喜！您已经达到财务独立！</p>':fiRatio>=50?'<p style="color:#22d3ee">✅ 进展不错！您已完成'+fiRatio.toFixed(1)+'%的财务独立目标，预计'+years+'年后完全达到。</p>':'<p style="color:#f87171">⏳ 加油！您目前完成'+fiRatio.toFixed(1)+'%，还需'+years+'年。考虑增加储蓄或降低支出。</p>';
document.getElementById('assessment').innerHTML=msg;
document.getElementById('resultSection').classList.add('show');
}
document.getElementById('calcBtn').addEventListener('click',calc);
document.getElementById('resetBtn').addEventListener('click',function(){document.getElementById('currentAge').value=30;document.getElementById('annualExpense').value=120000;document.getElementById('savings').value=200000;document.getElementById('monthlyCont').value=8000;document.getElementById('returnRate').value=7;document.getElementById('strategy').value='4';document.getElementById('resultSection').classList.remove('show');});
calc();
})();

document.addEventListener('click',function(e){
  if(e.target&&e.target.closest&&e.target.closest('button')){
    setTimeout(ftEnsureCopy,250);
  }
});
function ftEnsureCopy(){
  var res=document.getElementById('result');
  if(!res||res.offsetParent===null)return;
  if(res.querySelector('.ft-copy-btn'))return;
  var langEN=/^en/i.test((document.documentElement.getAttribute('lang')||'zh'));
  var btn=document.createElement('button');
  btn.className='btn btn-secondary ft-copy-btn';
  btn.textContent=langEN?'📋 Copy Result':'📋 复制结果';
  btn.style.cssText='margin-top:12px;display:block';
  btn.onclick=function(){
    var txt=(res.innerText||res.textContent||'').replace(/\s+/g,' ').trim();
    function toast(m){
      var t=document.getElementById('toast');
      if(t){t.textContent=m;t.classList.add('show');setTimeout(function(){t.classList.remove('show')},2000)}
    }
    if(navigator.clipboard&&navigator.clipboard.writeText){
      navigator.clipboard.writeText(txt).then(function(){toast(langEN?'Copied!':'已复制')}).catch(function(){ftFallbackCopy(txt);toast(langEN?'Copied!':'已复制')});
    }else{ftFallbackCopy(txt);toast(langEN?'Copied!':'已复制')}
  };
  res.appendChild(btn);
}
function ftFallbackCopy(txt){
  var ta=document.createElement('textarea');
  ta.value=txt;ta.style.position='fixed';ta.style.opacity='0';
  document.body.appendChild(ta);ta.select();
  try{document.execCommand('copy')}catch(err){}
  document.body.removeChild(ta);
}

