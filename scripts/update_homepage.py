#!/usr/bin/env python3
"""Insert 10 new tool cards into CN and EN homepages, update counts, sitemap"""
import re

BASE = '/home/chison/tools-site'

NEW_CN_CARDS = [
    ('dev-tools', '🔧', 'JS代码格式化', 'JavaScript代码美化，支持缩进、括号换行、空格优化', '/js-beautify/'),
    ('dev-tools', '🎨', 'CSS代码格式化', 'CSS样式表美化，支持缩进、属性排序、选择器分组', '/css-beautify/'),
    ('dev-tools', '🏗️', 'HTML代码格式化', 'HTML代码美化，支持缩进、标签闭合检查、属性排序', '/html-beautify/'),
    ('dev-tools', '📐', '屏幕分辨率测试', '实时检测屏幕分辨率、像素比、色深、窗口大小', '/screen-resolution-test/'),
    ('dev-tools', '🌐', '路由追踪', '可视化网络路径追踪，诊断延迟和路由问题', '/traceroute/'),
    ('dev-tools', '🔍', 'Open Graph调试器', 'OG标签解析和社交媒体分享预览', '/open-graph-debugger/'),
    ('dev-tools', '🖼️', '占位图生成器', '自定义尺寸/颜色/文字，生成占位图片', '/placeholder-image/'),
    ('utility-tools', '⏳', '倒计时计算器', '计算距目标日期的天/小时/分钟，含节假日预设', '/days-until/'),
    ('dev-tools', '🔐', 'Bcrypt密码验证', '验证bcrypt哈希、检测轮数、分析格式', '/bcrypt-checker/'),
    ('dev-tools', '🔧', 'Unix权限计算器', '可视化设置rwx权限，生成chmod命令', '/unix-permissions-calculator/'),
]

NEW_EN_CARDS = [
    ('dev-tools', '🔧', 'JS Code Beautifier', 'JavaScript formatter with indent, braces, semicolons', '/en/js-beautify/'),
    ('dev-tools', '🎨', 'CSS Code Beautifier', 'CSS formatter with indent, sort, property grouping', '/en/css-beautify/'),
    ('dev-tools', '🏗️', 'HTML Code Beautifier', 'HTML formatter with indent, tag closure, attribute sort', '/en/html-beautify/'),
    ('dev-tools', '📐', 'Screen Resolution Test', 'Real-time screen resolution, DPR, color depth detection', '/en/screen-resolution-test/'),
    ('dev-tools', '🌐', 'Traceroute', 'Visual network path tracing and latency diagnostics', '/en/traceroute/'),
    ('dev-tools', '🔍', 'Open Graph Debugger', 'OG tag parsing and social media share previews', '/en/open-graph-debugger/'),
    ('dev-tools', '🖼️', 'Placeholder Image', 'Custom size/color/text placeholder image generator', '/en/placeholder-image/'),
    ('utility-tools', '⏳', 'Countdown Calculator', 'Days/hours/minutes until target date with holiday presets', '/en/days-until/'),
    ('dev-tools', '🔐', 'Bcrypt Checker', 'Verify bcrypt hashes, detect rounds, analyze format', '/en/bcrypt-checker/'),
    ('dev-tools', '🔧', 'Unix Permissions Calculator', 'Visual rwx permission setting, chmod command generation', '/en/unix-permissions-calculator/'),
]

def generate_card(cat, icon, name, desc, href):
    return f'<div class="tool-card" data-cat="{cat}"><span class="tool-icon">{icon}</span><span class="tool-name">{name}</span><span class="tool-desc">{desc}</span><a href="{href}" class="btn">立即使用</a></div>'

def generate_card_en(cat, icon, name, desc, href):
    return f'<div class="tool-card" data-cat="{cat}"><span class="tool-icon">{icon}</span><span class="tool-name">{name}</span><span class="tool-desc">{desc}</span><a href="{href}" class="btn">Use Now</a></div>'

# Update CN homepage
print("=== CN Homepage ===")
cn_path = f'{BASE}/index.html'
with open(cn_path, 'r') as f:
    cn = f.read()

# Find last tool-card before </div> + <script>
# Insert before the last empty line before <script>
marker = '\n<script>\n// Make tool cards clickable'
new_cards = '\n'.join(generate_card(*c) for c in NEW_CN_CARDS)
cn = cn.replace(marker, '\n' + new_cards + '\n' + marker)

# Update count
old_count = len(re.findall(r'class="tool-card"', cn)) - len(NEW_CN_CARDS)  # count before insertion
new_count = len(re.findall(r'class="tool-card"', cn))
print(f"Cards: {old_count} → {new_count}")

# Update stat number
cn = re.sub(r'<span class="stat-number">\d+\+?</span><span class="stat-label">免费在线工具</span>',
            f'<span class="stat-number">{new_count}+</span><span class="stat-label">免费在线工具</span>', cn)

with open(cn_path, 'w') as f:
    f.write(cn)
print(f"Written: {cn_path}")

# Update EN homepage
print("\n=== EN Homepage ===")
en_path = f'{BASE}/en/index.html'
with open(en_path, 'r') as f:
    en = f.read()

# Find insertion point
marker_en = '\n<script>\n// Make tool cards clickable'
new_cards_en = '\n'.join(generate_card_en(*c) for c in NEW_EN_CARDS)
en = en.replace(marker_en, '\n' + new_cards_en + '\n' + marker_en)

old_en = len(re.findall(r'class="tool-card"', en)) - len(NEW_EN_CARDS)
new_en = len(re.findall(r'class="tool-card"', en))
print(f"Cards: {old_en} → {new_en}")

# Update stat number
en = re.sub(r'<span class="stat-number">\d+\+?</span><span class="stat-label">free online tools</span>',
            f'<span class="stat-number">{new_en}+</span><span class="stat-label">free online tools</span>', en, flags=re.IGNORECASE)
en = re.sub(r'<span class="stat-number">\d+\+?</span><span class="stat-label">browser-based utilities</span>',
            f'<span class="stat-number">{new_en}+</span><span class="stat-label">browser-based utilities</span>', en, flags=re.IGNORECASE)

with open(en_path, 'w') as f:
    f.write(en)
print(f"Written: {en_path}")

# Verify
cn_final = len(re.findall(r'class="tool-card"', open(cn_path).read()))
en_final = len(re.findall(r'class="tool-card"', open(en_path).read()))
print(f"\n=== VERIFY ===")
print(f"CN cards: {cn_final}")
print(f"EN cards: {en_final}")
print(f"Match: {'✅' if cn_final == en_final else '❌ MISMATCH!'}")

# Update sitemap.xml
print("\n=== Sitemap ===")
sitemap_path = f'{BASE}/sitemap.xml'
with open(sitemap_path, 'r') as f:
    sitemap = f.read()

new_urls = ''
for _, _, name, _, href in NEW_CN_CARDS:
    new_urls += f'  <url><loc>https://free-toolbase.com{href}</loc></url>\n'
    en_href = href.replace('/js-beautify/', '/en/js-beautify/') if '/js-beautify/' in href else \
              href.replace('/css-beautify/', '/en/css-beautify/') if '/css-beautify/' in href else \
              href.replace('/html-beautify/', '/en/html-beautify/') if '/html-beautify/' in href else \
              href.replace('/screen-resolution-test/', '/en/screen-resolution-test/') if '/screen-resolution-test/' in href else \
              href.replace('/traceroute/', '/en/traceroute/') if '/traceroute/' in href else \
              href.replace('/open-graph-debugger/', '/en/open-graph-debugger/') if '/open-graph-debugger/' in href else \
              href.replace('/placeholder-image/', '/en/placeholder-image/') if '/placeholder-image/' in href else \
              href.replace('/days-until/', '/en/days-until/') if '/days-until/' in href else \
              href.replace('/bcrypt-checker/', '/en/bcrypt-checker/') if '/bcrypt-checker/' in href else \
              href.replace('/unix-permissions-calculator/', '/en/unix-permissions-calculator/')
    new_urls += f'  <url><loc>https://free-toolbase.com{en_href}</loc></url>\n'

# Insert before </urlset>
sitemap = sitemap.replace('</urlset>', new_urls + '</urlset>')
with open(sitemap_path, 'w') as f:
    f.write(sitemap)
url_count = sitemap.count('<loc>')
print(f"Sitemap URLs: {url_count}")

print("\n✅ Done!")