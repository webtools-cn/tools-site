#!/usr/bin/env python3
"""批量生成5个新工具的中英文版本"""
import os

BASE = '/home/chison/tools-site'

# ====== CSS 共享样式（深色主题，和 tip-calculator 一致） ======
CSS = '''*{box-sizing:border-box;margin:0;padding:0}
body{background:#0f172a;color:#e2e8f0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,"PingFang SC","Microsoft YaHei",sans-serif;line-height:1.6;min-height:100vh}
a{color:#06b6d4;text-decoration:none}
.container{max-width:900px;margin:0 auto;padding:24px 16px}
.header{display:flex;justify-content:space-between;align-items:center;margin-bottom:24px}
.header h1{font-size:1.6rem;color:#f1f5f9}
.lang-switch{display:flex;gap:4px;background:#1e293b;border-radius:8px;padding:4px;border:1px solid rgba(148,163,184,.1)}
.lang-switch a{padding:6px 12px;border-radius:5px;font-size:.85rem;color:#94a3b8}
.lang-switch a.active{background:rgba(6,182,212,.2);color:#22d3ee}
.nav-back{color:#64748b;font-size:.85rem;margin-bottom:16px}
.nav-back a{color:#64748b}
.nav-back a:hover{color:#94a3b8}
.hero{background:#1e293b;border-radius:12px;padding:16px 20px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1)}
.hero p{color:#94a3b8;font-size:.9rem}
.badge{display:inline-block;margin-top:8px;padding:2px 10px;border-radius:4px;background:rgba(6,182,212,.15);color:#22d3ee;font-size:.75rem}
.input-section{background:#1e293b;border-radius:12px;padding:20px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1)}
.input-section h2{font-size:1.1rem;color:#f1f5f9;margin-bottom:12px}
.input-row{display:flex;gap:12px;flex-wrap:wrap;margin-bottom:12px;align-items:flex-end}
.input-group{flex:1;min-width:140px}
.input-group label{display:block;font-size:.85rem;color:#94a3b8;margin-bottom:4px}
.input-group input,.input-group select{width:100%;padding:10px 12px;background:#0f172a;color:#e2e8f0;border:1px solid rgba(148,163,184,.2);border-radius:8px;font-size:.9rem}
.input-group input:focus,.input-group select:focus{outline:none;border-color:rgba(6,182,212,.5)}
.btn-row{display:flex;gap:8px;flex-wrap:wrap;margin-top:12px}
.btn{padding:8px 20px;border:none;border-radius:6px;font-size:.85rem;cursor:pointer;transition:all .2s}
.btn-primary{background:rgba(6,182,212,.2);color:#22d3ee;border:1px solid rgba(6,182,212,.3)}
.btn-primary:hover{background:rgba(6,182,212,.3)}
.btn-secondary{background:rgba(148,163,184,.1);color:#94a3b8;border:1px solid rgba(148,163,184,.2)}
.btn-secondary:hover{background:rgba(148,163,184,.2)}
.result-section{background:#1e293b;border-radius:12px;padding:20px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1);display:none}
.result-section.show{display:block}
.result-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:12px;margin-top:16px}
.result-card{background:#0f172a;border-radius:8px;padding:16px;text-align:center}
.result-card .label{font-size:.75rem;color:#64748b;margin-bottom:4px}
.result-card .value{font-size:1.3rem;color:#f1f5f9;font-weight:600}
.result-card .unit{font-size:.75rem;color:#64748b;margin-top:2px}
.result-card.highlight .value{color:#22d3ee}
.info-section{background:#1e293b;border-radius:12px;padding:20px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1)}
.info-section h2{font-size:1.1rem;color:#f1f5f9;margin-bottom:12px}
.info-section h3{font-size:.95rem;color:#e2e8f0;margin:16px 0 8px}
.info-section p{color:#94a3b8;font-size:.9rem;margin-bottom:8px}
.info-section ul{margin-left:20px;color:#94a3b8;font-size:.9rem}
.info-section li{margin-bottom:6px}
.faq-item{margin-bottom:16px}
.faq-item h3{font-size:.95rem;color:#e2e8f0;margin-bottom:6px}
.faq-item p{color:#94a3b8;font-size:.9rem;line-height:1.7}
.footer{border-top:1px solid rgba(148,163,184,.1);padding:24px 0;margin-top:32px;text-align:center;color:#64748b;font-size:.85rem}
.footer a{color:#64748b;margin:0 8px}
.footer a:hover{color:#94a3b8}
.toast{position:fixed;bottom:20px;left:50%;transform:translateX(-50%);background:#1e293b;color:#22d3ee;padding:10px 24px;border-radius:8px;border:1px solid rgba(6,182,212,.3);font-size:.85rem;z-index:999;opacity:0;transition:opacity .3s}
.toast.show{opacity:1}
.ad-slot{margin:0 auto;text-align:center;max-width:960px}.ad-slot:not(:has(ins[frame])){display:none}.ad-slot:empty{display:none}.ad-slot ins{display:block}.ad-slot.ad-sidebar{max-width:300px}
@media(max-width:600px){.input-row{flex-direction:column;gap:8px}.input-group{min-width:100%}.result-grid{grid-template-columns:repeat(2,1fr)}}
@media(max-width:640px){h1{font-size:1.2rem;word-break:break-word}.header{flex-direction:column;gap:8px}}
</style>'''

# ====== 工具定义 ======
TOOLS = [
    {
        'slug': 'meeting-cost-calculator',
        'cn': {
            'title': '会议成本计算器 - Free ToolBase',
            'og_title': '免费在线会议成本计算器 | Meeting Cost Calculator',
            'desc': '免费在线会议成本计算器，输入参会人数和平均时薪，实时计算会议总成本。帮助企业量化会议开销，提升会议效率，减少无效会议。纯前端本地运算。',
            'h1': '💸 会议成本计算器',
            'hero': '免费在线会议成本计算器，输入参会人数和平均时薪，实时计算会议总成本。帮助企业量化会议开销，提升会议效率，减少无效会议。 | 无需注册 · 数据绝不上传服务器',
            'schema_name': '会议成本计算器',
            'section_title': '会议成本计算',
            'section_desc': '输入参会人数、平均时薪和会议时长，自动计算会议总成本',
        },
        'en': {
            'title': 'Meeting Cost Calculator - Free ToolBase',
            'og_title': 'Free Online Meeting Cost Calculator | Real-time Meeting Cost',
            'desc': 'Free online meeting cost calculator. Input attendee count and hourly rate to instantly calculate total meeting cost. Quantify meeting expenses, boost efficiency. Pure client-side computation.',
            'h1': '💸 Meeting Cost Calculator',
            'hero': 'Free online meeting cost calculator. Input attendee count and hourly rate to instantly calculate total meeting cost. Quantify meeting expenses, boost efficiency. | No sign-up · Data never leaves your device',
            'schema_name': 'Meeting Cost Calculator',
            'section_title': 'Meeting Cost Calculation',
            'section_desc': 'Enter attendee count, average hourly rate, and meeting duration to calculate total meeting cost',
        },
        'inputs_cn': '''
  <div class="input-row">
    <div class="input-group">
      <label>参会人数</label>
      <input type="number" id="attendees" placeholder="如 10" min="1" value="10" oninput="calc()">
    </div>
    <div class="input-group">
      <label>平均时薪 (元/小时)</label>
      <input type="number" id="hourlyRate" placeholder="如 150" min="0" step="0.01" value="150" oninput="calc()">
    </div>
  </div>
  <div class="input-row">
    <div class="input-group">
      <label>会议时长 (分钟)</label>
      <input type="number" id="duration" placeholder="如 60" min="1" value="60" oninput="calc()">
    </div>
  </div>
  <div class="btn-row">
    <button class="btn btn-secondary" onclick="resetCalc()">🔄 重置</button>
    <button class="btn btn-primary" onclick="calc()">⚡ 计算</button>
  </div>''',
        'inputs_en': '''
  <div class="input-row">
    <div class="input-group">
      <label>Number of Attendees</label>
      <input type="number" id="attendees" placeholder="e.g. 10" min="1" value="10" oninput="calc()">
    </div>
    <div class="input-group">
      <label>Average Hourly Rate ($)</label>
      <input type="number" id="hourlyRate" placeholder="e.g. 50" min="0" step="0.01" value="50" oninput="calc()">
    </div>
  </div>
  <div class="input-row">
    <div class="input-group">
      <label>Meeting Duration (minutes)</label>
      <input type="number" id="duration" placeholder="e.g. 60" min="1" value="60" oninput="calc()">
    </div>
  </div>
  <div class="btn-row">
    <button class="btn btn-secondary" onclick="resetCalc()">🔄 Reset</button>
    <button class="btn btn-primary" onclick="calc()">⚡ Calculate</button>
  </div>''',
        'js': '''
function showToast(m){var t=document.getElementById("toast");t.textContent=m;t.classList.add("show");setTimeout(function(){t.classList.remove("show")},2500)}
function fmtMoney(v){if(isNaN(v)||!isFinite(v))return"--";return v.toLocaleString("zh-CN",{style:"currency",currency:"CNY"})}
function fmtMoneyEN(v){if(isNaN(v)||!isFinite(v))return"--";return "$"+v.toFixed(2)}
function makeCard(label,value,highlight){var cls=highlight?"result-card highlight":"result-card";return'<div class="'+cls+'"><div class="label">'+label+'</div><div class="value">'+value+'</div></div>'}
function calc(){
  var att=parseInt(document.getElementById("attendees").value)||0;
  var rate=parseFloat(document.getElementById("hourlyRate").value)||0;
  var dur=parseInt(document.getElementById("duration").value)||0;
  var grid=document.getElementById("resultGrid");
  if(att<=0||rate<=0||dur<=0){grid.innerHTML="";document.getElementById("resultSection").classList.remove("show");return}
  var costPerPerson=rate*dur/60;
  var totalCost=att*costPerPerson;
  var isEN=document.documentElement.lang==="en";
  var f=isEN?fmtMoneyEN:fmtMoney;
  grid.innerHTML=makeCard(isEN?"Attendees":"参会人数",att)+makeCard(isEN?"Hourly Rate":"时薪",f(rate))+makeCard(isEN?"Duration":"会议时长",dur+(isEN?" min":"分钟"))+makeCard(isEN?"Cost Per Person":"每人成本",f(costPerPerson))+makeCard(isEN?"Total Meeting Cost":"会议总成本",f(totalCost),true);
  document.getElementById("resultSection").classList.add("show")
}
function resetCalc(){document.getElementById("attendees").value="10";document.getElementById("hourlyRate").value="150";document.getElementById("duration").value="60";document.getElementById("resultSection").classList.remove("show");calc()}
calc();''',
        'faq_cn': '''
  <div class="faq-item"><h3>会议成本怎么计算的？</h3><p>公式：参会人数 × 时薪 × (会议时长÷60)。例如10人参会，平均时薪150元，开会1小时=10×150×1=1,500元。这还不包括会议准备、会议室等间接成本。</p></div>
  <div class="faq-item"><h3>为什么要计算会议成本？</h3><p>研究表明中层管理者每周花35%时间在会议上，高层更是50%+。量化成本有助于减少无效会议、控制参会人数、缩短会议时长，提升企业运营效率。</p></div>
  <div class="faq-item"><h3>时薪怎么估算？</h3><p>粗略算法：年薪÷2000小时（按每年250个工作日×8小时）。如年薪30万，时薪≈150元。也可以按职级平均值估算：初级100-200元，中级200-400元，高级400-800元。</p></div>''',
        'faq_en': '''
  <div class="faq-item"><h3>How is meeting cost calculated?</h3><p>Formula: Attendees × Hourly Rate × (Duration ÷ 60). Example: 10 people at $50/hr for 1 hour = 10×50×1 = $500. This excludes preparation time and meeting room costs.</p></div>
  <div class="faq-item"><h3>Why calculate meeting costs?</h3><p>Research shows middle managers spend 35% of their week in meetings, and executives 50%+. Quantifying costs helps reduce unnecessary meetings, control attendee count, and shorten duration — boosting organizational efficiency.</p></div>
  <div class="faq-item"><h3>How to estimate hourly rate?</h3><p>Rough formula: Annual salary ÷ 2000 hours (250 working days × 8 hours). E.g. $100K/year ≈ $50/hr. You can also use role-based averages: Junior $25-50/hr, Mid $50-100/hr, Senior $100-200/hr.</p></div>''',
    },
    {
        'slug': 'blood-alcohol-calculator',
        'cn': {
            'title': '血液酒精浓度计算器 - Free ToolBase',
            'og_title': '免费在线血液酒精浓度(BAC)计算器 | Blood Alcohol Calculator',
            'desc': '免费在线血液酒精浓度计算器，根据体重、性别、饮酒量和时间估算BAC值。了解酒精代谢规律，安全驾驶参考。纯前端本地运算，数据不上传。',
            'h1': '🍺 血液酒精浓度(BAC)计算器',
            'hero': '免费在线血液酒精浓度计算器，根据体重、性别、饮酒量和时间估算BAC值。了解酒精代谢规律，安全驾驶参考。 | 无需注册 · 数据绝不上传服务器 · 仅供参考不构成法律建议',
            'schema_name': '血液酒精浓度计算器',
            'section_title': 'BAC计算',
            'section_desc': '输入体重、性别、饮酒类型和数量、饮酒时间，估算血液酒精浓度',
        },
        'en': {
            'title': 'Blood Alcohol Concentration Calculator - Free ToolBase',
            'og_title': 'Free Online BAC Calculator | Blood Alcohol Content Estimator',
            'desc': 'Free online blood alcohol concentration (BAC) calculator. Estimate your BAC based on weight, gender, drinks, and time. Understand alcohol metabolism for safe driving reference. Pure client-side, no data upload.',
            'h1': '🍺 Blood Alcohol Concentration (BAC) Calculator',
            'hero': 'Free online blood alcohol concentration calculator. Estimate your BAC based on weight, gender, drinks, and time. Understand alcohol metabolism for safe driving reference. | No sign-up · Data never leaves your device · Reference only, not legal advice',
            'schema_name': 'Blood Alcohol Concentration Calculator',
            'section_title': 'BAC Calculation',
            'section_desc': 'Enter weight, gender, drink type/quantity, and time since drinking to estimate BAC',
        },
        'inputs_cn': '''
  <div class="input-row">
    <div class="input-group">
      <label>体重 (kg)</label>
      <input type="number" id="weight" placeholder="如 70" min="30" max="200" value="70" oninput="calcBAC()">
    </div>
    <div class="input-group">
      <label>性别</label>
      <select id="gender" onchange="calcBAC()">
        <option value="male">男性</option>
        <option value="female">女性</option>
      </select>
    </div>
  </div>
  <div class="input-row">
    <div class="input-group">
      <label>饮酒类型</label>
      <select id="drinkType" onchange="calcBAC()">
        <option value="beer">啤酒 (5% 酒精, 500ml/罐)</option>
        <option value="wine">红酒 (12% 酒精, 150ml/杯)</option>
        <option value="spirit">白酒/烈酒 (40% 酒精, 45ml/杯)</option>
        <option value="sake">清酒 (15% 酒精, 180ml/杯)</option>
      </select>
    </div>
    <div class="input-group">
      <label>饮酒数量 (杯/罐)</label>
      <input type="number" id="drinks" placeholder="如 3" min="0" step="0.5" value="3" oninput="calcBAC()">
    </div>
  </div>
  <div class="input-row">
    <div class="input-group">
      <label>饮酒时长 (小时)</label>
      <input type="number" id="hours" placeholder="如 2" min="0" step="0.5" value="2" oninput="calcBAC()">
    </div>
  </div>
  <div class="btn-row">
    <button class="btn btn-secondary" onclick="resetBAC()">🔄 重置</button>
    <button class="btn btn-primary" onclick="calcBAC()">⚡ 计算</button>
  </div>''',
        'inputs_en': '''
  <div class="input-row">
    <div class="input-group">
      <label>Weight (kg)</label>
      <input type="number" id="weight" placeholder="e.g. 70" min="30" max="200" value="70" oninput="calcBAC()">
    </div>
    <div class="input-group">
      <label>Gender</label>
      <select id="gender" onchange="calcBAC()">
        <option value="male">Male</option>
        <option value="female">Female</option>
      </select>
    </div>
  </div>
  <div class="input-row">
    <div class="input-group">
      <label>Drink Type</label>
      <select id="drinkType" onchange="calcBAC()">
        <option value="beer">Beer (5% ABV, 500ml/can)</option>
        <option value="wine">Wine (12% ABV, 150ml/glass)</option>
        <option value="spirit">Spirits (40% ABV, 45ml/shot)</option>
        <option value="sake">Sake (15% ABV, 180ml/cup)</option>
      </select>
    </div>
    <div class="input-group">
      <label>Number of Drinks</label>
      <input type="number" id="drinks" placeholder="e.g. 3" min="0" step="0.5" value="3" oninput="calcBAC()">
    </div>
  </div>
  <div class="input-row">
    <div class="input-group">
      <label>Hours Since First Drink</label>
      <input type="number" id="hours" placeholder="e.g. 2" min="0" step="0.5" value="2" oninput="calcBAC()">
    </div>
  </div>
  <div class="btn-row">
    <button class="btn btn-secondary" onclick="resetBAC()">🔄 Reset</button>
    <button class="btn btn-primary" onclick="calcBAC()">⚡ Calculate</button>
  </div>''',
        'js': '''
function showToast(m){var t=document.getElementById("toast");t.textContent=m;t.classList.add("show");setTimeout(function(){t.classList.remove("show")},2500)}
function makeCard(label,value,highlight){var cls=highlight?"result-card highlight":"result-card";return'<div class="'+cls+'"><div class="label">'+label+'</div><div class="value">'+value+'</div></div>'}
function calcBAC(){
  var w=parseFloat(document.getElementById("weight").value)||0;
  var g=document.getElementById("gender").value;
  var dt=document.getElementById("drinkType").value;
  var d=parseFloat(document.getElementById("drinks").value)||0;
  var h=parseFloat(document.getElementById("hours").value)||0;
  var grid=document.getElementById("resultGrid");
  if(w<=0||d<=0){grid.innerHTML="";document.getElementById("resultSection").classList.remove("show");return}
  // 酒精克数计算
  var alcGrams={beer:500*0.05*0.789,wine:150*0.12*0.789,spirit:45*0.40*0.789,sake:180*0.15*0.789};
  var totalAlc=d*alcGrams[dt];
  // Widmark公式: BAC% = (酒精克数/(体重g×分布系数))×100 - 代谢率×小时
  var r=g==="male"?0.68:0.55; // Widmark分布系数
  var bac=(totalAlc/(w*1000*r))*100-0.015*h;
  if(bac<0)bac=0;
  var isEN=document.documentElement.lang==="en";
  // 判断状态
  var status,statusColor;
  if(bac<0.02){status=isEN?"Sober":"清醒";statusColor="#22c55e"}
  else if(bac<0.05){status=isEN?"Mild":"微醺";statusColor="#eab308"}
  else if(bac<0.08){status=isEN?"Impaired":"醉酒";statusColor="#f97316"}
  else if(bac<0.15){status=isEN?"Intoxicated":"重度醉酒";statusColor="#ef4444"}
  else{status=isEN?"Dangerous":"危险";statusColor="#dc2626"}
  var soberTime=bac/0.015;
  grid.innerHTML=makeCard(isEN?"Total Alcohol":"总酒精量",totalAlc.toFixed(1)+"g")+makeCard(isEN?"BAC":"血液酒精浓度",bac.toFixed(3)+"%",true)+makeCard(isEN?"Status":"状态","<span style=\\"color:"+statusColor+"\\">"+status+"</span>")+makeCard(isEN?"Time to Sober":"预计清醒时间",soberTime.toFixed(1)+(isEN?" hours":"小时"));
  document.getElementById("resultSection").classList.add("show")
}
function resetBAC(){document.getElementById("weight").value="70";document.getElementById("gender").value="male";document.getElementById("drinkType").value="beer";document.getElementById("drinks").value="3";document.getElementById("hours").value="2";document.getElementById("resultSection").classList.remove("show");calcBAC()}
calcBAC();''',
        'faq_cn': '''
  <div class="faq-item"><h3>BAC计算准确吗？</h3><p>本计算器使用Widmark公式，是法医学常用的BAC估算方法。但实际BAC受食物摄入、个体代谢差异、肝功能等多种因素影响。结果仅供参考，不能作为是否开车的法律依据。</p></div>
  <div class="faq-item"><h3>中国酒驾标准是多少？</h3><p>中国法律规定：BAC≥20mg/100ml（约0.02%）为饮酒驾驶，BAC≥80mg/100ml（约0.08%）为醉酒驾驶。本计算器显示BAC百分比，0.02%=20mg/100ml。注意各国标准不同。</p></div>
  <div class="faq-item"><h3>多久能醒酒？</h3><p>人体平均每小时代谢约0.015% BAC（约15mg/100ml）。例如BAC 0.06%约需4小时降至0。但个体差异大，喝水、咖啡、运动不能加速酒精代谢，只有时间能醒酒。</p></div>''',
        'faq_en': '''
  <div class="faq-item"><h3>How accurate is the BAC calculation?</h3><p>This calculator uses the Widmark formula, a standard forensic BAC estimation method. Actual BAC varies by food intake, individual metabolism, liver function, etc. Results are for reference only and not legal advice for driving.</p></div>
  <div class="faq-item"><h3>What is the legal BAC limit?</h3><p>Most countries set legal driving limits at 0.05% or 0.08% BAC. The US federal limit is 0.08%. Many European countries use 0.05%. Some countries (e.g. China, Japan) have near-zero tolerance. Always check local laws.</p></div>
  <div class="faq-item"><h3>How long until I'm sober?</h3><p>The body metabolizes alcohol at about 0.015% BAC per hour on average. BAC of 0.06% takes ~4 hours to reach zero. Water, coffee, or exercise cannot speed up alcohol metabolism — only time works.</p></div>''',
    },
    {
        'slug': 'invoice-template',
        'cn': {
            'title': '发票模板生成器 - Free ToolBase',
            'og_title': '免费在线发票模板生成器 | Invoice Template Generator',
            'desc': '免费在线发票模板生成器，快速创建专业发票。自定义公司信息、客户信息、项目明细，一键导出PDF或打印。自由职业者、小微企业必备工具。纯前端处理。',
            'h1': '🧾 发票模板生成器',
            'hero': '免费在线发票模板生成器，快速创建专业发票。自定义公司信息、客户信息、项目明细，一键导出PDF或打印。自由职业者、小微企业必备工具。 | 无需注册 · 数据绝不上传服务器',
            'schema_name': '发票模板生成器',
            'section_title': '发票信息填写',
            'section_desc': '填写公司/客户信息和项目明细，生成可打印的专业发票',
        },
        'en': {
            'title': 'Invoice Template Generator - Free ToolBase',
            'og_title': 'Free Online Invoice Template Generator | Professional Invoice Maker',
            'desc': 'Free online invoice template generator. Quickly create professional invoices with custom company info, client details, and line items. Export as PDF or print. Essential for freelancers and small businesses. Pure client-side.',
            'h1': '🧾 Invoice Template Generator',
            'hero': 'Free online invoice template generator. Quickly create professional invoices with custom company info, client details, and line items. Export as PDF or print. Essential for freelancers and small businesses. | No sign-up · Data never leaves your device',
            'schema_name': 'Invoice Template Generator',
            'section_title': 'Invoice Details',
            'section_desc': 'Fill in company/client info and line items to generate a professional printable invoice',
        },
        'inputs_cn': '''
  <h3 style="color:#f1f5f9;margin-bottom:8px">公司信息</h3>
  <div class="input-row">
    <div class="input-group"><label>公司名称</label><input type="text" id="companyName" placeholder="如 XX科技有限公司" oninput="previewInvoice()"></div>
    <div class="input-group"><label>地址</label><input type="text" id="companyAddr" placeholder="如 北京市朝阳区XX路100号" oninput="previewInvoice()"></div>
  </div>
  <div class="input-row">
    <div class="input-group"><label>电话</label><input type="text" id="companyPhone" placeholder="如 010-12345678" oninput="previewInvoice()"></div>
    <div class="input-group"><label>邮箱</label><input type="email" id="companyEmail" placeholder="如 hello@company.com" oninput="previewInvoice()"></div>
  </div>
  <h3 style="color:#f1f5f9;margin:16px 0 8px">客户信息</h3>
  <div class="input-row">
    <div class="input-group"><label>客户名称</label><input type="text" id="clientName" placeholder="如 XX集团" oninput="previewInvoice()"></div>
    <div class="input-group"><label>客户地址</label><input type="text" id="clientAddr" placeholder="如 上海市浦东新区XX路200号" oninput="previewInvoice()"></div>
  </div>
  <h3 style="color:#f1f5f9;margin:16px 0 8px">发票信息</h3>
  <div class="input-row">
    <div class="input-group"><label>发票编号</label><input type="text" id="invoiceNo" placeholder="如 INV-2024-001" oninput="previewInvoice()"></div>
    <div class="input-group"><label>发票日期</label><input type="date" id="invoiceDate" oninput="previewInvoice()"></div>
    <div class="input-group"><label>到期日</label><input type="date" id="dueDate" oninput="previewInvoice()"></div>
  </div>
  <h3 style="color:#f1f5f9;margin:16px 0 8px">项目明细</h3>
  <div id="itemsContainer">
    <div class="input-row item-row">
      <div class="input-group" style="flex:2"><label>项目描述</label><input type="text" class="item-desc" placeholder="如 网站设计服务" oninput="previewInvoice()"></div>
      <div class="input-group"><label>数量</label><input type="number" class="item-qty" value="1" min="1" oninput="previewInvoice()"></div>
      <div class="input-group"><label>单价</label><input type="number" class="item-price" placeholder="0.00" step="0.01" min="0" oninput="previewInvoice()"></div>
      <div class="input-group" style="max-width:60px;align-self:center"><button class="btn btn-secondary" onclick="removeItem(this)" style="padding:6px 10px;font-size:.75rem">✕</button></div>
    </div>
  </div>
  <div class="btn-row" style="margin-bottom:12px">
    <button class="btn btn-secondary" onclick="addItem()">+ 添加项目</button>
  </div>
  <div class="input-row">
    <div class="input-group"><label>税率 (%)</label><input type="number" id="taxRate" value="0" min="0" step="0.1" oninput="previewInvoice()"></div>
    <div class="input-group"><label>备注</label><input type="text" id="notes" placeholder="如 银行转账 / 支付宝" oninput="previewInvoice()"></div>
  </div>
  <div class="btn-row">
    <button class="btn btn-secondary" onclick="resetInvoice()">🔄 重置</button>
    <button class="btn btn-primary" onclick="printInvoice()">🖨️ 打印发票</button>
  </div>''',
        'inputs_en': '''
  <h3 style="color:#f1f5f9;margin-bottom:8px">Company Info</h3>
  <div class="input-row">
    <div class="input-group"><label>Company Name</label><input type="text" id="companyName" placeholder="e.g. Acme Inc." oninput="previewInvoice()"></div>
    <div class="input-group"><label>Address</label><input type="text" id="companyAddr" placeholder="e.g. 123 Main St, New York, NY" oninput="previewInvoice()"></div>
  </div>
  <div class="input-row">
    <div class="input-group"><label>Phone</label><input type="text" id="companyPhone" placeholder="e.g. +1 555-0123" oninput="previewInvoice()"></div>
    <div class="input-group"><label>Email</label><input type="email" id="companyEmail" placeholder="e.g. hello@company.com" oninput="previewInvoice()"></div>
  </div>
  <h3 style="color:#f1f5f9;margin:16px 0 8px">Client Info</h3>
  <div class="input-row">
    <div class="input-group"><label>Client Name</label><input type="text" id="clientName" placeholder="e.g. Global Corp" oninput="previewInvoice()"></div>
    <div class="input-group"><label>Client Address</label><input type="text" id="clientAddr" placeholder="e.g. 456 Park Ave, Los Angeles, CA" oninput="previewInvoice()"></div>
  </div>
  <h3 style="color:#f1f5f9;margin:16px 0 8px">Invoice Info</h3>
  <div class="input-row">
    <div class="input-group"><label>Invoice #</label><input type="text" id="invoiceNo" placeholder="e.g. INV-2024-001" oninput="previewInvoice()"></div>
    <div class="input-group"><label>Invoice Date</label><input type="date" id="invoiceDate" oninput="previewInvoice()"></div>
    <div class="input-group"><label>Due Date</label><input type="date" id="dueDate" oninput="previewInvoice()"></div>
  </div>
  <h3 style="color:#f1f5f9;margin:16px 0 8px">Line Items</h3>
  <div id="itemsContainer">
    <div class="input-row item-row">
      <div class="input-group" style="flex:2"><label>Description</label><input type="text" class="item-desc" placeholder="e.g. Web Design Service" oninput="previewInvoice()"></div>
      <div class="input-group"><label>Qty</label><input type="number" class="item-qty" value="1" min="1" oninput="previewInvoice()"></div>
      <div class="input-group"><label>Unit Price</label><input type="number" class="item-price" placeholder="0.00" step="0.01" min="0" oninput="previewInvoice()"></div>
      <div class="input-group" style="max-width:60px;align-self:center"><button class="btn btn-secondary" onclick="removeItem(this)" style="padding:6px 10px;font-size:.75rem">✕</button></div>
    </div>
  </div>
  <div class="btn-row" style="margin-bottom:12px">
    <button class="btn btn-secondary" onclick="addItem()">+ Add Item</button>
  </div>
  <div class="input-row">
    <div class="input-group"><label>Tax Rate (%)</label><input type="number" id="taxRate" value="0" min="0" step="0.1" oninput="previewInvoice()"></div>
    <div class="input-group"><label>Notes</label><input type="text" id="notes" placeholder="e.g. Bank Transfer / PayPal" oninput="previewInvoice()"></div>
  </div>
  <div class="btn-row">
    <button class="btn btn-secondary" onclick="resetInvoice()">🔄 Reset</button>
    <button class="btn btn-primary" onclick="printInvoice()">🖨️ Print Invoice</button>
  </div>''',
        'js': '''
function showToast(m){var t=document.getElementById("toast");t.textContent=m;t.classList.add("show");setTimeout(function(){t.classList.remove("show")},2500)}
function addItem(){var c=document.getElementById("itemsContainer");var d=document.createElement("div");d.className="input-row item-row";d.innerHTML='<div class="input-group" style="flex:2"><input type="text" class="item-desc" placeholder="项目描述" oninput="previewInvoice()"></div><div class="input-group"><input type="number" class="item-qty" value="1" min="1" oninput="previewInvoice()"></div><div class="input-group"><input type="number" class="item-price" placeholder="0.00" step="0.01" min="0" oninput="previewInvoice()"></div><div class="input-group" style="max-width:60px;align-self:center"><button class="btn btn-secondary" onclick="removeItem(this)" style="padding:6px 10px;font-size:.75rem">✕</button></div>';c.appendChild(d);previewInvoice()}
function removeItem(btn){var rows=document.querySelectorAll(".item-row");if(rows.length<=1){showToast("至少保留一个项目");return}btn.closest(".item-row").remove();previewInvoice()}
function previewInvoice(){
  var isEN=document.documentElement.lang==="en";
  var company=document.getElementById("companyName").value||(isEN?"Your Company":"您的公司");
  var addr=document.getElementById("companyAddr").value||"";
  var phone=document.getElementById("companyPhone").value||"";
  var email=document.getElementById("companyEmail").value||"";
  var client=document.getElementById("clientName").value||(isEN?"Client Name":"客户名称");
  var cAddr=document.getElementById("clientAddr").value||"";
  var invNo=document.getElementById("invoiceNo").value||"INV-001";
  var invDate=document.getElementById("invoiceDate").value||new Date().toISOString().split("T")[0];
  var dueDate=document.getElementById("dueDate").value||"";
  var taxRate=parseFloat(document.getElementById("taxRate").value)||0;
  var notes=document.getElementById("notes").value||"";
  // 汇总项目
  var rows=document.querySelectorAll(".item-row");
  var items=[],subtotal=0;
  rows.forEach(function(r){
    var desc=r.querySelector(".item-desc").value||(isEN?"Item":"项目");
    var qty=parseFloat(r.querySelector(".item-qty").value)||0;
    var price=parseFloat(r.querySelector(".item-price").value)||0;
    var amt=qty*price;
    items.push({desc:desc,qty:qty,price:price,amt:amt});
    subtotal+=amt;
  });
  var tax=subtotal*taxRate/100;
  var total=subtotal+tax;
  // 渲染预览
  var html='<div style="padding:20px;background:#fff;color:#1e293b;border-radius:8px;font-size:.9rem">';
  html+='<div style="display:flex;justify-content:space-between;margin-bottom:20px"><div><h2 style="color:#1e293b;margin:0">'+company+'</h2><p style="color:#64748b;margin:4px 0">'+addr+'</p><p style="color:#64748b;margin:4px 0">'+phone+' | '+email+'</p></div><div style="text-align:right"><h1 style="color:#4F46E5;margin:0;font-size:1.8rem">'+(isEN?"INVOICE":"发票")+'</h1><p style="color:#64748b;margin:4px 0">'+(isEN?"Invoice #":"编号")+': '+invNo+'</p><p style="color:#64748b;margin:4px 0">'+(isEN?"Date":"日期")+': '+invDate+'</p>'+(dueDate?'<p style="color:#64748b;margin:4px 0">'+(isEN?"Due":"到期")+': '+dueDate+'</p>':'')+'</div></div>';
  html+='<div style="margin-bottom:20px"><h3 style="color:#64748b;margin:0 0 8px;font-size:.85rem">'+(isEN?"Bill To":"客户")+':</h3><p style="margin:0;font-weight:600">'+client+'</p><p style="color:#64748b;margin:4px 0">'+cAddr+'</p></div>';
  html+='<table style="width:100%;border-collapse:collapse;margin-bottom:16px"><thead><tr style="background:#f1f5f9"><th style="padding:10px;text-align:left">'+(isEN?"Description":"项目描述")+'</th><th style="padding:10px;text-align:center">'+(isEN?"Qty":"数量")+'</th><th style="padding:10px;text-align:right">'+(isEN?"Unit Price":"单价")+'</th><th style="padding:10px;text-align:right">'+(isEN?"Amount":"金额")+'</th></tr></thead><tbody>';
  items.forEach(function(it){
    html+='<tr style="border-bottom:1px solid #e2e8f0"><td style="padding:10px">'+it.desc+'</td><td style="padding:10px;text-align:center">'+it.qty+'</td><td style="padding:10px;text-align:right">'+it.price.toFixed(2)+'</td><td style="padding:10px;text-align:right">'+it.amt.toFixed(2)+'</td></tr>';
  });
  html+='</tbody></table>';
  html+='<div style="text-align:right;margin-bottom:16px"><p style="margin:4px 0;color:#64748b">'+(isEN?"Subtotal":"小计")+': '+subtotal.toFixed(2)+'</p>'+(taxRate>0?'<p style="margin:4px 0;color:#64748b">'+(isEN?"Tax":"税额")+' ('+taxRate+'%): '+tax.toFixed(2)+'</p>':'')+'<p style="margin:4px 0;font-size:1.2rem;font-weight:700;color:#4F46E5">'+(isEN?"Total":"总计")+': '+total.toFixed(2)+'</p></div>';
  if(notes)html+='<p style="color:#64748b;font-size:.85rem;border-top:1px solid #e2e8f0;padding-top:12px"><strong>'+(isEN?"Notes":"备注")+':</strong> '+notes+'</p>';
  html+='</div>';
  document.getElementById("previewArea").innerHTML=html;
  document.getElementById("resultSection").classList.add("show")
}
function printInvoice(){window.print()}
function resetInvoice(){
  document.getElementById("companyName").value="";document.getElementById("companyAddr").value="";document.getElementById("companyPhone").value="";document.getElementById("companyEmail").value="";
  document.getElementById("clientName").value="";document.getElementById("clientAddr").value="";
  document.getElementById("invoiceNo").value="";document.getElementById("invoiceDate").value="";document.getElementById("dueDate").value="";
  document.getElementById("taxRate").value="0";document.getElementById("notes").value="";
  var rows=document.querySelectorAll(".item-row");
  rows.forEach(function(r,i){if(i>0)r.remove()});
  var first=document.querySelector(".item-row");
  if(first){first.querySelector(".item-desc").value="";first.querySelector(".item-qty").value="1";first.querySelector(".item-price").value=""}
  document.getElementById("resultSection").classList.remove("show")
}
document.getElementById("invoiceDate").value=new Date().toISOString().split("T")[0];
previewInvoice();''',
        'faq_cn': '''
  <div class="faq-item"><h3>生成的发票有法律效力吗？</h3><p>本工具生成的是发票模板，可打印使用。在中国，正式发票需通过税务局系统开具（增值税发票）。本模板适用于不需要税务系统的小额交易、内部报销凭证或海外invoice场景。</p></div>
  <div class="faq-item"><h3>如何导出为PDF？</h3><p>点击"打印发票"按钮，在打印对话框中选择"另存为PDF"即可。所有浏览器都支持此功能。数据仅在本地处理，不会上传到任何服务器。</p></div>
  <div class="faq-item"><h3>可以自定义货币符号吗？</h3><p>当前版本使用¥符号（人民币）。如需其他货币，可在备注中注明币种。未来版本将支持多币种切换。</p></div>''',
        'faq_en': '''
  <div class="faq-item"><h3>Is the generated invoice legally valid?</h3><p>This tool generates an invoice template suitable for printing. Legal requirements vary by jurisdiction. For official tax invoices, check your local tax authority regulations. This template works well for freelance invoices, internal records, and international billing.</p></div>
  <div class="faq-item"><h3>How to export as PDF?</h3><p>Click "Print Invoice" and select "Save as PDF" in the print dialog. All modern browsers support this. Data is processed locally — nothing is uploaded to any server.</p></div>
  <div class="faq-item"><h3>Can I customize the currency symbol?</h3><p>The current version uses $ by default. Future versions will support multi-currency switching. You can note the currency in the notes field.</p></div>''',
    },
    {
        'slug': 'moon-phase-calendar',
        'cn': {
            'title': '月相日历 - Free ToolBase',
            'og_title': '免费在线月相日历查询 | Moon Phase Calendar',
            'desc': '免费在线月相日历，查看任意日期的月相状态。显示新月、上弦月、满月、下弦月等月相信息，以及月龄和可见度百分比。天文爱好者、摄影爱好者必备工具。',
            'h1': '🌙 月相日历',
            'hero': '免费在线月相日历，查看任意日期的月相状态。显示新月、上弦月、满月、下弦月等月相信息，以及月龄和可见度百分比。天文爱好者、摄影爱好者必备工具。 | 无需注册 · 纯前端运算',
            'schema_name': '月相日历',
            'section_title': '月相查询',
            'section_desc': '选择日期查看当日月相状态、月龄和可见度',
        },
        'en': {
            'title': 'Moon Phase Calendar - Free ToolBase',
            'og_title': 'Free Online Moon Phase Calendar | Lunar Phase Lookup',
            'desc': 'Free online moon phase calendar. Check moon phase for any date — new moon, first quarter, full moon, last quarter. Shows moon age and illumination percentage. Essential for astronomers and photographers.',
            'h1': '🌙 Moon Phase Calendar',
            'hero': 'Free online moon phase calendar. Check moon phase for any date — new moon, first quarter, full moon, last quarter. Shows moon age and illumination percentage. Essential for astronomers and photographers. | No sign-up · Pure client-side computation',
            'schema_name': 'Moon Phase Calendar',
            'section_title': 'Moon Phase Lookup',
            'section_desc': 'Select a date to see the moon phase, age, and illumination',
        },
        'inputs_cn': '''
  <div class="input-row">
    <div class="input-group">
      <label>查询日期</label>
      <input type="date" id="queryDate" onchange="calcMoon()">
    </div>
  </div>
  <div class="btn-row">
    <button class="btn btn-secondary" onclick="setToday()">📅 今天</button>
    <button class="btn btn-secondary" onclick="prevDay()">◀ 前一天</button>
    <button class="btn btn-primary" onclick="nextDay()">后一天 ▶</button>
  </div>''',
        'inputs_en': '''
  <div class="input-row">
    <div class="input-group">
      <label>Query Date</label>
      <input type="date" id="queryDate" onchange="calcMoon()">
    </div>
  </div>
  <div class="btn-row">
    <button class="btn btn-secondary" onclick="setToday()">📅 Today</button>
    <button class="btn btn-secondary" onclick="prevDay()">◀ Previous</button>
    <button class="btn btn-primary" onclick="nextDay()">Next ▶</button>
  </div>''',
        'js': '''
function showToast(m){var t=document.getElementById("toast");t.textContent=m;t.classList.add("show");setTimeout(function(){t.classList.remove("show")},2500)}
// 月相计算 (Conway算法)
function getMoonPhase(date){
  var y=date.getFullYear(),m=date.getMonth()+1,d=date.getDate();
  if(m<3){y--;m+=12}
  var c=365.25*y;
  var e=30.6*(m+1);
  var jd=c+e+d-694039.09; // 儒略日偏移
  jd/=29.5305882; // 朔望月周期
  var phase=jd-Math.floor(jd); // 0~1
  return phase;
}
function phaseInfo(phase){
  var isEN=document.documentElement.lang==="en";
  // phase: 0=新月, 0.25=上弦, 0.5=满月, 0.75=下弦
  var names=[
    {cn:"🌑 新月",en:"🌑 New Moon",emoji:"🌑"},
    {cn:"🌒 蛾眉月",en:"🌒 Waxing Crescent",emoji:"🌒"},
    {cn:"🌓 上弦月",en:"🌓 First Quarter",emoji:"🌓"},
    {cn:"🌔 盈凸月",en:"🌔 Waxing Gibbous",emoji:"🌔"},
    {cn:"🌕 满月",en:"🌕 Full Moon",emoji:"🌕"},
    {cn:"🌖 亏凸月",en:"🌖 Waning Gibbous",emoji:"🌖"},
    {cn:"🌗 下弦月",en:"🌗 Last Quarter",emoji:"🌗"},
    {cn:"🌘 残月",en:"🌘 Waning Crescent",emoji:"🌘"}
  ];
  var idx=Math.floor(phase*8)%8;
  var info=names[idx];
  // 可见度：0和0.5时最小，0.25和0.75时约50%
  var illum=Math.abs(phase-0.5)*2; // 0~1, 0=满月, 1=新月
  var pct=Math.round((1-illum)*100);
  var age=Math.round(phase*29.53*10)/10;
  return {name:isEN?info.en:info.cn,emoji:info.emoji,illum:pct,age:age,phase:phase};
}
function makeCard(label,value,highlight){var cls=highlight?"result-card highlight":"result-card";return'<div class="'+cls+'"><div class="label">'+label+'</div><div class="value">'+value+'</div></div>'}
function calcMoon(){
  var dStr=document.getElementById("queryDate").value;
  if(!dStr)return;
  var date=new Date(dStr+"T12:00:00");
  var phase=getMoonPhase(date);
  var info=phaseInfo(phase);
  var isEN=document.documentElement.lang==="en";
  var grid=document.getElementById("resultGrid");
  grid.innerHTML=makeCard(isEN?"Moon Phase":"月相","<span style=\\"font-size:2rem\\">"+info.emoji+"</span><br>"+info.name,true)+makeCard(isEN?"Illumination":"可见度",info.illum+"%")+makeCard(isEN?"Moon Age":"月龄",info.age+(isEN?" days":"天"))+makeCard(isEN?"Phase":"相位值",(info.phase*100).toFixed(1)+"%");
  document.getElementById("resultSection").classList.add("show")
}
function setToday(){
  var d=new Date().toISOString().split("T")[0];
  document.getElementById("queryDate").value=d;calcMoon();
}
function prevDay(){
  var d=document.getElementById("queryDate").value;
  if(!d){setToday();return}
  var dt=new Date(d+"T12:00:00");dt.setDate(dt.getDate()-1);
  document.getElementById("queryDate").value=dt.toISOString().split("T")[0];calcMoon();
}
function nextDay(){
  var d=document.getElementById("queryDate").value;
  if(!d){setToday();return}
  var dt=new Date(d+"T12:00:00");dt.setDate(dt.getDate()+1);
  document.getElementById("queryDate").value=dt.toISOString().split("T")[0];calcMoon();
}
setToday();''',
        'faq_cn': '''
  <div class="faq-item"><h3>月相计算准确吗？</h3><p>使用Conway天文算法，基于朔望月周期29.53天计算。日常使用精度足够（误差<1天）。如需天文级精度（如日食月食预测），请使用专业天文软件。</p></div>
  <div class="faq-item"><h3>月相影响什么？</h3><p>月相影响潮汐、夜间亮度。许多文化中月相与农业（播种收割）、渔业、传统节日相关。满月夜适合夜间摄影，新月夜适合观星。</p></div>
  <div class="faq-item"><h3>如何查看任意年份的月相？</h3><p>点击日期选择器，可以前后翻月翻年，或点击"前一天/后一天"逐日查看。算法支持公元前后任意日期。</p></div>''',
        'faq_en': '''
  <div class="faq-item"><h3>How accurate is the moon phase calculation?</h3><p>Uses the Conway astronomical algorithm based on the 29.53-day synodic month. Sufficient for daily use (error <1 day). For astronomical-grade precision (eclipse prediction), use professional software.</p></div>
  <div class="faq-item"><h3>What does the moon phase affect?</h3><p>Moon phases affect tides and nighttime brightness. Many cultures link moon phases to agriculture (planting/harvesting), fishing, and traditional festivals. Full moon nights are great for photography; new moon nights for stargazing.</p></div>
  <div class="faq-item"><h3>How to check moon phases for any year?</h3><p>Use the date picker to navigate months and years, or click Previous/Next to browse day by day. The algorithm supports any date.</p></div>''',
    },
    {
        'slug': 'amortization-schedule',
        'cn': {
            'title': '分期还款计划表 - Free ToolBase',
            'og_title': '免费在线分期还款计划表 | Amortization Schedule Calculator',
            'desc': '免费在线分期还款计算器，输入贷款金额、年利率和期限，自动生成详细还款计划表。支持等额本息和等额本金两种方式。房贷、车贷必备工具。纯前端运算。',
            'h1': '📊 分期还款计划表',
            'hero': '免费在线分期还款计算器，输入贷款金额、年利率和期限，自动生成详细还款计划表。支持等额本息和等额本金两种方式。房贷、车贷必备工具。 | 无需注册 · 数据绝不上传服务器',
            'schema_name': '分期还款计划表',
            'section_title': '还款计算',
            'section_desc': '输入贷款金额、年利率和期限，查看详细还款计划',
        },
        'en': {
            'title': 'Amortization Schedule Calculator - Free ToolBase',
            'og_title': 'Free Online Amortization Schedule Calculator | Loan Repayment Table',
            'desc': 'Free online amortization schedule calculator. Enter loan amount, annual interest rate, and term to generate a detailed repayment schedule. Supports equal installment and equal principal methods. Essential for mortgage and auto loans.',
            'h1': '📊 Amortization Schedule Calculator',
            'hero': 'Free online amortization schedule calculator. Enter loan amount, annual interest rate, and term to generate a detailed repayment schedule. Supports equal installment and equal principal methods. Essential for mortgage and auto loans. | No sign-up · Data never leaves your device',
            'schema_name': 'Amortization Schedule Calculator',
            'section_title': 'Loan Calculation',
            'section_desc': 'Enter loan amount, annual rate, and term to view the detailed repayment schedule',
        },
        'inputs_cn': '''
  <div class="input-row">
    <div class="input-group">
      <label>贷款金额 (元)</label>
      <input type="number" id="loanAmount" placeholder="如 1000000" min="0" step="0.01" value="1000000" oninput="calcAmort()">
    </div>
    <div class="input-group">
      <label>年利率 (%)</label>
      <input type="number" id="annualRate" placeholder="如 4.5" min="0" step="0.01" value="4.5" oninput="calcAmort()">
    </div>
  </div>
  <div class="input-row">
    <div class="input-group">
      <label>贷款期限 (年)</label>
      <input type="number" id="loanYears" placeholder="如 30" min="1" max="50" value="30" oninput="calcAmort()">
    </div>
    <div class="input-group">
      <label>还款方式</label>
      <select id="repayType" onchange="calcAmort()">
        <option value="equal">等额本息</option>
        <option value="principal">等额本金</option>
      </select>
    </div>
  </div>
  <div class="btn-row">
    <button class="btn btn-secondary" onclick="resetAmort()">🔄 重置</button>
    <button class="btn btn-primary" onclick="calcAmort()">⚡ 计算</button>
  </div>''',
        'inputs_en': '''
  <div class="input-row">
    <div class="input-group">
      <label>Loan Amount ($)</label>
      <input type="number" id="loanAmount" placeholder="e.g. 300000" min="0" step="0.01" value="300000" oninput="calcAmort()">
    </div>
    <div class="input-group">
      <label>Annual Interest Rate (%)</label>
      <input type="number" id="annualRate" placeholder="e.g. 4.5" min="0" step="0.01" value="4.5" oninput="calcAmort()">
    </div>
  </div>
  <div class="input-row">
    <div class="input-group">
      <label>Loan Term (years)</label>
      <input type="number" id="loanYears" placeholder="e.g. 30" min="1" max="50" value="30" oninput="calcAmort()">
    </div>
    <div class="input-group">
      <label>Repayment Method</label>
      <select id="repayType" onchange="calcAmort()">
        <option value="equal">Equal Installment</option>
        <option value="principal">Equal Principal</option>
      </select>
    </div>
  </div>
  <div class="btn-row">
    <button class="btn btn-secondary" onclick="resetAmort()">🔄 Reset</button>
    <button class="btn btn-primary" onclick="calcAmort()">⚡ Calculate</button>
  </div>''',
        'js': '''
function showToast(m){var t=document.getElementById("toast");t.textContent=m;t.classList.add("show");setTimeout(function(){t.classList.remove("show")},2500)}
function fmtMoney(v){if(isNaN(v)||!isFinite(v))return"--";return v.toLocaleString("zh-CN",{minimumFractionDigits:2,maximumFractionDigits:2})}
function fmtMoneyEN(v){if(isNaN(v)||!isFinite(v))return"--";return v.toLocaleString("en-US",{minimumFractionDigits:2,maximumFractionDigits:2})}
function makeCard(label,value,highlight){var cls=highlight?"result-card highlight":"result-card";return'<div class="'+cls+'"><div class="label">'+label+'</div><div class="value">'+value+'</div></div>'}
function calcAmort(){
  var P=parseFloat(document.getElementById("loanAmount").value)||0;
  var r=parseFloat(document.getElementById("annualRate").value)||0;
  var years=parseInt(document.getElementById("loanYears").value)||0;
  var type=document.getElementById("repayType").value;
  var isEN=document.documentElement.lang==="en";
  var f=isEN?fmtMoneyEN:fmtMoney;
  var grid=document.getElementById("resultGrid");
  if(P<=0||years<=0){grid.innerHTML="";document.getElementById("resultSection").classList.remove("show");document.getElementById("scheduleTable").innerHTML="";return}
  var n=years*12;
  var mr=r/100/12; // 月利率
  var totalPayment=0,totalInterest=0;
  var schedule=[];
  if(type==="equal"){
    // 等额本息
    var monthly=P*mr*Math.pow(1+mr,n)/(Math.pow(1+mr,n)-1);
    var balance=P;
    for(var i=1;i<=n&&i<=360;i++){
      var interest=balance*mr;
      var principal=monthly-interest;
      balance-=principal;
      if(balance<0)balance=0;
      schedule.push({period:i,payment:monthly,principal:principal,interest:interest,balance:balance});
      totalPayment+=monthly;totalInterest+=interest;
    }
  }else{
    // 等额本金
    var monthlyPrincipal=P/n;
    var balance=P;
    for(var i=1;i<=n&&i<=360;i++){
      var interest=balance*mr;
      var monthly=monthlyPrincipal+interest;
      balance-=monthlyPrincipal;
      if(balance<0)balance=0;
      schedule.push({period:i,payment:monthly,principal:monthlyPrincipal,interest:interest,balance:balance});
      totalPayment+=monthly;totalInterest+=interest;
    }
  }
  grid.innerHTML=makeCard(isEN?"Monthly Payment":"月供",f(type==="equal"?schedule[0].payment:schedule[0].payment)+"~"+f(schedule[schedule.length-1].payment),true)+makeCard(isEN?"Total Payment":"还款总额",f(totalPayment))+makeCard(isEN?"Total Interest":"利息总额",f(totalInterest))+makeCard(isEN?"Total Periods":"总期数",n+(isEN?" months":"个月"));
  // 生成表格（前24期+最后1期）
  var tableHtml='<div style="overflow-x:auto"><table style="width:100%;border-collapse:collapse;font-size:.8rem;margin-top:12px"><thead><tr style="background:rgba(6,182,212,.1)"><th style="padding:8px;color:#22d3ee;text-align:center">'+(isEN?"#":"期数")+'</th><th style="padding:8px;color:#22d3ee;text-align:right">'+(isEN?"Payment":"月供")+'</th><th style="padding:8px;color:#22d3ee;text-align:right">'+(isEN?"Principal":"本金")+'</th><th style="padding:8px;color:#22d3ee;text-align:right">'+(isEN?"Interest":"利息")+'</th><th style="padding:8px;color:#22d3ee;text-align:right">'+(isEN?"Balance":"剩余")+'</th></tr></thead><tbody>';
  var show=schedule.slice(0,24);
  if(schedule.length>24){
    show.push(null); // 省略号
    show.push(schedule[schedule.length-1]);
  }
  show.forEach(function(s){
    if(s===null){tableHtml+='<tr><td colspan="5" style="text-align:center;color:#64748b;padding:8px">...</td></tr>';return}
    tableHtml+='<tr style="border-bottom:1px solid rgba(148,163,184,.1)"><td style="padding:8px;text-align:center;color:#94a3b8">'+s.period+'</td><td style="padding:8px;text-align:right">'+f(s.payment)+'</td><td style="padding:8px;text-align:right">'+f(s.principal)+'</td><td style="padding:8px;text-align:right;color:#f97316">'+f(s.interest)+'</td><td style="padding:8px;text-align:right;color:#94a3b8">'+f(s.balance)+'</td></tr>';
  });
  tableHtml+='</tbody></table></div>';
  document.getElementById("scheduleTable").innerHTML=tableHtml;
  document.getElementById("resultSection").classList.add("show")
}
function resetAmort(){document.getElementById("loanAmount").value="1000000";document.getElementById("annualRate").value="4.5";document.getElementById("loanYears").value="30";document.getElementById("repayType").value="equal";document.getElementById("resultSection").classList.remove("show");document.getElementById("scheduleTable").innerHTML="";calcAmort()}
calcAmort();''',
        'faq_cn': '''
  <div class="faq-item"><h3>等额本息和等额本金有什么区别？</h3><p>等额本息：每月还款额固定，前期利息占比高，后期本金占比高。总利息较多但月供压力均匀。等额本金：每月还本金固定，利息逐月递减，月供前期高后期低。总利息较少但前期压力大。</p></div>
  <div class="faq-item"><h3>提前还款划算吗？</h3><p>等额本息方式下，前期利息占比大，提前还款能省较多利息。等额本金方式下，利息已逐月递减，提前还款节省有限。建议在贷款前期（前1/3期限）提前还款性价比最高。</p></div>
  <div class="faq-item"><h3>计算结果含其他费用吗？</h3><p>本计算器仅计算本金和利息，不含贷款服务费、保险费、评估费等其他费用。实际月供可能略高于计算结果。请以银行最终审批结果为准。</p></div>''',
        'faq_en': '''
  <div class="faq-item"><h3>What's the difference between equal installment and equal principal?</h3><p>Equal Installment: Fixed monthly payment, higher interest portion early on. Total interest is higher but cash flow is predictable. Equal Principal: Fixed principal payment each month, decreasing interest. Lower total interest but higher initial payments.</p></div>
  <div class="faq-item"><h3>Is early repayment worth it?</h3><p>Under equal installment, early repayment saves more interest since interest is front-loaded. Under equal principal, savings are smaller since interest decreases over time. Early repayment in the first 1/3 of the term gives the best ROI.</p></div>
  <div class="faq-item"><h3>Does the calculation include other fees?</h3><p>This calculator only computes principal and interest. It excludes origination fees, insurance, appraisal, and other charges. Actual monthly payments may be slightly higher. Refer to your bank's final approval.</p></div>''',
    },
]

# ====== 模板函数 ======
def build_page(tool, lang):
    """构建完整HTML页面"""
    is_cn = (lang == 'cn')
    data = tool['cn'] if is_cn else tool['en']
    inputs = tool['inputs_cn'] if is_cn else tool['inputs_en']
    faq = tool['faq_cn'] if is_cn else tool['faq_en']
    slug = tool['slug']
    
    en_path = f'../en/{slug}/' if is_cn else f'../../en/{slug}/'
    cn_path = f'../../{slug}/' if not is_cn else 'index.html'
    home = '../index.html' if is_cn else '../../index.html'
    home_tools = '../index.html#tools' if is_cn else '../../index.html#tools'
    
    lang_attr = 'zh-CN' if is_cn else 'en'
    hreflang_zh = f'https://free-toolbase.com/{slug}/' if is_cn else f'https://free-toolbase.com/{slug}/'
    hreflang_en = f'https://free-toolbase.com/en/{slug}/'
    canonical = f'https://free-toolbase.com/{slug}/' if is_cn else f'https://free-toolbase.com/en/{slug}/'
    
    # 根据语言决定某些JS细节
    lang_check = '' if is_cn else ' document.documentElement.lang="en";'
    
    # resultSection后插入schedule table（仅amortization）
    schedule_div = ''
    if slug == 'amortization-schedule':
        schedule_div = '\n<div id="scheduleTable" style="background:#1e293b;border-radius:12px;padding:20px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1)"></div>\n'
    
    # 发票预览区
    preview_div = ''
    if slug == 'invoice-template':
        preview_div = '\n<div id="previewArea" style="background:#1e293b;border-radius:12px;padding:20px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1)"></div>\n'
    
    page = f'''<!DOCTYPE html>
<html lang="{lang_attr}">
<head>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-9W1157EBQV"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-9W1157EBQV');</script>
<script>window.addEventListener("error",function(e){{if(e&&e.message===""){{e.preventDefault();}}}});window.addEventListener("unhandledrejection",function(e){{if(e&&e.reason&&e.reason.message===""){{e.preventDefault();}}}});</script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="{data['desc']}">
<title>{data['title']}</title>
<link rel="canonical" href="{canonical}">
<meta property="og:title" content="{data['og_title']}">
<meta property="og:description" content="{data['desc']}">
<meta property="og:url" content="{canonical}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Free ToolBase">
<link rel="alternate" hreflang="zh" href="https://free-toolbase.com/{slug}/">
<link rel="alternate" hreflang="en" href="https://free-toolbase.com/en/{slug}/">
<link rel="alternate" hreflang="x-default" href="https://free-toolbase.com/en/{slug}/">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"SoftwareApplication","name":"{data['schema_name']}","description":"{data['desc']}","applicationCategory":"UtilitiesApplication","operatingSystem":"Web","publisher":{{"@type":"Organization","name":"Free ToolBase","email":"dexshuang@google.com"}},"offers":{{"@type":"Offer","price":"0","priceCurrency":"USD"}}}}</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"{'首页' if is_cn else 'Home'}","item":"https://free-toolbase.com/"}},{{"@type":"ListItem","position":2,"name":"{'工具' if is_cn else 'Tools'}","item":"https://free-toolbase.com/#tools"}},{{"@type":"ListItem","position":3,"name":"{data['schema_name']}","item":"{canonical}"}}]}}</script>
<style>
{CSS}
</head>
<body>
<div class="container">
<div class="header"><h1>{data['h1']}</h1><div class="lang-switch"><a href="{'index.html' if is_cn else cn_path}" class="{'active' if is_cn else ''}">{'中文' if is_cn else '中文'}</a><a href="{'../en/'+slug+'/' if is_cn else 'index.html'}" class="{'' if is_cn else 'active'}">EN</a></div></div>
<p class="nav-back"><a href="{home}">{'首页' if is_cn else 'Home'}</a> &rsaquo; <a href="{home_tools}">{'工具' if is_cn else 'Tools'}</a> &rsaquo; {data['schema_name']}</p>
<div class="hero"><p>{data['hero']}</p><span class="badge">{'零依赖·可离线使用' if is_cn else 'Zero Dependencies · Works Offline'}</span></div>

<div class="input-section" id="input">
  <h2>{data['section_title']}</h2>
  <p style="color:#94a3b8;font-size:.85rem;margin-bottom:12px">{data['section_desc']}</p>
{inputs}
</div>

{preview_div}
{schedule_div}
<div class="result-section" id="resultSection">
  <h2 style="text-align:center;color:#f1f5f9;margin-bottom:12px">{'计算结果' if is_cn else 'Results'}</h2>
  <div class="result-grid" id="resultGrid"></div>
</div>

<div class="info-section">
  <h2>{'使用教程' if is_cn else 'How to Use'}</h2>
  <p>{data['section_desc']}</p>
</div>

<div class="info-section">
  <h2>{'常见问题 FAQ' if is_cn else 'FAQ'}</h2>
{faq}
</div>
</div>

<div class="footer container">
<div style="margin-bottom:12px">
<a href="{home}">{'首页' if is_cn else 'Home'}</a>
<a href="{home_tools}">{'全部工具' if is_cn else 'All Tools'}</a>
<a href="mailto:dexshuang@google.com">{'联系我们' if is_cn else 'Contact'}</a>
<a href="../privacy/">{'隐私政策' if is_cn else 'Privacy'}</a>
<a href="../terms/">{'服务条款' if is_cn else 'Terms'}</a>
<a href="{'../en/'+slug+'/' if is_cn else cn_path}">EN</a>
</div>
<p>{data['schema_name']} | {'无需注册 · 数据绝不上传服务器' if is_cn else 'No sign-up · Data never leaves your device'}</p>
<p style="margin-top:8px;color:#475569;font-size:.8rem">{'问题反馈' if is_cn else 'Feedback'}: dexshuang@google.com</p>
</div>
<div class="toast" id="toast"></div>
<script>{lang_check}
{tool['js']}
</script>
</body>
</html>'''
    return page


# ====== 生成文件 ======
for tool in TOOLS:
    slug = tool['slug']
    
    # CN
    cn_path = os.path.join(BASE, slug, 'index.html')
    cn_html = build_page(tool, 'cn')
    with open(cn_path, 'w', encoding='utf-8') as f:
        f.write(cn_html)
    print(f'✅ CN: {slug}/index.html')
    
    # EN
    en_path = os.path.join(BASE, 'en', slug, 'index.html')
    en_html = build_page(tool, 'en')
    with open(en_path, 'w', encoding='utf-8') as f:
        f.write(en_html)
    print(f'✅ EN: en/{slug}/index.html')

print(f'\n🎉 共生成 {len(TOOLS)*2} 个文件')