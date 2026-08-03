#!/usr/bin/env python3
"""
Fix div imbalance in remaining 25 pages.

For diff > 0 (missing </div>): add missing </div> before </body>
For diff < 0 (extra </div>): remove extra </div> from specific locations

This script handles both cases with careful verification.
"""

import os
import re
import sys

TARGET_FILES = [
    # diff > 0 (missing </div>)
    ('en/ip-range-calculator/index.html', +14),
    ('en/loan-payoff-calculator/index.html', +12),
    ('en/sales-tax-calculator/index.html', +8),
    ('en/text-animation-generator/index.html', +6),
    ('en/readability-score/index.html', +6),
    ('en/standard-deviation-calculator/index.html', +6),
    ('en/unicode-lookup/index.html', +4),
    ('en/carbon-footprint-calculator/index.html', +2),
    ('en/reading-speed-test/index.html', +2),
    # diff < 0 (extra </div>)
    ('color-picker-hex/index.html', -12),
    ('en/html-preview/index.html', -5),
    ('barcode-reader/index.html', -4),
    ('en/schema-generator/index.html', -4),
    ('en/css-skeleton-loader-generator/index.html', -4),
    ('en/character-frequency-analyzer/index.html', -4),
    ('line-chart-maker/index.html', -4),
    ('pie-chart-maker/index.html', -4),
    ('bar-chart-maker/index.html', -4),
    ('en/diff-viewer/index.html', -2),
    ('en/seo-meta-generator/index.html', -2),
    ('en/ai-context-window-comparator/index.html', -2),
    ('en/css-to-inline-styles/index.html', -2),
    ('en/html-stripper/index.html', -2),
    ('cookie-editor/index.html', -2),
    ('matrix-calculator/index.html', -2),
]


def count_div_balance(content):
    """Count div balance, excluding script/style content."""
    clean = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL)
    clean = re.sub(r'<style[^>]*>.*?</style>', '', clean, flags=re.DOTALL)
    clean = re.sub(r'<!--.*?-->', '', clean, flags=re.DOTALL)
    open_divs = len(re.findall(r'<div[\s>]', clean))
    close_divs = len(re.findall(r'</div>', clean))
    return open_divs, close_divs


def fix_missing_close_divs(filepath, expected_diff):
    """Add missing </div> tags before </body> or before </main> if main is the last tag."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the position to insert </div> tags
    # Strategy: insert before </body> (or before <footer> if that's more appropriate)
    # But we need to be careful not to break </main>
    
    # Find </body> position
    body_close = content.rfind('</body>')
    if body_close == -1:
        return False, "No </body> found"
    
    # Check if there's a </main> before </body>
    main_close = content.rfind('</main>', 0, body_close)
    
    # Insert the missing </div> tags before </main> if it exists, otherwise before </body>
    insert_point = main_close if main_close != -1 else body_close
    
    # Build the missing </div> tags
    missing = '\n' + '\n'.join(['</div>'] * expected_diff) + '\n'
    
    fixed = content[:insert_point] + missing + content[insert_point:]
    
    # Verify
    open_d, close_d = count_div_balance(fixed)
    diff = open_d - close_d
    
    if diff != 0:
        return False, f"Still unbalanced: open={open_d} close={close_d} diff={diff}"
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(fixed)
    
    return True, f"Added {expected_diff} </div> tags"


def fix_extra_close_divs(filepath, expected_diff):
    """Remove extra </div> tags. 
    Strategy: find lines that are just '</div>' and remove them from the end of the file
    (before </body></html>), working backwards.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    abs_diff = abs(expected_diff)
    
    # Find all </div> positions in the content (excluding scripts/styles)
    # We need to find standalone </div> lines near the end of the body content
    
    # Strategy: Find the position of </main> or <footer> (whichever comes first)
    # Then remove extra </div> tags between the last content and that point
    
    # Find <footer> position
    footer_pos = content.find('<footer>')
    # Find </main> position  
    main_close_pos = content.find('</main>')
    
    # The extra </div>s are likely between the content and footer/main close
    # Let's find the region just before footer or </main>
    end_region = min(
        p for p in [footer_pos, main_close_pos] if p != -1
    ) if any(p != -1 for p in [footer_pos, main_close_pos]) else content.rfind('</body>')
    
    # Look backwards from end_region for standalone </div> lines
    before_end = content[:end_region]
    
    # Find lines that are just '</div>' (with optional whitespace)
    lines = before_end.split('\n')
    
    # Collect indices of standalone </div> lines, from the end
    standalone_indices = []
    for i in range(len(lines) - 1, -1, -1):
        if lines[i].strip() == '</div>':
            standalone_indices.append(i)
        if len(standalone_indices) >= abs_diff:
            break
    
    if len(standalone_indices) < abs_diff:
        # Try a different approach: find any </div> that can be removed
        # Look for lines where </div> appears multiple times
        return False, f"Could not find {abs_diff} standalone </div> lines to remove (found {len(standalone_indices)})"
    
    # Remove the last N standalone </div> lines
    indices_to_remove = set(standalone_indices[:abs_diff])
    new_lines = [line for i, line in enumerate(lines) if i not in indices_to_remove]
    
    fixed = '\n'.join(new_lines) + content[end_region:]
    
    # Verify
    open_d, close_d = count_div_balance(fixed)
    diff = open_d - close_d
    
    if diff != 0:
        return False, f"Still unbalanced: open={open_d} close={close_d} diff={diff}"
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(fixed)
    
    return True, f"Removed {abs_diff} extra </div> tags"


def main():
    os.chdir('/home/chison/tools-site')
    
    fixed_count = 0
    failed_count = 0
    
    for filepath, expected_diff in TARGET_FILES:
        if not os.path.exists(filepath):
            print(f"SKIP (not found): {filepath}")
            continue
        
        if expected_diff > 0:
            success, msg = fix_missing_close_divs(filepath, expected_diff)
        else:
            success, msg = fix_extra_close_divs(filepath, expected_diff)
        
        if success:
            print(f"OK: {filepath} — {msg}")
            fixed_count += 1
        else:
            print(f"FAIL: {filepath} — {msg}")
            failed_count += 1
    
    print(f"\nSummary: {fixed_count} fixed, {failed_count} failed")


if __name__ == '__main__':
    main()
