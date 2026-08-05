#!/usr/bin/env python3
"""Static analysis of tool pages for common runtime bugs."""
import re
import sys

def check_tool(filepath, name):
    print(f"=== {name} ===")
    with open(filepath) as f:
        html = f.read()

    # Extract non-JSON-LD scripts
    all_tags = list(re.finditer(r'<script[^>]*>', html))
    all_content = re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL)
    js_code = ''
    for i, tag in enumerate(all_tags):
        if 'application/ld+json' not in tag.group():
            js_code += all_content[i] + '\n'

    issues = []

    # Check function definitions
    func_defs = set(re.findall(r'function\s+(\w+)\s*\(', js_code))
    func_defs |= set(re.findall(r'(?:const|let|var)\s+(\w+)\s*=\s*function', js_code))
    func_defs |= set(re.findall(r'(?:const|let|var)\s+(\w+)\s*=\s*\([^)]*\)\s*=>', js_code))

    # Check onclick handlers
    onclicks = re.findall(r'onclick="(\w+)\(', html)
    for oc in onclicks:
        if oc not in func_defs:
            issues.append(f'  WARN: onclick references {oc}() - not found in function defs')

    # Check getElementById references
    ids_in_js = set(re.findall(r"getElementById\(['\"](\w+)['\"]\)", js_code))
    ids_in_html = set(re.findall(r'id="(\w+)"', html))
    ids_in_html |= set(re.findall(r"id='(\w+)'", html))
    missing_ids = ids_in_js - ids_in_html
    if missing_ids:
        issues.append(f'  WARN: JS references IDs not in HTML: {missing_ids}')

    # Check for querySelector references
    qs_ids = re.findall(r"querySelector\(['\"]#(\w+)['\"]\)", js_code)
    for qid in qs_ids:
        if qid not in ids_in_html:
            issues.append(f'  WARN: querySelector #{qid} not in HTML')

    # Check for common runtime errors
    if 'undefined' in js_code and 'typeof' not in js_code:
        # Look for direct access patterns that might cause errors
        pass

    # Check for addEventListener on missing elements
    listeners = re.findall(r"getElementById\(['\"](\w+)['\"]\)\.addEventListener", js_code)
    for lid in listeners:
        if lid not in ids_in_html:
            issues.append(f'  WARN: addEventListener on missing ID: {lid}')

    # Check dark theme
    has_bg = '#0f172a' in html
    has_card = '#1e293b' in html
    if not has_bg:
        issues.append('  WARN: Missing --bg #0f172a')
    if not has_card:
        issues.append('  WARN: Missing --card-bg #1e293b')

    # Check for light backgrounds used as page/card bg (not text color)
    # Look for background: #fff patterns
    light_bgs = re.findall(r'background\s*:\s*(#fff|#ffffff|#f8fafc|#f8f9fa)\b', html, re.IGNORECASE)
    if light_bgs:
        issues.append(f'  WARN: Light background found: {light_bgs[:3]}')

    if not issues:
        print("  Static check: OK")
    else:
        for issue in issues:
            print(issue)
    return len(issues)

if __name__ == '__main__':
    tools = sys.argv[1:] if len(sys.argv) > 1 else [
        'keyboard-shortcut-visualizer',
        'flexbox-playground',
        'land-transfer-tax-calculator',
        'decimal-to-octal',
        'emergency-fund-calculator',
        'css-shape-generator',
        'vacation-budget',
    ]
    total_issues = 0
    for t in tools:
        total_issues += check_tool(f'{t}/index.html', t)
        # Also check EN
        total_issues += check_tool(f'en/{t}/index.html', f'{t} (EN)')
    print(f"\nTotal issues: {total_issues}")
