#!/usr/bin/env python3
"""给content_thin页面增加描述文本，使其文本长度>500"""
import re, os

# 每个页面的工具名和附加描述
TOOL_DESCRIPTIONS = {
    'api-doc-generator/index.html': {
        'tool_name': 'API文档生成器',
        'extra_desc': '<p style="color:#94a3b8;font-size:.9rem;line-height:1.7;margin-top:8px">API文档生成器支持OpenAPI 3.0和Swagger 2.0规范，自动解析JSON结构并生成清晰易读的API文档。您只需粘贴API定义即可获得完整的Markdown或HTML文档，包含端点列表、请求参数、响应示例等。所有处理均在浏览器本地完成，无需上传数据到服务器，保障您的API信息安全。适用于前后端开发者快速生成项目文档。</p>'
    },
    'html-beautify/index.html': {
        'tool_name': 'HTML代码格式化',
        'extra_desc': '<p style="color:#94a3b8;font-size:.9rem;line-height:1.7;margin-top:8px">HTML代码格式化工具支持自动缩进调整、标签闭合检查、属性排序等功能。您可以选择2/4空格或Tab缩进，一键将混乱的HTML代码转换为结构清晰、易于阅读的格式。工具完全在浏览器本地运行，代码不会上传到任何服务器，安全可靠。适用于前端开发者日常代码整理和团队代码规范统一。</p>'
    },
    'receipt-generator/index.html': {
        'tool_name': '收据生成器',
        'extra_desc': '<p style="color:#94a3b8;font-size:.9rem;line-height:1.7;margin-top:8px">收据生成器让您轻松创建专业格式的收据，支持自定义商家信息、商品明细、税率和折扣等。生成的收据可直接打印或保存为PDF，适合小商家、自由职业者和个人使用。所有数据均在浏览器本地处理，不会上传到服务器，保护您的商业隐私。</p>'
    },
    'tag-cloud/index.html': {
        'tool_name': '标签云生成器',
        'extra_desc': '<p style="color:#94a3b8;font-size:.9rem;line-height:1.7;margin-top:8px">标签云生成器将您的关键词列表转换为美观的标签云，支持自定义颜色方案、字体大小范围和排列方式。适用于博客侧边栏、PPT演示文稿和网页设计项目。工具完全在浏览器本地运行，无需注册，即开即用。生成的标签云可复制HTML代码直接嵌入您的网站。</p>'
    },
    'en/markdown-to-pdf-converter/index.html': {
        'tool_name': 'Markdown to PDF Converter',
        'extra_desc': '<p style="color:#94a3b8;font-size:.9rem;line-height:1.7;margin-top:8px">The Markdown to PDF Converter transforms your Markdown documents into professional PDF files with customizable styling. Supports headers, lists, code blocks, tables, and images. All processing happens locally in your browser — your documents are never uploaded to any server. Perfect for developers, technical writers, and anyone who needs to share Markdown content as PDF documents.</p>'
    },
}

BASE = '/home/chison/tools-site'
fixed = 0

for filepath, info in TOOL_DESCRIPTIONS.items():
    path = os.path.join(BASE, filepath)
    if not os.path.exists(path):
        print(f'SKIP: {filepath}')
        continue
    
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 在 hero/subtitle 区域插入额外描述
    # 模式：<p class="subtitle">...</p> 或 <div class="hero"><p>...</p></div>
    # 在这些后面插入 extra_desc
    
    extra = info['extra_desc']
    
    # 尝试在 subtitle 后面插入
    if re.search(r'<p class="subtitle">.*?</p>', content):
        content = re.sub(
            r'(<p class="subtitle">.*?</p>)',
            r'\1\n' + extra,
            content,
            count=1
        )
        fixed += 1
        print(f'FIXED (subtitle): {filepath}')
    # 尝试在 hero p 后面插入
    elif re.search(r'<div class="hero"><p>.*?</p></div>', content):
        content = re.sub(
            r'(<div class="hero"><p>.*?</p>)</div>',
            r'\1' + extra + '</div>',
            content,
            count=1
        )
        fixed += 1
        print(f'FIXED (hero): {filepath}')
    else:
        print(f'NO MATCH: {filepath}')
        continue
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

print(f'\nTotal fixed: {fixed}')