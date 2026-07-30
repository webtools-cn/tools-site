#!/usr/bin/env python3
"""全站JS语法检测 - 比Puppeteer快100倍"""
import re, glob, subprocess, tempfile, os
from collections import Counter

errors = Counter()
error_tools = []
total = 0
js_ok = 0
js_err = 0
no_js = 0

for f in sorted(glob.glob('*/index.html')):
    total += 1
    html = open(f, errors='ignore').read()
    tool = f.replace('/index.html', '')
    
    scripts = re.findall(r'<script>(.*?)</script>', html, re.DOTALL)
    js_parts = []
    for s in scripts:
        s = s.strip()
        if not s:
            continue
        if 'dataLayer' in s[:50] or 'gtag' in s[:30]:
            continue
        if 'application/ld+json' in s[:30]:
            continue
        js_parts.append(s)
    
    if not js_parts:
        no_js += 1
        continue
    
    js = '\n'.join(js_parts)
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as tmp:
        tmp.write(js)
        tmp_path = tmp.name
    
    try:
        r = subprocess.run(['node', '--check', tmp_path], capture_output=True, text=True, timeout=5)
        if r.returncode == 0:
            js_ok += 1
        else:
            js_err += 1
            err_msg = r.stderr.strip().split('\n')[-1] if r.stderr else 'unknown'
            if 'Unexpected' in err_msg or 'Invalid' in err_msg:
                errors['语法错误-Unexpected'] += 1
            elif 'Illegal return' in err_msg:
                errors['语法错误-Illegal return'] += 1
            elif 'missing' in err_msg:
                errors['语法错误-missing'] += 1
            elif 'Unexpected end' in err_msg:
                errors['语法错误-Unexpected end'] += 1
            else:
                errors['语法错误-其他'] += 1
            error_tools.append((tool, err_msg[:80]))
    except subprocess.TimeoutExpired:
        js_err += 1
        errors['超时'] += 1
    except Exception as e:
        js_err += 1
        errors[f'异常:{str(e)[:30]}'] += 1
    finally:
        os.unlink(tmp_path)

print(f"=== CN页面JS语法全量检测 ===")
print(f"总页面: {total}")
print(f"JS正常: {js_ok}")
print(f"无功能JS: {no_js}")
print(f"JS错误: {js_err}")
print(f"通过率: {(js_ok+no_js)/total*100:.1f}%")
print()
print("错误分类:")
for k, v in errors.most_common():
    print(f"  {v:4d} | {k}")
print()
print("所有错误页面:")
for tool, err in error_tools:
    print(f"  {tool}: {err}")
