#!/usr/bin/env python3
"""Fix P0 bug: calc() doesn't show result (display:none never set to block)"""
import re, os

tools = [
    "working-capital-calculator",
    "parking-fee-calculator", 
    "gold-purity-calculator",
    "gold-price-calculator",
    "silver-price-calculator",
    "fabric-yardage-calculator",
    "rug-size-calculator",
    "dress-size-converter",
]

base = "/home/chison/tools-site"
fixed = 0

for tool in tools:
    for lang_dir in ["", "en/"]:
        path = os.path.join(base, lang_dir, tool, "index.html")
        if not os.path.exists(path):
            print(f"SKIP (not found): {path}")
            continue
        
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if already fixed
        if "result.style.display" in content:
            print(f"ALREADY FIXED: {path}")
            continue
        
        # Find result.innerHTML = `...`; line and insert result.style.display='block'; before it
        # Pattern: result.innerHTML = `
        pattern = r'(result\.innerHTML\s*=\s*`)'
        replacement = r"result.style.display='block';\n\1"
        
        new_content = re.sub(pattern, replacement, content)
        
        if new_content != content:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"FIXED: {path}")
            fixed += 1
        else:
            print(f"NO MATCH: {path}")

print(f"\nTotal fixed: {fixed}")
