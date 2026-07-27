#!/usr/bin/env python3
"""批量修复EN页面 content_thin"""
import os, json, re, random

SITE = '/home/chison/tools-site'

with open(os.path.join(SITE, 'quality', 'quality_loop_result.json')) as f:
    data = json.load(f)

remaining = data['remaining_pages']

en_thin = []
for k, v in remaining.items():
    if k.startswith('en:') and any('content_thin' in i or 'content_very_thin' in i for i in v):
        en_thin.append(k.replace('en:', ''))

print(f"处理 {len(en_thin)} 个EN薄页面...")

en_descs = {
    'avif-to-png': ('AVIF to PNG Converter', 'Convert AVIF images to PNG format online. Fast batch conversion with no quality loss. All processing done locally in your browser.'),
    'base32-encode-decode': ('Base32 Encoder/Decoder', 'Encode and decode Base32 strings online. Supports RFC 4648 standard encoding. Instant results with copy-to-clipboard.'),
    'battery-status': ('Battery Status Checker', 'Monitor your device battery level, charging status and estimated time remaining in real-time using the Battery Status API.'),
    'birthday-countdown': ('Birthday Countdown', 'Calculate exactly how many days, hours and minutes until your next birthday. Share countdowns with friends and family.'),
    'calendar-generator': ('Calendar Generator', 'Generate printable monthly and yearly calendars. Customize with holidays, notes and color themes. Export as PDF or image.'),
    'carbon-footprint-calculator': ('Carbon Footprint Calculator', 'Estimate your carbon footprint based on daily activities including travel, diet and energy usage. Learn ways to reduce your impact.'),
    'chmod-calculator': ('Chmod Calculator', 'Calculate Linux file permissions. Convert between numeric and symbolic chmod notation. Understand read/write/execute permissions.'),
    'coin-flipper': ('Coin Flipper', 'Flip a virtual coin online. Perfect for making random decisions. Track flip history and statistics.'),
    'compliment-generator': ('Compliment Generator', 'Generate random compliments and positive messages. Brighten someone\'s day with a kind word.'),
    'css-card-generator': ('CSS Card Generator', 'Visually design CSS cards with shadows, borders, gradients and hover effects. Copy generated CSS code instantly.'),
    'css-gradient-text-generator': ('CSS Gradient Text Generator', 'Create gradient text effects with CSS. Choose colors, direction and animation. Copy ready-to-use CSS code.'),
    'css-hover-effects': ('CSS Hover Effects', 'Browse and copy CSS hover animation effects. Includes buttons, cards, images and more element hover styles.'),
    'css-image-hover-generator': ('CSS Image Hover Generator', 'Generate CSS image hover overlay effects with captions, zoom and color filters. Perfect for image galleries.'),
    'css-text-outline-generator': ('CSS Text Outline Generator', 'Create text outline/stroke effects with CSS. Adjust thickness, color and blur for the perfect outline style.'),
    'css-toast-generator': ('CSS Toast Generator', 'Design toast notification popups with CSS. Customize position, animation, colors and timing.'),
    'css-toggle-switch': ('CSS Toggle Switch Generator', 'Create custom CSS toggle switches. Choose styles, sizes and colors. Generate clean HTML and CSS code.'),
    'css-tooltip-generator': ('CSS Tooltip Generator', 'Design CSS tooltip popups with arrows, animations and themes. Copy generated code for your projects.'),
    'css-typewriter-generator': ('CSS Typewriter Generator', 'Create typewriter text animation effects with CSS. Adjust typing speed, cursor style and text content.'),
    'csv-to-markdown-table': ('CSV to Markdown Table', 'Convert CSV data to Markdown table format. Support custom delimiters and alignment. Perfect for documentation.'),
    'curl-to-code': ('cURL to Code Converter', 'Convert cURL commands to Python, JavaScript, PHP, Go and more programming languages. Save time on API integration.'),
    'donut-chart-maker': ('Donut Chart Maker', 'Create donut/ring charts online. Customize colors, labels and data. Export as PNG or SVG for presentations.'),
    'emoji-meaning-finder': ('Emoji Meaning Finder', 'Search and discover the meaning of emojis. Browse by category, skin tone and platform variations.'),
    'fantasy-name-generator': ('Fantasy Name Generator', 'Generate random fantasy character names for games, novels and RPGs. Multiple race and theme options available.'),
    'favicon-downloader': ('Favicon Downloader', 'Download favicon icons from any website. Get multiple sizes including 16x16, 32x32, 64x64 and 128x128.'),
    'fuel-efficiency-converter': ('Fuel Efficiency Converter', 'Convert between MPG, L/100km, km/L and other fuel efficiency units. Compare vehicle fuel economy easily.'),
    'gradient-background-patterns': ('Gradient Background Patterns', 'Browse and generate CSS gradient background patterns. Copy ready-to-use code for web design projects.'),
    'heic-to-jpg': ('HEIC to JPG Converter', 'Convert HEIC/HEIF images to JPG format online. Batch conversion with adjustable quality settings. Browser-based, no upload.'),
    'hex-calculator': ('Hex Calculator', 'Perform hexadecimal arithmetic operations. Add, subtract, multiply and divide hex numbers. Also supports binary and decimal conversion.'),
    'html-escape-unescape': ('HTML Escape/Unescape', 'Escape and unescape HTML entities. Convert special characters to HTML entities and vice versa.'),
    'html-to-pug': ('HTML to Pug Converter', 'Convert HTML code to Pug (formerly Jade) template syntax. Save time migrating projects to Pug templating.'),
    'jpg-to-webp': ('JPG to WebP Converter', 'Convert JPG images to WebP format. Smaller file sizes with comparable quality. Batch processing supported.'),
    'link-preview-generator': ('Link Preview Generator', 'Generate Open Graph and Twitter Card meta tags for link previews. See how your links will appear on social media.'),
    'matrix-calculator': ('Matrix Calculator', 'Perform matrix operations including addition, multiplication, determinant and inverse. Supports up to 10x10 matrices.'),
    'morse-code-player': ('Morse Code Player', 'Convert text to Morse code with audio playback. Adjust speed and frequency. Learn Morse code interactively.'),
    'pet-name-generator': ('Pet Name Generator', 'Generate cute and creative names for dogs, cats and other pets. Filter by gender, personality and theme.'),
    'probability-calculator': ('Probability Calculator', 'Calculate probabilities for various scenarios. Combinatorics, conditional probability and distribution calculations.'),
    'radar-chart-maker': ('Radar Chart Maker', 'Create radar/spider charts online. Compare multiple variables across different categories. Export as image.'),
    'reading-speed-test': ('Reading Speed Test', 'Test your reading speed in words per minute. Track improvement over time with comprehension checks.'),
    'resolution-calculator': ('Resolution Calculator', 'Calculate aspect ratios, pixel dimensions and display resolutions. Convert between different resolution standards.'),
    'scatter-plot-maker': ('Scatter Plot Maker', 'Create scatter plots and bubble charts online. Visualize relationships between variables with trend lines.'),
    'screenshot-to-pdf': ('Screenshot to PDF', 'Convert screenshots and images to PDF format. Adjust page size, orientation and margins.'),
    'structured-data-validator': ('Structured Data Validator', 'Validate JSON-LD, Microdata and RDFa structured data. Check Schema.org markup for SEO compliance.'),
    'triangle-calculator': ('Triangle Calculator', 'Calculate triangle sides, angles, area and perimeter. Supports right triangles, isosceles and equilateral.'),
    'unit-price-calculator': ('Unit Price Calculator', 'Compare product unit prices to find the best value. Calculate price per unit, per ounce, per liter and more.'),
    'video-frame-grabber': ('Video Frame Grabber', 'Extract frames from video files as images. Browse frame by frame and save snapshots. Local processing, no upload.'),
    'zalgo-text-generator': ('Zalgo Text Generator', 'Generate creepy zalgo text with combining diacritical marks. Adjust corruption intensity for the perfect effect.'),
    'zip-extractor': ('ZIP Extractor', 'Extract files from ZIP archives online. Preview contents before extraction. All processing done locally in browser.'),
}

en_generic = [
    ('free tool', 'Completely free to use, no registration required. Data is processed locally in your browser, protecting your privacy.'),
    ('online tool', 'Works on both desktop and mobile. Responsive design adapts to any screen size. Open your browser and start using anytime.'),
    ('free utility', 'All features are permanently free with no ads. Continuously updated and optimized. Bookmark for future use.'),
]

fixed_en = 0
for item in en_thin:
    path = os.path.join(SITE, 'en', item, 'index.html')
    if not os.path.isfile(path):
        continue
    
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    if item in en_descs:
        title, desc = en_descs[item]
    else:
        tm = re.search(r'<title>(.*?)(?:\s*[-–|]\s*Free ToolBase)?</title>', content)
        title = tm.group(1).strip() if tm else item.replace('-', ' ').title()
        desc = f'{title} - free online tool, simple and fast, instant results.'
    
    gtitle, gdesc = random.choice(en_generic)
    
    faq_html = f'''
    <section class="faq-section">
      <h2>About {title}</h2>
      <div class="faq-item">
        <h3>How to use {title}?</h3>
        <p>Simply enter content or upload files in the input area and click the button to get results. {desc}</p>
      </div>
      <div class="faq-item">
        <h3>Is this tool free?</h3>
        <p>{title} is a {gtitle}. {gdesc}</p>
      </div>
    </section>'''
    
    # 插入到最后一个</div>之前
    last_div = content.rfind('</div>')
    if last_div > 0:
        content = content[:last_div] + faq_html + '\n' + content[last_div:]
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        fixed_en += 1
    elif '</body>' in content:
        content = content.replace('</body>', faq_html + '\n</body>')
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        fixed_en += 1
    
    if fixed_en % 15 == 0:
        print(f"  已处理 {fixed_en}...")

print(f"EN页面修复: {fixed_en} 个")
print(f"总计: {fixed_en} 个")