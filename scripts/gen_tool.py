# 用exec执行，数据源先存JSON
# 这个脚本读取JSON数据，生成HTML页面
import json, os

DATA_FILE = os.path.join(os.path.dirname(__file__), '..', '.batch_tool_data.json')

def gen_cn(t):
    """生成中文版HTML"""
    slug = t['slug']
    features = '\n'.join(f'<span class="feature-tag">{f}</span>' for f in t['cn_features'])
    howto = '\n'.join(f'<li><strong>{s}</strong><br><span>{s}</span></li>' for s in t['cn_howto'])
    faq = '\n'.join(f'<div class="faq-item"><div class="q">{q}</div><div class="a">{a}</div></div>' for q, a in t['cn_faq'])
    body, js = get_body_js(slug, 'cn')
    kw = ','.join(t['cn_name'].replace('🔄','').replace('🎤','').replace('🎵','').replace('😊','').replace('🖼️','').replace('⌨️','').split()[:5])
    
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-9W1157EBQV"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-9W1157EBQV');</script>
<script>window.addEventListener("error",function(e){{if(e&&e.message===""){{e.preventDefault();}}}});window.addEventListener("unhandledrejection",function(e){{if(e&&e.reason&&e.reason.message===""){{e.preventDefault();}}}});</script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="{t['cn_desc']}">
<meta name="keywords" content="{kw}">
<title>{t['cn_title']}</title>
<link rel="canonical" href="https://free-toolbase.com/{slug}/">
<meta property="og:title" content="{t['cn_title']}">
<meta property="og:description" content="{t['cn_desc']}">
<meta property="og:url" content="https://free-toolbase.com/{slug}/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Free ToolBase">
<link rel="alternate" hreflang="zh" href="https://free-toolbase.com/{slug}/">
<link rel="alternate" hreflang="en" href="https://free-toolbase.com/en/{slug}/">
<link rel="alternate" hreflang="x-default" href="https://free-toolbase.com/en/{slug}/">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"SoftwareApplication","name":"{t['cn_name']}","description":"{t['cn_desc']}","applicationCategory":"UtilitiesApplication","operatingSystem":"Web","publisher":{{"@type":"Organization","name":"Free ToolBase","email":"dexshuang@google.com"}},"offers":{{"@type":"Offer","price":"0","priceCurrency":"USD"}}}}</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"首页","item":"https://free-toolbase.com/"}},{{"@type":"ListItem","position":2,"name":"工具","item":"https://free-toolbase.com/#tools"}},{{"@type":"ListItem","position":3,"name":"{t['cn_name']}","item":"https://free-toolbase.com/{slug}/"}}]}}</script>
<meta property="og:image" content="https://free-toolbase.com/og-image.svg">
<meta name="twitter:image" content="https://free-toolbase.com/og-image.svg">
<meta name="twitter:card" content="summary_large_image">
<meta name="robots" content="index, follow">
<link rel="icon" type="image/svg+xml" href="favicon.svg">
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5998441792679372" crossorigin="anonymous"></script>
{get_css()}
</head>
<body>
<div class="container">
<div class="header"><h1>{t['cn_h1']}</h1><div class="lang-switch"><a href="index.html" class="active">中文</a><a href="../en/{slug}/">EN</a></div></div>
<p class="nav-back"><a href="../index.html">首页</a> &rsaquo; <a href="../index.html#tools">工具</a> &rsaquo; {t['cn_name']}</p>
<div class="hero"><p>{t['cn_hero']}</p><span class="badge">零依赖·可离线使用</span></div>
<div class="main-grid">
<div>
<div style="text-align:center;margin-top:-8px;margin-bottom:16px;font-size:0.8rem;color:#64748b">
  <span style="display:inline-flex;align-items:center;gap:5px;padding:3px 14px;border-radius:20px;background:rgba(6,182,212,.08);border:1px solid rgba(6,182,212,.12)">
    <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="#06b6d4" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
    Updated: {get_date()}
  </span>
</div>
<div class="section">
<h2>功能操作区</h2>
<div class="feature-list">
{features}
</div>
{body}
</div>
<div class="section">
<h2>常见问题</h2>
{faq}
</div>
</div>
<div class="seo-content">
<h2>如何使用{t['cn_name']}</h2>
<p>使用{t['cn_name']}非常简单：</p>
<ol>
{howto}
</ol>
</div>
</div>
<div>
<ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-5998441792679372" data-ad-slot="auto" data-ad-format="auto" data-full-width-responsive="true"></ins>
<script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
<footer class="footer container">
<div style="margin-bottom:12px">
<a href="../index.html">首页</a><a href="../index.html">全部工具</a><a href="mailto:dexshuang@google.com">联系我们</a><a href="../privacy/">隐私政策</a><a href="../terms/">服务条款</a><a href="../about/">关于我们</a><a href="../en/{slug}/">EN</a>
</div>
<p>{t['cn_name']} | 无需注册 · 数据绝不上传服务器</p>
<p style="margin-top:8px;color:#475569;font-size:.8rem">问题反馈: dexshuang@google.com</p>
</footer>
</div>
<div class="toast" id="toast"></div>
{js}
</body>
</html>"""

print("OK")