#!/usr/bin/env python3
"""批量开发5个金融工具：CN+EN双版本"""
import os, json

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TOOLS = [
    {
        "slug": "escrow-calculator",
        "cn_name": "在线托管账户计算器",
        "en_name": "Online Escrow Calculator",
        "cn_desc": "免费在线托管账户计算器，快速计算房屋托管账户的月度缴款和年度总额。输入房产税、房屋保险、PMI等费用，一键算出托管账户月供。适合购房者预算规划。",
        "en_desc": "Free online escrow calculator to quickly calculate monthly escrow payments and annual totals. Enter property tax, home insurance, PMI and more to get instant results. Perfect for homebuyer budget planning.",
        "cn_icon": "🏦",
        "en_icon": "🏦",
        "calc_func": "calcEscrow",
        "inputs": [
            {"id": "ecTax", "cn_label": "年房产税", "en_label": "Annual Property Tax", "cn_unit": "元", "en_unit": "$", "default": 6000},
            {"id": "ecInsurance", "cn_label": "年房屋保险", "en_label": "Annual Home Insurance", "cn_unit": "元", "en_unit": "$", "default": 1200},
            {"id": "ecPMI", "cn_label": "年PMI保费", "en_label": "Annual PMI", "cn_unit": "元", "en_unit": "$", "default": 0},
            {"id": "ecHOA", "cn_label": "年HOA费用", "en_label": "Annual HOA Fee", "cn_unit": "元", "en_unit": "$", "default": 0},
            {"id": "ecFlood", "cn_label": "年洪水保险", "en_label": "Annual Flood Insurance", "cn_unit": "元", "en_unit": "$", "default": 0},
            {"id": "ecCushion", "cn_label": "缓冲月数", "en_label": "Cushion Months", "cn_unit": "月", "en_unit": "mo", "default": 2},
        ],
        "result_html_cn": """<div style="display:flex;gap:16px;flex-wrap:wrap;margin-bottom:16px">
<div class="result-card"><div class="label">月度托管缴款</div><div class="value highlight" id="ecMonthly">$0.00</div></div>
<div class="result-card"><div class="label">年度总费用</div><div class="value" id="ecTotal">$0.00</div></div>
<div class="result-card"><div class="label">含缓冲月供</div><div class="value warn" id="ecWithCushion">$0.00</div></div>
<div class="result-card"><div class="label">缓冲总额</div><div class="value" id="ecCushionAmt">$0.00</div></div>
</div>""",
        "result_html_en": """<div style="display:flex;gap:16px;flex-wrap:wrap;margin-bottom:16px">
<div class="result-card"><div class="label">Monthly Escrow</div><div class="value highlight" id="ecMonthly">$0.00</div></div>
<div class="result-card"><div class="label">Annual Total</div><div class="value" id="ecTotal">$0.00</div></div>
<div class="result-card"><div class="label">With Cushion</div><div class="value warn" id="ecWithCushion">$0.00</div></div>
<div class="result-card"><div class="label">Cushion Amount</div><div class="value" id="ecCushionAmt">$0.00</div></div>
</div>""",
        "calc_js": """function calcEscrow(){
  var tax=parseFloat(document.getElementById('ecTax').value)||0;
  var ins=parseFloat(document.getElementById('ecInsurance').value)||0;
  var pmi=parseFloat(document.getElementById('ecPMI').value)||0;
  var hoa=parseFloat(document.getElementById('ecHOA').value)||0;
  var flood=parseFloat(document.getElementById('ecFlood').value)||0;
  var cushion=parseInt(document.getElementById('ecCushion').value)||0;
  var total=tax+ins+pmi+hoa+flood;
  var monthly=total/12;
  var withCushion=monthly*(1+cushion/12);
  var fmt=function(n){return '$'+n.toFixed(2).replace(/\\B(?=(\\d{3})+(?!\\d))/g,',');};
  document.getElementById('ecMonthly').textContent=fmt(monthly);
  document.getElementById('ecTotal').textContent=fmt(total);
  document.getElementById('ecWithCushion').textContent=fmt(withCushion);
  document.getElementById('ecCushionAmt').textContent=fmt(total*(cushion/12));
}"""
    },
    {
        "slug": "cash-out-refinance-calculator",
        "cn_name": "在线Cash-Out Refinance计算器",
        "en_name": "Online Cash-Out Refinance Calculator",
        "cn_desc": "免费在线Cash-Out Refinance计算器，快速计算套现再融资的月供和现金收益。输入当前贷款余额、房屋估值、新利率等参数，一键算出可套现金额和新月供。适合房主评估再融资方案。",
        "en_desc": "Free online cash-out refinance calculator to calculate new monthly payment and cash proceeds. Enter current loan balance, home value, new rate and more. Perfect for homeowners evaluating refinance options.",
        "cn_icon": "🏠",
        "en_icon": "🏠",
        "calc_func": "calcCO",
        "inputs": [
            {"id": "coHomeVal", "cn_label": "房屋估值", "en_label": "Home Value", "cn_unit": "万元", "en_unit": "$", "default": 500000},
            {"id": "coLoanBal", "cn_label": "当前贷款余额", "en_label": "Current Loan Balance", "cn_unit": "万元", "en_unit": "$", "default": 300000},
            {"id": "coRate", "cn_label": "新利率", "en_label": "New Interest Rate", "cn_unit": "%", "en_unit": "%", "default": 6.5},
            {"id": "coYears", "cn_label": "贷款年限", "en_label": "Loan Term", "cn_unit": "年", "en_unit": "yrs", "default": 30},
            {"id": "coLTV", "cn_label": "最高LTV", "en_label": "Max LTV", "cn_unit": "%", "en_unit": "%", "default": 80},
            {"id": "coCosts", "cn_label": "结算费用", "en_label": "Closing Costs", "cn_unit": "万元", "en_unit": "$", "default": 5000},
        ],
        "result_html_cn": """<div style="display:flex;gap:16px;flex-wrap:wrap;margin-bottom:16px">
<div class="result-card"><div class="label">可套现金额</div><div class="value highlight" id="coCash">$0.00</div></div>
<div class="result-card"><div class="label">新月供</div><div class="value" id="coMonthly">$0.00</div></div>
<div class="result-card"><div class="label">新贷款总额</div><div class="value warn" id="coNewLoan">$0.00</div></div>
<div class="result-card"><div class="label">实际LTV</div><div class="value" id="coLTVact">0%</div></div>
</div>""",
        "result_html_en": """<div style="display:flex;gap:16px;flex-wrap:wrap;margin-bottom:16px">
<div class="result-card"><div class="label">Cash Out</div><div class="value highlight" id="coCash">$0.00</div></div>
<div class="result-card"><div class="label">New Monthly Payment</div><div class="value" id="coMonthly">$0.00</div></div>
<div class="result-card"><div class="label">New Loan Amount</div><div class="value warn" id="coNewLoan">$0.00</div></div>
<div class="result-card"><div class="label">Actual LTV</div><div class="value" id="coLTVact">0%</div></div>
</div>""",
        "calc_js": """function calcCO(){
  var home=parseFloat(document.getElementById('coHomeVal').value)||0;
  var bal=parseFloat(document.getElementById('coLoanBal').value)||0;
  var rate=parseFloat(document.getElementById('coRate').value)||0;
  var years=parseInt(document.getElementById('coYears').value)||30;
  var ltv=parseFloat(document.getElementById('coLTV').value)||80;
  var costs=parseFloat(document.getElementById('coCosts').value)||0;
  var maxLoan=home*ltv/100;
  var newLoan=Math.min(maxLoan, bal+50000);
  var cashOut=Math.max(0, newLoan-bal-costs);
  var r=rate/100/12; var n=years*12;
  var payment=0;
  if(r>0) payment=newLoan*r*Math.pow(1+r,n)/(Math.pow(1+r,n)-1);
  else payment=newLoan/n;
  var fmt=function(n){return '$'+n.toFixed(2).replace(/\\B(?=(\\d{3})+(?!\\d))/g,',');};
  document.getElementById('coCash').textContent=fmt(cashOut);
  document.getElementById('coMonthly').textContent=fmt(payment);
  document.getElementById('coNewLoan').textContent=fmt(newLoan);
  document.getElementById('coLTVact').textContent=home>0?(newLoan/home*100).toFixed(1)+'%':'0%';
}"""
    },
    {
        "slug": "bridge-loan-calculator",
        "cn_name": "在线过桥贷款计算器",
        "en_name": "Online Bridge Loan Calculator",
        "cn_desc": "免费在线过桥贷款计算器，快速计算买房过桥贷款的月度利息和总成本。输入新房价格、旧房净值、利率和期限，一键算出过桥贷款月供和总利息。适合换房者资金规划。",
        "en_desc": "Free online bridge loan calculator to calculate monthly interest and total cost for bridge financing. Enter new home price, old home equity, rate and term. Perfect for home swap financing.",
        "cn_icon": "🌉",
        "en_icon": "🌉",
        "calc_func": "calcBridge",
        "inputs": [
            {"id": "blNewPrice", "cn_label": "新房价格", "en_label": "New Home Price", "cn_unit": "万元", "en_unit": "$", "default": 600000},
            {"id": "blDown", "cn_label": "首付比例", "en_label": "Down Payment", "cn_unit": "%", "en_unit": "%", "default": 20},
            {"id": "blEquity", "cn_label": "旧房净值", "en_label": "Old Home Equity", "cn_unit": "万元", "en_unit": "$", "default": 200000},
            {"id": "blRate", "cn_label": "过桥利率", "en_label": "Bridge Rate", "cn_unit": "%", "en_unit": "%", "default": 8.5},
            {"id": "blMonths", "cn_label": "期限", "en_label": "Term", "cn_unit": "月", "en_unit": "mo", "default": 6},
            {"id": "blOrigFee", "cn_label": "手续费率", "en_label": "Origination Fee", "cn_unit": "%", "en_unit": "%", "default": 1},
        ],
        "result_html_cn": """<div style="display:flex;gap:16px;flex-wrap:wrap;margin-bottom:16px">
<div class="result-card"><div class="label">过桥金额</div><div class="value highlight" id="blGap">$0.00</div></div>
<div class="result-card"><div class="label">月度利息</div><div class="value" id="blMonthly">$0.00</div></div>
<div class="result-card"><div class="label">总利息</div><div class="value warn" id="blTotalInterest">$0.00</div></div>
<div class="result-card"><div class="label">总成本</div><div class="value" id="blTotalCost">$0.00</div></div>
</div>""",
        "result_html_en": """<div style="display:flex;gap:16px;flex-wrap:wrap;margin-bottom:16px">
<div class="result-card"><div class="label">Bridge Amount</div><div class="value highlight" id="blGap">$0.00</div></div>
<div class="result-card"><div class="label">Monthly Interest</div><div class="value" id="blMonthly">$0.00</div></div>
<div class="result-card"><div class="label">Total Interest</div><div class="value warn" id="blTotalInterest">$0.00</div></div>
<div class="result-card"><div class="label">Total Cost</div><div class="value" id="blTotalCost">$0.00</div></div>
</div>""",
        "calc_js": """function calcBridge(){
  var price=parseFloat(document.getElementById('blNewPrice').value)||0;
  var dpPct=parseFloat(document.getElementById('blDown').value)||20;
  var equity=parseFloat(document.getElementById('blEquity').value)||0;
  var rate=parseFloat(document.getElementById('blRate').value)||8.5;
  var months=parseInt(document.getElementById('blMonths').value)||6;
  var orig=parseFloat(document.getElementById('blOrigFee').value)||1;
  var downNeeded=price*dpPct/100;
  var gap=Math.max(0, downNeeded-equity);
  var monthlyInterest=gap*rate/100/12;
  var totalInterest=monthlyInterest*months;
  var origFee=gap*orig/100;
  var totalCost=totalInterest+origFee;
  var fmt=function(n){return '$'+n.toFixed(2).replace(/\\B(?=(\\d{3})+(?!\\d))/g,',');};
  document.getElementById('blGap').textContent=fmt(gap);
  document.getElementById('blMonthly').textContent=fmt(monthlyInterest);
  document.getElementById('blTotalInterest').textContent=fmt(totalInterest);
  document.getElementById('blTotalCost').textContent=fmt(totalCost);
}"""
    },
]

# Too complex, let me just write the files directly
print("Switching to direct file generation...")