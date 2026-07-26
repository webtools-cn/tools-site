#!/usr/bin/env python3
"""直接写文件，不用复杂的模板"""
import os, json

TOOLS_DATA = [
    {
        "slug": "debt-snowball",
        "name_zh": "债务雪球计算器",
        "name_en": "Debt Snowball Calculator",
        "desc_zh": "在线债务雪球计算器，按雪球法/雪崩法规划债务还款策略，可视化还款时间线，免费在线工具，浏览器本地处理。",
        "desc_en": "Online debt snowball calculator. Plan debt repayment using snowball or avalanche method, visualize payoff timeline. Free online tool, browser-side processing.",
        "icon_zh": "🏔️",
        "icon_en": "🏔️",
        "instructions_zh": "输入每笔债务信息，选择还款策略，查看还款计划",
        "instructions_en": "Enter debt details, choose repayment strategy, view payoff plan",
        "special": "debt",
    },
    {
        "slug": "tax-estimator",
        "name_zh": "个税估算器",
        "name_en": "Tax Estimator",
        "desc_zh": "在线个税估算器，计算个人所得税，支持月收入/年终奖，新旧个税法对比，免费在线工具，浏览器本地处理。",
        "desc_en": "Online income tax estimator. Calculate personal income tax for monthly salary and year-end bonus. Free online tool, browser-side processing.",
        "icon_zh": "🧾",
        "icon_en": "🧾",
        "instructions_zh": "输入月收入和扣除项，估算个人所得税",
        "instructions_en": "Enter monthly income and deductions to estimate income tax",
        "special": "",
    },
    {
        "slug": "hourly-to-salary",
        "name_zh": "时薪转年薪计算器",
        "name_en": "Hourly to Salary Calculator",
        "desc_zh": "在线时薪转年薪计算器，快速换算出时薪/日薪/周薪/月薪/年薪，支持不同工作小时数，免费在线工具。",
        "desc_en": "Online hourly to salary calculator. Convert between hourly, daily, weekly, monthly, and annual salary. Free online tool.",
        "icon_zh": "⏱️",
        "icon_en": "⏱️",
        "instructions_zh": "输入时薪和工作时间，换算不同周期的薪资",
        "instructions_en": "Enter hourly rate and work hours to convert across pay periods",
        "special": "",
    },
    {
        "slug": "cap-rate-calculator",
        "name_zh": "资本化率计算器",
        "name_en": "Cap Rate Calculator",
        "desc_zh": "在线资本化率(Cap Rate)计算器，计算房产投资回报率，评估商业地产/租赁物业价值，免费在线工具。",
        "desc_en": "Online cap rate calculator. Calculate real estate investment return, evaluate commercial/rental property value. Free online tool.",
        "icon_zh": "🏢",
        "icon_en": "🏢",
        "instructions_zh": "输入净运营收入和房产价值，计算资本化率",
        "instructions_en": "Enter net operating income and property value to calculate cap rate",
        "special": "",
    },
    {
        "slug": "rental-yield",
        "name_zh": "租金回报率计算器",
        "name_en": "Rental Yield Calculator",
        "desc_zh": "在线租金回报率计算器，计算房产租金年回报率，分析毛回报率和净回报率，免费在线工具，浏览器本地处理。",
        "desc_en": "Online rental yield calculator. Calculate property rental return, analyze gross and net yield. Free online tool, browser-side processing.",
        "icon_zh": "🏠",
        "icon_en": "🏠",
        "instructions_zh": "输入购房价格和租金收入，计算租金回报率",
        "instructions_en": "Enter purchase price and rental income to calculate rental yield",
        "special": "",
    },
]

# 公共头部、CSS、Footer等
HEAD_CSS = '''<!DOCTYPE html>
<html lang="LANG">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>TITLE</title>
  <meta name="description" content="DESC">
  <meta property="og:title" content="OGTITLE">
  <meta property="og:description" content="DESC">
  <meta property="og:type" content="website">
  <script type="application/ld+json">SAPP</script>
  <style>
    :root{--primary:#4F46E5;--bg:#f8fafc;--card:#fff;--text:#1e293b;--sub:#64748b;--border:#e2e8f0;--radius:12px}
    *{margin:0;padding:0;box-sizing:border-box}
    body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;background:var(--bg);color:var(--text);min-height:100vh;display:flex;flex-direction:column}
    header{background:var(--card);border-bottom:1px solid var(--border);padding:16px 24px;display:flex;justify-content:space-between;align-items:center}
    header a{color:var(--primary);text-decoration:none;font-weight:600;font-size:18px}
    .lang-switch a{color:var(--sub);font-size:14px;text-decoration:none;padding:4px 12px;border-radius:6px;border:1px solid var(--border)}
    .lang-switch a:hover{color:var(--primary);border-color:var(--primary)}
    main{flex:1;max-width:700px;margin:0 auto;padding:40px 20px;width:100%}
    h1{font-size:28px;margin-bottom:8px;text-align:center}
    .subtitle{text-align:center;color:var(--sub);margin-bottom:32px}
    .card{background:var(--card);border-radius:var(--radius);padding:24px;border:1px solid var(--border);margin-bottom:20px}
    .form-group{margin-bottom:16px}
    .form-group label{display:block;font-weight:600;margin-bottom:6px;font-size:14px}
    .form-group input,.form-group select{width:100%;padding:12px;border:2px solid var(--border);border-radius:8px;font-size:16px}
    .form-group input:focus,.form-group select:focus{outline:none;border-color:var(--primary)}
    .row{display:flex;gap:12px}.row>*{flex:1}
    .btn{width:100%;padding:14px;border:none;border-radius:8px;font-size:16px;cursor:pointer;font-weight:600;background:var(--primary);color:#fff;transition:all .2s}
    .btn:hover{opacity:.9;transform:translateY(-1px)}
    .btn-secondary{background:var(--border);color:var(--text);margin-bottom:8px}
    .result{background:#eef2ff;border-radius:8px;padding:20px;margin-top:20px;text-align:center}
    .result .final{font-size:36px;font-weight:700;color:var(--primary)}
    .result .detail{font-size:14px;color:var(--sub);margin-top:8px;line-height:1.8}
    .result-item{display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid rgba(0,0,0,.05);text-align:left}
    .result-item:last-child{border-bottom:none}
    .result-item .label{color:var(--sub);font-size:13px}
    .result-item .value{font-weight:600;font-size:15px}
    .debt-row{background:#f8fafc;border-radius:8px;padding:12px;margin-bottom:8px;position:relative}
    .debt-row .row{margin-bottom:8px}
    .debt-row .row:last-child{margin-bottom:0}
    .remove-btn{position:absolute;top:8px;right:12px;background:none;border:none;color:var(--sub);cursor:pointer;font-size:18px}
    table{width:100%;border-collapse:collapse;margin-top:16px;font-size:13px}
    th,td{padding:8px;text-align:left;border-bottom:1px solid var(--border)}
    th{background:var(--bg);font-weight:600;color:var(--sub)}
    .highlight{color:var(--primary);font-weight:700}
    footer{text-align:center;padding:24px;color:var(--sub);font-size:13px;border-top:1px solid var(--border)}
    @media(max-width:600px){main{padding:20px 12px}h1{font-size:22px}.row{flex-direction:column}table{font-size:11px}}
  @media(max-width:640px){h1{font-size:1.2rem;word-break:break-word}.header{flex-direction:column;gap:8px}}
.copy-btn{display:inline-flex;align-items:center;gap:4px;padding:6px 12px;background:rgba(6,182,212,.1);color:#22d3ee;border:1px solid rgba(6,182,212,.25);border-radius:6px;cursor:pointer;font-size:.8rem;transition:all .2s;margin-left:8px;vertical-align:top}
.copy-btn:hover{background:rgba(6,182,212,.25)}
.copy-btn.copied{background:rgba(34,197,94,.15);color:#22c55e;border-color:rgba(34,197,94,.3)}
</style>
'''

HEAD_META = '''
<meta property="og:image" content="https://free-toolbase.com/og-image.svg">
<meta name="twitter:image" content="https://free-toolbase.com/og-image.svg">
<meta name="twitter:card" content="summary_large_image">
<link rel="canonical" href="CANONICAL">
<link rel="alternate" hreflang="zh" href="HREF_ZH">
<link rel="alternate" hreflang="en" href="HREF_EN">
<link rel="alternate" hreflang="x-default" href="HREF_X">
<meta name="robots" content="index, follow">
<link rel="icon" type="image/svg+xml" href="favicon.svg">
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5998441792679372" crossorigin="anonymous"></script>
BREADCRUMB
</head>
<body>
'''

TOAST_JS = '''
<script>
(function(){
  var processed = new Set();
  function addCopyBtns(){
    var results = document.querySelectorAll('[id*="result"],[id*="Result"],[id*="output"],[id*="Output"],[class*="result"],[class*="output"]');
    results.forEach(function(el){
      if(processed.has(el)) return;
      if(el.querySelector('.copy-btn')) return;
      if(el.tagName==='INPUT'||el.tagName==='TEXTAREA'||el.tagName==='SELECT') return;
      if(el.children.length===0 && el.textContent.trim().length<5) return;
      var btn = document.createElement('button');
      btn.className = 'copy-btn';
      btn.innerHTML = 'COPY_LABEL';
      btn.title = 'COPY_TITLE';
      btn.onclick = function(e){
        e.stopPropagation();
        var text = el.textContent || el.value || '';
        if(el.tagName==='INPUT'||el.tagName==='TEXTAREA') text = el.value;
        navigator.clipboard.writeText(text.trim()).then(function(){
          btn.innerHTML = 'COPIED_LABEL';
          btn.classList.add('copied');
          setTimeout(function(){btn.innerHTML='COPY_LABEL';btn.classList.remove('copied');},2000);
        }).catch(function(){
          var ta = document.createElement('textarea');
          ta.value = text.trim();
          ta.style.position='fixed';ta.style.opacity='0';
          document.body.appendChild(ta);
          ta.select();
          document.execCommand('copy');
          document.body.removeChild(ta);
          btn.innerHTML = 'COPIED_LABEL';
          btn.classList.add('copied');
          setTimeout(function(){btn.innerHTML='COPY_LABEL';btn.classList.remove('copied');},2000);
        });
      };
      el.appendChild(btn);
      processed.add(el);
    });
  }
  addCopyBtns();
  document.addEventListener('click', function(){setTimeout(addCopyBtns,100);});
  if(window.MutationObserver){
    var obs = new MutationObserver(function(){addCopyBtns();});
    obs.observe(document.body,{childList:true,subtree:true});
  }
})();
</script>
'''

FOOTER = '</body>\n</html>'

def gen_breadcrumb_cn(name, slug):
    return f'<script type="application/ld+json">{{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{{"@type": "ListItem", "position": 1, "name": "\\u9996\\u9875", "item": "https://free-toolbase.com/"}}, {{"@type": "ListItem", "position": 2, "name": "\\u5de5\\u5177", "item": "https://free-toolbase.com/#tools"}}, {{"@type": "ListItem", "position": 3, "name": "{name}", "item": "https://free-toolbase.com/{slug}/"}}]}}</script>'

def gen_breadcrumb_en(name, slug):
    return f'<script type="application/ld+json">{{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{{"@type": "ListItem", "position": 1, "name": "Home", "item": "https://free-toolbase.com/en/"}}, {{"@type": "ListItem", "position": 2, "name": "Tools", "item": "https://free-toolbase.com/en/#tools"}}, {{"@type": "ListItem", "position": 3, "name": "{name}", "item": "https://free-toolbase.com/en/{slug}/"}}]}}</script>'

def gen_schema_app(name, desc):
    d = desc[:50] if len(desc) > 50 else desc
    return '{"@context":"https://schema.org","@type":"SoftwareApplication","name":"' + name + '","applicationCategory":"FinanceApplication","operatingSystem":"Web","description":"' + d + '"}'

# 现在给每个工具写专门的脚本片段

# --- debt-snowball ---
DEBT_SNOWBALL_JS = '''
<script>
let debtCount=1;
function addDebtRow(){
  debtCount++;
  var div=document.createElement('div');
  div.className='debt-row';
  div.id='debt-row-'+debtCount;
  div.innerHTML='<button class="remove-btn" onclick="removeDebt('+debtCount+')">\\u00d7</button>'+
    '<div class="row"><div class="form-group"><label>LABEL_DEBT_NAME</label><input type="text" id="debt'+debtCount+'" placeholder="PH_DEBT"></div>'+
    '<div class="form-group"><label>LABEL_BAL</label><input type="number" id="bal'+debtCount+'" min="0" step="0.01"></div></div>'+
    '<div class="row"><div class="form-group"><label>LABEL_RATE</label><input type="number" id="rate'+debtCount+'" min="0" max="100" step="0.1"></div>'+
    '<div class="form-group"><label>LABEL_MIN</label><input type="number" id="min'+debtCount+'" min="0" step="0.01"></div></div>';
  document.getElementById('debts-container').appendChild(div);
}
function removeDebt(id){
  var el=document.getElementById('debt-row-'+id);
  if(el)el.remove();
}
document.getElementById('btnCalc').addEventListener('click',function(){
  var method=document.getElementById('method').value;
  var extra=parseFloat(document.getElementById('extraPayment').value)||0;
  var debts=[];
  for(var i=1;i<=debtCount;i++){
    var row=document.getElementById('debt-row-'+i);
    if(!row)continue;
    var nameEl=document.getElementById('debt'+i);
    var name=nameEl?nameEl.value:'DEFAULT_DEBT';
    var bal=parseFloat((document.getElementById('bal'+i)||{}).value)||0;
    var rate=parseFloat((document.getElementById('rate'+i)||{}).value)||0;
    var min=parseFloat((document.getElementById('min'+i)||{}).value)||0;
    if(bal>0)debts.push({name:name,bal:bal,rate:rate/100,min:min,orig:bal});
  }
  if(debts.length===0){alert('ALERT_NO_DEBT');return;}
  var totalMin=debts.reduce(function(s,d){return s+d.min;},0)+extra;
  var months=0,totalPaid=0;
  var timeline=[];
  var maxMonths=Math.min(600,debts.reduce(function(s,d){return s+Math.ceil(d.bal/Math.max(d.min,1));},0)+100);
  while(debts.some(function(d){return d.bal>0.01;})&&months<600){
    months++;
    var paidThisMonth=0;
    for(var j=0;j<debts.length;j++){
      var d=debts[j];
      if(d.bal<=0.01)continue;
      var pay=Math.min(d.min,d.bal);
      d.bal-=pay;paidThisMonth+=pay;
    }
    var remaining=totalMin-paidThisMonth;
    if(method==='snowball'){
      debts.sort(function(a,b){return a.bal-b.bal;});
    }else{
      debts.sort(function(a,b){return b.rate-a.rate;});
    }
    for(var k=0;k<debts.length;k++){
      var dd=debts[k];
      if(dd.bal<=0.01||remaining<=0)continue;
      var pay2=Math.min(remaining,dd.bal);
      dd.bal-=pay2;remaining-=pay2;paidThisMonth+=pay2;
    }
    totalPaid+=paidThisMonth;
    if(months%4===0||months===1){
      var row2={month:months,total:totalPaid};
      debts.forEach(function(d){row2[d.name]=(d.orig-d.bal).toFixed(0);});
      timeline.push(row2);
    }
  }
  var names=debts.map(function(d){return d.name;});
  var totalOrig=debts.reduce(function(s,d){return s+d.orig;},0);
  var html='<div style="text-align:left"><div class="result-item"><span class="label">STRATEGY_LABEL</span><span class="value">METHOD_LABEL</span></div>';
  html+='<div class="result-item"><span class="label">MONTHS_LABEL</span><span class="value">'+months+' MONTHS_UNIT</span></div>';
  html+='<div class="result-item"><span class="label">LABEL_TOTAL_DEBT</span><span class="value">CURRENCY'+totalOrig.toFixed(2)+'</span></div>';
  html+='<div class="result-item"><span class="label">LABEL_TOTAL_PAID</span><span class="value highlight">CURRENCY'+totalPaid.toFixed(2)+'</span></div>';
  html+='<div class="result-item"><span class="label">LABEL_EXTRA</span><span class="value">CURRENCY'+extra.toFixed(2)+'</span></div>';
  html+='<table><tr><th>LABEL_MONTH</th>'+names.map(function(n){return '<th>'+n+'</th>';}).join('')+'<th>LABEL_CUMULATIVE</th></tr>';
  timeline.forEach(function(r){
    html+='<tr><td>'+r.month+'</td>'+names.map(function(n){return '<td>CURRENCY'+(r[n]||'0')+'</td>';}).join('')+'<td>CURRENCY'+r.total.toFixed(0)+'</td></tr>';
  });
  html+='</table></div>';
  document.getElementById('result').innerHTML=html;
  document.getElementById('result').style.display='block';
});
document.getElementById('btnClear').addEventListener('click',function(){
  document.getElementById('result').style.display='none';
  document.getElementById('result').innerHTML='';
  document.getElementById('extraPayment').value='0';
  while(debtCount>1)removeDebt(debtCount--);
  document.getElementById('debt1').value='DEFAULT_DEBT1_NAME';
  document.getElementById('bal1').value='10000';
  document.getElementById('rate1').value='18';
  document.getElementById('min1').value='200';
});
</script>'''

# 为每个工具页面填充：先把JS里的占位符替换成对应语言的字符串
def localize_js(js, lang):
    """替换JS中的文本占位符为实际语言文本"""
    if lang == 'zh':
        replacements = {
            'LABEL_DEBT_NAME': '债务名称', 'PH_DEBT': '债务名称',
            'LABEL_BAL': '欠款金额（元）', 'LABEL_RATE': '年利率 (%)', 'LABEL_MIN': '每月最低还款（元）',
            'DEFAULT_DEBT': '债务名称', 'DEFAULT_DEBT1_NAME': '信用卡A',
            'ALERT_NO_DEBT': '请至少添加一笔债务',
            'STRATEGY_LABEL': '还款策略',
            'METHOD_LABEL': "(method==='snowball'?'雪球法（先还小债务）':'雪崩法（先还高利率）')",
            'MONTHS_LABEL': '总还款月数', 'MONTHS_UNIT': '个月',
            'LABEL_TOTAL_DEBT': '原始总债务', 'LABEL_TOTAL_PAID': '总还款金额', 'LABEL_EXTRA': '额外月供',
            'LABEL_MONTH': '月份', 'LABEL_CUMULATIVE': '累计还款',
            'CURRENCY': '¥',
            'COPY_LABEL': '📋 复制', 'COPIED_LABEL': '✅ 已复制', 'COPY_TITLE': '复制结果',
        }
    else:
        replacements = {
            'LABEL_DEBT_NAME': 'Debt Name', 'PH_DEBT': 'Debt Name',
            'LABEL_BAL': 'Balance ($)', 'LABEL_RATE': 'APR (%)', 'LABEL_MIN': 'Min Payment ($)',
            'DEFAULT_DEBT': 'Debt Name', 'DEFAULT_DEBT1_NAME': 'Credit Card A',
            'ALERT_NO_DEBT': 'Please add at least one debt',
            'STRATEGY_LABEL': 'Strategy',
            'METHOD_LABEL': "(method==='snowball'?'Snowball (smallest first)':'Avalanche (highest APR first)')",
            'MONTHS_LABEL': 'Total Months', 'MONTHS_UNIT': 'months',
            'LABEL_TOTAL_DEBT': 'Total Original Debt', 'LABEL_TOTAL_PAID': 'Total Paid', 'LABEL_EXTRA': 'Extra Monthly',
            'LABEL_MONTH': 'Month', 'LABEL_CUMULATIVE': 'Cumulative',
            'CURRENCY': '$',
            'COPY_LABEL': '📋 Copy', 'COPIED_LABEL': '✅ Copied', 'COPY_TITLE': 'Copy result',
        }
    # 需要特殊处理METHOD_LABEL（它是JS表达式，不能简单替换为字符串）
    # 直接在代码里处理
    for k, v in replacements.items():
        if k == 'METHOD_LABEL':
            continue  # 下面单独处理
        js = js.replace(k, v)
    
    # 特殊处理：METHOD_LABEL是JS表达式
    if lang == 'zh':
        js = js.replace('METHOD_LABEL', "(method==='snowball'?'雪球法（先还小债务）':'雪崩法（先还高利率）')")
    else:
        js = js.replace('METHOD_LABEL', "(method==='snowball'?'Snowball (smallest first)':'Avalanche (highest APR first)')")
    
    return js

# --- 工具特定JS ---
OTHER_TOOLS_JS = {
    "tax-estimator": {
        "zh": '''
<script>
document.getElementById('btnCalc').addEventListener('click',function(){
  var income=parseFloat(document.getElementById('income').value)||0;
  var deduction=parseFloat(document.getElementById('deduction').value)||0;
  var special=parseFloat(document.getElementById('special').value)||0;
  var bonus=parseFloat(document.getElementById('bonus').value)||0;
  var threshold=5000;
  var taxable=Math.max(0,income-threshold-deduction-special);
  var tax=0;
  var brackets=[{limit:3000,rate:0.03,qd:0},{limit:12000,rate:0.1,qd:210},{limit:25000,rate:0.2,qd:1410},{limit:35000,rate:0.25,qd:2660},{limit:55000,rate:0.3,qd:4410},{limit:80000,rate:0.35,qd:7160},{limit:1e9,rate:0.45,qd:15160}];
  for(var i=0;i<brackets.length;i++){if(taxable<=brackets[i].limit){tax=Math.max(0,taxable*brackets[i].rate-brackets[i].qd);break;}}
  var bonusTax=0;
  var monthlyBonus=bonus/12;
  for(var i=0;i<brackets.length;i++){if(monthlyBonus<=brackets[i].limit){bonusTax=Math.max(0,bonus*brackets[i].rate-brackets[i].qd);break;}}
  var monthlyTakeHome=income-deduction-special-tax/12;
  var annualTakeHome=income*12+bonus-deduction*12-special*12-tax*12-bonusTax;
  var html='<div class="final">年税后收入 ¥'+annualTakeHome.toFixed(2)+'</div>'+
    '<div class="detail">'+
    '<div class="result-item"><span class="label">月应纳税所得额</span><span class="value">¥'+taxable.toFixed(2)+'</span></div>'+
    '<div class="result-item"><span class="label">月个税</span><span class="value highlight">¥'+(tax/12).toFixed(2)+'</span></div>'+
    '<div class="result-item"><span class="label">月税后收入</span><span class="value">¥'+monthlyTakeHome.toFixed(2)+'</span></div>'+
    '<div class="result-item"><span class="label">年终奖个税</span><span class="value highlight">¥'+bonusTax.toFixed(2)+'</span></div>'+
    '<div class="result-item"><span class="label">年终奖税后</span><span class="value">¥'+(bonus-bonusTax).toFixed(2)+'</span></div>'+
    '<div class="result-item"><span class="label">有效税率</span><span class="value">'+((tax*12+bonusTax)/(income*12+bonus)*100).toFixed(1)+'%</span></div>'+
    '</div>';
  document.getElementById('result').innerHTML=html;
  document.getElementById('result').style.display='block';
});
document.getElementById('btnClear').addEventListener('click',function(){
  document.getElementById('income').value='15000';
  document.getElementById('deduction').value='3000';
  document.getElementById('special').value='2000';
  document.getElementById('bonus').value='30000';
  document.getElementById('result').style.display='none';
});
</script>''',
        "en": '''
<script>
document.getElementById('btnCalc').addEventListener('click',function(){
  var income=parseFloat(document.getElementById('income').value)||0;
  var deduction=parseFloat(document.getElementById('deduction').value)||0;
  var special=parseFloat(document.getElementById('special').value)||0;
  var bonus=parseFloat(document.getElementById('bonus').value)||0;
  var threshold=5000;
  var taxable=Math.max(0,income-threshold-deduction-special);
  var tax=0;
  var brackets=[{limit:3000,rate:0.03,qd:0},{limit:12000,rate:0.1,qd:210},{limit:25000,rate:0.2,qd:1410},{limit:35000,rate:0.25,qd:2660},{limit:55000,rate:0.3,qd:4410},{limit:80000,rate:0.35,qd:7160},{limit:1e9,rate:0.45,qd:15160}];
  for(var i=0;i<brackets.length;i++){if(taxable<=brackets[i].limit){tax=Math.max(0,taxable*brackets[i].rate-brackets[i].qd);break;}}
  var bonusTax=0;
  var monthlyBonus=bonus/12;
  for(var i=0;i<brackets.length;i++){if(monthlyBonus<=brackets[i].limit){bonusTax=Math.max(0,bonus*brackets[i].rate-brackets[i].qd);break;}}
  var monthlyTakeHome=income-deduction-special-tax/12;
  var annualTakeHome=income*12+bonus-deduction*12-special*12-tax*12-bonusTax;
  var html='<div class="final">Annual After-Tax $'+annualTakeHome.toFixed(2)+'</div>'+
    '<div class="detail">'+
    '<div class="result-item"><span class="label">Monthly Taxable Income</span><span class="value">$'+taxable.toFixed(2)+'</span></div>'+
    '<div class="result-item"><span class="label">Monthly Tax</span><span class="value highlight">$'+(tax/12).toFixed(2)+'</span></div>'+
    '<div class="result-item"><span class="label">Monthly Take-home</span><span class="value">$'+monthlyTakeHome.toFixed(2)+'</span></div>'+
    '<div class="result-item"><span class="label">Bonus Tax</span><span class="value highlight">$'+bonusTax.toFixed(2)+'</span></div>'+
    '<div class="result-item"><span class="label">Bonus After-Tax</span><span class="value">$'+(bonus-bonusTax).toFixed(2)+'</span></div>'+
    '<div class="result-item"><span class="label">Effective Tax Rate</span><span class="value">'+((tax*12+bonusTax)/(income*12+bonus)*100).toFixed(1)+'%</span></div>'+
    '</div>';
  document.getElementById('result').innerHTML=html;
  document.getElementById('result').style.display='block';
});
document.getElementById('btnClear').addEventListener('click',function(){
  document.getElementById('income').value='15000';
  document.getElementById('deduction').value='3000';
  document.getElementById('special').value='2000';
  document.getElementById('bonus').value='30000';
  document.getElementById('result').style.display='none';
});
</script>''',
    },
    "hourly-to-salary": {
        "zh": '''
<script>
document.getElementById('btnCalc').addEventListener('click',function(){
  var hourly=parseFloat(document.getElementById('hourly').value)||0;
  var hoursDay=parseFloat(document.getElementById('hoursDay').value)||0;
  var daysWeek=parseFloat(document.getElementById('daysWeek').value)||0;
  var daily=hourly*hoursDay;
  var weekly=daily*daysWeek;
  var monthly=weekly*4.33;
  var annual=weekly*52;
  var html='<div class="final">年薪 ¥'+annual.toFixed(2)+'</div>'+
    '<div class="detail">'+
    '<div class="result-item"><span class="label">时薪</span><span class="value highlight">¥'+hourly.toFixed(2)+'</span></div>'+
    '<div class="result-item"><span class="label">日薪（'+hoursDay+'小时）</span><span class="value">¥'+daily.toFixed(2)+'</span></div>'+
    '<div class="result-item"><span class="label">周薪（'+daysWeek+'天）</span><span class="value">¥'+weekly.toFixed(2)+'</span></div>'+
    '<div class="result-item"><span class="label">月薪（4.33周）</span><span class="value">¥'+monthly.toFixed(2)+'</span></div>'+
    '<div class="result-item"><span class="label">年薪（52周）</span><span class="value highlight">¥'+annual.toFixed(2)+'</span></div>'+
    '</div>';
  document.getElementById('result').innerHTML=html;
  document.getElementById('result').style.display='block';
});
document.getElementById('btnClear').addEventListener('click',function(){
  document.getElementById('hourly').value='50';
  document.getElementById('hoursDay').value='8';
  document.getElementById('daysWeek').value='5';
  document.getElementById('result').style.display='none';
});
</script>''',
        "en": '''
<script>
document.getElementById('btnCalc').addEventListener('click',function(){
  var hourly=parseFloat(document.getElementById('hourly').value)||0;
  var hoursDay=parseFloat(document.getElementById('hoursDay').value)||0;
  var daysWeek=parseFloat(document.getElementById('daysWeek').value)||0;
  var daily=hourly*hoursDay;
  var weekly=daily*daysWeek;
  var monthly=weekly*4.33;
  var annual=weekly*52;
  var html='<div class="final">Annual Salary $'+annual.toFixed(2)+'</div>'+
    '<div class="detail">'+
    '<div class="result-item"><span class="label">Hourly Rate</span><span class="value highlight">$'+hourly.toFixed(2)+'</span></div>'+
    '<div class="result-item"><span class="label">Daily ('+hoursDay+' hours)</span><span class="value">$'+daily.toFixed(2)+'</span></div>'+
    '<div class="result-item"><span class="label">Weekly ('+daysWeek+' days)</span><span class="value">$'+weekly.toFixed(2)+'</span></div>'+
    '<div class="result-item"><span class="label">Monthly (4.33 weeks)</span><span class="value">$'+monthly.toFixed(2)+'</span></div>'+
    '<div class="result-item"><span class="label">Annual (52 weeks)</span><span class="value highlight">$'+annual.toFixed(2)+'</span></div>'+
    '</div>';
  document.getElementById('result').innerHTML=html;
  document.getElementById('result').style.display='block';
});
document.getElementById('btnClear').addEventListener('click',function(){
  document.getElementById('hourly').value='50';
  document.getElementById('hoursDay').value='8';
  document.getElementById('daysWeek').value='5';
  document.getElementById('result').style.display='none';
});
</script>''',
    },
    "cap-rate-calculator": {
        "zh": '''
<script>
document.getElementById('btnCalc').addEventListener('click',function(){
  var noi=parseFloat(document.getElementById('noi').value)||0;
  var value=parseFloat(document.getElementById('value').value)||0;
  var expenses=parseFloat(document.getElementById('expenses').value)||0;
  var gross=noi+expenses;
  var capRate=value>0?(noi/value*100):0;
  var payback=noi>0?(value/noi):0;
  var html='<div class="final">Cap Rate '+capRate.toFixed(2)+'%</div>'+
    '<div class="detail">'+
    '<div class="result-item"><span class="label">年总收入</span><span class="value">¥'+gross.toFixed(2)+'</span></div>'+
    '<div class="result-item"><span class="label">年运营费用</span><span class="value">¥'+expenses.toFixed(2)+'</span></div>'+
    '<div class="result-item"><span class="label">净运营收入 (NOI)</span><span class="value highlight">¥'+noi.toFixed(2)+'</span></div>'+
    '<div class="result-item"><span class="label">资本化率</span><span class="value highlight">'+capRate.toFixed(2)+'%</span></div>'+
    '<div class="result-item"><span class="label">回本年限</span><span class="value">'+(payback>0?payback.toFixed(1):'--')+' 年</span></div>'+
    '</div>';
  document.getElementById('result').innerHTML=html;
  document.getElementById('result').style.display='block';
});
document.getElementById('btnClear').addEventListener('click',function(){
  document.getElementById('noi').value='120000';
  document.getElementById('value').value='2000000';
  document.getElementById('expenses').value='80000';
  document.getElementById('result').style.display='none';
});
</script>''',
        "en": '''
<script>
document.getElementById('btnCalc').addEventListener('click',function(){
  var noi=parseFloat(document.getElementById('noi').value)||0;
  var value=parseFloat(document.getElementById('value').value)||0;
  var expenses=parseFloat(document.getElementById('expenses').value)||0;
  var gross=noi+expenses;
  var capRate=value>0?(noi/value*100):0;
  var payback=noi>0?(value/noi):0;
  var html='<div class="final">Cap Rate '+capRate.toFixed(2)+'%</div>'+
    '<div class="detail">'+
    '<div class="result-item"><span class="label">Gross Annual Income</span><span class="value">$'+gross.toFixed(2)+'</span></div>'+
    '<div class="result-item"><span class="label">Annual Expenses</span><span class="value">$'+expenses.toFixed(2)+'</span></div>'+
    '<div class="result-item"><span class="label">Net Operating Income (NOI)</span><span class="value highlight">$'+noi.toFixed(2)+'</span></div>'+
    '<div class="result-item"><span class="label">Cap Rate</span><span class="value highlight">'+capRate.toFixed(2)+'%</span></div>'+
    '<div class="result-item"><span class="label">Payback Period</span><span class="value">'+(payback>0?payback.toFixed(1):'--')+' years</span></div>'+
    '</div>';
  document.getElementById('result').innerHTML=html;
  document.getElementById('result').style.display='block';
});
document.getElementById('btnClear').addEventListener('click',function(){
  document.getElementById('noi').value='120000';
  document.getElementById('value').value='2000000';
  document.getElementById('expenses').value='80000';
  document.getElementById('result').style.display='none';
});
</script>''',
    },
    "rental-yield": {
        "zh": '''
<script>
document.getElementById('btnCalc').addEventListener('click',function(){
  var price=parseFloat(document.getElementById('price').value)||0;
  var rent=parseFloat(document.getElementById('rent').value)||0;
  var costs=parseFloat(document.getElementById('costs').value)||0;
  var annualRent=rent*12;
  var grossYield=price>0?(annualRent/price*100):0;
  var netIncome=annualRent-costs;
  var netYield=price>0?(netIncome/price*100):0;
  var html='<div class="final">净回报率 '+netYield.toFixed(2)+'%</div>'+
    '<div class="detail">'+
    '<div class="result-item"><span class="label">年租金收入</span><span class="value">¥'+annualRent.toFixed(2)+'</span></div>'+
    '<div class="result-item"><span class="label">年持有成本</span><span class="value">¥'+costs.toFixed(2)+'</span></div>'+
    '<div class="result-item"><span class="label">年净收入</span><span class="value highlight">¥'+netIncome.toFixed(2)+'</span></div>'+
    '<div class="result-item"><span class="label">毛回报率</span><span class="value">'+grossYield.toFixed(2)+'%</span></div>'+
    '<div class="result-item"><span class="label">净回报率</span><span class="value highlight">'+netYield.toFixed(2)+'%</span></div>'+
    '<div class="result-item"><span class="label">月净现金流</span><span class="value">¥'+(netIncome/12).toFixed(2)+'</span></div>'+
    '</div>';
  document.getElementById('result').innerHTML=html;
  document.getElementById('result').style.display='block';
});
document.getElementById('btnClear').addEventListener('click',function(){
  document.getElementById('price').value='2000000';
  document.getElementById('rent').value='6000';
  document.getElementById('costs').value='15000';
  document.getElementById('result').style.display='none';
});
</script>''',
        "en": '''
<script>
document.getElementById('btnCalc').addEventListener('click',function(){
  var price=parseFloat(document.getElementById('price').value)||0;
  var rent=parseFloat(document.getElementById('rent').value)||0;
  var costs=parseFloat(document.getElementById('costs').value)||0;
  var annualRent=rent*12;
  var grossYield=price>0?(annualRent/price*100):0;
  var netIncome=annualRent-costs;
  var netYield=price>0?(netIncome/price*100):0;
  var html='<div class="final">Net Yield '+netYield.toFixed(2)+'%</div>'+
    '<div class="detail">'+
    '<div class="result-item"><span class="label">Annual Rental Income</span><span class="value">$'+annualRent.toFixed(2)+'</span></div>'+
    '<div class="result-item"><span class="label">Annual Holding Costs</span><span class="value">$'+costs.toFixed(2)+'</span></div>'+
    '<div class="result-item"><span class="label">Annual Net Income</span><span class="value highlight">$'+netIncome.toFixed(2)+'</span></div>'+
    '<div class="result-item"><span class="label">Gross Yield</span><span class="value">'+grossYield.toFixed(2)+'%</span></div>'+
    '<div class="result-item"><span class="label">Net Yield</span><span class="value highlight">'+netYield.toFixed(2)+'%</span></div>'+
    '<div class="result-item"><span class="label">Monthly Cash Flow</span><span class="value">$'+(netIncome/12).toFixed(2)+'</span></div>'+
    '</div>';
  document.getElementById('result').innerHTML=html;
  document.getElementById('result').style.display='block';
});
document.getElementById('btnClear').addEventListener('click',function(){
  document.getElementById('price').value='2000000';
  document.getElementById('rent').value='6000';
  document.getElementById('costs').value='15000';
  document.getElementById('result').style.display='none';
});
</script>''',
    },
}

# 其他工具的HTML form字段
OTHER_FORMS = {
    "tax-estimator": {
        "zh": '''
    <div class="row">
      <div class="form-group"><label>月收入（元）</label><input type="number" id="income" value="15000" step="1"></div>
      <div class="form-group"><label>社保公积金扣除（元）</label><input type="number" id="deduction" value="3000" step="1"></div>
    </div>
    <div class="row">
      <div class="form-group"><label>专项附加扣除（元/月）</label><input type="number" id="special" value="2000" step="1"></div>
      <div class="form-group"><label>年终奖（元）</label><input type="number" id="bonus" value="30000" step="1"></div>
    </div>''',
        "en": '''
    <div class="row">
      <div class="form-group"><label>Monthly Income ($)</label><input type="number" id="income" value="15000" step="1"></div>
      <div class="form-group"><label>Social Insurance ($)</label><input type="number" id="deduction" value="3000" step="1"></div>
    </div>
    <div class="row">
      <div class="form-group"><label>Special Deductions ($/mo)</label><input type="number" id="special" value="2000" step="1"></div>
      <div class="form-group"><label>Year-end Bonus ($)</label><input type="number" id="bonus" value="30000" step="1"></div>
    </div>''',
    },
    "hourly-to-salary": {
        "zh": '''
    <div class="row">
      <div class="form-group"><label>时薪（元）</label><input type="number" id="hourly" value="50" step="0.01"></div>
      <div class="form-group"><label>每天工作小时</label><input type="number" id="hoursDay" value="8" step="0.5"></div>
    </div>
    <div class="form-group"><label>每周工作天数</label><input type="number" id="daysWeek" value="5" step="0.5"></div>''',
        "en": '''
    <div class="row">
      <div class="form-group"><label>Hourly Rate ($)</label><input type="number" id="hourly" value="50" step="0.01"></div>
      <div class="form-group"><label>Hours per Day</label><input type="number" id="hoursDay" value="8" step="0.5"></div>
    </div>
    <div class="form-group"><label>Days per Week</label><input type="number" id="daysWeek" value="5" step="0.5"></div>''',
    },
    "cap-rate-calculator": {
        "zh": '''
    <div class="row">
      <div class="form-group"><label>年净运营收入（元）</label><input type="number" id="noi" value="120000" step="1"></div>
      <div class="form-group"><label>房产价值（元）</label><input type="number" id="value" value="2000000" step="1"></div>
    </div>
    <div class="form-group"><label>年运营费用（元）</label><input type="number" id="expenses" value="80000" step="1"></div>''',
        "en": '''
    <div class="row">
      <div class="form-group"><label>Annual NOI ($)</label><input type="number" id="noi" value="120000" step="1"></div>
      <div class="form-group"><label>Property Value ($)</label><input type="number" id="value" value="2000000" step="1"></div>
    </div>
    <div class="form-group"><label>Annual Expenses ($)</label><input type="number" id="expenses" value="80000" step="1"></div>''',
    },
    "rental-yield": {
        "zh": '''
    <div class="row">
      <div class="form-group"><label>购房总价（元）</label><input type="number" id="price" value="2000000" step="1"></div>
      <div class="form-group"><label>月租金收入（元）</label><input type="number" id="rent" value="6000" step="1"></div>
    </div>
    <div class="form-group"><label>年持有成本（元）</label><input type="number" id="costs" value="15000" step="1"></div>''',
        "en": '''
    <div class="row">
      <div class="form-group"><label>Purchase Price ($)</label><input type="number" id="price" value="2000000" step="1"></div>
      <div class="form-group"><label>Monthly Rent ($)</label><input type="number" id="rent" value="6000" step="1"></div>
    </div>
    <div class="form-group"><label>Annual Holding Costs ($)</label><input type="number" id="costs" value="15000" step="1"></div>''',
    },
}

DEBT_DEBTROW_CN = '''
    <div id="debts-container">
      <div class="debt-row" id="debt-row-1">
        <div class="row"><div class="form-group"><label>债务名称</label><input type="text" id="debt1" value="信用卡A"></div><div class="form-group"><label>欠款金额（元）</label><input type="number" id="bal1" value="10000" min="0" step="0.01"></div></div>
        <div class="row"><div class="form-group"><label>年利率 (%)</label><input type="number" id="rate1" value="18" min="0" max="100" step="0.1"></div><div class="form-group"><label>每月最低还款（元）</label><input type="number" id="min1" value="200" min="0" step="0.01"></div></div>
      </div>
    </div>
    <button type="button" class="btn btn-secondary" onclick="addDebtRow()">➕ 添加债务</button>
    <div class="form-group"><label>还款策略</label><select id="method"><option value="snowball">雪球法（先还最小余额）</option><option value="avalanche">雪崩法（先还最高利率）</option></select></div>
    <div class="form-group"><label>额外月还款（元）</label><input type="number" id="extraPayment" value="0" min="0" step="1"></div>'''

DEBT_DEBTROW_EN = '''
    <div id="debts-container">
      <div class="debt-row" id="debt-row-1">
        <div class="row"><div class="form-group"><label>Debt Name</label><input type="text" id="debt1" value="Credit Card A"></div><div class="form-group"><label>Balance ($)</label><input type="number" id="bal1" value="10000" min="0" step="0.01"></div></div>
        <div class="row"><div class="form-group"><label>APR (%)</label><input type="number" id="rate1" value="18" min="0" max="100" step="0.1"></div><div class="form-group"><label>Min Payment ($)</label><input type="number" id="min1" value="200" min="0" step="0.01"></div></div>
      </div>
    </div>
    <button type="button" class="btn btn-secondary" onclick="addDebtRow()">➕ Add Debt</button>
    <div class="form-group"><label>Strategy</label><select id="method"><option value="snowball">Snowball (smallest first)</option><option value="avalanche">Avalanche (highest APR first)</option></select></div>
    <div class="form-group"><label>Extra Monthly Payment ($)</label><input type="number" id="extraPayment" value="0" min="0" step="1"></div>'''

def build_page(tool, lang):
    slug = tool['slug']
    if lang == 'zh':
        name = tool['name_zh']
        desc = tool['desc_zh']
        icon = tool['icon_zh']
        instructions = tool['instructions_zh']
        header_home = '/'
        lang_link = '/en/' + slug + '/'
        lang_label = 'English'
        footer_text = '© 2024 Free ToolBase · 纯前端工具，仅供参考不构成财务建议'
        canonical = 'https://free-toolbase.com/' + slug + '/'
        href_zh = canonical
        href_en = 'https://free-toolbase.com/en/' + slug + '/'
        href_x = canonical
        breadcrumb = gen_breadcrumb_cn(name, slug)
        toast_copy_label = '📋 复制'
        toast_copied_label = '✅ 已复制'
        toast_copy_title = '复制结果'
        button_text = '🧮 计算'
        clear_text = '🗑️ 清空'
    else:
        name = tool['name_en']
        desc = tool['desc_en']
        icon = tool['icon_en']
        instructions = tool['instructions_en']
        header_home = '/en/'
        lang_link = '/' + slug + '/'
        lang_label = '中文'
        footer_text = '© 2024 Free ToolBase · Frontend tool, for reference only, not financial advice'
        canonical = 'https://free-toolbase.com/en/' + slug + '/'
        href_zh = 'https://free-toolbase.com/' + slug + '/'
        href_en = canonical
        href_x = canonical
        breadcrumb = gen_breadcrumb_en(name, slug)
        toast_copy_label = '📋 Copy'
        toast_copied_label = '✅ Copied'
        toast_copy_title = 'Copy result'
        button_text = '🧮 Calculate'
        clear_text = '🗑️ Clear'

    # 构建schema
    schema_app = gen_schema_app(name, desc)

    # 构建head
    head = HEAD_CSS.replace('LANG', 'zh-CN' if lang == 'zh' else 'en')
    head = head.replace('TITLE', name + ' - Free ToolBase')
    head = head.replace('OGTITLE', name + ' - Free ToolBase')
    head = head.replace('DESC', desc)
    head = head.replace('SAPP', schema_app)

    meta = HEAD_META.replace('CANONICAL', canonical)
    meta = meta.replace('HREF_ZH', href_zh)
    meta = meta.replace('HREF_EN', href_en)
    meta = meta.replace('HREF_X', href_x)
    meta = meta.replace('BREADCRUMB', breadcrumb)

    # toast JS
    toast = TOAST_JS.replace('COPY_LABEL', toast_copy_label)
    toast = toast.replace('COPIED_LABEL', toast_copied_label)
    toast = toast.replace('COPY_TITLE', toast_copy_title)

    # 表单
    if tool['special'] == 'debt':
        form_html = DEBT_DEBTROW_CN if lang == 'zh' else DEBT_DEBTROW_EN
        js = localize_js(DEBT_SNOWBALL_JS, lang)
    else:
        form_html = OTHER_FORMS[slug][lang]
        js = OTHER_TOOLS_JS[slug][lang]

    # 组装
    header_html = f'<header><a href="{header_home}">🧰 Free ToolBase</a><div class="lang-switch"><a href="{lang_link}">{lang_label}</a></div></header>'
    
    page = head + meta + header_html + f'''
<main>
  <h1>{icon} {name}</h1>
  <p class="subtitle">{instructions}</p>
  <div class="card">
    {form_html}
    <button class="btn" id="btnCalc">{button_text}</button>
    <button class="btn btn-secondary" id="btnClear">{clear_text}</button>
    <div class="result" id="result" style="display:none"></div>
  </div>
</main>
<ins class="adsbygoogle"
     style="display:block"
     data-ad-client="ca-pub-5998441792679372"
     data-ad-slot="auto"
     data-ad-format="auto"
     data-full-width-responsive="true"></ins>
<script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
<footer>{footer_text}</footer>''' + js + toast + FOOTER

    return page

# 生成所有页面
for tool in TOOLS_DATA:
    slug = tool['slug']
    os.makedirs(slug, exist_ok=True)
    os.makedirs('en/' + slug, exist_ok=True)
    
    cn = build_page(tool, 'zh')
    en = build_page(tool, 'en')
    
    with open(slug + '/index.html', 'w') as f:
        f.write(cn)
    with open('en/' + slug + '/index.html', 'w') as f:
        f.write(en)
    
    print(f'✅ {slug} (CN+EN) generated')

print('\nDone!')
