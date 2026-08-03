#!/usr/bin/env python3
"""Fix corrupted meta descriptions - replace entire content value between double quotes."""
import re

# Correct descriptions
correct = {
    'jensen-alpha-calculator/index.html': "免费在线Jensen's Alpha詹森阿尔法计算器，评估投资组合超越市场基准的超额收益表现。输入实际收益率、无风险利率、市场收益率和贝塔系数，一键计算詹森阿尔法值衡量基金经理主动管理能力。适合基金绩效评估、投资组合归因分析和金融学教学。纯前端计算，数据安全不上传服务器，无需注册完全免费。",
    'pizza-dough-calculator/index.html': "免费在线披萨面团计算器，基于烘焙师百分比（Baker's Percent）精确计算面粉、水、盐、酵母用量。支持那不勒斯、纽约、底特律、西西里等多种风格预设，鲜酵母/干酵母/酸种换算，克/盎司双单位。适合家庭烘焙和披萨店备料，纯前端本地计算，无需注册完全免费。",
    'metal-weight-calculator/index.html': "免费在线金属重量计算器，支持钢、铝、铜、不锈钢等12种材质，圆棒、方棒、圆管、钢板等7种型材。输入尺寸自动计算重量，支持公制英制切换和批量件数计算，机械加工制造行业必备工具。纯前端本地计算，数据安全不上传，无需注册完全免费。",
    'en/ohms-law-calculator/index.html': "Free online Ohm's law calculator: compute voltage, current, resistance and power. Enter any two values to solve the rest. No signup, browser-based.",
    'en/jensen-alpha-calculator/index.html': "Free online Jensen's Alpha calculator: measure portfolio performance vs market benchmark. Enter return, risk-free rate, beta. No signup, browser-based.",
    'en/conways-game-of-life/index.html': "Free Conway's Game of Life simulator: watch cellular automata evolve on a grid. Adjust speed and patterns. Explore gliders and complex structures. No signup.",
    'en/pizza-dough-calculator/index.html': "Free pizza dough calculator using baker's percentages. Calculate flour, water, salt and yeast amounts. Supports Neapolitan, NY, Detroit styles. No signup.",
    'en/due-date-calculator/index.html': "Free due date calculator: estimate pregnancy due date and gestational age from LMP or conception date. Naegele's rule. No signup, browser-based.",
}

for fpath, new_desc in correct.items():
    with open(fpath, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Match the full meta description tag and replace content value
    # Pattern: <meta name="description" content="...anything...">
    pattern = r'(<meta\s+name="description"\s+content=")[^"]*(")'
    new_html = re.sub(pattern, lambda m: m.group(1) + new_desc + m.group(2), html, count=1)
    
    if new_html != html:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(new_html)
        print(f'{fpath}: {len(new_desc)} chars -> FIXED')
    else:
        print(f'{fpath}: NO MATCH')

print('\nDone!')
