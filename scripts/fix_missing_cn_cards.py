#!/usr/bin/env python3
"""补充CN首页缺失的4个工具卡片，同步首页"""
import re

extra_cn = [
    ('csr-generator', '🔐', 'CSR生成器', '在线生成证书签名请求CSR和RSA私钥，纯前端本地处理', '安全工具'),
    ('keycode-info', '⌨️', '键盘码查询器', '按下任意键查看keyCode/key/code值，前端开发必备', '开发工具'),
    ('mimetype-checker', '📁', 'MIME类型查询', '查询600+文件扩展名对应的MIME/Content-Type', '开发工具'),
    ('url-encoder-decode', '🔗', 'URL编解码工具', 'URL编码(encodeURIComponent)和解码双向转换', '开发工具'),
]

cat_map = {
    '安全工具': 'security-tools', '开发工具': 'dev-tools',
}

def make_card(slug, icon, name, desc, cat):
    data_cat = cat_map.get(cat, 'utility-tools')
    return f'<div class="tool-card" data-category="{data_cat}"><span class="tool-icon">{icon}</span><span class="tool-name">{name}</span><span class="tool-desc">{desc}</span><a href="/{slug}/" class="btn">立即使用</a></div>'

with open('index.html', 'r') as f:
    cn = f.read()

new_cards = '\n'.join(make_card(*t) for t in extra_cn)

# 插入在tools-grid结束前
end_marker = '  </div>\n  <div class="search-section"'
if end_marker in cn:
    cn = cn.replace(end_marker, '\n' + new_cards + '\n' + end_marker)
else:
    # try other variant
    end_marker2 = '</div>\n\n  <div class="search-section"'
    if end_marker2 in cn:
        cn = cn.replace(end_marker2, '\n' + new_cards + '\n' + end_marker2)
    else:
        print("Cannot find insertion point!")
        exit(1)

cn_cards = len(re.findall(r'class=\"tool-card\"', cn))
with open('index.html', 'w') as f:
    f.write(cn)

# Verify EN
with open('en/index.html') as f:
    en = f.read()
en_cards = len(re.findall(r'class=\"tool-card\"', en))

print(f"CN cards: {cn_cards}")
print(f"EN cards: {en_cards}")
print(f"Match: {'✅' if cn_cards == en_cards else '❌'}")