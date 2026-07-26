#!/usr/bin/env python3
"""批量修复: 给10个页面加AdSense + 修复4个title_long"""
import re, os

SITE = '/home/chison/tools-site'

ADSENSE_HEAD = '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5998441792679372" crossorigin="anonymous"></script>\n'
ADSENSE_BODY = '''<ins class="adsbygoogle"
     style="display:block"
     data-ad-client="ca-pub-5998441792679372"
     data-ad-slot="auto"
     data-ad-format="auto"
     data-full-width-responsive="true"></ins>
<script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
'''

# 10个文件需要加AdSense
ADSENSE_FILES = [
    'capacitor-code-calculator/index.html',
    'inflation-impact-calculator/index.html',
    'led-resistor-calculator/index.html',
    'pcb-trace-width-calculator/index.html',
    'voltage-divider-calculator/index.html',
    'en/capacitor-code-calculator/index.html',
    'en/inflation-impact-calculator/index.html',
    'en/led-resistor-calculator/index.html',
    'en/pcb-trace-width-calculator/index.html',
    'en/voltage-divider-calculator/index.html',
]

fixed_adsense = 0
for rel in ADSENSE_FILES:
    path = os.path.join(SITE, rel)
    if not os.path.isfile(path): continue
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()
    modified = False

    # 1. 在</head>前加AdSense script
    if 'adsbygoogle.js' not in c:
        c = c.replace('</head>', ADSENSE_HEAD + '</head>')
        modified = True

    # 2. 在<footer前加AdSense ins（仅当页面存在footer时）
    # 如果没footer，在</body>前加
    if '<footer' in c:
        if '<ins class="adsbygoogle"' not in c:
            c = c.replace('<footer', ADSENSE_BODY + '<footer', 1)
            modified = True
    elif '</body>' in c:
        if '<ins class="adsbygoogle"' not in c:
            c = c.replace('</body>', ADSENSE_BODY + '\n</body>')
            modified = True

    if modified:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(c)
        fixed_adsense += 1
        print(f"[AdSense] {rel}")

# 修复title_long - EN版4个
TITLE_FILES = [
    'en/capacitor-code-calculator/index.html',
    'en/inflation-impact-calculator/index.html',
    'en/led-resistor-calculator/index.html',
    'en/voltage-divider-calculator/index.html',
]

fixed_title = 0
for rel in TITLE_FILES:
    path = os.path.join(SITE, rel)
    if not os.path.isfile(path): continue
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()
    m = re.search(r'<title>([^<]+)</title>', c)
    if not m: continue
    t = m.group(1)
    if len(t) <= 60: continue

    # 缩短: 去掉 "Free Online " → 然后用更短格式
    nt = t
    # 策略: 把 "- Free ToolBase" 之前的部分缩短
    if ' - Free ToolBase' in nt:
        core = nt.split(' - Free ToolBase')[0]
        # 去掉前导 "Free " 和 "Online "
        core = core.replace('Free Online ', '').replace('Free ', '').replace('Online ', '')
        max_core = 60 - len(' - Free ToolBase')
        if len(core) > max_core:
            core = core[:max_core-1].rstrip() + '…'
        nt = core + ' - Free ToolBase'

    if nt != t and len(nt) <= 60:
        c = c.replace(f'<title>{t}</title>', f'<title>{nt}</title>')
        # 同步更新og:title
        c = c.replace(f'og:title\" content=\"{t}\"', f'og:title\" content=\"{nt}\"')
        with open(path, 'w', encoding='utf-8') as f:
            f.write(c)
        fixed_title += 1
        print(f"[Title] {rel}: '{t[:80]}' → '{nt}'")

print(f"\n总计: AdSense修复{fixed_adsense}个, Title修复{fixed_title}个")
