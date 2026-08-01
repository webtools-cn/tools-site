#!/usr/bin/env python3
"""
Fix remaining Chinese short descriptions - batch cleanup.
- Clean emoji prefixes from h1-derived text
- Further extend very short descriptions
"""
import os
import re
import glob

BASE = '/home/chison/tools-site'

def clean_desc(desc):
    """Clean up description - remove emoji prefixes, double periods, etc."""
    # Remove leading emoji and space
    desc = re.sub(r'^[\U0001F300-\U0001F9FF\u2600-\u27BF\u2B50\U0001F600-\U0001F64F\U0001F680-\U0001F6FF\U0001F900-\U0001F9FF\u2702-\u27B0\u24C2-\U0001F251\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF\U00002500-\U00002BEF\U0001F900-\U0001F9FF\U0000200D\U0000FE0F]+\s*', '', desc)
    # Fix double periods
    desc = re.sub(r'\.{2,}', '.', desc)
    desc = re.sub(r'。。+', '。', desc)
    desc = re.sub(r'，,', '，', desc)
    # Fix "模型，。" -> "模型。"
    desc = re.sub(r'[，,]\s*[。.]', '。', desc)
    # Remove trailing partial sentence like "纯前端本地处理，数据不上传服务器，无需注册免费使用" at the end without proper ending
    desc = re.sub(r'无需注册免费使用$', '无需注册，免费使用。', desc)
    desc = re.sub(r'无需注册完全免费$', '无需注册，完全免费。', desc)
    if not desc.endswith('。') and not desc.endswith('.') and len(desc) > 50:
        desc += '。'
    
    return desc

def fix_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    
    m = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', content)
    if not m:
        return False
    
    old_desc = m.group(1)
    if len(old_desc) >= 140:
        return False
    
    new_desc = clean_desc(old_desc)
    
    # If still too short, add generic ending
    if len(new_desc) < 120:
        if '无需注册' not in new_desc and '免费' not in new_desc:
            new_desc = new_desc.rstrip('。') + '。纯前端本地处理，数据不上传服务器，无需注册完全免费。'
        elif '数据不上传' not in new_desc:
            new_desc = new_desc.rstrip('。') + '。纯前端本地处理，数据安全有保障。'
    
    # Trim to 160
    if len(new_desc) > 160:
        cutoff = new_desc.rfind('。', 0, 158)
        if cutoff > 130:
            new_desc = new_desc[:cutoff+1]
        else:
            new_desc = new_desc[:157] + '...'
    
    if new_desc == old_desc:
        return False
    
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
        if fix_file(f):
            fixed += 1
            if fixed <= 30:
                with open(f, 'r') as fh:
                    content = fh.read()
                m = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', content)
                new_len = len(m.group(1)) if m else 0
                print(f"[{new_len}c] {f}")
    
    print(f"\nTotal fixed: {fixed}")

if __name__ == '__main__':
    main()