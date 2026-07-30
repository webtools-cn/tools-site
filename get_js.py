import re, sys

tool = sys.argv[1] if len(sys.argv) > 1 else 'binary-calculator'
html = open(f'{tool}/index.html', errors='ignore').read()
scripts = re.findall(r'<script>(.*?)</script>', html, re.DOTALL)
js_parts = [s.strip() for s in scripts if s.strip() and 'dataLayer' not in s[:50] and 'gtag' not in s[:30] and 'application/ld+json' not in s[:30]]
js = '\n'.join(js_parts)
print(js)
