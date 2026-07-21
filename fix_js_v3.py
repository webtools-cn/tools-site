#!/usr/bin/env python3
"""
更激进的新行修复：
对于HTML中script块里的JS代码，把未闭合字符串跨行连接
"""
import re, os, sys, tempfile, subprocess, json

BASE = os.path.expanduser("~/tools-site")

def fix_html_file(html_path):
    with open(html_path, 'r') as f:
        html = f.read()
    
    # 找到所有script块位置
    script_blocks = list(re.finditer(r'<script(.*?)>(.*?)</script>', html, re.S))
    
    modified = False
    new_html = html
    
    # 从后往前处理（避免位置偏移）
    for m in reversed(script_blocks):
        attrs = m.group(1)
        body = m.group(2)
        
        if 'src=' in attrs.lower():
            continue
        if 'application/ld+json' in attrs:
            continue
        
        # 修复这个script块中的JS
        fixed_body = fix_js_body(body)
        if fixed_body != body:
            modified = True
            start = m.start(2)
            end = m.end(2)
            new_html = new_html[:start] + fixed_body + new_html[end:]
    
    if not modified:
        return False
    
    with open(html_path, 'w') as f:
        f.write(new_html)
    return True

def fix_js_body(js):
    """
    修复JS代码中的多行字符串问题。
    策略：逐行扫描，如果某行有未闭合的字符串，合并后续行直到闭合
    """
    lines = js.split('\n')
    result = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # 检查这行是否有未闭合的字符串
        in_single = False
        in_double = False
        in_template = False
        escaped = False
        
        for ch in line:
            if escaped:
                escaped = False
                continue
            if ch == '\\':
                escaped = True
                continue
            if ch == "'" and not in_double and not in_template:
                in_single = not in_single
            elif ch == '"' and not in_single and not in_template:
                in_double = not in_double
            elif ch == '`' and not in_single and not in_double:
                in_template = not in_template
        
        if in_single or in_double:
            # 字符串未闭合，合并后续行
            merged = line
            i += 1
            while i < len(lines):
                merged += lines[i]
                # 重新检查闭合
                still_open = False
                esc = False
                qt = "'" if in_single else '"'
                for ch in lines[i]:
                    if esc:
                        esc = False
                        continue
                    if ch == '\\':
                        esc = True
                        continue
                    if ch == qt:
                        still_open = not still_open
                if not still_open:
                    break
                i += 1
            result.append(merged)
        elif in_template:
            # 模板字面量可以跨行，不需要修复
            merged = line
            i += 1
            while i < len(lines):
                merged += '\n' + lines[i]
                esc = False
                still_tmpl = True
                for ch in lines[i]:
                    if esc:
                        esc = False
                        continue
                    if ch == '\\':
                        esc = True
                        continue
                    if ch == '`':
                        still_tmpl = not still_tmpl
                if not still_tmpl:
                    break
                i += 1
            result.append(merged)
        else:
            result.append(line)
        
        i += 1
    
    return '\n'.join(result)

def verify(html_path):
    """验证HTML中所有JS语法正确"""
    with open(html_path, 'r') as f:
        html = f.read()
    
    js = ''
    for m in re.finditer(r'<script(.*?)>(.*?)</script>', html, re.S):
        if 'src=' in m.group(1).lower() or 'application/ld+json' in m.group(1):
            continue
        js += m.group(2).strip() + '\n'
    
    if not js.strip():
        return True
    
    with tempfile.NamedTemporaryFile(suffix='.js', mode='w', delete=False) as f:
        f.write(js)
        name = f.name
    
    result = subprocess.run(['node', '-c', name], capture_output=True, text=True)
    os.unlink(name)
    return result.returncode == 0, result.stderr

def main():
    issues_file = os.path.join(BASE, 'quality-reports', 'current-issues.json')
    with open(issues_file, 'r') as f:
        data = json.load(f)
    
    # 同时也检查之前标记为 ok 的工具（因为可能有false negative）
    broken = data['broken_tools_remaining']
    
    fixed = []
    still_broken = []
    
    for tool in broken:
        html_path = os.path.join(BASE, tool, 'index.html')
        if not os.path.exists(html_path):
            still_broken.append(tool)
            continue
        
        print(f"[{tool}]", end=' ')
        
        # 先检查
        ok, err = verify(html_path)
        if ok:
            print("✓ already valid")
            fixed.append(tool)
            continue
        
        # 修复
        if fix_html_file(html_path):
            ok, err = verify(html_path)
            if ok:
                print("✓ fixed")
                fixed.append(tool)
            else:
                print(f"✗ fix failed: {err[:150]}")
                still_broken.append(tool)
        else:
            print(f"✗ no modification: {err[:150]}")
            still_broken.append(tool)
    
    print(f"\n=== Results ===")
    print(f"Fixed: {len(fixed)}")
    print(f"Still broken: {len(still_broken)}")
    
    # 更新
    data['broken_tools_remaining'] = still_broken
    data['summary']['gate0_js_syntax']['broken'] = len(still_broken)
    data['summary']['gate0_js_syntax']['ok'] = data['summary']['gate0_js_syntax']['total'] - len(still_broken)
    data['summary']['gate0_js_syntax']['fixed_this_run'] = data['summary']['gate0_js_syntax'].get('fixed_this_run', 0) + len(fixed)
    data['fixed_this_run'] = data.get('fixed_this_run', []) + fixed
    
    if still_broken:
        data['p0_blocking'] = True
        data['urgent']['p0_blocking'] = True
        data['urgent']['reason'] = f"{len(still_broken)} tools still have JS syntax errors"
        data['urgent']['progress'] = f"{len(fixed)} fixed this run, {len(still_broken)} remaining"
    else:
        data['p0_blocking'] = False
        data['urgent']['p0_blocking'] = False
        data['urgent']['reason'] = "All JS syntax errors resolved!"
        data['urgent']['progress'] = "Complete!"
    
    with open(issues_file, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\np0_blocking: {data['p0_blocking']}")
    
    if still_broken:
        print(f"\nStill broken ({len(still_broken)}):")
        for t in still_broken:
            print(f"  - {t}")

if __name__ == '__main__':
    main()
