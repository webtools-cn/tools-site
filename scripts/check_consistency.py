#!/usr/bin/env python3
"""全站一致性检查 - 首页卡片 + 工具页面结构"""
import re, os, json
from datetime import datetime
from collections import Counter

ISSUES = {}
os.chdir('/home/chison/tools-site')

# ============ 首页卡片一致性 ============
print("=== 首页卡片 ===")
with open('index.html') as f:
    content = f.read()

cards_raw = content.split('class="tool-card"')[1:]
btn_counter = Counter()
no_btn_tools = []
non_standard_btns = []

for card in cards_raw:
    m = re.search(r'<a href="([^"]+)">([^<]*)</a>', card)
    h3 = re.search(r'<h3>([^<]+)</h3>', card)
    tool = h3.group(1) if h3 else '?'
    if not m:
        no_btn_tools.append(tool)
    else:
        text = m.group(2).strip()
        if text == '立即使用':
            btn_counter['立即使用'] += 1
        elif text == '使用工具 →':
            btn_counter['使用工具 →'] += 1
            non_standard_btns.append((tool, text))
        elif text == '使用':
            btn_counter['使用'] += 1
            non_standard_btns.append((tool, text))
        else:
            btn_counter[text] += 1
            non_standard_btns.append((tool, text))

print(f"  按钮文本分布: {dict(btn_counter)}")
print(f"  无按钮: {len(no_btn_tools)} 个")
if no_btn_tools:
    print(f"    示例: {no_btn_tools[:5]}")
print(f"  文本不统一: {len(non_standard_btns)} 个")
if non_standard_btns:
    for t, b in non_standard_btns[:5]:
        print(f"    [{b}] → {t}")

card_issues = []
if no_btn_tools:
    card_issues.append(f"无按钮:{len(no_btn_tools)}个")
if non_standard_btns:
    card_issues.append(f"文本不统一:{len(non_standard_btns)}个")
if card_issues:
    ISSUES['首页卡片'] = card_issues

# ============ 工具页面结构一致性 ============
print("\n=== 工具页面结构 ===")
SKIP = {'_gen','__pycache__','en','libs','js','css','scripts','tools',
        '.git','data','about','blog','privacy-policy','terms-of-service','category',
        'calc','design','dev','fun','health','image','math','media','network',
        'office','pdf','security','seo','text','utility'}

structure_issues = []
total = 0
for d in sorted(os.listdir('.')):
    if not os.path.isdir(d) or d in SKIP or d.startswith('.'):
        continue
    html = os.path.join(d, 'index.html')
    if not os.path.exists(html):
        continue
    total += 1
    with open(html) as f:
        content = f.read()
    
    tool_issues = []
    if 'class="header"' not in content:
        tool_issues.append('NO_HEADER')
    if 'class="footer' not in content:
        tool_issues.append('NO_FOOTER')
    if 'class="container"' not in content:
        tool_issues.append('NO_CONTAINER')
    if 'class="toast"' not in content and "class='toast'" not in content and 'id="toast"' not in content:
        tool_issues.append('NO_TOAST')
    if 'function showToast' not in content:
        tool_issues.append('NO_SHOWTOAST')
    if 'function copyText' not in content:
        tool_issues.append('NO_COPYTEXT')
    if tool_issues:
        structure_issues.append({'tool': d, 'issues': tool_issues})

print(f"  检查工具: {total}")
print(f"  结构问题: {len(structure_issues)} 个")
if structure_issues:
    # 按问题类型分组
    issue_types = Counter()
    for item in structure_issues:
        for iss in item['issues']:
            issue_types[iss] += 1
    for iss, count in issue_types.most_common():
        print(f"    {iss}: {count}个")
    ISSUES['工具页面结构'] = [f"{iss}:{count}个" for iss, count in issue_types.most_common()]

# ============ 报告 ============
report = {
    'timestamp': datetime.now().isoformat(),
    'type': 'consistency_check',
    'total_tools': total,
    'issues': ISSUES,
    'card_no_btn': len(no_btn_tools),
    'card_non_standard': len(non_standard_btns),
    'structure_issues': len(structure_issues),
    'pass': len(ISSUES) == 0
}

os.makedirs('quality-reports', exist_ok=True)
fname = f"quality-reports/consistency-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
with open(fname, 'w') as f:
    json.dump(report, f, indent=2, ensure_ascii=False)

print(f"\n{'='*40}")
if report['pass']:
    print("✅ 一致性检查通过")
else:
    print("❌ 发现问题:")
    for cat, items in ISSUES.items():
        print(f"  {cat}: {', '.join(items)}")
print(f"报告: {fname}")