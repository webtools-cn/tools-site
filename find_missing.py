import re, glob

for f in sorted(glob.glob('*/index.html')):
    html = open(f, errors='ignore').read()
    scripts = re.findall(r'<script>(.*?)</script>', html, re.DOTALL)
    js_parts = [s.strip() for s in scripts if s.strip() and 'dataLayer' not in s[:50] and 'gtag' not in s[:30] and 'application/ld+json' not in s[:30]]
    if not js_parts: continue
    js = '\n'.join(js_parts)
    events = re.findall(r'(?:onclick|oninput|onchange)\s*=\s*["\x27]([^"\x27]+)["\x27]', html)
    event_fns = set()
    for e in events:
        m = re.match(r'(\w+)\s*\(', e)
        if m and m.group(1) not in ('if','else','for','while','return','this','document','window','event','e','typeof','void','not','and','or','true','false','null','undefined'):
            event_fns.add(m.group(1))
    fn_defs = set(re.findall(r'function\s+(\w+)\s*\(', js))
    missing = event_fns - fn_defs
    if missing:
        tool = f.replace('/index.html','')
        print(f'{tool}|{",".join(sorted(missing))}')
