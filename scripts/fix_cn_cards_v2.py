#!/usr/bin/env python3
"""精确在tools-grid闭合前插入卡片"""
import re

extra_cn = [
    ('csr-generator', '🔐', 'CSR生成器', '在线生成证书签名请求CSR和RSA私钥，纯前端本地处理', 'security-tools'),
    ('keycode-info', '⌨️', '键盘码查询器', '按下任意键查看keyCode/key/code值，前端开发必备', 'dev-tools'),
    ('mimetype-checker', '📁', 'MIME类型查询', '查询600+文件扩展名对应的MIME/Content-Type', 'dev-tools'),
    ('url-encoder-decode', '🔗', 'URL编解码工具', 'URL编码(encodeURIComponent)和解码双向转换', 'dev-tools'),
]

def make_card(slug, icon, name, desc, cat):
    return f'<div class="tool-card" data-category="{cat}"><span class="tool-icon">{icon}</span><span class="tool-name">{name}</span><span class="tool-desc">{desc}</span><a href="/{slug}/" class="btn">立即使用</a></div>'

# CN
with open('index.html', 'r') as f:
    cn = f.read()

# Find tools-grid closing div
# The pattern: last tool-card inside tools-grid, then </div>\n</div>
# Find the position of </div>\n</div> after the tools-grid
new_cards = '\n'.join(make_card(*t) for t in extra_cn)

# Find tools-grid and its closing
start = cn.find('<div class="tools-grid"')
grid_end = cn.find('</div>', start)
# Find the tools-grid's own closing tag
depth = 1
pos = start + len('<div class="tools-grid"')
while depth > 0 and pos < len(cn):
    next_open = cn.find('<div', pos)
    next_close = cn.find('</div>', pos)
    if next_close == -1: break
    if next_open != -1 and next_open < next_close:
        depth += 1
        pos = next_open + 4
    else:
        depth -= 1
        if depth == 0:
            grid_end = next_close
            break
        pos = next_close + 6

print(f"Grid end at position: {grid_end}")
# Insert before the closing </div> of tools-grid
cn = cn[:grid_end] + '\n' + new_cards + '\n' + cn[grid_end:]
with open('index.html', 'w') as f:
    f.write(cn)

cn_cards = len(re.findall(r'class="tool-card"', cn))
print(f"CN cards after: {cn_cards}")

# EN 
with open('en/index.html', 'r') as f:
    en = f.read()

en_cards = len(re.findall(r'class="tool-card"', en))
print(f"EN cards: {en_cards}")
print(f"Match: {'✅' if cn_cards == en_cards else '❌'}")