#!/usr/bin/env python3
"""批量修复EN页面残留中文碎片 v6"""
import os, re

SITE = '/home/chison/tools-site'

FIX_MAP = [
    # loading-spinner
    ('visuallySelect30+loading动画', 'visually select 30+ loading animations'),
    ('HTML+CSS代码。Support旋转、脉冲、弹跳、波纹等多样式', 'HTML+CSS code. Supports spin, pulse, bounce, ripple and more styles'),
    # loan-calc
    ('每monthly paymentandtotal interest', 'monthly payment and total interest'),
    ('两Repayment Method, with de', 'repayment methods, with de'),
    ('剩余Principal', 'Remaining Principal'),
    # money-counter
    ('欧元', 'EUR'),
    ('日元', 'JPY'),
    ('英镑', 'GBP'),
    # mortgage-calc
    ('calculatesMonthly Payment、总利息and还款总额。Support等额本息and等额本', 'calculates monthly payment, total interest and payoff amount. Supports equal installment and equal'),
    # percentage-change
    ('or decrease。Support正负Increase、反向Calculate, 数据', 'or decrease. Supports positive/negative change, reverse calculation, data'),
    ('分析and财务报表必备', 'analysis and financial reporting'),
    # typewriter-effect
    ('visually配置typing speed, cursor style、Delete动画等Parameter, Live Preview', 'visually configure typing speed, cursor style, delete animation and other parameters, live preview'),
]

items = ['loading-spinner','loan-calc','money-counter','mortgage-calc','percentage-change','typewriter-effect']
fixed = 0

for item in items:
    path = os.path.join(SITE, 'en', item, 'index.html')
    if not os.path.exists(path): continue
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    original = content
    for cn, en in FIX_MAP:
        if cn in content:
            content = content.replace(cn, en)
    if content != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"FIXED: en/{item}/index.html")
        fixed += 1
    else:
        print(f"SKIP: en/{item}/index.html (no match)")

print(f"\nFixed: {fixed}/{len(items)}")