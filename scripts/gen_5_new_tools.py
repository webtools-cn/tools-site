#!/usr/bin/env python3
"""批量生成5个新金融/健康工具"""
import os

BASE = "/home/chison/tools-site"

tools = {
    "cd-ladder-calculator-detailed": {
        "cn": {
            "title": "免费在线CD阶梯计算器（详细版）",
            "short": "CD阶梯计算器",
            "desc": "免费在线CD阶梯（Certificate of Deposit Ladder）详细计算器，输入投资总额、CD期限分布和利率，自动计算各阶梯收益和到期滚动策略。纯前端本地计算，无需注册。",
            "faq_title": "什么是CD阶梯策略？",
            "faq_answer": "CD阶梯（CD Ladder）是将资金分散投资于不同期限的定期存款，每隔一段时间就有CD到期，兼顾流动性和收益率。例如将$10,000分成5份分别投资1/2/3/4/5年期CD，每年都有CD到期可续投或取出。",
            "hero_desc": "免费在线CD阶梯（Certificate of Deposit Ladder）详细计算器，输入投资总额、CD期限分布和利率，自动计算各阶梯收益和到期滚动策略。纯前端本地计算。",
            "calc_label": "输入投资总额、利率和期限分布，计算CD阶梯收益",
            "input1_label": "投资总额 ($)：",
            "input1_id": "totalAmount",
            "input1_val": "25000",
            "input2_label": "阶梯层数：",
            "input2_id": "rungs",
            "input2_val": "5",
            "result_label": "总收益",
            "formula": "各阶梯利息之和",
            "calc_js": """
var total=parseFloat(document.getElementById('totalAmount').value)||0;
var rungs=parseInt(document.getElementById('rungs').value)||5;
var rates=document.getElementById('rates').value.trim();
var rateList=[];
if(rates){
  var parts=rates.split(/[,\\n ]+/);
  for(var i=0;i<parts.length;i++){var v=parseFloat(parts[i]);if(!isNaN(v))rateList.push(v);}
}
while(rateList.length<rungs){rateList.push(3.5+rateList.length*0.3);}
var perRung=total/rungs;
var totalInterest=0;
var details='';
for(var i=0;i<rungs;i++){
  var years=i+1;
  var rate=rateList[i];
  var interest=perRung*(rate/100)*years;
  totalInterest+=interest;
  details+='<tr><td>阶梯'+(i+1)+'</td><td>'+years+'年</td><td>$'+perRung.toFixed(2)+'</td><td>'+rate.toFixed(2)+'%</td><td>$'+interest.toFixed(2)+'</td><td>$'+(perRung+interest).toFixed(2)+'</td></tr>';
}
document.getElementById('val1').textContent='$'+totalInterest.toFixed(2);
document.getElementById('val2').textContent='$'+(total+totalInterest).toFixed(2);
document.getElementById('val3').textContent=(totalInterest/total*100).toFixed(2)+'%';
document.getElementById('val4').textContent='$'+perRung.toFixed(2);
document.getElementById('detailTable').innerHTML=details;
""",
            "extra_input": '<div class="form-row"><label>各阶梯利率 (%)：</label><textarea id="rates" placeholder="每行一个利率，对应1年/2年/3年...如：&#10;4.0&#10;4.3&#10;4.5&#10;4.7&#10;5.0" rows="4"></textarea></div>',
            "extra_labels": {"label2": "到期总金额", "label3": "总收益率", "label4": "每层金额"},
            "info_html": '<h3>💰 CD阶梯策略</h3><p>CD阶梯是将资金分散投资于不同期限定期存款的策略。例如将$25,000分成5份，分别投资1-5年期CD，每年到期后滚动续投最长期限。</p><h3>📊 使用说明</h3><p>输入总投资额和阶梯层数（通常3-5层），然后输入各期限对应的年利率。计算器会显示每层收益和到期滚动计划。</p><h3>📋 阶梯明细</h3><div style="overflow-x:auto;margin-top:8px"><table style="width:100%;border-collapse:collapse;font-size:.85rem"><thead><tr style="color:#94a3b8"><th>阶梯</th><th>期限</th><th>本金</th><th>利率</th><th>利息</th><th>到期金额</th></tr></thead><tbody id="detailTable"></tbody></table></div>'
        },
        "en": {
            "title": "Free Online CD Ladder Calculator (Detailed)",
            "short": "CD Ladder Calculator",
            "desc": "Free online CD Ladder detailed calculator. Enter total investment, CD term distribution, and interest rates to calculate each rung return and maturity rollover strategy. Pure frontend computation.",
            "faq_title": "What is a CD Ladder Strategy?",
            "faq_answer": "A CD Ladder spreads funds across CDs with different maturities. Each rung matures at a different time, providing both liquidity and higher yields. E.g., split $10,000 into 5 CDs of 1/2/3/4/5 years — each year one matures for reinvestment or withdrawal.",
            "hero_desc": "Free online CD Ladder detailed calculator. Enter total investment, CD term distribution, and interest rates to calculate each rung return and maturity rollover strategy. Pure frontend computation.",
            "calc_label": "Enter investment amount, rates and term distribution to calculate CD ladder returns",
            "input1_label": "Total Investment ($):",
            "input1_val": "25000",
            "input2_label": "Number of Rungs:",
            "input2_val": "5",
            "result_label": "Total Interest",
            "formula": "Sum of all rung interests",
            "extra_input": '<div class="form-row"><label>Interest Rates per Rung (%):</label><textarea id="rates" placeholder="One rate per line, corresponding to 1yr/2yr/3yr... e.g.:&#10;4.0&#10;4.3&#10;4.5&#10;4.7&#10;5.0" rows="4"></textarea></div>',
            "extra_labels": {"label2": "Total at Maturity", "label3": "Total Yield", "label4": "Per Rung Amount"},
            "info_html": '<h3>💰 CD Ladder Strategy</h3><p>A CD ladder spreads funds across CDs with different maturities. E.g., split $25,000 into 5 CDs of 1-5 years — each year one matures and rolls into a new long-term CD.</p><h3>📊 How to Use</h3><p>Enter the total investment, number of rungs (usually 3-5), and annual rates for each term. The calculator shows per-rung returns and rollover planning.</p><h3>📋 Ladder Details</h3><div style="overflow-x:auto;margin-top:8px"><table style="width:100%;border-collapse:collapse;font-size:.85rem"><thead><tr style="color:#94a3b8"><th>Rung</th><th>Term</th><th>Principal</th><th>Rate</th><th>Interest</th><th>Maturity</th></tr></thead><tbody id="detailTable"></tbody></table></div>'
        }
    },
    "medicare-cost-calculator": {
        "cn": {
            "title": "免费在线Medicare费用计算器",
            "short": "Medicare费用计算器",
            "desc": "免费在线Medicare费用计算器，估算Part A/B/C/D保费、IRMAA附加费和自付费用。输入收入和医保选择，自动计算年度Medicare总费用。纯前端本地计算。",
            "faq_title": "Medicare Part A/B/C/D是什么？",
            "faq_answer": "Medicare Part A覆盖住院费用（通常免费），Part B覆盖门诊（标准保费$174.70/月），Part C是Medicare Advantage替代方案，Part D覆盖处方药。高收入者需额外支付IRMAA附加费。",
            "hero_desc": "免费在线Medicare费用计算器，估算Part A/B/C/D保费、IRMAA附加费和自付费用。输入收入和医保选择，自动计算年度Medicare总费用。纯前端本地计算。",
            "calc_label": "输入年收入和医保选择，估算年度Medicare费用",
            "input1_label": "年收入 ($)：",
            "input1_id": "income",
            "input1_val": "85000",
            "input2_label": "Part B保费 ($/月)：",
            "input2_id": "partB",
            "input2_val": "174.70",
            "result_label": "年度总费用",
            "formula": "(PartB+PartD+IRMAA)×12 + 自付",
            "calc_js": """
var income=parseFloat(document.getElementById('income').value)||0;
var partB=parseFloat(document.getElementById('partB').value)||174.70;
var partD=parseFloat(document.getElementById('partD').value)||0;
var partC=parseFloat(document.getElementById('partC').value)||0;
var outOfPocket=parseFloat(document.getElementById('outOfPocket').value)||0;
var irmaa=0;
if(income>103000&&income<=129000)irmaa=69.90;
else if(income>129000&&income<=161000)irmaa=174.70;
else if(income>161000&&income<=193000)irmaa=279.50;
else if(income>193000&&income<500000)irmaa=384.30;
else if(income>=500000)irmaa=419.30;
var partDIrmaa=0;
if(income>103000&&income<=129000)partDIrmaa=12.90;
else if(income>129000&&income<=161000)partDIrmaa=33.30;
else if(income>161000&&income<=193000)partDIrmaa=53.80;
else if(income>193000&&income<500000)partDIrmaa=74.20;
else if(income>=500000)partDIrmaa=81.00;
var annualB=partB*12;
var annualD=partD*12;
var annualC=partC*12;
var totalIrmaa=(irmaa+partDIrmaa)*12;
var total=annualB+annualD+annualC+totalIrmaa+outOfPocket;
document.getElementById('val1').textContent='$'+total.toFixed(2);
document.getElementById('val2').textContent='$'+(annualB+totalIrmaa).toFixed(2);
document.getElementById('val3').textContent='$'+totalIrmaa.toFixed(2);
document.getElementById('val4').textContent='$'+outOfPocket.toFixed(2);
""",
            "extra_input": '<div class="form-row"><label>Part D保费 ($/月)：</label><input type="number" id="partD" value="33" step="any"></div><div class="form-row"><label>Part C/Advantage ($/月)：</label><input type="number" id="partC" value="0" step="any"></div><div class="form-row"><label>年度自付费用 ($)：</label><input type="number" id="outOfPocket" value="2000" step="any"></div>',
            "extra_labels": {"label2": "Part B+IRMAA", "label3": "IRMAA附加费", "label4": "年度自付"},
            "info_html": '<h3>🏥 Medicare费用构成</h3><p>Medicare费用由多个部分组成：</p><p><strong>Part B保费：</strong>2026年标准保费约$174.70/月。</p><p><strong>IRMAA：</strong>高收入者（年收入>$103,000）需支付额外附加费，单身和已婚分开计算。</p><p><strong>Part D：</strong>处方药计划保费，因计划而异。</p><p><strong>自付费用：</strong>包括免赔额、共付额和共同保险。</p>'
        },
        "en": {
            "title": "Free Online Medicare Cost Calculator",
            "short": "Medicare Cost Calculator",
            "desc": "Free online Medicare Cost Calculator. Estimate Part A/B/C/D premiums, IRMAA surcharges, and out-of-pocket costs. Enter income and coverage selections. Pure frontend computation.",
            "faq_title": "What are Medicare Parts A/B/C/D?",
            "faq_answer": "Part A covers hospital stays (usually free), Part B covers outpatient care (standard premium ~$174.70/mo), Part C is Medicare Advantage, and Part D covers prescriptions. Higher-income beneficiaries pay IRMAA surcharges.",
            "hero_desc": "Free online Medicare Cost Calculator. Estimate Part A/B/C/D premiums, IRMAA surcharges, and out-of-pocket costs. Enter income and coverage selections. Pure frontend computation.",
            "calc_label": "Enter annual income and coverage selections to estimate yearly Medicare costs",
            "input1_label": "Annual Income ($):",
            "input1_val": "85000",
            "input2_label": "Part B Premium ($/mo):",
            "input2_val": "174.70",
            "result_label": "Total Annual Cost",
            "formula": "(PartB+PartD+IRMAA)×12 + Out-of-Pocket",
            "extra_input": '<div class="form-row"><label>Part D Premium ($/mo):</label><input type="number" id="partD" value="33" step="any"></div><div class="form-row"><label>Part C/Advantage ($/mo):</label><input type="number" id="partC" value="0" step="any"></div><div class="form-row"><label>Annual Out-of-Pocket ($):</label><input type="number" id="outOfPocket" value="2000" step="any"></div>',
            "extra_labels": {"label2": "Part B+IRMAA", "label3": "IRMAA Surcharge", "label4": "Out-of-Pocket"},
            "info_html": '<h3>🏥 Medicare Cost Breakdown</h3><p>Medicare costs consist of several components:</p><p><strong>Part B Premium:</strong> 2026 standard premium ~$174.70/month.</p><p><strong>IRMAA:</strong> Higher-income beneficiaries (over $103,000/year) pay additional surcharges.</p><p><strong>Part D:</strong> Prescription drug plan premium, varies by plan.</p><p><strong>Out-of-Pocket:</strong> Includes deductibles, copays, and coinsurance.</p>'
        }
    },
    "savings-account-comparison": {
        "cn": {
            "title": "免费在线储蓄账户比较计算器",
            "short": "储蓄账户比较器",
            "desc": "免费在线储蓄账户比较计算器，对比多个银行储蓄账户的APY利率、复利频率和费用，找出最优收益方案。纯前端本地计算，无需注册。",
            "faq_title": "APY和利率有什么区别？",
            "faq_answer": "APY（年化收益率）包含了复利效应，比名义利率更准确地反映实际收益。例如5%名义利率按月复利的APY为5.12%。比较账户时应看APY而非名义利率。",
            "hero_desc": "免费在线储蓄账户比较计算器，对比多个银行储蓄账户的APY利率、复利频率和费用，找出最优收益方案。纯前端本地计算。",
            "calc_label": "输入本金和多个账户的APY，比较各账户收益",
            "input1_label": "初始本金 ($)：",
            "input1_id": "principal",
            "input1_val": "10000",
            "input2_label": "投资年限：",
            "input2_id": "years",
            "input2_val": "5",
            "result_label": "最优账户",
            "formula": "本金×(1+APY)^年数 - 年费×年数",
            "calc_js": """
var principal=parseFloat(document.getElementById('principal').value)||0;
var years=parseFloat(document.getElementById('years').value)||5;
var accts=document.getElementById('accounts').value.trim();
var bestName='-';var bestVal=0;var rows='';
if(accts){
  var lines=accts.split('\\n');
  for(var i=0;i<lines.length;i++){
    var parts=lines[i].split(/[,\\t]+/);
    if(parts.length>=2){
      var name=parts[0].trim();
      var apy=parseFloat(parts[1])||0;
      var fee=parts.length>=3?parseFloat(parts[2]):0;
      var compound=parts.length>=4?parts[3].trim().toLowerCase():'daily';
      var n=compound==='daily'?365:compound==='monthly'?12:compound==='quarterly'?4:1;
      var r=apy/100;
      var balance=principal*Math.pow(1+r/n,n*years)-fee*years;
      var net=balance-principal;
      if(net>bestVal){bestVal=net;bestName=name;}
      rows+='<tr><td>'+name+'</td><td>'+apy.toFixed(2)+'%</td><td>'+compound+'</td><td>$'+balance.toFixed(2)+'</td><td>$'+net.toFixed(2)+'</td></tr>';
    }
  }
}
document.getElementById('val1').textContent=bestName;
document.getElementById('val2').textContent='$'+bestVal.toFixed(2);
document.getElementById('val3').textContent=bestVal>0?'$'+(principal+bestVal).toFixed(2):'-';
document.getElementById('val4').textContent=bestVal>0?(bestVal/principal*100).toFixed(2)+'%':'-';
document.getElementById('compareTable').innerHTML=rows;
""",
            "extra_input": '<div class="form-row"><label>账户列表：</label><textarea id="accounts" rows="5" placeholder="每行一个账户：名称,APY,年费,复利频率&#10;例：&#10;Ally,4.25,0,daily&#10;Marcus,4.40,0,daily&#10;CapitalOne,4.10,0,monthly&#10;本地银行,2.50,36,quarterly"></textarea></div>',
            "extra_labels": {"label2": "最优净收益", "label3": "到期余额", "label4": "总回报率"},
            "info_html": '<h3>🏦 如何比较储蓄账户</h3><p>比较储蓄账户时应关注三个关键因素：</p><p><strong>APY：</strong>年化收益率，包含复利效应，越高越好。</p><p><strong>复利频率：</strong>日复利>月复利>季复利>年复利，频率越高收益越高。</p><p><strong>年费：</strong>有些账户收取维护费，需从收益中扣除。</p><h3>📋 比较结果</h3><div style="overflow-x:auto;margin-top:8px"><table style="width:100%;border-collapse:collapse;font-size:.85rem"><thead><tr style="color:#94a3b8"><th>账户</th><th>APY</th><th>复利</th><th>到期余额</th><th>净收益</th></tr></thead><tbody id="compareTable"></tbody></table></div>'
        },
        "en": {
            "title": "Free Online Savings Account Comparison Calculator",
            "short": "Savings Account Comparator",
            "desc": "Free online Savings Account Comparison Calculator. Compare multiple bank savings accounts by APY, compounding frequency, and fees to find the best return. Pure frontend computation.",
            "faq_title": "What is the difference between APY and interest rate?",
            "faq_answer": "APY (Annual Percentage Yield) includes the effect of compounding, giving a more accurate picture of actual returns than the nominal rate. E.g., 5% nominal rate compounded monthly gives ~5.12% APY. Always compare APY, not nominal rates.",
            "hero_desc": "Free online Savings Account Comparison Calculator. Compare multiple bank savings accounts by APY, compounding frequency, and fees to find the best return. Pure frontend computation.",
            "calc_label": "Enter principal and multiple account APYs to compare returns",
            "input1_label": "Initial Principal ($):",
            "input1_val": "10000",
            "input2_label": "Investment Years:",
            "input2_val": "5",
            "result_label": "Best Account",
            "formula": "Principal×(1+APY)^Years - Annual Fee×Years",
            "extra_input": '<div class="form-row"><label>Account List:</label><textarea id="accounts" rows="5" placeholder="One account per line: Name,APY,AnnualFee,CompoundFreq&#10;Example:&#10;Ally,4.25,0,daily&#10;Marcus,4.40,0,daily&#10;CapitalOne,4.10,0,monthly&#10;Local Bank,2.50,36,quarterly"></textarea></div>',
            "extra_labels": {"label2": "Best Net Return", "label3": "Maturity Balance", "label4": "Total Return %"},
            "info_html": '<h3>🏦 How to Compare Savings Accounts</h3><p>Focus on three key factors when comparing:</p><p><strong>APY:</strong> Annual Percentage Yield — includes compounding. Higher is better.</p><p><strong>Compounding Frequency:</strong> Daily > Monthly > Quarterly > Annual. More frequent compounding yields higher returns.</p><p><strong>Annual Fees:</strong> Some accounts charge maintenance fees that reduce net returns.</p><h3>📋 Comparison Results</h3><div style="overflow-x:auto;margin-top:8px"><table style="width:100%;border-collapse:collapse;font-size:.85rem"><thead><tr style="color:#94a3b8"><th>Account</th><th>APY</th><th>Compound</th><th>Maturity</th><th>Net Return</th></tr></thead><tbody id="compareTable"></tbody></table></div>'
        }
    },
    "retirement-expense-planner": {
        "cn": {
            "title": "免费在线退休支出规划计算器",
            "short": "退休支出规划器",
            "desc": "免费在线退休支出规划计算器，估算退休后月度/年度生活开支、医疗费用和通胀调整。输入当前开支和预期通胀率，计算退休储蓄目标。纯前端本地计算。",
            "faq_title": "退休后需要多少储蓄？",
            "faq_answer": "常见的退休储蓄目标有4%法则（储蓄 = 年度开支 × 25）和80%替代率法则（退休后开支 = 退休前收入的80%）。考虑通胀后，今天的$1在30年后购买力约为$0.41（按3%通胀）。",
            "hero_desc": "免费在线退休支出规划计算器，估算退休后月度/年度生活开支、医疗费用和通胀调整。输入当前开支和预期通胀率，计算退休储蓄目标。纯前端本地计算。",
            "calc_label": "输入当前开支和预期通胀率，计算退休储蓄目标",
            "input1_label": "当前月开支 ($)：",
            "input1_id": "monthlyExpense",
            "input1_val": "4000",
            "input2_label": "距退休年数：",
            "input2_id": "yearsToRetire",
            "input2_val": "25",
            "result_label": "所需储蓄",
            "formula": "退休后月开支×12×25 (4%法则)",
            "calc_js": """
var monthly=parseFloat(document.getElementById('monthlyExpense').value)||0;
var years=parseFloat(document.getElementById('yearsToRetire').value)||25;
var inflation=parseFloat(document.getElementById('inflation').value)||3;
var medicalPct=parseFloat(document.getElementById('medicalPct').value)||15;
var retirementYears=parseFloat(document.getElementById('retirementYears').value)||30;
var infRate=inflation/100;
var futureMonthly=monthly*Math.pow(1+infRate,years);
var futureAnnual=futureMonthly*12;
var medicalAnnual=futureAnnual*(medicalPct/100);
var totalAnnual=futureAnnual+medicalAnnual;
var nestEgg4=totalAnnual*25;
var nestEgg5=totalAnnual*20;
document.getElementById('val1').textContent='$'+nestEgg4.toFixed(0);
document.getElementById('val2').textContent='$'+futureMonthly.toFixed(0)+'/月';
document.getElementById('val3').textContent='$'+totalAnnual.toFixed(0)+'/年';
document.getElementById('val4').textContent='$'+nestEgg5.toFixed(0);
""",
            "extra_input": '<div class="form-row"><label>年通胀率 (%)：</label><input type="number" id="inflation" value="3" step="any"></div><div class="form-row"><label>医疗费用占比 (%)：</label><input type="number" id="medicalPct" value="15" step="any"></div><div class="form-row"><label>退休年限：</label><input type="number" id="retirementYears" value="30" step="any"></div>',
            "extra_labels": {"label2": "退休后月开支", "label3": "年度总开支", "label4": "保守目标(5%)"},
            "info_html": '<h3>📊 退休储蓄目标</h3><p><strong>4%法则（安全提款率）：</strong>储蓄 = 年度开支 × 25。研究表明，每年提取储蓄的4%在30年内耗尽储蓄的概率很低。</p><p><strong>通胀调整：</strong>按3%年通胀，25年后$4,000的购买力相当于现在约$1,900。</p><p><strong>医疗费用：</strong>退休后医疗支出通常占总支出的15-25%，需单独考虑。</p>'
        },
        "en": {
            "title": "Free Online Retirement Expense Planner",
            "short": "Retirement Expense Planner",
            "desc": "Free online Retirement Expense Planner. Estimate post-retirement monthly/annual living expenses, medical costs, and inflation adjustment. Calculate your retirement savings target. Pure frontend computation.",
            "faq_title": "How much savings do I need for retirement?",
            "faq_answer": "Common retirement savings targets include the 4% Rule (Savings = Annual Expenses × 25) and the 80% Replacement Rate rule (post-retirement expenses = 80% of pre-retirement income). With 3% inflation, $1 today has about $0.41 purchasing power in 30 years.",
            "hero_desc": "Free online Retirement Expense Planner. Estimate post-retirement monthly/annual living expenses, medical costs, and inflation adjustment. Calculate your retirement savings target. Pure frontend computation.",
            "calc_label": "Enter current expenses and expected inflation to calculate retirement savings target",
            "input1_label": "Current Monthly Expenses ($):",
            "input1_val": "4000",
            "input2_label": "Years to Retirement:",
            "input2_val": "25",
            "result_label": "Savings Needed",
            "formula": "Post-retirement monthly expense×12×25 (4% Rule)",
            "extra_input": '<div class="form-row"><label>Annual Inflation Rate (%):</label><input type="number" id="inflation" value="3" step="any"></div><div class="form-row"><label>Medical Cost Share (%):</label><input type="number" id="medicalPct" value="15" step="any"></div><div class="form-row"><label>Years in Retirement:</label><input type="number" id="retirementYears" value="30" step="any"></div>',
            "extra_labels": {"label2": "Retirement Monthly", "label3": "Annual Total", "label4": "Conservative(5%)"},
            "info_html": '<h3>📊 Retirement Savings Target</h3><p><strong>4% Rule (Safe Withdrawal Rate):</strong> Savings = Annual Expenses × 25. Research shows withdrawing 4% annually has a low probability of depleting savings over 30 years.</p><p><strong>Inflation Adjustment:</strong> At 3% inflation, $4,000 in 25 years has the purchasing power of ~$1,900 today.</p><p><strong>Medical Costs:</strong> Healthcare typically accounts for 15-25% of retirement spending and should be planned separately.</p>'
        }
    },
    "forex-risk-calculator": {
        "cn": {
            "title": "免费在线外汇风险计算器",
            "short": "外汇风险计算器",
            "desc": "免费在线外汇风险计算器，计算外汇交易中的头寸规模、止损点数、风险金额和盈亏比。输入账户余额、风险比例和入场/止损价格，自动计算最优头寸。纯前端本地计算。",
            "faq_title": "什么是外汇风险管理的2%法则？",
            "faq_answer": "2%法则是外汇交易中最基本的风险管理原则：每笔交易的风险不应超过账户总额的2%。例如$10,000账户，每笔最多亏损$200。公式：<code>头寸规模 = 风险金额 ÷ (止损点数 × 点值)</code>。",
            "hero_desc": "免费在线外汇风险计算器，计算外汇交易中的头寸规模、止损点数、风险金额和盈亏比。输入账户余额、风险比例和入场/止损价格，自动计算最优头寸。纯前端本地计算。",
            "calc_label": "输入账户余额和交易参数，计算最优头寸规模",
            "input1_label": "账户余额 ($)：",
            "input1_id": "balance",
            "input1_val": "10000",
            "input2_label": "风险比例 (%)：",
            "input2_id": "riskPercent",
            "input2_val": "2",
            "result_label": "建议头寸",
            "formula": "(余额×风险%) ÷ (止损点数×点值)",
            "calc_js": """
var balance=parseFloat(document.getElementById('balance').value)||0;
var riskPct=parseFloat(document.getElementById('riskPercent').value)||2;
var entry=parseFloat(document.getElementById('entry').value)||0;
var stop=parseFloat(document.getElementById('stop').value)||0;
var target=parseFloat(document.getElementById('target').value)||0;
var pair=document.getElementById('pair').value;
var riskAmount=balance*(riskPct/100);
var pipValue=0.0001;
if(pair.indexOf('JPY')!==-1)pipValue=0.01;
var stopPips=Math.abs(entry-stop)/pipValue;
var targetPips=Math.abs(target-entry)/pipValue;
var positionSize=0;
if(stopPips>0)positionSize=riskAmount/(stopPips*10);
var rrRatio=stopPips>0?(targetPips/stopPips):0;
var potentialProfit=positionSize*10*targetPips;
document.getElementById('val1').textContent=positionSize.toFixed(0)+' units';
document.getElementById('val2').textContent='$'+riskAmount.toFixed(2);
document.getElementById('val3').textContent=stopPips.toFixed(0)+' pips';
document.getElementById('val4').textContent='1:'+rrRatio.toFixed(1)+' ($'+potentialProfit.toFixed(2)+')';
""",
            "extra_input": '<div class="form-row"><label>货币对：</label><select id="pair"><option value="EUR/USD">EUR/USD</option><option value="GBP/USD">GBP/USD</option><option value="USD/JPY">USD/JPY</option><option value="AUD/USD">AUD/USD</option><option value="USD/CAD">USD/CAD</option><option value="NZD/USD">NZD/USD</option></select></div><div class="form-row"><label>入场价格：</label><input type="number" id="entry" value="1.0850" step="any"></div><div class="form-row"><label>止损价格：</label><input type="number" id="stop" value="1.0800" step="any"></div><div class="form-row"><label>止盈价格：</label><input type="number" id="target" value="1.0950" step="any"></div>',
            "extra_labels": {"label2": "风险金额", "label3": "止损点数", "label4": "盈亏比"},
            "info_html": '<h3>💱 外汇风险计算</h3><p>外汇风险管理是交易成功的基石：</p><p><strong>头寸规模：</strong>根据账户余额和风险容忍度，计算每次交易应持有的货币单位数量。</p><p><strong>点值：</strong>大多数货币对1点=0.0001，日元对1点=0.01。</p><p><strong>盈亏比：</strong>建议不低于1:1.5，即每冒$1风险，预期收益至少$1.5。</p><p><strong>⚠️ 免责声明：</strong>本工具仅供教育参考，不构成投资建议。外汇交易存在重大亏损风险。</p>'
        },
        "en": {
            "title": "Free Online Forex Risk Calculator",
            "short": "Forex Risk Calculator",
            "desc": "Free online Forex Risk Calculator. Calculate position size, stop-loss pips, risk amount, and risk-reward ratio for forex trading. Enter account balance, risk percentage, entry/stop prices. Pure frontend computation.",
            "faq_title": "What is the 2% Rule in forex risk management?",
            "faq_answer": "The 2% Rule is the most fundamental risk management principle in forex: never risk more than 2% of your account on a single trade. E.g., a $10,000 account allows a maximum loss of $200 per trade. Formula: <code>Position Size = Risk Amount ÷ (Stop-Loss Pips × Pip Value)</code>.",
            "hero_desc": "Free online Forex Risk Calculator. Calculate position size, stop-loss pips, risk amount, and risk-reward ratio for forex trading. Enter account balance, risk percentage, entry/stop prices. Pure frontend computation.",
            "calc_label": "Enter account balance and trade parameters to calculate optimal position size",
            "input1_label": "Account Balance ($):",
            "input1_val": "10000",
            "input2_label": "Risk Percentage (%):",
            "input2_val": "2",
            "result_label": "Suggested Position",
            "formula": "(Balance×Risk%) ÷ (Stop-Loss Pips×Pip Value)",
            "extra_input": '<div class="form-row"><label>Currency Pair:</label><select id="pair"><option value="EUR/USD">EUR/USD</option><option value="GBP/USD">GBP/USD</option><option value="USD/JPY">USD/JPY</option><option value="AUD/USD">AUD/USD</option><option value="USD/CAD">USD/CAD</option><option value="NZD/USD">NZD/USD</option></select></div><div class="form-row"><label>Entry Price:</label><input type="number" id="entry" value="1.0850" step="any"></div><div class="form-row"><label>Stop-Loss Price:</label><input type="number" id="stop" value="1.0800" step="any"></div><div class="form-row"><label>Take-Profit Price:</label><input type="number" id="target" value="1.0950" step="any"></div>',
            "extra_labels": {"label2": "Risk Amount", "label3": "Stop-Loss Pips", "label4": "Risk-Reward Ratio"},
            "info_html": '<h3>💱 Forex Risk Calculation</h3><p>Risk management is the foundation of successful forex trading:</p><p><strong>Position Size:</strong> Calculate how many currency units to trade based on your account balance and risk tolerance.</p><p><strong>Pip Value:</strong> Most pairs: 1 pip = 0.0001; JPY pairs: 1 pip = 0.01.</p><p><strong>Risk-Reward Ratio:</strong> Aim for at least 1:1.5 — for every $1 risked, target at least $1.50 in profit.</p><p><strong>⚠️ Disclaimer:</strong> This tool is for educational purposes only and does not constitute investment advice. Forex trading carries significant risk of loss.</p>'
        }
    }
}

def generate_tool(name, cfg, lang, is_cn=True):
    """Generate a tool HTML file"""
    c = dict(cfg[lang])
    # Inherit IDs from CN if not present in EN
    for k in ['input1_id', 'input2_id', 'calc_js']:
        if k not in c:
            c[k] = cfg['cn'][k]
    _dir = f"{BASE}/{name}" if is_cn else f"{BASE}/en/{name}"
    os.makedirs(_dir, exist_ok=True)
    
    lcode = "zh-CN" if is_cn else "en"
    hreflang_self = "zh" if is_cn else "en"
    hreflang_other = "en" if is_cn else "zh"
    canonical = f"https://free-toolbase.com/{name}/" if is_cn else f"https://free-toolbase.com/en/{name}/"
    alt_en = f"https://free-toolbase.com/en/{name}/"
    alt_zh = f"https://free-toolbase.com/{name}/"
    
    nav_home = "首页" if is_cn else "Home"
    nav_tools = "工具" if is_cn else "Tools"
    nav_back_href = "../index.html" if is_cn else "../index.html"
    lang_switch = f'<a href="index.html" class="active">中文</a><a href="../en/{name}/" class="">EN</a>' if is_cn else f'<a href="../{name}/" class="">中文</a><a href="index.html" class="active">EN</a>'
    breadcrumb_home = "首页" if is_cn else "Home"
    
    extra_input = c.get("extra_input", "")
    extra_labels = c.get("extra_labels", {})
    info_html = c.get("info_html", "")
    
    faqs = [
        (c["faq_title"], c["faq_answer"]),
        (f'{c["short"]}有什么使用限制吗？' if is_cn else f'Are there usage limits?',
         f'{c["short"]}是免费在线工具，没有使用次数限制。' if is_cn else f'The {c["short"]} is free with no usage limits.'),
        (f'{c["short"]}支持手机端使用吗？' if is_cn else f'Does it work on mobile?',
         f'支持。{c["short"]}采用响应式设计，可以在手机、平板和电脑上正常使用。' if is_cn else f'Yes, it uses responsive design and works on phones, tablets, and desktops.'),
        (f'数据安全吗？' if is_cn else 'Is my data secure?',
         f'安全。所有计算在浏览器中完成，数据不上传服务器。' if is_cn else 'All calculations happen in your browser — no data is uploaded to any server.'),
    ]
    faq_json = []
    for q, a in faqs:
        faq_json.append('{"@type": "Question", "name": "' + q.replace('"','\\"') + '", "acceptedAnswer": {"@type": "Answer", "text": "' + a.replace('"','\\"').replace('\n',' ') + '"}}')
    
    faq_html = ""
    for q, a in faqs:
        faq_html += f'<div class="faq-item"><h3>{q}</h3><p>{a}</p></div>\n'
    
    faq_ld = '[' + ','.join(faq_json) + ']'
    
    extra_cards = ""
    default_labels = {"label2": "指标2", "label3": "指标3", "label4": "指标4"}
    for k in ["label2", "label3", "label4"]:
        lbl = extra_labels.get(k, default_labels[k])
        vid = "val" + k[-1]
        extra_cards += f'<div class="card"><div class="label">{lbl}</div><div class="value" id="{vid}">--</div></div>\n'
    
    extra_copy = ""
    for k in ["label1", "label2", "label3", "label4"]:
        vid = "val" + k[-1]
        if k == "label1":
            extra_copy += f'var l1=document.getElementById("label1").textContent;var v1=document.getElementById("val1").textContent;if(v1!=="--")r.push(l1+": "+v1);\n'
        else:
            lbl = extra_labels.get(k, default_labels[k])
            extra_copy += f'var v{vid[-1]}=document.getElementById("{vid}").textContent;if(v{vid[-1]}!=="--")r.push("{lbl}: "+v{vid[-1]});\n'
    
    html = f'''<!DOCTYPE html>
<html lang="{lcode}">
<head>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-9W1157EBQV"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-9W1157EBQV');</script>
<script>window.addEventListener("error",function(e){{if(e&&e.message===""){{e.preventDefault();}}}});window.addEventListener("unhandledrejection",function(e){{if(e&&e.reason&&e.reason.message===""){{e.preventDefault();}}}});</script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="{c['desc']}">
<meta name="keywords" content="{c['title']},工具,在线工具,免费">
<title>{c['title']} | 无需注册</title>
<link rel="canonical" href="{canonical}">
<meta property="og:title" content="{c['title']} | 无需注册">
<meta property="og:description" content="{c['desc']}">
<meta property="og:url" content="{canonical}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Free ToolBase">
<link rel="alternate" hreflang="{hreflang_self}" href="{canonical}">
<link rel="alternate" hreflang="{hreflang_other}" href="{alt_en if is_cn else alt_zh}">
<link rel="alternate" hreflang="x-default" href="https://free-toolbase.com/en/{name}/">
<script type="application/ld+json">{{"@context": "https://schema.org", "@type": "SoftwareApplication", "name": "{c['title']}", "description": "{c['desc']}", "applicationCategory": "UtilitiesApplication", "operatingSystem": "Web", "publisher": {{"@type": "Organization", "name": "Free ToolBase", "email": "dexshuang@google.com"}}, "offers": {{"@type": "Offer", "price": "0", "priceCurrency": "USD"}}}}</script>
<script type="application/ld+json">{{"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": {faq_ld}}}</script>
<script type="application/ld+json">{{"@context": "https://schema.org", "@type": "HowTo", "name": "如何使用{c['title']}", "description": "如何使用{c['title']}的详细步骤指南", "totalTime": "PT2M", "tool": {{"@type": "HowToTool", "name": "{c['title']}"}}, "step": [{{"@type": "HowToStep", "position": 1, "name": "输入数据", "text": "在输入框中输入需要计算的数值"}}, {{"@type": "HowToStep", "position": 2, "name": "选择选项", "text": "根据需要选择计算模式或参数"}}, {{"@type": "HowToStep", "position": 3, "name": "点击计算", "text": "点击计算按钮获取结果"}}, {{"@type": "HowToStep", "position": 4, "name": "查看结果", "text": "查看计算结果，支持一键复制"}}]}}</script>
<script type="application/ld+json">{{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{{"@type": "ListItem", "position": 1, "name": "{breadcrumb_home}", "item": "{'https://free-toolbase.com/' if is_cn else 'https://free-toolbase.com/en/'}"}}, {{"@type": "ListItem", "position": 2, "name": "{nav_tools}", "item": "{'https://free-toolbase.com/#tools' if is_cn else 'https://free-toolbase.com/en/#tools'}"}}, {{"@type": "ListItem", "position": 3, "name": "{c['title']}", "item": "{canonical}"}}]}}</script>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#0f172a;color:#e2e8f0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,{"PingFang SC","Microsoft YaHei" if is_cn else ""}sans-serif;line-height:1.6;min-height:100vh}}
a{{color:#06b6d4;text-decoration:none}}
.container{{max-width:900px;margin:0 auto;padding:24px 16px}}
.header{{display:flex;justify-content:space-between;align-items:center;margin-bottom:24px}}
.header h1{{font-size:1.6rem;color:#f1f5f9}}
.lang-switch{{display:flex;gap:4px;background:#1e293b;border-radius:8px;padding:4px;border:1px solid rgba(148,163,184,.1)}}
.lang-switch a{{padding:6px 12px;border-radius:5px;font-size:.85rem;color:#94a3b8}}
.lang-switch a.active{{background:rgba(6,182,212,.2);color:#22d3ee}}
.nav-back{{color:#64748b;font-size:.85rem;margin-bottom:16px}}
.nav-back a{{color:#64748b}}
.nav-back a:hover{{color:#94a3b8}}
.hero{{background:#1e293b;border-radius:12px;padding:16px 20px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1);font-size:.9rem;color:#94a3b8}}
.hero .badge{{display:inline-block;margin-top:8px;background:rgba(6,182,212,.1);color:#22d3ee;padding:4px 10px;border-radius:4px;font-size:.75rem}}
.input-section{{background:#1e293b;border-radius:12px;padding:20px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1)}}
.input-section h2{{font-size:1.1rem;color:#f1f5f9;margin-bottom:12px}}
.form-row{{display:flex;gap:16px;flex-wrap:wrap;margin-bottom:12px;align-items:center}}
.form-row label{{font-size:.9rem;color:#94a3b8;min-width:100px}}
.form-row input,.form-row select,.form-row textarea{{background:#0f172a;color:#e2e8f0;border:1px solid rgba(148,163,184,.2);border-radius:6px;padding:8px 12px;font-size:.9rem;width:200px}}
.form-row textarea{{width:100%;min-height:100px;resize:vertical;font-family:monospace}}
.form-row input:focus,.form-row select:focus,.form-row textarea:focus{{outline:none;border-color:rgba(6,182,212,.5)}}
.btn-row{{display:flex;gap:8px;flex-wrap:wrap;margin-top:12px}}
.btn{{padding:8px 20px;border:none;border-radius:6px;font-size:.85rem;cursor:pointer;transition:all .2s}}
.btn-primary{{background:rgba(6,182,212,.2);color:#22d3ee;border:1px solid rgba(6,182,212,.3)}}
.btn-primary:hover{{background:rgba(6,182,212,.3)}}
.btn-secondary{{background:rgba(148,163,184,.1);color:#94a3b8;border:1px solid rgba(148,163,184,.2)}}
.btn-secondary:hover{{background:rgba(148,163,184,.2)}}
.result-section{{background:#1e293b;border-radius:12px;padding:20px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1)}}
.result-section h2{{font-size:1.1rem;color:#f1f5f9;margin-bottom:12px}}
.result-card{{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px}}
.card{{background:#0f172a;border:1px solid rgba(148,163,184,.15);border-radius:8px;padding:16px;text-align:center}}
.card .label{{font-size:.8rem;color:#64748b;margin-bottom:4px}}
.card .value{{font-size:1.4rem;font-weight:700;color:#22d3ee}}
.card .sub{{font-size:.75rem;color:#64748b;margin-top:4px}}
.info-section{{background:#1e293b;border-radius:12px;padding:20px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1)}}
.info-section h2{{font-size:1.1rem;color:#f1f5f9;margin-bottom:12px}}
.info-section h3{{font-size:.95rem;color:#e2e8f0;margin:16px 0 8px}}
.info-section p{{color:#94a3b8;font-size:.9rem;margin-bottom:8px}}
.info-section code{{background:rgba(6,182,212,.1);color:#22d3ee;padding:2px 6px;border-radius:3px;font-size:.85rem}}
.footer{{border-top:1px solid rgba(148,163,184,.1);padding:24px 0;margin-top:32px;text-align:center;color:#64748b;font-size:.85rem}}
.footer a{{color:#64748b;margin:0 8px}}
.footer a:hover{{color:#94a3b8}}
.toast{{position:fixed;bottom:20px;left:50%;transform:translateX(-50%);background:#1e293b;color:#22d3ee;padding:10px 24px;border-radius:8px;border:1px solid rgba(6,182,212,.3);font-size:.85rem;z-index:999;opacity:0;transition:opacity .3s}}
.toast.show{{opacity:1}}
.faq-section{{margin-top:24px}}
.faq-section h2{{margin-bottom:16px}}
.faq-item{{margin-bottom:12px;padding:14px 16px;border-radius:8px;background:#1e293b;border:1px solid rgba(148,163,184,.08);transition:border-color .2s}}
.faq-item:hover{{border-color:rgba(6,182,212,.2)}}
.faq-item h3{{font-size:.95rem;color:#e2e8f0;margin-bottom:6px;cursor:pointer;display:flex;align-items:center;gap:8px}}
.faq-item h3::before{{content:'Q';display:inline-flex;align-items:center;justify-content:center;width:22px;height:22px;border-radius:50%;background:rgba(6,182,212,.15);color:#22d3ee;font-size:.7rem;font-weight:700;flex-shrink:0}}
.faq-item p{{color:#94a3b8;font-size:.88rem;line-height:1.6;padding-left:30px}}
@media(max-width:600px){{.form-row{{flex-direction:column;align-items:flex-start}}.form-row label{{min-width:auto}}.form-row input,.form-row select,.form-row textarea{{width:100%}}.header{{flex-direction:column;gap:8px}}.header h1{{font-size:1.2rem}}}}
</style>
<meta property="og:image" content="https://free-toolbase.com/og-image.svg">
<meta name="twitter:image" content="https://free-toolbase.com/og-image.svg">
<meta name="twitter:card" content="summary_large_image">
<meta name="robots" content="index, follow">
<link rel="icon" type="image/svg+xml" href="favicon.svg">
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5998441792679372" crossorigin="anonymous"></script>
</head>
<body>
<div class="container">
<div class="header"><h1>📊 {c['title']}</h1><div class="lang-switch">{lang_switch}</div></div>
<p class="nav-back"><a href="{nav_back_href}">{nav_home}</a> &rsaquo; <a href="{nav_back_href}#tools">{nav_tools}</a> &rsaquo; {c['title']}</p>
<div class="hero"><p>{c['hero_desc']} | {'无需注册 · 数据绝不上传服务器' if is_cn else 'No signup · Data never leaves your device'}</p><span class="badge">{'零依赖·可离线使用' if is_cn else 'Zero dependencies · Works offline'}</span></div>

<div class="input-section">
<h2>📊 {'输入数据' if is_cn else 'Input Data'}</h2>
<div class="form-row"><label>{c['input1_label']}</label><input type="number" id="{c['input1_id']}" value="{c['input1_val']}" step="any"></div>
<div class="form-row"><label>{c['input2_label']}</label><input type="number" id="{c['input2_id']}" value="{c['input2_val']}" step="any"></div>
{extra_input}
<div class="btn-row">
<button class="btn btn-primary" onclick="calculate()">🔍 {'计算' if is_cn else 'Calculate'}</button>
<button class="btn btn-secondary" onclick="resetAll()">🔄 {'重置' if is_cn else 'Reset'}</button>
<button class="btn btn-secondary" onclick="copyResults()">📋 {'复制结果' if is_cn else 'Copy Results'}</button>
</div>
</div>

<div class="result-section" id="resultSection">
<h2>📈 {'计算结果' if is_cn else 'Results'}</h2>
<div class="result-card">
<div class="card"><div class="label" id="label1">{c['result_label']}</div><div class="value" id="val1">--</div></div>
{extra_cards}
</div>
</div>

<div class="info-section">
<h2>📖 {'公式说明' if is_cn else 'Formula Guide'}</h2>
{info_html}
</div>

<div class="faq-section info-section">
<h2>❓ {'常见问题' if is_cn else 'FAQ'}</h2>
{faq_html}
</div>

<div class="footer">
<p>&copy; 2026 Free ToolBase. {'完全免费 · 无需注册 · 纯前端计算' if is_cn else '100% Free · No Signup · Client-Side Only'}</p>
<p><a href="{'../about/' if is_cn else '../about/'}">{'关于' if is_cn else 'About'}</a> <a href="{'../contact/' if is_cn else '../contact/'}">{'联系' if is_cn else 'Contact'}</a> <a href="{'../privacy/' if is_cn else '../privacy/'}">{'隐私' if is_cn else 'Privacy'}</a> <a href="{'../terms/' if is_cn else '../terms/'}">{'条款' if is_cn else 'Terms'}</a></p>
</div>
</div>
<div class="toast" id="toast"></div>

<script>
function showToast(msg){{var t=document.getElementById('toast');t.textContent=msg;t.classList.add('show');setTimeout(function(){{t.classList.remove('show')}},2000)}}
function copyResults(){{var r=[];{extra_copy}if(r.length===0){{showToast("{'请先计算' if is_cn else 'Please calculate first'}");return}}navigator.clipboard.writeText(r.join('\\n')).then(function(){{showToast("{'已复制到剪贴板' if is_cn else 'Copied to clipboard'}")}}).catch(function(){{showToast("{'复制失败' if is_cn else 'Copy failed'}")}})}}
function calculate(){{{c['calc_js']}}}
function resetAll(){{var defaults={{}};defaults["{c['input1_id']}"]="{c['input1_val']}";defaults["{c['input2_id']}"]="{c['input2_val']}";for(var k in defaults){{var el=document.getElementById(k);if(el)el.value=defaults[k]}};document.getElementById('val1').textContent='--';document.getElementById('val2').textContent='--';document.getElementById('val3').textContent='--';document.getElementById('val4').textContent='--';}}
calculate();
</script>
</body>
</html>'''
    
    filepath = os.path.join(_dir, "index.html")
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"  ✓ {filepath}")

# Generate all tools
for name, cfg in tools.items():
    print(f"\n🔨 {name}:")
    generate_tool(name, cfg, "cn", is_cn=True)
    generate_tool(name, cfg, "en", is_cn=False)

print("\n✅ All 5 tools generated!")