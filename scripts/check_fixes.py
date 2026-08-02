#!/usr/bin/env python3
"""Check description lengths after fix."""
import re

files = [
    'voltage-drop-calculator/index.html',
    'work-hours-calculator/index.html',
    'rich-text-editor/index.html',
    'image-mirror/index.html',
    'fuel-efficiency/index.html',
    'headline-generator/index.html',
    'net-worth-calculator/index.html',
    'ingredient-substitute-finder/index.html',
    'circle-calculator/index.html',
    'forex-pip-calculator/index.html',
    'percentage-difference-calculator/index.html',
    'directory-tree-generator/index.html',
    'word-density-analyzer/index.html',
    'keyword-density-analyzer/index.html',
    'image-batch-resizer/index.html',
]
for f in files:
    content = open(f, encoding='utf-8').read()
    m = re.search(r'<meta\s+name=[\"\']description[\"\']\s+content=\"([^\"]+)\"', content)
    if m:
        d = m.group(1)
        print(f'{len(d):3d} | {f}: {d}')
    else:
        print(f'  ? | {f}: NOT FOUND')