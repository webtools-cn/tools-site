#!/usr/bin/env python3
"""Extract the last non-JSON-LD script content from an HTML file."""
import sys, re

with open(sys.argv[1], 'r') as f:
    html = f.read()

# Find all script blocks
scripts = re.findall(r'<script(?![^>]*type=["\']application/ld\+json["\'])[^>]*>(.*?)</script>', html, re.DOTALL)
if not scripts:
    print("// No script found")
    sys.exit(0)

# Get the last one
js = scripts[-1].strip()
print(js)
