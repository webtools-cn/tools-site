#!/usr/bin/env python3
"""Fix tool structure: add missing header, footer, ad-slot, toast"""
import sys, re, os

tool = sys.argv[1]
path = f"{tool}/index.html"

if not os.path.exists(path):
    print(f"❌ {tool}: file not found")
    sys.exit(1)

with open(path) as f:
    html = f.read()

# Backup
os.system(f"cp {path} {path}.bak.latest")

has_header = '<div class="header">' in html and 'lang-switch' in html
has_footer = '<div class="footer' in html
has_ad = 'ad-slot' in html
has_toast = 'class="toast"' in html

print(f"{tool}: header={has_header} footer={has_footer} ad={has_ad} toast={has_toast}")

lang_match = re.search(r'<html lang="([^"]+)"', html)
lang = lang_match.group(1) if lang_match else 'zh-CN'
is_cn = 'zh' in lang

og_match = re.search(r'<meta property="og:title" content="([^"]+)"', html)
tool_name = og_match.group(1) if og_match else tool.replace('-', ' ').title()

en_tool = f"../en/{tool}/" if is_cn else f"../{tool}/"
cn_tool = f"../{tool}/" if not is_cn else "index.html"

changes = []

# Fix missing header
if not has_header:
    body_match = re.search(r'(<body[^>]*>)\s*(<div class="container">)', html, re.DOTALL)
    if not body_match:
        body_match = re.search(r'(<body[^>]*>)', html)
        if body_match:
            header_html = f'''{body_match.group(1)}
<div class="ad-slot" id="ad-top"><ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-5998441792679372" data-ad-slot="XXXXXXX" data-ad-format="horizontal" data-full-width-responsive="true"></ins></div>
<div class="container">
<div class="header"><h1>{tool_name}</h1><div class="lang-switch"><a href="index.html" class="active">{'中文' if is_cn else 'EN'}</a><a href="{en_tool}">{'EN' if is_cn else '中文'}</a></div></div>
<p class="nav-back"><a href="{'../' if is_cn else '../../'}index.html">{'首页' if is_cn else 'Home'}</a> &rsaquo; <a href="{'../' if is_cn else '../../'}index.html#tools">{'工具' if is_cn else 'Tools'}</a> &rsaquo; {tool_name}</p>
'''
            html = html.replace(body_match.group(0), header_html)
            changes.append('header')
    else:
        header_html = f'''{body_match.group(1)}
<div class="ad-slot" id="ad-top"><ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-5998441792679372" data-ad-slot="XXXXXXX" data-ad-format="horizontal" data-full-width-responsive="true"></ins></div>
{body_match.group(2)}
<div class="header"><h1>{tool_name}</h1><div class="lang-switch"><a href="index.html" class="active">{'中文' if is_cn else 'EN'}</a><a href="{en_tool}">{'EN' if is_cn else '中文'}</a></div></div>
<p class="nav-back"><a href="{'../' if is_cn else '../../'}index.html">{'首页' if is_cn else 'Home'}</a> &rsaquo; <a href="{'../' if is_cn else '../../'}index.html#tools">{'工具' if is_cn else 'Tools'}</a> &rsaquo; {tool_name}</p>
'''
        html = html.replace(body_match.group(0), header_html)
        changes.append('header+ad')

# Fix missing footer
if not has_footer:
    footer_html = f'''
<div class="footer container">
<div style="margin-bottom:12px">
<a href="{'../' if is_cn else '../../'}index.html">{'首页' if is_cn else 'Home'}</a>
<a href="{'../' if is_cn else '../../'}index.html">{'全部工具' if is_cn else 'All Tools'}</a>
<a href="mailto:dexshuang@google.com">{'联系我们' if is_cn else 'Contact'}</a>
<a href="{'../' if is_cn else '../../'}privacy/">{'隐私政策' if is_cn else 'Privacy'}</a>
<a href="{'../' if is_cn else '../../'}terms/">{'服务条款' if is_cn else 'Terms'}</a>
<a href="{'../' if is_cn else '../../'}about/">{'关于我们' if is_cn else 'About'}</a>
<a href="{en_tool}">EN</a>
</div>
<p>{tool_name} · {'纯前端本地处理 · 数据绝不上传服务器' if is_cn else 'Client-side processing · No data upload'}</p>
<p style="margin-top:8px;color:#475569;font-size:.8rem">{'问题反馈' if is_cn else 'Feedback'}: dexshuang@google.com</p>
</div>'''
    html = html.replace('</body>', footer_html + '\n</body>')
    changes.append('footer')

# Add CSS
if ('header' in str(changes) or 'footer' in str(changes)) and '.header{' not in html:
    css_add = '''
.header{display:flex;justify-content:space-between;align-items:center;margin-bottom:24px}
.header h1{font-size:1.6rem;color:#f1f5f9}
.lang-switch{display:flex;gap:4px;background:#1e293b;border-radius:8px;padding:4px;border:1px solid rgba(148,163,184,.1)}
.lang-switch a{padding:6px 12px;border-radius:5px;font-size:.85rem;color:#94a3b8;text-decoration:none}
.lang-switch a.active{background:rgba(6,182,212,.2);color:#22d3ee}
.nav-back{color:#64748b;font-size:.85rem;margin-bottom:16px}
.nav-back a{color:#64748b;text-decoration:none}
.nav-back a:hover{color:#94a3b8}
.footer{border-top:1px solid rgba(148,163,184,.1);padding:24px 0;margin-top:32px;text-align:center;color:#64748b;font-size:.85rem}
.footer a{color:#64748b;margin:0 8px;text-decoration:none}
.footer a:hover{color:#94a3b8}
.toast{position:fixed;bottom:24px;left:50%;transform:translateX(-50%);background:#1e293b;color:#e2e8f0;padding:12px 24px;border-radius:8px;font-size:.9rem;border:1px solid rgba(148,163,184,.15);opacity:0;transition:opacity .3s;pointer-events:none;z-index:999}
.toast.show{opacity:1}
.ad-slot{margin:0 auto;text-align:center;max-width:960px}.ad-slot:not(:has(ins[frame])){display:none}.ad-slot:empty{display:none}.ad-slot ins{display:block}
'''
    html = html.replace('</style>', css_add + '\n</style>')
    changes.append('css')

with open(path, 'w') as f:
    f.write(html)

# Validate
try:
    result = os.popen(f'node -c {path} 2>&1').read()
    if 'SyntaxError' in result:
        print(f"❌ Node syntax check failed: {result[:200]}")
        sys.exit(1)
except:
    pass

print(f"✅ {tool}: changes={changes}")
