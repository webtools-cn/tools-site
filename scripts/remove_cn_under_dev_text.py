#!/usr/bin/env python3
"""Remove '本工具正在完善中' placeholder sections from CN tool pages.

Same issue as EN pages - these pages have actual functional code but
contain a misleading 'under development' message that hurts SEO.
"""

import os
import re
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# The placeholder paragraph to remove
PLACEHOLDER_P = re.compile(
    r'\s*<p[^>]*>本工具正在完善中，更多功能即将上线。感谢您的耐心等待。</p>',
    re.IGNORECASE
)

# Also remove the empty tool-section that contained it
# Pattern: <div class="tool-section">\n    <h2>❓ 常见问题</h2>\n    [placeholder removed]\n  </div>
TOOL_SECTION_PATTERN = re.compile(
    r'\s*<div class="tool-section">\s*'
    r'<h2>❓\s*常见问题</h2>\s*'
    r'</div>',
    re.IGNORECASE
)

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # First remove the placeholder paragraph
    content = PLACEHOLDER_P.sub('', content)
    
    # Then remove the now-empty tool-section (only has FAQ heading, no content)
    content = TOOL_SECTION_PATTERN.sub('', content)
    
    if content == original:
        return False
    
    # Verify div balance didn't get worse
    orig_diff = original.count('<div') - original.count('</div>')
    new_diff = content.count('<div') - content.count('</div>')
    
    if new_diff != orig_diff:
        # The removal might have affected div balance - check if we removed divs
        # If we removed a tool-section div+close, that's fine (diff stays same)
        # If there was an extra </div> on the placeholder line, diff changes
        print(f"  Note: div diff changed {orig_diff} -> {new_diff}")
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

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
    skipped = 0
    
    for tool in tools:
        filepath = os.path.join(BASE, tool, 'index.html')
        if not os.path.exists(filepath):
            print(f"SKIP: {filepath} not found")
            skipped += 1
            continue
        
        if fix_file(filepath):
            fixed += 1
            print(f"FIXED: {tool}/index.html")
        else:
            # Check if already fixed
            with open(filepath, 'r') as f:
                if '本工具正在完善中' in f.read():
                    print(f"STILL HAS: {tool}/index.html (pattern not matched)")
                else:
                    print(f"ALREADY CLEAN: {tool}/index.html")
    
    # Also check online-pdf-editor which had slightly different text
    filepath = os.path.join(BASE, 'online-pdf-editor', 'index.html')
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            content = f.read()
        if '更强大的PDF编辑功能即将上线' in content:
            # This one is different - it's a notice about a lightweight version
            # Keep it as it provides useful context to users
            print(f"INFO: online-pdf-editor has different notice (lightweight version) - keeping")
    
    print(f"\n=== Summary ===")
    print(f"Fixed: {fixed}")
    print(f"Skipped: {skipped}")
    
    # Verify no remaining
    remaining = 0
    for tool in tools:
        filepath = os.path.join(BASE, tool, 'index.html')
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                if '本工具正在完善中' in f.read():
                    remaining += 1
                    print(f"  STILL HAS: {tool}/index.html")
    
    print(f"Remaining '本工具正在完善中': {remaining}")

if __name__ == '__main__':
    main()
