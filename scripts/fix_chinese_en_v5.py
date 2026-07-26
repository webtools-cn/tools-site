#!/usr/bin/env python3
"""批量修复EN页面中文碎片 v5 - 基于实际检测结果全面修复"""
import os, re, sys

SITE = '/home/chison/tools-site'
CN_RE = re.compile(r'[\u4e00-\u9fff]')

# 全面的中文→英文映射
FIX_MAP = [
    # 通用碎片（多个页面都有）
    ('数据绝不Upload服务器', 'Data never leaves your device'),
    ('零依赖·可离线使用', 'Zero dependencies · Works offline'),
    ('问题反馈: dexshuang@google.com', 'Feedback: dexshuang@google.com'),
    ('房价', 'home price'),
    ('Input房价和', 'Input home price and'),
    ('InputOriginal', 'Input original'),
    ('和New Value', ' and new value'),
    ('自动CalculateIncrease或Decrease的PercentageChange', 'auto-calculates percentage increase or decrease'),
    ('自动Calculate', 'auto-calculates'),
    ('，自动Calculate每Monthly额和总Interest', ', auto-calculates monthly payment and total interest'),
    ('期限', 'term'),
    ('，InputLoan Amount、Annual Rate和term, auto-calculates每Monthly额和总Interest', ', input loan amount, annual rate and term, auto-calculates monthly payment and total interest'),
    ('InputLoan Amount、Annual Rate和term', 'Input loan amount, annual rate and term'),
    ('Select币种', 'Select currency'),
    ('人民币', 'CNY'),
    ('美元', 'USD'),
    ('Check拼写', 'Check spelling'),
    ('等待Input', 'Waiting for input'),
    ('虚拟钢琴键盘', 'Virtual Piano Keyboard'),
    ('和', 'and'),
    ('种', ''),
    ('空格', 'spaces'),
    ('可视化', 'visually'),
    ('，', ', '),
    ('可视化Select', 'visually select'),
    ('，实时Preview效果并一键Copy', ', preview effects in real-time and copy with one click'),
    ('实时Preview效果并一键Copy', 'preview effects in real-time and copy with one click'),
    ('可视化配置打字速度、Cursor Style、De', 'visually configure typing speed, cursor style, de'),
    ('打字速度、Cursor Style', 'typing speed, cursor style'),
    ('可视化配置', 'visually configure'),
    ('Equal Installment和Equal Principal两种Repayment Method，提供详细还款计划表', 'Equal Installment and Equal Principal repayment methods with detailed amortization schedule'),
    ('两种Repayment Method，提供详细还款计划表', 'repayment methods with detailed amortization schedule'),
    ('提供详细还款计划表', 'with detailed amortization schedule'),
    ('InputLoan Amount、Annual Rate', 'Input loan amount, annual rate'),
    ('自动Calculate每Monthly额', 'auto-calculates monthly payment'),
    ('Monthly额', 'monthly payment'),
    ('总Interest', 'total interest'),
    ('Input房价', 'Input home price'),
    ('Down Payment', 'down payment'),
    ('自动CalculateMonthly Payment', 'auto-calculates monthly payment'),
]

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        original = f.read()
    content = original

    changed = False
    for cn, en in FIX_MAP:
        if cn in content:
            content = content.replace(cn, en)
            changed = True

    if changed:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

# 从quality_loop_result获取目标页面列表
targets = [
    'expense-splitter', 'grams-to-cups', 'grams-to-ounces', 'indent-formatter',
    'kelvin-to-celsius', 'loading-spinner', 'loan-calc', 'military-time-converter',
    'money-counter', 'mortgage-calc', 'one-rep-max', 'percentage-change',
    'roman-numerals', 'spell-checker', 'square-meter-to-square-foot',
    'typewriter-effect', 'unicode-decode', 'virtual-piano-keyboard'
]

fixed = 0
for item in targets:
    path = os.path.join(SITE, 'en', item, 'index.html')
    if not os.path.exists(path):
        print(f"NOT FOUND: en/{item}/index.html")
        continue
    if fix_file(path):
        print(f"FIXED: en/{item}/index.html")
        fixed += 1
    else:
        print(f"SKIP: en/{item}/index.html (no changes)")

print(f"\nFixed: {fixed}/{len(targets)}")