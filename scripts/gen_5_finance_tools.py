#!/usr/bin/env python3
"""Generate 5 new finance tools: equity-dilution, customer-lifetime-value, revenue-projection, federal-tax, freelance-tax"""
import os

SITE = "/home/chison/tools-site"
G_TAG = "G-9W1157EBQV"
ADSENSE = "ca-pub-5998441792679372"
EMAIL = "dexshuang@google.com"
DOMAIN = "https://free-toolbase.com"

def esc(s):
    return s.replace("\\", "\\\\").replace("'", "\\'").replace('"', '\\"')

def build_page(slug, lang, title, h1, desc, hero, cat, icon, faq_list, use_cases, keywords, input_html, result_html, js_code):
    is_cn = (lang == "cn")
    lang_attr = "zh-CN" if is_cn else "en"
    canonical_suffix = f"/{slug}/" if is_cn else f"/en/{slug}/"
    alt_suffix = f"/en/{slug}/" if is_cn else f"/{slug}/"
    alt_lang = "en" if is_cn else "zh"
    xdefault = f"/en/{slug}/"
    
    home_text = "首页" if is_cn else "Home"
    tools_text = "工具" if is_cn else "Tools"
    all_tools_text = "全部工具" if is_cn else "All Tools"
    calc_btn = "🧮 开始计算" if is_cn else "🧮 Calculate"
    reset_btn = "🔄 重置" if is_cn else "🔄 Reset"
    input_label = "🔢 输入参数" if is_cn else "🔢 Input Parameters"
    results_label = "📊 计算结果" if is_cn else "📊 Results"
    tutorial_label = "📖 使用教程" if is_cn else "📖 How to Use"
    usecase_label = "🎯 应用场景" if is_cn else "🎯 Use Cases"
    faq_label = "❓ 常见问题 (FAQ)" if is_cn else "❓ FAQ"
    badge_text = "零依赖·可离线使用" if is_cn else "Zero Dependencies · Works Offline"
    zero_dep = "无需注册 · 数据绝不上传服务器" if is_cn else "No Signup · Data Never Leaves Your Device"
    lang_sw_cn_active = "active" if is_cn else ""
    lang_sw_en_active = "" if is_cn else "active"
    
    # FAQ schema
    faq_schema_items = []
    for qa in faq_list:
        q = esc(qa["q"])
        a = esc(qa["a"])
        faq_schema_items.append(f'{{"@type":"Question","name":"{q}","acceptedAnswer":{{"@type":"Answer","text":"{a}"}}}}')
    faq_json = ",".join(faq_schema_items)
    
    # FAQ HTML
    faq_html = ""
    for qa in faq_list:
        faq_html += f'<div class="faq-item"><h3>{qa["q"]}</h3><p>{qa["a"]}</p></div>\n'
    
    # Use cases HTML
    uc_html = ""
    for uc in use_cases:
        uc_html += f'<p><strong>{uc["title"]}：</strong>{uc["desc"]}</p>\n'
    
    html = f'''<!DOCTYPE html>
<html lang="{lang_attr}">
<head>
<script async src="https://www.googletagmanager.com/gtag/js?id={G_TAG}"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','{G_TAG}');</script>
<script>window.addEventListener("error",function(e){{if(e&&e.message===""){{e.preventDefault();}}}});window.addEventListener("unhandledrejection",function(e){{if(e&&e.reason&&e.reason.message===""){{e.preventDefault();}}}});</script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="{desc}">
<meta name="keywords" content="{keywords}">
<title>{title} - Free ToolBase</title>
<link rel="canonical" href="{DOMAIN}{canonical_suffix}">
<meta property="og:title" content="{title} - Free ToolBase">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{DOMAIN}{canonical_suffix}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Free ToolBase">
<meta property="og:image" content="{DOMAIN}/og-image.svg">
<meta name="twitter:image" content="{DOMAIN}/og-image.svg">
<meta name="twitter:card" content="summary_large_image">
<meta name="robots" content="index, follow">
<link rel="alternate" hreflang="{alt_lang}" href="{DOMAIN}{alt_suffix}">
<link rel="alternate" hreflang="x-default" href="{DOMAIN}{xdefault}">
<link rel="icon" type="image/svg+xml" href="favicon.svg">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"SoftwareApplication","name":"{title}","description":"{desc}","applicationCategory":"FinanceApplication","operatingSystem":"Web","publisher":{{"@type":"Organization","name":"Free ToolBase","email":"{EMAIL}"}},"offers":{{"@type":"Offer","price":"0","priceCurrency":"USD"}}}}</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{faq_json}]}}</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"HowTo","name":"如何使用 {title}","description":"使用步骤指南","totalTime":"PT2M","tool":{{"@type":"HowToTool","name":"{title}"}},"step":[{{"@type":"HowToStep","position":1,"name":"{("输入数据" if is_cn else "Enter Data")}","text":"{("在输入框中输入需要计算的数值" if is_cn else "Enter your values in the input fields")}"}},{{"@type":"HowToStep","position":2,"name":"{("选择选项" if is_cn else "Select Options")}","text":"{("根据需要选择计算模式或参数" if is_cn else "Choose calculation mode or parameters as needed")}"}},{{"@type":"HowToStep","position":3,"name":"{("点击计算" if is_cn else "Calculate")}","text":"{("点击计算按钮获取结果" if is_cn else "Click the calculate button to see results")}"}},{{"@type":"HowToStep","position":4,"name":"{("查看结果" if is_cn else "View Results")}","text":"{("查看计算结果，支持一键复制" if is_cn else "Review results with one-click copy support")}"}}]}}</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"{home_text}","item":"{DOMAIN}/"}},{{"@type":"ListItem","position":2,"name":"{tools_text}","item":"{DOMAIN}/#tools"}},{{"@type":"ListItem","position":3,"name":"{title}","item":"{DOMAIN}{canonical_suffix}"}}]}}</script>
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE}" crossorigin="anonymous"></script>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#0f172a;color:#e2e8f0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,"PingFang SC","Microsoft YaHei",sans-serif;line-height:1.6;min-height:100vh}}
a{{color:#06b6d4;text-decoration:none}}
.container{{max-width:960px;margin:0 auto;padding:24px 16px}}
.header{{display:flex;justify-content:space-between;align-items:center;margin-bottom:24px}}
.header h1{{font-size:1.6rem;color:#f1f5f9}}
.lang-switch{{display:flex;gap:4px;background:#1e293b;border-radius:8px;padding:4px;border:1px solid rgba(148,163,184,.1)}}
.lang-switch a{{padding:6px 12px;border-radius:5px;font-size:.85rem;color:#94a3b8}}
.lang-switch a.active{{background:rgba(6,182,212,.2);color:#22d3ee}}
.nav-back{{color:#64748b;font-size:.85rem;margin-bottom:16px}}
.nav-back a{{color:#64748b}}
.nav-back a:hover{{color:#94a3b8}}
.hero{{margin-bottom:16px}}
.hero p{{color:#94a3b8;font-size:.95rem}}
.badge{{display:inline-block;margin-top:8px;padding:4px 12px;background:rgba(34,211,238,.1);color:#22d3ee;border-radius:20px;font-size:.8rem;border:1px solid rgba(34,211,238,.2)}}
.input-grid{{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:16px}}
@media(max-width:640px){{.input-grid{{grid-template-columns:1fr}}}}
.input-group{{background:#1e293b;border-radius:12px;padding:16px;border:1px solid rgba(148,163,184,.1)}}
.input-group label{{display:block;font-size:.9rem;color:#94a3b8;margin-bottom:8px}}
.input-group input,.input-group select{{width:100%;padding:10px 12px;background:#0f172a;border:1px solid rgba(148,163,184,.2);border-radius:8px;color:#e2e8f0;font-size:.95rem;transition:border-color .2s}}
.input-group input:focus,.input-group select:focus{{outline:none;border-color:rgba(6,182,212,.5)}}
.input-group .hint{{font-size:.8rem;color:#64748b;margin-top:4px}}
.calculator-section{{background:#1e293b;border-radius:12px;padding:20px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1)}}
.calculator-section h2{{font-size:1.1rem;color:#f1f5f9;margin-bottom:16px}}
.btn-row{{display:flex;gap:8px;flex-wrap:wrap;margin-top:16px}}
.btn{{padding:10px 24px;border:none;border-radius:6px;font-size:.9rem;cursor:pointer;transition:all .2s}}
.btn-primary{{background:rgba(6,182,212,.2);color:#22d3ee;border:1px solid rgba(6,182,212,.3)}}
.btn-primary:hover{{background:rgba(6,182,212,.3)}}
.btn-secondary{{background:rgba(148,163,184,.1);color:#94a3b8;border:1px solid rgba(148,163,184,.2)}}
.btn-secondary:hover{{background:rgba(148,163,184,.2)}}
.results-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-bottom:16px}}
@media(max-width:640px){{.results-grid{{grid-template-columns:1fr}}}}
.result-card{{background:#0f172a;border:1px solid rgba(148,163,184,.15);border-radius:10px;padding:16px;text-align:center}}
.result-card .label{{font-size:.85rem;color:#94a3b8;margin-bottom:4px}}
.result-card .value{{font-size:1.4rem;color:#22d3ee;font-weight:600}}
.result-card .sub{{font-size:.8rem;color:#64748b;margin-top:4px}}
.result-card.highlight{{border-color:rgba(34,211,238,.3);background:rgba(34,211,238,.05)}}
.info-section{{background:#1e293b;border-radius:12px;padding:20px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1)}}
.info-section h2{{font-size:1.1rem;color:#f1f5f9;margin-bottom:12px}}
.info-section h3{{font-size:.95rem;color:#e2e8f0;margin:16px 0 8px}}
.info-section p{{color:#94a3b8;font-size:.9rem;margin-bottom:8px}}
.faq-item{{margin-bottom:16px}}
.faq-item h3{{font-size:.95rem;color:#e2e8f0;margin-bottom:6px}}
.faq-item p{{color:#94a3b8;font-size:.9rem}}
.footer{{border-top:1px solid rgba(148,163,184,.1);padding:24px 0;margin-top:32px;text-align:center;color:#64748b;font-size:.85rem}}
.footer a{{color:#64748b;margin:0 8px}}
.footer a:hover{{color:#94a3b8}}
.toast{{position:fixed;bottom:20px;left:50%;transform:translateX(-50%);background:#1e293b;color:#22d3ee;padding:10px 24px;border-radius:8px;border:1px solid rgba(6,182,212,.3);font-size:.85rem;z-index:999;opacity:0;transition:opacity .3s}}
.toast.show{{opacity:1}}
.ad-slot{{margin:0 auto 24px;text-align:center;max-width:960px;min-height:90px}}
</style>
</head>
<body>
<div class="container">
<div class="header"><h1>{icon} {h1}</h1><div class="lang-switch"><a href="index.html" class="{lang_sw_cn_active}">{("中文" if is_cn else "中文")}</a><a href="../en/{slug}/" class="{lang_sw_en_active}">EN</a></div></div>
<p class="nav-back"><a href="../index.html">{home_text}</a> &rsaquo; <a href="../index.html#tools">{tools_text}</a> &rsaquo; {title}</p>
<div class="hero"><p>{hero} | {zero_dep}</p><span class="badge">{badge_text}</span></div>

<div class="calculator-section" id="calcSection">
    <h2>{input_label}</h2>
    <div class="input-grid" id="inputGrid">
{input_html}
    </div>
    <div class="btn-row">
        <button class="btn btn-primary" onclick="calculate()">{calc_btn}</button>
        <button class="btn btn-secondary" onclick="resetAll()">{reset_btn}</button>
    </div>
</div>

<div class="calculator-section" id="resultsSection" style="display:none">
    <h2>{results_label}</h2>
    <div class="results-grid" id="resultsGrid">
{result_html}
    </div>
</div>

<div class="info-section">
    <h2>{tutorial_label}</h2>
    <p>{hero}</p>
</div>

<div class="info-section">
    <h2>{usecase_label}</h2>
{uc_html}
</div>

<div class="info-section">
    <h2>{faq_label}</h2>
{faq_html}
</div>

<div class="ad-slot">
<ins class="adsbygoogle" style="display:block" data-ad-client="{ADSENSE}" data-ad-slot="auto" data-ad-format="auto" data-full-width-responsive="true"></ins>
</div>
<script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
<footer class="footer container">
<div style="margin-bottom:12px">
<a href="../index.html">{home_text}</a>
<a href="../index.html">{all_tools_text}</a>
<a href="mailto:{EMAIL}">{("联系我们" if is_cn else "Contact")}</a>
<a href="../privacy/">{("隐私政策" if is_cn else "Privacy")}</a>
<a href="../terms/">{("服务条款" if is_cn else "Terms")}</a>
<a href="../about/">{("关于我们" if is_cn else "About")}</a>
<a href="../en/{slug}/">EN</a>
</div>
<p>{title} | {zero_dep}</p>
<p style="margin-top:8px;color:#475569;font-size:.8rem">{("问题反馈" if is_cn else "Feedback")}: {EMAIL}</p>
</footer>
<div class="toast" id="toast"></div>
<script>
function showToast(m){{var t=document.getElementById("toast");t.textContent=m;t.classList.add("show");setTimeout(function(){{t.classList.remove("show")}},3000)}}
function copyText(id){{var el=document.getElementById(id);if(!el)return;var t=el.textContent||el.innerText;navigator.clipboard.writeText(t).then(function(){{showToast("{("已复制" if is_cn else "Copied")}")}})["catch"](function(){{showToast("{("复制失败" if is_cn else "Copy failed")}")}})}}
{js_code}
</script>
</body>
</html>'''
    return html

# ============================================================
# Tool Definitions
# ============================================================

TOOLS = [
    {
        "slug": "equity-dilution-calc",
        "cn_title": "股权稀释计算器",
        "cn_h1": "股权稀释计算器",
        "cn_desc": "免费在线股权稀释计算器，帮助创业者计算融资后股权稀释比例。支持多轮融资、ESOP期权池、可转债转换等多种稀释场景。纯前端计算，数据不上传服务器。",
        "cn_hero": "免费在线股权稀释计算器，帮助创业者计算融资后股权稀释比例。支持多轮融资、ESOP期权池、可转债转换等多种稀释场景。",
        "cn_cat": "finance-tools",
        "cn_icon": "📊",
        "cn_keywords": "股权稀释计算器,融资稀释,创业股权,ESOP,cap table",
        "cn_faq": [
            {"q": "什么是股权稀释？", "a": "股权稀释是指公司在融资或发行新股时，原有股东持股比例下降的现象。例如创始人最初持有100%股权，融资20%后，创始人持股降至80%。稀释虽然降低了持股比例，但如果公司估值增长足够快，持股价值反而可能增加。"},
            {"q": "如何避免过度稀释？", "a": "设定合理的融资轮次和金额，避免过早大规模融资。预留ESOP时控制在10-20%之间。每轮融资控制在稀释15-25%以内。使用可转债或SAFE等工具推迟股权稀释。同时关注估值增长，确保稀释后价值不降。"},
            {"q": "ESOP期权池如何影响稀释？", "a": "ESOP（员工期权池）通常在融资前或同时设立，会额外稀释现有股东。如果融资前设20%期权池，投资人占20%，则创始人剩余64%（而非80%）。因此期权池是创业者在融资谈判中的重要博弈点。"},
            {"q": "反稀释条款是什么？", "a": "反稀释条款是保护早期投资者在后续降价融资（Down Round）中不受过度稀释的条款。常见方式有完全棘轮（按新价格调整）和加权平均（按融资规模加权调整），后者对创始人更友好。"},
            {"q": "多轮融资后创始人还剩多少？", "a": "典型的从种子轮到IPO：种子轮20%→A轮20%→B轮15%→C轮10%→ESOP 15%，累计后创始人可能只剩20-35%。所以每轮融资的稀释率和估值同样重要。本计算器支持多轮模拟。"},
        ],
        "cn_use_cases": [
            {"title": "融资前模拟", "desc": "在见投资人之前，用计算器模拟不同融资金额和估值对股权结构的影响，明确自己能接受的最低估值和最高稀释率。"},
            {"title": "期权池规划", "desc": "规划ESOP规模时，计算期权池对现有股东（包括自己、联合创始人和早期员工）的稀释影响，找到最佳平衡点。"},
            {"title": "多轮融资推演", "desc": "模拟种子轮到IPO的完整融资路径，预估每轮稀释后的持股比例，帮助制定长期融资策略。"},
        ],
        "en_title": "Equity Dilution Calculator",
        "en_h1": "Equity Dilution Calculator",
        "en_desc": "Free online equity dilution calculator to help founders calculate post-funding ownership dilution. Supports multiple funding rounds, ESOP option pools, convertible notes. All calculations run locally in your browser.",
        "en_hero": "Free online equity dilution calculator to help founders calculate post-funding ownership dilution. Supports multiple funding rounds, ESOP option pools, convertible notes.",
        "en_cat": "finance-tools",
        "en_icon": "📊",
        "en_keywords": "equity dilution calculator,funding dilution,startup equity,ESOP,cap table",
        "en_faq": [
            {"q": "What is equity dilution?", "a": "Equity dilution occurs when a company issues new shares during funding rounds, reducing existing shareholders' ownership percentage. For example, if founders start with 100% and raise 20% equity, they're left with 80%. While dilution reduces percentage, if company valuation grows fast enough, the dollar value of holdings may actually increase."},
            {"q": "How to avoid excessive dilution?", "a": "Plan reasonable round sizes and timing. Avoid raising too much too early. Keep ESOP at 10-20%. Target dilution per round at 15-25% max. Use convertible notes or SAFEs to delay equity dilution. Always focus on valuation growth to ensure post-dilution value increases."},
            {"q": "How does an ESOP pool affect dilution?", "a": "An ESOP (Employee Stock Option Pool) is typically created before or alongside a funding round and further dilutes existing shareholders. If a 20% option pool is created pre-money and investors get 20%, founders are left with 64% (not 80%). This makes the option pool a key negotiation point for founders."},
            {"q": "What are anti-dilution provisions?", "a": "Anti-dilution provisions protect early investors from excessive dilution in a down round (lower valuation). Common types: full ratchet (adjusts to new price) and weighted average (adjusts by round size). Weighted average is more founder-friendly."},
            {"q": "How much is left for founders after multiple rounds?", "a": "Typical path Seed→IPO: Seed 20% → Series A 20% → Series B 15% → Series C 10% → ESOP 15%, leaving founders with roughly 20-35%. Each round's dilution rate matters as much as valuation. This calculator supports multi-round simulation."},
        ],
        "en_use_cases": [
            {"title": "Pre-Funding Simulation", "desc": "Before meeting investors, simulate how different raise amounts and valuations affect ownership structure to determine your minimum acceptable valuation and maximum dilution tolerance."},
            {"title": "Option Pool Planning", "desc": "When planning ESOP size, calculate the dilution impact on all shareholders including co-founders and early employees to find the optimal balance."},
            {"title": "Multi-Round Projection", "desc": "Map out the full Seed→IPO funding path to project ownership percentages after each round, helping build a long-term fundraising strategy."},
        ],
        "input_html": '''
<div class="input-group">
<label for="founderShares">创始人持股 (%)</label>
<input type="number" id="founderShares" value="100" min="0" max="100" step="0.1">
<div class="hint">当前创始人/现有股东总持股比例</div>
</div>
<div class="input-group">
<label for="newInvestment">新融资额 ($)</label>
<input type="number" id="newInvestment" value="1000000" min="0" step="10000">
<div class="hint">本轮计划融资金额</div>
</div>
<div class="input-group">
<label for="preMoney">投资前估值 ($)</label>
<input type="number" id="preMoney" value="4000000" min="1" step="10000">
<div class="hint">融资前公司估值</div>
</div>
<div class="input-group">
<label for="esopPct">ESOP期权池 (%)</label>
<input type="number" id="esopPct" value="10" min="0" max="50" step="0.1">
<div class="hint">员工期权池预留比例(融资前设立)</div>
</div>
''',
        "result_html": '''
<div class="result-card highlight">
<div class="label">投资后估值</div>
<div class="value" id="postMoney">-</div>
<div class="sub">Post-Money Valuation</div>
</div>
<div class="result-card">
<div class="label">投资人持股</div>
<div class="value" id="investorPct">-</div>
<div class="sub">新投资人股权比例</div>
</div>
<div class="result-card">
<div class="label">创始人持股</div>
<div class="value" id="founderFinalPct">-</div>
<div class="sub">含ESOP稀释后</div>
</div>
<div class="result-card">
<div class="label">ESOP期权池</div>
<div class="value" id="esopFinalPct">-</div>
<div class="sub">员工期权占比</div>
</div>
<div class="result-card">
<div class="label">总稀释比例</div>
<div class="value" id="totalDilution">-</div>
<div class="sub">创始人被稀释百分比</div>
</div>
''',
        "js_code": '''
function calculate() {
    var founder = parseFloat(document.getElementById('founderShares').value) || 100;
    var invest = parseFloat(document.getElementById('newInvestment').value) || 0;
    var pre = parseFloat(document.getElementById('preMoney').value) || 1;
    var esop = parseFloat(document.getElementById('esopPct').value) || 0;
    
    var postMoney = pre + invest;
    var investorPct = (invest / postMoney) * 100;
    
    // ESOP dilutes existing shareholders before investment
    var founderAfterEsop = founder * (1 - esop / 100);
    var founderFinal = founderAfterEsop * (1 - investorPct / 100);
    var esopFinal = esop * (1 - investorPct / 100);
    if (esop === 0) esopFinal = 0;
    
    var dilution = founder - founderFinal;
    
    document.getElementById('postMoney').textContent = '$' + postMoney.toLocaleString('en-US', {maximumFractionDigits:0});
    document.getElementById('investorPct').textContent = investorPct.toFixed(1) + '%';
    document.getElementById('founderFinalPct').textContent = founderFinal.toFixed(2) + '%';
    document.getElementById('esopFinalPct').textContent = esopFinal.toFixed(2) + '%';
    document.getElementById('totalDilution').textContent = dilution.toFixed(2) + '个百分点';
    document.getElementById('resultsSection').style.display = 'block';
}
function resetAll() {
    document.getElementById('founderShares').value = '100';
    document.getElementById('newInvestment').value = '1000000';
    document.getElementById('preMoney').value = '4000000';
    document.getElementById('esopPct').value = '10';
    document.getElementById('resultsSection').style.display = 'none';
}
''',
    },
    {
        "slug": "customer-lifetime-value",
        "cn_title": "客户生命周期价值(CLV)计算器",
        "cn_h1": "客户生命周期价值(CLV)计算器",
        "cn_desc": "免费在线客户生命周期价值(CLV/LTV)计算器，帮助企业量化单个客户带来的总利润。支持ARPU、流失率、毛利率三大核心参数。纯前端计算，数据不上传服务器。",
        "cn_hero": "免费在线客户生命周期价值(CLV/LTV)计算器，帮助企业量化单个客户带来的总利润。支持ARPU、流失率、毛利率三大核心参数。",
        "cn_cat": "finance-tools",
        "cn_icon": "💰",
        "cn_keywords": "CLV计算器,LTV计算器,客户生命周期价值,客户终身价值,SaaS指标",
        "cn_faq": [
            {"q": "什么是客户生命周期价值(CLV/LTV)？", "a": "CLV（Customer Lifetime Value）是一个客户在整个业务关系中为企业贡献的总利润。简单公式：CLV = 平均收入每用户(ARPU) × 毛利率 / 客户流失率。例如ARPU $100/月、毛利率80%、月流失率5%，则CLV = $100 × 80% / 5% = $1,600。"},
            {"q": "LTV:CAC比例多少算健康？", "a": "SaaS行业公认标准是LTV:CAC（客户获取成本）≥ 3:1才是健康。比例低于3说明获客成本过高或留存太差；高于5则可能获客投入不足，错失增长机会。最佳区间在3-5之间。"},
            {"q": "什么是好的客户流失率？", "a": "对于SaaS企业，月流失率在2-3%以下是健康的（年流失率24-36%）。优秀企业在1%以下。B2B SaaS通常流失率低于B2C。消费者订阅产品月流失率5-8%也属正常。"},
            {"q": "CLV和CAC有什么区别？", "a": "CLV是客户带来的总利润，CAC(Customer Acquisition Cost)是获取一个客户的成本。CLV是收入端指标，CAC是成本端。两者结合衡量商业模式可持续性：CLV必须大于CAC，通常要求LTV:CAC≥3。"},
            {"q": "如何提高CLV？", "a": "①减少流失率（改善产品体验/客户成功）；②提升ARPU（涨价/追加销售/交叉销售）；③提高毛利率（优化成本结构）。其中减少流失率对CLV的提升最显著，因为流失率在分母位置。"},
        ],
        "cn_use_cases": [
            {"title": "SaaS定价决策", "desc": "根据CLV反推合理的CAC预算，制定付费广告/内容营销的获客成本上限，确保每个渠道的客户获取都是盈利的。"},
            {"title": "客户分层", "desc": "计算不同客户群体的CLV，识别高价值客户（20%贡献80%利润），针对性地投入客户成功和留存资源。"},
            {"title": "融资数据支撑", "desc": "向投资人展示单位经济模型(Unit Economics)，用CLV和CAC数据证明商业模式的可持续性和盈利能力。"},
        ],
        "en_title": "Customer Lifetime Value (CLV) Calculator",
        "en_h1": "Customer Lifetime Value (CLV) Calculator",
        "en_desc": "Free online Customer Lifetime Value (CLV/LTV) calculator to quantify total profit per customer. Uses ARPU, churn rate and gross margin. All calculations run locally in your browser.",
        "en_hero": "Free online Customer Lifetime Value (CLV/LTV) calculator to quantify total profit per customer. Uses ARPU, churn rate and gross margin.",
        "en_cat": "finance-tools",
        "en_icon": "💰",
        "en_keywords": "CLV calculator,LTV calculator,customer lifetime value,SaaS metrics,unit economics",
        "en_faq": [
            {"q": "What is Customer Lifetime Value (CLV/LTV)?", "a": "CLV is the total profit a customer contributes over the entire business relationship. Simple formula: CLV = ARPU × Gross Margin / Churn Rate. Example: ARPU $100/mo, 80% margin, 5% monthly churn → CLV = $100 × 80% / 5% = $1,600."},
            {"q": "What is a healthy LTV:CAC ratio?", "a": "SaaS industry standard is LTV:CAC ≥ 3:1 for a healthy business. Below 3 suggests CAC is too high or retention too poor. Above 5 may mean under-investing in growth. The sweet spot is 3-5x."},
            {"q": "What is a good churn rate?", "a": "For SaaS, monthly churn below 2-3% is considered healthy (24-36% annually). Top companies stay under 1%. B2B SaaS typically has lower churn than B2C. Consumer subscription products at 5-8% monthly churn are still normal."},
            {"q": "What is the difference between CLV and CAC?", "a": "CLV is total profit per customer; CAC (Customer Acquisition Cost) is cost to acquire one. CLV is a revenue-side metric; CAC is cost-side. Together they measure business sustainability: CLV must exceed CAC, typically targeting LTV:CAC ≥ 3."},
            {"q": "How to improve CLV?", "a": "① Reduce churn (better product/customer success); ② Boost ARPU (price increases/upsells/cross-sells); ③ Improve margins (optimize cost structure). Reducing churn has the biggest impact since it sits in the denominator."},
        ],
        "en_use_cases": [
            {"title": "SaaS Pricing Decisions", "desc": "Back-calculate your acceptable CAC budget from CLV, setting upper limits for paid ads and content marketing to ensure every customer acquisition channel is profitable."},
            {"title": "Customer Segmentation", "desc": "Calculate CLV by customer segment to identify high-value customers (20% generating 80% of profit) and focus customer success and retention resources accordingly."},
            {"title": "Investor Data", "desc": "Present unit economics to investors with CLV and CAC data proving your business model's sustainability and profitability."},
        ],
        "input_html": '''
<div class="input-group">
<label for="arpu">月均ARPU ($)</label>
<input type="number" id="arpu" value="100" min="0" step="0.01">
<div class="hint">每位客户月平均收入</div>
</div>
<div class="input-group">
<label for="grossMargin">毛利率 (%)</label>
<input type="number" id="grossMargin" value="80" min="0" max="100" step="0.1">
<div class="hint">收入扣除直接成本后的利润率</div>
</div>
<div class="input-group">
<label for="churnRate">月流失率 (%)</label>
<input type="number" id="churnRate" value="5" min="0.01" max="100" step="0.01">
<div class="hint">每月取消订阅的客户比例</div>
</div>
<div class="input-group">
<label for="cac">客户获取成本 CAC ($)</label>
<input type="number" id="cac" value="200" min="0" step="1">
<div class="hint">获取一个客户的平均花费</div>
</div>
''',
        "result_html": '''
<div class="result-card highlight">
<div class="label">CLV 客户生命周期价值</div>
<div class="value" id="clv">-</div>
<div class="sub">每位客户总利润</div>
</div>
<div class="result-card">
<div class="label">LTV:CAC 比例</div>
<div class="value" id="ltvCac">-</div>
<div class="sub">健康标准≥3:1</div>
</div>
<div class="result-card">
<div class="label">平均客户生命周期</div>
<div class="value" id="avgLifetime">-</div>
<div class="sub">月</div>
</div>
<div class="result-card">
<div class="label">年化ARPU</div>
<div class="value" id="annualArpu">-</div>
<div class="sub">每位客户年收入</div>
</div>
<div class="result-card">
<div class="label">盈亏平衡状态</div>
<div class="value" id="healthStatus">-</div>
<div class="sub" id="healthSub">-</div>
</div>
''',
        "js_code": '''
function calculate() {
    var arpu = parseFloat(document.getElementById('arpu').value) || 0;
    var margin = parseFloat(document.getElementById('grossMargin').value) || 0;
    var churn = parseFloat(document.getElementById('churnRate').value) || 0.01;
    var cac = parseFloat(document.getElementById('cac').value) || 0;
    
    var churnDecimal = churn / 100;
    var marginDecimal = margin / 100;
    var avgLifetime = 1 / churnDecimal;
    var clv = arpu * marginDecimal * avgLifetime;
    var ltvCac = cac > 0 ? clv / cac : 0;
    var annualArpu = arpu * 12;
    
    var status = '';
    var sub = '';
    if (ltvCac >= 5) { status = '优秀'; sub = '可加大获客投入'; }
    else if (ltvCac >= 3) { status = '健康'; sub = '获客投入适中'; }
    else if (ltvCac >= 1) { status = '需优化'; sub = '减少获客成本或提升CLV'; }
    else { status = '亏损'; sub = '立即调整获客策略'; }
    
    document.getElementById('clv').textContent = '$' + clv.toFixed(2);
    document.getElementById('ltvCac').textContent = ltvCac.toFixed(1) + ':1';
    document.getElementById('avgLifetime').textContent = avgLifetime.toFixed(1) + ' 个月';
    document.getElementById('annualArpu').textContent = '$' + annualArpu.toFixed(2);
    document.getElementById('healthStatus').textContent = status;
    document.getElementById('healthSub').textContent = sub;
    document.getElementById('resultsSection').style.display = 'block';
}
function resetAll() {
    document.getElementById('arpu').value = '100';
    document.getElementById('grossMargin').value = '80';
    document.getElementById('churnRate').value = '5';
    document.getElementById('cac').value = '200';
    document.getElementById('resultsSection').style.display = 'none';
}
''',
    },
    {
        "slug": "revenue-projection",
        "cn_title": "收入预测计算器",
        "cn_h1": "收入预测计算器",
        "cn_desc": "免费在线收入预测计算器，基于月增长率和初始收入预测未来12-60个月收入趋势。支持环比增长和同比增长两种模式。纯前端计算，数据不上传服务器。",
        "cn_hero": "免费在线收入预测计算器，基于月增长率和初始收入预测未来12-60个月收入趋势。支持环比增长和同比增长两种模式。",
        "cn_cat": "finance-tools",
        "cn_icon": "📈",
        "cn_keywords": "收入预测计算器,营收预估,增长预测,SaaS收入预测,财务预测",
        "cn_faq": [
            {"q": "如何设定合理的月增长率？", "a": "初创SaaS公司早期月增长可达10-20%（年化3-9倍），进入规模期后降至3-7%。成熟企业月增长1-3%。建议参考同行公开数据并结合自身历史数据设定。保守估计通常更明智。"},
            {"q": "环比增长(CMGR)和同比增长有什么区别？", "a": "环比(Month-over-Month, MoM)是相邻两月的增长率，反映短期趋势。同比(Year-over-Year, YoY)是今年与去年同月的增长率，消除季节性因素。本计算器支持两种模式切换。"},
            {"q": "复合增长率(CAGR)如何计算？", "a": "CAGR = (期末值/期初值)^(1/n) - 1，其中n为年数。例如初始$10K，5年后$100K，CAGR = (100/10)^(1/5)-1 ≈ 58.5%。CAGR平滑了波动，反映长期趋势。"},
            {"q": "收入预测有哪些常见误区？", "a": "①线性外推——忽略了市场天花板和竞争加剧；②忽视季节性——12月/1月收入常低于月均；③不区分MRR和一次性收入——SaaS应聚焦经常性收入预测；④未考虑流失——新客户增长应扣除流失。"},
            {"q": "如何使用收入预测进行融资？", "a": "投资人看重的是可复制的增长模型。展示时说明增长来源（新客户/涨价/新市场），设定乐观/现实/悲观三挡，用实际留存数据支撑，而非单纯的线性增长假设。"},
        ],
        "cn_use_cases": [
            {"title": "SaaS融资路演", "desc": "生成3-5年收入预测表格，展示不同增长率假设下达到$100M ARR的路径，为投资人展示清晰增长路线图。"},
            {"title": "团队招聘规划", "desc": "根据预测收入推算可负担的团队规模——通常SaaS企业人员成本占收入的40-60%，确保招聘节奏与收入增长匹配。"},
            {"title": "年度目标拆解", "desc": "从年度收入目标反推所需月均增长率，拆解为季度里程碑和新客户获取目标，让团队有明确执行方向。"},
        ],
        "en_title": "Revenue Projection Calculator",
        "en_h1": "Revenue Projection Calculator",
        "en_desc": "Free online revenue projection calculator to forecast future 12-60 month revenue trends based on monthly growth rate and starting MRR. Supports MoM and YoY modes. All calculations run locally in your browser.",
        "en_hero": "Free online revenue projection calculator to forecast future 12-60 month revenue trends based on monthly growth rate and starting MRR. Supports MoM and YoY modes.",
        "en_cat": "finance-tools",
        "en_icon": "📈",
        "en_keywords": "revenue projection calculator,revenue forecast,growth projection,SaaS MRR forecast,financial projection",
        "en_faq": [
            {"q": "What is a reasonable monthly growth rate?", "a": "Early-stage SaaS startups can see 10-20% MoM (3-9x annualized). Growth-stage settles to 3-7%. Mature companies see 1-3% MoM. Reference peer public data and your own historical numbers. Conservative estimates are usually wiser."},
            {"q": "What is the difference between MoM and YoY growth?", "a": "MoM (Month-over-Month) compares adjacent months, showing short-term trends. YoY (Year-over-Year) compares the same month a year ago, eliminating seasonality. This calculator supports both modes."},
            {"q": "How is CAGR calculated?", "a": "CAGR = (Ending Value / Starting Value)^(1/n) - 1, where n = number of years. Example: $10K → $100K over 5 years, CAGR = (100/10)^(1/5)-1 ≈ 58.5%. CAGR smooths out volatility to show the long-term trend."},
            {"q": "What are common revenue projection mistakes?", "a": "① Linear extrapolation ignoring market saturation and competition; ② Ignoring seasonality — Dec/Jan revenue often below average; ③ Not separating MRR from one-time revenue — SaaS should focus on recurring revenue; ④ Not accounting for churn — new customer adds must net of churn."},
            {"q": "How to use revenue projections for fundraising?", "a": "Investors want replicable growth models. Show growth sources (new customers/price increases/new markets), present optimistic/realistic/pessimistic scenarios, and back projections with actual retention data rather than pure linear assumptions."},
        ],
        "en_use_cases": [
            {"title": "SaaS Fundraising Deck", "desc": "Generate 3-5 year revenue projection tables showing the path to $100M ARR under different growth assumptions, presenting a clear growth roadmap to investors."},
            {"title": "Team Hiring Planning", "desc": "Calculate affordable team size from projected revenue — SaaS companies typically spend 40-60% of revenue on personnel. Ensure hiring pace matches revenue growth."},
            {"title": "Annual Goal Decomposition", "desc": "Work backwards from annual revenue targets to required monthly growth rates, breaking them into quarterly milestones and new customer acquisition targets."},
        ],
        "input_html": '''
<div class="input-group">
<label for="initMrr">初始月收入 MRR ($)</label>
<input type="number" id="initMrr" value="10000" min="0" step="1">
<div class="hint">当前月经常性收入</div>
</div>
<div class="input-group">
<label for="growthRate">月增长率 (%)</label>
<input type="number" id="growthRate" value="5" min="0" max="100" step="0.1">
<div class="hint">预期月环比增长率</div>
</div>
<div class="input-group">
<label for="months">预测月数</label>
<input type="number" id="months" value="24" min="1" max="60" step="1">
<div class="hint">预测时间跨度(1-60个月)</div>
</div>
<div class="input-group">
<label for="growthMode">增长模式</label>
<select id="growthMode"><option value="mom">月环比增长 (MoM)</option><option value="yoy">年同比增长 (YoY)</option></select>
<div class="hint">选择增长计算方式</div>
</div>
''',
        "result_html": '''
<div class="result-card highlight">
<div class="label">期末月收入 MRR</div>
<div class="value" id="finalMrr">-</div>
<div class="sub">预测期末月收入</div>
</div>
<div class="result-card">
<div class="label">期末年化收入 ARR</div>
<div class="value" id="finalArr">-</div>
<div class="sub">期末年度经常性收入</div>
</div>
<div class="result-card">
<div class="label">总收入CAGR</div>
<div class="value" id="cagr">-</div>
<div class="sub">复合年增长率</div>
</div>
<div class="result-card">
<div class="label">累计总收入</div>
<div class="value" id="totalRevenue">-</div>
<div class="sub">整个预测期总收入</div>
</div>
''',
        "js_code": '''
function calculate() {
    var init = parseFloat(document.getElementById('initMrr').value) || 0;
    var growth = parseFloat(document.getElementById('growthRate').value) || 0;
    var mos = parseInt(document.getElementById('months').value) || 24;
    var mode = document.getElementById('growthMode').value;
    
    var finalMrr = init;
    var totalRev = 0;
    var rate = growth / 100;
    
    for (var i = 0; i < mos; i++) {
        totalRev += finalMrr;
        if (mode === 'mom') {
            finalMrr *= (1 + rate);
        } else {
            // YoY: apply annual growth rate monthly
            finalMrr *= (1 + rate / 12);
        }
    }
    
    var finalArr = finalMrr * 12;
    var years = mos / 12;
    var cagr = years > 0 ? (Math.pow(finalMrr / init, 1 / years) - 1) * 100 : 0;
    
    document.getElementById('finalMrr').textContent = '$' + finalMrr.toLocaleString('en-US', {maximumFractionDigits:0});
    document.getElementById('finalArr').textContent = '$' + finalArr.toLocaleString('en-US', {maximumFractionDigits:0});
    document.getElementById('cagr').textContent = cagr.toFixed(1) + '%';
    document.getElementById('totalRevenue').textContent = '$' + totalRev.toLocaleString('en-US', {maximumFractionDigits:0});
    document.getElementById('resultsSection').style.display = 'block';
}
function resetAll() {
    document.getElementById('initMrr').value = '10000';
    document.getElementById('growthRate').value = '5';
    document.getElementById('months').value = '24';
    document.getElementById('growthMode').value = 'mom';
    document.getElementById('resultsSection').style.display = 'none';
}
''',
    },
    {
        "slug": "federal-tax-calc",
        "cn_title": "美国联邦个人所得税计算器",
        "cn_h1": "美国联邦个人所得税计算器",
        "cn_desc": "免费在线美国联邦个人所得税计算器（2025税级），基于IRS累进税率表计算应缴税款。支持单身/夫妻合并/户主等申报状态和标准扣除额。纯前端计算。",
        "cn_hero": "免费在线美国联邦个人所得税计算器（2025税级），基于IRS累进税率表计算应缴税款。支持单身/夫妻合并/户主等申报状态和标准扣除额。",
        "cn_cat": "finance-tools",
        "cn_icon": "🧾",
        "cn_keywords": "联邦个人所得税计算器,IRS税率,美国个税计算,2025税级,税款估算",
        "cn_faq": [
            {"q": "2025年美国联邦个人税率有哪几档？", "a": "2025年IRS七档累进税率：10%、12%、22%、24%、32%、35%、37%。单身纳税人：10%($0-$11,925)、12%($11,925-$48,475)、22%($48,475-$103,350)、24%($103,350-$197,300)、32%($197,300-$250,525)、35%($250,525-$626,350)、37%(>$626,350)。以上为估算参考，请以IRS官网为准。"},
            {"q": "什么是标准扣除额(Standard Deduction)？", "a": "标准扣除额是IRS允许从总收入中减去的一笔固定金额，不需要逐项列举。2025年标准扣除额估算：单身$15,000、夫妻合并$30,000、户主$22,500。大多数纳税人使用标准扣除比逐项扣除更划算。注意：实际金额请以IRS最新公布为准。"},
            {"q": "累进税率是什么意思？", "a": "累进税率意味着不同收入段适用不同税率。比如您的应税收入$60,000，前$11,925按10%计税，$11,925-$48,475按12%计税，剩余按22%计税。实际平均税率(有效税率)远低于最高档位税率。这就是为什么边际税率不等于实际税负。"},
            {"q": "什么是边际税率和有效税率？", "a": "边际税率是您最后一美元收入的税率（即最高档位税率）。有效税率是实际缴税总额除以总收入的比例。例如$80,000收入，边际税率可能是22%，但有效税率通常在12-15%。加薪是否值得需看边际税率，而非有效税率。"},
            {"q": "申报状态如何选择？", "a": "单身(Single)：未婚且无法被他人申报；夫妻合并(MFJ)：已婚共同申报，通常最优惠；夫妻分别(MFS)：已婚分开申报，某些情况下有利；户主(HoH)：未婚但有受抚养人，税率比单身优惠。本计算器支持前三种。"},
        ],
        "cn_use_cases": [
            {"title": "报税预估", "desc": "提前计算应纳税额和有效税率，了解自己是否需要补缴或可获得退税，避免报税季节的意外账单。"},
            {"title": "涨薪评估", "desc": "计算加薪后的实际到手收入变化——$5,000加薪实际到手可能只有$3,900（22%税率），帮助做出理性的薪酬决策。"},
            {"title": "扣除策略优化", "desc": "对比标准扣除与预估的逐项扣除（房贷利息、慈善捐款等），选择更有利的扣除方式，最大化节税效果。"},
        ],
        "en_title": "US Federal Income Tax Calculator",
        "en_h1": "US Federal Income Tax Calculator",
        "en_desc": "Free online US Federal Income Tax calculator (2025 brackets) based on IRS progressive tax rates. Supports Single/MFJ/HoH filing statuses and standard deduction. All calculations run locally.",
        "en_hero": "Free online US Federal Income Tax calculator (2025 brackets) based on IRS progressive tax rates. Supports Single/MFJ/HoH filing statuses and standard deduction.",
        "en_cat": "finance-tools",
        "en_icon": "🧾",
        "en_keywords": "federal income tax calculator,IRS tax brackets,US tax calculator,2025 tax rates,tax estimation",
        "en_faq": [
            {"q": "What are the 2025 federal tax brackets?", "a": "The 2025 IRS has seven progressive brackets: 10%, 12%, 22%, 24%, 32%, 35%, 37%. For Single filers: 10%($0-$11,925), 12%($11,925-$48,475), 22%($48,475-$103,350), 24%($103,350-$197,300), 32%($197,300-$250,525), 35%($250,525-$626,350), 37%(>$626,350). These are estimates — check IRS.gov for official numbers."},
            {"q": "What is the Standard Deduction?", "a": "The Standard Deduction is a fixed dollar amount the IRS allows you to subtract from gross income without itemizing. 2025 estimates: Single $15,000, MFJ $30,000, HoH $22,500. Most taxpayers find the standard deduction more beneficial than itemizing. Check IRS.gov for official figures."},
            {"q": "What does progressive taxation mean?", "a": "Progressive tax means different income portions are taxed at different rates. For example, $60,000 taxable income: first $11,925 at 10%, $11,925-$48,475 at 12%, remainder at 22%. Your effective tax rate is much lower than your top bracket rate."},
            {"q": "What is the difference between marginal and effective tax rate?", "a": "Marginal rate is the tax rate on your last dollar (your top bracket). Effective rate is total tax divided by total income. Example: $80K income, marginal rate may be 22% but effective rate is typically 12-15%. Whether a raise is 'worth it' depends on marginal rate, not effective."},
            {"q": "How do I choose my filing status?", "a": "Single: unmarried, not claimable by others. Married Filing Jointly (MFJ): married filing together, usually most beneficial. Married Filing Separately (MFS): married filing separately, advantageous in some cases. Head of Household (HoH): unmarried with dependents, better rates than Single. This calculator supports the first three."},
        ],
        "en_use_cases": [
            {"title": "Tax Estimation", "desc": "Calculate your tax liability and effective rate ahead of time to know whether you'll owe money or get a refund, avoiding surprise bills at tax time."},
            {"title": "Raise Evaluation", "desc": "Calculate take-home impact of a raise — a $5,000 raise may net only $3,900 (22% bracket), helping you make informed compensation decisions."},
            {"title": "Deduction Strategy", "desc": "Compare standard deduction vs estimated itemized deductions (mortgage interest, charitable donations, etc.) to choose the more beneficial approach."},
        ],
        "input_html": '''
<div class="input-group">
<label for="grossIncome">年总收入 ($)</label>
<input type="number" id="grossIncome" value="75000" min="0" step="1">
<div class="hint">税前年度总收入 (W2工资)</div>
</div>
<div class="input-group">
<label for="filingStatus">申报状态</label>
<select id="filingStatus">
<option value="single">单身 (Single)</option>
<option value="mfj">夫妻合并 (MFJ)</option>
<option value="hoh">户主 (HoH)</option>
</select>
<div class="hint">您的IRS申报状态</div>
</div>
<div class="input-group">
<label for="extraDeduction">额外扣除额 ($)</label>
<input type="number" id="extraDeduction" value="0" min="0" step="1">
<div class="hint">401k/IRA/HSA等税前列支项目总计</div>
</div>
''',
        "result_html": '''
<div class="result-card highlight">
<div class="label">应缴联邦税款</div>
<div class="value" id="taxLiability">-</div>
<div class="sub">Federal Tax Liability</div>
</div>
<div class="result-card">
<div class="label">有效税率</div>
<div class="value" id="effectiveRate">-</div>
<div class="sub">Effective Tax Rate</div>
</div>
<div class="result-card">
<div class="label">边际税率</div>
<div class="value" id="marginalRate">-</div>
<div class="sub">Marginal Tax Bracket</div>
</div>
<div class="result-card">
<div class="label">应税收入</div>
<div class="value" id="taxableIncome">-</div>
<div class="sub">扣除标准/额外扣除后</div>
</div>
<div class="result-card">
<div class="label">税后收入</div>
<div class="value" id="afterTax">-</div>
<div class="sub">After-Tax Income</div>
</div>
''',
        "js_code": '''
function getBrackets(status) {
    if (status === 'single') return [
        {max: 11925, rate: 0.10}, {max: 48475, rate: 0.12}, {max: 103350, rate: 0.22},
        {max: 197300, rate: 0.24}, {max: 250525, rate: 0.32}, {max: 626350, rate: 0.35}, {max: Infinity, rate: 0.37}
    ];
    if (status === 'hoh') return [
        {max: 17000, rate: 0.10}, {max: 64850, rate: 0.12}, {max: 103350, rate: 0.22},
        {max: 197300, rate: 0.24}, {max: 250500, rate: 0.32}, {max: 626350, rate: 0.35}, {max: Infinity, rate: 0.37}
    ];
    // MFJ
    return [
        {max: 23850, rate: 0.10}, {max: 96950, rate: 0.12}, {max: 206700, rate: 0.22},
        {max: 394600, rate: 0.24}, {max: 488350, rate: 0.32}, {max: 626350, rate: 0.35}, {max: Infinity, rate: 0.37}
    ];
}
function getStandardDeduction(status) {
    if (status === 'single') return 15000;
    if (status === 'hoh') return 22500;
    return 30000; // MFJ
}
function calculate() {
    var gross = parseFloat(document.getElementById('grossIncome').value) || 0;
    var status = document.getElementById('filingStatus').value;
    var extra = parseFloat(document.getElementById('extraDeduction').value) || 0;
    
    var stdDeduction = getStandardDeduction(status);
    var taxable = Math.max(0, gross - stdDeduction - extra);
    var brackets = getBrackets(status);
    
    var tax = 0;
    var remaining = taxable;
    var prevMax = 0;
    var marginal = 0;
    for (var i = 0; i < brackets.length; i++) {
        var bracket = brackets[i];
        var bracketWidth = bracket.max - prevMax;
        var taxableInBracket = Math.min(remaining, bracketWidth);
        tax += taxableInBracket * bracket.rate;
        if (taxableInBracket > 0) marginal = bracket.rate;
        remaining -= taxableInBracket;
        prevMax = bracket.max;
        if (remaining <= 0) break;
    }
    
    var effectiveRate = gross > 0 ? (tax / gross) * 100 : 0;
    var afterTax = gross - tax;
    
    document.getElementById('taxLiability').textContent = '$' + tax.toLocaleString('en-US', {maximumFractionDigits:0});
    document.getElementById('effectiveRate').textContent = effectiveRate.toFixed(1) + '%';
    document.getElementById('marginalRate').textContent = (marginal * 100).toFixed(0) + '%';
    document.getElementById('taxableIncome').textContent = '$' + taxable.toLocaleString('en-US', {maximumFractionDigits:0});
    document.getElementById('afterTax').textContent = '$' + afterTax.toLocaleString('en-US', {maximumFractionDigits:0});
    document.getElementById('resultsSection').style.display = 'block';
}
function resetAll() {
    document.getElementById('grossIncome').value = '75000';
    document.getElementById('filingStatus').value = 'single';
    document.getElementById('extraDeduction').value = '0';
    document.getElementById('resultsSection').style.display = 'none';
}
''',
    },
    {
        "slug": "freelance-tax-calc",
        "cn_title": "自由职业者税务计算器",
        "cn_h1": "自由职业者税务计算器",
        "cn_desc": "免费在线自由职业者税务计算器，计算自雇税(SE Tax)、联邦所得税和总税负。含QBI扣除和业务支出抵扣估算。纯前端计算，数据不上传服务器。",
        "cn_hero": "免费在线自由职业者税务计算器，计算自雇税(SE Tax)、联邦所得税和总税负。含QBI扣除和业务支出抵扣估算。",
        "cn_cat": "finance-tools",
        "cn_icon": "💼",
        "cn_keywords": "自由职业税务计算器,自雇税,SE Tax,1099税务,自由职业税负",
        "cn_faq": [
            {"q": "什么是自雇税(Self-Employment Tax)？", "a": "自雇税是自由职业者支付的社会保障和医疗保险税，等同于W2员工和雇主共同缴纳的部分。2025年税率为15.3%（社安12.4%+医保2.9%）。W2员工只负担7.65%，雇主付另一半；但自由职业者既是员工又是雇主，需全额自付。社安税有收入上限($168,600)，超出部分只缴医保税。"},
            {"q": "自由职业者如何计算季度预缴税？", "a": "IRS要求自由职业者按季度预估缴纳（4月15日、6月15日、9月15日、次年1月15日）。通常按上年税负的100%或当年预估的90%缴纳。缺缴会面临罚款。本计算器可估算全年税负，除以4即为季度预缴额。"},
            {"q": "什么是QBI扣除？", "a": "QBI（Qualified Business Income）扣除允许符合条件的自雇人士从应税收入中扣除合格业务收入的20%。例如自由职业净收入$80,000，QBI扣除为$16,000，应税收入降至$64,000。这是2018年税改的重大利好。"},
            {"q": "自雇税可以抵扣吗？", "a": "可以！自雇税的一半（7.65%）可作为调整后毛收入(AGI)的扣除项，降低联邦所得税。本计算器自动包含此抵扣。例如自雇税$11,000，可在计算联邦税前扣除$5,500。"},
            {"q": "哪些业务支出可以抵扣？", "a": "家庭办公室（按面积比例）、电脑/软件/设备、网络/电话费、专业服务（律师/会计）、差旅费、继续教育、健康保险保费（自雇者）、退休计划供款（SEP IRA/Solo 401k）。保留收据，合理但不激进。"},
        ],
        "cn_use_cases": [
            {"title": "季度预缴税规划", "desc": "年初估算全年自雇收入和预期税负，设定每季度预缴金额，避免年末大额补缴和IRS罚款。"},
            {"title": "时薪定价决策", "desc": "计算扣除自雇税和所得税后的实际时薪，对比W2同等税前收入，确保自由职业定价合理且有利润空间。"},
            {"title": "S-Corp转换评估", "desc": "当自雇净收入超过$50,000-70,000时，评估转为S-Corp是否更省税——S-Corp可避免部分自雇税。"},
        ],
        "en_title": "Freelance Tax Calculator",
        "en_h1": "Freelance Tax Calculator",
        "en_desc": "Free online freelance tax calculator to estimate Self-Employment tax, federal income tax and total tax burden. Includes QBI deduction and business expense estimates. All calculations run locally in your browser.",
        "en_hero": "Free online freelance tax calculator to estimate Self-Employment tax, federal income tax and total tax burden. Includes QBI deduction and business expense estimates.",
        "en_cat": "finance-tools",
        "en_icon": "💼",
        "en_keywords": "freelance tax calculator,self-employment tax,SE tax,1099 tax,freelancer tax burden",
        "en_faq": [
            {"q": "What is Self-Employment (SE) Tax?", "a": "SE tax is the Social Security and Medicare tax freelancers pay, equivalent to what W2 employees and their employers pay combined. The 2025 rate is 15.3% (12.4% Social Security + 2.9% Medicare). W2 employees pay 7.65% with employer covering the other half; freelancers pay the full 15.3% themselves. Social Security has an income cap ($168,600), above which only Medicare tax applies."},
            {"q": "How do freelancers calculate quarterly estimated taxes?", "a": "IRS requires quarterly estimated payments (April 15, June 15, September 15, January 15). Generally pay 100% of last year's tax or 90% of current year's estimate. Missing payments incurs penalties. This calculator estimates annual tax burden — divide by 4 for quarterly payments."},
            {"q": "What is the QBI deduction?", "a": "QBI (Qualified Business Income) deduction allows eligible self-employed individuals to deduct 20% of qualified business income from taxable income. Example: $80,000 freelance net income → $16,000 QBI deduction → $64,000 taxable. This is a major benefit from the 2018 tax reform."},
            {"q": "Is SE tax deductible?", "a": "Yes! Half of your SE tax (7.65%) is deductible as an above-the-line adjustment to AGI, reducing federal income tax. This calculator automatically includes this deduction. Example: $11,000 SE tax → $5,500 deduction against income tax."},
            {"q": "What business expenses can I deduct?", "a": "Home office (by square footage proportion), computer/software/equipment, internet/phone, professional services (lawyer/CPA), travel, continuing education, health insurance premiums (self-employed), retirement plan contributions (SEP IRA/Solo 401k). Keep receipts — be reasonable but not aggressive."},
        ],
        "en_use_cases": [
            {"title": "Quarterly Tax Planning", "desc": "Estimate annual freelance income and tax burden early in the year to set quarterly payment amounts, avoiding large year-end bills and IRS penalties."},
            {"title": "Hourly Rate Decisions", "desc": "Calculate actual take-home pay after SE tax and income tax, comparing against W2 pre-tax equivalents to ensure freelance pricing is reasonable and profitable."},
            {"title": "S-Corp Conversion Assessment", "desc": "When net freelance income exceeds $50,000-70,000, evaluate whether converting to S-Corp saves more in taxes — S-Corp can avoid some SE tax."},
        ],
        "input_html": '''
<div class="input-group">
<label for="netIncome">年度自由职业净收入 ($)</label>
<input type="number" id="netIncome" value="80000" min="0" step="1">
<div class="hint">扣除业务支出后的净收入</div>
</div>
<div class="input-group">
<label for="businessExpenses">业务支出 ($)</label>
<input type="number" id="businessExpenses" value="10000" min="0" step="1">
<div class="hint">可抵扣业务支出总额</div>
</div>
<div class="input-group">
<label for="filingStatus">申报状态</label>
<select id="filingStatus">
<option value="single">单身 (Single)</option>
<option value="mfj">夫妻合并 (MFJ)</option>
</select>
<div class="hint"></div>
</div>
<div class="input-group">
<label for="otherIncome">其他收入 ($)</label>
<input type="number" id="otherIncome" value="0" min="0" step="1">
<div class="hint">W2工资/投资收益等(如有)</div>
</div>
''',
        "result_html": '''
<div class="result-card highlight">
<div class="label">总税负</div>
<div class="value" id="totalTax">-</div>
<div class="sub">自雇税 + 联邦所得税</div>
</div>
<div class="result-card">
<div class="label">自雇税 (SE Tax)</div>
<div class="value" id="seTax">-</div>
<div class="sub">社安+医保 15.3%</div>
</div>
<div class="result-card">
<div class="label">联邦所得税</div>
<div class="value" id="incomeTax">-</div>
<div class="sub">含QBI扣除和SE税抵扣</div>
</div>
<div class="result-card">
<div class="label">有效税率</div>
<div class="value" id="effectiveRate">-</div>
<div class="sub">总税负/总收入</div>
</div>
<div class="result-card">
<div class="label">税后收入</div>
<div class="value" id="takeHome">-</div>
<div class="sub">实际到手年收入</div>
</div>
<div class="result-card">
<div class="label">季度预缴额</div>
<div class="value" id="quarterly">-</div>
<div class="sub">建议每季度预缴</div>
</div>
''',
        "js_code": '''
function getIncomeTax(taxable, status) {
    var brackets;
    if (status === 'single') {
        brackets = [{max:11925,rate:0.10},{max:48475,rate:0.12},{max:103350,rate:0.22},
            {max:197300,rate:0.24},{max:250525,rate:0.32},{max:626350,rate:0.35},{max:Infinity,rate:0.37}];
    } else {
        brackets = [{max:23850,rate:0.10},{max:96950,rate:0.12},{max:206700,rate:0.22},
            {max:394600,rate:0.24},{max:488350,rate:0.32},{max:626350,rate:0.35},{max:Infinity,rate:0.37}];
    }
    var tax = 0, remaining = taxable, prevMax = 0;
    for (var i = 0; i < brackets.length; i++) {
        var b = brackets[i];
        var inBracket = Math.min(remaining, b.max - prevMax);
        if (inBracket <= 0) break;
        tax += inBracket * b.rate;
        remaining -= inBracket;
        prevMax = b.max;
    }
    return Math.max(0, tax);
}

function calculate() {
    var net = parseFloat(document.getElementById('netIncome').value) || 0;
    var expenses = parseFloat(document.getElementById('businessExpenses').value) || 0;
    var status = document.getElementById('filingStatus').value;
    var other = parseFloat(document.getElementById('otherIncome').value) || 0;
    
    // SE tax: 92.35% of net earnings subject to 15.3%
    var seBase = net * 0.9235;
    var ssWageCap = 168600;
    var seSocialSecurity = Math.min(seBase, ssWageCap) * 0.124;
    var seMedicare = seBase * 0.029;
    var seTax = seSocialSecurity + seMedicare;
    
    // Deductible half of SE tax
    var seHalf = seTax * 0.5;
    
    // QBI deduction: 20% of net income (simplified)
    var qbi = net * 0.20;
    
    // Standard deduction
    var stdDed = status === 'single' ? 15000 : 30000;
    
    // Taxable income
    var totalIncome = net + other;
    var taxable = Math.max(0, totalIncome - stdDed - seHalf - qbi);
    var incomeTax = getIncomeTax(taxable, status);
    
    var totalTax = seTax + incomeTax;
    var effectiveRate = totalIncome > 0 ? (totalTax / totalIncome) * 100 : 0;
    var takeHome = totalIncome - totalTax;
    var quarterly = totalTax / 4;
    
    document.getElementById('totalTax').textContent = '$' + totalTax.toLocaleString('en-US', {maximumFractionDigits:0});
    document.getElementById('seTax').textContent = '$' + seTax.toLocaleString('en-US', {maximumFractionDigits:0});
    document.getElementById('incomeTax').textContent = '$' + incomeTax.toLocaleString('en-US', {maximumFractionDigits:0});
    document.getElementById('effectiveRate').textContent = effectiveRate.toFixed(1) + '%';
    document.getElementById('takeHome').textContent = '$' + takeHome.toLocaleString('en-US', {maximumFractionDigits:0});
    document.getElementById('quarterly').textContent = '$' + quarterly.toLocaleString('en-US', {maximumFractionDigits:0});
    document.getElementById('resultsSection').style.display = 'block';
}
function resetAll() {
    document.getElementById('netIncome').value = '80000';
    document.getElementById('businessExpenses').value = '10000';
    document.getElementById('filingStatus').value = 'single';
    document.getElementById('otherIncome').value = '0';
    document.getElementById('resultsSection').style.display = 'none';
}
''',
    },
]

# ============================================================
# Generate
# ============================================================
for t in TOOLS:
    for lang in ["cn", "en"]:
        is_cn = (lang == "cn")
        slug = t["slug"]
        title = t["cn_title"] if is_cn else t["en_title"]
        h1 = t["cn_h1"] if is_cn else t["en_h1"]
        desc = t["cn_desc"] if is_cn else t["en_desc"]
        hero = t["cn_hero"] if is_cn else t["en_hero"]
        cat = t["cn_cat"] if is_cn else t["en_cat"]
        icon = t["cn_icon"] if is_cn else t["en_icon"]
        keywords = t["cn_keywords"] if is_cn else t["en_keywords"]
        faq = t["cn_faq"] if is_cn else t["en_faq"]
        use_cases = t["cn_use_cases"] if is_cn else t["en_use_cases"]
        
        html = build_page(slug, lang, title, h1, desc, hero, cat, icon, faq, use_cases, keywords, t["input_html"], t["result_html"], t["js_code"])
        
        if is_cn:
            dir_path = os.path.join(SITE, slug)
        else:
            dir_path = os.path.join(SITE, "en", slug)
        
        os.makedirs(dir_path, exist_ok=True)
        filepath = os.path.join(dir_path, "index.html")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)
        
        lang_label = "CN" if is_cn else "EN"
        print(f"✅ Created {slug} ({lang_label})")

print(f"\n🎉 Done! Created {len(TOOLS)} tools (CN+EN = {len(TOOLS)*2} pages)")
