#!/usr/bin/env python3
"""
Tool Site Template Engine v3.0
统一页面生成模板 - 所有新工具和重构页面必须使用此模板

核心原则:
1. URL路径不变
2. Schema/SEO成果保留
3. 外壳统一（head/body/footer/广告位）
4. 内核保留（工具HTML/JS/SEO/FAQ）

使用方法:
    from tool_template_v3 import ToolPageBuilder
    
    builder = ToolPageBuilder()
    page = builder.build(
        slug='my-tool',
        title_cn='我的工具',
        title_en='My Tool',
        desc_cn='描述...',
        desc_en='Description...',
        icon='🔧',
        cat_cn='开发工具',
        cat_en='Developer Tools',
        cat_anchor='developer-tools',
        tool_html_cn='<div>...</div>',
        tool_html_en='<div>...</div>',
        tool_js='var x=1;...',
        faqs_cn=[('Q1','A1')],
        faqs_en=[('Q1','A1')],
        seo_cn='<h2>...</h2>',
        seo_en='<h2>...</h2>',
    )
    builder.save(page, 'my-tool')
"""

import json
import os

BASE = os.path.expanduser("~/tools-site")

# ============================================================
# 一、固定部分（所有页面完全相同，不得修改）
# ============================================================

GA4 = '''<script async src="https://www.googletagmanager.com/gtag/js?id=G-9W1157EBQV"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','G-9W1157EBQV');</script>'''

ADSENSE = '''<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5998441792679372" crossorigin="anonymous"></script>'''

# 统一CSS - 深色主题，所有页面共享
CSS_UNIFIED = '''*{box-sizing:border-box;margin:0;padding:0}body{background:#0f172a;color:#e2e8f0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,"PingFang SC","Microsoft YaHei",sans-serif;line-height:1.6;min-height:100vh}a{color:#06b6d4;text-decoration:none}a:hover{color:#22d3ee}.container{max-width:960px;margin:0 auto;padding:24px 16px}.header{display:flex;justify-content:space-between;align-items:center;margin-bottom:24px;flex-wrap:wrap;gap:12px}.header h1{font-size:1.5rem;color:#f1c40f}.lang-switch{display:flex;gap:4px;background:#1e293b;border-radius:8px;padding:4px;border:1px solid rgba(148,163,184,.1)}.lang-switch a{padding:6px 12px;border-radius:5px;font-size:.85rem;color:#94a3b8}.lang-switch a.active{background:rgba(6,182,212,.2);color:#22d3ee}.nav-back{color:#64748b;font-size:.85rem;margin-bottom:16px}.nav-back a{color:#64748b}.nav-back a:hover{color:#94a3b8}.hero{margin-bottom:24px}.hero p{color:#94a3b8;font-size:1rem;margin-bottom:8px}.badge{display:inline-block;background:rgba(6,182,212,.15);color:#22d3ee;padding:4px 12px;border-radius:20px;font-size:.8rem;margin-bottom:16px}.main-grid{display:grid;grid-template-columns:1fr 300px;gap:24px;margin-bottom:24px}@media(max-width:768px){.main-grid{grid-template-columns:1fr}}.section{background:#1e293b;border-radius:12px;padding:20px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1)}.section h2{font-size:1.1rem;color:#f1c40f;margin-bottom:12px}.form-group{margin-bottom:14px}.form-group label{display:block;color:#94a3b8;font-size:.9rem;margin-bottom:6px;font-weight:500}.form-group input,.form-group select,.form-group textarea{width:100%;padding:10px 14px;background:#0f172a;border:1px solid rgba(148,163,184,.2);border-radius:8px;color:#e2e8f0;font-size:.9rem;outline:none;transition:all .2s}.form-group input:focus,.form-group select:focus,.form-group textarea:focus{border-color:rgba(6,182,212,.4);box-shadow:0 0 0 3px rgba(6,182,212,.1)}.form-row{display:flex;gap:12px;flex-wrap:wrap}.form-row .form-group{flex:1;min-width:200px}.btn-group{display:flex;gap:8px;flex-wrap:wrap;margin:12px 0}.btn{padding:10px 24px;border:none;border-radius:8px;font-size:.9rem;cursor:pointer;transition:all .2s;font-weight:600}.btn-primary{background:rgba(6,182,212,.2);color:#22d3ee;border:1px solid rgba(6,182,212,.3)}.btn-primary:hover{background:rgba(6,182,212,.3)}.btn-secondary{background:rgba(148,163,184,.1);color:#94a3b8;border:1px solid rgba(148,163,184,.2)}.btn-secondary:hover{background:rgba(148,163,184,.2)}.btn-success{background:rgba(34,197,94,.15);color:#4ade80;border:1px solid rgba(34,197,94,.2)}.btn-success:hover{background:rgba(34,197,94,.25)}.btn-danger{background:rgba(239,68,68,.15);color:#f87171;border:1px solid rgba(239,68,68,.2)}.btn-danger:hover{background:rgba(239,68,68,.25)}.ad-slot{margin:16px auto;text-align:center;max-width:960px;min-height:90px;background:rgba(148,163,184,.05);border-radius:8px}.ad-slot:empty{display:none}.ad-slot ins{display:block}.ad-slot.ad-sidebar{min-height:250px;max-width:300px}.seo-content{margin-top:24px;padding:20px;background:#1e293b;border-radius:12px;border:1px solid rgba(148,163,184,.1)}.seo-content h2{font-size:1.1rem;color:#f1c40f;margin:16px 0 8px}.seo-content h3{font-size:1rem;color:#e2e8f0;margin:12px 0 6px}.seo-content p{color:#94a3b8;margin-bottom:8px;font-size:.9rem}.seo-content ul,.seo-content ol{margin-left:20px;margin-bottom:8px;color:#94a3b8;font-size:.9rem}.seo-content li{margin-bottom:4px}.faq-item{margin-bottom:12px;padding:12px;background:#0f172a;border-radius:8px;border:1px solid rgba(148,163,184,.1)}.faq-item h3{font-size:.95rem;color:#e2e8f0;margin-bottom:6px;cursor:pointer}.faq-item p{color:#94a3b8;font-size:.85rem}.footer{border-top:1px solid rgba(148,163,184,.1);padding:24px 0;margin-top:32px;text-align:center;color:#64748b;font-size:.85rem}.footer a{color:#64748b;margin:0 8px}.footer a:hover{color:#94a3b8}.footer p{margin-bottom:8px}.toast{position:fixed;bottom:20px;right:20px;background:#1e293b;color:#e2e8f0;padding:12px 20px;border-radius:8px;border:1px solid rgba(148,163,184,.2);opacity:0;transition:opacity .3s;z-index:1000;pointer-events:none}.toast.show{opacity:1}'''

# 广告位模板
AD_TOP = '<div class="ad-slot" id="ad-top"><ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-5998441792679372" data-ad-slot="XXXXXXX" data-ad-format="horizontal" data-full-width-responsive="true"></ins></div>'
AD_MID = '<div class="ad-slot" style="margin:24px auto"><ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-5998441792679372" data-ad-slot="XXXXXXX" data-ad-format="horizontal" data-full-width-responsive="true"></ins></div>'
AD_SIDEBAR1 = '<div class="ad-slot ad-sidebar"><ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-5998441792679372" data-ad-slot="XXXXXXX" data-ad-format="rectangle" data-full-width-responsive="true"></ins></div>'
AD_SIDEBAR2 = '<div class="ad-slot ad-sidebar" style="margin-top:16px"><ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-5998441792679372" data-ad-slot="XXXXXXX" data-ad-format="rectangle" data-full-width-responsive="true"></ins></div>'

# ============================================================
# 二、Schema生成器（Google规则兼容）
# ============================================================

def schema_software(name, desc, cat='UtilitiesApplication'):
    """SoftwareApplication Schema - Google要求字段"""
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": name,
        "description": desc,
        "applicationCategory": cat,
        "operatingSystem": "Web",
        "publisher": {
            "@type": "Organization",
            "name": "Free ToolBase",
            "email": "dexshuang@google.com"
        },
        "offers": {
            "@type": "Offer",
            "price": "0",
            "priceCurrency": "USD"
        }
    }, ensure_ascii=False)

def schema_faq(faqs):
    """FAQPage Schema"""
    entities = []
    for q, a in faqs:
        entities.append({
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {
                "@type": "Answer",
                "text": a
            }
        })
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": entities
    }, ensure_ascii=False)

def schema_howto(name, steps):
    """HowTo Schema"""
    step_list = []
    for i, (sname, stext) in enumerate(steps, 1):
        step_list.append({
            "@type": "HowToStep",
            "position": i,
            "name": sname,
            "text": stext
        })
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "HowTo",
        "name": f"如何使用{name}",
        "description": f"{name}的使用步骤",
        "totalTime": "PT2M",
        "tool": {"@type": "HowToTool", "name": name},
        "step": step_list
    }, ensure_ascii=False)

def schema_breadcrumb(cat_name, cat_anchor, tool_name, tool_url):
    """BreadcrumbList Schema"""
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "首页", "item": "https://free-toolbase.com/"},
            {"@type": "ListItem", "position": 2, "name": cat_name, "item": f"https://free-toolbase.com/#{cat_anchor}"},
            {"@type": "ListItem", "position": 3, "name": tool_name, "item": tool_url}
        ]
    }, ensure_ascii=False)

# ============================================================
# 三、页面构建器
# ============================================================

class ToolPageBuilder:
    """统一页面构建器 - 所有新工具和重构页面必须使用"""
    
    def build(self, slug, title_cn, title_en, desc_cn, desc_en, icon,
              cat_cn, cat_en, cat_anchor,
              tool_html_cn, tool_html_en, tool_js,
              faqs_cn, faqs_en,
              seo_cn='', seo_en='',
              custom_css='',
              lang='zh'):
        """
        构建单个页面
        
        参数:
            slug: URL路径名（如 'bmi-calculator'）
            title_cn: 中文标题
            title_en: 英文标题
            desc_cn: 中文描述（120字内）
            desc_en: 英文描述
            icon: 图标emoji
            cat_cn: 中文分类名
            cat_en: 英文分类名
            cat_anchor: 分类锚点（如 'calculators'）
            tool_html_cn: 中文工具HTML
            tool_html_en: 英文工具HTML
            tool_js: 工具JavaScript（中英文共用）
            faqs_cn: 中文FAQ [(Q,A),...]
            faqs_en: 英文FAQ [(Q,A),...]
            seo_cn: 中文SEO长文HTML
            seo_en: 英文SEO长文HTML
            custom_css: 页面特有CSS（追加到统一CSS后）
            lang: 'zh'或'en'
        """
        is_cn = lang == 'zh'
        title = title_cn if is_cn else title_en
        desc = desc_cn if is_cn else desc_en
        cat = cat_cn if is_cn else cat_en
        faqs = faqs_cn if is_cn else faqs_en
        tool_html = tool_html_cn if is_cn else tool_html_en
        seo = seo_cn if is_cn else seo_en
        
        # URL
        base_url = f"https://free-toolbase.com/{slug}/" if is_cn else f"https://free-toolbase.com/en/{slug}/"
        hreflang_zh = f"https://free-toolbase.com/{slug}/"
        hreflang_en = f"https://free-toolbase.com/en/{slug}/"
        
        # 语言切换
        switch_cn = "index.html" if is_cn else f"../{slug}/"
        switch_en = f"../en/{slug}/" if is_cn else "index.html"
        active_cn = 'active' if is_cn else ''
        active_en = '' if is_cn else 'active'
        
        # 面包屑
        breadcrumb = f'<a href="../index.html">{"首页" if is_cn else "Home"}</a> &rsaquo; <a href="../index.html#{cat_anchor}">{cat}</a> &rsaquo; {title}'
        
        # Hero
        hero_text = f'{desc} · {"纯前端本地处理 · 数据绝不上传服务器" if is_cn else "Pure Frontend · No Server Uploads"}'
        badge_text = '零依赖·可离线使用' if is_cn else 'Zero Dependencies·Works Offline'
        
        # FAQ HTML
        faq_html = ''
        for q, a in faqs:
            faq_html += f'<div class="faq-item"><h3>{q}</h3><p>{a}</p></div>\n'
        
        # Footer
        home_label = "首页" if is_cn else "Home"
        all_label = "全部工具" if is_cn else "All Tools"
        contact_label = "联系我们" if is_cn else "Contact"
        privacy_label = "隐私政策" if is_cn else "Privacy"
        terms_label = "服务条款" if is_cn else "Terms"
        about_label = "关于我们" if is_cn else "About"
        other_label = "EN" if is_cn else "中文"
        other_url = f"../en/{slug}/" if is_cn else f"../{slug}/"
        tagline = f'{title} · {"纯前端本地处理 · 数据绝不上传服务器" if is_cn else "Pure Frontend · No Server Uploads"}'
        feedback_label = "问题反馈" if is_cn else "Feedback"
        
        footer = f'''<div class="footer container">
<div style="margin-bottom:12px">
<a href="../index.html">{home_label}</a>
<a href="../index.html">{all_label}</a>
<a href="mailto:dexshuang@google.com">{contact_label}</a>
<a href="../privacy/">{privacy_label}</a>
<a href="../terms/">{terms_label}</a>
<a href="../about/">{about_label}</a>
<a href="{other_url}">{other_label}</a>
</div>
<p>{tagline}</p>
<p style="margin-top:8px;color:#475569;font-size:.8rem">{feedback_label}: dexshuang@google.com</p>
</div>'''
        
        # Schema
        schema_soft = schema_software(title, desc)
        schema_faq_json = schema_faq(faqs)
        schema_how = schema_howto(title, [
            ("准备输入" if is_cn else "Prepare Input", "输入或粘贴需要处理的数据" if is_cn else "Enter or paste data to process"),
            ("配置选项" if is_cn else "Configure Options", "根据需要调整参数设置" if is_cn else "Adjust parameters as needed"),
            ("查看结果" if is_cn else "View Results", "获取处理后的输出结果" if is_cn else "Get processed output")
        ])
        schema_bc = schema_breadcrumb(cat, cat_anchor, title, base_url)
        
        # 组装页面
        page = f'''<!DOCTYPE html>
<html lang="{'zh-CN' if is_cn else 'en'}">
<head>
{GA4}
{ADSENSE}
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="{desc}">
<meta name="keywords" content="{title},{cat},{'在线工具' if is_cn else 'online tool'},{'免费' if is_cn else 'free'}">
<title>{title} - {"免费在线工具·纯前端本地处理" if is_cn else "Free Online Tool·Pure Frontend"}</title>
<link rel="canonical" href="{base_url}">
<meta property="og:title" content="{icon} {title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{base_url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{"Free ToolBase" if is_cn else "Free ToolBase"}">
<link rel="alternate" hreflang="zh" href="{hreflang_zh}">
<link rel="alternate" hreflang="en" href="{hreflang_en}">
<link rel="alternate" hreflang="x-default" href="{hreflang_en}">
<script type="application/ld+json">{schema_soft}</script>
<script type="application/ld+json">{schema_faq_json}</script>
<script type="application/ld+json">{schema_how}</script>
<script type="application/ld+json">{schema_bc}</script>
<style>{custom_css if custom_css.strip().startswith('*{box-sizing') else CSS_UNIFIED + custom_css}</style>
</head>
<body>
{AD_TOP}
<div class="container">
<div class="header"><h1>{icon} {title}</h1><div class="lang-switch"><a href="{switch_cn}" class="{active_cn}">中文</a><a href="{switch_en}" class="{active_en}">EN</a></div></div>
<p class="nav-back">{breadcrumb}</p>
<div class="hero"><p>{hero_text}</p><span class="badge">{badge_text}</span></div>
<div class="main-grid">
<div><div class="section">{tool_html}</div></div>
<div>{AD_SIDEBAR1}{AD_SIDEBAR2}</div>
</div>
{AD_MID}
<div class="seo-content">{seo}</div>
<div class="section"><h2>{"常见问题" if is_cn else "FAQ"}</h2>{faq_html}</div>
{AD_MID}
</div>
{footer}
<div class="toast" id="toast"></div>
<script>
function showToast(m){{var t=document.getElementById("toast");t.textContent=m;t.classList.add("show");setTimeout(function(){{t.classList.remove("show")}},3000)}}
function copyText(id){{var el=document.getElementById(id);if(!el)return;var t=el.textContent||el.innerText;navigator.clipboard.writeText(t).then(function(){{showToast("{'已复制' if is_cn else 'Copied'}")}})["catch"](function(){{showToast("{'复制失败' if is_cn else 'Copy failed'}")}})}}
{tool_js}
</script>
</body>
</html>'''
        
        return page
    
    def save(self, page_html, slug, lang='zh'):
        """保存页面到指定路径"""
        if lang == 'zh':
            dir_path = os.path.join(BASE, slug)
        else:
            dir_path = os.path.join(BASE, 'en', slug)
        
        os.makedirs(dir_path, exist_ok=True)
        file_path = os.path.join(dir_path, 'index.html')
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(page_html)
        
        return file_path
    
    def build_bilingual(self, **kwargs):
        """同时生成中英文版本"""
        cn_page = self.build(lang='zh', **kwargs)
        en_page = self.build(lang='en', **kwargs)
        
        cn_path = self.save(cn_page, kwargs['slug'], 'zh')
        en_path = self.save(en_page, kwargs['slug'], 'en')
        
        return cn_path, en_path


# ============================================================
# 四、页面提取器（用于重构老页面）
# ============================================================

class PageExtractor:
    """从现有HTML页面提取内核内容"""
    
    def extract(self, html_content):
        """提取页面内核内容 - 支持多种HTML结构"""
        import re
        
        result = {}
        
        # 1. 提取meta信息
        title_match = re.search(r'<title>(.*?)</title>', html_content, re.I)
        result['title'] = title_match.group(1) if title_match else ''
        
        desc_match = re.search(r'<meta name="description" content="(.*?)">', html_content, re.I)
        result['desc'] = desc_match.group(1) if desc_match else ''
        
        keywords_match = re.search(r'<meta name="keywords" content="(.*?)">', html_content, re.I)
        result['keywords'] = keywords_match.group(1) if keywords_match else ''
        
        # 2. 提取canonical
        canon_match = re.search(r'<link rel="canonical" href="(.*?)">', html_content, re.I)
        result['canonical'] = canon_match.group(1) if canon_match else ''
        
        # 3. 提取Schema
        schema_matches = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html_content, re.S)
        result['schemas'] = schema_matches
        
        # 4. 提取body内容
        body_match = re.search(r'<body[^>]*>(.*?)</body>', html_content, re.S|re.I)
        body = body_match.group(1) if body_match else html_content
        
        # 5. 找到工具HTML区域
        # 策略1：找到ad-slot#ad-top结束位置
        ad_top_match = re.search(r'<div class="ad-slot" id="ad-top">.*?</div>\s*', body, re.S|re.I)
        # 策略2：如果没有ad-slot，找ad-container（旧版页面）
        if not ad_top_match:
            ad_top_match = re.search(r'<div class="ad-container"[^>]*>.*?</div>\s*', body, re.S|re.I)
        
        tool_start = ad_top_match.end() if ad_top_match else 0
        
        # 找到footer开始位置
        footer_match = re.search(r'<(div class="footer|footer)', body, re.S|re.I)
        tool_end = footer_match.start() if footer_match else len(body)
        
        if tool_start > 0 and tool_end > tool_start:
            middle = body[tool_start:tool_end]
            
            # 去掉所有广告位（ad-slot和ad-container）
            middle = re.sub(r'<div class="ad-slot[^"]*"[^>]*>.*?</div>\s*', '', middle, flags=re.S|re.I)
            middle = re.sub(r'<div class="ad-container"[^>]*>.*?</div>\s*', '', middle, flags=re.S|re.I)
            
            # 去掉container开始标签
            middle = re.sub(r'^\s*<div class="container">\s*', '', middle, count=1)
            # 去掉container结束标签
            middle = re.sub(r'\s*</div>\s*$', '', middle, count=1)
            
            # 去掉header区域（多种格式）
            middle = re.sub(r'<div class="header">.*?</div>\s*<p class="nav-back">.*?</p>\s*', '', middle, count=1, flags=re.S|re.I)
            middle = re.sub(r'<header>.*?</header>\s*', '', middle, count=1, flags=re.S|re.I)
            
            # 去掉hero区域
            middle = re.sub(r'<div class="hero">.*?</div>\s*', '', middle, count=1, flags=re.S|re.I)
            
            # 去掉breadcrumb
            middle = re.sub(r'<p class="nav-back">.*?</p>\s*', '', middle, count=1, flags=re.S|re.I)
            middle = re.sub(r'<div class="nav-back">.*?</div>\s*', '', middle, count=1, flags=re.S|re.I)
            
            # 去掉SEO内容
            seo_match = re.search(r'<div class="seo-content">(.*?)</div>', middle, re.S|re.I)
            result['seo'] = seo_match.group(1) if seo_match else ''
            middle = re.sub(r'<div class="seo-content">.*?</div>\s*', '', middle, count=1, flags=re.S|re.I)
            
            # 去掉FAQ区域
            faq_match = re.search(r'<div class="section">\s*<h2>.*?</h2>\s*(.*?)</div>\s*</div>', middle, re.S|re.I)
            if faq_match:
                result['faq_html'] = faq_match.group(1)
                middle = re.sub(r'<div class="section">\s*<h2>.*?</h2>\s*.*?</div>\s*</div>\s*', '', middle, count=1, flags=re.S|re.I)
            
            # 去掉feedback-widget
            middle = re.sub(r'<div class="feedback-widget">.*?</div>\s*', '', middle, flags=re.S|re.I)
            
            # 去掉related-tools
            middle = re.sub(r'<div class="related-tools">.*?</div>\s*', '', middle, flags=re.S|re.I)
            
            # 去掉toast
            middle = re.sub(r'<div class="toast"[^>]*>.*?</div>\s*', '', middle, flags=re.S|re.I)
            
            # 剩下的就是工具HTML
            result['tool_html'] = middle.strip()
        else:
            # 如果找不到ad-top和footer，尝试从h1和第一个ad-container之间提取
            h1_end = re.search(r'</h1>', body, re.I)
            if h1_end:
                after_h1 = body[h1_end.end():]
                ad_match = re.search(r'<div class="ad-container"[^>]*>.*?</div>', after_h1, re.S|re.I)
                if ad_match:
                    tool_html = after_h1[:ad_match.start()]
                    # 清理
                    tool_html = re.sub(r'<div class="lang-switch".*?</div>\s*', '', tool_html, count=1, flags=re.S|re.I)
                    tool_html = re.sub(r'<div class="star-rating".*?</div>\s*', '', tool_html, count=1, flags=re.S|re.I)
                    tool_html = re.sub(r'<div class="trust-signals".*?</div>\s*', '', tool_html, count=1, flags=re.S|re.I)
                    tool_html = re.sub(r'<div class="nav-back">.*?</div>\s*', '', tool_html, count=1, flags=re.S|re.I)
                    tool_html = re.sub(r'<p class="nav-back">.*?</p>\s*', '', tool_html, count=1, flags=re.S|re.I)
                    result['tool_html'] = tool_html.strip()
                else:
                    result['tool_html'] = ''
            else:
                result['tool_html'] = ''
            result['seo'] = ''
        
        # 6. 提取工具JS（最后一个script标签）
        js_matches = re.findall(r'<script>(.*?)</script>', body, re.S|re.I)
        if js_matches:
            # 通常最后一个script是工具JS
            result['tool_js'] = js_matches[-1]
        else:
            result['tool_js'] = ''
        
        # 7. 提取自定义CSS
        style_match = re.search(r'<style[^>]*>(.*?)</style>', html_content, re.S|re.I)
        if style_match:
            css = style_match.group(1)
            # normalize后匹配统一CSS前缀，找到分割点
            css_norm = re.sub(r'\s+', '', css)
            unified_norm = re.sub(r'\s+', '', CSS_UNIFIED)
            if css_norm.startswith(unified_norm):
                # 逐字符扫描原始css，跳过空白差异，找到统一CSS结束位置
                ui = 0  # unified_norm的索引
                end_pos = 0  # 原始css中统一CSS结束的位置
                for ci in range(len(css)):
                    if ui >= len(unified_norm):
                        end_pos = ci
                        break
                    if css[ci].isspace():
                        continue
                    if css[ci] == unified_norm[ui]:
                        ui += 1
                    else:
                        break
                if ui >= len(unified_norm):
                    result['custom_css'] = css[end_pos:]
                else:
                    result['custom_css'] = css
            else:
                # 原页面CSS不以统一CSS开头，保留全部
                result['custom_css'] = css
        else:
            result['custom_css'] = ''
        
        # 8. 提取icon
        icon_match = re.search(r'<h1>(\S+)\s', html_content)
        result['icon'] = icon_match.group(1) if icon_match else '🔧'
        
        # 9. 提取FAQ（如果上面没提取到）
        if 'faq_html' not in result or not result['faq_html']:
            faq_items = re.findall(r'<div class="faq-item">(.*?)</div>', body, re.S|re.I)
            result['faq_items'] = faq_items
        
        return result


# ============================================================
# 五、使用示例
# ============================================================

if __name__ == '__main__':
    # 示例：创建一个新工具
    builder = ToolPageBuilder()
    
    cn_path, en_path = builder.build_bilingual(
        slug='test-tool-v3',
        title_cn='测试工具V3',
        title_en='Test Tool V3',
        desc_cn='这是一个测试工具，用于验证模板V3的正确性。',
        desc_en='This is a test tool for verifying template v3.',
        icon='🧪',
        cat_cn='测试工具',
        cat_en='Test Tools',
        cat_anchor='test-tools',
        tool_html_cn='<div class="form-group"><label>输入</label><textarea id="input"></textarea></div><div class="btn-group"><button class="btn btn-primary" onclick="process()">处理</button></div><div class="form-group"><label>输出</label><textarea id="output" readonly></textarea></div>',
        tool_html_en='<div class="form-group"><label>Input</label><textarea id="input"></textarea></div><div class="btn-group"><button class="btn btn-primary" onclick="process()">Process</button></div><div class="form-group"><label>Output</label><textarea id="output" readonly></textarea></div>',
        tool_js='function process(){var i=document.getElementById("input").value;document.getElementById("output").value=i.toUpperCase();showToast("处理完成");}',
        faqs_cn=[
            ('这个工具做什么？', '这是一个测试工具，用于验证模板。'),
            ('数据安全吗？', '所有处理在浏览器本地完成，不上传服务器。'),
        ],
        faqs_en=[
            ('What does this tool do?', 'This is a test tool for template verification.'),
            ('Is my data safe?', 'All processing happens locally in your browser.'),
        ],
        seo_cn='<h2>测试工具介绍</h2><p>这是一个用于测试模板V3的工具。</p>',
        seo_en='<h2>Test Tool Introduction</h2><p>This is a tool for testing template v3.</p>',
    )
    
    print(f"Created: {cn_path}")
    print(f"Created: {en_path}")
    
    # 示例：提取老页面
    extractor = PageExtractor()
    with open('/home/chison/tools-site/bmi-calculator/index.html', 'r') as f:
        old_page = f.read()
    
    extracted = extractor.extract(old_page)
    print(f"\nExtracted from bmi-calculator:")
    print(f"  Title: {extracted['title']}")
    print(f"  Desc: {extracted['desc'][:50]}...")
    print(f"  Tool HTML: {len(extracted['tool_html'])} bytes")
    print(f"  Tool JS: {len(extracted['tool_js'])} bytes")
    print(f"  SEO: {len(extracted['seo'])} bytes")
    print(f"  FAQ items: {len(extracted['faq_items'])}")
    print(f"  Schemas: {len(extracted['schemas'])}")
