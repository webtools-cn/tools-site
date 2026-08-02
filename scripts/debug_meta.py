#!/usr/bin/env python3
import re
with open('jensen-alpha-calculator/index.html') as f:
    c = f.read()
# Try to find the meta description
for line in c.split('\n'):
    if 'description' in line.lower() and 'meta' in line.lower():
        print(repr(line.strip()[:200]))
        # Extract content
        m = re.search(r"""content=["'](.+?)["']""", line)
        if m:
            print('CONTENT LEN:', len(m.group(1)))
            print('CONTENT:', m.group(1)[:200])