#!/usr/bin/env python3
"""批量更新首页：插入新工具卡片 + 更新工具数量"""
import re

NEW_TOOLS = [
    # (中文目录, 中文名, 英文名, 分类, 图标, 描述)
    ('precious-metal-calculator', '贵金属价值计算器', 'Precious Metal Calculator', 'calc-tools', '💎',
     '黄金/白银/铂金/钯金价值计算，输入重量纯度自动计算'),
    ('gross-net-salary-calculator', '税前税后工资计算器', 'Gross to Net Salary Calculator', 'calc-tools', '💰',
     '扣除五险一金和个人所得税，计算实际到手工资'),
    ('currency-weight-calculator', '货币重量计算器', 'Currency Weight Calculator', 'calc-tools', '💵',
     '计算纸币和硬币总重量和价值，支持人民币美元欧元日元英镑'),
    ('stock-split-calculator', '股票分割计算器', 'Stock Split Calculator', 'calc-tools', '📊',
     '计算股票分割后股数和成本价变化'),
    ('overtime-pay-calculator', '加班费计算器', 'Overtime Pay Calculator', 'calc-tools', '⏰',
     '根据工时和倍率计算加班工资'),
]

EN_NEW_TOOLS = [
    ('precious-metal-calculator', 'Precious Metal Calculator', 'calc-tools', '💎',
     'Calculate gold, silver, platinum, palladium value by weight and purity'),
    ('gross-net-salary-calculator', 'Gross to Net Salary Calculator', 'calc-tools', '💰',
     'Calculate take-home pay after social insurance, housing fund and tax deductions'),
    ('currency-weight-calculator', 'Currency Weight Calculator', 'calc-tools', '💵',
     'Calculate total weight and value of banknotes and coins for CNY/USD/EUR/JPY/GBP'),
    ('stock-split-calculator', 'Stock Split Calculator', 'calc-tools', '📊',
     'Calculate post-split shares and adjusted cost basis'),
    ('overtime-pay-calculator', 'Overtime Pay Calculator', 'calc-tools', '⏰',
     'Calculate overtime pay based on hours and rate multipliers'),
]

def update_cn_index():
    path = 'index.html'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if already added
    for tool_dir, cn_name, en_name, cat, icon, desc in NEW_TOOLS:
        if f'/{tool_dir}/' in content:
            print(f"  SKIP (already in CN index): {tool_dir}")
            continue

        card = f'<div class="tool-card" data-category="{cat}"><span class="tool-title">{icon} {cn_name}</span><p class="tool-desc">免费在线{cn_name}，{desc}。无需注册，数据不上传服务器。</p><a href="/{tool_dir}/" class="btn">使用工具</a></div>'

        # Insert before first closing tag of tools section or before footer
        # Insert before <div class="footer"
        insert_marker = '<div class="footer"'
        if insert_marker in content:
            content = content.replace(insert_marker, card + '\n' + insert_marker, 1)
            print(f"  ADDED to CN index: {tool_dir}")
        else:
            print(f"  FAILED to find insert point for: {tool_dir}")

    # Update tool count: 3081 -> 3086
    content = re.sub(r'3081\+个免费工具', '3086+个免费工具', content)
    content = re.sub(r'>3081<', '>3086<', content)
    # Update all mentions of 3081
    content = content.replace('3081+', '3086+')
    content = content.replace('3081个', '3086个')

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("CN index.html updated")

def update_en_index():
    path = 'en/index.html'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    for tool_dir, en_name, cat, icon, desc in EN_NEW_TOOLS:
        if f'/en/{tool_dir}/' in content or f'/{tool_dir}/' in content:
            print(f"  SKIP (already in EN index): {tool_dir}")
            continue

        card = f'<div class="tool-card" data-category="{cat}"><span class="tool-title">{icon} {en_name}</span><p class="tool-desc">Free online {en_name}. {desc}. No registration, data never uploaded.</p><a href="/en/{tool_dir}/" class="btn">Use Tool</a></div>'

        insert_marker = '<div class="footer"'
        if insert_marker in content:
            content = content.replace(insert_marker, card + '\n' + insert_marker, 1)
            print(f"  ADDED to EN index: {tool_dir}")
        else:
            print(f"  FAILED to find insert point for: {tool_dir}")

    content = re.sub(r'3083\+ Free Tools', '3088+ Free Tools', content)
    content = re.sub(r'>3083<', '>3088<', content)
    content = content.replace('3083+', '3088+')
    content = content.replace('3083个', '3088个')

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("EN index.html updated")

def update_sitemap():
    """Add new URLs to sitemap.xml"""
    path = 'sitemap.xml'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    new_urls = []
    for tool_dir, cn_name, en_name, cat, icon, desc in NEW_TOOLS:
        cn_url = f'  <url><loc>https://free-toolbase.com/{tool_dir}/</loc><changefreq>monthly</changefreq><priority>0.7</priority></url>'
        en_url = f'  <url><loc>https://free-toolbase.com/en/{tool_dir}/</loc><changefreq>monthly</changefreq><priority>0.7</priority></url>'
        if f'{tool_dir}/' not in content:
            new_urls.append(cn_url)
            new_urls.append(en_url)

    if new_urls:
        insert_before = '</urlset>'
        insert_text = '\n'.join(new_urls) + '\n'
        content = content.replace(insert_before, insert_text + insert_before)
        print(f"  ADDED {len(new_urls)} URLs to sitemap")
    else:
        print("  All URLs already in sitemap")

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("sitemap.xml updated")

if __name__ == '__main__':
    print("=== Updating CN index ===")
    update_cn_index()
    print("\n=== Updating EN index ===")
    update_en_index()
    print("\n=== Updating sitemap ===")
    update_sitemap()
    print("\n✅ Done")