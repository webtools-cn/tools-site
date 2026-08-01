#!/usr/bin/env python3
"""从EN首页HTML提取卡片数据，去重，输出JSON"""
import re, json

with open('en/index.html', 'r') as f:
    html = f.read()

cards = []

# 格式1
for m in re.finditer(r'data-cat="([^"]+)"[^>]*?>\s*<span class="tool-icon">(.*?)</span>\s*<span class="tool-name">(.*?)</span>\s*<span class="tool-desc">(.*?)</span>\s*<a href="([^"]+?)"[^>]*class="btn"', html, re.DOTALL):
    cat, icon, name, desc, href = m.groups()
    cards.append({'cat': cat, 'icon': icon.strip(), 'name': name.strip(), 'desc': desc.strip()[:150], 'href': href.strip()})

# 格式2
for m in re.finditer(r'data-cat="([^"]+)"[^>]*data-name="[^"]*">\s*<a href="([^"]+?)">\s*<div class="tool-icon">(.*?)</div>\s*<h3>(.*?)</h3>\s*<p>(.*?)</p>', html, re.DOTALL):
    cat, href, icon, name, desc = m.groups()
    cards.append({'cat': cat, 'icon': icon.strip(), 'name': name.strip(), 'desc': desc.strip()[:150], 'href': href.strip()})

print(f'EN提取: {len(cards)}')

# 去重
seen = set()
unique = []
for c in cards:
    if c['href'] not in seen:
        seen.add(c['href'])
        unique.append(c)
print(f'EN去重后: {len(unique)}')

# 按分类分组，数组格式
groups = {}
for c in unique:
    cat = c['cat']
    if cat not in groups:
        groups[cat] = []
    groups[cat].append([c['icon'], c['name'], c['desc'][:40], c['href'].lstrip('/')])

compressed = json.dumps(groups, ensure_ascii=False, separators=(',',':'))
print(f'EN JSON: {len(compressed)} bytes ({len(compressed)/1024:.0f}KB)')

with open('tools-data-en.json', 'w') as f:
    f.write(compressed)
print('已保存 tools-data-en.json')
