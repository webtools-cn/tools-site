#!/usr/bin/env python3
"""分析 no_copy_btn 页面结构"""
import json, os, re

with open('quality/quality_loop_result.json') as f:
    data = json.load(f)

only_copy = [(k,v) for k,v in data['remaining_pages'].items() if 'no_copy_btn' in v and 'low_interact' not in v]

patterns = {}
for page_key, issues in only_copy[:50]:
    lang, item = page_key.split(':', 1)
    path = f'{item}/index.html' if lang == 'cn' else f'en/{item}/index.html'
    if not os.path.exists(path): continue
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        c = f.read()
    
    # Check for result/output ids
    result_ids = re.findall(r'getElementById\(["\']([^"\']*result[^"\']*)["\']\)', c, re.I)
    output_ids = re.findall(r'getElementById\(["\']([^"\']*output[^"\']*)["\']\)', c, re.I)
    display_ids = re.findall(r'getElementById\(["\']([^"\']*display[^"\']*)["\']\)', c, re.I)
    all_ids = result_ids + output_ids + display_ids
    
    has_copy_btn = 'copy' in c.lower() and ('copyBtn' in c or 'copy-btn' in c or 'copyButton' in c)
    has_copy_func = 'navigator.clipboard' in c or 'document.execCommand' in c
    
    if all_ids:
        patterns[item] = {'ids': all_ids, 'has_copy_btn': has_copy_btn, 'has_copy_func': has_copy_func}
    else:
        # Check for innerHTML patterns
        inner_ids = re.findall(r'getElementById\(["\']([^"\']+)["\']\).*innerHTML', c, re.I)
        if inner_ids:
            patterns[item] = {'ids': inner_ids[:3], 'has_copy_btn': has_copy_btn, 'has_copy_func': has_copy_func, 'source': 'innerHTML'}

for item, info in list(patterns.items())[:20]:
    print(f'{item}: ids={info["ids"]}, has_btn={info["has_copy_btn"]}, has_func={info["has_copy_func"]}')
print(f'\nTotal with detectable output: {len(patterns)}')