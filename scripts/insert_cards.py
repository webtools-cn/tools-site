#!/usr/bin/env python3
"""在CN和EN首页插入新工具卡片"""
import re

tools_cn = [
    ('dns-records', '🌐', 'DNS记录查询', '查询域名A/AAAA/CNAME/MX/NS/TXT等DNS记录', '网络工具'),
    ('email-verifier', '📧', '邮箱验证器', '验证邮箱格式，检测临时邮箱和域名有效性', '文本工具'),
    ('screen-resolution-checker', '🖥️', '屏幕分辨率检测', '检测屏幕分辨率、视口尺寸、DPR、色彩深度', '开发工具'),
    ('viewport-checker', '📐', '视口检测器', '实时检测视口尺寸，支持响应式断点预设', '开发工具'),
    ('cookie-analyzer', '🍪', 'Cookie分析器', '查看和管理当前网站Cookie，保护隐私', '开发工具'),
    ('localstorage-viewer', '💾', 'LocalStorage浏览器', '查看管理浏览器LocalStorage数据，支持导出', '开发工具'),
    ('sessionstorage-viewer', '📋', 'SessionStorage浏览器', '查看管理浏览器SessionStorage，会话自动清除', '开发工具'),
    ('tap-code-translator', '🔢', '敲击码翻译器', 'Tap Code编码解码，5×5网格密码转换', '加密工具'),
    ('leet-speak-generator', '💻', 'Leet Speak生成器', '文本转1337黑客语言，支持多种替换级别', '文本工具'),
    ('google-fonts-preview', '🔤', 'Google Fonts预览', '搜索预览上千种免费字体，实时调整字重字号', '设计工具'),
    ('icon-finder', '🔍', '图标搜索器', '搜索复制Emoji和Unicode符号，分类浏览', '文本工具'),
]

tools_en = [
    ('dns-records', '🌐', 'DNS Records Lookup', 'Query A/AAAA/CNAME/MX/NS/TXT DNS records', 'Network Tools'),
    ('email-verifier', '📧', 'Email Verifier', 'Validate email format, detect disposable addresses', 'Text Tools'),
    ('screen-resolution-checker', '🖥️', 'Screen Resolution Checker', 'Check screen resolution, viewport, DPR, color depth', 'Dev Tools'),
    ('viewport-checker', '📐', 'Viewport Checker', 'Real-time viewport size with responsive breakpoints', 'Dev Tools'),
    ('cookie-analyzer', '🍪', 'Cookie Analyzer', 'View and manage website cookies, protect privacy', 'Dev Tools'),
    ('localstorage-viewer', '💾', 'LocalStorage Viewer', 'View/manage LocalStorage data, export as JSON', 'Dev Tools'),
    ('sessionstorage-viewer', '📋', 'SessionStorage Viewer', 'View/manage SessionStorage, auto-clears on session end', 'Dev Tools'),
    ('tap-code-translator', '🔢', 'Tap Code Translator', 'Encode/decode Tap Code with 5×5 grid cipher', 'Encryption Tools'),
    ('leet-speak-generator', '💻', 'Leet Speak Generator', 'Convert text to 1337 hacker speak, multiple levels', 'Text Tools'),
    ('google-fonts-preview', '🔤', 'Google Fonts Preview', 'Search and preview 1000+ free fonts, adjust weight/size', 'Design Tools'),
    ('icon-finder', '🔍', 'Icon Finder', 'Search and copy Emoji & Unicode symbols by category', 'Text Tools'),
]

cat_map_cn = {
    '网络工具': 'network-tools', '文本工具': 'text-tools', '开发工具': 'dev-tools',
    '加密工具': 'encryption-tools', '设计工具': 'design-tools',
}
cat_map_en = {
    'Network Tools': 'network-tools', 'Text Tools': 'text-tools', 'Dev Tools': 'dev-tools',
    'Encryption Tools': 'encryption-tools', 'Design Tools': 'design-tools',
}

def make_card(slug, icon, name, desc, cat, cat_map):
    data_cat = cat_map.get(cat, 'utility-tools')
    return f'<div class="tool-card" data-category="{data_cat}"><span class="tool-icon">{icon}</span><span class="tool-name">{name}</span><span class="tool-desc">{desc}</span><a href="/{slug}/" class="btn">立即使用</a></div>'

def make_card_en(slug, icon, name, desc, cat, cat_map):
    data_cat = cat_map.get(cat, 'utility-tools')
    return f'<div class="tool-card" data-category="{data_cat}"><span class="tool-icon">{icon}</span><span class="tool-name">{name}</span><span class="tool-desc">{desc}</span><a href="/en/{slug}/" class="btn">Use Now</a></div>'

# CN首页：在最后一张卡片后插入（找tools-grid内最后的tool-card）
with open('index.html', 'r') as f:
    cn_html = f.read()

# 找tools-grid内部最后一张卡片
grid_match = re.search(r'(<div class="tools-grid"[^>]*>)(.*?)(</div>\s*(?:<!--|$))', cn_html, re.DOTALL)
if not grid_match:
    # try alternative
    parts = cn_html.split('</div>')
    print("Cannot find tools-grid end")

# 更简单的方法：在tools-grid结束前插入
# 找到最后一个tool-card后面的位置
new_cards = '\n'.join(make_card(*t, cat_map_cn) for t in tools_cn)
# 找到 tools-grid 结束标签
end_marker = '  </div>\n  <div class="search-section"'
if end_marker not in cn_html:
    # fallback
    end_marker = '  </div>\n\n  <div class="search-section"'
if end_marker not in cn_html:
    end_marker = '</div>\n\n  <div class="search-section"'
    
# 在 tools-grid 的 </div> 前插入
cn_html = cn_html.replace(end_marker, '\n' + new_cards + '\n' + end_marker)
with open('index.html', 'w') as f:
    f.write(cn_html)

# EN首页
with open('en/index.html', 'r') as f:
    en_html = f.read()

new_cards_en = '\n'.join(make_card_en(*t, cat_map_en) for t in tools_en)
en_end_marker = '  </div>\n  <div class="search-section"'
if en_end_marker not in en_html:
    en_end_marker = '  </div>\n\n  <div class="search-section"'
if en_end_marker not in en_html:
    en_end_marker = '</div>\n\n  <div class="search-section"'

en_html = en_html.replace(en_end_marker, '\n' + new_cards_en + '\n' + en_end_marker)
with open('en/index.html', 'w') as f:
    f.write(en_html)

print("✅ 卡片插入完成")
print(f"CN卡片: {cn_html.count('tool-card')}")
print(f"EN卡片: {en_html.count('tool-card')}")