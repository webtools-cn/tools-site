#!/usr/bin/env python3
"""Fix Chinese text in EN calculator JS output."""
import os

# Translation map: Chinese -> English
TRANSLATIONS = {
    # Error messages
    "'请输入有效数值'": "'Please enter valid numbers'",
    "'分母不能为零'": "'Denominator cannot be zero'",
    # Investment return
    "'收益额: <strong>'": "'Profit: <strong>'",
    "'回报率: <strong style=\"'": "'ROI: <strong style=\"'",
    "'%</strong>'": "'%</strong>'",  # keep as is
    # Loan installment
    "'每月还款: <strong>'": "'Monthly Payment: <strong>'",
    "'总还款额: <strong>'": "'<br>Total Payment: <strong>'",
    "'总利息: <strong>'": "'<br>Total Interest: <strong>'",
    # Marketing ROI
    "'利润: <strong>'": "'<br>Profit: <strong>'",
    "'获客成本: <strong>'": "'<br>Cost Per Acquisition: <strong>'",
    # Simplify fractions
    "'最简分数: <strong>'": "'Simplest Form: <strong>'",
    "'小数: <strong>'": "'<br>Decimal: <strong>'",
    "'带分数: <strong>'": "'<br>Mixed Number: <strong>'",
    # SIP return
    "'总投资: <strong>'": "'Total Invested: <strong>'",
    "'最终价值: <strong>'": "'<br>Final Value: <strong>'",
    "'收益: <strong>'": "'<br>Gain: <strong>'",
    # Rule of 72
    "'翻倍约需: <strong>'": "'Doubles in approx: <strong>'",
    "' 年</strong>'": "' years</strong>'",
    "'注: 72法则为近似估算，精确值为 ln(2)/ln(1+r) ≈ '": "'Note: Rule of 72 is an approximation. Exact value: ln(2)/ln(1+r) ≈ '",
    # NPV - check verdict text
    "'值得投资'": "'Worth investing'",
    "'不建议投资'": "'Not recommended'",
    "'NPV: '": "'NPV: '",  # already English
    # SEO section
    "'输入第一个参数'": "'Enter the first parameter'",
    "'输入第二个参数'": "'Enter the second parameter'",
    "'点击\"计算\"按钮查看结果'": "'Click the Calculate button to see results'",
    # Toast
    "'请输入有效数值'": "'Please enter valid numbers'",
}

TOOLS = [
    "investment-return-calculator",
    "loan-installment-calculator",
    "marketing-roi-calculator",
    "simplify-fractions",
    "sip-return-calculator",
    "net-present-value",
    "rule-72-calculator",
    "daily-calorie-burn",
]

fixed = []
for tool in TOOLS:
    path = f"en/{tool}/index.html"
    if not os.path.exists(path):
        continue
    
    with open(path, 'r') as f:
        content = f.read()
    
    original = content
    for cn, en in TRANSLATIONS.items():
        content = content.replace(cn, en)
    
    # Also fix the "如何使用" heading and "关于" heading in EN
    content = content.replace('>关于 ', '>About ')
    content = content.replace('>如何使用<', '>How to Use<')
    content = content.replace('计算公式基于标准数学公式，结果精确可靠。', 'Calculations are based on standard mathematical formulas, results are accurate and reliable.')
    content = content.replace('完全不需要，打开网页即可使用，纯前端计算。', 'No download needed. Open the page and use it immediately, all calculations run in your browser.')
    content = content.replace('这个工具准确吗？', 'Is this tool accurate?')
    content = content.replace('需要下载吗？', 'Do I need to download anything?')
    
    # Fix FAQ schema
    content = content.replace('"这个工具准确吗？"', '"Is this tool accurate?"')
    content = content.replace('"需要下载吗？"', '"Do I need to download anything?"')
    content = content.replace('计算公式基于标准数学公式，结果精确可靠。', 'Calculations are based on standard mathematical formulas, results are accurate and reliable.')
    content = content.replace('完全不需要，打开网页即可使用，纯前端计算。', 'No download needed. Open the page and use it immediately, all calculations run in your browser.')
    
    if content != original:
        with open(path, 'w') as f:
            f.write(content)
        fixed.append(path)

print(f"Fixed: {len(fixed)}")
for f in fixed:
    print(f"  ✅ {f}")
