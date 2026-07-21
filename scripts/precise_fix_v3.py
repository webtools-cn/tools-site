#!/usr/bin/env python3
"""精确修复broken工具的JS语法错误 - v3: 逐个分析错误原因并修复"""
import subprocess, re, os, json, sys

BROKEN_TOOLS = json.load(open('/home/chison/tools-site/quality-reports/current-issues.json'))['broken_tools_remaining']

def extract_js_blocks(html):
    """提取所有<script>块（跳过已知框架标签如gtag, adsbygoogle, ld+json）"""
    blocks = []
    for m in re.finditer(r'<script(?![^>]*src=)([^>]*)>(.*?)</script>', html, re.DOTALL):
        attrs = m.group(1)
        code = m.group(2)
        # 跳过ld+json和gtag/analytics
        if 'ld+json' in attrs.lower() or 'application/ld+json' in attrs.lower():
            continue
        blocks.append(code)
    return blocks

def check_js(js_code):
    """用node -c检查JS语法，返回(ok, error_msg)"""
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
        f.write(js_code)
        tmpath = f.name
    try:
        r = subprocess.run(['node', '-c', tmpath], capture_output=True, text=True, timeout=10)
        os.unlink(tmpath)
        return r.returncode == 0, r.stderr.strip()
    except Exception as e:
        os.unlink(tmpath)
        return False, str(e)

def find_specific_error(js_code):
    """使用acorn精确定位JS语法错误"""
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
        f.write(js_code)
        tmpath = f.name
    try:
        r = subprocess.run(
            ['node', '-e', f'const acorn=require("acorn");acorn.parse(require("fs").readFileSync("{tmpath}","utf8"),{{ecmaVersion:2022}});'],
            capture_output=True, text=True, timeout=10
        )
        os.unlink(tmpath)
        if r.returncode == 0:
            return None
        # 解析错误信息
        return r.stderr.strip()
    except Exception as e:
        try: os.unlink(tmpath)
        except: pass
        return str(e)

def fix_common_issues(html):
    """修复常见问题"""
    # 1. 修复重复的header（如 <h1>XXX</h1> XXX</h1>）
    html = re.sub(r'(<h1>[^<]+)</h1>\s*\1', r'\1', html)
    html = re.sub(r'</h1>\s*[A-Za-z\u4e00-\u9fff].*?</h1>', '</h1>', html)  # 移除多余的header文本
    
    # 2. 修复 hero/section 中出现两次header的情况
    html = re.sub(r'(<div class="hero">).*?(<div class="header">)', r'\1</div>\n<div class="main-grid">\n<div>\2', html, flags=re.DOTALL)
    
    # 3. 修复空OG title
    html = re.sub(r'<meta property="og:title" content="">', r'<meta property="og:title" content="Free Online Tool">', html)
    
    return html

def fix_tool(tool_name):
    """修复单个工具"""
    path = f'/home/chison/tools-site/{tool_name}/index.html'
    if not os.path.exists(path):
        print(f"  ❌ File not found: {path}")
        return False
    
    with open(path, 'r') as f:
        html = f.read()
    
    # 提取JS块
    js_blocks = extract_js_blocks(html)
    
    broken_blocks = []
    for i, block in enumerate(js_blocks):
        ok, err = check_js(block)
        if not ok:
            broken_blocks.append((i, block[:200], err))
    
    if not broken_blocks:
        print(f"  ✅ {tool_name}: All JS blocks pass syntax check")
        return True
    
    print(f"  🔧 {tool_name}: {len(broken_blocks)} broken JS blocks")
    
    # 对于每个broken block，找到具体错误
    for idx, snippet, node_err in broken_blocks:
        # 找精确错误
        acorn_err = find_specific_error(js_blocks[idx])
        if acorn_err:
            print(f"    Block {idx}: {acorn_err[:300]}")
        else:
            print(f"    Block {idx}: {node_err[:200]}")
    
    # 尝试通用修复
    html_fixed = fix_common_issues(html)
    
    # 再次检查
    js_blocks2 = extract_js_blocks(html_fixed)
    all_ok = True
    for block in js_blocks2:
        ok, err = check_js(block)
        if not ok:
            all_ok = False
    
    if all_ok:
        # 备份原文件
        bak = path + '.bak'
        with open(bak, 'w') as f:
            f.write(html)
        with open(path, 'w') as f:
            f.write(html_fixed)
        print(f"  ✅ {tool_name}: Fixed! (backup: {tool_name}/index.html.bak)")
        return True
    
    print(f"  ❌ {tool_name}: Still broken after generic fix")
    return False

# 只处理前5个
results = {'fixed': [], 'still_broken': [], 'already_ok': []}
for tool in BROKEN_TOOLS[:5]:
    print(f"\n--- {tool} ---")
    result = fix_tool(tool)
    if result:
        results['fixed'].append(tool)
    else:
        results['still_broken'].append(tool)

print(f"\n=== Summary ===")
print(f"Fixed: {results['fixed']}")
print(f"Still broken: {results['still_broken']}")
