#!/usr/bin/env python3
"""最后一轮微调，确保140-160字符"""
import re

FIXES = {
    "yaml-path-finder": (
        "免费在线YAML路径查找器，输入YAML配置文档和路径表达式快速定位并提取嵌套数据。支持点号语法访问嵌套键、方括号语法访问数组元素和通配符匹配多个节点，一键列出文档中所有数据路径并可导出结果。所有解析计算在浏览器本地完成无需注册下载，保障您的配置文件数据安全不泄露到任何外部服务器。",
    ),
    "youtube-timestamp-link": (
        "免费在线YouTube视频时间戳链接生成器，输入YouTube视频网址和指定时间点自动生成带t参数的时间戳直达分享链接。支持时分秒精确输入和总秒数两种时间模式，点击生成的链接直接跳转到视频精确位置。适合分享教程重点内容、会议录像关键节点和视频精彩片段，无需注册登录一键复制链接即可使用。",
    ),
    "word-counter-online": (
        "免费在线字数统计工具，实时精确统计输入文本的字数、字符数含不含空格、英文单词数、行数和段落数。全面支持中英文及混合文本计数，提供基于不同阅读速度的阅读时间估算方便内容排期。所有统计计算在浏览器本地完成文本不上传服务器。适合写作、翻译校对、SEO内容优化和社交媒体文案编辑等场景。",
    ),
    "dividend-yield-calculator": (
        "免费在线股息率计算器，输入股票当前市场价和每股年度派息金额实时自动计算股息率、股息支付率和年化分红收益。支持同时添加多只股票进行横向对比分析，帮助价值投资者快速评估股票的分红投资回报率。所有计算在浏览器本地完成数据不上传服务器，无需注册即可免费使用，适合股票投资者日常研究分析。",
    ),
    "google-font-previewer": (
        "免费在线Google Fonts字体预览和对比工具，实时浏览预览Google Fonts开源字体库中上千款精选网页字体。支持自定义预览文本内容，自由调节字体大小、字重粗细和字体颜色样式。一键复制字体CSS引入代码快速集成到网页项目中。适合网页设计师和前端开发者进行字体选型搭配测试对比，无需注册即开即用。",
    ),
    "css-validator": (
        "免费在线CSS代码验证和语法错误检测工具，实时检查CSS中的语法错误、缺失花括号、无效属性值和存在浏览器兼容性问题的过时前缀。精确显示每个错误的类型、所在行号和修复建议，全面支持CSS3最新特性验证包括Grid和Flexbox。所有代码在浏览器本地完成检测绝不上传服务器，保障您的代码安全隐私。",
    ),
    "markdown-link-checker": (
        "免费在线Markdown链接有效性检查工具，自动提取文档中所有超链接URL和内页锚点引用并逐一验证HTTP响应状态码检测死链和失效链接。支持识别重复出现的链接地址、无效锚点跳转和相对路径引用。适合技术文档维护、开源项目README质量检查和博客文章发布前的链接完整性审核验证，无需注册。",
    ),
    "css-grid-inspector": (
        "免费在线CSS Grid布局可视化交互构建工具，通过直观的图形界面设置网格容器的列数、行数、列间距和行间距等核心参数。实时预览网格布局效果并自动生成完整CSS Grid代码，支持调整对齐方式和跨行列设置。无需手动编写复杂Grid语法，适合CSS初学者学习Grid布局原理和有经验开发者快速原型设计验证。",
    ),
}

for slug, (new_meta,) in FIXES.items():
    filepath = f"{slug}/index.html"
    with open(filepath, 'r') as f:
        content = f.read()
    
    for _ in range(2):
        for pat_key in ['description', 'og:description']:
            if pat_key == 'description':
                pattern = re.compile(r'(<meta\s+name="description"\s+content=")([^"]*)(")', re.IGNORECASE)
            else:
                pattern = re.compile(r'(<meta\s+property="og:description"\s+content=")([^"]*)(")', re.IGNORECASE)
            m = pattern.search(content)
            if m:
                content = content[:m.start(2)] + new_meta + content[m.end(2):]
        
        pattern_schema = re.compile(r'("description"\s*:\s*")([^"]*)(")', re.IGNORECASE)
        m = pattern_schema.search(content)
        if m:
            content = content[:m.start(2)] + new_meta + content[m.end(2):]
    
    with open(filepath, 'w') as f:
        f.write(content)
    print(f"  ✓ {slug}: {len(new_meta)} chars")
print("\nDone.")