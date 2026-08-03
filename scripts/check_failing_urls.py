#!/usr/bin/env python3
"""Check failing URLs for common SEO/functional issues."""
import re
import os

failing_urls = [
    'tax-calculator', 'checksum-calculator', 'business-days-calculator',
    'mac-address-lookup', 'vin-decoder', 'unicode-lookup', 'token-estimator',
    'sql-explainer', 'reaction-test', 'gpa-calculator', 'compound-interest-calculator',
    'running-pace-calculator', 'metronome-online', 'speed-test', 'wifi-password-generator',
]

for url in failing_urls:
    f = f'{url}/index.html'
    if not os.path.exists(f):
        continue
    with open(f) as fh:
        html = fh.read()
    
    issues = []
    
    # 1. Placeholder content
    if 'Coming soon' in html or 'coming soon' in html or '敬请期待' in html:
        issues.append('placeholder_content')
    
    # 2. Broken onclick handlers
    onclicks = re.findall(r'onclick="(\w+)\(', html)
    scripts = ' '.join(re.findall(r'<script>(.*?)</script>', html, re.DOTALL))
    for func in onclicks:
        if f'function {func}' not in scripts and f'{func} =' not in scripts:
            issues.append(f'broken_onclick:{func}')
    
    # 3. Uncaught throws
    if 'throw new Error' in scripts and 'catch' not in scripts:
        issues.append('uncaught_throw')
    
    # 4. Missing element IDs referenced in JS
    elem_ids = set(re.findall(r'id="([^"]+)"', html))
    js_id_pattern = r"getElementById\(['\"]([^'\"]+)['\"]\)"
    js_ids = set(re.findall(js_id_pattern, scripts))
    missing_ids = js_ids - elem_ids
    if missing_ids:
        issues.append(f'missing_elements:{missing_ids}')
    
    # 5. Meta description length
    desc = re.search(r'meta name="description" content="([^"]+)"', html)
    if desc:
        dlen = len(desc.group(1))
        if dlen < 120:
            issues.append(f'short_desc:{dlen}')
    
    # 6. Dark theme
    if '#0f172a' not in html and '--bg' not in html:
        issues.append('missing_dark_theme')
    
    # 7. Check for querySelector with missing elements
    qs_selectors = re.findall(r"querySelector\(['\"]([^'\"]+)['\"]\)", scripts)
    for sel in qs_selectors:
        if sel.startswith('#'):
            sid = sel[1:]
            if sid not in elem_ids:
                issues.append(f'missing_qs:{sel}')
    
    if issues:
        print(f'WARNING  {url}: {issues}')
    else:
        print(f'OK  {url}: no issues found')
