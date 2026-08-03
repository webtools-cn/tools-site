#!/usr/bin/env python3
"""Scan all tool pages for short meta descriptions (<120 chars).
Uses correct regex that handles double-quoted content values."""
import os, re

short_cn = []
short_en = []
all_cn = []
all_en = []

# CN pages
for d in sorted(os.listdir('.')):
    if d in ('en', '.git', 'css', 'js', 'scripts', 'quality', '.gsc-data', 'node_modules'):
        continue
    f = os.path.join(d, 'index.html')
    if not os.path.isfile(f):
        continue
    html = open(f, encoding='utf-8', errors='ignore').read()
    m = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', html)
    if m:
        ln = len(m.group(1))
        all_cn.append(ln)
        if ln < 120:
            short_cn.append((ln, d, m.group(1)))
    else:
        # Try single quotes
        m = re.search(r"<meta\s+name='description'\s+content='([^']*)'", html)
        if m:
            ln = len(m.group(1))
            all_cn.append(ln)
            if ln < 120:
                short_cn.append((ln, d, m.group(1)))

# EN pages
en_dir = 'en'
if os.path.isdir(en_dir):
    for d in sorted(os.listdir(en_dir)):
        f = os.path.join(en_dir, d, 'index.html')
        if not os.path.isfile(f):
            continue
        html = open(f, encoding='utf-8', errors='ignore').read()
        m = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', html)
        if m:
            ln = len(m.group(1))
            all_en.append(ln)
            if ln < 120:
                short_en.append((ln, d, m.group(1)))
        else:
            m = re.search(r"<meta\s+name='description'\s+content='([^']*)'", html)
            if m:
                ln = len(m.group(1))
                all_en.append(ln)
                if ln < 120:
                    short_en.append((ln, d, m.group(1)))

# Summary stats
cn_avg = sum(all_cn) / len(all_cn) if all_cn else 0
en_avg = sum(all_en) / len(all_en) if all_en else 0
cn_short_count = sum(1 for l in all_cn if l < 120)
en_short_count = sum(1 for l in all_en if l < 120)
cn_long_count = sum(1 for l in all_cn if l > 160)
en_long_count = sum(1 for l in all_en if l > 160)

print(f'=== CN Pages ===')
print(f'Total: {len(all_cn)}, Avg: {cn_avg:.0f} chars')
print(f'Short (<120): {cn_short_count}, Long (>160): {cn_long_count}')
for ln, name, d in sorted(short_cn)[:30]:
    print(f'  {ln} {name}: {d[:70]}...')

print(f'\n=== EN Pages ===')
print(f'Total: {len(all_en)}, Avg: {en_avg:.0f} chars')
print(f'Short (<120): {en_short_count}, Long (>160): {en_long_count}')
for ln, name, d in sorted(short_en)[:30]:
    print(f'  {ln} {name}: {d[:70]}...')
