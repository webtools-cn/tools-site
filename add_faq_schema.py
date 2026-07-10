#!/usr/bin/env python3
"""
Batch add FAQPage Schema to tool pages that only have SoftwareApplication (no FAQ).
Generates 4-6 FAQ Q&A pairs based on page metadata.
Processes both zh-CN and en pages.
"""
import os
import re
import json
import html

SITE = "/opt/project"

# Generic FAQ templates for zh-CN
FAQ_TEMPLATES_ZH = [
    {
        "q_pattern": "{name}是免费的吗？",
        "a_pattern": "是的，{name}完全免费使用，无需注册，无需登录，所有功能都可以直接使用。"
    },
    {
        "q_pattern": "使用{name}时数据会上传到服务器吗？",
        "a_pattern": "不会。{name}采用纯前端技术，所有处理都在你的浏览器中完成，数据不会上传到任何服务器。即使断开网络，工具也能正常使用。"
    },
    {
        "q_pattern": "{name}支持手机端使用吗？",
        "a_pattern": "支持。{name}采用响应式设计，可以在手机、平板和电脑上正常使用，界面会自动适配屏幕大小。"
    },
    {
        "q_pattern": "{name}需要安装软件吗？",
        "a_pattern": "不需要。{name}是一个在线工具，直接在浏览器中打开网页即可使用，无需下载安装任何软件或插件。"
    },
    {
        "q_pattern": "使用{name}处理的数据安全吗？",
        "a_pattern": "安全。由于所有数据都在你的浏览器本地处理，不会经过任何服务器，因此不存在数据泄露的风险。你的数据始终在你的掌控之中。"
    },
    {
        "q_pattern": "{name}有什么使用限制吗？",
        "a_pattern": "{name}是免费在线工具，没有使用次数限制。由于采用纯前端处理，处理速度取决于你的设备性能。对于超大文件，建议分批处理以获得最佳体验。"
    },
]

# Generic FAQ templates for en
FAQ_TEMPLATES_EN = [
    {
        "q_pattern": "Is {name} free to use?",
        "a_pattern": "Yes, {name} is completely free to use. No registration or login required — all features are available directly."
    },
    {
        "q_pattern": "Does {name} upload my data to a server?",
        "a_pattern": "No. {name} uses pure front-end technology. All processing happens in your browser — no data is uploaded to any server. The tool works even without an internet connection."
    },
    {
        "q_pattern": "Can I use {name} on my phone?",
        "a_pattern": "Yes. {name} is fully responsive and works on phones, tablets, and desktops. The interface automatically adapts to your screen size."
    },
    {
        "q_pattern": "Do I need to install any software to use {name}?",
        "a_pattern": "No. {name} is an online tool — just open the webpage in your browser. No downloads, plugins, or installations needed."
    },
    {
        "q_pattern": "Is my data safe when using {name}?",
        "a_pattern": "Yes. Since all data is processed locally in your browser and never sent to any server, there is no risk of data leakage. Your data stays under your control at all times."
    },
    {
        "q_pattern": "Are there any usage limits for {name}?",
        "a_pattern": "{name} is a free online tool with no usage limits. Since processing is done locally, performance depends on your device. For very large files, we recommend processing in batches for the best experience."
    },
]


def extract_title(soup_text):
    """Extract tool name from <title> tag."""
    m = re.search(r'<title>(.*?)</title>', soup_text, re.IGNORECASE | re.DOTALL)
    if m:
        title = m.group(1).strip()
        # Remove common suffixes
        for suffix in [' · 免费在线工具', ' · Free Online Tool', ' - 在线', ' - Online', ' | 免费在线工具', ' | Free Online Tool']:
            title = title.replace(suffix, '')
        # Take first part before separator if too long
        if len(title) > 40:
            parts = re.split(r'[·\-–—|]', title)
            title = parts[0].strip()
        return title
    return "此工具"


def extract_name_en(soup_text):
    """Extract English tool name from <title> tag."""
    m = re.search(r'<title>(.*?)</title>', soup_text, re.IGNORECASE | re.DOTALL)
    if m:
        title = m.group(1).strip()
        for suffix in [' · Free Online Tool', ' · Free Tool', ' - Online', ' | Free Online Tool', ' | Free Tool']:
            title = title.replace(suffix, '')
        if len(title) > 50:
            parts = re.split(r'[·\-–—|]', title)
            title = parts[0].strip()
        return title
    return "This tool"


def generate_faq_schema_zh(name):
    """Generate FAQPage JSON-LD for zh-CN page."""
    faqs = []
    for tmpl in FAQ_TEMPLATES_ZH:
        q = tmpl["q_pattern"].format(name=name)
        a = tmpl["a_pattern"].format(name=name)
        faqs.append({
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {
                "@type": "Answer",
                "text": a
            }
        })
    schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": faqs
    }
    return json.dumps(schema, ensure_ascii=False, indent=2)


def generate_faq_schema_en(name):
    """Generate FAQPage JSON-LD for en page."""
    faqs = []
    for tmpl in FAQ_TEMPLATES_EN:
        q = tmpl["q_pattern"].format(name=name)
        a = tmpl["a_pattern"].format(name=name)
        faqs.append({
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {
                "@type": "Answer",
                "text": a
            }
        })
    schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": faqs
    }
    return json.dumps(schema, ensure_ascii=False, indent=2)


def add_faq_to_page(filepath):
    """Add FAQ Schema to a page that doesn't have one."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Skip if already has FAQ
    if 'FAQPage' in content:
        return False
    
    # Determine language
    is_en = 'lang="en"' in content or 'lang="en-US"' in content
    
    # Extract tool name
    if is_en:
        name = extract_name_en(content)
        faq_schema = generate_faq_schema_en(name)
    else:
        name = extract_title(content)
        faq_schema = generate_faq_schema_zh(name)
    
    # Insert FAQ schema after SoftwareApplication schema or before </head>
    faq_script = f'<script type="application/ld+json">\n{faq_schema}\n</script>'
    
    # Try to insert after the last </script> that contains ld+json
    # Find the last application/ld+json script block
    pattern = r'(<script type="application/ld\+json">.*?</script>)'
    matches = list(re.finditer(pattern, content, re.DOTALL))
    
    if matches:
        last_match = matches[-1]
        insert_pos = last_match.end()
        content = content[:insert_pos] + '\n' + faq_script + content[insert_pos:]
    else:
        # Insert before </head>
        content = content.replace('</head>', faq_script + '\n</head>', 1)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True


def main():
    count_zh = 0
    count_en = 0
    errors = 0
    
    # Process zh-CN pages (not in /en/ subdirectory)
    for root, dirs, files in os.walk(SITE):
        # Skip .git and en directories at top level
        if '/.git' in root:
            continue
        if '/en/' in root and root.startswith(os.path.join(SITE, 'en')):
            continue
        
        if 'index.html' not in files:
            continue
        
        filepath = os.path.join(root, 'index.html')
        
        # Skip the main index
        if filepath == os.path.join(SITE, 'index.html'):
            continue
        
        try:
            if add_faq_to_page(filepath):
                is_en = '/en/' in filepath
                if is_en:
                    count_en += 1
                else:
                    count_zh += 1
        except Exception as e:
            errors += 1
            print(f"Error processing {filepath}: {e}")
    
    # Process en pages
    en_dir = os.path.join(SITE, 'en')
    if os.path.isdir(en_dir):
        for root, dirs, files in os.walk(en_dir):
            if '/.git' in root:
                continue
            if 'index.html' not in files:
                continue
            filepath = os.path.join(root, 'index.html')
            if filepath == os.path.join(en_dir, 'index.html'):
                continue
            try:
                if add_faq_to_page(filepath):
                    count_en += 1
            except Exception as e:
                errors += 1
                print(f"Error processing {filepath}: {e}")
    
    print(f"\n=== Summary ===")
    print(f"zh-CN pages updated: {count_zh}")
    print(f"en pages updated: {count_en}")
    print(f"Total updated: {count_zh + count_en}")
    print(f"Errors: {errors}")


if __name__ == "__main__":
    main()
