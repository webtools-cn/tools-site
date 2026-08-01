#!/usr/bin/env python3
import os, re, json

results = []
for root, dirs, files in os.walk('.'):
    if '.git' in root or 'scripts' in root or 'quality' in root:
        continue
    for f in files:
        if f == 'index.html':
            path = os.path.join(root, f)
            with open(path, 'r') as fh:
                content = fh.read()
            
            # Extract meta description
            desc_pattern = r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']+)["\']'
            m = re.search(desc_pattern, content, re.IGNORECASE)
            desc = m.group(1) if m else 'MISSING'
            desc_len = len(desc) if desc != 'MISSING' else 0
            
            # Check for noindex
            noindex = '<meta name="robots" content="noindex"' in content or "name='robots'" in content and "noindex" in content
            
            # Extract title
            tm = re.search(r'<title>([^<]+)</title>', content)
            title = tm.group(1) if tm else 'MISSING'
            
            # Extract h1
            h1m = re.search(r'<h1[^>]*>([^<]+)</h1>', content)
            h1 = h1m.group(1) if h1m else 'MISSING'
            
            lang = 'EN' if '/en/' in path or path == './en/index.html' else 'CN'
            
            status = 'OK'
            if desc_len == 0:
                status = 'MISSING'
            elif desc_len < 100:
                status = 'SHORT'
            elif desc_len > 160:
                status = 'LONG'
            if noindex:
                status = 'NOINDEX_' + status
            
            results.append({
                'path': path,
                'lang': lang,
                'title': title,
                'h1': h1,
                'desc': desc,
                'desc_len': desc_len,
                'noindex': noindex,
                'status': status
            })

missing = [r for r in results if r['status'].startswith('MISSING')]
short = [r for r in results if r['status'].startswith('SHORT')]
long = [r for r in results if r['status'].startswith('LONG')]
noindex = [r for r in results if r['noindex']]
ok = [r for r in results if r['status'] == 'OK']

print(f'Total pages: {len(results)}')
print(f'OK: {len(ok)}')
print(f'MISSING: {len(missing)}')
print(f'SHORT (<100): {len(short)}')
print(f'LONG (>160): {len(long)}')
print(f'NOINDEX: {len(noindex)}')
print()

print('=== MISSING ===')
for r in missing:
    print(f'  {r["path"]} | {r["lang"]} | h1={r["h1"]}')

print()
print('=== SHORT (<100 chars) ===')
for r in sorted(short, key=lambda x: x['desc_len']):
    print(f'  [{r["desc_len"]}] {r["path"]} | {r["lang"]} | "{r["desc"]}"')

print()
print('=== LONG (>160 chars) ===')
for r in sorted(long, key=lambda x: -x['desc_len'])[:30]:
    print(f'  [{r["desc_len"]}] {r["path"]} | {r["lang"]}')

print()
print('=== NOINDEX ===')
for r in noindex:
    print(f'  {r["path"]} | {r["lang"]} | status={r["status"]}')
