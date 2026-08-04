#!/usr/bin/env python3
import os, re

files_to_check = [
    'html-dialog-generator/index.html',
    'html-sanitizer/index.html',
    'kanban-board/index.html'
]
for p in files_to_check:
    with open(p) as fh:
        ct = fh.read()
    onclick_funcs = set(re.findall(r'onclick="(\w+)\(', ct))
    all_scripts = ' '.join(re.findall(r'<script[^>]*>(.*?)</script>', ct, re.DOTALL))
    
    missing = []
    for func in onclick_funcs:
        if f'function {func}(' in all_scripts or f'{func} =' in all_scripts or f'{func}=' in all_scripts:
            continue
        # Check if onclick is only inside generated strings (innerHTML etc)
        # Count occurrences: if all onclick uses of this func are inside template strings, skip
        lines_with_onclick = re.findall(rf'.*onclick.*{func}.*', ct)
        real_html_usage = [l for l in lines_with_onclick if not ('innerHTML' in l or 'html +=' in l or '\\x' in l)]
        if real_html_usage:
            missing.append(func)
    
    if missing:
        print(f'{p}: MISSING: {missing}')
    else:
        print(f'{p}: OK ({len(onclick_funcs)} unique onclick functions)')
