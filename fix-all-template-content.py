#!/usr/bin/env python3
"""
全面修复6个受影响的EN工具页面中的所有JS beautifier模板残留。
覆盖：How to Use, How It Works, Use Cases, FAQ可见HTML部分。
"""
import re
import os

# Each tool's correct descriptions for the body sections
TOOL_BODY = {
    "en/sass-to-css/index.html": {
        "how_to_use": "Paste or type your Sass/SCSS code in the input area and click 'Convert'. The tool compiles it to clean, browser-ready CSS instantly. Supports variables, nesting, mixins, inheritance, functions, and all Sass features.",
        "how_it_works": "Uses the sass.js compiler (a JavaScript port of Dart Sass) to parse and compile Sass/SCSS code to standard CSS entirely in your browser. No server-side processing needed.",
        "use_cases": "Convert Sass/SCSS to CSS for web projects; prototype styles quickly without setting up a build tool; learn Sass by seeing compiled output; share Sass code snippets with frontend teams.",
    },
    "en/text-diff-checker/index.html": {
        "how_to_use": "Paste two versions of text into the left and right panels. Choose a comparison mode (line, word, or character) and view the highlighted differences instantly.",
        "how_it_works": "Uses the diffs.js library to compute the longest common subsequence (LCS) between two texts, then renders additions, deletions, and changes with color-coded highlighting.",
        "use_cases": "Review code changes before committing; compare document revisions; find differences between configuration files; verify data migration accuracy; check plagiarism between texts.",
    },
    "en/less-to-css/index.html": {
        "how_to_use": "Paste or type your Less code in the input area and click 'Convert'. The tool compiles it to standard CSS instantly with support for variables, nesting, mixins, operations, and functions.",
        "how_it_works": "Uses the less.js compiler to parse and compile Less code to standard CSS entirely in your browser. Processes variables, mixins, operations, and imports with no server call.",
        "use_cases": "Convert Less to CSS for web projects; prototype styles without build tool setup; learn Less by seeing compiled output; share Less code snippets with your team.",
    },
    "en/text-sorter/index.html": {
        "how_to_use": "Paste your text into the input area. Choose a sort mode: A-Z, Z-A, Numeric, By Length, or Random. Optionally enable duplicate removal. Results appear instantly.",
        "how_it_works": "Uses JavaScript's native Array.sort() with custom comparators for each sort mode. Line-by-line processing with optional deduplication and whitespace trimming.",
        "use_cases": "Organize unformatted lists alphabetically; sort CSV data by specific columns; remove duplicate entries from mailing lists; randomize team assignments or prize draws.",
    },
    "en/list-to-json/index.html": {
        "how_to_use": "Paste a list of items (one per line, comma-separated, or custom-delimited) and click 'Convert'. The tool transforms your list into a valid JSON array. Choose output format (quoted, numeric, nested).",
        "how_it_works": "Parses input using configurable delimiters, then serializes into JSON arrays using JavaScript's JSON.stringify(). Supports pretty-print and minified output modes.",
        "use_cases": "Convert CSV exports to JSON for API integration; transform line-separated URLs to JSON arrays; prepare test data for frontend development; migrate data between different formats.",
    },
    "en/hash-file-checker/index.html": {
        "how_to_use": "Select or drag-and-drop any file onto the upload area. Choose one or more hash algorithms (MD5, SHA-1, SHA-256, SHA-384, SHA-512). The checksum is computed instantly in your browser.",
        "how_it_works": "Uses the Web Crypto API (SubtleCrypto.digest()) to compute cryptographic hash functions. The file is read as an ArrayBuffer and processed entirely in your browser — never uploaded.",
        "use_cases": "Verify downloaded files match the publisher's checksum; detect file corruption during transfer; confirm two files are identical; generate integrity checksums for distributed software packages.",
    }
}

# The old patterns to remove (from full sections)
OLD_SECTIONS_EN = [
    # How to Use - JS beautifier
    (r'<div class="content-section" id="options">\s*<h2>📖 How to Use</h2>\s*<p>One-click beautify and format JavaScript code with indentation adjustment, line break optimization, and syntax highlighting\. Handles minified/obfuscated code\.</p>\s*</div>',
     'HOW_TO_USE_PLACEHOLDER'),
    # How It Works - JS beautifier
    (r'<div class="content-section">\s*<h2>⚡ How It Works</h2>\s*<p>Uses a hybrid approach combining regex and AST analysis to format JavaScript code\. Supports ES5/ES6\+, TypeScript, and JSX syntax\.</p>\s*</div>',
     'HOW_IT_WORKS_PLACEHOLDER'),
    # Use Cases - JS beautifier
    (r'<div class="content-section">\s*<h2>💼 Use Cases</h2>\s*<p>Read and modify minified JS code; unify code style in projects; quickly restore obfuscated code during debugging; refactor legacy JavaScript projects\.</p>\s*</div>',
     'USE_CASES_PLACEHOLDER'),
    # Orphaned JS beautifier FAQ items
    (r'<div class="faq-item"><div class="q">❓ What formatting options are available\?</div><div class="a">Supports indentation size \(2/4/8 spaces or tab\), indentation type, space padding around operators, and HTML template beautification options\.</div></div>',
     None),
    (r'<div class="faq-item"><div class="q">❓ Can it handle minified JS\?</div><div class="a">Yes\. The tool is optimized for minified/obfuscated JavaScript code, automatically adding line breaks, adjusting indentation, and restoring readability\.</div></div>',
     None),
    (r'<div class="faq-item"><div class="q">❓ Which JS syntax does it support\?</div><div class="a">Supports ES5/ES6\+, TypeScript, and JSX\. The formatter engine recognizes the latest JavaScript language features\.</div></div>',
     None),
    (r'<div class="faq-item"><div class="q">❓ Can I copy the result\?</div><div class="a">Yes\. After beautification, you can one-click copy the formatted code or download it as a \.js file\.</div></div>',
     None),
    (r'<div class="faq-item"><div class="q">❓ Is this tool free\?</div><div class="a">Yes, completely free\. No registration or payment required\.</div></div>',
     None),
    (r'<div class="faq-item"><div class="q">❓ Do I need to upload my code\?</div><div class="a">No\. All beautification is done locally in your browser\. Your JavaScript code is never uploaded to any server\.</div></div>',
     None),
]

# For CN files, just clean up the old FAQ items
OLD_SECTIONS_CN = [
    (r'<div class="faq-item"><div class="q">❓ JavaScript美化需要上传代码吗\?</div><div class="a">不需要。所有美化操作完全在您的浏览器中执行，JS代码不会上传到任何服务器，保障代码安全。</div></div>', None),
    (r'<div class="faq-item"><div class="q">❓ 支持哪些JS美化选项\?</div><div class="a">支持缩进大小调整（2/4/8空格或Tab）、缩进类型选择、是否在运算符前后加空格、是否美化HTML模板等。</div></div>', None),
    (r'<div class="faq-item"><div class="q">❓ 可以处理压缩后的JS代码吗\?</div><div class="a">可以。工具专门针对压缩/混淆的JavaScript代码进行了优化，可以自动添加换行、调整缩进、还原可读格式。</div></div>', None),
    (r'<div class="faq-item"><div class="q">❓ 支持哪些JavaScript语法\?</div><div class="a">支持ES5/ES6\+、TypeScript、JSX等现代JavaScript语法。工具的格式化引擎能识别最新的JavaScript语言特性。</div></div>', None),
    (r'<div class="faq-item"><div class="q">❓ 转换结果可以复制吗\?</div><div class="a">可以。美化完成后，您可以一键复制格式化后的JS代码，或点击「下载」保存为.js文件。</div></div>', None),
    (r'<div class="faq-item"><div class="q">❓ 本工具收费吗\?</div><div class="a">完全免费。本工具属于在线小工具矩阵的一部分，所有功能均无需注册、无需付费即可使用。</div></div>', None),
]

def fix_file(filepath):
    """Fix a single EN file, replacing old JS beautifier content with correct content."""
    tool_name = os.path.relpath(filepath, start=os.path.dirname(os.path.abspath(__file__)))
    
    if tool_name not in TOOL_BODY:
        print(f"⚠️  No config for: {tool_name}")
        return False
    
    config = TOOL_BODY[tool_name]
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Step 1: Remove old sections and orphaned FAQ items
    for pattern, placeholder in OLD_SECTIONS_EN:
        if placeholder:
            content = re.sub(pattern, placeholder, content, flags=re.DOTALL)
        else:
            content = re.sub(pattern, '', content, flags=re.DOTALL)
    
    # Step 2: Replace placeholders with correct content
    content = content.replace('HOW_TO_USE_PLACEHOLDER', 
        f'<div class="content-section" id="options">\n'
        f'<h2>📖 How to Use</h2>\n'
        f'<p>{config["how_to_use"]}</p>\n'
        f'</div>')
    
    content = content.replace('HOW_IT_WORKS_PLACEHOLDER',
        f'<div class="content-section">\n'
        f'<h2>⚡ How It Works</h2>\n'
        f'<p>{config["how_it_works"]}</p>\n'
        f'</div>')
    
    content = content.replace('USE_CASES_PLACEHOLDER',
        f'<div class="content-section">\n'
        f'<h2>💼 Use Cases</h2>\n'
        f'<p>{config["use_cases"]}</p>\n'
        f'</div>')
    
    # Step 3: Clean up extra blank lines
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    # Step 4: Fix the closing structure after FAQ section (remove extra orphaned </div>)
    # Look for pattern: </div></div>\n\n<div class="content-section"> (FAQ -> Related Tools)
    # But if there's a stray </div>, it should be:
    # ...</div></div>\n\n</div>\n\n<div class="content-section"> -> ...</div></div>\n\n<div class="content-section">
    # Actually let me check what's left
    # After removing orphaned items, there might be a stray </div> or empty lines
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Fixed: {tool_name}")
        return True
    else:
        print(f"⚠️  No changes: {tool_name}")
        return False


def fix_cn_faq(filepath):
    """Fix CN FAQ items."""
    tool_name = os.path.relpath(filepath, start=os.path.dirname(os.path.abspath(__file__)))
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    for pattern, _ in OLD_SECTIONS_CN:
        content = re.sub(pattern, '', content, flags=re.DOTALL)
    
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ CN cleaned: {tool_name}")
        return True
    else:
        print(f"⚠️  CN no changes: {tool_name}")
        return False


# Fix all EN files
print("=== 修复EN文件 ===")
for filepath in TOOL_BODY:
    full_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), filepath)
    if os.path.exists(full_path):
        fix_file(full_path)
    else:
        print(f"❌ Not found: {full_path}")

# Fix CN files
print("\n=== 清理CN文件FAQ ===")
CN_PATHS = [
    "sass-to-css/index.html",
    "text-diff-checker/index.html",
    "less-to-css/index.html",
    "text-sorter/index.html",
    "list-to-json/index.html",
    "hash-file-checker/index.html",
]
for filepath in CN_PATHS:
    full_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), filepath)
    if os.path.exists(full_path):
        fix_cn_faq(full_path)
    else:
        print(f"❌ Not found: {full_path}")

print("\n全部修复完成！")
