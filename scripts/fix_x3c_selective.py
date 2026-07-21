#!/usr/bin/env python3
"""修复被\x3C误替换的JS - 只保留字符串/模板字面量内的\x3C，其他还原为<"""
import subprocess, re, os

def check_tool_js(tool_dir):
    html_path = f'{tool_dir}/index.html'
    if not os.path.exists(html_path):
        return True  # skip
    with open(html_path) as f:
        content = f.read()
    scripts = re.findall(r'<script>(.*?)</script>', content, re.DOTALL)
    js_parts = []
    for s in scripts:
        s = s.strip()
        if not s: continue
        if s.startswith('{') and ('@context' in s or '"@type"' in s): continue
        js_parts.append(s)
    if not js_parts: return True
    js = '\n'.join(js_parts)
    r = subprocess.run(['node', '-c', '-'], input=js, capture_output=True, text=True, timeout=5)
    return r.returncode == 0

def selective_fix(tool_dir):
    html_path = f'{tool_dir}/index.html'
    with open(html_path) as f:
        content = f.read()
    
    new_content = content
    
    # 对每个script块，把\x3C还原为<，但保留字符串内的\x3C
    def fix_script(match):
        script_content = match.group(1)
        if script_content.strip().startswith('{') and ('@context' in script_content or '"@type"' in script_content):
            return match.group(0)
        
        # 简单策略：把所有\x3C还原为<，然后只对字符串/模板字面量内的<重新替换
        # 但这太复杂了。更简单：把\x3C后面跟字母的保留（字符串内的HTML标签），
        # 把\x3C后面跟空格/数字/运算符的还原为<（比较运算符）
        fixed = re.sub(r'\\x3C(\s|[^A-Za-z/])', r'<\1', script_content)
        # 也还原 \x3C 后面跟 = 的情况 (<=)
        fixed = fixed.replace('\\x3C=', '<=')
        
        return '<script>' + fixed + '</script>'
    
    new_content = re.sub(r'<script>(.*?)</script>', fix_script, new_content, flags=re.DOTALL)
    
    if new_content != content:
        with open(html_path, 'w') as f:
            f.write(new_content)
        if check_tool_js(tool_dir):
            return 'fixed'
        else:
            # Still broken, revert
            with open(html_path, 'w') as f:
                f.write(content)
            return 'still_broken'
    return 'no_change'

if __name__ == '__main__':
    SKIP = {'_gen','__pycache__','en','libs','js','css','scripts','tools',
            '.git','data','about','blog','privacy-policy','terms-of-service','category',
            'calc','design','dev','fun','health','image','math','media','network',
            'office','pdf','security','seo','text','utility'}
    
    fixed = []
    still_broken = []
    
    for d in sorted(os.listdir('.')):
        if not os.path.isdir(d) or d in SKIP or d.startswith('.'): continue
        f = f'{d}/index.html'
        if not os.path.exists(f): continue
        if check_tool_js(d):
            continue  # already OK
        
        result = selective_fix(d)
        if result == 'fixed':
            fixed.append(d)
        elif result == 'still_broken':
            still_broken.append(d)
    
    print(f"Fixed: {len(fixed)}")
    print(f"Still broken: {len(still_broken)}")
    if still_broken:
        print("Still broken tools:")
        for t in still_broken[:30]:
            print(f"  {t}")
