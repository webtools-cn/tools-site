#!/usr/bin/env python3
"""生成首页静态预渲染内容，让Google爬虫看到内部链接"""
import json
import re

with open('tools-data-cn.json') as f:
    data = json.load(f)

# 分类名称映射
cat_name_map = {
    'dev-tools':'开发者工具','utility-tools':'实用工具','finance-tools':'金融工具',
    'text-tools':'文字工具','design-tools':'设计工具','health-tools':'健康工具',
    'image-tools':'图片工具','calc-tools':'计算工具','media-tools':'媒体工具',
    'fun-tools':'趣味娱乐','office-tools':'办公工具','pdf-tools':'PDF工具',
    'math-tools':'数学工具','security-tools':'安全工具','creative-tools':'创意工具',
    'network-tools':'网络工具','life-tools':'生活工具','seo-tools':'SEO工具',
    'productivity-tools':'效率工具','conv-tools':'转换工具','audio-tools':'音频工具',
    'business-tools':'商业工具','converter-tools':'转换工具','gen-tools':'生成工具',
    'developer-tools':'开发工具','travel-tools':'旅行工具','education-tools':'教育工具',
    'kitchen-tools':'厨房工具','css-tools':'CSS工具','color-tools':'颜色工具',
    'sports-tools':'运动工具','study-tools':'学习工具','science-tools':'科学工具',
    'video-tools':'视频工具','data-tools':'数据工具','generator-tools':'生成工具',
    'new-tools':'新工具','check-tools':'检测工具'
}

# 按工具数排序
cats = sorted(data.keys(), key=lambda k: len(data[k]), reverse=True)

static_parts = []
for cat in cats:
    name = cat_name_map.get(cat, cat.replace('-',' '))
    tools = data[cat]
    static_parts.append(f'<li><strong>{name}</strong>: ')
    links = []
    for t in tools[:5]:
        links.append(f'<a href="/{t[3]}">{t[1]}</a>')
    static_parts.append(' · '.join(links))
    static_parts.append('</li>\n')

static_html = '<ul class="static-tool-links">\n' + ''.join(static_parts) + '</ul>'

# 读首页
with open('index.html') as f:
    html = f.read()

# 替换 <noscript> 内容，添加静态链接
old_noscript = '<noscript>\n<p style="text-align:center;padding:2rem;color:#94a3b8">请启用JavaScript以浏览工具列表，或访问 <a href="sitemap.xml">sitemap.xml</a> 查看所有工具。</p>\n</noscript>'

new_noscript = f'<noscript>\n<div style="max-width:900px;margin:0 auto;padding:16px;color:#94a3b8;font-size:.85rem;line-height:2">\n{static_html}\n</div>\n<p style="text-align:center;padding:1rem;color:#64748b">请启用JavaScript以获取完整交互体验，或访问 <a href="sitemap.xml">sitemap.xml</a> 查看全部{sum(len(v) for v in data.values())}+工具。</p>\n</noscript>'

html = html.replace(old_noscript, new_noscript)

# 添加静态链接的CSS（隐藏给普通用户，只给爬虫看）
static_css = """
/* 静态工具链接 - 仅给搜索引擎爬虫看 */
.static-tool-links{display:none}  /* JS正常时不显示 */
.static-tool-links a{color:#06b6d4}
.static-tool-links a:hover{color:#22d3ee}
"""

# 把CSS插入到</style>前
html = html.replace('</style>', static_css + '\n</style>')

with open('index.html', 'w') as f:
    f.write(html)

print(f"✅ 首页已更新：{len(cats)}个分类、{sum(len(v) for v in data.values())}个工具链接已预渲染到<noscript>")
print(f"   文件大小: {len(html)} bytes")