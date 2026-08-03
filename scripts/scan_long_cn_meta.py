#!/usr/bin/env python3
"""Find CN pages with meta description >160 chars."""
import os, re

long_cn = []

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
        if ln > 160:
            long_cn.append((ln, d, m.group(1)))

print(f'CN pages with desc >160: {len(long_cn)}')
for ln, name, desc in sorted(long_cn, reverse=True):
    print(f'{ln}\t{name}\t{desc[:100]}...')
