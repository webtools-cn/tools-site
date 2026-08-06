#!/usr/bin/env python3
"""
检查所有工具的calc函数：最终输出result.innerHTML前是否有display:block。
只报告有问题的（正常输出路径缺少display:block）。
"""
import re
import os
import glob

BASE = "/home/chison/tools-site"

# 找所有有calc函数的HTML文件
all_files = glob.glob(os.path.join(BASE, "*/index.html")) + glob.glob(os.path.join(BASE, "en/*/index.html"))

problems = []

for filepath in sorted(all_files):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # 找calc函数（更宽松的匹配）
    calc_match = re.search(r'function calc\(\)\{(.*?)(?:\nfunction |\n</script>)', html, re.DOTALL)
    if not calc_match:
        continue
    
    calc_body = calc_match.group(1)
    
    # 检查是否有.result CSS display:none
    has_css_none = bool(re.search(r'\.result\s*\{[^}]*display:\s*none', html))
    if not has_css_none:
        continue  # 没有display:none的CSS，不需要检查
    
    # 找所有 result.innerHTML 或 result.textContent 的位置
    output_matches = list(re.finditer(r'result\.innerHTML\s*=', calc_body))
    if not output_matches:
        output_matches = list(re.finditer(r'result\.textContent\s*=', calc_body))
    if not output_matches:
        # 可能用document.getElementById('result').innerHTML
        output_matches = list(re.finditer(r"document\.getElementById\(['\"]result['\"]\)\.innerHTML\s*=", calc_body))
    
    if not output_matches:
        continue  # 没有直接设置result，可能用show()
    
    # 检查最后一次输出前是否有display:block
    last_output = output_matches[-1]
    before_last = calc_body[:last_output.start()]
    
    # 检查最近200字符内是否有display设置
    recent = before_last[-200:]
    has_display_block = ("display='block'" in recent or 
                         'display="block"' in recent or 
                         "display = 'block'" in recent or
                         "display =\"block\"" in recent or
                         ".style.display='block'" in recent or
                         ".style.display = 'block'" in recent or
                         ".style.display=\"block\"" in recent)
    
    if not has_display_block:
        rel_path = os.path.relpath(filepath, BASE)
        problems.append(rel_path)

if problems:
    print(f"发现 {len(problems)} 个问题文件:")
    for p in problems:
        print(f"  ❌ {p}")
else:
    print("全部OK")
