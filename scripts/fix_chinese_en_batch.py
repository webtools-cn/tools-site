#!/usr/bin/env python3
"""Fix chinese_in_en for 5 specific pages - patch body content to English"""
import re, json, os

SITE = '/home/chison/tools-site'

# Translation maps for each file: (old_chinese_str, new_english_str)
# For each file, we patch the body content that has Chinese

# === customer-lifetime-value ===
clv_patches = [
    ('<h2>🔢 Input Parameters</h2>\n    <div class="input-grid" id="inputGrid">\n\n<div class="input-group">\n<label for="arpu">月均ARPU ($)</label>\n<input type="number" id="arpu" value="100" min="0" step="0.01">\n<div class="hint">每位客户月平均收入</div>\n</div>\n<div class="input-group">\n<label for="grossMargin">毛利率 (%)</label>\n<input type="number" id="grossMargin" value="80" min="0" max="100" step="0.1">\n<div class="hint">收入扣除直接成本后的利润率</div>\n</div>\n<div class="input-group">\n<label for="churnRate">月流失率 (%)</label>\n<input type="number" id="churnRate" value="5" min="0.01" max="100" step="0.01">\n<div class="hint">每月取消订阅的客户比例</div>\n</div>\n<div class="input-group">\n<label for="cac">客户获取成本 CAC ($)</label>\n<input type="number" id="cac" value="200" min="0" step="1">\n<div class="hint">获取一个客户的平均花费</div>\n</div>',
     '<h2>🔢 Input Parameters</h2>\n    <div class="input-grid" id="inputGrid">\n\n<div class="input-group">\n<label for="arpu">Monthly ARPU ($)</label>\n<input type="number" id="arpu" value="100" min="0" step="0.01">\n<div class="hint">Average monthly revenue per customer</div>\n</div>\n<div class="input-group">\n<label for="grossMargin">Gross Margin (%)</label>\n<input type="number" id="grossMargin" value="80" min="0" max="100" step="0.1">\n<div class="hint">Profit margin after direct costs</div>\n</div>\n<div class="input-group">\n<label for="churnRate">Monthly Churn Rate (%)</label>\n<input type="number" id="churnRate" value="5" min="0.01" max="100" step="0.01">\n<div class="hint">Percentage of customers cancelling monthly</div>\n</div>\n<div class="input-group">\n<label for="cac">Customer Acquisition Cost CAC ($)</label>\n<input type="number" id="cac" value="200" min="0" step="1">\n<div class="hint">Average cost to acquire one customer</div>\n</div>'),
    ('<div class="label">CLV 客户生命周期价值</div>\n<div class="value" id="clv">', '<div class="label">CLV Customer Lifetime Value</div>\n<div class="value" id="clv">'),
    ('<div class="label">LTV:CAC 比例</div>\n<div class="value" id="ltvCac">', '<div class="label">LTV:CAC Ratio</div>\n<div class="value" id="ltvCac">'),
    ('<div class="sub">健康标准≥3:1</div>', '<div class="sub">Healthy benchmark ≥3:1</div>'),
    ('<div class="label">平均客户生命周期</div>\n<div class="value" id="avgLifetime">', '<div class="label">Avg Customer Lifetime</div>\n<div class="value" id="avgLifetime">'),
    ('<div class="sub">月</div>', '<div class="sub">Months</div>'),
    ('<div class="label">年化ARPU</div>\n<div class="value" id="annualArpu">', '<div class="label">Annualized ARPU</div>\n<div class="value" id="annualArpu">'),
    ('<div class="sub">每位客户年收入</div>', '<div class="sub">Annual revenue per customer</div>'),
    ('<div class="label">盈亏平衡状态</div>\n<div class="value" id="healthStatus">', '<div class="label">Break-Even Status</div>\n<div class="value" id="healthStatus">'),
    ('    var status = \'\';', '    var healthStatus = \'\';'),
    ('    if (ltvCac >= 5) { status = \'优秀\'; sub = \'可加大获客投入\'; }', '    if (ltvCac >= 5) { healthStatus = \'Excellent\'; sub = \'Increase acquisition spend\'; }'),
    ('    else if (ltvCac >= 3) { status = \'健康\'; sub = \'获客投入适中\'; }', '    else if (ltvCac >= 3) { healthStatus = \'Healthy\'; sub = \'Acquisition spend is balanced\'; }'),
    ('    else if (ltvCac >= 1) { status = \'需优化\'; sub = \'减少获客成本或提升CLV\'; }', '    else if (ltvCac >= 1) { healthStatus = \'Needs Optimization\'; sub = \'Reduce CAC or improve CLV\'; }'),
    ('    else { status = \'亏损\'; sub = \'立即调整获客策略\'; }', '    else { healthStatus = \'Loss Making\'; sub = \'Adjust acquisition strategy immediately\'; }'),
    ('    document.getElementById(\'healthStatus\').textContent = status;', '    document.getElementById(\'healthStatus\').textContent = healthStatus;'),
    ('    document.getElementById(\'avgLifetime\').textContent = avgLifetime.toFixed(1) + \' 个月\';', '    document.getElementById(\'avgLifetime\').textContent = avgLifetime.toFixed(1) + \' months\';'),
]

# === equity-dilution-calc ===
equity_patches = [
    ('<label for="founderShares">创始人持股 (%)</label>', '<label for="founderShares">Founder Ownership (%)</label>'),
    ('<div class="hint">当前创始人/现有股东总持股比例</div>\n</div>\n<div class="input-group">\n<label for="newInvestment">新融资额 ($)</label>', '<div class="hint">Current total ownership of founders/existing shareholders</div>\n</div>\n<div class="input-group">\n<label for="newInvestment">New Investment ($)</label>'),
    ('<div class="hint">本轮计划融资金额</div>\n</div>\n<div class="input-group">\n<label for="preMoney">投资前估值 ($)</label>', '<div class="hint">Planned funding amount for this round</div>\n</div>\n<div class="input-group">\n<label for="preMoney">Pre-Money Valuation ($)</label>'),
    ('<div class="hint">融资前公司估值</div>\n</div>\n<div class="input-group">\n<label for="esopPct">ESOP期权池 (%)</label>', '<div class="hint">Company valuation before funding</div>\n</div>\n<div class="input-group">\n<label for="esopPct">ESOP Option Pool (%)</label>'),
    ('<div class="hint">员工期权池预留比例(融资前设立)</div>', '<div class="hint">Employee option pool reserved before funding</div>'),
    ('<div class="label">投资后估值</div>', '<div class="label">Post-Money Valuation</div>'),
    ('<div class="label">投资人持股</div>', '<div class="label">Investor Ownership</div>'),
    ('<div class="sub">新投资人股权比例</div>', '<div class="sub">New investor equity percentage</div>'),
    ('<div class="label">创始人持股</div>', '<div class="label">Founder Ownership</div>'),
    ('<div class="sub">含ESOP稀释后</div>', '<div class="sub">After ESOP dilution</div>'),
    ('<div class="label">ESOP期权池</div>', '<div class="label">ESOP Option Pool</div>'),
    ('<div class="sub">员工期权占比</div>', '<div class="sub">Employee option percentage</div>'),
    ('<div class="label">总稀释比例</div>', '<div class="label">Total Dilution</div>'),
    ('<div class="sub">创始人被稀释百分比</div>', '<div class="sub">Founder dilution percentage</div>'),
    ('.textContent = dilution.toFixed(2) + \'个百分点\'', '.textContent = dilution.toFixed(2) + \' percentage points\''),
]

# === federal-tax-calc ===
tax_patches = [
    ('<label for="grossIncome">年总收入 ($)</label>', '<label for="grossIncome">Annual Gross Income ($)</label>'),
    ('<div class="hint">税前年度总收入 (W2工资)</div>', '<div class="hint">Pre-tax annual income (W2 wages)</div>'),
    ('<label for="filingStatus">申报状态</label>', '<label for="filingStatus">Filing Status</label>'),
    ('<option value="single">单身 (Single)</option>', '<option value="single">Single</option>'),
    ('<option value="mfj">夫妻合并 (MFJ)</option>', '<option value="mfj">Married Filing Jointly (MFJ)</option>'),
    ('<option value="hoh">户主 (HoH)</option>', '<option value="hoh">Head of Household (HoH)</option>'),
    ('<div class="hint">您的IRS申报状态</div>', '<div class="hint">Your IRS filing status</div>'),
    ('<label for="extraDeduction">额外扣除额 ($)</label>', '<label for="extraDeduction">Additional Deductions ($)</label>'),
    ('<div class="hint">401k/IRA/HSA等税前列支项目总计</div>', '<div class="hint">Total pre-tax deductions: 401k/IRA/HSA etc.</div>'),
    ('<div class="label">应缴联邦税款</div>', '<div class="label">Federal Tax Liability</div>'),
    ('<div class="label">有效税率</div>', '<div class="label">Effective Tax Rate</div>'),
    ('<div class="label">边际税率</div>', '<div class="label">Marginal Tax Rate</div>'),
    ('<div class="label">应税收入</div>', '<div class="label">Taxable Income</div>'),
    ('<div class="sub">扣除标准/额外扣除后</div>', '<div class="sub">After standard/extra deductions</div>'),
    ('<div class="label">税后收入</div>', '<div class="label">After-Tax Income</div>'),
]

# === freelance-tax-calc ===
freelance_patches = [
    ('<label for="netIncome">年度自由职业净收入 ($)</label>', '<label for="netIncome">Annual Freelance Net Income ($)</label>'),
    ('<div class="hint">扣除业务支出后的净收入</div>', '<div class="hint">Net income after business expenses</div>'),
    ('<label for="businessExpenses">业务支出 ($)</label>', '<label for="businessExpenses">Business Expenses ($)</label>'),
    ('<div class="hint">可抵扣业务支出总额</div>', '<div class="hint">Total deductible business expenses</div>'),
    ('<label for="filingStatus">申报状态</label>\n<select id="filingStatus">\n<option value="single">单身 (Single)</option>\n<option value="mfj">夫妻合并 (MFJ)</option>', '<label for="filingStatus">Filing Status</label>\n<select id="filingStatus">\n<option value="single">Single</option>\n<option value="mfj">Married Filing Jointly (MFJ)</option>'),
    ('<label for="otherIncome">其他收入 ($)</label>', '<label for="otherIncome">Other Income ($)</label>'),
    ('<div class="hint">W2工资/投资收益等(如有)</div>', '<div class="hint">W2 wages/investment income etc. (if any)</div>'),
    ('<div class="label">总税负</div>', '<div class="label">Total Tax Burden</div>'),
    ('<div class="sub">自雇税 + 联邦所得税</div>', '<div class="sub">SE Tax + Federal Income Tax</div>'),
    ('<div class="label">自雇税 (SE Tax)</div>', '<div class="label">Self-Employment Tax (SE Tax)</div>'),
    ('<div class="sub">社安+医保 15.3%</div>', '<div class="sub">Social Security + Medicare 15.3%</div>'),
    ('<div class="label">联邦所得税</div>', '<div class="label">Federal Income Tax</div>'),
    ('<div class="sub">含QBI扣除和SE税抵扣</div>', '<div class="sub">With QBI deduction & SE tax deduction</div>'),
    ('<div class="label">有效税率</div>\n<div class="value" id="effectiveRate">', '<div class="label">Effective Tax Rate</div>\n<div class="value" id="effectiveRate">'),
    ('<div class="sub">总税负/总收入</div>', '<div class="sub">Total Tax / Total Income</div>'),
    ('<div class="label">税后收入</div>', '<div class="label">Take-Home Pay</div>'),
    ('<div class="sub">实际到手年收入</div>', '<div class="sub">Actual annual take-home pay</div>'),
    ('<div class="label">季度预缴额</div>', '<div class="label">Quarterly Estimated Payment</div>'),
    ('<div class="sub">建议每季度预缴</div>', '<div class="sub">Suggested quarterly payment</div>'),
]

# === revenue-projection ===
revenue_patches = [
    ('<label for="initMrr">初始月收入 MRR ($)</label>', '<label for="initMrr">Initial Monthly Revenue MRR ($)</label>'),
    ('<div class="hint">当前月经常性收入</div>', '<div class="hint">Current monthly recurring revenue</div>'),
    ('<label for="growthRate">月增长率 (%)</label>', '<label for="growthRate">Monthly Growth Rate (%)</label>'),
    ('<div class="hint">预期月环比增长率</div>', '<div class="hint">Expected month-over-month growth rate</div>'),
    ('<label for="months">预测月数</label>', '<label for="months">Forecast Months</label>'),
    ('<div class="hint">预测时间跨度(1-60个月)</div>', '<div class="hint">Forecast time span (1-60 months)</div>'),
    ('<label for="growthMode">增长模式</label>', '<label for="growthMode">Growth Mode</label>'),
    ('<option value="mom">月环比增长 (MoM)</option>', '<option value="mom">Month-over-Month (MoM)</option>'),
    ('<option value="yoy">年同比增长 (YoY)</option>', '<option value="yoy">Year-over-Year (YoY)</option>'),
    ('<div class="hint">选择增长计算方式</div>', '<div class="hint">Select growth calculation method</div>'),
    ('<div class="label">期末月收入 MRR</div>', '<div class="label">Ending Monthly Revenue MRR</div>'),
    ('<div class="sub">预测期末月收入</div>', '<div class="sub">Forecast ending monthly revenue</div>'),
    ('<div class="label">期末年化收入 ARR</div>', '<div class="label">Ending Annualized Revenue ARR</div>'),
    ('<div class="sub">期末年度经常性收入</div>', '<div class="sub">Forecast ending annual recurring revenue</div>'),
    ('<div class="label">总收入CAGR</div>', '<div class="label">Total Revenue CAGR</div>'),
    ('<div class="sub">复合年增长率</div>', '<div class="sub">Compound annual growth rate</div>'),
    ('<div class="label">累计总收入</div>', '<div class="label">Cumulative Total Revenue</div>'),
    ('<div class="sub">整个预测期总收入</div>', '<div class="sub">Total revenue over the forecast period</div>'),
]

file_patches = {
    'en/customer-lifetime-value/index.html': clv_patches,
    'en/equity-dilution-calc/index.html': equity_patches,
    'en/federal-tax-calc/index.html': tax_patches,
    'en/freelance-tax-calc/index.html': freelance_patches,
    'en/revenue-projection/index.html': revenue_patches,
}

for fname, patches in file_patches.items():
    fpath = os.path.join(SITE, fname)
    with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    for old, new in patches:
        if old in content:
            content = content.replace(old, new)
        else:
            print(f"  WARN: patch not found in {fname}: {old[:60]}...")
    
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    # verify no Chinese left
    cn = re.findall(r'[\u4e00-\u9fff]+', content)
    print(f"  {fname}: {len(cn)} Chinese chars remaining: {cn[:5]}")
    
print("\nDone!")
