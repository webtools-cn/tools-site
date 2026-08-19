#!/usr/bin/env python3
"""Generate category hub pages for SEO internal linking."""
import json
import os
import re
from collections import defaultdict

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load data
with open('/tmp/cat_tools.json', 'r') as f:
    en_tools = json.load(f)
with open('/tmp/cat_tools_cn.json', 'r') as f:
    cn_tools = json.load(f)
with open('/tmp/cat_meta.json', 'r') as f:
    cat_meta = json.load(f)

# Category FAQ data
cat_faqs = {
    'dev': [
        {'q': 'Are these developer tools free to use?', 'a': 'Yes, all developer tools on this page are 100% free. No signup, no hidden fees, no usage limits. Every tool works directly in your browser.'},
        {'q': 'Is my data safe when using these tools?', 'a': 'Absolutely. All processing happens locally in your browser using JavaScript. Your code, JSON data, and files never leave your device. You can even use these tools offline.'},
        {'q': 'What formats do the JSON tools support?', 'a': 'Our JSON tools support standard JSON format including objects, arrays, nested structures, and Unicode. The formatter handles files up to 10MB, and the validator provides detailed error messages with line numbers.'},
        {'q': 'Can I use these tools for production code?', 'a': 'Yes. The generated code, formatted output, and encoded/decoded results are production-ready. Hash generators use the Web Crypto API for cryptographic-grade output.'},
    ],
    'utility': [
        {'q': 'Are these utility tools really free?', 'a': 'Yes, 100% free with no signup required. No usage limits, no premium tiers, no hidden costs. Every tool is fully functional for free.'},
        {'q': 'How secure is the password generator?', 'a': "The password generator uses the browser's Crypto.getRandomValues() API for cryptographically secure random numbers. Passwords are generated locally and never sent to any server."},
        {'q': 'Can I use these tools on my phone?', 'a': 'Yes, all tools are fully responsive and work on any device with a modern browser — desktop, tablet, or phone.'},
        {'q': 'Do I need to install anything?', 'a': 'No installation needed. All tools run directly in your web browser. Just open the page and start using them immediately.'},
    ],
    'image': [
        {'q': 'What image formats are supported?', 'a': 'Our image tools support PNG, JPEG, WebP, GIF, BMP, SVG, ICO, and TIFF formats. You can convert between any of these formats.'},
        {'q': 'Is there a file size limit for image processing?', 'a': "Since all processing happens in your browser, the limit depends on your device's memory. Most tools handle images up to 20-50MB without issues."},
        {'q': 'Will my images be uploaded to a server?', 'a': 'No. All image processing happens locally in your browser using Canvas API and WebAssembly. Your images never leave your device.'},
        {'q': 'Can I batch process multiple images?', 'a': 'Yes, many of our image tools support batch processing. You can upload multiple files and process them all at once.'},
    ],
    'calc': [
        {'q': 'How accurate are these calculators?', 'a': "Our calculators use standard mathematical formulas and JavaScript's IEEE 754 double-precision arithmetic. Results are accurate to at least 15 significant digits for most calculations."},
        {'q': 'Can I use these for professional work?', 'a': 'Yes. While we recommend double-checking critical financial or engineering calculations, our tools use the same formulas used in professional applications.'},
        {'q': 'Do the calculators store my data?', 'a': 'No. All calculations happen in your browser. Your input data is never sent to any server and is not stored anywhere after you close the page.'},
    ],
    'text': [
        {'q': 'What text encoding do these tools support?', 'a': 'Our text tools support UTF-8, ASCII, Unicode, and most common encodings. They handle multilingual text including Chinese, Japanese, Korean, and emoji.'},
        {'q': 'Is there a character or word limit?', 'a': 'Most text tools handle up to 1MB of text (roughly 500,000 characters). For very large files, we recommend splitting them first.'},
        {'q': 'Can I use these tools for coding?', 'a': 'Absolutely. Many developers use our text diff, case converter, and encoding tools daily. The output is ready to paste directly into code editors.'},
    ],
    'design': [
        {'q': 'Can I use the generated CSS in my projects?', 'a': 'Yes, all generated CSS code is production-ready. Just copy and paste it into your stylesheets. The code follows modern CSS standards.'},
        {'q': 'What color formats are supported?', 'a': 'Our color tools support HEX, RGB, RGBA, HSL, HSLA, and named CSS colors. You can convert between any of these formats.'},
        {'q': 'Do the design tools work with frameworks like Tailwind or Bootstrap?', 'a': 'Yes. The generated CSS is framework-agnostic and works with any CSS framework. Some tools even offer Tailwind-specific output options.'},
    ],
    'pdf': [
        {'q': 'Are these PDF tools really free?', 'a': 'Yes, all PDF tools are 100% free with no signup. Unlike other services that limit free usage, our tools have no daily limits or watermarks.'},
        {'q': 'Is my PDF data safe?', 'a': 'Absolutely. All PDF processing happens in your browser using the pdf-lib library. Your documents never leave your device — no server upload, no cloud processing.'},
        {'q': 'What PDF operations are supported?', 'a': 'We support merging, splitting, compressing, rotating, adding watermarks, extracting text, adding page numbers, converting to/from images, and many more operations.'},
        {'q': 'Can I process password-protected PDFs?', 'a': 'Some tools support password-protected PDFs for decryption. For encryption, you can add password protection to any PDF using our Protect PDF tool.'},
    ],
    'office': [
        {'q': 'What file formats do the office tools support?', 'a': 'Our office tools support CSV, Excel (XLSX), Word (DOCX), PowerPoint (PPTX), Markdown, and other common document formats.'},
        {'q': 'Can I convert between office formats?', 'a': 'Yes. You can convert between CSV and Excel, Markdown and HTML, and many other format combinations. All conversions happen in your browser.'},
        {'q': 'Do I need Microsoft Office installed?', 'a': "No. All processing happens in your browser. You don't need any desktop software installed."},
    ],
    'media': [
        {'q': 'What audio/video formats are supported?', 'a': 'Our media tools support MP3, WAV, OGG, MP4, WebM, and other common audio and video formats.'},
        {'q': 'Is there a file size limit for media processing?', 'a': "Since processing happens in your browser, the limit depends on your device. Most tools handle files up to 100MB. For larger files, we recommend desktop software."},
        {'q': 'Will my media files be uploaded to a server?', 'a': 'No. All media processing happens locally in your browser. Your files never leave your device.'},
    ],
    'fun': [
        {'q': 'Are these fun tools free?', 'a': 'Yes, all fun tools are completely free. Generate as many ASCII art, random names, or creative text as you want.'},
        {'q': 'Can I share the results?', 'a': 'Absolutely. All generated content can be copied and shared freely. No attribution required.'},
    ],
    'health': [
        {'q': 'How accurate are the health calculators?', 'a': 'Our health calculators use standard medical formulas (e.g., Mifflin-St Jeor for calories, standard BMI formula). They provide good estimates but should not replace professional medical advice.'},
        {'q': 'Should I use these for medical decisions?', 'a': 'These tools provide estimates for informational purposes. Always consult a healthcare professional for medical decisions.'},
    ],
    'math': [
        {'q': 'What mathematical operations are supported?', 'a': 'Our math tools cover arithmetic, algebra, geometry, trigonometry, statistics, and number theory. From basic calculators to advanced equation solvers.'},
        {'q': 'How precise are the calculations?', 'a': "Calculations use JavaScript's IEEE 754 double-precision (64-bit) arithmetic, providing about 15-17 significant decimal digits of precision."},
    ],
    'creative': [
        {'q': 'Can I use the generated content commercially?', 'a': 'Yes. All content generated by our creative tools is free to use for any purpose, including commercial projects.'},
        {'q': 'How do the generators work?', 'a': 'Our generators use various algorithms — from random word combinations to template-based generation. Each tool is designed to produce unique, useful output.'},
    ],
    'security': [
        {'q': 'Are these security tools safe to use?', 'a': "Yes. All cryptographic operations use the browser's built-in Web Crypto API, which implements industry-standard algorithms. Your data never leaves your browser."},
        {'q': 'Can I use these for real encryption?', 'a': 'The encryption tools use standard algorithms (AES-256, SHA-256, bcrypt, etc.) suitable for real-world use. However, for highly sensitive data, we recommend using dedicated security software.'},
        {'q': 'What hashing algorithms are supported?', 'a': 'We support MD5, SHA-1, SHA-256, SHA-384, SHA-512, SHA-3, bcrypt, Argon2, and more. All using the Web Crypto API for cryptographic-grade output.'},
    ],
    'video': [
        {'q': 'What video formats are supported?', 'a': 'Our video tools support MP4, WebM, AVI, MOV, and other common video formats. Processing happens entirely in your browser.'},
        {'q': 'Is there a file size limit?', 'a': "Video processing in the browser is limited by your device's memory. Most tools handle files up to 100MB. For larger videos, desktop software is recommended."},
    ],
}

CSS = """*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:#0f172a;color:#e2e8f0;line-height:1.6}
.container{max-width:1200px;margin:0 auto;padding:0 20px}
header{background:linear-gradient(135deg,#1e293b 0%,#0f172a 100%);border-bottom:1px solid rgba(148,163,184,.1);padding:16px 0}
header .container{display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px}
.logo{font-size:1.3rem;font-weight:700;color:#f1f5f9;text-decoration:none}
.logo:hover{color:#60a5fa}
nav a{color:#94a3b8;text-decoration:none;margin-left:20px;font-size:.9rem}
nav a:hover{color:#60a5fa}
.hero{padding:48px 0 32px;text-align:center}
.hero h1{font-size:2.2rem;font-weight:800;margin-bottom:12px;background:linear-gradient(135deg,#60a5fa,#a78bfa);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.hero p{font-size:1.1rem;color:#94a3b8;max-width:700px;margin:0 auto 16px}
.hero .count{display:inline-block;background:rgba(96,165,250,.15);color:#60a5fa;padding:6px 16px;border-radius:20px;font-size:.9rem;font-weight:600}
.trust{display:flex;justify-content:center;gap:24px;margin:24px 0;flex-wrap:wrap}
.trust span{display:flex;align-items:center;gap:6px;color:#94a3b8;font-size:.85rem}
.trust span::before{content:'';display:inline-block;width:8px;height:8px;border-radius:50%;background:#22c55e}
.howto{background:#1e293b;border-radius:12px;padding:24px;margin:24px 0;border:1px solid rgba(148,163,184,.08)}
.howto h2{font-size:1.2rem;color:#f1f5f9;margin-bottom:16px}
.howto ol{padding-left:24px}
.howto li{margin-bottom:8px;color:#cbd5e1;font-size:.95rem}
.tools-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:16px;margin:32px 0}
.tool-card{background:#1e293b;border:1px solid rgba(148,163,184,.08);border-radius:12px;padding:20px;transition:all .2s}
.tool-card:hover{border-color:rgba(96,165,250,.3);transform:translateY(-2px);box-shadow:0 8px 24px rgba(0,0,0,.3)}
.tool-card .icon{font-size:1.5rem;margin-bottom:8px}
.tool-card h3{font-size:1rem;color:#f1f5f9;margin-bottom:6px;font-weight:600}
.tool-card p{font-size:.85rem;color:#94a3b8;margin-bottom:12px;line-height:1.5;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.tool-card a{display:inline-block;color:#60a5fa;text-decoration:none;font-size:.85rem;font-weight:500}
.tool-card a:hover{text-decoration:underline}
.faq-section{margin:40px 0}
.faq-section h2{font-size:1.3rem;color:#f1f5f9;margin-bottom:20px}
.faq-item{margin-bottom:12px;padding:16px;border-radius:10px;background:#1e293b;border:1px solid rgba(148,163,184,.08)}
.faq-item h3{font-size:.95rem;color:#f1f5f9;margin-bottom:6px;cursor:pointer}
.faq-item p{color:#94a3b8;font-size:.9rem}
.related{margin:40px 0;padding:24px;background:#1e293b;border-radius:12px;border:1px solid rgba(148,163,184,.08)}
.related h2{font-size:1.2rem;color:#f1f5f9;margin-bottom:16px}
.related-links{display:flex;flex-wrap:wrap;gap:10px}
.related-links a{display:inline-flex;align-items:center;gap:6px;padding:8px 16px;background:rgba(96,165,250,.1);color:#60a5fa;border-radius:8px;text-decoration:none;font-size:.9rem;transition:all .2s}
.related-links a:hover{background:rgba(96,165,250,.2)}
footer{padding:24px 0;text-align:center;color:#64748b;font-size:.8rem;border-top:1px solid rgba(148,163,184,.08);margin-top:40px}
@media(max-width:768px){.hero h1{font-size:1.6rem}.tools-grid{grid-template-columns:1fr}.trust{gap:12px}}"""


def generate_category_page(cat, tools, lang='en'):
    meta = cat_meta.get(cat, {})
    
    if lang == 'en':
        name = meta.get('en_name', cat.title() + ' Tools')
        desc = meta.get('en_desc', '')
        icon = meta.get('icon', '🔧')
        keywords = meta.get('keywords', '')
        lang_attr = 'en'
        site_name = 'Online Tools'
        base_url = 'https://free-toolbase.com/en/category'
        tool_base = '/en'
        breadcrumb_home = 'Home'
        faqs = cat_faqs.get(cat, cat_faqs.get('utility', []))
        heading = icon + ' Free Online ' + name
        subheading = desc
        tool_count_text = str(len(tools)) + ' free tools'
        home_text = 'Home'
        faq_title = 'Frequently Asked Questions'
        related_title = 'Explore Other Categories'
        howto_title = 'How to Use These Tools'
        howto_steps = [
            'Choose a tool from the list above that matches your needs.',
            'Click "Use Now" to open the tool in a new page.',
            'Follow the tool-specific instructions to process your data.',
            'Copy or download the results — all processing happens in your browser!'
        ]
    else:
        name = meta.get('cn_name', cat.title() + '工具')
        desc = meta.get('cn_desc', '')
        icon = meta.get('icon', '🔧')
        keywords = name + ',在线' + name + ',免费' + name
        lang_attr = 'zh-CN'
        site_name = '在线工具'
        base_url = 'https://free-toolbase.com/category'
        tool_base = ''
        breadcrumb_home = '首页'
        faqs = cat_faqs.get(cat, cat_faqs.get('utility', []))
        heading = icon + ' 免费在线' + name
        subheading = desc
        tool_count_text = str(len(tools)) + '个免费工具'
        home_text = '首页'
        faq_title = '常见问题'
        related_title = '浏览其他分类'
        howto_title = '如何使用这些工具'
        howto_steps = [
            '从上方列表中选择您需要的工具。',
            '点击"立即使用"打开工具页面。',
            '按照工具说明处理您的数据。',
            '复制或下载结果——所有处理都在浏览器中完成！'
        ]
    
    sorted_tools = sorted(tools, key=lambda x: x['name'])
    
    # Build Schema JSON
    faq_schema = []
    for faq in faqs:
        faq_schema.append({
            "@type": "Question",
            "name": faq['q'],
            "acceptedAnswer": {
                "@type": "Answer",
                "text": faq['a']
            }
        })
    
    item_list = []
    for i, tool in enumerate(sorted_tools[:50]):
        item_list.append({
            "@type": "ListItem",
            "position": i + 1,
            "name": tool['name'],
            "url": base_url + "/" + tool['url'] + "/"
        })
    
    collection_schema = {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": "Free Online " + name,
        "description": desc,
        "url": base_url + "/" + cat + "/",
        "numberOfItems": len(tools),
        "about": {"@type": "Thing", "name": name},
        "provider": {"@type": "Organization", "name": site_name}
    }
    
    itemlist_schema = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "numberOfItems": len(tools),
        "itemListElement": item_list
    }
    
    faqpage_schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": faq_schema
    }
    
    breadcrumb_schema = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": breadcrumb_home, "item": base_url + "/"},
            {"@type": "ListItem", "position": 2, "name": name, "item": base_url + "/" + cat + "/"}
        ]
    }
    
    # Related categories
    all_cats = list(cat_meta.keys())
    related_cats = [c for c in all_cats if c != cat][:8]
    
    # Build HTML
    parts = []
    parts.append('<!DOCTYPE html>')
    parts.append('<html lang="' + lang_attr + '">')
    parts.append('<head>')
    parts.append('<!-- Google tag (gtag.js) -->')
    parts.append('<script async src="https://www.googletagmanager.com/gtag/js?id=G-9W1157EBQV"></script>')
    parts.append('<script>')
    parts.append('  window.dataLayer = window.dataLayer || [];')
    parts.append('  function gtag(){dataLayer.push(arguments);}')
    parts.append("  gtag('js', new Date());")
    parts.append("  gtag('config', 'G-9W1157EBQV');")
    parts.append('</script>')
    parts.append('<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5998441792679372"')
    parts.append('     crossorigin="anonymous"></script>')
    parts.append('<meta charset="UTF-8">')
    parts.append('<meta name="viewport" content="width=device-width, initial-scale=1.0">')
    parts.append('<meta name="description" content="' + desc + ' ' + str(len(tools)) + ' free tools available.">')
    parts.append('<meta name="keywords" content="' + keywords + '">')
    parts.append('<title>Free Online ' + name + ' - ' + str(len(tools)) + '+ Tools | No Signup Required</title>')
    parts.append('<link rel="canonical" href="' + base_url + '/' + cat + '/">')
    parts.append('<meta property="og:title" content="Free Online ' + name + ' - ' + str(len(tools)) + '+ Tools">')
    parts.append('<meta property="og:description" content="' + desc + '">')
    parts.append('<meta property="og:url" content="' + base_url + '/' + cat + '/">')
    parts.append('<meta property="og:type" content="website">')
    parts.append('<meta property="og:site_name" content="' + site_name + '">')
    parts.append('<meta property="og:image" content="https://free-toolbase.com/og-image.svg">')
    parts.append('<meta name="twitter:card" content="summary_large_image">')
    parts.append('<meta name="twitter:title" content="Free Online ' + name + ' - ' + str(len(tools)) + '+ Tools">')
    parts.append('<meta name="twitter:description" content="' + desc + '">')
    parts.append('<meta name="twitter:image" content="https://free-toolbase.com/og-image.svg">')
    
    # Schema scripts
    parts.append('<script type="application/ld+json">')
    parts.append(json.dumps(collection_schema, ensure_ascii=False, indent=2))
    parts.append('</script>')
    parts.append('<script type="application/ld+json">')
    parts.append(json.dumps(itemlist_schema, ensure_ascii=False, indent=2))
    parts.append('</script>')
    parts.append('<script type="application/ld+json">')
    parts.append(json.dumps(faqpage_schema, ensure_ascii=False, indent=2))
    parts.append('</script>')
    parts.append('<script type="application/ld+json">')
    parts.append(json.dumps(breadcrumb_schema, ensure_ascii=False, indent=2))
    parts.append('</script>')
    
    # CSS
    parts.append('<style>')
    parts.append(CSS)
    parts.append('</style>')
    parts.append('</head>')
    parts.append('<body>')
    
    # Header
    parts.append('<header>')
    parts.append('  <div class="container">')
    parts.append('    <a href="' + tool_base + '/" class="logo">🔧 ' + site_name + '</a>')
    parts.append('    <nav>')
    parts.append('      <a href="' + tool_base + '/">' + home_text + '</a>')
    parts.append('    </nav>')
    parts.append('  </div>')
    parts.append('</header>')
    
    # Hero
    parts.append('<main class="container">')
    parts.append('  <section class="hero">')
    parts.append('    <h1>' + heading + '</h1>')
    parts.append('    <p>' + subheading + '</p>')
    parts.append('    <span class="count">' + tool_count_text + '</span>')
    parts.append('  </section>')
    
    # Trust signals
    parts.append('  <div class="trust">')
    parts.append('    <span>100% Free</span>')
    parts.append('    <span>No Signup</span>')
    parts.append('    <span>Client-Side Processing</span>')
    parts.append('    <span>No Data Upload</span>')
    parts.append('  </div>')
    
    # HowTo
    parts.append('  <section class="howto">')
    parts.append('    <h2>' + howto_title + '</h2>')
    parts.append('    <ol>')
    for step in howto_steps:
        parts.append('      <li>' + step + '</li>')
    parts.append('    </ol>')
    parts.append('  </section>')
    
    # Tools grid
    parts.append('  <section class="tools-grid">')
    for tool in sorted_tools:
        url = tool_base + '/' + tool['url'] + '/'
        desc_short = tool['desc'][:150]
        parts.append('    <div class="tool-card">')
        parts.append('      <div class="icon">' + tool['icon'] + '</div>')
        parts.append('      <h3>' + tool['name'] + '</h3>')
        parts.append('      <p>' + desc_short + '</p>')
        parts.append('      <a href="' + url + '">Use Now →</a>')
        parts.append('    </div>')
    parts.append('  </section>')
    
    # FAQ
    parts.append('  <section class="faq-section">')
    parts.append('    <h2>' + faq_title + '</h2>')
    for faq in faqs:
        parts.append('    <div class="faq-item">')
        parts.append('      <h3>' + faq['q'] + '</h3>')
        parts.append('      <p>' + faq['a'] + '</p>')
        parts.append('    </div>')
    parts.append('  </section>')
    
    # Related categories
    parts.append('  <section class="related">')
    parts.append('    <h2>' + related_title + '</h2>')
    parts.append('    <div class="related-links">')
    for rc in related_cats:
        rm = cat_meta.get(rc, {})
        ricon = rm.get('icon', '🔧')
        rname = rm.get('en_name' if lang == 'en' else 'cn_name', rc.title())
        rurl = tool_base + '/category/' + rc + '/'
        rcount = len(en_tools.get(rc, [])) if lang == 'en' else len(cn_tools.get(rc, []))
        parts.append('      <a href="' + rurl + '">' + ricon + ' ' + rname + ' (' + str(rcount) + ')</a>')
    parts.append('    </div>')
    parts.append('  </section>')
    
    parts.append('</main>')
    
    # Footer
    parts.append('<footer>')
    parts.append('  <p>© 2024-2026 ' + site_name + '. All tools are free and run entirely in your browser.</p>')
    parts.append('</footer>')
    parts.append('</body>')
    parts.append('</html>')
    
    return '\n'.join(parts)


# Generate pages
generated = 0
for cat in cat_meta:
    # EN page - use /en/category/{cat}/ to avoid conflicts with tool pages
    en_dir = os.path.join(BASE_DIR, 'en', 'category', cat)
    os.makedirs(en_dir, exist_ok=True)
    en_path = os.path.join(en_dir, 'index.html')
    tools = en_tools.get(cat, [])
    if tools:
        html = generate_category_page(cat, tools, 'en')
        with open(en_path, 'w') as f:
            f.write(html)
        generated += 1
        print('EN: ' + cat + ' -> ' + en_path + ' (' + str(len(tools)) + ' tools)')
    
    # CN page - use /category/{cat}/ to avoid conflicts with tool pages
    cn_dir = os.path.join(BASE_DIR, 'category', cat)
    os.makedirs(cn_dir, exist_ok=True)
    cn_path = os.path.join(cn_dir, 'index.html')
    cn_tool_list = cn_tools.get(cat, [])
    if cn_tool_list:
        html = generate_category_page(cat, cn_tool_list, 'cn')
        with open(cn_path, 'w') as f:
            f.write(html)
        generated += 1
        print('CN: ' + cat + ' -> ' + cn_path + ' (' + str(len(cn_tool_list)) + ' tools)')

print('\nGenerated ' + str(generated) + ' category pages (EN + CN)')
