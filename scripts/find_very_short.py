#!/usr/bin/env python3
"""Find severely short descriptions (<85 chars)."""
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
                m = re.search(r'<meta\s+name="description"\s+content="([^"]+)"', content)
                if not m:
                    m = re.search(r"<meta\s+name='description'\s+content='([^']+)'", content)
                if m:
                    desc = m.group(1)
                    l = len(desc)
                    if l < 85:
                        slug = path.replace('./', '').replace('/index.html', '')
                        results.append((l, slug, desc))
            except:
                pass

results.sort()
for l, slug, desc in results[:50]:
    print(f'{l:4d} | {slug} | {desc[:85]}')
print(f'\n... total <85: {len(results)}')
