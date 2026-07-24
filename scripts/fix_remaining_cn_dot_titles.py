#!/usr/bin/env python3
"""Fix remaining · separator in CN tool page titles - replace with |"""
import re, os

tools_dir = '/home/chison/tools-site'
fixed = 0
errors = []

# Read the list of pages with · in title
with open('/tmp/cn_dot_titles.txt', 'r') as f:
    pages = [line.strip() for line in f if line.strip()]

print(f"Found {len(pages)} pages with · in <title>")

for index_path in pages:
    if not os.path.isfile(index_path):
        continue
    
    rel = os.path.relpath(index_path, tools_dir)
    try:
        with open(index_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        
        # Replace · with | in <title> tags (handle one or multiple ·)
        content = re.sub(
            r'<title>([^<]*)·([^<]*)</title>',
            lambda m: '<title>' + m.group(1).strip() + '|' + m.group(2).strip() + '</title>',
            content
        )
        
        # Also fix og:title consistently
        content = re.sub(
            r'<meta property="og:title" content="([^"]*)·([^"]*)">',
            lambda m: '<meta property="og:title" content="' + m.group(1).strip() + '|' + m.group(2).strip() + '">',
            content
        )
        
        # Run a second pass for titles with multiple ·
        content = re.sub(
            r'<title>([^<]*)·([^<]*)</title>',
            lambda m: '<title>' + m.group(1).strip() + '|' + m.group(2).strip() + '</title>',
            content
        )
        content = re.sub(
            r'<meta property="og:title" content="([^"]*)·([^"]*)">',
            lambda m: '<meta property="og:title" content="' + m.group(1).strip() + '|' + m.group(2).strip() + '">',
            content
        )
        
        if content != original:
            with open(index_path, 'w', encoding='utf-8') as f:
                f.write(content)
            fixed += 1
            old_title = re.search(r'<title>([^<]+)</title>', original).group(1)
            new_title = re.search(r'<title>([^<]+)</title>', content).group(1)
            print(f'  ✓ {rel}: "{old_title}" → "{new_title}"')
    except Exception as e:
        errors.append(f'{rel}: {e}')

print(f'\nFixed {fixed} CN tool pages')
if errors:
    print(f'Errors: {len(errors)}')
    for e in errors[:5]:
        print(f'  ✗ {e}')
