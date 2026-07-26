#!/usr/bin/env python3
"""批量修复EN页面中文碎片 v8 - 彻底清理"""
import os, re

SITE = '/home/chison/tools-site'

def fix_file(path, replacements):
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        c = f.read()
    original = c
    for old, new in replacements:
        c = c.replace(old, new)
    if c != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(c)
        return True
    return False

# loading-spinner
loading_fixes = [
    ('自定义Color', 'Custom Color'),
    ('常用问题', 'FAQ'),
    ('如何使用Generate', 'How to Use'),
]

# loan-calc
loan_fixes = [
    ('或Equal Principal', 'or Equal Principal'),
    ('ClickCalculate, 查看Monthly Payment、total interestand还款计划表', 'Click Calculate to view monthly payment, total interest and amortization schedule'),
    ('查看Monthly Payment', 'view monthly payment'),
    ('total interestand', 'total interest and'),
    ('还款计划表', 'amortization schedule'),
    ('还款', 'payment'),
]

# mortgage-calc
mortgage_fixes = [
    ('10年', '10 years'),
    ('15年', '15 years'),
    ('20年', '20 years'),
    ('25年', '25 years'),
    ('30年', '30 years'),
    ('年限', 'Term'),
    ('还款方式', 'Method'),
    ('等额本息', 'Equal Installment'),
    ('等额本金', 'Equal Principal'),
    ('月供', 'Monthly Payment'),
    ('总利息', 'Total Interest'),
    ('还款总额', 'Total Payment'),
    ('本金', 'Principal'),
    ('利息', 'Interest'),
    ('首付比例', 'Down Payment %'),
    ('利率', 'Rate'),
    ('计算结果', 'Result'),
]

# percentage-change
pct_fixes = [
    ('Result自动实时Calculate, DisplayPercentageChange、Change量andChange方向', 'Result calculates in real-time, displaying percentage change, change amount and direction'),
    ('自动实时Calculate', 'calculates in real-time'),
    ('DisplayPercentageChange', 'display percentage change'),
    ('Change量', 'change amount'),
    ('Change方向', 'change direction'),
    ('Click「Swap」', 'Click "Swap"'),
    ('按钮交换', 'to swap'),
    ('数值位置', 'values'),
    ('Increase/decrease', 'increase/decrease'),
    ('方向自动判断', 'direction auto-detected'),
    ('结果自动', 'result automatically'),
]

fixes = {
    'loading-spinner': loading_fixes,
    'loan-calc': loan_fixes,
    'mortgage-calc': mortgage_fixes,
    'percentage-change': pct_fixes,
}

fixed = 0
for item, replacements in fixes.items():
    path = os.path.join(SITE, 'en', item, 'index.html')
    if fix_file(path, replacements):
        print(f"FIXED: en/{item}/index.html")
        fixed += 1
    else:
        print(f"SKIP: en/{item}/index.html")

# Helper
def fix_file(path, replacements):
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        c = f.read()
    original = c
    for old, new in replacements:
        c = c.replace(old, new)
    if c != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(c)
        return True
    return False

print(f"\nFixed: {fixed}/{len(fixes)}")