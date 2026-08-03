#!/usr/bin/env python3
"""Remove 'under active development' placeholder sections from EN tool pages.

These pages have actual functional code but contain a misleading
'This tool is under active development' message in a tool-section div
that only has a FAQ heading with no content. This hurts SEO as Google
sees the page as incomplete/low-quality.
"""

import os
import re
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Pattern: <div class="tool-section">\n    <h2>❓ FAQ</h2>\n    <p ...>...under active development...</p>\n  </div>
PATTERN = re.compile(
    r'\s*<div class="tool-section">\s*'
    r'<h2>❓\s*FAQ</h2>\s*'
    r'<p[^>]*>This tool is under active development[^<]*</p>\s*'
    r'</div>',
    re.IGNORECASE
)

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    matches = PATTERN.findall(content)
    if not matches:
        return False, 0
    
    new_content = PATTERN.sub('', content)
    
    # Verify we didn't break anything - check div balance
    open_divs = new_content.count('<div')
    close_divs = new_content.count('</div>')
    diff = open_divs - close_divs
    
    if abs(diff) > 3:
        print(f"  WARNING: div imbalance after fix: {diff} (was {content.count('<div') - content.count('</div')})")
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return True, len(matches)

def main():
    tools = [
        'ai-sentence-rewriter', 'audio-normalize', 'audio-volume-adjuster',
        'bitwise-calculator', 'color-palette-from-image', 'crossword-generator',
        'csv-sorter', 'gif-to-webp', 'graphql-to-json', 'html-to-react',
        'image-round-corners', 'json-to-protobuf', 'mesh-gradient-generator',
        'pdf-page-numbers', 'protobuf-to-json', 'svg-to-base64',
        'text-progress-bar-generator', 'tiff-to-jpg', 'webp-to-gif',
        'xml-to-yaml', 'yaml-to-xml',
    ]
    
    fixed = 0
    errors = 0
    
    for tool in tools:
        filepath = os.path.join(BASE, 'en', tool, 'index.html')
        if not os.path.exists(filepath):
            print(f"SKIP: {filepath} not found")
            continue
        
        success, count = fix_file(filepath)
        if success:
            fixed += 1
            print(f"FIXED: en/{tool}/index.html ({count} section removed)")
        else:
            errors += 1
            print(f"NO MATCH: en/{tool}/index.html")
    
    print(f"\n=== Summary ===")
    print(f"Fixed: {fixed}/{len(tools)}")
    print(f"No match: {errors}/{len(tools)}")
    
    # Verify no remaining
    remaining = 0
    for tool in tools:
        filepath = os.path.join(BASE, 'en', tool, 'index.html')
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                if 'under active development' in f.read():
                    remaining += 1
                    print(f"  STILL HAS: en/{tool}/index.html")
    
    print(f"Remaining 'under active development': {remaining}")

if __name__ == '__main__':
    main()
