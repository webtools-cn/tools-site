#!/usr/bin/env python3
"""批量给缺robots标签的页面加 <meta name="robots" content="index, follow">"""
import os, re

fixed = 0
for prefix in ['', 'en/']:
    for d in sorted(os.listdir(prefix or '.')):
        p = os.path.join(prefix, d, 'index.html') if prefix else os.path.join(d, 'index.html')
        if not os.path.isfile(p): continue
        if prefix == '' and d == 'en': continue
        c = open(p, 'r', errors='ignore').read()
        # Skip if already has robots tag
        if '<meta name="robots"' in c: continue
        # Skip if has noindex
        if 'noindex' in c.lower(): continue
        # Add robots tag after <meta charset>
        if '<meta charset="UTF-8">' in c:
            c = c.replace('<meta charset="UTF-8">', '<meta charset="UTF-8">\n  <meta name="robots" content="index, follow">', 1)
            open(p, 'w', encoding='utf-8', errors='ignore').write(c)
            fixed += 1

print(f"Added robots tag to {fixed} pages")
