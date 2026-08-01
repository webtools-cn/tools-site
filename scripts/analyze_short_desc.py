#!/usr/bin/env python3
"""Analyze short meta descriptions in detail."""
import os, re

short_details = []
for root, dirs, files in os.walk('.'):
    if '.git' in root or 'scripts' in root or 'quality' in root:
        continue
    for f in files:
        if not f.endswith('.html'):
            continue
        path = os.path.join(root, f)
        with open(path, 'r', encoding='utf-8', errors='ignore') as fh:
            content = fh.read()
        m = re.search(r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']*)["\']', content)
        if not m:
            continue
        desc = m.group(1)
        desc_len = len(desc)
        if desc_len < 100:
            parts = path.replace('./', '').replace('/index.html', '').replace('en/', '')
            short_details.append((desc_len, path, desc[:120], parts))

short_details.sort()
print(f'Total short (<100): {len(short_details)}')
print()

for l, p, d, t in short_details:
    if l < 70:
        print(f'[{l}] {t}')
        print(f'    {d}')
        print()