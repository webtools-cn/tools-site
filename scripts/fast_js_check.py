#!/usr/bin/env python3
"""
全站JS快速检查 - 只检查语法错误和关键模式
"""
import re, os, subprocess, json
from datetime import datetime

SKIP = {'_gen','__pycache__','en','libs','js','css','scripts','tools',
        '.git','data','about','blog','privacy-policy','terms-of-service','category'}

syntax_errors = []
missing_h1 = []
no_js = []
ok_count = 0
total = 0

dirs = sorted([d for d in os.listdir('.') if os.path.isdir(d) and d not in SKIP and not d.startswith('.')])

for d in dirs:
    html_path = os.path.join(d, 'index.html')
    if not os.path.exists(html_path):
        continue
    total += 1
    
    try:
        with open(html_path) as f:
            content = f.read()
    except:
        continue
    
    # Check h1
    if '<h1' not in content.lower() and '<h1>' not in content:
        missing_h1.append(d)
    
    # Extract last inline script
    scripts = list(re.finditer(r'<script([^>]*)>(.*?)</script>', content, re.DOTALL))
    inline_scripts = []
    for m in scripts:
        attrs = m.group(1)
        body = m.group(2).strip()
        if 'application/ld+json' in attrs or 'src=' in attrs or not body:
            continue
        inline_scripts.append(body)
    
    if not inline_scripts:
        no_js.append(d)
        continue
    
    # Syntax check the last script (usually the main logic)
    last_js = inline_scripts[-1]
    r = subprocess.run(['node', '-c'], input=last_js, capture_output=True, text=True, timeout=5)
    if r.returncode != 0:
        err = r.stderr.strip()
        for line in err.split('\n'):
            if 'SyntaxError' in line:
                syntax_errors.append({'tool': d, 'error': line.strip()[:150]})
                break
    else:
        ok_count += 1

report = {
    'timestamp': datetime.now().isoformat(),
    'type': 'fast_js_check',
    'total': total,
    'ok': ok_count,
    'syntax_errors': len(syntax_errors),
    'missing_h1': len(missing_h1),
    'no_js': len(no_js),
    'syntax_error_list': syntax_errors[:50],
    'missing_h1_list': missing_h1[:50],
}

os.makedirs('quality-reports', exist_ok=True)
fname = f"quality-reports/fast-js-check-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
with open(fname, 'w') as f:
    json.dump(report, f, indent=2, ensure_ascii=False)

print(f'Total: {total} | OK: {ok_count} | Syntax errors: {len(syntax_errors)} | Missing h1: {len(missing_h1)} | No JS: {len(no_js)}')
if syntax_errors:
    print('\nSyntax errors (first 10):')
    for e in syntax_errors[:10]:
        print(f'  {e["tool"]}: {e["error"]}')