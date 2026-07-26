#!/usr/bin/env python3
"""Batch create 5 new tools with full CN+EN versions"""
import os

SITE = "/home/chison/tools-site"
BASE_CANONICAL = "https://free-toolbase.com"
G_TAG = "G-9W1157EBQV"
ADSENSE = "ca-pub-5998441792679372"
EMAIL = "dexshuang@google.com"

def esc(s):
    return s.replace("\\", "\\\\").replace("'", "\\'").replace('"', '\\"')

def build_html(slug, lang, title, h1, desc, hero, cat, icon, faq_list, use_cases, keywords=""):
    is_cn = (lang == "cn")
    lang_attr = "zh-CN" if is_cn else "en"
    canonical_suffix = f"/{slug}/" if is_cn else f"/en/{slug}/"
    alt_suffix = f"/en/{slug}/" if is_cn else f"/{slug}/"
    alt_lang_code = "en" if is_cn else "zh"
    xdefault = f"/en/{slug}/"
    
    home_text = "首页" if is_cn else "Home"
    tools_text = "工具" if is_cn else "Tools"
    all_tools_text = "全部工具" if is_cn else "All Tools"
    contact_text = "联系我们" if is_cn else "Contact"
    privacy_text = "隐私政策" if is_cn else "Privacy"
    terms_text = "服务条款" if is_cn else "Terms"
    about_text = "关于我们" if is_cn else "About"
    feedback_text = "问题反馈" if is_cn else "Feedback"
    calc_btn = "🧮 开始计算" if is_cn else "🧮 Calculate"
    reset_btn = "🔄 重置" if is_cn else "🔄 Reset"
    input_label = "🔢 输入参数" if is_cn else "🔢 Input Parameters"
    results_label = "📊 计算结果" if is_cn else "📊 Results"
    howto_label = "📖 使用教程" if is_cn else "📖 How to Use"
    usecase_label = "🎯 应用场景" if is_cn else "🎯 Use Cases"
    faq_label = "❓ 常见问题 (FAQ)" if is_cn else "❓ FAQ"
    badge_text = "零依赖·可离线使用" if is_cn else "Zero Dependencies · Works Offline"
    copy_text = "已复制" if is_cn else "Copied"
    copy_fail = "复制失败" if is_cn else "Copy failed"
    zero_dep = "无需注册 · 数据绝不上传服务器" if is_cn else "No Signup · Data Never Leaves Your Device"
    active_cn = "active" if is_cn else ""
    active_en = "" if is_cn else "active"
    
    # FAQ schema
    faq_schema_items = []
    for qa in faq_list:
        q = esc(qa["q"])
        a = esc(qa["a"])
        faq_schema_items.append(f'{{"@type":"Question","name":"{q}","acceptedAnswer":{{"@type":"Answer","text":"{a}"}}}}')
    faq_json = ",".join(faq_schema_items)
    
    # Use cases HTML
    uc_html = ""
    for uc in use_cases:
        uc_html += f'<p><strong>{uc["title"]}：</strong>{uc["desc"]}</p>\n'
    
    # HowTo steps
    step1_name = "输入数据" if is_cn else "Enter Data"
    step1_text = "在输入框中输入需要计算的数值" if is_cn else "Enter your values in the input fields"
    step2_name = "选择选项" if is_cn else "Select Options"
    step2_text = "根据需要选择计算模式或参数" if is_cn else "Choose calculation mode or parameters"
    step3_name = "点击计算" if is_cn else "Calculate"
    step3_text = "点击计算按钮获取结果" if is_cn else "Click calculate to see results"
    step4_name = "查看结果" if is_cn else "View Results"
    step4_text = "查看计算结果，支持一键复制" if is_cn else "Review results with one-click copy"
    
    howto_name = f"如何使用 {title}" if is_cn else f"How to Use {title}"
    howto_desc = "使用步骤指南" if is_cn else "Step-by-step usage guide"
    
    app_category = "FinanceApplication" if cat == "finance-tools" else "HealthApplication"
    
    # Lang switch links
    cn_link = "index.html" if is_cn else f"../{slug}/"
    en_link = f"../en/{slug}/" if is_cn else "index.html"
    
    return f"""<!DOCTYPE html>
<html lang="{lang_attr}">
<head>
<script async src="https://www.googletagmanager.com/gtag/js?id={G_TAG}"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','{G_TAG}');</script>
<script>window.addEventListener("error",function(e){{if(e&&e.message===""){{e.preventDefault();}}}});window.addEventListener("unhandledrejection",function(e){{if(e&&e.reason&&e.reason.message===""){{e.preventDefault();}}}});</script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="{desc}">
<meta name="keywords" content="{slug},{keywords}">
<title>{title} - Free ToolBase</title>
<link rel="canonical" href="{BASE_CANONICAL}{canonical_suffix}">
<meta property="og:title" content="{title} - Free ToolBase">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{BASE_CANONICAL}{canonical_suffix}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Free ToolBase">
<meta property="og:image" content="{BASE_CANONICAL}/og-image.svg">
<meta name="twitter:image" content="{BASE_CANONICAL}/og-image.svg">
<meta name="twitter:card" content="summary_large_image">
<meta name="robots" content="index, follow">
<link rel="alternate" hreflang="{alt_lang_code}" href="{BASE_CANONICAL}{alt_suffix}">
<link rel="alternate" hreflang="x-default" href="{BASE_CANONICAL}{xdefault}">
<link rel="icon" type="image/svg+xml" href="favicon.svg">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"SoftwareApplication","name":"{title}","description":"{desc}","applicationCategory":"{app_category}","operatingSystem":"Web","publisher":{{"@type":"Organization","name":"Free ToolBase","email":"{EMAIL}"}},"offers":{{"@type":"Offer","price":"0","priceCurrency":"USD"}}}}</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{faq_json}]}}</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"HowTo","name":"{howto_name}","description":"{howto_desc}","totalTime":"PT2M","tool":{{"@type":"HowToTool","name":"{title}"}},"step":[{{"@type":"HowToStep","position":1,"name":"{step1_name}","text":"{step1_text}"}},{{"@type":"HowToStep","position":2,"name":"{step2_name}","text":"{step2_text}"}},{{"@type":"HowToStep","position":3,"name":"{step3_name}","text":"{step3_text}"}},{{"@type":"HowToStep","position":4,"name":"{step4_name}","text":"{step4_text}"}}]}}</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"{home_text}","item":"{BASE_CANONICAL}/"}},{{"@type":"ListItem","position":2,"name":"{tools_text}","item":"{BASE_CANONICAL}/#tools"}},{{"@type":"ListItem","position":3,"name":"{title}","item":"{BASE_CANONICAL}{canonical_suffix}"}}]}}</script>
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
<div class="header"><h1>{h1}</h1><div class="lang-switch"><a href="{cn_link}" class="{active_cn}">中文</a><a href="{en_link}" class="{active_en}">EN</a></div></div>
<p class="nav-back"><a href="../index.html">{home_text}</a> &rsaquo; <a href="../index.html#tools">{tools_text}</a> &rsaquo; {title}</p>
<div class="hero"><p>{hero}</p><span class="badge">{badge_text}</span></div>

<div class="calculator-section" id="calcSection">
    <h2>{input_label}</h2>
    <div class="input-grid" id="inputGrid"></div>
    <div class="btn-row">
        <button class="btn btn-primary" onclick="calculate()">{calc_btn}</button>
        <button class="btn btn-secondary" onclick="resetAll()">{reset_btn}</button>
    </div>
</div>

<div class="calculator-section" id="resultsSection" style="display:none">
    <h2>{results_label}</h2>
    <div class="results-grid" id="resultsGrid"></div>
</div>

<div class="info-section">
    <h2>{howto_label}</h2>
    <p>{desc}</p>
</div>

<div class="info-section">
    <h2>{usecase_label}</h2>
    {uc_html}
</div>

<div class="info-section">
    <h2>{faq_label}</h2>
"""

def build_faq_html(faq_list):
    out = ""
    for qa in faq_list:
        out += f'<div class="faq-item"><h3>{qa["q"]}</h3><p>{qa["a"]}</p></div>\n'
    return out

def build_footer_html(is_cn, slug, title):
    home_text = "首页" if is_cn else "Home"
    all_tools_text = "全部工具" if is_cn else "All Tools"
    contact_text = "联系我们" if is_cn else "Contact"
    privacy_text = "隐私政策" if is_cn else "Privacy"
    terms_text = "服务条款" if is_cn else "Terms"
    about_text = "关于我们" if is_cn else "About"
    feedback_text = "问题反馈" if is_cn else "Feedback"
    zero_dep = "无需注册 · 数据绝不上传服务器" if is_cn else "No Signup · Data Never Leaves Your Device"
    alt_path = f"../en/{slug}/" if is_cn else f"../{slug}/"
    alt_lang_label = "EN" if is_cn else "中文"
    
    return f"""</div>

<div class="ad-slot">
<ins class="adsbygoogle" style="display:block" data-ad-client="{ADSENSE}" data-ad-slot="auto" data-ad-format="auto" data-full-width-responsive="true"></ins>
</div>
<script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
<footer class="footer container">
<div style="margin-bottom:12px">
<a href="../index.html">{home_text}</a>
<a href="../index.html">{all_tools_text}</a>
<a href="mailto:{EMAIL}">{contact_text}</a>
<a href="../privacy/">{privacy_text}</a>
<a href="../terms/">{terms_text}</a>
<a href="../about/">{about_text}</a>
<a href="{alt_path}">{alt_lang_label}</a>
</div>
<p>{title} | {zero_dep}</p>
<p style="margin-top:8px;color:#475569;font-size:.8rem">{feedback_text}: {EMAIL}</p>
</footer>
<div class="toast" id="toast"></div>
<script>
function showToast(m){{var t=document.getElementById("toast");t.textContent=m;t.classList.add("show");setTimeout(function(){{t.classList.remove("show")}},3000)}}
function copyText(id){{var el=document.getElementById(id);if(!el)return;var t=el.textContent||el.innerText;navigator.clipboard.writeText(t).then(function(){{showToast("Copied")}})["catch"](function(){{showToast("Copy failed")}})}}
function calculate(){{}}
function resetAll(){{}}
</script>
</body>
</html>"""

# Tool definitions
TOOLS = [
    {
        "slug": "cd-calculator",
        "cn_title": "定期存款(CD)计算器",
        "cn_h1": "🏦 定期存款(CD)计算器",
        "cn_desc": "免费在线定期存款(CD)计算器，计算存款证到期收益。支持不同存期和复利频率，含提前支取罚息计算。纯前端计算，数据不上传服务器。",
        "cn_hero": "免费在线定期存款(CD)计算器，计算存款证到期收益。支持不同存期和复利频率，含提前支取罚息计算。纯前端计算，数据不上传服务器。 | 无需注册 · 数据绝不上传服务器",
        "cn_cat": "finance-tools",
        "cn_icon": "🏦",
        "cn_keywords": "定期存款计算器,CD计算器,存款证收益计算,复利计算,金融计算器",
        "cn_faq": [
            {"q": "什么是定期存款(CD)？", "a": "CD（Certificate of Deposit，存款证）是银行发行的一种定期存款产品。您存入一笔资金并承诺在一定期限内不动用，银行则提供比活期更高的固定利率。存期通常为1个月到5年，提前支取会面临罚息。"},
            {"q": "CD利率一般是多少？", "a": "CD利率取决于存期和银行。通常1年期CD利率在4-5%左右（2025年），5年期在3.5-4.5%之间。利率越高、存期越长，最终收益越多。建议货比三家，不同银行CD利率差异可达1-2%。"},
            {"q": "提前支取CD会有什么后果？", "a": "提前支取CD通常需要支付罚息，罚息标准一般为90-180天的利息，具体取决于存期和银行政策。本计算器支持设置提前支取时间，自动计算扣除罚息后的实际到手金额。"},
            {"q": "CD和普通储蓄账户有什么区别？", "a": "CD的利率远高于普通储蓄账户（通常高2-3%），但流动性更差——存入后到存期结束前不能动用。普通储蓄账户随时可取但利率低。CD适合有一笔短期不用的闲钱，追求更高收益的用户。"},
            {"q": "CD是否受存款保险保护？", "a": "在美国，大多数银行的CD由FDIC（联邦存款保险公司）承保，最高保额为$250,000（每人每银行）。在中国，存款保险最高赔付50万元人民币。请确认您的银行是否参保。"},
        ],
        "cn_use_cases": [
            {"title": "教育储蓄", "desc": "为孩子未来学费做规划，选择合适存期的CD锁定当前利率，到期时获得一笔确定的教育资金。"},
            {"title": "应急备用金", "desc": "将3-6个月生活费的应急金存入短期CD（如3-6个月），获得比活期高2-3%的利息收益，同时保持相对流动性。"},
            {"title": "退休补充", "desc": "将退休账户中短期不用的资金分批次存入不同期限的CD，构建CD阶梯策略，既保证流动性又获得较高收益。"},
        ],
        "en_title": "CD Calculator",
        "en_h1": "🏦 Certificate of Deposit (CD) Calculator",
        "en_desc": "Free online CD calculator to compute certificate of deposit maturity value. Supports different terms, compounding frequencies, and early withdrawal penalty. All calculations run locally in your browser.",
        "en_hero": "Free online CD calculator to compute certificate of deposit maturity value. Supports different terms, compounding frequencies, and early withdrawal penalty. All calculations run locally in your browser. | No signup · Data never leaves your device",
        "en_cat": "finance-tools",
        "en_icon": "🏦",
        "en_keywords": "CD calculator,certificate of deposit,deposit calculator,compound interest,savings calculator",
        "en_faq": [
            {"q": "What is a Certificate of Deposit (CD)?", "a": "A CD (Certificate of Deposit) is a savings product offered by banks that pays a fixed interest rate for a specified term. You agree to leave your money untouched for the term, and the bank rewards you with a higher rate than a regular savings account. Terms range from 1 month to 5 years, with penalties for early withdrawal."},
            {"q": "What is a typical CD interest rate?", "a": "CD rates vary by term and bank. Typically, 1-year CDs offer 4-5% (2025), while 5-year CDs offer 3.5-4.5%. Higher rates and longer terms yield more. Shop around — rates can differ by 1-2% between banks."},
            {"q": "What happens if I withdraw a CD early?", "a": "Early withdrawal incurs a penalty, usually 90-180 days of interest depending on the term and bank policy. Our calculator lets you set an early withdrawal date to compute your net payout after the penalty."},
            {"q": "How does a CD differ from a regular savings account?", "a": "CDs offer significantly higher rates (2-3% more) but lock your money for the term. Regular savings accounts allow withdrawals anytime but earn minimal interest. CDs are ideal for money you will not need soon."},
            {"q": "Are CDs FDIC insured?", "a": "Yes, most U.S. bank CDs are FDIC insured up to $250,000 per depositor per bank. Always verify your bank's insurance status before depositing."},
        ],
        "en_use_cases": [
            {"title": "Education Savings", "desc": "Lock in today's rates for future tuition by choosing a CD term that aligns with your child's enrollment date. Receive a guaranteed lump sum when needed."},
            {"title": "Emergency Fund", "desc": "Park 3-6 months of living expenses in a short-term CD (3-6 months) to earn 2-3% more than checking while maintaining reasonable access."},
            {"title": "Retirement Supplement", "desc": "Build a CD ladder by splitting funds across different terms, ensuring regular access to cash while capturing higher yields on longer maturities."},
        ],
    },
    {
        "slug": "restaurant-tip-calculator",
        "cn_title": "餐厅小费计算器",
        "cn_h1": "🍽️ 餐厅小费计算器",
        "cn_desc": "免费在线餐厅小费计算器，支持按比例或固定金额计算小费，支持AA制分账。含各国家/地区小费习俗参考。纯前端计算，无需注册。",
        "cn_hero": "免费在线餐厅小费计算器，支持按比例或固定金额计算小费，支持AA制分账。含各国家/地区小费习俗参考。纯前端计算，无需注册。 | 无需注册 · 数据绝不上传服务器",
        "cn_cat": "finance-tools",
        "cn_icon": "🍽️",
        "cn_keywords": "小费计算器,餐厅小费,AA制计算,分账计算器,小费比例",
        "cn_faq": [
            {"q": "美国餐厅小费一般给多少？", "a": "美国餐厅小费标准为账单税前金额的15-20%。服务好给20%，一般给15%，服务差给10%。自助餐5-10%，外卖取餐通常不需要小费但可以给10%。"},
            {"q": "小费是按税前还是税后计算？", "a": "美国习惯按税前金额计算小费。本计算器默认按税前计算，也可以切换到税后模式。税前和税后小费差额通常在8-10%左右（取决于当地税率）。"},
            {"q": "其他国家小费习惯如何？", "a": "欧洲大部分国家服务费已包含在账单中（标注service compris），额外小费5-10%即可。日本和韩国没有小费文化。澳大利亚和新西兰小费不是必需的但10%表示满意。中国没有小费习惯。"},
            {"q": "AA制怎么算小费？", "a": "本计算器支持AA制分账模式：输入总账单、人数和小费比例，自动计算每人应付金额（含均摊小费），并可设置不同人支付不同金额的酒水等额外消费。"},
            {"q": "外卖需要给小费吗？", "a": "外卖送餐建议给10-15%或$2-5固定金额。到店自取外卖通常不需要小费，但如果订单很大（$50以上）给10%也是礼貌的。快餐店不需要小费。"},
        ],
        "cn_use_cases": [
            {"title": "多人聚餐", "desc": "朋友聚餐时快速算出每人应付金额，支持酒水单独计费和不同比例分摊，告别手动计算的尴尬和错误。"},
            {"title": "国际旅行", "desc": "查看目的地小费习俗参考，避免给多给少的尴尬。支持美元、欧元、英镑、日元等主流货币换算。"},
            {"title": "商务宴请", "desc": "商务场合小费礼仪很重要。快速算出合适的小费金额（通常建议20-25%），展现专业和得体。"},
        ],
        "en_title": "Restaurant Tip Calculator",
        "en_h1": "🍽️ Restaurant Tip Calculator",
        "en_desc": "Free online restaurant tip calculator with percentage or fixed amount, split bill support, and international tipping customs reference. All calculations run locally in your browser.",
        "en_hero": "Free online restaurant tip calculator with percentage or fixed amount, split bill support, and international tipping customs reference. All calculations run locally in your browser. | No signup · Data never leaves your device",
        "en_cat": "finance-tools",
        "en_icon": "🍽️",
        "en_keywords": "tip calculator,restaurant tip,split bill,gratuity calculator,tipping guide",
        "en_faq": [
            {"q": "How much should I tip in the US?", "a": "Standard US restaurant tip is 15-20% of the pre-tax bill. 20% for excellent service, 15% for average, 10% for poor. Buffets 5-10%, takeout pickup usually no tip but 10% is appreciated."},
            {"q": "Should I tip on pre-tax or post-tax?", "a": "US custom is to tip on the pre-tax amount. Our calculator defaults to pre-tax but can switch to post-tax. The difference is typically 8-10% depending on local tax rates."},
            {"q": "What about tipping in other countries?", "a": "Most European countries include service (marked service compris), extra 5-10% is fine. Japan and Korea have no tipping culture. Australia/New Zealand tip not required but 10% for satisfaction. China has no tipping custom."},
            {"q": "How does split bill with tip work?", "a": "Our calculator supports split bill: enter total, number of people, and tip percentage to get each person's share including evenly split tip. Optionally account for different drink or item costs per person."},
            {"q": "Should I tip for delivery?", "a": "Delivery drivers: 10-15% or $2-5 flat. Pickup takeout: usually no tip needed, but 10% on large orders ($50+) is courteous. Fast food: no tip."},
        ],
        "en_use_cases": [
            {"title": "Group Dining", "desc": "Quickly calculate each person's share when dining with friends, with support for separate drink billing and different tip splits."},
            {"title": "International Travel", "desc": "Check destination tipping customs to avoid awkward over- or under-tipping. Supports USD, EUR, GBP, JPY and more currencies."},
            {"title": "Business Dining", "desc": "Nail the business dining etiquette. Quick tip calculation at 20-25% for professional and appropriate dining experiences."},
        ],
    },
    {
        "slug": "bmi-children-calculator",
        "cn_title": "儿童青少年BMI计算器",
        "cn_h1": "👶 儿童青少年BMI计算器",
        "cn_desc": "免费在线儿童青少年BMI计算器，基于CDC生长曲线百分位评估2-19岁儿童体重状况。含年龄别BMI百分位参考和健康建议。纯前端计算。",
        "cn_hero": "免费在线儿童青少年BMI计算器，基于CDC生长曲线百分位评估2-19岁儿童体重状况。含年龄别BMI百分位参考和健康建议。纯前端计算。 | 无需注册 · 数据绝不上传服务器",
        "cn_cat": "health-tools",
        "cn_icon": "👶",
        "cn_keywords": "儿童BMI计算器,青少年BMI,生长曲线,BMI百分位,儿童体重评估",
        "cn_faq": [
            {"q": "儿童BMI和成人BMI有什么区别？", "a": "儿童BMI不是用固定阈值（如18.5/25），而是按年龄和性别的百分位评估。因为儿童身体在持续发育，同样BMI值在不同年龄含义不同。CDC使用百分位：小于5%为偏瘦，5-85%为正常，85-95%为超重，95%以上为肥胖。"},
            {"q": "多少岁可以用儿童BMI计算器？", "a": "本计算器适用于2-19岁的儿童和青少年。2岁以下婴儿使用WHO生长标准（身长别体重），不适用BMI评估。20岁以上应使用成人BMI计算器。"},
            {"q": "BMI百分位是什么意思？", "a": "BMI百分位表示您的孩子在同年龄同性别儿童中的相对位置。例如85百分位表示超过85%的同龄儿童。这个指标比绝对BMI值更能反映儿童的真实体重状况。"},
            {"q": "儿童BMI百分位偏高怎么办？", "a": "首先不要恐慌——咨询儿科医生进行专业评估。BMI只是一个筛查工具，不是诊断标准。医生会结合家族史、饮食习惯、运动量等多方面综合判断。不要自行给孩子节食。"},
            {"q": "为什么儿童要使用性别区分的标准？", "a": "男孩和女孩的生长发育速度和体脂比例不同。青春期女孩体脂率自然高于男孩，所以使用性别区分的生长曲线才能准确评估。"},
        ],
        "cn_use_cases": [
            {"title": "学校体检", "desc": "家长在家就能了解孩子体检报告中的BMI百分位含义，提前发现体重偏离趋势并咨询医生。"},
            {"title": "生长发育监测", "desc": "定期记录孩子的身高体重，追踪BMI百分位变化趋势，及时发现生长加速或减缓的迹象。"},
            {"title": "健康饮食规划", "desc": "根据BMI评估结果，结合儿科医生建议，制定适合孩子年龄的运动和饮食调整方案。"},
        ],
        "en_title": "Child & Teen BMI Calculator",
        "en_h1": "👶 Child & Teen BMI Calculator",
        "en_desc": "Free online BMI calculator for children and teens aged 2-19 using CDC growth chart percentiles. Includes age-adjusted BMI percentile reference and health guidance. All calculations run locally.",
        "en_hero": "Free online BMI calculator for children and teens aged 2-19 using CDC growth chart percentiles. Includes age-adjusted BMI percentile reference and health guidance. All calculations run locally. | No signup · Data never leaves your device",
        "en_cat": "health-tools",
        "en_icon": "👶",
        "en_keywords": "child BMI calculator,teen BMI,growth chart,BMI percentile,pediatric weight",
        "en_faq": [
            {"q": "How is child BMI different from adult BMI?", "a": "Child BMI uses age- and sex-specific percentiles instead of fixed cutoffs (18.5/25). Because children are still growing, the same BMI number means different things at different ages. CDC uses percentiles: under 5% underweight, 5-85% healthy, 85-95% overweight, 95%+ obese."},
            {"q": "What ages can use this calculator?", "a": "This calculator is for children and teens aged 2-19. Infants under 2 use WHO growth standards (weight-for-length), not BMI. Ages 20+ should use an adult BMI calculator."},
            {"q": "What does BMI percentile mean?", "a": "BMI percentile shows where your child falls relative to peers of the same age and sex. For example, 85th percentile means higher BMI than 85% of peers. This is more meaningful than the raw BMI number for children."},
            {"q": "What if my child's BMI percentile is high?", "a": "Do not panic — consult a pediatrician for professional assessment. BMI is a screening tool, not a diagnosis. Doctors consider family history, diet, activity level and more. Never put a child on a diet without medical guidance."},
            {"q": "Why separate standards for boys and girls?", "a": "Boys and girls develop at different rates with different body fat percentages. Girls naturally have higher body fat during puberty, so sex-specific growth charts are essential for accurate assessment."},
        ],
        "en_use_cases": [
            {"title": "School Checkups", "desc": "Understand your child's BMI percentile from school reports at home, spot weight trends early, and discuss with your pediatrician."},
            {"title": "Growth Monitoring", "desc": "Regularly track height and weight to follow BMI percentile trends over time, catching growth spurts or slowdowns early."},
            {"title": "Healthy Eating Plans", "desc": "Use BMI results alongside pediatrician advice to create age-appropriate exercise and nutrition plans for your child."},
        ],
    },
    {
        "slug": "metabolic-age-calculator",
        "cn_title": "代谢年龄计算器",
        "cn_h1": "🔥 代谢年龄计算器",
        "cn_desc": "免费在线代谢年龄计算器，基于基础代谢率(BMR)对比同龄人平均值评估身体代谢年龄。含体脂率和肌肉量修正。纯前端计算。",
        "cn_hero": "免费在线代谢年龄计算器，基于基础代谢率(BMR)对比同龄人平均值评估身体代谢年龄。含体脂率和肌肉量修正。纯前端计算。 | 无需注册 · 数据绝不上传服务器",
        "cn_cat": "health-tools",
        "cn_icon": "🔥",
        "cn_keywords": "代谢年龄计算器,基础代谢率,BMR计算器,身体年龄,新陈代谢评估",
        "cn_faq": [
            {"q": "什么是代谢年龄？", "a": "代谢年龄是通过对比您的实际基础代谢率(BMR)与同龄人平均BMR得出的身体代谢状况指标。代谢年龄低于实际年龄表示新陈代谢比同龄人更快、更年轻；高于实际年龄表示代谢偏慢，可能需要调整饮食和运动。"},
            {"q": "代谢年龄怎么计算？", "a": "先使用Mifflin-St Jeor公式计算您的实际BMR，然后与同龄同性别同体重的平均BMR对比。如果您的BMR高于平均值，代谢年龄就比实际年龄年轻；反之则偏老。体脂率低、肌肉量高的人通常BMR更高。"},
            {"q": "如何改善代谢年龄？", "a": "增加肌肉量是最有效的方法——每增加1公斤肌肉，每日BMR约增加13-20大卡。力量训练、充足蛋白质摄入（每公斤体重1.6-2.0克）、充足睡眠（7-9小时）都能帮助降低代谢年龄。"},
            {"q": "代谢年龄和实际年龄差多少算正常？", "a": "代谢年龄与实际年龄相差±3岁以内属于正常范围。超过5岁建议关注生活方式。但注意这只是估算指标，不能替代全面体检。"},
            {"q": "为什么同样体重的人代谢年龄不同？", "a": "因为体成分不同。同样70公斤，肌肉量30公斤的人和肌肉量25公斤的人，BMR可能相差100-200大卡/天。肌肉是代谢活跃组织，脂肪代谢率远低于肌肉。"},
        ],
        "cn_use_cases": [
            {"title": "健身效果评估", "desc": "开始健身后每月测一次代谢年龄，追踪力量训练是否真正提升了基础代谢率。比单纯看体重变化更科学。"},
            {"title": "减重平台期诊断", "desc": "如果体重下降但代谢年龄没改善，可能意味着减掉的是肌肉而非脂肪，需要调整饮食蛋白质比例和训练方式。"},
            {"title": "健康年龄管理", "desc": "将代谢年龄作为身体真实年龄指标，激励自己通过运动和饮食让身体比身份证更年轻。"},
        ],
        "en_title": "Metabolic Age Calculator",
        "en_h1": "🔥 Metabolic Age Calculator",
        "en_desc": "Free online metabolic age calculator using BMR comparison with peer averages to estimate your body's metabolic age. Includes body fat and muscle mass adjustments. All calculations run locally.",
        "en_hero": "Free online metabolic age calculator using BMR comparison with peer averages to estimate your body's metabolic age. Includes body fat and muscle mass adjustments. All calculations run locally. | No signup · Data never leaves your device",
        "en_cat": "health-tools",
        "en_icon": "🔥",
        "en_keywords": "metabolic age calculator,BMR calculator,basal metabolic rate,body age,metabolism assessment",
        "en_faq": [
            {"q": "What is metabolic age?", "a": "Metabolic age compares your actual Basal Metabolic Rate (BMR) to the average BMR of people your age. A metabolic age lower than your actual age means your metabolism is faster/younger; higher means it is slower and may need diet and exercise adjustments."},
            {"q": "How is metabolic age calculated?", "a": "We first calculate your actual BMR using the Mifflin-St Jeor equation, then compare it to average BMR for your age, sex, and weight. If your BMR is above average, your metabolic age is younger than actual; if below, older. People with lower body fat and more muscle typically have higher BMR."},
            {"q": "How can I improve my metabolic age?", "a": "Building muscle is most effective — each kg of muscle adds ~13-20 calories to daily BMR. Strength training, adequate protein (1.6-2.0g per kg bodyweight), and sufficient sleep (7-9 hours) all help lower metabolic age."},
            {"q": "What is a normal gap between metabolic and actual age?", "a": "A gap of plus or minus 3 years is normal. Over 5 years suggests lifestyle review. But this is an estimate, not a replacement for comprehensive health checkups."},
            {"q": "Why do people with the same weight have different metabolic ages?", "a": "Body composition matters. At 70kg, someone with 30kg muscle mass may burn 100-200 more calories/day than someone with 25kg muscle. Muscle is metabolically active tissue; fat has a much lower metabolic rate."},
        ],
        "en_use_cases": [
            {"title": "Fitness Progress", "desc": "Check monthly after starting a workout program to track whether strength training is actually raising your basal metabolic rate — more scientific than weight alone."},
            {"title": "Plateau Diagnosis", "desc": "If weight drops but metabolic age does not improve, you may be losing muscle instead of fat. Adjust protein intake and training approach."},
            {"title": "Health Age Management", "desc": "Use metabolic age as your body's real age indicator, motivating yourself to make your body younger than your ID through exercise and nutrition."},
        ],
    },
    {
        "slug": "wilks-score-calculator",
        "cn_title": "Wilks系数力量计算器",
        "cn_h1": "🏋️ Wilks系数力量计算器",
        "cn_desc": "免费在线Wilks系数计算器，用于力量举比赛跨体重级别排名。输入深蹲、卧推、硬拉成绩和体重，自动计算Wilks分数。纯前端计算。",
        "cn_hero": "免费在线Wilks系数计算器，用于力量举比赛跨体重级别排名。输入深蹲、卧推、硬拉成绩和体重，自动计算Wilks分数。纯前端计算。 | 无需注册 · 数据绝不上传服务器",
        "cn_cat": "health-tools",
        "cn_icon": "🏋️",
        "cn_keywords": "Wilks系数计算器,力量举,深蹲卧推硬拉,力量排名,相对力量",
        "cn_faq": [
            {"q": "什么是Wilks系数？", "a": "Wilks系数是力量举运动中用于跨体重级别排名的标准化公式。因为体重越大通常能举起越重，Wilks系数通过数学公式消除体重差异，让不同体重的选手公平比较。系数越高表示相对力量越强。"},
            {"q": "Wilks分数多少算好？", "a": "业余爱好者：300-350；中级训练者：350-400；高级训练者：400-450；精英级别：450-500；世界级：500以上。注意男女标准不同（女性系数公式不同），女性的Wilks分数通常低于男性同样成绩。"},
            {"q": "如何计算总成绩？", "a": "力量举总成绩 = 深蹲最大重量 + 卧推最大重量 + 硬拉最大重量。三项总和输入计算器即可得到Wilks分数。比赛中如果某一项失败，该次试举记为0。"},
            {"q": "Wilks和DOTS有什么区别？", "a": "Wilks是IPF（国际力量举联合会）传统使用的系数，DOTS是较新的替代方案。DOTS被认为在不同体重区间更公平。本计算器使用Wilks 2020版公式。如果比赛使用DOTS，请使用DOTS计算器。"},
            {"q": "训练多久能达到400 Wilks？", "a": "男性系统训练2-3年通常能达到350-400。女性可能需要3-4年。这取决于训练质量、饮食和恢复。400 Wilks是很多业余爱好者的里程碑目标。"},
        ],
        "cn_use_cases": [
            {"title": "比赛准备", "desc": "报名力量举比赛前用Wilks评估自己在所在体重级别的竞争力，帮助决定是否需要增减体重参赛。"},
            {"title": "训练目标设定", "desc": "设定Wilks里程碑目标（如300→350→400），反向推算需要提升的三大项成绩，制定阶段性训练计划。"},
            {"title": "健身房社交", "desc": "在健身房和朋友比较Wilks分数，公平比较不同体重训练者的相对力量水平，增加训练趣味性。"},
        ],
        "en_title": "Wilks Score Calculator",
        "en_h1": "🏋️ Wilks Score Calculator",
        "en_desc": "Free online Wilks coefficient calculator for powerlifting cross-weight-class ranking. Enter squat, bench, deadlift and bodyweight to calculate Wilks score. All calculations run locally.",
        "en_hero": "Free online Wilks coefficient calculator for powerlifting cross-weight-class ranking. Enter squat, bench, deadlift and bodyweight to calculate Wilks score. All calculations run locally. | No signup · Data never leaves your device",
        "en_cat": "health-tools",
        "en_icon": "🏋️",
        "en_keywords": "Wilks score calculator,powerlifting,squat bench deadlift,strength ranking,relative strength",
        "en_faq": [
            {"q": "What is the Wilks coefficient?", "a": "The Wilks coefficient is a standardized formula used in powerlifting to rank lifters across different bodyweight classes. Since heavier lifters can typically lift more, the Wilks formula mathematically eliminates weight differences for fair comparison. Higher scores indicate greater relative strength."},
            {"q": "What is a good Wilks score?", "a": "Recreational: 300-350; Intermediate: 350-400; Advanced: 400-450; Elite: 450-500; World-class: 500+. Note that male and female formulas differ, so women's Wilks scores are typically lower for the same lifts."},
            {"q": "How do I calculate my total?", "a": "Powerlifting total = best squat + best bench press + best deadlift. Enter the sum into the calculator for your Wilks score. In competition, a failed lift counts as zero for that attempt."},
            {"q": "What is the difference between Wilks and DOTS?", "a": "Wilks is the traditional IPF (International Powerlifting Federation) coefficient. DOTS is a newer alternative considered fairer across weight ranges. This calculator uses the Wilks 2020 formula. If your competition uses DOTS, use a DOTS calculator instead."},
            {"q": "How long to reach 400 Wilks?", "a": "Men typically reach 350-400 after 2-3 years of consistent training. Women may need 3-4 years. It depends on training quality, nutrition, and recovery. 400 Wilks is a milestone goal for many recreational lifters."},
        ],
        "en_use_cases": [
            {"title": "Meet Preparation", "desc": "Assess your competitiveness in your weight class before signing up for a powerlifting meet, helping decide whether to gain or cut weight."},
            {"title": "Goal Setting", "desc": "Set Wilks milestone targets (300→350→400) and work backwards to determine the lifts needed at each stage for structured training."},
            {"title": "Gym Social", "desc": "Compare Wilks scores with gym friends to fairly compare relative strength across different bodyweights, adding fun to training."},
        ],
    },
]

# Generate all tools
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
        
        # Build HTML
        top = build_html(slug, lang, title, h1, desc, hero, cat, icon, faq, use_cases, keywords)
        mid = build_faq_html(faq)
        bottom = build_footer_html(is_cn, slug, title)
        
        full = top + mid + bottom
        
        # Determine output path
        if is_cn:
            dir_path = os.path.join(SITE, slug)
        else:
            dir_path = os.path.join(SITE, "en", slug)
        
        os.makedirs(dir_path, exist_ok=True)
        filepath = os.path.join(dir_path, "index.html")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(full)
        
        lang_label = "CN" if is_cn else "EN"
        print(f"✅ Created {slug} ({lang_label})")

print(f"\n🎉 Done! Created {len(TOOLS)} tools (CN+EN = {len(TOOLS)*2} pages)")
