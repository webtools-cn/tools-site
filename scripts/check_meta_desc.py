#!/usr/bin/env python3
"""SEO巡检：检查meta description长度（修正版）"""
import os, re, html

results = []
for dirpath, dirnames, filenames in os.walk('.'):
    dirnames[:] = [d for d in dirnames if not d.startswith('.')]
    if 'index.html' not in filenames:
        continue
    if dirpath in ['.', './quality', './scripts', './.gsc-data']:
        continue
    if dirpath == './en':
        continue

    filepath = os.path.join(dirpath, 'index.html')
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        continue

    # Extract meta description - match the full line then parse content
    desc = None
    for line in content.split('\n'):
        if 'name="description"' in line or "name='description'" in line:
            # Extract content= value - handle both " and ' quoting
            m = re.search(r'''content\s*=\s*"([^"]*)"''', line)
            if not m:
                m = re.search(r"""content\s*=\s*'([^']*)'""", line)
            if m:
                desc = html.unescape(m.group(1))
            break

    has_noindex = bool(re.search(r'<meta\s+name=["\']robots["\']\s+content=["\'][^"\']*noindex', content, re.IGNORECASE))

    title_m = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
    title = title_m.group(1) if title_m else 'N/A'

    if desc is not None:
        desc_len = len(desc)
    else:
        desc = '(MISSING)'
        desc_len = 0

    results.append((desc_len, filepath, title, desc[:120], has_noindex))

results.sort()

print(f'Total pages checked: {len(results)}')
print()

# Short (<100)
short_list = [r for r in results if r[0] < 100]
print(f'=== SHORT (<100 chars): {len(short_list)} ===')
for r in short_list[:50]:
    print(f'  [{r[0]:3d}] {r[1]:55s} | {r[3][:100]}')

# Missing
missing_list = [r for r in results if r[0] == 0]
print(f'\n=== MISSING: {len(missing_list)} ===')

# Noindex
noindex_list = [r for r in results if r[4]]
print(f'\n=== NOINDEX: {len(noindex_list)} ===')
for r in noindex_list[:10]:
    print(f'  {r[1]}')

# Too long
long_list = [r for r in results if r[0] > 160]
print(f'\n=== TOO LONG (>160): {len(long_list)} ===')

# Distribution
bins = [(0,50), (50,100), (100,120), (120,140), (140,160), (160,200), (200,999)]
for lo, hi in bins:
    count = sum(1 for r in results if lo <= r[0] < hi)
    print(f'  [{lo:3d}-{hi:3d}): {count}')