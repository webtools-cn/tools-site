#!/usr/bin/env python3
"""Fix remaining LONG meta descriptions."""
import os, re

fixes = [
    ('./css-skeleton-loader-generator/index.html',
     "免费在线骨架屏生成器，为网页内容占位生成加载骨架屏的HTML+CSS代码。支持自定义卡片、列表、头像、段落等多种布局样式和动画效果。用骨架屏替代空白加载页，提升用户体验、减少感知等待时间。纯前端本地生成，无需注册完全免费。"),
    ('./phone-link-generator/index.html',
     "免费在线手机链接生成器，一键生成tel:协议的HTML链接代码。点击后在手机上自动拨打电话，在电脑上打开Skype等通话软件。支持添加国家区号和分机号，纯前端本地处理保障数据安全，无需注册完全免费。"),
    ('./canvas-painter/index.html',
     "免费在线画布绘画工具，在浏览器中自由绘画创作。支持画笔、橡皮擦、颜色选择、线条粗细调节等基本功能。触屏设备可用手指绘画，纯浏览器端本地处理，数据绝不上传服务器，保障隐私安全，无需注册完全免费。"),
    ('./text-reverse/index.html',
     "免费在线文本反转工具，一键将文本字符顺序反转。支持逐字符反转、逐词反转、整句反转等多种模式。输入\"Hello World\" → 输出\"dlroW olleH\"，纯前端本地处理，数据不上传服务器，无需注册完全免费。"),
    ('./en/resignation-letter-generator/index.html',
     "Free resignation letter generator — create a professional resignation letter in seconds. Choose from formal, friendly, or short templates. Fill in your details, copy to clipboard or download as PDF. No sign-up needed, 100% private."),
    ('./en/js-deobfuscator/index.html',
     "Free JavaScript deobfuscator — decode and beautify obfuscated JS code. Decode hex/unicode strings, simplify expressions, restore array references, and format for readability. All processing is 100% client-side with no upload. No sign-up required."),
    ('./en/url-encoder-decoder/index.html',
     "Free URL encoder and decoder — encode special characters, Chinese text, spaces, and query strings for safe URLs, or decode them back to plain text. Supports encodeURIComponent and decodeURIComponent. 100% browser-side, no registration needed."),
]

fixed = 0
errors = []

for filepath, new_desc in fixes:
    if not os.path.exists(filepath):
        errors.append(f'MISSING FILE: {filepath}')
        continue
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    for line in content.split('\n'):
        if 'name="description"' in line:
            m = re.search(r'content=["\'](.+?)["\']\s*(?:/>|>)', line)
            if m:
                old_val = m.group(1)
                old_len = len(old_val)
                break
    
    if not m:
        errors.append(f'NO META DESC FOUND: {filepath}')
        continue
    
    new_len = len(new_desc)
    
    if old_val == new_desc:
        print(f'  SKIP: {filepath}')
        continue
    
    # Replace
    new_content = content.replace(f'content="{old_val}"', f'content="{new_desc}"', 1)
    if new_content == content:
        new_content = content.replace(f"content='{old_val}'", f"content='{new_desc}'", 1)
    
    with open(filepath, 'w') as f:
        f.write(new_content)
    
    print(f'✓ {filepath}: {old_len}→{new_len} chars')
    fixed += 1

print(f'\nFixed: {fixed}, Errors: {len(errors)}')
for e in errors:
    print(f'  ✗ {e}')