#!/usr/bin/env python3
"""Extract tool name from path and generate proper meta descriptions for short ones."""
import os, re
from pathlib import Path

exclude = {'node_modules', '.git', 'scripts', 'quality', '.gsc-data', 'css', 'js', 'assets', 'images'}
non_tool = {
    'index.html', 'en/index.html',
    'about/index.html', 'contact/index.html', 'terms/index.html', 'privacy/index.html',
    'en/about/index.html', 'en/contact/index.html', 'en/terms/index.html', 'en/privacy/index.html',
    'dev/index.html'
}

# Tool-specific description templates based on tool type
def guess_tool_type(name, content):
    """Guess tool category for better description generation."""
    content_lower = content[:5000].lower() if content else ""
    name_lower = name.lower()
    
    if any(k in name_lower for k in ['calculator', 'calc', 'converter', 'convert', 'generator', 'maker', 'creator', 'builder', 'finder', 'checker', 'tester', 'analyzer', 'viewer', 'editor', 'reader', 'tracker', 'planner', 'timer', 'counter', 'parser', 'scanner', 'extractor', 'resizer', 'compressor', 'encoder', 'decoder', 'formatter', 'validator', 'visualizer', 'monitor']):
        pass
    
    return 'general'

root = Path('.')

# Collect all short desc pages first
short_pages = []
for filepath in root.rglob('index.html'):
    rel = str(filepath)
    parts = set(rel.split('/'))
    if parts & exclude:
        continue
    if rel[2:] in non_tool:
        continue
    
    content = filepath.read_text(encoding='utf-8')
    
    m = re.search(r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']+)["\']', content, re.IGNORECASE)
    desc = m.group(1) if m else 'MISSING'
    desc_len = len(desc)
    
    if desc_len >= 100:
        continue
    
    # Extract h1
    h1m = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.IGNORECASE)
    h1 = re.sub(r'<[^>]+>', '', h1m.group(1)) if h1m else ''
    
    # Extract title
    tm = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
    title = tm.group(1) if tm else ''
    
    lang = 'EN' if '/en/' in rel else 'CN'
    short_pages.append({
        'path': rel,
        'len': desc_len,
        'desc': desc,
        'title': title,
        'h1': h1,
        'lang': lang,
        'content': content
    })

# Sort by length ascending
short_pages.sort(key=lambda x: x['len'])

# Focus on worst offenders first: <80 chars
print(f"Total short pages: {len(short_pages)}")
print(f"Pages with desc < 80 chars: {len([p for p in short_pages if p['len'] < 80])}")
print()

# Show the first 50 worst ones (shortest)
print("=== 50 WORST descriptions ===")
for p in short_pages[:50]:
    print(f"[{p['len']:3d}] {p['lang']} {p['path']}")
    print(f"      DESC: {p['desc']}")
    print(f"      H1: {p['h1']}")
    print(f"      TITLE: {p['title']}")
    print()