#!/usr/bin/env python3
"""Batch-add 5 new health tool cards to both CN and EN homepages."""
import re

NEW_TOOLS_CN = [
    ('🍬 糖尿病风险评估计算器', '基于年龄/BMI/血压/家族史评估2型糖尿病患病风险', '/diabetes-risk-calculator/'),
    ('🫀 代谢综合征评估计算器', '腰围/血压/血糖/血脂5项指标综合评估', '/metabolic-syndrome-calculator/'),
    ('😴 最佳睡眠时间计算器', '基于90分钟睡眠周期计算最佳入睡/起床时间', '/sleep-optimal-calculator/'),
    ('🧠 脑卒中风险计算器', '基于Framingham模型评估10年脑卒中发病风险', '/stroke-risk-calculator/'),
    ('❤️ 心脏病风险计算器', '综合血压/胆固醇/年龄等评估10年心脏病风险', '/heart-disease-risk-calculator/'),
]

NEW_TOOLS_EN = [
    ('🍬 Diabetes Risk Calculator', 'Assess type 2 diabetes risk using age, BMI, BP & family history', '/en/diabetes-risk-calculator/'),
    ('🫀 Metabolic Syndrome Calculator', '5-criteria assessment: waist, BP, glucose, lipids', '/en/metabolic-syndrome-calculator/'),
    ('😴 Sleep Cycle Calculator', 'Find optimal bedtime/wake-up time based on 90-min cycles', '/en/sleep-optimal-calculator/'),
    ('🧠 Stroke Risk Calculator', '10-year stroke risk based on Framingham model', '/en/stroke-risk-calculator/'),
    ('❤️ Heart Disease Risk Calculator', '10-year CVD risk using BP, cholesterol, age & more', '/en/heart-disease-risk-calculator/'),
]

def make_card(tool_name, tool_desc, tool_url, use_icon_span=False):
    if use_icon_span:
        icon = tool_name.split(' ')[0]
        name = ' '.join(tool_name.split(' ')[1:])
        return f'<div class="tool-card" data-category="health-tools"><span class="tool-icon">{icon}</span><span class="tool-name">{name}</span><span class="tool-desc">{tool_desc}</span><a href="{tool_url}" class="btn">立即使用</a></div>'
    return f'<div class="tool-card" data-category="health-tools"><span class="tool-name">{tool_name}</span><span class="tool-desc">{tool_desc}</span><a href="{tool_url}" class="btn">立即使用</a></div>'

def update_file(path, tools, use_icon_span):
    with open(path, 'r') as f:
        content = f.read()
    
    # Find last health-tools card to insert after
    # Strategy: find the last occurrence of data-category="health-tools" and insert after that closing </div>
    pattern = r'(data-category="health-tools".*?</div>)'
    matches = list(re.finditer(pattern, content, re.DOTALL))
    if not matches:
        print(f"  ERROR: No health-tools cards found in {path}")
        return False
    
    last_match = matches[-1]
    insert_pos = last_match.end()
    
    cards_html = '\n'.join([make_card(*t, use_icon_span=use_icon_span) for t in tools])
    
    new_content = content[:insert_pos] + '\n' + cards_html + content[insert_pos:]
    
    with open(path, 'w') as f:
        f.write(new_content)
    
    print(f"  Added {len(tools)} cards to {path}")
    return True

# Update CN homepage
print("Updating CN homepage...")
update_file('/home/chison/tools-site/index.html', NEW_TOOLS_CN, use_icon_span=False)

# Update EN homepage
print("Updating EN homepage...")
update_file('/home/chison/tools-site/en/index.html', NEW_TOOLS_EN, use_icon_span=True)

# Verify
for path in ['/home/chison/tools-site/index.html', '/home/chison/tools-site/en/index.html']:
    with open(path) as f:
        cnt = f.read().count('tool-card')
    print(f"  {path}: {cnt} tool-cards")