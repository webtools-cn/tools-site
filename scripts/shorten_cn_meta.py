#!/usr/bin/env python3
"""Shorten CN meta descriptions >160 chars to 120-160 range."""
import os, re

fixed = 0
for d in sorted(os.listdir('.')):
    if d in ('en', '.git', 'css', 'js', 'scripts', 'quality', '.gsc-data', 'node_modules'):
        continue
    f = os.path.join(d, 'index.html')
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
    
    # Split by Chinese period 。and keep first few sentences
    sentences = desc.split('。')
    new_desc = ''
    for i, s in enumerate(sentences):
        if not s:
            continue
        candidate = (new_desc + '。' + s) if new_desc else s
        if len(candidate) <= 158:
            new_desc = candidate
        else:
            if len(new_desc) >= 120:
                break
            # Try to fit truncated
            remaining = 158 - len(new_desc) - 1
            if remaining > 15:
                new_desc = new_desc + '。' + s[:remaining]
            break
    
    if not new_desc or len(new_desc) < 120:
        new_desc = desc[:157]
    
    # Add trailing period
    if not new_desc.endswith('。') and not new_desc.endswith('...'):
        new_desc = new_desc.rstrip('，；：、 ') + '。'
    
    new_ln = len(new_desc)
    if 120 <= new_ln <= 160:
        new_html = html[:m.start(2)] + new_desc + html[m.end(2):]
        with open(f, 'w', encoding='utf-8') as fw:
            fw.write(new_html)
        fixed += 1
        print(f'{new_ln} {d}: {new_desc[:80]}...')
    else:
        print(f'ERROR {new_ln} {d}: {new_desc[:80]}...')

print(f'\nFixed: {fixed}')
