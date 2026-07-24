#!/usr/bin/env python3
"""Update index.html and en/index.html with new tool cards"""
import re

BASE = "/home/chison/tools-site"

NEW_CARDS_CN = [
    ('🎨', 'RGB转HSL', '在线转换RGB颜色值到HSL格式，实时预览和一键复制', 'rgb-to-hsl/', 'new-tools'),
    ('🎨', 'HSV转RGB', '在线转换HSV颜色值到RGB/HEX格式，实时预览', 'hsv-to-rgb/', 'new-tools'),
    ('🎯', 'RGB转HSV', '在线转换RGB颜色值到HSV格式，实时预览和一键复制', 'rgb-to-hsv/', 'new-tools'),
    ('🗜️', 'SQL压缩美化', 'SQL压缩和格式化工具，支持多种SQL方言', 'sql-minifier/', 'new-tools'),
    ('📊', '百分比变化计算', '计算两个数值的百分比增减，支持反向推算', 'percent-change/', 'new-tools'),
]

NEW_CARDS_EN = [
    ('🎨', 'RGB to HSL', 'Convert RGB color values to HSL format with live preview', 'rgb-to-hsl/', 'new-tools'),
    ('🎨', 'HSV to RGB', 'Convert HSV color values to RGB/HEX format with live preview', 'hsv-to-rgb/', 'new-tools'),
    ('🎯', 'RGB to HSV', 'Convert RGB color values to HSV format with live preview', 'rgb-to-hsv/', 'new-tools'),
    ('🗜️', 'SQL Minifier', 'Compress and beautify SQL queries, supports multiple dialects', 'sql-minifier/', 'new-tools'),
    ('📊', '% Change Calculator', 'Calculate percentage increase/decrease with reverse calculation', 'percent-change/', 'new-tools'),
]

def card_html(icon, name, desc, url, cat):
    return f'<div class="tool-card" data-cat="{cat}"><span class="tool-icon">{icon}</span><span class="tool-name">{name}</span><span class="tool-desc">{desc}</span><a href="{url}" class="btn">立即使用</a></div>'

def card_html_en(icon, name, desc, url, cat):
    return f'<div class="tool-card" data-cat="{cat}"><span class="tool-icon">{icon}</span><span class="tool-name">{name}</span><span class="tool-desc">{desc}</span><a href="{url}" class="btn">Use Now</a></div>'

# Update Chinese index
with open(f"{BASE}/index.html", "r") as f:
    cn = f.read()

insert_marker = '<div class="tool-card" data-cat="new-tools"><span class="tool-icon">🎨</span><span class="tool-name">图片调色</span>'
cards_html = "\n".join(card_html(*c) for c in NEW_CARDS_CN)
cn = cn.replace(insert_marker, cards_html + "\n" + insert_marker)

with open(f"{BASE}/index.html", "w") as f:
    f.write(cn)

# Update English index
with open(f"{BASE}/en/index.html", "r") as f:
    en = f.read()

insert_marker_en = '<div class="tool-card" data-cat="new-tools"><span class="tool-icon">🎨</span><span class="tool-name">Tint Image'
cards_html_en = "\n".join(card_html_en(*c) for c in NEW_CARDS_EN)
en = en.replace(insert_marker_en, cards_html_en + "\n" + insert_marker_en)

with open(f"{BASE}/en/index.html", "w") as f:
    f.write(en)

print("✅ Index pages updated (CN + EN)")

# Update sitemap.xml
with open(f"{BASE}/sitemap.xml", "r") as f:
    sitemap = f.read()

new_urls = ""
for slug in ["rgb-to-hsl", "hsv-to-rgb", "rgb-to-hsv", "sql-minifier", "percent-change"]:
    new_urls += f"""  <url>
    <loc>https://free-toolbase.com/{slug}/</loc>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>
  <url>
    <loc>https://free-toolbase.com/en/{slug}/</loc>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>
"""

# Insert before closing </urlset>
sitemap = sitemap.replace("</urlset>", new_urls + "</urlset>")

with open(f"{BASE}/sitemap.xml", "w") as f:
    f.write(sitemap)

print("✅ Sitemap updated")

# Count total URLs in sitemap
url_count = sitemap.count("<loc>")
print(f"📊 Total URLs in sitemap: {url_count}")