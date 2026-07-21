#!/usr/bin/env python3
"""
Fix common JS syntax errors in tool index.html files.
This script handles the most common patterns:
1. </script> inside JS strings (breaks HTML parsing)
2. HTML tags inside script blocks
3. Various JS syntax errors
"""
import re
import os

os.chdir('/home/chison/tools-site')

def fix_html_script_tags(content):
    """Replace </script> inside JS strings with <\/script> or string concatenation."""
    # Find all <script> blocks (not type="application/ld+json")
    # We need to be careful - only fix </script> that appears INSIDE a JS string
    lines = content.split('\n')
    in_script = False
    result = []
    
    for i, line in enumerate(lines):
        # Track script blocks
        if re.search(r'<script(?![^>]*type=["\']application/ld\+json["\'])[^>]*>', line) and not re.search(r'</script>', line):
            in_script = True
        if re.search(r'</script>', line) and in_script:
            in_script = False
        
        result.append(line)
    
    return '\n'.join(result)

# Let me take a different approach - fix each tool individually
# based on the specific error

def read_file(path):
    with open(path, 'r') as f:
        return f.read()

def write_file(path, content):
    with open(path, 'w') as f:
        f.write(content)

# Tool-specific fixes
fixes = {}

# 1. pdf-to-html: </script> inside JS string breaks parsing
# The push string spans multiple lines and contains </script>
content = read_file('pdf-to-html/index.html')
# Replace the multi-line htmlParts.push that contains </script>
# First, find the problematic section
old = """htmlParts.push('<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>'+fileName+' - PDF转HTML</title><style>body{font-family:sans-serif;line-height:1.6;max-width:800px;margin:0 auto;padding:20px;color:#e2e8f0}h1,h2,h3{color:#222}p{margin:0 0 1em 0}.page-marker{background:#f0f0f0;padding:4px 8px;font-size:.8rem;color:#94a3b8;margin:16px 0 8px 0;border-radius:4px}</style>
<script type="application/ld+json">{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "首页",
      "item": "https://free-toolbase.com/"
    },
    {
      "@type": "ListItem",
      "position": 2,
      "name": "PDF工具",
      "item": "https://free-toolbase.com/#pdf-tools"
    },
    {
      "@type": "ListItem",
      "position": 3,
      "name": "PDF转HTML",
      "item": "https://free-toolbase.com/pdf-to-html/"
    }
  ],
  "name": "PDF转HTML"
}</script>
</head><body>');"""

new = """htmlParts.push('<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>'+fileName+' - PDF转HTML</title><style>body{font-family:sans-serif;line-height:1.6;max-width:800px;margin:0 auto;padding:20px;color:#e2e8f0}h1,h2,h3{color:#222}p{margin:0 0 1em 0}.page-marker{background:#f0f0f0;padding:4px 8px;font-size:.8rem;color:#94a3b8;margin:16px 0 8px 0;border-radius:4px}</style><scr'+'ipt type="application/ld+json">{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"首页","item":"https://free-toolbase.com/"},{"@type":"ListItem","position":2,"name":"PDF工具","item":"https://free-toolbase.com/#pdf-tools"},{"@type":"ListItem","position":3,"name":"PDF转HTML","item":"https://free-toolbase.com/pdf-to-html/"}],"name":"PDF转HTML"}</scr'+'ipt></head><body>');"""

if old in content:
    content = content.replace(old, new)
    # Also fix the other </script> inside strings
    # The processPage function also has </script> in strings
    content = content.replace('<script src="https://free-toolbase.com/related-tools.js"></script>', "<scr'+'ipt src=\"https://free-toolbase.com/related-tools.js\"></scr'+'ipt>")
    write_file('pdf-to-html/index.html', content)
    print("Fixed pdf-to-html")
else:
    print("WARNING: Could not find pattern in pdf-to-html")
