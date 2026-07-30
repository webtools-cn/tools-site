#!/usr/bin/env python3
"""
修复"函数未定义"错误 V2：直接从.bak文件中复制核心JS脚本块。
策略：当前文件的<script>区域被截断了，从.bak提取完整的核心JS替换。
"""
import json
import os
import re
import sys

BASE = '/home/chison/tools-site'

def extract_core_js_from_bak(bak_path):
    """从.bak文件中提取核心工具JS脚本块"""
    with open(bak_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 找到所有<script>块（非schema、非GTAG）
    script_blocks = []
    for m in re.finditer(r'<script>(.*?)</script>', content, re.DOTALL):
        js = m.group(1).strip()
        if len(js) > 500 and 'application/ld+json' not in js and 'googletagmanager' not in js.lower() and 'adsbygoogle' not in js.lower():
            script_blocks.append(js)
    
    if not script_blocks:
        return None
    
    # 返回最长的脚本块（核心工具JS）
    return max(script_blocks, key=len)


def extract_utility_js_from_bak(bak_path):
    """从.bak提取辅助JS（showToast, copyText等）"""
    with open(bak_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    util_blocks = []
    for m in re.finditer(r'<script>(.*?)</script>', content, re.DOTALL):
        js = m.group(1).strip()
        if 100 < len(js) <= 500 and 'application/ld+json' not in js:
            util_blocks.append(js)
    
    return util_blocks


def fix_file_v2(tool_name):
    """修复文件：从.bak提取核心JS，替换当前文件的简化版script"""
    current = os.path.join(BASE, tool_name, 'index.html')
    bak = os.path.join(BASE, tool_name, 'index.html.bak')
    
    if not os.path.exists(bak):
        return False, "no bak"
    
    core_js = extract_core_js_from_bak(bak)
    if not core_js:
        return False, "no core js in bak"
    
    with open(current, 'r', encoding='utf-8') as f:
        cur_content = f.read()
    
    # 找到当前文件中"瘦"的核心script块（IIFE related-tools相关，很短）
    # 在最后一个</script>之前替换
    
    # 查找当前文件的核心JS script块
    cur_scripts = list(re.finditer(r'<script>(.*?)</script>', cur_content, re.DOTALL))
    
    if not cur_scripts:
        return False, "no script tags in current"
    
    # 找最长的script块（应该是核心工具JS）
    longest_idx = -1
    longest_len = 0
    for i, m in enumerate(cur_scripts):
        js = m.group(1).strip()
        if len(js) > longest_len and 'application/ld+json' not in js and 'googletagmanager' not in js.lower():
            longest_len = len(js)
            longest_idx = i
    
    if longest_idx == -1 or longest_len > 2000:
        # 当前文件已经有完整JS了，不需要修复
        return False, "current js looks complete"
    
    # 替换这个script块
    old_script = cur_scripts[longest_idx]
    new_script_block = f'<script>\n{core_js}\n</script>'
    new_content = cur_content[:old_script.start()] + new_script_block + cur_content[old_script.end():]
    
    with open(current, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return True, f"replaced core JS ({longest_len} → {len(core_js)} chars)"


def main():
    with open(os.path.join(BASE, 'quality-reports/puppeteer-L0.json')) as f:
        data = json.load(f)
    
    nd_tools = [f['tool'] for f in data['failures'] if 'not defined' in f['reason']]
    
    print(f"Total 'not defined' tools: {len(nd_tools)}")
    
    fixed = []
    failed = []
    skipped = []
    
    batch = nd_tools[:20]
    for tool in batch:
        success, msg = fix_file_v2(tool)
        if success:
            fixed.append((tool, msg))
            print(f"  ✅ {tool}: {msg}")
        elif 'no bak' in msg or 'complete' in msg:
            skipped.append((tool, msg))
            print(f"  ⏭ {tool}: {msg}")
        else:
            failed.append((tool, msg))
            print(f"  ❌ {tool}: {msg}")
    
    print(f"\n=== Summary ===")
    print(f"Fixed: {len(fixed)}")
    print(f"Skipped: {len(skipped)}")
    print(f"Failed: {len(failed)}")


if __name__ == '__main__':
    main()