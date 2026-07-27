#!/usr/bin/env python3
"""缩短 EN title 到 60 字符以内"""
import re
import os

BASE = "/home/chison/tools-site"

SHORT_TITLES = {
    "bench-press-calculator": "Bench Press 1RM Calculator | Free ToolBase",
    "caffeine-half-life-calculator": "Caffeine Half-Life Calculator | Free ToolBase",
    "confidence-interval-calculator": "Confidence Interval Calculator | Free ToolBase",
    "cost-per-click-calculator": "CPC Calculator - Ad Budget | Free ToolBase",
    "monte-carlo-simulator": "Monte Carlo Simulator | Free ToolBase",
}

for name, short_title in SHORT_TITLES.items():
    fp = os.path.join(BASE, "en", name, "index.html")
    with open(fp, 'r') as f:
        content = f.read()
    
    old_title = re.search(r'<title>.*?</title>', content)
    if old_title:
        new_full = f'<title>{short_title}</title>'
        print(f"{name}: {old_title.group()} ({len(old_title.group())} chars) -> {new_full} ({len(new_full)} chars)")
        content = content.replace(old_title.group(), new_full)
        
        # Also fix og:title
        old_og = re.search(r'<meta property="og:title" content=".*?">', content)
        if old_og:
            og_new = f'<meta property="og:title" content="{short_title}">'
            content = content.replace(old_og.group(), og_new)
    
    with open(fp, 'w') as f:
        f.write(content)

print("\nDone")
