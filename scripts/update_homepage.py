#!/usr/bin/env python3
"""在CN和EN首页添加5个新工具的tool-card"""
import re

new_tools = [
    ('max-drawdown-calculator', '📉 最大回撤计算器', '计算投资组合最大回撤率和回撤金额，分析投资风险', 'finance-tools',
     'Max Drawdown Calculator', 'Calculate maximum drawdown rate and amount, analyze investment risk'),
    ('treynor-ratio-calculator', '📊 特雷诺比率计算器', '衡量每单位系统性风险的超额回报，评估投资组合表现', 'finance-tools',
     'Treynor Ratio Calculator', 'Measure excess return per unit of systematic risk, evaluate portfolio performance'),
    ('information-ratio-calculator', '📈 信息比率计算器', '衡量相对基准的超额回报稳定性，评估主动管理能力', 'finance-tools',
     'Information Ratio Calculator', 'Measure consistency of excess return vs benchmark, evaluate active management'),
    ('kidney-function-calculator', '🩺 肾功能计算器(eGFR)', 'CKD-EPI公式估算肾小球滤过率，评估肾功能分期', 'health-tools',
     'Kidney Function Calculator', 'CKD-EPI formula to estimate eGFR, assess kidney function stage'),
    ('iron-deficiency-calculator', '🩸 缺铁性贫血评估器', '基于血红蛋白和铁蛋白评估缺铁风险，识别贫血程度', 'health-tools',
     'Iron Deficiency Calculator', 'Assess iron deficiency risk based on hemoglobin and ferritin, identify anemia severity'),
]

for lang, home_file in [('cn', 'index.html'), ('en', 'en/index.html')]:
    filepath = f'/home/chison/tools-site/{home_file}'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    cards = ''
    for t in new_tools:
        slug = t[0]
        name = t[1] if lang == 'cn' else t[4]
        desc = t[2] if lang == 'cn' else t[5]
        category = t[3]
        href = f'/{slug}/' if lang == 'cn' else f'/en/{slug}/'
        cards += f'<div class="tool-card" data-category="{category}"><span class="tool-name">{name}</span><span class="tool-desc">{desc}</span><a href="{href}" class="btn">{"立即使用" if lang == "cn" else "Use Now"}</a></div>\n'

    # Insert cards before the last tool-card in the file (or before a specific marker)
    # Better: find the position just before the category-tag "其他工具" section or end of tools grid
    # Insert before "other-tools" or at the end of tools grid
    if lang == 'cn':
        # Find the last health-tools card and insert after it
        last_health = content.rfind('data-category="health-tools"')
        if last_health > 0:
            # Find end of that line's </div>
            insert_pos = content.index('</div>', content.index('\n', last_health)) + 6
            content = content[:insert_pos] + '\n' + cards + content[insert_pos:]
    else:
        last_health = content.rfind('data-category="health-tools"')
        if last_health > 0:
            insert_pos = content.index('</div>', content.index('\n', last_health)) + 6
            content = content[:insert_pos] + '\n' + cards + content[insert_pos:]

    # Update tool count
    old_count = content.count('data-category=')
    # The count displayed in the page: find and update
    # CN: <span class="tool-count">...</span>
    # EN: <span class="tool-count">...</span>
    # We need to find and increment the number

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f'Updated: {home_file} - added {len(new_tools)} cards')

# Now update tool count
for home_file in ['index.html', 'en/index.html']:
    filepath = f'/home/chison/tools-site/{home_file}'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find and update count in stats section
    # Pattern: <span class="count" id="totalTools">NNNN</span> or similar
    # Let's search for the count pattern
    import re
    # Common patterns for tool count
    patterns = [
        r'(<span[^>]*class="[^"]*count[^"]*"[^>]*>)(\d+)(</span>)',
        r'(id="totalTools"[^>]*>)(\d+)',
        r'(id="toolCount"[^>]*>)(\d+)',
    ]
    for p in patterns:
        m = re.search(p, content)
        if m:
            old_num = int(m.group(2))
            new_num = old_num + 5
            content = content[:m.start(2)] + str(new_num) + content[m.end(2):]
            print(f'Updated count in {home_file}: {old_num} -> {new_num}')
            break

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print('Done!')