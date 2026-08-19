#!/usr/bin/env python3
"""Fix missing </body></html> closing tags in tool pages."""
import os

fixed = 0

for root, dirs, files in os.walk('.'):
    if 'index.html' not in files:
        continue
    if '/en/' not in root and root.count('/') < 1:
        # Skip root level non-tool pages
        if root == '.':
            continue
    
    filepath = os.path.join(root, 'index.html')
    with open(filepath, 'r', errors='ignore') as f:
        content = f.read()
    
    if '</body>' in content and '</html>' in content:
        continue
    
    # Add missing closing tags
    additions = ''
    if '</body>' not in content:
        additions += '</body>'
    if '</html>' not in content:
        additions += '\n</html>'
    
    if additions:
        content = content.rstrip() + '\n' + additions + '\n'
        with open(filepath, 'w', errors='ignore') as f:
            f.write(content)
        fixed += 1

print(f"Fixed {fixed} pages with missing closing tags")
