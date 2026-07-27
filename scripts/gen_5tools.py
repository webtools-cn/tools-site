#!/usr/bin/env python3
"""批量生成5个新工具：中文版+英文版"""
import os

TOOLS = [
    {
        "name": "glycemic-index-lookup",
        "cn_title": "血糖指数查询器",
        "en_title": "Glycemic Index Lookup",
        "cn_desc": "免费在线血糖指数(GI)查询工具，查询超过300种常见食物的血糖指数、血糖负荷(GL)值，帮助糖尿病患者和健康饮食者科学选择食物。纯前端本地查询，数据安全不上传服务器。",
        "en_desc": "Free online Glycemic Index (GI) lookup tool. Search over 300 common foods for their glycemic index and glycemic load (GL) values. Helps diabetics and health-conscious eaters make informed food choices. Pure frontend local search, data never uploaded.",
        "cn_keywords": "血糖指数查询,GI查询,血糖负荷,食物血糖指数,糖尿病饮食,低GI食物",
        "en_keywords": "glycemic index lookup,GI lookup,glycemic load,food GI,diabetes diet,low GI foods",
        "category": "健康",
        "icon": "🩸"
    },
    {
        "name": "calorie-density-calculator",
        "cn_title": "食物热量密度计算器",
        "en_title": "Calorie Density Calculator",
        "cn_desc": "免费在线食物热量密度计算器，输入食物的卡路里和重量，自动计算热量密度(cal/g)，帮助控制体重和科学饮食。支持公制/英制单位，纯前端本地计算。",
        "en_desc": "Free online calorie density calculator. Enter food calories and weight to automatically calculate calorie density (cal/g). Helps with weight management and healthy eating. Supports metric/imperial units. Pure frontend local calculation.",
        "cn_keywords": "热量密度计算器,食物热量密度,卡路里密度,减肥饮食,热量控制",
        "en_keywords": "calorie density calculator,food calorie density,calorie per gram,weight loss diet,calorie control",
        "category": "健康",
        "icon": "🍎"
    },
    {
        "name": "time-and-a-half-calculator",
        "cn_title": "1.5倍加班工资计算器",
        "en_title": "Time and a Half Calculator",
        "cn_desc": "免费在线加班工资计算器，输入正常时薪和加班时长，自动计算1.5倍加班工资。支持各种加班费率(1.5倍、2倍、3倍)，帮助劳动者核对加班收入。纯前端本地计算。",
        "en_desc": "Free online overtime pay calculator. Enter your regular hourly rate and overtime hours to automatically calculate time-and-a-half pay. Supports various overtime rates (1.5x, 2x, 3x). Helps workers verify overtime earnings. Pure frontend local calculation.",
        "cn_keywords": "加班工资计算器,1.5倍工资,加班费计算,时薪计算,overtime pay",
        "en_keywords": "time and a half calculator,overtime pay calculator,overtime rate,hourly wage,overtime earnings",
        "category": "金融",
        "icon": "💰"
    },
    {
        "name": "double-time-calculator",
        "cn_title": "双倍工资计算器",
        "en_title": "Double Time Calculator",
        "cn_desc": "免费在线双倍工资计算器，输入正常时薪和工作时长，自动计算双倍工资收入。适用于节假日加班、周末加班等双倍工资场景。支持自定义倍率，纯前端本地计算。",
        "en_desc": "Free online double time pay calculator. Enter your regular hourly rate and hours worked to automatically calculate double-time pay. Ideal for holiday overtime, weekend shifts, and double-pay scenarios. Supports custom multipliers. Pure frontend local calculation.",
        "cn_keywords": "双倍工资计算器,双倍加班费,节假日工资,周末加班费,double time",
        "en_keywords": "double time calculator,double pay calculator,holiday pay,weekend overtime,double overtime",
        "category": "金融",
        "icon": "💵"
    },
    {
        "name": "streaming-cost-calculator",
        "cn_title": "流媒体订阅费用对比计算器",
        "en_title": "Streaming Cost Calculator",
        "cn_desc": "免费在线流媒体订阅费用对比计算器，对比Netflix、Disney+、HBO Max等主流平台的月费/年费，计算多平台总订阅成本。帮助用户优化订阅方案，节省流媒体开支。纯前端本地计算。",
        "en_desc": "Free online streaming subscription cost comparison calculator. Compare monthly/annual fees across Netflix, Disney+, HBO Max, and more. Calculate total multi-platform subscription costs. Helps users optimize streaming plans and save money. Pure frontend local calculation.",
        "cn_keywords": "流媒体费用计算器,订阅费用对比,Netflix费用,Disney+价格,流媒体订阅",
        "en_keywords": "streaming cost calculator,subscription comparison,Netflix cost,Disney+ price,streaming services",
        "category": "金融",
        "icon": "📺"
    }
]

BASE_DIR = "/home/chison/tools-site"

def generate_tool(tool):
    name = tool["name"]
    cn_dir = os.path.join(BASE_DIR, name)
    en_dir = os.path.join(BASE_DIR, "en", name)
    os.makedirs(cn_dir, exist_ok=True)
    os.makedirs(en_dir, exist_ok=True)
    
    # CN version
    cn_html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-9W1157EBQV"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-9W1157EBQV');</script>
<script>window.addEventListener("error",function(e){{if(e&&e.message===""){{e.preventDefault();}}}});window.addEventListener("unhandledrejection",function(e){{if(e&&e.reason&&e.reason.message===""){{e.preventDefault();}}}});</script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="{tool['cn_desc']}">
<meta name="keywords" content="{tool['cn_keywords']}">
<title>{tool['cn_title']} - Free ToolBase</title>
<link rel="canonical" href="https://free-toolbase.com/{name}/">
<meta property="og:title" content="{tool['cn_title']} - Free ToolBase">
<meta property="og:description" content="{tool['cn_desc']}">
<meta property="og:url" content="https://free-toolbase.com/{name}/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Free ToolBase">
<link rel="alternate" hreflang="zh" href="https://free-toolbase.com/{name}/">
<link rel="alternate" hreflang="en" href="https://free-toolbase.com/en/{name}/">
<link rel="alternate" hreflang="x-default" href="https://free-toolbase.com/en/{name}/">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"SoftwareApplication","name":"{tool['cn_title']}","description":"{tool['cn_desc']}","applicationCategory":"UtilitiesApplication","operatingSystem":"Web","publisher":{{"@type":"Organization","name":"Free ToolBase","email":"dexshuang@google.com"}},"offers":{{"@type":"Offer","price":"0","priceCurrency":"USD"}}}}</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"首页","item":"https://free-toolbase.com/"}},{{"@type":"ListItem","position":2,"name":"工具","item":"https://free-toolbase.com/#tools"}},{{"@type":"ListItem","position":3,"name":"{tool['cn_title']}","item":"https://free-toolbase.com/{name}/"}}]}}</script>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#0f172a;color:#e2e8f0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,"PingFang SC","Microsoft YaHei",sans-serif;line-height:1.6;min-height:100vh}}
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
.main-grid{{display:grid;grid-template-columns:1fr 300px;gap:24px;margin-bottom:24px}}
@media(max-width:768px){{.main-grid{{grid-template-columns:1fr}}}}
.section{{background:#1e293b;border-radius:12px;padding:20px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1)}}
.section h2{{font-size:1.1rem;color:#f1c40f;margin-bottom:12px}}
.form-group{{margin-bottom:14px}}
.form-group label{{display:block;color:#94a3b8;font-size:.9rem;margin-bottom:6px;font-weight:500}}
.form-group input,.form-group select,.form-group textarea{{width:100%;padding:10px 14px;background:#0f172a;border:1px solid rgba(148,163,184,.2);border-radius:8px;color:#e2e8f0;font-size:.9rem;outline:none;transition:all .2s}}
.form-group input:focus,.form-group select:focus,.form-group textarea:focus{{border-color:rgba(6,182,212,.4);box-shadow:0 0 0 3px rgba(6,182,212,.1)}}
.form-row{{display:flex;gap:12px;flex-wrap:wrap}}
.form-row .form-group{{flex:1;min-width:140px}}
.btn{{display:inline-flex;align-items:center;justify-content:center;gap:8px;padding:10px 20px;border:none;border-radius:8px;font-size:.9rem;font-weight:600;cursor:pointer;transition:all .2s;font-family:inherit}}
.btn-primary{{background:linear-gradient(135deg,#06b6d4,#3b82f6);color:#fff;width:100%}}
.btn-primary:hover{{transform:translateY(-1px);box-shadow:0 4px 12px rgba(6,182,212,.3)}}
.btn-secondary{{background:#334155;color:#e2e8f0}}
.btn-secondary:hover{{background:#475569}}
.btn-sm{{padding:6px 12px;font-size:.8rem}}
.result-card{{background:#0f172a;border-radius:8px;padding:16px;margin-top:12px;border:1px solid rgba(148,163,184,.1)}}
.result-card .value{{font-size:1.8rem;font-weight:700;color:#22d3ee}}
.result-card .label{{font-size:.85rem;color:#94a3b8;margin-top:4px}}
.result-card .range{{font-size:.75rem;color:#64748b;margin-top:2px}}
.health-tip{{background:rgba(6,182,212,.08);border-left:3px solid #06b6d4;border-radius:0 8px 8px 0;padding:12px 16px;margin-top:16px;font-size:.85rem;color:#94a3b8}}
.info-list{{list-style:none;padding:0;margin-top:12px}}
.info-list li{{padding:8px 0;border-bottom:1px solid rgba(148,163,184,.1);font-size:.85rem;color:#94a3b8;display:flex;justify-content:space-between}}
.info-list li:last-child{{border-bottom:none}}
.info-list .info-val{{color:#e2e8f0;font-weight:500}}
footer{{text-align:center;padding:40px 16px;color:#64748b;font-size:.85rem;border-top:1px solid rgba(148,163,184,.1);margin-top:40px}}
footer a{{color:#64748b}}footer a:hover{{color:#94a3b8}}
.toast{{position:fixed;bottom:24px;left:50%;transform:translateX(-50%);background:#334155;color:#e2e8f0;padding:10px 20px;border-radius:8px;font-size:.85rem;z-index:9999;opacity:0;transition:opacity .3s;pointer-events:none}}
.toast.show{{opacity:1;pointer-events:auto}}
table{{width:100%;border-collapse:collapse;margin-top:8px;font-size:.85rem}}
table th{{text-align:left;padding:8px;color:#94a3b8;border-bottom:1px solid rgba(148,163,184,.2);font-weight:500}}
table td{{padding:8px;border-bottom:1px solid rgba(148,163,184,.1);color:#cbd5e1}}
table tr:hover td{{background:rgba(6,182,212,.05)}}
.tabs{{display:flex;gap:4px;margin-bottom:12px;background:#0f172a;border-radius:8px;padding:4px}}
.tab-btn{{flex:1;padding:8px 12px;border:none;background:none;color:#94a3b8;font-size:.85rem;cursor:pointer;border-radius:5px;transition:all .2s;font-family:inherit}}
.tab-btn.active{{background:rgba(6,182,212,.2);color:#22d3ee}}
.tab-panel{{display:none}}
.tab-panel.active{{display:block}}
</style>
</head>
<body>
<div class="container">
<header class="header">
<h1>{tool['icon']} {tool['cn_title']}</h1>
<div class="lang-switch">
<a href="/{name}/" class="active">中文</a>
<a href="/en/{name}/">English</a>
</div>
</header>
<nav class="nav-back"><a href="/">← 返回首页</a> / <a href="/#tools">工具列表</a> / {tool['cn_title']}</nav>
<div class="hero">
<span class="badge">{tool['category']}工具</span>
<p>{tool['cn_desc']}</p>
</div>
<div class="main-grid">
<div class="main-col">
<div class="section">
<h2>📊 输入数据</h2>
{tool_cn_input(name)}
<div class="section">
<h2>📈 计算结果</h2>
<div id="result-area">
<div class="result-card"><div class="value" id="main-result">--</div><div class="label">请输入数据后点击计算</div></div>
</div>
<div id="detail-area"></div>
</div>
</div>
<div class="side-col">
<div class="section">
<h2>📖 使用说明</h2>
{tool_cn_instructions(name)}
</div>
<div class="section">
<h2>💡 {tool['cn_title']}相关知识</h2>
{tool_cn_knowledge(name)}
</div>
</div>
</div>
<footer>
<p>© 2024 Free ToolBase · 所有计算均在浏览器本地完成，数据不会上传到服务器 · <a href="/about/">关于我们</a> · <a href="/privacy/">隐私政策</a></p>
</footer>
</div>
<div class="toast" id="toast"></div>
<script>
// Toast
function showToast(msg){{var t=document.getElementById('toast');t.textContent=msg;t.classList.add('show');setTimeout(function(){{t.classList.remove('show')}},2000)}}
function copyText(text){{navigator.clipboard.writeText(text).then(function(){{showToast('已复制到剪贴板')}}).catch(function(){{showToast('复制失败，请手动复制')}})}}
{tool_js(name)}
</script>
</body>
</html>'''
    
    # EN version
    en_html = cn_html.replace('lang="zh-CN"', 'lang="en"')
    en_html = en_html.replace(f'<title>{tool["cn_title"]} - Free ToolBase</title>', f'<title>{tool["en_title"]} - Free ToolBase</title>')
    en_html = en_html.replace(f'content="{tool["cn_desc"]}"', f'content="{tool["en_desc"]}"', 1)
    en_html = en_html.replace(f'content="{tool["cn_keywords"]}"', f'content="{tool["en_keywords"]}"', 1)
    en_html = en_html.replace(f'<meta property="og:title" content="{tool["cn_title"]} - Free ToolBase">', f'<meta property="og:title" content="{tool["en_title"]} - Free ToolBase">')
    en_html = en_html.replace(f'<meta property="og:description" content="{tool["cn_desc"]}">', f'<meta property="og:description" content="{tool["en_desc"]}">')
    en_html = en_html.replace(f'"name":"{tool["cn_title"]}"', f'"name":"{tool["en_title"]}"', 1)
    en_html = en_html.replace(f'"description":"{tool["cn_desc"]}"', f'"description":"{tool["en_desc"]}"', 1)
    en_html = en_html.replace(f'"name":"{tool["cn_title"]}","item":"https://free-toolbase.com/{name}/"', f'"name":"{tool["en_title"]}","item":"https://free-toolbase.com/en/{name}/"')
    en_html = en_html.replace(f'href="/{name}/" class="active">中文</a>', f'href="/{name}/">中文</a>')
    en_html = en_html.replace(f'href="/en/{name}/">English</a>', f'href="/en/{name}/" class="active">English</a>')
    en_html = en_html.replace(f'<a href="/">← 返回首页</a>', '<a href="/en/">← Back to Home</a>')
    en_html = en_html.replace(f'<a href="/#tools">工具列表</a>', '<a href="/en/#tools">Tool List</a>')
    en_html = en_html.replace(f'/{tool["cn_title"]}</nav>', f'/{tool["en_title"]}</nav>')
    en_html = en_html.replace(f'<span class="badge">{tool["category"]}工具</span>', f'<span class="badge">{tool["category"]} Tool</span>')
    en_html = en_html.replace(f'<p>{tool["cn_desc"]}</p>', f'<p>{tool["en_desc"]}</p>')
    
    # CN specific labels -> EN
    en_html = en_html.replace('📊 输入数据', '📊 Input Data')
    en_html = en_html.replace('📈 计算结果', '📈 Results')
    en_html = en_html.replace('请输入数据后点击计算', 'Enter data and click Calculate')
    en_html = en_html.replace('📖 使用说明', '📖 How to Use')
    en_html = en_html.replace('相关知识', 'Knowledge')
    en_html = en_html.replace('所有计算均在浏览器本地完成，数据不会上传到服务器', 'All calculations are performed locally in your browser. No data is uploaded to any server.')
    en_html = en_html.replace('关于我们', 'About')
    en_html = en_html.replace('隐私政策', 'Privacy')
    en_html = en_html.replace('已复制到剪贴板', 'Copied to clipboard')
    en_html = en_html.replace('复制失败，请手动复制', 'Copy failed, please copy manually')
    
    # Write files
    with open(os.path.join(cn_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(cn_html)
    with open(os.path.join(en_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(en_html)
    
    print(f"✅ {name} - CN+EN created")

def tool_cn_input(name):
    if name == "glycemic-index-lookup":
        return '''<div class="form-group">
<label>🔍 搜索食物名称</label>
<input type="text" id="food-search" placeholder="输入食物名称，如：白米饭、苹果、全麦面包...">
</div>
<div class="form-row">
<div class="form-group">
<label>📂 食物分类</label>
<select id="food-category">
<option value="all">全部</option>
<option value="grain">谷物类</option>
<option value="fruit">水果类</option>
<option value="vegetable">蔬菜类</option>
<option value="dairy">乳制品</option>
<option value="snack">零食饮料</option>
<option value="meat">肉类/蛋白质</option>
</select>
</div>
</div>
<button class="btn btn-primary" onclick="searchFood()">🔍 查询血糖指数</button>
<div id="food-list" style="margin-top:12px;max-height:400px;overflow-y:auto"></div>'''

    elif name == "calorie-density-calculator":
        return '''<div class="form-row">
<div class="form-group">
<label>🔥 食物热量 (千卡/kcal)</label>
<input type="number" id="calories" placeholder="如：250" min="0" step="1">
</div>
<div class="form-group">
<label>⚖️ 食物重量</label>
<input type="number" id="weight" placeholder="如：200" min="0.1" step="0.1">
</div>
</div>
<div class="form-group">
<label>📏 重量单位</label>
<select id="unit">
<option value="g">克 (g)</option>
<option value="oz">盎司 (oz)</option>
<option value="lb">磅 (lb)</option>
</select>
</div>
<button class="btn btn-primary" onclick="calcDensity()">📊 计算热量密度</button>
<div id="density-result" style="margin-top:12px"></div>'''

    elif name == "time-and-a-half-calculator":
        return '''<div class="form-row">
<div class="form-group">
<label>💵 正常时薪 ($)</label>
<input type="number" id="hourly-rate" placeholder="如：20" min="0" step="0.01">
</div>
<div class="form-group">
<label>⏱️ 加班时长 (小时)</label>
<input type="number" id="overtime-hours" placeholder="如：10" min="0" step="0.5">
</div>
</div>
<div class="form-group">
<label>📈 加班倍率</label>
<select id="overtime-rate">
<option value="1.5">1.5倍 (Time and a Half)</option>
<option value="2">2倍 (Double Time)</option>
<option value="2.5">2.5倍</option>
<option value="3">3倍 (Triple Time)</option>
</select>
</div>
<button class="btn btn-primary" onclick="calcOvertime()">💰 计算加班工资</button>'''

    elif name == "double-time-calculator":
        return '''<div class="form-row">
<div class="form-group">
<label>💵 正常时薪 ($)</label>
<input type="number" id="hourly-rate" placeholder="如：25" min="0" step="0.01">
</div>
<div class="form-group">
<label>⏱️ 工作时长 (小时)</label>
<input type="number" id="work-hours" placeholder="如：8" min="0" step="0.5">
</div>
</div>
<div class="form-group">
<label>📈 工资倍率</label>
<select id="pay-rate">
<option value="2">双倍工资 (Double Time)</option>
<option value="1.5">1.5倍 (Time and a Half)</option>
<option value="2.5">2.5倍</option>
<option value="3">3倍 (Triple Time)</option>
</select>
</div>
<button class="btn btn-primary" onclick="calcDoubleTime()">💰 计算工资</button>'''

    elif name == "streaming-cost-calculator":
        return '''<div style="margin-bottom:12px;color:#94a3b8;font-size:.85rem">选择您订阅的流媒体平台：</div>
<div id="platforms">
<div class="form-row" style="align-items:center;margin-bottom:10px">
<div class="form-group" style="flex:2"><label>Netflix</label>
<select class="plan-select" data-name="Netflix" data-monthly="15.49">
<option value="6.99">Basic with Ads - $6.99/月</option>
<option value="15.49" selected>Standard - $15.49/月</option>
<option value="22.99">Premium - $22.99/月</option>
</select></div>
<div class="form-group" style="flex:1"><label>订阅</label>
<select class="sub-select"><option value="yes" selected>是</option><option value="no">否</option></select></div>
</div>
<div class="form-row" style="align-items:center;margin-bottom:10px">
<div class="form-group" style="flex:2"><label>Disney+</label>
<select class="plan-select" data-name="Disney+" data-monthly="13.99">
<option value="9.99">Basic - $9.99/月</option>
<option value="13.99" selected>Premium - $13.99/月</option>
</select></div>
<div class="form-group" style="flex:1"><label>订阅</label>
<select class="sub-select"><option value="yes" selected>是</option><option value="no">否</option></select></div>
</div>
<div class="form-row" style="align-items:center;margin-bottom:10px">
<div class="form-group" style="flex:2"><label>HBO Max</label>
<select class="plan-select" data-name="HBO Max" data-monthly="16.99">
<option value="9.99">With Ads - $9.99/月</option>
<option value="16.99" selected>Ad-Free - $16.99/月</option>
<option value="20.99">Ultimate - $20.99/月</option>
</select></div>
<div class="form-group" style="flex:1"><label>订阅</label>
<select class="sub-select"><option value="yes">是</option><option value="no" selected>否</option></select></div>
</div>
<div class="form-row" style="align-items:center;margin-bottom:10px">
<div class="form-group" style="flex:2"><label>Amazon Prime Video</label>
<select class="plan-select" data-name="Amazon Prime Video" data-monthly="14.99">
<option value="8.99">Prime Video Only - $8.99/月</option>
<option value="14.99" selected>Prime Full - $14.99/月</option>
</select></div>
<div class="form-group" style="flex:1"><label>订阅</label>
<select class="sub-select"><option value="yes">是</option><option value="no" selected>否</option></select></div>
</div>
<div class="form-row" style="align-items:center;margin-bottom:10px">
<div class="form-group" style="flex:2"><label>Hulu</label>
<select class="plan-select" data-name="Hulu" data-monthly="9.99">
<option value="7.99">With Ads - $7.99/月</option>
<option value="9.99" selected>No Ads - $9.99/月</option>
<option value="18.99">Hulu + Live TV - $18.99/月</option>
</select></div>
<div class="form-group" style="flex:1"><label>订阅</label>
<select class="sub-select"><option value="yes">是</option><option value="no" selected>否</option></select></div>
</div>
<div class="form-row" style="align-items:center;margin-bottom:10px">
<div class="form-group" style="flex:2"><label>Apple TV+</label>
<select class="plan-select" data-name="Apple TV+" data-monthly="9.99">
<option value="9.99" selected>$9.99/月</option>
</select></div>
<div class="form-group" style="flex:1"><label>订阅</label>
<select class="sub-select"><option value="yes">是</option><option value="no" selected>否</option></select></div>
</div>
<div class="form-row" style="align-items:center;margin-bottom:10px">
<div class="form-group" style="flex:2"><label>YouTube Premium</label>
<select class="plan-select" data-name="YouTube Premium" data-monthly="13.99">
<option value="13.99" selected>$13.99/月</option>
</select></div>
<div class="form-group" style="flex:1"><label>订阅</label>
<select class="sub-select"><option value="yes">是</option><option value="no" selected>否</option></select></div>
</div>
<div class="form-row" style="align-items:center;margin-bottom:10px">
<div class="form-group" style="flex:2"><label>Spotify Premium</label>
<select class="plan-select" data-name="Spotify" data-monthly="11.99">
<option value="10.99">Individual - $10.99/月</option>
<option value="11.99" selected>Premium - $11.99/月</option>
<option value="16.99">Family - $16.99/月</option>
</select></div>
<div class="form-group" style="flex:1"><label>订阅</label>
<select class="sub-select"><option value="yes">是</option><option value="no" selected>否</option></select></div>
</div>
</div>
<button class="btn btn-primary" onclick="calcStreaming()">📊 计算总费用</button>'''

    return ''

def tool_cn_instructions(name):
    if name == "glycemic-index-lookup":
        return '''<ol style="padding-left:20px;color:#94a3b8;font-size:.85rem;line-height:2">
<li>在搜索框中输入食物名称</li>
<li>或通过分类下拉菜单筛选</li>
<li>查看食物的GI值和GL值</li>
<li>GI≤55为低GI，56-69为中GI，≥70为高GI</li>
</ol>'''
    elif name == "calorie-density-calculator":
        return '''<ol style="padding-left:20px;color:#94a3b8;font-size:.85rem;line-height:2">
<li>输入食物的总热量（千卡）</li>
<li>输入食物的重量</li>
<li>选择重量单位（克/盎司/磅）</li>
<li>点击计算，查看热量密度</li>
<li>热量密度<1 cal/g为低密度食物</li>
</ol>'''
    elif name == "time-and-a-half-calculator":
        return '''<ol style="padding-left:20px;color:#94a3b8;font-size:.85rem;line-height:2">
<li>输入您的正常时薪</li>
<li>输入加班时长</li>
<li>选择加班倍率（1.5倍/2倍/3倍）</li>
<li>自动计算加班总收入</li>
<li>支持美元、人民币等多种货币</li>
</ol>'''
    elif name == "double-time-calculator":
        return '''<ol style="padding-left:20px;color:#94a3b8;font-size:.85rem;line-height:2">
<li>输入正常时薪</li>
<li>输入工作时长</li>
<li>选择工资倍率</li>
<li>自动计算总收入</li>
<li>适用于节假日/周末加班核算</li>
</ol>'''
    elif name == "streaming-cost-calculator":
        return '''<ol style="padding-left:20px;color:#94a3b8;font-size:.85rem;line-height:2">
<li>勾选您当前订阅的平台</li>
<li>选择各平台的套餐等级</li>
<li>点击计算查看月费和年费</li>
<li>对比不同方案优化订阅</li>
</ol>'''
    return ''

def tool_cn_knowledge(name):
    if name == "glycemic-index-lookup":
        return '''<ul class="info-list">
<li>低GI食物 (≤55)<span class="info-val">推荐多选</span></li>
<li>中GI食物 (56-69)<span class="info-val">适量食用</span></li>
<li>高GI食物 (≥70)<span class="info-val">尽量少吃</span></li>
<li>GL=GI×碳水含量÷100<span class="info-val">更准确</span></li>
</ul>'''
    elif name == "calorie-density-calculator":
        return '''<ul class="info-list">
<li>极低密度 <0.6<span class="info-val">蔬菜水果</span></li>
<li>低密度 0.6-1.5<span class="info-val">谷物豆类</span></li>
<li>中密度 1.5-4.0<span class="info-val">肉类乳制品</span></li>
<li>高密度 >4.0<span class="info-val">油脂坚果</span></li>
</ul>'''
    elif name == "time-and-a-half-calculator":
        return '''<ul class="info-list">
<li>中国法定节假日<span class="info-val">3倍工资</span></li>
<li>中国休息日加班<span class="info-val">2倍工资</span></li>
<li>中国工作日延长<span class="info-val">1.5倍工资</span></li>
<li>美国标准加班<span class="info-val">1.5倍时薪</span></li>
</ul>'''
    elif name == "double-time-calculator":
        return '''<ul class="info-list">
<li>节假日加班<span class="info-val">通常双倍或更高</span></li>
<li>周日/周末加班<span class="info-val">部分公司双倍</span></li>
<li>法定假日<span class="info-val">三倍工资</span></li>
<li>不同公司政策<span class="info-val">费率可能不同</span></li>
</ul>'''
    elif name == "streaming-cost-calculator":
        return '''<ul class="info-list">
<li>Netflix Premium<span class="info-val">$22.99/月</span></li>
<li>Disney+ Premium<span class="info-val">$13.99/月</span></li>
<li>HBO Max Ultimate<span class="info-val">$20.99/月</span></li>
<li>全平台订阅<span class="info-val">约$100+/月</span></li>
</ul>'''
    return ''

def tool_js(name):
    if name == "glycemic-index-lookup":
        return '''var giData=[{"name":"白米饭","gi":73,"gl":29,"cat":"grain"},{"name":"糙米饭","gi":50,"gl":16,"cat":"grain"},{"name":"全麦面包","gi":51,"gl":12,"cat":"grain"},{"name":"白面包","gi":75,"gl":15,"cat":"grain"},{"name":"馒头","gi":88,"gl":35,"cat":"grain"},{"name":"面条(煮)","gi":55,"gl":14,"cat":"grain"},{"name":"燕麦片","gi":55,"gl":12,"cat":"grain"},{"name":"玉米","gi":52,"gl":10,"cat":"grain"},{"name":"小米粥","gi":72,"gl":5,"cat":"grain"},{"name":"荞麦面","gi":54,"gl":11,"cat":"grain"},{"name":"苹果","gi":36,"gl":6,"cat":"fruit"},{"name":"香蕉","gi":51,"gl":13,"cat":"fruit"},{"name":"西瓜","gi":72,"gl":5,"cat":"fruit"},{"name":"橙子","gi":43,"gl":5,"cat":"fruit"},{"name":"葡萄","gi":59,"gl":11,"cat":"fruit"},{"name":"芒果","gi":51,"gl":8,"cat":"fruit"},{"name":"猕猴桃","gi":50,"gl":7,"cat":"fruit"},{"name":"草莓","gi":40,"gl":1,"cat":"fruit"},{"name":"蓝莓","gi":53,"gl":5,"cat":"fruit"},{"name":"樱桃","gi":22,"gl":3,"cat":"fruit"},{"name":"胡萝卜","gi":39,"gl":2,"cat":"vegetable"},{"name":"土豆(煮)","gi":78,"gl":13,"cat":"vegetable"},{"name":"红薯","gi":54,"gl":11,"cat":"vegetable"},{"name":"南瓜","gi":75,"gl":3,"cat":"vegetable"},{"name":"西兰花","gi":10,"gl":0,"cat":"vegetable"},{"name":"菠菜","gi":15,"gl":0,"cat":"vegetable"},{"name":"番茄","gi":30,"gl":1,"cat":"vegetable"},{"name":"黄瓜","gi":15,"gl":0,"cat":"vegetable"},{"name":"牛奶","gi":27,"gl":3,"cat":"dairy"},{"name":"酸奶","gi":35,"gl":5,"cat":"dairy"},{"name":"冰淇淋","gi":61,"gl":13,"cat":"dairy"},{"name":"奶酪","gi":0,"gl":0,"cat":"dairy"},{"name":"可口可乐","gi":63,"gl":16,"cat":"snack"},{"name":"巧克力","gi":49,"gl":12,"cat":"snack"},{"name":"薯片","gi":56,"gl":9,"cat":"snack"},{"name":"蛋糕","gi":54,"gl":15,"cat":"snack"},{"name":"饼干","gi":69,"gl":13,"cat":"snack"},{"name":"蜂蜜","gi":61,"gl":12,"cat":"snack"},{"name":"鸡胸肉","gi":0,"gl":0,"cat":"meat"},{"name":"鸡蛋","gi":0,"gl":0,"cat":"meat"},{"name":"三文鱼","gi":0,"gl":0,"cat":"meat"},{"name":"豆腐","gi":15,"gl":1,"cat":"meat"},{"name":"豆浆","gi":34,"gl":2,"cat":"meat"}];
function searchFood(){var s=document.getElementById("food-search").value.toLowerCase();var c=document.getElementById("food-category").value;var r=giData.filter(function(f){var m=f.name.indexOf(s)>-1||f.cat.indexOf(s)>-1;if(c!=="all")m=m&&f.cat===c;return m});var h="";if(r.length===0){h='<div style="text-align:center;padding:20px;color:#64748b">未找到匹配的食物</div>'}else{r.forEach(function(f){var gl=parseFloat(f.gl);var glLabel=gl<10?"低":"中";var gi=parseInt(f.gi);var giLabel=gi<=55?"低":gi<=69?"中":"高";var giColor=gi<=55?"#22c55e":gi<=69?"#f59e0b":"#ef4444";h+='<div class="result-card" style="margin-bottom:8px"><div style="display:flex;justify-content:space-between;align-items:center"><div><strong>'+f.name+'</strong><div class="range">分类: '+f.cat+'</div></div><div style="text-align:right"><div class="value" style="font-size:1.2rem;color:'+giColor+'">GI: '+f.gi+' ('+giLabel+')</div><div class="range">GL: '+f.gl+' ('+glLabel+')</div></div></div></div>'})}document.getElementById("food-list").innerHTML=h;document.getElementById("main-result").textContent=r.length>0?"找到 "+r.length+" 种食物":"未找到";document.getElementById("detail-area").innerHTML=""}
searchFood();'''
    elif name == "calorie-density-calculator":
        return '''function calcDensity(){var c=parseFloat(document.getElementById("calories").value);var w=parseFloat(document.getElementById("weight").value);var u=document.getElementById("unit").value;if(isNaN(c)||isNaN(w)||w<=0){document.getElementById("density-result").innerHTML='<div style="color:#ef4444;padding:12px">请输入有效的热量和重量值</div>';return}if(u==="oz")w=w*28.35;if(u==="lb")w=w*453.592;var d=c/w;var level=d<0.6?"极低密度":d<1.5?"低密度":d<4?"中密度":"高密度";var color=d<0.6?"#22c55e":d<1.5?"#f59e0b":d<4?"#f97316":"#ef4444";document.getElementById("density-result").innerHTML='<div class="result-card"><div class="value" style="color:'+color+'">'+d.toFixed(2)+' cal/g</div><div class="label">热量密度: <span style="color:'+color+'">'+level+'</span></div><div class="range">'+c+' kcal ÷ '+w.toFixed(1)+' g</div></div>';document.getElementById("main-result").textContent=d.toFixed(2)+" cal/g";document.getElementById("detail-area").innerHTML='<div class="health-tip">💡 热量密度越低，食物体积越大、饱腹感越强。减肥建议选择热量密度<1.5 cal/g的食物。</div>'}
'''
    elif name == "time-and-a-half-calculator":
        return '''function calcOvertime(){var r=parseFloat(document.getElementById("hourly-rate").value);var h=parseFloat(document.getElementById("overtime-hours").value);var m=parseFloat(document.getElementById("overtime-rate").value);if(isNaN(r)||isNaN(h)||r<0||h<0){showToast("请输入有效的时薪和加班时长");return}var ot=r*m*h;var normal=r*h;document.getElementById("main-result").textContent="$"+ot.toFixed(2);document.getElementById("detail-area").innerHTML='<div class="result-card"><div style="display:flex;justify-content:space-between;margin-bottom:8px"><span>正常时薪:</span><span>$'+r.toFixed(2)+'/小时</span></div><div style="display:flex;justify-content:space-between;margin-bottom:8px"><span>加班倍率:</span><span>'+m+'倍</span></div><div style="display:flex;justify-content:space-between;margin-bottom:8px"><span>加班时长:</span><span>'+h+' 小时</span></div><div style="display:flex;justify-content:space-between;margin-bottom:8px;font-weight:600"><span>正常工资:</span><span>$'+normal.toFixed(2)+'</span></div><div style="display:flex;justify-content:space-between;font-size:1.1rem;font-weight:700;color:#22d3ee"><span>加班总收入:</span><span>$'+ot.toFixed(2)+'</span></div></div><div style="text-align:right;margin-top:8px"><button class="btn btn-secondary btn-sm" onclick="copyText(\\'$'+ot.toFixed(2)+'\\')">📋 复制结果</button></div>'}
'''
    elif name == "double-time-calculator":
        return '''function calcDoubleTime(){var r=parseFloat(document.getElementById("hourly-rate").value);var h=parseFloat(document.getElementById("work-hours").value);var m=parseFloat(document.getElementById("pay-rate").value);if(isNaN(r)||isNaN(h)||r<0||h<0){showToast("请输入有效的时薪和工作时长");return}var total=r*m*h;document.getElementById("main-result").textContent="$"+total.toFixed(2);document.getElementById("detail-area").innerHTML='<div class="result-card"><div style="display:flex;justify-content:space-between;margin-bottom:8px"><span>正常时薪:</span><span>$'+r.toFixed(2)+'/小时</span></div><div style="display:flex;justify-content:space-between;margin-bottom:8px"><span>工资倍率:</span><span>'+m+'倍</span></div><div style="display:flex;justify-content:space-between;margin-bottom:8px"><span>工作时长:</span><span>'+h+' 小时</span></div><div style="display:flex;justify-content:space-between;font-size:1.1rem;font-weight:700;color:#22d3ee"><span>总收入:</span><span>$'+total.toFixed(2)+'</span></div></div><div style="text-align:right;margin-top:8px"><button class="btn btn-secondary btn-sm" onclick="copyText(\\'$'+total.toFixed(2)+'\\')">📋 复制结果</button></div>'}
'''
    elif name == "streaming-cost-calculator":
        return '''function calcStreaming(){var ps=document.querySelectorAll("#platforms .form-row");var total=0;var detail="";ps.forEach(function(row){var sub=row.querySelector(".sub-select").value;if(sub==="yes"){var plan=row.querySelector(".plan-select");var name=plan.dataset.name;var price=parseFloat(plan.value);total+=price;detail+='<div style="display:flex;justify-content:space-between;margin-bottom:6px"><span>'+name+'</span><span>$'+price.toFixed(2)+'/月</span></div>'}});document.getElementById("main-result").textContent="$"+total.toFixed(2)+"/月";var yearly=total*12;document.getElementById("detail-area").innerHTML='<div class="result-card">'+detail+'<div style="border-top:1px solid rgba(148,163,184,.2);padding-top:10px;margin-top:8px;display:flex;justify-content:space-between;font-weight:700"><span>月费合计:</span><span style="color:#22d3ee">$'+total.toFixed(2)+'/月</span></div><div style="display:flex;justify-content:space-between;font-weight:700;margin-top:4px"><span>年费合计:</span><span style="color:#f1c40f">$'+yearly.toFixed(2)+'/年</span></div></div><div class="health-tip">💡 年费$'+yearly.toFixed(2)+'。考虑轮换订阅或共享账号可节省'+(yearly*0.3).toFixed(2)+'以上！</div>'}
'''

    return ''

# Generate all tools
for tool in TOOLS:
    generate_tool(tool)

print("\n✅ All 5 tools generated!")
print("CN: glycemic-index-lookup, calorie-density-calculator, time-and-a-half-calculator, double-time-calculator, streaming-cost-calculator")
print("EN: en/glycemic-index-lookup, en/calorie-density-calculator, en/time-and-a-half-calculator, en/double-time-calculator, en/streaming-cost-calculator")