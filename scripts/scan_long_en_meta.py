#!/usr/bin/env python3
"""Find EN pages with meta description >160 chars."""
import os, re

long_en = []

en_dir = 'en'
for d in sorted(os.listdir(en_dir)):
    f = os.path.join(en_dir, d, 'index.html')
    if not os.path.isfile(f):
        continue
    html = open(f, encoding='utf-8', errors='ignore').read()
    m = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', html)
    if m:
        ln = len(m.group(1))
        if ln > 160:
            long_en.append((ln, d, m.group(1)))

print(f'EN pages with desc >160: {len(long_en)}')
for ln, name, desc in sorted(long_en, reverse=True):
    print(f'{ln}\t{name}\t{desc[:100]}...')
