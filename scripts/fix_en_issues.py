import re

fixes = {
    'en/budget-by-category/index.html': [
        ('在线分类预算计算器,工具,在线工具,免费', 'budget calculator,tools,online tools,free'),
        ('"name": "首页"', '"name": "Home"'),
        ('"name": "工具"', '"name": "Tools"'),
        ('"name": "在线分类预算计算器"', '"name": "Budget by Category"'),
    ],
    'en/meal-cost-calculator/index.html': [
        ('在线餐食成本计算器,工具,在线工具,免费', 'meal cost calculator,tools,online tools,free'),
        ('"name": "首页"', '"name": "Home"'),
        ('"name": "工具"', '"name": "Tools"'),
        ('"name": "在线餐食成本计算器"', '"name": "Meal Cost Calculator"'),
        ('"text": "例如一袋5kg大米', '"text": "Example: 5kg rice costs'),
        ('"name": "数据安全吗？"', '"name": "Is my data secure?"'),
    ],
    'en/baby-cost-calculator/index.html': [
        ('在线育儿成本计算器,工具,在线工具,免费', 'baby cost calculator,tools,online tools,free'),
        ('"name": "首页"', '"name": "Home"'),
        ('"name": "工具"', '"name": "Tools"'),
        ('"name": "在线育儿成本计算器"', '"name": "Baby Cost Calculator"'),
        ('"name": "数据安全吗？"', '"name": "Is my data secure?"'),
    ],
    'en/rmd-table/index.html': [
        ('在线RMD计算器,工具,在线工具,免费', 'RMD calculator,tools,online tools,free'),
        ('"name": "首页"', '"name": "Home"'),
        ('"name": "工具"', '"name": "Tools"'),
        ('"name": "在线RMD计算器"', '"name": "RMD Calculator"'),
    ],
    'en/subscription-manager/index.html': [
        ('"name": "首页"', '"name": "Home"'),
        ('"name": "工具"', '"name": "Tools"'),
        ('"name": "在线订阅管理器"', '"name": "Subscription Manager"'),
    ],
}

for filepath, replacements in fixes.items():
    with open(filepath, 'r') as f:
        content = f.read()
    for old, new in replacements:
        if old in content:
            content = content.replace(old, new)
    with open(filepath, 'w') as f:
        f.write(content)
    print(f'Fixed: {filepath}')
