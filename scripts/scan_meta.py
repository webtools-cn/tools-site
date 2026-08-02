import os, re

short = []
skip = {'en','css','js','scripts','quality','chrome-extension','docs','cron-reports','.gsc-data','.git'}

for d in sorted(os.listdir('.')):
    if d in skip or not os.path.isdir(d) or d.startswith('.'):
        continue
    f = os.path.join(d, 'index.html')
    if not os.path.exists(f):
        continue
    with open(f) as fh:
        content = fh.read(3000)
    m = re.search(r'<meta name="description" content="([^"]*)"', content)
    if not m:
        continue
    desc = m.group(1)
    l = len(desc)
    if l < 100:
        tm = re.search(r'<title>([^<]+)</title>', content)
        title = tm.group(1) if tm else '?'
        short.append((l, d, title[:100]))

short.sort()
print(f"Total < 100 char: {len(short)}")
print()
for l, d, t in short[:30]:
    print(f'{l:3d} | {d:40s} | {t}')
