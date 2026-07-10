#!/usr/bin/env python3
"""Add dateModified to SoftwareApplication Schema on all tool pages.
Handles both multi-line and single-line formats.
"""
import os
import re
from datetime import date

TOOLS_DIR = os.path.expanduser("~/project")
TODAY = date.today().isoformat()

def add_datemodified_to_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if '"dateModified"' in content:
        return False  # Already has it
    
    # Case 1: Multi-line SoftwareApplication schema (prettified JSON)
    # Match from "@type": "SoftwareApplication" through the offers block
    pattern1 = r'("@type":\s*"SoftwareApplication"[^}]*?"operatingSystem":\s*"[^"]*")'
    
    def add_date_multi(match):
        block = match.group(1)
        if '"dateModified"' in block:
            return block
        # Add dateModified after operatingSystem field
        return re.sub(
            r'("operatingSystem":\s*"[^"]*")',
            r'\1,\n  "dateModified": "' + TODAY + '"',
            block
        )
    
    new_content = re.sub(pattern1, add_date_multi, content)
    
    # Case 2: Single-line SoftwareApplication schema (compact JSON)
    # Match {"@context":"https://schema.org","@type":"SoftwareApplication", ...}
    pattern2 = r'(\{"@context":"https://schema.org","@type":"SoftwareApplication"[^}]*?"operatingSystem":"[^"]*")'
    
    def add_date_single(match):
        block = match.group(1)
        if '"dateModified"' in block:
            return block
        # Add dateModified after operatingSystem
        return re.sub(
            r'("operatingSystem":"[^"]*")',
            r'\1,"dateModified":"' + TODAY + '"',
            block
        )
    
    new_content = re.sub(pattern2, add_date_single, new_content)
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

def main():
    # Walk all HTML files in tools-site
    updated = 0
    skipped = 0
    
    for root, dirs, files in os.walk(TOOLS_DIR):
        # Skip .git directory
        if '.git' in root:
            continue
        for f in files:
            if f == 'index.html':
                filepath = os.path.join(root, f)
                if add_datemodified_to_file(filepath):
                    updated += 1
                else:
                    skipped += 1
    
    print(f"{updated} files updated, {skipped} skipped (already had dateModified or no SoftwareApplication)")

if __name__ == "__main__":
    main()
