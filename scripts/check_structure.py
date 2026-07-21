#!/usr/bin/env python3
"""全站页面结构一致性检查 - 检查header/footer/ad-slot/toast/语言切换"""
import re, os, json
from datetime import datetime

SKIP = {'_gen','__pycache__','en','libs','js','css','scripts','tools',
        '.git','data','about','blog','privacy-policy','terms-of-service','category'}

issues = []
ok = 0

for d in sorted(os.listdir('.')):
    if not os.path.isdir(d) or d in SKIP or d.startswith('.'):
        continue
    html = os.path.join(d, 'index.html')
    if not os.path.exists(html):
        continue
    
    with open(html) as f:
        content = f.read()
    
    tool_issues = []
    
    # 检查核心结构
    if 'class="header"' not in content and "class='header'" not in content:
        tool_issues.append('MISSING_HEADER')
    if 'class="footer' not in content and "class='footer" not in content:
        tool_issues.append('MISSING_FOOTER')
    if 'class="container"' not in content:
        tool_issues.append('MISSING_CONTAINER')
    
    # 检查toast
    if 'class="toast"' not in content and "class='toast'" not in content and 'id="toast"' not in content:
        tool_issues.append('MISSING_TOAST')
    
    # 检查公共函数
    if 'function showToast' not in content:
        tool_issues.append('MISSING_SHOWTOAST')
    if 'function copyText' not in content:
        tool_issues.append('MISSING_COPYTEXT')
    
    # 检查语言切换
    if '../en/' + d + '/' not in content and '/en/' + d + '/' not in content:
        tool_issues.append('MISSING_EN_LINK')
    
    # 检查ad-slot
    ad_count = content.count('class="ad-slot"') + content.count("class='ad-slot'")
    if ad_count != 2:
        tool_issues.append(f'AD_SLOT_COUNT({ad_count})')
    
    # 检查header结构（logo+搜索+语言切换）
    header_match = re.search(r'<header[^>]*>(.*?)</header>', content, re.DOTALL)
    if header_match:
        header = header_match.group(1)
        if 'logo' not in header.lower() and 'free-toolbase' not in header.lower():
            tool_issues.append('HEADER_NO_LOGO')
        if 'search' not in header.lower() and '搜索' not in header and 'Search' not in header:
            tool_issues.append('HEADER_NO_SEARCH')
    
    if tool_issues:
        issues.append({'tool': d, 'issues': tool_issues})
    else:
        ok += 1

report = {
    'timestamp': datetime.now().isoformat(),
    'type': 'structure_check',
    'total': ok + len(issues),
    'ok': ok,
    'issues': len(issues),
    'issue_list': issues
}

os.makedirs('quality-reports', exist_ok=True)
fname = f"quality-reports/structure-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
with open(fname, 'w') as f:
    json.dump(report, f, indent=2, ensure_ascii=False)

print(f"OK={ok} Issues={len(issues)}")
for item in issues[:10]:
    print(f"  {item['tool']}: {','.join(item['issues'])}")
if len(issues) > 10:
    print(f"  ... and {len(issues)-10} more")