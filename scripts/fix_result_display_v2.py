#!/usr/bin/env python3
"""
精确修复calc()函数中result.style.display='block'缺失的问题。
策略：在calc函数中最后一次设置result.innerHTML之前确保有display:block。
如果display:block已经在错误处理分支里（第一次出现result.innerHTML），
还需要在最终输出（最后一次result.innerHTML）前也加上。
"""
import re
import os

TOOLS = [
    "capacitor-energy-calculator",
    "growth-rate-calculator",
    "pizza-size-comparison",
    "plant-spacing-calculator",
    "price-per-unit",
    "resistor-color-code",
    "target-heart-rate",
]

BASE = "/home/chison/tools-site"
fixed = 0

for tool in TOOLS:
    for lang_prefix in ["", "en/"]:
        filepath = os.path.join(BASE, lang_prefix, tool, "index.html")
        if not os.path.exists(filepath):
            continue
        
        with open(filepath, 'r', encoding='utf-8') as f:
            html = f.read()
        
        # 找所有 result.innerHTML 的位置
        # 找calc函数
        calc_match = re.search(r'(function calc\(\)\{)(.*?)(\n\})', html, re.DOTALL)
        if not calc_match:
            print(f"SKIP (no calc): {filepath}")
            continue
        
        calc_body = calc_match.group(2)
        
        # 找所有 result.innerHTML 出现的位置
        innerhtml_positions = [m.start() for m in re.finditer(r'result\.innerHTML', calc_body)]
        
        if not innerhtml_positions:
            # 可能用了别的写法
            innerhtml_positions = [m.start() for m in re.finditer(r"result\.textContent", calc_body)]
        
        if not innerhtml_positions:
            print(f"SKIP (no result set): {filepath}")
            continue
        
        # 检查最后一次result.innerHTML前是否已有display:block
        last_pos = innerhtml_positions[-1]
        before_last = calc_body[:last_pos]
        
        # 如果最后一次设置前100字符内没有display:block，就加
        if "display='block'" not in before_last[-200:] and 'display="block"' not in before_last[-200:] and 'display =\'block\'' not in before_last[-200:]:
            # 在最后一次result.innerHTML前插入
            new_calc_body = calc_body[:last_pos] + "result.style.display='block';" + calc_body[last_pos:]
            new_calc = calc_match.group(1) + new_calc_body + calc_match.group(3)
            new_html = html.replace(calc_match.group(0), new_calc, 1)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_html)
            print(f"FIXED: {filepath}")
            fixed += 1
        else:
            print(f"OK (already has display before last innerHTML): {filepath}")

print(f"\n总计修复: {fixed}")
