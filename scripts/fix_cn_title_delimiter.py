#!/usr/bin/env python3
"""Fix · separator in CN tool page titles - replace with |"""
import re, os, glob

tools_dir = '/home/chison/tools-site'
fixed = 0
errors = []

for root, dirs, files in os.walk(tools_dir):
    # Only look at root-level tool directories (CN pages), skip en/ and special dirs
    skip_dirs = {'en', 'css', 'js', 'scripts', 'quality', '.git', '.gsc-data', 'node_modules'}
    rel = os.path.relpath(root, tools_dir)
    if rel == '.':
        continue
    # Only process immediate subdirectories (tool pages)
    if '/' in rel and not rel.startswith('en/'):
        continue
    
    # Only process toplevel tool dirs (CN pages)
    if '/' in rel or rel == 'en':
        continue
    if rel in skip_dirs:
        continue
    
    index_path = os.path.join(root, 'index.html')
    if not os.path.isfile(index_path):
        continue
    
    try:
        with open(index_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace · with | inside <title> tags only
        new_content = re.sub(
            r'<title>([^<]*)·([^<]*)</title>',
            r'<title>\1|\2</title>',
            content
        )
        
        if new_content != content:
            # Also fix og:title consistently
            new_content2 = re.sub(
                r'<meta property="og:title" content="([^"]*)·([^"]*)">',
                r'<meta property="og:title" content="\1|\2">',
                new_content
            )
            
            with open(index_path, 'w', encoding='utf-8') as f:
                f.write(new_content2)
            fixed += 1
            old_title = re.search(r'<title>([^<]+)</title>', content).group(1)
            new_title = re.search(r'<title>([^<]+)</title>', new_content2).group(1)
            print(f'  ✓ {rel}: "{old_title}" → "{new_title}"')
    except Exception as e:
        errors.append(f'{rel}: {e}')

print(f'\nFixed {fixed} CN tool pages')
if errors:
    print(f'Errors: {len(errors)}')
    for e in errors[:5]:
        print(f'  ✗ {e}')
