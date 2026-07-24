#!/usr/bin/env python3
"""批量生成工具页面 HTML（中英文双语）"""
import os, json

SITE_DIR = '/home/chison/tools-site'
TOOLS = json.load(open(os.path.join(SITE_DIR, 'scripts/gen_new_tools.py').replace('.py','_data.json'), 'r')) if os.path.exists(os.path.join(SITE_DIR, 'scripts/gen_new_tools_data.json')) else None

# 由于上面已经定义了TOOLS数据，直接在脚本中内联
# 重复的工具定义数据从 gen_new_tools.py 中导入
import sys
sys.path.insert(0, os.path.join(SITE_DIR, 'scripts'))
from gen_new_tools import TOOLS

def generate_html(tool, lang='zh'):
    """生成单个工具页面HTML"""
    is_zh = lang == 'zh'
    slug = tool['slug']
    name = tool['name_zh'] if is_zh else tool['name_en']
    desc = tool['desc_zh'] if is_zh else tool['desc_en']
    keywords = tool['keywords_zh'] if is_zh else tool['keywords_en']
    cat = tool['category_zh'] if is_zh else tool['category_en']
    badge = tool['badge_zh'] if is_zh else tool['badge_en']
    icon = tool['icon']
    input_label = tool['input_label_zh'] if is_zh else tool['input_label_en']
    input_placeholder = tool['input_placeholder_zh'] if is_zh else tool['input_placeholder_en']
    output_label = tool['output_label_zh'] if is_zh else tool['output_label_en']
    seo = tool['seo_zh'] if is_zh else tool['seo_en']
    faqs = tool['faq_zh'] if is_zh else tool['faq_en']
    
    hreflang = 'zh' if is_zh else 'en'
    canonical = f'https://free-toolbase.com/{slug}/' if is_zh else f'https://free-toolbase.com/en/{slug}/'
    alt_href = f'https://free-toolbase.com/en/{slug}/' if is_zh else f'https://free-toolbase.com/{slug}/'
    alt_hreflang = 'en' if is_zh else 'zh'
    
    # 输入输出元素ID
    input_id = {'words-to-numbers': 'wt', 'date-converter': 'dt', 'swift-code-validator': 'sw', 'vat-number-validator': 'vt', 'iban-checker': 'ib'}[slug]
    output_id = input_id + '-output'
    convert_func = 'convert()'
    
    # 面包屑
    breadcrumb_zh = f'<a href="../index.html">首页</a> &rsaquo; <a href="../index.html#{tool["category"]}">{cat}</a> &rsaquo; {name}'
    breadcrumb_en = f'<a href="../../index.html">Home</a> &rsaquo; <a href="../../index.html#{tool["category"]}">{cat}</a> &rsaquo; {name}'
    breadcrumb = breadcrumb_zh if is_zh else breadcrumb_en
    
    # 语言切换链接
    lang_switch_zh = f'<a href="index.html" class="active">中文</a><a href="../en/{slug}/">EN</a>'
    lang_switch_en = f'<a href="../../{slug}/">中文</a><a href="index.html" class="active">EN</a>'
    lang_switch = lang_switch_zh if is_zh else lang_switch_en
    
    # 首页链接
    home_link = '../index.html' if is_zh else '../../index.html'
    en_link = f'../index.html#text-tools' if is_zh else f'../../index.html#text-tools'
    
    # 页脚
    footer_zh = f'''<div class="footer container">
<div style="margin-bottom:12px">
<a href="../index.html">首页</a>
<a href="../index.html">全部工具</a>
<a href="mailto:dexshuang@google.com">联系我们</a>
<a href="../privacy/">隐私政策</a>
<a href="../terms/">服务条款</a>
<a href="../about/">关于我们</a>
<a href="../en/{slug}/">EN</a>
</div>
<p>{name} | 无需注册 · 数据绝不上传服务器</p>
<p style="margin-top:8px;color:#475569;font-size:.8rem">问题反馈: dexshuang@google.com</p>
</div>'''
    
    footer_en = f'''<div class="footer container">
<div style="margin-bottom:12px">
<a href="../../index.html">Home</a>
<a href="../../index.html">All Tools</a>
<a href="mailto:dexshuang@google.com">Contact</a>
<a href="../../privacy/">Privacy</a>
<a href="../../terms/">Terms</a>
<a href="../../about/">About</a>
<a href="../../{slug}/">中文</a>
</div>
<p>{name} | No registration · Your data never touches our servers</p>
<p style="margin-top:8px;color:#475569;font-size:.8rem">Feedback: dexshuang@google.com</p>
</div>'''
    footer = footer_zh if is_zh else footer_en
    
    # Schema: SoftwareApplication
    schema_name = name
    schema_desc = desc[:160]
    
    # FAQ Schema
    faq_items = []
    for q, a in faqs:
        faq_items.append(f'{{"@type":"Question","name":"{q}","acceptedAnswer":{{"@type":"Answer","text":"{a}"}}}}')
    faq_json = '[' + ','.join(faq_items) + ']'
    
    # HowTo
    howto_name = f'如何使用{name}' if is_zh else f'How to use {name}'
    howto_desc = f'如何使用{name}的详细步骤指南' if is_zh else f'Step-by-step guide for using {name}'
    howto_title = f'{name}使用教程' if is_zh else f'{name} Tutorial'
    
    # SEO content section
    if is_zh:
        seo_section = f'<div class="seo-content"><h2>{name} - {seo[:40]}…</h2><p>{seo}</p></div>'
    else:
        seo_section = f'<div class="seo-content"><h2>{name}</h2><p>{seo}</p></div>'
    
    # FAQ visible section
    faq_html = '<div class="section"><h2>' + ('常见问题' if is_zh else 'FAQ') + '</h2>'
    for q, a in faqs:
        faq_html += f'<div class="faq-item"><h3>{q}</h3><p>{a}</p></div>'
    faq_html += '</div>'
    
    html = f'''<!DOCTYPE html>
<html lang="{'zh-CN' if is_zh else 'en'}">
<head>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-9W1157EBQV"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-9W1157EBQV');</script>
<script>window.addEventListener("error",function(e){{if(e&&e.message===""){{e.preventDefault();}}}});window.addEventListener("unhandledrejection",function(e){{if(e&&e.reason&&e.reason.message===""){{e.preventDefault();}}}});</script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="{desc[:160]}">
<meta name="keywords" content="{keywords}">
<title>{name} - Free ToolBase</title>
<link rel="canonical" href="{canonical}">
<meta property="og:title" content="{name} - Free ToolBase">
<meta property="og:description" content="{desc[:160]}">
<meta property="og:url" content="{canonical}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Free ToolBase">
<link rel="alternate" hreflang="{hreflang}" href="{canonical}">
<link rel="alternate" hreflang="{alt_hreflang}" href="{alt_href}">
<link rel="alternate" hreflang="x-default" href="{alt_href}">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"SoftwareApplication","name":"{schema_name}","description":"{schema_desc}","applicationCategory":"UtilitiesApplication","operatingSystem":"Web","publisher":{{"@type":"Organization","name":"Free ToolBase","email":"dexshuang@google.com"}},"offers":{{"@type":"Offer","price":"0","priceCurrency":"USD"}}}}</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"FAQPage","mainEntity":{faq_json}}}</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"HowTo","name":"{howto_name}","description":"{howto_desc}","totalTime":"PT2M","tool":{{"@type":"HowToTool","name":"{name}"}},"step":[{{"@type":"HowToStep","position":1,"name":"{'输入数据' if is_zh else 'Enter data'}","text":"{'在输入框中输入需要计算/验证的内容' if is_zh else 'Enter the content to process or validate'}"}},{{"@type":"HowToStep","position":2,"name":"{'自动处理' if is_zh else 'Auto process'}","text":"{'工具自动实时处理并显示结果' if is_zh else 'The tool automatically processes and displays results in real-time'}"}},{{"@type":"HowToStep","position":3,"name":"{'查看结果' if is_zh else 'View results'}","text":"{'查看处理结果，支持一键复制' if is_zh else 'View the results with one-click copy support'}"}}]}}</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"{'首页' if is_zh else 'Home'}","item":"{'https://free-toolbase.com/' if is_zh else 'https://free-toolbase.com/en/'}"}},{{"@type":"ListItem","position":2,"name":"{cat}","item":"{'https://free-toolbase.com/#' if is_zh else 'https://free-toolbase.com/en/#'}{tool['category']}"}},{{"@type":"ListItem","position":3,"name":"{schema_name}","item":"{canonical}"}}]}}</script>
<style>*{{box-sizing:border-box;margin:0;padding:0}}body{{background:#0f172a;color:#e2e8f0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,"PingFang SC","Microsoft YaHei",sans-serif;line-height:1.6;min-height:100vh}}a{{color:#06b6d4;text-decoration:none}}a:hover{{color:#22d3ee}}.container{{max-width:960px;margin:0 auto;padding:24px 16px}}.header{{display:flex;justify-content:space-between;align-items:center;margin-bottom:24px;flex-wrap:wrap;gap:12px}}.header h1{{font-size:1.5rem;color:#f1c40f}}.lang-switch{{display:flex;gap:4px;background:#1e293b;border-radius:8px;padding:4px;border:1px solid rgba(148,163,184,.1)}}.lang-switch a{{padding:6px 12px;border-radius:5px;font-size:.85rem;color:#94a3b8}}.lang-switch a.active{{background:rgba(6,182,212,.2);color:#22d3ee}}.nav-back{{color:#64748b;font-size:.85rem;margin-bottom:16px}}.nav-back a{{color:#64748b}}.nav-back a:hover{{color:#94a3b8}}.hero{{margin-bottom:24px}}.hero p{{color:#94a3b8;font-size:1rem;margin-bottom:8px}}.badge{{display:inline-block;background:rgba(6,182,212,.15);color:#22d3ee;padding:4px 12px;border-radius:20px;font-size:.8rem;margin-bottom:16px}}.main-grid{{display:grid;grid-template-columns:1fr 300px;gap:24px;margin-bottom:24px}}@media(max-width:768px){{.main-grid{{grid-template-columns:1fr}}}}.section{{background:#1e293b;border-radius:12px;padding:20px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1)}}.section h2{{font-size:1.1rem;color:#f1c40f;margin-bottom:12px}}.form-group{{margin-bottom:14px}}.form-group label{{display:block;color:#94a3b8;font-size:.9rem;margin-bottom:6px;font-weight:500}}.form-group input,.form-group textarea{{width:100%;padding:10px 14px;background:#0f172a;border:1px solid rgba(148,163,184,.2);border-radius:8px;color:#e2e8f0;font-size:.9rem;outline:none;transition:all .2s}}.form-group input:focus,.form-group textarea:focus{{border-color:rgba(6,182,212,.4);box-shadow:0 0 0 3px rgba(6,182,212,.1)}}.ad-slot{{margin:16px auto;text-align:center;max-width:960px;min-height:90px;background:rgba(148,163,184,.05);border-radius:8px}}.ad-slot:empty{{display:none}}.ad-slot ins{{display:block}}.ad-slot.ad-sidebar{{min-height:250px;max-width:300px}}.btn{{display:inline-flex;align-items:center;gap:6px;padding:10px 20px;border:none;background:rgba(6,182,212,.2);color:#22d3ee;border-radius:8px;font-size:.9rem;cursor:pointer;transition:all .2s}}.btn:hover{{background:rgba(6,182,212,.35)}}.btn-mini{{display:inline-flex;align-items:center;padding:2px 8px;border:none;background:rgba(6,182,212,.15);color:#22d3ee;border-radius:4px;font-size:.8rem;cursor:pointer}}.btn-mini:hover{{background:rgba(6,182,212,.3)}}.seo-content{{margin-top:24px;padding:20px;background:#1e293b;border-radius:12px;border:1px solid rgba(148,163,184,.1)}}.seo-content h2{{font-size:1.1rem;color:#f1c40f;margin:16px 0 8px}}.seo-content h3{{font-size:1rem;color:#e2e8f0;margin:12px 0 6px}}.seo-content p{{color:#94a3b8;margin-bottom:8px;font-size:.9rem}}.seo-content ul,.seo-content ol{{margin-left:20px;margin-bottom:8px;color:#94a3b8;font-size:.9rem}}.seo-content li{{margin-bottom:4px}}.faq-item{{margin-bottom:12px;padding:12px;background:#0f172a;border-radius:8px;border:1px solid rgba(148,163,184,.1)}}.faq-item h3{{font-size:.95rem;color:#e2e8f0;margin-bottom:6px;cursor:pointer}}.faq-item p{{color:#94a3b8;font-size:.85rem}}.footer{{border-top:1px solid rgba(148,163,184,.1);padding:24px 0;margin-top:32px;text-align:center;color:#64748b;font-size:.85rem}}.footer a{{color:#64748b;margin:0 8px}}.footer a:hover{{color:#94a3b8}}.footer p{{margin-bottom:8px}}.toast{{position:fixed;bottom:24px;left:50%;transform:translateX(-50%);background:#1e293b;color:#e2e8f0;padding:12px 24px;border-radius:8px;font-size:.9rem;border:1px solid rgba(148,163,184,.15);opacity:0;transition:opacity .3s;pointer-events:none;z-index:999}}.toast.show{{opacity:1}}@media(max-width:640px){{h1{{font-size:1.2rem;word-break:break-word}}.header{{flex-direction:column;gap:8px}}}}</style>
</head>
<body>
<div class="container">
<div class="header"><h1>{icon} {name}</h1><div class="lang-switch">{lang_switch}</div></div>
<p class="nav-back">{breadcrumb}</p>
<div class="hero"><p>{desc}</p><span class="badge">{badge}</span></div>
<div class="main-grid">
<div>
<div class="section">
<div class="form-group"><label for="{input_id}-input">{input_label}</label>
<textarea id="{input_id}-input" style="min-height:80px;resize:vertical" oninput="{convert_func}" placeholder="{input_placeholder}"></textarea></div>
<div id="{output_id}" style="min-height:40px"></div>
</div>
</div>
</div>
{seo_section}
{faq_html}
</div>
{footer}
<div class="toast" id="toast"></div>
<script>
function showToast(m){{var t=document.getElementById("toast");t.textContent=m;t.classList.add("show");setTimeout(function(){{t.classList.remove("show")}},3000)}}
{tool['js_code']}
</script>
</body>
</html>'''
    return html

# 生成所有工具
for tool in TOOLS:
    slug = tool['slug']
    zh_dir = os.path.join(SITE_DIR, slug)
    en_dir = os.path.join(SITE_DIR, 'en', slug)
    os.makedirs(zh_dir, exist_ok=True)
    os.makedirs(en_dir, exist_ok=True)
    
    # 中文版
    zh_html = generate_html(tool, 'zh')
    with open(os.path.join(zh_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(zh_html)
    print(f'✓ {slug}/index.html (中文)')
    
    # 英文版
    en_html = generate_html(tool, 'en')
    with open(os.path.join(en_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(en_html)
    print(f'✓ en/{slug}/index.html (英文)')

print(f'\n总计: {len(TOOLS)} 个工具, {len(TOOLS)*2} 个页面')
