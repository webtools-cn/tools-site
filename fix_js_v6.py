#!/usr/bin/env python3
"""
v6 - 针对每类错误的精确修复
"""
import os, re, tempfile, subprocess, json, sys

BASE = os.path.expanduser("~/tools-site")

def verify_js(js_text):
    if not js_text.strip(): return True, ''
    with tempfile.NamedTemporaryFile(suffix='.js', mode='w', delete=False) as f:
        f.write(js_text); name = f.name
    r = subprocess.run(['node', '-c', name], capture_output=True, text=True)
    os.unlink(name)
    return r.returncode == 0, r.stderr.strip()

def extract_js_blocks(html):
    blocks = []
    for m in re.finditer(r'<script([^>]*)>(.*?)</script>', html, re.S):
        attrs = m.group(1)
        body = m.group(2)
        if 'src=' in attrs.lower() or 'application/ld+json' in attrs:
            continue
        blocks.append((m.start(2), m.end(2), body))
    return blocks

# === 修复策略 ===

def fix_newline_in_string(js):
    """修复字符串中的物理换行 → \\n"""
    result = []
    i = 0
    while i < len(js):
        ch = js[i]
        if ch in ("'", '"', '`'):
            quote = ch
            result.append(ch)
            i += 1
            while i < len(js):
                c2 = js[i]
                if c2 == '\\':
                    result.append(c2)
                    i += 1
                    if i < len(js):
                        result.append(js[i])
                    i += 1
                    continue
                if c2 == quote:
                    result.append(c2)
                    i += 1
                    break
                if c2 == '\n':
                    result.append('\\n')
                    i += 1
                    continue
                if c2 == '\r':
                    result.append('\\r')
                    i += 1
                    continue
                if c2 == '\t':
                    result.append('\\t')
                    i += 1
                    continue
                result.append(c2)
                i += 1
        else:
            result.append(ch)
            i += 1
    return ''.join(result)

def fix_iife_balance(js):
    """修复IIFE括号/花括号不匹配"""
    # 计算括号差
    opens = sum(1 for c in js if c == '(') - sum(1 for c in js if c == ')')
    braces = sum(1 for c in js if c == '{') - sum(1 for c in js if c == '}')
    
    fixed = js.rstrip()
    # 如果多闭括号，去掉末尾多余的
    while opens < 0 and fixed.endswith(')'):
        fixed = fixed[:-1].rstrip()
        opens += 1
    while braces < 0 and fixed.endswith('}'):
        fixed = fixed[:-1].rstrip()
        braces += 1
    # 如果缺括号，补上
    if opens > 0:
        fixed = fixed + '\n' + ')' * opens
    if braces > 0:
        fixed = fixed + '\n' + '}' * braces
    return fixed

def fix_missing_paren(js):
    """补充缺失的括号"""
    # 简单计数补全
    opens = sum(1 for c in js if c == '(') - sum(1 for c in js if c == ')')
    braces = sum(1 for c in js if c == '{') - sum(1 for c in js if c == '}')
    squares = sum(1 for c in js if c == '[') - sum(1 for c in js if c == ']')
    
    fixed = js.rstrip()
    if opens > 0:
        fixed = fixed + '\n' + ')' * opens
    if braces > 0:
        fixed = fixed + '\n' + '}' * braces
    if squares > 0:
        fixed = fixed + '\n' + ']' * squares
    return fixed

def fix_regex_flags(js):
    """修复正则表达式flag问题：.replace(/g, → .replace(//g,"""
    # 模式: .replace(/g,' → .replace(//g,'
    fixed = re.sub(r'\.replace\(/g\b', '.replace(//g', js)
    return fixed

def fix_escaped_script(js):
    """修复JS字符串中的 </script> — 已转义为 <\/script> 但可能被二次转义"""
    # 如果字符串中有 \\/script 可能是过度转义，不管它
    # 主要问题是多行字符串中混入了HTML
    return js

def fix_unexpected_token(js):
    """处理各种unexpected token"""
    # 先试试修复换行
    fixed = fix_newline_in_string(js)
    # 再试试修复括号
    fixed = fix_iife_balance(fixed)
    return fixed

def fix_other(js, tool):
    """特殊修复"""
    if tool == 'sql-migration-generator':
        # 这个文件的问题是多行字符串中有未转义的换行
        return fix_newline_in_string(js)
    return js

# === 主修复逻辑 ===

def fix_file(html_path, error_type):
    with open(html_path) as f: html = f.read()
    blocks = extract_js_blocks(html)
    modified = False
    
    # 反向处理以保持索引
    for start, end, body in reversed(blocks):
        if error_type == 'newline_in_string':
            fixed = fix_newline_in_string(body)
        elif error_type == 'iife_balance':
            fixed = fix_iife_balance(body)
        elif error_type == 'missing_paren':
            fixed = fix_missing_paren(body)
        elif error_type == 'regex_flags':
            fixed = fix_regex_flags(body)
        elif error_type == 'unexpected_token':
            fixed = fix_unexpected_token(body)
        else:
            tool = os.path.basename(os.path.dirname(html_path))
            fixed = fix_other(body, tool)
        
        if fixed != body:
            modified = True
            html = html[:start] + fixed + html[end:]
    
    if modified:
        with open(html_path, 'w') as f: f.write(html)
    
    # 重新验证
    blocks = extract_js_blocks(html)
    all_js = '\n'.join(b[2].strip() for b in blocks)
    ok, err = verify_js(all_js)
    return ok, err

def main():
    issues_file = os.path.join(BASE, 'quality-reports', 'current-issues.json')
    
    error_map = {
        'newline_in_string': ["html-entity-converter","markdown-to-pdf-converter","meta-tag-generator",
            "pdf-to-html","quiz-generator","receipt-generator","shopping-list-generator",
            "sql-to-csv","word-search-generator","workout-generator"],
        'iife_balance': ["html-wysiwyg-editor","http-cache-header-generator","markdown-previewer",
            "md5-generator","sitemap-validator"],
        'missing_paren': ["html-meta-refresh-generator","html-table-to-json","maze-generator","properties-to-yaml"],
        'unexpected_token': ["fancy-text-generator","regex-cheatsheet"],
        'other': ["sql-migration-generator"],
    }
    
    all_fixed = []
    all_broken = []
    
    for error_type, tools in error_map.items():
        for tool in tools:
            html_path = os.path.join(BASE, tool, 'index.html')
            if not os.path.exists(html_path):
                all_broken.append(tool)
                continue
            
            print(f"[{tool}] ({error_type})", end=' ', flush=True)
            ok, err = fix_file(html_path, error_type)
            if ok:
                print("✓")
                all_fixed.append(tool)
            else:
                print(f"✗ {err[:80]}")
                all_broken.append(tool)
    
    print(f"\n=== Results ===")
    print(f"Fixed: {len(all_fixed)}")
    print(f"Still broken: {len(all_broken)}")
    if all_broken:
        print("Still broken:", all_broken)
    
    # Update issues file
    if os.path.exists(issues_file):
        with open(issues_file) as f:
            data = json.load(f)
    else:
        data = {"urgent": {"p0_blocking": False}}
    
    data['broken_tools_remaining'] = all_broken
    data['p0_blocking'] = bool(all_broken)
    data['urgent']['p0_blocking'] = bool(all_broken)
    
    with open(issues_file, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    return len(all_broken)

if __name__ == '__main__':
    remaining = main()
    sys.exit(0 if not remaining else 1)