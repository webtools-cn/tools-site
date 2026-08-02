import os, re

check_list = [
    'text-to-list', 'recipe-nutrition-analyzer', 'tip-calculator', 'carpet-calculator',
    'gray-code-converter', 'image-hue-rotate', 'inheritance-tax-calculator', 'list-sorter',
    'marathon-pace-calculator', 'name-meaning-finder', 'random-password', 'retirement-corpus',
    'tap-code', 'ternary-converter', 'vaccination-schedule', 'coin-flipper',
    'file-size-calculator', 'image-merge', 'image-shadow-generator', 'color-palette',
    'currency-strength-meter', 'data-generator', 'date-add-subtract', 'education-loan-calculator',
    'effective-tax-rate', 'expense-split-calculator', 'graphing-calculator', 'home-loan-calculator',
    'house-affordability-calculator', 'hydration-tracker'
]

for d in check_list:
    with open(f'{d}/index.html') as f:
        content = f.read(3000)
    m = re.search(r'<meta name="description" content="([^"]*)"', content)
    if m:
        l = len(m.group(1))
        flag = 'GOOD' if 100 <= l <= 160 else f'BAD ({l})'
        print(f'{flag:10s} | {d:40s} | {l} chars')
    else:
        print(f'MISSING   | {d:40s} |')
