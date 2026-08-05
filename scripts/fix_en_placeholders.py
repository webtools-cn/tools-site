#!/usr/bin/env python3
"""修复8个EN页面的 TOOL_NAME_CN 占位符"""
import os

NAMES = {
    'paint-needed-calculator': 'Paint Needed Calculator',
    'paper-size-calculator': 'Paper Size Converter',
    'mix-ratio-calculator': 'Mix Ratio Calculator',
    'coffee-cost-calculator': 'Coffee Cost Calculator',
    'ramp-slope-calculator': 'Ramp Slope Calculator',
    'carpet-cost-calculator': 'Carpet Cost Calculator',
    'soil-volume-calculator': 'Soil Volume Calculator',
    'event-budget-calculator': 'Event Budget Calculator',
}

for tool, en_name in NAMES.items():
    filepath = f'en/{tool}/index.html'
    if not os.path.exists(filepath):
        print(f"SKIP: {filepath} not found")
        continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    count = content.count('TOOL_NAME_CN')
    content = content.replace('TOOL_NAME_CN', en_name)
    
    # 同时修复 "关于 TOOL_NAME" → "About TOOL_NAME"
    content = content.replace(f'关于 {en_name}', f'About {en_name}')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"FIXED: {filepath} ({count} replacements)")

print("\nDone!")
