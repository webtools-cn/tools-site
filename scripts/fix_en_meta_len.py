#!/usr/bin/env python3
"""Fix EN meta descriptions that are too long (>160 chars)."""
import re

fixes = {
    'en/ohms-law-calculator/index.html': "Free online Ohm's law calculator: compute voltage, current, resistance & power. Enter any two values to solve the rest. Perfect for electronics and circuit design. No signup.",
    'en/jensen-alpha-calculator/index.html': "Free online Jensen's Alpha calculator: measure portfolio performance vs market benchmark. Enter return, risk-free rate, market return & beta. Ideal for fund evaluation. No signup.",
    'en/conways-game-of-life/index.html': "Free online Conway's Game of Life simulator: watch cellular automata evolve. Adjust speed, grid size & patterns. Explore gliders and complex structures. No signup required.",
    'en/pizza-dough-calculator/index.html': "Free online pizza dough calculator using baker's percentages. Calculate flour, water, salt & yeast amounts. Supports Neapolitan, NY, Detroit styles. Runs in your browser.",
    'en/due-date-calculator/index.html': "Free due date calculator: estimate pregnancy due date & gestational age from LMP or conception date. Accurate Naegele's rule calculation. No signup, browser-based.",
}

for fpath, new_desc in fixes.items():
    with open(fpath, 'r', encoding='utf-8') as f:
        html = f.read()
    
    ln = len(new_desc)
    pattern = r'(name=["\']description["\']\s+content=["\'])[^"\']+(["\'])'
    new_html = re.sub(pattern, lambda m: m.group(1) + new_desc + m.group(2), html, count=1)
    
    if new_html != html:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(new_html)
        print(f'{fpath}: {ln} chars -> FIXED')
    else:
        print(f'{fpath}: no match')

print('\nDone!')
