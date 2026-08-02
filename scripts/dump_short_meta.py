#!/usr/bin/env python3
"""提取30个最短描述的页面的h1和当前描述"""
import os, re, html as htmlmod

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

    desc = None
    for line in content.split('\n'):
        if 'name="description"' in line or "name='description'" in line:
            m = re.search(r'''content\s*=\s*"([^"]*)"''', line)
            if not m:
                m = re.search(r"""content\s*=\s*'([^']*)'""", line)
            if m:
                desc = htmlmod.unescape(m.group(1))
            break

    title_m = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
    h1_m = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.IGNORECASE)

    title = title_m.group(1) if title_m else 'N/A'
    h1 = h1_m.group(1) if h1_m else 'N/A'

    desc_len = len(desc) if desc else 0
    results.append((desc_len, filepath, title, h1, desc or ''))

# Sort: shortest first, then by path
results.sort()

# Take first 30 (shortest)
for i, (dlen, fp, title, h1, desc) in enumerate(results[:30]):
    print(f'--- {i+1}. [{dlen}c] {fp} ---')
    print(f'  Title: {title[:100]}')
    print(f'  H1:    {h1.strip()[:100]}')
    print(f'  Desc:  {desc[:120]}')
    print()