#!/usr/bin/env python3
"""检查failing URLs的JS语法和HTML结构问题"""
import re
import os
import subprocess

failing_urls = [
    "tax-calculator", "checksum-calculator", "business-days-calculator",
    "mac-address-lookup", "vin-decoder", "unicode-lookup", "token-estimator",
    "sql-explainer", "reaction-test", "gpa-calculator", "compound-interest-calculator",
    "running-pace-calculator", "metronome-online", "speed-test", "wifi-password-generator",
    "en/backwards-text", "en/website-status-checker",
]

# Also check more failing URLs from the list
more_urls = [
    "image-cropper", "image-rotator", "image-compressor", "image-pixel-art",
    "pdf-to-text", "merge-pdf", "audio-recorder", "video-cropper",
    "countdown-days", "calendar-printable", "invoice-generator",
    "network-speed-test", "qr-code-reader", "file-encrypt", "file-decrypt",
    "html-to-pdf", "jpg-to-pdf", "png-to-pdf",
]

all_urls = failing_urls + more_urls

issues = []

for url in all_urls:
    fpath = f"{url}/index.html"
    if not os.path.exists(fpath):
        issues.append(f"❌ {url}: FILE NOT FOUND")
        continue
    
    with open(fpath, 'r') as f:
        content = f.read()
    
    # Check DOCTYPE
    if not content.strip().startswith('<!DOCTYPE'):
        issues.append(f"❌ {url}: Missing DOCTYPE")
    
    # Check html/head/body tags
    for tag in ['html', 'head', 'body']:
        open_count = len(re.findall(f'<{tag}[\\s>]', content))
        close_count = len(re.findall(f'</{tag}>', content))
        if open_count != close_count:
            issues.append(f"❌ {url}: <{tag}> tag mismatch: {open_count}/{close_count}")
    
    # Check div balance
    div_open = len(re.findall(r'<div[\s>]', content))
    div_close = len(re.findall(r'</div>', content))
    if div_open != div_close:
        issues.append(f"❌ {url}: div mismatch: open={div_open}, close={div_close}, diff={div_open-div_close}")
    
    # Check script tags
    script_open = len(re.findall(r'<script', content))
    script_close = len(re.findall(r'</script>', content))
    if script_open != script_close:
        issues.append(f"❌ {url}: script tag mismatch: {script_open}/{script_close}")
    
    # Check meta description
    metadesc = re.search(r'name="description" content="([^"]+)"', content)
    if not metadesc:
        issues.append(f"❌ {url}: Missing meta description")
    elif len(metadesc.group(1)) < 120:
        issues.append(f"⚠️  {url}: Meta desc too short: {len(metadesc.group(1))} chars")
    
    # Check canonical
    canonical = re.search(r'rel="canonical" href="([^"]+)"', content)
    if not canonical:
        issues.append(f"⚠️  {url}: Missing canonical URL")
    
    # Check robots
    robots = re.search(r'name="robots" content="([^"]+)"', content)
    if not robots:
        issues.append(f"⚠️  {url}: Missing robots tag")
    
    # Check Schema.org
    schemas = re.findall(r'<script type="application/ld\+json">(.*?)</script>', content, re.DOTALL)
    if not schemas:
        issues.append(f"⚠️  {url}: Missing Schema.org structured data")
    else:
        import json
        for s in schemas:
            try:
                json.loads(s.strip())
            except json.JSONDecodeError as e:
                issues.append(f"❌ {url}: Schema.org JSON error: {e}")
    
    # Check for unclosed meta tags (meta should be self-closing)
    # Check for broken HTML attributes
    if 'content="' in content:
        # Find meta tags where content value is not properly closed
        broken_meta = re.findall(r'content="[^"]*$', content, re.MULTILINE)
        if broken_meta:
            issues.append(f"❌ {url}: Unclosed content attribute in meta tag")
    
    # Check H1
    h1_count = len(re.findall(r'<h1', content))
    if h1_count == 0:
        issues.append(f"⚠️  {url}: No H1 tag")
    elif h1_count > 1:
        issues.append(f"⚠️  {url}: Multiple H1 tags: {h1_count}")
    
    # Check for JS syntax using node
    scripts = re.findall(r'<script>([\s\S]*?)</script>', content)
    for i, script_code in enumerate(scripts):
        # Skip analytics
        if 'dataLayer' in script_code or 'gtag' in script_code:
            continue
        # Write to temp file and check
        with open('/tmp/check_js.js', 'w') as tf:
            tf.write(script_code)
        result = subprocess.run(['node', '--check', '/tmp/check_js.js'], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            issues.append(f"❌ {url}: JS syntax error in script {i}: {result.stderr.strip()[:200]}")
    
    # Check page size (too small = thin content)
    if len(content) < 3000:
        issues.append(f"⚠️  {url}: Very small page ({len(content)} bytes) - thin content?")

if issues:
    print(f"\nFound {len(issues)} issues:\n")
    for issue in issues:
        print(issue)
else:
    print("\n✅ All checked URLs passed all checks!")
