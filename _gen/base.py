#!/usr/bin/env python3
"""Generate 5 new tool pages (CN+EN bilingual) for tools-site."""
import os

BASE = os.path.expanduser("~/tools-site")
DATE = "2026-07-14"

# Common CSS (dark theme per PAGE-STANDARD.md)
CSS = """*{box-sizing:border-box;margin:0;padding:0}body{background:#0f172a;color:#e2e8f0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,"PingFang SC","Microsoft YaHei",sans-serif;line-height:1.6;min-height:100vh}a{color:#06b6d4;text-decoration:none}.container{max-width:1200px;margin:0 auto;padding:24px 16px}.header{display:flex;justify-content:space-between;align-items:center;margin-bottom:24px;flex-wrap:wrap;gap:12px}.header h1{font-size:1.6rem;color:#f1f5f9}.lang-switch{display:flex;gap:4px;background:#1e293b;border-radius:8px;padding:4px;border:1px solid rgba(148,163,184,.1)}.lang-switch a{padding:6px 12px;border-radius:5px;font-size:.85rem;color:#94a3b8}.lang-switch a.active{background:rgba(6,182,212,.2);color:#22d3ee}.nav-back{color:#64748b;font-size:.85rem;margin-bottom:16px}.nav-back a{color:#64748b}.nav-back a:hover{color:#94a3b8}textarea,input,select{background:#0f172a;border:1px solid rgba(148,163,184,.2);border-radius:6px;padding:8px 12px;color:#e2e8f0;font-size:.85rem;outline:none;font-family:inherit}textarea:focus,input:focus,select:focus{border-color:rgba(6,182,212,.5)}textarea{width:100%;min-height:120px;resize:vertical;font-family:ui-monospace,SFMono-Regular,Consolas,monospace;font-size:.85rem}.btn{padding:8px 20px;border:none;border-radius:6px;font-size:.85rem;cursor:pointer;transition:all .2s;display:inline-flex;align-items:center;gap:4px}.btn-primary{background:rgba(6,182,212,.2);color:#22d3ee;border:1px solid rgba(6,182,212,.3)}.btn-primary:hover{background:rgba(6,182,212,.3)}.btn-secondary{background:rgba(148,163,184,.1);color:#94a3b8;border:1px solid rgba(148,163,184,.2)}.btn-secondary:hover{background:rgba(148,163,184,.2)}.btn-success{background:rgba(34,197,94,.15);color:#4ade80;border:1px solid rgba(34,197,94,.2)}.btn-success:hover{background:rgba(34,197,94,.25)}.tool-section{background:#1e293b;border-radius:12px;padding:20px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1)}.tool-section h2{font-size:1.1rem;color:#f1f5f9;margin-bottom:12px}.tool-section p{color:#94a3b8;font-size:.9rem;margin-bottom:8px}.input-area{margin-bottom:12px}.input-row{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:8px;align-items:center}.options-area{margin-bottom:12px}.option-row{display:flex;gap:12px;flex-wrap:wrap;align-items:center;margin-bottom:8px}.option-row label{color:#94a3b8;font-size:.85rem}.result-output{background:#0f172a;border-radius:8px;padding:16px;color:#e2e8f0;font-size:.85rem;overflow-x:auto;max-height:400px;white-space:pre-wrap;word-break:break-all;margin-bottom:12px;font-family:ui-monospace,SFMono-Regular,Consolas,monospace}.result-actions{display:flex;gap:8px;flex-wrap:wrap}.faq-item{margin-bottom:16px}.faq-item h3{font-size:.95rem;color:#e2e8f9;margin-bottom:6px}.faq-item p{color:#94a3b8;font-size:.9rem}.seo-content{color:#94a3b8;font-size:.9rem;line-height:1.8}.seo-content h2{color:#f1f5f9;font-size:1.15rem;margin:20px 0 10px}.seo-content h3{color:#e2e8f0;font-size:1rem;margin:16px 0 8px}.seo-content ul{padding-left:20px;margin:8px 0}.seo-content li{margin:4px 0}.footer{border-top:1px solid rgba(148,163,184,.1);padding:24px 0;margin-top:32px;text-align:center;color:#64748b;font-size:.85rem}.footer a{color:#64748b;margin:0 8px}.footer a:hover{color:#94a3b8}.toast{position:fixed;bottom:20px;left:50%;transform:translateX(-50%);background:#1e293b;color:#22d3ee;padding:10px 24px;border-radius:8px;border:1px solid rgba(6,182,212,.3);font-size:.85rem;z-index:999;opacity:0;transition:opacity .3s}.toast.show{opacity:1}select{min-width:120px}input[type=number]{width:80px}.grid-2{display:grid;grid-template-columns:1fr 1fr;gap:12px}.badge{display:inline-block;background:rgba(6,182,212,.15);color:#22d3ee;padding:2px 10px;border-radius:12px;font-size:.75rem;border:1px solid rgba(6,182,212,.2);margin-left:8px}.history-list{max-height:150px;overflow-y:auto;margin:8px 0}.history-item{padding:6px 10px;cursor:pointer;border-radius:4px;font-size:.8rem;color:#94a3b8}.history-item:hover{background:rgba(148,163,184,.1)}@media(max-width:640px){.header h1{font-size:1.3rem}.btn{padding:6px 14px;font-size:.8rem}.grid-2{grid-template-columns:1fr}}.ad-slot{margin:16px auto;text-align:center;max-width:960px;min-height:90px}.ad-slot:empty{display:none}.ad-slot ins{display:block}.ad-slot.ad-sidebar{min-height:250px;max-width:300px}"""

# Common GA4 + AdSense head
def head_start(title, desc, keywords, canonical, og_title, og_desc, og_url, schema_name, schema_desc, faq_json, lang, slug):
    lang_switch_zh = f"index.html" if lang=="zh" else f"../../{slug}/"
    lang_switch_en = f"en/{slug}/" if lang=="zh" else "index.html"
    lang_label_zh = "中文"
    lang_label_en = "EN"
    active_zh = 'class="active"' if lang=="zh" else ""
    active_en = 'class="active"' if lang=="en" else ""
    site_name = "在线小工具矩阵" if lang=="zh" else "WebTools Suite"
    breadcrumb_name = "在线工具" if lang=="zh" else "Online Tools"
    hreflang_zh = f"https://free-toolbase.com/{slug}/"
    hreflang_en = f"https://free-toolbase.com/en/{slug}/"
    
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-9W1157EBQV"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag("js",new Date());gtag("config","G-9W1157EBQV");</script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="{desc}">
<meta name="keywords" content="{keywords}">
<title>{title}</title>
<link rel="canonical" href="{canonical}">
<link rel="alternate" hreflang="zh" href="{hreflang_zh}">
<link rel="alternate" hreflang="en" href="{hreflang_en}">
<link rel="alternate" hreflang="x-default" href="{hreflang_zh}">
<meta property="og:title" content="{og_title}">
<meta property="og:description" content="{og_desc}">
<meta property="og:url" content="{og_url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{site_name}">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"SoftwareApplication","name":"{schema_name}","applicationCategory":"DeveloperApplication","operatingSystem":"Web","publisher":{{"@type":"Organization","name":"Online Tools","email":"dexshuang@google.com"}},"author":{{"@type":"Organization","name":"Online Tools"}},"dateModified":"{DATE}","description":"{schema_desc}","offers":{{"@type":"Offer","price":"0","priceCurrency":"CNY"}}}}</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"FAQPage","name":"{schema_name}","mainEntity":{faq_json}}}</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"首页","item":"https://free-toolbase.com/"}},{{"@type":"ListItem","position":2,"name":"{breadcrumb_name}","item":"https://free-toolbase.com/#online-tools"}},{{"@type":"ListItem","position":3,"name":"{schema_name}","item":"{canonical}"}}]}}</script>
<style>{CSS}</style>
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5998441792679372" crossorigin="anonymous"></script>
</head>
<body>
<div class="container">
<div class="header"><h1>{schema_name}</h1><div class="lang-switch"><a href="{lang_switch_zh}" {active_zh}>{lang_label_zh}</a><a href="{lang_switch_en}" {active_en}>{lang_label_en}</a></div></div>
<p class="nav-back"><a href="{'../index.html' if lang=='zh' else '../../index.html'}">← {'全部工具' if lang=='zh' else 'All Tools'}</a></p>
<div class="ad-slot" id="ad-top"><ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-5998441792679372" data-ad-slot="XXXXXXX" data-ad-format="horizontal" data-full-width-responsive="true"></ins></div>"""

def footer(lang, slug, tool_label):
    home = "../index.html" if lang=="zh" else "../../index.html"
    privacy = "../privacy/" if lang=="zh" else "../../privacy/"
    terms = "../terms/" if lang=="zh" else "../../terms/"
    about = "../about/" if lang=="zh" else "../../about/"
    other_lang = f"../en/{slug}/" if lang=="zh" else f"../../{slug}/"
    other_label = "EN" if lang=="zh" else "中文"
    contact_label = "联系我们" if lang=="zh" else "Contact"
    privacy_label = "隐私政策" if lang=="zh" else "Privacy"
    terms_label = "服务条款" if lang=="zh" else "Terms"
    about_label = "关于我们" if lang=="zh" else "About"
    home_label = "首页" if lang=="zh" else "Home"
    all_label = "全部工具" if lang=="zh" else "All Tools"
    tagline = f"{tool_label} · 纯前端本地处理 · 数据绝不上传服务器" if lang=="zh" else f"{tool_label} · Pure Frontend · No Server Uploads"
    feedback_label = "问题反馈" if lang=="zh" else "Feedback"
    
    return f"""
<div class="ad-slot" style="margin-top:24px"><ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-5998441792679372" data-ad-slot="XXXXXXX" data-ad-format="horizontal" data-full-width-responsive="true"></ins></div>
</div>
<div class="footer container">
<div style="margin-bottom:12px">
<a href="{home}">{home_label}</a>
<a href="{home}">{all_label}</a>
<a href="mailto:dexshuang@google.com">{contact_label}</a>
<a href="{privacy}">{privacy_label}</a>
<a href="{terms}">{terms_label}</a>
<a href="{about}">{about_label}</a>
<a href="{other_lang}">{other_label}</a>
</div>
<p>{tagline}</p>
<p style="margin-top:8px;color:#475569;font-size:.8rem">{feedback_label}: dexshuang@google.com</p>
</div>
<script src="{'../libs/related-tools.js' if lang=='zh' else '../../libs/related-tools.js'}" data-slug="{slug}" data-lang="{'zh' if lang=='zh' else 'en'}"></script>
<div id="related-tools"></div>
<div id="feedback-widget"></div>
<script src="{'../libs/feedback.js' if lang=='zh' else '../../libs/feedback.js'}"></script>
<div id="toast" class="toast"></div>
<script>
function showToast(m){{var t=document.getElementById("toast");t.textContent=m;t.classList.add("show");setTimeout(function(){{t.classList.remove("show")}},3000)}}
function copyText(id){{var el=document.getElementById(id);if(!el)return;var t=el.textContent||el.innerText;navigator.clipboard.writeText(t).then(function(){{showToast("{'已复制到剪贴板' if lang=='zh' else 'Copied to clipboard'}")}})["catch"](function(){{showToast("{'复制失败' if lang=='zh' else 'Copy failed'}")}})}}
function downloadText(filename,text){{var b=new Blob([text],{{type:'text/plain'}});var a=document.createElement('a');a.href=URL.createObjectURL(b);a.download=filename;a.click();URL.revokeObjectURL(a.href)}}
document.addEventListener('keydown',function(e){{if(e.ctrlKey&&e.key==='Enter'){{execute();e.preventDefault()}}if(e.ctrlKey&&e.shiftKey&&e.key==='C'){{copyText('output');e.preventDefault()}}if(e.ctrlKey&&e.shiftKey&&e.key==='X'){{clearInput();e.preventDefault()}}}});
function saveHistory(key,val){{var h=JSON.parse(localStorage.getItem(key)||'[]');h=h.filter(function(x){{return x!==val}});h.unshift(val);if(h.length>5)h=h.slice(0,5);localStorage.setItem(key,JSON.stringify(h))}}
function loadHistory(key){{return JSON.parse(localStorage.getItem(key)||'[]')}}
</script>
"""

def make_faq_json(questions):
    """Build FAQ JSON-LD from list of (q,a) tuples."""
    items = []
    for q, a in questions:
        items.append(f'{{"@type":"Question","name":"{q}","acceptedAnswer":{{"@type":"Answer","text":"{a}"}}}}')
    return "[" + ",".join(items) + "]"

def faq_html(questions, lang):
    """Build visible FAQ HTML."""
    html = '<div class="tool-section"><h2>❓ ' + ('常见问题' if lang=='zh' else 'FAQ') + '</h2>'
    for q, a in questions:
        html += f'<div class="faq-item"><h3>{q}</h3><p>{a}</p></div>'
    html += '</div>'
    return html

print("Generator module loaded. Ready for tool definitions.")
