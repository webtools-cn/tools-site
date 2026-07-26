#!/usr/bin/env python3
"""精确修复EN页面的中文碎片 v4"""
import os, re

SITE = '/home/chison/tools-site'

# 已知的EN页面中文→英文映射
FIXES = {
    'en/expense-splitter/index.html': [
        ('数据绝不Upload服务器', 'All data stays on your device'),
    ],
    'en/loan-calc/index.html': [
        ('期限，自动Calculate每Monthly额和总Interest', 'term, auto-calculates monthly payment and total interest'),
    ],
    'en/military-time-converter/index.html': [
        ('零依赖·可离线使用', 'Zero dependencies · Works offline'),
    ],
    'en/grams-to-cups/index.html': [],
    'en/grams-to-ounces/index.html': [],
    'en/indent-formatter/index.html': [],
    'en/kelvin-to-celsius/index.html': [],
    'en/loading-spinner/index.html': [],
    'en/money-counter/index.html': [],
    'en/mortgage-calc/index.html': [],
    'en/one-rep-max/index.html': [],
    'en/percentage-change/index.html': [],
    'en/roman-numerals/index.html': [],
    'en/spell-checker/index.html': [],
    'en/square-meter-to-square-foot/index.html': [],
    'en/typewriter-effect/index.html': [],
    'en/unicode-decode/index.html': [],
    'en/virtual-piano-keyboard/index.html': [],
}

CN_RE = re.compile(r'[\u4e00-\u9fff]')

fixed_count = 0
skipped_count = 0

for rel_path, manual_fixes in FIXES.items():
    path = os.path.join(SITE, rel_path)
    if not os.path.exists(path):
        print(f"NOT FOUND: {rel_path}")
        skipped_count += 1
        continue

    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        original = f.read()
    content = original

    # 应用手动修复
    for cn_text, en_text in manual_fixes:
        if cn_text in content:
            content = content.replace(cn_text, en_text)

    # 扫描剩余的中文
    clean = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL)
    clean = re.sub(r'<style[^>]*>.*?</style>', '', clean, flags=re.DOTALL)
    text_only = re.sub(r'<[^>]+>', ' ', clean)

    cn_matches = list(CN_RE.finditer(text_only))
    remaining_cn = []
    for m in cn_matches:
        start = max(0, m.start()-20)
        end = min(len(text_only), m.end()+20)
        remaining_cn.append(text_only[start:end].strip())

    if remaining_cn:
        # 还有残留中文
        for ctx in remaining_cn[:5]:
            print(f"STILL_CN {rel_path}: ...{ctx}...")
        skipped_count += 1
    elif content != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"FIXED {rel_path}")
        fixed_count += 1
    else:
        # 可能是误报，检查质量检测的阈值
        cn_count = len(cn_matches)
        print(f"SKIP {rel_path}: {cn_count} CN chars in visible text (may be false positive)")
        skipped_count += 1

print(f"\n=== Summary ===")
print(f"Fixed: {fixed_count}, Skipped: {skipped_count}")