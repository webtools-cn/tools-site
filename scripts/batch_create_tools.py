#!/usr/bin/env python3
"""批量创建新工具页面 - 第1批：10个工具"""
import os

BASE = "/home/chison/tools-site"

# 10个工具的元数据
tools = [
    {
        "dir": "file-compare",
        "cn_name": "文件对比工具",
        "en_name": "File Compare",
        "cn_desc": "免费在线文件内容对比工具。对比两个文件的文本内容差异，高亮显示新增、删除和修改行。支持拖拽上传和粘贴文本。",
        "en_desc": "Free online file content comparison tool. Compare text differences between two files, highlight added, deleted and modified lines. Support drag & drop upload and paste.",
        "keywords": "文件对比,文件比较,diff,文本对比,在线对比",
        "category": "developer",
        "icon": "📄",
        "template": "file-compare"
    },
    {
        "dir": "image-compare",
        "cn_name": "图片对比工具",
        "en_name": "Image Compare",
        "cn_desc": "免费在线图片对比工具。并排对比两张图片，支持滑动对比、叠层对比，轻松发现图片间的差异。",
        "en_desc": "Free online image comparison tool. Compare two images side by side with slider and overlay modes, easily spot differences between images.",
        "keywords": "图片对比,图片比较,图像对比,在线对比,图片差异",
        "category": "image",
        "icon": "🖼️",
        "template": "image-compare"
    },
    {
        "dir": "base32-encode",
        "cn_name": "Base32编码工具",
        "en_name": "Base32 Encoder",
        "cn_desc": "免费在线Base32编码工具。将文本字符串编码为Base32格式，支持RFC 4648标准编码。",
        "en_desc": "Free online Base32 encoding tool. Encode text strings to Base32 format, supporting RFC 4648 standard encoding.",
        "keywords": "Base32编码,Base32,编码工具,在线编码,base32 encode",
        "category": "developer",
        "icon": "🔢",
        "template": "base32-encode"
    },
    {
        "dir": "base32-decode",
        "cn_name": "Base32解码工具",
        "en_name": "Base32 Decoder",
        "cn_desc": "免费在线Base32解码工具。将Base32编码的字符串解码为原始文本，支持RFC 4648标准。",
        "en_desc": "Free online Base32 decoding tool. Decode Base32 encoded strings back to original text, supporting RFC 4648 standard.",
        "keywords": "Base32解码,Base32,解码工具,在线解码,base32 decode",
        "category": "developer",
        "icon": "🔢",
        "template": "base32-decode"
    },
    {
        "dir": "unicode-analyzer",
        "cn_name": "Unicode字符分析工具",
        "en_name": "Unicode Analyzer",
        "cn_desc": "免费在线Unicode字符分析工具。输入任意字符查看其Unicode编码、码点、UTF-8/UTF-16编码、HTML实体和字符名称。",
        "en_desc": "Free online Unicode character analyzer. Input any character to view its Unicode code point, UTF-8/UTF-16 encoding, HTML entity and character name.",
        "keywords": "Unicode分析,Unicode,字符分析,码点,UTF编码",
        "category": "developer",
        "icon": "🔤",
        "template": "unicode-analyzer"
    },
    {
        "dir": "utf8-converter",
        "cn_name": "UTF-8编码转换工具",
        "en_name": "UTF-8 Converter",
        "cn_desc": "免费在线UTF-8编码转换工具。在文本与UTF-8十六进制字节之间互相转换，支持查看每个字符的UTF-8编码字节序列。",
        "en_desc": "Free online UTF-8 encoding converter. Convert between text and UTF-8 hex bytes, view the UTF-8 byte sequence for each character.",
        "keywords": "UTF-8,UTF8,编码转换,UTF-8转换,字符编码",
        "category": "developer",
        "icon": "🔤",
        "template": "utf8-converter"
    },
    {
        "dir": "password-strength",
        "cn_name": "密码强度检测工具",
        "en_name": "Password Strength Checker",
        "cn_desc": "免费在线密码强度检测工具。分析密码长度、字符类型和复杂度，评估密码强度等级，检测常见弱密码模式。",
        "en_desc": "Free online password strength checker. Analyze password length, character types and complexity, evaluate strength level, detect common weak password patterns.",
        "keywords": "密码强度,密码检测,密码安全,密码测试,密码评估",
        "category": "security",
        "icon": "🔐",
        "template": "password-strength"
    },
    {
        "dir": "sha1-hash",
        "cn_name": "SHA-1哈希生成器",
        "en_name": "SHA-1 Hash Generator",
        "cn_desc": "免费在线SHA-1哈希生成器。使用Web Crypto API计算文本的SHA-1哈希值，支持十六进制输出。",
        "en_desc": "Free online SHA-1 hash generator. Calculate SHA-1 hash of text using Web Crypto API, with hex output support.",
        "keywords": "SHA-1,SHA1,哈希,hash,加密,sha1生成器",
        "category": "security",
        "icon": "🔐",
        "template": "sha1-hash"
    },
    {
        "dir": "semver-checker",
        "cn_name": "语义版本比较工具",
        "en_name": "Semantic Version Checker",
        "cn_desc": "免费在线语义化版本比较工具。验证semver格式，比较两个版本号大小，检查版本是否符合semver规范。",
        "en_desc": "Free online semantic version comparison tool. Validate semver format, compare two version numbers, check if versions comply with semver specification.",
        "keywords": "语义版本,semver,版本比较,版本号,版本管理",
        "category": "developer",
        "icon": "🏷️",
        "template": "semver-checker"
    },
    {
        "dir": "query-string-parser",
        "cn_name": "URL查询字符串解析工具",
        "en_name": "Query String Parser",
        "cn_desc": "免费在线URL查询字符串解析工具。解析URL中的查询参数，支持编码解码，可视化展示参数键值对。",
        "en_desc": "Free online URL query string parser. Parse query parameters from URLs, support encoding/decoding, visually display parameter key-value pairs.",
        "keywords": "URL解析,查询字符串,query string,参数解析,URL参数",
        "category": "developer",
        "icon": "🔗",
        "template": "query-string-parser"
    },
]

def make_page(tool):
    """生成中文工具页面"""
    d = tool
    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-9W1157EBQV"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-9W1157EBQV');</script>
<script>window.addEventListener("error",function(e){{if(e&&e.message===""){{e.preventDefault();}}}});window.addEventListener("unhandledrejection",function(e){{if(e&&e.reason&&e.reason.message===""){{e.preventDefault();}}}});</script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="{d['cn_desc']}">
<meta name="keywords" content="{d['keywords']}">
<title>{d['cn_name']} - Free ToolBase</title>
<link rel="canonical" href="https://free-toolbase.com/{d['dir']}/">
<meta property="og:title" content="{d['cn_name']} - Free ToolBase">
<meta property="og:description" content="{d['cn_desc']}">
<meta property="og:url" content="https://free-toolbase.com/{d['dir']}/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Free ToolBase">
<link rel="alternate" hreflang="zh" href="https://free-toolbase.com/{d['dir']}/">
<link rel="alternate" hreflang="en" href="https://free-toolbase.com/en/{d['dir']}/">
<link rel="alternate" hreflang="x-default" href="https://free-toolbase.com/en/{d['dir']}/">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"SoftwareApplication","name":"{d['cn_name']}","description":"{d['cn_desc']}","applicationCategory":"UtilitiesApplication","operatingSystem":"Web","publisher":{{"@type":"Organization","name":"Free ToolBase","email":"dexshuang@google.com"}},"offers":{{"@type":"Offer","price":"0","priceCurrency":"USD"}}}}</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{{"@type":"Question","name":"这个工具免费吗？","acceptedAnswer":{{"@type":"Answer","text":"完全免费，无需注册，无需下载。所有功能在浏览器本地运行，数据不会上传到任何服务器。"}}}},{{"@type":"Question","name":"数据会经过服务器吗？","acceptedAnswer":{{"@type":"Answer","text":"不会。本工具是纯前端应用，所有操作都在您的浏览器中本地完成，数据绝不离开您的设备。"}}}}]}}</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"HowTo","name":"如何使用{d['cn_name']}","description":"如何使用{d['cn_name']}的详细步骤指南","totalTime":"PT2M","tool":{{"@type":"HowToTool","name":"{d['cn_name']}"}},"step":[{{"@type":"HowToStep","position":1,"name":"输入内容","text":"输入或粘贴需要处理的文本/数据"}},{{"@type":"HowToStep","position":2,"name":"点击处理","text":"点击处理按钮执行操作"}},{{"@type":"HowToStep","position":3,"name":"查看结果","text":"查看处理后的结果"}},{{"@type":"HowToStep","position":4,"name":"复制或下载","text":"一键复制结果或下载为文件"}}]}}</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"首页","item":"https://free-toolbase.com/"}},{{"@type":"ListItem","position":2,"name":"工具","item":"https://free-toolbase.com/#tools"}},{{"@type":"ListItem","position":3,"name":"{d['cn_name']}","item":"https://free-toolbase.com/{d['dir']}/"}}]}}</script>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#0f172a;color:#e2e8f0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,"PingFang SC","Microsoft YaHei",sans-serif;line-height:1.6;min-height:100vh}}
a{{color:#06b6d4;text-decoration:none}}
.container{{max-width:900px;margin:0 auto;padding:24px 16px}}
.header{{display:flex;justify-content:space-between;align-items:center;margin-bottom:24px;flex-wrap:wrap;gap:8px}}
.header h1{{font-size:1.6rem;color:#f1f5f9}}
.lang-switch{{display:flex;gap:4px;background:#1e293b;border-radius:8px;padding:4px;border:1px solid rgba(148,163,184,.1)}}
.lang-switch a{{padding:6px 12px;border-radius:5px;font-size:.85rem;color:#94a3b8}}
.lang-switch a.active{{background:rgba(6,182,212,.2);color:#22d3ee}}
.nav-back{{color:#64748b;font-size:.85rem;margin-bottom:16px}}
.nav-back a{{color:#64748b}}
.hero{{text-align:center;margin-bottom:20px}}
.hero p{{color:#94a3b8;font-size:.95rem;margin-bottom:8px}}
.badge{{display:inline-block;padding:2px 10px;border-radius:12px;background:rgba(34,197,94,.1);color:#4ade80;font-size:.75rem;border:1px solid rgba(34,197,94,.2)}}
.input-section{{background:#1e293b;border-radius:12px;padding:20px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1)}}
.input-section h2{{font-size:1.1rem;color:#f1f5f9;margin-bottom:12px}}
label{{display:block;color:#94a3b8;font-size:.85rem;margin-bottom:4px}}
textarea{{width:100%;padding:10px 12px;background:#0f172a;color:#e2e8f0;border:1px solid rgba(148,163,184,.2);border-radius:8px;font-size:.9rem;font-family:inherit;resize:vertical;min-height:100px;margin-bottom:12px}}
textarea:focus,input:focus{{outline:none;border-color:rgba(6,182,212,.5)}}
input[type=text],input[type=number],input[type=url]{{width:100%;padding:10px 12px;background:#0f172a;color:#e2e8f0;border:1px solid rgba(148,163,184,.2);border-radius:8px;font-size:.9rem;margin-bottom:12px}}
select{{width:100%;padding:10px 12px;background:#0f172a;color:#e2e8f0;border:1px solid rgba(148,163,184,.2);border-radius:8px;font-size:.9rem;margin-bottom:12px}}
select:focus{{outline:none;border-color:rgba(6,182,212,.5)}}
.options{{display:flex;gap:12px;align-items:center;margin:12px 0;flex-wrap:wrap}}
.options label{{display:flex;align-items:center;gap:6px;font-size:.85rem;color:#94a3b8;cursor:pointer;margin-bottom:0}}
.options input[type=checkbox],.options input[type=radio]{{accent-color:#06b6d4}}
.row{{display:flex;gap:12px;flex-wrap:wrap}}
.row .field{{flex:1;min-width:140px}}
.btn-row{{display:flex;gap:8px;flex-wrap:wrap;margin-top:12px}}
.btn{{padding:8px 20px;border:none;border-radius:6px;font-size:.85rem;cursor:pointer;transition:all .2s}}
.btn-primary{{background:rgba(6,182,212,.2);color:#22d3ee;border:1px solid rgba(6,182,212,.3)}}
.btn-primary:hover{{background:rgba(6,182,212,.3)}}
.btn-secondary{{background:rgba(148,163,184,.1);color:#94a3b8;border:1px solid rgba(148,163,184,.2)}}
.btn-secondary:hover{{background:rgba(148,163,184,.2)}}
.btn-success{{background:rgba(34,197,94,.15);color:#4ade80;border:1px solid rgba(34,197,94,.2)}}
.btn-success:hover{{background:rgba(34,197,94,.25)}}
.btn-danger{{background:rgba(239,68,68,.15);color:#f87171;border:1px solid rgba(239,68,68,.2)}}
.result-section{{background:#1e293b;border-radius:12px;padding:20px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1);display:none}}
.result-section.show{{display:block}}
.result-section h2{{font-size:1.1rem;color:#f1f5f9;margin-bottom:12px}}
.result-box{{background:#0f172a;border-radius:8px;padding:12px;margin:8px 0;border:1px solid rgba(148,163,184,.08);overflow-x:auto;white-space:pre-wrap;word-break:break-all;font-family:monospace;font-size:.85rem}}
.info-section{{background:#1e293b;border-radius:12px;padding:20px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1)}}
.info-section h2{{font-size:1.1rem;color:#f1f5f9;margin-bottom:12px}}
.info-section p{{color:#94a3b8;font-size:.9rem;margin-bottom:8px}}
.strength-bar{{height:8px;border-radius:4px;background:rgba(148,163,184,.1);margin:8px 0;overflow:hidden}}
.strength-fill{{height:100%;border-radius:4px;transition:width .3s,background .3s}}
.strength-0{{background:#ef4444}}
.strength-1{{background:#f97316}}
.strength-2{{background:#eab308}}
.strength-3{{background:#22c55e}}
.strength-4{{background:#06b6d4}}
.checks{{display:grid;grid-template-columns:1fr 1fr;gap:4px;margin:8px 0;font-size:.85rem}}
.check-item{{display:flex;align-items:center;gap:6px}}
.check-pass{{color:#4ade80}}
.check-fail{{color:#f87171}}
.slider-container{{position:relative;overflow:hidden;margin:8px 0;border-radius:8px;border:1px solid rgba(148,163,184,.1)}}
.slider-container img{{width:100%;display:block}}
.slider-overlay{{position:absolute;top:0;left:0;width:50%;height:100%;overflow:hidden;border-right:3px solid #06b6d4}}
.slider-overlay img{{position:absolute;top:0;left:0;width:auto;min-width:100%;height:100%;object-fit:cover}}
.slider-handle{{position:absolute;top:50%;transform:translate(-50%,-50%);width:36px;height:36px;background:#06b6d4;border-radius:50%;cursor:ew-resize;display:flex;align-items:center;justify-content:center;color:#fff;font-size:14px;z-index:10;box-shadow:0 0 8px rgba(0,0,0,.5)}}
.footer{{border-top:1px solid rgba(148,163,184,.1);padding:24px 0;margin-top:32px;text-align:center;color:#64748b;font-size:.85rem}}
.footer a{{color:#64748b;margin:0 8px}}
.footer a:hover{{color:#94a3b8}}
.faq-item{{margin-bottom:16px}}
.faq-item h3{{font-size:.95rem;color:#f1f5f9;margin-bottom:6px}}
.faq-item p{{color:#94a3b8;font-size:.85rem}}
@media(max-width:600px){{.row{{flex-direction:column}}.checks{{grid-template-columns:1fr}}.header h1{{font-size:1.2rem}}}}
</style>
</head>
<body>
<div class="container">
<div class="header"><h1>{d['icon']} {d['cn_name']}</h1><div class="lang-switch"><a href="index.html" class="active">中文</a><a href="../en/{d['dir']}/">EN</a></div></div>
<p class="nav-back"><a href="../index.html">首页</a> › <a href="../index.html#tools">工具</a> › {d['cn_name']}</p>
<div class="hero"><p>{d['cn_desc']}</p><span class="badge">零依赖 · 可离线使用</span></div>
<div id="app"></div>
<div class="info-section"><h2>使用说明</h2><p>{d['cn_desc']}</p><p>数据在浏览器本地处理，不会上传到任何服务器，确保您的数据安全。</p></div>
<div class="faq-item"><h3>这个工具免费吗？</h3><p>完全免费，无需注册，无需下载。所有功能在浏览器本地运行，数据不会上传到任何服务器。</p></div>
<div class="faq-item"><h3>数据会经过服务器吗？</h3><p>不会。本工具是纯前端应用，所有操作都在您的浏览器中本地完成，数据绝不离开您的设备。</p></div>
</div>
<div class="footer container">
<div style="margin-bottom:12px">
<a href="../index.html">首页</a>
<a href="../index.html">全部工具</a>
<a href="mailto:dexshuang@google.com">联系我们</a>
<a href="../privacy/">隐私政策</a>
<a href="../terms/">服务条款</a>
<a href="../about/">关于我们</a>
<a href="../en/{d['dir']}/">EN</a>
</div>
<p>{d['cn_name']} | 无需注册 · 数据绝不上传服务器</p>
<p style="margin-top:8px;color:#475569;font-size:.8rem">问题反馈: dexshuang@google.com</p>
</div>
<div class="toast" id="toast" style="position:fixed;bottom:20px;left:50%;transform:translateX(-50%);background:#1e293b;color:#e2e8f0;padding:10px 24px;border-radius:8px;font-size:.85rem;z-index:999;opacity:0;transition:opacity .3s;pointer-events:none"></div>
<script>
function showToast(m){{var t=document.getElementById("toast");t.textContent=m;t.style.opacity="1";setTimeout(function(){{t.style.opacity="0"}},3000)}}
function copyText(el){{var t=el.textContent||el.innerText;navigator.clipboard.writeText(t).then(function(){{showToast("已复制 ✓")}})["catch"](function(){{showToast("复制失败")}})}}
</script>
</body>
</html>'''

def make_en_page(tool):
    """生成英文工具页面"""
    d = tool
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-9W1157EBQV"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-9W1157EBQV');</script>
<script>window.addEventListener("error",function(e){{if(e&&e.message===""){{e.preventDefault();}}}});window.addEventListener("unhandledrejection",function(e){{if(e&&e.reason&&e.reason.message===""){{e.preventDefault();}}}});</script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="{d['en_desc']}">
<meta name="keywords" content="{d['keywords']}">
<title>{d['en_name']} - Free ToolBase</title>
<link rel="canonical" href="https://free-toolbase.com/en/{d['dir']}/">
<meta property="og:title" content="{d['en_name']} - Free ToolBase">
<meta property="og:description" content="{d['en_desc']}">
<meta property="og:url" content="https://free-toolbase.com/en/{d['dir']}/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Free ToolBase">
<link rel="alternate" hreflang="en" href="https://free-toolbase.com/en/{d['dir']}/">
<link rel="alternate" hreflang="zh" href="https://free-toolbase.com/{d['dir']}/">
<link rel="alternate" hreflang="x-default" href="https://free-toolbase.com/en/{d['dir']}/">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"SoftwareApplication","name":"{d['en_name']}","description":"{d['en_desc']}","applicationCategory":"UtilitiesApplication","operatingSystem":"Web","publisher":{{"@type":"Organization","name":"Free ToolBase","email":"dexshuang@google.com"}},"offers":{{"@type":"Offer","price":"0","priceCurrency":"USD"}}}}</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{{"@type":"Question","name":"Is this tool free?","acceptedAnswer":{{"@type":"Answer","text":"Yes, completely free. No registration, no download required. All functions run locally in your browser, data never leaves your device."}}}},{{"@type":"Question","name":"Does data go through a server?","acceptedAnswer":{{"@type":"Answer","text":"No. This is a pure client-side application. All operations happen locally in your browser. Your data never leaves your device."}}}}]}}</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"HowTo","name":"How to use {d['en_name']}","description":"Step-by-step guide for using {d['en_name']}","totalTime":"PT2M","tool":{{"@type":"HowToTool","name":"{d['en_name']}"}},"step":[{{"@type":"HowToStep","position":1,"name":"Enter content","text":"Input or paste the text/data to process"}},{{"@type":"HowToStep","position":2,"name":"Click process","text":"Click the process button to execute"}},{{"@type":"HowToStep","position":3,"name":"View result","text":"View the processed result"}},{{"@type":"HowToStep","position":4,"name":"Copy or download","text":"One-click copy result or download as file"}}]}}</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"Home","item":"https://free-toolbase.com/en/"}},{{"@type":"ListItem","position":2,"name":"Tools","item":"https://free-toolbase.com/en/#tools"}},{{"@type":"ListItem","position":3,"name":"{d['en_name']}","item":"https://free-toolbase.com/en/{d['dir']}/"}}]}}</script>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#0f172a;color:#e2e8f0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;line-height:1.6;min-height:100vh}}
a{{color:#06b6d4;text-decoration:none}}
.container{{max-width:900px;margin:0 auto;padding:24px 16px}}
.header{{display:flex;justify-content:space-between;align-items:center;margin-bottom:24px;flex-wrap:wrap;gap:8px}}
.header h1{{font-size:1.6rem;color:#f1f5f9}}
.lang-switch{{display:flex;gap:4px;background:#1e293b;border-radius:8px;padding:4px;border:1px solid rgba(148,163,184,.1)}}
.lang-switch a{{padding:6px 12px;border-radius:5px;font-size:.85rem;color:#94a3b8}}
.lang-switch a.active{{background:rgba(6,182,212,.2);color:#22d3ee}}
.nav-back{{color:#64748b;font-size:.85rem;margin-bottom:16px}}
.nav-back a{{color:#64748b}}
.hero{{text-align:center;margin-bottom:20px}}
.hero p{{color:#94a3b8;font-size:.95rem;margin-bottom:8px}}
.badge{{display:inline-block;padding:2px 10px;border-radius:12px;background:rgba(34,197,94,.1);color:#4ade80;font-size:.75rem;border:1px solid rgba(34,197,94,.2)}}
.input-section{{background:#1e293b;border-radius:12px;padding:20px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1)}}
.input-section h2{{font-size:1.1rem;color:#f1f5f9;margin-bottom:12px}}
label{{display:block;color:#94a3b8;font-size:.85rem;margin-bottom:4px}}
textarea{{width:100%;padding:10px 12px;background:#0f172a;color:#e2e8f0;border:1px solid rgba(148,163,184,.2);border-radius:8px;font-size:.9rem;font-family:inherit;resize:vertical;min-height:100px;margin-bottom:12px}}
textarea:focus,input:focus{{outline:none;border-color:rgba(6,182,212,.5)}}
input[type=text],input[type=number],input[type=url]{{width:100%;padding:10px 12px;background:#0f172a;color:#e2e8f0;border:1px solid rgba(148,163,184,.2);border-radius:8px;font-size:.9rem;margin-bottom:12px}}
select{{width:100%;padding:10px 12px;background:#0f172a;color:#e2e8f0;border:1px solid rgba(148,163,184,.2);border-radius:8px;font-size:.9rem;margin-bottom:12px}}
select:focus{{outline:none;border-color:rgba(6,182,212,.5)}}
.options{{display:flex;gap:12px;align-items:center;margin:12px 0;flex-wrap:wrap}}
.options label{{display:flex;align-items:center;gap:6px;font-size:.85rem;color:#94a3b8;cursor:pointer;margin-bottom:0}}
.options input[type=checkbox],.options input[type=radio]{{accent-color:#06b6d4}}
.row{{display:flex;gap:12px;flex-wrap:wrap}}
.row .field{{flex:1;min-width:140px}}
.btn-row{{display:flex;gap:8px;flex-wrap:wrap;margin-top:12px}}
.btn{{padding:8px 20px;border:none;border-radius:6px;font-size:.85rem;cursor:pointer;transition:all .2s}}
.btn-primary{{background:rgba(6,182,212,.2);color:#22d3ee;border:1px solid rgba(6,182,212,.3)}}
.btn-primary:hover{{background:rgba(6,182,212,.3)}}
.btn-secondary{{background:rgba(148,163,184,.1);color:#94a3b8;border:1px solid rgba(148,163,184,.2)}}
.btn-secondary:hover{{background:rgba(148,163,184,.2)}}
.btn-success{{background:rgba(34,197,94,.15);color:#4ade80;border:1px solid rgba(34,197,94,.2)}}
.btn-success:hover{{background:rgba(34,197,94,.25)}}
.btn-danger{{background:rgba(239,68,68,.15);color:#f87171;border:1px solid rgba(239,68,68,.2)}}
.result-section{{background:#1e293b;border-radius:12px;padding:20px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1);display:none}}
.result-section.show{{display:block}}
.result-section h2{{font-size:1.1rem;color:#f1f5f9;margin-bottom:12px}}
.result-box{{background:#0f172a;border-radius:8px;padding:12px;margin:8px 0;border:1px solid rgba(148,163,184,.08);overflow-x:auto;white-space:pre-wrap;word-break:break-all;font-family:monospace;font-size:.85rem}}
.info-section{{background:#1e293b;border-radius:12px;padding:20px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1)}}
.info-section h2{{font-size:1.1rem;color:#f1f5f9;margin-bottom:12px}}
.info-section p{{color:#94a3b8;font-size:.9rem;margin-bottom:8px}}
.strength-bar{{height:8px;border-radius:4px;background:rgba(148,163,184,.1);margin:8px 0;overflow:hidden}}
.strength-fill{{height:100%;border-radius:4px;transition:width .3s,background .3s}}
.strength-0{{background:#ef4444}}
.strength-1{{background:#f97316}}
.strength-2{{background:#eab308}}
.strength-3{{background:#22c55e}}
.strength-4{{background:#06b6d4}}
.checks{{display:grid;grid-template-columns:1fr 1fr;gap:4px;margin:8px 0;font-size:.85rem}}
.check-item{{display:flex;align-items:center;gap:6px}}
.check-pass{{color:#4ade80}}
.check-fail{{color:#f87171}}
.slider-container{{position:relative;overflow:hidden;margin:8px 0;border-radius:8px;border:1px solid rgba(148,163,184,.1)}}
.slider-container img{{width:100%;display:block}}
.slider-overlay{{position:absolute;top:0;left:0;width:50%;height:100%;overflow:hidden;border-right:3px solid #06b6d4}}
.slider-overlay img{{position:absolute;top:0;left:0;width:auto;min-width:100%;height:100%;object-fit:cover}}
.slider-handle{{position:absolute;top:50%;transform:translate(-50%,-50%);width:36px;height:36px;background:#06b6d4;border-radius:50%;cursor:ew-resize;display:flex;align-items:center;justify-content:center;color:#fff;font-size:14px;z-index:10;box-shadow:0 0 8px rgba(0,0,0,.5)}}
.footer{{border-top:1px solid rgba(148,163,184,.1);padding:24px 0;margin-top:32px;text-align:center;color:#64748b;font-size:.85rem}}
.footer a{{color:#64748b;margin:0 8px}}
.footer a:hover{{color:#94a3b8}}
.faq-item{{margin-bottom:16px}}
.faq-item h3{{font-size:.95rem;color:#f1f5f9;margin-bottom:6px}}
.faq-item p{{color:#94a3b8;font-size:.85rem}}
@media(max-width:600px){{.row{{flex-direction:column}}.checks{{grid-template-columns:1fr}}.header h1{{font-size:1.2rem}}}}
</style>
</head>
<body>
<div class="container">
<div class="header"><h1>{d['icon']} {d['en_name']}</h1><div class="lang-switch"><a href="../{d['dir']}/">中文</a><a href="index.html" class="active">EN</a></div></div>
<p class="nav-back"><a href="../index.html">Home</a> › <a href="../index.html#tools">Tools</a> › {d['en_name']}</p>
<div class="hero"><p>{d['en_desc']}</p><span class="badge">Zero Dependency · Works Offline</span></div>
<div id="app"></div>
<div class="info-section"><h2>How to Use</h2><p>{d['en_desc']}</p><p>All data is processed locally in your browser and never uploaded to any server, ensuring your data security.</p></div>
<div class="faq-item"><h3>Is this tool free?</h3><p>Yes, completely free. No registration, no download required. All functions run locally in your browser, data never leaves your device.</p></div>
<div class="faq-item"><h3>Does data go through a server?</h3><p>No. This is a pure client-side application. All operations happen locally in your browser. Your data never leaves your device.</p></div>
</div>
<div class="footer container">
<div style="margin-bottom:12px">
<a href="../index.html">Home</a>
<a href="../index.html">All Tools</a>
<a href="mailto:dexshuang@google.com">Contact</a>
<a href="../privacy/">Privacy</a>
<a href="../terms/">Terms</a>
<a href="../about/">About</a>
<a href="../{d['dir']}/">中文</a>
</div>
<p>{d['en_name']} | No registration · Data never leaves your device</p>
<p style="margin-top:8px;color:#475569;font-size:.8rem">Feedback: dexshuang@google.com</p>
</div>
<div class="toast" id="toast" style="position:fixed;bottom:20px;left:50%;transform:translateX(-50%);background:#1e293b;color:#e2e8f0;padding:10px 24px;border-radius:8px;font-size:.85rem;z-index:999;opacity:0;transition:opacity .3s;pointer-events:none"></div>
<script>
function showToast(m){{var t=document.getElementById("toast");t.textContent=m;t.style.opacity="1";setTimeout(function(){{t.style.opacity="0"}},3000)}}
function copyText(el){{var t=el.textContent||el.innerText;navigator.clipboard.writeText(t).then(function(){{showToast("Copied! ✓")}})["catch"](function(){{showToast("Copy failed")}})}}
</script>
</body>
</html>'''

# 创建目录和文件
for tool in tools:
    d = tool['dir']
    # 中文版
    os.makedirs(os.path.join(BASE, d), exist_ok=True)
    cn_path = os.path.join(BASE, d, 'index.html')
    cn_content = make_page(tool)
    with open(cn_path, 'w', encoding='utf-8') as f:
        f.write(cn_content)
    print(f"Created: {d}/index.html")
    
    # 英文版
    en_dir = os.path.join(BASE, 'en', d)
    os.makedirs(en_dir, exist_ok=True)
    en_path = os.path.join(BASE, 'en', d, 'index.html')
    en_content = make_en_page(tool)
    with open(en_path, 'w', encoding='utf-8') as f:
        f.write(en_content)
    print(f"Created: en/{d}/index.html")

print(f"\n✅ Created {len(tools)} tools (CN + EN)")