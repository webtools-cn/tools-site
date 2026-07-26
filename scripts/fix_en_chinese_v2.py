#!/usr/bin/env python3
"""第二轮修复EN页面中文残留"""
import re, os

SITE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(SITE)

# 具体页面中文→英文映射
PAGE_FIXES = {
    'a1c-calculator': {
        '输入HbA1c值': 'Enter HbA1c Value',
        'HbA1c (%)': 'HbA1c (%)',
        '血糖单位': 'Blood Sugar Unit',
        '估算平均血糖 (eAG)': 'Estimated Average Glucose (eAG)',
        '血糖控制水平': 'Blood Sugar Control Level',
        '什么是HbA1c？': 'What is HbA1c?',
        'HbA1c（糖化血红蛋白）反映过去2-3个月的平均血糖水平。正常值低于5.7%，糖尿病前期为5.7%-6.4%，糖尿病≥6.5%。': 'HbA1c (glycated hemoglobin) reflects average blood sugar over the past 2-3 months. Normal: below 5.7%, Prediabetes: 5.7%-6.4%, Diabetes: ≥6.5%.',
        'eAG是什么意思？': 'What is eAG?',
        'eAG（估算平均血糖）是将HbA1c百分比转换为日常血糖监测单位的值。公式：eAG(mg/dL) = 28.7 × A1C - 46.7。': 'eAG (estimated Average Glucose) converts HbA1c percentage to daily blood sugar monitoring units. Formula: eAG(mg/dL) = 28.7 × A1C - 46.7.',
        'mg/dL': 'mg/dL',  # no change needed
        'mmol/L': 'mmol/L',  # no change needed
        '计算': 'Calculate',
    },
    'calorie-deficit-calculator': {
        '性别': 'Gender',
        '男': 'Male',
        '女': 'Female',
        '年龄': 'Age',
        '身高 (cm)': 'Height (cm)',
        '体重 (kg)': 'Weight (kg)',
        '活动水平': 'Activity Level',
        '久坐（几乎不运动）': 'Sedentary (little or no exercise)',
        '轻度活跃（每周1-3天）': 'Lightly active (1-3 days/week)',
        '中度活跃（每周3-5天）': 'Moderately active (3-5 days/week)',
        '非常活跃（每周6-7天）': 'Very active (6-7 days/week)',
        '极度活跃（高强度体力劳动）': 'Extra active (intense physical labor)',
        '目标减重速度': 'Target Weight Loss Rate',
        '温和（每周减0.25kg）': 'Mild (0.25kg/week)',
        '标准（每周减0.5kg）': 'Standard (0.5kg/week)',
        '快速（每周减0.75kg）': 'Fast (0.75kg/week)',
        '极速（每周减1kg）': 'Rapid (1kg/week)',
        '基础代谢率 (BMR)': 'Basal Metabolic Rate (BMR)',
        '每日总能量消耗 (TDEE)': 'Total Daily Energy Expenditure (TDEE)',
        '目标每日摄入': 'Target Daily Intake',
        '每日热量缺口': 'Daily Calorie Deficit',
        '预计每周减重': 'Estimated Weekly Weight Loss',
        '什么是热量缺口？': 'What is a calorie deficit?',
        '热量缺口 = 消耗的热量 - 摄入的热量。当缺口为正值时，身体会消耗脂肪储备来弥补能量差，从而实现减重。': 'Calorie deficit = calories burned - calories consumed. When the deficit is positive, the body uses fat reserves to make up the energy difference, leading to weight loss.',
        '安全减重速度是多少？': 'What is a safe rate of weight loss?',
        '建议每周减重0.5-1kg。过快的减重可能导致肌肉流失、营养不良和代谢下降。': 'A safe rate is 0.5-1kg per week. Faster weight loss may lead to muscle loss, malnutrition, and metabolic slowdown.',
    },
    'capital-gains-tax-calculator': {
        '资产类型': 'Asset Type',
        '股票': 'Stocks',
        '房产': 'Real Estate',
        '加密货币': 'Cryptocurrency',
        '其他': 'Other',
        '买入价格 ($)': 'Purchase Price ($)',
        '卖出价格 ($)': 'Selling Price ($)',
        '持有时间': 'Holding Period',
        '短期（≤1年）': 'Short-term (≤1 year)',
        '长期（>1年）': 'Long-term (>1 year)',
        '年收入 ($)': 'Annual Income ($)',
        '资本利得': 'Capital Gain',
        '适用税率': 'Applicable Tax Rate',
        '应缴税额': 'Tax Owed',
        '税后利润': 'After-Tax Profit',
        '什么是资本利得税？': 'What is capital gains tax?',
        '资本利得税是对出售资产所得利润征收的税。短期利得通常按普通所得税率征税，长期利得享有优惠税率。': 'Capital gains tax is levied on profits from selling assets. Short-term gains are typically taxed at ordinary income rates, while long-term gains enjoy preferential rates.',
        '长期和短期如何区分？': 'What is the difference between long-term and short-term?',
        '持有超过1年属于长期资本利得，享受较低税率；持有1年及以下属于短期，按普通所得税率征税。': 'Holding over 1 year is long-term capital gains with lower tax rates; holding 1 year or less is short-term, taxed at ordinary income rates.',
    },
    'cholesterol-ratio-calculator': {
        '总胆固醇 (mg/dL)': 'Total Cholesterol (mg/dL)',
        'HDL胆固醇 (mg/dL)': 'HDL Cholesterol (mg/dL)',
        'LDL胆固醇 (mg/dL)': 'LDL Cholesterol (mg/dL)',
        '甘油三酯 (mg/dL)': 'Triglycerides (mg/dL)',
        '总胆固醇/HDL比率': 'Total Cholesterol/HDL Ratio',
        'LDL/HDL比率': 'LDL/HDL Ratio',
        '甘油三酯/HDL比率': 'Triglycerides/HDL Ratio',
        '非HDL胆固醇': 'Non-HDL Cholesterol',
        '风险评估': 'Risk Assessment',
        '什么是胆固醇比率？': 'What is cholesterol ratio?',
        '胆固醇比率是评估心血管疾病风险的重要指标。总胆固醇/HDL比值越低越好，理想值<3.5。': 'Cholesterol ratio is an important indicator for assessing cardiovascular disease risk. Lower Total/HDL ratio is better, ideal value <3.5.',
        '正常范围是多少？': 'What are normal ranges?',
        '总胆固醇/HDL：理想<3.5，正常3.5-5.0，偏高>5.0。LDL/HDL：理想<2.0，正常2.0-3.0，偏高>3.0。': 'Total/HDL: ideal <3.5, normal 3.5-5.0, high >5.0. LDL/HDL: ideal <2.0, normal 2.0-3.0, high >3.0.',
    },
    'self-employment-tax-calculator': {
        '净自雇收入 ($)': 'Net Self-Employment Income ($)',
        '自雇税率': 'Self-Employment Tax Rate',
        '社会保障税 (12.4%)': 'Social Security Tax (12.4%)',
        '医疗保险税 (2.9%)': 'Medicare Tax (2.9%)',
        '社保税': 'Social Security Tax',
        '医保税': 'Medicare Tax',
        '总自雇税': 'Total Self-Employment Tax',
        '可扣除部分（50%）': 'Deductible Portion (50%)',
        '什么是自雇税？': 'What is self-employment tax?',
        '自雇税是美国自雇人士（自由职业者、独立承包商等）需要缴纳的社会保障和医疗保险税。2024年税率为15.3%（12.4%社会保障+2.9%医疗保险）。': 'Self-employment tax is the Social Security and Medicare tax that US self-employed individuals (freelancers, independent contractors, etc.) must pay. The 2024 rate is 15.3% (12.4% Social Security + 2.9% Medicare).',
        '可以抵扣吗？': 'Is it deductible?',
        '自雇税的一半（50%）可以从应纳税所得额中扣除，这有助于降低个人所得税负担。': 'Half (50%) of self-employment tax can be deducted from taxable income, which helps reduce personal income tax burden.',
    },
    'capm-calculator': {
        '无风险利率 (%)': 'Risk-Free Rate (%)',
        '市场期望收益率 (%)': 'Expected Market Return (%)',
        '贝塔系数 (β)': 'Beta Coefficient (β)',
        '期望收益率': 'Expected Return',
        '市场风险溢价': 'Market Risk Premium',
        '什么是CAPM？': 'What is CAPM?',
        'CAPM（资本资产定价模型）用于计算资产的期望收益率。公式：E(Ri) = Rf + β × (Rm - Rf)。': 'CAPM (Capital Asset Pricing Model) calculates expected return of an asset. Formula: E(Ri) = Rf + β × (Rm - Rf).',
        '贝塔系数代表什么？': 'What does Beta represent?',
        'β衡量资产相对于市场的系统性风险。β=1表示与市场同步，β>1表示波动性高于市场，β<1表示波动性低于市场。': 'Beta measures systematic risk relative to the market. β=1 means moving with the market, β>1 means higher volatility, β<1 means lower volatility.',
    },
    'sharpe-ratio': {
        '投资组合年化收益率 (%)': 'Portfolio Annual Return (%)',
        '无风险利率 (%)': 'Risk-Free Rate (%)',
        '年化标准差 (%)': 'Annual Standard Deviation (%)',
        'Sharpe Ratio': 'Sharpe Ratio',
        '超额收益': 'Excess Return',
        '风险评估': 'Risk Assessment',
        '什么是Sharpe Ratio？': 'What is Sharpe Ratio?',
        '夏普比率衡量投资组合每单位风险的超额回报。公式：(Rp - Rf) / σp。值越高，风险调整后回报越好。': 'Sharpe Ratio measures excess return per unit of risk. Formula: (Rp - Rf) / σp. Higher values indicate better risk-adjusted returns.',
        '好的夏普比率是多少？': 'What is a good Sharpe Ratio?',
        '<1：低于平均水平，1-2：良好，2-3：非常好，>3：优秀。': '<1: Below average, 1-2: Good, 2-3: Very good, >3: Excellent.',
    },
    'debt-payoff-calculator': {
        '债务总额 ($)': 'Total Debt ($)',
        '年利率 (%)': 'Annual Interest Rate (%)',
        '每月还款额 ($)': 'Monthly Payment ($)',
        '额外还款 ($/月)': 'Extra Payment ($/month)',
        '还款方式': 'Repayment Method',
        '雪球法（先还最小额）': 'Snowball (smallest first)',
        '雪崩法（先还最高利率）': 'Avalanche (highest interest first)',
        '还清时间': 'Payoff Time',
        '总利息': 'Total Interest',
        '总还款额': 'Total Payment',
        '什么是雪球法和雪崩法？': 'What are Snowball and Avalanche methods?',
        '雪球法：先还清最小余额的债务，获得心理成就感。雪崩法：先还清最高利率的债务，数学上最优，节省更多利息。': 'Snowball: pay off smallest balance first for psychological wins. Avalanche: pay off highest interest first, mathematically optimal, saves more interest.',
    },
    'dividend-calculator': {
        '持股数量': 'Number of Shares',
        '每股股息 ($)': 'Dividend Per Share ($)',
        '股息频率': 'Dividend Frequency',
        '每季度': 'Quarterly',
        '每半年': 'Semi-Annually',
        '每年': 'Annually',
        '每月': 'Monthly',
        '年度股息收入': 'Annual Dividend Income',
        '股息率': 'Dividend Yield',
        '每股价格 ($)': 'Price Per Share ($)',
        '什么是股息率？': 'What is dividend yield?',
        '股息率 = 年度每股股息 / 每股价格。它衡量股票通过股息产生的投资回报率。': 'Dividend yield = annual dividend per share / price per share. It measures the investment return from dividends.',
    },
}

def fix_en_page(tool_name):
    path = os.path.join(SITE, 'en', tool_name, 'index.html')
    if not os.path.exists(path):
        return False
    
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    original = content
    fixes = PAGE_FIXES.get(tool_name, {})
    
    # Common fixes for all pages
    common_fixes = {
        '中文': '中文',  # Keep this in lang-switch as label
        '清空': 'Clear',
    }
    
    all_fixes = {**common_fixes, **fixes}
    
    # Sort by length (longest first) to avoid partial replacements
    for cn, en_text in sorted(all_fixes.items(), key=lambda x: -len(x[0])):
        if cn == en_text:
            continue
        # Only replace in text content, not in tags/attributes
        # Strategy: replace exact matches in the HTML
        content = content.replace(cn, en_text)
    
    if content != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    en_tools = [
        'a1c-calculator', 'calorie-deficit-calculator', 'capital-gains-tax-calculator',
        'cholesterol-ratio-calculator', 'self-employment-tax-calculator',
        'capm-calculator', 'sharpe-ratio', 'debt-payoff-calculator', 'dividend-calculator',
        'beta-calculator',
    ]
    
    fixed = 0
    for tool in en_tools:
        if tool not in PAGE_FIXES:
            continue
        result = fix_en_page(tool)
        if result:
            fixed += 1
            print(f"  ✅ Fixed: en/{tool}/")
        else:
            print(f"  ⚠️ No changes: en/{tool}/")
    
    print(f"\nFixed {fixed} pages")

if __name__ == '__main__':
    main()