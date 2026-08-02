#!/usr/bin/env python3
"""Check meta description lengths for CN tool pages."""
import os
import re

results = {'too_short': [], 'good': [], 'too_long': [], 'missing': []}
count = 0

for root, dirs, files in os.walk('.'):
    dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', 'quality', '.gsc-data', 'scripts', 'css', 'js']]
    for f in files:
        if f == 'index.html' and '/en/' not in root:
            path = os.path.join(root, f)
            count += 1
            try:
                with open(path) as fh:
                    content = fh.read(5000)
                m = re.search(r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']+)["\']', content)
                if m:
                    desc = m.group(1)
                    l = len(desc)
                    if l < 100:
                        results['too_short'].append((path, l))
                    elif l > 160:
                        results['too_long'].append((path, l))
                    else:
                        results['good'].append((path, l))
                else:
                    results['missing'].append(path)
            except:
                pass

print(f'Total CN pages: {count}')
print(f'Good (100-160): {len(results["good"])}')
print(f'Too short (<100): {len(results["too_short"])}')
print(f'Too long (>160): {len(results["too_long"])}')
print(f'Missing: {len(results["missing"])}')
print()
print('=== TOO SHORT ===')
for p, l in results['too_short'][:30]:
    print(f'{l:4d} | {p}')
if len(results['too_short']) > 30:
    print(f'... and {len(results["too_short"]) - 30} more')
print()
print('=== MISSING ===')
for p in results['missing'][:10]:
    print(f'   - | {p}')
if len(results['missing']) > 10:
    print(f'... and {len(results["missing"]) - 10} more')
