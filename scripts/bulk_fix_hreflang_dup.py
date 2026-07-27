#!/usr/bin/env python3
"""批量修复 hreflang_duplicate: 去重hreflang标签"""
import os, json, re

SITE = '/home/chison/tools-site'

with open(os.path.join(SITE, 'quality', 'quality_loop_result.json')) as f:
    data = json.load(f)

remaining = data['remaining_pages']

dup_pages = []
for k, v in remaining.items():
    if 'hreflang_duplicate' in v:
        lang, item = k.split(':')
        dup_pages.append((lang, item))

print(f"处理 {len(dup_pages)} 个hreflang重复页面...")

fixed = 0
for lang, item in dup_pages:
    if lang == 'cn':
        path = os.path.join(SITE, item, 'index.html')
    else:
        path = os.path.join(SITE, 'en', item, 'index.html')
    
    if not os.path.isfile(path):
        continue
    
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # 找所有hreflang行
    lines = content.split('\n')
    seen = set()
    new_lines = []
    removed = 0
    for line in lines:
        m = re.search(r'hreflang="([^"]+)"\s+href="([^"]+)"', line)
        if m:
            key = (m.group(1), m.group(2))
            if key in seen:
                removed += 1
                continue  # 跳过重复
            seen.add(key)
        new_lines.append(line)
    
    if removed > 0:
        with open(path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_lines))
        fixed += 1

print(f"修复: {fixed} 个")