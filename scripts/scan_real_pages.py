#!/usr/bin/env python3
"""Find EN pages with real content and short description."""
import os, re

redirect_pattern = re.compile(r'已升级至新版本|has been upgraded|merged|Merged')

results = []

for root, dirs, files in os.walk('.'):
    if '/.' in root or 'quality' in root or 'scripts' in root or '.gsc-data' in root or 'node_modules' in root:
        continue
    for f in files:
        if f == 'index.html':
            path = os.path.join(root, f)
            if '/en/' not in path:
                continue
            try:
                with open(path, 'r', encoding='utf-8') as fh:
                    content = fh.read()
                
                # Skip redirect/merged pages
                if redirect_pattern.search(content[:500]):
                    continue
                
                # Check for real interactive content
                interactive = len(re.findall(r'<(input|textarea|button|select)\s', content, re.I))
                if interactive < 2:
                    continue
                
                # Extract description
                m = re.search(r'<meta\s+name=["\']description["\']\s+content="([^"]{1,400})"', content, re.I)
                if not m:
                    results.append(('MISSING', path, '', 0))
                    continue
                
                desc = m.group(1)
                length = len(desc)
                
                if length < 100 or length > 160:
                    results.append(('SHORT' if length < 100 else 'LONG', path, desc, length))
            except Exception as e:
                pass

short_en = [(p,d,l) for t,p,d,l in results if t=='SHORT']
long_en = [(p,d,l) for t,p,d,l in results if t=='LONG']
missing = [(p,d,l) for t,p,d,l in results if t=='MISSING']

short_en.sort(key=lambda x: x[2])
long_en.sort(key=lambda x: -x[2])

print(f"Real EN pages: short={len(short_en)}, long={len(long_en)}, missing={len(missing)}")
print()

for path, desc, length in short_en[:35]:
    tool = path.replace('./en/', '').replace('/index.html', '')
    print(f"[{length:3d}] {tool}")
    print(f"     |{desc}|")
    print()