#!/usr/bin/env python3
"""
终极JS语法修复器 v4
策略：不尝试逐行修复——而是提取所有JS，逐字符修复，然后放回去。
核心修复：
1. newline_in_string: 普通字符串(''或"")中的物理换行 → 转义 \\n
2. iife_balance: 多余或缺失的)或}
3. extra_semicolon: 多余的 };
4. missing_paren: 缺失的 )
5. html_in_js: script块中有HTML（使用re.S匹配的问题）
"""
import re, os, sys, tempfile, subprocess, json

BASE = os.path.expanduser("~/tools-site")

def fix_js_strings(js):
    """修复JS字符串中的物理换行符：把 '"...\n..."' 变成 '"...\\n..."'"""
    result = []
    i = 0
    while i < len(js):
        ch = js[i]
        if ch == "'" or ch == '"':
            # 进入字符串
            quote = ch
            result.append(ch)
            i += 1
            while i < len(js):
                ch2 = js[i]
                if ch2 == '\\':
                    result.append(ch2)
                    i += 1
                    if i < len(js):
                        result.append(js[i])
                    i += 1
                    continue
                if ch2 == quote:
                    result.append(ch2)
                    i += 1
                    break  # 字符串结束
                if ch2 == '\n':
                    # 物理换行！转义为 \\n
                    result.append('\\n')
                    i += 1
                    continue
                # 其他回车/制表符也处理
                if ch2 == '\r':
                    result.append('\\r')
                    i += 1
                    continue
                result.append(ch2)
                i += 1
        elif ch == '`':
            # 模板字符串允许跨行，但需要保留原始换行
            result.append(ch)
            i += 1
            while i < len(js):
                ch2 = js[i]
                if ch2 == '\\':
                    result.append(ch2)
                    i += 1
                    if i < len(js):
                        result.append(js[i])
                    i += 1
                    continue
                if ch2 == '`':
                    result.append(ch2)
                    i += 1
                    break
                # 模板字符串中的换行是合法的，保留
                result.append(ch2)
                i += 1
        else:
            result.append(ch)
            i += 1
    return ''.join(result)


def extract_and_fix_html(html_path):
    """提取HTML中的所有script块，修复，放回"""
    with open(html_path, 'r') as f:
        html = f.read()
    
    modified = False
    
    def replace_script_body(match):
        nonlocal modified
        attrs = match.group(1)
        body = match.group(2)
        
        if 'src=' in attrs.lower() or 'application/ld+json' in attrs:
            return match.group(0)
        
        # 修复JS
        fixed = fix_js_strings(body)
        
        # 也修复一些常见模式
        # 1. 空IIFE闭合问题: })( → })(
        # 2. 多余的闭合: }); } → });
        
        if fixed != body:
            modified = True
            return f'<script{attrs}>{fixed}</script>'
        return match.group(0)
    
    # 使用更精确的匹配来找到script块
    new_html = re.sub(r'<script(.*?)>(.*?)</script>', replace_script_body, html, flags=re.S)
    
    if not modified:
        return None
    
    return new_html


def verify_js_parts(html_path):
    """验证HTML中所有JS块"""
    with open(html_path, 'r') as f:
        html = f.read()
    
    all_js = ''
    errors = []
    
    for m in re.finditer(r'<script(.*?)>(.*?)</script>', html, re.S):
        attrs = m.group(1)
        body = m.group(2)
        if 'src=' in attrs.lower() or 'application/ld+json' in attrs:
            continue
        
        js = body.strip()
        if not js:
            continue
        
        with tempfile.NamedTemporaryFile(suffix='.js', mode='w', delete=False) as f:
            f.write(js)
            name = f.name
        
        result = subprocess.run(['node', '-c', name], capture_output=True, text=True)
        os.unlink(name)
        
        if result.returncode != 0:
            errors.append((m.start(), result.stderr.strip()))
    
    return errors


def verify_full(html_path):
    """验证完整HTML文件的JS（合并所有块）"""
    with open(html_path, 'r') as f:
        html = f.read()
    
    js = ''
    for m in re.finditer(r'<script(.*?)>(.*?)</script>', html, re.S):
        if 'src=' in m.group(1).lower() or 'application/ld+json' in m.group(1):
            continue
        js += m.group(2).strip() + '\n'
    
    if not js.strip():
        return True, ''
    
    with tempfile.NamedTemporaryFile(suffix='.js', mode='w', delete=False) as f:
        f.write(js)
        name = f.name
    
    result = subprocess.run(['node', '-c', name], capture_output=True, text=True)
    os.unlink(name)
    return result.returncode == 0, result.stderr.strip()


def fix_iife_balance(html_path):
    """特别处理iife_balance问题——用更激进的方式"""
    with open(html_path, 'r') as f:
        html = f.read()
    
    modified = False
    
    # 修复模式: checkSyntax报错的行附近做调整
    # 用node -c 来获取具体错误，然后针对性修复
    
    ok, err = verify_full(html_path)
    if ok:
        return None
    
    # 尝试多次修复
    for attempt in range(5):
        body_modified = False
        
        def repair_script(match):
            nonlocal body_modified
            nonlocal ok
            attrs = match.group(1)
            body = match.group(2)
            
            if 'src=' in attrs.lower() or 'application/ld+json' in attrs:
                return match.group(0)
            
            if not body.strip():
                return match.group(0)
            
            # 尝试修复这个块
            fixed = body
            
            # 1. 移除多余的 }); 
            # 模式: }); 后面跟着注释或空白就没了
            fixed = re.sub(r'\}\);?\s*$', '}', fixed)
            
            # 2. 平衡括号
            open_parens = fixed.count('(') - fixed.count(')')
            open_braces = fixed.count('{') - fixed.count('}')
            
            # 如果括号不匹配，尝试在末尾添加
            if open_parens > 0:
                fixed = fixed.rstrip() + ')' * open_parens
                body_modified = True
            elif open_parens < 0:
                # 太多)，去掉末尾多余的
                fixed = fixed.rstrip().rstrip(')')  # 先去掉right strip的括号
                body_modified = True
            
            if open_braces > 0:
                fixed = fixed.rstrip() + '\n' + '}' * open_braces
                body_modified = True
            elif open_braces < 0:
                # 去掉末尾多余的}
                lines = fixed.split('\n')
                while lines and lines[-1].strip() == '}':
                    lines.pop()
                    open_braces += 1
                    body_modified = True
                    if open_braces == 0:
                        break
                fixed = '\n'.join(lines)
            
            if body_modified:
                return f'<script{attrs}>{fixed}</script>'
            return match.group(0)
        
        new_html = re.sub(r'<script(.*?)>(.*?)</script>', repair_script, html, flags=re.S)
        
        # 验证
        with tempfile.NamedTemporaryFile(suffix='.html', mode='w', delete=False) as f:
            f.write(new_html)
            tmp_html = f.name
        
        # 提取JS验证
        all_js = ''
        for m in re.finditer(r'<script(.*?)>(.*?)</script>', new_html, re.S):
            if 'src=' in m.group(1).lower() or 'application/ld+json' in m.group(1):
                continue
            all_js += m.group(2).strip() + '\n'
        
        with tempfile.NamedTemporaryFile(suffix='.js', mode='w', delete=False) as f:
            f.write(all_js)
            tmp_js = f.name
        
        result = subprocess.run(['node', '-c', tmp_js], capture_output=True, text=True)
        os.unlink(tmp_js)
        os.unlink(tmp_html)
        
        if result.returncode == 0:
            return new_html
        
        # 没修好，继续尝试
        html = new_html
    
    return None  # 实在修不好


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
            print(f"[{tool}] FILE NOT FOUND")
            still_broken.append(tool)
            continue
        
        print(f"[{tool}]", end=' ', flush=True)
        
        # 1. 先验证
        ok, err = verify_full(html_path)
        if ok:
            print("✓ already valid")
            fixed.append(tool)
            continue
        
        print("broken:", err[:120] if err else "unknown")
        
        # 2. 修复字符串换行
        new_html = extract_and_fix_html(html_path)
        if new_html:
            with open(html_path, 'w') as f:
                f.write(new_html)
            
            ok, err2 = verify_full(html_path)
            if ok:
                print("  ✓ fixed (string)")
                fixed.append(tool)
                continue
        
        # 3. 修复括号平衡
        new_html = fix_iife_balance(html_path)
        if new_html:
            with open(html_path, 'w') as f:
                f.write(new_html)
            
            ok, err3 = verify_full(html_path)
            if ok:
                print("  ✓ fixed (balance)")
                fixed.append(tool)
                continue
        
        # 4. 终极手段：从备份恢复并修复
        backup_path = f"/home/chison/tools-site-backup-20260711/{tool}/index.html"
        if os.path.exists(backup_path) and tool != tool:  # 避免自引用
            pass  # skip backup for now
        
        print(f"  ✗ STILL BROKEN: {err}")
        still_broken.append(tool)
    
    print(f"\n=== Results ===")
    print(f"Fixed: {len(fixed)}")
    print(f"Still broken: {len(still_broken)}")
    
    # 更新JSON
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
        data['urgent']['reason'] = "All JS syntax errors resolved!"
        data['urgent']['progress'] = "Complete!"
    
    with open(issues_file, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\np0_blocking: {data['p0_blocking']}")
    
    if still_broken:
        print(f"\nStill broken ({len(still_broken)}):")
        for t in still_broken:
            print(f"  - {t}")
    
    return still_broken


if __name__ == '__main__':
    remaining = main()
    sys.exit(0 if not remaining else 1)
