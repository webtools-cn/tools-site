#!/usr/bin/env python3
"""批量修复5个残留工具（10页面）: AdSense + related-tools + title修复"""
import re, os

TOOLS = [
    'cat-age-calculator',
    'cocktail-recipe-generator',
    'coffee-ratio-calculator',
    'currency-bill-counter',
    'ingredient-substitute-finder',
]

BASE = '/home/chison/tools-site'

# AdSense ins代码块
ADSENSE_INS = '''<!-- AdSense -->
<ins class="adsbygoogle"
     style="display:block"
     data-ad-client="ca-pub-5998441792679372"
     data-ad-slot="auto"
     data-ad-format="auto"
     data-full-width-responsive="true"></ins>
<script>(adsbygoogle = window.adsbygoogle || []).push({});</script>'''

# AdSense script tag (放在</head>之前)
ADSENSE_SCRIPT = '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5998441792679372" crossorigin="anonymous"></script>'

# related-tools (放在</body>之前)
RELATED_TOOLS = '''<link rel="stylesheet" href="https://free-toolbase.com/related-tools.css">
<div id="related-tools-section" class="related-tools-section"><div class="related-tools-loading">Loading related tools...</div></div>
<script src="https://free-toolbase.com/related-tools.js"></script>'''

# title长度修复：目标<60字符
TITLE_FIXES = {
    'en:cat-age-calculator': 'Cat Age Calculator - Convert Cat Years to Human Years | Free ToolBase',
    'en:cocktail-recipe-generator': 'Cocktail Recipe Generator - Random Drink Recipes | Free ToolBase',
    'en:coffee-ratio-calculator': 'Coffee Ratio Calculator - Perfect Brew Guide | Free ToolBase',
    'en:currency-bill-counter': 'Currency Bill Counter - Count Money Online | Free ToolBase',
    'en:ingredient-substitute-finder': 'Ingredient Substitute Finder - Cooking Alternatives | Free ToolBase',
}

fixed_count = 0
errors = []

for tool in TOOLS:
    for lang in ['cn', 'en']:
        if lang == 'cn':
            fpath = os.path.join(BASE, tool, 'index.html')
        else:
            fpath = os.path.join(BASE, 'en', tool, 'index.html')
        
        if not os.path.exists(fpath):
            errors.append(f"MISSING: {fpath}")
            continue
        
        with open(fpath, 'r') as f:
            content = f.read()
        
        original = content
        fixes = []
        
        # 1. 修复title过长（仅EN页）
        key = f'{lang}:{tool}'
        if key in TITLE_FIXES:
            new_title = TITLE_FIXES[key]
            # 替换<title>标签内容
            old_title_match = re.search(r'<title>(.*?)</title>', content)
            if old_title_match:
                old_title = old_title_match.group(1)
                content = content.replace(f'<title>{old_title}</title>', f'<title>{new_title}</title>')
                # 同时修复og:title
                content = re.sub(
                    r'<meta property="og:title" content="[^"]*">',
                    f'<meta property="og:title" content="{new_title}">',
                    content
                )
                fixes.append('title')
        
        # 修复1: 添加AdSense script (在</head>之前)
        if 'adsbygoogle.js' not in content:
            content = content.replace('</head>', f'\n{ADSENSE_SCRIPT}\n</head>')
            fixes.append('adsense-script')
        
        # 修复2: 添加AdSense ins代码块 (在</body>之前, footer之前)
        if 'class="adsbygoogle"' not in content and 'adsbygoogle' not in content.lower():
            # 在<footer>之前或</body>之前插入
            if '<footer' in content:
                content = content.replace('<footer', f'{ADSENSE_INS}\n<footer')
            else:
                content = content.replace('</body>', f'\n{ADSENSE_INS}\n</body>')
            fixes.append('adsense-ins')
        
        # 修复3: 添加related-tools (在</body>之前)
        if 'related-tools' not in content:
            content = content.replace('</body>', f'\n{RELATED_TOOLS}\n</body>')
            fixes.append('related-tools')
        
        if content != original:
            with open(fpath, 'w') as f:
                f.write(content)
            fixed_count += 1
            print(f"✅ {lang}:{tool} — {', '.join(fixes)}")
        else:
            print(f"⏭️  {lang}:{tool} — 无需修复")

print(f"\n修复: {fixed_count}个文件")
if errors:
    print(f"错误: {len(errors)}")
    for e in errors:
        print(f"  ❌ {e}")