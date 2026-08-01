#!/usr/bin/env python3
"""Find short non-migrated Chinese tool pages that need meta desc fix."""
import os, re

results = []
for root, dirs, files in os.walk('.'):
    if '.git' in root or 'scripts' in root or 'quality' in root:
        continue
    for f in files:
        if not f.endswith('.html'):
            continue
        path = os.path.join(root, f)
        # Skip English pages, 404, feedback, chrome-extension, category pages
        if '/en/' in path or '404' in path or 'feedback' in path or 'chrome-extension' in path or 'google' in path:
            continue
        if path in ('./index.html',):
            continue  # homepage handled separately
        
        with open(path, 'r', encoding='utf-8', errors='ignore') as fh:
            content = fh.read()
        
        m = re.search(r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']*)["\']', content)
        if not m:
            continue
        desc = m.group(1)
        desc_len = len(desc)
        if desc_len >= 100:
            continue
        if '此工具已迁移' in desc:
            continue  # skip migrated pages
        
        # Get tool slug
        tool_slug = path.replace('./', '').replace('/index.html', '')
        # Skip category pages like tools/text, tools/converter
        if tool_slug.startswith('tools/'):
            continue
        
        results.append((desc_len, tool_slug, desc[:150]))

results.sort()
print(f'Non-migrated short desc Chinese tool pages: {len(results)}')
print()

for l, slug, d in results[:50]:
    print(f'[{l}] {slug}')
    print(f'    {d}')
    print()
