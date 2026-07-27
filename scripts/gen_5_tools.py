#!/usr/bin/env python3
"""批量生成5个新工具的中英文页面"""
import os
import json

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ========== 工具定义 ==========
TOOLS = [
    {
        "slug": "bmi-percentile-calculator",
        "name_cn": "儿童BMI百分位计算器",
        "name_en": "BMI Percentile Calculator for Children",
        "desc_cn": "在线儿童和青少年BMI百分位计算器，根据CDC标准按年龄性别评估生长发育，支持2-20岁儿童BMI百分位数和Z-score计算，纯前端本地计算。",
        "desc_en": "Free online BMI Percentile Calculator for children and teens (ages 2-20), using CDC growth charts to calculate BMI percentile and Z-score by age and gender. Pure frontend local calculation.",
        "keywords_cn": "儿童BMI百分位计算器,CDC生长曲线,BMI百分位数,Z-score,儿童肥胖评估,在线工具,免费",
        "keywords_en": "BMI percentile calculator,CDC growth charts,children BMI,Z-score,child obesity assessment,online tool,free",
        "category_cn": "健康",
        "category_en": "Health",
    },
    {
        "slug": "calorie-burned-calculator",
        "name_cn": "运动消耗热量计算器",
        "name_en": "Calories Burned Calculator",
        "desc_cn": "免费在线运动消耗热量计算器，基于MET代谢当量标准计算跑步、游泳、骑行等50+种运动消耗热量，支持体重和时间自定义，科学管理运动减肥。",
        "desc_en": "Free online Calories Burned Calculator using MET values for 50+ activities including running, swimming, cycling. Customize weight and duration for accurate calorie tracking. Pure frontend.",
        "keywords_cn": "运动消耗热量计算器,MET代谢当量,卡路里消耗,运动减肥,跑步消耗热量,在线工具,免费",
        "keywords_en": "calories burned calculator,MET values,exercise calories,calorie tracker,fitness calculator,online tool,free",
        "category_cn": "健康",
        "category_en": "Health",
    },
    {
        "slug": "bmr-calculator-harris-benedict",
        "name_cn": "哈里斯-本尼迪克特基础代谢计算器",
        "name_en": "BMR Calculator - Harris-Benedict Equation",
        "desc_cn": "基于哈里斯-本尼迪克特公式的在线基础代谢率计算器，精确计算静息状态每日消耗热量，支持多种活动水平调整TDEE总消耗，科学指导饮食和运动。",
        "desc_en": "Free BMR calculator using the Harris-Benedict equation. Calculate your resting metabolic rate and TDEE with activity level adjustments. Pure frontend, data stays private.",
        "keywords_cn": "基础代谢率计算器,哈里斯本尼迪克特,BMR,TDEE总消耗,每日热量计算,在线工具,免费",
        "keywords_en": "BMR calculator,Harris-Benedict equation,TDEE calculator,resting metabolic rate,daily calorie needs,online tool,free",
        "category_cn": "健康",
        "category_en": "Health",
    },
    {
        "slug": "cholesterol-units-converter",
        "name_cn": "胆固醇单位换算器",
        "name_en": "Cholesterol Units Converter",
        "desc_cn": "免费在线胆固醇单位换算器，在mmol/L和mg/dL之间快速转换总胆固醇、HDL、LDL和甘油三酯，支持美制和国际单位，方便看懂化验单。",
        "desc_en": "Free Cholesterol Units Converter: instantly convert between mmol/L and mg/dL for total cholesterol, HDL, LDL, and triglycerides. Supports both US and international units. Pure frontend.",
        "keywords_cn": "胆固醇单位换算,mmol/L转mg/dL,血脂换算,总胆固醇换算,HDL LDL换算,在线工具,免费",
        "keywords_en": "cholesterol converter,mmol/L to mg/dL,lipid units converter,HDL LDL conversion,triglycerides converter,online tool,free",
        "category_cn": "健康",
        "category_en": "Health",
    },
    {
        "slug": "roi-calculator-investment",
        "name_cn": "投资回报率计算器",
        "name_en": "Investment ROI Calculator",
        "desc_cn": "免费在线投资回报率计算器，一键计算年化ROI、总回报率和净利润，支持初始投资和最终价值输入，可视化投资表现，帮助做出明智投资决策。",
        "desc_en": "Free Investment ROI Calculator: calculate annualized ROI, total return, and net profit. Input initial investment and final value for instant visualization. Pure frontend, data stays private.",
        "keywords_cn": "投资回报率计算器,ROI计算,年化回报率,投资收益率,投资理财计算器,在线工具,免费",
        "keywords_en": "investment ROI calculator,annualized ROI,return on investment,investment performance,profit calculator,online tool,free",
        "category_cn": "金融",
        "category_en": "Finance",
    },
]


def gen_html(tool, lang="cn"):
    slug = tool["slug"]
    is_cn = lang == "cn"
    name = tool["name_cn"] if is_cn else tool["name_en"]
    desc = tool["desc_cn"] if is_cn else tool["desc_en"]
    kws = tool["keywords_cn"] if is_cn else tool["keywords_en"]
    category = tool["category_cn"] if is_cn else tool["category_en"]
    code = "zh-CN" if is_cn else "en"
    hreflang_self = "zh" if is_cn else "en"
    hreflang_other = "en" if is_cn else "zh"
    prefix = "" if is_cn else "/en"
    other_prefix = "/en" if is_cn else ""

    og_title = f"{name} - Free ToolBase"
    page_title = f"{name} - Free ToolBase | {'免费在线工具' if is_cn else 'Free Online Tool'}"

    return f'''<!DOCTYPE html>
<html lang="{code}">
<head>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-9W1157EBQV"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-9W1157EBQV');</script>
<script>window.addEventListener("error",function(e){{if(e&&e.message===""){{e.preventDefault();}}}});window.addEventListener("unhandledrejection",function(e){{if(e&&e.reason&&e.reason.message===""){{e.preventDefault();}}}});</script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="{desc}">
<meta name="keywords" content="{kws}">
<title>{page_title}</title>
<link rel="canonical" href="https://free-toolbase.com{prefix}/{slug}/">
<meta property="og:title" content="{og_title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="https://free-toolbase.com{prefix}/{slug}/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Free ToolBase">
<meta property="og:image" content="https://free-toolbase.com/og-default.png">
<meta name="robots" content="index, follow">
<link rel="alternate" hreflang="{hreflang_self}" href="https://free-toolbase.com{prefix}/{slug}/">
<link rel="alternate" hreflang="{hreflang_other}" href="https://free-toolbase.com{other_prefix}/{slug}/">
<link rel="alternate" hreflang="x-default" href="https://free-toolbase.com/en/{slug}/">
<link rel="icon" type="image/svg+xml" href="https://free-toolbase.com/favicon.svg">
<script type="application/ld+json">{{"@context": "https://schema.org", "@type": "SoftwareApplication", "name": "{name}", "description": "{desc}", "applicationCategory": "UtilitiesApplication", "operatingSystem": "Web", "publisher": {{"@type": "Organization", "name": "Free ToolBase", "email": "dexshuang@google.com"}}, "offers": {{"@type": "Offer", "price": "0", "priceCurrency": "USD"}}}}</script>
<script type="application/ld+json">{{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{{"@type": "ListItem", "position": 1, "name": "{'首页' if is_cn else 'Home'}", "item": "https://free-toolbase.com{prefix}/"}}, {{"@type": "ListItem", "position": 2, "name": "{'工具' if is_cn else 'Tools'}", "item": "https://free-toolbase.com{prefix}/#tools"}}, {{"@type": "ListItem", "position": 3, "name": "{name}", "item": "https://free-toolbase.com{prefix}/{slug}/"}}]}}</script>
<style>:root{{--primary:#4F46E5;--bg:#0f172a;--surface:#1e293b;--text:#e2e8f0;--muted:#94a3b8;--accent:#06b6d4;--gold:#f1c40f;--border:rgba(148,163,184,.1)}}*{{box-sizing:border-box;margin:0;padding:0}}body{{background:var(--bg);color:var(--text);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,"PingFang SC","Microsoft YaHei",sans-serif;line-height:1.6;min-height:100vh}}a{{color:var(--accent);text-decoration:none}}a:hover{{color:#22d3ee}}.container{{max-width:960px;margin:0 auto;padding:24px 16px}}.header{{display:flex;justify-content:space-between;align-items:center;margin-bottom:24px;flex-wrap:wrap;gap:12px}}.header h1{{font-size:1.5rem;color:var(--gold)}}.lang-switch{{display:flex;gap:4px;background:var(--surface);border-radius:8px;padding:4px;border:1px solid var(--border)}}.lang-switch a{{padding:6px 12px;border-radius:5px;font-size:.85rem;color:var(--muted)}}.lang-switch a.active{{background:rgba(6,182,212,.2);color:#22d3ee}}.nav-back{{color:#64748b;font-size:.85rem;margin-bottom:16px}}.nav-back a{{color:#64748b}}.nav-back a:hover{{color:var(--muted)}}.hero{{margin-bottom:24px}}.hero p{{color:var(--muted);font-size:1rem;margin-bottom:8px}}.badge{{display:inline-block;background:rgba(6,182,212,.15);color:#22d3ee;padding:4px 12px;border-radius:20px;font-size:.8rem;margin-bottom:16px}}.section{{background:var(--surface);border-radius:12px;padding:24px;margin-bottom:16px;border:1px solid var(--border)}}.section h2{{font-size:1.1rem;color:var(--gold);margin-bottom:16px}}.form-group{{margin-bottom:14px}}.form-group label{{display:block;color:var(--muted);font-size:.9rem;margin-bottom:6px;font-weight:500}}.form-group input,.form-group select,.form-group textarea{{width:100%;padding:10px 14px;background:var(--bg);border:1px solid rgba(148,163,184,.2);border-radius:8px;color:var(--text);font-size:.9rem;outline:none;transition:all .2s}}.form-group input:focus,.form-group select:focus,.form-group textarea:focus{{border-color:rgba(6,182,212,.4);box-shadow:0 0 0 3px rgba(6,182,212,.1)}}.form-row{{display:flex;gap:12px;flex-wrap:wrap}}.form-row .form-group{{flex:1;min-width:140px}}.btn-row{{display:flex;gap:10px;flex-wrap:wrap;margin-top:16px}}.btn{{padding:10px 20px;border:none;border-radius:8px;font-size:.9rem;cursor:pointer;font-weight:600;transition:all .2s}}.btn-primary{{background:linear-gradient(135deg,#4F46E5,#7C3AED);color:#fff}}.btn-primary:hover{{transform:translateY(-2px);box-shadow:0 4px 12px rgba(79,70,229,.4)}}.btn-secondary{{background:transparent;border:1px solid var(--border);color:var(--muted)}}.btn-secondary:hover{{border-color:var(--accent);color:var(--text)}}.btn-clear{{background:transparent;border:1px solid rgba(239,68,68,.3);color:#ef4444}}.btn-clear:hover{{background:rgba(239,68,68,.1)}}.btn-copy{{background:rgba(6,182,212,.15);color:var(--accent);border:1px solid rgba(6,182,212,.3)}}.btn-copy:hover{{background:rgba(6,182,212,.25)}}.result-box{{background:var(--bg);border-radius:8px;padding:16px;margin-top:12px;min-height:60px;border:1px solid var(--border)}}.result-box .result-value{{font-size:1.6rem;font-weight:700;color:var(--accent)}}.result-box .result-label{{font-size:.8rem;color:var(--muted);margin-top:4px}}.result-card{{display:flex;align-items:center;gap:16px;padding:16px;background:var(--bg);border-radius:8px;border:1px solid var(--border);margin-bottom:8px}}.result-card .icon{{font-size:2rem}}.result-card .info{{flex:1}}.result-card .value{{font-size:1.2rem;font-weight:700;color:var(--accent)}}.result-card .label{{font-size:.8rem;color:var(--muted)}}.result-card .range{{font-size:.75rem;color:#64748b;margin-top:2px}}.health-tip{{background:rgba(6,182,212,.08);border-left:3px solid var(--accent);border-radius:0 8px 8px 0;padding:12px 16px;margin-top:16px;font-size:.85rem;color:var(--muted)}}.footer{{border-top:1px solid var(--border);padding-top:16px;margin-top:24px;font-size:.8rem;color:#64748b;text-align:center}}.toast{{position:fixed;bottom:24px;left:50%;transform:translateX(-50%);background:#334155;color:#e2e8f0;padding:10px 24px;border-radius:8px;font-size:.9rem;z-index:9999;opacity:0;transition:opacity .3s;pointer-events:none}}.toast.show{{opacity:1}}.ad-space{{margin:16px 0;text-align:center}}@media(max-width:768px){{.container{{padding:16px 12px}}.header h1{{font-size:1.25rem}}.section{{padding:16px}}.form-row{{flex-direction:column}}.form-row .form-group{{min-width:100%}}.result-card{{flex-direction:column;text-align:center}}}}@media(max-width:375px){{.header{{flex-direction:column;align-items:flex-start}}.btn-row{{flex-direction:column}}.btn{{width:100%}}}}</style>
</head>
<body>
<div class="container">
<div class="nav-back"><a href="{prefix}/">&larr; {'返回首页' if is_cn else 'Back to Home'}</a>  /  {name}</div>
<div class="header">
<h1>{name}</h1>
<div class="lang-switch">
<a href="{prefix}/{slug}/"{' class="active"' if is_cn else ''}>{'中文' if is_cn else '中文'}</a>
<a href="{other_prefix}/{slug}/"{' class="active"' if not is_cn else ''}>{'EN' if is_cn else 'EN'}</a>
</div>
</div>
<div class="hero">
<span class="badge">{category}</span>
<p>{desc}</p>
</div>

<!-- PLACEHOLDER: 工具交互区 -->

<div class="section" id="tool-section">
<h2>{'计算器' if is_cn else 'Calculator'}</h2>
<div id="tool-content">
<p style="color:var(--muted);text-align:center;padding:40px">{'正在加载...' if is_cn else 'Loading...'}</p>
</div>
</div>

<div class="footer">
<p>{'纯前端计算 · 数据不上传 · 完全免费' if is_cn else 'Pure frontend · Data stays private · 100% Free'}</p>
<p>&copy; 2025 Free ToolBase</p>
</div>
</div>
<div class="toast" id="toast"></div>

<script>
// Toast
function showToast(msg) {{
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.classList.add('show');
  setTimeout(() => t.classList.remove('show'), 2000);
}}

// Copy
function copyResult(text) {{
  if (navigator.clipboard) {{
    navigator.clipboard.writeText(text).then(() => showToast('{'已复制' if is_cn else 'Copied!'}'));
  }} else {{
    const ta = document.createElement('textarea');
    ta.value = text;
    document.body.appendChild(ta);
    ta.select();
    document.execCommand('copy');
    document.body.removeChild(ta);
    showToast('{'已复制' if is_cn else 'Copied!'}');
  }}
}}

// === TOOL-SPECIFIC JS ===
// (Will be injected)

// === RELATED TOOLS ===
const lang = '{lang}';
const relatedTools = [];
// (Will be injected)

function renderRelated() {{
  if (relatedTools.length === 0) return;
  const section = document.createElement('div');
  section.className = 'section';
  section.innerHTML = '<h2>{'相关工具' if is_cn else 'Related Tools'}</h2><div style="display:flex;flex-wrap:wrap;gap:8px" id="related-container"></div>';
  const container = section.querySelector('#related-container');
  relatedTools.forEach(t => {{
    const a = document.createElement('a');
    a.href = (lang === 'en' ? '/en/' : '/') + t.slug + '/';
    a.style.cssText = 'background:rgba(6,182,212,.1);color:var(--accent);padding:6px 14px;border-radius:20px;font-size:.85rem;text-decoration:none;transition:all .2s';
    a.textContent = t.name;
    a.onmouseenter = function(){{this.style.background='rgba(6,182,212,.25)';}};
    a.onmouseleave = function(){{this.style.background='rgba(6,182,212,.1)';}};
    container.appendChild(a);
  }});
  document.getElementById('tool-section').after(section);
}}

// Init
document.addEventListener('DOMContentLoaded', () => {{
  initTool();
  renderRelated();
}});
</script>
</body>
</html>'''


def main():
    for tool in TOOLS:
        slug = tool["slug"]
        # CN
        cn_dir = os.path.join(SITE, slug)
        os.makedirs(cn_dir, exist_ok=True)
        cn_html = gen_html(tool, "cn")
        with open(os.path.join(cn_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(cn_html)

        # EN
        en_dir = os.path.join(SITE, "en", slug)
        os.makedirs(en_dir, exist_ok=True)
        en_html = gen_html(tool, "en")
        with open(os.path.join(en_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(en_html)

        print(f"✅ {slug} CN+EN 已生成")

if __name__ == "__main__":
    main()
