#!/usr/bin/env python3
"""Correctly detect meta description lengths - v2."""
import os, re

results = []
for root, dirs, files in os.walk('.'):
    if '.git' in root or 'scripts' in root or 'quality' in root:
        continue
    for f in files:
        if f == 'index.html':
            path = os.path.join(root, f)
            with open(path, 'r') as fh:
                content = fh.read()
            
            # Find meta description line and extract content
            desc = None
            for line in content.split('\n'):
                if 'name="description"' in line or "name='description'" in line:
                    m = re.search(r'content=["\'](.+?)["\']\s*(?:/>|>)', line)
                    if m:
                        desc = m.group(1)
                    break
            
            desc_len = len(desc) if desc else 0
            
            # Check for noindex
            noindex = 'noindex' in line if desc else False  # rough
            
            # Extract title
            tm = re.search(r'<title>([^<]+)</title>', content)
            title = tm.group(1) if tm else 'MISSING'
            
            lang = 'EN' if '/en/' in path or path == './en/index.html' else 'CN'
            
            if desc_len == 0:
                status = 'MISSING'
            elif desc_len < 100:
                status = 'SHORT'
            elif desc_len > 160:
                status = 'LONG'
            else:
                status = 'OK'
            
            if noindex:
                status = 'NOINDEX_' + status
            
            results.append({
                'path': path,
                'lang': lang,
                'desc_len': desc_len,
                'status': status
            })

missing = [r for r in results if r['status'].startswith('MISSING')]
short = [r for r in results if r['status'].startswith('SHORT')]
long = [r for r in results if r['status'].startswith('LONG')]
ok = [r for r in results if r['status'] == 'OK']

print(f'Total pages: {len(results)}')
print(f'OK: {len(ok)}')
print(f'MISSING: {len(missing)}')
print(f'SHORT (<100): {len(short)}')
print(f'LONG (>160): {len(long)}')
print()

if long:
    print(f'=== LONG ({len(long)}) ===')
    for r in sorted(long, key=lambda x: -x['desc_len']):
        print(f'  [{r["desc_len"]}] {r["path"]}')

if short:
    print(f'=== SHORT ({len(short)}) ===')
    for r in sorted(short, key=lambda x: x['desc_len']):
        print(f'  [{r["desc_len"]}] {r["path"]}')

if missing:
    print(f'=== MISSING ({len(missing)}) ===')
    for r in missing:
        print(f'  {r["path"]}')
