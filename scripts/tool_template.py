#!/usr/bin/env python3
"""批量生成剩余工具页面的辅助脚本"""
import os, json

BASE = '/home/chison/tools-site'

# 模板公共部分 - head
CN_HEAD_TOP = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-9W1157EBQV"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','G-9W1157EBQV');</script>
<script>window.addEventListener("error",function(e){if(e&&e.message===""){e.preventDefault();}});window.addEventListener("unhandledrejection",function(e){if(e&&e.reason&&e.reason.message===""){e.preventDefault();}});</script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
'''

EN_HEAD_TOP = '''<!DOCTYPE html>
<html lang="en">
<head>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-9W1157EBQV"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','G-9W1157EBQV');</script>
<script>window.addEventListener("error",function(e){if(e&&e.message===""){e.preventDefault();}});window.addEventListener("unhandledrejection",function(e){if(e&&e.reason&&e.reason.message===""){e.preventDefault();}});</script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
'''

def build_cn_tool(slug, cn_name, cn_desc, cn_keywords, cn_icon, cn_controls, cn_faqs, cn_extra_css='', cn_extra_js=''):
    faq_json = ','.join([f'''{{"@type":"Question","name":"{q}","acceptedAnswer":{{"@type":"Answer","text":"{a}"}}}}''' for q,a in cn_faqs])
    meta_desc = cn_desc[:160]
    
    return f'''{CN_HEAD_TOP}<meta name="description" content="{meta_desc}">
<meta name="keywords" content="{cn_keywords}">
<title>{cn_name} - Free ToolBase</title>
<link rel="canonical" href="https://free-toolbase.com/{slug}/">
<meta property="og:title" content="{cn_name} - Free ToolBase">
<meta property="og:description" content="{meta_desc}">
<meta property="og:url" content="https://free-toolbase.com/{slug}/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Free ToolBase">
<link rel="alternate" hreflang="zh" href="https://free-toolbase.com/{slug}/">
<link rel="alternate" hreflang="en" href="https://free-toolbase.com/en/{slug}/">
<link rel="alternate" hreflang="x-default" href="https://free-toolbase.com/en/{slug}/">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"SoftwareApplication","name":"{cn_name}","description":"{cn_desc}","applicationCategory":"UtilitiesApplication","operatingSystem":"Web","publisher":{{"@type":"Organization","name":"Free ToolBase","email":"dexshuang@google.com"}},"offers":{{"@type":"Offer","price":"0","priceCurrency":"USD"}}}}</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{faq_json}]}}</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"首页","item":"https://free-toolbase.com/"}},{{"@type":"ListItem","position":2,"name":"工具","item":"https://free-toolbase.com/#tools"}},{{"@type":"ListItem","position":3,"name":"{cn_name}","item":"https://free-toolbase.com/{slug}/"}}]}}</script>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#0f172a;color:#e2e8f0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,"PingFang SC","Microsoft YaHei",sans-serif;line-height:1.6;min-height:100vh}}
a{{color:#06b6d4;text-decoration:none}}
.container{{max-width:960px;margin:0 auto;padding:24px 16px}}
.header{{display:flex;justify-content:space-between;align-items:center;margin-bottom:20px;flex-wrap:wrap;gap:12px}}
.header h1{{font-size:1.6rem;color:#f1f5f9}}
.lang-switch{{display:flex;gap:4px;background:#1e293b;border-radius:8px;padding:4px;border:1px solid rgba(148,163,184,.1)}}
.lang-switch a{{padding:6px 12px;border-radius:5px;font-size:.85rem;color:#94a3b8}}
.lang-switch a.active{{background:rgba(6,182,212,.2);color:#22d3ee}}
.nav-back{{color:#64748b;font-size:.85rem;margin-bottom:16px}}
.nav-back a{{color:#64748b}}
.panel{{background:#1e293b;border-radius:12px;padding:20px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1)}}
.panel-title{{font-size:1.1rem;color:#f1f5f9;margin-bottom:14px;font-weight:600}}
.btn{{padding:8px 20px;border:none;border-radius:6px;font-size:.9rem;cursor:pointer;transition:all .2s;display:inline-flex;align-items:center;gap:6px}}
.btn-primary{{background:rgba(6,182,212,.2);color:#22d3ee;border:1px solid rgba(6,182,212,.3)}}
.btn-primary:hover{{background:rgba(6,182,212,.35);transform:translateY(-1px)}}
.btn-secondary{{background:rgba(148,163,184,.1);color:#94a3b8;border:1px solid rgba(148,163,184,.2)}}
.btn-secondary:hover{{background:rgba(148,163,184,.2)}}
.btn-large{{padding:12px 32px;font-size:1.1rem;font-weight:600}}
.btn-row{{display:flex;gap:8px;flex-wrap:wrap;justify-content:center;margin-top:16px}}
.input-row{{display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin-bottom:16px}}
.input-row input{{padding:10px 12px;border:1px solid rgba(148,163,184,.2);border-radius:8px;background:#0f172a;color:#e2e8f0;font-size:.9rem;min-width:180px;transition:border-color .2s}}
.input-row input:focus{{outline:none;border-color:#06b6d4}}
.faq-item{{margin-bottom:16px;border-bottom:1px solid rgba(148,163,184,.1);padding-bottom:16px}}
.faq-item:last-child{{border-bottom:none;margin-bottom:0;padding-bottom:0}}
.faq-q{{font-weight:600;color:#f1f5f9;margin-bottom:6px}}
.faq-a{{color:#94a3b8;font-size:.9rem}}
.privacy-note{{background:rgba(6,182,212,.05);border:1px solid rgba(6,182,212,.15);border-radius:8px;padding:12px 16px;font-size:.85rem;color:#94a3b8;margin-top:16px;display:flex;align-items:center;gap:8px}}
.footer{{border-top:1px solid rgba(148,163,184,.1);padding:24px 0;margin-top:48px;text-align:center;color:#64748b;font-size:.85rem}}
.footer a{{color:#64748b;margin:0 8px}}
.hero{{margin-bottom:20px}}
.hero p{{color:#94a3b8;font-size:.95rem;line-height:1.7}}
.badge{{display:inline-block;padding:4px 12px;border-radius:20px;font-size:.75rem;font-weight:600;background:rgba(6,182,212,.1);color:#22d3ee;border:1px solid rgba(6,182,212,.2);margin-top:8px}}
.toast{{position:fixed;bottom:20px;left:50%;transform:translateX(-50%);background:#1e293b;color:#22d3ee;padding:10px 24px;border-radius:8px;border:1px solid rgba(6,182,212,.3);font-size:.85rem;z-index:999;opacity:0;transition:opacity .3s}}
.toast.show{{opacity:1}}
{cn_extra_css}
@media(max-width:640px){{.header h1{{font-size:1.3rem}}}}
</style>
</head>
<body>
<div class="container">
<div class="header"><h1>{cn_icon} {cn_name}</h1><div class="lang-switch"><a href="index.html" class="active">中文</a><a href="../en/{slug}/">EN</a></div></div>
<p class="nav-back"><a href="../index.html">首页</a> &rsaquo; <a href="../#tools">工具</a> &rsaquo; {cn_name}</p>
<div class="hero"><p>{cn_desc} <span class="badge">🔒 无需注册 · 数据绝不上传</span></p></div>
<div class="panel">
  <div class="panel-title">{cn_icon} {cn_name}</div>
  {cn_controls}
</div>
<div class="privacy-note">🔒 <span>所有处理均在浏览器本地完成，数据不会上传到服务器。</span></div>
<div class="panel">
  <div class="panel-title">❓ 常见问题</div>
''' + ''.join([f'<div class="faq-item"><div class="faq-q">{q}</div><div class="faq-a">{a}</div></div>\n' for q,a in cn_faqs]) + f'''</div>
<div class="footer"><a href="../">首页</a> | <a href="../about/">关于</a> | <a href="../contact/">联系</a> | <a href="../privacy/">隐私</a><br>© 2026 Free ToolBase. All rights reserved.</div>
</div>
<div class="toast" id="toast"></div>
<script>
function showToast(msg){{var t=document.getElementById('toast');t.textContent=msg;t.classList.add('show');setTimeout(function(){{t.classList.remove('show')}},2000)}}
{cn_extra_js}
</script>
</body>
</html>'''

print("CN模板函数就绪")
print("OK")