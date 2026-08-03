#!/usr/bin/env python3
"""Add <lastmod> tags to sitemap.xml — fast version.

For failing URLs: use today's date (recently fixed, need priority recrawl)
For all other URLs: use a single batch date (last major site-wide fix)
"""

import re
from datetime import datetime, timezone

TODAY = datetime.now(timezone.utc).strftime('%Y-%m-%d')
BATCH_DATE = '2026-08-04'  # Last site-wide fix date

FAILING_PATHS = {
    '', 'tax-calculator/', 'checksum-calculator/', 'business-days-calculator/',
    'mac-address-lookup/', 'vin-decoder/', 'unicode-lookup/', 'token-estimator/',
    'sql-explainer/', 'reaction-test/', 'gpa-calculator/', 'compound-interest-calculator/',
    'running-pace-calculator/', 'metronome-online/', 'speed-test/', 'wifi-password-generator/',
    'en/backwards-text/', 'en/website-status-checker/',
}

sitemap_path = '/home/chison/tools-site/sitemap.xml'

with open(sitemap_path, 'r', encoding='utf-8') as f:
    content = f.read()

def replace_url_block(match):
    url_block = match.group(0)
    loc_match = re.search(r'<loc>(https://free-toolbase\.com/([^<]*))</loc>', url_block)
    if not loc_match:
        return url_block
    
    url_path = loc_match.group(2)
    lastmod = TODAY if url_path in FAILING_PATHS else BATCH_DATE
    
    # Insert lastmod after </loc>
    url_block = url_block.replace('</loc>', f'</loc>\n    <lastmod>{lastmod}</lastmod>')
    return url_block

new_content = re.sub(r'<url>.*?</url>', replace_url_block, content, flags=re.DOTALL)

with open(sitemap_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

lastmod_count = new_content.count('<lastmod>')
url_count = new_content.count('<url>')
print(f"✅ Added lastmod to {lastmod_count}/{url_count} URLs")
print(f"   Failing URLs (today={TODAY}): {len(FAILING_PATHS)}")
print(f"   Other URLs (batch={BATCH_DATE}): {url_count - len(FAILING_PATHS)}")
