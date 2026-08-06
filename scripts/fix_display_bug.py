#!/usr/bin/env python3
"""Fix display:none bug in 8 new calculator tools (CN + EN)."""
import re, os

TOOLS = [
    "investment-return-calculator",  # CN already fixed, EN needs fix
    "loan-installment-calculator",
    "marketing-roi-calculator",
    "simplify-fractions",
    "sip-return-calculator",
    "net-present-value",
    "rule-72-calculator",
    "daily-calorie-burn",
]

fixed = []
skipped = []

for tool in TOOLS:
    for path in [f"{tool}/index.html", f"en/{tool}/index.html"]:
        if not os.path.exists(path):
            skipped.append(f"{path} (not found)")
            continue
        
        with open(path, 'r') as f:
            content = f.read()
        
        # Check if already fixed
        if "style.display='block'" in content or 'style.display="block"' in content:
            skipped.append(f"{path} (already fixed)")
            continue
        
        # Strategy: 
        # 1. Add display toggle before the first result.innerHTML assignment
        # 2. Replace all bare "result.innerHTML" with "document.getElementById('result').innerHTML"
        
        # Find the first occurrence of "result.innerHTML" after the input validation block
        # and add display toggle before it
        lines = content.split('\n')
        new_lines = []
        display_added = False
        
        for line in lines:
            # Add display toggle before first result.innerHTML usage
            if 'result.innerHTML' in line and not display_added:
                # Check this is inside calc() - after the validation lines
                new_lines.append("document.getElementById('result').style.display='block';")
                display_added = True
            
            # Replace bare result.innerHTML with document.getElementById('result').innerHTML
            new_line = line.replace('result.innerHTML', "document.getElementById('result').innerHTML")
            new_lines.append(new_line)
        
        new_content = '\n'.join(new_lines)
        
        with open(path, 'w') as f:
            f.write(new_content)
        
        fixed.append(path)

print(f"Fixed: {len(fixed)}")
for f in fixed:
    print(f"  ✅ {f}")
print(f"\nSkipped: {len(skipped)}")
for s in skipped:
    print(f"  ⏭️ {s}")
