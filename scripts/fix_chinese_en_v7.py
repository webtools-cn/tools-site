#!/usr/bin/env python3
"""批量修复EN页面中文碎片 v7 - 逐一处理所有残留"""
import os, re

SITE = '/home/chison/tools-site'

def fix_loading_spinner(c):
    c = c.replace('前端开发必备Tools', 'Essential tool for frontend developers')
    return c

def fix_loan_calc(c):
    # 修复表格和描述中的中文
    c = c.replace('每monthly payment', 'Monthly Payment')
    c = c.replace('InputLoan Amount（如100000）。', 'Input loan amount (e.g. 100000).')
    c = c.replace('InputAnnual Rate（如商业贷款基准利率4.9%）。', 'Input annual rate (e.g. 4.9%).')
    c = c.replace('Select l', 'Select l')
    # 修复表格头
    c = re.sub(r'<th[^>]*>期数</th>', '<th>Period</th>', c)
    c = re.sub(r'<th[^>]*>每monthly payment</th>', '<th>Monthly Payment</th>', c)
    c = re.sub(r'<th[^>]*>本金</th>', '<th>Principal</th>', c)
    c = re.sub(r'<th[^>]*>利息</th>', '<th>Interest</th>', c)
    c = re.sub(r'<th[^>]*>剩余Principal</th>', '<th>Remaining</th>', c)
    # 通用中文残留
    c = c.replace('等额本息', 'Equal Installment')
    c = c.replace('等额本金', 'Equal Principal')
    c = c.replace('贷款金额', 'Loan Amount')
    c = c.replace('年利率', 'Annual Rate')
    c = c.replace('贷款期限', 'Loan Term')
    c = c.replace('年', 'year')
    c = re.sub(r'(\\d+)年', r'\1 year', c)
    # 表格内的数字
    c = re.sub(r'(\d+)期', r'\1', c)
    return c

def fix_money_counter(c):
    c = c.replace('总计：', 'Total:')
    c = c.replace('清零', 'Clear')
    c = c.replace('币种', 'Currency')
    c = c.replace('数量', 'Quantity')
    c = c.replace('面额', 'Denomination')
    return c

def fix_mortgage_calc(c):
    c = c.replace('and equal金两方式, 购房预算规划必备Tools', 'and equal principal methods. Essential tool for home budget planning')
    c = c.replace('Input房价（如500000）。', 'Input home price (e.g. 500000).')
    c = c.replace('Input首付（如150000）。', 'Input down payment (e.g. 150000).')
    c = c.replace('购房预算规划必备Tools', 'Essential tool for home budget planning')
    c = c.replace('金两方式', 'principal methods')
    c = c.replace('等额本息', 'Equal Installment')
    c = c.replace('等额本金', 'Equal Principal')
    c = c.replace('房价', 'Home Price')
    c = c.replace('首付', 'Down Payment')
    c = c.replace('利率', 'Rate')
    c = c.replace('期限', 'Term')
    c = c.replace('还款', 'Payment')
    c = c.replace('月供', 'Monthly')
    c = c.replace('总利息', 'Total Interest')
    c = c.replace('还款总额', 'Total Payment')
    c = c.replace('剩余', 'Remaining')
    c = c.replace('本金', 'Principal')
    c = c.replace('利息', 'Interest')
    c = c.replace('元', '')
    # 修复How to Use
    c = re.sub(r'(\d)\. ([^<]+)（([^)]+)）', r'\1. \2(\3)', c)
    return c

def fix_percentage_change(c):
    c = c.replace('在「Original Value」Input框中InputChange前的数值。', 'Enter the original value in the "Original Value" input box.')
    c = c.replace('在「New Value」Input框中InputChange后的数值。', 'Enter the new value in the "New Value" input box.')
    c = c.replace('在「', 'in the "')
    c = c.replace('」Input框中Input', '" input box, enter')
    c = c.replace('前的数值。', ' the before value.')
    c = c.replace('后的数值。', ' the after value.')
    c = c.replace('数据分', 'data analy')
    c = c.replace('必备', 'essential')
    c = c.replace('数据分析', 'data analysis')
    c = c.replace('反向Calculate', 'reverse calculation')
    c = c.replace('正负Increase', 'positive/negative change')
    c = c.replace('Increase、', 'increase,')
    c = c.replace('。Support', '. Supports')
    c = c.replace('，数据', ', data')
    c = c.replace('财务报表', 'financial reporting')
    return c

def fix_typewriter_effect(c):
    c = c.replace('preview并一键CopyHTML/CSS代码', 'preview and one-click copy HTML/CSS code')
    c = c.replace('并一键Copy', 'and one-click copy')
    return c

FIXERS = {
    'loading-spinner': fix_loading_spinner,
    'loan-calc': fix_loan_calc,
    'money-counter': fix_money_counter,
    'mortgage-calc': fix_mortgage_calc,
    'percentage-change': fix_percentage_change,
    'typewriter-effect': fix_typewriter_effect,
}

fixed = 0
for item, fixer in FIXERS.items():
    path = os.path.join(SITE, 'en', item, 'index.html')
    if not os.path.exists(path): continue
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        original = f.read()
    content = fixer(original)

    # 再用通用替换清理残留中文（script/style除外）
    CN_RE = re.compile(r'[\u4e00-\u9fff]')
    # 处理inline残留
    content = re.sub(r'<th[^>]*>([^<]*[\u4e00-\u9fff][^<]*)</th>', lambda m: '<th>' + re.sub(r'[\u4e00-\u9fff]+', '', m.group(1)) + '</th>', content)

    if content != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"FIXED: en/{item}/index.html")
        fixed += 1
    else:
        print(f"SKIP: en/{item}/index.html")

print(f"\nFixed: {fixed}/{len(FIXERS)}")