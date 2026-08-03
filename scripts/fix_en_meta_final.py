#!/usr/bin/env python3
"""Fix EN meta descriptions to 120-160 range."""
import re

fixes = {
    'en/ohms-law-calculator/index.html': "Free online Ohm's law calculator: compute voltage, current, resistance and power. Enter any two values to solve the rest. No signup, browser-based.",
    'en/jensen-alpha-calculator/index.html': "Free online Jensen's Alpha calculator: measure portfolio performance vs market benchmark. Enter return, risk-free rate, beta. No signup, browser-based.",
    'en/conways-game-of-life/index.html': "Free Conway's Game of Life simulator: watch cellular automata evolve on a grid. Adjust speed and patterns. Explore gliders and complex structures. No signup.",
    'en/pizza-dough-calculator/index.html': "Free pizza dough calculator using baker's percentages. Calculate flour, water, salt and yeast amounts. Supports Neapolitan, NY, Detroit styles. No signup.",
    'en/due-date-calculator/index.html': "Free due date calculator: estimate pregnancy due date and gestational age from LMP or conception date. Naegele's rule. No signup, browser-based.",
}

for fpath, new_desc in fixes.items():
    ln = len(new_desc)
    print(f'{fpath}: {ln} chars')
    with open(fpath, 'r', encoding='utf-8') as f:
        html = f.read()
    pattern = r'(name=["\']description["\']\s+content=["\'])[^"\']+(["\'])'
    new_html = re.sub(pattern, lambda m: m.group(1) + new_desc + m.group(2), html, count=1)
    if new_html != html:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(new_html)
        print(f'  -> FIXED')
    else:
        print(f'  -> NO MATCH')

print('\nDone!')
