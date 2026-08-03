#!/usr/bin/env python3
"""Fix nested h2 tags in related-tools sections across all tool pages.

The pattern is:
<section class="related-tools" ...><h2 style="...color:#374151;">🔗 <h2 style="color:#e2e8f0;...">🔗 相关工具推荐</h2>

Should be:
<section class="related-tools" ...><h2 style="color:#e2e8f0;...">🔗 相关工具推荐</h2>
"""

import os
import re
import glob

OLD_PATTERN = r'<h2 style="font-size:1\.1rem;margin-bottom:0\.5rem;color:#374151;">🔗 <h2 style="color:#e2e8f0;font-size:18px;margin-bottom:12px">🔗 相关工具推荐</h2>'
NEW_TEXT = '<h2 style="color:#e2e8f0;font-size:18px;margin-bottom:12px">🔗 相关工具推荐</h2>'

# Also fix English variant if exists
OLD_PATTERN_EN = r'<h2 style="font-size:1\.1rem;margin-bottom:0\.5rem;color:#374151;">🔗 <h2 style="color:#e2e8f0;font-size:18px;margin-bottom:12px">🔗 Related Tools</h2>'
NEW_TEXT_EN = '<h2 style="color:#e2e8f0;font-size:18px;margin-bottom:12px">🔗 Related Tools</h2>'

fixed = 0
checked = 0

for html_file in glob.glob('**/index.html', recursive=True):
    checked += 1
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    content = re.sub(OLD_PATTERN, NEW_TEXT, content)
    content = re.sub(OLD_PATTERN_EN, NEW_TEXT_EN, content)
    
    if content != original:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        fixed += 1
        print(f"Fixed: {html_file}")

print(f"\nChecked: {checked}, Fixed: {fixed}")
