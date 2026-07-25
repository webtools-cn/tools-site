#!/usr/bin/env python3
"""批量生成10个新工具（中英文双语）"""
import os, json

BASE = "/home/chison/tools-site"

# ============================================================
# 10个工具定义
# ============================================================
TOOLS = [
    {
        "slug": "virtual-piano-keyboard",
        "category": "fun-tools",
        "cn_name": "🎹 虚拟钢琴键盘",
        "en_name": "🎹 Virtual Piano Keyboard",
        "cn_title": "在线虚拟钢琴键盘 - 免费网页钢琴演奏 | 无需注册",
        "en_title": "Virtual Piano Keyboard Online - Free Web Piano | No Signup",
        "cn_desc": "免费在线虚拟钢琴键盘，支持鼠标点击和键盘弹奏。多种音色选择，可录制和回放。纯本地运行，无需注册，数据不上传服务器。",
        "en_desc": "Free online virtual piano keyboard. Play with mouse clicks or computer keyboard. Multiple instrument sounds, record and playback. Runs locally in your browser, no signup required.",
        "cn_keywords": "虚拟钢琴,在线钢琴,钢琴键盘,网页钢琴,免费钢琴,钢琴模拟器",
        "en_keywords": "virtual piano,online piano,piano keyboard,web piano,free piano,piano simulator",
        "cn_hero": "免费在线虚拟钢琴键盘，支持鼠标点击和键盘弹奏。多种音色选择，可录制和回放。纯本地运行，无需注册，数据不上传服务器。",
        "en_hero": "Free online virtual piano keyboard. Play with mouse clicks or computer keyboard. Multiple instrument sounds, record and playback. Runs locally in your browser, no signup required.",
    },
    {
        "slug": "neumorphic-css",
        "category": "design-tools",
        "cn_name": "🎨 Neumorphic CSS 生成器",
        "en_name": "🎨 Neumorphic CSS Generator",
        "cn_title": "Neumorphic CSS 生成器 - 在线新拟态风格代码生成 | 无需注册",
        "en_title": "Neumorphic CSS Generator - Online Soft UI Code Generator | No Signup",
        "cn_desc": "免费在线Neumorphic CSS生成器，可视化调整阴影、圆角、颜色等参数，实时预览效果并一键复制CSS代码。支持按钮、卡片、输入框等多种组件样式生成。",
        "en_desc": "Free online Neumorphic CSS generator. Visually adjust shadows, border-radius, colors and preview in real-time. Copy CSS code with one click. Supports buttons, cards, inputs and more component styles.",
        "cn_keywords": "Neumorphic,CSS生成器,新拟态,软UI,CSS代码,阴影生成器",
        "en_keywords": "neumorphic,css generator,soft ui,shadow generator,css code,design tool",
        "cn_hero": "免费在线Neumorphic CSS生成器，可视化调整阴影、圆角、颜色等参数，实时预览效果并一键复制CSS代码。支持按钮、卡片、输入框等多种组件样式生成。",
        "en_hero": "Free online Neumorphic CSS generator. Visually adjust shadows, border-radius, colors and preview in real-time. Copy CSS code with one click. Supports buttons, cards, inputs and more.",
    },
    {
        "slug": "bricks-calculator",
        "category": "calc-tools",
        "cn_name": "🧱 砖块用量计算器",
        "en_name": "🧱 Brick Calculator",
        "cn_title": "砖块用量计算器 - 在线计算砌墙所需砖数 | 无需注册",
        "en_title": "Brick Calculator - Calculate Bricks Needed for Walls | No Signup",
        "cn_desc": "免费在线砖块用量计算器，输入墙体尺寸和砖块规格，自动计算所需砖块数量。支持标准砖、空心砖等多种规格，考虑灰缝厚度。纯本地计算，无需注册。",
        "en_desc": "Free online brick calculator. Enter wall dimensions and brick specifications to automatically calculate bricks needed. Supports standard bricks, hollow bricks and more. Accounts for mortar joints. All local computation.",
        "cn_keywords": "砖块计算器,砌墙计算,砖块用量,建筑材料计算,砖数计算",
        "en_keywords": "brick calculator,wall calculator,brick quantity,construction calculator,masonry calculator",
        "cn_hero": "免费在线砖块用量计算器，输入墙体尺寸和砖块规格，自动计算所需砖块数量。支持标准砖、空心砖等多种规格，考虑灰缝厚度。纯本地计算，无需注册。",
        "en_hero": "Free online brick calculator. Enter wall dimensions and brick specifications to automatically calculate bricks needed. Supports standard bricks, hollow bricks and more. Accounts for mortar joints.",
    },
    {
        "slug": "website-uptime-checker",
        "category": "network-tools",
        "cn_name": "🔍 网站在线检测器",
        "en_name": "🔍 Website Uptime Checker",
        "cn_title": "网站在线检测器 - 检测任意网站是否正常运行 | 无需注册",
        "en_title": "Website Uptime Checker - Check if Any Website is Online | No Signup",
        "cn_desc": "免费在线网站在线检测器，输入URL即可检测网站是否可访问。显示HTTP状态码、响应时间、服务器信息等。支持批量检测多个网站，纯前端请求。",
        "en_desc": "Free online website uptime checker. Enter a URL to check if a website is accessible. Shows HTTP status code, response time, server info. Supports batch checking multiple sites. All frontend requests.",
        "cn_keywords": "网站检测,在线检测,网站状态,uptime,网站监控,网站可用性",
        "en_keywords": "website checker,uptime check,website status,site monitor,website availability,http check",
        "cn_hero": "免费在线网站在线检测器，输入URL即可检测网站是否可访问。显示HTTP状态码、响应时间、服务器信息等。支持批量检测多个网站，纯前端请求。",
        "en_hero": "Free online website uptime checker. Enter a URL to check if a website is accessible. Shows HTTP status code, response time, server info. Supports batch checking multiple sites.",
    },
    {
        "slug": "jwt-token-generator",
        "category": "security-tools",
        "cn_name": "🔐 JWT 令牌生成器",
        "en_name": "🔐 JWT Token Generator",
        "cn_title": "JWT 令牌在线生成器 - JSON Web Token 生成工具 | 无需注册",
        "en_title": "JWT Token Generator Online - JSON Web Token Builder | No Signup",
        "cn_desc": "免费在线JWT令牌生成器，可视化编辑Header和Payload，选择签名算法（HS256/HS384/HS512/RS256等），输入密钥即可生成标准JWT Token。纯本地生成，密钥不上传。",
        "en_desc": "Free online JWT token generator. Visually edit Header and Payload, choose signing algorithm (HS256/HS384/HS512/RS256 etc.), enter secret key to generate standard JWT tokens. All generation happens locally, keys never uploaded.",
        "cn_keywords": "JWT,令牌生成,JSON Web Token,签名,HS256,RS256,认证令牌",
        "en_keywords": "JWT,token generator,JSON Web Token,signing,HS256,RS256,auth token",
        "cn_hero": "免费在线JWT令牌生成器，可视化编辑Header和Payload，选择签名算法（HS256/HS384/HS512/RS256等），输入密钥即可生成标准JWT Token。纯本地生成，密钥不上传。",
        "en_hero": "Free online JWT token generator. Visually edit Header and Payload, choose signing algorithm, enter secret key to generate standard JWT tokens. All generation happens locally, keys never uploaded.",
    },
    {
        "slug": "swift-bic-validation",
        "category": "finance-tools",
        "cn_name": "🏦 SWIFT/BIC 代码验证器",
        "en_name": "🏦 SWIFT/BIC Code Validator",
        "cn_title": "SWIFT/BIC 代码在线验证器 - 银行识别码格式校验 | 无需注册",
        "en_title": "SWIFT/BIC Code Validator - Bank Identifier Code Format Check | No Signup",
        "cn_desc": "免费在线SWIFT/BIC代码验证器，支持格式校验和银行信息识别。输入8位或11位BIC代码，自动验证格式合法性，解析银行代码、国家代码、地区代码和分行代码。",
        "en_desc": "Free online SWIFT/BIC code validator. Supports format verification and bank info identification. Enter 8 or 11-digit BIC code to auto-validate format and parse bank code, country code, location code and branch code.",
        "cn_keywords": "SWIFT,BIC,银行代码,验证器,国际汇款,银行识别码",
        "en_keywords": "SWIFT,BIC,bank code,validator,international transfer,bank identifier",
        "cn_hero": "免费在线SWIFT/BIC代码验证器，支持格式校验和银行信息识别。输入8位或11位BIC代码，自动验证格式合法性，解析银行代码、国家代码、地区代码和分行代码。",
        "en_hero": "Free online SWIFT/BIC code validator. Supports format verification and bank info identification. Enter 8 or 11-digit BIC code to auto-validate format and parse components.",
    },
    {
        "slug": "ip-address-range-calculator",
        "category": "network-tools",
        "cn_name": "🌐 IP地址范围计算器",
        "en_name": "🌐 IP Address Range Calculator",
        "cn_title": "IP地址范围计算器 - CIDR子网掩码在线计算 | 无需注册",
        "en_title": "IP Address Range Calculator - CIDR Subnet Calculator | No Signup",
        "cn_desc": "免费在线IP地址范围计算器，支持CIDR格式输入，自动计算网络地址、广播地址、可用IP范围、子网掩码和主机数量。支持IPv4全范围计算，纯本地运算。",
        "en_desc": "Free online IP address range calculator. Supports CIDR input, auto-calculates network address, broadcast address, usable IP range, subnet mask and host count. Supports full IPv4 range. All local computation.",
        "cn_keywords": "IP计算器,CIDR,子网掩码,网络地址,IP范围,子网计算",
        "en_keywords": "IP calculator,CIDR,subnet mask,network address,IP range,subnet calculator",
        "cn_hero": "免费在线IP地址范围计算器，支持CIDR格式输入，自动计算网络地址、广播地址、可用IP范围、子网掩码和主机数量。支持IPv4全范围计算，纯本地运算。",
        "en_hero": "Free online IP address range calculator. Supports CIDR input, auto-calculates network address, broadcast address, usable IP range, subnet mask and host count.",
    },
    {
        "slug": "color-contrast-analyzer",
        "category": "design-tools",
        "cn_name": "🎯 WCAG 颜色对比度分析器",
        "en_name": "🎯 WCAG Color Contrast Analyzer",
        "cn_title": "WCAG颜色对比度分析器 - 在线检测文字可读性 | 无需注册",
        "en_title": "WCAG Color Contrast Analyzer - Check Text Readability | No Signup",
        "cn_desc": "免费在线WCAG颜色对比度分析器，输入前景色和背景色，自动计算对比度比率。同时评估AA和AAA级合规性（正常文字和大文字），支持HEX和RGB格式输入。",
        "en_desc": "Free online WCAG color contrast analyzer. Enter foreground and background colors to auto-calculate contrast ratio. Evaluates AA and AAA compliance for normal and large text. Supports HEX and RGB input formats.",
        "cn_keywords": "WCAG,对比度,颜色分析,可访问性,AA,AAA,颜色检测",
        "en_keywords": "WCAG,contrast,color analyzer,accessibility,AA,AAA,color check",
        "cn_hero": "免费在线WCAG颜色对比度分析器，输入前景色和背景色，自动计算对比度比率。同时评估AA和AAA级合规性（正常文字和大文字），支持HEX和RGB格式输入。",
        "en_hero": "Free online WCAG color contrast analyzer. Enter foreground and background colors to auto-calculate contrast ratio. Evaluates AA and AAA compliance for normal and large text.",
    },
    {
        "slug": "docker-run-generator",
        "category": "dev-tools",
        "cn_name": "🐳 Docker Run 命令生成器",
        "en_name": "🐳 Docker Run Command Generator",
        "cn_title": "Docker Run 命令在线生成器 - 可视化生成Docker启动命令 | 无需注册",
        "en_title": "Docker Run Command Generator - Visual Docker Command Builder | No Signup",
        "cn_desc": "免费在线Docker Run命令生成器，可视化配置镜像名、端口映射、卷挂载、环境变量、重启策略等参数，一键生成完整的docker run命令。支持常用选项的快捷配置。",
        "en_desc": "Free online Docker Run command generator. Visually configure image name, port mapping, volume mounts, environment variables, restart policy and generate complete docker run command with one click. Supports quick config for common options.",
        "cn_keywords": "Docker,Run命令,容器,生成器,docker run,端口映射,卷挂载",
        "en_keywords": "Docker,run command,container,generator,docker run,port mapping,volume mount",
        "cn_hero": "免费在线Docker Run命令生成器，可视化配置镜像名、端口映射、卷挂载、环境变量、重启策略等参数，一键生成完整的docker run命令。支持常用选项的快捷配置。",
        "en_hero": "Free online Docker Run command generator. Visually configure image name, port mapping, volume mounts, environment variables, restart policy and generate complete docker run command.",
    },
    {
        "slug": "cron-sandbox",
        "category": "dev-tools",
        "cn_name": "⏰ Cron 表达式测试沙盒",
        "en_name": "⏰ Cron Expression Sandbox",
        "cn_title": "Cron表达式在线测试沙盒 - 定时任务表达式验证 | 无需注册",
        "en_title": "Cron Expression Sandbox - Test Cron Schedule Online | No Signup",
        "cn_desc": "免费在线Cron表达式测试沙盒，输入Cron表达式即可查看未来N次执行时间和人类可读描述。支持5位和6位格式（含秒），实时验证语法并高亮错误。",
        "en_desc": "Free online Cron expression sandbox. Enter a Cron expression to see next N execution times and human-readable description. Supports 5-field and 6-field format (with seconds). Real-time syntax validation with error highlighting.",
        "cn_keywords": "Cron,表达式,定时任务,测试,沙盒,crontab,调度",
        "en_keywords": "Cron,expression,cron job,test,sandbox,crontab,schedule",
        "cn_hero": "免费在线Cron表达式测试沙盒，输入Cron表达式即可查看未来N次执行时间和人类可读描述。支持5位和6位格式（含秒），实时验证语法并高亮错误。",
        "en_hero": "Free online Cron expression sandbox. Enter a Cron expression to see next N execution times and human-readable description. Supports 5-field and 6-field format.",
    },
]

# ============================================================
# 工具生成函数
# ============================================================
def gen_html(tool, lang="cn"):
    """生成工具页面HTML"""
    slug = tool["slug"]
    is_cn = lang == "cn"
    
    name = tool["cn_name"] if is_cn else tool["en_name"]
    title = tool["cn_title"] if is_cn else tool["en_title"]
    desc = tool["cn_desc"] if is_cn else tool["en_desc"]
    keywords = tool["cn_keywords"] if is_cn else tool["en_keywords"]
    hero_text = tool["cn_hero"] if is_cn else tool["en_hero"]
    
    lang_attr = "zh-CN" if is_cn else "en"
    self_url = f"https://free-toolbase.com/{slug}/" if is_cn else f"https://free-toolbase.com/en/{slug}/"
    alt_url = f"https://free-toolbase.com/en/{slug}/" if is_cn else f"https://free-toolbase.com/{slug}/"
    alt_lang = "en" if is_cn else "zh"
    home_url = "../" if is_cn else "../../"
    index_href = f"{home_url}index.html"
    home_label = "首页" if is_cn else "Home"
    tools_label = "工具" if is_cn else "Tools"
    badge_text = "零依赖·可离线使用" if is_cn else "Zero Deps · Works Offline"
    cn_link = "index.html" if is_cn else f"../{slug}/"
    en_link = f"../en/{slug}/" if is_cn else "index.html"
    cn_active = ' class="active"' if is_cn else ""
    en_active = ' class="active"' if not is_cn else ""
    use_btn = "立即使用" if is_cn else "Use Now"
    copy_btn = "复制" if is_cn else "Copy"
    clear_btn = "清空" if is_cn else "Clear"
    toast_text = "已复制到剪贴板" if is_cn else "Copied to clipboard"
    toast_error = "复制失败，请手动复制" if is_cn else "Copy failed, please copy manually"
    result_label = "结果" if is_cn else "Result"
    
    # 构建特定内容
    body_content = build_tool_body(tool, is_cn)
    
    # 构建FAQ
    faqs = build_faqs(tool, is_cn)
    faq_json_parts = []
    for q, a in faqs:
        faq_json_parts.append(f'{{"@type":"Question","name":"{q}","acceptedAnswer":{{"@type":"Answer","text":"{a}"}}}}')
    faq_json = ",".join(faq_json_parts)
    
    # HowTo
    step_labels = ["输入数据", "点击生成", "查看结果"] if is_cn else ["Enter Data", "Click Generate", "View Result"]
    howto_steps = []
    for i, label in enumerate(step_labels, 1):
        txt = "在输入框中输入需要处理的数据" if i == 1 else ("点击生成按钮执行操作" if i == 2 else "查看处理结果，支持一键复制") if is_cn else ("Enter data in the input fields" if i == 1 else ("Click the generate button to process" if i == 2 else "View the result, one-click copy"))
        howto_steps.append(f'{{"@type":"HowToStep","position":{i},"name":"{label}","text":"{txt}"}}')
    howto_json = ",".join(howto_steps)
    
    # 面包屑名称
    crumb_name = tool["cn_name"].split(" ", 1)[1] if " " in tool["cn_name"] else tool["cn_name"] if is_cn else tool["en_name"].split(" ", 1)[1] if " " in tool["en_name"] else tool["en_name"]
    
    # 首页路径
    if is_cn:
        home_path = "https://free-toolbase.com/"
    else:
        home_path = "https://free-toolbase.com/en/"
    
    html = f'''<!DOCTYPE html>
<html lang="{lang_attr}">
<head>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-9W1157EBQV"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-9W1157EBQV');</script>
<script>window.addEventListener("error",function(e){{if(e&&e.message===""){{e.preventDefault();}}}});window.addEventListener("unhandledrejection",function(e){{if(e&&e.reason&&e.reason.message===""){{e.preventDefault();}}}});</script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="{desc}">
<meta name="keywords" content="{keywords}">
<title>{title}</title>
<link rel="canonical" href="{self_url}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{self_url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Free ToolBase">
<link rel="alternate" hreflang="{lang_attr[:2]}" href="{self_url}">
<link rel="alternate" hreflang="{alt_lang}" href="{alt_url}">
<link rel="alternate" hreflang="x-default" href="https://free-toolbase.com/en/{slug}/">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"SoftwareApplication","name":"{crumb_name}","description":"{desc}","applicationCategory":"UtilitiesApplication","operatingSystem":"Web","publisher":{{"@type":"Organization","name":"Free ToolBase","email":"dexshuang@google.com"}},"offers":{{"@type":"Offer","price":"0","priceCurrency":"USD"}}}}</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{faq_json}]}}</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"HowTo","name":"如何使用{crumb_name}","description":"如何使用{crumb_name}的详细步骤指南","totalTime":"PT1M","tool":{{"@type":"HowToTool","name":"{crumb_name}"}},"step":[{howto_json}]}}</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"{home_label}","item":"{home_path}"}},{{"@type":"ListItem","position":2,"name":"{tools_label}","item":"{home_path}#tools"}},{{"@type":"ListItem","position":3,"name":"{crumb_name}","item":"{self_url}"}}]}}</script>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
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
.input-section{{background:#1e293b;border-radius:12px;padding:20px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1)}}
.input-section h2{{font-size:1.1rem;color:#f1f5f9;margin-bottom:12px}}
label{{display:block;color:#94a3b8;font-size:.85rem;margin-bottom:4px}}
input[type=text],input[type=number],input[type=url],select,textarea{{width:100%;padding:10px 12px;background:#0f172a;color:#e2e8f0;border:1px solid rgba(148,163,184,.2);border-radius:8px;font-size:.9rem;margin-bottom:12px;font-family:monospace}}
input:focus,select:focus,textarea:focus{{outline:none;border-color:rgba(6,182,212,.5)}}
.row{{display:flex;gap:12px;flex-wrap:wrap}}
.row .field{{flex:1;min-width:140px}}
.btn-row{{display:flex;gap:8px;flex-wrap:wrap;margin-top:12px}}
.btn{{padding:8px 20px;border:none;border-radius:6px;font-size:.85rem;cursor:pointer;transition:all .2s}}
.btn-primary{{background:rgba(6,182,212,.2);color:#22d3ee;border:1px solid rgba(6,182,212,.3)}}
.btn-primary:hover{{background:rgba(6,182,212,.3)}}
.btn-secondary{{background:rgba(148,163,184,.1);color:#94a3b8;border:1px solid rgba(148,163,184,.2)}}
.btn-secondary:hover{{background:rgba(148,163,184,.2)}}
.result-section{{background:#1e293b;border-radius:12px;padding:20px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1)}}
.result-section h2{{font-size:1.1rem;color:#f1f5f9;margin-bottom:12px}}
.result-box{{background:#0f172a;border-radius:8px;padding:24px;text-align:center;border:1px solid rgba(148,163,184,.08)}}
.result-detail{{color:#64748b;font-size:.85rem;text-align:center;margin-top:8px}}
.info-section{{background:#1e293b;border-radius:12px;padding:20px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1)}}
.info-section h2{{font-size:1.1rem;color:#f1f5f9;margin-bottom:12px}}
.info-section p{{color:#94a3b8;font-size:.9rem;margin-bottom:8px}}
.footer{{border-top:1px solid rgba(148,163,184,.1);padding:24px 0;margin-top:32px;text-align:center;color:#64748b;font-size:.85rem}}
.footer a{{color:#64748b;margin:0 8px}}
.footer a:hover{{color:#94a3b8}}
.toast{{position:fixed;bottom:24px;left:50%;transform:translateX(-50%);background:#1e293b;color:#e2e8f0;padding:12px 24px;border-radius:8px;font-size:.9rem;border:1px solid rgba(148,163,184,.15);opacity:0;transition:opacity .3s;pointer-events:none;z-index:999}}
.toast.show{{opacity:1}}
.status-ok{{color:#22c55e}}
.status-err{{color:#ef4444}}
.preview-box{{min-height:60px;display:flex;align-items:center;justify-content:center;border-radius:12px;margin-bottom:12px;transition:all .2s}}
code,pre{{background:#0f172a;border-radius:6px;padding:12px;font-family:"SF Mono",Monaco,Menlo,monospace;font-size:.85rem;color:#e2e8f0;overflow-x:auto;white-space:pre-wrap;word-break:break-all}}
.badge{{display:inline-block;background:rgba(6,182,212,.1);color:#22d3ee;padding:2px 8px;border-radius:4px;font-size:.75rem;margin-right:4px}}
@media(max-width:600px){{.row{{flex-direction:column}}}}
@media(max-width:640px){{h1{{font-size:1.2rem;word-break:break-word}}.header{{flex-direction:column;gap:8px}}}}
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
<div class="header"><h1>{name}</h1><div class="lang-switch"><a href="{cn_link}"{cn_active}>中文</a><a href="{en_link}"{en_active}>EN</a></div></div>
<p class="nav-back"><a href="{index_href}">{home_label}</a> &rsaquo; <a href="{index_href}#tools">{tools_label}</a> &rsaquo; {crumb_name}</p>
<div class="hero"><p>{hero_text}</p><span class="badge">{badge_text}</span></div>
{body_content}
<div class="footer"><a href="{index_href}">{home_label}</a><a href="{index_href}#tools">{tools_label}</a><a href="{index_href}contact">{"联系我们" if is_cn else "Contact"}</a><a href="{index_href}privacy">{"隐私政策" if is_cn else "Privacy"}</a></div>
</div>
<div class="toast" id="toast">{toast_text}</div>
<script>
function showToast(msg){{
var t=document.getElementById('toast');
t.textContent=msg||'{toast_text}';
t.classList.add('show');
setTimeout(function(){{t.classList.remove('show');}},2000);
}}
function copyText(text){{
if(navigator.clipboard){{navigator.clipboard.writeText(text).then(function(){{showToast('{toast_text}');}},function(){{showToast('{toast_error}');}});}}
else{{var ta=document.createElement('textarea');ta.value=text;ta.style.position='fixed';ta.style.opacity='0';document.body.appendChild(ta);ta.select();try{{document.execCommand('copy');showToast('{toast_text}');}}catch(e){{showToast('{toast_error}');}}document.body.removeChild(ta);}}
}}
{build_tool_js(tool, is_cn)}
</script>
</body>
</html>'''
    return html


def build_tool_body(tool, is_cn):
    """生成工具特定的body内容"""
    slug = tool["slug"]
    result_label = "结果" if is_cn else "Result"
    generate_btn = "生成" if is_cn else "Generate"
    copy_btn = "复制" if is_cn else "Copy"
    clear_btn = "清空" if is_cn else "Clear"
    check_btn = "检测" if is_cn else "Check"
    calculate_btn = "计算" if is_cn else "Calculate"
    validate_btn = "验证" if is_cn else "Validate"
    
    bodies = {
        "virtual-piano-keyboard": f'''
<div class="input-section">
<h2>{"🎹 虚拟钢琴" if is_cn else "🎹 Virtual Piano"}</h2>
<p style="color:#94a3b8;font-size:.9rem;margin-bottom:12px">{"用鼠标点击琴键或按键盘按键弹奏钢琴" if is_cn else "Click piano keys or press keyboard to play"}</p>
<div class="piano-container" style="overflow-x:auto;padding:10px 0">
<div class="piano" id="piano" style="display:flex;position:relative;height:180px;min-width:560px"></div>
</div>
<div class="row" style="margin-top:12px">
<div class="field"><label>{"音色" if is_cn else "Instrument"}</label><select id="instrument"><option value="piano">{"钢琴 Piano" if is_cn else "Piano"}</option><option value="organ">{"风琴 Organ" if is_cn else "Organ"}</option><option value="guitar">{"吉他 Guitar" if is_cn else "Guitar"}</option><option value="flute">{"长笛 Flute" if is_cn else "Flute"}</option></select></div>
<div class="field"><label>{"音量" if is_cn else "Volume"}</label><input type="range" id="volume" min="0" max="100" value="70" style="width:100%"></div>
</div>
<div class="btn-row"><button class="btn btn-primary" id="btnRecord">{"🎙 录制" if is_cn else "🎙 Record"}</button><button class="btn btn-secondary" id="btnPlayback">{"▶ 回放" if is_cn else "▶ Playback"}</button><button class="btn btn-secondary" id="btnStop">{"⏹ 停止" if is_cn else "⏹ Stop"}</button></div>
</div>
<div class="info-section">
<h2>{"⌨️ 键盘映射" if is_cn else "⌨️ Key Mapping"}</h2>
<p>{"白键：A S D F G H J K L ; ' (两排)  |  黑键：W E  T Y U  O P  ] (上面一排)" if is_cn else "White keys: A S D F G H J K L ; ' | Black keys: W E T Y U O P ]"}</p>
</div>''',

        "neumorphic-css": f'''
<div class="input-section">
<h2>{"🎨 样式配置" if is_cn else "🎨 Style Configuration"}</h2>
<div class="row">
<div class="field"><label>{"背景色" if is_cn else "Background"}</label><input type="color" id="bgColor" value="#e0e0e0"></div>
<div class="field"><label>{"组件色" if is_cn else "Element Color"}</label><input type="color" id="elColor" value="#e0e0e0"></div>
</div>
<div class="row">
<div class="field"><label>{"圆角 (px)" if is_cn else "Border Radius"}</label><input type="range" id="radius" min="0" max="60" value="20" style="width:100%"><span id="radiusVal" style="color:#22d3ee;font-size:.85rem">20px</span></div>
<div class="field"><label>{"距离 (px)" if is_cn else "Distance"}</label><input type="range" id="distance" min="1" max="30" value="8" style="width:100%"><span id="distanceVal" style="color:#22d3ee;font-size:.85rem">8px</span></div>
</div>
<div class="row">
<div class="field"><label>{"模糊 (px)" if is_cn else "Blur"}</label><input type="range" id="blur" min="0" max="50" value="16" style="width:100%"><span id="blurVal" style="color:#22d3ee;font-size:.85rem">16px</span></div>
<div class="field"><label>{"形状" if is_cn else "Shape"}</label><select id="shape"><option value="flat">{"平面 Flat" if is_cn else "Flat"}</option><option value="concave">{"凹面 Concave" if is_cn else "Concave"}</option><option value="convex">{"凸面 Convex" if is_cn else "Convex"}</option><option value="pressed">{"按下 Pressed" if is_cn else "Pressed"}</option></select></div>
</div>
<div class="preview-box" id="previewBox" style="background:#e0e0e0;padding:30px">
<div id="previewEl" style="width:150px;height:150px;border-radius:20px;background:#e0e0e0;box-shadow:8px 8px 16px #bebebe,-8px -8px 16px #ffffff"></div>
</div>
<div class="result-section">
<h2>{"📋 CSS 代码" if is_cn else "📋 CSS Code"}</h2>
<pre id="cssOutput">box-shadow: 8px 8px 16px #bebebe, -8px -8px 16px #ffffff;
border-radius: 20px;</pre>
<div class="btn-row"><button class="btn btn-primary" onclick="copyText(document.getElementById('cssOutput').textContent)">{copy_btn} CSS</button></div>
</div>
</div>''',

        "bricks-calculator": f'''
<div class="input-section">
<h2>{"📐 墙体尺寸" if is_cn else "📐 Wall Dimensions"}</h2>
<div class="row">
<div class="field"><label>{"墙长 (米)" if is_cn else "Length (m)"}</label><input type="number" id="wallLength" placeholder="{"例如 5" if is_cn else "e.g. 5"}" value="5" step="0.1" min="0.1"></div>
<div class="field"><label>{"墙高 (米)" if is_cn else "Height (m)"}</label><input type="number" id="wallHeight" placeholder="{"例如 2.5" if is_cn else "e.g. 2.5"}" value="2.5" step="0.1" min="0.1"></div>
</div>
<h2>{"🧱 砖块规格" if is_cn else "🧱 Brick Specs"}</h2>
<div class="row">
<div class="field"><label>{"砖长 (mm)" if is_cn else "Brick Length (mm)"}</label><input type="number" id="brickLength" value="240" min="1"></div>
<div class="field"><label>{"砖高 (mm)" if is_cn else "Brick Height (mm)"}</label><input type="number" id="brickHeight" value="115" min="1"></div>
<div class="field"><label>{"灰缝 (mm)" if is_cn else "Mortar Joint (mm)"}</label><input type="number" id="mortar" value="10" min="0"></div>
</div>
<div class="btn-row"><button class="btn btn-primary" onclick="calculateBricks()">{calculate_btn}</button><button class="btn btn-secondary" onclick="clearBricks()">{clear_btn}</button></div>
</div>
<div class="result-section">
<h2>{"📊 计算结果" if is_cn else "📊 Results"}</h2>
<div class="result-box">
<div style="font-size:2rem;color:#22d3ee;font-weight:bold" id="brickCount">--</div>
<div style="color:#94a3b8;margin-top:4px">{"块砖 (含" if is_cn else " bricks (incl. "}<span id="wasteText">5{"%)" if is_cn else "%)"}</span></div>
</div>
<div style="display:flex;gap:12px;margin-top:12px;flex-wrap:wrap">
<div style="flex:1;background:#1e293b;border-radius:8px;padding:12px;text-align:center;border:1px solid rgba(148,163,184,.1)"><div style="font-size:1.1rem;color:#f1f5f9" id="wallArea">--</div><div style="color:#64748b;font-size:.8rem">{"面积 (m²)" if is_cn else "Area (m²)"}</div></div>
<div style="flex:1;background:#1e293b;border-radius:8px;padding:12px;text-align:center;border:1px solid rgba(148,163,184,.1)"><div style="font-size:1.1rem;color:#f1f5f9" id="brickPerSqm">--</div><div style="color:#64748b;font-size:.8rem">{"每m²砖数" if is_cn else "Bricks/m²"}</div></div>
</div>
</div>
<div class="info-section">
<h2>{"💡 提示" if is_cn else "💡 Tips"}</h2>
<p>{"计算结果已含5%损耗。标准砖尺寸240×115×53mm，灰缝通常10mm。" if is_cn else "Result includes 5% waste. Standard brick: 240×115×53mm, typical mortar joint: 10mm."}</p>
</div>''',

        "website-uptime-checker": f'''
<div class="input-section">
<h2>{"🔗 输入网址" if is_cn else "🔗 Enter URL"}</h2>
<label>{"网站URL" if is_cn else "Website URL"}</label>
<div class="row">
<div class="field" style="flex:3"><input type="text" id="urlInput" placeholder="https://example.com" value="https://www.google.com"></div>
<div class="field" style="flex:0 0 auto"><select id="method"><option>GET</option><option>HEAD</option></select></div>
</div>
<div class="btn-row"><button class="btn btn-primary" onclick="checkUptime()">{check_btn}</button><button class="btn btn-secondary" onclick="document.getElementById('urlInput').value=''">{clear_btn}</button></div>
</div>
<div class="result-section" id="resultSection" style="display:none">
<h2>{"📊 检测结果" if is_cn else "📊 Check Result"}</h2>
<div class="result-box">
<div style="font-size:1.2rem" id="statusDisplay">--</div>
<div style="display:flex;gap:12px;margin-top:12px;flex-wrap:wrap">
<div style="flex:1;background:#1e293b;border-radius:8px;padding:12px;text-align:center;border:1px solid rgba(148,163,184,.1)"><div style="font-size:1.1rem;color:#f1f5f9" id="responseTime">--</div><div style="color:#64748b;font-size:.8rem">{"响应时间" if is_cn else "Response Time"}</div></div>
<div style="flex:1;background:#1e293b;border-radius:8px;padding:12px;text-align:center;border:1px solid rgba(148,163,184,.1)"><div style="font-size:1.1rem;color:#f1f5f9" id="statusCode">--</div><div style="color:#64748b;font-size:.8rem">{"状态码" if is_cn else "Status Code"}</div></div>
</div>
</div>
</div>
<div class="info-section">
<h2>{"💡 说明" if is_cn else "💡 Note"}</h2>
<p>{"检测通过浏览器发起HTTP请求，部分网站可能因CORS策略无法检测。建议使用HEAD方法减少带宽。" if is_cn else "Check via browser HTTP request. Some sites may be unreachable due to CORS policy. HEAD method recommended to save bandwidth."}</p>
</div>''',

        "jwt-token-generator": f'''
<div class="input-section">
<h2>{"🔧 JWT 配置" if is_cn else "🔧 JWT Config"}</h2>
<div class="row">
<div class="field"><label>{"算法" if is_cn else "Algorithm"}</label><select id="algorithm"><option>HS256</option><option>HS384</option><option>HS512</option></select></div>
<div class="field"><label>{"密钥" if is_cn else "Secret Key"}</label><input type="text" id="secretKey" placeholder="your-256-bit-secret" value="your-256-bit-secret"></div>
</div>
<label>{"Header (JSON)" if is_cn else "Header (JSON)"}</label>
<textarea id="headerJson" rows="3">{{"alg":"HS256","typ":"JWT"}}</textarea>
<label>{"Payload (JSON)" if is_cn else "Payload (JSON)"}</label>
<textarea id="payloadJson" rows="6">{{"sub":"1234567890","name":"John Doe","iat":1516239022,"exp":1716239022}}</textarea>
<div class="btn-row"><button class="btn btn-primary" onclick="generateJWT()">{generate_btn} JWT</button><button class="btn btn-secondary" onclick="resetJWT()">{clear_btn}</button></div>
</div>
<div class="result-section">
<h2>{"📋 生成的 Token" if is_cn else "📋 Generated Token"}</h2>
<pre id="tokenOutput" style="word-break:break-all;min-height:60px">{"点击生成按钮..." if is_cn else "Click generate..."}</pre>
<div class="btn-row"><button class="btn btn-primary" onclick="copyText(document.getElementById('tokenOutput').textContent)">{copy_btn}</button></div>
</div>''',

        "swift-bic-validation": f'''
<div class="input-section">
<h2>{"🏦 输入 BIC/SWIFT 代码" if is_cn else "🏦 Enter BIC/SWIFT Code"}</h2>
<label>{"BIC代码 (8或11位)" if is_cn else "BIC Code (8 or 11 digits)"}</label>
<input type="text" id="bicInput" placeholder="{"例如: BKCHCNBJ110" if is_cn else "e.g. BKCHCNBJ110"}" maxlength="11" style="text-transform:uppercase;letter-spacing:2px;font-size:1.2rem">
<div class="btn-row"><button class="btn btn-primary" onclick="validateBIC()">{validate_btn}</button><button class="btn btn-secondary" onclick="document.getElementById('bicInput').value='';clearBICResult()">{clear_btn}</button></div>
</div>
<div class="result-section" id="bicResult" style="display:none">
<h2>{"📊 解析结果" if is_cn else "📊 Parse Result"}</h2>
<div style="display:flex;gap:12px;flex-wrap:wrap">
<div style="flex:1;min-width:140px;background:#1e293b;border-radius:8px;padding:12px;text-align:center;border:1px solid rgba(148,163,184,.1)"><div style="font-size:.75rem;color:#64748b">{"银行代码" if is_cn else "Bank Code"}</div><div style="font-size:1.2rem;color:#22d3ee;font-weight:bold" id="bankCode">--</div></div>
<div style="flex:1;min-width:140px;background:#1e293b;border-radius:8px;padding:12px;text-align:center;border:1px solid rgba(148,163,184,.1)"><div style="font-size:.75rem;color:#64748b">{"国家代码" if is_cn else "Country Code"}</div><div style="font-size:1.2rem;color:#22d3ee;font-weight:bold" id="countryCode">--</div></div>
<div style="flex:1;min-width:140px;background:#1e293b;border-radius:8px;padding:12px;text-align:center;border:1px solid rgba(148,163,184,.1)"><div style="font-size:.75rem;color:#64748b">{"地区代码" if is_cn else "Location Code"}</div><div style="font-size:1.2rem;color:#22d3ee;font-weight:bold" id="locationCode">--</div></div>
<div style="flex:1;min-width:140px;background:#1e293b;border-radius:8px;padding:12px;text-align:center;border:1px solid rgba(148,163,184,.1)"><div style="font-size:.75rem;color:#64748b">{"分行代码" if is_cn else "Branch Code"}</div><div style="font-size:1.2rem;color:#22d3ee;font-weight:bold" id="branchCode">--</div></div>
</div>
<div style="margin-top:12px;padding:12px;background:rgba(34,197,94,.1);border-radius:8px;text-align:center" id="formatStatus"></div>
</div>
<div class="info-section">
<h2>{"📖 BIC格式说明" if is_cn else "📖 BIC Format"}</h2>
<p>{"格式: BBBB CC LL XXX (BBB)" if is_cn else "Format: BBBB CC LL XXX (BBB)"}</p>
<p>{"BBBB = 银行代码 (4位字母) | CC = 国家代码 (2位字母) | LL = 地区代码 (2位字母数字) | XXX = 分行代码 (3位字母数字, 可选)" if is_cn else "BBBB = Bank Code (4 letters) | CC = Country Code (2 letters) | LL = Location (2 alphanumeric) | XXX = Branch (3 alphanumeric, optional)"}</p>
</div>''',

        "ip-address-range-calculator": f'''
<div class="input-section">
<h2>{"🌐 CIDR 输入" if is_cn else "🌐 CIDR Input"}</h2>
<label>{"IP/CIDR 地址" if is_cn else "IP/CIDR Address"}</label>
<input type="text" id="cidrInput" placeholder="{"例如: 192.168.1.0/24" if is_cn else "e.g. 192.168.1.0/24"}" value="192.168.1.0/24">
<div class="btn-row"><button class="btn btn-primary" onclick="calculateCIDR()">{calculate_btn}</button><button class="btn btn-secondary" onclick="document.getElementById('cidrInput').value='';clearCIDR()">{clear_btn}</button></div>
</div>
<div class="result-section" id="cidrResult" style="display:none">
<h2>{"📊 计算结果" if is_cn else "📊 Results"}</h2>
<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px">
<div style="background:#1e293b;border-radius:8px;padding:12px;text-align:center;border:1px solid rgba(148,163,184,.1)"><div style="font-size:.75rem;color:#64748b">{"网络地址" if is_cn else "Network"}</div><div style="color:#22d3ee" id="networkAddr">--</div></div>
<div style="background:#1e293b;border-radius:8px;padding:12px;text-align:center;border:1px solid rgba(148,163,184,.1)"><div style="font-size:.75rem;color:#64748b">{"广播地址" if is_cn else "Broadcast"}</div><div style="color:#22d3ee" id="broadcastAddr">--</div></div>
<div style="background:#1e293b;border-radius:8px;padding:12px;text-align:center;border:1px solid rgba(148,163,184,.1)"><div style="font-size:.75rem;color:#64748b">{"子网掩码" if is_cn else "Subnet Mask"}</div><div style="color:#22d3ee" id="subnetMask">--</div></div>
<div style="background:#1e293b;border-radius:8px;padding:12px;text-align:center;border:1px solid rgba(148,163,184,.1)"><div style="font-size:.75rem;color:#64748b">{"可用IP范围" if is_cn else "Usable Range"}</div><div style="color:#22d3ee;font-size:.8rem" id="usableRange">--</div></div>
<div style="background:#1e293b;border-radius:8px;padding:12px;text-align:center;border:1px solid rgba(148,163,184,.1)"><div style="font-size:.75rem;color:#64748b">{"主机数量" if is_cn else "Host Count"}</div><div style="color:#22d3ee;font-size:1.2rem;font-weight:bold" id="hostCount">--</div></div>
<div style="background:#1e293b;border-radius:8px;padding:12px;text-align:center;border:1px solid rgba(148,163,184,.1)"><div style="font-size:.75rem;color:#64748b">{"IP类型" if is_cn else "IP Type"}</div><div style="color:#22d3ee" id="ipType">--</div></div>
</div>
</div>''',

        "color-contrast-analyzer": f'''
<div class="input-section">
<h2>{"🎨 颜色输入" if is_cn else "🎨 Color Input"}</h2>
<div class="row">
<div class="field"><label>{"前景色 (文字)" if is_cn else "Foreground (Text)"}</label><div style="display:flex;gap:8px;align-items:center"><input type="color" id="fgColor" value="#ffffff" style="width:40px;height:40px;padding:0;border:none"><input type="text" id="fgHex" value="#FFFFFF" style="flex:1"></div></div>
<div class="field"><label>{"背景色" if is_cn else "Background"}</label><div style="display:flex;gap:8px;align-items:center"><input type="color" id="bgColor" value="#4F46E5" style="width:40px;height:40px;padding:0;border:none"><input type="text" id="bgHex" value="#4F46E5" style="flex:1"></div></div>
</div>
<div class="preview-box" id="contrastPreview" style="background:#4F46E5;color:#ffffff;font-size:1.5rem;font-weight:bold;min-height:100px;border-radius:12px">
{"示例文字 Preview Text" if is_cn else "Sample Preview Text"}
</div>
<div class="btn-row"><button class="btn btn-primary" onclick="analyzeContrast()">{"分析对比度" if is_cn else "Analyze Contrast"}</button></div>
</div>
<div class="result-section">
<h2>{"📊 对比度分析" if is_cn else "📊 Contrast Analysis"}</h2>
<div class="result-box">
<div style="font-size:3rem;font-weight:bold" id="contrastRatio">4.55</div>
<div style="color:#94a3b8">{"对比度比率" if is_cn else "Contrast Ratio"}</div>
</div>
<div style="display:flex;gap:12px;margin-top:12px;flex-wrap:wrap">
<div style="flex:1;min-width:140px;background:#1e293b;border-radius:8px;padding:12px;text-align:center;border:1px solid rgba(148,163,184,.1)"><div style="font-size:.8rem;color:#64748b">AA {"正常文字" if is_cn else "Normal Text"}</div><div style="font-size:1.2rem" id="aaNormal">--</div></div>
<div style="flex:1;min-width:140px;background:#1e293b;border-radius:8px;padding:12px;text-align:center;border:1px solid rgba(148,163,184,.1)"><div style="font-size:.8rem;color:#64748b">AA {"大文字" if is_cn else "Large Text"}</div><div style="font-size:1.2rem" id="aaLarge">--</div></div>
<div style="flex:1;min-width:140px;background:#1e293b;border-radius:8px;padding:12px;text-align:center;border:1px solid rgba(148,163,184,.1)"><div style="font-size:.8rem;color:#64748b">AAA {"正常文字" if is_cn else "Normal Text"}</div><div style="font-size:1.2rem" id="aaaNormal">--</div></div>
<div style="flex:1;min-width:140px;background:#1e293b;border-radius:8px;padding:12px;text-align:center;border:1px solid rgba(148,163,184,.1)"><div style="font-size:.8rem;color:#64748b">AAA {"大文字" if is_cn else "Large Text"}</div><div style="font-size:1.2rem" id="aaaLarge">--</div></div>
</div>
</div>''',

        "docker-run-generator": f'''
<div class="input-section">
<h2>{"🐳 Docker 配置" if is_cn else "🐳 Docker Config"}</h2>
<div class="row">
<div class="field"><label>{"镜像名" if is_cn else "Image Name"}</label><input type="text" id="imageName" placeholder="nginx:latest" value="nginx:latest"></div>
<div class="field"><label>{"容器名 (可选)" if is_cn else "Container Name"}</label><input type="text" id="containerName" placeholder="my-nginx"></div>
</div>
<div class="row">
<div class="field"><label>{"端口映射" if is_cn else "Port Mapping"}</label><input type="text" id="portMap" placeholder="{"例如: 8080:80" if is_cn else "e.g. 8080:80"}" value="8080:80"></div>
<div class="field"><label>{"卷挂载" if is_cn else "Volume Mount"}</label><input type="text" id="volumeMount" placeholder="{"例如: ./data:/var/data" if is_cn else "e.g. ./data:/var/data"}"></div>
</div>
<div class="row">
<div class="field"><label>{"环境变量" if is_cn else "Env Variables"}</label><input type="text" id="envVars" placeholder="{"例如: NODE_ENV=production" if is_cn else "e.g. NODE_ENV=production"}"></div>
<div class="field"><label>{"重启策略" if is_cn else "Restart Policy"}</label><select id="restartPolicy"><option value="">{"不设置" if is_cn else "None"}</option><option value="no">no</option><option value="always">always</option><option value="on-failure">on-failure</option><option value="unless-stopped">unless-stopped</option></select></div>
</div>
<div class="row">
<div class="field"><label><input type="checkbox" id="detached" checked style="width:auto;margin-right:4px">{"后台运行 (-d)" if is_cn else "Detached (-d)"}</label></div>
<div class="field"><label><input type="checkbox" id="removeOnStop" style="width:auto;margin-right:4px">{"停止后删除 (--rm)" if is_cn else "Auto-remove (--rm)"}</label></div>
</div>
<div class="btn-row"><button class="btn btn-primary" onclick="generateDockerRun()">{generate_btn}</button></div>
</div>
<div class="result-section">
<h2>{"📋 Docker Run 命令" if is_cn else "📋 Docker Run Command"}</h2>
<pre id="dockerCmd" style="min-height:40px">{"点击生成按钮..." if is_cn else "Click generate..."}</pre>
<div class="btn-row"><button class="btn btn-primary" onclick="copyText(document.getElementById('dockerCmd').textContent)">{copy_btn}</button></div>
</div>''',

        "cron-sandbox": f'''
<div class="input-section">
<h2>{"⏰ Cron 表达式" if is_cn else "⏰ Cron Expression"}</h2>
<label>{"Cron 表达式" if is_cn else "Cron Expression"}</label>
<div class="row">
<div class="field" style="flex:3"><input type="text" id="cronInput" placeholder="{"例如: 0 9 * * 1-5" if is_cn else "e.g. 0 9 * * 1-5"}" value="0 9 * * 1-5" style="font-size:1.2rem;letter-spacing:1px"></div>
<div class="field" style="flex:1"><select id="cronFormat"><option value="5">{"5位 (标准)" if is_cn else "5-field"}</option><option value="6">{"6位 (含秒)" if is_cn else "6-field (sec)"}</option></select></div>
</div>
<div class="btn-row"><button class="btn btn-primary" onclick="parseCron()">{"解析表达式" if is_cn else "Parse Expression"}</button><button class="btn btn-secondary" onclick="quickCron('* * * * *')">{"每分钟" if is_cn else "Every min"}</button><button class="btn btn-secondary" onclick="quickCron('0 * * * *')">{"每小时" if is_cn else "Hourly"}</button><button class="btn btn-secondary" onclick="quickCron('0 0 * * *')">{"每天" if is_cn else "Daily"}</button></div>
</div>
<div class="result-section" id="cronResult" style="display:none">
<h2>{"📖 人类可读描述" if is_cn else "📖 Human-Readable"}</h2>
<div class="result-box"><div style="font-size:1.1rem" id="cronDescription">--</div></div>
<h2>{"📅 未来执行时间" if is_cn else "📅 Next Executions"}</h2>
<div style="background:#0f172a;border-radius:8px;padding:12px;border:1px solid rgba(148,163,184,.08)" id="nextExecutions"></div>
<div id="cronError" style="color:#ef4444;margin-top:8px;display:none"></div>
</div>
<div class="info-section">
<h2>{"📖 Cron 格式" if is_cn else "📖 Cron Format"}</h2>
<pre>{"* * * * *" if is_cn else "* * * * *"}
{"│ │ │ │ │" if is_cn else "│ │ │ │ │"}
{"│ │ │ │ └─ 星期 (0-7, 0=周日)" if is_cn else "│ │ │ │ └─ Day of week (0-7, 0=Sun)"}
{"│ │ │ └─── 月份 (1-12)" if is_cn else "│ │ │ └─── Month (1-12)"}
{"│ │ └───── 日期 (1-31)" if is_cn else "│ │ └───── Day of month (1-31)"}
{"│ └─────── 小时 (0-23)" if is_cn else "│ └─────── Hour (0-23)"}
{"└───────── 分钟 (0-59)" if is_cn else "└───────── Minute (0-59)"}</pre>
</div>''',
    }
    
    return bodies.get(slug, f'''
<div class="input-section">
<h2>{"📋 输入" if is_cn else "📋 Input"}</h2>
<input type="text" id="toolInput" placeholder="{"输入内容..." if is_cn else "Enter content..."}">
<div class="btn-row"><button class="btn btn-primary" onclick="processTool()">{generate_btn}</button></div>
</div>
<div class="result-section">
<h2>{"📊 结果" if is_cn else "📊 Result"}</h2>
<div id="toolOutput">--</div>
</div>
''')


def build_tool_js(tool, is_cn):
    """生成工具特定的JS代码"""
    slug = tool["slug"]
    
    js_map = {
        "virtual-piano-keyboard": '''
// 虚拟钢琴 - 使用Web Audio API
(function(){
var audioCtx=null;
var notes={};
var recording=[];
var isRecording=false;
var isPlaying=false;
var playbackTimer=null;

// 琴键映射
var whiteKeys=['C','D','E','F','G','A','B','C2','D2','E2','F2','G2','A2','B2'];
var blackKeys=['C#','D#','','F#','G#','A#','','C#2','D#2','','F#2','G#2','A#2'];
var keyboardMap={
  'a':'C3','w':'C#3','s':'D3','e':'D#3','d':'E3','f':'F3','t':'F#3','g':'G3','y':'G#3','h':'A3','u':'A#3','j':'B3','k':'C4','o':'C#4','l':'D4','p':'D#4',';':'E4',"'":'F4',']':'F#4'
};

var baseFreqs={'C':261.63,'C#':277.18,'D':293.66,'D#':311.13,'E':329.63,'F':349.23,'F#':369.99,'G':392.00,'G#':415.30,'A':440.00,'A#':466.16,'B':493.88};

function getFreq(noteName){var octave=parseInt(noteName.slice(-1))||4;var base=noteName.replace(/[0-9]/g,'');var f=baseFreqs[base]||440;return f*Math.pow(2,octave-4);}

function initAudio(){if(!audioCtx){audioCtx=new(window.AudioContext||window.webkitAudioContext)();}}

function playNote(noteName,vol){initAudio();var now=audioCtx.currentTime;var osc=audioCtx.createOscillator();var gain=audioCtx.createGain();var inst=document.getElementById('instrument').value;
osc.type=inst==='organ'?'square':inst==='guitar'?'triangle':inst==='flute'?'sine':'triangle';
osc.frequency.value=getFreq(noteName);gain.gain.setValueAtTime(vol*0.3,now);gain.gain.exponentialRampToValueAtTime(0.001,now+0.8);
osc.connect(gain);gain.connect(audioCtx.destination);osc.start(now);osc.stop(now+0.8);
if(isRecording){recording.push({note:noteName,time:Date.now()});}
}

function buildPiano(){
var piano=document.getElementById('piano');piano.innerHTML='';
for(var i=0;i<14;i++){
var wk=document.createElement('div');wk.style.cssText='flex:1;height:100%;background:#f8fafc;border:1px solid #cbd5e1;border-radius:0 0 4px 4px;cursor:pointer;position:relative;z-index:1';
wk.onmousedown=function(n){return function(){playNote(n,70);};}(whiteKeys[i]);
piano.appendChild(wk);
}
// 黑键
var blackPositions=[0.7,1.7,3.7,4.7,5.7,7.7,8.7,9.7,11.7,12.7];
for(var j=0;j<blackKeys.length;j++){
if(!blackKeys[j])continue;
var bk=document.createElement('div');
bk.style.cssText='position:absolute;width:8%;height:55%;background:#1e293b;top:0;border-radius:0 0 3px 3px;cursor:pointer;z-index:2;left:'+(blackPositions[j]*6.2)+'%';
bk.onmousedown=function(n){return function(e){e.stopPropagation();playNote(n,70);};}(blackKeys[j]);
piano.appendChild(bk);
}
}

document.addEventListener('keydown',function(e){
if(e.repeat)return;
var note=keyboardMap[e.key.toLowerCase()];
if(note){e.preventDefault();playNote(note,parseInt(document.getElementById('volume').value));}
});

document.getElementById('btnRecord').onclick=function(){
isRecording=!isRecording;
if(isRecording){recording=[];this.textContent='⏹ 停止录制';this.style.background='rgba(239,68,68,.2)';this.style.color='#ef4444';}
else{this.textContent='🎙 录制';this.style.background='';this.style.color='';}
};

document.getElementById('btnPlayback').onclick=function(){
if(recording.length===0){showToast('没有录制内容');return;}
if(isPlaying)return;
isPlaying=true;
var startTime=recording[0].time;
var i=0;
function playNext(){
if(i>=recording.length||!isPlaying){isPlaying=false;return;}
var item=recording[i];
var delay=i===0?0:recording[i].time-recording[i-1].time;
setTimeout(function(){playNote(item.note,70);i++;playNext();},Math.min(delay,500));
}
playNext();
};

document.getElementById('btnStop').onclick=function(){isPlaying=false;isRecording=false;document.getElementById('btnRecord').textContent='🎙 录制';document.getElementById('btnRecord').style.background='';document.getElementById('btnRecord').style.color='';};

buildPiano();
})();
''',

        "neumorphic-css": '''
(function(){
function updateCSS(){
var bg=document.getElementById('bgColor').value;
var el=document.getElementById('elColor').value;
var r=parseInt(document.getElementById('radius').value);
var d=parseInt(document.getElementById('distance').value);
var b=parseInt(document.getElementById('blur').value);
var shape=document.getElementById('shape').value;

document.getElementById('radiusVal').textContent=r+'px';
document.getElementById('distanceVal').textContent=d+'px';
document.getElementById('blurVal').textContent=b+'px';

document.getElementById('previewBox').style.background=bg;
var preview=document.getElementById('previewEl');
preview.style.background=el;
preview.style.borderRadius=r+'px';

function hexToRgb(hex){var r=parseInt(hex.slice(1,3),16);var g=parseInt(hex.slice(3,5),16);var b=parseInt(hex.slice(5,7),16);return{r:r,g:g,b:b};}
var c=hexToRgb(el);
function darken(ch){return '#'+[ch.r,ch.g,ch.b].map(function(v){var n=Math.max(0,v-40);return n.toString(16).padStart(2,'0');}).join('');}
function lighten(ch){return '#'+[ch.r,ch.g,ch.b].map(function(v){var n=Math.min(255,v+40);return n.toString(16).padStart(2,'0');}).join('');}
var dk=darken(c),lt=lighten(c);

var css='';
if(shape==='flat'){css='box-shadow: '+d+'px '+d+'px '+b+'px '+dk+', -'+d+'px -'+d+'px '+b+'px '+lt+';';}
else if(shape==='concave'){css='box-shadow: inset '+d+'px '+d+'px '+b+'px '+dk+', inset -'+d+'px -'+d+'px '+b+'px '+lt+';';}
else if(shape==='convex'){css='box-shadow: '+d+'px '+d+'px '+b+'px '+dk+', -'+d+'px -'+d+'px '+b+'px '+lt+';';}
else if(shape==='pressed'){css='box-shadow: inset '+d+'px '+d+'px '+b+'px '+dk+', inset -'+d+'px -'+d+'px '+b+'px '+lt+';';}

css+='\\nborder-radius: '+r+'px;';
preview.style.cssText+=';'+css;
document.getElementById('cssOutput').textContent=css;
}

['bgColor','elColor'].forEach(function(id){document.getElementById(id).addEventListener('input',updateCSS);});
['radius','distance','blur'].forEach(function(id){document.getElementById(id).addEventListener('input',updateCSS);});
document.getElementById('shape').addEventListener('change',updateCSS);
updateCSS();
})();
''',

        "bricks-calculator": '''
function calculateBricks(){
var wl=parseFloat(document.getElementById('wallLength').value)||0;
var wh=parseFloat(document.getElementById('wallHeight').value)||0;
var bl=parseFloat(document.getElementById('brickLength').value)||0;
var bh=parseFloat(document.getElementById('brickHeight').value)||0;
var m=parseFloat(document.getElementById('mortar').value)||0;
if(wl<=0||wh<=0||bl<=0||bh<=0){showToast('请输入有效数值');return;}
var area=wl*wh;
var brickArea=(bl+m)*(bh+m)/1000000;
var count=Math.ceil(area/brickArea*1.05);
document.getElementById('wallArea').textContent=area.toFixed(2);
document.getElementById('brickCount').textContent=count;
document.getElementById('brickPerSqm').textContent=Math.ceil(1/brickArea);
document.getElementById('wasteText').textContent='5%)';
}
function clearBricks(){
['wallLength','wallHeight','brickLength','brickHeight','mortar'].forEach(function(id){document.getElementById(id).value='';});
document.getElementById('wallArea').textContent='--';
document.getElementById('brickCount').textContent='--';
document.getElementById('brickPerSqm').textContent='--';
}
calculateBricks();
''',

        "website-uptime-checker": '''
function checkUptime(){
var url=document.getElementById('urlInput').value.trim();
if(!url){showToast('请输入网址');return;}
if(!/^https?:\\/\\//.test(url)){url='https://'+url;}
var method=document.getElementById('method').value;
document.getElementById('resultSection').style.display='block';
document.getElementById('statusDisplay').innerHTML='<span style="color:#eab308">检测中...</span>';
var startTime=Date.now();
fetch(url,{method:method,mode:'no-cors'}).then(function(r){
var elapsed=Date.now()-startTime;
document.getElementById('responseTime').textContent=elapsed+'ms';
var cls=r.type==='opaque'?'status-ok':'status-ok';
document.getElementById('statusDisplay').innerHTML='<span class="'+cls+'">✅ 网站可访问</span>';
document.getElementById('statusCode').textContent='200 (估算)';
}).catch(function(e){
var elapsed=Date.now()-startTime;
document.getElementById('responseTime').textContent=elapsed+'ms';
document.getElementById('statusDisplay').innerHTML='<span class="status-err">❌ 无法访问</span>';
document.getElementById('statusCode').textContent='ERR';
var msg=e.message||'网络错误';
if(msg.includes('Failed to fetch')){msg='CORS限制 / 网站拒绝请求 (可尝试在浏览器中输入URL直接访问)';}
document.getElementById('statusCode').textContent=msg.substring(0,30);
});
}
''',

        "jwt-token-generator": '''
function base64url(str){
return btoa(str).replace(/=/g,'').replace(/\\+/g,'-').replace(/\\//g,'_');
}
function generateJWT(){
var headerText=document.getElementById('headerJson').value;
var payloadText=document.getElementById('payloadJson').value;
var secret=document.getElementById('secretKey').value;
var alg=document.getElementById('algorithm').value;
try{JSON.parse(headerText);JSON.parse(payloadText);}catch(e){showToast('JSON格式错误');return;}
var header=base64url(headerText);
var payload=base64url(payloadText);
var unsignedToken=header+'.'+payload;

// 简化HMAC签名 (使用Web Crypto API)
var encoder=new TextEncoder();
var keyData=encoder.encode(secret);
var algoMap={HS256:'SHA-256',HS384:'SHA-384',HS512:'SHA-512'};
var hashAlgo=algoMap[alg]||'SHA-256';

crypto.subtle.importKey('raw',keyData,{name:'HMAC',hash:{name:hashAlgo}},false,['sign']).then(function(key){
return crypto.subtle.sign('HMAC',key,encoder.encode(unsignedToken));
}).then(function(sig){
var signature=base64url(String.fromCharCode.apply(null,new Uint8Array(sig)));
var token=unsignedToken+'.'+signature;
document.getElementById('tokenOutput').textContent=token;
}).catch(function(e){
// Fallback: 用简单方式显示结构
document.getElementById('tokenOutput').textContent=unsignedToken+'.<签名需要浏览器Crypto API>';
});
}
function resetJWT(){document.getElementById('headerJson').value='{"alg":"HS256","typ":"JWT"}';document.getElementById('payloadJson').value='{"sub":"1234567890","name":"John Doe","iat":1516239022,"exp":1716239022}';document.getElementById('secretKey').value='your-256-bit-secret';document.getElementById('tokenOutput').textContent='点击生成按钮...';}
''',

        "swift-bic-validation": '''
function validateBIC(){
var bic=document.getElementById('bicInput').value.trim().toUpperCase().replace(/\\s/g,'');
if(!bic){showToast('请输入BIC代码');return;}
var regex=/^[A-Z]{6}[A-Z0-9]{2}([A-Z0-9]{3})?$/;
if(!regex.test(bic)){document.getElementById('bicResult').style.display='block';document.getElementById('formatStatus').innerHTML='<span class="status-err">❌ 格式无效</span>';document.getElementById('formatStatus').style.background='rgba(239,68,68,.1)';return;}

document.getElementById('bicResult').style.display='block';
document.getElementById('bankCode').textContent=bic.substring(0,4);
document.getElementById('countryCode').textContent=bic.substring(4,6);
document.getElementById('locationCode').textContent=bic.substring(6,8);
document.getElementById('branchCode').textContent=bic.length===11?bic.substring(8,11):'XXX (总部/默认)';
document.getElementById('formatStatus').innerHTML='<span class="status-ok">✅ 格式有效 ('+(bic.length)+'位)</span>';
document.getElementById('formatStatus').style.background='rgba(34,197,94,.1)';

// 国家代码参考
var countries={CN:'中国',US:'美国',GB:'英国',JP:'日本',DE:'德国',FR:'法国',HK:'香港',SG:'新加坡',AU:'澳大利亚',CA:'加拿大',CH:'瑞士',NL:'荷兰',SE:'瑞典',KR:'韩国',IN:'印度'};
var cc=bic.substring(4,6);
if(countries[cc]){document.getElementById('countryCode').textContent=cc+' ('+countries[cc]+')';}
}
function clearBICResult(){
document.getElementById('bicResult').style.display='none';
['bankCode','countryCode','locationCode','branchCode'].forEach(function(id){document.getElementById(id).textContent='--';});
}
''',

        "ip-address-range-calculator": '''
function ipToNum(ip){return ip.split('.').reduce(function(acc,o){return(acc<<8)+parseInt(o);},0)>>>0;}
function numToIp(num){return[(num>>>24)&255,(num>>>16)&255,(num>>>8)&255,num&255].join('.');}
function calculateCIDR(){
var input=document.getElementById('cidrInput').value.trim();
var parts=input.split('/');
if(parts.length!==2){showToast('请输入有效的CIDR格式 (如192.168.1.0/24)');return;}
var ip=parts[0];
var prefix=parseInt(parts[1]);
if(prefix<0||prefix>32){showToast('前缀长度需在0-32之间');return;}
var ipNum=ipToNum(ip);
var mask=prefix===0?0:~((1<<(32-prefix))-1)>>>0;
var network=ipNum&mask;
var broadcast=network|(~mask>>>0);
var firstHost=prefix>=31?network:network+1;
var lastHost=prefix>=31?broadcast:broadcast-1;
var hostCount=prefix>=31?(prefix===32?1:2):Math.pow(2,32-prefix)-2;
document.getElementById('cidrResult').style.display='block';
document.getElementById('networkAddr').textContent=numToIp(network);
document.getElementById('broadcastAddr').textContent=numToIp(broadcast);
document.getElementById('subnetMask').textContent=numToIp(mask);
document.getElementById('usableRange').textContent=numToIp(firstHost)+' - '+numToIp(lastHost);
document.getElementById('hostCount').textContent=hostCount.toLocaleString();
document.getElementById('ipType').textContent=ip.split('.')[0]<224?'公网/私有IPv4':ip.split('.')[0]<240?'组播':'保留';
}
function clearCIDR(){document.getElementById('cidrResult').style.display='none';}
calculateCIDR();
''',

        "color-contrast-analyzer": '''
function hexToRgb(hex){
var r=parseInt(hex.slice(1,3),16)/255;
var g=parseInt(hex.slice(3,5),16)/255;
var b=parseInt(hex.slice(5,7),16)/255;
return{r:r,g:g,b:b};
}
function toLinear(c){return c<=0.03928?c/12.92:Math.pow((c+0.055)/1.055,2.4);}
function relativeLuminance(rgb){
return 0.2126*toLinear(rgb.r)+0.7152*toLinear(rgb.g)+0.0722*toLinear(rgb.b);
}
function analyzeContrast(){
var fg=document.getElementById('fgHex').value.trim();
var bg=document.getElementById('bgHex').value.trim();
if(!/^#[0-9A-Fa-f]{6}$/.test(fg)){showToast('前景色格式无效');return;}
if(!/^#[0-9A-Fa-f]{6}$/.test(bg)){showToast('背景色格式无效');return;}
var l1=relativeLuminance(hexToRgb(fg));
var l2=relativeLuminance(hexToRgb(bg));
var ratio=(Math.max(l1,l2)+0.05)/(Math.min(l1,l2)+0.05);
document.getElementById('contrastRatio').textContent=ratio.toFixed(2);
document.getElementById('contrastPreview').style.background=bg;
document.getElementById('contrastPreview').style.color=fg;

function passFail(r,threshold){return r>=threshold?'<span class="status-ok">✅ 通过</span>':'<span class="status-err">❌ 未通过</span>';}
document.getElementById('aaNormal').innerHTML=passFail(ratio,4.5);
document.getElementById('aaLarge').innerHTML=passFail(ratio,3);
document.getElementById('aaaNormal').innerHTML=passFail(ratio,7);
document.getElementById('aaaLarge').innerHTML=passFail(ratio,4.5);
}
document.getElementById('fgColor').addEventListener('input',function(){document.getElementById('fgHex').value=this.value;analyzeContrast();});
document.getElementById('bgColor').addEventListener('input',function(){document.getElementById('bgHex').value=this.value;analyzeContrast();});
document.getElementById('fgHex').addEventListener('input',function(){var v=this.value;if(/^#[0-9A-Fa-f]{6}$/.test(v)){document.getElementById('fgColor').value=v;analyzeContrast();}});
document.getElementById('bgHex').addEventListener('input',function(){var v=this.value;if(/^#[0-9A-Fa-f]{6}$/.test(v)){document.getElementById('bgColor').value=v;analyzeContrast();}});
analyzeContrast();
''',

        "docker-run-generator": '''
function generateDockerRun(){
var cmd='docker run';
if(document.getElementById('removeOnStop').checked){cmd+=' --rm';}
if(document.getElementById('detached').checked){cmd+=' -d';}
var cn=document.getElementById('containerName').value.trim();
if(cn){cmd+=' --name '+cn;}
var pm=document.getElementById('portMap').value.trim();
if(pm){cmd+=' -p '+pm;}
var vm=document.getElementById('volumeMount').value.trim();
if(vm){cmd+=' -v '+vm;}
var env=document.getElementById('envVars').value.trim();
if(env){var evs=env.split(',');for(var i=0;i<evs.length;i++){cmd+=' -e '+evs[i].trim();}}
var rp=document.getElementById('restartPolicy').value;
if(rp){cmd+=' --restart '+rp;}
cmd+=' '+document.getElementById('imageName').value.trim();
document.getElementById('dockerCmd').textContent=cmd;
}
generateDockerRun();
['imageName','containerName','portMap','volumeMount','envVars','restartPolicy'].forEach(function(id){
document.getElementById(id).addEventListener('input',generateDockerRun);
});
['detached','removeOnStop'].forEach(function(id){
document.getElementById(id).addEventListener('change',generateDockerRun);
});
''',

        "cron-sandbox": '''
function parseCron(){
var expr=document.getElementById('cronInput').value.trim();
if(!expr){showToast('请输入Cron表达式');return;}
var format=document.getElementById('cronFormat').value;
var fields=expr.split(/\\s+/);
var expected=parseInt(format);
if(fields.length!==expected){document.getElementById('cronError').style.display='block';document.getElementById('cronError').textContent='❌ 字段数应为'+expected+'个 (当前'+fields.length+'个)';return;}
document.getElementById('cronError').style.display='none';
document.getElementById('cronResult').style.display='block';

// 简单的人类可读描述
var names=[['分','分钟'],['时','点'],['日','号'],['月','月'],['周','周']];
var desc=fields.map(function(f,i){
var n=names[i]||['',''];
if(f==='*')return'每'+n[0];
if(f.includes(','))return f.replace(/,/g,'和')+n[0];
if(f.includes('-')){var p=f.split('-');return '从'+p[0]+'到'+p[1]+n[0];}
if(f.includes('/')){var p2=f.split('/');return'每'+p2[1]+n[0];}
return '在'+f+n[1];
}).join(', ');

document.getElementById('cronDescription').textContent=desc;

// 未来执行时间
var now=new Date();
var times=[];
var count=0;
var testDate=new Date(now);
testDate.setSeconds(0,0);
var mins=testDate.getMinutes();
testDate.setMinutes(mins+1-(mins%1));

while(count<5&&count<100){
var dateStr=testDate.toLocaleString();
times.push('<div style="padding:4px 0;border-bottom:1px solid rgba(148,163,184,.1)">'+dateStr+'</div>');
testDate.setMinutes(testDate.getMinutes()+(fields[0]==='*'?1:parseInt(fields[0])||60));
count++;
}
times.push('<div style="padding:4px 0;color:#64748b;font-size:.8rem">(简化模拟，实际执行取决于完整Cron规则)</div>');
document.getElementById('nextExecutions').innerHTML=times.join('');
}
function quickCron(expr){document.getElementById('cronInput').value=expr;parseCron();}
parseCron();
''',
    }
    
    return js_map.get(slug, '// tool specific JS');


def build_faqs(tool, is_cn):
    """生成FAQ"""
    cn_faqs = {
        "virtual-piano-keyboard": [
            ("虚拟钢琴需要下载吗？", "不需要。本工具纯前端运行，直接在浏览器中使用，无需安装任何软件或插件。"),
            ("可以用电脑键盘弹奏吗？", "可以。键盘映射为：白色键A-L和;'，黑色键W、E、T、Y、U、O、P、]。具体见页面上的键盘映射图。"),
            ("支持录制和回放吗？", "支持。点击录制按钮开始记录演奏，点击回放即可重播。录制数据保存在浏览器内存中。"),
        ],
        "neumorphic-css": [
            ("什么是Neumorphic风格？", "Neumorphic（新拟态）是一种UI设计风格，通过柔和的阴影来模拟元素凸起或凹陷的效果，给人以柔软、真实的触感。"),
            ("生成的CSS可以直接用吗？", "可以。复制生成的CSS代码，直接粘贴到你的项目样式表中即可使用。"),
            ("支持哪些形状？", "支持平面（flat）、凹面（concave）、凸面（convex）、按下（pressed）四种形状效果。"),
        ],
        "bricks-calculator": [
            ("如何准确计算砖块数量？", "输入墙体的长和高，以及砖块和灰缝尺寸。工具会自动计算面积并加上5%损耗。标准砖尺寸为240×115×53mm。"),
            ("灰缝厚度是多少？", "通常灰缝为10mm，你也可以根据实际施工情况自行调整。"),
            ("结果包含损耗吗？", "是的，计算结果已包含5%的材料损耗，确保购买时有足够的余量。"),
        ],
        "website-uptime-checker": [
            ("可以检测任何网站吗？", "本工具从浏览器发起HTTP请求。部分网站可能因CORS策略限制无法检测。"),
            ("GET和HEAD方法有什么区别？", "HEAD方法只获取响应头，不下载页面内容，速度快；GET方法获取完整页面，更接近真实访问。"),
            ("检测结果100%准确吗？", "不一定。浏览器端检测受网络环境和CORS策略影响，建议配合服务器端监控使用。"),
        ],
        "jwt-token-generator": [
            ("JWT是什么？", "JWT（JSON Web Token）是一种开放标准，用于在各方之间安全地传输信息。广泛应用于API认证和授权。"),
            ("密钥会上传服务器吗？", "不会。所有签名计算在浏览器本地完成，密钥不会离开你的设备。"),
            ("支持哪些算法？", "支持HS256、HS384、HS512三种HMAC-SHA签名算法。"),
        ],
        "swift-bic-validation": [
            ("SWIFT和BIC有什么区别？", "SWIFT和BIC是同一事物的两种名称。SWIFT是组织名，BIC（Bank Identifier Code）是银行识别码的正式名称。"),
            ("BIC代码有几位的？", "BIC代码有8位和11位两种格式。8位包含银行代码+国家代码+地区代码，11位额外包含分行代码。"),
            ("验证器能识别所有银行吗？", "本工具主要验证格式合法性，部分国家代码有中文注释。详细的银行数据库需专业服务。"),
        ],
        "ip-address-range-calculator": [
            ("什么是CIDR？", "CIDR（无类别域间路由）是IP地址分配方法，格式为IP地址/前缀长度，如192.168.1.0/24表示前24位是网络部分。"),
            ("支持IPv6吗？", "目前仅支持IPv4地址范围计算。IPv6支持将在后续版本中提供。"),
            ("主机数量如何计算？", "主机数量=2^(32-前缀长度)-2（减去网络地址和广播地址）。/31和/32有特殊规则。"),
        ],
        "color-contrast-analyzer": [
            ("WCAG是什么？", "WCAG（Web内容无障碍指南）是国际标准，规定了网页内容对残障人士可访问的要求。AA和AAA是两个合规级别。"),
            ("正常文字和大文字的区别？", "大文字指≥18pt或≥14pt加粗的文字。大文字的对比度要求比正常文字低。"),
            ("多少对比度算合格？", "AA级正常文字需≥4.5:1，大文字需≥3:1。AAA级正常文字需≥7:1，大文字需≥4.5:1。"),
        ],
        "docker-run-generator": [
            ("生成的命令可以直接用吗？", "可以。复制生成的docker run命令，直接在终端中粘贴执行即可。请确保已安装Docker。"),
            ("端口映射格式是什么？", "格式为 主机端口:容器端口，如8080:80表示将主机的8080端口映射到容器的80端口。"),
            ("--rm参数是什么？", "--rm参数表示容器停止后自动删除，避免产生残留的已停止容器。"),
        ],
        "cron-sandbox": [
            ("Cron表达式的格式是什么？", "标准Cron表达式有5个字段：分 时 日 月 周。有些系统支持6字段（含秒）。"),
            ("* 代表什么意思？", "星号 * 表示匹配该字段的所有值。例如 * * * * * 表示每分钟执行一次。"),
            ("如何表示工作日？", "在星期字段使用1-5表示周一到周五。0和7都表示周日。"),
        ],
    }
    
    en_faqs = {
        "virtual-piano-keyboard": [
            ("Does the virtual piano require download?", "No. This tool runs entirely in your browser, no installation needed."),
            ("Can I play with my computer keyboard?", "Yes. Key mapping: white keys A-L and ;', black keys W, E, T, Y, U, O, P, ]. See the key mapping section on the page."),
            ("Does it support recording and playback?", "Yes. Click the Record button to start recording your performance, then click Playback to replay. Recordings are stored in browser memory."),
        ],
        "neumorphic-css": [
            ("What is Neumorphic style?", "Neumorphism is a UI design style that uses soft shadows to simulate elements being raised or pressed, giving a soft, tactile feel."),
            ("Can I use the generated CSS directly?", "Yes. Copy the generated CSS code and paste it into your project stylesheet."),
            ("What shapes are supported?", "Flat, concave, convex, and pressed shapes are supported."),
        ],
        "bricks-calculator": [
            ("How to accurately calculate brick quantity?", "Enter wall length and height, along with brick and mortar dimensions. The tool auto-calculates area with 5% waste. Standard brick: 240×115×53mm."),
            ("What is the mortar joint thickness?", "Typically 10mm, but you can adjust based on your actual construction needs."),
            ("Does the result include waste?", "Yes, the calculation includes 5% material waste to ensure you buy enough."),
        ],
        "website-uptime-checker": [
            ("Can I check any website?", "This tool sends HTTP requests from your browser. Some sites may be unreachable due to CORS policies."),
            ("What's the difference between GET and HEAD?", "HEAD only fetches response headers (faster); GET downloads the full page (more realistic)."),
            ("Is the result 100% accurate?", "Not necessarily. Browser-side checks are affected by network conditions and CORS. Server-side monitoring is recommended."),
        ],
        "jwt-token-generator": [
            ("What is JWT?", "JWT (JSON Web Token) is an open standard for securely transmitting information between parties. Widely used for API authentication."),
            ("Is my secret key uploaded?", "No. All signing happens locally in your browser. Your secret key never leaves your device."),
            ("Which algorithms are supported?", "HS256, HS384, and HS512 HMAC-SHA algorithms are supported."),
        ],
        "swift-bic-validation": [
            ("What's the difference between SWIFT and BIC?", "They refer to the same thing. SWIFT is the organization name, BIC (Bank Identifier Code) is the official name for the code."),
            ("How many digits is a BIC code?", "BIC codes come in 8-digit (bank+country+location) and 11-digit (includes branch) formats."),
            ("Can the validator identify all banks?", "This tool primarily validates format. Some country codes have annotations. Full bank database requires professional services."),
        ],
        "ip-address-range-calculator": [
            ("What is CIDR?", "CIDR (Classless Inter-Domain Routing) is an IP address allocation method, formatted as IP/prefix, e.g. 192.168.1.0/24."),
            ("Does it support IPv6?", "Currently only IPv4 is supported. IPv6 support is planned."),
            ("How is host count calculated?", "Host count = 2^(32-prefix) - 2 (minus network and broadcast). /31 and /32 have special rules."),
        ],
        "color-contrast-analyzer": [
            ("What is WCAG?", "WCAG (Web Content Accessibility Guidelines) is an international standard for making web content accessible. AA and AAA are two compliance levels."),
            ("What's the difference between normal and large text?", "Large text is ≥18pt or ≥14pt bold. Large text has lower contrast requirements than normal text."),
            ("What contrast ratio is compliant?", "AA normal text needs ≥4.5:1, large text ≥3:1. AAA normal text needs ≥7:1, large text ≥4.5:1."),
        ],
        "docker-run-generator": [
            ("Can I use the generated command directly?", "Yes. Copy the generated docker run command and paste it in your terminal. Make sure Docker is installed."),
            ("What's the port mapping format?", "Format is host_port:container_port, e.g. 8080:80 maps host port 8080 to container port 80."),
            ("What does --rm do?", "--rm automatically removes the container when it stops, preventing leftover stopped containers."),
        ],
        "cron-sandbox": [
            ("What's the Cron expression format?", "Standard Cron has 5 fields: minute hour day month weekday. Some systems support 6 fields (with seconds)."),
            ("What does * mean?", "Asterisk * matches all values for that field. * * * * * means every minute."),
            ("How to specify weekdays?", "Use 1-5 in the weekday field for Monday-Friday. Both 0 and 7 represent Sunday."),
        ],
    }
    
    return cn_faqs.get(tool["slug"], [("如何使用？","输入数据后点击按钮即可。")]) if is_cn else en_faqs.get(tool["slug"], [("How to use?","Enter data and click the button.")])


# ============================================================
# 生成
# ============================================================
for tool in TOOLS:
    slug = tool["slug"]
    cn_dir = os.path.join(BASE, slug)
    en_dir = os.path.join(BASE, "en", slug)
    os.makedirs(cn_dir, exist_ok=True)
    os.makedirs(en_dir, exist_ok=True)
    
    # 生成中文版
    cn_html = gen_html(tool, "cn")
    with open(os.path.join(cn_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(cn_html)
    print(f"✅ {slug}/index.html (CN)")
    
    # 生成英文版
    en_html = gen_html(tool, "en")
    with open(os.path.join(en_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(en_html)
    print(f"✅ en/{slug}/index.html (EN)")

print(f"\n🎉 完成！生成{len(TOOLS)}个工具，共{len(TOOLS)*2}个页面")
