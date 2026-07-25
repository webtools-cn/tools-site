#!/usr/bin/env python3
"""Batch generate EN versions for 16 tools missing English pages."""
import os, re, shutil

BASE = '/home/chison/tools-site'

tools = [
    ('stakeholder-map', 'Stakeholder Map', 'Stakeholder Analysis Matrix',
     'Free online stakeholder analysis tool. Create stakeholder matrix by influence and interest. Export PNG. No registration required.',
     'Stakeholder Map', 'business'),
    ('markdown-table-formatter', 'Markdown Table Formatter', 'Format & Beautify Markdown Tables',
     'Free online Markdown table formatter. Auto-align columns, CSV/Markdown conversion, table beautification. Pure client-side, no registration.',
     'Markdown Table Formatter', 'dev'),
    ('image-brightness', 'Image Brightness Adjuster', 'Adjust Image Brightness Online',
     'Online image brightness adjustment tool. Drag & drop upload, slider control, download result. Pure browser-side processing.',
     'Image Brightness Adjuster', 'image'),
    ('image-hue-rotate', 'Image Hue Rotator', 'Rotate Image Hue Online',
     'Online image hue rotation tool. Upload image, rotate hue 0-360°, create artistic effects. Pure browser-side processing.',
     'Image Hue Rotator', 'image'),
    ('saturation-adjuster', 'Image Saturation Adjuster', 'Adjust Image Saturation Online',
     'Online image saturation adjustment tool. Upload, adjust from grayscale to vivid. Slider control, download result.',
     'Image Saturation Adjuster', 'image'),
    ('fertilizer-calculator', 'Fertilizer Calculator', 'Garden Fertilizer Dosage Calculator',
     'Online fertilizer dosage calculator. Calculate NPK amounts, application rates per acre/m²/ft². Free, no registration.',
     'Fertilizer Calculator', 'life'),
    ('seed-spacing-calculator', 'Seed Spacing Calculator', 'Garden Seed Spacing Planner',
     'Online seed spacing calculator. Calculate rows, plants per row, total seeds needed. Supports sq ft and acres.',
     'Seed Spacing Calculator', 'life'),
    ('wire-gauge-calculator', 'AWG Wire Gauge Calculator', 'Wire Gauge & Current Capacity Calculator',
     'Free online AWG wire gauge calculator. Calculate cross-section, resistance, and max current capacity. Essential for electricians and engineers.',
     'AWG Wire Gauge Calculator', 'dev'),
    ('ping-tester', 'Ping Tester', 'Website Latency & Response Time Tester',
     'Free online ping test tool. Measure website response time and latency. HTTP request timing, multiple tests, average calculation. No installation needed.',
     'Ping Tester', 'dev'),
    ('emoji-reaction-generator', 'Emoji Reaction Generator', 'Create Custom Emoji Reactions',
     'Free online emoji reaction generator. Create custom emoji reactions with text. Support popular social platform formats. No registration.',
     'Emoji Reaction Generator', 'text'),
    ('lens-focal-length-calculator', 'Lens Focal Length Calculator', 'Equivalent Focal Length & Angle of View',
     'Free online lens focal length calculator. Calculate 35mm equivalent focal length, horizontal/vertical/diagonal angle of view. Supports major camera sensors.',
     'Lens Focal Length Calculator', 'life'),
    ('api-response-time-tester', 'API Response Time Tester', 'API Performance Testing Tool',
     'Free online API response time tester. Batch test multiple endpoints, concurrent requests, latency analysis, export CSV report. Pure client-side.',
     'API Response Time Tester', 'dev'),
    ('luggage-weight-limit-checker', 'Luggage Weight Limit Checker', 'Airline Baggage Weight Checker',
     'Free online luggage weight checker. Check against major airline carry-on and checked baggage limits. Calculate excess fees. Essential travel tool.',
     'Luggage Weight Limit Checker', 'life'),
    ('dday-counter', 'D-Day Counter', 'Countdown to Important Dates',
     'Online D-Day countdown calculator. Calculate days until important dates. Support countdown and count-up modes. Real-time second-level updates.',
     'D-Day Counter', 'life'),
    ('battery-life-calculator', 'Battery Life Calculator', 'Estimate Device Battery Runtime',
     'Free online battery life calculator. Estimate runtime from battery capacity (mAh), voltage, and device power consumption. Wh/W unit conversion.',
     'Battery Life Calculator', 'life'),
    ('image-contrast', 'Image Contrast Adjuster', 'Adjust Image Contrast Online',
     'Online image contrast adjustment tool. Upload, adjust contrast with slider. Download results. Pure browser-side processing.',
     'Image Contrast Adjuster', 'image'),
]

generated = []
for tool, en_title, og_title, en_desc, en_h1_clean, cat in tools:
    cn_path = f'{BASE}/{tool}/index.html'
    en_dir = f'{BASE}/en/{tool}'
    en_path = f'{en_dir}/index.html'
    
    if not os.path.exists(cn_path):
        print(f'SKIP {tool}: CN file not found')
        continue
    
    with open(cn_path) as f:
        html = f.read()
    
    # Replace lang
    html = html.replace('<html lang="zh-CN">', '<html lang="en">')
    
    # Replace title
    html = re.sub(r'<title>.*?</title>', f'<title>{en_title} - Free ToolBase</title>', html, count=1)
    
    # Replace meta description
    html = re.sub(
        r'<meta name="description" content="[^"]*"',
        f'<meta name="description" content="{en_desc}"',
        html, count=1
    )
    
    # Replace OG title
    html = re.sub(
        r'<meta property="og:title" content="[^"]*"',
        f'<meta property="og:title" content="{og_title} - Free ToolBase"',
        html, count=1
    )
    
    # Replace OG description
    html = re.sub(
        r'<meta property="og:description" content="[^"]*"',
        f'<meta property="og:description" content="{en_desc}"',
        html, count=1
    )
    
    # Replace OG URL
    html = re.sub(
        r'<meta property="og:url" content="https://free-toolbase\.com/[^"]*"',
        f'<meta property="og:url" content="https://free-toolbase.com/en/{tool}/"',
        html, count=1
    )
    
    # Replace canonical
    html = re.sub(
        r'<link rel="canonical" href="https://free-toolbase\.com/[^"]*"',
        f'<link rel="canonical" href="https://free-toolbase.com/en/{tool}/"',
        html, count=1
    )
    
    # Replace hreflang - swap en and zh
    html = re.sub(
        r'<link rel="alternate" hreflang="en" href="https://free-toolbase\.com/[^"]*"',
        f'<link rel="alternate" hreflang="en" href="https://free-toolbase.com/en/{tool}/"',
        html
    )
    html = re.sub(
        r'<link rel="alternate" hreflang="zh" href="https://free-toolbase\.com/[^"]*"',
        f'<link rel="alternate" hreflang="zh" href="https://free-toolbase.com/{tool}/"',
        html
    )
    html = re.sub(
        r'<link rel="alternate" hreflang="x-default" href="https://free-toolbase\.com/[^"]*"',
        f'<link rel="alternate" hreflang="x-default" href="https://free-toolbase.com/en/{tool}/"',
        html
    )
    
    # Replace Schema name/description/url
    html = re.sub(
        r'"name":\s*"[^"]*"',
        f'"name": "{en_title}"',
        html, count=1
    )
    html = re.sub(
        r'"description":\s*"[^"]*"',
        f'"description": "{en_desc}"',
        html, count=1
    )
    html = re.sub(
        r'"url":\s*"https://free-toolbase\.com/[^"]*"',
        f'"url": "https://free-toolbase.com/en/{tool}/"',
        html, count=1
    )
    
    # Replace h1 content (keep the span if present)
    html = re.sub(
        r'<h1[^>]*>.*?</h1>',
        f'<h1>{en_h1_clean}</h1>',
        html, count=1
    )
    
    # Remove emoji from h1 if any
    html = re.sub(r'<h1>[\u2600-\u27BF\uD83C-\uDBFF\uDC00-\uDFFF]+', '<h1>', html)
    
    os.makedirs(en_dir, exist_ok=True)
    with open(en_path, 'w') as f:
        f.write(html)
    
    generated.append(tool)
    print(f'OK {tool}')

print(f'\nGenerated {len(generated)} EN pages:')
for g in generated:
    print(f'  en/{g}/index.html')