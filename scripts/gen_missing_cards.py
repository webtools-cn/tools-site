#!/usr/bin/env python3
"""批量添加缺失工具的首页卡片到 CN 和 EN 首页"""
import re

# 20个缺失工具的数据
tools_cn = {
    "barcode-generator": ("条形码生成器", "免费在线条形码生成器，支持Code128、EAN-13、EAN-8、UPC-A等主流条码格式。纯前端本地生成，可自定义尺寸和颜色。"),
    "cookie-analyzer": ("Cookie分析器", "查看和管理当前网站的Cookie，支持查看名称、值、域名、路径、过期时间等详细信息。保护您的隐私。"),
    "dns-records": ("DNS记录查询", "在线DNS记录查询工具，支持A/AAAA/CNAME/MX/NS/TXT/SOA等多种记录类型。快速获取域名解析信息。"),
    "email-verifier": ("邮箱验证器", "在线邮箱格式验证工具，检查邮箱地址是否有效。支持格式校验、域名MX记录检测和常见临时邮箱识别。"),
    "git-cheatsheet": ("Git命令速查表", "免费在线Git命令速查表，包含常用Git命令的中文说明和示例。支持搜索、分类浏览、一键复制命令。"),
    "google-fonts-preview": ("Google Fonts预览", "在线Google Fonts字体预览工具，支持搜索和预览上千种免费字体。实时调整字重、字号和样式。"),
    "icon-finder": ("图标搜索器", "在线Emoji和Unicode符号搜索工具。快速查找并复制各种图标、表情符号和特殊字符，支持分类浏览。"),
    "jsonpath-tester": ("JSONPath查询测试器", "免费在线JSONPath查询测试器。支持实时解析JSON数据、测试JSONPath表达式、查看匹配结果。"),
    "keycode-finder": ("键盘按键检测器", "免费在线键盘按键检测器。实时检测键盘按键的keyCode、key、code等属性值，开发调试必备。"),
    "leet-speak-generator": ("Leet Speak生成器", "在线Leet Speak(1337)文本转换工具。将普通文本转换为黑客风格的Leet语言，支持多种替换规则。"),
    "localstorage-viewer": ("LocalStorage浏览器", "在线查看和管理浏览器的LocalStorage数据。支持查看键值、修改值、删除条目和导出JSON。"),
    "mimetype-checker": ("MIME类型查询", "免费在线MIME类型查询工具。输入文件扩展名或MIME类型快速查找对应的Content-Type。覆盖600+常见类型。"),
    "qrcode-reader": ("二维码识别工具", "免费在线二维码识别工具。上传图片或使用摄像头扫描二维码，即时解析QR Code内容。"),
    "regex-cheatsheet": ("正则表达式速查表", "免费在线正则表达式速查表+测试器。交互式正则速查，实时匹配高亮，支持常用正则模式库。"),
    "screen-resolution-checker": ("屏幕分辨率检测", "在线检测您的屏幕分辨率、视口尺寸、像素比、色彩深度等显示器参数。无需安装任何软件。"),
    "sessionstorage-viewer": ("SessionStorage浏览器", "在线查看和管理浏览器的SessionStorage数据。支持查看键值对、修改和删除，会话关闭后自动清除。"),
    "tap-code-translator": ("敲击码翻译器", "在线敲击码(Tap Code)编码解码工具。将文本转换为5×5网格敲击码，常用于密码学学习。"),
    "timezone-converter": ("时区转换器", "免费在线时区转换器，支持全球400+时区快速转换。选择来源和目标时区，即时显示转换结果。"),
    "viewport-checker": ("视口检测器", "实时检测浏览器视口尺寸。支持拖拽调整窗口查看不同断点下的视口大小，前端开发必备工具。"),
}

tools_en = {
    "barcode-generator": ("Free Online Barcode Generator", "Free online barcode generator supporting Code128, EAN-13, EAN-8, UPC-A, CODE39. Generate barcodes locally, customize size and colors."),
    "cookie-analyzer": ("Cookie Analyzer", "View and manage cookies for the current website. See name, value, domain, path, and expiry. Protect your privacy."),
    "dns-records": ("DNS Records Lookup", "Free online DNS records lookup tool. Query A, AAAA, CNAME, MX, NS, TXT, SOA records for any domain."),
    "email-verifier": ("Email Verifier", "Free online email verification tool. Validate email format, check MX records, and detect disposable emails."),
    "git-cheatsheet": ("Git Command Cheatsheet", "Free online Git command cheatsheet with 50+ common commands, descriptions, and examples. Search, browse, and copy."),
    "google-fonts-preview": ("Google Fonts Preview", "Free Google Fonts preview tool. Search and preview thousands of free fonts. Adjust weight, size, and style in real time."),
    "icon-finder": ("Icon Finder", "Free online emoji and Unicode symbol search tool. Find and copy icons, emojis, and special characters."),
    "jsonpath-tester": ("JSONPath Tester", "Free online JSONPath query tester. Test JSONPath expressions against JSON data in real time. View matched results."),
    "keycode-finder": ("Keyboard Keycode Finder", "Free keycode finder: press any key to see keyCode, key, code, and all event properties. Essential for developers."),
    "leet-speak-generator": ("Leet Speak Generator", "Free online Leet Speak (1337) text converter. Transform normal text into hacker-style leet language."),
    "localstorage-viewer": ("LocalStorage Viewer", "View and manage browser LocalStorage data. Inspect key-value pairs, edit values, delete entries, and export JSON."),
    "mimetype-checker": ("MIME Type Checker", "Free online MIME type checker. Look up Content-Type by file extension or MIME type. Covers 600+ common types."),
    "qrcode-reader": ("QR Code Reader", "Free online QR Code Reader. Upload an image or use your camera to scan and decode QR codes instantly."),
    "regex-cheatsheet": ("Regex Cheat Sheet", "Free online regex cheat sheet with interactive tester. Real-time match highlighting. Includes common pattern library."),
    "screen-resolution-checker": ("Screen Resolution Checker", "Check your screen resolution, viewport size, device pixel ratio, color depth, and more. No install required."),
    "sessionstorage-viewer": ("SessionStorage Viewer", "View and manage browser SessionStorage data. Inspect key-value pairs, edit and delete entries. Auto-clears on close."),
    "tap-code-translator": ("Tap Code Translator", "Free online Tap Code encoder and decoder. Convert text to 5x5 grid tap codes. Great for cryptography learning."),
    "timezone-converter": ("Timezone Converter", "Free online timezone converter supporting 400+ timezones worldwide. Select source and target timezones instantly."),
    "viewport-checker": ("Viewport Checker", "Real-time viewport size checker. Resize your browser to see viewport dimensions at different breakpoints."),
}

def gen_card_cn(name, desc, slug):
    return f'<div class="tool-card" data-category="utility"><span>{name}</span><p>{desc}</p><a href="/{slug}/" class="btn">立即使用</a></div>'

def gen_card_en(name, desc, slug):
    return f'<div class="tool-card" data-category="utility"><span>{name}</span><p>{desc}</p><a href="/en/{slug}/" class="btn">Use Now</a></div>'

# Generate CN cards
cn_cards = []
for slug, (name, desc) in tools_cn.items():
    cn_cards.append(gen_card_cn(name, desc, slug))

# Generate EN cards
en_cards = []
for slug, (name, desc) in tools_en.items():
    en_cards.append(gen_card_en(name, desc, slug))

print("=== CN CARDS ===")
print("\n".join(cn_cards))
print("\n=== EN CARDS ===")
print("\n".join(en_cards))
print(f"\nTotal: CN={len(cn_cards)}, EN={len(en_cards)}")