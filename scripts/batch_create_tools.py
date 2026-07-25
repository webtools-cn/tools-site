#!/usr/bin/env python3
"""批量创建5个新工具: CN+EN, 同步首页"""

import os, re, json
from datetime import datetime

BASE = '/home/chison/tools-site'
TODAY = '2026-07-26'

# ============================================================
# 工具定义
# ============================================================
TOOLS = [
    {
        'slug': 'wedding-budget-calculator',
        'cn_name': '婚礼预算计算器',
        'en_name': 'Wedding Budget Calculator',
        'cn_desc': '免费在线婚礼预算计算器，按类别分配婚礼支出。输入总预算自动计算各项目建议金额，支持自定义调整，帮助合理规划婚礼开销。纯前端处理，无需注册，数据不上传服务器。',
        'en_desc': 'Free online wedding budget calculator. Allocate your wedding expenses by category with suggested amounts. Input your total budget to get recommended spending for each item. Supports custom adjustments. Pure client-side processing, no registration required.',
        'cn_short': '免费在线婚礼预算计算器，按类别分配婚礼支出。',
        'en_short': 'Free online wedding budget calculator. Allocate expenses by category.',
        'category': 'life-tools',
        'icon': '💒',
        'cn_keywords': '婚礼预算,婚礼费用,婚礼规划,预算计算器,结婚预算',
        'en_keywords': 'wedding budget,wedding cost,wedding planner,budget calculator,wedding expenses',
    },
    {
        'slug': 'carpet-calculator',
        'cn_name': '地毯用量计算器',
        'en_name': 'Carpet Calculator',
        'cn_desc': '免费在线地毯用量计算器，根据房间尺寸计算所需地毯面积和费用。支持矩形、L形房间，自动计算废料余量，支持不同地毯单价。纯前端处理，无需注册，数据不上传服务器。',
        'en_desc': 'Free online carpet calculator. Calculate carpet area and cost based on room dimensions. Supports rectangular and L-shaped rooms, automatic waste allowance, and different carpet prices. Pure client-side processing, no registration required.',
        'cn_short': '免费在线地毯用量计算器，计算房间所需地毯面积和费用。',
        'en_short': 'Free online carpet calculator. Calculate carpet area and cost for any room.',
        'category': 'life-tools',
        'icon': '🏠',
        'cn_keywords': '地毯计算,地板面积,地毯用量,装修计算,地毯费用',
        'en_keywords': 'carpet calculator,flooring calculator,carpet area,carpet cost,room carpet',
    },
    {
        'slug': 'gas-mileage-calculator',
        'cn_name': '油耗计算器',
        'en_name': 'Gas Mileage Calculator',
        'cn_desc': '免费在线油耗计算器，计算车辆百公里油耗和每公里费用。输入行驶距离、加油量和油价，自动计算油耗、每公里成本及年度油费预估。纯前端处理，无需注册，数据不上传服务器。',
        'en_desc': 'Free online gas mileage calculator. Calculate fuel consumption per 100km and cost per km. Input distance, fuel amount and price to get MPG, cost per mile and annual fuel cost estimate. Pure client-side processing, no registration required.',
        'cn_short': '免费在线油耗计算器，计算百公里油耗和每公里油费。',
        'en_short': 'Free online gas mileage calculator. Calculate MPG and cost per mile.',
        'category': 'life-tools',
        'icon': '⛽',
        'cn_keywords': '油耗计算,百公里油耗,油费计算,油耗,汽车油耗',
        'en_keywords': 'gas mileage,MPG calculator,fuel cost,fuel economy,gas calculator',
    },
    {
        'slug': 'screen-resolution-tester',
        'cn_name': '屏幕分辨率检测器',
        'en_name': 'Screen Resolution Tester',
        'cn_desc': '免费在线屏幕分辨率检测工具，实时显示屏幕尺寸、分辨率、像素密度、色彩深度和视口信息。支持检测设备像素比、浏览器窗口大小，帮助开发者测试响应式设计。纯前端处理，无需注册。',
        'en_desc': 'Free online screen resolution tester. Real-time display of screen size, resolution, pixel density, color depth and viewport information. Detects device pixel ratio and browser window size. Helpful for responsive design testing. Pure client-side, no registration.',
        'cn_short': '免费在线屏幕分辨率检测，实时显示屏幕尺寸、分辨率和像素密度。',
        'en_short': 'Free online screen resolution tester. Check your screen size, resolution and DPI.',
        'category': 'dev-tools',
        'icon': '🖥️',
        'cn_keywords': '屏幕分辨率,分辨率检测,屏幕测试,显示器分辨率,像素密度',
        'en_keywords': 'screen resolution,resolution tester,display resolution,screen size,DPI check',
    },
    {
        'slug': 'protein-calculator',
        'cn_name': '蛋白质摄入计算器',
        'en_name': 'Protein Intake Calculator',
        'cn_desc': '免费在线蛋白质摄入量计算器，根据体重和运动目标计算每日蛋白质需求。支持增肌、减脂、维持体重三种模式，提供食物蛋白质含量参考。纯前端处理，无需注册，数据不上传服务器。',
        'en_desc': 'Free online protein intake calculator. Calculate daily protein needs based on weight and fitness goals. Supports muscle gain, fat loss, and maintenance modes with food protein reference guide. Pure client-side processing, no registration required.',
        'cn_short': '免费在线蛋白质摄入量计算器，根据体重和目标计算每日蛋白质需求。',
        'en_short': 'Free online protein intake calculator. Calculate your daily protein needs.',
        'category': 'health-tools',
        'icon': '💪',
        'cn_keywords': '蛋白质计算,蛋白质摄入,健身营养,蛋白质需求,增肌饮食',
        'en_keywords': 'protein calculator,protein intake,fitness nutrition,protein needs,muscle building',
    },
]

# ============================================================
# HTML模板
# ============================================================

CN_TEMPLATE = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-9W1157EBQV"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-9W1157EBQV');</script>
<script>window.addEventListener("error",function(e){{if(e&&e.message===""){{e.preventDefault();}}}});window.addEventListener("unhandledrejection",function(e){{if(e&&e.reason&&e.reason.message===""){{e.preventDefault();}}}});</script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="{cn_desc}">
<meta name="keywords" content="{cn_keywords}">
<title>{cn_name} - Free ToolBase</title>
<link rel="canonical" href="https://free-toolbase.com/{slug}/">
<meta property="og:title" content="{cn_name} - Free ToolBase">
<meta property="og:description" content="{cn_desc}">
<meta property="og:url" content="https://free-toolbase.com/{slug}/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Free ToolBase">
<link rel="alternate" hreflang="zh" href="https://free-toolbase.com/{slug}/">
<link rel="alternate" hreflang="en" href="https://free-toolbase.com/en/{slug}/">
<link rel="alternate" hreflang="x-default" href="https://free-toolbase.com/en/{slug}/">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"SoftwareApplication","name":"{cn_name}","description":"{cn_desc}","applicationCategory":"UtilitiesApplication","operatingSystem":"Web","publisher":{{"@type":"Organization","name":"Free ToolBase","email":"dexshuang@google.com"}},"offers":{{"@type":"Offer","price":"0","priceCurrency":"USD"}}}}</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"HowTo","name":"如何使用{cn_name}","description":"如何使用{cn_name}的详细步骤指南","totalTime":"PT2M","tool":{{"@type":"HowToTool","name":"{cn_name}"}},"step":[{{"@type":"HowToStep","position":1,"name":"输入数据","text":"在输入框中输入需要计算的数值"}},{{"@type":"HowToStep","position":2,"name":"选择选项","text":"根据需要选择计算模式或参数"}},{{"@type":"HowToStep","position":3,"name":"点击计算","text":"点击计算按钮获取结果"}},{{"@type":"HowToStep","position":4,"name":"查看结果","text":"查看计算结果，支持一键复制"}}]}}</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"首页","item":"https://free-toolbase.com/"}},{{"@type":"ListItem","position":2,"name":"工具","item":"https://free-toolbase.com/#tools"}},{{"@type":"ListItem","position":3,"name":"{cn_name}","item":"https://free-toolbase.com/{slug}/"}}]}}</script>
<style>*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#0f172a;color:#e2e8f0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,"PingFang SC","Microsoft YaHei",sans-serif;line-height:1.6;min-height:100vh}}
a{{color:#06b6d4;text-decoration:none}}
.container{{max-width:900px;margin:0 auto;padding:24px 16px}}
.header{{display:flex;justify-content:space-between;align-items:center;margin-bottom:24px}}
.header h1{{font-size:1.6rem;color:#f1f5f9}}
.lang-switch{{display:flex;gap:4px;background:#1e293b;border-radius:8px;padding:4px;border:1px solid rgba(148,163,184,.1)}}
.lang-switch a{{padding:6px 12px;border-radius:5px;font-size:.85rem;color:#94a3b8}}
.lang-switch a.active{{background:rgba(6,182,212,.2);color:#22d3ee}}
.nav-back{{color:#64748b;font-size:.85rem;margin-bottom:16px}}
.nav-back a{{color:#64748b}}
.hero{{background:linear-gradient(135deg,rgba(6,182,212,.08),rgba(139,92,246,.06));border-radius:12px;padding:20px;margin-bottom:20px;border:1px solid rgba(148,163,184,.1)}}
.hero p{{color:#cbd5e1;font-size:.95rem}}
.badge{{display:inline-block;margin-top:8px;padding:3px 10px;border-radius:12px;font-size:.75rem;background:rgba(6,182,212,.15);color:#22d3ee;border:1px solid rgba(6,182,212,.25)}}
.input-section{{background:#1e293b;border-radius:12px;padding:20px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1)}}
.input-section h2{{font-size:1.1rem;color:#f1f5f9;margin-bottom:12px}}
select{{width:100%;padding:10px 12px;background:#0f172a;color:#e2e8f0;border:1px solid rgba(148,163,184,.2);border-radius:8px;font-size:.9rem;margin-bottom:12px}}
select:focus{{outline:none;border-color:rgba(6,182,212,.5)}}
label{{display:block;color:#94a3b8;font-size:.85rem;margin-bottom:4px}}
input[type=text],input[type=number],input[type=range]{{width:100%;padding:10px 12px;background:#0f172a;color:#e2e8f0;border:1px solid rgba(148,163,184,.2);border-radius:8px;font-size:.9rem;margin-bottom:12px}}
input:focus{{outline:none;border-color:rgba(6,182,212,.5)}}
.row{{display:flex;gap:12px;flex-wrap:wrap}}
.row .field{{flex:1;min-width:140px}}
.options{{display:flex;gap:12px;align-items:center;margin:12px 0;flex-wrap:wrap}}
.options label{{display:flex;align-items:center;gap:6px;font-size:.85rem;color:#94a3b8;cursor:pointer;margin-bottom:0}}
.options input[type=checkbox],.options input[type=radio]{{accent-color:#06b6d4}}
.btn-row{{display:flex;gap:8px;flex-wrap:wrap;margin-top:12px}}
.btn{{padding:8px 20px;border:none;border-radius:6px;font-size:.85rem;cursor:pointer;transition:all .2s}}
.btn-primary{{background:rgba(6,182,212,.2);color:#22d3ee;border:1px solid rgba(6,182,212,.3)}}
.btn-primary:hover{{background:rgba(6,182,212,.3)}}
.btn-secondary{{background:rgba(148,163,184,.1);color:#94a3b8;border:1px solid rgba(148,163,184,.2)}}
.btn-secondary:hover{{background:rgba(148,163,184,.2)}}
.result-section{{background:#1e293b;border-radius:12px;padding:20px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1);display:none}}
.result-section.show{{display:block}}
.result-box{{background:#0f172a;border-radius:8px;padding:12px;margin:8px 0;border:1px solid rgba(148,163,184,.08);overflow-x:auto;white-space:pre-wrap;word-break:break-all;font-family:monospace;font-size:.85rem}}
.info-section{{background:#1e293b;border-radius:12px;padding:20px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1)}}
.info-section h2{{font-size:1.1rem;color:#f1f5f9;margin-bottom:12px}}
.info-section p{{color:#94a3b8;font-size:.9rem;margin-bottom:8px}}
.pc-result{{background:#0f172a;border-radius:10px;padding:16px;margin:8px 0;text-align:center;border:1px solid rgba(148,163,184,.1)}}
.pc-result .val{{font-size:1.5rem;font-weight:700;color:#22d3ee;font-family:monospace}}
.pc-result .lbl{{font-size:.8rem;color:#64748b;margin-top:4px}}
.pc-detail{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;margin:8px 0}}
.pc-detail .item{{background:#0f172a;border-radius:6px;padding:10px 14px;display:flex;flex-direction:column;text-align:center}}
.pc-detail .item .val{{color:#f1f5f9;font-weight:600;font-family:monospace;font-size:1.1rem}}
.pc-detail .item .lbl{{color:#94a3b8;font-size:.75rem}}
.pc-tip{{background:rgba(6,182,212,.1);border-radius:8px;padding:12px;margin:8px 0;border:1px solid rgba(6,182,212,.15);font-size:.85rem;color:#7dd3fc}}
.footer{{border-top:1px solid rgba(148,163,184,.1);padding:24px 0;margin-top:32px;text-align:center;color:#64748b;font-size:.85rem}}
.footer a{{color:#64748b;margin:0 8px}}
.footer a:hover{{color:#94a3b8}}
.toast{{position:fixed;bottom:20px;left:50%;transform:translateX(-50%);background:#1e293b;color:#e2e8f0;padding:10px 24px;border-radius:8px;font-size:.85rem;z-index:9999;border:1px solid rgba(148,163,184,.2);opacity:0;pointer-events:none;transition:opacity .3s}}
.toast.show{{opacity:1}}
.ad-slot{{margin:0 auto;text-align:center;max-width:960px}}.ad-slot:not(:has(ins[frame])){{display:none}}.ad-slot:empty{{display:none}}.ad-slot ins{{display:block}}
@media(max-width:640px){{.pc-detail{{grid-template-columns:1fr 1fr}}.row .field{{min-width:100%}}}}
</style>
<meta property="og:image" content="https://free-toolbase.com/og-image.svg">
<meta name="twitter:image" content="https://free-toolbase.com/og-image.svg">
<meta name="twitter:card" content="summary_large_image">
<meta name="robots" content="index, follow">
<link rel="icon" type="image/svg+xml" href="favicon.svg">
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5998441792679372" crossorigin="anonymous"></script>
</head>
<body>
<div class="container">
<div class="header"><h1>{cn_name}</h1><div class="lang-switch"><a href="index.html" class="active">中文</a><a href="../en/{slug}/">EN</a></div></div>
<p class="nav-back"><a href="../index.html">首页</a> &rsaquo; <a href="../index.html#tools">工具</a> &rsaquo; {cn_name}</p>
<div class="hero"><p>{cn_desc}</p><span class="badge">零依赖·可离线使用</span></div>
<div style="text-align:center;margin-top:-8px;margin-bottom:16px;font-size:0.8rem;color:#64748b">
  <span style="display:inline-flex;align-items:center;gap:5px;padding:3px 14px;border-radius:20px;background:rgba(6,182,212,.08);border:1px solid rgba(6,182,212,.12)">
    <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="#06b6d4" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
    Updated: {today}
  </span>
</div>
{cn_body}
<div class="info-section">
<h2>关于 {cn_name}</h2>
<p>{cn_desc}</p></div>
</div>
<ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-5998441792679372" data-ad-slot="auto" data-ad-format="auto" data-full-width-responsive="true"></ins>
<script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
<footer class="footer container">
<div style="margin-bottom:12px">
<a href="../index.html">首页</a>
<a href="../index.html">全部工具</a>
<a href="mailto:dexshuang@google.com">联系我们</a>
<a href="../privacy/">隐私政策</a>
<a href="../terms/">服务条款</a>
<a href="../about/">关于我们</a>
<a href="../en/{slug}/">EN</a>
</div>
<p>{cn_name} | 无需注册 · 数据绝不上传服务器</p>
<p style="margin-top:8px;color:#475569;font-size:.8rem">问题反馈: dexshuang@google.com</p>
</footer>
<div class="toast" id="toast"></div>
<script>
function showToast(m){{var t=document.getElementById("toast");t.textContent=m;t.classList.add("show");setTimeout(function(){{t.classList.remove("show")}},3000)}}
function copyText(id){{var el=document.getElementById(id);if(!el)return;var t=el.textContent||el.innerText;navigator.clipboard.writeText(t).then(function(){{showToast("已复制")}})["catch"](function(){{showToast("复制失败")}})}}
{cn_js}
</script>
</body>
</html>'''

EN_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-9W1157EBQV"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-9W1157EBQV');</script>
<script>window.addEventListener("error",function(e){{if(e&&e.message===""){{e.preventDefault();}}}});window.addEventListener("unhandledrejection",function(e){{if(e&&e.reason&&e.reason.message===""){{e.preventDefault();}}}});</script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="{en_desc}">
<meta name="keywords" content="{en_keywords}">
<title>{en_name} - Free ToolBase</title>
<link rel="canonical" href="https://free-toolbase.com/en/{slug}/">
<meta property="og:title" content="{en_name} - Free ToolBase">
<meta property="og:description" content="{en_desc}">
<meta property="og:url" content="https://free-toolbase.com/en/{slug}/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Free ToolBase">
<link rel="alternate" hreflang="en" href="https://free-toolbase.com/en/{slug}/">
<link rel="alternate" hreflang="zh" href="https://free-toolbase.com/{slug}/">
<link rel="alternate" hreflang="x-default" href="https://free-toolbase.com/en/{slug}/">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"SoftwareApplication","name":"{en_name}","description":"{en_desc}","applicationCategory":"UtilitiesApplication","operatingSystem":"Web","publisher":{{"@type":"Organization","name":"Free ToolBase","email":"dexshuang@google.com"}},"offers":{{"@type":"Offer","price":"0","priceCurrency":"USD"}}}}</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"HowTo","name":"How to Use {en_name}","description":"Step-by-step guide on using the {en_name}","totalTime":"PT2M","tool":{{"@type":"HowToTool","name":"{en_name}"}},"step":[{{"@type":"HowToStep","position":1,"name":"Enter Data","text":"Enter the values you need to calculate in the input fields"}},{{"@type":"HowToStep","position":2,"name":"Select Options","text":"Choose calculation mode or parameters as needed"}},{{"@type":"HowToStep","position":3,"name":"Click Calculate","text":"Click the calculate button to get results"}},{{"@type":"HowToStep","position":4,"name":"View Results","text":"View the calculation results with one-click copy"}}]}}</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"Home","item":"https://free-toolbase.com/en/"}},{{"@type":"ListItem","position":2,"name":"Tools","item":"https://free-toolbase.com/en/#tools"}},{{"@type":"ListItem","position":3,"name":"{en_name}","item":"https://free-toolbase.com/en/{slug}/"}}]}}</script>
<style>*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#0f172a;color:#e2e8f0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;line-height:1.6;min-height:100vh}}
a{{color:#06b6d4;text-decoration:none}}
.container{{max-width:900px;margin:0 auto;padding:24px 16px}}
.header{{display:flex;justify-content:space-between;align-items:center;margin-bottom:24px}}
.header h1{{font-size:1.6rem;color:#f1f5f9}}
.lang-switch{{display:flex;gap:4px;background:#1e293b;border-radius:8px;padding:4px;border:1px solid rgba(148,163,184,.1)}}
.lang-switch a{{padding:6px 12px;border-radius:5px;font-size:.85rem;color:#94a3b8}}
.lang-switch a.active{{background:rgba(6,182,212,.2);color:#22d3ee}}
.nav-back{{color:#64748b;font-size:.85rem;margin-bottom:16px}}
.nav-back a{{color:#64748b}}
.hero{{background:linear-gradient(135deg,rgba(6,182,212,.08),rgba(139,92,246,.06));border-radius:12px;padding:20px;margin-bottom:20px;border:1px solid rgba(148,163,184,.1)}}
.hero p{{color:#cbd5e1;font-size:.95rem}}
.badge{{display:inline-block;margin-top:8px;padding:3px 10px;border-radius:12px;font-size:.75rem;background:rgba(6,182,212,.15);color:#22d3ee;border:1px solid rgba(6,182,212,.25)}}
.input-section{{background:#1e293b;border-radius:12px;padding:20px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1)}}
.input-section h2{{font-size:1.1rem;color:#f1f5f9;margin-bottom:12px}}
select{{width:100%;padding:10px 12px;background:#0f172a;color:#e2e8f0;border:1px solid rgba(148,163,184,.2);border-radius:8px;font-size:.9rem;margin-bottom:12px}}
select:focus{{outline:none;border-color:rgba(6,182,212,.5)}}
label{{display:block;color:#94a3b8;font-size:.85rem;margin-bottom:4px}}
input[type=text],input[type=number],input[type=range]{{width:100%;padding:10px 12px;background:#0f172a;color:#e2e8f0;border:1px solid rgba(148,163,184,.2);border-radius:8px;font-size:.9rem;margin-bottom:12px}}
input:focus{{outline:none;border-color:rgba(6,182,212,.5)}}
.row{{display:flex;gap:12px;flex-wrap:wrap}}
.row .field{{flex:1;min-width:140px}}
.options{{display:flex;gap:12px;align-items:center;margin:12px 0;flex-wrap:wrap}}
.options label{{display:flex;align-items:center;gap:6px;font-size:.85rem;color:#94a3b8;cursor:pointer;margin-bottom:0}}
.options input[type=checkbox],.options input[type=radio]{{accent-color:#06b6d4}}
.btn-row{{display:flex;gap:8px;flex-wrap:wrap;margin-top:12px}}
.btn{{padding:8px 20px;border:none;border-radius:6px;font-size:.85rem;cursor:pointer;transition:all .2s}}
.btn-primary{{background:rgba(6,182,212,.2);color:#22d3ee;border:1px solid rgba(6,182,212,.3)}}
.btn-primary:hover{{background:rgba(6,182,212,.3)}}
.btn-secondary{{background:rgba(148,163,184,.1);color:#94a3b8;border:1px solid rgba(148,163,184,.2)}}
.btn-secondary:hover{{background:rgba(148,163,184,.2)}}
.result-section{{background:#1e293b;border-radius:12px;padding:20px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1);display:none}}
.result-section.show{{display:block}}
.result-box{{background:#0f172a;border-radius:8px;padding:12px;margin:8px 0;border:1px solid rgba(148,163,184,.08);overflow-x:auto;white-space:pre-wrap;word-break:break-all;font-family:monospace;font-size:.85rem}}
.info-section{{background:#1e293b;border-radius:12px;padding:20px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1)}}
.info-section h2{{font-size:1.1rem;color:#f1f5f9;margin-bottom:12px}}
.info-section p{{color:#94a3b8;font-size:.9rem;margin-bottom:8px}}
.pc-result{{background:#0f172a;border-radius:10px;padding:16px;margin:8px 0;text-align:center;border:1px solid rgba(148,163,184,.1)}}
.pc-result .val{{font-size:1.5rem;font-weight:700;color:#22d3ee;font-family:monospace}}
.pc-result .lbl{{font-size:.8rem;color:#64748b;margin-top:4px}}
.pc-detail{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;margin:8px 0}}
.pc-detail .item{{background:#0f172a;border-radius:6px;padding:10px 14px;display:flex;flex-direction:column;text-align:center}}
.pc-detail .item .val{{color:#f1f5f9;font-weight:600;font-family:monospace;font-size:1.1rem}}
.pc-detail .item .lbl{{color:#94a3b8;font-size:.75rem}}
.pc-tip{{background:rgba(6,182,212,.1);border-radius:8px;padding:12px;margin:8px 0;border:1px solid rgba(6,182,212,.15);font-size:.85rem;color:#7dd3fc}}
.footer{{border-top:1px solid rgba(148,163,184,.1);padding:24px 0;margin-top:32px;text-align:center;color:#64748b;font-size:.85rem}}
.footer a{{color:#64748b;margin:0 8px}}
.footer a:hover{{color:#94a3b8}}
.toast{{position:fixed;bottom:20px;left:50%;transform:translateX(-50%);background:#1e293b;color:#e2e8f0;padding:10px 24px;border-radius:8px;font-size:.85rem;z-index:9999;border:1px solid rgba(148,163,184,.2);opacity:0;pointer-events:none;transition:opacity .3s}}
.toast.show{{opacity:1}}
.ad-slot{{margin:0 auto;text-align:center;max-width:960px}}.ad-slot:not(:has(ins[frame])){{display:none}}.ad-slot:empty{{display:none}}.ad-slot ins{{display:block}}
@media(max-width:640px){{.pc-detail{{grid-template-columns:1fr 1fr}}.row .field{{min-width:100%}}}}
</style>
<meta property="og:image" content="https://free-toolbase.com/og-image.svg">
<meta name="twitter:image" content="https://free-toolbase.com/og-image.svg">
<meta name="twitter:card" content="summary_large_image">
<meta name="robots" content="index, follow">
<link rel="icon" type="image/svg+xml" href="favicon.svg">
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5998441792679372" crossorigin="anonymous"></script>
</head>
<body>
<div class="container">
<div class="header"><h1>{en_name}</h1><div class="lang-switch"><a href="../{slug}/">中文</a><a href="index.html" class="active">EN</a></div></div>
<p class="nav-back"><a href="../index.html">Home</a> &rsaquo; <a href="../index.html#tools">Tools</a> &rsaquo; {en_name}</p>
<div class="hero"><p>{en_desc}</p><span class="badge">Zero-dependency · Works offline</span></div>
<div style="text-align:center;margin-top:-8px;margin-bottom:16px;font-size:0.8rem;color:#64748b">
  <span style="display:inline-flex;align-items:center;gap:5px;padding:3px 14px;border-radius:20px;background:rgba(6,182,212,.08);border:1px solid rgba(6,182,212,.12)">
    <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="#06b6d4" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
    Updated: {today}
  </span>
</div>
{en_body}
<div class="info-section">
<h2>About {en_name}</h2>
<p>{en_desc}</p></div>
</div>
<ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-5998441792679372" data-ad-slot="auto" data-ad-format="auto" data-full-width-responsive="true"></ins>
<script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
<footer class="footer container">
<div style="margin-bottom:12px">
<a href="../index.html">Home</a>
<a href="../index.html">All Tools</a>
<a href="mailto:dexshuang@google.com">Contact</a>
<a href="../privacy/">Privacy</a>
<a href="../terms/">Terms</a>
<a href="../about/">About</a>
<a href="../{slug}/">中文</a>
</div>
<p>{en_name} | No registration · Data never leaves your device</p>
<p style="margin-top:8px;color:#475569;font-size:.8rem">Feedback: dexshuang@google.com</p>
</footer>
<div class="toast" id="toast"></div>
<script>
function showToast(m){{var t=document.getElementById("toast");t.textContent=m;t.classList.add("show");setTimeout(function(){{t.classList.remove("show")}},3000)}}
function copyText(id){{var el=document.getElementById(id);if(!el)return;var t=el.textContent||el.innerText;navigator.clipboard.writeText(t).then(function(){{showToast("Copied")}})["catch"](function(){{showToast("Copy failed")}})}}
{en_js}
</script>
</body>
</html>'''

# ============================================================
# 工具专属body和JS
# ============================================================

BODIES = {
    'wedding-budget-calculator': {
        'cn_body': '''<div class="input-section">
<h2>预算设置</h2>
<div class="row">
<div class="field"><label>婚礼总预算 (元)</label><input type="number" id="wbTotal" value="100000" min="1000" step="1000"></div>
<div class="field"><label>宾客人数</label><input type="number" id="wbGuests" value="100" min="10" step="10"></div>
</div>
<div class="btn-row"><button class="btn btn-primary" onclick="wbCalc()">计算预算分配</button></div>
</div>
<div class="result-section show">
<h2>预算分配方案</h2>
<div id="wbResultArea">
<div class="pc-result"><div class="val" id="wbTotalDisplay">¥100,000</div><div class="lbl">总预算</div></div>
<div class="pc-detail" id="wbDetail"></div>
<div class="pc-tip">💡 以上比例为行业建议值，可根据实际情况调整。婚宴场地通常占总预算40-50%。</div>
</div>
</div>''',
        'cn_js': '''const wbCategories=[
{name:'婚宴场地',pct:45,desc:'酒店/餐厅场地费及餐饮'},
{name:'婚纱摄影',pct:10,desc:'婚纱照拍摄及礼服租赁'},
{name:'婚庆策划',pct:8,desc:'司仪、化妆、现场布置'},
{name:'婚戒首饰',pct:8,desc:'钻戒、对戒等'},
{name:'婚纱礼服',pct:5,desc:'新娘婚纱、新郎礼服'},
{name:'婚车租赁',pct:3,desc:'婚车及跟拍车辆'},
{name:'蜜月旅行',pct:8,desc:'蜜月旅行费用'},
{name:'喜糖伴手礼',pct:2,desc:'喜糖、伴手礼等'},
{name:'请柬打印',pct:1,desc:'请柬设计及打印'},
{name:'其他预留',pct:10,desc:'应急及其他杂项'}
];
function wbCalc(){
const total=parseFloat(document.getElementById('wbTotal').value)||0;
const guests=parseInt(document.getElementById('wbGuests').value)||0;
document.getElementById('wbTotalDisplay').textContent='¥'+total.toLocaleString();
let html='';
wbCategories.forEach(c=>{
const amount=Math.round(total*c.pct/100);
html+='<div class="item"><span class="val">¥'+amount.toLocaleString()+'</span><span class="lbl">'+c.name+' ('+c.pct+'%)</span></div>';
});
document.getElementById('wbDetail').innerHTML=html;
}
document.getElementById('wbTotal').addEventListener('input',wbCalc);
document.getElementById('wbGuests').addEventListener('change',wbCalc);
document.addEventListener('DOMContentLoaded',wbCalc);
wbCalc();''',
        'en_body': '''<div class="input-section">
<h2>Budget Settings</h2>
<div class="row">
<div class="field"><label>Total Wedding Budget ($)</label><input type="number" id="wbTotal" value="30000" min="1000" step="1000"></div>
<div class="field"><label>Number of Guests</label><input type="number" id="wbGuests" value="100" min="10" step="10"></div>
</div>
<div class="btn-row"><button class="btn btn-primary" onclick="wbCalc()">Calculate Budget</button></div>
</div>
<div class="result-section show">
<h2>Budget Breakdown</h2>
<div id="wbResultArea">
<div class="pc-result"><div class="val" id="wbTotalDisplay">$30,000</div><div class="lbl">Total Budget</div></div>
<div class="pc-detail" id="wbDetail"></div>
<div class="pc-tip">💡 The percentages above are industry recommendations. Venue typically accounts for 40-50% of total budget.</div>
</div>
</div>''',
        'en_js': '''const wbCategories=[
{name:'Venue & Catering',pct:45,desc:'Venue rental and food & beverage'},
{name:'Photography',pct:10,desc:'Photoshoot and attire rental'},
{name:'Planning & Decor',pct:8,desc:'MC, makeup, venue decoration'},
{name:'Rings & Jewelry',pct:8,desc:'Engagement ring, wedding bands'},
{name:'Attire',pct:5,desc:'Wedding dress and groom suit'},
{name:'Transportation',pct:3,desc:'Wedding car and follow vehicles'},
{name:'Honeymoon',pct:8,desc:'Honeymoon travel expenses'},
{name:'Favors & Gifts',pct:2,desc:'Wedding favors and gifts'},
{name:'Invitations',pct:1,desc:'Invitation design and printing'},
{name:'Contingency',pct:10,desc:'Emergency fund and miscellaneous'}
];
function wbCalc(){
const total=parseFloat(document.getElementById('wbTotal').value)||0;
const guests=parseInt(document.getElementById('wbGuests').value)||0;
document.getElementById('wbTotalDisplay').textContent='$'+total.toLocaleString();
let html='';
wbCategories.forEach(c=>{
const amount=Math.round(total*c.pct/100);
html+='<div class="item"><span class="val">$'+amount.toLocaleString()+'</span><span class="lbl">'+c.name+' ('+c.pct+'%)</span></div>';
});
document.getElementById('wbDetail').innerHTML=html;
}
document.getElementById('wbTotal').addEventListener('input',wbCalc);
document.getElementById('wbGuests').addEventListener('change',wbCalc);
document.addEventListener('DOMContentLoaded',wbCalc);
wbCalc();''',
    },
    'carpet-calculator': {
        'cn_body': '''<div class="input-section">
<h2>房间尺寸</h2>
<div class="row">
<div class="field"><label>房间长度 (米)</label><input type="number" id="ccLen" value="5" min="0.1" step="0.1"></div>
<div class="field"><label>房间宽度 (米)</label><input type="number" id="ccWid" value="4" min="0.1" step="0.1"></div>
</div>
<div class="options"><label><input type="checkbox" id="ccLShape"> L形房间</label></div>
<div id="ccLShapeFields" style="display:none">
<div class="row">
<div class="field"><label>L形延伸长度 (米)</label><input type="number" id="ccL2Len" value="2" min="0" step="0.1"></div>
<div class="field"><label>L形延伸宽度 (米)</label><input type="number" id="ccL2Wid" value="2" min="0" step="0.1"></div>
</div>
</div>
<div class="row">
<div class="field"><label>地毯单价 (元/m²)</label><input type="number" id="ccPrice" value="80" min="1" step="1"></div>
<div class="field"><label>废料余量 (%)</label><select id="ccWaste"><option value="5">5% (标准)</option><option value="10" selected>10% (推荐)</option><option value="15">15% (不规则)</option></select></div>
</div>
<div class="btn-row"><button class="btn btn-primary" onclick="ccCalc()">计算地毯用量</button></div>
</div>
<div class="result-section show">
<h2>计算结果</h2>
<div id="ccResultArea">
<div class="pc-result"><div class="val" id="ccTotalCost">¥3,520</div><div class="lbl">预估总费用</div></div>
<div class="pc-detail">
<div class="item"><span class="val" id="ccArea">40.0</span><span class="lbl">净面积 (m²)</span></div>
<div class="item"><span class="val" id="ccWasteArea">4.0</span><span class="lbl">废料面积 (m²)</span></div>
<div class="item"><span class="val" id="ccTotalArea">44.0</span><span class="lbl">总需面积 (m²)</span></div>
</div>
</div>
</div>''',
        'cn_js': '''function ccCalc(){
const len=parseFloat(document.getElementById('ccLen').value)||0;
const wid=parseFloat(document.getElementById('ccWid').value)||0;
const isL=document.getElementById('ccLShape').checked;
const l2len=isL?parseFloat(document.getElementById('ccL2Len').value)||0:0;
const l2wid=isL?parseFloat(document.getElementById('ccL2Wid').value)||0:0;
const price=parseFloat(document.getElementById('ccPrice').value)||0;
const waste=parseFloat(document.getElementById('ccWaste').value)||10;
let area=len*wid;
if(isL)area+=l2len*l2wid;
const wasteArea=Math.round(area*waste/100*10)/10;
const totalArea=Math.round((area+wasteArea)*10)/10;
const cost=Math.round(totalArea*price);
document.getElementById('ccArea').textContent=Math.round(area*10)/10;
document.getElementById('ccWasteArea').textContent=wasteArea;
document.getElementById('ccTotalArea').textContent=totalArea;
document.getElementById('ccTotalCost').textContent='¥'+cost.toLocaleString();
}
document.getElementById('ccLShape').addEventListener('change',function(){
document.getElementById('ccLShapeFields').style.display=this.checked?'block':'none';
ccCalc();
});
['ccLen','ccWid','ccL2Len','ccL2Wid','ccPrice','ccWaste'].forEach(id=>{
const el=document.getElementById(id);
if(el)el.addEventListener('input',ccCalc);
if(el)el.addEventListener('change',ccCalc);
});
document.addEventListener('DOMContentLoaded',ccCalc);
ccCalc();''',
        'en_body': '''<div class="input-section">
<h2>Room Dimensions</h2>
<div class="row">
<div class="field"><label>Room Length (ft)</label><input type="number" id="ccLen" value="16" min="1" step="0.5"></div>
<div class="field"><label>Room Width (ft)</label><input type="number" id="ccWid" value="13" min="1" step="0.5"></div>
</div>
<div class="options"><label><input type="checkbox" id="ccLShape"> L-Shaped Room</label></div>
<div id="ccLShapeFields" style="display:none">
<div class="row">
<div class="field"><label>L-Extension Length (ft)</label><input type="number" id="ccL2Len" value="6" min="0" step="0.5"></div>
<div class="field"><label>L-Extension Width (ft)</label><input type="number" id="ccL2Wid" value="6" min="0" step="0.5"></div>
</div>
</div>
<div class="row">
<div class="field"><label>Carpet Price ($/ft²)</label><input type="number" id="ccPrice" value="3" min="0.1" step="0.1"></div>
<div class="field"><label>Waste Allowance (%)</label><select id="ccWaste"><option value="5">5% (Standard)</option><option value="10" selected>10% (Recommended)</option><option value="15">15% (Irregular)</option></select></div>
</div>
<div class="btn-row"><button class="btn btn-primary" onclick="ccCalc()">Calculate Carpet</button></div>
</div>
<div class="result-section show">
<h2>Results</h2>
<div id="ccResultArea">
<div class="pc-result"><div class="val" id="ccTotalCost">$733</div><div class="lbl">Estimated Total Cost</div></div>
<div class="pc-detail">
<div class="item"><span class="val" id="ccArea">208.0</span><span class="lbl">Net Area (ft²)</span></div>
<div class="item"><span class="val" id="ccWasteArea">20.8</span><span class="lbl">Waste Area (ft²)</span></div>
<div class="item"><span class="val" id="ccTotalArea">228.8</span><span class="lbl">Total Area (ft²)</span></div>
</div>
</div>
</div>''',
        'en_js': '''function ccCalc(){
const len=parseFloat(document.getElementById('ccLen').value)||0;
const wid=parseFloat(document.getElementById('ccWid').value)||0;
const isL=document.getElementById('ccLShape').checked;
const l2len=isL?parseFloat(document.getElementById('ccL2Len').value)||0:0;
const l2wid=isL?parseFloat(document.getElementById('ccL2Wid').value)||0:0;
const price=parseFloat(document.getElementById('ccPrice').value)||0;
const waste=parseFloat(document.getElementById('ccWaste').value)||10;
let area=len*wid;
if(isL)area+=l2len*l2wid;
const wasteArea=Math.round(area*waste/100*10)/10;
const totalArea=Math.round((area+wasteArea)*10)/10;
const cost=Math.round(totalArea*price);
document.getElementById('ccArea').textContent=Math.round(area*10)/10;
document.getElementById('ccWasteArea').textContent=wasteArea;
document.getElementById('ccTotalArea').textContent=totalArea;
document.getElementById('ccTotalCost').textContent='$'+cost.toLocaleString();
}
document.getElementById('ccLShape').addEventListener('change',function(){
document.getElementById('ccLShapeFields').style.display=this.checked?'block':'none';
ccCalc();
});
['ccLen','ccWid','ccL2Len','ccL2Wid','ccPrice','ccWaste'].forEach(id=>{
const el=document.getElementById(id);
if(el)el.addEventListener('input',ccCalc);
if(el)el.addEventListener('change',ccCalc);
});
document.addEventListener('DOMContentLoaded',ccCalc);
ccCalc();''',
    },
    'gas-mileage-calculator': {
        'cn_body': '''<div class="input-section">
<h2>行程数据</h2>
<div class="row">
<div class="field"><label>行驶距离 (公里)</label><input type="number" id="gmDist" value="500" min="1" step="1"></div>
<div class="field"><label>消耗油量 (升)</label><input type="number" id="gmFuel" value="40" min="0.1" step="0.1"></div>
</div>
<div class="row">
<div class="field"><label>油价 (元/升)</label><input type="number" id="gmPrice" value="8.5" min="0.1" step="0.01"></div>
<div class="field"><label>年行驶里程 (公里)</label><input type="number" id="gmYear" value="15000" min="1" step="1000"></div>
</div>
<div class="btn-row"><button class="btn btn-primary" onclick="gmCalc()">计算油耗</button></div>
</div>
<div class="result-section show">
<h2>计算结果</h2>
<div id="gmResultArea">
<div class="pc-result"><div class="val" id="gmConsumption">8.0 L/100km</div><div class="lbl">百公里油耗</div></div>
<div class="pc-detail">
<div class="item"><span class="val" id="gmPerKm">¥0.68</span><span class="lbl">每公里费用</span></div>
<div class="item"><span class="val" id="gmTotalCost">¥340</span><span class="lbl">本次行程油费</span></div>
<div class="item"><span class="val" id="gmYearCost">¥10,200</span><span class="lbl">预估年油费</span></div>
</div>
<div class="pc-detail">
<div class="item"><span class="val" id="gmMpg">29.4</span><span class="lbl">MPG (美制)</span></div>
<div class="item"><span class="val" id="gmKmpl">12.5</span><span class="lbl">每升公里数</span></div>
<div class="item"><span class="val" id="gmCo2">92.8</span><span class="lbl">CO₂排放 (kg)</span></div>
</div>
</div>
</div>''',
        'cn_js': '''function gmCalc(){
const dist=parseFloat(document.getElementById('gmDist').value)||0;
const fuel=parseFloat(document.getElementById('gmFuel').value)||1;
const price=parseFloat(document.getElementById('gmPrice').value)||0;
const year=parseFloat(document.getElementById('gmYear').value)||0;
const l100km=Math.round(fuel/dist*100*10)/10;
const perKm=Math.round(price*fuel/dist*100)/100;
const total=Math.round(price*fuel);
const yearCost=Math.round(price*fuel/dist*year);
const mpg=Math.round(235.214/l100km*10)/10;
const kmpl=Math.round(dist/fuel*10)/10;
const co2=Math.round(fuel*2.31*10)/10;
document.getElementById('gmConsumption').textContent=l100km+' L/100km';
document.getElementById('gmPerKm').textContent='¥'+perKm.toFixed(2);
document.getElementById('gmTotalCost').textContent='¥'+total.toLocaleString();
document.getElementById('gmYearCost').textContent='¥'+yearCost.toLocaleString();
document.getElementById('gmMpg').textContent=mpg;
document.getElementById('gmKmpl').textContent=kmpl;
document.getElementById('gmCo2').textContent=co2;
}
['gmDist','gmFuel','gmPrice','gmYear'].forEach(id=>{
const el=document.getElementById(id);
if(el)el.addEventListener('input',gmCalc);
if(el)el.addEventListener('change',gmCalc);
});
document.addEventListener('DOMContentLoaded',gmCalc);
gmCalc();''',
        'en_body': '''<div class="input-section">
<h2>Trip Data</h2>
<div class="row">
<div class="field"><label>Distance (miles)</label><input type="number" id="gmDist" value="300" min="1" step="1"></div>
<div class="field"><label>Fuel Used (gallons)</label><input type="number" id="gmFuel" value="10" min="0.1" step="0.1"></div>
</div>
<div class="row">
<div class="field"><label>Fuel Price ($/gallon)</label><input type="number" id="gmPrice" value="3.5" min="0.01" step="0.01"></div>
<div class="field"><label>Annual Mileage</label><input type="number" id="gmYear" value="12000" min="1" step="1000"></div>
</div>
<div class="btn-row"><button class="btn btn-primary" onclick="gmCalc()">Calculate Mileage</button></div>
</div>
<div class="result-section show">
<h2>Results</h2>
<div id="gmResultArea">
<div class="pc-result"><div class="val" id="gmConsumption">30.0 MPG</div><div class="lbl">Fuel Economy</div></div>
<div class="pc-detail">
<div class="item"><span class="val" id="gmPerKm">$0.12</span><span class="lbl">Cost per Mile</span></div>
<div class="item"><span class="val" id="gmTotalCost">$35</span><span class="lbl">Trip Fuel Cost</span></div>
<div class="item"><span class="val" id="gmYearCost">$1,400</span><span class="lbl">Est. Annual Cost</span></div>
</div>
<div class="pc-detail">
<div class="item"><span class="val" id="gmMpg">30.0</span><span class="lbl">MPG</span></div>
<div class="item"><span class="val" id="gmKmpl">7.8</span><span class="lbl">L/100km</span></div>
<div class="item"><span class="val" id="gmCo2">88.8</span><span class="lbl">CO₂ (kg)</span></div>
</div>
</div>
</div>''',
        'en_js': '''function gmCalc(){
const dist=parseFloat(document.getElementById('gmDist').value)||0;
const fuel=parseFloat(document.getElementById('gmFuel').value)||1;
const price=parseFloat(document.getElementById('gmPrice').value)||0;
const year=parseFloat(document.getElementById('gmYear').value)||0;
const mpg=Math.round(dist/fuel*10)/10;
const perMile=Math.round(price*fuel/dist*100)/100;
const total=Math.round(price*fuel);
const yearCost=Math.round(price*fuel/dist*year);
const l100km=Math.round(235.214/mpg*10)/10;
const co2=Math.round(fuel*8.887*10)/10;
document.getElementById('gmConsumption').textContent=mpg+' MPG';
document.getElementById('gmPerKm').textContent='$'+perMile.toFixed(2);
document.getElementById('gmTotalCost').textContent='$'+total.toLocaleString();
document.getElementById('gmYearCost').textContent='$'+yearCost.toLocaleString();
document.getElementById('gmMpg').textContent=mpg;
document.getElementById('gmKmpl').textContent=l100km;
document.getElementById('gmCo2').textContent=co2;
}
['gmDist','gmFuel','gmPrice','gmYear'].forEach(id=>{
const el=document.getElementById(id);
if(el)el.addEventListener('input',gmCalc);
if(el)el.addEventListener('change',gmCalc);
});
document.addEventListener('DOMContentLoaded',gmCalc);
gmCalc();''',
    },
    'screen-resolution-tester': {
        'cn_body': '''<div class="input-section">
<h2>屏幕信息</h2>
<div class="btn-row"><button class="btn btn-primary" onclick="srtRefresh()">刷新检测</button></div>
</div>
<div class="result-section show">
<h2>检测结果</h2>
<div id="srtResultArea">
<div class="pc-result"><div class="val" id="srtResolution">-</div><div class="lbl">屏幕分辨率</div></div>
<div class="pc-detail">
<div class="item"><span class="val" id="srtWidth">-</span><span class="lbl">屏幕宽度 (px)</span></div>
<div class="item"><span class="val" id="srtHeight">-</span><span class="lbl">屏幕高度 (px)</span></div>
<div class="item"><span class="val" id="srtAvail">-</span><span class="lbl">可用区域</span></div>
</div>
<div class="pc-detail">
<div class="item"><span class="val" id="srtDpr">-</span><span class="lbl">设备像素比</span></div>
<div class="item"><span class="val" id="srtColor">-</span><span class="lbl">色彩深度</span></div>
<div class="item"><span class="val" id="srtOrientation">-</span><span class="lbl">屏幕方向</span></div>
</div>
<div class="pc-detail">
<div class="item"><span class="val" id="srtViewW">-</span><span class="lbl">视口宽度</span></div>
<div class="item"><span class="val" id="srtViewH">-</span><span class="lbl">视口高度</span></div>
<div class="item"><span class="val" id="srtTouch">-</span><span class="lbl">触摸支持</span></div>
</div>
<div class="pc-tip">💡 调整浏览器窗口大小或旋转设备后点击"刷新检测"查看变化。</div>
</div>
</div>''',
        'cn_js': '''function srtRefresh(){
const sw=screen.width;
const sh=screen.height;
const aw=screen.availWidth;
const ah=screen.availHeight;
const dpr=window.devicePixelRatio||1;
const cd=screen.colorDepth;
const ori=screen.orientation?screen.orientation.type:'不支持';
const vw=window.innerWidth;
const vh=window.innerHeight;
const touch='ontouchstart' in window||navigator.maxTouchPoints>0?'支持 ('+(navigator.maxTouchPoints||1)+'点)':'不支持';
document.getElementById('srtResolution').textContent=sw+' × '+sh;
document.getElementById('srtWidth').textContent=sw+' px';
document.getElementById('srtHeight').textContent=sh+' px';
document.getElementById('srtAvail').textContent=aw+' × '+ah;
document.getElementById('srtDpr').textContent=dpr+'x';
document.getElementById('srtColor').textContent=cd+'-bit';
document.getElementById('srtOrientation').textContent=ori;
document.getElementById('srtViewW').textContent=vw+' px';
document.getElementById('srtViewH').textContent=vh+' px';
document.getElementById('srtTouch').textContent=touch;
}
window.addEventListener('resize',srtRefresh);
window.addEventListener('orientationchange',function(){setTimeout(srtRefresh,300);});
document.addEventListener('DOMContentLoaded',srtRefresh);
srtRefresh();''',
        'en_body': '''<div class="input-section">
<h2>Screen Information</h2>
<div class="btn-row"><button class="btn btn-primary" onclick="srtRefresh()">Refresh Detection</button></div>
</div>
<div class="result-section show">
<h2>Detection Results</h2>
<div id="srtResultArea">
<div class="pc-result"><div class="val" id="srtResolution">-</div><div class="lbl">Screen Resolution</div></div>
<div class="pc-detail">
<div class="item"><span class="val" id="srtWidth">-</span><span class="lbl">Screen Width (px)</span></div>
<div class="item"><span class="val" id="srtHeight">-</span><span class="lbl">Screen Height (px)</span></div>
<div class="item"><span class="val" id="srtAvail">-</span><span class="lbl">Available Area</span></div>
</div>
<div class="pc-detail">
<div class="item"><span class="val" id="srtDpr">-</span><span class="lbl">Device Pixel Ratio</span></div>
<div class="item"><span class="val" id="srtColor">-</span><span class="lbl">Color Depth</span></div>
<div class="item"><span class="val" id="srtOrientation">-</span><span class="lbl">Orientation</span></div>
</div>
<div class="pc-detail">
<div class="item"><span class="val" id="srtViewW">-</span><span class="lbl">Viewport Width</span></div>
<div class="item"><span class="val" id="srtViewH">-</span><span class="lbl">Viewport Height</span></div>
<div class="item"><span class="val" id="srtTouch">-</span><span class="lbl">Touch Support</span></div>
</div>
<div class="pc-tip">💡 Resize your browser window or rotate your device, then click "Refresh Detection" to see changes.</div>
</div>
</div>''',
        'en_js': '''function srtRefresh(){
const sw=screen.width;
const sh=screen.height;
const aw=screen.availWidth;
const ah=screen.availHeight;
const dpr=window.devicePixelRatio||1;
const cd=screen.colorDepth;
const ori=screen.orientation?screen.orientation.type:'Not supported';
const vw=window.innerWidth;
const vh=window.innerHeight;
const touch='ontouchstart' in window||navigator.maxTouchPoints>0?'Supported ('+(navigator.maxTouchPoints||1)+' points)':'Not supported';
document.getElementById('srtResolution').textContent=sw+' × '+sh;
document.getElementById('srtWidth').textContent=sw+' px';
document.getElementById('srtHeight').textContent=sh+' px';
document.getElementById('srtAvail').textContent=aw+' × '+ah;
document.getElementById('srtDpr').textContent=dpr+'x';
document.getElementById('srtColor').textContent=cd+'-bit';
document.getElementById('srtOrientation').textContent=ori;
document.getElementById('srtViewW').textContent=vw+' px';
document.getElementById('srtViewH').textContent=vh+' px';
document.getElementById('srtTouch').textContent=touch;
}
window.addEventListener('resize',srtRefresh);
window.addEventListener('orientationchange',function(){setTimeout(srtRefresh,300);});
document.addEventListener('DOMContentLoaded',srtRefresh);
srtRefresh();''',
    },
    'protein-calculator': {
        'cn_body': '''<div class="input-section">
<h2>个人信息</h2>
<div class="row">
<div class="field"><label>体重 (公斤)</label><input type="number" id="pcWt" value="70" min="30" max="200" step="0.1"></div>
<div class="field"><label>运动目标</label><select id="pcGoal"><option value="maintain">维持体重</option><option value="gain" selected>增肌</option><option value="lose">减脂</option></select></div>
</div>
<div class="row">
<div class="field"><label>运动频率</label><select id="pcActivity"><option value="light">轻度 (每周1-2次)</option><option value="moderate" selected>中度 (每周3-4次)</option><option value="heavy">重度 (每周5-6次)</option><option value="intense">高强度 (每天训练)</option></select></div>
</div>
<div class="btn-row"><button class="btn btn-primary" onclick="pcCalc()">计算蛋白质需求</button></div>
</div>
<div class="result-section show">
<h2>每日蛋白质需求</h2>
<div id="pcResultArea">
<div class="pc-result"><div class="val" id="pcDaily">140 克/天</div><div class="lbl">推荐每日摄入量</div></div>
<div class="pc-detail">
<div class="item"><span class="val" id="pcPerKg">2.0</span><span class="lbl">每公斤体重 (克)</span></div>
<div class="item"><span class="val" id="pcPerMeal">35</span><span class="lbl">每餐约 (4餐)</span></div>
<div class="item"><span class="val" id="pcCal">560</span><span class="lbl">蛋白质热量 (千卡)</span></div>
</div>
<div class="pc-tip">💡 常见高蛋白食物：鸡胸肉100g≈31g蛋白 | 鸡蛋1个≈6g | 牛奶250ml≈8g | 豆腐100g≈8g</div>
</div>
</div>''',
        'cn_js': '''function pcCalc(){
const wt=parseFloat(document.getElementById('pcWt').value)||70;
const goal=document.getElementById('pcGoal').value;
const act=document.getElementById('pcActivity').value;
let factor=1.2;
if(goal==='gain')factor=1.8;
else if(goal==='lose')factor=2.2;
else factor=1.2;
if(act==='light')factor-=0.2;
else if(act==='heavy')factor+=0.2;
else if(act==='intense')factor+=0.4;
const daily=Math.round(wt*factor);
const perMeal=Math.round(daily/4);
const cal=daily*4;
document.getElementById('pcDaily').textContent=daily+' 克/天';
document.getElementById('pcPerKg').textContent=Math.round(factor*10)/10;
document.getElementById('pcPerMeal').textContent=perMeal;
document.getElementById('pcCal').textContent=cal;
}
['pcWt','pcGoal','pcActivity'].forEach(id=>{
const el=document.getElementById(id);
if(el)el.addEventListener('input',pcCalc);
if(el)el.addEventListener('change',pcCalc);
});
document.addEventListener('DOMContentLoaded',pcCalc);
pcCalc();''',
        'en_body': '''<div class="input-section">
<h2>Personal Info</h2>
<div class="row">
<div class="field"><label>Weight (lbs)</label><input type="number" id="pcWt" value="154" min="66" max="440" step="0.1"></div>
<div class="field"><label>Fitness Goal</label><select id="pcGoal"><option value="maintain">Maintain Weight</option><option value="gain" selected>Muscle Gain</option><option value="lose">Fat Loss</option></select></div>
</div>
<div class="row">
<div class="field"><label>Activity Level</label><select id="pcActivity"><option value="light">Light (1-2x/week)</option><option value="moderate" selected>Moderate (3-4x/week)</option><option value="heavy">Heavy (5-6x/week)</option><option value="intense">Intense (daily training)</option></select></div>
</div>
<div class="btn-row"><button class="btn btn-primary" onclick="pcCalc()">Calculate Protein</button></div>
</div>
<div class="result-section show">
<h2>Daily Protein Needs</h2>
<div id="pcResultArea">
<div class="pc-result"><div class="val" id="pcDaily">126 g/day</div><div class="lbl">Recommended Daily Intake</div></div>
<div class="pc-detail">
<div class="item"><span class="val" id="pcPerKg">0.82</span><span class="lbl">Per lb Body Weight (g)</span></div>
<div class="item"><span class="val" id="pcPerMeal">32</span><span class="lbl">Per Meal (~4 meals)</span></div>
<div class="item"><span class="val" id="pcCal">504</span><span class="lbl">Protein Calories (kcal)</span></div>
</div>
<div class="pc-tip">💡 High protein foods: Chicken breast 100g≈31g | 1 egg≈6g | Milk 250ml≈8g | Tofu 100g≈8g</div>
</div>
</div>''',
        'en_js': '''function pcCalc(){
const wtLb=parseFloat(document.getElementById('pcWt').value)||154;
const wtKg=wtLb/2.2046;
const goal=document.getElementById('pcGoal').value;
const act=document.getElementById('pcActivity').value;
let factor=1.2;
if(goal==='gain')factor=1.8;
else if(goal==='lose')factor=2.2;
else factor=1.2;
if(act==='light')factor-=0.2;
else if(act==='heavy')factor+=0.2;
else if(act==='intense')factor+=0.4;
const daily=Math.round(wtKg*factor);
const perLb=Math.round(factor/2.2046*100)/100;
const perMeal=Math.round(daily/4);
const cal=daily*4;
document.getElementById('pcDaily').textContent=daily+' g/day';
document.getElementById('pcPerKg').textContent=perLb;
document.getElementById('pcPerMeal').textContent=perMeal;
document.getElementById('pcCal').textContent=cal;
}
['pcWt','pcGoal','pcActivity'].forEach(id=>{
const el=document.getElementById(id);
if(el)el.addEventListener('input',pcCalc);
if(el)el.addEventListener('change',pcCalc);
});
document.addEventListener('DOMContentLoaded',pcCalc);
pcCalc();''',
    },
}

# ============================================================
# 首页卡片模板
# ============================================================
CN_CARD = '<div class="tool-card" data-category="{category}"><span class="tool-icon">{icon}</span><span class="tool-name">{cn_name}</span><span class="tool-desc">{cn_short}</span><a href="/{slug}/" class="btn">立即使用</a></div>'
EN_CARD = '<div class="tool-card" data-category="{category}"><span class="tool-icon">{icon}</span><span class="tool-name">{en_name}</span><span class="tool-desc">{en_short}</span><a href="/en/{slug}/" class="btn">Use Now</a></div>'

# ============================================================
# 生成
# ============================================================

def make_tool(tool):
    slug = tool['slug']
    body = BODIES[slug]
    
    cn_dir = os.path.join(BASE, slug)
    en_dir = os.path.join(BASE, 'en', slug)
    os.makedirs(cn_dir, exist_ok=True)
    os.makedirs(en_dir, exist_ok=True)
    
    cn_html = CN_TEMPLATE.format(
        slug=slug,
        cn_name=tool['cn_name'],
        cn_desc=tool['cn_desc'],
        cn_keywords=tool['cn_keywords'],
        cn_body=body['cn_body'],
        cn_js=body['cn_js'],
        today=TODAY,
    )
    
    en_html = EN_TEMPLATE.format(
        slug=slug,
        en_name=tool['en_name'],
        en_desc=tool['en_desc'],
        en_keywords=tool['en_keywords'],
        en_body=body['en_body'],
        en_js=body['en_js'],
        today=TODAY,
    )
    
    with open(os.path.join(cn_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(cn_html)
    with open(os.path.join(en_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(en_html)
    
    print(f'✅ Created: {slug} (CN + EN)')

def add_to_homepage(tool):
    cn_card = CN_CARD.format(
        category=tool['category'],
        icon=tool['icon'],
        cn_name=tool['cn_name'],
        cn_short=tool['cn_short'],
        slug=tool['slug'],
    )
    en_card = EN_CARD.format(
        category=tool['category'],
        icon=tool['icon'],
        en_name=tool['en_name'],
        en_short=tool['en_short'],
        slug=tool['slug'],
    )
    
    # CN首页：插在 <div class="tools-grid"> 内，最后一个 </div> 前
    cn_path = os.path.join(BASE, 'index.html')
    with open(cn_path, 'r', encoding='utf-8') as f:
        cn = f.read()
    
    # Find the tools-grid div and insert before its closing tag
    marker = '    </div>\n    <!-- /tools-grid -->'
    if marker in cn:
        cn = cn.replace(marker, cn_card + '\n' + marker, 1)
    else:
        print(f'⚠️ Could not find tools-grid marker in CN homepage')
    
    with open(cn_path, 'w', encoding='utf-8') as f:
        f.write(cn)
    
    # EN首页
    en_path = os.path.join(BASE, 'en', 'index.html')
    with open(en_path, 'r', encoding='utf-8') as f:
        en = f.read()
    
    if marker in en:
        en = en.replace(marker, en_card + '\n' + marker, 1)
    else:
        print(f'⚠️ Could not find tools-grid marker in EN homepage')
    
    with open(en_path, 'w', encoding='utf-8') as f:
        f.write(en)
    
    print(f'✅ Added card to CN + EN homepage')

def update_homepage_counts():
    """更新首页工具数量"""
    cn_path = os.path.join(BASE, 'index.html')
    en_path = os.path.join(BASE, 'en', 'index.html')
    
    cn_count = 0
    with open(cn_path, 'r') as f:
        cn = f.read()
        cn_count = cn.count('tool-card')
    
    en_count = 0
    with open(en_path, 'r') as f:
        en = f.read()
        en_count = en.count('tool-card')
    
    # Update CN numbers
    import re
    cn = re.sub(r'\d+(?=个免费工具)', str(cn_count), cn)
    cn = re.sub(r'\d+(?=\+免费在线工具)', str(cn_count), cn)
    
    # Update EN numbers
    en = re.sub(r'\d+(?=\+ free online tools)', str(en_count), en)
    en = re.sub(r'\d+(?=\+ browser-based utilities)', str(en_count), en)
    
    with open(cn_path, 'w') as f:
        f.write(cn)
    with open(en_path, 'w') as f:
        f.write(en)
    
    print(f'📊 CN cards: {cn_count}, EN cards: {en_count}')
    return cn_count == en_count

def update_sitemap(tools):
    sitemap_path = os.path.join(BASE, 'sitemap.xml')
    with open(sitemap_path, 'r') as f:
        sm = f.read()
    
    new_entries = ''
    for t in tools:
        new_entries += f'  <url><loc>https://free-toolbase.com/{t["slug"]}/</loc></url>\n'
        new_entries += f'  <url><loc>https://free-toolbase.com/en/{t["slug"]}/</loc></url>\n'
    
    # Insert before </urlset>
    sm = sm.replace('</urlset>', new_entries + '</urlset>')
    
    with open(sitemap_path, 'w') as f:
        f.write(sm)
    
    print(f'✅ Updated sitemap.xml with {len(tools)*2} URLs')

# ============================================================
# Main
# ============================================================
if __name__ == '__main__':
    for tool in TOOLS:
        make_tool(tool)
        add_to_homepage(tool)
    
    ok = update_homepage_counts()
    update_sitemap(TOOLS)
    
    if ok:
        print('\n🎉 All done! Homepage card counts match.')
    else:
        print('\n⚠️ WARNING: Homepage card counts do not match!')