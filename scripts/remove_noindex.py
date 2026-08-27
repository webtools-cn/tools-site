#!/usr/bin/env python3
"""Remove noindex tags from all HTML files"""

import os
import re
from pathlib import Path

SITE_DIR = Path("/home/chison/tools-site")

def remove_noindex(filepath):
    """Remove noindex meta tag from file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if file has noindex
        if 'noindex' not in content:
            return False
        
        # Remove noindex meta tags (various formats)
        patterns = [
            r'<meta\s+name="robots"\s+content="[^"]*noindex[^"]*"[^>]*>',
            r'<meta\s+content="[^"]*noindex[^"]*"\s+name="robots"[^>]*>',
        ]
        
        original = content
        for pattern in patterns:
            content = re.sub(pattern, '', content, flags=re.IGNORECASE)
        
        # Clean up empty lines left behind
        content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
        
        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

def main():
    fixed = 0
    errors = []
    
    print("Scanning for noindex tags...")
    
    for root, dirs, files in os.walk(SITE_DIR):
        # Skip hidden directories
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for file in files:
            if file.endswith('.html'):
                filepath = Path(root) / file
                if remove_noindex(filepath):
                    fixed += 1
                    rel_path = filepath.relative_to(SITE_DIR)
                    print(f"Fixed: {rel_path}")
    
    print(f"\nTotal fixed: {fixed} files")

if __name__ == "__main__":
    main()
