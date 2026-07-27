#!/usr/bin/env python3
"""更新首页：添加5个新工具卡片 + 更新计数 + 更新sitemap"""
import os
import re

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 新工具卡片
CN_CARDS = [
    ('health-tools', '👶', '儿童BMI百分位计算器', '根据CDC标准，评估2-20岁儿童BMI百分位数和Z-score，科学判断生长发育状况。', '/bmi-percentile-calculator/'),
    ('health-tools', '🔥', '运动消耗热量计算器', '基于MET代谢当量，计算50+种运动消耗热量，支持自定义体重和时长。', '/calorie-burned-calculator/'),
    ('health-tools', '⚡', '基础代谢率计算器(HB)', '基于Harris-Benedict公式计算BMR和TDEE，科学指导饮食和运动计划。', '/bmr-calculator-harris-benedict/'),
    ('health-tools', '🩺', '胆固醇单位换算器', '在mmol/L和mg/dL之间快速换算总胆固醇/HDL/LDL/甘油三酯。', '/cholesterol-units-converter/'),
    ('fin-tools', '📈', '投资回报率计算器', '一键计算投资ROI、年化回报率和净利润，可视化投资表现。', '/roi-calculator-investment/'),
]

EN_CARDS = [
    ('health-tools', '👶', 'BMI Percentile Calculator', 'Calculate BMI percentile and Z-score for children 2-20 using CDC growth charts.', '/en/bmi-percentile-calculator/'),
    ('health-tools', '🔥', 'Calories Burned Calculator', 'Calculate calories burned for 50+ activities using MET values. Customize weight and duration.', '/en/calorie-burned-calculator/'),
    ('health-tools', '⚡', 'BMR Calculator (Harris-Benedict)', 'Calculate BMR and TDEE using the Harris-Benedict equation for science-based diet planning.', '/en/bmr-calculator-harris-benedict/'),
    ('health-tools', '🩺', 'Cholesterol Units Converter', 'Convert between mmol/L and mg/dL for total cholesterol, HDL, LDL, and triglycerides.', '/en/cholesterol-units-converter/'),
    ('fin-tools', '📈', 'Investment ROI Calculator', 'Calculate ROI, annualized return, and net profit. Visualize investment performance instantly.', '/en/roi-calculator-investment/'),
]

def gen_card(cat, icon, name, desc, href):
    return f'<div class="tool-card" data-category="{cat}"><span class="tool-icon">{icon}</span><span class="tool-name">{name}</span><span class="tool-desc">{desc}</span><a href="{href}" class="btn">{"使用工具" if "/en/" not in href else "Use Tool"}</a></div>'

def update_homepage(path, cards):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find last tool-card and insert after it
    # Strategy: find a known stable anchor card and insert after the last one
    # Use the "使用工具" or "Use Tool" closing div pattern
    
    # Find the last tool-card
    is_en = '/en/' in path
    btn_text = 'Use Tool' if is_en else '使用工具'
    
    # Find the position of the last occurrence of btn_text
    last_idx = content.rindex(btn_text + '</a></div>')
    # Find the end of that div
    insert_pos = content.index('\n', last_idx) + 1
    
    # Build card HTML
    card_htmls = []
    for cat, icon, name, desc, href in cards:
        card_htmls.append(gen_card(cat, icon, name, desc, href))
    insert_block = '\n' + '\n'.join(card_htmls)
    
    new_content = content[:insert_pos] + insert_block + content[insert_pos:]
    
    # Update tool count
    # Find stat-number and increment
    def repl_count(m):
        current = int(m.group(1).replace(',', ''))
        return f'<span class="stat-number">{current + 5:,}</span>'
    
    # Only update the first occurrence (the total tools count)
    new_content = re.sub(r'(<span class="stat-number">)([0-9,]+)(</span>)', 
                         lambda m: f'{m.group(1)}{int(m.group(2).replace(",","")) + 5:,}{m.group(3)}', 
                         new_content, count=1)
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"  ✅ {path} 已更新")


def update_sitemap():
    """Update sitemap.xml with new tool URLs"""
    spath = os.path.join(SITE, 'sitemap.xml')
    with open(spath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    slugs = ['bmi-percentile-calculator', 'calorie-burned-calculator', 
             'bmr-calculator-harris-benedict', 'cholesterol-units-converter', 
             'roi-calculator-investment']
    
    new_entries = ''
    for slug in slugs:
        new_entries += f'''  <url>
    <loc>https://free-toolbase.com/{slug}/</loc>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>
  <url>
    <loc>https://free-toolbase.com/en/{slug}/</loc>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>
'''
    
    # Insert before </urlset>
    content = content.replace('</urlset>', new_entries + '</urlset>')
    
    with open(spath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  ✅ sitemap.xml 已更新 (新增10个URL)")


def update_llms_txt():
    """Update llms.txt with new tool entries"""
    lpath = os.path.join(SITE, 'llms.txt')
    with open(lpath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    slugs = ['bmi-percentile-calculator', 'calorie-burned-calculator', 
             'bmr-calculator-harris-benedict', 'cholesterol-units-converter', 
             'roi-calculator-investment']
    
    new_entries = '\n'
    for slug in slugs:
        new_entries += f'{slug}/\n'
        new_entries += f'en/{slug}/\n'
    
    content += new_entries
    
    with open(lpath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  ✅ llms.txt 已更新")


if __name__ == '__main__':
    update_homepage(os.path.join(SITE, 'index.html'), CN_CARDS)
    update_homepage(os.path.join(SITE, 'en/index.html'), EN_CARDS)
    update_sitemap()
    update_llms_txt()
    print('\n首页同步完成！')