#!/usr/bin/env python3
"""批量生成5个新工具：CN + EN 页面"""
import os

BASE_DIR = "/home/chison/tools-site"

# Google Analytics代码
GA_CODE = '''<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-9W1157EBQV"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','G-9W1157EBQV');</script>
<script>window.addEventListener("error",function(e){if(e&&e.message===""){e.preventDefault();}});window.addEventListener("unhandledrejection",function(e){if(e&&e.reason&&e.reason.message===""){e.preventDefault();}});</script>'''

# 通用CSS
CSS = '''*{box-sizing:border-box;margin:0;padding:0}
body{background:#0f172a;color:#e2e8f0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,"PingFang SC","Microsoft YaHei",sans-serif;line-height:1.6}
a{color:#06b6d4;text-decoration:none}
.container{max-width:1200px;margin:0 auto;padding:0 16px}
.breadcrumb{color:#94a3b8;font-size:13px;padding:12px 0}
.breadcrumb a{color:#94a3b8;text-decoration:none}
.breadcrumb a:hover{color:#e2e8f0}
.hero{background:linear-gradient(135deg,#0c4a6e,#0f172a);border-radius:16px;padding:32px 24px;margin-bottom:24px;text-align:center;border:1px solid rgba(6,182,212,.15)}
h1{font-size:2rem;color:#f1f5f9;margin-bottom:8px}
.subtitle{color:#94a3b8;font-size:.95rem}
.badge{background:rgba(16,185,129,.15);color:#10b981;padding:4px 12px;border-radius:20px;font-size:.8rem;display:inline-block;margin-top:8px;border:1px solid rgba(16,185,129,.2)}
.panel{background:#1e293b;border-radius:16px;padding:24px;border:1px solid rgba(148,163,184,.1);margin-bottom:20px}
.panel-title{font-size:1rem;color:#f1f5f9;margin-bottom:16px;font-weight:600}
.input-group{margin-bottom:12px}
.input-group label{display:block;color:#94a3b8;font-size:.85rem;margin-bottom:6px}
.input-group input,.input-group select{width:100%;background:#0f172a;border:1px solid rgba(148,163,184,.2);border-radius:10px;color:#e2e8f0;padding:10px 14px;font-size:.9rem}
.input-group input:focus,.input-group select:focus{outline:none;border-color:#06b6d4}
.btn-group{display:flex;gap:10px;margin-top:16px;flex-wrap:wrap}
.btn{padding:10px 20px;border-radius:10px;border:none;font-size:.9rem;font-weight:500;cursor:pointer;transition:all .2s;white-space:nowrap}
.btn:disabled{opacity:.5;cursor:not-allowed}
.btn-primary{background:#06b6d4;color:#0f172a}
.btn-primary:hover:not(:disabled){background:#22d3ee;transform:translateY(-1px)}
.btn-secondary{background:#334155;color:#e2e8f0}
.btn-secondary:hover:not(:disabled){background:#475569}
.btn-success{background:rgba(16,185,129,.15);color:#10b981;border:1px solid rgba(16,185,129,.2)}
.btn-success:hover:not(:disabled){background:rgba(16,185,129,.25)}
.btn-danger{background:rgba(239,68,68,.15);color:#ef4444;border:1px solid rgba(239,68,68,.2)}
.btn-danger:hover:not(:disabled){background:rgba(239,68,68,.25)}
.privacy-note{background:rgba(16,185,129,.08);border:1px solid rgba(16,185,129,.15);border-radius:10px;padding:12px 16px;margin-top:16px;color:#10b981;font-size:.85rem}
.result-box{background:#0f172a;border:1px solid rgba(148,163,184,.2);border-radius:10px;padding:16px;margin-top:16px}
.result-item{display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid rgba(148,163,184,.1)}
.result-item:last-child{border-bottom:none}
.result-label{color:#94a3b8;font-size:.85rem}
.result-value{color:#f1f5f9;font-weight:600;font-size:1.1rem}
.result-highlight{color:#10b981;font-size:1.3rem}
footer{text-align:center;padding:40px 0;color:#64748b;font-size:.85rem;margin-top:40px}
footer a{color:#06b6d4}
@media(max-width:640px){h1{font-size:1.5rem}.panel{padding:16px}}'''

def gen_seo_meta(slug, title_cn, desc_cn, title_en, desc_en):
    return f'''<meta name="description" content="{desc_cn}">
<meta name="keywords" content="{slug},工具,在线工具,免费">
<title>{title_cn} - Free ToolBase</title>
<link rel="canonical" href="https://free-toolbase.com/{slug}/">
<meta property="og:title" content="{title_cn} - Free ToolBase">
<meta property="og:description" content="{desc_cn}">
<meta property="og:url" content="https://free-toolbase.com/{slug}/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Free ToolBase">
<link rel="alternate" hreflang="zh" href="https://free-toolbase.com/{slug}/">
<link rel="alternate" hreflang="en" href="https://free-toolbase.com/en/{slug}/">
<link rel="alternate" hreflang="x-default" href="https://free-toolbase.com/en/{slug}/">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"SoftwareApplication","name":"{title_cn}","description":"{desc_cn}","applicationCategory":"UtilitiesApplication","operatingSystem":"Web","publisher":{{"@type":"Organization","name":"Free ToolBase","email":"dexshuang@google.com"}},"offers":{{"@type":"Offer","price":"0","priceCurrency":"USD"}}}}</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"首页","item":"https://free-toolbase.com/"}},{{"@type":"ListItem","position":2,"name":"工具","item":"https://free-toolbase.com/#tools"}},{{"@type":"ListItem","position":3,"name":"{title_cn}","item":"https://free-toolbase.com/{slug}/"}}]}}</script>'''

def gen_en_seo_meta(slug, title, desc):
    return f'''<meta name="description" content="{desc}">
<meta name="keywords" content="{slug},tool,online tool,free">
<title>{title} - Free ToolBase</title>
<link rel="canonical" href="https://free-toolbase.com/en/{slug}/">
<meta property="og:title" content="{title} - Free ToolBase">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="https://free-toolbase.com/en/{slug}/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Free ToolBase">
<link rel="alternate" hreflang="zh" href="https://free-toolbase.com/{slug}/">
<link rel="alternate" hreflang="en" href="https://free-toolbase.com/en/{slug}/">
<link rel="alternate" hreflang="x-default" href="https://free-toolbase.com/en/{slug}/">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"SoftwareApplication","name":"{title}","description":"{desc}","applicationCategory":"UtilitiesApplication","operatingSystem":"Web","publisher":{{"@type":"Organization","name":"Free ToolBase","email":"dexshuang@google.com"}},"offers":{{"@type":"Offer","price":"0","priceCurrency":"USD"}}}}</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"Home","item":"https://free-toolbase.com/en/"}},{{"@type":"ListItem","position":2,"name":"Tools","item":"https://free-toolbase.com/en/#tools"}},{{"@type":"ListItem","position":3,"name":"{title}","item":"https://free-toolbase.com/en/{slug}/"}}]}}</script>'''

# === TOOL 1: Capital Gains Tax Calculator ===
tool1_cn = {
    "slug": "capital-gains-tax-calculator",
    "title_cn": "资本利得税计算器",
    "desc_cn": "免费在线资本利得税计算器，计算股票、房产等资产出售后的资本利得税。支持短期和长期资本利得，2026年最新税率，无需注册。",
    "title_en": "Capital Gains Tax Calculator",
    "desc_en": "Free online capital gains tax calculator. Calculate tax on profits from selling stocks, real estate and other assets. Supports short-term and long-term capital gains with 2026 tax rates.",
    "hero_title": "📊 资本利得税计算器",
    "hero_subtitle": "计算股票、房产等资产出售后的资本利得税",
    "panel_title": "输入交易信息",
    "inputs": [
        ("purchase-price", "number", "买入价格 ($)", "0", "100"),
        ("sell-price", "number", "卖出价格 ($)", "0", "100"),
        ("holding-period", "select", "持有期限", "short", [("short", "短期（≤1年）"), ("long", "长期（>1年）")]),
        ("tax-rate", "number", "适用税率 (%)", "15", "0,100"),
        ("state-tax", "number", "州税率 (%)", "0", "0,100"),
    ],
    "result_items": [
        ("capital-gain", "资本利得"),
        ("federal-tax", "联邦税"),
        ("state-tax-amount", "州税"),
        ("net-proceeds", "净收益"),
    ],
    "faq": [
        ("什么是资本利得税？", "资本利得税是对出售资产（如股票、房产、加密货币等）所获利润征收的税。短期资本利得（持有≤1年）按普通所得税率征税，长期资本利得（持有>1年）享受优惠税率。"),
        ("2026年美国联邦资本利得税率是多少？", "2026年长期资本利得税率为0%、15%或20%，取决于应税收入。短期资本利得按普通所得税率（10%-37%）征收。此外，高收入者可能还需缴纳3.8%的净投资收入税（NIIT）。"),
    ],
    "steps": [
        ("输入买入价格", "输入资产的买入价格（成本基础）"),
        ("输入卖出价格", "输入资产的卖出价格"),
        ("选择持有期限", "选择短期（≤1年）或长期（>1年）"),
        ("查看计算结果", "查看资本利得、联邦税、州税和净收益"),
    ],
}

# === TOOL 2: Self Employment Tax Calculator ===
tool2_cn = {
    "slug": "self-employment-tax-calculator",
    "title_cn": "自雇税计算器",
    "desc_cn": "免费在线自雇税计算器，计算自由职业者、独立承包商的自雇税（社会保障税+医疗保险税）。支持2026年最新税率，无需注册。",
    "title_en": "Self Employment Tax Calculator",
    "desc_en": "Free online self-employment tax calculator for freelancers and independent contractors. Calculate Social Security and Medicare taxes with 2026 rates. No registration required.",
    "hero_title": "💼 自雇税计算器",
    "hero_subtitle": "计算自由职业者和独立承包商的自雇税",
    "panel_title": "输入收入信息",
    "inputs": [
        ("net-income", "number", "净自雇收入 ($)", "50000", "0"),
        ("tax-year", "select", "纳税年度", "2026", [("2024","2024"),("2025","2025"),("2026","2026")]),
    ],
    "result_items": [
        ("social-security", "社会保障税 (12.4%)"),
        ("medicare", "医疗保险税 (2.9%)"),
        ("total-se-tax", "自雇税合计"),
        ("effective-rate", "有效税率"),
        ("after-tax", "税后收入"),
    ],
    "faq": [
        ("什么是自雇税？", "自雇税是自由职业者、独立承包商等自雇人士需要缴纳的社会保障税和医疗保险税。2026年自雇税率为15.3%，其中社会保障税12.4%（收入上限$176,100），医疗保险税2.9%（无上限）。"),
        ("谁需要缴纳自雇税？", "年自雇净收入超过$400的个人需要缴纳自雇税。包括自由职业者、独立承包商、小型企业主等。"),
    ],
    "steps": [
        ("输入净自雇收入", "输入您的年净自雇收入"),
        ("选择纳税年度", "选择适用的纳税年度"),
        ("查看计算结果", "查看社会保障税、医疗保险税和有效税率"),
    ],
}

# === TOOL 3: A1C Calculator ===
tool3_cn = {
    "slug": "a1c-calculator",
    "title_cn": "糖化血红蛋白（HbA1c）计算器",
    "desc_cn": "免费在线糖化血红蛋白计算器，将HbA1c百分比转换为平均血糖值，帮助糖尿病管理和血糖监测。支持mmol/L和mg/dL两种单位。",
    "title_en": "HbA1c Calculator",
    "desc_en": "Free online HbA1c calculator to convert A1C percentage to estimated average glucose (eAG). Supports both mmol/L and mg/dL units for diabetes management.",
    "hero_title": "🩸 糖化血红蛋白（HbA1c）计算器",
    "hero_subtitle": "将HbA1c百分比转换为平均血糖值",
    "panel_title": "输入HbA1c值",
    "inputs": [
        ("a1c", "number", "HbA1c (%)", "6.5", "3,20", "0.1"),
        ("unit", "select", "血糖单位", "mgdl", [("mgdl","mg/dL"),("mmol","mmol/L")]),
    ],
    "result_items": [
        ("eag", "估算平均血糖 (eAG)"),
        ("category", "血糖控制水平"),
    ],
    "faq": [
        ("什么是HbA1c？", "HbA1c（糖化血红蛋白）反映过去2-3个月的平均血糖水平。正常值低于5.7%，糖尿病前期为5.7%-6.4%，糖尿病≥6.5%。"),
        ("eAG是什么意思？", "eAG（估算平均血糖）是将HbA1c百分比转换为日常血糖监测单位的值。公式：eAG(mg/dL) = 28.7 × A1C - 46.7。"),
    ],
    "steps": [
        ("输入HbA1c值", "输入您的糖化血红蛋白百分比值"),
        ("选择血糖单位", "选择mg/dL或mmol/L"),
        ("查看计算结果", "查看估算平均血糖值和血糖控制水平评估"),
    ],
}

# === TOOL 4: Calorie Deficit Calculator ===
tool4_cn = {
    "slug": "calorie-deficit-calculator",
    "title_cn": "热量缺口计算器",
    "desc_cn": "免费在线热量缺口计算器，根据目标计算每日应摄入的热量。支持减重、维持和增重三种模式，科学管理体重。",
    "title_en": "Calorie Deficit Calculator",
    "desc_en": "Free online calorie deficit calculator to determine daily calorie intake for weight loss, maintenance, or gain goals. Science-based weight management tool.",
    "hero_title": "🔥 热量缺口计算器",
    "hero_subtitle": "科学计算减重所需的每日热量缺口",
    "panel_title": "输入个人信息",
    "inputs": [
        ("weight", "number", "体重 (kg)", "70", "30,300", "0.1"),
        ("height", "number", "身高 (cm)", "170", "100,250"),
        ("age", "number", "年龄", "30", "1,120"),
        ("gender", "select", "性别", "male", [("male","男性"),("female","女性")]),
        ("activity", "select", "活动水平", "moderate", [("sedentary","久坐不动"),("light","轻度活动"),("moderate","中度活动"),("active","积极运动"),("very-active","高强度运动")]),
        ("goal", "select", "目标", "lose", [("lose","减重"),("maintain","维持"),("gain","增重")]),
        ("deficit", "number", "每日热量缺口 (kcal)", "500", "100,1500", "50"),
    ],
    "result_items": [
        ("bmr", "基础代谢率 (BMR)"),
        ("tdee", "每日总能量消耗 (TDEE)"),
        ("target-calories", "目标每日摄入"),
        ("weekly-change", "预计每周体重变化"),
    ],
    "faq": [
        ("什么是热量缺口？", "热量缺口是指每日消耗的热量与摄入热量之间的差值。500kcal/天的缺口可减重约0.5kg/周，1000kcal/天的缺口可减重约1kg/周。"),
        ("什么是BMR和TDEE？", "BMR（基础代谢率）是身体在完全静止状态下消耗的热量。TDEE（每日总能量消耗）是BMR加上日常活动和运动消耗的总热量。"),
    ],
    "steps": [
        ("输入个人信息", "输入体重、身高、年龄和性别"),
        ("选择活动水平", "选择日常活动水平"),
        ("选择目标", "选择减重、维持或增重目标"),
        ("设置热量缺口", "设置每日热量缺口（建议300-1000kcal）"),
        ("查看计算结果", "查看BMR、TDEE、目标摄入和预计体重变化"),
    ],
}

# === TOOL 5: Cholesterol Ratio Calculator ===
tool5_cn = {
    "slug": "cholesterol-ratio-calculator",
    "title_cn": "胆固醇比率计算器",
    "desc_cn": "免费在线胆固醇比率计算器，计算总胆固醇/HDL、LDL/HDL、甘油三酯/HDL比率，评估心血管疾病风险。支持mg/dL和mmol/L两种单位。",
    "title_en": "Cholesterol Ratio Calculator",
    "desc_en": "Free online cholesterol ratio calculator. Calculate Total/HDL, LDL/HDL, and Triglyceride/HDL ratios to assess cardiovascular disease risk. Supports both mg/dL and mmol/L.",
    "hero_title": "❤️ 胆固醇比率计算器",
    "hero_subtitle": "评估心血管疾病风险的胆固醇比率分析",
    "panel_title": "输入血脂数据",
    "inputs": [
        ("total-cholesterol", "number", "总胆固醇", "200", "50,500"),
        ("hdl", "number", "HDL胆固醇（好胆固醇）", "50", "10,150"),
        ("ldl", "number", "LDL胆固醇（坏胆固醇）", "120", "10,300"),
        ("triglycerides", "number", "甘油三酯", "150", "30,1000"),
        ("unit", "select", "单位", "mgdl", [("mgdl","mg/dL"),("mmol","mmol/L")]),
    ],
    "result_items": [
        ("tc-hdl", "总胆固醇/HDL比率"),
        ("ldl-hdl", "LDL/HDL比率"),
        ("tg-hdl", "甘油三酯/HDL比率"),
        ("tc-hdl-assessment", "总胆固醇/HDL评估"),
        ("ldl-hdl-assessment", "LDL/HDL评估"),
        ("tg-hdl-assessment", "甘油三酯/HDL评估"),
    ],
    "faq": [
        ("什么是胆固醇比率？", "胆固醇比率是评估心血管疾病风险的重要指标。总胆固醇/HDL比率理想值<3.5，LDL/HDL比率理想值<2.5，甘油三酯/HDL比率理想值<2.0。"),
        ("为什么胆固醇比率比单项指标更重要？", "胆固醇比率综合考虑了'好胆固醇'和'坏胆固醇'的平衡，比单独的胆固醇数值更能反映心血管疾病风险。"),
    ],
    "steps": [
        ("输入血脂数据", "输入总胆固醇、HDL、LDL和甘油三酯数值"),
        ("选择单位", "选择mg/dL或mmol/L"),
        ("查看计算结果", "查看各项胆固醇比率和风险评估"),
    ],
}

TOOLS = [tool1_cn, tool2_cn, tool3_cn, tool4_cn, tool5_cn]

def gen_html(tool, lang="cn"):
    """生成工具HTML"""
    if lang == "cn":
        seo = gen_seo_meta(tool["slug"], tool["title_cn"], tool["desc_cn"], tool["title_en"], tool["desc_en"])
        hero_title = tool["hero_title"]
        hero_sub = tool["hero_subtitle"]
        panel_title = tool["panel_title"]
        breadcrumb_home = "首页"
        breadcrumb_tools = "工具"
        breadcrumb_current = tool["title_cn"]
        html_lang = "zh-CN"
        labels = {
            "calculate": "计算",
            "clear": "清空",
            "privacy": "🔒 所有计算均在浏览器本地完成，数据不会上传到服务器",
            "home": "首页",
            "about": "关于",
            "privacy_link": "隐私政策",
            "copyright": f"© 2026 Free ToolBase. 保留所有权利。",
            "result_label": "计算结果",
        }
    else:
        seo = gen_en_seo_meta(tool["slug"], tool["title_en"], tool["desc_en"])
        hero_title = tool["hero_title"]
        hero_sub = tool["hero_subtitle"]
        panel_title = tool["panel_title"]
        breadcrumb_home = "Home"
        breadcrumb_tools = "Tools"
        breadcrumb_current = tool["title_en"]
        html_lang = "en"
        labels = {
            "calculate": "Calculate",
            "clear": "Clear",
            "privacy": "🔒 All calculations are done locally in your browser. No data is uploaded.",
            "home": "Home",
            "about": "About",
            "privacy_link": "Privacy Policy",
            "copyright": f"© 2026 Free ToolBase. All rights reserved.",
            "result_label": "Results",
        }

    # Input fields HTML
    inputs_html = ""
    for inp in tool["inputs"]:
        name, itype, label, default, extra = inp[0], inp[1], inp[2], inp[3], inp[4]
        if itype == "select":
            options = "".join([f'<option value="{v}">{t}</option>' for v, t in extra])
            inputs_html += f'''<div class="input-group">
<label for="{name}">{label}</label>
<select id="{name}">{options}</select>
</div>\n'''
        else:
            step = f' step="{extra}"' if extra else ""
            min_attr = ""
            max_attr = ""
            if extra and "," in str(extra):
                parts = extra.split(",")
                min_attr = f' min="{parts[0]}"' if parts[0] else ""
                max_attr = f' max="{parts[1]}"' if parts[1] else ""
            inputs_html += f'''<div class="input-group">
<label for="{name}">{label}</label>
<input type="{itype}" id="{name}" value="{default}"{min_attr}{max_attr}{step}>
</div>\n'''

    # Result items
    result_items_html = ""
    for rid, rlabel in tool["result_items"]:
        result_items_html += f'<div class="result-item"><span class="result-label">{rlabel}</span><span class="result-value" id="{rid}">-</span></div>\n'

    # FAQ
    faq_html = ""
    for q, a in tool["faq"]:
        faq_html += f'''<details style="margin-bottom:12px">
<summary style="cursor:pointer;color:#06b6d4;font-weight:500">{q}</summary>
<p style="color:#94a3b8;margin-top:8px;font-size:.9rem;line-height:1.7">{a}</p>
</details>\n'''

    # Steps
    steps_html = ""
    for i, (step_title, step_desc) in enumerate(tool["steps"], 1):
        steps_html += f'''<div style="display:flex;gap:12px;align-items:flex-start;padding:10px 0;border-bottom:1px solid rgba(148,163,184,.1)">
<div style="background:#06b6d4;color:#0f172a;width:28px;height:28px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:.85rem;flex-shrink:0">{i}</div>
<div><strong style="color:#e2e8f0">{step_title}</strong><p style="color:#94a3b8;font-size:.85rem;margin-top:4px">{step_desc}</p></div>
</div>\n'''

    html = f'''<!DOCTYPE html>
<html lang="{html_lang}">
<head>
{GA_CODE}
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
{seo}
<style>
{CSS}
</style>
</head>
<body>
<div class="container">
<nav class="breadcrumb">
<a href="{"/" if lang == "cn" else "/en/"}">{labels["home"]}</a> › 
<a href="{"/#tools" if lang == "cn" else "/en/#tools"}">{breadcrumb_tools}</a> › 
<span>{breadcrumb_current}</span>
</nav>

<div class="hero">
<h1>{hero_title}</h1>
<p class="subtitle">{hero_sub}</p>
<span class="badge">🆓 免费使用</span>
</div>

<div class="panel">
<h2 class="panel-title">{panel_title}</h2>
{inputs_html}
<div class="btn-group">
<button class="btn btn-primary" onclick="calculate()">{labels["calculate"]}</button>
<button class="btn btn-secondary" onclick="clearAll()">{labels["clear"]}</button>
</div>
<div class="privacy-note">{labels["privacy"]}</div>
</div>

<div class="panel" id="result-panel" style="display:none">
<h2 class="panel-title">{labels["result_label"]}</h2>
<div class="result-box">
{result_items_html}
</div>
</div>

<div class="panel">
<h2 class="panel-title">📖 常见问题</h2>
{faq_html}
</div>

<div class="panel">
<h2 class="panel-title">📝 使用步骤</h2>
{steps_html}
</div>

<footer>
<p><a href="{"/" if lang == "cn" else "/en/"}">{labels["home"]}</a> | <a href="{"/about/" if lang == "cn" else "/en/about/"}">{labels["about"]}</a> | <a href="{"/privacy/" if lang == "cn" else "/en/privacy/"}">{labels["privacy_link"]}</a></p>
<p>{labels["copyright"]}</p>
</footer>
</div>
<script>
{gen_js(tool)}
</script>
</body>
</html>'''
    return html

def gen_js(tool):
    """生成每个工具的JS逻辑"""
    slug = tool["slug"]
    
    if slug == "capital-gains-tax-calculator":
        return '''function calculate(){
const p=parseFloat(document.getElementById('purchase-price').value)||0;
const s=parseFloat(document.getElementById('sell-price').value)||0;
const period=document.getElementById('holding-period').value;
const taxRate=parseFloat(document.getElementById('tax-rate').value)||15;
const stateTax=parseFloat(document.getElementById('state-tax').value)||0;
const gain=s-p;
let fedTax;
if(period==='short'){fedTax=gain*(taxRate/100);}
else{fedTax=gain*(taxRate/100);}
const stTax=gain*(stateTax/100);
const net=gain-fedTax-stTax;
document.getElementById('capital-gain').textContent='$'+gain.toFixed(2);
document.getElementById('federal-tax').textContent='$'+fedTax.toFixed(2);
document.getElementById('state-tax-amount').textContent='$'+stTax.toFixed(2);
document.getElementById('net-proceeds').textContent='$'+net.toFixed(2);
document.getElementById('result-panel').style.display='block';
}
function clearAll(){
['purchase-price','sell-price','tax-rate','state-tax'].forEach(id=>document.getElementById(id).value=id==='tax-rate'?'15':id==='state-tax'?'0':'0');
document.getElementById('holding-period').value='short';
document.getElementById('result-panel').style.display='none';
}'''

    elif slug == "self-employment-tax-calculator":
        return '''function calculate(){
const income=parseFloat(document.getElementById('net-income').value)||0;
const year=parseInt(document.getElementById('tax-year').value);
let ssLimit=176100;
if(year===2024)ssLimit=168600;
else if(year===2025)ssLimit=174900;
const ssIncome=Math.min(income,ssLimit);
const ssTax=ssIncome*0.124;
const medTax=income*0.029;
const total=ssTax+medTax;
const effRate=income>0?(total/income*100).toFixed(1):'0.0';
const after=income-total;
document.getElementById('social-security').textContent='$'+ssTax.toFixed(2);
document.getElementById('medicare').textContent='$'+medTax.toFixed(2);
document.getElementById('total-se-tax').textContent='$'+total.toFixed(2);
document.getElementById('effective-rate').textContent=effRate+'%';
document.getElementById('after-tax').textContent='$'+after.toFixed(2);
document.getElementById('result-panel').style.display='block';
}
function clearAll(){
document.getElementById('net-income').value='50000';
document.getElementById('tax-year').value='2026';
document.getElementById('result-panel').style.display='none';
}'''

    elif slug == "a1c-calculator":
        return '''function calculate(){
const a1c=parseFloat(document.getElementById('a1c').value)||0;
const unit=document.getElementById('unit').value;
let eag,cat;
if(unit==='mgdl'){
eag=28.7*a1c-46.7;
if(a1c<5.7)cat='✅ 正常 (Normal)';
else if(a1c<6.5)cat='⚠️ 糖尿病前期 (Prediabetes)';
else cat='🔴 糖尿病范围 (Diabetes)';
}else{
eag=(28.7*a1c-46.7)/18.018;
if(a1c<5.7)cat='✅ 正常 (Normal)';
else if(a1c<6.5)cat='⚠️ 糖尿病前期 (Prediabetes)';
else cat='🔴 糖尿病范围 (Diabetes)';
}
document.getElementById('eag').textContent=eag.toFixed(1)+' '+unit.replace('mgdl','mg/dL').replace('mmol','mmol/L');
document.getElementById('category').innerHTML=cat;
document.getElementById('result-panel').style.display='block';
}
function clearAll(){
document.getElementById('a1c').value='6.5';
document.getElementById('unit').value='mgdl';
document.getElementById('result-panel').style.display='none';
}'''

    elif slug == "calorie-deficit-calculator":
        return '''function calculate(){
const w=parseFloat(document.getElementById('weight').value)||0;
const h=parseFloat(document.getElementById('height').value)||0;
const a=parseInt(document.getElementById('age').value)||0;
const g=document.getElementById('gender').value;
const act=document.getElementById('activity').value;
const goal=document.getElementById('goal').value;
const deficit=parseFloat(document.getElementById('deficit').value)||500;
let bmr;
if(g==='male'){bmr=10*w+6.25*h-5*a+5;}
else{bmr=10*w+6.25*h-5*a-161;}
const actM={sedentary:1.2,light:1.375,moderate:1.55,active:1.725,'very-active':1.9};
const tdee=bmr*actM[act];
let target;
if(goal==='lose'){target=tdee-deficit;}
else if(goal==='gain'){target=tdee+deficit;}
else{target=tdee;}
const weekly=(target-tdee)*7/7700;
document.getElementById('bmr').textContent=Math.round(bmr)+' kcal';
document.getElementById('tdee').textContent=Math.round(tdee)+' kcal';
document.getElementById('target-calories').textContent=Math.round(target)+' kcal';
document.getElementById('weekly-change').textContent=weekly.toFixed(2)+' kg';
document.getElementById('result-panel').style.display='block';
}
function clearAll(){
document.getElementById('weight').value='70';
document.getElementById('height').value='170';
document.getElementById('age').value='30';
document.getElementById('gender').value='male';
document.getElementById('activity').value='moderate';
document.getElementById('goal').value='lose';
document.getElementById('deficit').value='500';
document.getElementById('result-panel').style.display='none';
}'''

    elif slug == "cholesterol-ratio-calculator":
        return '''function calculate(){
const tc=parseFloat(document.getElementById('total-cholesterol').value)||0;
const hdl=parseFloat(document.getElementById('hdl').value)||0;
const ldl=parseFloat(document.getElementById('ldl').value)||0;
const tg=parseFloat(document.getElementById('triglycerides').value)||0;
const unit=document.getElementById('unit').value;
let tcHdl=tc/hdl,ldlHdl=ldl/hdl,tgHdl=tg/hdl;
let tcAssess,ldlAssess,tgAssess;
if(tcHdl<3.5)tcAssess='✅ 理想 (Ideal)';
else if(tcHdl<5)tcAssess='⚠️ 临界 (Borderline)';
else tcAssess='🔴 高风险 (High Risk)';
if(ldlHdl<2.5)ldlAssess='✅ 理想 (Ideal)';
else if(ldlHdl<3.5)ldlAssess='⚠️ 临界 (Borderline)';
else ldlAssess='🔴 高风险 (High Risk)';
if(tgHdl<2)tgAssess='✅ 理想 (Ideal)';
else if(tgHdl<4)tgAssess='⚠️ 临界 (Borderline)';
else tgAssess='🔴 高风险 (High Risk)';
document.getElementById('tc-hdl').textContent=tcHdl.toFixed(1);
document.getElementById('ldl-hdl').textContent=ldlHdl.toFixed(1);
document.getElementById('tg-hdl').textContent=tgHdl.toFixed(1);
document.getElementById('tc-hdl-assessment').textContent=tcAssess;
document.getElementById('ldl-hdl-assessment').textContent=ldlAssess;
document.getElementById('tg-hdl-assessment').textContent=tgAssess;
document.getElementById('result-panel').style.display='block';
}
function clearAll(){
document.getElementById('total-cholesterol').value='200';
document.getElementById('hdl').value='50';
document.getElementById('ldl').value='120';
document.getElementById('triglycerides').value='150';
document.getElementById('unit').value='mgdl';
document.getElementById('result-panel').style.display='none';
}'''

    return ""

# Generate all files
for tool in TOOLS:
    slug = tool["slug"]
    cn_dir = os.path.join(BASE_DIR, slug)
    en_dir = os.path.join(BASE_DIR, "en", slug)
    os.makedirs(cn_dir, exist_ok=True)
    os.makedirs(en_dir, exist_ok=True)
    
    cn_html = gen_html(tool, "cn")
    en_html = gen_html(tool, "en")
    
    with open(os.path.join(cn_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(cn_html)
    with open(os.path.join(en_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(en_html)
    
    print(f"✅ Generated: {slug} (CN + EN)")

print("\\n✅ All 5 tools generated!")