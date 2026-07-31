#!/usr/bin/env python3
"""List shortest meta descriptions with context."""
import os, re

results = []
for root, dirs, files in os.walk('.'):
    if '.git' in root or len(results) >= 120:
        continue
    for f in files:
        if not f.endswith('.html') or len(results) >= 120:
            continue
        path = os.path.join(root, f)
        with open(path, 'r', encoding='utf-8', errors='ignore') as fh:
            content = fh.read()
        
        m = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', content)
        if not m:
            continue
        desc_len = len(m.group(1))
        if desc_len >= 100:
            continue
        title_m = re.search(r'<title>(.*?)</title>', content)
        title = title_m.group(1) if title_m else 'N/A'
        h1_m = re.search(r'<h1[^>]*>(.*?)</h1>', content)
        h1 = h1_m.group(1) if h1_m else ''
        results.append((desc_len, path, m.group(1), title, h1))

results.sort(key=lambda x: x[0])
for i, r in enumerate(results[:50]):
    print(f'{i+1}. LEN={r[0]} | PATH={r[1]}')
    print(f'   TITLE: {r[3][:80]}')
    print(f'   H1: {r[4][:80]}')
    print(f'   DESC: {r[2][:120]}')
    print()