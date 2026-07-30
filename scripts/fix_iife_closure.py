#!/usr/bin/env python3
"""修复多余IIFE闭合 - 删除多余的})();"""
import re, glob, subprocess, tempfile, os

def fix_extra_iife(filepath):
    html = open(filepath, errors='ignore').read()
    tool = os.path.basename(os.path.dirname(filepath))
    
    scripts = list(re.finditer(r'<script>(.*?)</script>', html, re.DOTALL))
    main_idx = -1
    main_len = 0
    for i, m in enumerate(scripts):
        content = m.group(1).strip()
        if not content: continue
        if 'dataLayer' in content[:50] or 'gtag' in content[:30]: continue
        if 'application/ld+json' in content[:30]: continue
        if len(content) > main_len:
            main_len = len(content)
            main_idx = i
    
    if main_idx == -1:
        return False, 'no_main_script'
    
    main_match = scripts[main_idx]
    main_js = main_match.group(1)
    
    # 找所有 })();
    iife_closes = list(re.finditer(r'\}\)\s*\(\s*\)\s*;', main_js))
    
    if len(iife_closes) <= 1:
        return False, 'no_extra_iife'
    
    # 保留最后一个（真正的IIFE闭合），删除前面的
    # 但实际上，很多页面有多个独立的小IIFE，不能简单删除
    # 策略：只删除JS末尾多余的（最后一个script闭合前的）
    
    # 检查JS末尾是否有多余的
    js_stripped = main_js.rstrip()
    
    # 如果末尾是 })(); 且括号不匹配，说明有多余
    paren_diff = main_js.count('(') - main_js.count(')')
    brace_diff = main_js.count('{') - main_js.count('}')
    
    if abs(paren_diff) <= 3 and abs(brace_diff) <= 2:
        return False, 'already_balanced'
    
    # 尝试删除末尾多余的 })();
    # 从后往前找
    new_js = main_js
    changed = True
    iterations = 0
    while changed and iterations < 10:
        changed = False
        iterations += 1
        new_paren = new_js.count('(') - new_js.count(')')
        new_brace = new_js.count('{') - new_js.count('}')
        
        if new_paren > 3 and new_js.rstrip().endswith(')();'):
            # 末尾有多余的 })();
            # 删除最后一个
            stripped = new_js.rstrip()
            # 找到末尾的 })(); 
            last_iife = stripped.rfind('})();')
            if last_iife > 0:
                # 检查删除后是否改善
                test_js = stripped[:last_iife]
                test_paren = test_js.count('(') - test_js.count(')')
                if abs(test_paren) < abs(new_paren):
                    new_js = test_js + '\n'
                    changed = True
                else:
                    break
            else:
                break
        elif new_paren < -3:
            # 缺少(，在末尾加
            new_js = new_js.rstrip() + '(' * abs(new_paren) + ';\n'
            changed = True
        elif new_brace < -2:
            # 缺少{
            break  # 不能简单加
        else:
            break
    
    if new_js == main_js:
        return False, 'no_change'
    
    # 验证
    all_scripts = re.findall(r'<script>(.*?)</script>', html[:main_match.start()] + '<script>' + new_js + '</script>' + html[main_match.end():], re.DOTALL)
    js_full = '\n'.join(s.strip() for s in all_scripts if s.strip() and 'dataLayer' not in s[:50] and 'gtag' not in s[:30] and 'application/ld+json' not in s[:30])
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as tmp:
        tmp.write(js_full)
        tmp_path = tmp.name
    
    try:
        r = subprocess.run(['node', '--check', tmp_path], capture_output=True, text=True, timeout=5)
        if r.returncode != 0:
            return False, f'node_check_failed: {r.stderr.strip()[:80]}'
    except:
        return False, 'timeout'
    finally:
        os.unlink(tmp_path)
    
    new_html = html[:main_match.start()] + '<script>' + new_js + '</script>' + html[main_match.end():]
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_html)
    
    return True, f'fixed_iife: paren={main_js.count("(")-main_js.count(")")}→{new_js.count("(")-new_js.count(")")}'

os.chdir('/home/chison/tools-site')
fixed = []
failed = []

for f in sorted(glob.glob('*/index.html')) + sorted(glob.glob('en/*/index.html')):
    html = open(f, errors='ignore').read()
    scripts = re.findall(r'<script>(.*?)</script>', html, re.DOTALL)
    js_parts = [s.strip() for s in scripts if s.strip() and 'dataLayer' not in s[:50] and 'gtag' not in s[:30] and 'application/ld+json' not in s[:30]]
    if not js_parts: continue
    js = '\n'.join(js_parts)
    
    paren_diff = js.count('(') - js.count(')')
    brace_diff = js.count('{') - js.count('}')
    has_extra_iife = js.rstrip().endswith(')();') and js.count(')();') > 1
    
    if abs(paren_diff) <= 3 and abs(brace_diff) <= 2 and not has_extra_iife:
        continue
    
    ok, msg = fix_extra_iife(f)
    tool = f.replace('/index.html', '')
    if ok:
        fixed.append((tool, msg))
    else:
        failed.append((tool, msg))

print(f"IIFE修复结果: {len(fixed)} 成功, {len(failed)} 失败")
for tool, msg in fixed[:20]:
    print(f"  ✅ {tool}: {msg}")
if failed:
    print(f"\n失败({len(failed)}):")
    for tool, msg in failed[:10]:
        print(f"  ❌ {tool}: {msg}")
