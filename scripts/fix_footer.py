#!/usr/bin/env python3
"""批量修复Footer残缺页面 - 替换为标准footer"""
import os, re

STANDARD_FOOTER_CN = '''<footer style="background:#0f172a;border-top:1px solid rgba(148,163,184,.1);padding:24px 0;margin-top:40px">
  <div style="max-width:1200px;margin:0 auto;padding:0 20px;display:flex;flex-wrap:wrap;justify-content:center;gap:16px">
    <a href="../index.html" style="color:#94a3b8;text-decoration:none;font-size:14px">首页</a>
    <a href="mailto:dexshuang@google.com" style="color:#94a3b8;text-decoration:none;font-size:14px">联系我们</a>
    <a href="../privacy/" style="color:#94a3b8;text-decoration:none;font-size:14px">隐私政策</a>
    <a href="../terms/" style="color:#94a3b8;text-decoration:none;font-size:14px">服务条款</a>
    <a href="../about/" style="color:#94a3b8;text-decoration:none;font-size:14px">关于我们</a>
    <a href="https://github.com/webtools-cn/tools-site" target="_blank" rel="noopener" style="color:#94a3b8;text-decoration:none;font-size:14px">GitHub</a>
    <a href="../en/__SLUG__/" style="color:#94a3b8;text-decoration:none;font-size:14px">EN</a>
  </div>
  <p style="text-align:center;color:#64748b;font-size:12px;margin-top:12px">问题反馈: dexshuang@google.com</p>
</footer>'''

STANDARD_FOOTER_EN = '''<footer style="background:#0f172a;border-top:1px solid rgba(148,163,184,.1);padding:24px 0;margin-top:40px">
  <div style="max-width:1200px;margin:0 auto;padding:0 20px;display:flex;flex-wrap:wrap;justify-content:center;gap:16px">
    <a href="../index.html" style="color:#94a3b8;text-decoration:none;font-size:14px">Home</a>
    <a href="mailto:dexshuang@google.com" style="color:#94a3b8;text-decoration:none;font-size:14px">Contact</a>
    <a href="../privacy/" style="color:#94a3b8;text-decoration:none;font-size:14px">Privacy</a>
    <a href="../terms/" style="color:#94a3b8;text-decoration:none;font-size:14px">Terms</a>
    <a href="../about/" style="color:#94a3b8;text-decoration:none;font-size:14px">About</a>
    <a href="https://github.com/webtools-cn/tools-site" target="_blank" rel="noopener" style="color:#94a3b8;text-decoration:none;font-size:14px">GitHub</a>
    <a href="../../__SLUG__/" style="color:#94a3b8;text-decoration:none;font-size:14px">中文</a>
  </div>
  <p style="text-align:center;color:#64748b;font-size:12px;margin-top:12px">Feedback: dexshuang@google.com</p>
</footer>'''

cn_fixed = 0
en_fixed = 0

# Fix CN pages
for d in sorted(os.listdir('.')):
    p = os.path.join(d, 'index.html')
    if not os.path.isfile(p) or d == 'en': continue
    c = open(p, 'r', errors='ignore').read()
    
    # Check if footer has < 4 links
    footer_m = re.search(r'role="contentinfo"[^>]*>(.*?)</(?:div|footer|section)', c, re.DOTALL)
    if not footer_m:
        footer_m = re.search(r'<footer[^>]*>(.*?)</footer>', c, re.DOTALL)
    if not footer_m: continue
    
    links = re.findall(r'<a[^>]*>', footer_m.group(1))
    if len(links) >= 4: continue
    
    # Replace the entire footer section
    footer_html = footer_m.group(0)
    new_footer = STANDARD_FOOTER_CN.replace('__SLUG__', d)
    
    # Handle different footer patterns
    if '<footer' in c:
        c = re.sub(r'<footer[^>]*>.*?</footer>', new_footer, c, count=1, flags=re.DOTALL)
    else:
        # role="contentinfo" pattern - replace the containing div
        c = c.replace(footer_html, new_footer)
    
    open(p, 'w', encoding='utf-8', errors='ignore').write(c)
    cn_fixed += 1

# Fix EN pages
for d in sorted(os.listdir('en')):
    p = os.path.join('en', d, 'index.html')
    if not os.path.isfile(p): continue
    c = open(p, 'r', errors='ignore').read()
    
    footer_m = re.search(r'role="contentinfo"[^>]*>(.*?)</(?:div|footer|section)', c, re.DOTALL)
    if not footer_m:
        footer_m = re.search(r'<footer[^>]*>(.*?)</footer>', c, re.DOTALL)
    if not footer_m: continue
    
    links = re.findall(r'<a[^>]*>', footer_m.group(1))
    if len(links) >= 4: continue
    
    footer_html = footer_m.group(0)
    new_footer = STANDARD_FOOTER_EN.replace('__SLUG__', d)
    
    if '<footer' in c:
        c = re.sub(r'<footer[^>]*>.*?</footer>', new_footer, c, count=1, flags=re.DOTALL)
    else:
        c = c.replace(footer_html, new_footer)
    
    open(p, 'w', encoding='utf-8', errors='ignore').write(c)
    en_fixed += 1

print(f"CN footer fixed: {cn_fixed}")
print(f"EN footer fixed: {en_fixed}")
print(f"Total: {cn_fixed + en_fixed}")
