#!/usr/bin/env python3
"""批量创建5个新工具的中英文版本"""
import os, json

tools_to_create = [
    {
        'slug': 'fifo-lifo-calculator',
        'cn_title': 'FIFO/LIFO 库存成本计算器',
        'en_title': 'FIFO/LIFO Inventory Cost Calculator',
        'cn_desc': '免费在线FIFO/LIFO库存成本计算器，计算先进先出/后进先出库存计价。支持多批次管理，自动计算期末存货和销货成本。纯前端处理，数据不上传。',
        'en_desc': 'Free online FIFO/LIFO inventory cost calculator. Calculate first-in-first-out / last-in-first-out inventory valuation. Supports multi-batch management, auto-calculates ending inventory and COGS. Pure frontend, no data upload.',
        'cn_h1': '📦 FIFO/LIFO 库存成本计算器',
        'en_h1': '📦 FIFO/LIFO Inventory Cost Calculator',
        'category': 'business',
        'keywords': 'FIFO,LIFO,inventory,cost,库存,先进先出,后进先出',
    },
    {
        'slug': 'fitness-plan-generator',
        'cn_title': '健身计划生成器',
        'en_title': 'Fitness Plan Generator',
        'cn_desc': '免费在线健身计划生成器，根据目标（增肌/减脂/塑形）自动生成个性化训练计划。包含每周训练安排、动作指导、组数次数。纯前端处理，数据不上传。',
        'en_desc': 'Free online fitness plan generator. Auto-generates personalized training plans based on goals (muscle gain/fat loss/body shaping). Includes weekly schedule, exercise guide, sets and reps. Pure frontend, no data upload.',
        'cn_h1': '🏋️ 健身计划生成器',
        'en_h1': '🏋️ Fitness Plan Generator',
        'category': 'health',
        'keywords': 'fitness,workout,exercise,gym,training,健身,训练,运动',
    },
    {
        'slug': 'gross-profit-calculator',
        'cn_title': '毛利润计算器',
        'en_title': 'Gross Profit Calculator',
        'cn_desc': '免费在线毛利润计算器，计算毛利润、毛利率和加价率。支持批量计算，对比多个产品的利润率。纯前端处理，数据不上传。',
        'en_desc': 'Free online gross profit calculator. Calculate gross profit, gross margin and markup percentage. Supports batch calculation and profit comparison across multiple products. Pure frontend, no data upload.',
        'cn_h1': '💰 毛利润计算器',
        'en_h1': '💰 Gross Profit Calculator',
        'category': 'business',
        'keywords': 'gross profit,margin,markup,profit,毛利润,毛利率',
    },
    {
        'slug': 'co-worker-salary-calculator',
        'cn_title': '同行薪资对比计算器',
        'en_title': 'Co-worker Salary Comparison Calculator',
        'cn_desc': '免费在线同行薪资对比计算器，比较不同岗位/经验/城市的薪资水平。支持多维度对比分析，计算薪资差距和涨幅。纯前端处理，数据不上传。',
        'en_desc': 'Free online co-worker salary comparison calculator. Compare salaries across different roles, experience levels, and cities. Supports multi-dimensional comparison with gap and growth analysis. Pure frontend, no data upload.',
        'cn_h1': '👥 同行薪资对比计算器',
        'en_h1': '👥 Co-worker Salary Comparison Calculator',
        'category': 'finance',
        'keywords': 'salary,comparison,pay,income,wage,薪资,对比,工资',
    },
    {
        'slug': 'day-trading-calculator',
        'cn_title': '日内交易盈亏计算器',
        'en_title': 'Day Trading P&L Calculator',
        'cn_desc': '免费在线日内交易盈亏计算器，计算股票/加密货币交易盈亏。支持多笔交易汇总、手续费计算、盈亏比分析。纯前端处理，数据不上传。',
        'en_desc': 'Free online day trading P&L calculator. Calculate stock/crypto trading profit and loss. Supports multi-trade aggregation, fee calculation, and win/loss ratio analysis. Pure frontend, no data upload.',
        'cn_h1': '📈 日内交易盈亏计算器',
        'en_h1': '📈 Day Trading P&L Calculator',
        'category': 'finance',
        'keywords': 'day trading,P&L,stock,crypto,profit,loss,交易,盈亏',
    },
]

def make_tool(tool_info, lang):
    slug = tool_info['slug']
    is_cn = lang == 'cn'
    
    title = tool_info['cn_title'] if is_cn else tool_info['en_title']
    desc = tool_info['cn_desc'] if is_cn else tool_info['en_desc']
    h1 = tool_info['cn_h1'] if is_cn else tool_info['en_h1']
    keywords = tool_info['keywords']
    
    if is_cn:
        lang_code = 'zh-CN'
        home_link = '../'
        en_link = f'../en/{slug}/'
        cn_link = 'index.html'
        canonical = f'https://free-toolbase.com/{slug}/'
        en_canonical = f'https://free-toolbase.com/en/{slug}/'
        x_default = en_canonical
        home_name = '首页'
        tools_name = '工具'
        privacy_text = '隐私政策'
        result_copied = '结果已复制 📋'
        breadcrumb_name = title
        no_reg = '无需注册 · 数据绝不上传服务器'
        zero_dep = '零依赖·可离线使用'
        no_result = '没有可复制的结果'
        seo_extra = f'<p>{title}是一款免费的在线工具，帮助用户快速进行相关计算。所有处理在浏览器本地完成，数据不上传，保障隐私安全。该工具响应速度快，支持移动端使用，操作简便直观。</p>'
        related_title = '🔗 相关工具推荐'
        cn_url_str = canonical
    else:
        lang_code = 'en'
        home_link = '../'
        en_link = 'index.html'
        cn_link = f'../../{slug}/'
        canonical = f'https://free-toolbase.com/en/{slug}/'
        en_canonical = canonical
        cn_url_str = f'https://free-toolbase.com/{slug}/'
        x_default = canonical
        home_name = 'Home'
        tools_name = 'Tools'
        privacy_text = 'Privacy Policy'
        result_copied = 'Results copied 📋'
        breadcrumb_name = title
        no_reg = 'No registration · Data never leaves your device'
        zero_dep = 'Zero dependencies · Works offline'
        no_result = 'No results to copy'
        seo_extra = f'<p>The {title} is a free online tool that helps users perform quick calculations. All processing happens locally in the browser with no data upload, ensuring privacy. The tool is fast, mobile-friendly, and easy to use.</p>'
        related_title = '🔗 Related Tools'
    
    bc_data = json.dumps({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": home_name, "item": f"https://free-toolbase.com/{'' if is_cn else 'en/'}"},
            {"@type": "ListItem", "position": 2, "name": tools_name, "item": f"https://free-toolbase.com/{'' if is_cn else 'en/'}#tools"},
            {"@type": "ListItem", "position": 3, "name": breadcrumb_name}
        ]
    }, ensure_ascii=False)
    
    sa_data = json.dumps({
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": title,
        "description": desc,
        "applicationCategory": "BusinessApplication",
        "operatingSystem": "Web",
        "publisher": {"@type": "Organization", "name": "Free ToolBase", "email": "dexshuang@google.com"},
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}
    }, ensure_ascii=False)
    
    html = f'''<!DOCTYPE html>
<html lang="{lang_code}">
<head>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-9W1157EBQV"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-9W1157EBQV');</script>
<script>window.addEventListener("error",function(e){{if(e&&e.message===""){{e.preventDefault();}}}});window.addEventListener("unhandledrejection",function(e){{if(e&&e.reason&&e.reason.message===""){{e.preventDefault();}}}});</script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="{desc}">
<meta name="keywords" content="{keywords}">
<title>{title} - Free ToolBase</title>
<link rel="canonical" href="{canonical}">
<meta property="og:title" content="{title} - Free ToolBase">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Free ToolBase">
<meta property="og:image" content="https://free-toolbase.com/og-image.svg">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="https://free-toolbase.com/og-image.svg">
<meta name="robots" content="index, follow">
<link rel="icon" type="image/svg+xml" href="{home_link}favicon.svg">
<link rel="alternate" hreflang="{'zh' if is_cn else 'en'}" href="{canonical}">
<link rel="alternate" hreflang="{'en' if is_cn else 'zh'}" href="{en_canonical if is_cn else cn_url_str}">
<link rel="alternate" hreflang="x-default" href="{x_default}">
<script type="application/ld+json">{sa_data}</script>
<script type="application/ld+json">{bc_data}</script>
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5998441792679372" crossorigin="anonymous"></script>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#0f172a;color:#e2e8f0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;line-height:1.6;min-height:100vh}}
a{{color:#06b6d4;text-decoration:none}}a:hover{{color:#22d3ee}}
.container{{max-width:960px;margin:0 auto;padding:24px 16px}}
.header{{display:flex;justify-content:space-between;align-items:center;margin-bottom:24px;flex-wrap:wrap;gap:12px}}
.header h1{{font-size:1.5rem;color:#f1c40f}}
.lang-switch{{display:flex;gap:4px;background:#1e293b;border-radius:8px;padding:4px;border:1px solid rgba(148,163,184,.1)}}
.lang-switch a{{padding:6px 12px;border-radius:5px;font-size:.85rem;color:#94a3b8}}
.lang-switch a.active{{background:rgba(6,182,212,.2);color:#22d3ee}}
.nav-back{{color:#64748b;font-size:.85rem;margin-bottom:16px}}
.nav-back a{{color:#64748b}}.nav-back a:hover{{color:#94a3b8}}
.hero{{margin-bottom:24px}}.hero p{{color:#94a3b8;font-size:1rem;margin-bottom:8px}}
.badge{{display:inline-block;background:rgba(6,182,212,.15);color:#22d3ee;padding:4px 12px;border-radius:20px;font-size:.8rem;margin-bottom:16px}}
.section{{background:#1e293b;border-radius:12px;padding:20px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1)}}
.section h2{{font-size:1.1rem;color:#f1c40f;margin-bottom:12px}}
.form-group{{margin-bottom:12px}}
.form-group label{{display:block;color:#94a3b8;font-size:.85rem;margin-bottom:4px;font-weight:500}}
.form-group input,.form-group select{{width:100%;padding:10px 14px;background:#0f172a;border:1px solid rgba(148,163,184,.2);border-radius:8px;color:#e2e8f0;font-size:.9rem;outline:none;transition:all .2s}}
.form-group input:focus,.form-group select:focus{{border-color:rgba(6,182,212,.4);box-shadow:0 0 0 3px rgba(6,182,212,.1)}}
.form-group select{{cursor:pointer}}
.form-row{{display:flex;gap:10px;flex-wrap:wrap}}.form-row .form-group{{flex:1;min-width:120px}}
.result-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:12px}}
.result-card{{background:#0f172a;border-radius:10px;padding:16px;border:1px solid rgba(148,163,184,.1);text-align:center}}
.result-card .result-label{{color:#94a3b8;font-size:.8rem;margin-bottom:4px}}
.result-card .result-value{{font-size:1.3rem;font-weight:700;color:#06b6d4}}
.result-card.highlight{{border-color:rgba(16,185,129,.4);background:rgba(16,185,129,.05)}}.result-card.highlight .result-value{{color:#10b981}}
.result-card.warn{{border-color:rgba(239,68,68,.2)}}.result-card.warn .result-value{{color:#ef4444}}
.btn-row{{display:flex;gap:10px;flex-wrap:wrap;margin-top:16px}}
.btn{{padding:10px 20px;border-radius:8px;border:none;cursor:pointer;font-size:.9rem;font-weight:500;transition:all .2s}}
.btn-primary{{background:#06b6d4;color:#fff}}.btn-primary:hover{{background:#0891b2}}
.btn-secondary{{background:#334155;color:#e2e8f0}}.btn-secondary:hover{{background:#475569}}
.toast{{position:fixed;bottom:20px;left:50%;transform:translateX(-50%);background:#1e293b;color:#22d3ee;padding:10px 24px;border-radius:8px;border:1px solid rgba(6,182,212,.3);font-size:.85rem;z-index:999;opacity:0;transition:opacity .3s}}
.task-item{{background:#0f172a;border-radius:8px;padding:12px;margin-bottom:8px;border:1px solid rgba(148,163,184,.1)}}
.task-header{{display:flex;justify-content:space-between;align-items:center;margin-bottom:8px}}
.task-name{{font-weight:600;color:#e2e8f0}}
.task-del{{color:#ef4444;cursor:pointer;font-size:.85rem}}.task-del:hover{{color:#f87171}}
.detail-row{{display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid rgba(148,163,184,.06)}}
.detail-label{{color:#94a3b8;font-size:.85rem}}
.detail-value{{font-weight:600;color:#06b6d4}}
@media(max-width:640px){{h1{{font-size:1.2rem;word-break:break-word}}.container{{padding:0 12px}}.btn{{padding:8px 14px;font-size:.85rem}}.panel{{padding:16px}}.result-grid{{grid-template-columns:1fr 1fr}}}}
</style>
</head>
<body>
<div class="container">
<div class="header"><h1>{h1}</h1>
<div class="lang-switch"><a href="{cn_link}"{' class="active"' if is_cn else ''}>中文</a><a href="{en_link}"{'' if is_cn else ' class="active"'}>EN</a></div></div>
<p class="nav-back"><a href="{home_link}">{home_name}</a> › <a href="{home_link}#tools">{tools_name}</a> › {breadcrumb_name}</p>
<div class="hero"><p>{desc} | {no_reg}</p><span class="badge">{zero_dep}</span></div>

<div id="toolContent"></div>

<div class="seo-content" style="margin:1.5rem 0;padding:1rem;background:#f8fafc;border-radius:8px;font-size:.95rem;color:#475569;line-height:1.8">{seo_extra}</div>
<section class="related-tools" style="margin:2rem 0;padding:1rem;background:#f8fafc;border-radius:8px;"><h2 style="font-size:1.1rem;margin-bottom:0.5rem;color:#374151;">{related_title}</h2><div style="display:flex;flex-wrap:wrap;gap:4px;"></div></section>
</div>
<div id="toast" class="toast"></div>
<script>
(function(){{
var el=function(id){{return document.getElementById(id);}};
var toastTimer=null;
function showToast(msg){{var t=el('toast');t.textContent=msg;t.style.opacity='1';clearTimeout(toastTimer);toastTimer=setTimeout(function(){{t.style.opacity='0';}},2000);}}
function copyResults(){{
  var labels=document.querySelectorAll('.result-label');
  var text=[];
  labels.forEach(function(label){{
    var valEl=label.nextElementSibling;
    if(valEl&&valEl.classList.contains('result-value')){{
      text.push(label.textContent+': '+valEl.textContent);
    }}
  }});
  var details=document.querySelectorAll('.detail-row');
  details.forEach(function(row){{
    var lbl=row.querySelector('.detail-label');
    var val=row.querySelector('.detail-value');
    if(lbl&&val)text.push(lbl.textContent+': '+val.textContent);
  }});
  if(text.length>0){{navigator.clipboard.writeText(text.join('\\n')).then(function(){{showToast('{result_copied}');}});}}
  else{{showToast('{no_result}');}}
}}

var TOOL_SLUG='{slug}';
var LANG='{lang_code}';

}})();
</script>
<footer style="border-top:1px solid rgba(148,163,184,.1);padding:24px 0;margin-top:32px;text-align:center;color:#64748b;font-size:.85rem"><a href="{home_link}" style="color:#64748b;margin:0 8px">{home_name}</a> <a href="{home_link}privacy" style="color:#64748b;margin:0 8px">{privacy_text}</a></footer>
</body>
</html>'''

    return html

# Generate all 10 files
for tool in tools_to_create:
    slug = tool['slug']
    # CN
    os.makedirs(slug, exist_ok=True)
    cn_html = make_tool(tool, 'cn')
    with open(f'{slug}/index.html', 'w') as f:
        f.write(cn_html)
    print(f'Created {slug}/index.html ({len(cn_html)} bytes)')
    
    # EN
    os.makedirs(f'en/{slug}', exist_ok=True)
    en_html = make_tool(tool, 'en')
    with open(f'en/{slug}/index.html', 'w') as f:
        f.write(en_html)
    print(f'Created en/{slug}/index.html ({len(en_html)} bytes)')

print(f'\nDone! Created {len(tools_to_create)} tools x 2 = {len(tools_to_create)*2} pages')