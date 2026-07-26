#!/usr/bin/env python3
"""批量创建新工具 - 基于ROI模板"""
import os, re, json

SITE = '/home/chison/tools-site'

def create_tool(name, cn_title, en_title, cn_desc, en_desc, cn_keywords, en_keywords,
                form_html, calc_js, results_html, faq_cn, faq_en, steps_cn, steps_en):
    """创建中英文工具页面"""
    
    # === 中文版 ===
    cn_path = os.path.join(SITE, name, 'index.html')
    os.makedirs(os.path.dirname(cn_path), exist_ok=True)
    
    cn_html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-9W1157EBQV"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-9W1157EBQV');</script>
<script>window.addEventListener("error",function(e){{if(e&&e.message===""){{e.preventDefault();}}}});window.addEventListener("unhandledrejection",function(e){{if(e&&e.reason&&e.reason.message===""){{e.preventDefault();}}}});</script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="{cn_desc}">
<meta name="keywords" content="{name},工具,在线工具,免费,{cn_keywords}">
<title>{cn_title} - Free ToolBase</title>
<link rel="canonical" href="https://free-toolbase.com/{name}/">
<meta property="og:title" content="{cn_title} - Free ToolBase">
<meta property="og:description" content="{cn_desc}">
<meta property="og:url" content="https://free-toolbase.com/{name}/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Free ToolBase">
<link rel="alternate" hreflang="zh" href="https://free-toolbase.com/{name}/">
<link rel="alternate" hreflang="en" href="https://free-toolbase.com/en/{name}/">
<link rel="alternate" hreflang="x-default" href="https://free-toolbase.com/en/{name}/">
<script type="application/ld+json">{{"@context": "https://schema.org", "@type": "SoftwareApplication", "name": "{cn_title}", "description": "{cn_desc}", "applicationCategory": "UtilitiesApplication", "operatingSystem": "Web", "publisher": {{"@type": "Organization", "name": "Free ToolBase", "email": "dexshuang@google.com"}}, "offers": {{"@type": "Offer", "price": "0", "priceCurrency": "USD"}}}}</script>
<script type="application/ld+json">{{"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{faq_cn}]}}</script>
<script type="application/ld+json">{{"@context": "https://schema.org", "@type": "HowTo", "name": "如何使用{cn_title}", "description": "如何使用{cn_title}的详细步骤指南", "totalTime": "PT2M", "tool": {{"@type": "HowToTool", "name": "{cn_title}"}}, "step": [{steps_cn}]}}</script>
<script type="application/ld+json">{{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{{"@type": "ListItem", "position": 1, "name": "首页", "item": "https://free-toolbase.com/"}}, {{"@type": "ListItem", "position": 2, "name": "工具", "item": "https://free-toolbase.com/#tools"}}, {{"@type": "ListItem", "position": 3, "name": "{cn_title}", "item": "https://free-toolbase.com/{name}/"}}]}}</script>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#0f172a;color:#e2e8f0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,"PingFang SC","Microsoft YaHei",sans-serif;line-height:1.6;min-height:100vh}}
a{{color:#06b6d4;text-decoration:none}}
.container{{max-width:960px;margin:0 auto;padding:24px 16px}}
.header{{display:flex;justify-content:space-between;align-items:center;margin-bottom:24px;flex-wrap:wrap;gap:12px}}
.header h1{{font-size:1.5rem;color:#f1f5f9}}
.lang-switch{{display:flex;gap:4px;background:#1e293b;border-radius:8px;padding:4px}}
.lang-switch a{{padding:6px 12px;border-radius:5px;font-size:.85rem;color:#94a3b8}}
.lang-switch a.active{{background:rgba(6,182,212,.2);color:#22d3ee}}
.nav-back{{color:#64748b;font-size:.85rem;margin-bottom:16px}}
.nav-back a{{color:#64748b}}
.section{{background:#1e293b;border-radius:12px;padding:20px;margin-bottom:16px}}
.section h2{{font-size:1.1rem;color:#f1f5f9;margin-bottom:12px}}
.form-group{{margin-bottom:14px}}
.form-group label{{display:block;color:#94a3b8;font-size:.9rem;margin-bottom:6px;font-weight:500}}
.form-group input,.form-group select,.form-group textarea{{width:100%;padding:10px 14px;background:#0f172a;border:1px solid rgba(148,163,184,.2);border-radius:8px;color:#e2e8f0;font-size:.9rem;outline:none}}
.form-group input:focus,.form-group select:focus,.form-group textarea:focus{{border-color:rgba(6,182,212,.4)}}
.form-group textarea{{min-height:120px;resize:vertical;font-family:monospace}}
.form-row{{display:flex;gap:12px;flex-wrap:wrap}}
.form-row .form-group{{flex:1;min-width:200px}}
.btn{{padding:10px 24px;border:none;border-radius:8px;font-size:.9rem;cursor:pointer;transition:all .2s;font-weight:600}}
.btn-primary{{background:linear-gradient(135deg,#06b6d4,#0891b2);color:#fff}}
.btn-primary:hover{{transform:translateY(-2px);box-shadow:0 4px 15px rgba(6,182,212,.3)}}
.btn-secondary{{background:rgba(148,163,184,.1);color:#94a3b8}}
.btn-group{{display:flex;gap:8px;flex-wrap:wrap;margin-top:12px}}
.result-grid{{display:grid;grid-template-columns:1fr 1fr;gap:12px}}
.result-item{{background:#0a0f1e;border-radius:8px;padding:14px}}
.result-item .label{{color:#94a3b8;font-size:.8rem}}
.result-item .value{{font-size:1.2rem;font-weight:700;color:#22d3ee;margin-top:4px}}
.result-item .value.highlight{{color:#fbbf24;font-size:1.5rem}}
.faq-item{{margin-bottom:16px;border-bottom:1px solid rgba(148,163,184,.08);padding-bottom:16px}}
.faq-item:last-child{{border-bottom:none;margin-bottom:0;padding-bottom:0}}
.faq-item h3{{color:#f1f5f9;font-size:.95rem;margin-bottom:4px}}
.faq-item p{{color:#94a3b8;font-size:.85rem;margin-top:6px;line-height:1.7}}
.footer{{text-align:center;color:#64748b;font-size:.85rem;margin-top:32px;padding-top:20px;border-top:1px solid rgba(148,163,184,.08)}}
.toast{{position:fixed;bottom:24px;left:50%;transform:translateX(-50%);background:#1e293b;color:#e2e8f0;padding:12px 24px;border-radius:8px;font-size:.9rem;opacity:0;transition:opacity .3s;pointer-events:none;z-index:999}}
.toast.show{{opacity:1}}
@media(max-width:640px){{.result-grid{{grid-template-columns:1fr}}}}
</style>
<meta property="og:image" content="https://free-toolbase.com/og-image.svg">
<meta name="twitter:image" content="https://free-toolbase.com/og-image.svg">
<meta name="twitter:card" content="summary_large_image">
<meta name="robots" content="index, follow">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5998441792679372" crossorigin="anonymous"></script>
</head>
<body>
<div class="container">
<div class="header"><h1>📈 {cn_title}</h1><div class="lang-switch"><a href="index.html" class="active">中文</a><a href="../en/{name}/">EN</a></div></div>
<p class="nav-back"><a href="../index.html">首页</a> &rsaquo; <a href="../index.html#tools">工具</a> &rsaquo; {cn_title}</p>
<div class="hero"><p>{cn_desc} | 无需注册 · 数据绝不上传服务器</p><span class="badge">零依赖·可离线使用</span></div>
<div class="main-grid">
<div>
<div style="text-align:center;margin-top:-8px;margin-bottom:16px;font-size:0.8rem;color:#64748b">
  <span style="display:inline-flex;align-items:center;gap:5px;padding:3px 14px;border-radius:20px;background:rgba(6,182,212,.08);border:1px solid rgba(6,182,212,.12)">
    <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="#06b6d4" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
    Updated: 2026-07-26
  </span>
</div>
{form_html}
<div class="section"><h2>常见问题</h2>
{faq_html_cn}
</div>
</div>
</div>
<div class="seo-content">
    <h2>如何使用{cn_title}</h2>
    <p>使用{cn_title}非常简单：</p>
    <ol style="padding-left:20px;margin-top:12px">
{steps_html_cn}
    </ol>
  </div>
<div>
<ins class="adsbygoogle"
     style="display:block"
     data-ad-client="ca-pub-5998441792679372"
     data-ad-slot="auto"
     data-ad-format="auto"
     data-full-width-responsive="true"></ins>
<script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
<footer class="footer container">
<div style="margin-bottom:12px">
<a href="../index.html">首页</a>
<a href="../index.html">全部工具</a>
<a href="mailto:dexshuang@google.com">联系我们</a>
<a href="../privacy/">隐私政策</a>
<a href="../terms/">服务条款</a>
<a href="../about/">关于我们</a>
<a href="../en/{name}/">EN</a>
</footer>
<p>{cn_title} | 无需注册 · 数据绝不上传服务器</p>
<p style="margin-top:8px;color:#475569;font-size:.8rem">问题反馈: dexshuang@google.com</p>
</div>
<div class="toast" id="toast"></div>
<script>
function showToast(m){{var t=document.getElementById("toast");t.textContent=m;t.classList.add("show");setTimeout(function(){{t.classList.remove("show")}},3000)}}
function copyText(id){{var el=document.getElementById(id);if(!el)return;var t=el.textContent||el.innerText;navigator.clipboard.writeText(t).then(function(){{showToast("已复制")}}).catch(function(){{showToast("复制失败")}})}}
{calc_js}
</script>
</body>
</html>'''
    
    # Build FAQ HTML for CN
    faq_items = []
    for q, a in faq_cn:
        faq_items.append(f'<div class="faq-item"><h3>{q}</h3><p>{a}</p></div>')
    faq_html_cn = '\n'.join(faq_items)
    
    # Build Steps HTML for CN
    step_items = []
    for i, (title, desc) in enumerate(steps_cn):
        step_items.append(f'      <li style="margin-bottom:16px"><strong>{title}</strong><br><span style="color:#94a3b8;font-size:.9rem">{desc}</span></li>')
    steps_html_cn = '\n'.join(step_items)
    
    cn_html = cn_html.replace('{faq_html_cn}', faq_html_cn).replace('{steps_html_cn}', steps_html_cn)
    
    with open(cn_path, 'w', encoding='utf-8') as f:
        f.write(cn_html)
    print(f'✅ CN: {cn_path}')
    
    # === 英文版 ===
    en_path = os.path.join(SITE, 'en', name, 'index.html')
    os.makedirs(os.path.dirname(en_path), exist_ok=True)
    
    en_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-9W1157EBQV"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-9W1157EBQV');</script>
<script>window.addEventListener("error",function(e){{if(e&&e.message===""){{e.preventDefault();}}}});window.addEventListener("unhandledrejection",function(e){{if(e&&e.reason&&e.reason.message===""){{e.preventDefault();}}}});</script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="{en_desc}">
<meta name="keywords" content="{name},tools,online,free,{en_keywords}">
<title>{en_title} - Free ToolBase</title>
<link rel="canonical" href="https://free-toolbase.com/en/{name}/">
<meta property="og:title" content="{en_title} - Free ToolBase">
<meta property="og:description" content="{en_desc}">
<meta property="og:url" content="https://free-toolbase.com/en/{name}/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Free ToolBase">
<link rel="alternate" hreflang="zh" href="https://free-toolbase.com/{name}/">
<link rel="alternate" hreflang="en" href="https://free-toolbase.com/en/{name}/">
<link rel="alternate" hreflang="x-default" href="https://free-toolbase.com/en/{name}/">
<script type="application/ld+json">{{"@context": "https://schema.org", "@type": "SoftwareApplication", "name": "{en_title}", "description": "{en_desc}", "applicationCategory": "UtilitiesApplication", "operatingSystem": "Web", "publisher": {{"@type": "Organization", "name": "Free ToolBase", "email": "dexshuang@google.com"}}, "offers": {{"@type": "Offer", "price": "0", "priceCurrency": "USD"}}}}</script>
<script type="application/ld+json">{{"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{faq_en}]}}</script>
<script type="application/ld+json">{{"@context": "https://schema.org", "@type": "HowTo", "name": "How to Use {en_title}", "description": "Step-by-step guide on how to use {en_title}", "totalTime": "PT2M", "tool": {{"@type": "HowToTool", "name": "{en_title}"}}, "step": [{steps_en}]}}</script>
<script type="application/ld+json">{{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{{"@type": "ListItem", "position": 1, "name": "Home", "item": "https://free-toolbase.com/en/"}}, {{"@type": "ListItem", "position": 2, "name": "Tools", "item": "https://free-toolbase.com/en/#tools"}}, {{"@type": "ListItem", "position": 3, "name": "{en_title}", "item": "https://free-toolbase.com/en/{name}/"}}]}}</script>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#0f172a;color:#e2e8f0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif;line-height:1.6;min-height:100vh}}
a{{color:#06b6d4;text-decoration:none}}
.container{{max-width:960px;margin:0 auto;padding:24px 16px}}
.header{{display:flex;justify-content:space-between;align-items:center;margin-bottom:24px;flex-wrap:wrap;gap:12px}}
.header h1{{font-size:1.5rem;color:#f1f5f9}}
.lang-switch{{display:flex;gap:4px;background:#1e293b;border-radius:8px;padding:4px}}
.lang-switch a{{padding:6px 12px;border-radius:5px;font-size:.85rem;color:#94a3b8}}
.lang-switch a.active{{background:rgba(6,182,212,.2);color:#22d3ee}}
.nav-back{{color:#64748b;font-size:.85rem;margin-bottom:16px}}
.nav-back a{{color:#64748b}}
.section{{background:#1e293b;border-radius:12px;padding:20px;margin-bottom:16px}}
.section h2{{font-size:1.1rem;color:#f1f5f9;margin-bottom:12px}}
.form-group{{margin-bottom:14px}}
.form-group label{{display:block;color:#94a3b8;font-size:.9rem;margin-bottom:6px;font-weight:500}}
.form-group input,.form-group select,.form-group textarea{{width:100%;padding:10px 14px;background:#0f172a;border:1px solid rgba(148,163,184,.2);border-radius:8px;color:#e2e8f0;font-size:.9rem;outline:none}}
.form-group input:focus,.form-group select:focus,.form-group textarea:focus{{border-color:rgba(6,182,212,.4)}}
.form-group textarea{{min-height:120px;resize:vertical;font-family:monospace}}
.form-row{{display:flex;gap:12px;flex-wrap:wrap}}
.form-row .form-group{{flex:1;min-width:200px}}
.btn{{padding:10px 24px;border:none;border-radius:8px;font-size:.9rem;cursor:pointer;transition:all .2s;font-weight:600}}
.btn-primary{{background:linear-gradient(135deg,#06b6d4,#0891b2);color:#fff}}
.btn-primary:hover{{transform:translateY(-2px);box-shadow:0 4px 15px rgba(6,182,212,.3)}}
.btn-secondary{{background:rgba(148,163,184,.1);color:#94a3b8}}
.btn-group{{display:flex;gap:8px;flex-wrap:wrap;margin-top:12px}}
.result-grid{{display:grid;grid-template-columns:1fr 1fr;gap:12px}}
.result-item{{background:#0a0f1e;border-radius:8px;padding:14px}}
.result-item .label{{color:#94a3b8;font-size:.8rem}}
.result-item .value{{font-size:1.2rem;font-weight:700;color:#22d3ee;margin-top:4px}}
.result-item .value.highlight{{color:#fbbf24;font-size:1.5rem}}
.faq-item{{margin-bottom:16px;border-bottom:1px solid rgba(148,163,184,.08);padding-bottom:16px}}
.faq-item:last-child{{border-bottom:none;margin-bottom:0;padding-bottom:0}}
.faq-item h3{{color:#f1f5f9;font-size:.95rem;margin-bottom:4px}}
.faq-item p{{color:#94a3b8;font-size:.85rem;margin-top:6px;line-height:1.7}}
.footer{{text-align:center;color:#64748b;font-size:.85rem;margin-top:32px;padding-top:20px;border-top:1px solid rgba(148,163,184,.08)}}
.toast{{position:fixed;bottom:24px;left:50%;transform:translateX(-50%);background:#1e293b;color:#e2e8f0;padding:12px 24px;border-radius:8px;font-size:.9rem;opacity:0;transition:opacity .3s;pointer-events:none;z-index:999}}
.toast.show{{opacity:1}}
@media(max-width:640px){{.result-grid{{grid-template-columns:1fr}}}}
</style>
<meta property="og:image" content="https://free-toolbase.com/og-image.svg">
<meta name="twitter:image" content="https://free-toolbase.com/og-image.svg">
<meta name="twitter:card" content="summary_large_image">
<meta name="robots" content="index, follow">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5998441792679372" crossorigin="anonymous"></script>
</head>
<body>
<div class="container">
<div class="header"><h1>📈 {en_title}</h1><div class="lang-switch"><a href="../../{name}/">中文</a><a href="index.html" class="active">EN</a></div></div>
<p class="nav-back"><a href="../index.html">Home</a> &rsaquo; <a href="../index.html#tools">Tools</a> &rsaquo; {en_title}</p>
<div class="hero"><p>{en_desc} | No registration · Data never leaves your browser</p><span class="badge">Zero-dependency · Works offline</span></div>
<div class="main-grid">
<div>
<div style="text-align:center;margin-top:-8px;margin-bottom:16px;font-size:0.8rem;color:#64748b">
  <span style="display:inline-flex;align-items:center;gap:5px;padding:3px 14px;border-radius:20px;background:rgba(6,182,212,.08);border:1px solid rgba(6,182,212,.12)">
    <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="#06b6d4" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
    Updated: 2026-07-26
  </span>
</div>
{form_html_en}
<div class="section"><h2>Frequently Asked Questions</h2>
{faq_html_en}
</div>
</div>
</div>
<div class="seo-content">
    <h2>How to Use {en_title}</h2>
    <p>Using {en_title} is simple:</p>
    <ol style="padding-left:20px;margin-top:12px">
{steps_html_en}
    </ol>
  </div>
<div>
<ins class="adsbygoogle"
     style="display:block"
     data-ad-client="ca-pub-5998441792679372"
     data-ad-slot="auto"
     data-ad-format="auto"
     data-full-width-responsive="true"></ins>
<script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
<footer class="footer container">
<div style="margin-bottom:12px">
<a href="../index.html">Home</a>
<a href="../index.html">All Tools</a>
<a href="mailto:dexshuang@google.com">Contact</a>
<a href="../../privacy/">Privacy</a>
<a href="../../terms/">Terms</a>
<a href="../../about/">About</a>
<a href="../../{name}/">中文</a>
</footer>
<p>{en_title} | No registration · Data never leaves your browser</p>
<p style="margin-top:8px;color:#475569;font-size:.8rem">Feedback: dexshuang@google.com</p>
</div>
<div class="toast" id="toast"></div>
<script>
function showToast(m){{var t=document.getElementById("toast");t.textContent=m;t.classList.add("show");setTimeout(function(){{t.classList.remove("show")}},3000)}}
function copyText(id){{var el=document.getElementById(id);if(!el)return;var t=el.textContent||el.innerText;navigator.clipboard.writeText(t).then(function(){{showToast("Copied")}}).catch(function(){{showToast("Copy failed")}})}}
{calc_js}
</script>
</body>
</html>'''
    
    # Build FAQ HTML for EN
    faq_items = []
    for q, a in faq_en:
        faq_items.append(f'<div class="faq-item"><h3>{q}</h3><p>{a}</p></div>')
    faq_html_en = '\n'.join(faq_items)
    
    # Build Steps HTML for EN
    step_items = []
    for i, (title, desc) in enumerate(steps_en):
        step_items.append(f'      <li style="margin-bottom:16px"><strong>{title}</strong><br><span style="color:#94a3b8;font-size:.9rem">{desc}</span></li>')
    steps_html_en = '\n'.join(step_items)
    
    # EN version: replace simple CN strings in form_html with EN equivalents
    form_html_en = form_html.replace('计算', 'Calculate').replace('复制结果', 'Copy Results').replace('清空', 'Clear')
    
    en_html = en_html.replace('{faq_html_en}', faq_html_en).replace('{steps_html_en}', steps_html_en).replace('{form_html_en}', form_html_en)
    
    with open(en_path, 'w', encoding='utf-8') as f:
        f.write(en_html)
    print(f'✅ EN: {en_path}')
    
    return True


# ============================================
#  Stock Return Calculator
# ============================================
name = 'stock-return-calculator'
cn_title = '股票收益计算器'
en_title = 'Stock Return Calculator'

cn_desc = '免费在线股票收益计算器，计算股票投资总收益、年化收益率、股息收益。支持多笔交易计算，自动分析投资表现，无需注册，数据不上传服务器。'
en_desc = 'Free online stock return calculator. Calculate total return, annualized return, and dividend yield. Supports multiple trades, auto-analyzes investment performance. No registration required, data never leaves your browser.'

cn_keywords = '股票收益,投资计算器,年化收益率,股息收益'
en_keywords = 'stock return,investment calculator,annualized return,dividend yield'

form_html = '''  <div class="section">
    <p style="color:#94a3b8;font-size:.85rem;margin-bottom:12px">输入股票买入和卖出信息，计算总收益率和年化收益率。</p>
    <div class="form-row">
      <div class="form-group"><label>买入价格</label><input type="number" id="buyPrice" step="0.01" min="0" value="100"></div>
      <div class="form-group"><label>卖出价格</label><input type="number" id="sellPrice" step="0.01" min="0" value="150"></div>
    </div>
    <div class="form-row">
      <div class="form-group"><label>持股数量</label><input type="number" id="shares" step="1" min="1" value="100"></div>
      <div class="form-group"><label>持有年数</label><input type="number" id="years" step="0.5" min="0.1" value="2"></div>
    </div>
    <div class="form-group"><label>累计股息（每股）</label><input type="number" id="dividends" step="0.01" min="0" value="5"></div>
    <div class="btn-group"><button class="btn btn-primary" onclick="calc()">计算收益</button><button class="btn btn-secondary" onclick="clearAll()">清空</button></div>
    <div class="result-grid" style="margin-top:16px">
      <div class="result-item"><div class="label">总投资金额</div><div class="value" id="rInvest">&mdash;</div></div>
      <div class="result-item"><div class="label">卖出总金额</div><div class="value" id="rSell">&mdash;</div></div>
      <div class="result-item"><div class="label">总收益</div><div class="value highlight" id="rGain">&mdash;</div></div>
      <div class="result-item"><div class="label">总收益率</div><div class="value highlight" id="rROI">&mdash;</div></div>
      <div class="result-item"><div class="label">年化收益率</div><div class="value" id="rAnn">&mdash;</div></div>
      <div class="result-item"><div class="label">股息总收益</div><div class="value" id="rDiv">&mdash;</div></div>
    </div>
    <div class="btn-group"><button class="btn btn-secondary" onclick="copyAll()">📋 复制结果</button></div>
  </div>'''

calc_js = '''
function calc(){
  var bp=parseFloat(document.getElementById("buyPrice").value)||0;
  var sp=parseFloat(document.getElementById("sellPrice").value)||0;
  var sh=parseFloat(document.getElementById("shares").value)||0;
  var yr=parseFloat(document.getElementById("years").value)||1;
  var dv=parseFloat(document.getElementById("dividends").value)||0;
  if(bp<=0||sp<=0||sh<=0){showToast("请输入有效的数值");return}
  var invest=bp*sh;
  var sell=sp*sh;
  var divTotal=dv*sh;
  var totalGain=sell-invest+divTotal;
  var roi=(totalGain/invest*100).toFixed(2);
  var annual=((Math.pow((sell+divTotal)/invest,1/yr)-1)*100).toFixed(2);
  document.getElementById("rInvest").textContent="$"+invest.toLocaleString("en-US",{minimumFractionDigits:2});
  document.getElementById("rSell").textContent="$"+sell.toLocaleString("en-US",{minimumFractionDigits:2});
  document.getElementById("rGain").textContent="$"+totalGain.toLocaleString("en-US",{minimumFractionDigits:2});
  document.getElementById("rROI").textContent=roi+"%";
  document.getElementById("rAnn").textContent=annual+"%";
  document.getElementById("rDiv").textContent="$"+divTotal.toLocaleString("en-US",{minimumFractionDigits:2});
}
function clearAll(){
  document.getElementById("buyPrice").value="100";
  document.getElementById("sellPrice").value="150";
  document.getElementById("shares").value="100";
  document.getElementById("years").value="2";
  document.getElementById("dividends").value="5";
  ["rInvest","rSell","rGain","rROI","rAnn","rDiv"].forEach(function(id){document.getElementById(id).textContent="—"});
}
function copyAll(){
  var lines=[];
  ["rInvest","rSell","rGain","rROI","rAnn","rDiv"].forEach(function(id){
    var el=document.getElementById(id); if(el) lines.push(el.parentElement.querySelector(".label").textContent+": "+el.textContent);
  });
  navigator.clipboard.writeText(lines.join("\\n")).then(function(){showToast("已复制")}).catch(function(){showToast("复制失败")});
}
'''

faq_cn = [
    ("如何计算股票收益率？", "股票总收益率 = (卖出金额 + 股息 - 买入金额) / 买入金额 × 100%。例如，以每股100元买入100股（总投入10000元），以150元卖出（总收入15000元），加上每股5元股息共500元，总收益 = (15000+500-10000)/10000 = 55%。"),
    ("年化收益率怎么计算？", "年化收益率 = ((终值/本金)^(1/年数) - 1) × 100%。它让不同持有期的投资可以公平比较。例如，2年赚55%的年化收益率约为24.5%。"),
    ("股息对总收益有多大影响？", "股息是股票投资的重要组成部分。长期来看，股息再投资可以显著提高总回报。例如标普500指数长期总回报中约40%来自股息。"),
    ("如何评估股票投资收益？", "可以从三方面评估：1）对比基准指数（如沪深300/标普500）的同期表现；2）计算风险调整后的收益（如夏普比率）；3）考虑税收和通胀影响后的实际收益。"),
]
faq_en = [
    ("How do I calculate stock return?", "Total stock return = (Sell value + Dividends - Buy cost) / Buy cost × 100%. For example, buying 100 shares at $100 each ($10,000 invested) and selling at $150 each ($15,000), plus $5/share dividends ($500), total return = (15,000+500-10,000)/10,000 = 55%."),
    ("How is annualized return calculated?", "Annualized return = ((Final value / Principal)^(1/years) - 1) × 100%. It allows fair comparison across different holding periods. For example, 55% return over 2 years gives about 24.5% annualized."),
    ("How much do dividends impact total returns?", "Dividends are a significant component of stock returns. Over the long term, dividend reinvestment can dramatically boost total returns. Historically, about 40% of S&P 500 total returns came from dividends."),
    ("How to evaluate stock investment performance?", "Evaluate from three angles: 1) Compare against benchmark indices (like S&P 500) over the same period; 2) Calculate risk-adjusted returns (e.g., Sharpe ratio); 3) Consider real returns after taxes and inflation."),
]
steps_cn = [
    ("输入买入价格", "输入股票的买入价格和持股数量，计算总投资金额。"),
    ("输入卖出价格", "输入卖出价格，如果还持有可填当前市价估算。"),
    ("输入股息", "输入持有期间累计收到的每股股息，股息也是收益的重要来源。"),
    ("查看计算结果", "系统自动计算总收益、总收益率和年化收益率，支持一键复制。"),
]
steps_en = [
    ("Enter purchase price", "Enter the stock purchase price and number of shares to calculate total investment."),
    ("Enter selling price", "Enter the selling price, or current market price if still holding for estimation."),
    ("Enter dividends", "Enter cumulative dividends per share received during the holding period."),
    ("View results", "The calculator automatically computes total gain, total return rate, and annualized return. One-click copy supported."),
]

create_tool(name, cn_title, en_title, cn_desc, en_desc, cn_keywords, en_keywords,
            form_html, calc_js, '', faq_cn, faq_en, steps_cn, steps_en)
print(f'Done: {name}')
