#!/usr/bin/env python3
"""SEO audit: check meta description length and noindex tags."""
import os, re

html_files = []
for root, dirs, files in os.walk('/home/chison/tools-site'):
    dirs[:] = [d for d in dirs if d not in ('.git', 'node_modules', 'quality', 'scripts', 'tests', '.gsc-data')]
    for f in files:
        if f == 'index.html':
            html_files.append(os.path.join(root, f))

results = []
for f in sorted(html_files):
    try:
        with open(f, 'r', encoding='utf-8') as fh:
            content = fh.read()
        
        # Extract meta description
        m = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', content)
        if not m:
            m = re.search(r"<meta\s+name='description'\s+content='([^']*)'", content)
        desc = m.group(1) if m else 'MISSING'
        desc_len = len(desc) if desc != 'MISSING' else 0
        
        # Check noindex
        noindex = 'noindex' in content.lower()
        
        # Extract title
        t = re.search(r'<title>([^<]*)</title>', content)
        title = t.group(1) if t else 'MISSING'
        
        flag = ''
        if desc == 'MISSING':
            flag = 'MISSING'
        elif desc_len < 100:
            flag = f'TOO_SHORT({desc_len})'
        elif desc_len > 160:
            flag = f'TOO_LONG({desc_len})'
        
        if flag or noindex:
            results.append((f, flag if flag else 'OK', desc_len, noindex, desc[:200]))
    except Exception as e:
        pass

print(f'Total files scanned: {len(html_files)}')
print(f'Issues found: {len(results)}')
print()

# Separate by issue type
too_short = [(f, d, dl) for f, fl, dl, ni, d in results if 'TOO_SHORT' in fl]
too_long = [(f, d, dl) for f, fl, dl, ni, d in results if 'TOO_LONG' in fl]
missing = [(f, d, dl) for f, fl, dl, ni, d in results if fl == 'MISSING']
has_noindex = [(f, fl, dl, ni) for f, fl, dl, ni, d in results if ni]

print(f'TOO SHORT (<100 chars): {len(too_short)}')
print(f'TOO LONG (>160 chars): {len(too_long)}')
print(f'MISSING description: {len(missing)}')
print(f'HAS noindex: {len(has_noindex)}')
print()

print('=' * 80)
print('TOO SHORT (need expansion):')
for f, d, dl in too_short:
    print(f'  [{dl}c] {f}')
    print(f'    "{d}"')
    print()

print('=' * 80)
print('TOO LONG (need trimming):')
for f, d, dl in too_long:
    print(f'  [{dl}c] {f}')
    print(f'    "{d}"')
    print()

print('=' * 80)
print('MISSING description:')
for f, d, dl in missing:
    print(f'  {f}')

print('=' * 80)
print('HAS noindex:')
for f, fl, dl, ni in has_noindex:
    print(f'  {f}  flag={fl}')