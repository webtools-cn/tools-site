#!/usr/bin/env python3
"""Update sitemap.xml with new tools"""
from datetime import date
import re

filepath = '/home/chison/tools-site/sitemap.xml'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

today = date.today().strftime('%Y-%m-%d')

new_slugs = [
    'max-drawdown-calculator',
    'treynor-ratio-calculator',
    'information-ratio-calculator',
    'kidney-function-calculator',
    'iron-deficiency-calculator',
]

new_entries = ''
for slug in new_slugs:
    for prefix in ['', 'en/']:
        new_entries += f'''  <url>
    <loc>https://free-toolbase.com/{prefix}{slug}/</loc>
    <lastmod>{today}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
'''

# Insert before closing </urlset>
content = content.replace('</urlset>', new_entries + '</urlset>')

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print(f'Sitemap updated with {len(new_slugs)*2} new URLs')