#!/usr/bin/env python3
"""
Fix HTML syntax errors: remove extra '>' characters after meta/link tags.
Patterns:
  - content="...">>  → content="...">
  - content="...">>>  → content="...">
  - content="...">>>> → content="...">
  - follow">>  → follow">
  - follow">>> → follow">
"""
import os
import re
import sys

def fix_extra_gt(content):
    """Replace patterns like '">>' or '">>>' with '">'."""
    # Match: " followed by 2 or more > characters
    # But NOT inside attribute values or text content
    # We specifically target: content="...">>+ or similar tag endings
    
    # Pattern 1: after closing quote of attribute value, 2+ '>' chars
    fixed = re.sub(r'">[>]+', r'">', content)
    
    # Pattern 2: after 'follow"' or 'noindex"' with extra '>'  
    # Already covered by pattern 1
    
    return fixed

def process_file(filepath):
    """Process a single HTML file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"  ERROR reading {filepath}: {e}")
        return False
    
    original = content
    fixed = fix_extra_gt(content)
    
    if fixed != original:
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(fixed)
            # Count how many fixes
            count = original.count('">>') + original.count('">>>') + original.count('">>>>')
            return True
        except Exception as e:
            print(f"  ERROR writing {filepath}: {e}")
            return False
    return False

def main():
    root = '/home/chison/tools-site'
    fixed_count = 0
    total_scanned = 0
    
    for dirpath, dirnames, filenames in os.walk(root):
        # Skip .git, node_modules, etc.
        dirnames[:] = [d for d in dirnames if d not in ('.git', 'node_modules', '__pycache__')]
        
        for filename in filenames:
            if filename == 'index.html':
                filepath = os.path.join(dirpath, filename)
                total_scanned += 1
                if process_file(filepath):
                    fixed_count += 1
                    if fixed_count <= 20:
                        print(f"  Fixed: {filepath}")
                    elif fixed_count == 21:
                        print(f"  ... (more files fixed, suppressing output)")
    
    print(f"\n=== Summary ===")
    print(f"Total files scanned: {total_scanned}")
    print(f"Files fixed: {fixed_count}")

if __name__ == '__main__':
    main()
