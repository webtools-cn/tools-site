#!/usr/bin/env python3
"""Scan all tool pages for meta description length and noindex issues."""
import os, re
from pathlib import Path

results = []
exclude = {'node_modules', '.git', 'scripts', 'quality', '.gsc-data', 'css', 'js', 'assets', 'images'}
non_tool = {
    'index.html', 'en/index.html',
    'about/index.html', 'contact/index.html', 'terms/index.html', 'privacy/index.html',
    'en/about/index.html', 'en/contact/index.html', 'en/terms/index.html', 'en/privacy/index.html',
    'dev/index.html'
}

root = Path('.')

for filepath in root.rglob('index.html'):
    rel = str(filepath)
    # skip excluded dirs
    parts = set(rel.split('/'))
    if parts & exclude:
        continue
    # skip non-tool pages
    if rel[2:] in non_tool:
        continue
    
    content = filepath.read_text(encoding='utf-8')
    
    # meta description
    m = re.search(r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']+)["\']', content, re.IGNORECASE)
    desc = m.group(1) if m else 'MISSING'
    desc_len = len(desc)
    
    # title
    tm = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
    title = tm.group(1) if tm else 'MISSING'
    
    # noindex in head
    head = content[:1000].lower()
    noindex = 'noindex' in head
    
    # canonical
    canon = re.search(r'<link\s+rel=["\']canonical["\'][^>]*href=["\']([^"\']+)["\']', content, re.IGNORECASE)
    canonical = canon.group(1) if canon else 'MISSING'
    
    lang = 'EN' if '/en/' in rel else 'CN'
    results.append({
        'len': desc_len,
        'path': rel,
        'desc': desc,
        'title': title,
        'lang': lang,
        'noindex': noindex,
        'canonical': canonical
    })

# Sort by length
results.sort(key=lambda x: x['len'])

print(f'Total tool pages scanned: {len(results)}')
print()

# Short descriptions (<100 chars)
short = [r for r in results if r['len'] < 100 and r['len'] > 0]
print(f'=== SHORT descriptions (<100 chars): {len(short)} pages ===')
for r in short[:30]:
    print(f"[{r['len']:3d}] {r['lang']} {r['path']}")
    print(f"      DESC: {r['desc']}")
    print(f"      NOINDEX: {r['noindex']} | CANON: {r['canonical'][:60]}")
    print()

# Long descriptions (>160 chars)
long_list = [r for r in results if r['len'] > 160]
print(f'=== LONG descriptions (>160 chars): {len(long_list)} pages ===')
for r in long_list[:15]:
    print(f"[{r['len']:3d}] {r['lang']} {r['path']}")
    print(f"      DESC: {r['desc'][:100]}...")
    print(f"      NOINDEX: {r['noindex']} | CANON: {r['canonical'][:60]}")
    print()

# Missing
missing = [r for r in results if r['len'] == 0 or r['desc'] == 'MISSING']
print(f'=== MISSING descriptions: {len(missing)} pages ===')
for r in missing:
    print(f"  {r['lang']} {r['path']} | NOINDEX: {r['noindex']}")

# Noindex
noindex_pages = [r for r in results if r['noindex']]
print(f'\n=== NOINDEX pages: {len(noindex_pages)} pages ===')
for r in noindex_pages:
    print(f"  {r['lang']} {r['path']}")

# Distribution stats
lengths = [r['len'] for r in results if r['len'] > 0]
if lengths:
    print(f'\n=== STATS ===')
    print(f'  Min: {min(lengths)} | Max: {max(lengths)} | Avg: {sum(lengths)//len(lengths)}')
    print(f'  <100: {len(short)} | 100-160: {len([r for r in results if 100 <= r["len"] <= 160])} | >160: {len(long_list)}')
