#!/usr/bin/env python3
"""Batch translate CN tools to EN versions with proper URL mapping"""
import os, re, shutil

BASE = '/home/chison/tools-site'

TOOLS = {
    'js-beautify': {
        'title': 'JS Code Beautifier',
        'desc': 'Free online JavaScript code formatter and beautifier. Supports indent adjustment, brace placement, and whitespace optimization. Make messy JS code clean and readable.',
        'h1': 'JS Code Beautifier',
        'hero': 'Free online JavaScript code formatter and beautifier. Supports indent adjustment, brace placement, and whitespace optimization. Make messy JS code clean and readable.',
        'badge': 'Zero Dependencies · Works Offline',
        'faq_questions': ['Is JS Code Beautifier free?', 'Is my data secure?', 'What JS versions are supported?'],
        'faq_answers': ['Yes, completely free to use, no registration required.', 'This tool runs entirely in your browser. Your code never leaves your device.', 'Supports ES5, ES6+, TypeScript, and all modern JavaScript syntax.'],
    },
    'css-beautify': {
        'title': 'CSS Code Beautifier',
        'desc': 'Free online CSS code formatter and beautifier. Supports indent adjustment, selector sorting, and property grouping. Make messy CSS stylesheets clean and readable.',
        'h1': 'CSS Code Beautifier',
        'hero': 'Free online CSS code formatter and beautifier. Supports indent adjustment, selector sorting, and property grouping. Make messy CSS stylesheets clean and readable.',
        'badge': 'Zero Dependencies · Works Offline',
        'faq_questions': ['Is CSS Code Beautifier free?', 'Is my data secure?', 'Does it support CSS3 and preprocessors?'],
        'faq_answers': ['Yes, completely free to use, no registration required.', 'This tool runs entirely in your browser. Your code never leaves your device.', 'Supports standard CSS and CSS3 syntax. SCSS/LESS may need compilation first.'],
    },
    'html-beautify': {
        'title': 'HTML Code Beautifier',
        'desc': 'Free online HTML code formatter and beautifier. Supports indent adjustment, tag closure checking, and attribute sorting. Make messy HTML code clean and readable.',
        'h1': 'HTML Code Beautifier',
        'hero': 'Free online HTML code formatter and beautifier. Supports indent adjustment, tag closure checking, and attribute sorting. Make messy HTML code clean and readable.',
        'badge': 'Zero Dependencies · Works Offline',
        'faq_questions': ['Is HTML Code Beautifier free?', 'Is my data secure?', 'Does it support HTML5?'],
        'faq_answers': ['Yes, completely free to use, no registration required.', 'This tool runs entirely in your browser. Your code never leaves your device.', 'Supports HTML5 and all standard HTML syntax, including inline SVG and MathML.'],
    },
    'screen-resolution-test': {
        'title': 'Screen Resolution Test',
        'desc': 'Free online screen resolution testing tool. Real-time detection of your screen resolution, pixel ratio, color depth, window size and more. No installation required.',
        'h1': 'Screen Resolution Test',
        'hero': 'Free online screen resolution testing tool. Real-time detection of your screen resolution, pixel ratio, color depth, and window size. No installation required.',
        'badge': 'Real-Time Detection · Works Offline',
        'faq_questions': ['Is Screen Resolution Test free?', 'Is my data secure?', 'Why might results differ from actual resolution?'],
        'faq_answers': ['Yes, completely free to use, no registration required.', 'This tool runs entirely in your browser. No personal information is collected.', 'Browsers are affected by system scaling settings. DPR > 1 means scaling is enabled (e.g., Retina = 2).'],
    },
    'traceroute': {
        'title': 'Traceroute',
        'desc': 'Free online traceroute tool. Visualize the network path from your device to target servers, helping diagnose network latency and routing issues.',
        'h1': 'Traceroute',
        'hero': 'Free online traceroute tool. Visualize the network path from your device to target servers, helping diagnose network latency and routing issues.',
        'badge': 'Network Diagnostics · Works Offline',
        'faq_questions': ['Is Traceroute free?', 'How accurate is it?', 'Which browsers are supported?'],
        'faq_answers': ['Yes, completely free to use, no registration required.', 'Uses WebRTC and HTTP requests to simulate traceroute. Results are for reference only.', 'Supports all modern browsers including Chrome, Firefox, Safari, and Edge.'],
    },
    'open-graph-debugger': {
        'title': 'Open Graph Debugger',
        'desc': 'Free online Open Graph tag debugger. Enter a URL to preview how your website appears on social media, and check if OG tags are properly configured.',
        'h1': 'Open Graph Debugger',
        'hero': 'Free online Open Graph tag debugger. Enter a URL or paste HTML code to preview social media appearance and check OG tag configuration.',
        'badge': 'SEO Tool · Works Offline',
        'faq_questions': ['Is Open Graph Debugger free?', 'How does it work?'],
        'faq_answers': ['Yes, completely free to use, no registration required.', 'Enter a URL to automatically extract OG tags and render Facebook and Twitter share previews.'],
    },
    'placeholder-image': {
        'title': 'Placeholder Image Generator',
        'desc': 'Free online placeholder image generator. Quickly create images of any size with custom background colors, text, and text colors. Perfect for development prototypes and design mockups.',
        'h1': 'Placeholder Image Generator',
        'hero': 'Free online placeholder image generator. Quickly create images of any size with custom background colors, text, and text colors. Perfect for development prototypes and design mockups.',
        'badge': 'Canvas Generated · Works Offline',
        'faq_questions': ['Is Placeholder Image Generator free?', 'Do generated images have copyright restrictions?'],
        'faq_answers': ['Yes, completely free to use, no registration required.', 'Images are fully customizable by you with no copyright restrictions. Free for any project.'],
    },
    'days-until': {
        'title': 'Countdown Calculator - Days Until',
        'desc': 'Free online countdown calculator. Calculate the remaining days, weeks, and months from today to a specified date. Includes holiday presets, perfect for event countdowns and project deadlines.',
        'h1': 'Countdown Calculator',
        'hero': 'Free online countdown calculator. Calculate the remaining days, weeks, and months from today to a specified date. Includes holiday presets, perfect for event countdowns and project deadlines.',
        'badge': 'Real-Time Calculation · Works Offline',
        'faq_questions': ['Is Countdown Calculator free?', 'Is my data secure?', 'Which browsers are supported?'],
        'faq_answers': ['Yes, completely free to use, no registration required.', 'This tool runs entirely in your browser. No data is uploaded to any server.', 'Supports all modern browsers including Chrome, Firefox, Safari, and Edge.'],
    },
    'bcrypt-checker': {
        'title': 'Bcrypt Password Checker',
        'desc': 'Free online bcrypt password verification tool. Verify bcrypt hashes, detect salt rounds, and help developers validate password hashes. Browser-local computation, data stays private.',
        'h1': 'Bcrypt Password Checker',
        'hero': 'Free online bcrypt password verification tool. Verify bcrypt hashes, detect salt rounds, and help developers validate password hashes. All computation is browser-local.',
        'badge': 'Security Tool · Works Offline',
        'faq_questions': ['Is Bcrypt Checker free?', 'Is my data secure?', 'What bcrypt formats are supported?'],
        'faq_answers': ['Yes, completely free to use, no registration required.', 'This tool uses pure JavaScript running locally in your browser. Passwords and hashes never leave your device.', 'Supports standard $2a$, $2b$, and $2y$ bcrypt hash formats with rounds 4-31.'],
    },
    'unix-permissions-calculator': {
        'title': 'Unix Permissions Calculator',
        'desc': 'Free online Unix file permissions calculator. Visually set read/write/execute permissions and automatically generate octal and symbolic permission values. Supports chmod command generation.',
        'h1': 'Unix Permissions Calculator',
        'hero': 'Free online Unix file permissions calculator. Visually set read/write/execute permissions and automatically generate octal and symbolic permission values. Supports chmod command generation.',
        'badge': 'System Administration · Works Offline',
        'faq_questions': ['Is Unix Permissions Calculator free?', 'What are octal permissions?', 'What does 755 permission mean?'],
        'faq_answers': ['Yes, completely free to use, no registration required.', 'Unix file permissions are represented by a 3-digit octal number: owner/group/others read(4)+write(2)+execute(1) permissions.', 'Owner can read/write/execute (rwx), group and others can read/execute (r-x). Commonly used for directories and executables.'],
    },
}

TRANSLATIONS = {
    # Nav / UI
    '首页': 'Home',
    '工具': 'Tools',
    '英文版': 'English',
    'EN': '中文',
    # Buttons
    '格式化': 'Beautify',
    '压缩': 'Minify',
    '清空': 'Clear',
    '示例': 'Sample',
    '复制结果': 'Copy Result',
    '下载': 'Download',
    '刷新检测': 'Refresh',
    '全屏测试': 'Fullscreen',
    '开始追踪': 'Start Trace',
    '复制': 'Copy',
    '调试': 'Debug',
    '生成': 'Generate',
    '下载PNG': 'Download PNG',
    '下载SVG': 'Download SVG',
    '复制Data URL': 'Copy Data URL',
    '计算倒计时': 'Calculate',
    '今天': 'Today',
    '复制结果': 'Copy Result',
    '分享链接': 'Share Link',
    '验证': 'Verify',
    '分析哈希': 'Analyze Hash',
    '重置': 'Reset',
    '复制命令': 'Copy Command',
    '复制八进制值': 'Copy Octal',
    '复制符号值': 'Copy Symbolic',
    # Labels
    '缩进': 'Indent',
    '空格': 'spaces',
    'Tab': 'Tab',
    '大括号换行': 'Braces on new line',
    '分号结尾': 'Semicolons',
    '属性排序': 'Sort Properties',
    '屏幕分辨率': 'Screen Resolution',
    '可用分辨率': 'Available Resolution',
    '窗口大小': 'Window Size',
    '设备像素比': 'Device Pixel Ratio',
    '色深': 'Color Depth',
    '像素深度': 'Pixel Depth',
    '屏幕方向': 'Orientation',
    '宽高比': 'Aspect Ratio',
    '颜色': 'Color',
    '文件权限': 'File Permissions',
    '文件名': 'Filename',
    '所有现代浏览器': 'all modern browsers',
    '数据不上传': 'data stays private',
    '数据绝不上传服务器': 'data never leaves your device',
    # Domain
    '横屏': 'Landscape',
    '竖屏': 'Portrait',
}

# Short descriptive phrases that appear in hero/p paragraphs (already handled in TOOLS)
# For inline UI text, we do targeted replacements

def translate_file(tool_name, info):
    cn_path = os.path.join(BASE, tool_name, 'index.html')
    en_path = os.path.join(BASE, 'en', tool_name, 'index.html')

    with open(cn_path, 'r') as f:
        content = f.read()

    # Replace lang
    content = content.replace('lang="zh-CN"', 'lang="en"')

    # Replace title
    content = re.sub(r'<title>.*?</title>', f'<title>{info["title"]} - Free ToolBase</title>', content)
    content = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{info["desc"]}">', content)

    # Replace OG tags
    content = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{info["title"]}">', content)
    content = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{info["desc"]}">', content)

    # Replace canonical
    content = content.replace(f'https://free-toolbase.com/{tool_name}/', f'https://free-toolbase.com/en/{tool_name}/')
    content = content.replace(f'href="https://free-toolbase.com/en/{tool_name}/"', f'href="https://free-toolbase.com/{tool_name}/"')

    # Fix hreflang
    content = content.replace(f'href="https://free-toolbase.com/en/{tool_name}/"', f'href="https://free-toolbase.com/{tool_name}/"', 1)
    # Actually we need to swap them
    # cn: alternate en -> /en/..., alternate x-default -> /en/...
    # en: alternate en -> /, alternate x-default -> /
    content = re.sub(
        r'<link rel="alternate" hreflang="en" href="https://free-toolbase\.com/en/[^"]*">',
        f'<link rel="alternate" hreflang="en" href="https://free-toolbase.com/en/{tool_name}/">',
        content
    )
    content = re.sub(
        r'<link rel="alternate" hreflang="x-default" href="https://free-toolbase\.com/en/[^"]*">',
        f'<link rel="alternate" hreflang="x-default" href="https://free-toolbase.com/en/{tool_name}/">',
        content
    )

    # Replace Schema software name and desc
    content = re.sub(
        r'"name": "[^"]*"',
        f'"name": "{info["title"]}"',
        content, count=1
    )
    content = re.sub(
        r'"description": "[^"]*"',
        f'"description": "{info["desc"]}"',
        content, count=1
    )

    # Replace FAQ questions and answers
    for i, q in enumerate(info['faq_questions']):
        # Replace question name
        content = re.sub(
            r'"name": "[^"]*"',
            f'"name": "{q}"',
            content, count=1
        )
    for i, a in enumerate(info['faq_answers']):
        content = re.sub(
            r'"text": "[^"]*"',
            f'"text": "{a}"',
            content, count=1
        )

    # Replace BreadcrumbList items
    content = re.sub(
        r'"name": "首页"',
        '"name": "Home"',
        content
    )
    content = re.sub(
        r'"name": "工具"',
        '"name": "Tools"',
        content
    )

    # Replace h1
    content = re.sub(r'<h1>[^<]*</h1>', f'<h1>{info["h1"]}</h1>', content)

    # Replace hero paragraph
    content = re.sub(
        r'<div class="hero"><p>[^<]*</p>',
        f'<div class="hero"><p>{info["hero"]}</p>',
        content
    )

    # Replace badge text
    content = re.sub(
        r'<span class="badge">[^<]*</span>',
        f'<span class="badge">{info["badge"]}</span>',
        content
    )

    # Breadcrumb navigation text
    content = re.sub(
        r'<a href="\.\./index\.html">首页</a>',
        f'<a href="../index.html">Home</a>',
        content
    )
    content = re.sub(
        r'<a href="\.\./index\.html#tools">工具</a>',
        '<a href="../index.html#tools">Tools</a>',
        content
    )
    content = content.replace(' &rsaquo; 首页', ' &rsaquo; Home')
    content = content.replace(' &rsaquo; 工具', ' &rsaquo; Tools')

    # Replace tool-specific breadcrumb last item
    content = re.sub(
        r' &rsaquo; [^<\n]+</p>',
        f' &rsaquo; {info["h1"]}</p>',
        content
    )

    # Switch language links
    content = content.replace(f'href="../en/{tool_name}/" class="active"', f'href="../{tool_name}/" class=""')
    content = content.replace(f'href="../en/{tool_name}/">EN</a>', f'href="../{tool_name}/">中文</a>')

    # Buttons - translate common CN button text
    replacements = {
        '✨ 格式化': '✨ Beautify',
        '📦 压缩': '📦 Minify',
        '🗑 清空': '🗑 Clear',
        '📋 示例': '📋 Sample',
        '📋 复制结果': '📋 Copy Result',
        '💾 下载': '💾 Download',
        '🔄 刷新检测': '🔄 Refresh',
        '⛶ 全屏测试': '⛶ Fullscreen',
        '🚀 开始追踪': '🚀 Start Trace',
        '🔍 调试': '🔍 Debug',
        '🔍 验证': '🔍 Verify',
        '📊 分析哈希': '📊 Analyze Hash',
        '✨ 生成': '✨ Generate',
        '💾 下载PNG': '💾 Download PNG',
        '📥 下载SVG': '📥 Download SVG',
        '📋 复制Data URL': '📋 Copy Data URL',
        '📅 计算倒计时': '📅 Calculate',
        '📍 今天': '📍 Today',
        '🔗 分享链接': '🔗 Share Link',
        '🔄 重置': '🔄 Reset',
        '📋 复制命令': '📋 Copy Command',
        '📋 复制八进制值': '📋 Copy Octal',
        '📋 复制符号值': '📋 Copy Symbolic',
        '📋 复制结果': '📋 Copy Result',
        '📋 复制标签': '📋 Copy Tags',
    }
    for cn, en in replacements.items():
        content = content.replace(cn, en)

    # Common UI labels
    ui_replacements = {
        '缩进:': 'Indent:',
        '2空格': '2 spaces',
        '4空格': '4 spaces',
        '大括号换行': 'Braces on new line',
        '分号结尾': 'Semicolons',
        '属性排序': 'Sort Properties',
        '屏幕分辨率': 'Screen Resolution',
        '可用分辨率': 'Available Resolution',
        '窗口大小': 'Window Size',
        '设备像素比': 'Device Pixel Ratio',
        '像素深度': 'Pixel Depth',
        '屏幕方向': 'Orientation',
        '色深': 'Color Depth',
        '宽高比': 'Aspect Ratio',
        '文件名:': 'Filename:',
    }
    for cn, en in ui_replacements.items():
        content = content.replace(cn, en)

    # Labels that appear as standalone text
    content = content.replace('目标日期:', 'Target Date:')
    content = content.replace('背景色:', 'Bg Color:')
    content = content.replace('文字色:', 'Text Color:')
    content = content.replace('文字:', 'Text:')
    content = content.replace('字号:', 'Font Size:')
    content = content.replace('Bcrypt哈希:', 'Bcrypt Hash:')
    content = content.replace('明文密码:', 'Password:')
    content = content.replace('显示密码', 'Show Password')
    content = content.replace('选择转换模式:', 'Select Mode:')
    content = content.replace('选择目标日期', 'Select Target Date')

    # Tool section headers
    content = content.replace('📝 JS代码格式化', '📝 JS Code Beautifier')
    content = content.replace('🎨 CSS代码格式化', '🎨 CSS Code Beautifier')
    content = content.replace('🏗 HTML代码格式化', '🏗 HTML Code Beautifier')
    content = content.replace('📐 屏幕参数', '📐 Screen Parameters')
    content = content.replace('🎨 色彩测试', '🎨 Color Test')
    content = content.replace('🖥 可视区域', '🖥 Viewport')
    content = content.replace('🌐 路由追踪', '🌐 Traceroute')
    content = content.replace('🔍 OG标签调试', '🔍 OG Tag Debugger')
    content = content.replace('🖼 占位图生成', '🖼 Placeholder Generator')
    content = content.replace('⏳ 倒计时计算', '⏳ Countdown Calculator')
    content = content.replace('🔐 Bcrypt哈希验证', '🔐 Bcrypt Hash Verifier')
    content = content.replace('🔧 权限计算器', '🔧 Permissions Calculator')

    # Section descriptions (simplified pattern)
    content = content.replace('粘贴混乱的JavaScript代码，一键格式化为清晰易读的代码。 | 无需注册 · 数据绝不上传服务器', 'Paste messy JavaScript code and beautify it with one click. | No registration · Data never leaves your device')
    content = content.replace('粘贴混乱的CSS代码，一键格式化为清晰易读的代码。 | 无需注册 · 数据绝不上传服务器', 'Paste messy CSS code and beautify it with one click. | No registration · Data never leaves your device')
    content = content.replace('粘贴混乱的HTML代码，一键格式化为清晰易读的代码。 | 无需注册 · 数据绝不上传服务器', 'Paste messy HTML code and beautify it with one click. | No registration · Data never leaves your device')
    content = content.replace('实时检测您的屏幕和浏览器窗口参数。 | 无需注册 · 数据不上传服务器', 'Real-time detection of your screen and browser window parameters. | No registration · Data stays private')
    content = content.replace('测试屏幕色彩显示能力，点击色块可全屏显示该颜色。', 'Test your screen color display capabilities. Click a color block to view it fullscreen.')
    content = content.replace('当前浏览器窗口可视区域大小。', 'Current browser viewport size.')
    content = content.replace('输入目标域名或IP地址，追踪网络数据包的传输路径。 | 无需注册 · 数据不上传服务器', 'Enter a target domain or IP address to trace the network packet path. | No registration · Data stays private')
    content = content.replace('输入URL或粘贴HTML代码，查看OG标签解析结果和社交分享预览。 | 无需注册', 'Enter a URL or paste HTML code to view OG tag analysis and social previews. | No registration')
    content = content.replace('设置尺寸、颜色和文字，一键生成占位图片。 | 无需注册 · 浏览器本地生成', 'Set size, color, and text, generate placeholder images with one click. | No registration · Browser local generation')
    content = content.replace('选择目标日期，查看距离今天还有多少天。 | 无需注册 · 数据不上传服务器', 'Select a target date to see how many days remain. | No registration · Data stays private')
    content = content.replace('输入bcrypt哈希和明文密码，验证是否匹配。同时分析哈希格式和参数。 | 无需注册 · 数据不上传服务器', 'Enter a bcrypt hash and plaintext password to verify. Also analyzes hash format and parameters. | No registration · Data stays private')
    content = content.replace('勾选权限复选框，自动计算八进制值和chmod命令。 | 无需注册 · 数据不上传服务器', 'Check permission boxes to auto-calculate octal values and chmod commands. | No registration · Data stays private')

    # FAQ section
    content = content.replace('❓ 常见问题', '❓ FAQ')
    content = content.replace('JS格式化是免费的吗？', 'Is JS Code Beautifier free?')
    content = content.replace('JS格式化的数据安全吗？', 'Is my data secure?')
    content = content.replace('支持哪些JS版本？', 'What JS versions are supported?')
    content = content.replace('支持ES5、ES6+、TypeScript等所有主流JavaScript语法。', 'Supports ES5, ES6+, TypeScript, and all modern JavaScript syntax.')
    content = content.replace('CSS格式化是免费的吗？', 'Is CSS Code Beautifier free?')
    content = content.replace('CSS格式化的数据安全吗？', 'Is my data secure?')
    content = content.replace('支持CSS3和预处理器吗？', 'Does it support CSS3 and preprocessors?')
    content = content.replace('支持标准CSS和CSS3语法。SCSS/LESS可能需要先编译。', 'Supports standard CSS and CSS3 syntax. SCSS/LESS may need compilation first.')
    content = content.replace('HTML格式化是免费的吗？', 'Is HTML Code Beautifier free?')
    content = content.replace('HTML格式化的数据安全吗？', 'Is my data secure?')
    content = content.replace('支持HTML5吗？', 'Does it support HTML5?')
    content = content.replace('支持HTML5及所有标准HTML语法，包括内联SVG和MathML。', 'Supports HTML5 and all standard HTML syntax, including inline SVG and MathML.')
    content = content.replace('屏幕分辨率测试是免费的吗？', 'Is Screen Resolution Test free?')
    content = content.replace('屏幕分辨率测试的数据安全吗？', 'Is my data secure?')
    content = content.replace('为什么检测结果和实际分辨率不同？', 'Why might results differ from actual resolution?')
    content = content.replace('浏览器受系统缩放设置影响。DPR值>1表示启用了缩放（如Retina=2）。', 'Browsers are affected by system scaling. DPR > 1 means scaling is enabled (e.g., Retina = 2).')
    content = content.replace('路由追踪是免费的吗？', 'Is Traceroute free?')
    content = content.replace('路由追踪准确吗？', 'How accurate is it?')
    content = content.replace('路由追踪支持哪些浏览器？', 'Which browsers are supported?')
    content = content.replace('通过HTTP HEAD请求逐跳探测，部分路由器可能不响应。结果仅供参考。', 'Uses HTTP HEAD requests for hop-by-hop probing. Some routers may not respond. Results are for reference only.')
    content = content.replace('Open Graph调试器是免费的吗？', 'Is Open Graph Debugger free?')
    content = content.replace('OG调试器如何工作？', 'How does it work?')
    content = content.replace('输入URL后自动提取该页面的OG标签，渲染Facebook和Twitter分享预览卡片。', 'Enter a URL to automatically extract OG tags and render Facebook and Twitter share previews.')
    content = content.replace('OG标签是什么？', 'What are OG tags?')
    content = content.replace('Open Graph标签是HTML meta标签，控制网页在Facebook、Twitter、LinkedIn等社交媒体分享时的标题、描述和图片显示。', 'Open Graph tags are HTML meta tags that control title, description, and image display when sharing on Facebook, Twitter, LinkedIn, etc.')
    content = content.replace('为什么预览图片不显示？', 'Why are preview images not showing?')
    content = content.replace('可能因为跨域限制，浏览器无法加载远程图片。请检查og:image标签的URL是否正确。', 'May be due to cross-origin restrictions. Check if the og:image URL is correct.')
    content = content.replace('占位图生成器是免费的吗？', 'Is Placeholder Image Generator free?')
    content = content.replace('占位图如何生成？', 'How are placeholder images generated?')
    content = content.replace('使用HTML5 Canvas在浏览器本地生成，无需服务器，支持PNG/SVG/JPEG格式下载。', 'Uses HTML5 Canvas for browser-local generation. No server needed. Supports PNG/SVG/JPEG download.')
    content = content.replace('生成的图片有版权吗？', 'Do generated images have copyright restrictions?')
    content = content.replace('生成图片完全由您自定义，无版权限制，可自由用于任何项目。', 'Images are fully customizable by you with no copyright restrictions. Free for any project.')
    content = content.replace('倒计时计算器是免费的吗？', 'Is Countdown Calculator free?')
    content = content.replace('倒计时数据安全吗？', 'Is my data secure?')
    content = content.replace('Bcrypt密码验证是免费的吗？', 'Is Bcrypt Password Checker free?')
    content = content.replace('Bcrypt验证的数据安全吗？', 'Is my data secure?')
    content = content.replace('Bcrypt验证如何工作？', 'How does it work?')
    content = content.replace('支持哪些bcrypt格式？', 'What bcrypt formats are supported?')
    content = content.replace('支持标准$2a$、$2b$、$2y$格式的bcrypt哈希，轮数4-31。', 'Supports standard $2a$, $2b$, and $2y$ bcrypt hash formats with rounds 4-31.')
    content = content.replace('Unix权限计算器是免费的吗？', 'Is Unix Permissions Calculator free?')
    content = content.replace('什么是八进制权限？', 'What are octal permissions?')
    content = content.replace('Unix文件权限用3位八进制数表示：所有者/组/其他人的读(4)+写(2)+执行(1)权限。', 'Unix file permissions use a 3-digit octal number: owner/group/others read(4)+write(2)+execute(1) permissions.')
    content = content.replace('755权限是什么意思？', 'What does 755 permission mean?')
    content = content.replace('所有者可读写执行(rwx)，组和其他人可读执行(r-x)。常用于目录和可执行文件。', 'Owner can read/write/execute (rwx), group and others can read/execute (r-x). Common for directories and executables.')
    content = content.replace('可以离线使用JS格式化吗？', 'Can I use it offline?')
    content = content.replace('可以离线使用CSS格式化吗？', 'Can I use it offline?')
    content = content.replace('可以离线使用HTML格式化吗？', 'Can I use it offline?')
    content = content.replace('可以离线使用屏幕分辨率测试吗？', 'Can I use it offline?')

    # Footer
    content = content.replace('© 2025 Free ToolBase · <a href="../index.html">首页</a>', '© 2025 Free ToolBase · <a href="../index.html">Home</a>')
    content = content.replace('<a href="../en/{}/">English</a>'.format(tool_name), '<a href="../en/{}/">中文</a>'.format(tool_name))

    # Toast messages in JS
    content = content.replace("'请先输入JS代码'", "'Please enter JS code first'")
    content = content.replace("'格式化完成！'", "'Beautify complete!'")
    content = content.replace("'格式化出错: '", "'Beautify error: '")
    content = content.replace("'请先输入CSS代码'", "'Please enter CSS code first'")
    content = content.replace("'压缩完成！原始: '", "'Minify complete! Original: '")
    content = content.replace("' → 压缩: '", "' → Minified: '")
    content = content.replace("' (节省'", "' (saved '")
    content = content.replace("'压缩出错: '", "'Minify error: '")
    content = content.replace("'请先输入HTML代码'", "'Please enter HTML code first'")
    content = content.replace("'已复制到剪贴板！'", "'Copied to clipboard!'")
    content = content.replace("'已下载！'", "'Downloaded!'")
    content = content.replace("'没有可复制的内容'", "'Nothing to copy'")
    content = content.replace("'已刷新检测！'", "'Detection refreshed!'")
    content = content.replace("'已进入全屏模式'", "'Entered fullscreen mode'")
    content = content.replace("'请输入目标地址'", "'Please enter a target address'")
    content = content.replace("'追踪完成！'", "'Trace complete!'")
    content = content.replace("'已复制到剪贴板！'", "'Copied to clipboard!'")
    content = content.replace("'请输入URL或HTML代码'", "'Please enter a URL or HTML code'")
    content = content.replace("'已解析HTML代码'", "'HTML code parsed'")
    content = content.replace("'正在获取页面...'", "'Fetching page...'")
    content = content.replace("'调试完成！'", "'Debug complete!'")
    content = content.replace("'无法获取URL，尝试解析为HTML代码'", "'Could not fetch URL, trying to parse as HTML'")
    content = content.replace("'已生成占位图'", "'Placeholder generated'")
    content = content.replace("'PNG已下载'", "'PNG downloaded'")
    content = content.replace("'SVG已下载'", "'SVG downloaded'")
    content = content.replace("'Data URL已复制到剪贴板！'", "'Data URL copied!'")
    content = content.replace("'请选择目标日期'", "'Please select a target date'")
    content = content.replace("'倒计时已开始'", "'Countdown started'")
    content = content.replace("'请先计算倒计时'", "'Please calculate first'")
    content = content.replace("'请先选择目标日期'", "'Please select a target date first'")
    content = content.replace("'距离目标日期还有 '", "'Days until target date: '")
    content = content.replace("'分享链接已复制！'", "'Share link copied!'")
    content = content.replace("'请输入bcrypt哈希'", "'Please enter a bcrypt hash'")
    content = content.replace("'请输入密码'", "'Please enter a password'")
    content = content.replace("'验证完成'", "'Verification complete'")
    content = content.replace("'分析完成'", "'Analysis complete'")
    content = content.replace("'已加载示例'", "'Sample loaded'")
    content = content.replace("'已设置权限 '", "'Permission set to '")
    content = content.replace("'已重置'", "'Reset'")
    content = content.replace("'已复制！'", "'Copied!'")

    # Placeholders in textareas/inputs
    content = content.replace('在此粘贴混乱的JavaScript代码...', 'Paste messy JavaScript code here...')
    content = content.replace('在此粘贴混乱的CSS代码...', 'Paste messy CSS code here...')
    content = content.replace('在此粘贴混乱的HTML代码...', 'Paste messy HTML code here...')
    content = content.replace('格式化后的代码将显示在这里...', 'Formatted code will appear here...')
    content = content.replace('输入域名或IP地址，例如: google.com', 'Enter domain or IP, e.g.: google.com')
    content = content.replace('输入URL（如 https://example.com）或粘贴HTML代码', 'Enter URL (e.g., https://example.com) or paste HTML code')
    content = content.replace('粘贴bcrypt哈希值，例如:', 'Paste bcrypt hash, e.g.:')
    content = content.replace('输入要验证的密码', 'Enter password to verify')

    # Other UI elements
    content = content.replace('正在分析...', 'Analyzing...')
    content = content.replace('未设置', 'Not set')
    content = content.replace('缺失', 'Missing')
    content = content.replace('无图片', 'No Image')
    content = content.replace('图片加载失败', 'Image load failed')
    content = content.replace('预设尺寸:', 'Presets:')
    content = content.replace('快速选择:', 'Quick Select:')
    content = content.replace('常用预设:', 'Common:')
    content = content.replace('物理像素', 'Physical px')
    content = content.replace('减去任务栏', 'Minus taskbar')
    content = content.replace('浏览器视口', 'Browser viewport')
    content = content.replace('DPR/Retina', 'DPR/Retina')
    content = content.replace('宽 × 高 (CSS像素)', 'Width × Height (CSS px)')
    content = content.replace('角色', 'Role')
    content = content.replace('读 (r)', 'Read (r)')
    content = content.replace('写 (w)', 'Write (w)')
    content = content.replace('执行 (x)', 'Exec (x)')
    content = content.replace('所有者 Owner', 'Owner')
    content = content.replace('用户组 Group', 'Group')
    content = content.replace('其他人 Other', 'Other')
    content = content.replace('📘 Facebook / LinkedIn', '📘 Facebook / LinkedIn')
    content = content.replace('🐦 Twitter', '🐦 Twitter')

    # Status messages
    content = content.replace('🔍 正在追踪到 ', '🔍 Tracing route to ')
    content = content.replace(' 的路由...', '...')
    content = content.replace('✅ 追踪完成！共 ', '✅ Trace complete! ')
    content = content.replace(' 跳，目标: ', ' hops, target: ')
    content = content.replace('追踪中...', 'Tracing...')
    content = content.replace('输入目标地址后点击"开始追踪"', 'Enter a target and click "Start Trace"')
    content = content.replace('没有可复制的结果', 'No results to copy')
    content = content.replace('Traceroute to ', 'Traceroute to ')

    # error messages
    content = content.replace('哈希格式无效。bcrypt哈希应以 $2a$、$2b$ 或 $2y$ 开头', 'Invalid hash format. Bcrypt hash should start with $2a$, $2b$, or $2y$')
    content = content.replace('轮数必须在4-31之间，当前为 ', 'Rounds must be between 4-31, got ')
    content = content.replace('⚠️ 纯JS无法执行完整的bcrypt验证', '⚠️ Pure JS cannot perform full bcrypt verification')
    content = content.replace('。此结果仅供参考格式分析。建议在生产环境中使用bcryptjs库或服务端验证。', '. This result is for format analysis only. Use bcryptjs library or server-side verification in production.')
    content = content.replace('📊 哈希结构: ', '📊 Hash Structure: ')
    content = content.replace('格式=', 'Format=')
    content = content.replace('轮数=', 'Rounds=')
    content = content.replace('盐=', 'Salt=')
    content = content.replace('哈希=', 'Hash=')
    content = content.replace('✅ 哈希格式有效', '✅ Hash format valid')
    content = content.replace('❌ 密码不匹配。', '❌ Password does not match.')
    content = content.replace('✅ 密码匹配！哈希验证通过。', '✅ Password matches! Hash verified.')
    content = content.replace('完整哈希: ', 'Full Hash: ')
    content = content.replace('格式: ', 'Format: ')
    content = content.replace('轮数: ', 'Rounds: ')
    content = content.replace('盐值: ', 'Salt: ')
    content = content.replace(' (cost factor)', ' (cost factor)')

    # Days-until specific
    content = content.replace('距离 ', 'Until ')
    content = content.replace(' 还有', ' - ')
    content = content.replace('天 ', 'd ')
    content = content.replace('小时 ', 'h ')
    content = content.replace('分钟', 'min')
    content = content.replace('🎉 时间到！', '🎉 Time\'s up!')
    content = content.replace('年', '-')
    content = content.replace('月', '-')
    content = content.replace('日', '')

    # Write EN file
    with open(en_path, 'w') as f:
        f.write(content)
    print(f'  ✅ {tool_name} EN')

for tool_name, info in TOOLS.items():
    try:
        translate_file(tool_name, info)
    except Exception as e:
        print(f'  ❌ {tool_name}: {e}')

print('Done!')
