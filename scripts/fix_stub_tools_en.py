#!/usr/bin/env python3
"""Add functional JS to EN stub tool pages."""
import os, re

TOOLS_DIR = "/home/chison/tools-site/en"

# Read the CN implementations and adapt toast messages
def get_cn_js(tool_name):
    cn_path = os.path.join("/home/chison/tools-site", tool_name, "index.html")
    with open(cn_path, 'r', encoding='utf-8') as f:
        c = f.read()
    # Extract the functional script (not gtag, not error listener, not json-ld)
    scripts = re.findall(r'<script>(.+?)</script>', c, re.DOTALL)
    for s in scripts:
        if 'gtag' in s[:80] or 'addEventListener("error"' in s[:100] or 'application/ld+json' in s:
            continue
        if len(s.strip()) > 50:
            # Replace Chinese toast messages with English
            s = s.replace('已复制', 'Copied')
            s = s.replace('已复制全部', 'All copied')
            s = s.replace('请输入', 'Please enter ')
            s = s.replace('无效', 'Invalid ')
            s = s.replace('失败', 'failed')
            s = s.replace('选择', 'Select ')
            return '<script>' + s + '</script>'
    return None

# Tools to add JS
JS_TOOLS = ["decimal-to-roman", "hex-encoder-decoder", "hsl-to-rgb", 
            "unix-timestamp-converter", "md5-hash"]

# Tools that can't be implemented in pure frontend → add noindex
NOINDEX_TOOLS = [
    "excel-to-pdf", "ico-converter", "image-resize", "jpg-to-webp",
    "mp4-to-gif", "pdf-compress", "wav-to-mp3", "webp-converter",
    "dns-records-lookup", "url-unshortener", "og-checker",
    "log-viewer", "php-formatter", "mermaid-editor", "data-unit-converter"
]

def add_js_to_tool(tool_name, js_code):
    filepath = os.path.join(TOOLS_DIR, tool_name, "index.html")
    if not os.path.exists(filepath):
        print(f"  SKIP: {filepath} not found")
        return False
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    if 'calcMD5' in content or ('function convert(' in content and 'gtag' not in content[:200]):
        # Check if it already has real functional JS
        has_real_js = False
        scripts = re.findall(r'<script>(.+?)</script>', content, re.DOTALL)
        for s in scripts:
            if 'gtag' not in s[:80] and 'addEventListener("error"' not in s[:100] and len(s.strip()) > 100:
                has_real_js = True
                break
        if has_real_js:
            print(f"  SKIP: {tool_name} already has functional JS")
            return False
    if '</body>' in content:
        content = content.replace('</body>', js_code + '\n</body>')
    else:
        content += js_code
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  OK: {tool_name}")
    return True

def add_noindex(tool_name):
    filepath = os.path.join(TOOLS_DIR, tool_name, "index.html")
    if not os.path.exists(filepath):
        return False
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    if 'noindex' in content:
        return False
    if 'index, follow' in content:
        content = content.replace('index, follow', 'noindex, follow')
    elif 'index,follow' in content:
        content = content.replace('index,follow', 'noindex,follow')
    else:
        content = content.replace('<meta charset="UTF-8">', '<meta charset="UTF-8">\n<meta name="robots" content="noindex, follow">')
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  NOINDEX: {tool_name}")
    return True

if __name__ == '__main__':
    print("=== Adding functional JS to EN stub tools ===")
    for tool in JS_TOOLS:
        js = get_cn_js(tool)
        if js:
            add_js_to_tool(tool, js)
        else:
            print(f"  WARN: could not extract JS from CN {tool}")
    
    print("\n=== Adding noindex to EN non-implementable tools ===")
    for tool in NOINDEX_TOOLS:
        add_noindex(tool)
    
    print("\nDone!")
