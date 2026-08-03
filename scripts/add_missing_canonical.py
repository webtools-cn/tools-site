#!/usr/bin/env python3
"""
Add missing canonical tags to pages that don't have one.
"""

import re
import os
import sys

def add_canonical(filepath, dry_run=False):
    """Add canonical tag if missing."""
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Check if canonical already exists
    if re.search(r'<link\s+rel=["\']canonical["\']', html):
        return False, 'already has canonical'
    
    # Get expected URL
    dir_path = os.path.relpath(os.path.dirname(filepath), '.')
    if dir_path == '.':
        expected_url = 'https://free-toolbase.com/'
    else:
        expected_url = f'https://free-toolbase.com/{dir_path}/'
    
    canonical_tag = f'<link rel="canonical" href="{expected_url}">'
    
    # Try to insert after <meta charset> or after <head>
    # Pattern 1: after charset meta
    new_html = re.sub(
        r'(<meta\s+charset=["\'][^"\']*["\'][^>]*>)',
        r'\1\n  ' + canonical_tag,
        html,
        count=1
    )
    
    if new_html == html:
        # Pattern 2: after <head>
        new_html = re.sub(
            r'(<head[^>]*>)',
            r'\1\n  ' + canonical_tag,
            html,
            count=1
        )
    
    if new_html == html:
        return False, 'could not find insertion point'
    
    if not dry_run:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_html)
    
    return True, f'added: {expected_url}'


def main():
    dry_run = '--dry-run' in sys.argv
    
    fixed = 0
    skipped = 0
    errors = 0
    
    for root, dirs, files in os.walk('.'):
        if '.git' in root or 'node_modules' in root:
            continue
        if 'index.html' in files:
            filepath = os.path.join(root, 'index.html')
            rel_path = os.path.relpath(filepath, '.')
            
            success, msg = add_canonical(filepath, dry_run)
            if success:
                fixed += 1
                print(f'FIXED: {rel_path} ({msg})')
            elif msg == 'already has canonical':
                skipped += 1
            else:
                errors += 1
                print(f'ERROR: {rel_path} ({msg})')
    
    print(f'\nResults: {fixed} fixed, {skipped} already have canonical, {errors} errors')


if __name__ == '__main__':
    main()
