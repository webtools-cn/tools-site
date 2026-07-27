#!/usr/bin/env python3
"""批量生成工具页面（中文+英文）"""
import os, json, datetime

BASE = "/home/chison/tools-site"

# 通用CSS
CSS = """*{box-sizing:border-box;margin:0;padding:0}
body{background:#0f172a;color:#e2e8f0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,"PingFang SC","Microsoft YaHei",sans-serif;line-height:1.6;min-height:100vh}
a{color:#06b6d4;text-decoration:none}
.container{max-width:960px;margin:0 auto;padding:24px 16px}
.header{display:flex;justify-content:space-between;align-items:center;margin-bottom:24px;flex-wrap:wrap;gap:12px}
.header h1{font-size:1.6rem;color:#f1f5f9}
.lang-switch{display:flex;gap:4px;background:#1e293b;border-radius:8px;padding:4px;border:1px solid rgba(148,163,184,.1)}
.lang-switch a{padding:6px 12px;border-radius:5px;font-size:.85rem;color:#94a3b8}
.lang-switch a.active{background:rgba(6,182,212,.2);color:#22d3ee}
.nav-back{color:#64748b;font-size:.85rem;margin-bottom:16px}
.nav-back a{color:#64748b}.nav-back a:hover{color:#94a3b8}
.hero{background:linear-gradient(135deg,rgba(6,182,212,.1),rgba(34,211,238,.05));border:1px solid rgba(6,182,212,.2);border-radius:12px;padding:16px 20px;margin-bottom:20px;display:flex;align-items:center;gap:12px;flex-wrap:wrap}
.hero p{color:#94a3b8;font-size:.9rem;flex:1;min-width:200px}
.badge{background:rgba(6,182,212,.15);color:#22d3ee;padding:4px 10px;border-radius:20px;font-size:.8rem;white-space:nowrap}
.input-grid{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:16px}
@media(max-width:640px){.input-grid{grid-template-columns:1fr}}
.input-group{background:#1e293b;border-radius:12px;padding:16px;border:1px solid rgba(148,163,184,.1)}
.input-group label{display:block;font-size:.9rem;color:#94a3b8;margin-bottom:8px}
.input-group input,.input-group select{width:100%;padding:10px 12px;background:#0f172a;border:1px solid rgba(148,163,184,.2);border-radius:8px;color:#e2e8f0;font-size:.95rem;transition:border-color .2s}
.input-group input:focus,.input-group select:focus{outline:none;border-color:rgba(6,182,212,.5)}
.input-group .hint{font-size:.8rem;color:#64748b;margin-top:4px}
.calculator-section{background:#1e293b;border-radius:12px;padding:20px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1)}
.calculator-section h2{font-size:1.1rem;color:#f1f5f9;margin-bottom:16px}
.btn-row{display:flex;gap:8px;flex-wrap:wrap;margin-top:16px}
.btn{padding:10px 24px;border:none;border-radius:6px;font-size:.9rem;cursor:pointer;transition:all .2s}
.btn-primary{background:rgba(6,182,212,.2);color:#22d3ee;border:1px solid rgba(6,182,212,.3)}
.btn-primary:hover{background:rgba(6,182,212,.3)}
.btn-secondary{background:rgba(148,163,184,.1);color:#94a3b8;border:1px solid rgba(148,163,184,.2)}
.btn-secondary:hover{background:rgba(148,163,184,.2)}
.results-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-bottom:16px}
@media(max-width:640px){.results-grid{grid-template-columns:1fr}}
.result-card{background:#0f172a;border:1px solid rgba(148,163,184,.15);border-radius:10px;padding:16px;text-align:center}
.result-card .label{font-size:.85rem;color:#94a3b8;margin-bottom:4px}
.result-card .value{font-size:1.4rem;color:#22d3ee;font-weight:600}
.result-card .sub{font-size:.8rem;color:#64748b;margin-top:4px}
.result-card.highlight{border-color:rgba(34,211,238,.3);background:rgba(34,211,238,.05)}
.result-card.good{border-color:rgba(34,197,94,.3);background:rgba(34,197,94,.05)}
.result-card.good .value{color:#4ade80}
.result-card.warn{border-color:rgba(251,191,36,.3);background:rgba(251,191,36,.05)}
.result-card.warn .value{color:#fbbf24}
.info-section{background:#1e293b;border-radius:12px;padding:20px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1)}
.info-section h2{font-size:1.1rem;color:#f1f5f9;margin-bottom:12px}
.info-section h3{font-size:.95rem;color:#e2e8f0;margin:16px 0 8px}
.info-section p{color:#94a3b8;font-size:.9rem;margin-bottom:8px}
.footer{border-top:1px solid rgba(148,163,184,.1);padding:24px 0;margin-top:32px;text-align:center;color:#64748b;font-size:.85rem}
.footer a{color:#64748b;margin:0 8px}.footer a:hover{color:#94a3b8}
.toast{position:fixed;bottom:20px;left:50%;transform:translateX(-50%);background:#1e293b;color:#22d3ee;padding:10px 24px;border-radius:8px;border:1px solid rgba(6,182,212,.3);font-size:.85rem;z-index:999;opacity:0;transition:opacity .3s}
.toast.show{opacity:1}
.ad-slot{margin:0 auto;text-align:center;max-width:960px}.ad-slot:not(:has(ins[frame])){display:none}.ad-slot:empty{display:none}.ad-slot ins{display:block}"""

HEAD_EXTRA = """<meta property="og:image" content="https://free-toolbase.com/og-image.svg">
<meta name="twitter:image" content="https://free-toolbase.com/og-image.svg">
<meta name="twitter:card" content="summary_large_image">
<meta name="robots" content="index, follow">
<link rel="icon" type="image/svg+xml" href="favicon.svg">
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5998441792679372" crossorigin="anonymous"></script>"""

GA_SCRIPT = """<script async src="https://www.googletagmanager.com/gtag/js?id=G-9W1157EBQV"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','G-9W1157EBQV');</script>"""

ERROR_SCRIPT = """<script>window.addEventListener("error",function(e){if(e&&e.message===""){e.preventDefault();}});window.addEventListener("unhandledrejection",function(e){if(e&&e.reason&&e.reason.message===""){e.preventDefault();}});</script>"""

TOAST_JS = """function showToast(msg){const t=document.getElementById('toast');t.textContent=msg;t.classList.add('show');setTimeout(()=>t.classList.remove('show'),2000)}"""

def gen_html(slug, cfg, lang='zh'):
    """生成单个工具的HTML"""
    is_zh = lang == 'zh'
    t = cfg['title_cn'] if is_zh else cfg['title_en']
    d = cfg['desc_cn'] if is_zh else cfg['desc_en']
    emoji = cfg.get('emoji', '🔧')
    cat = cfg.get('cat', 'UtilitiesApplication')
    
    cn_url = f"https://free-toolbase.com/{slug}/"
    en_url = f"https://free-toolbase.com/en/{slug}/"
    can_url = en_url if is_zh else en_url
    
    # SEO
    lang_html = 'zh-CN' if is_zh else 'en'
    home_label = '首页' if is_zh else 'Home'
    tools_label = '工具' if is_zh else 'Tools'
    all_tools = '全部工具' if is_zh else 'All Tools'
    about_label = '关于我们' if is_zh else 'About'
    badge_text = '零依赖 · 可离线使用' if is_zh else 'Zero-dependency · Works offline'
    input_title = '🔢 输入参数' if is_zh else '🔢 Input Parameters'
    calc_btn = '🔍 计算' if is_zh else '🔍 Calculate'
    reset_btn = '🔄 重置' if is_zh else '🔄 Reset'
    copy_btn = '📋 复制结果' if is_zh else '📋 Copy Results'
    info_title = '📖 关于此工具' if is_zh else '📖 About This Tool'
    footer_offline = '纯前端计算 · 数据不上传服务器 · 可离线使用' if is_zh else 'Client-side only · No data uploaded · Works offline'
    privacy = '隐私政策' if is_zh else 'Privacy'
    copy_ok = '✅ 已复制到剪贴板' if is_zh else '✅ Copied to clipboard'
    copy_fail = '复制失败' if is_zh else 'Copy failed'
    
    # Breadcrumb
    bc_name1 = '首页' if is_zh else 'Home'
    bc_name2 = '工具' if is_zh else 'Tools'
    bc_item1 = 'https://free-toolbase.com/' if is_zh else 'https://free-toolbase.com/en/'
    bc_item2 = 'https://free-toolbase.com/#tools' if is_zh else 'https://free-toolbase.com/en/#tools'
    bc_item3 = cn_url if is_zh else en_url
    bc_pos1 = bc_name1 if is_zh else 'Home'
    bc_pos2 = bc_name2 if is_zh else 'Tools'
    bc_pos3 = t
    
    # Schema
    schema_app = json.dumps({
        "@context": "https://schema.org", "@type": "SoftwareApplication",
        "name": t, "description": d, "applicationCategory": cat, "operatingSystem": "Web",
        "publisher": {"@type": "Organization", "name": "Free ToolBase", "email": "dexshuang@google.com"},
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}
    }, ensure_ascii=False)
    
    schema_bc = json.dumps({
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": bc_pos1, "item": bc_item1},
            {"@type": "ListItem", "position": 2, "name": bc_pos2, "item": bc_item2},
            {"@type": "ListItem", "position": 3, "name": bc_pos3, "item": bc_item3}
        ]
    }, ensure_ascii=False)
    
    op_zh = '中文' if is_zh else 'EN'
    op_en = 'EN' if is_zh else '中文'
    cn_active = 'active' if is_zh else ''
    en_active = '' if is_zh else 'active'
    
    cn_link = 'index.html' if is_zh else f'../../{slug}/'
    en_link = f'../en/{slug}/' if is_zh else 'index.html'
    
    # Generate inputs
    inputs_html = ''
    inputs_html2 = ''
    for var_name, var_cfg in cfg.get('vars', {}).items():
        label = var_cfg['label_cn'] if is_zh else var_cfg['label_en']
        default = var_cfg.get('default', '0')
        hint = var_cfg.get('hint_cn' if is_zh else 'hint_en', '')
        vtype = var_cfg.get('type', 'number')
        
        if vtype == 'select':
            options = var_cfg.get('options', '').split('|')
            opts_html = ''.join(f'<option value="{o}">{o}</option>' for o in options)
            field_html = f'<select id="{var_name}">{opts_html}</select>'
        else:
            attrs = f'type="number" id="{var_name}" value="{default}"'
            if 'min' in var_cfg: attrs += f' min="{var_cfg["min"]}"'
            if 'max' in var_cfg: attrs += f' max="{var_cfg["max"]}"'
            if 'step' in var_cfg: attrs += f' step="{var_cfg["step"]}"'
            field_html = f'<input {attrs}>'
        
        inputs_html2 += f"""    <div class="input-group"><label for="{var_name}">{label}</label>{field_html}<div class="hint">{hint}</div></div>\n"""
    
    # Generate results
    results_html = ''
    for r in cfg.get('results', []):
        lbl = r['label_cn'] if is_zh else r['label_en']
        sub = r.get('sub_cn' if is_zh else 'sub_en', '')
        hl = ' highlight' if r.get('highlight') else ''
        results_html += f'  <div class="result-card{hl}"><div class="label">{lbl}</div><div class="value" id="{r["id"]}">-</div><div class="sub">{sub}</div></div>\n'
    
    # JS vars
    js_vars = '\n'.join(f"const {vn}=document.getElementById('{vn}');" for vn in cfg.get('vars', {}))
    
    # JS default reset
    js_defaults = '\n'.join(f"{vn}.value={cfg['vars'][vn].get('default','0')};" for vn in cfg.get('vars', {}))
    
    # JS result reset
    js_reset_results = '\n'.join(f"document.getElementById('{r['id']}').textContent='-';" for r in cfg.get('results', []))
    
    # JS calc logic - from config
    js_calc = cfg.get('js_calc', '')
    js_set_results = cfg.get('js_set_results', '')
    
    # JS copy
    copy_lines = []
    for r in cfg.get('results', []):
        lbl = r['label_cn'] if is_zh else r['label_en']
        rid = r['id']
        copy_lines.append("'" + lbl + ": '+document.getElementById('" + rid + "').textContent")
    copy_str = ',\\n'.join(copy_lines)
    
    # Build JS
    js = f"""(function(){{
const $=s=>document.getElementById(s);
{js_vars}
function fmt(n){{return '$'+n.toLocaleString('en-US',{{minimumFractionDigits:2,maximumFractionDigits:2}})}}
function fmtPct(n){{return n.toFixed(1)+'%'}}
function fmtNum(n){{return n.toLocaleString('en-US',{{maximumFractionDigits:0}})}}
function calc(){{
{js_calc}
}}
function reset(){{
{js_defaults}
{js_reset_results}
}}
function copyResult(){{
const lines=[{copy_str}];
navigator.clipboard.writeText(lines.join('\\n')).then(()=>showToast('{copy_ok}')).catch(()=>showToast('{copy_fail}'))
}}
{TOAST_JS}
document.getElementById('calcBtn').addEventListener('click',calc);
document.getElementById('resetBtn').addEventListener('click',reset);
document.getElementById('copyBtn').addEventListener('click',copyResult);
calc();
}})();"""
    
    # Footer
    footer_items_cn = f'<a href="/" style="color:#64748b;margin:0 8px">首页</a> <a href="/privacy" style="color:#64748b;margin:0 8px">隐私政策</a>'
    footer_items_en = f'<a href="/en/" style="color:#64748b;margin:0 8px">Home</a> <a href="/privacy" style="color:#64748b;margin:0 8px">Privacy</a>'
    footer_items = footer_items_cn if is_zh else footer_items_en
    
    # Info section
    info_cn = cfg.get('info_cn', '')
    info_en = cfg.get('info_en', '')
    info = info_cn if is_zh else info_en
    
    # Home back link
    home_url = '../index.html' if is_zh else '../index.html'
    if not is_zh:
        cn_rel = f'../../{slug}/'
    else:
        cn_rel = 'index.html'
    
    html = f"""<!DOCTYPE html>
<html lang="{lang_html}">
<head>
{GA_SCRIPT}
{ERROR_SCRIPT}
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="{d}">
<meta name="keywords" content="{slug.replace('-', ' ')},online tool,free,calculator">
<title>{t} | Free ToolBase</title>
<link rel="canonical" href="{can_url}">
<meta property="og:title" content="{t} | Free ToolBase">
<meta property="og:description" content="{d}">
<meta property="og:url" content="{can_url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Free ToolBase">
<link rel="alternate" hreflang="zh" href="{cn_url}">
<link rel="alternate" hreflang="en" href="{en_url}">
<link rel="alternate" hreflang="x-default" href="{en_url}">
<script type="application/ld+json">{schema_app}</script>
<script type="application/ld+json">{schema_bc}</script>
<style>
{CSS}
</style>
{HEAD_EXTRA}
</head>
<body>
<div class="container">
<div class="header"><h1>{emoji} {t}</h1><div class="lang-switch"><a href="{cn_rel}" class="{cn_active}">中文</a><a href="{en_link}" class="{en_active}">EN</a></div></div>
<p class="nav-back"><a href="{home_url}">{home_label}</a> › <a href="{home_url}#tools">{tools_label}</a> › {t}</p>
<div class="hero"><p>{d}</p><span class="badge">{badge_text}</span></div>
<div class="ad-slot"><ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-5998441792679372" data-ad-slot="9876543210" data-ad-format="auto" data-full-width-responsive="true"></ins></div>
<div class="calculator-section">
  <h2>{input_title}</h2>
  <div class="input-grid">
{inputs_html2}  </div>
  <div class="btn-row">
    <button class="btn btn-primary" id="calcBtn">{calc_btn}</button>
    <button class="btn btn-secondary" id="resetBtn">{reset_btn}</button>
    <button class="btn btn-secondary" id="copyBtn">{copy_btn}</button>
  </div>
</div>
<div class="results-grid">
{results_html}</div>
{info}
<div class="footer">
  <p>© 2024 Free ToolBase · <a href="../about/">{about_label}</a> · <a href="{home_url}">{all_tools}</a></p>
  <p>{footer_offline}</p>
</div>
</div>
<div class="toast" id="toast"></div>
<script>
{js}
</script>
<footer style="border-top:1px solid rgba(148,163,184,.1);padding:24px 0;margin-top:32px;text-align:center;color:#64748b;font-size:.85rem">{footer_items}</footer>
</body>
</html>"""
    return html


# ===== 工具定义 =====
TOOLS = {
    "401k-match-calculator": {
        "title_cn": "401k雇主匹配计算器",
        "title_en": "401k Employer Match Calculator",
        "desc_cn": "免费在线401k雇主匹配计算器，精确计算不同匹配方案下的雇主贡献金额。支持100%匹配、50%匹配、阶梯式匹配等多种方案。纯前端计算，帮助您最大化退休福利。",
        "desc_en": "Free online 401k Employer Match Calculator. Calculate employer contributions under various matching formulas. Supports 100% match, 50% match, tiered matching, and more. Maximize your retirement benefits.",
        "emoji": "🏢", "cat": "FinanceApplication",
        "vars": {
            "annualSalary": {"label_cn": "年薪 ($)", "label_en": "Annual Salary ($)", "default": "80000", "min": "0", "step": "1000", "hint_cn": "您的税前年薪", "hint_en": "Your pre-tax annual salary"},
            "contributePct": {"label_cn": "个人贡献比例 (%)", "label_en": "Your Contribution (%)", "default": "6", "min": "0", "max": "100", "step": "0.1", "hint_cn": "您计划存入401k的工资百分比", "hint_en": "Percentage of salary you'll contribute"},
            "matchPattern": {"label_cn": "雇主匹配方案", "label_en": "Employer Match Formula", "type": "select", "options": "100% on first 3%|50% on first 6%|100% on first 4%, 50% on next 4%|100% on first 5%|50% on first 8%|Dollar-for-dollar up to 4%", "default": "50% on first 6%"},
            "matchCap": {"label_cn": "匹配金额上限 ($)", "label_en": "Match Dollar Cap ($)", "default": "0", "min": "0", "step": "100", "hint_cn": "0 = 无上限；部分雇主设定年度匹配上限", "hint_en": "0 = no cap; some employers cap total match"}
        },
        "results": [
            {"id": "empMatch", "label_cn": "🏢 雇主年匹配金额", "label_en": "🏢 Annual Employer Match", "highlight": True, "sub_cn": "雇主为您存的钱", "sub_en": "Free money from your employer"},
            {"id": "yourContrib", "label_cn": "👤 个人年贡献", "label_en": "👤 Your Annual Contribution", "sub_cn": "您自己存入的金额", "sub_en": "Your own contribution"},
            {"id": "totalAnnual", "label_cn": "📊 年度总贡献", "label_en": "📊 Total Annual Contribution", "sub_cn": "个人+雇主合计", "sub_en": "Your contributions + employer match"},
            {"id": "effectiveMatch", "label_cn": "📈 有效匹配率", "label_en": "📈 Effective Match Rate", "sub_cn": "雇主匹配占年薪百分比", "sub_en": "Match as % of salary"},
            {"id": "freeMoney10yr", "label_cn": "💰 10年累计匹配（含收益）", "label_en": "💰 10-Year Match (with growth)", "sub_cn": "含7%年化复利", "sub_en": "With 7% compound growth"},
            {"id": "freeMoney30yr", "label_cn": "🏦 30年累计匹配（含收益）", "label_en": "🏦 30-Year Match (with growth)", "sub_cn": "含7%年化复利", "sub_en": "With 7% compound growth"}
        ],
        "js_calc": """const salary=+annualSalary.value,myPct=+contributePct.value/100,
pat=matchPattern.value,cap=+matchCap.value||1e9,ret=0.07;
let match=0;
const myContrib=Math.min(salary*myPct,23000);
if(pat==='100% on first 3%') match=Math.min(salary*0.03,myContrib);
else if(pat==='50% on first 6%') match=Math.min(salary*0.03,myContrib*0.5);
else if(pat==='100% on first 4%, 50% on next 4%') match=Math.min(salary*0.04,myContrib)+Math.min(salary*0.04,Math.max(0,myContrib-salary*0.04))*0.5;
else if(pat==='100% on first 5%') match=Math.min(salary*0.05,myContrib);
else if(pat==='50% on first 8%') match=Math.min(salary*0.04,myContrib*0.5);
else if(pat==='Dollar-for-dollar up to 4%') match=Math.min(salary*0.04,myContrib);
match=Math.min(match,cap);
const total=match+myContrib;
const effMatch=match/salary*100;
let fv10=0,fv30=0;
for(let i=0;i<10;i++){fv10+=match;fv10*=(1+ret)}
for(let i=0;i<30;i++){fv30+=match;fv30*=(1+ret)}
document.getElementById('empMatch').textContent=fmt(match);
document.getElementById('yourContrib').textContent=fmt(myContrib);
document.getElementById('totalAnnual').textContent=fmt(total);
document.getElementById('effectiveMatch').textContent=fmtPct(effMatch);
document.getElementById('freeMoney10yr').textContent=fmt(fv10);
document.getElementById('freeMoney30yr').textContent=fmt(fv30);""",
        "info_cn": """<div class="info-section">
  <h2>📖 关于401k雇主匹配</h2>
  <h3>什么是雇主匹配？</h3>
  <p>雇主匹配（Employer Match）是公司为鼓励员工储蓄退休金而提供的福利。公司按照员工贡献的一定比例额外向401k账户存入资金，这笔钱是"免费"的额外薪酬。</p>
  <h3>常见匹配方案</h3>
  <p>50%匹配前6%：员工存6%，公司给3%。100%匹配前3-5%：员工存3%，公司给3%。阶梯式：如前4%按100%匹配，后4%按50%匹配。</p>
  <h3>为什么不要错过匹配？</h3>
  <p>雇主匹配相当于即时100%以上的回报。如果公司匹配50%（存$1得$0.5），实际回报率为50%。建议至少存够获得全额匹配的金额。</p>
</div>""",
        "info_en": """<div class="info-section">
  <h2>📖 About 401k Employer Match</h2>
  <h3>What is Employer Match?</h3>
  <p>Employer match is a benefit companies offer to encourage retirement saving. The company contributes additional money to your 401k based on your own contributions — essentially free extra compensation.</p>
  <h3>Common Match Formulas</h3>
  <p>50% match on first 6%: you save 6%, company adds 3%. 100% match on first 3-5%. Tiered: e.g. 100% on first 4%, then 50% on next 4%.</p>
  <h3>Never Leave Free Money on the Table</h3>
  <p>Employer match is an immediate 50-100% return. Contribute at least enough to get the full match — it's the best guaranteed return you'll ever get.</p>
</div>"""
    },
    
    "monthly-payment-calculator": {
        "title_cn": "月供计算器",
        "title_en": "Monthly Payment Calculator",
        "desc_cn": "免费在线月供计算器，快速计算房贷、车贷、个人贷款每月还款额。支持等额本息和等额本金两种还款方式，生成完整还款对比。纯前端计算，数据不上传服务器。",
        "desc_en": "Free online Monthly Payment Calculator. Quickly calculate monthly payments for mortgages, auto loans, and personal loans. Supports amortized and equal principal methods with full payment comparison.",
        "emoji": "💳", "cat": "FinanceApplication",
        "vars": {
            "loanAmount": {"label_cn": "贷款金额 ($)", "label_en": "Loan Amount ($)", "default": "300000", "min": "0", "step": "1000", "hint_cn": "您计划借贷的总金额", "hint_en": "Total amount you plan to borrow"},
            "interestRate": {"label_cn": "年利率 (%)", "label_en": "Annual Interest Rate (%)", "default": "6.5", "min": "0", "max": "50", "step": "0.01", "hint_cn": "贷款年化利率", "hint_en": "Annual interest rate"},
            "loanTerm": {"label_cn": "贷款期限 (年)", "label_en": "Loan Term (Years)", "default": "30", "min": "1", "max": "50", "step": "1", "hint_cn": "还款总年限", "hint_en": "Total repayment period"},
            "paymentType": {"label_cn": "还款方式", "label_en": "Payment Method", "type": "select", "options": "等额本息|等额本金", "default": "等额本息"}
        },
        "results": [
            {"id": "monthlyPayment", "label_cn": "💵 月供金额", "label_en": "💵 Monthly Payment", "highlight": True, "sub_cn": "每月需要还款的金额", "sub_en": "Amount due each month"},
            {"id": "totalPayment", "label_cn": "📊 总还款额", "label_en": "📊 Total Payment", "sub_cn": "本金+利息总额", "sub_en": "Principal + interest total"},
            {"id": "totalInterest", "label_cn": "📈 总利息", "label_en": "📈 Total Interest", "sub_cn": "贷款期限内支付的利息", "sub_en": "Interest paid over loan life"},
            {"id": "interestRatio", "label_cn": "📉 利息占比", "label_en": "📉 Interest Ratio", "sub_cn": "利息占总支出的比例", "sub_en": "Interest as % of total cost"},
            {"id": "firstMonthPrincipal", "label_cn": "🏠 首月本金", "label_en": "🏠 First Month Principal", "sub_cn": "首月还款中本金部分", "sub_en": "Principal portion in first payment"},
            {"id": "lastMonthInterest", "label_cn": "📅 末月利息", "label_en": "📅 Last Month Interest", "sub_cn": "最后一个月利息", "sub_en": "Interest in final payment"}
        ],
        "js_calc": """const amount=+loanAmount.value,rate=+interestRate.value/100/12,
months=+loanTerm.value*12,type=paymentType.value;
let monthly,totalInterest,totalPayment,firstPrin,lastInt;
if(type==='等额本息'){
if(rate===0){monthly=amount/months;totalInterest=0}
else{monthly=amount*(rate*Math.pow(1+rate,months))/(Math.pow(1+rate,months)-1)}
totalPayment=monthly*months;
totalInterest=totalPayment-amount;
firstPrin=monthly-amount*rate;
lastInt=monthly*(1-Math.pow(1+rate,-1))/rate*rate;
}else{
let remaining=amount,firstPmt=amount/months;
totalInterest=0;
for(let i=0;i<months;i++){totalInterest+=remaining*rate;remaining-=firstPmt}
totalPayment=amount+totalInterest;
monthly=totalPayment/months;
firstPrin=amount/months;
lastInt=(amount/months)*rate;
}
const interestRatio=totalPayment>0?totalInterest/totalPayment*100:0;
document.getElementById('monthlyPayment').textContent=fmt(monthly);
document.getElementById('totalPayment').textContent=fmt(totalPayment);
document.getElementById('totalInterest').textContent=fmt(totalInterest);
document.getElementById('interestRatio').textContent=fmtPct(interestRatio);
document.getElementById('firstMonthPrincipal').textContent=fmt(firstPrin);
document.getElementById('lastMonthInterest').textContent=fmt(lastInt);""",
        "info_cn": """<div class="info-section">
  <h2>📖 关于月供计算</h2>
  <h3>等额本息 vs 等额本金</h3>
  <p>等额本息：每月还款额固定，前期利息占比高，后期本金占比高。适合收入稳定、希望月供不变的借款人。</p>
  <p>等额本金：每月还本金固定，利息逐月递减，总利息更少。适合前期还款能力强的借款人。</p>
  <h3>如何减少利息支出？</h3>
  <p>1）缩短贷款期限；2）提高首付比例；3）选择等额本金；4）提前还款或双周还款。</p>
</div>""",
        "info_en": """<div class="info-section">
  <h2>📖 About Monthly Payments</h2>
  <h3>Amortized vs Equal Principal</h3>
  <p>Amortized: fixed monthly payment, higher interest initially. Equal Principal: fixed principal payment, decreasing total. Equal principal saves more interest overall.</p>
  <h3>How to Reduce Interest?</h3>
  <p>1) Shorter loan term; 2) Larger down payment; 3) Choose equal principal; 4) Extra or bi-weekly payments.</p>
</div>"""
    },
    
    "safe-withdrawal-rate": {
        "title_cn": "安全提款率计算器",
        "title_en": "Safe Withdrawal Rate Calculator",
        "desc_cn": "免费在线安全提款率(SWR)计算器，基于4%规则和Trinity Study研究。计算退休后每年可安全提取多少资金，支持通胀调整和资金可持续性分析。纯前端计算，数据不上传。",
        "desc_en": "Free online Safe Withdrawal Rate (SWR) Calculator based on the 4% rule and Trinity Study. Calculate safe annual withdrawals with inflation adjustment and portfolio sustainability analysis.",
        "emoji": "🛡️", "cat": "FinanceApplication",
        "vars": {
            "portfolioValue": {"label_cn": "退休资产总额 ($)", "label_en": "Retirement Portfolio ($)", "default": "1000000", "min": "0", "step": "10000", "hint_cn": "退休时所有投资账户总额", "hint_en": "Total value of retirement accounts"},
            "withdrawalRate": {"label_cn": "初始提款率 (%)", "label_en": "Initial Withdrawal Rate (%)", "default": "4", "min": "1", "max": "10", "step": "0.1", "hint_cn": "经典4%规则；3%保守，5%激进", "hint_en": "Classic 4% rule; 3% conservative, 5% aggressive"},
            "retireYears": {"label_cn": "预期退休年限", "label_en": "Expected Retirement Years", "default": "30", "min": "5", "max": "60", "step": "1", "hint_cn": "通常30年（65-95岁）", "hint_en": "Typically 30 years (65-95)"},
            "annualReturn": {"label_cn": "预期年回报率 (%)", "label_en": "Expected Annual Return (%)", "default": "7", "min": "0", "max": "20", "step": "0.1", "hint_cn": "标普500长期约7%", "hint_en": "S&P 500 long-term ~7%"},
            "inflationRate": {"label_cn": "预期通胀率 (%)", "label_en": "Expected Inflation (%)", "default": "3", "min": "0", "max": "10", "step": "0.1", "hint_cn": "长期平均通胀约3%", "hint_en": "Long-term average ~3%"}
        },
        "results": [
            {"id": "annualWithdrawal", "label_cn": "💰 首年提款金额", "label_en": "💰 Year 1 Withdrawal", "highlight": True, "sub_cn": "按初始提款率计算", "sub_en": "Based on initial SWR"},
            {"id": "monthlyWithdrawal", "label_cn": "📅 每月可用金额", "label_en": "📅 Monthly Available", "sub_cn": "年度金额÷12", "sub_en": "Annual ÷ 12"},
            {"id": "totalWithdrawn", "label_cn": "📊 总提款额", "label_en": "📊 Total Withdrawn", "sub_cn": "退休期间累计提款", "sub_en": "Cumulative withdrawals"},
            {"id": "endingBalance", "label_cn": "🏦 期末余额", "label_en": "🏦 Ending Balance", "sub_cn": "退休期末估计剩余", "sub_en": "Estimated remaining at end"},
            {"id": "sustainability", "label_cn": "✅ 资金可持续性", "label_en": "✅ Sustainability", "sub_cn": "资金是否会耗尽", "sub_en": "Will funds last?"},
            {"id": "exhaustionYear", "label_cn": "⚠️ 耗尽年份", "label_en": "⚠️ Exhaustion Year", "sub_cn": "资金可能耗尽的年份", "sub_en": "Year funds may run out"}
        ],
        "js_calc": """const pv=+portfolioValue.value,wr=+withdrawalRate.value/100,
years=+retireYears.value,ret=+annualReturn.value/100,infl=+inflationRate.value/100;
let withdrawal=pv*wr,balance=pv,totalWithdrawn=0,exhaustionYear=-1;
for(let y=0;y<years;y++){
let w=withdrawal*Math.pow(1+infl,y);
if(balance<=0){if(exhaustionYear<0)exhaustionYear=y+1;w=0}
balance-=w;totalWithdrawn+=w;
balance=Math.max(0,balance*(1+ret));
}
let sustainability,cardClass;
if(balance>pv*0.5){sustainability='✅ 非常安全';cardClass='good'}
else if(balance>0){sustainability='✅ 安全';cardClass=''}
else if(balance===0&&exhaustionYear<0){sustainability='⚠️ 刚好用尽';cardClass='warn'}
else{sustainability='❌ 可能耗尽';cardClass='warn'}
document.getElementById('annualWithdrawal').textContent=fmt(withdrawal);
document.getElementById('monthlyWithdrawal').textContent=fmt(withdrawal/12);
document.getElementById('totalWithdrawn').textContent=fmt(totalWithdrawn);
document.getElementById('endingBalance').textContent=fmt(balance);
document.getElementById('sustainability').textContent=sustainability;
document.getElementById('exhaustionYear').textContent=exhaustionYear>0?'第'+exhaustionYear+'年':'N/A';""",
        "info_cn": """<div class="info-section">
  <h2>📖 关于安全提款率</h2>
  <h3>4%规则历史</h3>
  <p>4%规则源于1994年Bill Bengen的研究和1998年Trinity Study。研究表明：退休第一年提取资产的4%，之后按通胀调整，在30年退休期内有约95%的概率不会耗尽资金。</p>
  <h3>现代调整</h3>
  <p>部分专家建议使用3-3.5%更保守的提款率，考虑当前低利率环境和更长寿命预期。本计算器支持自定义提款率和参数。</p>
</div>""",
        "info_en": """<div class="info-section">
  <h2>📖 About Safe Withdrawal Rates</h2>
  <h3>The 4% Rule</h3>
  <p>Originating from Bill Bengen (1994) and the Trinity Study (1998): withdrawing 4% of portfolio in year 1, adjusted for inflation thereafter, has ~95% success rate over 30 years.</p>
  <h3>Modern Adjustments</h3>
  <p>Some experts recommend 3-3.5% for extra safety given longer life expectancies. This calculator lets you test any withdrawal rate.</p>
</div>"""
    },
    
    "fire-simulator": {
        "title_cn": "FIRE财务自由模拟器",
        "title_en": "FIRE Financial Independence Simulator",
        "desc_cn": "免费在线FIRE（财务独立提早退休）模拟器。输入收入、支出和储蓄率，计算达到财务独立所需的年限和资产目标。支持多种FIRE变体：Lean FIRE、Fat FIRE、Coast FIRE和Barista FIRE。纯前端计算。",
        "desc_en": "Free online FIRE (Financial Independence, Retire Early) Simulator. Input income, expenses & savings rate to calculate years to FI and target portfolio. Supports Lean FIRE, Fat FIRE, Coast FIRE & Barista FIRE variants.",
        "emoji": "🔥", "cat": "FinanceApplication",
        "vars": {
            "annualIncome": {"label_cn": "年收入（税后）($)", "label_en": "Annual Income (after tax) ($)", "default": "100000", "min": "0", "step": "1000", "hint_cn": "家庭年度税后总收入", "hint_en": "Annual after-tax household income"},
            "annualExpenses": {"label_cn": "年支出 ($)", "label_en": "Annual Expenses ($)", "default": "50000", "min": "0", "step": "1000", "hint_cn": "当前年度总支出", "hint_en": "Current total annual expenses"},
            "currentSavings": {"label_cn": "已有储蓄/投资 ($)", "label_en": "Current Savings ($)", "default": "100000", "min": "0", "step": "1000", "hint_cn": "已有投资账户总额", "hint_en": "Current investment portfolio"},
            "annualReturn": {"label_cn": "预期年回报率 (%)", "label_en": "Expected Annual Return (%)", "default": "7", "min": "0", "max": "20", "step": "0.1", "hint_cn": "标普500长期约7%", "hint_en": "S&P 500 real return ~7%"},
            "swr": {"label_cn": "安全提款率 (%)", "label_en": "Safe Withdrawal Rate (%)", "default": "4", "min": "2", "max": "8", "step": "0.1", "hint_cn": "退休后可安全提取的比例", "hint_en": "Safe withdrawal rate in retirement"},
            "fireType": {"label_cn": "FIRE类型", "label_en": "FIRE Type", "type": "select", "options": "Standard FIRE|Lean FIRE (支出×0.7)|Fat FIRE (支出×1.5)|Barista FIRE (半退休)|Coast FIRE (不再存钱)", "default": "Standard FIRE"}
        },
        "results": [
            {"id": "savingsRate", "label_cn": "📊 储蓄率", "label_en": "📊 Savings Rate", "highlight": True, "sub_cn": "年储蓄占收入比例", "sub_en": "Annual savings as % of income"},
            {"id": "fiNumber", "label_cn": "🎯 FI目标金额", "label_en": "🎯 FI Target Number", "sub_cn": "财务独立所需资产", "sub_en": "Portfolio needed for FI"},
            {"id": "yearsToFI", "label_cn": "⏱️ 达到FI年限", "label_en": "⏱️ Years to FI", "sub_cn": "按当前储蓄率估算", "sub_en": "Estimated with current savings rate"},
            {"id": "fireAge", "label_cn": "🎂 FI退休年龄", "label_en": "🎂 FI Retirement Age", "sub_cn": "假设25岁开始", "sub_en": "Assuming starting at 25"},
            {"id": "annualSavings", "label_cn": "💰 年储蓄金额", "label_en": "💰 Annual Savings", "sub_cn": "收入-支出", "sub_en": "Income minus expenses"},
            {"id": "fiProgress", "label_cn": "📈 FI进度", "label_en": "📈 FI Progress", "sub_cn": "已有资产/目标资产", "sub_en": "Current portfolio / FI target"}
        ],
        "js_calc": """const income=+annualIncome.value,exp=+annualExpenses.value,
sav=+currentSavings.value,ret=+annualReturn.value/100,swr=+swr.value/100,
ft=fireType.value;
let annualSave=income-exp;
let targetExp=exp;
if(ft==='Lean FIRE (支出×0.7)') targetExp=exp*0.7;
else if(ft==='Fat FIRE (支出×1.5)') targetExp=exp*1.5;
else if(ft==='Barista FIRE (半退休)') targetExp=exp*0.5;
else if(ft==='Coast FIRE (不再存钱)'){annualSave=0}
const fiNumber=targetExp/swr;
let years=0,portfolio=sav;
if(annualSave>0&&portfolio<fiNumber){
const r=1+ret;
years=Math.ceil(Math.log((fiNumber*r-annualSave)/(portfolio*r-annualSave))/Math.log(r));
}
if(annualSave<=0&&portfolio<fiNumber){years=Math.ceil(Math.log(fiNumber/portfolio)/Math.log(1+ret))}
const svRate=income>0?annualSave/income*100:0;
const fireAge=25+years;
const progress=fiNumber>0?sav/fiNumber*100:0;
document.getElementById('savingsRate').textContent=fmtPct(svRate);
document.getElementById('fiNumber').textContent=fmt(fiNumber);
document.getElementById('yearsToFI').textContent=years>0?years+' 年':'已经达到FI!';
document.getElementById('fireAge').textContent=fireAge+' 岁';
document.getElementById('annualSavings').textContent=fmt(annualSave);
document.getElementById('fiProgress').textContent=fmtPct(Math.min(100,progress));""",
        "info_cn": """<div class="info-section">
  <h2>📖 关于FIRE运动</h2>
  <h3>什么是FIRE？</h3>
  <p>FIRE = Financial Independence, Retire Early（财务独立，提早退休）。核心思想：通过高储蓄率（50%+）和低成本指数投资，在传统退休年龄之前积累25倍年支出的资产。</p>
  <h3>FIRE变体</h3>
  <p>Lean FIRE：极简退休（年支出<35000）。Fat FIRE：富裕退休。Barista FIRE：半退休+兼职收入。Coast FIRE：资产已够，无需再存。</p>
</div>""",
        "info_en": """<div class="info-section">
  <h2>📖 About the FIRE Movement</h2>
  <h3>What is FIRE?</h3>
  <p>Financial Independence, Retire Early. Core principle: save 50%+ of income, invest in low-cost index funds, accumulate 25x annual expenses for retirement.</p>
  <h3>FIRE Variants</h3>
  <p>Lean FIRE: minimalist retirement. Fat FIRE: affluent retirement. Barista FIRE: semi-retired with part-time work. Coast FIRE: enough saved, no need to contribute more.</p>
</div>"""
    }
}


def main():
    count = 0
    for slug, cfg in TOOLS.items():
        # 中文版
        html_cn = gen_html(slug, cfg, 'zh')
        path_cn = os.path.join(BASE, slug, 'index.html')
        os.makedirs(os.path.dirname(path_cn), exist_ok=True)
        with open(path_cn, 'w', encoding='utf-8') as f:
            f.write(html_cn)
        
        # 英文版
        html_en = gen_html(slug, cfg, 'en')
        path_en = os.path.join(BASE, 'en', slug, 'index.html')
        os.makedirs(os.path.dirname(path_en), exist_ok=True)
        with open(path_en, 'w', encoding='utf-8') as f:
            f.write(html_en)
        
        count += 1
        print(f"✅ {slug} (中文+英文)")
    
    print(f"\n🎉 成功生成 {count} 个工具（{count*2} 个页面）")

if __name__ == '__main__':
    main()
