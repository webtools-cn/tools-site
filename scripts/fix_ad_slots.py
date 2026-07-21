#!/usr/bin/env python3
"""批量给缺广告位的工具添加 ad-slot"""
import re, os

BASE = '/home/chison/tools-site'

TOOLS = [
    'exposure-calculator', 'font-face-generator', 'guitar-tuner',
    'gzip-text-compressor', 'heatmap-generator', 'hex-to-text',
    'html-entity-decode', 'image-diff', 'image-merge',
    'json-to-dart', 'json-to-rust', 'markdown-slides',
    'og-image-generator', 'seo-meta-generator', 'social-share-link-generator',
    'sql-to-json', 'svg-color-changer', 'swot-analysis-generator',
    'unique-id-generator', 'video-compress'
]

AD_SLOT_TOP = '<div class="ad-slot" id="ad-top"><ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-5998441792679372" data-ad-slot="XXXXXXX" data-ad-format="horizontal" data-full-width-responsive="true"></ins></div>\n'
AD_SLOT_BOTTOM = '<div class="ad-slot" style="margin:24px auto"><ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-5998441792679372" data-ad-slot="XXXXXXX" data-ad-format="horizontal" data-full-width-responsive="true"></ins></div>\n'
AD_CSS = '.ad-slot{margin:0 auto;text-align:center;max-width:960px}.ad-slot:not(:has(ins[frame])){display:none}.ad-slot:empty{display:none}.ad-slot ins{display:block}.ad-slot.ad-sidebar{max-width:300px}'

AD_SCRIPT = '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5998441792679372" crossorigin="anonymous"></script>\n'

fixed = []
skipped = []

for tool in TOOLS:
    path = os.path.join(BASE, tool, 'index.html')
    if not os.path.exists(path):
        print(f"  ⚠️ {tool}: 文件不存在")
        skipped.append(tool)
        continue
    
    with open(path) as f:
        content = f.read()
    
    # 检查是否已有 ad-slot
    if 'class="ad-slot"' in content or "class='ad-slot'" in content:
        print(f"  ✅ {tool}: 已有ad-slot，跳过")
        skipped.append(tool)
        continue
    
    modified = False
    
    # 1. 添加 Adsense script（如果还没有）
    if 'pagead2.googlesyndication.com' not in content:
        # 在 gtag script 后面加
        content = content.replace(
            "gtag('config','G-9W1157EBQV');</script>",
            "gtag('config','G-9W1157EBQV');</script>\n" + AD_SCRIPT,
            1
        )
        modified = True
    
    # 2. 添加 ad-slot CSS
    if '.ad-slot{' not in content:
        # 在 </style> 前加
        content = content.replace('</style>', '\n' + AD_CSS + '\n</style>', 1)
        modified = True
    
    # 3. 添加 top ad slot - 在 <body> 后紧跟
    if '<div class="ad-slot" id="ad-top">' not in content:
        content = content.replace('<body>', '<body>\n' + AD_SLOT_TOP, 1)
        modified = True
    
    # 4. 添加 bottom ad slot - 在 </body> 前
    if '<div class="ad-slot" style="margin:24px auto">' not in content:
        content = content.replace('</body>', AD_SLOT_BOTTOM + '</body>', 1)
        modified = True
    
    if modified:
        with open(path, 'w') as f:
            f.write(content)
        print(f"  🔧 {tool}: 已添加ad-slot")
        fixed.append(tool)
    else:
        print(f"  ❓ {tool}: 无需修改？")
        skipped.append(tool)

print(f"\n总结: 修复 {len(fixed)} 个, 跳过 {len(skipped)} 个")
for t in fixed:
    print(f"  修复: {t}")
