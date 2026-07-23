#!/usr/bin/env python3
"""Scan all 73 high-priority tools for missing FAQ (both CN and EN)."""
import json
import os
import re

with open('quality/faq-priority-list.json') as f:
    data = json.load(f)

tools = data['high_priority']['tools']
site_root = '/home/chison/tools-site'

missing_cn = []
missing_en = []
has_cn = []
has_en = []

for tool in tools:
    cn_path = os.path.join(site_root, tool, 'index.html')
    en_path = os.path.join(site_root, 'en', tool, 'index.html')
    
    # Check CN
    if os.path.exists(cn_path):
        with open(cn_path, 'r', encoding='utf-8') as f:
            content = f.read()
        has_faq = 'faq-item' in content.lower() or 'FAQPage' in content
        if has_faq:
            has_cn.append(tool)
        else:
            missing_cn.append(tool)
    else:
        missing_cn.append(f"{tool} [CN FILE MISSING]")
    
    # Check EN
    if os.path.exists(en_path):
        with open(en_path, 'r', encoding='utf-8') as f:
            content = f.read()
        has_faq = 'faq-item' in content.lower() or 'FAQPage' in content
        if has_faq:
            has_en.append(tool)
        else:
            missing_en.append(tool)
    else:
        missing_en.append(f"{tool} [EN FILE MISSING]")

print(f"Total tools in list: {len(tools)}")
print(f"\nCN: {len(has_cn)} have FAQ, {len(missing_cn)} missing FAQ")
print(f"EN: {len(has_en)} have FAQ, {len(missing_en)} missing FAQ")

if missing_cn:
    print(f"\n=== CN missing FAQ ({len(missing_cn)}) ===")
    for t in missing_cn:
        print(f"  {t}")

if missing_en:
    print(f"\n=== EN missing FAQ ({len(missing_en)}) ===")
    for t in missing_en:
        print(f"  {t}")

# Also check medium priority
medium_tools = data.get('medium_priority', {}).get('tools', [])
med_missing_cn = []
med_missing_en = []

for tool in medium_tools:
    cn_path = os.path.join(site_root, tool, 'index.html')
    en_path = os.path.join(site_root, 'en', tool, 'index.html')
    
    if os.path.exists(cn_path):
        with open(cn_path, 'r', encoding='utf-8') as f:
            content = f.read()
        if 'faq-item' not in content.lower() and 'FAQPage' not in content:
            med_missing_cn.append(tool)
    else:
        med_missing_cn.append(f"{tool} [MISSING]")
    
    if os.path.exists(en_path):
        with open(en_path, 'r', encoding='utf-8') as f:
            content = f.read()
        if 'faq-item' not in content.lower() and 'FAQPage' not in content:
            med_missing_en.append(tool)
    else:
        med_missing_en.append(f"{tool} [MISSING]")

print(f"\n=== Medium Priority ===")
print(f"CN: {len(med_missing_cn)} missing FAQ out of {len(medium_tools)}")
print(f"EN: {len(med_missing_en)} missing FAQ out of {len(medium_tools)}")

if med_missing_cn:
    print(f"\n--- Medium CN missing ({len(med_missing_cn)}) ---")
    for t in med_missing_cn:
        print(f"  {t}")
