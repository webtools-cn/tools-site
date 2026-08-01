#!/usr/bin/env python3
"""
Fix damaged descriptions (too short, missing content) by regenerating from title/h1.
"""
import os
import re
import glob

BASE = '/home/chison/tools-site'

def get_title(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    m = re.search(r'<title>(.*?)(?:\s*[-–—|]\s*Free ToolBase)?</title>', content, re.IGNORECASE)
    if m:
        return m.group(1).strip()
    return None

def fix_damaged(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    
    m = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', content)
    if not m:
        return False
    
    old_desc = m.group(1)
    if len(old_desc) >= 50:
        return False  # Not damaged enough
    
    # Regenerate from title
    title = get_title(filepath)
    if not title:
        return False
    
    # Clean up title for description
    clean_title = re.sub(r'^免费在线\s*', '', title)
    clean_title = re.sub(r'\s*工具$', '', clean_title)
    clean_title = re.sub(r'\s*在线$', '', clean_title)
    
    new_desc = f'免费在线{clean_title}工具，快速高效地完成{clean_title}操作。支持实时交互和即时结果显示。纯前端本地处理，数据不上传服务器，无需注册完全免费。'
    
    # Trim to 160
    if len(new_desc) > 160:
        cutoff = new_desc.rfind('。', 0, 158)
        if cutoff > 130:
            new_desc = new_desc[:cutoff+1]
    
    new_content = content.replace(
        f'<meta name="description" content="{old_desc}"',
        f'<meta name="description" content="{new_desc}"'
    )
    
    with open(filepath, 'w') as f:
        f.write(new_content)
    
    return True

def main():
    files = glob.glob(os.path.join(BASE, '*/index.html'))
    exclude = {'about', 'en', 'css', 'js', 'scripts', 'quality'}
    fixed = 0
    for f in sorted(files):
        dirname = os.path.basename(os.path.dirname(f))
        if dirname in exclude:
            continue
        if fix_damaged(f):
            fixed += 1
            if fixed <= 20:
                print(f"Repaired: {f}")
    
    print(f"\nTotal repaired: {fixed}")

if __name__ == '__main__':
    main()