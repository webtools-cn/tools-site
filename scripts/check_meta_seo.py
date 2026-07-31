#!/usr/bin/env python3
"""Check meta description lengths and noindex tags across all pages."""
import os, re

short = []
long = []
noindex_pages = []
missing = []
total = 0

for root, dirs, files in os.walk('.'):
    if '.git' in root:
        continue
    for f in files:
        if not f.endswith('.html'):
            continue
        total += 1
        path = os.path.join(root, f)
        with open(path, 'r', encoding='utf-8', errors='ignore') as fh:
            content = fh.read()
        
        desc_match = re.search(r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']*)["\']', content)
        desc_len = len(desc_match.group(1)) if desc_match else 0
        
        if desc_len == 0:
            missing.append(path)
        elif desc_len < 100:
            short.append((path, desc_len, desc_match.group(1)[:100] if desc_match else 'MISSING'))
        elif desc_len > 170:
            long.append((path, desc_len))
        
        if re.search(r'<meta\s+name=["\']robots["\'].*noindex', content, re.IGNORECASE):
            noindex_pages.append(path)

print(f'Total HTML files: {total}')
print(f'Missing desc: {len(missing)}')
print(f'Short desc (<100 chars): {len(short)}')
print(f'Long desc (>170 chars): {len(long)}')
print(f'Noindex pages: {len(noindex_pages)}')

if missing:
    print(f'\n=== MISSING DESC (first 10) ===')
    for p in missing[:10]:
        print(f'  {p}')

if noindex_pages:
    print(f'\n=== NOINDEX PAGES ===')
    for p in noindex_pages[:30]:
        print(f'  {p}')

# Short desc grouped
ranges = {'0-50': 0, '50-70': 0, '70-90': 0, '90-100': 0}
for _, l, _ in short:
    if l < 50: ranges['0-50'] += 1
    elif l < 70: ranges['50-70'] += 1
    elif l < 90: ranges['70-90'] += 1
    else: ranges['90-100'] += 1
print(f'\n=== Short desc distribution ===')
for k, v in ranges.items():
    print(f'  {k}: {v}')
