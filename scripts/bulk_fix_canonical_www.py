#!/usr/bin/env python3
"""批量修复 canonical_www: 去掉canonical URL中的www"""
import os, json, re

SITE = '/home/chison/tools-site'

with open(os.path.join(SITE, 'quality', 'quality_loop_result.json')) as f:
    data = json.load(f)

remaining = data['remaining_pages']

www_pages = []
for k, v in remaining.items():
    if 'canonical_www' in v:
        lang, item = k.split(':')
        www_pages.append((lang, item))

print(f"处理 {len(www_pages)} 个canonical_www页面...")

fixed = 0
for lang, item in www_pages:
    if lang == 'cn':
        path = os.path.join(SITE, item, 'index.html')
    else:
        path = os.path.join(SITE, 'en', item, 'index.html')
    
    if not os.path.isfile(path):
        continue
    
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    new_content = content.replace(
        'https://www.free-toolbase.com/',
        'https://free-toolbase.com/'
    )
    
    if new_content != content:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        fixed += 1

print(f"修复: {fixed} 个")