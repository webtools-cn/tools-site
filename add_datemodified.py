#!/usr/bin/env python3
"""Add dateModified to SoftwareApplication Schema on all tool pages.

GEO optimization: AI engines prefer recent, maintained sources.
Adding dateModified tells AI crawlers the content is current.
"""
import os
import re
import json
from datetime import date

TOOLS_DIR = os.path.expanduser("~/project")
TODAY = date.today().isoformat()  # 2026-07-10

def add_datemodified_to_file(filepath):
    """Add dateModified to SoftwareApplication schema in the file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find SoftwareApplication schema
    pattern = r'("@type":\s*"SoftwareApplication".*?"offers":\s*\{[^}]+\})'
    
    def add_date(match):
        schema_text = match.group(1)
        if '"dateModified"' in schema_text:
            return schema_text  # already has it
        # Add dateModified after operatingSystem
        schema_text = schema_text.replace(
            '"operatingSystem": "Web",',
            f'"operatingSystem": "Web",\n  "dateModified": "{TODAY}",'
        )
        return schema_text
    
    new_content = re.sub(pattern, add_date, content, flags=re.DOTALL)
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

def main():
    # Check if there are directories with index.html  
    all_dirs = []
    for root, dirs, files in os.walk(TOOLS_DIR):
        for f in files:
            if f == 'index.html' and root != TOOLS_DIR:
                # Skip non-tool dirs
                rel = os.path.relpath(root, TOOLS_DIR)
                if rel in ('.', 'en', '.git', '.github', 'policy', 'privacy', 'terms'):
                    continue
                all_dirs.append(os.path.join(root, f))
    
    # Also check en/ subdirs
    # Count and process
    cn_files = []
    en_files = []
    for fp in all_dirs:
        if fp.startswith(os.path.join(TOOLS_DIR, 'en')):
            en_files.append(fp)
        else:
            cn_files.append(fp)
    
    print(f"Found {len(cn_files)} CN pages, {len(en_files)} EN pages")
    
    # Process
    cn_updated = 0
    en_updated = 0
    cn_skipped = 0
    en_skipped = 0
    
    for fp in cn_files:
        if add_datemodified_to_file(fp):
            cn_updated += 1
        else:
            cn_skipped += 1
    
    for fp in en_files:
        if add_datemodified_to_file(fp):
            en_updated += 1
        else:
            en_skipped += 1
    
    print(f"CN: {cn_updated} updated, {cn_skipped} skipped (already had or no SoftwareApplication)")
    print(f"EN: {en_updated} updated, {en_skipped} skipped")
    print(f"Total: {cn_updated + en_updated} files modified")

if __name__ == "__main__":
    main()
