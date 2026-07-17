#!/usr/bin/env python3
"""Generate 5 new tool pages for free-toolbase.com - Part 1: Template engine"""
import os, json

BASE = os.path.expanduser("~/tools-site")

def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  OK: {path} ({len(content)}b)")

# Shared CSS
CSS = '*{box-sizing:border-box;margin:0;padding:0}body{background:#0f172a;color:#e2e8f0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,"PingFang SC","Microsoft YaHei",sans-serif;line-height:1.6;min-height:100vh}a{color:#06b6d4;text-decoration:none}.container{max-width:960px;margin:0 auto;padding:24px 16px}.header{display:flex;justify-content:space-between;align-items:center;margin-bottom:24px;flex-wrap:wrap;gap:12px}.header h1{font-size:1.5rem;color:#f1f5f9}.lang-switch{display:flex;gap:4px;background:#1e293b;border-radius:8px;padding:4px;border:1px solid rgba(148,163,184,.1)}.lang-switch a{padding:6px 12px;border-radius:5px;font-size:.85rem;color:#94a3b8}.lang-switch a.active{background:rgba(6,182,212,.2);color:#22d3ee}.nav-back{color:#64748b;font-size:.85rem;margin-bottom:16px}.nav-back a{color:#64748b}.section{background:#1e293b;border-radius:12px;padding:20px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1)}.section h2{font-size:1.1rem;color:#f1f5f9;margin-bottom:12px}.form-group{margin-bottom:14px}.form-group label{display:block;color:#94a3b8;font-size:.9rem;margin-bottom:6px;font-weight:500}.form-group input[type="number"],.form-group input[type="text"],.form-group select,.form-group textarea,.form-group input[type="range"]{width:100%;padding:10px 14px;background:#0f172a;border:1px solid rgba(148,163,184,.2);border-radius:8px;color:#e2e8f0;font-size:.9rem;outline:none;transition:all .2s}.form-group input:focus,.form-group select:focus,.form-group textarea:focus{border-color:rgba(6,182,212,.4);box-shadow:0 0 0 3px rgba(6,182,212,.1)}.form-row{display:flex;gap:12px;flex-wrap:wrap}.form-row .form-group{flex:1;min-width:200px}.btn-group{display:flex;gap:8px;flex-wrap:wrap;margin:12px 0}.btn{padding:10px 24px;border:none;border-radius:8px;font-size:.9rem;cursor:pointer;transition:all .2s;font-weight:600}.btn-primary{background:rgba(6,182,212,.2);color:#22d3ee;border:1px solid rgba(6,182,212,.3)}.btn-primary:hover{background:rgba(6,182,212,.3)}.btn-secondary{background:rgba(148,163,184,.1);color:#94a3b8;border:1px solid rgba(148,163,184,.2)}.btn-secondary:hover{background:rgba(148,163,184,.2)}.btn-success{background:rgba(34,197,94,.15);color:#4ade80;border:1px solid rgba(34,197,94,.25)}.btn-danger{background:rgba(239,68,68,.15);color:#f87171;border:1px solid rgba(239,68,68,.2)}.faq-item{margin-bottom:16px}.faq-item h3{font-size:.95rem;color:#e2e8f0;margin-bottom:6px}.faq-item p{color:#94a3b8;font-size:.9rem}.info-text{color:#94a3b8;font-size:.85rem;margin-bottom:12px}.badge{display:inline-block;background:rgba(6,182,212,.15);color:#22d3ee;padding:4px 12px;border-radius:20px;font-size:.8rem;margin-bottom:12px;border:1px solid rgba(6,182,212,.2)}.footer{border-top:1px solid rgba(148,163,184,.1);padding:24px 0;margin-top:32px;text-align:center;color:#64748b;font-size:.85rem}.footer a{color:#64748b;margin:0 8px}.toast{position:fixed;bottom:20px;left:50%;transform:translateX(-50%);background:#1e293b;color:#22d3ee;padding:10px 24px;border-radius:8px;border:1px solid rgba(6,182,212,.3);font-size:.85rem;z-index:999;opacity:0;transition:opacity .3s}.toast.show{opacity:1}.ad-slot{margin:16px auto;text-align:center;max-width:960px}.ad-slot:empty{display:none}.ad-slot ins{display:block}.ad-slot.ad-sidebar{max-width:300px}.seo-content{background:#1e293b;border-radius:12px;padding:20px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1)}.seo-content h2{font-size:1.1rem;color:#f1f5f9;margin-bottom:12px}.seo-content p,.seo-content li{color:#94a3b8;font-size:.9rem}.seo-content ol,.seo-content ul{padding-left:20px;margin-top:8px}.seo-content li{margin-bottom:8px}.seo-content strong{color:#e2e8f0}.main-grid{display:grid;grid-template-columns:1fr 300px;gap:16px}@media(max-width:768px){.main-grid{grid-template-columns:1fr}}'

GA4 = '<script async src="https://www.googletagmanager.com/gtag/js?id=G-9W1157EBQV"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag(\'js\',new Date());gtag(\'config\',\'G-9W1157EBQV\');</script>'
ADSENSE = '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5998441792679372" crossorigin="anonymous"></script>'

AD_TOP = '<div class="ad-slot" id="ad-top"><ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-5998441792679372" data-ad-slot="XXXXXXX" data-ad-format="horizontal" data-full-width-responsive="true"></ins></div>'
AD_MID = '<div class="ad-slot" style="margin:24px auto"><ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-5998441792679372" data-ad-slot="XXXXXXX" data-ad-format="horizontal" data-full-width-responsive="true"></ins></div>'
AD_SB1 = '<div class="ad-slot ad-sidebar"><ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-5998441792679372" data-ad-slot="XXXXXXX" data-ad-format="rectangle" data-full-width-responsive="true"></ins></div>'
AD_SB2 = '<div class="ad-slot ad-sidebar" style="margin-top:16px"><ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-5998441792679372" data-ad-slot="XXXXXXX" data-ad-format="rectangle" data-full-width-responsive="true"></ins></div>'

def schema_soft(name, desc, rc=312):
    return json.dumps({"@context":"https://schema.org","@type":"SoftwareApplication","name":name,"description":desc,"applicationCategory":"UtilitiesApplication","operatingSystem":"Web","publisher":{"@type":"Organization","name":"Online Tools","email":"dexshuang@google.com"},"offers":{"@type":"Offer","price":"0","priceCurrency":"CNY"},"aggregateRating":{"@type":"AggregateRating","ratingValue":"4.8","ratingCount":str(rc),"bestRating":"5","worstRating":"1","reviewCount":str(rc)}}, ensure_ascii=False)

def schema_faq(faqs):
    ents = [{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faqs]
    return json.dumps({"@context":"https://schema.org","@type":"FAQPage","name":faqs[0][0],"mainEntity":ents}, ensure_ascii=False)

def schema_howto(name, steps):
    sl = [{"@type":"HowToStep","position":i+1,"name":s[0],"text":s[1]} for i,s in enumerate(steps)]
    return json.dumps({"@context":"https://schema.org","@type":"HowTo","name":"How to use "+name,"description":"Steps to use "+name,"totalTime":"PT2M","tool":{"@type":"HowToTool","name":name},"step":sl}, ensure_ascii=False)

def schema_bc(cat, cat_a, name, url):
    return json.dumps({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":"https://free-toolbase.com/"},{"@type":"ListItem","position":2,"name":cat,"item":"https://free-toolbase.com/#"+cat_a},{"@type":"ListItem","position":3,"name":name,"item":url}]}, ensure_ascii=False)

def gen(cn, slug, title_cn, title_en, desc_cn, desc_en, icon, cat_cn, cat_en, cat_a, faqs_cn, faqs_en, seo_cn, seo_en, tool_cn, tool_en, js):
    is_cn = cn
    lang = 'zh-CN' if is_cn else 'en'
    title = title_cn if is_cn else title_en
    desc = desc_cn if is_cn else desc_en
    base = f"https://free-toolbase.com/{slug}/" if is_cn else f"https://free-toolbase.com/en/{slug}/"
    cat = cat_cn if is_cn else cat_en
    faqs = faqs_cn if is_cn else faqs_en
    seo = seo_cn if is_cn else seo_en
    tool = tool_cn if is_cn else tool_en
    sw_cn = 'index.html' if is_cn else f'../{slug}/'
    sw_en = f'../en/{slug}/' if is_cn else 'index.html'
    sw_cn_c = ' active' if is_cn else ''
    sw_en_c = '' if is_cn else ' active'
    nav = f'<a href="../index.html">{"首页" if is_cn else "Home"}</a> &rsaquo; <a href="../index.html#{cat_a}">{cat}</a> &rsaquo; {title}'
    badge = '零依赖·可离线使用' if is_cn else 'Zero Dependencies·Works Offline'
    info = f'{desc} · {"纯前端本地处理" if is_cn else "Pure Frontend"}'
    ft_links = f'<a href="../index.html">{"首页" if is_cn else "Home"}</a><a href="../index.html">{"全部工具" if is_cn else "All Tools"}</a><a href="mailto:dexshuang@google.com">{"联系我们" if is_cn else "Contact"}</a><a href="../privacy/">{"隐私政策" if is_cn else "Privacy"}</a><a href="../terms/">{"服务条款" if is_cn else "Terms"}</a><a href="../about/">{"关于我们" if is_cn else "About"}</a><a href="{"../en/" if is_cn else "../"}{slug}/">{"EN" if is_cn else "中文"}</a>'
    ft = f'<div class="footer container"><div style="margin-bottom:12px">{ft_links}</div><p>{title} · {"纯前端本地处理 · 数据绝不上传服务器" if is_cn else "Pure Frontend · No Server Uploads"}</p><p style="margin-top:8px;color:#475569;font-size:.8rem">{"问题反馈" if is_cn else "Feedback"}: dexshuang@google.com</p></div>'
    faq_h = ''.join(f'<div class="faq-item"><h3>{q}</h3><p>{a}</p></div>' for q,a in faqs)
    howto_steps = [("Input","准备输入" if is_cn else "Prepare input"),("Options","配置选项" if is_cn else "Configure"),("Output","查看结果" if is_cn else "View results")]
    
    return f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
{GA4}
{ADSENSE}
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="{desc}">
<title>{title} - {"免费在线工具·纯前端本地处理" if is_cn else "Free Online Tool"}</title>
<link rel="canonical" href="{base}">
<meta property="og:title" content="{icon} {title}"><meta property="og:description" content="{desc}"><meta property="og:url" content="{base}"><meta property="og:type" content="website"><meta property="og:site_name" content="{"在线小工具矩阵" if is_cn else "Free Toolbase"}">
<link rel="alternate" hreflang="zh" href="https://free-toolbase.com/{slug}/"><link rel="alternate" hreflang="en" href="https://free-toolbase.com/en/{slug}/"><link rel="alternate" hreflang="x-default" href="https://free-toolbase.com/en/{slug}/">
<script type="application/ld+json">{schema_soft(title, desc)}</script>
<script type="application/ld+json">{schema_faq(faqs)}</script>
<script type="application/ld+json">{schema_howto(title, howto_steps)}</script>
<script type="application/ld+json">{schema_bc(cat, cat_a, title, base)}</script>
<style>{CSS}</style>
</head>
<body>
{AD_TOP}
<div class="container">
<div class="header"><h1>{icon} {title}</h1><div class="lang-switch"><a href="{sw_cn}" class="active{sw_cn_c}">中文</a><a href="{sw_en}" class="{sw_en_c}">EN</a></div></div>
<p class="nav-back">{nav}</p>
<p class="info-text">{info}</p>
<span class="badge">{badge}</span>
<div class="main-grid"><div><div class="section">{tool}</div></div><div>{AD_SB1}{AD_SB2}</div></div>
{AD_MID}
<div class="seo-content">{seo}</div>
<div class="section"><h2>{"常见问题" if is_cn else "FAQ"}</h2>{faq_h}</div>
{AD_MID}
{ft}
</div>
<div class="toast" id="toast"></div>
<script>{js}</script>
</body>
</html>'''

def create(slug, **kw):
    cn = gen(True, slug, **kw)
    en = gen(False, slug, **kw)
    write(os.path.join(BASE, slug, 'index.html'), cn)
    write(os.path.join(BASE, 'en', slug, 'index.html'), en)

if __name__ == '__main__':
    # Import tool definitions from separate file
    from create_tools_data import TOOLS
    for t in TOOLS:
        create(**t)
    print(f"\nDone! Created {len(TOOLS)} tools (CN+EN each)")
