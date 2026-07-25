#!/usr/bin/env python3
"""Sync EN homepage cards with CN homepage - add missing cards."""
import re, os

BASE = '/home/chison/tools-site'

with open(f'{BASE}/index.html') as f:
    cn_html = f.read()
with open(f'{BASE}/en/index.html') as f:
    en_html = f.read()

# Get CN cards with their full block
cn_cards = re.findall(r'<div class="tool-card"[^>]*>.*?</div>', cn_html, re.DOTALL)

# Parse each CN card to get tool name and data
cn_card_map = {}
for card in cn_cards:
    href_m = re.search(r'href="([a-z0-9-]+)/" class="btn"', card)
    if href_m:
        tool = href_m.group(1)
        cn_card_map[tool] = card

# Get EN tools
en_hrefs = set(re.findall(r'href="\./([a-z0-9-]+)/" class="btn"', en_html))

missing = [t for t in cn_card_map if t not in en_hrefs]
print(f"CN cards: {len(cn_card_map)}, EN cards: {len(en_hrefs)}, Missing from EN: {len(missing)}")

if missing:
    # Generate EN cards for missing tools
    new_cards_html = ''
    for tool in sorted(missing):
        cn_card = cn_card_map[tool]
        
        # Fix href from "/tool/" to "./tool/"
        en_card = re.sub(r'href="([a-z0-9-]+)/" class="btn"', r'href="./\1/" class="btn"', cn_card)
        
        # Replace Chinese text with English approximations if needed, 
        # but for now just keep as-is (the card text is already extracted, just need to fix href)
        new_cards_html += en_card + '\n'
    
    # Insert before </div></div> before FAQ
    marker = '</div></div>\n\n    <!-- FAQ Section -->'
    insertion = new_cards_html + marker
    en_html = en_html.replace(marker, insertion)
    
    with open(f'{BASE}/en/index.html', 'w') as f:
        f.write(en_html)
    
    print(f'Added {len(missing)} missing cards to EN homepage')

# Final count
cn_count = cn_html.count('tool-card')
en_count = en_html.count('tool-card') if missing else en_html.count('tool-card')
print(f'Final: CN={cn_count}, EN={en_count}')