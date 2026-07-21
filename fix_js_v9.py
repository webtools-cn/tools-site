#!/usr/bin/env python3
"""
v9 - 修复双重转义问题
文件中的 \\n (反斜杠+n) 应该是真正的换行符
但只替换不在字符串内的 \\n
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

def fix_double_escaped_newlines(body):
    """
    修复文件中 \\n (反斜杠+n) 被错误地当作换行转义的问题。
    在JS源码中，\\n 只在字符串内有效。在字符串外，它就是反斜杠+n，是语法错误。
    
    策略：逐字符扫描，在字符串外的 \\n 替换为真正的换行符。
    在字符串内的 \\n 保持不变（它们是合法的转义）。
    """
    result = []
    i = 0
    in_string = False
    string_quote = None
    
    while i < len(body):
        ch = body[i]
        
        # 跟踪字符串状态
        if not in_string:
            if ch in ("'", '"', '`'):
                in_string = True
                string_quote = ch
                result.append(ch)
                i += 1
                continue
            # 在字符串外，检查 \n 模式
            if ch == '\\' and i + 1 < len(body) and body[i+1] == 'n':
                # 这是字符串外的 \n，替换为真正的换行
                result.append('\n')
                i += 2
                continue
            if ch == '\\' and i + 1 < len(body) and body[i+1] == 't':
                # 字符串外的 \t，替换为真正的tab
                result.append('\t')
                i += 2
                continue
            if ch == '\\' and i + 1 < len(body) and body[i+1] == 'r':
                # 字符串外的 \r
                result.append('\r')
                i += 2
                continue
            result.append(ch)
            i += 1
        else:
            # 在字符串内
            if ch == '\\':
                result.append(ch)
                i += 1
                if i < len(body):
                    result.append(body[i])
                i += 1
                continue
            if ch == string_quote:
                in_string = False
                result.append(ch)
                i += 1
                continue
            # 字符串内的物理换行 → 转义
            if ch == '\n':
                result.append('\\n')
                i += 1
                continue
            if ch == '\r':
                result.append('\\r')
                i += 1
                continue
            result.append(ch)
            i += 1
    
    return ''.join(result)

def fix_file(html_path):
    with open(html_path) as f: html = f.read()
    blocks = extract_js_blocks(html)
    modified = False
    
    for start, end, body in reversed(blocks):
        ok, err = verify_js(body.strip())
        if ok:
            continue
        
        fixed = fix_double_escaped_newlines(body)
        
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
    broken = [
        "fancy-text-generator","html-entity-converter","html-meta-refresh-generator",
        "html-table-to-json","http-cache-header-generator",
        "markdown-to-pdf-converter","maze-generator",
        "md5-generator","meta-tag-generator","pdf-to-html","properties-to-yaml",
        "quiz-generator","receipt-generator","regex-cheatsheet","shopping-list-generator",
        "sql-migration-generator","sql-to-csv",
        "word-search-generator","workout-generator"
    ]
    
    fixed_list = []
    still_broken = []
    
    for tool in broken:
        html_path = os.path.join(BASE, tool, 'index.html')
        if not os.path.exists(html_path):
            still_broken.append(tool)
            continue
        
        print(f"[{tool}]", end=' ', flush=True)
        ok, err = fix_file(html_path)
        if ok:
            print("✓")
            fixed_list.append(tool)
        else:
            print(f"✗ {err[:80]}")
            still_broken.append(tool)
    
    print(f"\nFixed: {len(fixed_list)}, Still broken: {len(still_broken)}")
    if still_broken:
        print("Still broken:", still_broken)
    
    # Update issues file
    issues_file = os.path.join(BASE, 'quality-reports', 'current-issues.json')
    if os.path.exists(issues_file):
        with open(issues_file) as f:
            data = json.load(f)
        data['broken_tools_remaining'] = still_broken
        data['p0_blocking'] = bool(still_broken)
        data['urgent']['p0_blocking'] = bool(still_broken)
        with open(issues_file, 'w') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    return len(still_broken)

if __name__ == '__main__':
    remaining = main()
    sys.exit(0 if not remaining else 1)