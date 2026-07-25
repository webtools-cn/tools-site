#!/usr/bin/env python3
"""Add missing tool cards to EN homepage."""
import os

BASE = '/home/chison/tools-site'

EN_NEW_CARDS = [
    ('stakeholder-map', '👥', 'Stakeholder Map', 'Analyze stakeholder influence & interest, create matrix, export PNG.', 'business'),
    ('markdown-table-formatter', '📝', 'Markdown Table Formatter', 'Auto-align columns, CSV/Markdown conversion, table beautification.', 'dev'),
    ('image-brightness', '☀️', 'Image Brightness Adjuster', 'Drag & drop upload, slider to adjust brightness, download result.', 'image'),
    ('image-hue-rotate', '🌈', 'Image Hue Rotator', 'Rotate image hue 0-360°, create artistic color effects. Pure browser-side.', 'image'),
    ('saturation-adjuster', '🎨', 'Image Saturation Adjuster', 'Adjust from grayscale to vivid. Slider control, download processed result.', 'image'),
    ('fertilizer-calculator', '🌱', 'Fertilizer Calculator', 'Calculate NPK amounts, application rates per acre/m²/ft².', 'life'),
    ('seed-spacing-calculator', '🌱', 'Seed Spacing Calculator', 'Calculate rows, plants per row, total seeds needed. Sq ft & acres.', 'life'),
    ('wire-gauge-calculator', '🔌', 'AWG Wire Gauge Calculator', 'Calculate cross-section, resistance, max current capacity.', 'dev'),
    ('ping-tester', '📡', 'Ping Tester', 'Measure website response time & latency. HTTP timing, multiple tests.', 'dev'),
    ('emoji-reaction-generator', '😂', 'Emoji Reaction Generator', 'Create custom emoji reactions with text. Social platform formats.', 'text'),
    ('lens-focal-length-calculator', '📷', 'Lens Focal Length Calculator', 'Calculate 35mm equivalent focal length, horizontal/vertical/diagonal angle of view.', 'life'),
    ('api-response-time-tester', '⚡', 'API Response Time Tester', 'Batch test multiple endpoints, concurrent requests, latency analysis.', 'dev'),
    ('luggage-weight-limit-checker', '🧳', 'Luggage Weight Limit Checker', 'Check carry-on & checked baggage limits for major airlines.', 'life'),
    ('dday-counter', '📅', 'D-Day Counter', 'Count down to important dates. Countdown & count-up modes, real-time updates.', 'life'),
    ('battery-life-calculator', '🔋', 'Battery Life Calculator', 'Estimate runtime from battery capacity (mAh), voltage, and power consumption.', 'life'),
    ('image-contrast', '🎚️', 'Image Contrast Adjuster', 'Upload image, adjust contrast with slider. Download results.', 'image'),
]

# Generate cards HTML
cards_html = ''
for tool, icon, name, desc, cat in EN_NEW_CARDS:
    cards_html += f'<div class="tool-card" data-cat="{cat}"><span class="tool-icon">{icon}</span><span class="tool-name">{name}</span><span class="tool-desc">{desc}</span><a href="./{tool}/" class="btn">Use Now</a></div>\n'

# Read EN index
en_path = f'{BASE}/en/index.html'
with open(en_path) as f:
    html = f.read()

# Insert before </div></div> (closing of tools-grid and its container)
# Find the last tool-card before closing
marker = '</div></div>\n\n    <!-- FAQ Section -->'
insertion = cards_html + marker
html = html.replace(marker, insertion)

with open(en_path, 'w') as f:
    f.write(html)

print(f'Added {len(EN_NEW_CARDS)} cards to EN homepage')

# Also check if these tools appear in CN homepage
cn_path = f'{BASE}/index.html'
with open(cn_path) as f:
    cn_html = f.read()

# Count
cn_count = cn_html.count('tool-card')
en_count = html.count('tool-card')
print(f'CN cards: {cn_count}, EN cards: {en_count}')
print(f'Difference: {cn_count - en_count}')