#!/usr/bin/env python3
"""Scan meta descriptions and categorize issues"""
import os, re, json

# Categories
too_short_en = []  # EN pages with <100 chars
too_short_cn = []  # CN pages with <100 chars (non-redirect)
too_long_en = []   # EN pages with >160 chars
too_long_cn = []   # CN pages with >160 chars
missing = []       # Missing description
redirect_pages = [] # "已升级至新版本" redirect pages

redirect_pattern = re.compile(r'已升级至新版本|has been upgraded')

for root, dirs, files in os.walk('.'):
    if '/.' in root or 'quality' in root or 'scripts' in root or '.gsc-data' in root or 'node_modules' in root:
        continue
    for f in files:
        if f == 'index.html':
            path = os.path.join(root, f)
            is_en = '/en/' in path
            try:
                with open(path, 'r', encoding='utf-8') as fh:
                    content = fh.read()
                m = re.search(r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']+)["\']', content, re.I)
                if not m:
                    missing.append(path)
                    continue
                
                desc = m.group(1)
                length = len(desc)
                
                if redirect_pattern.search(desc):
                    redirect_pages.append(path)
                    continue
                
                if length < 100:
                    if is_en:
                        too_short_en.append((path, desc, length))
                    else:
                        too_short_cn.append((path, desc, length))
                elif length > 160:
                    if is_en:
                        too_long_en.append((path, desc, length))
                    else:
                        too_long_cn.append((path, desc, length))
            except Exception as e:
                pass

print("=" * 60)
print(f"Redirect pages (skip): {len(redirect_pages)}")
print(f"Missing description: {len(missing)}")
print(f"EN too short (<100): {len(too_short_en)}")
print(f"CN too short (<100): {len(too_short_cn)}")
print(f"EN too long (>160): {len(too_long_en)}")
print(f"CN too long (>160): {len(too_long_cn)}")
print("=" * 60)

# Sort by length ascending (worst first)
too_short_en.sort(key=lambda x: x[2])
too_long_en.sort(key=lambda x: -x[2])

print("\n## EN too short (top 30):")
for path, desc, length in too_short_en[:30]:
    print(f"  [{length:3d}] {path}")
    print(f"        {desc}")

print("\n## EN too long (top 10):")
for path, desc, length in too_long_en[:10]:
    print(f"  [{length:3d}] {path}")
    print(f"        {desc[:120]}...")

print("\n## Missing (first 10):")
for path in missing[:10]:
    print(f"  {path}")