#!/usr/bin/env python3
"""批量生成5个新工具页（中英文双语）"""
import os

tools = {
    "spell-checker": {
        "cn": {
            "title": "在线拼写检查器 - Free ToolBase",
            "desc": "免费在线拼写检查器，支持中英文拼写检测，自动标记错误单词并提供修正建议。无需注册，纯浏览器本地处理。",
            "h1": "拼写检查器",
            "subtitle": "检查文本拼写错误，获取修正建议",
            "keywords": "拼写检查,spell check,拼写纠错,英文拼写检查,在线拼写检查",
            "howto": "输入文本：粘贴或输入需要检查的文本内容。点击检查：工具自动扫描并标记拼写错误。查看建议：点击错误单词查看修正建议列表。"
        },
        "en": {
            "title": "Free Online Spell Checker - Check Spelling Errors | ToolBase",
            "desc": "Free online spell checker for English and Chinese text. Automatically detect spelling errors and get correction suggestions. No signup, browser-based.",
            "h1": "Spell Checker",
            "subtitle": "Check spelling errors and get correction suggestions",
            "keywords": "spell checker,spell check,spelling correction,english spell check,online spell checker",
            "howto": "Enter text: Paste or type the text you want to check. Click Check: The tool scans and highlights spelling errors. View suggestions: Click any highlighted word for correction options."
        }
    },
    "acronym-finder": {
        "cn": {
            "title": "缩写含义查找器 - 在线缩写查询 | Free ToolBase",
            "desc": "免费在线缩写含义查找器，收录500+常见英文缩写全称和中文释义。AI、SEO、API、NASA等缩写一键查询。",
            "h1": "缩写含义查找器",
            "subtitle": "输入缩写，查找完整的英文全称和中文含义",
            "keywords": "缩写查找,acronym,abbreviation,英文缩写含义,缩略词查询,全称查询",
            "howto": "输入缩写：输入你遇到的英文缩写（如AI、NASA、SEO等）。即时搜索：系统实时匹配500+常见缩写词条。查看结果：显示英文全称、中文含义和详细解释。"
        },
        "en": {
            "title": "Acronym Finder - Find Meaning of Abbreviations | ToolBase",
            "desc": "Free online acronym finder with 500+ common abbreviations. Instantly look up meanings of AI, SEO, API, NASA and more. No signup required.",
            "h1": "Acronym Finder",
            "subtitle": "Enter an acronym to find its full meaning and explanation",
            "keywords": "acronym finder,abbreviation meaning,what does it stand for,acronym lookup,abbreviation dictionary",
            "howto": "Enter acronym: Type an abbreviation like AI, NASA, or SEO. Instant search: The tool matches against 500+ common acronyms. View result: See the full form, Chinese translation, and detailed explanation."
        }
    },
    "random-joke": {
        "cn": {
            "title": "随机笑话生成器 - 在线笑话大全 | Free ToolBase",
            "desc": "免费在线随机笑话生成器，收录200+精选中文笑话。支持随机切换、分类浏览、一键复制分享。无需注册，轻松一笑。",
            "h1": "随机笑话生成器",
            "subtitle": "一键生成随机笑话，让你会心一笑",
            "keywords": "笑话,随机笑话,笑话大全,搞笑,段子,开心一刻,幽默",
            "howto": "点击换一个：每次点击随机展示一条笑话。分类过滤：按编程、冷笑话、脑筋急转弯等分类筛选。一键复制：复制笑话文本分享给朋友。"
        },
        "en": {
            "title": "Random Joke Generator - Free Online Jokes | ToolBase",
            "desc": "Free online random joke generator with 200+ curated jokes. Browse categories including programming, dad jokes, puns. Copy and share instantly.",
            "h1": "Random Joke Generator",
            "subtitle": "Get a random joke with one click - laugh out loud",
            "keywords": "joke generator,random joke,funny jokes,dad jokes,programming jokes,pun generator",
            "howto": "Click New Joke: Get a random joke with each click. Filter by category: Choose from programming, dad jokes, puns. Copy & Share: Click to copy the joke text."
        }
    },
    "money-counter": {
        "cn": {
            "title": "数钱计算器 - 人民币/美元/欧元等在线金额计算 | Free ToolBase",
            "desc": "免费在线数钱计算器。输入每种面额纸币和硬币的数量，自动计算总金额。支持人民币、美元、欧元、英镑、日元等多种货币。无需注册。",
            "h1": "数钱计算器",
            "subtitle": "输入每种面额的数量，自动计算总金额",
            "keywords": "数钱计算器,现金计算,金额统计,纸币面额,硬币计算,货币换算",
            "howto": "选择货币：从人民币、美元、欧元等货币中选择。输入数量：填写每种面额纸币和硬币的张数/枚数。查看总计：自动计算显示总金额。"
        },
        "en": {
            "title": "Money Counter Calculator - Count Cash by Denominations | ToolBase",
            "desc": "Free online money counter. Enter quantities of each banknote and coin denomination, automatically calculate total amount. Supports USD, EUR, GBP, CNY, JPY.",
            "h1": "Money Counter",
            "subtitle": "Enter quantities per denomination to calculate total cash amount",
            "keywords": "money counter,cash calculator,count cash,currency denominations,banknote counter,coin calculator",
            "howto": "Select currency: Choose from USD, EUR, GBP, CNY, JPY. Enter quantities: Fill in counts for each bill and coin denomination. View total: See the calculated total amount instantly."
        }
    },
    "indent-formatter": {
        "cn": {
            "title": "代码缩进格式化工具 - 在线调整缩进 | Free ToolBase",
            "desc": "免费在线代码缩进格式化工具。支持调整代码缩进大小，在Tab和空格之间转换。支持JavaScript、Python、HTML、CSS、JSON等多种语言。纯前端处理。",
            "h1": "代码缩进格式化工具",
            "subtitle": "调整代码缩进，在Tab和空格之间自由转换",
            "keywords": "代码缩进,indent,格式化,tab替换空格,空格转tab,代码排版",
            "howto": "粘贴代码：将需要调整缩进的代码粘贴到输入框。选择设置：设置缩进大小（2/4/8空格或Tab）。点击格式化：自动调整缩进并美化代码排版。"
        },
        "en": {
            "title": "Code Indent Formatter - Adjust Indentation Online | ToolBase",
            "desc": "Free online code indent formatter. Adjust indentation size, convert between tabs and spaces. Supports JavaScript, Python, HTML, CSS, JSON and more.",
            "h1": "Code Indent Formatter",
            "subtitle": "Adjust code indentation - convert between tabs and spaces",
            "keywords": "indent formatter,code indentation,tab to spaces,spaces to tab,format code,beautify code",
            "howto": "Paste code: Paste your code into the input area. Choose settings: Set indent size (2/4/8 spaces or tab). Click Format: Auto-adjust indentation and beautify code layout."
        }
    }
}

BASE = os.path.expanduser("~/tools-site")

GA_TAG = """<script async src="https://www.googletagmanager.com/gtag/js?id=G-9W1157EBQV"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','G-9W1157EBQV');</script>"""

for slug, tool in tools.items():
    for lang, meta in [("cn", tool["cn"]), ("en", tool["en"])]:
        dir_path = os.path.join(BASE, slug) if lang == "cn" else os.path.join(BASE, "en", slug)
        os.makedirs(dir_path, exist_ok=True)
        
        # 确定多语言路径
        en_url = f"https://free-toolbase.com/en/{slug}/"
        cn_url = f"https://free-toolbase.com/{slug}/"
        
        if lang == "cn":
            html_lang = "zh-CN"
            page_url = cn_url
            alt_url = en_url
            alt_lang = "en"
        else:
            html_lang = "en"
            page_url = en_url
            alt_url = cn_url
            alt_lang = "zh-CN"
        
        html = f'''<!DOCTYPE html>
<html lang="{html_lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{meta["title"]}</title>
<meta name="description" content="{meta["desc"]}">
<meta name="keywords" content="{meta["keywords"]}">
<link rel="canonical" href="{page_url}">
<link rel="alternate" hreflang="{alt_lang}" href="{alt_url}">
<meta property="og:title" content="{meta["title"]}">
<meta property="og:description" content="{meta["desc"]}">
<meta property="og:url" content="{page_url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Free ToolBase">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{meta["title"]}">
<meta name="twitter:description" content="{meta["desc"]}">
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "WebApplication",
  "name": "{meta["h1"]}",
  "url": "{page_url}",
  "description": "{meta["desc"]}",
  "applicationCategory": "UtilityApplication",
  "operatingSystem": "Any",
  "offers": {{"@type": "Offer", "price": "0", "priceCurrency": "USD"}}
}}
</script>
{GA_TAG}
<style>
:root {{ --primary: #4F46E5; --primary-hover: #4338CA; --bg: #f8fafc; --card-bg: #ffffff; --text: #1e293b; --text-secondary: #64748b; --border: #e2e8f0; --radius: 12px; --shadow: 0 1px 3px rgba(0,0,0,.1), 0 1px 2px rgba(0,0,0,.06); }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: var(--bg); color: var(--text); line-height: 1.6; min-height: 100vh; }}
header {{ background: #fff; border-bottom: 1px solid var(--border); padding: 16px 20px; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 8px; }}
header a {{ text-decoration: none; color: inherit; }}
.logo {{ font-size: 1.25rem; font-weight: 700; color: var(--primary); }}
.nav {{ display: flex; gap: 12px; align-items: center; }}
.nav a {{ font-size: .875rem; color: var(--text-secondary); padding: 4px 8px; border-radius: 6px; }}
.nav a:hover {{ color: var(--primary); background: #f1f5f9; }}
main {{ max-width: 800px; margin: 0 auto; padding: 24px 16px 60px; }}
h1 {{ font-size: 1.75rem; font-weight: 700; margin-bottom: 8px; }}
.subtitle {{ color: var(--text-secondary); font-size: .95rem; margin-bottom: 24px; }}
.card {{ background: var(--card-bg); border-radius: var(--radius); box-shadow: var(--shadow); padding: 24px; margin-bottom: 20px; border: 1px solid var(--border); }}
.card h2 {{ font-size: 1.1rem; margin-bottom: 12px; }}
textarea, input[type="text"], select {{ width: 100%; padding: 12px; border: 1px solid var(--border); border-radius: 8px; font-size: .9rem; font-family: monospace; resize: vertical; }}
textarea:focus, input:focus, select:focus {{ outline: none; border-color: var(--primary); box-shadow: 0 0 0 3px rgba(79,70,229,.1); }}
.btn {{ display: inline-block; padding: 10px 20px; background: var(--primary); color: #fff; border: none; border-radius: 8px; font-size: .9rem; cursor: pointer; font-weight: 500; }}
.btn:hover {{ background: var(--primary-hover); }}
.btn-secondary {{ background: #f1f5f9; color: var(--text); }}
.btn-secondary:hover {{ background: #e2e8f0; }}
.output {{ background: #f8fafc; border: 1px solid var(--border); border-radius: 8px; padding: 16px; min-height: 60px; font-size: .9rem; white-space: pre-wrap; word-break: break-all; margin-top: 12px; }}
.result-item {{ padding: 8px 12px; border-bottom: 1px solid var(--border); display: flex; justify-content: space-between; align-items: center; }}
.result-item:last-child {{ border-bottom: none; }}
.count {{ font-weight: 600; color: var(--primary); font-size: 1.5rem; }}
footer {{ text-align: center; padding: 24px; color: var(--text-secondary); font-size: .85rem; border-top: 1px solid var(--border); background: #fff; }}
footer a {{ color: var(--primary); text-decoration: none; }}
.how-to {{ margin-top: 32px; }}
.how-to h3 {{ font-size: 1.1rem; margin-bottom: 12px; }}
.how-to ol {{ padding-left: 20px; color: var(--text-secondary); }}
.how-to ol li {{ margin-bottom: 6px; }}
.toast {{ position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%); background: #1e293b; color: #fff; padding: 12px 24px; border-radius: 8px; font-size: .85rem; opacity: 0; transition: opacity .3s; z-index: 999; }}
.toast.show {{ opacity: 1; }}
@media (max-width: 640px) {{ h1 {{ font-size: 1.4rem; }} .card {{ padding: 16px; }} }}
</style>
</head>
<body>
<header>
  <a href="{("/" if lang=="cn" else "/en/")}" class="logo">🔧 Free ToolBase</a>
  <nav class="nav">
    <a href="{("/" if lang=="cn" else "/en/")}">{"首页" if lang=="cn" else "Home"}</a>
    <a href="{("/" + slug + "/")}" hreflang="zh-CN">中文</a>
    <a href="{"/en/" + slug + "/"}">English</a>
  </nav>
</header>
<main>
  <h1>{meta["h1"]}</h1>
  <p class="subtitle">{meta["subtitle"]}</p>
  <div class="card" id="app-card">
    <!-- JS动态生成内容 -->
  </div>
  <div class="how-to">
    <h3>{"📖 如何使用" if lang=="cn" else "📖 How to Use"}</h3>
    <ol>
{chr(10).join(f'      <li>{item}</li>' for item in meta["howto"].split("。") if item.strip())}
    </ol>
  </div>
</main>
<footer>
  <p>&copy; 2025 Free ToolBase · {"所有工具均免费使用，无需注册" if lang=="cn" else "All tools are free to use, no signup required"}</p>
  <p style="margin-top:4px"><a href="{("/privacy/" if lang=="cn" else "/en/privacy/")}">{"隐私政策" if lang=="cn" else "Privacy Policy"}</a> · <a href="{("/terms/" if lang=="cn" else "/en/terms/")}">{"服务条款" if lang=="cn" else "Terms of Service"}</a></p>
</footer>
<div class="toast" id="toast"></div>
<script>
(function() {{
  'use strict';
}}());
</script>
</body>
</html>'''
        fpath = os.path.join(dir_path, "index.html")
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(html.strip() + "\n")
        print(f"✅ {fpath}")

print("\nDone! 5 tools x 2 languages = 10 files")