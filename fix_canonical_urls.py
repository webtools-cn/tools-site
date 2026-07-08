#!/usr/bin/env python3
"""Fix all canonical and og:url URLs that are missing /tools-site/ path prefix."""
import os
import re

SITE = "/opt/project"
DOMAIN = "https://webtools-cn.github.io"

def fix_file(filepath):
    """Fix canonical and og:url in a single HTML file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    changes = []
    
    # Fix canonical URL - pattern: href="https://webtools-cn.github.io/XXX/" (missing /tools-site/)
    # Need to add /tools-site/ after the domain
    # CN version: https://webtools-cn.github.io/tool-name/ -> https://webtools-cn.github.io/tools-site/tool-name/
    # EN version: https://webtools-cn.github.io/en/tool-name/ -> https://webtools-cn.github.io/tools-site/en/tool-name/
    
    # Fix rel="canonical" href
    content, count1 = re.subn(
        r'(rel="canonical"\s+href="https://webtools-cn\.github\.io)(?!/tools-site/)(/[^"]*/")',
        r'\1/tools-site\2',
        content
    )
    if count1 > 0:
        changes.append(f"canonical: {count1}")
    
    # Fix og:url
    content, count2 = re.subn(
        r'(property="og:url"\s+content="https://webtools-cn\.github\.io)(?!/tools-site/)(/[^"]*/")',
        r'\1/tools-site\2',
        content
    )
    if count2 > 0:
        changes.append(f"og:url: {count2}")
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True, changes
    return False, []

def main():
    fixed = 0
    errors = []
    
    # Walk through all index.html files
    for root, dirs, files in os.walk(SITE):
        # Skip hidden directories and .git
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ('libs', 'chrome-extension', 'quality-reports', '__pycache__')]
        
        if 'index.html' in files:
            filepath = os.path.join(root, 'index.html')
            success, changes = fix_file(filepath)
            if success:
                relpath = os.path.relpath(filepath, SITE)
                fixed += 1
                if fixed <= 10:
                    print(f"  FIXED: {relpath} - {', '.join(changes)}")
    
    print(f"\nTotal files fixed: {fixed}")

if __name__ == '__main__':
    main()
