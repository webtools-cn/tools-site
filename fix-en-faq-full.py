#!/usr/bin/env python3
"""
Replace entire Chinese FAQ sections on EN pages with proper English FAQ sections.
Handles both the heading and the FAQ items.
"""
import os, re, sys, random

TOOLS_SITE = os.path.expanduser("~/tools-site")

EN_FAQ_TEMPLATES = [
    ("Is {name} free to use?", "Yes, {name} is completely free to use. No registration or login required — all features are available immediately."),
    ("Does {name} upload my data to a server?", "No. {name} uses client-side processing — everything runs in your browser. Your data never leaves your device, and the tool works even without an internet connection."),
    ("Can I use {name} on my phone?", "Yes. {name} is fully responsive and works on phones, tablets, and desktops. The interface adapts automatically to your screen size."),
    ("Do I need to install any software?", "No. {name} is a web-based tool — just open it in your browser and start using it. No downloads, plugins, or extensions required."),
    ("Is my data safe when using {name}?", "Absolutely. All processing happens locally in your browser. No data is sent to any server, so there's zero risk of data leaks. Your information stays completely under your control."),
    ("Are there any usage limits for {name}?", "{name} has no usage limits — it's free and unlimited. Since processing is done client-side, speed depends on your device. For very large files, we recommend processing in batches for the best experience."),
]

CATEGORY_FAQS_EN = {
    "pdf": [
        ("Will the PDF quality decrease after processing?", "We preserve original quality whenever possible. For compression, you can choose the compression level to balance file size and quality."),
        ("Does it support encrypted PDF files?", "Some tools support encrypted PDFs. If the file is password-protected, you'll need to provide the password first."),
    ],
    "image": [
        ("What image formats are supported?", "Common formats including PNG, JPEG, WebP, GIF, BMP, and SVG are supported. The exact formats depend on the specific tool."),
        ("Will image quality decrease after processing?", "For lossless formats (like PNG), quality is preserved. For lossy formats (like JPEG), you can choose the output quality."),
    ],
    "json": [
        ("How large a JSON file can I process?", "Since processing is client-side, file size depends on your device memory. Files up to several MB typically process smoothly."),
        ("Does it support JSONPath queries?", "Yes, standard JSONPath syntax is supported. You can use dot notation and bracket syntax to access nested fields."),
    ],
    "password": [
        ("Are the generated passwords truly secure?", "Yes. Passwords are generated using the browser's native Crypto API, ensuring true randomness. Generated passwords are never stored on any server."),
    ],
    "color": [
        ("Are the color values accurate?", "Color values are based on standard color space conversion algorithms with high precision. Display may vary slightly depending on monitor calibration."),
    ],
    "css": [
        ("Can the generated CSS code be used directly in projects?", "Yes. The generated CSS code is compatible with all modern browsers. Some properties may need browser prefixes for older versions."),
    ],
    "qr": [
        ("Are there any usage limits for generated QR codes?", "No limits. Generated QR codes can be used for any purpose, including commercial use. QR codes themselves don't expire."),
    ],
    "hash": [
        ("Can hash values be reversed or decrypted?", "No. Hashing is a one-way function — it's impossible to derive the original data from a hash."),
    ],
    "converter": [
        ("Are converted files compatible with other software?", "Yes. Converted files follow standard format specifications and are compatible with mainstream software and platforms."),
    ],
    "audio": [
        ("What audio formats are supported?", "Common formats including MP3, WAV, OGG, AAC, and FLAC are supported."),
    ],
    "video": [
        ("What video formats are supported?", "Common formats including MP4, WebM, AVI, and MOV are supported. Processing is done entirely in your browser."),
    ],
    "encrypt": [
        ("Is the encryption secure?", "Yes. We use industry-standard encryption algorithms implemented via the Web Crypto API. All encryption happens locally in your browser."),
    ],
    "base64": [
        ("What is Base64 encoding?", "Base64 is a binary-to-text encoding scheme that represents binary data in an ASCII string format. It's commonly used for embedding data in HTML, CSS, and JSON."),
    ],
    "sql": [
        ("Does this tool connect to a database?", "No. All SQL processing happens locally in your browser. No database connections are made."),
    ],
    "cron": [
        ("What cron expressions are supported?", "Standard 5-field cron expressions (minute hour day month weekday) and 6-field expressions (with seconds) are supported."),
    ],
    "regex": [
        ("What regex flavors are supported?", "JavaScript regex flavor is used, which is similar to PCRE with some differences. Most common patterns are supported."),
    ],
    "network": [
        ("Does this tool make real network requests?", "Some tools make real requests while others work locally. Check the tool description for details."),
    ],
    "svg": [
        ("What SVG features are supported?", "Standard SVG 1.1 features are supported. Some advanced SVG 2.0 features may not be fully supported."),
    ],
    "text": [
        ("What text encodings are supported?", "UTF-8 is the primary encoding. Most tools also support ASCII, UTF-16, and other common encodings."),
    ],
    "calculator": [
        ("How accurate are the calculations?", "Calculations use JavaScript's floating-point arithmetic with up to 15 significant digits of precision. For most practical purposes, this is more than sufficient."),
    ],
}

def extract_tool_name_en(filepath):
    """Extract the English tool name from the page."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        # Try to get from h1
        m = re.search(r'<h1[^>]*>([^<]+)', content)
        if m:
            name = m.group(1).strip()
            name = re.sub(r'^[\U0001F300-\U0001F9FF]+\s*', '', name)
            name = name.split('\n')[0].strip()
            if name and not re.match(r'^[\u4e00-\u9fff]', name):
                return name
        # Fallback to title
        m = re.search(r'<title>([^<]+)</title>', content)
        if m:
            title = m.group(1)
            name = title.split('-')[0].split('|')[0].split('·')[0].strip()
            if not re.match(r'^[\u4e00-\u9fff]', name):
                return name
    except:
        pass
    # Final fallback: directory name
    dir_name = os.path.basename(os.path.dirname(filepath))
    return dir_name.replace('-', ' ').title()

def detect_categories(filepath, content):
    """Detect tool categories from file path and content."""
    categories = []
    path_lower = filepath.lower()
    cat_keywords = {
        'pdf': ['pdf'], 'image': ['image', 'img', 'png', 'jpeg', 'jpg', 'webp', 'gif', 'svg', 'icon', 'photo', 'qr', 'favicon', 'screenshot', 'watermark', 'crop', 'resize'],
        'json': ['json'], 'password': ['password', 'pass', 'bcrypt', 'argon'],
        'color': ['color', 'colour', 'palette', 'gradient', 'hsl', 'rgb', 'hex'],
        'css': ['css', 'flexbox', 'grid', 'shadow', 'border', 'animation', 'tailwind'],
        'qr': ['qr', 'barcode', 'qrcode'], 'hash': ['hash', 'sha', 'md5', 'crc', 'checksum', 'hmac'],
        'converter': ['converter', 'convert', 'to-', '-to-'],
        'audio': ['audio', 'mp3', 'wav', 'ogg', 'aac', 'flac'],
        'video': ['video', 'mp4', 'webm', 'avi', 'mov'],
        'encrypt': ['encrypt', 'decrypt', 'aes', 'rsa', 'cipher'],
        'base64': ['base64', 'base32', 'base58', 'base85'],
        'sql': ['sql', 'mysql', 'postgres', 'mongodb'],
        'cron': ['cron', 'crontab'], 'regex': ['regex', 'regexp'],
        'network': ['ip', 'dns', 'whois', 'ssl', 'http', 'url', 'port'],
        'svg': ['svg'], 'text': ['text', 'word', 'string', 'line', 'character'],
        'calculator': ['calculator', 'calc', 'math', 'bmi', 'age', 'loan', 'tip', 'interest'],
    }
    for cat, keywords in cat_keywords.items():
        for kw in keywords:
            if kw in path_lower:
                categories.append(cat)
                break
    return categories

def generate_faq_html_en(tool_name, categories):
    """Generate EN FAQ HTML section."""
    count = random.choice([4, 5, 6])
    selected = random.sample(EN_FAQ_TEMPLATES, min(count, len(EN_FAQ_TEMPLATES)))
    
    faqs = []
    for q, a in selected:
        faqs.append(f'    <div class="faq-item">\n      <h3>{q.format(name=tool_name)}</h3>\n      <p>{a.format(name=tool_name)}</p>\n    </div>')
    
    for cat in categories:
        if cat in CATEGORY_FAQS_EN:
            for q, a in CATEGORY_FAQS_EN[cat]:
                faqs.append(f'    <div class="faq-item">\n      <h3>{q.format(name=tool_name)}</h3>\n      <p>{a.format(name=tool_name)}</p>\n    </div>')
    
    faqs = faqs[:8]
    
    html = f'''  <div class="info-section faq-section">
    <h2>❓ Frequently Asked Questions</h2>
{chr(10).join(faqs)}
  </div>'''
    return html

def has_chinese_faq_items(content):
    """Check if FAQ items contain Chinese text."""
    # Find FAQ items and check for Chinese characters
    faq_items = re.findall(r'<div class="faq-item">(.*?)</div>\s*</div>', content, re.DOTALL)
    for item in faq_items:
        if re.search(r'[\u4e00-\u9fff]', item):
            return True
    return False

def replace_faq_section(content, new_faq_html):
    """Replace the entire FAQ section in the content."""
    
    # Pattern 1: <div class="info-section faq-section">...</div> (with nested divs)
    # This is tricky because of nested divs. We need to match the outer div properly.
    
    # Try to find the faq-section div and replace everything from it to its closing div
    # Strategy: find the start, then count div opens/closes to find the end
    
    start_marker = '<div class="info-section faq-section">'
    start_pos = content.find(start_marker)
    
    if start_pos == -1:
        # Try alternative: just the faq-section class
        start_marker = '<div class="faq-section">'
        start_pos = content.find(start_marker)
    
    if start_pos == -1:
        # Try finding by the heading
        heading_patterns = [
            '<h2>❓ 常见问题</h2>',
            '<h2>❓ Frequently Asked Questions</h2>',
            '<h2>常见问题</h2>',
        ]
        for hp in heading_patterns:
            hp_pos = content.find(hp)
            if hp_pos != -1:
                # Find the enclosing div
                # Search backwards for the opening div
                before = content[:hp_pos]
                last_div = before.rfind('<div')
                if last_div != -1:
                    start_pos = last_div
                    start_marker = content[last_div:hp_pos]
                    break
    
    if start_pos == -1:
        return None
    
    # Now find the matching closing div
    depth = 0
    pos = start_pos
    while pos < len(content):
        next_open = content.find('<div', pos + 1)
        next_close = content.find('</div>', pos + 1)
        
        if next_close == -1:
            break
        
        if next_open != -1 and next_open < next_close:
            depth += 1
            pos = next_open
        else:
            if depth == 0:
                # This is the closing div for our section
                end_pos = next_close + len('</div>')
                result = content[:start_pos] + new_faq_html + content[end_pos:]
                return result
            depth -= 1
            pos = next_close
    
    return None

def fix_en_page(filepath):
    """Fix an EN page that has Chinese FAQ items."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if page has FAQ section with Chinese items
    if 'faq-item' not in content and '常见问题' not in content and 'Frequently Asked' not in content:
        return False, "no FAQ section"
    
    if not has_chinese_faq_items(content) and 'Frequently Asked Questions' in content:
        return False, "already has proper EN FAQ"
    
    tool_name = extract_tool_name_en(filepath)
    if not tool_name:
        return False, "couldn't extract tool name"
    
    categories = detect_categories(filepath, content)
    faq_html = generate_faq_html_en(tool_name, categories)
    
    result = replace_faq_section(content, faq_html)
    if result:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(result)
        return True, f"Replaced FAQ section with EN ({tool_name})"
    
    return False, "couldn't replace FAQ section"

def main():
    fixed = 0
    skipped = 0
    errors = []
    
    en_dir = os.path.join(TOOLS_SITE, 'en')
    if not os.path.isdir(en_dir):
        print("No en/ directory found")
        return
    
    for dirpath, dirnames, filenames in os.walk(en_dir):
        if 'index.html' not in filenames:
            continue
        
        rel_path = os.path.relpath(dirpath, TOOLS_SITE)
        skip_dirs = ['blog', 'tools', 'category', 'chrome-extension', 'quality-reports']
        if any(skip_dir in rel_path for skip_dir in skip_dirs):
            continue
        
        filepath = os.path.join(dirpath, 'index.html')
        try:
            success, info = fix_en_page(filepath)
            if success:
                fixed += 1
                print(f"✅ {rel_path}: {info}")
            else:
                skipped += 1
        except Exception as e:
            errors.append(f"{rel_path}: {e}")
    
    print(f"\n=== Results ===")
    print(f"Fixed: {fixed} pages")
    print(f"Skipped: {skipped} pages")
    if errors:
        print(f"Errors: {len(errors)}")
        for e in errors[:10]:
            print(f"  {e}")

if __name__ == '__main__':
    main()
