#!/usr/bin/env python3
"""全站JS语法检测 - 用acorn批量解析，输出精确错误报告"""
import subprocess, re, os, json, sys
from collections import Counter

SKIP = {'_gen','__pycache__','en','libs','js','css','scripts','tools',
        '.git','data','about','blog','privacy-policy','terms-of-service','category',
        'calc','design','dev','fun','health','image','math','media','network',
        'office','pdf','security','seo','text','utility'}

WORKDIR = '/home/chison/tools-site'
REPORT_DIR = os.path.join(WORKDIR, 'quality-reports')

def extract_js_from_html(html_path):
    with open(html_path) as f:
        content = f.read()
    scripts = re.findall(r'<script>(.*?)</script>', content, re.DOTALL)
    js_parts = []
    for s in scripts:
        s = s.strip()
        if not s: continue
        if s.startswith('{') and ('@context' in s or '"@type"' in s): continue
        js_parts.append(s)
    return '\n'.join(js_parts) if js_parts else ''

def main():
    os.chdir(WORKDIR)
    os.makedirs(REPORT_DIR, exist_ok=True)
    
    # Collect all tool JS
    tools_js = {}
    for d in sorted(os.listdir('.')):
        if not os.path.isdir(d) or d in SKIP or d.startswith('.'): continue
        f = os.path.join(d, 'index.html')
        if not os.path.exists(f): continue
        js = extract_js_from_html(f)
        if js.strip():
            tools_js[d] = js
    
    # Write JS data to temp file (avoid arg list too long)
    tmp_js = os.path.join(REPORT_DIR, '_acorn_input.json')
    with open(tmp_js, 'w') as f:
        json.dump(tools_js, f)
    
    check_script = '''
const fs = require('fs');
const acorn = require('acorn');
const toolsData = JSON.parse(fs.readFileSync(''' + json.dumps(tmp_js) + ''', 'utf8'));
const results = [];
for (const [name, code] of Object.entries(toolsData)) {
    if (!code.trim()) { results.push({tool:name, ok:true}); continue; }
    try {
        acorn.parse(code, {ecmaVersion: 2022, locations: true});
        results.push({tool:name, ok:true});
    } catch(e) {
        results.push({
            tool: name,
            ok: false,
            line: e.loc ? e.loc.line : '?',
            column: e.loc ? e.loc.column : '?',
            message: e.message.slice(0, 150),
            code_snippet: code.split('\\n')[e.loc ? e.loc.line-1 : 0].slice(0, 120)
        });
    }
}
console.log(JSON.stringify(results));
'''
    
    r = subprocess.run(['node', '-e', check_script], capture_output=True, text=True, timeout=60, cwd=WORKDIR)
    
    try:
        results = json.loads(r.stdout)
    except:
        print(f"acorn check failed: {r.stderr[:500]}")
        sys.exit(1)
    
    ok = [r for r in results if r['ok']]
    broken = [r for r in results if not r['ok']]
    
    # Error type classification
    error_types = Counter()
    for b in broken:
        msg = b['message']
        if 'Unterminated string' in msg: error_types['string_not_closed'] += 1
        elif 'has already been declared' in msg: error_types['duplicate_declaration'] += 1
        elif 'Invalid regular expression' in msg: error_types['invalid_regex'] += 1
        elif 'Unexpected token' in msg: error_types['unexpected_token'] += 1
        elif 'Unsyntactic break' in msg: error_types['bad_break'] += 1
        elif 'Expecting Unicode' in msg: error_types['unicode_escape'] += 1
        else: error_types['other'] += 1
    
    # Write report
    report = {
        'timestamp': subprocess.check_output('date -Is', shell=True).decode().strip(),
        'total': len(results),
        'ok': len(ok),
        'broken': len(broken),
        'score': 0 if broken else 100,
        'error_types': dict(error_types),
        'broken_tools': broken
    }
    
    report_path = os.path.join(REPORT_DIR, 'acorn-errors.json')
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    # Summary output
    print(f"总工具: {len(results)}, OK: {len(ok)}, Broken: {len(broken)}, Score: {report['score']}")
    print(f"错误分类: {dict(error_types)}")
    print(f"报告: {report_path}")
    
    if broken:
        print(f"\n前10个broken工具:")
        for b in broken[:10]:
            print(f"  ❌ {b['tool']}:L{b['line']} {b['message'][:80]}")
    
    sys.exit(0 if not broken else 1)

if __name__ == '__main__':
    main()
