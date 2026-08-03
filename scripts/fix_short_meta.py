#!/usr/bin/env python3
"""Fix short meta descriptions."""
import re

files_to_fix = {
    # CN
    'jensen-alpha-calculator/index.html': '免费在线Jensen\'s Alpha詹森阿尔法计算器，评估投资组合超越市场基准的超额收益表现。输入实际收益率、无风险利率、市场收益率和贝塔系数，一键计算詹森阿尔法值衡量基金经理主动管理能力。适合基金绩效评估、投资组合归因分析和金融学教学。纯前端计算，数据安全不上传服务器，无需注册完全免费。',
    'pizza-dough-calculator/index.html': '免费在线披萨面团计算器，基于烘焙师百分比（Baker\'s Percent）精确计算面粉、水、盐、酵母用量。支持那不勒斯、纽约、底特律、西西里等多种风格预设，鲜酵母/干酵母/酸种换算，克/盎司双单位。适合家庭烘焙和披萨店备料，纯前端本地计算，无需注册完全免费。',
    'metal-weight-calculator/index.html': '免费在线金属重量计算器，支持钢、铝、铜、不锈钢等12种材质，圆棒、方棒、圆管、钢板等7种型材，输入尺寸自动计算重量。公制英制切换，批量件数计算，机械加工必备工具。',
    # EN
    'en/ohms-law-calculator/index.html': "Free online Ohm's law calculator: compute voltage, current, resistance, and power instantly. Enter any two known values to solve the rest. Perfect for electronics, circuit design, and engineering students. No signup, runs entirely in your browser.",
    'en/jensen-alpha-calculator/index.html': "Free online Jensen's Alpha calculator: measure portfolio performance vs market benchmark. Enter return, risk-free rate, market return & beta to calculate alpha. Ideal for fund evaluation and finance analysis. No signup, browser-based.",
    'en/conways-game-of-life/index.html': "Free online Conway's Game of Life simulator: watch cellular automata evolve on a grid. Adjust speed, grid size, and patterns. Explore gliders, blinkers, and complex structures. Perfect for learning emergence and complexity theory. No signup required.",
    'en/pizza-dough-calculator/index.html': "Free online pizza dough calculator using baker's percentages to precisely calculate flour, water, salt, and yeast amounts. Supports Neapolitan, NY, Detroit, Sicilian style presets, fresh/dry yeast conversion, and gram/ounce units. Runs entirely in your browser.",
    'en/due-date-calculator/index.html': "Free due date calculator: estimate pregnancy due date & gestational age from LMP or conception date. Accurate Naegele's rule calculation with weekly progress tracking. No signup, runs entirely in your browser.",
}

for fpath, new_desc in files_to_fix.items():
    with open(fpath, 'r', encoding='utf-8') as f:
        html = f.read()
    
    ln = len(new_desc)
    print(f'{fpath}: new desc len = {ln}')
    
    # Replace the meta description
    pattern = r'(name=["\']description["\']\s+content=["\'])[^"\']+(["\'])'
    new_html = re.sub(pattern, lambda m: m.group(1) + new_desc + m.group(2), html, count=1)
    
    if new_html != html:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(new_html)
        print(f'  -> FIXED')
    else:
        print(f'  -> NO MATCH (already ok?)')

print('\nDone!')
