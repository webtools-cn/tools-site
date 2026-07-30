#!/usr/bin/env python3
"""修复 schema JSON description 与 meta description 不一致的页面"""
import re, os, glob

count = 0
for path in sorted(glob.glob('*/index.html')):
    c = open(path).read()
    if 'meta http-equiv="refresh"' in c:
        continue
    
    # 提取meta description
    mm = re.search(r'<meta name="description" content="([^"]+)"', c)
    if not mm:
        continue
    meta_desc = mm.group(1)
    
    # 提取所有schema description
    # 找到所有JSON中的description字段
    schema_descs = re.findall(r'"description"\s*:\s*"([^"]*)"', c)
    if not schema_descs:
        continue
    
    # 检查是否有不一致的（schema比meta短很多，说明是旧版本）
    for old_sd in schema_descs:
        if old_sd != meta_desc and len(old_sd) < len(meta_desc) * 0.8:
            # 需要替换
            # JSON中需要对特殊字符转义: " → \", \ → \\
            escaped = meta_desc.replace('\\', '\\\\').replace('"', '\\"')
            new_c = c.replace(f'"description": "{old_sd}"', f'"description": "{escaped}"')
            if new_c != c:
                open(path, 'w').write(new_c)
                count += 1
                print(f'FIXED {path}: schema desc {len(old_sd)} → {len(meta_desc)} chars')
                break

print(f'\nTotal schema fixes: {count}')