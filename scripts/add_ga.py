#!/usr/bin/env python3
"""批量给缺GA的页面添加Google Analytics代码"""
import os, re

GA_CODE = '''<script async src="https://www.googletagmanager.com/gtag/js?id=G-9W1157EBQV"></script>
  <script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','G-9W1157EBQV');</script>'''

def add_ga(filepath):
    c = open(filepath, 'r', errors='ignore').read()
    if 'googletagmanager' in c:
        return False
    # Insert after AdSense script
    if 'adsbygoogle' in c:
        c = c.replace(
            '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5998441792679372" crossorigin="anonymous"></script>',
            '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5998441792679372" crossorigin="anonymous"></script>\n  ' + GA_CODE,
            1
        )
    else:
        # Insert after <head>
        c = c.replace('<head>', '<head>\n  ' + GA_CODE, 1)
    open(filepath, 'w').write(c)
    return True

# CN pages
cn_fixed = 0
for d in sorted(os.listdir('.')):
    p = os.path.join(d, 'index.html')
    if not os.path.isfile(p) or d == 'en': continue
    if add_ga(p):
        cn_fixed += 1

# EN pages
en_fixed = 0
for d in sorted(os.listdir('en')):
    p = os.path.join('en', d, 'index.html')
    if not os.path.isfile(p): continue
    if add_ga(p):
        en_fixed += 1

print(f'CN: {cn_fixed} pages fixed')
print(f'EN: {en_fixed} pages fixed')
print(f'Total: {cn_fixed + en_fixed} pages fixed')
