#!/usr/bin/env python3
"""Add truly missing tool cards and regenerate sitemap"""
import re, os

INDEX = "/opt/project/index.html"
EN_INDEX = "/opt/project/en/index.html"

# Only truly missing tools (verified)
cn_tools = [
    {
        "href": "coupon-code-generator",
        "cats": "实用工具",
        "icon": "🏷️",
        "title": "优惠券码生成器 · Coupon Code Generator",
        "desc": "免费在线优惠券码生成器，支持自定义前缀、长度、数量和字符类型。一键生成批量优惠码、折扣码、促销码，支持分隔符和去重。纯前端本地生成，适合电商促销和会员营销。",
        "tag": "实用工具"
    },
    {
        "href": "heatmap-generator",
        "cats": "设计工具",
        "icon": "🗺️",
        "title": "热力图生成器 · Heatmap Generator",
        "desc": "免费在线热力图生成器，将数据矩阵可视化为彩色热力图。支持多种配色方案、自定义数据标签、高清PNG导出。纯前端本地生成，数据不上传服务器。适合数据分析、可视化报告和学术研究。",
        "tag": "设计工具"
    },
    {
        "href": "pdf-password-protect",
        "cats": "办公工具",
        "icon": "🔐",
        "title": "PDF加密工具 · PDF Password Protect",
        "desc": "免费在线PDF加密工具，为PDF文件添加密码保护。支持设置打开密码和权限密码（限制打印、复制、编辑），纯前端本地加密，文件不上传服务器。",
        "tag": "办公工具"
    },
    {
        "href": "spin-wheel-picker",
        "cats": "趣味工具",
        "icon": "🎡",
        "title": "转盘抽选器 · Spin Wheel Picker",
        "desc": "免费在线转盘抽选器，自定义选项名称、数量和配色方案。支持添加/删除/清空选项，使用Crypto API随机抽选。适合课堂点名、抽奖、日常决策等场景。纯前端本地处理。",
        "tag": "趣味工具"
    }
]

en_tools = [
    {
        "href": "../coupon-code-generator",
        "cats": "utility",
        "icon": "🏷️",
        "title": "Coupon Code Generator",
        "desc": "Free online coupon code generator with customizable prefix, length, quantity and character types. Generate bulk discount codes instantly. Pure frontend, no data upload.",
        "tag": "utility"
    },
    {
        "href": "../heatmap-generator",
        "cats": "design",
        "icon": "🗺️",
        "title": "Heatmap Generator",
        "desc": "Free online heatmap generator for data matrix visualization. Supports multiple color schemes, custom labels, and high-res PNG export. Pure frontend, no data upload.",
        "tag": "design"
    },
    {
        "href": "../pdf-password-protect",
        "cats": "office",
        "icon": "🔐",
        "title": "PDF Password Protect",
        "desc": "Free online PDF encryption tool. Add password protection to PDF files - set open password and permissions (restrict printing, copying, editing). Pure frontend, no upload.",
        "tag": "office"
    },
    {
        "href": "../spin-wheel-picker",
        "cats": "utility",
        "icon": "🎡",
        "title": "Spin Wheel Picker",
        "desc": "Free online spin wheel picker with customizable options and colors. Supports add/edit/delete options, random selection. Great for classroom, raffles, and daily decisions.",
        "tag": "utility"
    }
]

def add_cards(filepath, tools, link_text):
    with open(filepath) as f:
        content = f.read()
    
    # Check which tools already exist
    existing = set()
    for t in tools:
        href_clean = t['href'].replace('../', '')
        if f'href="{href_clean}/"' in content or f'href="{t["href"]}/"' in content:
            existing.add(t['href'])
            print(f"  SKIP (exists): {href_clean}")
    
    # Build new cards for truly missing
    new_cards = ""
    added = 0
    for tool in tools:
        if tool['href'] in existing:
            continue
        card = f"""    <div class="tool-card" data-cats="{tool['cats']}">
      <div class="icon">{tool['icon']}</div>
      <h3>{tool['title']}</h3>
      <p>{tool['desc']}</p>
      <div class="tool-meta"><span>{tool['tag']}</span><span class="new-tag">NEW</span></div>
      <a href="{tool['href']}/">{link_text}</a>
    </div>"""
        new_cards += card + "\n"
        added += 1
    
    if not new_cards:
        print("  Nothing to add")
        return 0
    
    # Find insertion point: after the last tool-card
    last_card_start = content.rfind('<div class="tool-card"')
    if last_card_start < 0:
        print("  ERROR: No tool cards found")
        return 0
    
    # Count nested divs to find the end
    depth = 0
    insert_pos = -1
    for i in range(last_card_start, min(last_card_start + 2000, len(content))):
        if content[i:i+5] == '<div ' or content[i:i+4] == '<div>':
            depth += 1
        elif content[i:i+6] == '</div>':
            depth -= 1
            if depth == 0:
                insert_pos = i + 6
                break
    
    if insert_pos < 0:
        print("  ERROR: Could not find insertion point")
        return 0
    
    content = content[:insert_pos] + "\n" + new_cards + content[insert_pos:]
    
    with open(filepath, 'w') as f:
        f.write(content)
    
    print(f"  Added {added} cards")
    return added

print("=== Adding to Chinese index ===")
cn_added = add_cards(INDEX, cn_tools, "立即使用")

print("\n=== Adding to English index ===")
en_added = add_cards(EN_INDEX, en_tools, "Use Now")

# Verify
print("\n=== Verification ===")
for fp, name in [(INDEX, "Chinese"), (EN_INDEX, "English")]:
    with open(fp) as f:
        content = f.read()
    hrefs = re.findall(r'href="([^"]+)/">', content)
    tool_hrefs = [h for h in hrefs if not h.startswith('http') and not h.startswith('#') and not h.startswith('en/')]
    print(f"{name}: {len(tool_hrefs)} tool links, {len(set(tool_hrefs))} unique")
