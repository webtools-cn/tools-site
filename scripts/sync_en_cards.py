#!/usr/bin/env python3
"""同步EN首页缺失的46个工具卡片"""
import re

# 从CN首页提取的46个工具信息 (tool_name, tool_icon, tool_desc_cn, tool_desc_en, category, href)
tools = [
    ("Atbash密码", "🔐", "字母表反转替换密码，最古老的单表替换密码之一", "Atbash Cipher - ancient letter-reversal substitution cipher, one of the oldest monoalphabetic ciphers", "utility", "atbash/"),
    ("批量重命名", "📝", "支持前缀/后缀/替换/序号规则，生成重命名脚本", "Batch Rename - prefix/suffix/replace/number rules, generate rename scripts", "utility", "batch-rename/"),
    ("证书解码器", "🔐", "在线SSL/TLS证书解码，解析X.509证书信息", "SSL/TLS Certificate Decoder - parse X.509 certificate details online", "developer-tools", "certificate-decoder/"),
    ("字符Unicode查询", "🔤", "输入任意字符查询其Unicode编码、HTML实体、URL编码等详细信息，支持一键复制。", "Character Unicode Finder - lookup Unicode, HTML entity, URL encoding for any character, one-click copy", "developer-tools", "character-unicode-finder/"),
    ("图片渐变色提取", "🎨", "上传图片自动提取主要颜色和渐变配色方案，生成CSS代码，适合UI配色参考。", "Color Gradient Extractor - upload image to extract dominant colors and gradient palettes, generate CSS", "new-tools", "color-gradient-extractor/"),
    ("复利计算器", "📈", "计算投资复利增长，年/月/日复利+定投模拟", "Compound Interest Calculator - calculate investment growth with annual/monthly/daily compounding + DCA", "utility", "compound-interest/"),
    ("CSS前缀生成器", "🧬", "自动为CSS属性添加-webkit-、-moz-、-ms-浏览器前缀，提高跨浏览器兼容性。", "CSS Prefix Generator - auto-add -webkit-, -moz-, -ms- browser prefixes for cross-browser compatibility", "developer-tools", "css-prefix-generator/"),
    ("CSV转JSON Schema", "📊", "解析CSV数据自动推断字段类型并生成JSON Schema定义，支持一键复制。", "CSV to JSON Schema - parse CSV to infer field types and generate JSON Schema, one-click copy", "new-tools", "csv-to-json-schema/"),
    ("Data URI转图片", "🔗", "在线将Base64编码的Data URI解码为图片文件，支持PNG/JPG/GIF/SVG/WebP下载。", "Data URI to Image - decode Base64 Data URI to image file, support PNG/JPG/GIF/SVG/WebP download", "new-tools", "data-uri-to-image/"),
    ("日期差计算器", "📅", "计算两个日期间的天数/周数/月数/年数差", "Date Difference Calculator - calculate days/weeks/months/years between two dates", "date-time", "date-difference/"),
    ("日期格式转换器", "📅", "多种日期格式互相转换，支持ISO 8601、Unix时间戳、RFC 2822和自定义格式。", "Date Format Converter - convert between ISO 8601, Unix timestamp, RFC 2822 and custom formats", "utility-tools", "date-format-converter/"),
    ("星期几计算器", "📆", "输入日期快速查询对应星期几", "Day of Week Calculator - quickly find what day of the week any date falls on", "date-time", "day-of-week-calculator/"),
    ("日期相差天数", "📅", "计算两日期精确差距，支持排除周末", "Days Between Dates - calculate exact gap between two dates, exclude weekends option", "utility", "days-between/"),
    ("指数计算器", "📊", "在线指数幂运算，支持任意底数和指数", "Exponent Calculator - online power calculations with any base and exponent", "math", "exponent-calculator/"),
    ("文件格式转换器", "🔄", "支持JSON/CSV/XML/YAML/TOML互转，Base64和URL编解码，纯前端处理。", "File Format Converter - JSON/CSV/XML/YAML/TOML interconversion, Base64 & URL encode/decode, client-side only", "developer-tools", "file-converter/"),
    ("Flexbox可视化练习", "📐", "实时调整flex属性查看效果，理解justify-content/align-items等CSS布局。", "Flexbox Playground - real-time flex property adjustment, visualize CSS layout concepts interactively", "new-tools", "flexbox-playground/"),
    ("最大公因数计算器", "🔢", "计算多个数的最大公因数(GCF)", "GCF Calculator - find Greatest Common Factor of multiple numbers", "math", "gcf-calculator/"),
    ("CSS渐变代码生成器", "🎨", "可视化拖拽创建线性/径向/锥形渐变，实时预览并生成CSS代码，支持复制。", "CSS Gradient Generator - visual drag-and-drop linear/radial/conic gradients, live preview and CSS code", "new-tools", "gradient-code-generator/"),
    ("GUID生成器", "🆔", "在线生成全局唯一标识符GUID/UUID", "GUID/UUID Generator - online globally unique identifier generation", "developer-tools", "guid-generator/"),
    ("俳句生成器", "🌸", "输入主题生成传统日本俳句（5-7-5音节），支持自然/四季/爱情/禅意等多风格。", "Haiku Generator - generate traditional 5-7-5 haiku by theme, nature/seasons/love/zen styles", "text-tools", "haiku-generator/"),
    ("HTML颜色名称查询", "🎨", "浏览和搜索全部147种标准HTML颜色名称，预览颜色并获取HEX值，支持一键复制。", "HTML Color Names - browse all 147 standard HTML color names, preview colors and get HEX values", "developer-tools", "html-color-names/"),
    ("在线图片裁剪", "✂️", "上传图片后拖拽选择区域裁剪，支持自由比例和1:1/4:3/16:9固定比例下载。", "Online Image Cropper - upload and drag to crop, free ratio or 1:1/4:3/16:9 presets, download result", "new-tools", "image-cropper-online/"),
    ("图片转PNG", "🖼️", "将JPG、WebP、GIF、BMP等格式转换为PNG，纯浏览器端处理，安全隐私。", "Image to PNG Converter - convert JPG/WebP/GIF/BMP to PNG, browser-side processing, private & secure", "image-tools", "image-to-png/"),
    ("JSON差异对比", "🔍", "对比两个JSON对象找出新增/修改/删除字段，JSON Patch格式输出，一目了然。", "JSON Diff & Patch - compare two JSON objects, find added/modified/deleted fields, JSON Patch output", "new-tools", "json-diff-patch/"),
    ("JSON-LD生成器", "📋", "快速生成Article/Product/Breadcrumb/FAQ等Schema.org结构化数据标记。", "JSON-LD Generator - generate Article/Product/Breadcrumb/FAQ Schema.org structured data markup", "seo-tools", "json-ld/"),
    ("JSON转查询字符串", "🔗", "将JSON对象转换为URL查询参数格式，支持嵌套对象和数组，一键复制。", "JSON to Query String - convert JSON object to URL query parameters, nested objects & arrays supported", "developer-tools", "json-to-query-string/"),
    ("JWT在线验证", "🔑", "解析JWT Header/Payload，验证过期和签名", "JWT Verifier - decode JWT Header/Payload, validate expiration and signature online", "developer-tools", "jwt-verify/"),
    ("列表随机排序", "🔀", "将列表项随机打乱顺序，每行一个项目，支持多次洗牌和一键复制。", "List Shuffler - randomize list order, one item per line, multiple shuffles and one-click copy", "random-tools", "list-shuffler/"),
    ("Markdown转Google文档", "📄", "将Markdown转换为富文本格式，可直接复制粘贴到Google Docs、Word等编辑器。", "Markdown to Google Docs - convert Markdown to rich text, paste directly into Google Docs/Word", "text-tools", "markdown-to-google-docs/"),
    ("NATO音标字母表", "📻", "在线字母/数字与北约标准音标码双向转换", "NATO Phonetic Alphabet - online letter/number to NATO phonetic code bidirectional converter", "utility", "nato-alphabet/"),
    ("OG标签生成器", "📝", "在线生成Open Graph元标签，自动输出og:title/og:description等社交媒体分享标签。", "OG Tag Generator - generate Open Graph meta tags, auto-output og:title/og:description for social sharing", "seo-tools", "og-tag-generator/"),
    ("Open Graph标签检查器", "🔍", "输入URL检测og:title/description/image等OG标签，预览社交媒体分享效果。", "Open Graph Checker - check og:title/description/image tags by URL, preview social media share appearance", "seo-tools", "open-graph-checker/"),
    ("质数计算器", "🔢", "质数检测和生成，判断是否为质数", "Prime Number Calculator - primality testing and prime generation online", "math", "prime-number-calculator/"),
    ("进度条生成器", "📊", "可视化设计进度条样式，实时生成CSS代码", "Progress Bar Generator - visually design progress bar styles, generate CSS code in real-time", "developer-tools", "progress-bar/"),
    ("随机选择器", "🎲", "从列表中随机选择一个或多个项目，支持去重和自定义数量，适合抽奖和决策。", "Random Choice Picker - randomly select one or more items from a list, with dedup and custom count", "random-tools", "random-choice-picker/"),
    ("RSS Feed生成器", "📡", "快速创建标准RSS 2.0 XML Feed，支持多条目添加和一键下载，适用于博客和新闻站点。", "RSS Feed Generator - create standard RSS 2.0 XML feeds, multiple entries, one-click download", "developer-tools", "rss-generator/"),
    ("AA制分账计算器", "💸", "按人数均分账单，支持小费和自定义分摊比例", "Split Bill Calculator - split bills evenly, support tips and custom ratios", "utility", "split-bill/"),
    ("平方根计算器", "√", "平方根、立方根、N次根号在线计算", "Square Root Calculator - compute square roots, cube roots, nth roots online", "math", "square-root-calculator/"),
    ("字符串构建器", "🔤", "模板拼接、批量替换、大小写转换", "String Builder - template concatenation, batch replace, case conversion", "text-tools", "string-builder/"),
    ("敲击码转换器", "👆", "5×5网格密码，历史战俘通信方式", "Tap Code Converter - 5×5 grid cipher, historical POW communication method", "utility", "tap-code/"),
    ("文字样式生成器", "✨", "生成粗体/斜体/手写体/双线/圆圈等多种Unicode文字样式，一键复制到社交媒体。", "Text Styler - generate bold/italic/cursive/double-struck/circled Unicode text styles for social media", "new-tools", "text-styler/"),
    ("文本转二进制", "0️⃣1️⃣", "将文本转换为8位二进制表示，支持ASCII和Unicode字符，一键复制结果。", "Text to Binary Converter - convert text to 8-bit binary, supports ASCII and Unicode, one-click copy", "developer-tools", "text-to-binary-converter/"),
    ("三角函数计算器", "📐", "sin/cos/tan在线计算，角度弧度切换", "Trigonometry Calculator - sin/cos/tan online, degree/radian mode switching", "math", "trigonometry-calculator/"),
    ("语音转文字", "🎤", "使用浏览器内置语音识别将语音实时转为文字，支持中英日韩多语言，纯本地处理。", "Voice to Text - browser-based speech recognition, real-time transcription, supports multi-language, local processing", "utility-tools", "voice-to-text/"),
    ("网站速度测试", "🚀", "分析页面大小、资源数量、加载时间，获取性能优化建议，提升网站速度。", "Website Speed Test - analyze page size, resource count, load time, get performance optimization tips", "seo-tools", "website-speed-test/"),
    ("周数查询", "📆", "查询任意日期的ISO周数，全年周数概览", "Week Number Finder - lookup ISO week number for any date, full year week overview", "utility", "week-number/"),
]

# 生成EN卡片HTML
en_cards = []
for name, icon, desc_cn, desc_en, cat, href in tools:
    # EN卡片格式
    card = f'<div class="tool-card" data-cat="{cat}"><span class="tool-icon">{icon}</span><span class="tool-name">{name}</span><span class="tool-desc">{desc_en}</span><a href="/en/{href}" class="btn">Use Now</a></div>'
    en_cards.append(card)

# 读取EN首页
with open('en/index.html', 'r') as f:
    en_content = f.read()

# 找到最后一个tool-card的位置，在其后插入
# 先找 tools-grid 的结束位置
tools_grid_end = en_content.rfind('</div>', en_content.find('tools-grid'))
# 更精确：找到最后一个 </div> 在 tools-grid 区域内
import_pos = en_content.find('<!-- end tools-grid -->')
if import_pos == -1:
    # fallback: 找到 tools-grid 闭合标签
    start = en_content.find('class="tools-grid"')
    # 找到对应的闭合 </div> 
    depth = 0
    i = en_content.find('class="tools-grid"')
    # 简单方式：找最后一个tool-card后面的闭合div
    last_card_pos = en_content.rfind('tool-card')
    # 从last_card_pos往后找下一个</div>
    end_pos = en_content.find('</div>', last_card_pos)
    # 再找下一个</div>（这是tools-grid的闭合）
    end_pos2 = en_content.find('</div>', end_pos + 6)
    import_pos = end_pos2
else:
    import_pos = import_pos  # 直接在此标记前插入

# 插入新卡片
cards_html = '\n'.join(en_cards)
new_en = en_content[:import_pos] + '\n' + cards_html + '\n' + en_content[import_pos:]

with open('en/index.html', 'w') as f:
    f.write(new_en)

print(f"已插入 {len(en_cards)} 个EN卡片")