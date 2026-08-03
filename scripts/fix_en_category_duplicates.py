#!/usr/bin/env python3
"""
Fix English category pages with duplicated content blocks.

Problem: 17 English category pages (en/json, en/text, en/math, etc.) have
their FAQ + Related Categories + Footer blocks repeated 4 times, causing
div imbalance (diff=-10) and invalid HTML.

Strategy:
1. Find the first faq-section position (end of main content)
2. Find the second faq-section (first COMPLETE block with proper <footer>)
3. Keep main content + second block, discard the rest
4. Verify div balance after fix
"""

import os
import re
import sys

# The 17 English category pages with diff=-10
TARGET_PAGES = [
    'en/office/index.html',
    'en/json/index.html',
    'en/text/index.html',
    'en/math/index.html',
    'en/calc/index.html',
    'en/converter/index.html',
    'en/health/index.html',
    'en/creative/index.html',
    'en/dev/index.html',
    'en/design/index.html',
    'en/pdf/index.html',
    'en/css/index.html',
    'en/security/index.html',
    'en/fun/index.html',
    'en/image/index.html',
    'en/media/index.html',
    'en/utility/index.html',
]


def count_div_balance(content):
    """Count div balance, excluding script/style content."""
    clean = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL)
    clean = re.sub(r'<style[^>]*>.*?</style>', '', clean, flags=re.DOTALL)
    clean = re.sub(r'<!--.*?-->', '', clean, flags=re.DOTALL)
    open_divs = len(re.findall(r'<div[\s>]', clean))
    close_divs = len(re.findall(r'</div>', clean))
    return open_divs, close_divs


def fix_duplicated_blocks(filepath):
    """Fix duplicated FAQ/Related/Footer blocks in a category page."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Count faq-section occurrences
    faq_positions = [m.start() for m in re.finditer(r'<div class="faq-section">', content)]
    
    if len(faq_positions) < 2:
        return False, "No duplication found (faq-section < 2)"

    # Find the second faq-section (first COMPLETE block with proper <footer>)
    first_faq = faq_positions[0]
    second_faq = faq_positions[1]

    # Main content = everything before first faq-section
    main_content = content[:first_faq]

    # Second block = from second faq-section to second </html>
    second_html = content.find('</html>', second_faq)
    if second_html == -1:
        return False, "Could not find second </html>"
    second_html_end = second_html + len('</html>')

    # Block 2 = proper complete block with footer
    block2 = content[second_faq:second_html_end]

    # Fixed content
    fixed = main_content + block2

    # Verify
    open_d, close_d = count_div_balance(fixed)
    diff = open_d - close_d

    if diff != 0:
        return False, f"Div still unbalanced after fix: open={open_d} close={close_d} diff={diff}"

    # Verify structure
    faq_count = len(re.findall(r'<div class="faq-section">', fixed))
    footer_count = len(re.findall(r'<footer>', fixed))
    body_count = len(re.findall(r'</body>', fixed))
    html_count = len(re.findall(r'</html>', fixed))

    if faq_count != 1 or footer_count != 1 or body_count != 1 or html_count != 1:
        return False, f"Structure wrong: faq={faq_count} footer={footer_count} body={body_count} html={html_count}"

    # Write fixed content
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(fixed)

    return True, f"Fixed: removed {len(faq_positions) - 1} duplicate blocks, size {len(content)}→{len(fixed)}"


def main():
    os.chdir('/home/chison/tools-site')
    
    fixed_count = 0
    failed_count = 0
    
    for page in TARGET_PAGES:
        if not os.path.exists(page):
            print(f"SKIP (not found): {page}")
            continue
        
        success, msg = fix_duplicated_blocks(page)
        if success:
            print(f"OK: {page} — {msg}")
            fixed_count += 1
        else:
            print(f"FAIL: {page} — {msg}")
            failed_count += 1
    
    print(f"\nSummary: {fixed_count} fixed, {failed_count} failed")


if __name__ == '__main__':
    main()
