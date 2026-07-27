#!/usr/bin/env python3
"""修复 EN 页面被错误写入中文title的问题"""
import re
import os

BASE = "/home/chison/tools-site"

EN_TITLES = {
    "bench-press-calculator": "Bench Press 1RM Calculator - Max Weight & Strength Level",
    "caffeine-half-life-calculator": "Caffeine Half-Life Calculator - Intake & Metabolism Tracker",
    "confidence-interval-calculator": "Confidence Interval Calculator - Online Statistical Analysis",
    "cost-per-click-calculator": "CPC Cost Per Click Calculator - Ad Budget Analysis",
    "monte-carlo-simulator": "Monte Carlo Simulator - Online Probability & Risk Analysis",
}

for name, en_title in EN_TITLES.items():
    fp = os.path.join(BASE, "en", name, "index.html")
    with open(fp, 'r') as f:
        content = f.read()
    
    # Replace Chinese title with English
    old_title = re.search(r'<title>免费在线.*?</title>', content)
    if old_title:
        new_title = f'<title>{en_title} - Free ToolBase</title>'
        content = content.replace(old_title.group(), new_title)
        
        # Also fix og:title
        old_og = re.search(r'<meta property="og:title" content="免费在线.*?">', content)
        if old_og:
            og_new = f'<meta property="og:title" content="{en_title} - Free ToolBase">'
            content = content.replace(old_og.group(), og_new)
    
    with open(fp, 'w') as f:
        f.write(content)
    print(f"Fixed: en/{name}")

print("Done")
