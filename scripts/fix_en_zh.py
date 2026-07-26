#!/usr/bin/env python3
"""修复英文版残留中文"""
import os, re

SITE = '/home/chison/tools-site/en'
tools = ['biweekly-payment-calculator', 'extra-payment-calculator', 'balloon-payment-calculator', 'arm-vs-fixed-calculator', 'home-equity-calculator']

# Patterns to fix
FIXES = [
    # keywords
    ('浮动vsFixed Rate', 'ARM vs Fixed Rate'),
    ('ARM计算器', 'ARM Calculator'),
    ('可调利率', 'Adjustable Rate'),
    ('房贷对比', 'Mortgage Comparison'),
    ('在线Tools', 'Online Tools'),
    ('免费', 'Free'),
    # og:description & schema descriptions
    ('免费浮动vsFixed Rate对比计算器，模拟ARM可调利率贷款在不同场景下的总成本。帮助选择最优房贷方案。', 
     'Free ARM vs fixed rate comparison calculator. Simulate adjustable-rate mortgages vs fixed-rate loans under different rate scenarios to compare total costs.'),
    ('免费双周还款计算器，比较双周还款与月供的利息节省。输入贷款金额、利率、期限，查看提前还清时间和节省利息。',
     'Free biweekly payment calculator. Compare biweekly vs monthly payments to see interest savings and early payoff. Input loan amount, rate, and term to calculate savings.'),
    ('免费额外还款计算器，计算在月供基础上额外多还本金可节省的利息和缩短的还款期限。',
     'Free extra payment calculator. See how making additional principal payments saves interest and shortens your loan term.'),
    ('免费气球贷款计算器，计算期末一次性大额还款（Balloon Payment）的月供和总成本。',
     'Free balloon payment calculator. Calculate monthly payments and total cost with a large end-of-term balloon payment.'),
    ('免费房屋净值计算器，计算房产净值和可贷额度。',
     'Free home equity calculator. Calculate your home equity and borrowing capacity.'),
    # HowTo names & steps
    ('如何使用ARM vs Fixed Rate Calculator', 'How to Use ARM vs Fixed Rate Calculator'),
    ('输入Loan Parameters', 'Enter Loan Parameters'),
    ('输入贷款金额、Fixed Rate、浮动起始利率、调整后利率和固定期月数', 'Enter loan amount, fixed rate, ARM initial rate, adjusted rate, and fixed period'),
    ('查看对比结果', 'View Comparison Results'),
    ('查看Fixed Rate和浮动利率的月供对比和Total Interest差', 'Compare monthly payments and total interest between fixed and ARM'),
    ('一键复制对比结果', 'One-click copy comparison results'),
    ('Copy Results', 'Copy Results'),
    # Schema breadcrumb
    ('"name":"Home"', '"name":"Home"'),
    ('"name":"Tools"', '"name":"Tools"'),
    # Remaining Chinese in body
    ('如何', 'How to'),
    ('输入内容', 'Enter content'),
    ('设置参数', 'Set parameters'),
    ('执行操作', 'Execute'),
    ('获取结果', 'Get results'),
    ('如何使用', 'How to use'),
    # Any remaining
    ('贷款金额', 'Loan Amount'),
    ('利率', 'Rate'),
    ('期限', 'Term'),
    ('房贷', 'Mortgage'),
    ('还款', 'Payment'),
]

for tool in tools:
    path = os.path.join(SITE, tool, 'index.html')
    if not os.path.exists(path): continue
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    modified = False
    for old, new in FIXES:
        if old in content:
            content = content.replace(old, new)
            modified = True
    
    if modified:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed: {tool}")
    else:
        print(f"Clean: {tool}")

print("Done")