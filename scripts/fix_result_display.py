#!/usr/bin/env python3
"""修复calc()函数不设置result.style.display='block'的P0 bug"""
import re
import os

TOOLS = [
    "capacitor-energy-calculator",
    "dress-size-converter",
    "grams-to-pounds",
    "growth-rate-calculator",
    "impedance-calculator",
    "liters-to-gallons",
    "mortgage-affordability",
    "mph-to-kph",
    "parking-fee-calculator",
    "pizza-size-comparison",
    "plant-spacing-calculator",
    "price-per-unit",
    "resistor-color-code",
    "rug-size-calculator",
    "target-heart-rate",
    "watts-to-horsepower",
]

BASE = "/home/chison/tools-site"
fixed = 0
skipped = 0

for tool in TOOLS:
    for lang_prefix in ["", "en/"]:
        filepath = os.path.join(BASE, lang_prefix, tool, "index.html")
        if not os.path.exists(filepath):
            print(f"SKIP (not found): {filepath}")
            skipped += 1
            continue
        
        with open(filepath, 'r', encoding='utf-8') as f:
            html = f.read()
        
        # 检查是否已经有display设置在calc里
        m = re.search(r'function calc\(\)\{(.*?)\n\}', html, re.DOTALL)
        if not m:
            print(f"SKIP (no calc): {filepath}")
            skipped += 1
            continue
        
        calc_body = m.group(1)
        if 'display' in calc_body and 'block' in calc_body:
            print(f"SKIP (already fixed): {filepath}")
            skipped += 1
            continue
        
        # 在result.innerHTML第一次出现前插入display:block
        # 找到calc函数中第一次设置result的地方
        # 策略：在result.innerHTML = 或 result.textContent = 之前插入
        # 更安全的策略：在calc函数体的第一行（var result=...之后）插入
        
        # 找到calc函数的完整匹配
        calc_match = re.search(r'(function calc\(\)\{\n)(.*?)(\n\})', html, re.DOTALL)
        if not calc_match:
            # 尝试单行格式
            calc_match = re.search(r'(function calc\(\)\{)(.*?)(\})', html)
            if not calc_match:
                print(f"SKIP (can't parse calc): {filepath}")
                skipped += 1
                continue
        
        # 在calc函数体开头插入 result.style.display='block';
        # 找到 result 变量定义的位置
        old_calc = calc_match.group(0)
        
        # 在第一个 result.innerHTML 之前插入
        if 'result.innerHTML' in old_calc:
            new_calc = old_calc.replace(
                'result.innerHTML',
                "result.style.display='block';result.innerHTML",
                1  # 只替换第一次
            )
        elif 'result.textContent' in old_calc:
            new_calc = old_calc.replace(
                'result.textContent',
                "result.style.display='block';result.textContent",
                1
            )
        else:
            print(f"SKIP (no result set in calc): {filepath}")
            skipped += 1
            continue
        
        if new_calc == old_calc:
            print(f"SKIP (no change): {filepath}")
            skipped += 1
            continue
        
        new_html = html.replace(old_calc, new_calc, 1)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_html)
        
        print(f"FIXED: {filepath}")
        fixed += 1

print(f"\n总计: 修复 {fixed}, 跳过 {skipped}")
