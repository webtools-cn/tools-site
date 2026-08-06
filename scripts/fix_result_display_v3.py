#!/usr/bin/env python3
"""
精确修复：在calc函数中最后一次设置result.innerHTML前插入result.style.display='block'。
处理多种写法：result.innerHTML / document.getElementById('result').innerHTML
"""
import re
import os

BASE = "/home/chison/tools-site"

PROBLEM_FILES = [
    "calorie-deficit-calculator/index.html",
    "commission-calculator/index.html",
    "discount-price-calculator/index.html",
    "loan-payment/index.html",
    "profit-calculator/index.html",
    "recipe-converter/index.html",
    "speed-distance-time-calculator/index.html",
    "unit-price-calculator/index.html",
    "water-intake-calculator/index.html",
]

fixed = 0
for rel_path in PROBLEM_FILES:
    for lang in ["", "en/"]:
        filepath = os.path.join(BASE, lang + rel_path)
        if not os.path.exists(filepath):
            continue
        
        with open(filepath, 'r', encoding='utf-8') as f:
            html = f.read()
        
        # 找calc函数
        calc_match = re.search(r'(function calc\(\)\{)(.*?)(?:\nfunction |\n</script>)', html, re.DOTALL)
        if not calc_match:
            continue
        
        calc_body = calc_match.group(2)
        
        # 找最后一次 result.innerHTML = 或 document.getElementById('result').innerHTML =
        patterns = [
            r'result\.innerHTML\s*=',
            r"document\.getElementById\(['\"]result['\"]\)\.innerHTML\s*=",
        ]
        
        last_pos = -1
        last_match_text = ""
        for pat in patterns:
            for m in re.finditer(pat, calc_body):
                if m.start() > last_pos:
                    last_pos = m.start()
                    last_match_text = m.group(0)
        
        if last_pos == -1:
            continue
        
        # 检查前200字符是否已有display:block
        before = calc_body[:last_pos][-200:]
        if any(x in before for x in ["display='block'", 'display="block"', ".style.display='block'", '.style.display = \'block\'']):
            continue  # 已修复
        
        # 在最后一次输出前插入
        insert_text = "result.style.display='block';"
        
        # 如果用的是 document.getElementById('result').innerHTML，需要用完整写法
        if 'document.getElementById' in last_match_text:
            insert_text = "document.getElementById('result').style.display='block';"
        
        new_calc_body = calc_body[:last_pos] + insert_text + calc_body[last_pos:]
        new_calc = calc_match.group(1) + new_calc_body
        
        # 替换
        old_calc = calc_match.group(0)
        new_html = html.replace(old_calc, new_calc, 1)
        
        if new_html != html:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_html)
            print(f"FIXED: {lang + rel_path}")
            fixed += 1
        else:
            print(f"SKIP (no change): {lang + rel_path}")

print(f"\n总计修复: {fixed}")
