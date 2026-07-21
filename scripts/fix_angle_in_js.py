#!/usr/bin/env python3
"""修复JS中<符号导致script提前闭合的问题
把内联JS中的 < 替换为 \\x3C，防止HTML解析器误解析
"""
import subprocess, re, os

def extract_js_from_html(html_path):
    """直接从HTML文件读取，保留原始script标签"""
    with open(html_path) as f:
        content = f.read()
    return content

def check_tool(tool_dir):
    html_path = f'{tool_dir}/index.html'
    if not os.path.exists(html_path):
        return None
    
    with open(html_path) as f:
        content = f.read()
    
    # 提取JS（用正则，和之前一样）
    scripts = re.findall(r'<script>(.*?)</script>', content, re.DOTALL)
    js_parts = []
    for s in scripts:
        s = s.strip()
        if not s: continue
        if s.startswith('{') and ('@context' in s or '"@type"' in s): continue
        js_parts.append(s)
    if not js_parts:
        return None
    
    js = '\n'.join(js_parts)
    r = subprocess.run(['node', '-c', '-'], input=js, capture_output=True, text=True, timeout=5)
    return r.returncode == 0

def fix_angle_in_js(tool_dir):
    html_path = f'{tool_dir}/index.html'
    with open(html_path) as f:
        content = f.read()
    
    new_content = content
    
    # 对每个非JSON-LD的script块，替换JS中的 < 为 \x3C
    # 但不能替换HTML标签的 <（如 <div>, <script>等）
    # 策略：在script块内部，替换字符串字面量和模板字面量中的 <
    
    # 更简单的策略：用 \x3C 替换JS中所有非HTML标签的 <
    # 在script块内，< 后面跟字母或/ 的是HTML标签（不应该出现在JS中）
    # 但实际上这些就是问题所在！JS中的 <Proxy, <Directory 等被HTML解析器当成标签
    
    # 最安全的修复：把整个script块的内容中，所有 < 替换为 \x3C
    # 但这会破坏合法的HTML字符串比较（如 a < b）
    # 所以只替换 < 后面跟字母或 / 的情况（看起来像HTML标签的）
    
    def fix_script_block(match):
        script_content = match.group(1)
        if script_content.strip().startswith('{') and ('@context' in script_content or '"@type"' in script_content):
            return match.group(0)  # JSON-LD, skip
        
        # 替换 < 后跟字母或/ 的情况（看起来像HTML标签）
        # 但排除合法的JS比较运算符
        # 在字符串/模板字面量中的 <tag 应该替换
        # 在代码中的 a < b 不应该替换
        
        # 简单策略：替换所有 < 后跟大写字母的情况（HTML标签通常大写或小写）
        # 以及 </ 的情况
        fixed = re.sub(r'<(\/?[A-Za-z])', r'\\x3C\1', script_content)
        
        return '<script>' + fixed + '</script>'
    
    new_content = re.sub(r'<script>(.*?)</script>', fix_script_block, new_content, flags=re.DOTALL)
    
    if new_content != content:
        with open(html_path, 'w') as f:
            f.write(new_content)
        
        # Verify
        if check_tool(tool_dir):
            return 'fixed'
        else:
            # Revert
            with open(html_path, 'w') as f:
                f.write(content)
            return 'still_broken'
    
    return 'no_change'

if __name__ == '__main__':
    SKIP = {'_gen','__pycache__','en','libs','js','css','scripts','tools',
            '.git','data','about','blog','privacy-policy','terms-of-service','category',
            'calc','design','dev','fun','health','image','math','media','network',
            'office','pdf','security','seo','text','utility'}
    
    results = {'fixed': [], 'still_broken': [], 'no_change': []}
    
    for d in sorted(os.listdir('.')):
        if not os.path.isdir(d) or d in SKIP or d.startswith('.'): continue
        f = f'{d}/index.html'
        if not os.path.exists(f): continue
        
        result = fix_angle_in_js(d)
        if result == 'fixed':
            results['fixed'].append(d)
        elif result == 'still_broken':
            results['still_broken'].append(d)
        elif result == 'no_change':
            # Check if it's actually broken
            if not check_tool(d):
                results['still_broken'].append(d)
    
    print(f"Fixed: {len(results['fixed'])}")
    for t in results['fixed']:
        print(f"  ✅ {t}")
    print(f"\nStill broken: {len(results['still_broken'])}")
    for t in results['still_broken'][:30]:
        print(f"  ❌ {t}")
