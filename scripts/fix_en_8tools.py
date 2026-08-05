#!/usr/bin/env python3
"""Fix EN pages for 8 new tools - JS output Chinese, footer, hreflang, lang-switch, priceCurrency"""
import os, re

tools = [
    "em-to-px-converter",
    "oil-to-butter-converter",
    "aquarium-volume-calculator",
    "moving-box-calculator",
    "pond-volume-calculator",
    "curtain-length-calculator",
    "package-dimensions-calculator",
]

# JS output translations per tool
js_translations = {
    "em-to-px-converter": [
        ('innerHTML="结果: <b>"', 'innerHTML="Result: <b>"'),
        ('(基础字号 " +c+"px)"', '(base size " +c+"px)"'),
    ],
    "oil-to-butter-converter": [
        ('innerHTML="需要 <b>"', 'innerHTML="Need: <b>"'),
        ('克</b> "+oilType+" ("+(oil*0.2).toFixed(1)+" 茶匙)"', 'g</b> " +oilType+ " (" + (oil*0.2).toFixed(1) + " tsp)"'),
    ],
    "aquarium-volume-calculator": [
        ('innerHTML="实际水容积: <b>"', 'innerHTML="Actual water volume: <b>"'),
        ('升</b> / <b>"', 'L</b> / <b>"'),
        ('加仑</b>"', 'gal</b>"'),
    ],
    "moving-box-calculator": [
        ('innerHTML="预计需要 <b>"', 'innerHTML="Estimated: <b>"'),
        ('个纸箱<br>小箱: "', 'boxes<br>Small: "'),
        (' | 中箱: "', ' | Medium: "'),
        (' | 大箱: "', ' | Large: "'),
    ],
    "pond-volume-calculator": [
        ('innerHTML="水体体积: <b>"', 'innerHTML="Water volume: <b>"'),
        ('m³</b> ("+(vol*1000).toFixed(0)+" 升)"', 'm³</b> (" + (vol*1000).toFixed(0) + " L)"'),
    ],
    "curtain-length-calculator": [
        ('innerHTML="布料尺寸: <b>"', 'innerHTML="Fabric size: <b>"'),
        ('cm</b><br>面积: "', 'cm</b><br>Area: "'),
    ],
    "package-dimensions-calculator": [
        ('innerHTML="国内体积重(÷6000): <b>"', 'innerHTML="Domestic dim. weight (÷6000): <b>"'),
        ('kg</b> | 计费: <b>"', 'kg</b> | Charge: <b>"'),
        ('kg</b><br>国际体积重(÷5000): <b>"', 'kg</b><br>Intl. dim. weight (÷5000): <b>"'),
    ],
}

for tool in tools:
    fpath = f"en/{tool}/index.html"
    if not os.path.exists(fpath):
        print(f"SKIP: {fpath} not found")
        continue
    
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    changes = []
    
    # 1. Fix JS output Chinese
    for old, new in js_translations.get(tool, []):
        if old in content:
            content = content.replace(old, new)
            changes.append(f"  JS: {old[:40]}... → fixed")
    
    # 2. Fix footer links
    footer_map = {
        '联系我们': 'Contact Us',
        '隐私政策': 'Privacy Policy',
        '服务条款': 'Terms of Service',
        '关于我们': 'About Us',
    }
    for cn, en in footer_map.items():
        if f'>{cn}<' in content:
            content = content.replace(f'>{cn}<', f'>{en}<')
            changes.append(f"  Footer: {cn} → {en}")
    
    # 3. Fix footer copyright
    if '，数据不上传服务器' in content:
        content = content.replace('，数据不上传服务器', ', no data uploaded to servers')
        changes.append("  Copyright: CN → EN")
    
    # 4. Fix hreflang zh pointing to EN URL
    content = re.sub(
        r'hreflang="zh" href="https://free-toolbase\.com/en/' + tool + '/"',
        f'hreflang="zh" href="https://free-toolbase.com/{tool}/"',
        content
    )
    if 'hreflang="zh" href="https://free-toolbase.com/en/' + tool + '/"' not in original:
        if f'hreflang="zh" href="https://free-toolbase.com/{tool}/"' in content:
            changes.append("  hreflang: zh → CN URL")
    
    # 5. Fix lang-switch pointing to EN (self)
    content = content.replace(
        f'<a href="/en/{tool}/">English</a>',
        f'<a href="/{tool}/">中文</a>'
    )
    if f'<a href="/{tool}/">中文</a>' in content and f'<a href="/en/{tool}/">English</a>' in original:
        changes.append("  lang-switch: self → CN")
    
    # 6. Fix priceCurrency CNY → USD
    if '"priceCurrency":"CNY"' in content:
        content = content.replace('"priceCurrency":"CNY"', '"priceCurrency":"USD"')
        changes.append("  priceCurrency: CNY → USD")
    
    if content != original:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"FIXED {tool}: {len(changes)} changes")
        for c in changes:
            print(c)
    else:
        print(f"NO CHANGES: {tool}")

print("\nDone!")
