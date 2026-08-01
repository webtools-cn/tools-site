#!/usr/bin/env python3
"""
Fix remaining Chinese short descriptions (<100 chars) by intelligently extending them.
Reads the h1 and existing content, generates proper 140-160 char description.
"""
import os
import re
import glob

BASE = '/home/chison/tools-site'

def get_h1_text(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    m = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.DOTALL)
    if m:
        return re.sub(r'<[^>]+>', '', m.group(1)).strip()
    return None

def get_existing_desc(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    m = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', content)
    if m:
        return m.group(1)
    return None

def smart_extend(desc, h1):
    """Intelligently extend a short description to 140-160 chars."""
    desc = desc.strip()
    # Remove trailing junk
    desc = re.sub(r'[。，,\s]*$', '', desc)
    desc = re.sub(r'无需注册完全免费\.?$', '', desc).strip()
    desc = re.sub(r'数据不上传服务器[，,]?\s*$', '', desc).strip()
    desc = re.sub(r'纯前端本地处理[，,]?\s*$', '', desc).strip()
    
    if len(desc) >= 130:
        if '无需注册' not in desc:
            desc += '无需注册，免费使用。'
        return desc[:160]
    
    # Add standard closing if not present
    closing = '纯前端本地处理，数据不上传服务器，无需注册完全免费。'
    if '数据不上传' in desc:
        closing = '无需注册完全免费。'
    if '无需注册' in desc:
        closing = ''
    
    # Build extended description
    if h1:
        # Try to add h1-based context
        tool_type = h1.replace('免费在线', '').replace('工具', '').strip()
        if len(desc) < 120 and tool_type:
            extra = f'{tool_type}支持实时预览，操作简单快捷。'
            desc = f'{desc}{extra}{closing}'
    
    # Trim to 160 chars
    if len(desc) > 160:
        # Find last sentence boundary
        cutoff = desc.rfind('。', 0, 155)
        if cutoff > 130:
            desc = desc[:cutoff+1]
        else:
            desc = desc[:157] + '...'
    
    return desc

def fix_file(filepath):
    desc = get_existing_desc(filepath)
    if not desc:
        return False
    
    if len(desc) >= 100:
        return False
    
    h1 = get_h1_text(filepath)
    new_desc = smart_extend(desc, h1)
    
    if len(new_desc) < 100:
        # Fallback: generate from h1
        if h1:
            new_desc = f'{h1}，支持实时交互操作，结果即时显示。纯前端本地处理，数据不上传服务器，无需注册完全免费。'
        else:
            return False
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    new_content = re.sub(
        r'<meta\s+name="description"\s+content="[^"]*"',
        lambda m: f'<meta name="description" content="{new_desc}"',
        content
    )
    
    with open(filepath, 'w') as f:
        f.write(new_content)
    
    return True

def main():
    files = glob.glob(os.path.join(BASE, '*/index.html'))
    # Exclude special pages
    exclude = {'about', 'en', 'css', 'js', 'scripts', 'quality', 'data', 'dev', 'office', 'media', 'creative', 'security'}
    fixed = 0
    for f in sorted(files):
        dirname = os.path.basename(os.path.dirname(f))
        if dirname in exclude:
            continue
        if fix_file(f):
            fixed += 1
            if fixed <= 50:  # Limit verbose output
                print(f"[{len(get_existing_desc(f))}→{len(get_existing_desc(f))}] Fixed: {f}")
    
    print(f"\nTotal fixed: {fixed}")

if __name__ == '__main__':
    main()