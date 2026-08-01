#!/usr/bin/env python3
"""Fix template-failed EN meta descriptions - remove duplicate words"""
import os, re, json

def fix_desc(desc):
    fixed = desc
    # "free online free X" -> "Free online X"
    fixed = re.sub(r'(?i)free online free\s+', 'Free online ', fixed)
    # "free online online X" -> "Free online X"
    fixed = re.sub(r'(?i)free online online\s+', 'Free online ', fixed)
    # "online online" anywhere
    fixed = re.sub(r'(?i)\bonline online\b', 'online', fixed)
    # "tool tool" anywhere
    fixed = re.sub(r'\btool tool\b', 'tool', fixed)
    # "toolbase toolbase"
    fixed = re.sub(r'(?i)\btoolbase toolbase\b', 'toolbase', fixed)
    return fixed

def fix_file(path):
    with open(path) as f:
        content = f.read()
    
    changed = False
    
    # Fix meta description
    desc_match = re.search(r'(<meta name="description" content=")([^"]+)(")', content)
    if desc_match:
        old = desc_match.group(2)
        new = fix_desc(old)
        if old != new:
            content = content.replace(f'content="{old}"', f'content="{new}"')
            changed = True
    
    # Fix og:description
    og_match = re.search(r'(<meta property="og:description" content=")([^"]+)(")', content)
    if og_match:
        old = og_match.group(2)
        new = fix_desc(old)
        if old != new:
            content = content.replace(f'content="{old}"', f'content="{new}"')
            changed = True
    
    if changed:
        with open(path, 'w') as f:
            f.write(content)
    
    return changed

# Walk all EN pages
total = 0
fixed = 0
for root, dirs, files in os.walk('en'):
    for f in files:
        if f == 'index.html':
            total += 1
            path = os.path.join(root, f)
            if fix_file(path):
                fixed += 1
                print(f'✅ {path}')

print(f'\nTotal EN pages: {total}')
print(f'Fixed: {fixed}')