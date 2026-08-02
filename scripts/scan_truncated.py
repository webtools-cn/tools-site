#!/usr/bin/env python3
"""Find truncated meta descriptions."""
import os, re
from pathlib import Path

exclude = {'node_modules', '.git', 'scripts', 'quality', '.gsc-data', 'css', 'js', 'assets', 'images'}
non_tool = {
    'index.html', 'en/index.html',
    'about/index.html', 'contact/index.html', 'terms/index.html', 'privacy/index.html',
    'en/about/index.html', 'en/contact/index.html', 'en/terms/index.html', 'en/privacy/index.html',
    'dev/index.html'
}

root = Path('.')
truncated = []

for filepath in root.rglob('index.html'):
    rel = str(filepath)
    parts = set(rel.split('/'))
    if parts & exclude:
        continue
    if rel[2:] in non_tool:
        continue
    
    content = filepath.read_text(encoding='utf-8')
    m = re.search(r"""<meta\s+name=['"]description['"]\s+content=['"]([^"']+)['"]""", content, re.IGNORECASE)
    desc = m.group(1) if m else 'MISSING'
    desc_len = len(desc)
    
    if desc_len >= 100:
        continue
    
    # Check if truncated
    truncated_starters = ['/', '1和', '=', 'JPG', 'HTML', 'L/100km', 'EUR/USD', 'TF-IDF', 'SEO', 'ASCII', '100+', 'π', 'PDF']
    is_truncated = any(desc.startswith(s) for s in truncated_starters)
    
    lang = 'EN' if '/en/' in rel else 'CN'
    truncated.append((desc_len, rel, desc, is_truncated, lang))

truncated.sort(key=lambda x: (not x[3], x[0]))

print(f'Total short pages: {len(truncated)}')
print(f'Clearly truncated: {sum(1 for t in truncated if t[3])}')
print()

for t in truncated[:80]:
    marker = 'TRUNCATED' if t[3] else ''
    print(f"[{t[0]:3d}] {t[4]} {marker} {t[1]}")
    print(f"      DESC: {t[2][:120]}")
    print()