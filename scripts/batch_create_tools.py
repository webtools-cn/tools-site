#!/usr/bin/env python3
"""Batch create 10 new tools with Chinese + English versions."""
import os, json, datetime

BASE = "/home/chison/tools-site"
TODAY = "2026-07-25"

# ===== Tool definitions =====
TOOLS = [
    {
        "slug": "utc-converter",
        "cn_name": "UTC时间转换器",
        "en_name": "UTC Time Converter",
        "cn_desc": "免费在线UTC时间转换器，支持UTC与本地时间互转、多时区转换、ISO 8601格式解析。无需注册，隐私安全。",
        "en_desc": "Free online UTC time converter — convert between UTC and local time, support multiple timezones and ISO 8601 format. No registration required.",
        "cn_keywords": "UTC时间转换,UTC转本地时间,时区转换,ISO8601,时间格式转换,在线工具,免费",
        "en_keywords": "UTC time converter,UTC to local time,timezone converter,ISO 8601,time format,online tool,free",
        "cn_faq_q": "UTC时间和本地时间有什么区别？",
        "cn_faq_a": "UTC（协调世界时）是全球统一的时间标准，不随季节变化。本地时间是UTC加上时区偏移量（如UTC+8表示北京时间）。",
        "en_faq_q": "What's the difference between UTC and local time?",
        "en_faq_a": "UTC (Coordinated Universal Time) is the global time standard that doesn't change with seasons. Local time is UTC plus a timezone offset (e.g., UTC+8 for Beijing time).",
    },
    {
        "slug": "date-to-timestamp",
        "cn_name": "日期转时间戳",
        "en_name": "Date to Timestamp",
        "cn_desc": "免费在线日期时间戳转换器，支持日期转Unix时间戳、时间戳转日期、毫秒时间戳转换。无需注册，一键复制。",
        "en_desc": "Free online date to timestamp converter — convert date to Unix timestamp, timestamp to date, millisecond timestamp support. One-click copy.",
        "cn_keywords": "日期转时间戳,Unix时间戳,时间戳转换,毫秒时间戳,在线工具,免费",
        "en_keywords": "date to timestamp,Unix timestamp,timestamp converter,millisecond timestamp,online tool,free",
        "cn_faq_q": "Unix时间戳是什么？",
        "cn_faq_a": "Unix时间戳是从1970年1月1日00:00:00 UTC到指定时间的秒数（或毫秒数），广泛用于编程和数据库中表示时间。",
        "en_faq_q": "What is a Unix timestamp?",
        "en_faq_a": "A Unix timestamp is the number of seconds (or milliseconds) elapsed since January 1, 1970 00:00:00 UTC, widely used in programming and databases to represent time.",
    },
    {
        "slug": "color-names",
        "cn_name": "HTML颜色名称大全",
        "en_name": "HTML Color Names",
        "cn_desc": "免费在线HTML颜色名称参考大全，包含140+标准颜色名称、HEX值、RGB值。支持搜索和点击复制。无需注册。",
        "en_desc": "Free online HTML color names reference — 140+ standard color names with HEX and RGB values. Search and click to copy. No registration required.",
        "cn_keywords": "HTML颜色名称,CSS颜色,颜色代码,HEX颜色,RGB颜色,颜色参考,在线工具,免费",
        "en_keywords": "HTML color names,CSS colors,color codes,HEX colors,RGB colors,color reference,online tool,free",
        "cn_faq_q": "HTML支持多少种命名颜色？",
        "cn_faq_a": "HTML/CSS标准支持140+种命名颜色，包括基本颜色如red、blue、green，以及扩展颜色如tomato、coral、teal等。",
        "en_faq_q": "How many named colors does HTML support?",
        "en_faq_a": "HTML/CSS supports 140+ named colors, including basic colors like red, blue, green, and extended colors like tomato, coral, teal, and more.",
    },
    {
        "slug": "workdays-calculator",
        "cn_name": "工作日计算器",
        "en_name": "Workdays Calculator",
        "cn_desc": "免费在线工作日计算器，计算两个日期之间的工作日天数、排除周末和法定节假日。无需注册，结果精准。",
        "en_desc": "Free online workdays calculator — calculate business days between two dates, exclude weekends and holidays. Accurate results, no registration.",
        "cn_keywords": "工作日计算,工作日天数,排除周末,节假日计算,日期计算,在线工具,免费",
        "en_keywords": "workdays calculator,business days,exclude weekends,holiday calculation,date calculator,online tool,free",
        "cn_faq_q": "如何计算两个日期之间的工作日？",
        "cn_faq_a": "工作日计算器会自动排除周六和周日，只计算周一到周五的天数。您也可以手动排除特定的节假日日期。",
        "en_faq_q": "How to calculate workdays between two dates?",
        "en_faq_a": "The workdays calculator automatically excludes Saturdays and Sundays, counting only Monday through Friday. You can also manually exclude specific holiday dates.",
    },
    {
        "slug": "ideal-weight",
        "cn_name": "理想体重计算器",
        "en_name": "Ideal Weight Calculator",
        "cn_desc": "免费在线理想体重计算器，基于身高、性别和多种公式（BMI、Devine、Robinson）计算健康体重范围。无需注册。",
        "en_desc": "Free online ideal weight calculator — calculate healthy weight range based on height, gender and multiple formulas (BMI, Devine, Robinson). No registration.",
        "cn_keywords": "理想体重,BMI计算,标准体重,健康体重,体重计算器,在线工具,免费",
        "en_keywords": "ideal weight,BMI calculator,healthy weight,weight calculator,body weight,online tool,free",
        "cn_faq_q": "如何计算理想体重？",
        "cn_faq_a": "常见公式包括Devine公式（男性：50+2.3×(身高英寸-60)，女性：45.5+2.3×(身高英寸-60)）和Robinson公式等，不同公式结果略有差异。",
        "en_faq_q": "How is ideal weight calculated?",
        "en_faq_a": "Common formulas include Devine (Men: 50+2.3×(height_in-60), Women: 45.5+2.3×(height_in-60)) and Robinson formulas, with slight variations between methods.",
    },
    {
        "slug": "water-intake",
        "cn_name": "每日饮水量计算器",
        "en_name": "Daily Water Intake Calculator",
        "cn_desc": "免费在线每日饮水量计算器，根据体重、活动量和气候计算每日推荐饮水量。无需注册，科学建议。",
        "en_desc": "Free online daily water intake calculator — calculate recommended daily water intake based on weight, activity level and climate. Science-based, no registration.",
        "cn_keywords": "饮水量,每日饮水,喝水提醒,水分摄入,健康饮水,在线工具,免费",
        "en_keywords": "water intake,daily water,hydration calculator,drink water,health,online tool,free",
        "cn_faq_q": "每天应该喝多少水？",
        "cn_faq_a": "一般建议每天饮水约体重(kg)×30-40毫升。运动量大或天气炎热时应增加。本计算器根据体重和活动量提供个性化建议。",
        "en_faq_q": "How much water should I drink daily?",
        "en_faq_a": "General recommendation is body weight (kg) × 30-40 ml per day. Increase intake with exercise or hot weather. This calculator provides personalized recommendations.",
    },
    {
        "slug": "running-pace",
        "cn_name": "跑步配速计算器",
        "en_name": "Running Pace Calculator",
        "cn_desc": "免费在线跑步配速计算器，计算每公里配速、每英里配速、完赛时间预测。支持多种距离。无需注册。",
        "en_desc": "Free online running pace calculator — calculate pace per km, pace per mile, and race finish time predictions. Supports multiple distances. No registration.",
        "cn_keywords": "跑步配速,配速计算,马拉松配速,跑步计算器,完赛时间,在线工具,免费",
        "en_keywords": "running pace,pace calculator,marathon pace,running calculator,finish time,online tool,free",
        "cn_faq_q": "如何计算跑步配速？",
        "cn_faq_a": "配速 = 总时间 ÷ 距离。例如5公里跑了25分钟，配速为5分钟/公里。本计算器支持公里和英里单位，可预测不同距离的完赛时间。",
        "en_faq_q": "How to calculate running pace?",
        "en_faq_a": "Pace = total time ÷ distance. For example, 5K in 25 minutes = 5:00 min/km pace. This calculator supports both km and mile units and predicts finish times for different distances.",
    },
    {
        "slug": "paragraph-counter",
        "cn_name": "段落计数器",
        "en_name": "Paragraph Counter",
        "cn_desc": "免费在线段落计数器，实时统计文本中的段落数、每段字数、平均段落长度。无需注册，隐私安全。",
        "en_desc": "Free online paragraph counter — real-time count of paragraphs, words per paragraph, and average paragraph length. No registration, privacy safe.",
        "cn_keywords": "段落计数,段落统计,文本分析,段落长度,在线工具,免费",
        "en_keywords": "paragraph counter,paragraph count,text analysis,paragraph length,online tool,free",
        "cn_faq_q": "如何定义文本中的段落？",
        "cn_faq_a": "段落通常由换行符（一个或多个空行）分隔。本工具将连续的文本块视为一个段落，空行作为段落分隔符。",
        "en_faq_q": "How is a paragraph defined in text?",
        "en_faq_a": "A paragraph is typically separated by line breaks (one or more blank lines). This tool treats continuous text blocks as one paragraph, with blank lines as separators.",
    },
    {
        "slug": "vowel-counter",
        "cn_name": "元音计数器",
        "en_name": "Vowel Counter",
        "cn_desc": "免费在线元音计数器，统计文本中a/e/i/o/u元音字母数量和比例。支持大小写，实时统计。无需注册。",
        "en_desc": "Free online vowel counter — count a/e/i/o/u vowel letters and their ratio in text. Case-insensitive, real-time stats. No registration required.",
        "cn_keywords": "元音计数,元音统计,字母统计,文本分析,在线工具,免费",
        "en_keywords": "vowel counter,vowel count,letter count,text analysis,online tool,free",
        "cn_faq_q": "英语中有哪些元音字母？",
        "cn_faq_a": "英语有5个基本元音字母：a、e、i、o、u。有时y也被视为元音。本工具统计这5个标准元音的出现次数和比例。",
        "en_faq_q": "What are the vowel letters in English?",
        "en_faq_a": "English has 5 basic vowel letters: a, e, i, o, u. Sometimes y is also considered a vowel. This tool counts the 5 standard vowels and their ratio.",
    },
    {
        "slug": "keyword-density",
        "cn_name": "关键词密度分析器",
        "en_name": "Keyword Density Analyzer",
        "cn_desc": "免费在线关键词密度分析器，分析文本中关键词出现频率和密度百分比。支持多词短语。无需注册，SEO必备。",
        "en_desc": "Free online keyword density analyzer — analyze keyword frequency and density percentage in text. Supports multi-word phrases. No registration, SEO essential.",
        "cn_keywords": "关键词密度,关键词分析,SEO工具,文本分析,关键词频率,在线工具,免费",
        "en_keywords": "keyword density,keyword analysis,SEO tool,text analysis,keyword frequency,online tool,free",
        "cn_faq_q": "什么是关键词密度？",
        "cn_faq_a": "关键词密度是指关键词在文本中出现的次数占总词数的百分比。一般建议关键词密度在1-3%之间，过高可能被搜索引擎视为关键词堆砌。",
        "en_faq_q": "What is keyword density?",
        "en_faq_a": "Keyword density is the percentage of times a keyword appears relative to total word count. A density of 1-3% is generally recommended; higher may be seen as keyword stuffing by search engines.",
    },
]

def html_escape(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def make_cn_page(tool):
    slug = tool["slug"]
    name = tool["cn_name"]
    desc = tool["cn_desc"]
    keywords = tool["cn_keywords"]
    faq_q = tool["cn_faq_q"]
    faq_a = tool["cn_faq_a"]

    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-9W1157EBQV"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-9W1157EBQV');</script>
<script>window.addEventListener("error",function(e){{if(e&&e.message===""){{e.preventDefault();}}}});window.addEventListener("unhandledrejection",function(e){{if(e&&e.reason&&e.reason.message===""){{e.preventDefault();}}}});</script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="{html_escape(desc)}">
<meta name="keywords" content="{html_escape(keywords)}">
<title>免费{name} | Free ToolBase</title>
<link rel="canonical" href="https://free-toolbase.com/{slug}/">
<meta property="og:title" content="免费{name} | Free ToolBase">
<meta property="og:description" content="{html_escape(desc)}">
<meta property="og:url" content="https://free-toolbase.com/{slug}/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Free ToolBase">
<link rel="alternate" hreflang="zh" href="https://free-toolbase.com/{slug}/">
<link rel="alternate" hreflang="en" href="https://free-toolbase.com/en/{slug}/">
<link rel="alternate" hreflang="x-default" href="https://free-toolbase.com/en/{slug}/">
<script type="application/ld+json">{{"@context": "https://schema.org", "@type": "SoftwareApplication", "name": "{name}", "description": "{html_escape(desc)}", "applicationCategory": "UtilitiesApplication", "operatingSystem": "Web", "publisher": {{"@type": "Organization", "name": "Free ToolBase", "email": "dexshuang@google.com"}}, "offers": {{"@type": "Offer", "price": "0", "priceCurrency": "USD"}}}}</script>
<script type="application/ld+json">{{"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{{"@type": "Question", "name": "{html_escape(faq_q)}", "acceptedAnswer": {{"@type": "Answer", "text": "{html_escape(faq_a)}"}}}}]}}</script>
<script type="application/ld+json">{{"@context": "https://schema.org", "@type": "HowTo", "name": "如何使用{name}", "description": "如何使用{name}的详细步骤指南", "totalTime": "PT2M", "tool": {{"@type": "HowToTool", "name": "{name}"}}, "step": [{{"@type": "HowToStep", "position": 1, "name": "输入数据", "text": "在输入框中输入需要计算的数据"}}, {{"@type": "HowToStep", "position": 2, "name": "选择选项", "text": "根据需要选择计算模式或参数"}}, {{"@type": "HowToStep", "position": 3, "name": "点击计算", "text": "点击计算按钮获取结果"}}, {{"@type": "HowToStep", "position": 4, "name": "查看结果", "text": "查看计算结果，支持一键复制"}}]}}</script>
<script type="application/ld+json">{{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{{"@type": "ListItem", "position": 1, "name": "首页", "item": "https://free-toolbase.com/"}}, {{"@type": "ListItem", "position": 2, "name": "工具", "item": "https://free-toolbase.com/#tools"}}, {{"@type": "ListItem", "position": 3, "name": "{name}", "item": "https://free-toolbase.com/{slug}/"}}]}}</script>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#0f172a;color:#e2e8f0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,"PingFang SC","Microsoft YaHei",sans-serif;line-height:1.6;min-height:100vh}}
a{{color:#06b6d4;text-decoration:none}}
.container{{max-width:960px;margin:0 auto;padding:24px 16px}}
.header{{display:flex;justify-content:space-between;align-items:center;margin-bottom:24px;flex-wrap:wrap;gap:12px}}
.header h1{{font-size:1.5rem;color:#f1f5f9}}
.lang-switch{{display:flex;gap:4px;background:#1e293b;border-radius:8px;padding:4px}}
.lang-switch a{{padding:6px 12px;border-radius:5px;font-size:.85rem;color:#94a3b8}}
.lang-switch a.active{{background:rgba(6,182,212,.2);color:#22d3ee}}
.nav-back{{color:#64748b;font-size:.85rem;margin-bottom:16px}}
.nav-back a{{color:#64748b}}
.section{{background:#1e293b;border-radius:12px;padding:20px;margin-bottom:16px}}
.section h2{{font-size:1.1rem;color:#f1f5f9;margin-bottom:12px}}
.form-group{{margin-bottom:14px}}
.form-group label{{display:block;color:#94a3b8;font-size:.9rem;margin-bottom:6px;font-weight:500}}
.form-group input,.form-group select,.form-group textarea{{width:100%;padding:10px 14px;background:#0f172a;border:1px solid rgba(148,163,184,.2);border-radius:8px;color:#e2e8f0;font-size:.9rem;outline:none}}
.form-group input:focus,.form-group select:focus,.form-group textarea:focus{{border-color:rgba(6,182,212,.4)}}
.form-group textarea{{min-height:120px;resize:vertical;font-family:monospace}}
.form-row{{display:flex;gap:12px;flex-wrap:wrap}}
.form-row .form-group{{flex:1;min-width:200px}}
.btn{{padding:10px 24px;border:none;border-radius:8px;font-size:.9rem;cursor:pointer;transition:all .2s;font-weight:600}}
.btn-primary{{background:linear-gradient(135deg,#06b6d4,#0891b2);color:#fff}}
.btn-primary:hover{{transform:translateY(-2px);box-shadow:0 4px 15px rgba(6,182,212,.3)}}
.btn-secondary{{background:rgba(148,163,184,.1);color:#94a3b8}}
.btn-secondary:hover{{background:rgba(148,163,184,.2)}}
.btn-group{{display:flex;gap:8px;flex-wrap:wrap;margin-top:12px}}
.result-box{{background:#0f172a;border-radius:8px;padding:16px;margin-top:12px;display:none}}
.result-box.show{{display:block}}
.result-item{{display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid rgba(148,163,184,.1)}}
.result-item:last-child{{border-bottom:none}}
.result-label{{color:#94a3b8;font-size:.85rem}}
.result-value{{color:#22d3ee;font-weight:600;font-size:.9rem;cursor:pointer}}
.result-value:hover{{text-decoration:underline}}
.toast{{position:fixed;bottom:24px;left:50%;transform:translateX(-50%);background:#22d3ee;color:#0f172a;padding:10px 24px;border-radius:8px;font-weight:600;z-index:9999;opacity:0;transition:opacity .3s}}
.toast.show{{opacity:1}}
footer{{text-align:center;padding:24px;color:#64748b;font-size:.8rem}}
footer a{{color:#64748b}}
.copied{{color:#10b981!important}}
@media(max-width:600px){{.header h1{{font-size:1.2rem}}.section{{padding:16px}}}}
</style>
</head>
<body>
<div class="container">
<div class="nav-back"><a href="/">← 返回首页</a></div>
<div class="header">
<h1>🔧 {name}</h1>
<div class="lang-switch">
<a href="/{slug}/" class="active">中文</a>
<a href="/en/{slug}/">EN</a>
</div>
</div>
<!-- TOOL_CONTENT_PLACEHOLDER_CN -->
<footer>
<p><a href="/">首页</a> · <a href="/#tools">全部工具</a> · <a href="/about/">关于</a></p>
<p>© 2026 Free ToolBase · 免费在线工具，无需注册</p>
</footer>
</div>
<div class="toast" id="toast"></div>
<!-- TOOL_SCRIPT_PLACEHOLDER_CN -->
</body>
</html>'''

def make_en_page(tool):
    slug = tool["slug"]
    name = tool["en_name"]
    desc = tool["en_desc"]
    keywords = tool["en_keywords"]
    faq_q = tool["en_faq_q"]
    faq_a = tool["en_faq_a"]

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-9W1157EBQV"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-9W1157EBQV');</script>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="{html_escape(desc)}">
<meta name="keywords" content="{html_escape(keywords)}">
<title>Free {name} | Free ToolBase</title>
<link rel="canonical" href="https://free-toolbase.com/en/{slug}/">
<meta property="og:title" content="{name}">
<meta property="og:description" content="{html_escape(desc)}">
<meta property="og:url" content="https://free-toolbase.com/en/{slug}/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Free ToolBase">
<link rel="alternate" hreflang="zh" href="https://free-toolbase.com/{slug}/">
<link rel="alternate" hreflang="en" href="https://free-toolbase.com/en/{slug}/">
<link rel="alternate" hreflang="x-default" href="https://free-toolbase.com/en/{slug}/">
<script type="application/ld+json">{{"@context": "https://schema.org", "@type": "SoftwareApplication", "name": "{name}", "description": "{html_escape(desc)}", "applicationCategory": "UtilitiesApplication", "operatingSystem": "Web", "publisher": {{"@type": "Organization", "name": "Free ToolBase", "email": "dexshuang@google.com"}}, "author": {{"@type": "Organization", "name": "Free ToolBase"}}, "dateModified": "{TODAY}", "offers": {{"@type": "Offer", "price": "0", "priceCurrency": "USD"}}}}</script>
<script type="application/ld+json">{{"@context": "https://schema.org", "@type": "FAQPage", "name": "{html_escape(faq_q)}", "mainEntity": [{{"@type": "Question", "name": "{html_escape(faq_q)}", "acceptedAnswer": {{"@type": "Answer", "text": "{html_escape(faq_a)}"}}}}]}}</script>
<script type="application/ld+json">{{"@context": "https://schema.org", "@type": "HowTo", "name": "How to Use {name}", "description": "Step-by-step guide on using the {name}", "totalTime": "PT2M", "tool": {{"@type": "HowToTool", "name": "{name}"}}, "step": [{{"@type": "HowToStep", "position": 1, "name": "Enter Data", "text": "Enter the data you want to process"}}, {{"@type": "HowToStep", "position": 2, "name": "Select Options", "text": "Select mode or parameters as needed"}}, {{"@type": "HowToStep", "position": 3, "name": "Click Calculate", "text": "Click the calculate button to get results"}}, {{"@type": "HowToStep", "position": 4, "name": "View Results", "text": "View the results, one-click copy supported"}}]}}</script>
<script type="application/ld+json">{{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{{"@type": "ListItem", "position": 1, "name": "Home", "item": "https://free-toolbase.com/en/"}}, {{"@type": "ListItem", "position": 2, "name": "Tools", "item": "https://free-toolbase.com/en/#tools"}}, {{"@type": "ListItem", "position": 3, "name": "{name}", "item": "https://free-toolbase.com/en/{slug}/"}}]}}</script>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#0f172a;color:#e2e8f0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif;line-height:1.6;min-height:100vh}}
a{{color:#06b6d4;text-decoration:none}}
.container{{max-width:960px;margin:0 auto;padding:24px 16px}}
.header{{display:flex;justify-content:space-between;align-items:center;margin-bottom:24px;flex-wrap:wrap;gap:12px}}
.header h1{{font-size:1.5rem;color:#f1f5f9}}
.lang-switch{{display:flex;gap:4px;background:#1e293b;border-radius:8px;padding:4px}}
.lang-switch a{{padding:6px 12px;border-radius:5px;font-size:.85rem;color:#94a3b8}}
.lang-switch a.active{{background:rgba(6,182,212,.2);color:#22d3ee}}
.nav-back{{color:#64748b;font-size:.85rem;margin-bottom:16px}}
.nav-back a{{color:#64748b}}
.section{{background:#1e293b;border-radius:12px;padding:20px;margin-bottom:16px}}
.section h2{{font-size:1.1rem;color:#f1f5f9;margin-bottom:12px}}
.form-group{{margin-bottom:14px}}
.form-group label{{display:block;color:#94a3b8;font-size:.9rem;margin-bottom:6px;font-weight:500}}
.form-group input,.form-group select,.form-group textarea{{width:100%;padding:10px 14px;background:#0f172a;border:1px solid rgba(148,163,184,.2);border-radius:8px;color:#e2e8f0;font-size:.9rem;outline:none}}
.form-group input:focus,.form-group select:focus,.form-group textarea:focus{{border-color:rgba(6,182,212,.4)}}
.form-group textarea{{min-height:120px;resize:vertical;font-family:monospace}}
.form-row{{display:flex;gap:12px;flex-wrap:wrap}}
.form-row .form-group{{flex:1;min-width:200px}}
.btn{{padding:10px 24px;border:none;border-radius:8px;font-size:.9rem;cursor:pointer;transition:all .2s;font-weight:600}}
.btn-primary{{background:linear-gradient(135deg,#06b6d4,#0891b2);color:#fff}}
.btn-primary:hover{{transform:translateY(-2px);box-shadow:0 4px 15px rgba(6,182,212,.3)}}
.btn-secondary{{background:rgba(148,163,184,.1);color:#94a3b8}}
.btn-secondary:hover{{background:rgba(148,163,184,.2)}}
.btn-group{{display:flex;gap:8px;flex-wrap:wrap;margin-top:12px}}
.result-box{{background:#0f172a;border-radius:8px;padding:16px;margin-top:12px;display:none}}
.result-box.show{{display:block}}
.result-item{{display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid rgba(148,163,184,.1)}}
.result-item:last-child{{border-bottom:none}}
.result-label{{color:#94a3b8;font-size:.85rem}}
.result-value{{color:#22d3ee;font-weight:600;font-size:.9rem;cursor:pointer}}
.result-value:hover{{text-decoration:underline}}
.toast{{position:fixed;bottom:24px;left:50%;transform:translateX(-50%);background:#22d3ee;color:#0f172a;padding:10px 24px;border-radius:8px;font-weight:600;z-index:9999;opacity:0;transition:opacity .3s}}
.toast.show{{opacity:1}}
footer{{text-align:center;padding:24px;color:#64748b;font-size:.8rem}}
footer a{{color:#64748b}}
.copied{{color:#10b981!important}}
@media(max-width:600px){{.header h1{{font-size:1.2rem}}.section{{padding:16px}}}}
</style>
</head>
<body>
<div class="container">
<div class="nav-back"><a href="/en/">← Back to Home</a></div>
<div class="header">
<h1>🔧 {name}</h1>
<div class="lang-switch">
<a href="/{slug}/">中文</a>
<a href="/en/{slug}/" class="active">EN</a>
</div>
</div>
<!-- TOOL_CONTENT_PLACEHOLDER_EN -->
<footer>
<p><a href="/en/">Home</a> · <a href="/en/#tools">All Tools</a> · <a href="/about/">About</a></p>
<p>© 2026 Free ToolBase · Free Online Tools, No Registration</p>
</footer>
</div>
<div class="toast" id="toast"></div>
<!-- TOOL_SCRIPT_PLACEHOLDER_EN -->
</body>
</html>'''

# ===== Generate tool-specific content and JS =====

def get_tool_content_cn(tool):
    slug = tool["slug"]
    
    if slug == "utc-converter":
        return '''<div class="section">
<h2>UTC时间转换</h2>
<div class="form-group">
<label>当前UTC时间</label>
<div id="currentUTC" style="font-size:1.2rem;color:#22d3ee;font-family:monospace;"></div>
</div>
<div class="form-group">
<label>当前本地时间</label>
<div id="currentLocal" style="font-size:1.2rem;color:#22d3ee;font-family:monospace;"></div>
</div>
<div class="form-row">
<div class="form-group">
<label>输入UTC时间</label>
<input type="datetime-local" id="utcInput">
</div>
<div class="form-group">
<label>目标时区</label>
<select id="targetTZ"></select>
</div>
</div>
<div class="btn-group">
<button class="btn btn-primary" id="convertBtn">转换</button>
<button class="btn btn-secondary" id="nowBtn">使用当前时间</button>
</div>
<div class="result-box" id="resultBox">
<div class="result-item"><span class="result-label">输入UTC时间</span><span class="result-value" id="inputUTC"></span></div>
<div class="result-item"><span class="result-label">目标时区</span><span class="result-value" id="targetTZName"></span></div>
<div class="result-item"><span class="result-label">转换结果</span><span class="result-value" id="convertedTime"></span></div>
<div class="result-item"><span class="result-label">ISO 8601</span><span class="result-value" id="isoTime"></span></div>
</div>
</div>
<div class="section">
<h2>常用时区快速查询</h2>
<div class="form-group">
<select id="quickTZ" style="margin-bottom:8px"></select>
</div>
<div id="quickResult" style="font-size:1.1rem;color:#22d3ee;font-family:monospace;"></div>
</div>'''
    
    elif slug == "date-to-timestamp":
        return '''<div class="section">
<h2>日期 ↔ 时间戳</h2>
<div class="form-group">
<label>日期时间</label>
<input type="datetime-local" id="dateInput">
</div>
<div class="btn-group">
<button class="btn btn-primary" id="toTimestampBtn">转为时间戳</button>
<button class="btn btn-secondary" id="nowBtn">当前时间</button>
</div>
<div class="result-box" id="resultBox">
<div class="result-item"><span class="result-label">秒级时间戳</span><span class="result-value" id="tsSeconds"></span></div>
<div class="result-item"><span class="result-label">毫秒级时间戳</span><span class="result-value" id="tsMillis"></span></div>
</div>
</div>
<div class="section">
<h2>时间戳 → 日期</h2>
<div class="form-group">
<label>输入时间戳</label>
<input type="text" id="tsInput" placeholder="输入秒级或毫秒级时间戳">
</div>
<div class="btn-group">
<button class="btn btn-primary" id="toDateBtn">转为日期</button>
<button class="btn btn-secondary" id="nowTSBtn">当前时间戳</button>
</div>
<div class="result-box" id="dateResultBox">
<div class="result-item"><span class="result-label">UTC时间</span><span class="result-value" id="utcDate"></span></div>
<div class="result-item"><span class="result-label">本地时间</span><span class="result-value" id="localDate"></span></div>
<div class="result-item"><span class="result-label">ISO 8601</span><span class="result-value" id="isoDate"></span></div>
</div>
</div>'''
    
    elif slug == "color-names":
        return '''<div class="section">
<h2>HTML颜色名称搜索</h2>
<div class="form-row">
<div class="form-group">
<label>搜索颜色</label>
<input type="text" id="colorSearch" placeholder="输入颜色名称搜索...">
</div>
<div class="form-group">
<label>按色系筛选</label>
<select id="colorFilter">
<option value="all">全部颜色</option>
<option value="red">红色系</option>
<option value="pink">粉色系</option>
<option value="orange">橙色系</option>
<option value="yellow">黄色系</option>
<option value="green">绿色系</option>
<option value="blue">蓝色系</option>
<option value="purple">紫色系</option>
<option value="brown">棕色系</option>
<option value="gray">灰色系</option>
<option value="white">白色系</option>
</select>
</div>
</div>
<div id="colorGrid" style="display:grid;grid-template-columns:repeat(auto-fill,minmax(120px,1fr));gap:8px;margin-top:12px;"></div>
<div style="text-align:center;color:#64748b;margin-top:8px;font-size:.85rem">共 <span id="colorCount">0</span> 种颜色 · 点击复制颜色名称</div>
</div>'''
    
    elif slug == "workdays-calculator":
        return '''<div class="section">
<h2>工作日计算</h2>
<div class="form-row">
<div class="form-group">
<label>开始日期</label>
<input type="date" id="startDate">
</div>
<div class="form-group">
<label>结束日期</label>
<input type="date" id="endDate">
</div>
</div>
<div class="form-group">
<label>排除节假日（用逗号分隔）</label>
<input type="text" id="holidays" placeholder="可选：2026-10-01,2026-10-02">
</div>
<div class="btn-group">
<button class="btn btn-primary" id="calcBtn">计算工作日</button>
</div>
<div class="result-box" id="resultBox">
<div class="result-item"><span class="result-label">总天数</span><span class="result-value" id="totalDays"></span></div>
<div class="result-item"><span class="result-label">工作日</span><span class="result-value" id="workDays"></span></div>
<div class="result-item"><span class="result-label">周末天数</span><span class="result-value" id="weekendDays"></span></div>
<div class="result-item"><span class="result-label">排除节假日</span><span class="result-value" id="holidayDays"></span></div>
</div>
</div>'''
    
    elif slug == "ideal-weight":
        return '''<div class="section">
<h2>理想体重计算</h2>
<div class="form-row">
<div class="form-group">
<label>性别</label>
<select id="gender"><option value="male">男</option><option value="female">女</option></select>
</div>
<div class="form-group">
<label>身高 (cm)</label>
<input type="number" id="height" placeholder="例如：170" min="100" max="250" value="170">
</div>
</div>
<div class="form-group">
<label>计算公式</label>
<select id="formula">
<option value="devine">Devine公式</option>
<option value="robinson">Robinson公式</option>
<option value="miller">Miller公式</option>
<option value="bmi">BMI健康范围</option>
</select>
</div>
<div class="btn-group">
<button class="btn btn-primary" id="calcBtn">计算</button>
</div>
<div class="result-box" id="resultBox">
<div class="result-item"><span class="result-label">计算公式</span><span class="result-value" id="formulaName"></span></div>
<div class="result-item"><span class="result-label">理想体重</span><span class="result-value" id="idealWeightKg"></span></div>
<div class="result-item"><span class="result-label">健康体重范围</span><span class="result-value" id="healthyRange"></span></div>
</div>
</div>'''
    
    elif slug == "water-intake":
        return '''<div class="section">
<h2>每日饮水量</h2>
<div class="form-row">
<div class="form-group">
<label>体重 (kg)</label>
<input type="number" id="weight" placeholder="例如：65" min="30" max="200" value="65">
</div>
<div class="form-group">
<label>活动水平</label>
<select id="activity">
<option value="sedentary">久坐（几乎不运动）</option>
<option value="light">轻度活动（每周1-3次）</option>
<option value="moderate">中度活动（每周3-5次）</option>
<option value="active">高度活动（每周6-7次）</option>
<option value="very-active">极高强度（每天训练）</option>
</select>
</div>
</div>
<div class="form-group">
<label>气候条件</label>
<select id="climate">
<option value="cool">凉爽</option>
<option value="normal">常温</option>
<option value="hot">炎热</option>
<option value="very-hot">极热</option>
</select>
</div>
<div class="btn-group">
<button class="btn btn-primary" id="calcBtn">计算</button>
</div>
<div class="result-box" id="resultBox">
<div class="result-item"><span class="result-label">每日建议饮水量</span><span class="result-value" id="waterLiters"></span></div>
<div class="result-item"><span class="result-label">约合杯数 (250ml/杯)</span><span class="result-value" id="waterCups"></span></div>
<div class="result-item"><span class="result-label">每小时建议</span><span class="result-value" id="waterPerHour"></span></div>
</div>
</div>'''
    
    elif slug == "running-pace":
        return '''<div class="section">
<h2>跑步配速</h2>
<div class="form-row">
<div class="form-group">
<label>距离</label>
<input type="number" id="distance" placeholder="例如：5" min="0.1" step="0.1" value="5">
</div>
<div class="form-group">
<label>单位</label>
<select id="distUnit"><option value="km">公里 (km)</option><option value="mile">英里 (mi)</option></select>
</div>
</div>
<div class="form-row">
<div class="form-group">
<label>时间 (HH:MM:SS)</label>
<input type="text" id="timeInput" placeholder="例如：00:25:00" value="00:25:00">
</div>
</div>
<div class="btn-group">
<button class="btn btn-primary" id="calcBtn">计算配速</button>
</div>
<div class="result-box" id="resultBox">
<div class="result-item"><span class="result-label">每公里配速</span><span class="result-value" id="paceKm"></span></div>
<div class="result-item"><span class="result-label">每英里配速</span><span class="result-value" id="paceMile"></span></div>
<div class="result-item"><span class="result-label">速度</span><span class="result-value" id="speedKph"></span></div>
<div class="result-item"><span class="result-label">5K预测</span><span class="result-value" id="predict5k"></span></div>
<div class="result-item"><span class="result-label">半马预测</span><span class="result-value" id="predictHalf"></span></div>
<div class="result-item"><span class="result-label">全马预测</span><span class="result-value" id="predictFull"></span></div>
</div>
</div>'''
    
    elif slug == "paragraph-counter":
        return '''<div class="section">
<h2>段落统计</h2>
<div class="form-group">
<label>输入文本</label>
<textarea id="textInput" placeholder="在此粘贴或输入文本..."></textarea>
</div>
<div class="result-box show" id="resultBox">
<div class="result-item"><span class="result-label">段落总数</span><span class="result-value" id="paraCount">0</span></div>
<div class="result-item"><span class="result-label">总字数</span><span class="result-value" id="wordCount">0</span></div>
<div class="result-item"><span class="result-label">总字符数</span><span class="result-value" id="charCount">0</span></div>
<div class="result-item"><span class="result-label">平均每段字数</span><span class="result-value" id="avgWordsPerPara">0</span></div>
<div class="result-item"><span class="result-label">最长段落字数</span><span class="result-value" id="maxWordsPerPara">0</span></div>
<div class="result-item"><span class="result-label">最短段落字数</span><span class="result-value" id="minWordsPerPara">0</span></div>
</div>
</div>'''
    
    elif slug == "vowel-counter":
        return '''<div class="section">
<h2>元音统计</h2>
<div class="form-group">
<label>输入文本</label>
<textarea id="textInput" placeholder="在此粘贴或输入英文文本..."></textarea>
</div>
<div class="result-box show" id="resultBox">
<div class="result-item"><span class="result-label">总字符数</span><span class="result-value" id="totalChars">0</span></div>
<div class="result-item"><span class="result-label">总元音数</span><span class="result-value" id="totalVowels">0</span></div>
<div class="result-item"><span class="result-label">元音比例</span><span class="result-value" id="vowelRatio">0%</span></div>
<div class="result-item"><span class="result-label">A 数量</span><span class="result-value" id="countA">0</span></div>
<div class="result-item"><span class="result-label">E 数量</span><span class="result-value" id="countE">0</span></div>
<div class="result-item"><span class="result-label">I 数量</span><span class="result-value" id="countI">0</span></div>
<div class="result-item"><span class="result-label">O 数量</span><span class="result-value" id="countO">0</span></div>
<div class="result-item"><span class="result-label">U 数量</span><span class="result-value" id="countU">0</span></div>
</div>
</div>'''
    
    elif slug == "keyword-density":
        return '''<div class="section">
<h2>关键词密度分析</h2>
<div class="form-group">
<label>输入文本</label>
<textarea id="textInput" placeholder="在此粘贴需要分析的文本..." rows="8"></textarea>
</div>
<div class="form-group">
<label>关键词（逗号分隔多个）</label>
<input type="text" id="keywordInput" placeholder="例如：SEO, 关键词, 分析">
</div>
<div class="btn-group">
<button class="btn btn-primary" id="analyzeBtn">分析</button>
<button class="btn btn-secondary" id="clearBtn">清空</button>
</div>
<div class="result-box" id="resultBox">
<div class="result-item"><span class="result-label">总词数</span><span class="result-value" id="totalWords">-</span></div>
<div id="keywordResults"></div>
</div>
</div>'''

def get_tool_script_cn(tool):
    slug = tool["slug"]
    
    if slug == "utc-converter":
        return '''<script>
const tzs=["UTC-12","UTC-11","UTC-10","UTC-9","UTC-8","UTC-7","UTC-6","UTC-5","UTC-4","UTC-3","UTC-2","UTC-1","UTC+0","UTC+1","UTC+2","UTC+3","UTC+4","UTC+5","UTC+6","UTC+7","UTC+8","UTC+9","UTC+10","UTC+11","UTC+12"];
const tzNames={"UTC-12":"国际日期变更线西","UTC-11":"中途岛","UTC-10":"夏威夷","UTC-9":"阿拉斯加","UTC-8":"太平洋时间(美国)","UTC-7":"山地时间(美国)","UTC-6":"中部时间(美国)","UTC-5":"东部时间(美国)","UTC-4":"大西洋时间","UTC-3":"巴西","UTC-2":"中大西洋","UTC-1":"亚速尔群岛","UTC+0":"伦敦/格林威治","UTC+1":"巴黎/柏林","UTC+2":"开罗/雅典","UTC+3":"莫斯科","UTC+4":"迪拜","UTC+5":"巴基斯坦","UTC+6":"孟加拉","UTC+7":"曼谷/河内","UTC+8":"北京/新加坡","UTC+9":"东京/首尔","UTC+10":"悉尼","UTC+11":"所罗门群岛","UTC+12":"奥克兰"};
function getOffset(tz){return parseInt(tz.replace("UTC",""));}
function fmtDate(d){return d.toISOString().slice(0,16).replace("T"," ")+" UTC";}
function fmtLocal(d){return d.toLocaleString("zh-CN",{timeZone:Intl.DateTimeFormat().resolvedOptions().timeZone});}
function showToast(msg){var t=document.getElementById("toast");t.textContent=msg;t.classList.add("show");setTimeout(function(){t.classList.remove("show");},2000);}
function updateNow(){
  var now=new Date();
  document.getElementById("currentUTC").textContent=now.toISOString().replace("T"," ").slice(0,19)+" UTC";
  document.getElementById("currentLocal").textContent=fmtLocal(now);
}
function populateTZ(){
  var s1=document.getElementById("targetTZ"),s2=document.getElementById("quickTZ");
  var localTZ="UTC"+(new Date().getTimezoneOffset()/-60>=0?"+":"")+(new Date().getTimezoneOffset()/-60);
  tzs.forEach(function(tz){
    var o1=document.createElement("option"),o2=document.createElement("option");
    o1.value=o2.value=tz;o1.textContent=o2.textContent=tz+" ("+tzNames[tz]+")";
    if(tz===localTZ){o1.selected=true;o2.selected=true;}
    s1.appendChild(o1);s2.appendChild(o2);
  });
}
document.getElementById("convertBtn").addEventListener("click",function(){
  var utcVal=document.getElementById("utcInput").value;
  if(!utcVal){showToast("请先输入UTC时间");return;}
  var utcDate=new Date(utcVal+"Z");
  var tz=document.getElementById("targetTZ").value;
  var offset=getOffset(tz);
  var localDate=new Date(utcDate.getTime()+offset*3600000);
  document.getElementById("inputUTC").textContent=fmtDate(utcDate);
  document.getElementById("targetTZName").textContent=tz+" ("+tzNames[tz]+")";
  document.getElementById("convertedTime").textContent=localDate.toISOString().replace("T"," ").slice(0,19);
  document.getElementById("isoTime").textContent=localDate.toISOString().slice(0,19)+tz.replace("UTC","");
  document.getElementById("resultBox").classList.add("show");
});
document.getElementById("nowBtn").addEventListener("click",function(){
  var now=new Date();
  document.getElementById("utcInput").value=now.toISOString().slice(0,16);
});
document.getElementById("quickTZ").addEventListener("change",function(){
  var tz=this.value,offset=getOffset(tz),now=new Date();
  var localDate=new Date(now.getTime()+offset*3600000);
  document.getElementById("quickResult").textContent=tz+" ("+tzNames[tz]+"): "+localDate.toISOString().replace("T"," ").slice(0,19);
});
document.querySelectorAll(".result-value").forEach(function(el){el.addEventListener("click",function(){navigator.clipboard.writeText(this.textContent);showToast("已复制到剪贴板");});});
populateTZ();updateNow();setInterval(updateNow,1000);
document.getElementById("quickTZ").dispatchEvent(new Event("change"));
</script>'''
    
    elif slug == "date-to-timestamp":
        return '''<script>
function showToast(msg){var t=document.getElementById("toast");t.textContent=msg;t.classList.add("show");setTimeout(function(){t.classList.remove("show");},2000);}
document.getElementById("toTimestampBtn").addEventListener("click",function(){
  var val=document.getElementById("dateInput").value;
  if(!val){showToast("请先选择日期");return;}
  var d=new Date(val);
  var sec=Math.floor(d.getTime()/1000);
  document.getElementById("tsSeconds").textContent=sec;
  document.getElementById("tsMillis").textContent=d.getTime();
  document.getElementById("resultBox").classList.add("show");
});
document.getElementById("nowBtn").addEventListener("click",function(){
  document.getElementById("dateInput").value=new Date().toISOString().slice(0,16);
});
document.getElementById("toDateBtn").addEventListener("click",function(){
  var val=document.getElementById("tsInput").value.trim();
  if(!val){showToast("请输入时间戳");return;}
  var ts=parseInt(val);
  if(isNaN(ts)){showToast("时间戳格式错误");return;}
  if(ts<10000000000)ts*=1000;
  var d=new Date(ts);
  document.getElementById("utcDate").textContent=d.toISOString().replace("T"," ").slice(0,19)+" UTC";
  document.getElementById("localDate").textContent=d.toLocaleString("zh-CN");
  document.getElementById("isoDate").textContent=d.toISOString();
  document.getElementById("dateResultBox").classList.add("show");
});
document.getElementById("nowTSBtn").addEventListener("click",function(){
  document.getElementById("tsInput").value=Math.floor(Date.now()/1000);
});
document.querySelectorAll(".result-value").forEach(function(el){el.addEventListener("click",function(){navigator.clipboard.writeText(this.textContent);showToast("已复制");});});
</script>'''
    
    elif slug == "color-names":
        return '''<script>
var colors=[
  {name:"AliceBlue",hex:"#F0F8FF",rgb:"240,248,255",group:"white"},
  {name:"AntiqueWhite",hex:"#FAEBD7",rgb:"250,235,215",group:"white"},
  {name:"Aqua",hex:"#00FFFF",rgb:"0,255,255",group:"blue"},
  {name:"Aquamarine",hex:"#7FFFD4",rgb:"127,255,212",group:"green"},
  {name:"Azure",hex:"#F0FFFF",rgb:"240,255,255",group:"white"},
  {name:"Beige",hex:"#F5F5DC",rgb:"245,245,220",group:"white"},
  {name:"Bisque",hex:"#FFE4C4",rgb:"255,228,196",group:"orange"},
  {name:"Black",hex:"#000000",rgb:"0,0,0",group:"gray"},
  {name:"BlanchedAlmond",hex:"#FFEBCD",rgb:"255,235,205",group:"orange"},
  {name:"Blue",hex:"#0000FF",rgb:"0,0,255",group:"blue"},
  {name:"BlueViolet",hex:"#8A2BE2",rgb:"138,43,226",group:"purple"},
  {name:"Brown",hex:"#A52A2A",rgb:"165,42,42",group:"brown"},
  {name:"BurlyWood",hex:"#DEB887",rgb:"222,184,135",group:"brown"},
  {name:"CadetBlue",hex:"#5F9EA0",rgb:"95,158,160",group:"blue"},
  {name:"Chartreuse",hex:"#7FFF00",rgb:"127,255,0",group:"green"},
  {name:"Chocolate",hex:"#D2691E",rgb:"210,105,30",group:"brown"},
  {name:"Coral",hex:"#FF7F50",rgb:"255,127,80",group:"red"},
  {name:"CornflowerBlue",hex:"#6495ED",rgb:"100,149,237",group:"blue"},
  {name:"Cornsilk",hex:"#FFF8DC",rgb:"255,248,220",group:"white"},
  {name:"Crimson",hex:"#DC143C",rgb:"220,20,60",group:"red"},
  {name:"Cyan",hex:"#00FFFF",rgb:"0,255,255",group:"blue"},
  {name:"DarkBlue",hex:"#00008B",rgb:"0,0,139",group:"blue"},
  {name:"DarkCyan",hex:"#008B8B",rgb:"0,139,139",group:"blue"},
  {name:"DarkGoldenRod",hex:"#B8860B",rgb:"184,134,11",group:"yellow"},
  {name:"DarkGray",hex:"#A9A9A9",rgb:"169,169,169",group:"gray"},
  {name:"DarkGreen",hex:"#006400",rgb:"0,100,0",group:"green"},
  {name:"DarkKhaki",hex:"#BDB76B",rgb:"189,183,107",group:"yellow"},
  {name:"DarkMagenta",hex:"#8B008B",rgb:"139,0,139",group:"purple"},
  {name:"DarkOliveGreen",hex:"#556B2F",rgb:"85,107,47",group:"green"},
  {name:"DarkOrange",hex:"#FF8C00",rgb:"255,140,0",group:"orange"},
  {name:"DarkOrchid",hex:"#9932CC",rgb:"153,50,204",group:"purple"},
  {name:"DarkRed",hex:"#8B0000",rgb:"139,0,0",group:"red"},
  {name:"DarkSalmon",hex:"#E9967A",rgb:"233,150,122",group:"red"},
  {name:"DarkSeaGreen",hex:"#8FBC8F",rgb:"143,188,143",group:"green"},
  {name:"DarkSlateBlue",hex:"#483D8B",rgb:"72,61,139",group:"purple"},
  {name:"DarkSlateGray",hex:"#2F4F4F",rgb:"47,79,79",group:"gray"},
  {name:"DarkTurquoise",hex:"#00CED1",rgb:"0,206,209",group:"blue"},
  {name:"DarkViolet",hex:"#9400D3",rgb:"148,0,211",group:"purple"},
  {name:"DeepPink",hex:"#FF1493",rgb:"255,20,147",group:"pink"},
  {name:"DeepSkyBlue",hex:"#00BFFF",rgb:"0,191,255",group:"blue"},
  {name:"DimGray",hex:"#696969",rgb:"105,105,105",group:"gray"},
  {name:"DodgerBlue",hex:"#1E90FF",rgb:"30,144,255",group:"blue"},
  {name:"FireBrick",hex:"#B22222",rgb:"178,34,34",group:"red"},
  {name:"FloralWhite",hex:"#FFFAF0",rgb:"255,250,240",group:"white"},
  {name:"ForestGreen",hex:"#228B22",rgb:"34,139,34",group:"green"},
  {name:"Fuchsia",hex:"#FF00FF",rgb:"255,0,255",group:"purple"},
  {name:"Gainsboro",hex:"#DCDCDC",rgb:"220,220,220",group:"gray"},
  {name:"GhostWhite",hex:"#F8F8FF",rgb:"248,248,255",group:"white"},
  {name:"Gold",hex:"#FFD700",rgb:"255,215,0",group:"yellow"},
  {name:"GoldenRod",hex:"#DAA520",rgb:"218,165,32",group:"yellow"},
  {name:"Gray",hex:"#808080",rgb:"128,128,128",group:"gray"},
  {name:"Green",hex:"#008000",rgb:"0,128,0",group:"green"},
  {name:"GreenYellow",hex:"#ADFF2F",rgb:"173,255,47",group:"green"},
  {name:"HoneyDew",hex:"#F0FFF0",rgb:"240,255,240",group:"white"},
  {name:"HotPink",hex:"#FF69B4",rgb:"255,105,180",group:"pink"},
  {name:"IndianRed",hex:"#CD5C5C",rgb:"205,92,92",group:"red"},
  {name:"Indigo",hex:"#4B0082",rgb:"75,0,130",group:"purple"},
  {name:"Ivory",hex:"#FFFFF0",rgb:"255,255,240",group:"white"},
  {name:"Khaki",hex:"#F0E68C",rgb:"240,230,140",group:"yellow"},
  {name:"Lavender",hex:"#E6E6FA",rgb:"230,230,250",group:"purple"},
  {name:"LavenderBlush",hex:"#FFF0F5",rgb:"255,240,245",group:"pink"},
  {name:"LawnGreen",hex:"#7CFC00",rgb:"124,252,0",group:"green"},
  {name:"LemonChiffon",hex:"#FFFACD",rgb:"255,250,205",group:"yellow"},
  {name:"LightBlue",hex:"#ADD8E6",rgb:"173,216,230",group:"blue"},
  {name:"LightCoral",hex:"#F08080",rgb:"240,128,128",group:"red"},
  {name:"LightCyan",hex:"#E0FFFF",rgb:"224,255,255",group:"blue"},
  {name:"LightGoldenRodYellow",hex:"#FAFAD2",rgb:"250,250,210",group:"yellow"},
  {name:"LightGray",hex:"#D3D3D3",rgb:"211,211,211",group:"gray"},
  {name:"LightGreen",hex:"#90EE90",rgb:"144,238,144",group:"green"},
  {name:"LightPink",hex:"#FFB6C1",rgb:"255,182,193",group:"pink"},
  {name:"LightSalmon",hex:"#FFA07A",rgb:"255,160,122",group:"red"},
  {name:"LightSeaGreen",hex:"#20B2AA",rgb:"32,178,170",group:"green"},
  {name:"LightSkyBlue",hex:"#87CEFA",rgb:"135,206,250",group:"blue"},
  {name:"LightSlateGray",hex:"#778899",rgb:"119,136,153",group:"gray"},
  {name:"LightSteelBlue",hex:"#B0C4DE",rgb:"176,196,222",group:"blue"},
  {name:"LightYellow",hex:"#FFFFE0",rgb:"255,255,224",group:"yellow"},
  {name:"Lime",hex:"#00FF00",rgb:"0,255,0",group:"green"},
  {name:"LimeGreen",hex:"#32CD32",rgb:"50,205,50",group:"green"},
  {name:"Linen",hex:"#FAF0E6",rgb:"250,240,230",group:"white"},
  {name:"Magenta",hex:"#FF00FF",rgb:"255,0,255",group:"purple"},
  {name:"Maroon",hex:"#800000",rgb:"128,0,0",group:"red"},
  {name:"MediumAquaMarine",hex:"#66CDAA",rgb:"102,205,170",group:"green"},
  {name:"MediumBlue",hex:"#0000CD",rgb:"0,0,205",group:"blue"},
  {name:"MediumOrchid",hex:"#BA55D3",rgb:"186,85,211",group:"purple"},
  {name:"MediumPurple",hex:"#9370DB",rgb:"147,112,219",group:"purple"},
  {name:"MediumSeaGreen",hex:"#3CB371",rgb:"60,179,113",group:"green"},
  {name:"MediumSlateBlue",hex:"#7B68EE",rgb:"123,104,238",group:"purple"},
  {name:"MediumSpringGreen",hex:"#00FA9A",rgb:"0,250,154",group:"green"},
  {name:"MediumTurquoise",hex:"#48D1CC",rgb:"72,209,204",group:"blue"},
  {name:"MediumVioletRed",hex:"#C71585",rgb:"199,21,133",group:"pink"},
  {name:"MidnightBlue",hex:"#191970",rgb:"25,25,112",group:"blue"},
  {name:"MintCream",hex:"#F5FFFA",rgb:"245,255,250",group:"white"},
  {name:"MistyRose",hex:"#FFE4E1",rgb:"255,228,225",group:"pink"},
  {name:"Moccasin",hex:"#FFE4B5",rgb:"255,228,181",group:"orange"},
  {name:"NavajoWhite",hex:"#FFDEAD",rgb:"255,222,173",group:"orange"},
  {name:"Navy",hex:"#000080",rgb:"0,0,128",group:"blue"},
  {name:"OldLace",hex:"#FDF5E6",rgb:"253,245,230",group:"white"},
  {name:"Olive",hex:"#808000",rgb:"128,128,0",group:"yellow"},
  {name:"OliveDrab",hex:"#6B8E23",rgb:"107,142,35",group:"green"},
  {name:"Orange",hex:"#FFA500",rgb:"255,165,0",group:"orange"},
  {name:"OrangeRed",hex:"#FF4500",rgb:"255,69,0",group:"red"},
  {name:"Orchid",hex:"#DA70D6",rgb:"218,112,214",group:"purple"},
  {name:"PaleGoldenRod",hex:"#EEE8AA",rgb:"238,232,170",group:"yellow"},
  {name:"PaleGreen",hex:"#98FB98",rgb:"152,251,152",group:"green"},
  {name:"PaleTurquoise",hex:"#AFEEEE",rgb:"175,238,238",group:"blue"},
  {name:"PaleVioletRed",hex:"#DB7093",rgb:"219,112,147",group:"pink"},
  {name:"PapayaWhip",hex:"#FFEFD5",rgb:"255,239,213",group:"orange"},
  {name:"PeachPuff",hex:"#FFDAB9",rgb:"255,218,185",group:"orange"},
  {name:"Peru",hex:"#CD853F",rgb:"205,133,63",group:"brown"},
  {name:"Pink",hex:"#FFC0CB",rgb:"255,192,203",group:"pink"},
  {name:"Plum",hex:"#DDA0DD",rgb:"221,160,221",group:"purple"},
  {name:"PowderBlue",hex:"#B0E0E6",rgb:"176,224,230",group:"blue"},
  {name:"Purple",hex:"#800080",rgb:"128,0,128",group:"purple"},
  {name:"RebeccaPurple",hex:"#663399",rgb:"102,51,153",group:"purple"},
  {name:"Red",hex:"#FF0000",rgb:"255,0,0",group:"red"},
  {name:"RosyBrown",hex:"#BC8F8F",rgb:"188,143,143",group:"brown"},
  {name:"RoyalBlue",hex:"#4169E1",rgb:"65,105,225",group:"blue"},
  {name:"SaddleBrown",hex:"#8B4513",rgb:"139,69,19",group:"brown"},
  {name:"Salmon",hex:"#FA8072",rgb:"250,128,114",group:"red"},
  {name:"SandyBrown",hex:"#F4A460",rgb:"244,164,96",group:"orange"},
  {name:"SeaGreen",hex:"#2E8B57",rgb:"46,139,87",group:"green"},
  {name:"SeaShell",hex:"#FFF5EE",rgb:"255,245,238",group:"white"},
  {name:"Sienna",hex:"#A0522D",rgb:"160,82,45",group:"brown"},
  {name:"Silver",hex:"#C0C0C0",rgb:"192,192,192",group:"gray"},
  {name:"SkyBlue",hex:"#87CEEB",rgb:"135,206,235",group:"blue"},
  {name:"SlateBlue",hex:"#6A5ACD",rgb:"106,90,205",group:"purple"},
  {name:"SlateGray",hex:"#708090",rgb:"112,128,144",group:"gray"},
  {name:"Snow",hex:"#FFFAFA",rgb:"255,250,250",group:"white"},
  {name:"SpringGreen",hex:"#00FF7F",rgb:"0,255,127",group:"green"},
  {name:"SteelBlue",hex:"#4682B4",rgb:"70,130,180",group:"blue"},
  {name:"Tan",hex:"#D2B48C",rgb:"210,180,140",group:"brown"},
  {name:"Teal",hex:"#008080",rgb:"0,128,128",group:"blue"},
  {name:"Thistle",hex:"#D8BFD8",rgb:"216,191,216",group:"purple"},
  {name:"Tomato",hex:"#FF6347",rgb:"255,99,71",group:"red"},
  {name:"Turquoise",hex:"#40E0D0",rgb:"64,224,208",group:"blue"},
  {name:"Violet",hex:"#EE82EE",rgb:"238,130,238",group:"purple"},
  {name:"Wheat",hex:"#F5DEB3",rgb:"245,222,179",group:"orange"},
  {name:"White",hex:"#FFFFFF",rgb:"255,255,255",group:"white"},
  {name:"WhiteSmoke",hex:"#F5F5F5",rgb:"245,245,245",group:"white"},
  {name:"Yellow",hex:"#FFFF00",rgb:"255,255,0",group:"yellow"},
  {name:"YellowGreen",hex:"#9ACD32",rgb:"154,205,50",group:"green"}
];
function showToast(msg){var t=document.getElementById("toast");t.textContent=msg;t.classList.add("show");setTimeout(function(){t.classList.remove("show");},2000);}
function renderColors(filter,search){
  var grid=document.getElementById("colorGrid");grid.innerHTML="";
  var q=(search||"").toLowerCase(),g=(filter||"all");
  var shown=0;
  colors.forEach(function(c){
    if(g!=="all"&&c.group!==g)return;
    if(q&&c.name.toLowerCase().indexOf(q)===-1&&c.hex.toLowerCase().indexOf(q)===-1)return;
    shown++;
    var div=document.createElement("div");
    div.style.cssText="padding:12px 8px;border-radius:8px;text-align:center;cursor:pointer;transition:transform .15s;border:1px solid rgba(148,163,184,.1);background:"+c.hex+";color:"+(c.group==="white"||c.group==="yellow"?"#0f172a":"#fff");
    div.innerHTML='<div style="font-size:.8rem;font-weight:600;margin-bottom:4px">'+c.name+'</div><div style="font-size:.7rem;opacity:.8">'+c.hex+'</div>';
    div.addEventListener("click",function(){navigator.clipboard.writeText(c.name);showToast("已复制: "+c.name);});
    div.addEventListener("mouseenter",function(){this.style.transform="scale(1.05)";});
    div.addEventListener("mouseleave",function(){this.style.transform="scale(1)";});
    grid.appendChild(div);
  });
  document.getElementById("colorCount").textContent=shown;
}
document.getElementById("colorSearch").addEventListener("input",function(){renderColors(document.getElementById("colorFilter").value,this.value);});
document.getElementById("colorFilter").addEventListener("change",function(){renderColors(this.value,document.getElementById("colorSearch").value);});
renderColors("all","");
</script>'''
    
    elif slug == "workdays-calculator":
        return '''<script>
function showToast(msg){var t=document.getElementById("toast");t.textContent=msg;t.classList.add("show");setTimeout(function(){t.classList.remove("show");},2000);}
document.getElementById("calcBtn").addEventListener("click",function(){
  var s=document.getElementById("startDate").value,e=document.getElementById("endDate").value;
  if(!s||!e){showToast("请选择开始和结束日期");return;}
  var start=new Date(s+"T00:00:00"),end=new Date(e+"T00:00:00");
  if(start>end){showToast("开始日期不能晚于结束日期");return;}
  var holidays=document.getElementById("holidays").value.split(",").map(function(h){return h.trim();}).filter(Boolean);
  var total=0,work=0,weekend=0,holiday=0;
  var cur=new Date(start);
  while(cur<=end){
    total++;
    var ds=cur.toISOString().slice(0,10),isWeekend=cur.getDay()===0||cur.getDay()===6,isHoliday=holidays.indexOf(ds)!==-1;
    if(isHoliday){holiday++;}else if(isWeekend){weekend++;}else{work++;}
    cur.setDate(cur.getDate()+1);
  }
  document.getElementById("totalDays").textContent=total+" 天";
  document.getElementById("workDays").textContent=work+" 天";
  document.getElementById("weekendDays").textContent=weekend+" 天";
  document.getElementById("holidayDays").textContent=holiday+" 天";
  document.getElementById("resultBox").classList.add("show");
});
document.addEventListener("DOMContentLoaded",function(){
  var today=new Date().toISOString().slice(0,10);
  document.getElementById("startDate").value=today;
  var next=new Date();next.setDate(next.getDate()+30);
  document.getElementById("endDate").value=next.toISOString().slice(0,10);
});
</script>'''
    
    elif slug == "ideal-weight":
        return '''<script>
function showToast(msg){var t=document.getElementById("toast");t.textContent=msg;t.classList.add("show");setTimeout(function(){t.classList.remove("show");},2000);}
document.getElementById("calcBtn").addEventListener("click",function(){
  var h=parseFloat(document.getElementById("height").value),g=document.getElementById("gender").value,f=document.getElementById("formula").value;
  if(!h||h<100||h>250){showToast("请输入有效身高(100-250cm)");return;}
  var inch=h/2.54,kg,rangeLow,rangeHigh,fName;
  if(f==="devine"){
    kg=g==="male"?50+2.3*(inch-60):45.5+2.3*(inch-60);fName="Devine公式";
  }else if(f==="robinson"){
    kg=g==="male"?52+1.9*(inch-60):49+1.7*(inch-60);fName="Robinson公式";
  }else if(f==="miller"){
    kg=g==="male"?56.2+1.41*(inch-60):53.1+1.36*(inch-60);fName="Miller公式";
  }else{
    var hM=h/100;rangeLow=(18.5*hM*hM).toFixed(1);rangeHigh=(24*hM*hM).toFixed(1);kg=((parseFloat(rangeLow)+parseFloat(rangeHigh))/2).toFixed(1);fName="BMI健康范围";
  }
  var hM=h/100;rangeLow=(18.5*hM*hM).toFixed(1);rangeHigh=(24*hM*hM).toFixed(1);
  document.getElementById("formulaName").textContent=fName;
  document.getElementById("idealWeightKg").textContent=(typeof kg==="number"?kg.toFixed(1):kg)+" kg";
  document.getElementById("healthyRange").textContent=rangeLow+" - "+rangeHigh+" kg (BMI 18.5-24)";
  document.getElementById("resultBox").classList.add("show");
});
</script>'''
    
    elif slug == "water-intake":
        return '''<script>
function showToast(msg){var t=document.getElementById("toast");t.textContent=msg;t.classList.add("show");setTimeout(function(){t.classList.remove("show");},2000);}
document.getElementById("calcBtn").addEventListener("click",function(){
  var w=parseFloat(document.getElementById("weight").value),act=document.getElementById("activity").value,cli=document.getElementById("climate").value;
  if(!w||w<30||w>200){showToast("请输入有效体重(30-200kg)");return;}
  var base=w*35,actM={sedentary:0.8,light:1,moderate:1.2,active:1.5,"very-active":1.8},cliM={cool:0.9,normal:1,hot:1.2,"very-hot":1.4};
  var ml=base*actM[act]*cliM[cli];
  var liters=(ml/1000).toFixed(1),cups=Math.round(ml/250),perHour=(ml/16/1000).toFixed(1);
  document.getElementById("waterLiters").textContent=liters+" 升/天";
  document.getElementById("waterCups").textContent=cups+" 杯 (250ml/杯)";
  document.getElementById("waterPerHour").textContent=perHour+" 升 (按清醒16小时计)";
  document.getElementById("resultBox").classList.add("show");
});
</script>'''
    
    elif slug == "running-pace":
        return '''<script>
function showToast(msg){var t=document.getElementById("toast");t.textContent=msg;t.classList.add("show");setTimeout(function(){t.classList.remove("show");},2000);}
function fmtTime(sec){var m=Math.floor(sec/60),s=Math.round(sec%60);return m+":"+(s<10?"0":"")+s;}
function fmtPace(sec){var m=Math.floor(sec/60),s=Math.round(sec%60);return m+"'"+s+'"';}
document.getElementById("calcBtn").addEventListener("click",function(){
  var d=parseFloat(document.getElementById("distance").value),unit=document.getElementById("distUnit").value,timeStr=document.getElementById("timeInput").value.trim();
  if(!d||d<=0){showToast("请输入有效距离");return;}
  var parts=timeStr.split(":"),totalSec=0;
  if(parts.length===3)totalSec=parseInt(parts[0])*3600+parseInt(parts[1])*60+parseInt(parts[2]);
  else if(parts.length===2)totalSec=parseInt(parts[0])*60+parseInt(parts[1]);
  else totalSec=parseInt(parts[0]);
  if(isNaN(totalSec)||totalSec<=0){showToast("请输入有效时间格式(HH:MM:SS)");return;}
  var distKm=unit==="mile"?d*1.60934:d;
  var paceKm=totalSec/distKm,paceMile=paceKm*1.60934,speed=distKm/(totalSec/3600);
  document.getElementById("paceKm").textContent=fmtPace(paceKm)+" /km";
  document.getElementById("paceMile").textContent=fmtPace(paceMile)+" /mi";
  document.getElementById("speedKph").textContent=speed.toFixed(1)+" km/h";
  document.getElementById("predict5k").textContent=fmtTime(paceKm*5);
  document.getElementById("predictHalf").textContent=fmtTime(paceKm*21.0975);
  document.getElementById("predictFull").textContent=fmtTime(paceKm*42.195);
  document.getElementById("resultBox").classList.add("show");
});
</script>'''
    
    elif slug == "paragraph-counter":
        return '''<script>
function showToast(msg){var t=document.getElementById("toast");t.textContent=msg;t.classList.add("show");setTimeout(function(){t.classList.remove("show");},2000);}
document.getElementById("textInput").addEventListener("input",function(){
  var text=this.value;
  if(!text.trim()){document.getElementById("paraCount").textContent="0";document.getElementById("wordCount").textContent="0";document.getElementById("charCount").textContent="0";document.getElementById("avgWordsPerPara").textContent="0";document.getElementById("maxWordsPerPara").textContent="0";document.getElementById("minWordsPerPara").textContent="0";return;}
  var paras=text.split(/\\n\\s*\\n/).filter(function(p){return p.trim();});
  var totalWords=0,charCount=text.length,wordCounts=[];
  paras.forEach(function(p){
    var words=p.trim().split(/\\s+/).filter(function(w){return w.length>0;});
    wordCounts.push(words.length);totalWords+=words.length;
  });
  var avg=paras.length>0?Math.round(totalWords/paras.length):0;
  var maxW=wordCounts.length>0?Math.max.apply(null,wordCounts):0;
  var minW=wordCounts.length>0?Math.min.apply(null,wordCounts):0;
  document.getElementById("paraCount").textContent=paras.length;
  document.getElementById("wordCount").textContent=totalWords;
  document.getElementById("charCount").textContent=charCount;
  document.getElementById("avgWordsPerPara").textContent=avg;
  document.getElementById("maxWordsPerPara").textContent=maxW;
  document.getElementById("minWordsPerPara").textContent=minW;
});
</script>'''
    
    elif slug == "vowel-counter":
        return '''<script>
function showToast(msg){var t=document.getElementById("toast");t.textContent=msg;t.classList.add("show");setTimeout(function(){t.classList.remove("show");},2000);}
document.getElementById("textInput").addEventListener("input",function(){
  var text=this.value;
  if(!text){document.getElementById("totalChars").textContent="0";document.getElementById("totalVowels").textContent="0";document.getElementById("vowelRatio").textContent="0%";document.getElementById("countA").textContent="0";document.getElementById("countE").textContent="0";document.getElementById("countI").textContent="0";document.getElementById("countO").textContent="0";document.getElementById("countU").textContent="0";return;}
  var lower=text.toLowerCase(),total=text.length;
  var a=(lower.match(/a/g)||[]).length,e=(lower.match(/e/g)||[]).length,i=(lower.match(/i/g)||[]).length,o=(lower.match(/o/g)||[]).length,u=(lower.match(/u/g)||[]).length;
  var totalVowels=a+e+i+o+u,ratio=total>0?((totalVowels/total)*100).toFixed(1):0;
  document.getElementById("totalChars").textContent=total;
  document.getElementById("totalVowels").textContent=totalVowels;
  document.getElementById("vowelRatio").textContent=ratio+"%";
  document.getElementById("countA").textContent=a;
  document.getElementById("countE").textContent=e;
  document.getElementById("countI").textContent=i;
  document.getElementById("countO").textContent=o;
  document.getElementById("countU").textContent=u;
});
</script>'''
    
    elif slug == "keyword-density":
        return '''<script>
function showToast(msg){var t=document.getElementById("toast");t.textContent=msg;t.classList.add("show");setTimeout(function(){t.classList.remove("show");},2000);}
document.getElementById("analyzeBtn").addEventListener("click",function(){
  var text=document.getElementById("textInput").value,keywords=document.getElementById("keywordInput").value;
  if(!text.trim()){showToast("请输入文本");return;}
  if(!keywords.trim()){showToast("请输入关键词");return;}
  var words=text.toLowerCase().match(/[\\u4e00-\\u9fa5a-zA-Z0-9]+/g)||[],total=words.length;
  document.getElementById("totalWords").textContent=total+" 词";
  var kwList=keywords.split(",").map(function(k){return k.trim().toLowerCase();}).filter(Boolean);
  var container=document.getElementById("keywordResults");container.innerHTML="";
  kwList.forEach(function(kw){
    var count=0;words.forEach(function(w){if(w===kw)count++;});
    var density=total>0?((count/total)*100).toFixed(2):0,cls=density>5?"color:#f87171":density>3?"color:#fbbf24":"color:#22d3ee";
    var item=document.createElement("div");
    item.className="result-item";
    item.innerHTML='<span class="result-label">"'+kw+'"</span><span class="result-value" style="'+cls+'">'+count+" 次 ("+density+"%)</span>";
    container.appendChild(item);
  });
  document.getElementById("resultBox").classList.add("show");
});
document.getElementById("clearBtn").addEventListener("click",function(){
  document.getElementById("textInput").value="";document.getElementById("keywordInput").value="";document.getElementById("resultBox").classList.remove("show");
});
</script>'''

def get_tool_content_en(tool):
    slug = tool["slug"]
    
    if slug == "utc-converter":
        return '''<div class="section">
<h2>UTC Time Conversion</h2>
<div class="form-group">
<label>Current UTC Time</label>
<div id="currentUTC" style="font-size:1.2rem;color:#22d3ee;font-family:monospace;"></div>
</div>
<div class="form-group">
<label>Current Local Time</label>
<div id="currentLocal" style="font-size:1.2rem;color:#22d3ee;font-family:monospace;"></div>
</div>
<div class="form-row">
<div class="form-group">
<label>Enter UTC Time</label>
<input type="datetime-local" id="utcInput">
</div>
<div class="form-group">
<label>Target Timezone</label>
<select id="targetTZ"></select>
</div>
</div>
<div class="btn-group">
<button class="btn btn-primary" id="convertBtn">Convert</button>
<button class="btn btn-secondary" id="nowBtn">Use Current Time</button>
</div>
<div class="result-box" id="resultBox">
<div class="result-item"><span class="result-label">Input UTC Time</span><span class="result-value" id="inputUTC"></span></div>
<div class="result-item"><span class="result-label">Target Timezone</span><span class="result-value" id="targetTZName"></span></div>
<div class="result-item"><span class="result-label">Converted Time</span><span class="result-value" id="convertedTime"></span></div>
<div class="result-item"><span class="result-label">ISO 8601</span><span class="result-value" id="isoTime"></span></div>
</div>
</div>
<div class="section">
<h2>Quick Timezone Lookup</h2>
<div class="form-group">
<select id="quickTZ" style="margin-bottom:8px"></select>
</div>
<div id="quickResult" style="font-size:1.1rem;color:#22d3ee;font-family:monospace;"></div>
</div>'''
    
    elif slug == "date-to-timestamp":
        return '''<div class="section">
<h2>Date → Timestamp</h2>
<div class="form-group">
<label>Date & Time</label>
<input type="datetime-local" id="dateInput">
</div>
<div class="btn-group">
<button class="btn btn-primary" id="toTimestampBtn">Convert to Timestamp</button>
<button class="btn btn-secondary" id="nowBtn">Current Time</button>
</div>
<div class="result-box" id="resultBox">
<div class="result-item"><span class="result-label">Unix Timestamp (seconds)</span><span class="result-value" id="tsSeconds"></span></div>
<div class="result-item"><span class="result-label">Unix Timestamp (milliseconds)</span><span class="result-value" id="tsMillis"></span></div>
</div>
</div>
<div class="section">
<h2>Timestamp → Date</h2>
<div class="form-group">
<label>Enter Timestamp</label>
<input type="text" id="tsInput" placeholder="Enter seconds or milliseconds timestamp">
</div>
<div class="btn-group">
<button class="btn btn-primary" id="toDateBtn">Convert to Date</button>
<button class="btn btn-secondary" id="nowTSBtn">Current Timestamp</button>
</div>
<div class="result-box" id="dateResultBox">
<div class="result-item"><span class="result-label">UTC Time</span><span class="result-value" id="utcDate"></span></div>
<div class="result-item"><span class="result-label">Local Time</span><span class="result-value" id="localDate"></span></div>
<div class="result-item"><span class="result-label">ISO 8601</span><span class="result-value" id="isoDate"></span></div>
</div>
</div>'''
    
    elif slug == "color-names":
        return '''<div class="section">
<h2>HTML Color Name Search</h2>
<div class="form-row">
<div class="form-group">
<label>Search Colors</label>
<input type="text" id="colorSearch" placeholder="Search by color name...">
</div>
<div class="form-group">
<label>Filter by Group</label>
<select id="colorFilter">
<option value="all">All Colors</option>
<option value="red">Reds</option>
<option value="pink">Pinks</option>
<option value="orange">Oranges</option>
<option value="yellow">Yellows</option>
<option value="green">Greens</option>
<option value="blue">Blues</option>
<option value="purple">Purples</option>
<option value="brown">Browns</option>
<option value="gray">Grays</option>
<option value="white">Whites</option>
</select>
</div>
</div>
<div id="colorGrid" style="display:grid;grid-template-columns:repeat(auto-fill,minmax(120px,1fr));gap:8px;margin-top:12px;"></div>
<div style="text-align:center;color:#64748b;margin-top:8px;font-size:.85rem"><span id="colorCount">0</span> colors · Click to copy name</div>
</div>'''
    
    elif slug == "workdays-calculator":
        return '''<div class="section">
<h2>Workdays Calculation</h2>
<div class="form-row">
<div class="form-group">
<label>Start Date</label>
<input type="date" id="startDate">
</div>
<div class="form-group">
<label>End Date</label>
<input type="date" id="endDate">
</div>
</div>
<div class="form-group">
<label>Exclude Holidays (comma separated)</label>
<input type="text" id="holidays" placeholder="Optional: 2026-12-25,2026-01-01">
</div>
<div class="btn-group">
<button class="btn btn-primary" id="calcBtn">Calculate Workdays</button>
</div>
<div class="result-box" id="resultBox">
<div class="result-item"><span class="result-label">Total Days</span><span class="result-value" id="totalDays"></span></div>
<div class="result-item"><span class="result-label">Workdays</span><span class="result-value" id="workDays"></span></div>
<div class="result-item"><span class="result-label">Weekend Days</span><span class="result-value" id="weekendDays"></span></div>
<div class="result-item"><span class="result-label">Excluded Holidays</span><span class="result-value" id="holidayDays"></span></div>
</div>
</div>'''
    
    elif slug == "ideal-weight":
        return '''<div class="section">
<h2>Ideal Weight Calculator</h2>
<div class="form-row">
<div class="form-group">
<label>Gender</label>
<select id="gender"><option value="male">Male</option><option value="female">Female</option></select>
</div>
<div class="form-group">
<label>Height (cm)</label>
<input type="number" id="height" placeholder="e.g. 170" min="100" max="250" value="170">
</div>
</div>
<div class="form-group">
<label>Formula</label>
<select id="formula">
<option value="devine">Devine Formula</option>
<option value="robinson">Robinson Formula</option>
<option value="miller">Miller Formula</option>
<option value="bmi">BMI Healthy Range</option>
</select>
</div>
<div class="btn-group">
<button class="btn btn-primary" id="calcBtn">Calculate</button>
</div>
<div class="result-box" id="resultBox">
<div class="result-item"><span class="result-label">Formula</span><span class="result-value" id="formulaName"></span></div>
<div class="result-item"><span class="result-label">Ideal Weight</span><span class="result-value" id="idealWeightKg"></span></div>
<div class="result-item"><span class="result-label">Healthy Weight Range</span><span class="result-value" id="healthyRange"></span></div>
</div>
</div>'''
    
    elif slug == "water-intake":
        return '''<div class="section">
<h2>Daily Water Intake</h2>
<div class="form-row">
<div class="form-group">
<label>Weight (kg)</label>
<input type="number" id="weight" placeholder="e.g. 65" min="30" max="200" value="65">
</div>
<div class="form-group">
<label>Activity Level</label>
<select id="activity">
<option value="sedentary">Sedentary (little exercise)</option>
<option value="light">Light (1-3 times/week)</option>
<option value="moderate">Moderate (3-5 times/week)</option>
<option value="active">Active (6-7 times/week)</option>
<option value="very-active">Very Active (daily training)</option>
</select>
</div>
</div>
<div class="form-group">
<label>Climate</label>
<select id="climate">
<option value="cool">Cool</option>
<option value="normal">Normal</option>
<option value="hot">Hot</option>
<option value="very-hot">Very Hot</option>
</select>
</div>
<div class="btn-group">
<button class="btn btn-primary" id="calcBtn">Calculate</button>
</div>
<div class="result-box" id="resultBox">
<div class="result-item"><span class="result-label">Daily Water Recommendation</span><span class="result-value" id="waterLiters"></span></div>
<div class="result-item"><span class="result-label">Approx. Cups (250ml/cup)</span><span class="result-value" id="waterCups"></span></div>
<div class="result-item"><span class="result-label">Per Hour (16 waking hours)</span><span class="result-value" id="waterPerHour"></span></div>
</div>
</div>'''
    
    elif slug == "running-pace":
        return '''<div class="section">
<h2>Running Pace</h2>
<div class="form-row">
<div class="form-group">
<label>Distance</label>
<input type="number" id="distance" placeholder="e.g. 5" min="0.1" step="0.1" value="5">
</div>
<div class="form-group">
<label>Unit</label>
<select id="distUnit"><option value="km">Kilometers (km)</option><option value="mile">Miles (mi)</option></select>
</div>
</div>
<div class="form-row">
<div class="form-group">
<label>Time (HH:MM:SS)</label>
<input type="text" id="timeInput" placeholder="e.g. 00:25:00" value="00:25:00">
</div>
</div>
<div class="btn-group">
<button class="btn btn-primary" id="calcBtn">Calculate Pace</button>
</div>
<div class="result-box" id="resultBox">
<div class="result-item"><span class="result-label">Pace per km</span><span class="result-value" id="paceKm"></span></div>
<div class="result-item"><span class="result-label">Pace per mile</span><span class="result-value" id="paceMile"></span></div>
<div class="result-item"><span class="result-label">Speed</span><span class="result-value" id="speedKph"></span></div>
<div class="result-item"><span class="result-label">5K Prediction</span><span class="result-value" id="predict5k"></span></div>
<div class="result-item"><span class="result-label">Half Marathon Prediction</span><span class="result-value" id="predictHalf"></span></div>
<div class="result-item"><span class="result-label">Marathon Prediction</span><span class="result-value" id="predictFull"></span></div>
</div>
</div>'''
    
    elif slug == "paragraph-counter":
        return '''<div class="section">
<h2>Paragraph Statistics</h2>
<div class="form-group">
<label>Enter Text</label>
<textarea id="textInput" placeholder="Paste or type your text here..."></textarea>
</div>
<div class="result-box show" id="resultBox">
<div class="result-item"><span class="result-label">Total Paragraphs</span><span class="result-value" id="paraCount">0</span></div>
<div class="result-item"><span class="result-label">Total Words</span><span class="result-value" id="wordCount">0</span></div>
<div class="result-item"><span class="result-label">Total Characters</span><span class="result-value" id="charCount">0</span></div>
<div class="result-item"><span class="result-label">Avg Words per Paragraph</span><span class="result-value" id="avgWordsPerPara">0</span></div>
<div class="result-item"><span class="result-label">Longest Paragraph</span><span class="result-value" id="maxWordsPerPara">0</span></div>
<div class="result-item"><span class="result-label">Shortest Paragraph</span><span class="result-value" id="minWordsPerPara">0</span></div>
</div>
</div>'''
    
    elif slug == "vowel-counter":
        return '''<div class="section">
<h2>Vowel Statistics</h2>
<div class="form-group">
<label>Enter Text</label>
<textarea id="textInput" placeholder="Paste or type your English text here..."></textarea>
</div>
<div class="result-box show" id="resultBox">
<div class="result-item"><span class="result-label">Total Characters</span><span class="result-value" id="totalChars">0</span></div>
<div class="result-item"><span class="result-label">Total Vowels</span><span class="result-value" id="totalVowels">0</span></div>
<div class="result-item"><span class="result-label">Vowel Ratio</span><span class="result-value" id="vowelRatio">0%</span></div>
<div class="result-item"><span class="result-label">A Count</span><span class="result-value" id="countA">0</span></div>
<div class="result-item"><span class="result-label">E Count</span><span class="result-value" id="countE">0</span></div>
<div class="result-item"><span class="result-label">I Count</span><span class="result-value" id="countI">0</span></div>
<div class="result-item"><span class="result-label">O Count</span><span class="result-value" id="countO">0</span></div>
<div class="result-item"><span class="result-label">U Count</span><span class="result-value" id="countU">0</span></div>
</div>
</div>'''
    
    elif slug == "keyword-density":
        return '''<div class="section">
<h2>Keyword Density Analysis</h2>
<div class="form-group">
<label>Enter Text</label>
<textarea id="textInput" placeholder="Paste the text to analyze..." rows="8"></textarea>
</div>
<div class="form-group">
<label>Keywords (comma separated)</label>
<input type="text" id="keywordInput" placeholder="e.g. SEO, keyword, analysis">
</div>
<div class="btn-group">
<button class="btn btn-primary" id="analyzeBtn">Analyze</button>
<button class="btn btn-secondary" id="clearBtn">Clear</button>
</div>
<div class="result-box" id="resultBox">
<div class="result-item"><span class="result-label">Total Words</span><span class="result-value" id="totalWords">-</span></div>
<div id="keywordResults"></div>
</div>
</div>'''

# English scripts are same as Chinese (just different UI labels in HTML)
# We reuse the same JS for both

# ===== Generate all files =====
for tool in TOOLS:
    slug = tool["slug"]
    
    # Chinese version
    cn_dir = os.path.join(BASE, slug)
    os.makedirs(cn_dir, exist_ok=True)
    cn_content = get_tool_content_cn(tool)
    cn_script = get_tool_script_cn(tool)
    cn_page = make_cn_page(tool)
    cn_page = cn_page.replace("<!-- TOOL_CONTENT_PLACEHOLDER_CN -->", cn_content)
    cn_page = cn_page.replace("<!-- TOOL_SCRIPT_PLACEHOLDER_CN -->", cn_script)
    
    cn_path = os.path.join(cn_dir, "index.html")
    with open(cn_path, "w", encoding="utf-8") as f:
        f.write(cn_page)
    print(f"✅ Created: {slug}/index.html")
    
    # English version
    en_dir = os.path.join(BASE, "en", slug)
    os.makedirs(en_dir, exist_ok=True)
    en_content = get_tool_content_en(tool)
    en_script = cn_script  # Same JS
    en_page = make_en_page(tool)
    en_page = en_page.replace("<!-- TOOL_CONTENT_PLACEHOLDER_EN -->", en_content)
    en_page = en_page.replace("<!-- TOOL_SCRIPT_PLACEHOLDER_EN -->", en_script)
    
    en_path = os.path.join(en_dir, "index.html")
    with open(en_path, "w", encoding="utf-8") as f:
        f.write(en_page)
    print(f"✅ Created: en/{slug}/index.html")

print("\n=== All 10 tools created (CN + EN) ===")
print(f"Total: {len(TOOLS)*2} files")