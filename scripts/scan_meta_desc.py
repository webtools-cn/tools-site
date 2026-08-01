#!/usr/bin/env python3
import os, re

results = []
for root, dirs, files in os.walk('.'):
    if '/.' in root or 'quality' in root or 'scripts' in root or '.gsc-data' in root or 'node_modules' in root:
        continue
    for f in files:
        if f == 'index.html':
            path = os.path.join(root, f)
            try:
                with open(path, 'r', encoding='utf-8') as fh:
                    content = fh.read()
                m = re.search(r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']+)["\']', content, re.I)
                if not m:
                    results.append((path, 'MISSING', 0))
                else:
                    desc = m.group(1)
                    length = len(desc)
                    if length < 100 or length > 160:
                        results.append((path, desc[:100] + '...' if len(desc) > 100 else desc, length))
            except Exception as e:
                pass

results.sort(key=lambda x: x[2])
print(f'Total pages with description issues: {len(results)}')
print()
for path, desc, length in results[:40]:
    print(f'[{length:4d}] {path}')
    print(f'       {desc}')
    print()