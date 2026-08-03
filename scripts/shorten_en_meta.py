#!/usr/bin/env python3
"""Batch shorten EN meta descriptions from >160 to 120-160 chars.
Strategy: intelligently truncate at sentence boundary, keep first 1-2 sentences."""
import os, re

en_dir = 'en'
fixed = 0
errors = 0

for d in sorted(os.listdir(en_dir)):
    f = os.path.join(en_dir, d, 'index.html')
    if not os.path.isfile(f):
        continue
    html = open(f, encoding='utf-8', errors='ignore').read()
    m = re.search(r'(<meta\s+name="description"\s+content=")([^"]*)(")', html)
    if not m:
        continue
    desc = m.group(2)
    ln = len(desc)
    
    if ln <= 160:
        continue
    
    # Strategy: split into sentences, keep adding until we reach 120-160
    # Sentences split by '. ' 
    sentences = desc.split('. ')
    new_desc = ''
    for s in sentences:
        candidate = (new_desc + '. ' + s).strip() if new_desc else s
        if len(candidate) <= 160:
            new_desc = candidate
        else:
            # If adding this sentence exceeds 160, check if we already have enough
            if len(new_desc) >= 120:
                break
            # Try to fit a truncated version
            remaining = 160 - len(new_desc) - 2  # for ". "
            if remaining > 20:
                truncated = s[:remaining-3].rstrip() + '...'
                new_desc = (new_desc + '. ' + truncated).strip()
            break
    
    if not new_desc:
        # Fallback: hard truncate at 157 + ...
        new_desc = desc[:157].rstrip() + '...'
    
    # Ensure it ends with a period or ...
    if not new_desc.endswith('.') and not new_desc.endswith('...'):
        new_desc = new_desc.rstrip(',;: ') + '.'
    
    new_ln = len(new_desc)
    if new_ln < 120:
        # Too short - use hard truncate at 157
        new_desc = desc[:157].rstrip() + '...'
        new_ln = len(new_desc)
    
    if 120 <= new_ln <= 160:
        new_html = html[:m.start(2)] + new_desc + html[m.end(2):]
        with open(f, 'w', encoding='utf-8') as fw:
            fw.write(new_html)
        fixed += 1
        if fixed <= 10 or fixed % 10 == 0:
            print(f'{new_ln} {d}: {new_desc[:80]}...')
    else:
        errors += 1
        print(f'ERROR {new_ln} {d}: {new_desc[:80]}...')

print(f'\nFixed: {fixed}, Errors: {errors}')
