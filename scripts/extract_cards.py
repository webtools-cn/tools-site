#!/usr/bin/env python3
"""从首页HTML提取卡片数据，去重，输出JSON"""
import re, json, sys

with open('index.html', 'r') as f:
    html = f.read()

# 提取所有tool-card - 两种格式
# 格式1: <div class="tool-card" data-cat="..." data-category="..."><span class="tool-icon">...</span><span class="tool-name">...</span><span class="tool-desc">...</span><a href="..." class="btn">...</a></div>
# 格式2: <div class="tool-card" data-cat="..." data-name="..."><a href="..."><div class="tool-icon">...</div><h3>...</h3><p>...</p></a></div>

cards = []

# 格式1
for m in re.finditer(r'data-cat="([^"]+)"[^>]*?>\s*<span class="tool-icon">(.*?)</span>\s*<span class="tool-name">(.*?)</span>\s*<span class="tool-desc">(.*?)</span>\s*<a href="([^"]+?)"[^>]*class="btn"', html, re.DOTALL):
    cat, icon, name, desc, href = m.groups()
    cards.append({'cat': cat, 'icon': icon.strip(), 'name': name.strip(), 'desc': desc.strip()[:150], 'href': href.strip()})

# 格式2
for m in re.finditer(r'data-cat="([^"]+)"[^>]*data-name="[^"]*">\s*<a href="([^"]+?)">\s*<div class="tool-icon">(.*?)</div>\s*<h3>(.*?)</h3>\s*<p>(.*?)</p>', html, re.DOTALL):
    cat, href, icon, name, desc = m.groups()
    cards.append({'cat': cat, 'icon': icon.strip(), 'name': name.strip(), 'desc': desc.strip()[:150], 'href': href.strip()})

print(f'提取到卡片: {len(cards)}')

# 去重：按href去重，保留第一个
seen = set()
unique = []
dups = []
for c in cards:
    if c['href'] not in seen:
        seen.add(c['href'])
        unique.append(c)
    else:
        dups.append(c['name'])

print(f'去重后: {len(unique)}')
print(f'去掉重复: {len(cards) - len(unique)}')
if dups:
    from collections import Counter
    dup_counts = Counter(dups)
    print('重复最多的:')
    for name, cnt in dup_counts.most_common(10):
        print(f'  {name} x{cnt}')

# 分类统计
cats = {}
for c in unique:
    cats[c['cat']] = cats.get(c['cat'], 0) + 1
print('\n分类统计:')
for k, v in sorted(cats.items(), key=lambda x: -x[1]):
    print(f'  {k}: {v}')

# 保存
with open('tools-data-cn.json', 'w') as f:
    json.dump(unique, f, ensure_ascii=False, indent=2)

print(f'\n已保存 tools-data-cn.json ({len(json.dumps(unique, ensure_ascii=False))} bytes)')
