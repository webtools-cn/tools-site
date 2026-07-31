#!/usr/bin/env python3
"""微调超长和过短的描述"""
import re

FIXES = {
    "yaml-path-finder": (
        "免费在线YAML路径查找器，输入YAML配置文档和路径表达式快速定位并提取嵌套数据。支持点号语法访问嵌套键、方括号语法访问数组元素和通配符匹配多个节点，一键列出所有数据路径并导出结果。所有解析在浏览器本地完成无需注册下载，保障配置文件数据安全不泄露到服务器。",
    ),
    "youtube-timestamp-link": (
        "免费在线YouTube视频时间戳链接生成器，输入YouTube视频网址和指定时间点自动生成带t参数的时间戳直达分享链接。支持时分秒精确输入和总秒数两种时间模式，点击链接直接跳转到视频精确位置。适合分享教程重点内容和会议录像关键节点，无需注册一键复制即用。",
    ),
    "sass-to-css": (
        "免费在线Sass/SCSS转CSS实时编译工具，全面支持.scss和.sass两种语法格式，输入Sass代码即时编译为标准CSS输出。提供expanded展开和compressed压缩两种输出风格，自动检测显示编译错误的行号。所有代码在浏览器本地处理绝不上传服务器，保障样式代码安全。",
    ),
    "google-font-previewer": (
        "免费在线Google Fonts字体预览和对比工具，实时浏览预览Google Fonts开源字体库中上千款精选网页字体。支持自定义预览文本内容，自由调节字体大小、字重和颜色样式。一键复制字体CSS引入代码快速集成到网页项目。适合网页设计师和前端开发者进行字体选型和搭配测试对比。",
    ),
    "localstorage-viewer": (
        "免费在线LocalStorage浏览器和管理工具，实时读取并展示当前网站所有localStorage存储的键值对数据。支持按关键字快速搜索过滤条目，可在线编辑修改任意键的值并实时生效。提供批量删除和一键导出JSON备份功能。前端开发调试和排查存储问题的必备利器，无需安装任何浏览器扩展。",
    ),
    "css-validator": (
        "免费在线CSS代码验证和语法检测工具，实时检查CSS中的语法错误、缺失花括号、无效属性值和存在兼容性问题的过时前缀。精确显示每个错误的类型、行号和修复建议，全面支持CSS3最新特性验证包括Grid和Flexbox。所有代码在浏览器本地检测绝不上传服务器，保障代码安全隐私。",
    ),
    "markdown-link-checker": (
        "免费在线Markdown链接有效性检查工具，自动提取文档中所有超链接URL和锚点引用并逐一验证HTTP状态码检测死链。支持识别重复链接、无效锚点和相对路径引用。适合技术文档维护、开源README质量检查和博客发布前的链接完整性审核验证，无需注册即用。",
    ),
    "css-grid-inspector": (
        "免费在线CSS Grid布局可视化构建工具，通过直观界面设置网格容器的列数、行数和间距参数。实时预览布局效果并自动生成完整CSS Grid代码，支持调整对齐方式和跨行列设置。无需手动编写复杂Grid语法，适合CSS初学者学习Grid布局原理和有经验开发者快速原型验证设计。",
    ),
}

for slug, (new_meta,) in FIXES.items():
    filepath = f"{slug}/index.html"
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Replace meta description
    pattern_meta = re.compile(
        r'(<meta\s+name="description"\s+content=")([^"]*)(")',
        re.IGNORECASE
    )
    m = pattern_meta.search(content)
    if m:
        content = content[:m.start(2)] + new_meta + content[m.end(2):]
    
    # Replace og:description
    pattern_og = re.compile(
        r'(<meta\s+property="og:description"\s+content=")([^"]*)(")',
        re.IGNORECASE
    )
    m = pattern_og.search(content)
    if m:
        content = content[:m.start(2)] + new_meta + content[m.end(2):]
    
    # Replace Schema.org description
    pattern_schema = re.compile(
        r'("description"\s*:\s*")([^"]*)(")',
        re.IGNORECASE
    )
    m = pattern_schema.search(content)
    if m:
        content = content[:m.start(2)] + new_meta + content[m.end(2):]
    
    with open(filepath, 'w') as f:
        f.write(content)
    print(f"  ✓ {slug}: {len(new_meta)} chars")

print("\nDone.")