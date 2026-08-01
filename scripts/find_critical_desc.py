#!/usr/bin/env python3
"""List all short CN pages (non-migrated) with meta desc < 70 chars + English versions."""
import os, re

results = []
en_results = []
for root, dirs, files in os.walk('.'):
    if '.git' in root or 'scripts' in root or 'quality' in root:
        continue
    for f in files:
        if not f.endswith('.html'):
            continue
        path = os.path.join(root, f)
        if '404' in path or 'feedback' in path or 'chrome-extension' in path or 'google' in path:
            continue
        if '/tools/' in path:  # category pages
            continue
        
        with open(path, 'r', encoding='utf-8', errors='ignore') as fh:
            content = fh.read()
        
        m = re.search(r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']*)["\']', content)
        if not m:
            continue
        desc = m.group(1)
        desc_len = len(desc)
        if desc_len >= 70:
            continue
        if '此工具已迁移' in desc:
            continue
        
        tool_slug = path.replace('./', '').replace('/index.html', '')
        if '/en/' in path:
            en_results.append((desc_len, tool_slug, desc[:150]))
        else:
            results.append((desc_len, tool_slug, desc[:150]))

results.sort()
en_results.sort()

print(f'=== CN tool pages (<70 chars, non-migrated): {len(results)} ===')
for l, slug, d in results:
    print(f'  [{l}] {slug}')
    print(f'       {d}')

print(f'\n=== EN tool pages (<70 chars, non-migrated): {len(en_results)} ===')
for l, slug, d in en_results[:20]:
    print(f'  [{l}] {slug}')
    print(f'       {d}')
if len(en_results) > 20:
    print(f'  ... and {len(en_results)-20} more')
