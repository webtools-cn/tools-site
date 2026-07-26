#!/usr/bin/env python3
"""批量修复EN页面中文碎片 v9 - 全文件替换，最彻底"""
import os, re

SITE = '/home/chison/tools-site'

# 全局替换表
GLOBAL_REPLACEMENTS = [
    # loading-spinner
    ('loading动画,CSS加载,spinnerGenerate器,前端开发,CSS动画,加载图标', 'loading animation, CSS spinner, frontend development, loading icon'),
    ('loading动画', 'loading animation'),
    ('CSS加载', 'CSS loading'),
    ('spinnerGenerate器', 'spinner generator'),
    ('前端开发', 'frontend development'),
    ('CSS动画', 'CSS animation'),
    ('加载图标', 'loading icon'),

    # loan-calc
    (',每Monthly,InterestCalculate,Loan Term,Equal Installment,Equal Principal,个人贷款', ', monthly payment, interest calculation, loan term, equal installment, equal principal, personal loan'),
    ('每Monthly', 'monthly payment'),
    ('InterestCalculate', 'interest calculation'),
    (',Equal Installment,Equal Principal,个人贷款', ', equal installment, equal principal, personal loan'),
    ('Loan Calculate器', 'Loan Calculator'),
    ('如 100000', 'e.g. 100000'),
    ('如 4.9', 'e.g. 4.9'),
    ('如 30', 'e.g. 30'),

    # mortgage-calc
    (',按揭Calculate,Monthly PaymentCalculate,购房Loan,Provident FundLoan,房贷Calculate', ', mortgage calculation, monthly payment, home loan, provident fund, mortgage'),
    ('按揭Calculate', 'mortgage calculation'),
    ('Monthly PaymentCalculate', 'monthly payment calculation'),
    ('购房Loan', 'home loan'),
    ('Provident FundLoan', 'provident fund loan'),
    ('房贷Calculate', 'mortgage calculation'),
    ('如 300', 'e.g. 300'),
    ('年Rate', 'Annual Rate'),
    ('月供额', 'Monthly'),
    ('月供', 'Monthly'),
    ('总利息额', 'Total Interest'),
    ('还款总额', 'Total Payment'),
    ('首付额', 'Down Payment'),
    ('贷款额', 'Loan Amount'),

    # percentage-change
    (',Increase率Calculate,增幅Calculate,Change率,data analy析,OnlineCalculate器', ', percentage increase, percentage change, data analysis, online calculator'),
    ('Increase率Calculate', 'percentage increase calculator'),
    ('增幅Calculate', 'percentage change calculator'),
    ('Change率', 'change rate'),
    ('data analy析', 'data analysis'),
    ('OnlineCalculate器', 'online calculator'),
    ('PercentageChangeCalculate器', 'Percentage Change Calculator'),
]

def fix_file(path):
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        c = f.read()
    original = c
    for old, new in GLOBAL_REPLACEMENTS:
        c = c.replace(old, new)

    # 最后：清除任何残留的单字中文在非script/style区域内
    # 但先手动处理已知模板片段的残留
    c = c.replace('年Rate', 'Annual Rate')
    c = c.replace('计算Calculate', 'calculate')
    c = c.replace('Calculate器', 'Calculator')

    if c != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(c)
        return True
    return False

items = ['loading-spinner','loan-calc','mortgage-calc','percentage-change']
fixed = 0
for item in items:
    path = os.path.join(SITE, 'en', item, 'index.html')
    if fix_file(path):
        print(f"FIXED: en/{item}/index.html")
        fixed += 1
    else:
        print(f"SKIP: en/{item}/index.html")

print(f"\nFixed: {fixed}/{len(items)}")