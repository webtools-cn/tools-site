#!/usr/bin/env python3
"""Batch create 3 new tool pages: budget-calculator, decision-tree, date-diff"""
import os, json

BASE = "/home/chison/tools-site"
TOOLS = []

# ============================================================
# Tool 1: Budget Calculator (预算计算器)
# ============================================================
TOOLS.append({
    "slug": "budget-calculator",
    "zh_name": "预算计算器",
    "en_name": "Budget Calculator",
    "zh_desc": "免费在线预算计算器，轻松管理月度收支。支持多分类记账、收入支出对比、储蓄率计算。无需注册，数据不上传服务器。",
    "en_desc": "Free online budget calculator to manage monthly income and expenses. Multi-category tracking, income vs expense comparison, savings rate calculation. No registration, data stays on your device.",
    "zh_title": "免费在线预算计算器 - 月度收支管理 | 储蓄率计算 | 无需注册",
    "en_title": "Free Online Budget Calculator - Monthly Income & Expense Tracker | Savings Rate | No Login",
    "zh_icon": "💰",
    "en_icon": "💰",
    "zh_hero": "免费在线预算计算器，轻松管理月度收支。支持多分类记账、收入支出对比、储蓄率计算。无需注册，数据不上传服务器。",
    "en_hero": "Free online budget calculator to manage monthly income and expenses. Multi-category tracking, income vs expense comparison, savings rate calculation. No registration, data stays on your device.",
})

# ============================================================
# Tool 2: Decision Tree (决策树生成器)
# ============================================================
TOOLS.append({
    "slug": "decision-tree",
    "zh_name": "决策树生成器",
    "en_name": "Decision Tree Generator",
    "zh_desc": "免费在线决策树生成器，可视化辅助决策。支持添加多级节点、导出为文本大纲。帮助梳理复杂决策逻辑。无需注册，数据不上传服务器。",
    "en_desc": "Free online decision tree generator for visual decision making. Add multi-level nodes, export as text outline. Clarify complex decision logic. No registration, data stays on your device.",
    "zh_title": "免费在线决策树生成器 - 可视化辅助决策 | 思维导图 | 无需注册",
    "en_title": "Free Online Decision Tree Generator - Visual Decision Making | Mind Map | No Login",
    "zh_icon": "🌳",
    "en_icon": "🌳",
    "zh_hero": "免费在线决策树生成器，可视化辅助决策。支持添加多级节点、导出为文本大纲。帮助梳理复杂决策逻辑。无需注册，数据不上传服务器。",
    "en_hero": "Free online decision tree generator for visual decision making. Add multi-level nodes, export as text outline. Clarify complex decision logic. No registration, data stays on your device.",
})

# ============================================================
# Tool 3: Date Diff (日期差值计算器)
# ============================================================
TOOLS.append({
    "slug": "date-diff",
    "zh_name": "日期差值计算器",
    "en_name": "Date Difference Calculator",
    "zh_desc": "免费在线日期差值计算器，精确计算两个日期之间的天数、周数、月数和年数。支持工作日计算、倒计时功能。无需注册。",
    "en_desc": "Free online date difference calculator, precisely calculate days, weeks, months and years between two dates. Supports working day calculation and countdown. No registration.",
    "zh_title": "免费在线日期差值计算器 - 精确计算天数/周/月/年 | 工作日计算 | 无需注册",
    "en_title": "Free Online Date Difference Calculator - Days/Weeks/Months/Years | Working Days | No Login",
    "zh_icon": "📅",
    "en_icon": "📅",
    "zh_hero": "免费在线日期差值计算器，精确计算两个日期之间的天数、周数、月数和年数。支持工作日计算、倒计时功能。无需注册。",
    "en_hero": "Free online date difference calculator, precisely calculate days, weeks, months and years between two dates. Supports working day calculation and countdown. No registration.",
})

def make_html(tool, lang="zh"):
    """Generate tool page HTML."""
    is_zh = (lang == "zh")
    name = tool["zh_name"] if is_zh else tool["en_name"]
    desc = tool["zh_desc"] if is_zh else tool["en_desc"]
    title = tool["zh_title"] if is_zh else tool["en_title"]
    icon = tool["zh_icon"] if is_zh else tool["en_icon"]
    hero = tool["zh_hero"] if is_zh else tool["en_hero"]
    slug = tool["slug"]
    
    lang_code = "zh-CN" if is_zh else "en"
    hreflang_self = "zh" if is_zh else "en"
    hreflang_other = "en" if is_zh else "zh"
    
    if is_zh:
        canonical = f"https://free-toolbase.com/{slug}/"
        alt_href = f"https://free-toolbase.com/en/{slug}/"
        home_path = "../index.html"
        tools_path = "../index.html#tools"
        lang_zh_class = "active"
        lang_en_class = ""
        zh_href = "index.html"
        en_href = f"../en/{slug}/"
    else:
        canonical = f"https://free-toolbase.com/en/{slug}/"
        alt_href = f"https://free-toolbase.com/{slug}/"
        home_path = "../../index.html"
        tools_path = "../../index.html#tools"
        lang_zh_class = ""
        lang_en_class = "active"
        zh_href = f"../../{slug}/"
        en_href = "index.html"
    
    home_label = "首页" if is_zh else "Home"
    tools_label = "工具" if is_zh else "Tools"
    breadcrumb_name = name
    
    schema_name = name
    schema_desc = desc
    howto_name = f"如何使用{schema_name}" if is_zh else f"How to Use {schema_name}"
    howto_desc = f"如何使用{schema_name}的详细步骤指南" if is_zh else f"Detailed step-by-step guide on how to use {schema_name}"
    step1_name = "输入数据" if is_zh else "Enter Data"
    step1_text = "在输入框中输入需要计算的数据" if is_zh else "Enter the data to be calculated in the input fields"
    step2_name = "选择选项" if is_zh else "Choose Options"
    step2_text = "根据需要选择计算模式或参数" if is_zh else "Select calculation mode or parameters as needed"
    step3_name = "点击计算" if is_zh else "Click Calculate"
    step3_text = "点击计算按钮获取结果" if is_zh else "Click the calculate button to get results"
    step4_name = "查看结果" if is_zh else "View Results"
    step4_text = "查看计算结果，支持一键复制" if is_zh else "View the calculation results, one-click copy supported"
    
    page_title = title
    og_title = title
    
    # Tool-specific HTML body
    tool_body = ""
    tool_js = ""
    
    if slug == "budget-calculator":
        tool_body, tool_js = budget_calculator_body(is_zh)
    elif slug == "decision-tree":
        tool_body, tool_js = decision_tree_body(is_zh)
    elif slug == "date-diff":
        tool_body, tool_js = date_diff_body(is_zh)
    
    seo_title = "功能说明" if is_zh else "Features"
    seo_p1 = desc
    seo_p2 = "所有计算在浏览器本地完成，数据不会上传到服务器。支持离线使用。" if is_zh else "All calculations are done locally in the browser, data is never uploaded. Works offline."
    seo_p3 = "完全免费，无需注册或登录。" if is_zh else "Completely free, no registration or login required."
    faq_title = "常见问题" if is_zh else "FAQ"
    faq_q1 = "数据安全吗？" if is_zh else "Is my data safe?"
    faq_a1 = "所有计算在浏览器本地完成，数据不会上传到任何服务器。" if is_zh else "All calculations are done locally in your browser, data is never sent to any server."
    faq_q2 = "需要注册吗？" if is_zh else "Do I need to register?"
    faq_a2 = "完全不需要，直接使用即可。" if is_zh else "Not at all, just use it directly."
    faq_q3 = "移动端能用吗？" if is_zh else "Does it work on mobile?"
    faq_a3 = "完美适配手机和平板，随时随地使用。" if is_zh else "Fully responsive, works on phones and tablets."
    
    html = f'''<!DOCTYPE html>
<html lang="{lang_code}">
<head>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-9W1157EBQV"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-9W1157EBQV');</script>
<script>window.addEventListener("error",function(e){{if(e&&e.message===""){{e.preventDefault();}}}});window.addEventListener("unhandledrejection",function(e){{if(e&&e.reason&&e.reason.message===""){{e.preventDefault();}}}});</script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="{desc}">
<meta name="keywords" content="在线{name},工具,在线工具,免费">
<title>{page_title}</title>
<link rel="canonical" href="{canonical}">
<meta property="og:title" content="{og_title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Free ToolBase">
<link rel="alternate" hreflang="{hreflang_self}" href="{canonical}">
<link rel="alternate" hreflang="{hreflang_other}" href="{alt_href}">
<link rel="alternate" hreflang="x-default" href="https://free-toolbase.com/en/{slug}/">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"SoftwareApplication","name":"{schema_name}","description":"{schema_desc}","applicationCategory":"UtilitiesApplication","operatingSystem":"Web","publisher":{{"@type":"Organization","name":"Free ToolBase","email":"dexshuang@google.com"}},"offers":{{"@type":"Offer","price":"0","priceCurrency":"USD"}}}}</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"HowTo","name":"{howto_name}","description":"{howto_desc}","totalTime":"PT2M","tool":{{"@type":"HowToTool","name":"{schema_name}"}},"step":[{{"@type":"HowToStep","position":1,"name":"{step1_name}","text":"{step1_text}"}},{{"@type":"HowToStep","position":2,"name":"{step2_name}","text":"{step2_text}"}},{{"@type":"HowToStep","position":3,"name":"{step3_name}","text":"{step3_text}"}},{{"@type":"HowToStep","position":4,"name":"{step4_name}","text":"{step4_text}"}}]}}</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"{home_label}","item":"https://free-toolbase.com/"}},{{"@type":"ListItem","position":2,"name":"{tools_label}","item":"https://free-toolbase.com/#tools"}},{{"@type":"ListItem","position":3,"name":"{breadcrumb_name}","item":"{canonical}"}}]}}</script>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#0f172a;color:#e2e8f0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,"PingFang SC","Microsoft YaHei",sans-serif;line-height:1.6;min-height:100vh}}
a{{color:#06b6d4;text-decoration:none}}
.container{{max-width:800px;margin:0 auto;padding:24px 16px}}
.header{{display:flex;justify-content:space-between;align-items:center;margin-bottom:24px;flex-wrap:wrap;gap:12px}}
.header h1{{font-size:1.6rem;color:#f1f5f9}}
.lang-switch{{display:flex;gap:4px;background:#1e293b;border-radius:8px;padding:4px;border:1px solid rgba(148,163,184,.1)}}
.lang-switch a{{padding:6px 12px;border-radius:5px;font-size:.85rem;color:#94a3b8}}
.lang-switch a.active{{background:rgba(6,182,212,.2);color:#22d3ee}}
.nav-back{{color:#64748b;font-size:.85rem;margin-bottom:16px}}
.nav-back a{{color:#64748b}}
.nav-back a:hover{{color:#94a3b8}}
.input-section{{background:#1e293b;border-radius:12px;padding:20px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1)}}
.input-section h2{{font-size:1.1rem;color:#f1f5f9;margin-bottom:12px}}
label{{display:block;font-size:.9rem;color:#94a3b8;margin-bottom:6px}}
input[type="text"],input[type="number"],input[type="date"],select{{width:100%;padding:12px;background:#0f172a;color:#e2e8f0;border:1px solid rgba(148,163,184,.2);border-radius:8px;font-size:1rem;outline:none}}
input:focus,select:focus{{border-color:rgba(6,182,212,.5)}}
.btn-row{{display:flex;gap:8px;flex-wrap:wrap;margin-top:16px}}
.btn{{padding:10px 24px;border:none;border-radius:6px;font-size:.9rem;cursor:pointer;transition:all .2s;font-weight:600}}
.btn-primary{{background:rgba(6,182,212,.2);color:#22d3ee;border:1px solid rgba(6,182,212,.3)}}
.btn-primary:hover{{background:rgba(6,182,212,.3)}}
.btn-secondary{{background:rgba(148,163,184,.1);color:#94a3b8;border:1px solid rgba(148,163,184,.2)}}
.btn-secondary:hover{{background:rgba(148,163,184,.2)}}
.btn-danger{{background:rgba(239,68,68,.15);color:#f87171;border:1px solid rgba(239,68,68,.2)}}
.btn-danger:hover{{background:rgba(239,68,68,.25)}}
.result-section{{background:#1e293b;border-radius:12px;padding:20px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1);display:none}}
.result-section.show{{display:block}}
.result-section h2{{font-size:1.1rem;color:#f1f5f9;margin-bottom:16px}}
.result-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px}}
.result-card{{background:#0f172a;border-radius:8px;padding:16px;border:1px solid rgba(148,163,184,.1)}}
.result-card .label{{font-size:.8rem;color:#94a3b8;margin-bottom:4px}}
.result-card .value{{font-size:1.5rem;color:#22d3ee;font-weight:600}}
.result-card .sub{{font-size:.8rem;color:#64748b;margin-top:4px}}
.info-section{{background:#1e293b;border-radius:12px;padding:20px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1)}}
.info-section h2{{font-size:1.1rem;color:#f1f5f9;margin-bottom:12px}}
.info-section p,.info-section li{{color:#94a3b8;font-size:.9rem;margin-bottom:8px}}
.info-section ul{{padding-left:20px}}
.info-section h3{{font-size:1rem;color:#e2e8f0;margin:16px 0 8px}}
.faq-item{{margin-bottom:12px;padding:12px;background:#0f172a;border-radius:8px;border:1px solid rgba(148,163,184,.1)}}
.faq-item h3{{font-size:.95rem;color:#e2e8f0;margin-bottom:6px}}
.faq-item p{{color:#94a3b8;font-size:.85rem}}
.form-row{{display:flex;gap:12px;flex-wrap:wrap}}
.form-row .form-group{{flex:1;min-width:150px}}
.form-group{{margin-bottom:12px}}
.footer{{border-top:1px solid rgba(148,163,184,.1);padding:24px 0;margin-top:48px;text-align:center;color:#64748b;font-size:.85rem}}
.footer a{{color:#06b6d4}}
.hero{{margin-bottom:16px;color:#94a3b8;font-size:.95rem}}
.hero p{{margin-bottom:4px}}
.badge{{display:inline-block;background:rgba(6,182,212,.15);color:#22d3ee;padding:4px 12px;border-radius:20px;font-size:.8rem;margin-bottom:16px}}
.ad-slot{{margin:16px auto;text-align:center;max-width:960px;min-height:90px;background:rgba(148,163,184,.05);border-radius:8px}}
.ad-slot:empty{{display:none}}
.ad-slot ins{{display:block}}
@media(max-width:640px){{.header{{flex-direction:column;align-items:flex-start}}.result-grid{{grid-template-columns:1fr}}.form-row{{flex-direction:column}}.form-row .form-group{{min-width:100%}}}}
.toast{{position:fixed;bottom:24px;left:50%;transform:translateX(-50%);background:#1e293b;color:#e2e8f0;padding:12px 24px;border-radius:8px;font-size:.9rem;border:1px solid rgba(148,163,184,.15);opacity:0;transition:opacity .3s;pointer-events:none;z-index:999}}
.toast.show{{opacity:1}}
</style>
</head>
<body>
<div class="container">
<div class="header"><h1>{icon} {name}</h1><div class="lang-switch"><a href="{zh_href}" class="{lang_zh_class}">中文</a><a href="{en_href}" class="{lang_en_class}">EN</a></div></div>
<p class="nav-back"><a href="{home_path}">{home_label}</a> &rsaquo; <a href="{tools_path}">{tools_label}</a> &rsaquo; {name}</p>
<div class="hero"><p>{hero}</p><span class="badge">{"零依赖·可离线使用" if is_zh else "Zero Deps · Offline Ready"}</span></div>
{tool_body}
<div class="info-section">
<h2>{seo_title}</h2>
<p>{seo_p1}</p>
<p>{seo_p2}</p>
<p>{seo_p3}</p>
<h3>{faq_title}</h3>
<div class="faq-item"><h3>{faq_q1}</h3><p>{faq_a1}</p></div>
<div class="faq-item"><h3>{faq_q2}</h3><p>{faq_a2}</p></div>
<div class="faq-item"><h3>{faq_q3}</h3><p>{faq_a3}</p></div>
</div>
<div class="footer"><p>&copy; 2026 Free ToolBase | <a href="{'../privacy/' if is_zh else '../../privacy/'}">{'隐私政策' if is_zh else 'Privacy'}</a> | <a href="{'../terms/' if is_zh else '../../terms/'}">{'服务条款' if is_zh else 'Terms'}</a></p></div>
</div>
<div class="toast" id="toast"></div>
<script>
function showToast(msg){{var t=document.getElementById('toast');t.textContent=msg;t.classList.add('show');setTimeout(function(){{t.classList.remove('show')}},2000)}}
{tool_js}
</script>
</body>
</html>'''
    return html


def budget_calculator_body(is_zh):
    if is_zh:
        body = '''
<div class="input-section">
<h2>📊 添加收支项目</h2>
<div class="form-row">
<div class="form-group"><label>项目名称</label><input type="text" id="itemName" placeholder="如：工资、房租、餐饮"></div>
<div class="form-group"><label>金额</label><input type="number" id="itemAmount" placeholder="输入金额" min="0" step="0.01"></div>
<div class="form-group"><label>类型</label><select id="itemType"><option value="income">💰 收入</option><option value="expense">💸 支出</option></select></div>
</div>
<div class="form-group"><label>分类</label><select id="itemCategory"><option value="salary">工资</option><option value="freelance">自由职业</option><option value="investment">投资</option><option value="rent">房租</option><option value="food">餐饮</option><option value="transport">交通</option><option value="entertainment">娱乐</option><option value="shopping">购物</option><option value="utilities">水电</option><option value="other">其他</option></select></div>
<div class="btn-row"><button class="btn btn-primary" onclick="addItem()">➕ 添加项目</button><button class="btn btn-secondary" onclick="resetAll()">🔄 重置</button></div>
</div>
<div class="input-section">
<h2>📋 收支清单</h2>
<div id="itemList" style="max-height:300px;overflow-y:auto"><p style="color:#64748b;text-align:center;padding:20px">暂无项目，请添加</p></div>
</div>
<div class="result-section" id="resultSection">
<h2>📈 预算分析</h2>
<div class="result-grid">
<div class="result-card"><div class="label">总收入</div><div class="value" style="color:#4ade80" id="totalIncome">¥0</div></div>
<div class="result-card"><div class="label">总支出</div><div class="value" style="color:#f87171" id="totalExpense">¥0</div></div>
<div class="result-card"><div class="label">结余</div><div class="value" id="balance">¥0</div></div>
<div class="result-card"><div class="label">储蓄率</div><div class="value" id="savingsRate">0%</div></div>
</div>
</div>'''
    else:
        body = '''
<div class="input-section">
<h2>📊 Add Item</h2>
<div class="form-row">
<div class="form-group"><label>Item Name</label><input type="text" id="itemName" placeholder="e.g. Salary, Rent, Food"></div>
<div class="form-group"><label>Amount</label><input type="number" id="itemAmount" placeholder="Enter amount" min="0" step="0.01"></div>
<div class="form-group"><label>Type</label><select id="itemType"><option value="income">💰 Income</option><option value="expense">💸 Expense</option></select></div>
</div>
<div class="form-group"><label>Category</label><select id="itemCategory"><option value="salary">Salary</option><option value="freelance">Freelance</option><option value="investment">Investment</option><option value="rent">Rent</option><option value="food">Food</option><option value="transport">Transport</option><option value="entertainment">Entertainment</option><option value="shopping">Shopping</option><option value="utilities">Utilities</option><option value="other">Other</option></select></div>
<div class="btn-row"><button class="btn btn-primary" onclick="addItem()">➕ Add Item</button><button class="btn btn-secondary" onclick="resetAll()">🔄 Reset</button></div>
</div>
<div class="input-section">
<h2>📋 Item List</h2>
<div id="itemList" style="max-height:300px;overflow-y:auto"><p style="color:#64748b;text-align:center;padding:20px">No items yet, add some</p></div>
</div>
<div class="result-section" id="resultSection">
<h2>📈 Budget Analysis</h2>
<div class="result-grid">
<div class="result-card"><div class="label">Total Income</div><div class="value" style="color:#4ade80" id="totalIncome">$0</div></div>
<div class="result-card"><div class="label">Total Expense</div><div class="value" style="color:#f87171" id="totalExpense">$0</div></div>
<div class="result-card"><div class="label">Balance</div><div class="value" id="balance">$0</div></div>
<div class="result-card"><div class="label">Savings Rate</div><div class="value" id="savingsRate">0%</div></div>
</div>
</div>'''
    
    js = r'''
var items=[];
function addItem(){
  var n=document.getElementById('itemName').value.trim();
  var a=parseFloat(document.getElementById('itemAmount').value);
  var t=document.getElementById('itemType').value;
  var c=document.getElementById('itemCategory').value;
  if(!n||isNaN(a)||a<=0){showToast('请填写有效的名称和金额');return;}
  items.push({name:n,amount:a,type:t,category:c});
  document.getElementById('itemName').value='';
  document.getElementById('itemAmount').value='';
  renderItems();
}
function removeItem(i){items.splice(i,1);renderItems();}
function resetAll(){items=[];renderItems();document.getElementById('resultSection').classList.remove('show');}
function renderItems(){
  var list=document.getElementById('itemList');
  if(items.length===0){list.innerHTML='<p style="color:#64748b;text-align:center;padding:20px">'+(document.documentElement.lang==='zh-CN'?'暂无项目，请添加':'No items yet, add some')+'</p>';
    document.getElementById('resultSection').classList.remove('show');return;}
  var h='<table style="width:100%;border-collapse:collapse"><thead><tr style="border-bottom:1px solid rgba(148,163,184,.2)"><th style="padding:8px;text-align:left;color:#94a3b8;font-size:.85rem">'+(document.documentElement.lang==='zh-CN'?'名称':'Name')+'</th><th style="padding:8px;text-align:right;color:#94a3b8;font-size:.85rem">'+(document.documentElement.lang==='zh-CN'?'金额':'Amount')+'</th><th style="padding:8px;text-align:center;color:#94a3b8;font-size:.85rem">'+(document.documentElement.lang==='zh-CN'?'类型':'Type')+'</th><th style="padding:8px;text-align:center;color:#94a3b8;font-size:.85rem"></th></tr></thead><tbody>';
  for(var i=0;i<items.length;i++){
    var it=items[i];
    h+='<tr style="border-bottom:1px solid rgba(148,163,184,.05)"><td style="padding:8px;font-size:.9rem">'+it.name+'</td><td style="padding:8px;text-align:right;font-size:.9rem;color:'+(it.type==='income'?'#4ade80':'#f87171')+'">'+(document.documentElement.lang==='zh-CN'?'¥':'$')+it.amount.toFixed(2)+'</td><td style="padding:8px;text-align:center;font-size:.85rem">'+(it.type==='income'?(document.documentElement.lang==='zh-CN'?'收入':'Income'):(document.documentElement.lang==='zh-CN'?'支出':'Expense'))+'</td><td style="padding:8px;text-align:center"><button class="btn btn-danger" style="padding:4px 8px;font-size:.8rem" onclick="removeItem('+i+')">✕</button></td></tr>';
  }
  h+='</tbody></table>';
  list.innerHTML=h;
  calcBudget();
}
function calcBudget(){
  var inc=0,exp=0;
  for(var i=0;i<items.length;i++){
    if(items[i].type==='income')inc+=items[i].amount;else exp+=items[i].amount;
  }
  var bal=inc-exp;
  var rate=inc>0?Math.round(bal/inc*100):0;
  var sym=document.documentElement.lang==='zh-CN'?'¥':'$';
  document.getElementById('totalIncome').textContent=sym+inc.toFixed(2);
  document.getElementById('totalExpense').textContent=sym+exp.toFixed(2);
  document.getElementById('balance').textContent=sym+bal.toFixed(2);
  document.getElementById('balance').style.color=bal>=0?'#4ade80':'#f87171';
  document.getElementById('savingsRate').textContent=rate+'%';
  document.getElementById('resultSection').classList.add('show');
}
'''
    return body, js


def decision_tree_body(is_zh):
    if is_zh:
        body = '''
<div class="input-section">
<h2>🌳 创建决策节点</h2>
<div class="form-row">
<div class="form-group"><label>问题/决策描述</label><input type="text" id="nodeText" placeholder="如：今天要不要出门？"></div>
</div>
<div class="btn-row"><button class="btn btn-primary" onclick="addRootNode()">➕ 添加根节点</button><button class="btn btn-secondary" onclick="exportTree()">📋 导出大纲</button><button class="btn btn-secondary" onclick="resetTree()">🔄 重置</button></div>
</div>
<div class="input-section" id="treeSection" style="display:none">
<h2>📊 决策树</h2>
<div id="treeContainer" style="min-height:200px"></div>
</div>
<div class="result-section" id="exportSection">
<h2>📋 导出结果</h2>
<pre id="exportText" style="background:#0f172a;padding:16px;border-radius:8px;color:#e2e8f0;white-space:pre-wrap;font-size:.9rem;max-height:400px;overflow-y:auto"></pre>
</div>'''
    else:
        body = '''
<div class="input-section">
<h2>🌳 Create Decision Node</h2>
<div class="form-row">
<div class="form-group"><label>Question / Decision</label><input type="text" id="nodeText" placeholder="e.g. Should I go out today?"></div>
</div>
<div class="btn-row"><button class="btn btn-primary" onclick="addRootNode()">➕ Add Root Node</button><button class="btn btn-secondary" onclick="exportTree()">📋 Export Outline</button><button class="btn btn-secondary" onclick="resetTree()">🔄 Reset</button></div>
</div>
<div class="input-section" id="treeSection" style="display:none">
<h2>📊 Decision Tree</h2>
<div id="treeContainer" style="min-height:200px"></div>
</div>
<div class="result-section" id="exportSection">
<h2>📋 Export Result</h2>
<pre id="exportText" style="background:#0f172a;padding:16px;border-radius:8px;color:#e2e8f0;white-space:pre-wrap;font-size:.9rem;max-height:400px;overflow-y:auto"></pre>
</div>'''
    
    js = r'''
var treeData=null;
var selectedParent=null;
function addRootNode(){
  var t=document.getElementById('nodeText').value.trim();
  if(!t){showToast(document.documentElement.lang==='zh-CN'?'请输入节点描述':'Please enter node description');return;}
  if(!treeData){treeData={text:t,children:[],id:'n0'};}
  else if(selectedParent!==null){addChildTo(selectedParent,t);}
  else{treeData={text:t,children:[],id:'n0'};}
  document.getElementById('nodeText').value='';
  selectedParent=null;
  renderTree();
}
function addChildTo(parentId,text){
  function find(arr,id){
    for(var i=0;i<arr.length;i++){
      if(arr[i].id===id)return arr[i];
      if(arr[i].children){var f=find(arr[i].children,id);if(f)return f;}
    }
    return null;
  }
  var p=find([treeData],parentId);
  if(p){if(!p.children)p.children=[];p.children.push({text:text,children:[],id:'n'+Date.now()+Math.random().toString(36).slice(2)});}
}
function removeNode(id){
  function removeFrom(arr,id){
    for(var i=0;i<arr.length;i++){
      if(arr[i].id===id){arr.splice(i,1);return true;}
      if(arr[i].children&&removeFrom(arr[i].children,id))return true;
    }
    return false;
  }
  if(treeData&&treeData.id===id){treeData=null;renderTree();return;}
  if(treeData)removeFrom([treeData],id);
  renderTree();
}
function resetTree(){treeData=null;selectedParent=null;renderTree();document.getElementById('exportText').textContent='';}
function renderTree(){
  var c=document.getElementById('treeContainer');
  var s=document.getElementById('treeSection');
  if(!treeData){c.innerHTML='';s.style.display='none';return;}
  s.style.display='block';
  function renderNode(node,level){
    var pad=level*24;
    var bg=level===0?'rgba(6,182,212,.1)':level===1?'rgba(34,197,94,.08)':level===2?'rgba(234,179,8,.08)':'rgba(148,163,184,.05)';
    var color=level===0?'#22d3ee':level===1?'#4ade80':level===2?'#facc15':'#94a3b8';
    var h='<div style="margin-left:'+pad+'px;margin-bottom:8px;background:'+bg+';border-radius:8px;padding:10px 12px;border-left:3px solid '+color+'">';
    h+='<div style="display:flex;justify-content:space-between;align-items:center">';
    h+='<span style="color:'+color+';font-weight:600">'+node.text+'</span>';
    h+='<div style="display:flex;gap:4px">';
    h+='<button onclick="selectParent(\''+node.id+'\')" style="background:rgba(6,182,212,.15);color:#22d3ee;border:1px solid rgba(6,182,212,.2);border-radius:4px;padding:2px 8px;font-size:.75rem;cursor:pointer">+ '+(document.documentElement.lang==='zh-CN'?'子节点':'Child')+'</button>';
    h+='<button onclick="removeNode(\''+node.id+'\')" style="background:rgba(239,68,68,.1);color:#f87171;border:1px solid rgba(239,68,68,.2);border-radius:4px;padding:2px 8px;font-size:.75rem;cursor:pointer">✕</button>';
    h+='</div></div></div>';
    if(node.children&&node.children.length>0){
      for(var i=0;i<node.children.length;i++){h+=renderNode(node.children[i],level+1);}
    }
    return h;
  }
  c.innerHTML=renderNode(treeData,0);
  if(selectedParent!==null){showToast(document.documentElement.lang==='zh-CN'?'已选择父节点，输入新节点描述后点击添加':'Parent selected, enter new node text and click add');}
}
function selectParent(id){selectedParent=id;showToast(document.documentElement.lang==='zh-CN'?'已选择父节点':'Parent node selected');}
function exportTree(){
  if(!treeData){showToast(document.documentElement.lang==='zh-CN'?'请先创建决策树':'Please create a decision tree first');return;}
  var out='';
  function walk(node,level){
    var indent='  '.repeat(level);
    out+=indent+(level===0?'● ':'├─ ')+node.text+'\n';
    if(node.children){for(var i=0;i<node.children.length;i++)walk(node.children[i],level+1);}
  }
  walk(treeData,0);
  document.getElementById('exportText').textContent=out;
  document.getElementById('exportSection').classList.add('show');
}
'''
    return body, js


def date_diff_body(is_zh):
    if is_zh:
        body = '''
<div class="input-section">
<h2>📅 选择日期</h2>
<div class="form-row">
<div class="form-group"><label>起始日期</label><input type="date" id="startDate"></div>
<div class="form-group"><label>结束日期</label><input type="date" id="endDate"></div>
</div>
<div class="form-group"><label><input type="checkbox" id="excludeWeekends" style="width:auto;margin-right:8px"> 排除周末（仅计算工作日）</label></div>
<div class="btn-row"><button class="btn btn-primary" onclick="calcDiff()">📊 计算差值</button><button class="btn btn-secondary" onclick="resetDates()">🔄 重置</button></div>
</div>
<div class="result-section" id="resultSection">
<h2>📈 计算结果</h2>
<div class="result-grid">
<div class="result-card"><div class="label">相差天数</div><div class="value" id="diffDays">0</div></div>
<div class="result-card"><div class="label">相差周数</div><div class="value" id="diffWeeks">0</div><div class="sub" id="diffWeeksRemainder"></div></div>
<div class="result-card"><div class="label">相差月数</div><div class="value" id="diffMonths">0</div><div class="sub" id="diffMonthsRemainder"></div></div>
<div class="result-card"><div class="label">相差年数</div><div class="value" id="diffYears">0</div><div class="sub" id="diffYearsRemainder"></div></div>
</div>
<div id="workdayInfo" style="margin-top:16px;padding:12px;background:#0f172a;border-radius:8px;display:none">
<p style="color:#94a3b8;font-size:.9rem">📌 <span id="workdayCount"></span></p>
</div>
</div>'''
    else:
        body = '''
<div class="input-section">
<h2>📅 Select Dates</h2>
<div class="form-row">
<div class="form-group"><label>Start Date</label><input type="date" id="startDate"></div>
<div class="form-group"><label>End Date</label><input type="date" id="endDate"></div>
</div>
<div class="form-group"><label><input type="checkbox" id="excludeWeekends" style="width:auto;margin-right:8px"> Exclude weekends (working days only)</label></div>
<div class="btn-row"><button class="btn btn-primary" onclick="calcDiff()">📊 Calculate Difference</button><button class="btn btn-secondary" onclick="resetDates()">🔄 Reset</button></div>
</div>
<div class="result-section" id="resultSection">
<h2>📈 Result</h2>
<div class="result-grid">
<div class="result-card"><div class="label">Days</div><div class="value" id="diffDays">0</div></div>
<div class="result-card"><div class="label">Weeks</div><div class="value" id="diffWeeks">0</div><div class="sub" id="diffWeeksRemainder"></div></div>
<div class="result-card"><div class="label">Months</div><div class="value" id="diffMonths">0</div><div class="sub" id="diffMonthsRemainder"></div></div>
<div class="result-card"><div class="label">Years</div><div class="value" id="diffYears">0</div><div class="sub" id="diffYearsRemainder"></div></div>
</div>
<div id="workdayInfo" style="margin-top:16px;padding:12px;background:#0f172a;border-radius:8px;display:none">
<p style="color:#94a3b8;font-size:.9rem">📌 <span id="workdayCount"></span></p>
</div>
</div>'''
    
    js = r'''
function calcDiff(){
  var s=document.getElementById('startDate').value;
  var e=document.getElementById('endDate').value;
  if(!s||!e){showToast(document.documentElement.lang==='zh-CN'?'请选择起始和结束日期':'Please select start and end dates');return;}
  var sd=new Date(s);var ed=new Date(e);
  if(ed<sd){showToast(document.documentElement.lang==='zh-CN'?'结束日期必须晚于起始日期':'End date must be after start date');return;}
  var excludeWE=document.getElementById('excludeWeekends').checked;
  var diffMs=ed-sd;
  var diffDays=Math.floor(diffMs/(1000*60*60*24));
  if(excludeWE){
    var wd=0;
    var cur=new Date(sd);
    while(cur<=ed){
      var dow=cur.getDay();
      if(dow!==0&&dow!==6)wd++;
      cur.setDate(cur.getDate()+1);
    }
    diffDays=wd;
  }
  var diffWeeks=Math.floor(diffDays/7);
  var weekRem=diffDays%7;
  var yearDiff=ed.getFullYear()-sd.getFullYear();
  var monthDiff=ed.getMonth()-sd.getMonth();
  var totalMonths=yearDiff*12+monthDiff;
  if(ed.getDate()<sd.getDate())totalMonths--;
  var adjDate=new Date(sd);
  adjDate.setMonth(adjDate.getMonth()+totalMonths);
  var remainingDays=Math.floor((ed-adjDate)/(1000*60*60*24));
  if(remainingDays<0){totalMonths--;adjDate=new Date(sd);adjDate.setMonth(adjDate.getMonth()+totalMonths);remainingDays=Math.floor((ed-adjDate)/(1000*60*60*24));}
  var years=Math.floor(totalMonths/12);
  var months=totalMonths%12;
  document.getElementById('diffDays').textContent=diffDays;
  document.getElementById('diffWeeks').textContent=diffWeeks;
  var isZh=document.documentElement.lang==='zh-CN';
  document.getElementById('diffWeeksRemainder').textContent=(isZh?'余 ':'+ ')+weekRem+(isZh?' 天':' days');
  document.getElementById('diffMonths').textContent=totalMonths;
  document.getElementById('diffMonthsRemainder').textContent=(isZh?'余 ':'+ ')+remainingDays+(isZh?' 天':' days');
  document.getElementById('diffYears').textContent=years;
  document.getElementById('diffYearsRemainder').textContent=(isZh?'余 ':'+ ')+months+(isZh?' 个月 ':' months ')+remainingDays+(isZh?' 天':' days');
  if(excludeWE){
    document.getElementById('workdayInfo').style.display='block';
    document.getElementById('workdayCount').textContent=(isZh?'工作日数量：':'Working days: ')+diffDays+(isZh?' 天':' days');
  }else{document.getElementById('workdayInfo').style.display='none';}
  document.getElementById('resultSection').classList.add('show');
}
function resetDates(){
  document.getElementById('startDate').value='';
  document.getElementById('endDate').value='';
  document.getElementById('excludeWeekends').checked=false;
  document.getElementById('resultSection').classList.remove('show');
  document.getElementById('workdayInfo').style.display='none';
}
'''
    return body, js


def main():
    for tool in TOOLS:
        slug = tool["slug"]
        # Chinese version
        zh_dir = os.path.join(BASE, slug)
        os.makedirs(zh_dir, exist_ok=True)
        zh_html = make_html(tool, "zh")
        with open(os.path.join(zh_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(zh_html)
        print(f"Created: {slug}/index.html (zh)")
        
        # English version
        en_dir = os.path.join(BASE, "en", slug)
        os.makedirs(en_dir, exist_ok=True)
        en_html = make_html(tool, "en")
        with open(os.path.join(en_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(en_html)
        print(f"Created: en/{slug}/index.html (en)")

if __name__ == "__main__":
    main()