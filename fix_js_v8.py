#!/usr/bin/env python3
"""
v8 - 批量修复IIFE闭合问题
模式: })(\n)\n} → })();  或  })();\n})(); → })();
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

def fix_iife_patterns(body):
    """修复常见的IIFE闭合模式"""
    fixed = body
    
    # 模式1: })(\n)\n} → })();
    fixed = re.sub(r'\}\)\(\s*\n\s*\)\s*\n\s*\}', '})();', fixed)
    
    # 模式2: })();\n})(); → })();  (重复IIFE闭合)
    fixed = re.sub(r'\}\)\(\);\s*\n\s*\}\)\(\);', '})();', fixed)
    
    # 模式3: })();\n}} → })();  (多余花括号)
    fixed = re.sub(r'\}\)\(\);\s*\n\s*\}\}', '})();', fixed)
    
    # 模式4: })();\n} → })();  (多余花括号)
    # 但要小心不要误删正常的 }
    
    return fixed

def fix_newline_in_string(body):
    """修复字符串中的物理换行"""
    result = []
    i = 0
    while i < len(body):
        ch = body[i]
        if ch in ("'", '"', '`'):
            quote = ch
            result.append(ch)
            i += 1
            while i < len(body):
                c2 = body[i]
                if c2 == '\\':
                    result.append(c2)
                    i += 1
                    if i < len(body):
                        result.append(body[i])
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
                result.append(c2)
                i += 1
        else:
            result.append(ch)
            i += 1
    return ''.join(result)

def fix_missing_close_braces(body):
    """在末尾补充缺失的闭合括号"""
    brace_diff = body.count('{') - body.count('}')
    paren_diff = body.count('(') - body.count(')')
    
    fixed = body.rstrip()
    
    # 如果末尾是 })(); 但缺括号
    if brace_diff > 0 and fixed.endswith('})();'):
        fixed = fixed[:-5] + '}' * brace_diff + '})();'
    elif brace_diff > 0:
        fixed = fixed + '\n' + '}' * brace_diff
    
    if paren_diff > 0:
        fixed = fixed + ')' * paren_diff
    
    return fixed

def fix_extra_close_braces(body):
    """去掉末尾多余的闭合括号"""
    brace_diff = body.count('{') - body.count('}')
    paren_diff = body.count('(') - body.count(')')
    
    fixed = body.rstrip()
    
    # 去掉多余的 }
    while brace_diff < 0 and fixed.endswith('}'):
        fixed = fixed[:-1].rstrip()
        brace_diff += 1
    
    # 去掉多余的 )
    while paren_diff < 0 and fixed.endswith(')'):
        fixed = fixed[:-1].rstrip()
        paren_diff += 1
    
    return fixed

def fix_file(html_path):
    with open(html_path) as f: html = f.read()
    blocks = extract_js_blocks(html)
    modified = False
    
    for start, end, body in reversed(blocks):
        ok, err = verify_js(body.strip())
        if ok:
            continue
        
        # 尝试多种修复策略
        strategies = [
            fix_iife_patterns,
            fix_newline_in_string,
            fix_missing_close_braces,
            fix_extra_close_braces,
            lambda b: fix_iife_patterns(fix_newline_in_string(b)),
            lambda b: fix_missing_close_braces(fix_newline_in_string(b)),
            lambda b: fix_extra_close_braces(fix_newline_in_string(b)),
            lambda b: fix_iife_patterns(fix_missing_close_braces(b)),
            lambda b: fix_iife_patterns(fix_extra_close_braces(b)),
            lambda b: fix_missing_close_braces(fix_iife_patterns(fix_newline_in_string(b))),
            lambda b: fix_extra_close_braces(fix_iife_patterns(fix_newline_in_string(b))),
        ]
        
        best_fixed = body
        for strategy in strategies:
            try:
                fixed = strategy(body)
                if fixed != body:
                    ok2, _ = verify_js(fixed.strip())
                    if ok2:
                        best_fixed = fixed
                        break
            except:
                continue
        
        if best_fixed != body:
            modified = True
            html = html[:start] + best_fixed + html[end:]
    
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