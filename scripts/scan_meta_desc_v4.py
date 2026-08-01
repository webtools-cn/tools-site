#!/usr/bin/env python3
"""Correct scan: properly handle single quotes in content=""."""
import os, re

redirect_pattern = re.compile(r'已升级至新版本|has been upgraded')

all_short = []

for root, dirs, files in os.walk('.'):
    if '/.' in root or 'quality' in root or 'scripts' in root or '.gsc-data' in root or 'node_modules' in root:
        continue
    for f in files:
        if f == 'index.html':
            path = os.path.join(root, f)
            is_en = '/en/' in path
            try:
                with open(path, 'r', encoding='utf-8') as fh:
                    content = fh.read()
                
                # Match content up to closing "  (description NOT wrapped in single quotes)
                # content always uses double quotes
                m = re.search(r'<meta\s+name=["\']description["\']\s+content="([^"]{1,400})"', content, re.I)
                if not m:
                    # Try content with single quotes
                    m = re.search(r"<meta\s+name=[\"']description[\"']\s+content='([^']{1,400})'", content, re.I)
                
                if not m:
                    all_short.append(('MISSING', path, '', 0, is_en))
                    continue
                
                desc = m.group(1)
                length = len(desc)
                
                if redirect_pattern.search(desc):
                    continue
                
                if length < 100 or length > 160:
                    all_short.append(('SHORT' if length < 100 else 'LONG', path, desc, length, is_en))
            except Exception as e:
                pass

# Filter
short_en = [(p,d,l) for t,p,d,l,e in all_short if t=='SHORT' and e]
short_cn = [(p,d,l) for t,p,d,l,e in all_short if t=='SHORT' and not e]
long_en = [(p,d,l) for t,p,d,l,e in all_short if t=='LONG' and e]
long_cn = [(p,d,l) for t,p,d,l,e in all_short if t=='LONG' and not e]
missing = [(p,d,l) for t,p,d,l,e in all_short if t=='MISSING']

short_en.sort(key=lambda x: x[2])
short_cn.sort(key=lambda x: x[2])
long_en.sort(key=lambda x: -x[2])

print(f"EN short (<100): {len(short_en)} | CN short: {len(short_cn)}")
print(f"EN long (>160): {len(long_en)} | CN long: {len(long_cn)}")
print(f"MISSING: {len(missing)}")
print()

for path, desc, length in short_en[:35]:
    print(f"[{length:3d}] {path}")
    print(f"      |{desc}|")
    print()