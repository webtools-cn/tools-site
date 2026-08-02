#!/usr/bin/env python3
"""Extract too-short descriptions - get full file paths and current desc."""
import os, re

results = []

for root, dirs, files in os.walk('.'):
    dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', 'quality', '.gsc-data', 'scripts', 'css', 'js']]
    for f in files:
        if f == 'index.html' and '/en/' not in root:
            path = os.path.join(root, f)
            try:
                with open(path) as fh:
                    content = fh.read(5000)
                m = re.search(r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']+)["\']', content)
                if m:
                    desc = m.group(1)
                    l = len(desc)
                    if l < 100:
                        results.append((l, path, desc))
            except:
                pass

# Sort by length ascending
results.sort()
print(f'Total: {len(results)}')

# Pick 30: shorter ones with SEO potential
selected = [
    'cardio-risk-calculator', 'payroll-tax-calculator', 'workdays-calculator',
    'stock-average-calculator', 'days-between-dates', 'solar-roi-calculator',
    'fraction-to-decimal', 'timesheet-calculator', 'password-strength-tester',
    'random-color-generator', 'week-planner', 'css-to-tailwind-converter',
    'http-status-checker', 'web-accessibility-checker', 'color-palette',
    'perpetuity-calculator', 'dividend-growth-calculator', 'viewport-tester',
    'image-resizer', 'text-deduplicate', 'text-sorter', 'csv-to-geojson',
    'profit-margin-calculator', 'apy-to-apr-calculator', 'quadratic-solver',
    'color-blender', 'markdown-table-formatter', 'changelog-parser',
    'binary-clock', 'openapi-generator'
]

for r in results:
    for s in selected:
        if f'/{s}/index.html' in r[1]:
            print(f'{r[0]:4d} | {r[1]} | {r[2]}')
            break