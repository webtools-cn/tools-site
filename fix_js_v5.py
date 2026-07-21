#!/usr/bin/env python3
"""
强力JS修复器 v5 - 针对每种错误类型的精确修复
"""
import re, os, tempfile, subprocess, json

BASE = os.path.expanduser("~/tools-site")

def get_all_js(html):
    """提取HTML中所有非外部非ld+json的script块的JS"""
    parts = []
    for m in re.finditer(r'<script(.*?)>(.*?)</script>', html, re.S):
        attrs = m.group(1)
        body = m.group(2)
        if 'src=' in attrs.lower() or 'application/ld+json' in attrs:
            continue
        parts.append((m.start(), m.end(), m.start(2), m.end(2), body))
    return parts

def verify_js(js_text):
    """用node -c验证JS"""
    if not js_text.strip():
        return True, ''
    with tempfile.NamedTemporaryFile(suffix='.js', mode='w', delete=False) as f:
        f.write(js_text)
        name = f.name
    result = subprocess.run(['node', '-c', name], capture_output=True, text=True)
    os.unlink(name)
    return result.returncode == 0, result.stderr.strip()

def fix_html(html_path):
    """智能修复HTML文件"""
    with open(html_path, 'r') as f:
        html = f.read()
    
    # 先验证整体JS
    all_js = ''
    for _, _, _, _, body in get_all_js(html):
        all_js += body.strip() + '\n'
    
    ok, err = verify_js(all_js)
    if ok:
        return True  # already good
    
    original = html
    modified = False
    
    # === 策略1: 修复未转义的多行字符串 ===
    # 逐块处理
    script_blocks = get_all_js(html)
    
    for s_start, s_end, body_start, body_end, body in reversed(script_blocks):
        fixed_body = body
        
        # 修复: 普通字符串中物理换行 → \\n
        # 使用逐字符扫描
        result = []
        i = 0
        while i < len(fixed_body):
            ch = fixed_body[i]
            
            if ch in ("'", '"'):
                quote = ch
                result.append(ch)
                i += 1
                while i < len(fixed_body):
                    c2 = fixed_body[i]
                    if c2 == '\\':
                        result.append(c2)
                        i += 1
                        if i < len(fixed_body):
                            result.append(fixed_body[i])
                        i += 1
                        continue
                    if c2 == quote:
                        result.append(c2)
                        i += 1
                        break
                    if c2 == '\n':
                        # 物理换行 → 转义
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
        
        fixed_body = ''.join(result)
        
        # 修复: 双IIFE问题 - })(); })(); → })(); 
        # 检测连续两个 })();
        fixed_body = re.sub(r'\}\);?\s*\n\s*\}\);?\s*$', '})();', fixed_body)
        
        # 修复: 末尾多余 }) 或 )} 配对
        # 统计括号
        opens = fixed_body.count('(') - fixed_body.count(')')
        braces = fixed_body.count('{') - fixed_body.count('}')
        
        # 如果多了闭括号，去掉末尾多余的
        if opens < 0:
            # 去掉末尾多余的 )
            stripped = fixed_body.rstrip()
            while opens < 0 and stripped.endswith(')'):
                stripped = stripped[:-1].rstrip()
                opens += 1
                modified = True
            if stripped != fixed_body.rstrip():
                fixed_body = stripped + '\n'
        
        if braces < 0:
            # 去掉末尾多余的 }
            stripped = fixed_body.rstrip()
            lines = stripped.split('\n')
            while lines and lines[-1].strip() == '}' and braces < 0:
                lines.pop()
                braces += 1
                modified = True
            fixed_body = '\n'.join(lines) + '\n'
        
        if opens > 0:
            fixed_body = fixed_body.rstrip() + '\n' + ')' * opens
            modified = True
        
        if braces > 0:
            fixed_body = fixed_body.rstrip() + '\n' + '}' * braces
            modified = True
        
        if fixed_body != body:
            modified = True
            html = html[:body_start] + fixed_body + html[body_end:]
    
    if modified:
        with open(html_path, 'w') as f:
            f.write(html)
    
    # 再次验证
    all_js = ''
    for _, _, _, _, body in get_all_js(html):
        all_js += body.strip() + '\n'
    
    ok, err = verify_js(all_js)
    return ok


def fix_html_v2(html_path):
    """第二层修复：处理更复杂的情况"""
    with open(html_path, 'r') as f:
        html = f.read()
    
    # 先看看还不行的话尝试什么
    all_js = ''
    script_blocks = get_all_js(html)
    for _, _, _, _, body in script_blocks:
        all_js += body.strip() + '\n'
    
    ok, err = verify_js(all_js)
    if ok:
        return True
    
    # 策略2: 对于某些特殊模式
    # - 字符串里有 </script> (HTML escaped) 
    # - .replace(/g,' ') → .replace(//g,' ')
    # - regex中的问题
    
    # 修复 replace(/g,' ') → replace(//g,' ')  
    # 这种出现在properties-to-yaml里
    
    modified = False
    for s_start, s_end, body_start, body_end, body in reversed(script_blocks):
        fixed_body = body
        
        # 修复: .replace(/g, 变成 .replace(//g,
        fixed_body = re.sub(r'\.replace\(/g\b', '.replace(//g', fixed_body)
        
        # 修复: 末尾多余的闭括号
        # 模式: })();\n\n})(); 
        fixed_body = re.sub(r'\);?\s*\n\s*\n\s*\n\s*\};?\s*\n\s*\n\s*$', '', fixed_body)
        fixed_body = re.sub(r'\);?\s*\n\s*\};?\s*$', '', fixed_body)
        
        if fixed_body != body:
            modified = True
            html = html[:body_start] + fixed_body + html[body_end:]
    
    if modified:
        with open(html_path, 'w') as f:
            f.write(html)
    
    all_js = ''
    for _, _, _, _, body in get_all_js(html):
        all_js += body.strip() + '\n'
    
    ok, err = verify_js(all_js)
    return ok


def main():
    issues_file = os.path.join(BASE, 'quality-reports', 'current-issues.json')
    with open(issues_file, 'r') as f:
        data = json.load(f)
    
    broken = list(data['broken_tools_remaining'])
    
    fixed = []
    still_broken = []
    
    for tool in broken:
        html_path = os.path.join(BASE, tool, 'index.html')
        if not os.path.exists(html_path):
            still_broken.append(tool)
            continue
        
        print(f"[{tool}]", end=' ', flush=True)
        
        # 验证
        all_js = ''
        with open(html_path, 'r') as f:
            h = f.read()
        for _, _, _, _, body in get_all_js(h):
            all_js += body.strip() + '\n'
        
        ok, err = verify_js(all_js)
        if ok:
            print("✓")
            fixed.append(tool)
            continue
        
        # 第1轮修复
        ok = fix_html(html_path)
        if ok:
            print("✓(v1)")
            fixed.append(tool)
            continue
        
        # 第2轮修复
        ok = fix_html_v2(html_path)
        if ok:
            print("✓(v2)")
            fixed.append(tool)
            continue
        
        # 最终验证
        with open(html_path, 'r') as f:
            h = f.read()
        all_js = ''
        for _, _, _, _, body in get_all_js(h):
            all_js += body.strip() + '\n'
        ok, err = verify_js(all_js)
        if ok:
            print("✓(post)")
            fixed.append(tool)
            continue
        
        print(f"✗ {err[:100]}")
        still_broken.append(tool)
    
    print(f"\nFixed: {len(fixed)}, Broken: {len(still_broken)}")
    
    # 更新
    data['broken_tools_remaining'] = still_broken
    data['summary']['gate0_js_syntax']['broken'] = len(still_broken)
    data['summary']['gate0_js_syntax']['ok'] = data['summary']['gate0_js_syntax'].get('total', 245) - len(still_broken)
    data['summary']['gate0_js_syntax']['fixed_this_run'] = data['summary']['gate0_js_syntax'].get('fixed_this_run', 0) + len(fixed)
    data['fixed_this_run'] = data.get('fixed_this_run', []) + fixed
    
    if still_broken:
        data['p0_blocking'] = True
        data['urgent']['p0_blocking'] = True
        data['urgent']['progress'] = f"{len(fixed)} fixed this run, {len(still_broken)} remaining"
    else:
        data['p0_blocking'] = False
        data['urgent']['p0_blocking'] = False
        data['urgent']['progress'] = "Complete!"
    
    with open(issues_file, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"p0_blocking: {data['p0_blocking']}")
    return still_broken

if __name__ == '__main__':
    import sys
    remaining = main()
    sys.exit(0 if not remaining else 1)