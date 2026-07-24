#!/usr/bin/env python3
"""添加5个新工具到首页卡片和sitemap"""
import os, re, datetime

BASE = os.path.expanduser("~/tools-site")
TODAY = "2026-07-25"

NEW_TOOLS = [
    {"slug": "file-diff", "icon": "📂", "name_cn": "文件差异对比", "desc_cn": "在线文件差异对比，上传文件逐行高亮显示差异", "name_en": "File Diff Checker", "desc_en": "Compare files with line-by-line diff highlighting", "cat": "developer-tools"},
    {"slug": "css-selector-tester", "icon": "🎯", "name_cn": "CSS选择器测试", "desc_cn": "在线CSS选择器测试，输入HTML实时高亮匹配元素", "name_en": "CSS Selector Tester", "desc_en": "Test CSS selectors against HTML with real-time highlighting", "cat": "developer-tools"},
    {"slug": "xpath-tester", "icon": "🔍", "name_cn": "XPath测试器", "desc_cn": "在线XPath表达式测试，XML/HTML节点匹配查询", "name_en": "XPath Tester", "desc_en": "Test XPath expressions against XML/HTML code", "cat": "developer-tools"},
    {"slug": "html-encode-decode", "icon": "🔤", "name_cn": "HTML实体编码解码", "desc_cn": "在线HTML实体编码解码，三种格式特殊字符转义", "name_en": "HTML Entity Encoder", "desc_en": "Encode/decode HTML entities in named, decimal & hex formats", "cat": "developer-tools"},
    {"slug": "text-to-audio", "icon": "🔊", "name_cn": "文字转语音", "desc_cn": "在线文字转语音朗读，多语言语速音调调节", "name_en": "Text to Speech", "desc_en": "Convert text to speech with voice, speed & pitch control", "cat": "text-tools"},
]

def update_homepage(filepath, is_cn):
    """Insert tool cards at the top of the grid, after the first tool-card div"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find insertion point: right after the first tool-card line
    first_card_pattern = r'(<div class="tool-card"[^>]*>.*?</div>)'
    m = re.search(first_card_pattern, content, re.DOTALL)
    if not m:
        print(f"ERROR: Cannot find first tool-card in {filepath}")
        return

    insert_pos = m.start()  # insert BEFORE first card

    new_cards = []
    for t in NEW_TOOLS:
        if is_cn:
            card = f'<div class="tool-card" data-cat="{t["cat"]}"><span class="tool-icon">{t["icon"]}</span><span class="tool-name">{t["name_cn"]}</span><span class="tool-desc">{t["desc_cn"]}</span><a href="{t["slug"]}/" class="btn">立即使用</a></div>\n'
        else:
            card = f'<div class="tool-card" data-cat="{t["cat"]}"><span class="tool-icon">{t["icon"]}</span><span class="tool-name">{t["name_en"]}</span><span class="tool-desc">{t["desc_en"]}</span><a href="en/{t["slug"]}/" class="btn">Use Now</a></div>\n'
        new_cards.append(card)

    new_content = content[:insert_pos] + ''.join(new_cards) + content[insert_pos:]
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Updated {filepath}: added {len(NEW_TOOLS)} cards")


def update_sitemap():
    """Add new URLs to sitemap.xml"""
    sitemap_path = os.path.join(BASE, "sitemap.xml")
    with open(sitemap_path, 'r', encoding='utf-8') as f:
        content = f.read()

    new_urls = []
    for t in NEW_TOOLS:
        new_urls.append(f'''  <url>
    <loc>https://free-toolbase.com/{t["slug"]}/</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>''')
        new_urls.append(f'''  <url>
    <loc>https://free-toolbase.com/en/{t["slug"]}/</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>''')

    # Insert before </urlset>
    insert_text = '\n'.join(new_urls) + '\n'
    new_content = content.replace('</urlset>', insert_text + '</urlset>')

    with open(sitemap_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Updated sitemap.xml: added {len(new_urls)} URLs")


def update_tools_registry():
    """Update tools-registry.json"""
    reg_path = os.path.join(BASE, "tools-registry.json")
    with open(reg_path, 'r', encoding='utf-8') as f:
        registry = __import__('json').load(f)

    for t in NEW_TOOLS:
        entry = {
            "slug": t["slug"],
            "name_cn": t["name_cn"],
            "name_en": t["name_en"],
            "desc_cn": t["desc_cn"],
            "desc_en": t["desc_en"],
            "category": t["cat"],
            "icon": t["icon"],
            "date": TODAY,
            "has_en": True
        }
        registry["tools"].append(entry)

    registry["total_tools"] = len(registry["tools"])
    registry["count"] = len(registry["tools"])
    registry["updated_at"] = TODAY
    registry["updated"] = TODAY
    registry["last_updated"] = TODAY

    with open(reg_path, 'w', encoding='utf-8') as f:
        __import__('json').dump(registry, f, ensure_ascii=False, indent=2)
    print(f"Updated tools-registry.json: {registry['total_tools']} total tools")


def update_llms_txt():
    """Update llms.txt and llms-full.txt"""
    llms_path = os.path.join(BASE, "llms.txt")
    llms_full_path = os.path.join(BASE, "llms-full.txt")

    # llms.txt
    if os.path.exists(llms_path):
        with open(llms_path, 'r', encoding='utf-8') as f:
            content = f.read()
        # Update tool count in title
        content = re.sub(r'\d+\+ Free Online Tools', f'{2258+5}+ Free Online Tools', content)
        content = re.sub(r'Last updated: \d{4}-\d{2}-\d{2}', f'Last updated: {TODAY}', content)
        with open(llms_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("Updated llms.txt")

    # llms-full.txt
    if os.path.exists(llms_full_path):
        with open(llms_full_path, 'r', encoding='utf-8') as f:
            content = f.read()
        new_entries = ''
        for t in NEW_TOOLS:
            new_entries += f'{t["name_en"]}: {t["desc_en"]} | URL: https://free-toolbase.com/{t["slug"]}/\n'
        # Insert before footer
        content = content.replace('---\n\nTotal tools:', new_entries + '\n---\n\nTotal tools:')
        # Update count
        content = re.sub(r'Total tools: \d+', f'Total tools: {2258+5}', content)
        with open(llms_full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("Updated llms-full.txt")


if __name__ == "__main__":
    update_homepage(os.path.join(BASE, "index.html"), is_cn=True)
    update_homepage(os.path.join(BASE, "en", "index.html"), is_cn=False)
    update_sitemap()
    update_tools_registry()
    update_llms_txt()
    print("\nAll updates complete!")