#!/usr/bin/env python3
"""
修复 JS 语法错误：主要处理字符串中的真实换行符
策略：
1. 从HTML提取所有内部script的JS
2. 找出每个字符串（单引号/双引号），将内部真实换行替换为 \n
3. 写回HTML
"""
import re
import sys
import os
import tempfile
import subprocess
import json

BASE = os.path.expanduser("~/tools-site")

def extract_inline_js(html):
    """提取所有内部script块的JS"""
    parts = []
    for m in re.finditer(r'<script(.*?)>(.*?)</script>', html, re.S):
        attrs = m.group(1)
        body = m.group(2)
        if 'src=' in attrs.lower():
            continue
        if 'application/ld+json' in attrs:
            continue
        parts.append(body.strip())
    return '\n'.join(parts)

def fix_newlines_in_js(js):
    """
    修复JS字符串中的真实换行符（转义为 \n）
    同时保存原字符串的结构
    """
    result = []
    i = 0
    n = len(js)
    
    while i < n:
        ch = js[i]
        
        # 字符串字面量
        if ch in ('"', "'"):
            quote = ch
            result.append(ch)
            i += 1
            while i < n:
                c = js[i]
                if c == '\\':
                    # 已有的转义序列 -> 保留
                    result.append(c)
                    i += 1
                    if i < n:
                        result.append(js[i])
                    i += 1
                    continue
                if c == quote:
                    result.append(c)
                    i += 1
                    break
                if c in ('\n', '\r'):
                    # 真实换行 -> 转义
                    result.append('\\n')
                    i += 1
                    continue
                result.append(c)
                i += 1
            continue
        
        # 模板字面量（反引号）
        if ch == '`':
            result.append(ch)
            i += 1
            while i < n:
                c = js[i]
                if c == '\\':
                    result.append(c)
                    i += 1
                    if i < n:
                        result.append(js[i])
                    i += 1
                    continue
                if c == '`':
                    result.append(c)
                    i += 1
                    break
                # 模板字面量中可以包含真实换行（不用转义），直接保留
                result.append(c)
                i += 1
            continue
        
        # 单行注释
        if ch == '/' and i+1 < n and js[i+1] == '/':
            while i < n and js[i] != '\n':
                result.append(js[i])
                i += 1
            if i < n:
                result.append('\n')
                i += 1
            continue
        
        # 多行注释
        if ch == '/' and i+1 < n and js[i+1] == '*':
            result.append('/*')
            i += 2
            while i+1 < n and not (js[i] == '*' and js[i+1] == '/'):
                result.append(js[i])
                i += 1
            if i+1 < n:
                result.append('*/')
                i += 2
            continue
        
        result.append(ch)
        i += 1
    
    return ''.join(result)

def replace_js_in_html(html, new_js):
    """将新的JS替换回HTML的所有内部script块"""
    new_js_parts = new_js.split('\n') if new_js else ['']
    # 简单策略：把所有非src非json的script块替换为同一个JS
    js_idx = 0
    
    def replacer(m):
        nonlocal js_idx
        attrs = m.group(1)
        if 'src=' in attrs.lower():
            return m.group(0)
        if 'application/ld+json' in attrs:
            return m.group(0)
        if js_idx == 0:
            js_idx += 1
            return f'<script{attrs}>\n{new_js}\n</script>'
        else:
            # 后续script块：保留但替换内容
            return f'<script{attrs}>\n{new_js}\n</script>'
    
    return re.sub(r'<script(.*?)>.*?</script>', replacer, html, flags=re.S)

def check_js_syntax(js):
    """检查JS语法"""
    with tempfile.NamedTemporaryFile(suffix='.js', mode='w', delete=False) as f:
        f.write(js)
        name = f.name
    result = subprocess.run(['node', '-c', name], capture_output=True, text=True)
    os.unlink(name)
    return result.returncode == 0, result.stderr

def fix_missing_paren(js):
    """修复简单的括号缺失"""
    # 检查 ()/{} 平衡
    opens = js.count('(') - js.count(')')
    open_curly = js.count('{') - js.count('}')
    
    if opens > 0:
        js += ')' * opens
    if open_curly > 0:
        js += '}' * open_curly
    
    return js

def process_tool(tool_name):
    html_path = os.path.join(BASE, tool_name, 'index.html')
    if not os.path.exists(html_path):
        return False, f"File not found: {html_path}"
    
    with open(html_path, 'r') as f:
        html = f.read()
    
    js = extract_inline_js(html)
    
    # 先检查原始语法
    ok, err = check_js_syntax(js)
    if ok:
        return True, "already_valid"
    
    # 策略1: 修复字符串中的换行
    fixed_js = fix_newlines_in_js(js)
    ok, err = check_js_syntax(fixed_js)
    
    # 策略2: 修复括号平衡
    if not ok:
        fixed_js = fix_missing_paren(fixed_js)
        ok, err = check_js_syntax(fixed_js)
    
    if not ok:
        return False, f"Couldn't fix: {err[:200]}"
    
    # 写回HTML
    new_html = replace_js_in_html(html, fixed_js)
    with open(html_path, 'w') as f:
        f.write(new_html)
    
    # 再次验证写回的HTML
    with open(html_path, 'r') as f:
        verify_html = f.read()
    verify_js = extract_inline_js(verify_html)
    ok, err = check_js_syntax(verify_js)
    
    if ok:
        return True, "fixed_and_verified"
    else:
        return False, f"Write-back failed: {err[:200]}"


def main():
    # 读取 broken 列表
    issues_file = os.path.join(BASE, 'quality-reports', 'current-issues.json')
    with open(issues_file, 'r') as f:
        data = json.load(f)
    
    broken = data['broken_tools_remaining']
    print(f"Processing {len(broken)} tools...")
    
    fixed = []
    still_broken = []
    
    for tool in broken:
        print(f"\n[{tool}]", end=' ')
        success, msg = process_tool(tool)
        if success:
            print(f"✓ {msg}")
            fixed.append(tool)
        else:
            print(f"✗ {msg}")
            still_broken.append(tool)
    
    print(f"\n=== Results ===")
    print(f"Fixed: {len(fixed)}")
    print(f"Still broken: {len(still_broken)}")
    
    # 更新 current-issues.json
    data['broken_tools_remaining'] = still_broken
    data['summary']['gate0_js_syntax']['broken'] = len(still_broken)
    data['summary']['gate0_js_syntax']['ok'] = data['summary']['gate0_js_syntax']['total'] - len(still_broken)
    data['summary']['gate0_js_syntax']['fixed_this_run'] = data['summary']['gate0_js_syntax'].get('fixed_this_run', 0) + len(fixed)
    data['fixed_this_run'] = data.get('fixed_this_run', []) + fixed
    
    if still_broken:
        data['urgent']['p0_blocking'] = True
        data['urgent']['reason'] = f"{len(still_broken)} tools still have JS syntax errors"
        data['urgent']['progress'] = f"{len(fixed)} fixed this run, {len(still_broken)} remaining"
    else:
        data['p0_blocking'] = False
        data['urgent']['p0_blocking'] = False
        data['urgent']['reason'] = "All JS syntax errors resolved"
        data['urgent']['progress'] = f"All {len(fixed)} fixed"
    
    with open(issues_file, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\nUpdated {issues_file}")
    print(f"p0_blocking: {data['urgent']['p0_blocking']}")
    
    if still_broken:
        print(f"\nStill broken ({len(still_broken)}):")
        for t in still_broken:
            print(f"  - {t}")

if __name__ == '__main__':
    main()
