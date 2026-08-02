import os, re, glob

# Scan CN tool pages
short_meta = []
tool_dirs = glob.glob('*/') 
tool_dirs = [d for d in tool_dirs if not d.startswith('en/') and not d.startswith('.') and d not in ['css/','js/','scripts/','quality/']]

for d in sorted(tool_dirs):
    f = os.path.join(d, 'index.html')
    if not os.path.exists(f): continue
    with open(f) as fh:
        content = fh.read()
    pattern = r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']+)["\']'
    m = re.search(pattern, content, re.IGNORECASE)
    if m:
        desc = m.group(1)
        if len(desc) < 120:
            short_meta.append((d.strip('/'), len(desc), desc[:80]))
    else:
        short_meta.append((d.strip('/'), 0, 'MISSING'))

print(f'Total short/missing: {len(short_meta)}')
for name, length, snippet in short_meta[:50]:
    if length > 0:
        print(f'{length:>4} | {name}: {snippet}...')
    else:
        print(f'   0 | {name}: MISSING')
if len(short_meta) > 50:
    print(f'... and {len(short_meta)-50} more')