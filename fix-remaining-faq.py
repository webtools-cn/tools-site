#!/usr/bin/env python3
"""
进一步清理残留的旧FAQ条目 — 修复散落在HTML中各处的旧JS beautifier FAQ。
"""
import re
import os

# Clean up EN files - remove orphaned JS beautifier FAQ items
EN_FILES = [
    "en/sass-to-css/index.html",
    "en/text-diff-checker/index.html",
    "en/less-to-css/index.html",
    "en/text-sorter/index.html",
    "en/list-to-json/index.html",
    "en/hash-file-checker/index.html",
]

# Old FAQ items containing JS beautifier keywords to remove
OLD_FAQ_PATTERNS = [
    r'<div class="faq-item"><div class="q">❓ What formatting options are available\?</div><div class="a">Supports indentation size \(2/4/8 spaces or tab\), indentation type, space padding around operators, and HTML template beautification options\.</div></div>',
    r'<div class="faq-item"><div class="q">❓ Can it handle minified JS\?</div><div class="a">Yes\. The tool is optimized for minified/obfuscated JavaScript code, automatically adding line breaks, adjusting indentation, and restoring readability\.</div></div>',
    r'<div class="faq-item"><div class="q">❓ Which JS syntax does it support\?</div><div class="a">Supports ES5/ES6\+, TypeScript, and JSX\. The formatter engine recognizes the latest JavaScript language features\.</div></div>',
    r'<div class="faq-item"><div class="q">❓ Can I copy the result\?</div><div class="a">Yes. After beautification, you can one-click copy the formatted code or download it as a \.js file\.</div></div>',
    r'<div class="faq-item"><div class="q">❓ Is this tool free\?</div><div class="a">Yes, completely free\. No registration or payment required\.</div></div>',
    r'<div class="faq-item"><div class="q">❓ Do I need to upload my code\?</div><div class="a">No\. All beautification is done locally in your browser\. Your JavaScript code is never uploaded to any server\.</div></div>',
    # Also remove the "use cases" section that references JS beautifier
    r'<div class="content-section">\s*<h2>💼 Use Cases</h2>\s*<p>Read and modify minified JS code; unify code style in projects; quickly restore obfuscated code during debugging; refactor legacy JavaScript projects\.</p>\s*</div>',
]

# Also clean up CN files
CN_FILES = [
    "sass-to-css/index.html",
    "text-diff-checker/index.html",
    "less-to-css/index.html",
    "text-sorter/index.html",
    "list-to-json/index.html",
    "hash-file-checker/index.html",
]

OLD_CN_FAQ_PATTERNS = [
    r'<div class="faq-item"><div class="q">❓ JavaScript美化需要上传代码吗\?</div><div class="a">不需要。所有美化操作完全在您的浏览器中执行，JS代码不会上传到任何服务器，保障代码安全。</div></div>',
    r'<div class="faq-item"><div class="q">❓ 支持哪些JS美化选项\?</div><div class="a">支持缩进大小调整（2/4/8空格或Tab）、缩进类型选择、是否在运算符前后加空格、是否美化HTML模板等。</div></div>',
    r'<div class="faq-item"><div class="q">❓ 可以处理压缩后的JS代码吗\?</div><div class="a">可以。工具专门针对压缩/混淆的JavaScript代码进行了优化，可以自动添加换行、调整缩进、还原可读格式。</div></div>',
    r'<div class="faq-item"><div class="q">❓ 支持哪些JavaScript语法\?</div><div class="a">支持ES5/ES6\+、TypeScript、JSX等现代JavaScript语法。工具的格式化引擎能识别最新的JavaScript语言特性。</div></div>',
    r'<div class="faq-item"><div class="q">❓ 转换结果可以复制吗\?</div><div class="a">可以。美化完成后，您可以一键复制格式化后的JS代码，或点击「下载」保存为.js文件。</div></div>',
    r'<div class="faq-item"><div class="q">❓ 本工具收费吗\?</div><div class="a">完全免费。本工具属于在线小工具矩阵的一部分，所有功能均无需注册、无需付费即可使用。</div></div>',
]


def cleanup_file(filepath, patterns, file_label=""):
    """Remove old FAQ items from a file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    for pattern in patterns:
        content = re.sub(pattern, '', content, flags=re.DOTALL)
    
    # Also remove any resulting empty lines (more than 2 consecutive newlines)
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Cleaned: {file_label}: {filepath}")
        return True
    else:
        print(f"⚠️  Nothing to clean: {file_label}: {filepath}")
        return False

# Process all EN files
for filepath in EN_FILES:
    if os.path.exists(filepath):
        cleanup_file(filepath, OLD_FAQ_PATTERNS, "EN")
    else:
        print(f"❌ Not found: {filepath}")

# Process all CN files
for filepath in CN_FILES:
    if os.path.exists(filepath):
        cleanup_file(filepath, OLD_CN_FAQ_PATTERNS, "CN")
    else:
        print(f"❌ Not found: {filepath}")

# Also check and fix Use Cases section
print("\n=== 检查Use Cases部分残留 ===")
for filepath in EN_FILES:
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        if 'Read and modify minified JS code' in content:
            print(f"❌ Still has JS Use Cases: {filepath}")
        else:
            print(f"✅ Clean: {filepath}")

print("\n全部清理完成！")
