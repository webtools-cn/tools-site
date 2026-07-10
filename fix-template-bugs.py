#!/usr/bin/env python3
"""
批量修复6个工具页面的模板复制错误。
问题：6个EN页面的OG description、Schema description、FAQ内容错误地使用了JS beautifier的模板描述。
"""
import re
import json
import os

TOOLS = {
    "en/sass-to-css/index.html": {
        "title": "Sass/SCSS to CSS Converter",
        "desc": "Free online Sass/SCSS to CSS converter. Compile Sass and SCSS code to clean CSS instantly with full support for variables, nesting, mixins, inheritance, functions, and partials. Pure frontend, zero upload.",
        "faq": [
            ("What is Sass/SCSS to CSS Converter?",
             "It is a free online tool that compiles Sass/SCSS code into standard CSS. It supports all Sass features including variables, nesting, mixins, inheritance, functions, and partials — all processed locally in your browser."),
            ("Do I need to upload my Sass code to a server?",
             "No. All compilation happens locally in your browser. Your Sass/SCSS code is never uploaded to any server, ensuring your stylesheet code remains private and secure."),
            ("What Sass features are supported?",
             "The tool supports all major Sass features: variables ($var), nesting, mixins (@mixin/@include), inheritance (@extend), functions (@function), partials (@import/@use), control directives (@if/@for/@each/@while), and mathematical operations."),
            ("Can I convert both .sass and .scss syntax?",
             "Yes. The tool supports both SCSS syntax (CSS-like with curly braces) and the original Sass syntax (indentation-based). Simply paste your code and the compiler handles the rest."),
            ("Can I download the compiled CSS?",
             "Yes. After compilation, you can copy the result to clipboard with one click or download it as a .css file. All formatting is preserved."),
            ("Is this tool free to use?",
             "Yes, completely free. No registration, no payment, no limits on usage. Part of the Online Tools collection."),
        ]
    },
    "en/text-diff-checker/index.html": {
        "title": "Text Diff Checker",
        "desc": "Free online text diff checker. Compare two texts side by side and instantly highlight additions, deletions, and changes. Supports line-by-line, word-by-word, and character-level comparison. Pure frontend, zero upload.",
        "faq": [
            ("How does the Text Diff Checker work?",
             "Paste or type two versions of text into the left and right panels. The tool compares them instantly and highlights differences: added text in green, removed text in red, and changed text in yellow."),
            ("Do I need to upload my text to a server?",
             "No. All comparison is done locally in your browser. Your text data is never uploaded to any server, ensuring complete privacy and security."),
            ("What comparison modes are supported?",
             "Three modes: line-by-line (compares entire lines), word-by-word (highlights individual word changes), and character-by-character (shows exact character-level differences for fine detail)."),
            ("Can I compare code files?",
             "Yes. The tool works great for comparing source code, configuration files, JSON, HTML, and any text-based content. Line-by-line mode is ideal for code reviews."),
            ("Can I share or save the diff results?",
             "You can copy the diff results or download them. The tool also shows a unified diff format that can be shared with your team."),
            ("Is this tool free?",
             "Yes, completely free. No registration, no payment, no usage limits. Part of the Online Tools collection."),
        ]
    },
    "en/less-to-css/index.html": {
        "title": "Less to CSS Converter",
        "desc": "Free online Less to CSS converter. Compile Less code to standard CSS instantly with full support for variables, nesting, mixins, operations, functions, and imports. Pure frontend, zero upload.",
        "faq": [
            ("What is Less to CSS Converter?",
             "It is a free online tool that compiles Less (Leaner Style Sheets) code into standard CSS. It supports all Less features including variables, nesting, mixins, operations, functions, and imports — all processed in your browser."),
            ("Do I need to upload my Less code to a server?",
             "No. All compilation happens locally in your browser. Your Less code never leaves your device, ensuring complete privacy and security."),
            ("What Less features are supported?",
             "Full support for Less variables (@var), nesting, mixins (.mixin()), parametric mixins, operations (+, -, *, /), built-in functions (lighten, darken, fade, mix, etc.), namespaces, scope, and imports (@import)."),
            ("Can I convert both .less files and inline code?",
             "Yes. You can either paste your Less code directly or upload a .less file. The compiler processes both identically and outputs clean, browser-ready CSS."),
            ("Can I download the compiled CSS?",
             "Yes. After compilation, you can copy the result to clipboard or download it as a .css file. The output is formatted with proper indentation for readability."),
            ("Is this tool free?",
             "Yes, completely free. No registration, no payment, no usage limits. Part of the Online Tools collection."),
        ]
    },
    "en/text-sorter/index.html": {
        "title": "Text Sorter",
        "desc": "Free online text sorter. Sort text lines alphabetically (A-Z or Z-A), numerically, by line length, or randomly in seconds. Remove duplicates, trim whitespace, and ignore empty lines. Pure frontend, zero upload.",
        "faq": [
            ("How does the Text Sorter work?",
             "Paste your text in the input area and choose a sort mode: Alphabetical (A-Z or Z-A), Numeric, By Line Length, or Random. The sorted result appears instantly."),
            ("Do I need to upload my text to a server?",
             "No. All sorting is done locally in your browser. Your text data never leaves your device, ensuring complete privacy."),
            ("What sorting options are available?",
             "Five modes: A-Z (ascending alphabetical), Z-A (descending alphabetical), Numeric (sorted by number value), By Length (shortest/longest first), and Random (shuffle lines randomly)."),
            ("Can I remove duplicates while sorting?",
             "Yes. The tool has a 'Remove Duplicates' option that eliminates duplicate lines during sorting, leaving only unique entries."),
            ("What delimiters are supported?",
             "By default, the tool sorts line by line. You can also sort comma-separated, tab-separated, or custom-delimited values by splitting on your chosen delimiter."),
            ("Is this tool free?",
             "Yes, completely free. No registration, no payment, no usage limits. Part of the Online Tools collection."),
        ]
    },
    "en/list-to-json/index.html": {
        "title": "List to JSON Converter",
        "desc": "Free online list to JSON converter. Transform comma-separated, newline-separated, or custom-delimited lists into valid JSON arrays instantly. Supports nested structures, mixed types, and pretty-print formatting. Pure frontend.",
        "faq": [
            ("How does List to JSON Converter work?",
             "Paste a list of items (one per line or comma-separated) and click convert. The tool transforms your list into a valid JSON array, with each item as an array element."),
            ("Do I need to upload my data to a server?",
             "No. All conversion is done locally in your browser. Your data is never uploaded to any server, ensuring privacy and security."),
            ("What input formats are supported?",
             "Supports newline-separated (one item per line), comma-separated (CSV), tab-separated (TSV), and custom delimiters. You can also choose to quote each entry or handle numbers as numeric types."),
            ("Can I convert to nested JSON structures?",
             "Yes. For multi-column data (CSV with headers), the tool can generate an array of objects with key-value pairs, creating properly nested JSON structures."),
            ("Can I download the JSON output?",
             "Yes. After conversion, you can copy the JSON to clipboard or download it as a .json file. Output can be minified or pretty-printed with configurable indentation."),
            ("Is this tool free?",
             "Yes, completely free. No registration, no payment, no usage limits. Part of the Online Tools collection."),
        ]
    },
    "en/hash-file-checker/index.html": {
        "title": "File Hash Checker",
        "desc": "Free online file hash checker. Compute MD5, SHA-1, SHA-256, SHA-384, and SHA-512 checksums of any file instantly. Verify file integrity, detect corruption, and confirm downloads. Pure frontend, file never uploaded.",
        "faq": [
            ("How does File Hash Checker work?",
             "Select or drag-and-drop any file onto the tool. It computes the file's cryptographic hash using your selected algorithm and displays the checksum in real time — all in your browser."),
            ("Do I need to upload my file to a server?",
             "No. Absolutely not. The entire hash computation happens locally in your browser using the Web Crypto API. Your file never leaves your device."),
            ("What hash algorithms are supported?",
             "Five industry-standard algorithms: MD5 (128-bit), SHA-1 (160-bit), SHA-256 (256-bit), SHA-384 (384-bit), and SHA-512 (512-bit). You can compute multiple hashes simultaneously."),
            ("What is the maximum file size?",
             "There is no hard limit. Since the file is processed locally in your browser, performance depends on your device's memory and processing power. Most files up to several GB work well."),
            ("Can I compare two files' hashes?",
             "Yes. The tool supports hash comparison — compute the hash of one file and compare it against a known checksum to verify file integrity. It will indicate whether they match."),
            ("Is this tool free?",
             "Yes, completely free. No registration, no payment, no usage limits. Part of the Online Tools collection."),
        ]
    }
}

# Also fix CN FAQ for these tools
CN_TOOLS = {
    "sass-to-css/index.html": {
        "lang": "zh-CN",
        "faq": [
            ("什么是Sass/SCSS转CSS工具？",
             "这是一个免费在线工具，用于将Sass/SCSS代码编译为标准CSS。支持所有Sass特性，包括变量、嵌套、Mixin、继承、函数和Partial。所有处理都在你的浏览器本地完成。"),
            ("需要上传Sass代码到服务器吗？",
             "不需要。所有编译操作完全在您的浏览器中本地执行，Sass/SCSS代码不会上传到任何服务器，保障您的样式表代码安全。"),
            ("支持哪些Sass特性？",
             "支持所有主要Sass特性：变量($var)、嵌套、Mixin(@mixin/@include)、继承(@extend)、函数(@function)、Partial(@import/@use)、控制指令(@if/@for/@each/@while)和数学运算。"),
            ("支持.sass和.scss两种语法吗？",
             "支持。工具同时支持SCSS语法（类似CSS的花括号写法）和原始Sass语法（缩进式写法）。直接粘贴代码，编译器会自动识别处理。"),
            ("可以下载编译后的CSS吗？",
             "可以。编译完成后，您可以一键复制结果到剪贴板，或点击下载保存为.css文件。输出格式保持整洁缩进。"),
            ("本工具收费吗？",
             "完全免费。无需注册、无需付费、无使用限制。属于在线小工具矩阵的一部分。"),
        ]
    },
    "text-diff-checker/index.html": {
        "lang": "zh-CN",
        "faq": [
            ("文本差异对比工具怎么用？",
             "将两段文本分别粘贴到左侧和右侧输入框中，工具会立即对比并高亮显示差异：新增内容绿色、删除内容红色、修改内容黄色。"),
            ("需要上传文本到服务器吗？",
             "不需要。所有对比操作完全在您的浏览器中本地执行，您的文本数据不会上传到任何服务器，确保隐私安全。"),
            ("支持哪些对比模式？",
             "三种模式：逐行对比（比较整行差异）、逐词对比（高亮单词级别的变化）、逐字符对比（精确显示每个字符的差异）。"),
            ("可以对比代码文件吗？",
             "可以。工具非常适合对比源代码、配置文件、JSON、HTML等任何文本内容。逐行模式最适合代码审查。"),
            ("可以分享或保存对比结果吗？",
             "您可以复制差异结果，或下载对比报告。工具还支持统一差异格式(unified diff)，方便团队协作。"),
            ("本工具收费吗？",
             "完全免费。无需注册、无需付费、无使用限制。属于在线小工具矩阵的一部分。"),
        ]
    },
    "less-to-css/index.html": {
        "lang": "zh-CN",
        "faq": [
            ("什么是Less转CSS工具？",
             "这是一个免费在线工具，用于将Less代码编译为标准CSS。支持所有Less特性，包括变量、嵌套、Mixin、运算、函数和导入。所有处理都在你的浏览器本地完成。"),
            ("需要上传Less代码到服务器吗？",
             "不需要。所有编译操作完全在您的浏览器中本地执行，Less代码不会上传到任何服务器。"),
            ("支持哪些Less特性？",
             "完整支持Less变量(@var)、嵌套、Mixin(.mixin()带参数)、运算(+ - * /)、内置函数(lighten, darken, fade等)、命名空间、作用域和@import导入。"),
            ("支持.less文件和直接粘贴代码吗？",
             "都支持。您可以粘贴Less代码，也可以上传.less文件。两种方式都输出相同的干净CSS。"),
            ("可以下载编译后的CSS吗？",
             "可以。编译完成后可一键复制或下载为.css文件。输出格式保持良好的缩进。"),
            ("本工具收费吗？",
             "完全免费。无需注册、无需付费、无使用限制。属于在线小工具矩阵的一部分。"),
        ]
    },
    "text-sorter/index.html": {
        "lang": "zh-CN",
        "faq": [
            ("文本排序工具怎么用？",
             "将文本粘贴到输入区域，选择排序方式：字母序(A-Z或Z-A)、数字排序、按行长度排序或随机排序。结果立即显示。"),
            ("需要上传文本到服务器吗？",
             "不需要。所有排序操作完全在您的浏览器中本地执行，文本数据不会上传到任何服务器。"),
            ("支持哪些排序方式？",
             "五种模式：A-Z(升序字母序)、Z-A(降序字母序)、数字排序(按数值)、按长度(最短/最长优先)、随机排序(打乱行顺序)。"),
            ("排序时可以去除重复行吗？",
             "可以。工具提供\"去除重复行\"选项，排序时自动消除重复内容，只保留唯一条目。"),
            ("支持哪些分隔符？",
             "默认按行排序。也支持逗号分隔、Tab分隔或自定义分隔符的值进行排序。"),
            ("本工具收费吗？",
             "完全免费。无需注册、无需付费、无使用限制。属于在线小工具矩阵的一部分。"),
        ]
    },
    "list-to-json/index.html": {
        "lang": "zh-CN",
        "faq": [
            ("列表转JSON工具怎么用？",
             "粘贴列表（每行一个或逗号分隔），点击转换。工具将您的列表转换为有效的JSON数组，每个条目作为一个数组元素。"),
            ("需要上传数据到服务器吗？",
             "不需要。所有转换操作完全在您的浏览器中本地执行，数据不会上传到任何服务器。"),
            ("支持哪些输入格式？",
             "支持换行分隔（每行一项）、逗号分隔(CSV)、Tab分隔(TSV)和自定义分隔符。可选择是否给每项加引号或将数字保留为数值类型。"),
            ("可以转换为嵌套JSON吗？",
             "可以。对于多列数据（带表头的CSV），工具可以生成对象数组，每个对象包含键值对，形成正确的嵌套JSON结构。"),
            ("可以下载JSON吗？",
             "可以。转换后可一键复制或下载为.json文件。支持紧凑格式或格式化输出（可配置缩进）。"),
            ("本工具收费吗？",
             "完全免费。无需注册、无需付费、无使用限制。属于在线小工具矩阵的一部分。"),
        ]
    },
    "hash-file-checker/index.html": {
        "lang": "zh-CN",
        "faq": [
            ("文件哈希校验工具怎么用？",
             "选择或拖拽任意文件到工具上。工具使用您选择的算法计算文件的加密哈希值，并实时显示校验码——全部在浏览器中完成。"),
            ("需要上传文件到服务器吗？",
             "完全不需要。整个哈希计算在您的浏览器中使用Web Crypto API本地完成，文件不会离开您的设备。"),
            ("支持哪些哈希算法？",
             "五种业界标准算法：MD5(128位)、SHA-1(160位)、SHA-256(256位)、SHA-384(384位)和SHA-512(512位)。可同时计算多种哈希值。"),
            ("支持多大的文件？",
             "没有硬性限制。由于文件在浏览器本地处理，性能取决于您的设备内存和处理器。大多数几GB以内的文件都可以正常处理。"),
            ("可以对比两个文件的哈希值吗？",
             "可以。工具支持哈希对比——计算一个文件的哈希值后，与已知校验码对比，验证文件完整性。会显示是否匹配。"),
            ("本工具收费吗？",
             "完全免费。无需注册、无需付费、无使用限制。属于在线小工具矩阵的一部分。"),
        ]
    }
}

def generate_faq_json(faq_items):
    """Generate FAQPage schema JSON from list of (question, answer) tuples."""
    entities = []
    for q, a in faq_items:
        entities.append({
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {
                "@type": "Answer",
                "text": a
            }
        })
    return entities

def generate_faq_html(faq_items, lang="en"):
    """Generate visible FAQ HTML from list of (question, answer) tuples."""
    lines = []
    for q, a in faq_items:
        q_prefix = "❓ " if lang == "en" else "❓ "
        lines.append(f'<div class="faq-item"><div class="q">{q_prefix}{q}</div><div class="a">{a}</div></div>')
    return "\n".join(lines)

def fix_en_file(filepath, tool_config):
    """Fix an EN tool HTML file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    title = tool_config["title"]
    desc = tool_config["desc"]
    faq_items = tool_config["faq"]
    
    # 1. Fix meta description (usually just the tool name)
    meta_desc_pattern = r'<meta name="description" content="[^"]*">'
    content = re.sub(meta_desc_pattern, f'<meta name="description" content="{desc}">', content)
    
    # 2. Fix og:title if it's just the tool name (add context)
    og_title_pattern = r'<meta property="og:title" content="[^"]*">'
    new_og_title = f'<meta property="og:title" content="{title} - Free Online Tool">'
    content = re.sub(og_title_pattern, new_og_title, content)
    
    # 3. Fix og:description (has the JS beautifier text)
    og_desc_pattern = r'<meta property="og:description" content="Free online JavaScript beautifier and formatter[^"]*">'
    content = re.sub(og_desc_pattern, f'<meta property="og:description" content="{desc}">', content)
    
    # 4. Fix SoftwareApplication name (might already be correct, but let's be safe)
    # Fix SoftwareApplication description
    schema_desc_pattern = r'"description": "Free online JavaScript beautifier and formatter[^"]*"'
    content = re.sub(schema_desc_pattern, f'"description": "{desc}"', content)
    
    # 5. Fix the FAQPage schema - completely replace the FAQ JSON
    # Find the FAQPage schema block
    faq_entities = generate_faq_json(faq_items)
    new_faq_json = json.dumps({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": faq_entities
    }, ensure_ascii=False, indent=None)
    
    # Match the FAQPage schema pattern - from "@context" to the end of the FAQPage JSON
    faq_schema_pattern = r'\{"@context": "https://schema\.org", "@type": "FAQPage", "mainEntity": \[.*?\]\}'
    content = re.sub(faq_schema_pattern, new_faq_json, content, flags=re.DOTALL)
    
    # 6. Fix visible FAQ HTML section - find the FAQ items and replace them
    # The visible FAQ has patterns like:
    # <div class="faq-item"><div class="q">❓ Do I need to upload my code?</div><div class="a">...</div></div>
    # We need to find the entire FAQ section and replace it
    
    faq_html_section = generate_faq_html(faq_items, "en")
    
    # Find the faq-section div and replace its contents
    # Pattern: <div class="faq-list"> ...existing faq items... </div>
    faq_list_pattern = r'<div class="faq-list">.*?</div>\s*(?=</div>\s*</section|\s*</div>\s*<div|\s*</section)'
    faq_list_replacement = f'<div class="faq-list">\n{faq_html_section}\n</div>'
    content = re.sub(faq_list_pattern, faq_list_replacement, content, flags=re.DOTALL)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Fixed: {filepath}")
        return True
    else:
        print(f"⚠️  No changes made to: {filepath}")
        return False

def fix_cn_file(tool_dir, tool_config):
    """Fix a CN tool HTML file's FAQ (since OG/description was already correct)."""
    filepath = os.path.join("cn" if os.path.exists(f"cn/{tool_dir}") else "", tool_dir)
    if os.path.exists(tool_dir):
        filepath = tool_dir
    elif os.path.exists(f"cn/{tool_dir}"):
        filepath = f"cn/{tool_dir}"
    
    if not os.path.exists(filepath):
        print(f"⚠️  CN file not found: {tool_dir}")
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    faq_items = tool_config["faq"]
    
    # Fix FAQPage schema
    faq_entities = generate_faq_json(faq_items)
    new_faq_json = json.dumps({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": faq_entities
    }, ensure_ascii=False, indent=None)
    
    faq_schema_pattern = r'\{"@context": "https://schema\.org", "@type": "FAQPage", "mainEntity": \[.*?\]\}'
    content = re.sub(faq_schema_pattern, new_faq_json, content, flags=re.DOTALL)
    
    # Fix visible FAQ HTML
    faq_html_section = generate_faq_html(faq_items, "zh")
    faq_list_pattern = r'<div class="faq-list">.*?</div>\s*(?=</div>\s*</section|\s*</div>\s*<div|\s*</section)'
    faq_list_replacement = f'<div class="faq-list">\n{faq_html_section}\n</div>'
    content = re.sub(faq_list_pattern, faq_list_replacement, content, flags=re.DOTALL)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Fixed CN: {filepath}")
        return True
    else:
        print(f"⚠️  No changes to CN: {filepath}")
        return False

# Fix all 6 EN tools
success = 0
for rel_path, config in TOOLS.items():
    full_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), rel_path)
    if os.path.exists(full_path):
        if fix_en_file(full_path, config):
            success += 1
    else:
        print(f"❌ File not found: {full_path}")

print(f"\n=== EN修复完成: {success}/{len(TOOLS)} ===")

# Fix CN FAQ for corresponding tools
cn_success = 0
for tool_dir, config in CN_TOOLS.items():
    full_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), tool_dir)
    if os.path.exists(full_path):
        if fix_cn_file(full_path, config):
            cn_success += 1
    else:
        print(f"❌ CN file not found: {full_path}")

print(f"\n=== CN FAQ修复完成: {cn_success}/{len(CN_TOOLS)} ===")
