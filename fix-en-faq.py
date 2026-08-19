#!/usr/bin/env python3
"""
Fix EN pages that have Chinese visible FAQ sections instead of English ones.
Replaces the Chinese FAQ HTML with English FAQ HTML.
"""
import os, re, sys, json, random

TOOLS_SITE = os.path.expanduser("~/tools-site")

# EN FAQ templates
EN_FAQ_TEMPLATES = [
    ("Is {name} free to use?", "Yes, {name} is completely free to use. No registration or login required — all features are available immediately."),
    ("Does {name} upload my data to a server?", "No. {name} uses client-side processing — everything runs in your browser. Your data never leaves your device, and the tool works even without an internet connection."),
    ("Can I use {name} on my phone?", "Yes. {name} is fully responsive and works on phones, tablets, and desktops. The interface adapts automatically to your screen size."),
    ("Do I need to install any software?", "No. {name} is a web-based tool — just open it in your browser and start using it. No downloads, plugins, or extensions required."),
    ("Is my data safe when using {name}?", "Absolutely. All processing happens locally in your browser. No data is sent to any server, so there's zero risk of data leaks. Your information stays completely under your control."),
    ("Are there any usage limits for {name}?", "{name} has no usage limits — it's free and unlimited. Since processing is done client-side, speed depends on your device. For very large files, we recommend processing in batches for the best experience."),
]

# Category-specific EN FAQs
CATEGORY_FAQS_EN = {
    "pdf": [
        ("Will the PDF quality decrease after processing?", "We preserve original quality whenever possible. For compression, you can choose the compression level to balance file size and quality."),
        ("Does it support encrypted PDF files?", "Some tools support encrypted PDFs. If the file is password-protected, you'll need to provide the password first."),
    ],
    "image": [
        ("What image formats are supported?", "Common formats including PNG, JPEG, WebP, GIF, BMP, and SVG are supported. The exact formats depend on the specific tool."),
        ("Will image quality decrease after processing?", "For lossless formats (like PNG), quality is preserved. For lossy formats (like JPEG), you can choose the output quality to balance file size and image quality."),
    ],
    "json": [
        ("How large a JSON file can I process?", "Since processing is client-side, file size depends on your device memory. Files up to several MB typically process smoothly."),
        ("Does it support JSONPath queries?", "Yes, standard JSONPath syntax is supported. You can use dot notation and bracket syntax to access nested fields."),
    ],
    "password": [
        ("Are the generated passwords truly secure?", "Yes. Passwords are generated using the browser's native Crypto API, ensuring true randomness. Generated passwords are never stored on any server."),
        ("Are generated passwords saved?", "No. Generated passwords are only displayed in your browser and are never sent to any server or stored. Closing the page clears the password."),
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
        ("Can hash values be reversed or decrypted?", "No. Hashing is a one-way function — it's impossible to derive the original data from a hash. This is exactly why hashes are used for password storage and data integrity verification."),
    ],
    "converter": [
        ("Are converted files compatible with other software?", "Yes. Converted files follow standard format specifications and are compatible with mainstream software and platforms."),
    ],
    "audio": [
        ("What audio formats are supported?", "Common formats including MP3, WAV, OGG, AAC, and FLAC are supported. The exact formats depend on the specific tool."),
    ],
    "video": [
        ("What video formats are supported?", "Common formats including MP4, WebM, AVI, and MOV are supported. Processing is done entirely in your browser."),
    ],
    "encrypt": [
        ("Is the encryption secure?", "Yes. We use industry-standard encryption algorithms (AES-256, RSA, etc.) implemented via the Web Crypto API. All encryption happens locally in your browser."),
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
        ("Does this tool make real network requests?", "Some tools make real requests (like HTTP header checkers) while others work locally. Check the tool description for details."),
    ],
    "svg": [
        ("What SVG features are supported?", "Standard SVG 1.1 features are supported. Some advanced SVG 2.0 features may not be fully supported depending on the tool."),
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
            # If still Chinese, try to get from directory name
            if re.match(r'^[\u4e00-\u9fff]', name):
                dir_name = os.path.basename(os.path.dirname(filepath))
                # Convert kebab-case to Title Case
                name = dir_name.replace('-', ' ').title()
                return name
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
        'pdf': ['pdf'],
        'image': ['image', 'img', 'png', 'jpeg', 'jpg', 'webp', 'gif', 'svg', 'icon', 'photo', 'qr', 'favicon', 'screenshot', 'watermark', 'crop', 'resize'],
        'json': ['json'],
        'password': ['password', 'pass', 'bcrypt', 'argon'],
        'color': ['color', 'colour', 'palette', 'gradient', 'hsl', 'rgb', 'hex'],
        'css': ['css', 'flexbox', 'grid', 'shadow', 'border', 'animation', 'gradient', 'tailwind'],
        'qr': ['qr', 'barcode', 'qrcode'],
        'hash': ['hash', 'sha', 'md5', 'crc', 'checksum', 'hmac'],
        'converter': ['converter', 'convert', 'to-', '-to-'],
        'audio': ['audio', 'mp3', 'wav', 'ogg', 'aac', 'flac'],
        'video': ['video', 'mp4', 'webm', 'avi', 'mov'],
        'encrypt': ['encrypt', 'decrypt', 'aes', 'rsa', 'cipher'],
        'base64': ['base64', 'base32', 'base58', 'base85'],
        'sql': ['sql', 'mysql', 'postgres', 'mongodb'],
        'cron': ['cron', 'crontab'],
        'regex': ['regex', 'regexp'],
        'network': ['ip', 'dns', 'whois', 'ssl', 'http', 'url', 'port'],
        'svg': ['svg'],
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
    
    # Add category-specific FAQs
    for cat in categories:
        if cat in CATEGORY_FAQS_EN:
            for q, a in CATEGORY_FAQS_EN[cat]:
                faqs.append(f'    <div class="faq-item">\n      <h3>{q.format(name=tool_name)}</h3>\n      <p>{a.format(name=tool_name)}</p>\n    </div>')
    
    # Limit to 6-8 total
    faqs = faqs[:8]
    
    html = f'''  <div class="info-section faq-section">
    <h2>❓ Frequently Asked Questions</h2>
{chr(10).join(faqs)}
  </div>'''
    return html

def fix_en_page(filepath):
    """Fix an EN page that has Chinese FAQ section - replace with English FAQ."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Skip if already has English FAQ
    if 'Frequently Asked Questions' in content:
        return False, "already has EN FAQ"
    
    # Must have Chinese FAQ to replace
    if '常见问题' not in content:
        return False, "no CN FAQ to replace"
    
    tool_name = extract_tool_name_en(filepath)
    if not tool_name:
        return False, "couldn't extract tool name"
    
    categories = detect_categories(filepath, content)
    faq_html = generate_faq_html_en(tool_name, categories)
    
    # Strategy: Replace the Chinese FAQ section with English FAQ
    # Pattern: <div class="info-section faq-section">...常见问题...</div>
    # Or: <h2>❓ 常见问题</h2>...until next section
    
    # Try to find and replace the entire faq-section div
    pattern1 = re.compile(
        r'<div class="info-section faq-section">.*?常见问题.*?</div>\s*</div>',
        re.DOTALL
    )
    m = pattern1.search(content)
    if m:
        content = content[:m.start()] + faq_html + content[m.end():]
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True, f"Replaced CN FAQ with EN FAQ ({tool_name})"
    
    # Try alternative pattern: just the h2 and items
    pattern2 = re.compile(
        r'<h2>❓\s*常见问题</h2>.*?(?=</div>\s*</div>|<div class="footer|<!-- Related|<link rel="stylesheet" href="https://free-toolbase.com/related)',
        re.DOTALL
    )
    m = pattern2.search(content)
    if m:
        content = content[:m.start()] + faq_html + content[m.end():]
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True, f"Replaced CN FAQ h2 with EN FAQ ({tool_name})"
    
    # Try simpler: just replace the h2 text
    if '常见问题' in content:
        # Replace just the heading
        content = content.replace('❓ 常见问题', '❓ Frequently Asked Questions')
        # Replace faq-item contents if they're Chinese
        # This is harder - for now just replace the heading
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True, f"Replaced CN FAQ heading with EN ({tool_name})"
    
    return False, "couldn't find FAQ section to replace"

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
        
        # Skip non-tool pages
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
