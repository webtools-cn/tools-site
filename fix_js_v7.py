#!/usr/bin/env python3
"""
v7 - 自动修复JS括号不匹配问题
对每个script block，逐行计算括号累积差，找到缺闭合的行并修复
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

def fix_brace_imbalance(body):
    """修复花括号不匹配：找到缺闭合的行，在行末补}"""
    lines = body.split('\n')
    cumulative = 0
    fixed_lines = []
    
    for line in lines:
        diff = line.count('{') - line.count('}')
        cumulative += diff
        
        # 如果这行结束时cumulative > 0，但下一行开始新的语句（不是闭合）
        # 且这行以 ; 结尾，说明可能缺 }
        # 策略：如果行以 }; 结尾但实际缺 }，改为 }}; 等
        if cumulative > 0 and line.rstrip().endswith(';'):
            # 检查是否是赋值函数：xxx=function(){...};
            # 如果是，可能缺闭合
            stripped = line.rstrip()
            # 数一下这行应该有多少个闭合
            needed = cumulative  # 到这行为止还缺多少 }
            # 但不能盲目加，因为后面的行可能还有 }
            pass
        
        fixed_lines.append(line)
    
    # 如果最后cumulative > 0，在最后一行补 }
    if cumulative > 0:
        last = fixed_lines[-1] if fixed_lines else ''
        # 去掉末尾的 })();  如果有的话
        if last.strip().endswith('})();'):
            fixed_lines[-1] = last.rstrip()[:-5] + '}' * cumulative + '})();'
        else:
            fixed_lines[-1] = last.rstrip() + '\n' + '}' * cumulative
    
    return '\n'.join(fixed_lines)

def fix_newline_in_string_v2(body):
    """修复字符串中的物理换行 → \\n，但更智能地处理"""
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

def fix_file(html_path):
    with open(html_path) as f: html = f.read()
    blocks = extract_js_blocks(html)
    modified = False
    
    for start, end, body in reversed(blocks):
        # 先验证
        ok, err = verify_js(body.strip())
        if ok:
            continue
        
        fixed = body
        
        # 尝试修复换行
        fixed1 = fix_newline_in_string_v2(fixed)
        ok1, _ = verify_js(fixed1.strip())
        
        # 尝试修复括号
        fixed2 = fix_brace_imbalance(fixed)
        ok2, _ = verify_js(fixed2.strip())
        
        # 尝试两者
        fixed3 = fix_brace_imbalance(fix_newline_in_string_v2(fixed))
        ok3, _ = verify_js(fixed3.strip())
        
        # 选最好的
        if ok3:
            fixed = fixed3
        elif ok1:
            fixed = fixed1
        elif ok2:
            fixed = fixed2
        
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
        "sitemap-validator","sql-migration-generator","sql-to-csv",
        "word-search-generator","workout-generator"
    ]
    # markdown-previewer and html-wysiwyg-editor already fixed
    
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