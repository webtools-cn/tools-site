#!/usr/bin/env python3
"""全站JS语法检查 - 用node -c验证每个工具的JS"""
import re, os, subprocess, json
from datetime import datetime

SKIP = {'_gen','__pycache__','en','libs','js','css','scripts','tools',
        '.git','data','about','blog','privacy-policy','terms-of-service','category'}

broken = []
ok = 0

for d in sorted(os.listdir('.')):
    if not os.path.isdir(d) or d in SKIP or d.startswith('.'):
        continue
    html = os.path.join(d, 'index.html')
    if not os.path.exists(html):
        continue
    
    with open(html) as f:
        content = f.read()
    
    scripts = list(re.finditer(r'<script([^>]*)>(.*?)</script>', content, re.DOTALL))
    last_js = None
    for m in reversed(scripts):
        attrs = m.group(1)
        body = m.group(2).strip()
        if 'application/ld+json' in attrs or 'src=' in attrs or not body:
            continue
        last_js = body
        break
    
    if not last_js:
        broken.append({'tool': d, 'error': 'NO_JS'})
        continue
    
    r = subprocess.run(['node', '-c'], input=last_js, capture_output=True, text=True, timeout=10)
    if r.returncode != 0:
        err = r.stderr.strip()
        lines = err.split('\n')
        error_msg = ''
        for line in lines:
            if 'SyntaxError' in line:
                error_msg = line.strip()
                break
        broken.append({'tool': d, 'error': error_msg[:150]})
    else:
        ok += 1

report = {
    'timestamp': datetime.now().isoformat(),
    'type': 'js_syntax_check',
    'total': ok + len(broken),
    'ok': ok,
    'broken': len(broken),
    'broken_list': broken
}

os.makedirs('quality-reports', exist_ok=True)
fname = f"quality-reports/js-check-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
with open(fname, 'w') as f:
    json.dump(report, f, indent=2, ensure_ascii=False)

print(json.dumps(report, indent=2, ensure_ascii=False))