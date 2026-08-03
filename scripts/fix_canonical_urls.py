#!/usr/bin/env python3
"""
Fix wrong canonical URLs across all pages.
Each page's canonical should point to its own URL: https://free-toolbase.com/<dir_path>/
"""

import re
import os
import sys

def fix_canonical(filepath, dry_run=False):
    """Fix canonical URL in a single file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Get the directory path relative to site root
    dir_path = os.path.relpath(os.path.dirname(filepath), '.')
    if dir_path == '.':
        expected_url = 'https://free-toolbase.com/'
    else:
        expected_url = f'https://free-toolbase.com/{dir_path}/'
    
    # Find canonical tag
    canon_pattern = r'<link rel="canonical" href="([^"]+)"'
    match = re.search(canon_pattern, html)
    
    if not match:
        return False, 'no canonical tag'
    
    current_url = match.group(1)
    
    if current_url == expected_url:
        return False, 'already correct'
    
    # Fix the canonical
    old_tag = f'<link rel="canonical" href="{current_url}"'
    new_tag = f'<link rel="canonical" href="{expected_url}"'
    
    new_html = html.replace(old_tag, new_tag, 1)
    
    # Verify replacement happened
    if new_html == html:
        return False, 'replacement failed'
    
    if not dry_run:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_html)
    
    return True, f'{current_url} -> {expected_url}'


def main():
    dry_run = '--dry-run' in sys.argv
    
    fixed = 0
    skipped = 0
    errors = 0
    details = []
    
    for root, dirs, files in os.walk('.'):
        if '.git' in root or 'node_modules' in root:
            continue
        if 'index.html' in files:
            filepath = os.path.join(root, 'index.html')
            rel_path = os.path.relpath(filepath, '.')
            
            success, msg = fix_canonical(filepath, dry_run)
            if success:
                fixed += 1
                details.append(f'FIXED: {rel_path} ({msg})')
            elif msg == 'already correct':
                skipped += 1
            else:
                errors += 1
                details.append(f'ERROR: {rel_path} ({msg})')
    
    print(f'Results: {fixed} fixed, {skipped} already correct, {errors} errors')
    
    if details:
        print(f'\nFirst 20 changes:')
        for d in details[:20]:
            print(f'  {d}')
        if len(details) > 20:
            print(f'  ... and {len(details) - 20} more')


if __name__ == '__main__':
    main()
