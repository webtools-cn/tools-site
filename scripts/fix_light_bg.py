#!/usr/bin/env python3
"""批量修复浅色背景页面 - 将#fff等替换为#0f172a深色主题"""
import os, re, sys

DRY_RUN = '--dry' in sys.argv

def fix_light_bg(filepath):
    c = open(filepath, 'r', errors='ignore').read()
    original = c
    
    # Find <style> block
    style_m = re.search(r'(<style>)(.*?)(</style>)', c, re.DOTALL)
    if not style_m:
        return False, 'no style block'
    
    style = style_m.group(2)
    
    # Replace light backgrounds with dark theme
    replacements = [
        (r'background\s*:\s*#fff\b', 'background: #0f172a'),
        (r'background\s*:\s*#ffffff\b', 'background: #0f172a'),
        (r'background\s*:\s*#f8f9fa\b', 'background: #0f172a'),
        (r'background\s*:\s*#fafafa\b', 'background: #0f172a'),
        (r'background\s*:\s*#f5f5f5\b', 'background: #0f172a'),
        (r'background\s*:\s*#eee\b', 'background: #0f172a'),
        (r'background\s*:\s*#eeeeee\b', 'background: #0f172a'),
        (r'background-color\s*:\s*#fff\b', 'background-color: #0f172a'),
        (r'background-color\s*:\s*#ffffff\b', 'background-color: #0f172a'),
        (r'background-color\s*:\s*#f8f9fa\b', 'background-color: #0f172a'),
        (r'background-color\s*:\s*#fafafa\b', 'background-color: #0f172a'),
        (r'background-color\s*:\s*#f5f5f5\b', 'background-color: #0f172a'),
        (r'background-color\s*:\s*#eee\b', 'background-color: #0f172a'),
        (r'background-color\s*:\s*#eeeeee\b', 'background-color: #0f172a'),
        # Also fix light text on now-dark backgrounds
        (r'color\s*:\s*#333\b', 'color: #e2e8f0'),
        (r'color\s*:\s*#666\b', 'color: #94a3b8'),
        (r'color\s*:\s*#999\b', 'color: #64748b'),
        (r'color\s*:\s*#212529\b', 'color: #e2e8f0'),
        (r'color\s*:\s*#343a40\b', 'color: #e2e8f0'),
        # Fix light borders
        (r'border\s*:\s*1px\s+solid\s+#ddd\b', 'border: 1px solid rgba(148,163,184,.1)'),
        (r'border\s*:\s*1px\s+solid\s+#dee2e6\b', 'border: 1px solid rgba(148,163,184,.1)'),
        (r'border\s*:\s*1px\s+solid\s+#ccc\b', 'border: 1px solid rgba(148,163,184,.1)'),
    ]
    
    new_style = style
    for pattern, replacement in replacements:
        new_style = re.sub(pattern, replacement, new_style)
    
    if new_style == style:
        return False, 'no changes needed'
    
    c = c.replace(style, new_style, 1)
    
    if not DRY_RUN:
        open(filepath, 'w', encoding='utf-8', errors='ignore').write(c)
    
    return True, 'fixed'

# CN pages
cn_fixed = 0
cn_list = []
for d in sorted(os.listdir('.')):
    p = os.path.join(d, 'index.html')
    if not os.path.isfile(p) or d == 'en': continue
    c = open(p, 'r', errors='ignore').read()
    style_m = re.search(r'<style>(.*?)</style>', c, re.DOTALL)
    if not style_m: continue
    style = style_m.group(1)
    if re.search(r'background[^:]*:\s*#(fff|ffffff|f8f9fa|fafafa|f5f5f5|eee|eeeeee)', style, re.I):
        ok, msg = fix_light_bg(p)
        if ok:
            cn_fixed += 1
            cn_list.append(d)

# EN pages
en_fixed = 0
en_list = []
for d in sorted(os.listdir('en')):
    p = os.path.join('en', d, 'index.html')
    if not os.path.isfile(p): continue
    c = open(p, 'r', errors='ignore').read()
    style_m = re.search(r'<style>(.*?)</style>', c, re.DOTALL)
    if not style_m: continue
    style = style_m.group(1)
    if re.search(r'background[^:]*:\s*#(fff|ffffff|f8f9fa|fafafa|f5f5f5|eee|eeeeee)', style, re.I):
        ok, msg = fix_light_bg(p)
        if ok:
            en_fixed += 1
            en_list.append(d)

print(f"CN fixed: {cn_fixed}")
print(f"EN fixed: {en_fixed}")
print(f"Total: {cn_fixed + en_fixed}")
if DRY_RUN:
    print("(DRY RUN - no files written)")
