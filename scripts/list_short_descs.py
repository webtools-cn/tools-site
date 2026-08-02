#!/usr/bin/env python3
"""Extract too-short descriptions with tool names for prioritization."""
import os, re

results = []

for root, dirs, files in os.walk('.'):
    dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', 'quality', '.gsc-data', 'scripts', 'css', 'js']]
    for f in files:
        if f == 'index.html' and '/en/' not in root:
            path = os.path.join(root, f)
            try:
                with open(path) as fh:
                    content = fh.read(5000)
                m = re.search(r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']+)["\']', content)
                title_m = re.search(r'<title>([^<]+)</title>', content)
                if m:
                    desc = m.group(1)
                    l = len(desc)
                    if l < 100:
                        title = title_m.group(1) if title_m else os.path.basename(os.path.dirname(path))
                        results.append((l, path, title.strip()))
            except:
                pass

# Sort by length ascending (shortest first)
results.sort()
print(f'Total too-short: {len(results)}')
print()
for l, p, t in results[:50]:
    print(f'{l:4d} | {t}')