#!/usr/bin/env python3
"""Fix remaining Chinese in 5 EN pages - lang-switch, HowTo schema, leftovers"""
import re, os

SITE = '/home/chison/tools-site'

files = [
    'en/customer-lifetime-value/index.html',
    'en/equity-dilution-calc/index.html',
    'en/federal-tax-calc/index.html',
    'en/freelance-tax-calc/index.html',
    'en/revenue-projection/index.html',
]

for fname in files:
    fpath = os.path.join(SITE, fname)
    with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Fix lang-switch: "中文" -> "中文" (keep link text as is since it's a lang indicator, but make sure it's valid)
    # Actually in EN pages, lang-switch links to CN: text should be "中文"
    # The problem is the HowTo schema with Chinese name/description
    
    # Fix HowTo schema Chinese
    content = content.replace('"name":"如何使用 ', '"name":"How to Use ')
    content = content.replace('","description":"使用步骤指南"', '","description":"Step-by-step usage guide"')
    
    # Fix remaining Chinese in customer-lifetime-value
    content = content.replace('<div class="sub">每位客户总利润</div>', '<div class="sub">Total profit per customer</div>')
    
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    cn = re.findall(r'[\u4e00-\u9fff]+', content)
    print(f"  {fname}: {len(cn)} Chinese chars: {cn[:5]}")

print("\nDone!")