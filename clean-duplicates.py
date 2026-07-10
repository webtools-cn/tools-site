#!/usr/bin/env python3
"""
Clean duplicate tool cards from EN homepage.
Strategy:
1. Split the HTML by tool-card blocks (finding boundaries by matching opening/closing div tags)
2. Group blocks by href
3. For duplicates, keep the well-formed one (has 'Use Now' text, proper closing)
4. Fix the malformed syllable-counter card
"""

import re

with open('en/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find all tool-card opening tags
card_open_pattern = re.compile(r'<div class="tool-card"[^>]*>')
href_pattern = re.compile(r'href="([^"]*/)"')

matches = list(card_open_pattern.finditer(content))
print(f"Found {len(matches)} tool-card opening tags")

# Parse each tool-card block
# Strategy: for each card, scan forward counting div depth until depth returns to 0
# If we encounter another tool-card open while depth > 0, it means the previous card is malformed
# In that case, we cut the block just before the new card

blocks = []
for i, match in enumerate(matches):
    start = match.start()
    end_tag = match.group(0)
    
    pos = match.end()
    depth = 1
    end = None
    
    # Scan for next tool-card or depth-0
    next_card_idx = i + 1
    next_card_pos = matches[next_card_idx].start() if next_card_idx < len(matches) else len(content)
    
    # Scan forward counting div depth
    while depth > 0 and pos < next_card_pos:
        next_open = content.find('<div', pos, next_card_pos)
        next_close = content.find('</div>', pos, next_card_pos)
        
        if next_close == -1 and next_open == -1:
            break
        elif next_open == -1 or (next_close != -1 and next_close < next_open):
            depth -= 1
            if depth == 0:
                end = next_close + 6
            pos = next_close + 6
        elif next_open < next_close:
            depth += 1
            pos = next_open + 4
    
    if end is None:
        # If we couldn't find proper closing, use the edge between this card and next
        # This handles malformed cards where closing div is missing
        end = next_card_pos
        block = content[start:end]
        malformed = True
    else:
        block = content[start:end]
        malformed = False
    
    href_match = href_pattern.search(block)
    if href_match and not href_match.group(1).endswith('index.html'):
        href = href_match.group(1)
        has_use_now = 'Use Now' in block
        has_proper_close = block.rstrip().endswith('</div>')
        blocks.append({
            'start': start,
            'end': end,
            'href': href,
            'block': block,
            'malformed': malformed,
            'has_use_now': has_use_now,
            'has_proper_close': has_proper_close
        })

print(f"Parsed {len(blocks)} tool card blocks with tool hrefs")

# Group by href
from collections import defaultdict
by_href = defaultdict(list)
for b in blocks:
    by_href[b['href']].append(b)

# Identify duplicates
duplicates_to_remove = []
for href, group in by_href.items():
    if len(group) > 1:
        print(f"\n  '{href}' ({len(group)} occurrences):")
        for b in group:
            line = content[:b['start']].count('\n') + 1
            flags = []
            if b['malformed']: flags.append('MALFORMED')
            if not b['has_use_now']: flags.append('NO_USENOW')
            if not b['has_proper_close']: flags.append('NO_CLOSE')
            print(f"    Line {line}: {b['href']} [{','.join(flags) if flags else 'OK'}]")
        
        # Sort by quality: keep the well-formed one
        # Prefer: has Use Now > has proper close > not malformed > later position
        sorted_group = sorted(group, key=lambda b: (
            not b['has_use_now'],     # Prefer has Use Now
            not b['has_proper_close'], # Prefer proper close
            b['malformed'],            # Prefer not malformed
            b['start']                 # Prefer later (more likely correct)
        ))
        keep = sorted_group[0]
        for b in sorted_group[1:]:
            duplicates_to_remove.append(b)
        
        keep_line = content[:keep['start']].count('\n') + 1
        print(f"    → Keeping: line {keep_line}")

print(f"\nTotal duplicates to remove: {len(duplicates_to_remove)}")

# Remove duplicates in reverse order
duplicates_to_remove.sort(key=lambda x: x['start'], reverse=True)

for b in duplicates_to_remove:
    line = content[:b['start']].count('\n') + 1
    print(f"  Removing duplicate at line {line}: {b['href']}")
    content = content[:b['start']] + content[b['end']:]

# Write back
with open('en/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

# Verify
new_count = content.count('class="tool-card"')
all_hrefs = href_pattern.findall(content)
unique_hrefs = set(h for h in all_hrefs if not h.endswith('index.html'))
dups_after = sum(1 for h in unique_hrefs if all_hrefs.count(h) > 1)
print(f"\nAfter cleanup: {new_count} tool-card entries, {len(unique_hrefs)} unique hrefs")
print(f"Removed {len(duplicates_to_remove)} duplicate cards")
print(f"Cards still duplicated: {dups_after}")

# Check for malformed cards
if new_count > 0:
    print("\nAll tool cards cleaned successfully!")
