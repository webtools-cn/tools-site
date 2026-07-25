#!/usr/bin/env python3
"""批量开发新工具 - 本轮9个"""
import os, re, json

BASE = "/home/chison/tools-site"

# 工具定义: slug, cn_name, en_name, category, cn_desc, en_desc, cn_keywords, en_keywords
TOOLS = [
    {
        "slug": "seo-title-generator",
        "cn_name": "SEO标题生成器",
        "en_name": "SEO Title Generator",
        "category": "seo",
        "cn_desc": "免费SEO标题生成器，智能生成符合搜索引擎优化的网页标题。支持关键词组合、情感分析、长度优化（50-60字符），自动添加吸引点击的修饰词。",
        "en_desc": "Free SEO title generator that creates search-engine-optimized page titles. Supports keyword combinations, length optimization (50-60 chars), and click-attracting modifiers for higher CTR.",
        "cn_keywords": "SEO标题,网页标题生成,搜索引擎优化,title标签,点击率优化,元标题",
        "en_keywords": "SEO title,page title generator,meta title,title tag optimizer,CTR optimization",
        "cn_faq": [
            ("SEO标题应该多长？","理想长度为50-60个字符。过短浪费展示空间，过长会被搜索引擎截断。本工具自动计算并标注长度状态。"),
            ("如何写出高点击率的标题？","使用数字、情感词、紧迫感词汇（如'免费''2026''指南'），并在标题中自然融入主关键词。本工具内置修饰词库。"),
            ("标题和H1标签有什么区别？","title标签显示在搜索结果中，H1显示在页面内容顶部。两者可以相同也可以不同，但都应包含核心关键词。")
        ],
        "en_faq": [
            ("How long should an SEO title be?","The ideal length is 50-60 characters. Shorter titles waste SERP space, longer ones get truncated. This tool auto-calculates and flags length status."),
            ("How to write high-CTR titles?","Use numbers, emotional words, urgency triggers (e.g. 'Free', '2026', 'Guide'), and naturally include primary keywords. Our tool has built-in modifier suggestions."),
            ("What's the difference between title and H1?","The title tag appears in search results, H1 appears at the top of page content. They can be identical or different, but both should contain core keywords.")
        ]
    },
    {
        "slug": "domain-age-checker",
        "cn_name": "域名年龄查询",
        "en_name": "Domain Age Checker",
        "category": "seo",
        "cn_desc": "免费域名年龄查询工具，快速检测域名注册时间、距今年限、到期日期。输入任意域名即可查询，支持.com/.cn/.org等主流后缀。",
        "en_desc": "Free domain age checker to instantly look up domain registration date, years since registration, and expiration. Supports .com, .org, .net and all major TLDs.",
        "cn_keywords": "域名年龄,whois查询,域名注册时间,域名年限,网站年龄,域名信息",
        "en_keywords": "domain age,whois lookup,domain registration date,domain checker,website age",
        "cn_faq": [
            ("域名年龄对SEO有影响吗？","域名年龄是搜索引擎排名因素之一，但不是决定性因素。老域名可能拥有更多的反向链接和信任度，但新域名通过优质内容同样可以排名靠前。"),
            ("这个工具查询的是WHOIS数据吗？","是的，通过公共WHOIS服务查询域名的注册和到期时间。部分域名可能因隐私保护而隐藏详细信息。"),
            ("可以查询哪些后缀的域名？","支持所有常见顶级域名（TLD），包括.com、.cn、.org、.net、.io等。")
        ],
        "en_faq": [
            ("Does domain age affect SEO?","Domain age is one ranking signal but not decisive. Older domains may have more backlinks and trust, but new domains can rank well with quality content too."),
            ("Does this tool use WHOIS data?","Yes, it queries public WHOIS services for registration and expiration dates. Some domains may hide details via privacy protection."),
            ("Which TLDs are supported?","All common TLDs are supported, including .com, .org, .net, .io, .co, and country-code TLDs.")
        ]
    },
    {
        "slug": "random-username",
        "cn_name": "随机用户名生成器",
        "en_name": "Random Username Generator",
        "category": "generator",
        "cn_desc": "免费随机用户名生成器，支持多种风格（酷炫、可爱、专业、游戏ID），可添加数字后缀、特殊字符，批量生成1-100个独特用户名。",
        "en_desc": "Free random username generator supporting multiple styles (cool, cute, professional, gaming). Add number suffixes, special characters, and batch generate 1-100 unique usernames.",
        "cn_keywords": "随机用户名,用户名生成,游戏ID,昵称生成,账号名,唯一用户名",
        "en_keywords": "random username,username generator,gaming ID,nickname generator,account name",
        "cn_faq": [
            ("生成的用户名是否已被占用？","本工具仅生成随机用户名，不检查是否已被注册。建议在注册平台前先验证可用性。"),
            ("支持哪些用户名风格？","支持酷炫风、可爱风、专业风、游戏ID风等多种风格，可自定义前缀后缀和数字长度。"),
            ("最多可以生成多少个？","每次可生成1-100个用户名，一键复制全部或逐个使用。")
        ],
        "en_faq": [
            ("Are the generated usernames available?","This tool only generates random usernames, it doesn't check availability. Verify before registering on any platform."),
            ("What username styles are supported?","Cool, cute, professional, gaming ID, and more. Customize prefixes, suffixes, and number lengths."),
            ("How many can I generate at once?","Generate 1-100 usernames per batch, copy all at once or individually.")
        ]
    },
    {
        "slug": "random-password",
        "cn_name": "随机密码生成器",
        "en_name": "Random Password Generator",
        "category": "security",
        "cn_desc": "免费高强度随机密码生成器，使用密码学安全随机数。自定义长度、字符类型（大小写+数字+符号），实时评估密码强度，一键复制。",
        "en_desc": "Free strong random password generator using cryptographically secure randomness. Customize length, character types (upper/lower/digits/symbols), real-time strength meter, one-click copy.",
        "cn_keywords": "随机密码,密码生成,强密码,安全密码,密码管理器,密码工具",
        "en_keywords": "random password,password generator,strong password,secure password,crypto random",
        "cn_faq": [
            ("生成的密码安全吗？","使用Web Crypto API的密码学安全随机数生成器(crypto.getRandomValues)，比Math.random()安全得多，适合生成真实密码。"),
            ("多长的密码才安全？","建议至少12位以上。12位混合字符密码需要数千年才能暴力破解。本工具默认生成16位。"),
            ("密码会保存在服务器吗？","绝不保存。所有密码在您的浏览器本地生成，数据不上传服务器。")
        ],
        "en_faq": [
            ("Are the passwords secure?","Yes, we use the Web Crypto API (crypto.getRandomValues) for cryptographically secure randomness — far safer than Math.random()."),
            ("How long should a password be?","At least 12 characters. A 12-char mixed password takes thousands of years to brute-force. Our default is 16 characters."),
            ("Are passwords stored on a server?","Never. All passwords are generated locally in your browser — no data is ever uploaded.")
        ]
    },
    {
        "slug": "diceware-passphrase",
        "cn_name": "Diceware口令生成器",
        "en_name": "Diceware Passphrase Generator",
        "category": "security",
        "cn_desc": "免费Diceware口令生成器，基于EFF词表生成易记且高熵的密码短语。选择4-10个单词组合，安全又好记，适合主密码和加密密钥。",
        "en_desc": "Free Diceware passphrase generator using the EFF wordlist to create memorable high-entropy passphrases. Choose 4-10 word combinations — secure and memorable for master passwords.",
        "cn_keywords": "Diceware,口令生成,密码短语,易记密码,EFF词表,高熵密码",
        "en_keywords": "Diceware,passphrase generator,memorable password,EFF wordlist,high entropy",
        "cn_faq": [
            ("什么是Diceware？","Diceware是一种通过随机选择单词来生成密码短语的方法。6个随机单词的组合熵值约为77位，比复杂短密码更安全且更容易记忆。"),
            ("多少个单词才安全？","4个单词约51位熵（基本安全），6个单词约77位（推荐），8个单词约103位（高安全）。本工具默认6个单词。"),
            ("使用什么词表？","使用EFF（电子前哨基金会）推荐的Diceware词表，包含7776个常用英语单词，经过精心筛选避免混淆。")
        ],
        "en_faq": [
            ("What is Diceware?","Diceware generates passphrases by randomly selecting words. A 6-word combination has ~77 bits of entropy — more secure and memorable than complex short passwords."),
            ("How many words are secure enough?","4 words ≈ 51 bits (basic), 6 words ≈ 77 bits (recommended), 8 words ≈ 103 bits (high security). Our default is 6 words."),
            ("Which wordlist is used?","The EFF (Electronic Frontier Foundation) recommended Diceware wordlist with 7,776 carefully selected common English words.")
        ]
    },
    {
        "slug": "random-email",
        "cn_name": "随机邮箱生成器",
        "en_name": "Random Email Generator",
        "category": "generator",
        "cn_desc": "免费随机邮箱地址生成器，批量生成测试用邮箱地址。支持自定义域名、多种邮箱服务商（Gmail/Outlook/Yahoo等），适合开发和测试场景。",
        "en_desc": "Free random email address generator for bulk test email creation. Custom domains, multiple providers (Gmail/Outlook/Yahoo), perfect for development and testing.",
        "cn_keywords": "随机邮箱,邮箱生成,测试邮箱,临时邮箱,假邮箱,开发测试",
        "en_keywords": "random email,email generator,test email,fake email,dev testing",
        "cn_faq": [
            ("生成的邮箱可以收邮件吗？","本工具生成的是随机格式的邮箱地址，用于开发测试场景。这些邮箱并非真实注册，不能实际接收邮件。"),
            ("支持哪些邮箱域名？","默认提供Gmail、Outlook、Yahoo等常见服务商，也支持自定义任意域名。"),
            ("可以批量生成多少个？","每次可生成1-100个邮箱地址，一键复制全部。适合批量注册测试、数据填充等场景。")
        ],
        "en_faq": [
            ("Can these emails receive mail?","These are randomly formatted email addresses for dev/testing. They are not real registered accounts and cannot receive actual emails."),
            ("Which email providers are supported?","Default options include Gmail, Outlook, Yahoo, and more. You can also specify any custom domain."),
            ("How many can I generate?","Generate 1-100 email addresses per batch, copy all at once. Great for bulk registration testing and data seeding.")
        ]
    },
    {
        "slug": "dummy-xml-generator",
        "cn_name": "测试XML生成器",
        "en_name": "Dummy XML Generator",
        "category": "dev",
        "cn_desc": "免费测试XML数据生成器，快速生成可定制的XML测试数据。支持自定义根元素、子元素数量、属性，适合API测试、数据填充、XML解析验证。",
        "en_desc": "Free dummy XML data generator for quickly creating customizable XML test data. Custom root elements, child count, attributes — ideal for API testing and XML parsing validation.",
        "cn_keywords": "XML生成,测试数据,XML测试,假数据,API测试,XML工具",
        "en_keywords": "XML generator,test data,dummy XML,API testing,XML tool,mock data",
        "cn_faq": [
            ("生成的XML格式正确吗？","使用DOM API生成标准XML，保证格式正确、标签闭合。可直接复制用于测试。"),
            ("可以自定义XML结构吗？","可以设置根元素名称、子元素名称、记录数量、每条记录的字段。灵活适配不同测试场景。"),
            ("最多能生成多少条记录？","每次可生成1-100条记录，每条记录包含3-10个字段。生成内容完全在浏览器本地完成。")
        ],
        "en_faq": [
            ("Is the generated XML well-formed?","Yes, we use the DOM API to generate standard XML with proper tag closure. Ready to copy and use in tests."),
            ("Can I customize the XML structure?","Yes, set root element name, child element name, record count, and fields per record. Flexible for different test scenarios."),
            ("How many records can I generate?","Generate 1-100 records per batch, each with 3-10 fields. All generation happens locally in your browser.")
        ]
    },
    {
        "slug": "dummy-csv-generator",
        "cn_name": "测试CSV生成器",
        "en_name": "Dummy CSV Generator",
        "category": "dev",
        "cn_desc": "免费测试CSV数据生成器，快速生成可定制的CSV/TSV测试数据。自定义列名、行数、数据类型，支持导出下载，适合数据分析和导入测试。",
        "en_desc": "Free dummy CSV generator for customizable CSV/TSV test data. Custom columns, row count, data types, with export download — perfect for data analysis and import testing.",
        "cn_keywords": "CSV生成,测试数据,CSV测试,假数据,数据填充,CSV工具",
        "en_keywords": "CSV generator,test data,dummy CSV,mock data,data seeding,CSV tool",
        "cn_faq": [
            ("可以导出为文件吗？","可以。点击下载按钮即可将生成的CSV保存为.csv文件，支持UTF-8 BOM以确保Excel正确显示中文。"),
            ("支持哪些数据类型？","支持随机姓名、邮箱、电话号码、日期、数字、布尔值、UUID等常见测试数据类型。"),
            ("最多能生成多少行？","每次可生成1-1000行数据。生成完全在浏览器本地完成，不受服务器限制。")
        ],
        "en_faq": [
            ("Can I export as a file?","Yes, click the download button to save as a .csv file with UTF-8 BOM for correct Excel display."),
            ("What data types are supported?","Random names, emails, phone numbers, dates, numbers, booleans, UUIDs, and more common test data types."),
            ("How many rows can I generate?","Generate 1-1000 rows per batch. All generation happens locally in your browser with no server limits.")
        ]
    },
    {
        "slug": "fake-person-generator",
        "cn_name": "假数据人物生成器",
        "en_name": "Fake Person Generator",
        "category": "generator",
        "cn_desc": "免费假数据人物生成器，一键生成完整的虚拟人物档案。包含姓名、邮箱、电话、地址、公司、职业等，适合隐私保护和开发测试。",
        "en_desc": "Free fake person generator to create complete virtual profiles with one click. Includes name, email, phone, address, company, job — perfect for privacy and dev testing.",
        "cn_keywords": "假数据,人物生成,虚拟身份,测试数据,隐私保护,随机人物",
        "en_keywords": "fake data,person generator,virtual identity,test data,privacy,mock person",
        "cn_faq": [
            ("生成的人物信息是真实的吗？","否。所有数据随机生成，不与任何真实人物关联。请勿用于非法用途。"),
            ("包含哪些信息字段？","姓名、性别、邮箱、电话、地址、邮编、城市、国家、公司、职位、生日等完整档案。"),
            ("可以批量生成吗？","可以。每次生成1-20个完整人物档案，一键复制全部JSON格式数据。")
        ],
        "en_faq": [
            ("Are the generated profiles real?","No. All data is randomly generated and not associated with any real person. Do not use for illegal purposes."),
            ("What fields are included?","Name, gender, email, phone, address, ZIP, city, country, company, job title, birthday, and more."),
            ("Can I generate in bulk?","Yes, generate 1-20 complete profiles per batch, copy all as JSON with one click.")
        ]
    },
]

def build_tool_page(tool, lang="zh"):
    """生成工具页面HTML"""
    slug = tool["slug"]
    is_cn = lang == "zh"
    
    if is_cn:
        name = tool["cn_name"]
        desc = tool["cn_desc"]
        keywords = tool["cn_keywords"]
        faqs = tool["cn_faq"]
        lang_tag = "zh-CN"
        hreflang = "zh"
        canonical_slug = slug
        alt_slug = f"en/{slug}"
        home_path = "../"
        tools_path = "../#tools"
        lang_label = "中文"
        en_label = "EN"
        active_cn = "active"
        active_en = ""
        breadcrumb_name = name
        hero_text = f"免费{tool['cn_name']}，{tool['cn_desc'].split('。')[0]}。{tool['cn_desc'].split('。')[1] if '。' in tool['cn_desc'] else ''}"
        badge_text = "🔒 无需注册 · 数据绝不上传"
        generate_btn = "🎲 生成"
        copy_btn = "📋 一键复制"
        clear_btn = "🗑 清除"
        export_btn = "📥 下载"
        faq_title = "常见问题"
        privacy_text = "🔒 所有数据本地生成，使用密码学安全随机数，数据绝不上传服务器。"
        footer_line = f"{name} | 无需注册 · 数据绝不上传服务器"
        contact_text = "问题反馈: dexshuang@google.com"
    else:
        name = tool["en_name"]
        desc = tool["en_desc"]
        keywords = tool["en_keywords"]
        faqs = tool["en_faq"]
        lang_tag = "en"
        hreflang = "en"
        canonical_slug = f"en/{slug}"
        alt_slug = slug
        home_path = "../../"
        tools_path = "../../#tools"
        lang_label = "EN"
        en_label = "中文"
        active_cn = ""
        active_en = "active"
        breadcrumb_name = name
        hero_text = f"Free {tool['en_name']}. {tool['en_desc'].split('.')[0]}."
        badge_text = "🔒 No Registration · Data Never Uploaded"
        generate_btn = "🎲 Generate"
        copy_btn = "📋 Copy All"
        clear_btn = "🗑 Clear"
        export_btn = "📥 Download"
        faq_title = "FAQ"
        privacy_text = "🔒 All data is generated locally using cryptographically secure randomness. No data is ever uploaded to any server."
        footer_line = f"{name} | No Registration · Data Never Uploaded"
        contact_text = "Feedback: dexshuang@google.com"
    
    # Build FAQ items
    faq_html = ""
    for q, a in faqs:
        faq_html += f"""<div class="faq-item"><div class="faq-q">{q}</div><div class="faq-a">{a}</div></div>\n"""
    
    # Build Schema.org FAQ
    faq_schema_items = []
    for q, a in faqs:
        faq_schema_items.append(f'{{"@type":"Question","name":"{q}","acceptedAnswer":{{"@type":"Answer","text":"{a}"}}}}')
    faq_schema = ",".join(faq_schema_items)
    
    howto_steps = []
    for i, (q, _) in enumerate(faqs[:3]):
        howto_steps.append(f'{{"@type":"HowToStep","position":{i+1},"name":"{q.split("？")[0] if "？" in q else q.split("?")[0]}","text":"{q}"}}')
    howto_steps_json = ",".join(howto_steps)
    
    og_title = f"{name} | Free ToolBase" if not is_cn else f"{name} - Free ToolBase"
    
    html = f'''<!DOCTYPE html>
<html lang="{lang_tag}">
<head>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-9W1157EBQV"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-9W1157EBQV');</script>
<script>window.addEventListener("error",function(e){{if(e&&e.message===""){{e.preventDefault();}}}});window.addEventListener("unhandledrejection",function(e){{if(e&&e.reason&&e.reason.message===""){{e.preventDefault();}}}});</script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="{desc}">
<meta name="keywords" content="{keywords}">
<title>{name} | Free ToolBase</title>
<link rel="canonical" href="https://free-toolbase.com/{canonical_slug}/">
<meta property="og:title" content="{og_title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="https://free-toolbase.com/{canonical_slug}/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Free ToolBase">
<link rel="alternate" hreflang="zh" href="https://free-toolbase.com/{slug}/">
<link rel="alternate" hreflang="en" href="https://free-toolbase.com/en/{slug}/">
<link rel="alternate" hreflang="x-default" href="https://free-toolbase.com/en/{slug}/">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"SoftwareApplication","name":"{name}","description":"{desc}","applicationCategory":"UtilitiesApplication","operatingSystem":"Web","publisher":{{"@type":"Organization","name":"Free ToolBase","email":"dexshuang@google.com"}},"offers":{{"@type":"Offer","price":"0","priceCurrency":"USD"}}}}</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{faq_schema}]}}</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"HowTo","name":"如何使用{name}","description":"{name}使用步骤","totalTime":"PT1M","tool":{{"@type":"HowToTool","name":"{name}"}},"step":[{howto_steps_json}]}}</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"首页" if is_cn else "Home","item":"https://free-toolbase.com/"}},{{"@type":"ListItem","position":2,"name":"工具" if is_cn else "Tools","item":"https://free-toolbase.com/#tools"}},{{"@type":"ListItem","position":3,"name":"{name}","item":"https://free-toolbase.com/{canonical_slug}/"}}]}}</script>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}body{{background:#f8fafc;color:#1e293b;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"PingFang SC","Microsoft YaHei",sans-serif;line-height:1.6;min-height:100vh}}a{{color:#4F46E5;text-decoration:none}}.container{{max-width:960px;margin:0 auto;padding:24px 16px}}.header{{display:flex;justify-content:space-between;align-items:center;margin-bottom:20px;flex-wrap:wrap;gap:12px}}.header h1{{font-size:1.6rem}}.lang-switch{{display:flex;gap:4px;background:#fff;border-radius:8px;padding:4px;border:1px solid #e2e8f0}}.lang-switch a{{padding:6px 12px;border-radius:5px;font-size:.85rem;color:#64748b}}.lang-switch a.active{{background:#EEF2FF;color:#4F46E5;font-weight:600}}.nav-back{{color:#64748b;font-size:.85rem;margin-bottom:16px}}.nav-back a{{color:#64748b}}.nav-back a:hover{{color:#4F46E5}}.hero{{background:linear-gradient(135deg,#EEF2FF 0%,#E0E7FF 100%);border-radius:12px;padding:20px 24px;margin-bottom:20px;font-size:.95rem;color:#3730A3;line-height:1.7}}.hero .badge{{display:inline-block;background:#4F46E5;color:#fff;padding:3px 10px;border-radius:20px;font-size:.75rem;margin-top:8px}}.panel{{background:#fff;border-radius:12px;padding:20px;margin-bottom:16px;border:1px solid #e2e8f0;box-shadow:0 1px 3px rgba(0,0,0,.1)}}.panel-title{{font-size:1.1rem;margin-bottom:14px;font-weight:600}}.btn{{padding:8px 20px;border:none;border-radius:6px;font-size:.9rem;cursor:pointer;transition:all .2s;display:inline-flex;align-items:center;gap:6px}}.btn-primary{{background:#4F46E5;color:#fff}}.btn-primary:hover{{opacity:.9;transform:translateY(-1px)}}.btn-secondary{{background:#fff;color:#1e293b;border:1px solid #e2e8f0}}.btn-secondary:hover{{background:#f8fafc}}.btn-large{{padding:12px 32px;font-size:1.1rem;font-weight:600}}.btn-row{{display:flex;gap:8px;flex-wrap:wrap;margin-top:16px}}input,select,textarea{{padding:10px 12px;border:1px solid #e2e8f0;border-radius:8px;background:#fff;color:#1e293b;font-size:.9rem;width:100%}}input:focus,select:focus,textarea:focus{{outline:none;border-color:#4F46E5;box-shadow:0 0 0 3px rgba(79,70,229,.1)}}textarea{{min-height:120px;resize:vertical;font-family:monospace}}label{{font-weight:500;font-size:.85rem;display:block;margin-bottom:4px}}.result-area{{background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px;padding:12px;min-height:80px;max-height:400px;overflow-y:auto;font-family:monospace;font-size:.85rem;white-space:pre-wrap;word-break:break-all;line-height:1.8}}.privacy-note{{text-align:center;font-size:.85rem;color:#64748b;margin-bottom:16px;padding:12px;background:#EEF2FF;border-radius:8px}}.faq-item{{border-bottom:1px solid #f1f5f9;padding:14px 0}}.faq-item:last-child{{border-bottom:none}}.faq-q{{font-weight:600;margin-bottom:6px;color:#1e293b;cursor:pointer}}.faq-a{{color:#64748b;font-size:.9rem;line-height:1.7}}.footer{{margin-top:32px;padding:24px 16px;border-top:1px solid #e2e8f0;text-align:center;font-size:.85rem;color:#64748b}}.footer a{{margin:0 8px;color:#64748b}}.footer a:hover{{color:#4F46E5}}.toast{{position:fixed;bottom:24px;left:50%;transform:translateX(-50%);background:#1e293b;color:#fff;padding:10px 24px;border-radius:8px;font-size:.85rem;opacity:0;transition:opacity .3s;pointer-events:none;z-index:9999}}.toast.show{{opacity:1}}select{{appearance:auto}}.input-group{{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:16px}}.strength-bar{{height:8px;border-radius:4px;background:#e2e8f0;margin-top:8px;overflow:hidden}}.strength-fill{{height:100%;border-radius:4px;transition:width .3s,background .3s}}
</style>
</head>
<body>
<div class="container">
<div class="header"><h1>{name}</h1><div class="lang-switch"><a href="{home_path}{alt_slug}/" class="{active_cn}">{lang_label}</a><a href="{home_path}{alt_slug if is_cn else slug}/" class="{active_en}">{en_label}</a></div></div>
<p class="nav-back"><a href="{home_path}index.html">{'首页' if is_cn else 'Home'}</a> &rsaquo; <a href="{tools_path}">{'工具' if is_cn else 'Tools'}</a> &rsaquo; {breadcrumb_name}</p>
<div class="hero"><p>{hero_text} <span class="badge">{badge_text}</span></p></div>
'''

    # Tool-specific content section
    content_html = generate_tool_content(tool, is_cn)
    
    html += content_html
    
    html += f'''
<div class="privacy-note">{privacy_text}</div>
<div class="panel">
  <div class="panel-title">{'❓ ' if is_cn else ''}{faq_title}</div>
  {faq_html}
</div>
</div>
<div class="footer container">
<div style="margin-bottom:12px">
<a href="{home_path}index.html">{'首页' if is_cn else 'Home'}</a>
<a href="{tools_path}">{'全部工具' if is_cn else 'All Tools'}</a>
<a href="mailto:dexshuang@google.com">{'联系我们' if is_cn else 'Contact'}</a>
<a href="{home_path}privacy/">{'隐私政策' if is_cn else 'Privacy'}</a>
<a href="{home_path}terms/">{'服务条款' if is_cn else 'Terms'}</a>
<a href="{home_path}about/">{'关于我们' if is_cn else 'About'}</a>
<a href="{home_path}{alt_slug}/">{en_label}</a>
</div>
<p>{footer_line}</p>
<p style="margin-top:8px;color:#475569;font-size:.8rem">{contact_text}</p>
</div>
<div class="toast" id="toast"></div>
<script>function showToast(m){{var t=document.getElementById("toast");t.textContent=m;t.classList.add("show");setTimeout(function(){{t.classList.remove("show")}},3000)}}</script>
'''

    html += get_tool_script(tool, is_cn)
    html += '\n</body>\n</html>'
    
    return html


def generate_tool_content(tool, is_cn):
    """生成工具特有的交互内容"""
    slug = tool["slug"]
    
    if slug == "seo-title-generator":
        return generate_seo_title_gen(is_cn)
    elif slug == "domain-age-checker":
        return generate_domain_age(is_cn)
    elif slug == "random-username":
        return generate_username(is_cn)
    elif slug == "random-password":
        return generate_password(is_cn)
    elif slug == "diceware-passphrase":
        return generate_diceware(is_cn)
    elif slug == "random-email":
        return generate_email(is_cn)
    elif slug == "dummy-xml-generator":
        return generate_xml(is_cn)
    elif slug == "dummy-csv-generator":
        return generate_csv(is_cn)
    elif slug == "fake-person-generator":
        return generate_fake_person(is_cn)
    return ""


def generate_seo_title_gen(is_cn):
    if is_cn:
        return '''
<div class="panel">
  <div class="panel-title">⚙️ 设置</div>
  <div class="input-group">
    <div><label>主关键词</label><input type="text" id="keyword" placeholder="例如：在线图片压缩" value="在线图片压缩"></div>
    <div><label>修饰词（可选）</label><input type="text" id="modifier" placeholder="例如：免费、2026、最佳"></div>
  </div>
  <div class="btn-row">
    <button class="btn btn-primary btn-large" id="generateBtn">🎲 生成标题</button>
    <button class="btn btn-secondary" id="copyBtn">📋 复制最佳</button>
  </div>
</div>
<div class="panel">
  <div class="panel-title">📝 生成的标题</div>
  <div class="result-area" id="result">点击生成按钮获取SEO标题</div>
  <div style="margin-top:8px;font-size:.8rem;color:#64748b" id="stats"></div>
</div>'''
    else:
        return '''
<div class="panel">
  <div class="panel-title">⚙️ Settings</div>
  <div class="input-group">
    <div><label>Primary Keyword</label><input type="text" id="keyword" placeholder="e.g. online image compression" value="online image compression"></div>
    <div><label>Modifier (optional)</label><input type="text" id="modifier" placeholder="e.g. Free, 2026, Best"></div>
  </div>
  <div class="btn-row">
    <button class="btn btn-primary btn-large" id="generateBtn">🎲 Generate Titles</button>
    <button class="btn btn-secondary" id="copyBtn">📋 Copy Best</button>
  </div>
</div>
<div class="panel">
  <div class="panel-title">📝 Generated Titles</div>
  <div class="result-area" id="result">Click generate to get SEO titles</div>
  <div style="margin-top:8px;font-size:.8rem;color:#64748b" id="stats"></div>
</div>'''


def generate_domain_age(is_cn):
    if is_cn:
        return '''
<div class="panel">
  <div class="panel-title">🔍 查询域名</div>
  <div style="display:flex;gap:8px;flex-wrap:wrap">
    <input type="text" id="domainInput" placeholder="输入域名，如 example.com" style="flex:1;min-width:200px">
    <button class="btn btn-primary btn-large" id="checkBtn">🔍 查询年龄</button>
  </div>
</div>
<div class="panel">
  <div class="panel-title">📊 查询结果</div>
  <div class="result-area" id="result" style="font-family:-apple-system,BlinkMacSystemFont,sans-serif;font-size:.9rem">输入域名点击查询</div>
</div>'''
    else:
        return '''
<div class="panel">
  <div class="panel-title">🔍 Lookup Domain</div>
  <div style="display:flex;gap:8px;flex-wrap:wrap">
    <input type="text" id="domainInput" placeholder="Enter domain, e.g. example.com" style="flex:1;min-width:200px">
    <button class="btn btn-primary btn-large" id="checkBtn">🔍 Check Age</button>
  </div>
</div>
<div class="panel">
  <div class="panel-title">📊 Results</div>
  <div class="result-area" id="result" style="font-family:-apple-system,BlinkMacSystemFont,sans-serif;font-size:.9rem">Enter a domain and click check</div>
</div>'''


def generate_username(is_cn):
    if is_cn:
        return '''
<div class="panel">
  <div class="panel-title">⚙️ 设置</div>
  <div class="input-group">
    <div><label>风格</label><select id="style"><option value="cool">酷炫</option><option value="cute">可爱</option><option value="pro">专业</option><option value="gamer">游戏ID</option></select></div>
    <div><label>前缀（可选）</label><input type="text" id="prefix" placeholder="例如：Mr_"></div>
    <div><label>后缀（可选）</label><input type="text" id="suffix" placeholder="例如：_2026"></div>
    <div><label>数量</label><input type="number" id="count" value="10" min="1" max="100"></div>
  </div>
  <div class="btn-row">
    <button class="btn btn-primary btn-large" id="generateBtn">🎲 生成用户名</button>
    <button class="btn btn-secondary" id="copyBtn">📋 一键复制</button>
  </div>
</div>
<div class="panel">
  <div class="panel-title">👤 生成结果 (<span id="resultCount">0</span>)</div>
  <div class="result-area" id="result">点击生成按钮开始</div>
</div>'''
    else:
        return '''
<div class="panel">
  <div class="panel-title">⚙️ Settings</div>
  <div class="input-group">
    <div><label>Style</label><select id="style"><option value="cool">Cool</option><option value="cute">Cute</option><option value="pro">Professional</option><option value="gamer">Gamer ID</option></select></div>
    <div><label>Prefix (optional)</label><input type="text" id="prefix" placeholder="e.g. Mr_"></div>
    <div><label>Suffix (optional)</label><input type="text" id="suffix" placeholder="e.g. _2026"></div>
    <div><label>Count</label><input type="number" id="count" value="10" min="1" max="100"></div>
  </div>
  <div class="btn-row">
    <button class="btn btn-primary btn-large" id="generateBtn">🎲 Generate</button>
    <button class="btn btn-secondary" id="copyBtn">📋 Copy All</button>
  </div>
</div>
<div class="panel">
  <div class="panel-title">👤 Results (<span id="resultCount">0</span>)</div>
  <div class="result-area" id="result">Click generate to start</div>
</div>'''


def generate_password(is_cn):
    if is_cn:
        return '''
<div class="panel">
  <div class="panel-title">⚙️ 密码设置</div>
  <div class="input-group">
    <div><label>密码长度</label><input type="number" id="length" value="16" min="8" max="128"></div>
    <div><label>数量</label><input type="number" id="count" value="5" min="1" max="50"></div>
  </div>
  <div style="margin-top:12px;display:flex;gap:16px;flex-wrap:wrap">
    <label style="display:flex;align-items:center;gap:6px;font-weight:400"><input type="checkbox" id="useUpper" checked> 大写字母</label>
    <label style="display:flex;align-items:center;gap:6px;font-weight:400"><input type="checkbox" id="useLower" checked> 小写字母</label>
    <label style="display:flex;align-items:center;gap:6px;font-weight:400"><input type="checkbox" id="useDigits" checked> 数字</label>
    <label style="display:flex;align-items:center;gap:6px;font-weight:400"><input type="checkbox" id="useSymbols" checked> 特殊符号</label>
  </div>
  <div class="btn-row">
    <button class="btn btn-primary btn-large" id="generateBtn">🎲 生成密码</button>
    <button class="btn btn-secondary" id="copyBtn">📋 一键复制</button>
    <button class="btn btn-secondary" id="refreshBtn">🔄 重新生成</button>
  </div>
</div>
<div class="panel">
  <div class="panel-title">🔑 生成结果</div>
  <div class="result-area" id="result">点击生成按钮开始</div>
  <div class="strength-bar"><div class="strength-fill" id="strengthBar" style="width:0"></div></div>
  <div style="margin-top:4px;font-size:.8rem;color:#64748b" id="strengthLabel"></div>
</div>'''
    else:
        return '''
<div class="panel">
  <div class="panel-title">⚙️ Password Settings</div>
  <div class="input-group">
    <div><label>Length</label><input type="number" id="length" value="16" min="8" max="128"></div>
    <div><label>Count</label><input type="number" id="count" value="5" min="1" max="50"></div>
  </div>
  <div style="margin-top:12px;display:flex;gap:16px;flex-wrap:wrap">
    <label style="display:flex;align-items:center;gap:6px;font-weight:400"><input type="checkbox" id="useUpper" checked> Uppercase</label>
    <label style="display:flex;align-items:center;gap:6px;font-weight:400"><input type="checkbox" id="useLower" checked> Lowercase</label>
    <label style="display:flex;align-items:center;gap:6px;font-weight:400"><input type="checkbox" id="useDigits" checked> Digits</label>
    <label style="display:flex;align-items:center;gap:6px;font-weight:400"><input type="checkbox" id="useSymbols" checked> Symbols</label>
  </div>
  <div class="btn-row">
    <button class="btn btn-primary btn-large" id="generateBtn">🎲 Generate</button>
    <button class="btn btn-secondary" id="copyBtn">📋 Copy All</button>
    <button class="btn btn-secondary" id="refreshBtn">🔄 Regenerate</button>
  </div>
</div>
<div class="panel">
  <div class="panel-title">🔑 Results</div>
  <div class="result-area" id="result">Click generate to start</div>
  <div class="strength-bar"><div class="strength-fill" id="strengthBar" style="width:0"></div></div>
  <div style="margin-top:4px;font-size:.8rem;color:#64748b" id="strengthLabel"></div>
</div>'''


def generate_diceware(is_cn):
    if is_cn:
        return '''
<div class="panel">
  <div class="panel-title">⚙️ 口令设置</div>
  <div class="input-group">
    <div><label>单词数量</label><select id="wordCount"><option value="4">4 个 (~51位熵)</option><option value="5">5 个 (~64位熵)</option><option value="6" selected>6 个 (~77位熵, 推荐)</option><option value="7">7 个 (~90位熵)</option><option value="8">8 个 (~103位熵)</option><option value="10">10 个 (~129位熵)</option></select></div>
    <div><label>分隔符</label><select id="separator"><option value="-">短横线 -</option><option value=" ">空格</option><option value=".">句点 .</option><option value="_">下划线 _</option></select></div>
    <div><label>数量</label><input type="number" id="count" value="5" min="1" max="20"></div>
  </div>
  <div class="btn-row">
    <button class="btn btn-primary btn-large" id="generateBtn">🎲 生成口令</button>
    <button class="btn btn-secondary" id="copyBtn">📋 一键复制</button>
  </div>
</div>
<div class="panel">
  <div class="panel-title">🔐 生成的口令</div>
  <div class="result-area" id="result">点击生成按钮开始</div>
</div>'''
    else:
        return '''
<div class="panel">
  <div class="panel-title">⚙️ Passphrase Settings</div>
  <div class="input-group">
    <div><label>Word Count</label><select id="wordCount"><option value="4">4 words (~51 bits)</option><option value="5">5 words (~64 bits)</option><option value="6" selected>6 words (~77 bits, recommended)</option><option value="7">7 words (~90 bits)</option><option value="8">8 words (~103 bits)</option><option value="10">10 words (~129 bits)</option></select></div>
    <div><label>Separator</label><select id="separator"><option value="-">Dash -</option><option value=" ">Space</option><option value=".">Period .</option><option value="_">Underscore _</option></select></div>
    <div><label>Count</label><input type="number" id="count" value="5" min="1" max="20"></div>
  </div>
  <div class="btn-row">
    <button class="btn btn-primary btn-large" id="generateBtn">🎲 Generate</button>
    <button class="btn btn-secondary" id="copyBtn">📋 Copy All</button>
  </div>
</div>
<div class="panel">
  <div class="panel-title">🔐 Generated Passphrases</div>
  <div class="result-area" id="result">Click generate to start</div>
</div>'''


def generate_email(is_cn):
    if is_cn:
        return '''
<div class="panel">
  <div class="panel-title">⚙️ 设置</div>
  <div class="input-group">
    <div><label>邮箱服务商</label><select id="provider"><option value="random">随机</option><option value="gmail.com">Gmail</option><option value="outlook.com">Outlook</option><option value="yahoo.com">Yahoo</option><option value="proton.me">Proton</option><option value="custom">自定义</option></select></div>
    <div><label>自定义域名</label><input type="text" id="customDomain" placeholder="例如：mycompany.com" disabled></div>
    <div><label>数量</label><input type="number" id="count" value="10" min="1" max="100"></div>
  </div>
  <div class="btn-row">
    <button class="btn btn-primary btn-large" id="generateBtn">🎲 生成邮箱</button>
    <button class="btn btn-secondary" id="copyBtn">📋 一键复制</button>
  </div>
</div>
<div class="panel">
  <div class="panel-title">📧 生成结果 (<span id="resultCount">0</span>)</div>
  <div class="result-area" id="result">点击生成按钮开始</div>
</div>'''
    else:
        return '''
<div class="panel">
  <div class="panel-title">⚙️ Settings</div>
  <div class="input-group">
    <div><label>Provider</label><select id="provider"><option value="random">Random</option><option value="gmail.com">Gmail</option><option value="outlook.com">Outlook</option><option value="yahoo.com">Yahoo</option><option value="proton.me">Proton</option><option value="custom">Custom</option></select></div>
    <div><label>Custom Domain</label><input type="text" id="customDomain" placeholder="e.g. mycompany.com" disabled></div>
    <div><label>Count</label><input type="number" id="count" value="10" min="1" max="100"></div>
  </div>
  <div class="btn-row">
    <button class="btn btn-primary btn-large" id="generateBtn">🎲 Generate</button>
    <button class="btn btn-secondary" id="copyBtn">📋 Copy All</button>
  </div>
</div>
<div class="panel">
  <div class="panel-title">📧 Results (<span id="resultCount">0</span>)</div>
  <div class="result-area" id="result">Click generate to start</div>
</div>'''


def generate_xml(is_cn):
    if is_cn:
        return '''
<div class="panel">
  <div class="panel-title">⚙️ XML设置</div>
  <div class="input-group">
    <div><label>根元素名称</label><input type="text" id="rootName" value="users"></div>
    <div><label>子元素名称</label><input type="text" id="childName" value="user"></div>
    <div><label>记录数量</label><input type="number" id="recordCount" value="5" min="1" max="100"></div>
  </div>
  <div class="btn-row">
    <button class="btn btn-primary btn-large" id="generateBtn">🎲 生成XML</button>
    <button class="btn btn-secondary" id="copyBtn">📋 复制</button>
    <button class="btn btn-secondary" id="downloadBtn">📥 下载</button>
  </div>
</div>
<div class="panel">
  <div class="panel-title">📄 生成的XML</div>
  <textarea id="result" readonly style="min-height:300px;font-family:monospace;font-size:.85rem">点击生成按钮获取XML数据</textarea>
</div>'''
    else:
        return '''
<div class="panel">
  <div class="panel-title">⚙️ XML Settings</div>
  <div class="input-group">
    <div><label>Root Element</label><input type="text" id="rootName" value="users"></div>
    <div><label>Child Element</label><input type="text" id="childName" value="user"></div>
    <div><label>Record Count</label><input type="number" id="recordCount" value="5" min="1" max="100"></div>
  </div>
  <div class="btn-row">
    <button class="btn btn-primary btn-large" id="generateBtn">🎲 Generate XML</button>
    <button class="btn btn-secondary" id="copyBtn">📋 Copy</button>
    <button class="btn btn-secondary" id="downloadBtn">📥 Download</button>
  </div>
</div>
<div class="panel">
  <div class="panel-title">📄 Generated XML</div>
  <textarea id="result" readonly style="min-height:300px;font-family:monospace;font-size:.85rem">Click generate to get XML data</textarea>
</div>'''


def generate_csv(is_cn):
    if is_cn:
        return '''
<div class="panel">
  <div class="panel-title">⚙️ CSV设置</div>
  <div class="input-group">
    <div><label>行数</label><input type="number" id="rowCount" value="20" min="1" max="1000"></div>
    <div><label>分隔符</label><select id="delimiter"><option value=",">逗号 (,)</option><option value="\t">制表符 (TSV)</option><option value=";">分号 (;)</option></select></div>
    <div><label>数据类型</label><select id="dataType"><option value="mixed">混合</option><option value="names">姓名</option><option value="emails">邮箱</option><option value="numbers">数字</option></select></div>
  </div>
  <div class="btn-row">
    <button class="btn btn-primary btn-large" id="generateBtn">🎲 生成CSV</button>
    <button class="btn btn-secondary" id="copyBtn">📋 复制</button>
    <button class="btn btn-secondary" id="downloadBtn">📥 下载CSV</button>
  </div>
</div>
<div class="panel">
  <div class="panel-title">📊 生成的CSV</div>
  <textarea id="result" readonly style="min-height:250px;font-family:monospace;font-size:.85rem">点击生成按钮获取CSV数据</textarea>
</div>'''
    else:
        return '''
<div class="panel">
  <div class="panel-title">⚙️ CSV Settings</div>
  <div class="input-group">
    <div><label>Rows</label><input type="number" id="rowCount" value="20" min="1" max="1000"></div>
    <div><label>Delimiter</label><select id="delimiter"><option value=",">Comma (,)</option><option value="\t">Tab (TSV)</option><option value=";">Semicolon (;)</option></select></div>
    <div><label>Data Type</label><select id="dataType"><option value="mixed">Mixed</option><option value="names">Names</option><option value="emails">Emails</option><option value="numbers">Numbers</option></select></div>
  </div>
  <div class="btn-row">
    <button class="btn btn-primary btn-large" id="generateBtn">🎲 Generate CSV</button>
    <button class="btn btn-secondary" id="copyBtn">📋 Copy</button>
    <button class="btn btn-secondary" id="downloadBtn">📥 Download CSV</button>
  </div>
</div>
<div class="panel">
  <div class="panel-title">📊 Generated CSV</div>
  <textarea id="result" readonly style="min-height:250px;font-family:monospace;font-size:.85rem">Click generate to get CSV data</textarea>
</div>'''


def generate_fake_person(is_cn):
    if is_cn:
        return '''
<div class="panel">
  <div class="panel-title">⚙️ 设置</div>
  <div class="input-group">
    <div><label>性别</label><select id="gender"><option value="random">随机</option><option value="male">男</option><option value="female">女</option></select></div>
    <div><label>国家</label><select id="country"><option value="CN">中国</option><option value="US">美国</option><option value="UK">英国</option><option value="random">随机</option></select></div>
    <div><label>数量</label><input type="number" id="count" value="1" min="1" max="20"></div>
  </div>
  <div class="btn-row">
    <button class="btn btn-primary btn-large" id="generateBtn">🎲 生成人物</button>
    <button class="btn btn-secondary" id="copyBtn">📋 复制JSON</button>
  </div>
</div>
<div class="panel">
  <div class="panel-title">👤 生成结果</div>
  <textarea id="result" readonly style="min-height:250px;font-family:monospace;font-size:.85rem">点击生成按钮获取人物数据</textarea>
</div>'''
    else:
        return '''
<div class="panel">
  <div class="panel-title">⚙️ Settings</div>
  <div class="input-group">
    <div><label>Gender</label><select id="gender"><option value="random">Random</option><option value="male">Male</option><option value="female">Female</option></select></div>
    <div><label>Country</label><select id="country"><option value="US">United States</option><option value="UK">United Kingdom</option><option value="CN">China</option><option value="random">Random</option></select></div>
    <div><label>Count</label><input type="number" id="count" value="1" min="1" max="20"></div>
  </div>
  <div class="btn-row">
    <button class="btn btn-primary btn-large" id="generateBtn">🎲 Generate</button>
    <button class="btn btn-secondary" id="copyBtn">📋 Copy JSON</button>
  </div>
</div>
<div class="panel">
  <div class="panel-title">👤 Results</div>
  <textarea id="result" readonly style="min-height:250px;font-family:monospace;font-size:.85rem">Click generate to get person data</textarea>
</div>'''


def get_tool_script(tool, is_cn):
    """返回工具特定的JS"""
    slug = tool["slug"]
    
    if slug == "seo-title-generator":
        return get_seo_title_script(is_cn)
    elif slug == "domain-age-checker":
        return get_domain_age_script(is_cn)
    elif slug == "random-username":
        return get_username_script(is_cn)
    elif slug == "random-password":
        return get_password_script(is_cn)
    elif slug == "diceware-passphrase":
        return get_diceware_script(is_cn)
    elif slug == "random-email":
        return get_email_script(is_cn)
    elif slug == "dummy-xml-generator":
        return get_xml_script(is_cn)
    elif slug == "dummy-csv-generator":
        return get_csv_script(is_cn)
    elif slug == "fake-person-generator":
        return get_fake_person_script(is_cn)
    return ""


def get_seo_title_script(is_cn):
    if is_cn:
        return '''
<script>
'use strict';
var modifiers=["免费","在线","2026","最佳","终极","完整","快速","简单","实用","专业","高级","全面","最新","推荐","必备"];
var formats=["{keyword} - {modifier}工具 | Free ToolBase","{modifier}{keyword} - 免费在线使用","{keyword} | {modifier}指南 ({year})","{keyword}在线 - {modifier}解决方案","{modifier}{keyword} - 一键搞定 | Free ToolBase"];

document.getElementById("generateBtn").addEventListener("click",function(){
  var kw=document.getElementById("keyword").value.trim();
  var mod=document.getElementById("modifier").value.trim();
  if(!kw){showToast("请输入关键词");return;}
  var results=[];
  for(var i=0;i<8;i++){
    var m=mod||modifiers[Math.floor(Math.random()*modifiers.length)];
    var fmt=formats[Math.floor(Math.random()*formats.length)];
    var title=fmt.replace("{keyword}",kw).replace("{modifier}",m).replace("{year}","2026");
    var len=title.length;
    var status=len>=50&&len<=60?"✅ 最佳":len<50?"⚠️ 偏短":"⚠️ 偏长";
    results.push({title:title,len:len,status:status});
  }
  results.sort(function(a,b){return Math.abs(a.len-55)-Math.abs(b.len-55)});
  var html="";
  for(var i=0;i<results.length;i++){
    var r=results[i];
    html+='<div style="padding:8px 0;border-bottom:1px solid #f1f5f9"><span style="color:#4F46E5;font-weight:600">'+(i+1)+'.</span> '+r.title+' <span style="font-size:.75rem;color:#64748b">('+r.len+'字 '+r.status+')</span></div>';
  }
  document.getElementById("result").innerHTML=html;
  document.getElementById("stats").textContent="共生成 "+results.length+" 个标题，按最佳长度排序";
});
document.getElementById("copyBtn").addEventListener("click",function(){
  var best=document.getElementById("result").querySelector("div");
  if(!best){showToast("请先生成标题");return;}
  var text=best.textContent.replace(/^\\d+\\.\\s*/,"").replace(/\\s*\\(\\d+字.*\\)$/,"");
  navigator.clipboard.writeText(text).then(function(){showToast("已复制最佳标题")});
});
</script>'''
    else:
        return '''
<script>
'use strict';
var modifiers=["Free","Online","2026","Best","Ultimate","Complete","Quick","Easy","Professional","Advanced","Latest","Top","Essential"];
var formats=["{keyword} - {modifier} Tool | Free ToolBase","{modifier} {keyword} - Free Online Tool","{keyword} | The {modifier} Guide ({year})","{keyword} Online - {modifier} Solution","{modifier} {keyword} - One Click | Free ToolBase"];

document.getElementById("generateBtn").addEventListener("click",function(){
  var kw=document.getElementById("keyword").value.trim();
  var mod=document.getElementById("modifier").value.trim();
  if(!kw){showToast("Please enter a keyword");return;}
  var results=[];
  for(var i=0;i<8;i++){
    var m=mod||modifiers[Math.floor(Math.random()*modifiers.length)];
    var fmt=formats[Math.floor(Math.random()*formats.length)];
    var title=fmt.replace("{keyword}",kw).replace("{modifier}",m).replace("{year}","2026");
    var len=title.length;
    var status=len>=50&&len<=60?"✅ Optimal":len<50?"⚠️ Too Short":"⚠️ Too Long";
    results.push({title:title,len:len,status:status});
  }
  results.sort(function(a,b){return Math.abs(a.len-55)-Math.abs(b.len-55)});
  var html="";
  for(var i=0;i<results.length;i++){
    var r=results[i];
    html+='<div style="padding:8px 0;border-bottom:1px solid #f1f5f9"><span style="color:#4F46E5;font-weight:600">'+(i+1)+'.</span> '+r.title+' <span style="font-size:.75rem;color:#64748b">('+r.len+' chars '+r.status+')</span></div>';
  }
  document.getElementById("result").innerHTML=html;
  document.getElementById("stats").textContent=results.length+" titles generated, sorted by optimal length";
});
document.getElementById("copyBtn").addEventListener("click",function(){
  var best=document.getElementById("result").querySelector("div");
  if(!best){showToast("Please generate titles first");return;}
  var text=best.textContent.replace(/^\\d+\\.\\s*/,"").replace(/\\s*\\(\\d+ chars.*\\)$/,"");
  navigator.clipboard.writeText(text).then(function(){showToast("Best title copied!")});
});
</script>'''


def get_domain_age_script(is_cn):
    if is_cn:
        return '''
<script>
'use strict';
document.getElementById("checkBtn").addEventListener("click",function(){
  var domain=document.getElementById("domainInput").value.trim().toLowerCase().replace(/^https?:\\/\\//,"").replace(/\\/.*$/,"").replace(/^www\\./,"");
  if(!domain||!domain.includes(".")){showToast("请输入有效域名");return;}
  var result=document.getElementById("result");
  result.innerHTML='<div style="text-align:center;padding:20px">⏳ 正在查询...</div>';
  // Simulate WHOIS via public API
  fetch("https://rdap.verisign.com/com/v1/domain/"+domain)
    .then(function(r){return r.json()})
    .then(function(data){
      var events=data.events||[];
      var created="",expires="";
      for(var i=0;i<events.length;i++){
        if(events[i].eventAction==="registration")created=events[i].eventDate;
        if(events[i].eventAction==="expiration")expires=events[i].eventDate;
      }
      if(!created){
        // Try alternative
        return fetch("https://rdap.org/domain/"+domain).then(function(r){return r.json()});
      }
      return data;
    })
    .then(function(data){
      var events=data.events||[];
      var created="",expires="",updated="";
      for(var i=0;i<events.length;i++){
        if(events[i].eventAction==="registration")created=events[i].eventDate;
        if(events[i].eventAction==="expiration")expires=events[i].eventDate;
        if(events[i].eventAction==="last changed")updated=events[i].eventDate;
      }
      var createdDate=created?new Date(created):null;
      var expiresDate=expires?new Date(expires):null;
      if(!createdDate){
        result.innerHTML='<div style="color:#dc2626">⚠️ 无法获取域名信息。该域名可能不支持WHOIS查询，或输入格式不正确。</div>';
        return;
      }
      var now=new Date();
      var ageYears=Math.floor((now-createdDate)/(365.25*24*60*60*1000));
      var ageDays=Math.floor((now-createdDate)/(24*60*60*1000));
      var remaining=expiresDate?Math.ceil((expiresDate-now)/(24*60*60*1000)):null;
      result.innerHTML=
        '<div style="display:grid;grid-template-columns:1fr 1fr;gap:16px">'+
        '<div><strong>域名</strong><br>'+domain+'</div>'+
        '<div><strong>注册时间</strong><br>'+createdDate.toISOString().split("T")[0]+'</div>'+
        '<div><strong>域名年龄</strong><br><span style="color:#4F46E5;font-size:1.2rem;font-weight:700">'+ageYears+' 年 ('+ageDays+' 天)</span></div>'+
        (expiresDate?'<div><strong>到期时间</strong><br>'+expiresDate.toISOString().split("T")[0]+(remaining>0?' ('+remaining+'天后)':' (已过期)')+'</div>':'')+
        (data.name?'<div><strong>注册商</strong><br>'+data.name+'</div>':'')+
        '</div>';
    })
    .catch(function(e){
      result.innerHTML='<div style="color:#dc2626">⚠️ 查询失败: '+e.message+'。请检查域名格式或稍后重试。</div>';
    });
});
</script>'''
    else:
        return '''
<script>
'use strict';
document.getElementById("checkBtn").addEventListener("click",function(){
  var domain=document.getElementById("domainInput").value.trim().toLowerCase().replace(/^https?:\\/\\//,"").replace(/\\/.*$/,"").replace(/^www\\./,"");
  if(!domain||!domain.includes(".")){showToast("Please enter a valid domain");return;}
  var result=document.getElementById("result");
  result.innerHTML='<div style="text-align:center;padding:20px">⏳ Looking up...</div>';
  fetch("https://rdap.verisign.com/com/v1/domain/"+domain)
    .then(function(r){return r.json()})
    .then(function(data){
      var events=data.events||[];
      var created="",expires="";
      for(var i=0;i<events.length;i++){
        if(events[i].eventAction==="registration")created=events[i].eventDate;
        if(events[i].eventAction==="expiration")expires=events[i].eventDate;
      }
      if(!created){
        return fetch("https://rdap.org/domain/"+domain).then(function(r){return r.json()});
      }
      return data;
    })
    .then(function(data){
      var events=data.events||[];
      var created="",expires="";
      for(var i=0;i<events.length;i++){
        if(events[i].eventAction==="registration")created=events[i].eventDate;
        if(events[i].eventAction==="expiration")expires=events[i].eventDate;
      }
      var createdDate=created?new Date(created):null;
      var expiresDate=expires?new Date(expires):null;
      if(!createdDate){
        result.innerHTML='<div style="color:#dc2626">⚠️ Unable to retrieve domain info. The domain may not support WHOIS queries.</div>';
        return;
      }
      var now=new Date();
      var ageYears=Math.floor((now-createdDate)/(365.25*24*60*60*1000));
      var ageDays=Math.floor((now-createdDate)/(24*60*60*1000));
      var remaining=expiresDate?Math.ceil((expiresDate-now)/(24*60*60*1000)):null;
      result.innerHTML=
        '<div style="display:grid;grid-template-columns:1fr 1fr;gap:16px">'+
        '<div><strong>Domain</strong><br>'+domain+'</div>'+
        '<div><strong>Registered</strong><br>'+createdDate.toISOString().split("T")[0]+'</div>'+
        '<div><strong>Age</strong><br><span style="color:#4F46E5;font-size:1.2rem;font-weight:700">'+ageYears+' years ('+ageDays+' days)</span></div>'+
        (expiresDate?'<div><strong>Expires</strong><br>'+expiresDate.toISOString().split("T")[0]+(remaining>0?' ('+remaining+' days)':' (Expired)')+'</div>':'')+
        (data.name?'<div><strong>Registrar</strong><br>'+data.name+'</div>':'')+
        '</div>';
    })
    .catch(function(e){
      result.innerHTML='<div style="color:#dc2626">⚠️ Lookup failed: '+e.message+'. Please check the domain format and try again.</div>';
    });
});
</script>'''


def get_username_script(is_cn):
    if is_cn:
        return '''
<script>
'use strict';
var coolWords=["Shadow","Blaze","Storm","Frost","Phantom","Nova","Zenith","Vortex","Cyber","Neon","Cipher","Kraken","Titan","Onyx","Raven","Phoenix","Rogue","Apex","Havoc","Spectre"];
var cuteWords=["Bunny","Kitty","Panda","Mochi","Peach","Candy","Star","Moon","Cloud","Berry","Daisy","Luna","Bubbles","Cupcake","Cookie","Sunny","Fluffy","Sparkle","Twinkle","Mint"];
var proWords=["Alex","Morgan","Taylor","Jordan","Casey","Riley","Quinn","Avery","Blake","Drew","Parker","Hayden","Reese","Finley","Rowan","Sage","Cameron","Dakota","Emery","Skyler"];
var gamerWords=["Slayer","Sniper","Warlord","Destroyer","Predator","Assassin","Gladiator","Berserker","Marauder","Reaper","Vanguard","Sentinel","Juggernaut","Warden","Executioner","Annihilator","Overlord","Dominator","Vanquisher","Obliterator"];

function getWords(style){
  if(style==="cool")return coolWords;
  if(style==="cute")return cuteWords;
  if(style==="pro")return proWords;
  return gamerWords;
}

document.getElementById("generateBtn").addEventListener("click",function(){
  var style=document.getElementById("style").value;
  var prefix=document.getElementById("prefix").value.trim();
  var suffix=document.getElementById("suffix").value.trim();
  var count=parseInt(document.getElementById("count").value)||10;
  var words=getWords(style);
  var used={};
  var results=[];
  var arr=new Uint32Array(4);
  while(results.length<count&&results.length<words.length*100){
    crypto.getRandomValues(arr);
    var w1=words[arr[0]%words.length];
    var w2=words[arr[1]%words.length];
    var num=arr[2]%10000;
    var name=(w1!==w2)?w1+w2:w1+"_"+num;
    if(prefix)name=prefix+name;
    if(suffix)name=name+suffix;
    if(!used[name]){used[name]=true;results.push(name);}
  }
  document.getElementById("result").textContent=results.join("\\n");
  document.getElementById("resultCount").textContent=results.length;
});
document.getElementById("copyBtn").addEventListener("click",function(){
  var text=document.getElementById("result").textContent;
  if(!text||text==="点击生成按钮开始"){showToast("请先生成用户名");return;}
  navigator.clipboard.writeText(text).then(function(){showToast("已复制全部用户名")});
});
</script>'''
    else:
        return '''
<script>
'use strict';
var coolWords=["Shadow","Blaze","Storm","Frost","Phantom","Nova","Zenith","Vortex","Cyber","Neon","Cipher","Kraken","Titan","Onyx","Raven","Phoenix","Rogue","Apex","Havoc","Spectre"];
var cuteWords=["Bunny","Kitty","Panda","Mochi","Peach","Candy","Star","Moon","Cloud","Berry","Daisy","Luna","Bubbles","Cupcake","Cookie","Sunny","Fluffy","Sparkle","Twinkle","Mint"];
var proWords=["Alex","Morgan","Taylor","Jordan","Casey","Riley","Quinn","Avery","Blake","Drew","Parker","Hayden","Reese","Finley","Rowan","Sage","Cameron","Dakota","Emery","Skyler"];
var gamerWords=["Slayer","Sniper","Warlord","Destroyer","Predator","Assassin","Gladiator","Berserker","Marauder","Reaper","Vanguard","Sentinel","Juggernaut","Warden","Executioner","Annihilator","Overlord","Dominator","Vanquisher","Obliterator"];

function getWords(style){
  if(style==="cool")return coolWords;
  if(style==="cute")return cuteWords;
  if(style==="pro")return proWords;
  return gamerWords;
}

document.getElementById("generateBtn").addEventListener("click",function(){
  var style=document.getElementById("style").value;
  var prefix=document.getElementById("prefix").value.trim();
  var suffix=document.getElementById("suffix").value.trim();
  var count=parseInt(document.getElementById("count").value)||10;
  var words=getWords(style);
  var used={};
  var results=[];
  var arr=new Uint32Array(4);
  while(results.length<count&&results.length<words.length*100){
    crypto.getRandomValues(arr);
    var w1=words[arr[0]%words.length];
    var w2=words[arr[1]%words.length];
    var num=arr[2]%10000;
    var name=(w1!==w2)?w1+w2:w1+"_"+num;
    if(prefix)name=prefix+name;
    if(suffix)name=name+suffix;
    if(!used[name]){used[name]=true;results.push(name);}
  }
  document.getElementById("result").textContent=results.join("\\n");
  document.getElementById("resultCount").textContent=results.length;
});
document.getElementById("copyBtn").addEventListener("click",function(){
  var text=document.getElementById("result").textContent;
  if(!text||text==="Click generate to start"){showToast("Please generate usernames first");return;}
  navigator.clipboard.writeText(text).then(function(){showToast("All usernames copied!")});
});
</script>'''


def get_password_script(is_cn):
    if is_cn:
        return '''
<script>
'use strict';
function generatePassword(){
  var length=parseInt(document.getElementById("length").value)||16;
  var useUpper=document.getElementById("useUpper").checked;
  var useLower=document.getElementById("useLower").checked;
  var useDigits=document.getElementById("useDigits").checked;
  var useSymbols=document.getElementById("useSymbols").checked;
  var count=parseInt(document.getElementById("count").value)||5;
  var upper="ABCDEFGHIJKLMNOPQRSTUVWXYZ";
  var lower="abcdefghijklmnopqrstuvwxyz";
  var digits="0123456789";
  var symbols="!@#$%^&*()_+-=[]{}|;:,.<>?";
  var charset="";
  if(useUpper)charset+=upper;
  if(useLower)charset+=lower;
  if(useDigits)charset+=digits;
  if(useSymbols)charset+=symbols;
  if(!charset){showToast("请至少选择一种字符类型");return;}
  var arr=new Uint32Array(length*count);
  crypto.getRandomValues(arr);
  var results=[];
  for(var i=0;i<count;i++){
    var pwd="";
    for(var j=0;j<length;j++){pwd+=charset[arr[i*length+j]%charset.length];}
    results.push(pwd);
  }
  document.getElementById("result").textContent=results.join("\\n");
  updateStrength(results[0]||"");
}
function updateStrength(pwd){
  var score=0;
  if(pwd.length>=12)score+=2;
  else if(pwd.length>=8)score+=1;
  if(/[a-z]/.test(pwd))score++;
  if(/[A-Z]/.test(pwd))score++;
  if(/[0-9]/.test(pwd))score++;
  if(/[^a-zA-Z0-9]/.test(pwd))score++;
  var pct=Math.min(score*16,100);
  var bar=document.getElementById("strengthBar");
  var label=document.getElementById("strengthLabel");
  bar.style.width=pct+"%";
  if(score<=2){bar.style.background="#dc2626";label.textContent="强度: 弱";}
  else if(score<=4){bar.style.background="#f59e0b";label.textContent="强度: 中等";}
  else if(score<=5){bar.style.background="#10b981";label.textContent="强度: 强";}
  else{bar.style.background="#059669";label.textContent="强度: 非常强";}
}
document.getElementById("generateBtn").addEventListener("click",generatePassword);
document.getElementById("refreshBtn").addEventListener("click",generatePassword);
document.getElementById("copyBtn").addEventListener("click",function(){
  var text=document.getElementById("result").textContent;
  if(!text||text==="点击生成按钮开始"){showToast("请先生成密码");return;}
  navigator.clipboard.writeText(text).then(function(){showToast("已复制全部密码")});
});
generatePassword();
</script>'''
    else:
        return '''
<script>
'use strict';
function generatePassword(){
  var length=parseInt(document.getElementById("length").value)||16;
  var useUpper=document.getElementById("useUpper").checked;
  var useLower=document.getElementById("useLower").checked;
  var useDigits=document.getElementById("useDigits").checked;
  var useSymbols=document.getElementById("useSymbols").checked;
  var count=parseInt(document.getElementById("count").value)||5;
  var upper="ABCDEFGHIJKLMNOPQRSTUVWXYZ";
  var lower="abcdefghijklmnopqrstuvwxyz";
  var digits="0123456789";
  var symbols="!@#$%^&*()_+-=[]{}|;:,.<>?";
  var charset="";
  if(useUpper)charset+=upper;
  if(useLower)charset+=lower;
  if(useDigits)charset+=digits;
  if(useSymbols)charset+=symbols;
  if(!charset){showToast("Please select at least one character type");return;}
  var arr=new Uint32Array(length*count);
  crypto.getRandomValues(arr);
  var results=[];
  for(var i=0;i<count;i++){
    var pwd="";
    for(var j=0;j<length;j++){pwd+=charset[arr[i*length+j]%charset.length];}
    results.push(pwd);
  }
  document.getElementById("result").textContent=results.join("\\n");
  updateStrength(results[0]||"");
}
function updateStrength(pwd){
  var score=0;
  if(pwd.length>=12)score+=2;
  else if(pwd.length>=8)score+=1;
  if(/[a-z]/.test(pwd))score++;
  if(/[A-Z]/.test(pwd))score++;
  if(/[0-9]/.test(pwd))score++;
  if(/[^a-zA-Z0-9]/.test(pwd))score++;
  var pct=Math.min(score*16,100);
  var bar=document.getElementById("strengthBar");
  var label=document.getElementById("strengthLabel");
  bar.style.width=pct+"%";
  if(score<=2){bar.style.background="#dc2626";label.textContent="Strength: Weak";}
  else if(score<=4){bar.style.background="#f59e0b";label.textContent="Strength: Moderate";}
  else if(score<=5){bar.style.background="#10b981";label.textContent="Strength: Strong";}
  else{bar.style.background="#059669";label.textContent="Strength: Very Strong";}
}
document.getElementById("generateBtn").addEventListener("click",generatePassword);
document.getElementById("refreshBtn").addEventListener("click",generatePassword);
document.getElementById("copyBtn").addEventListener("click",function(){
  var text=document.getElementById("result").textContent;
  if(!text||text==="Click generate to start"){showToast("Please generate passwords first");return;}
  navigator.clipboard.writeText(text).then(function(){showToast("All passwords copied!")});
});
generatePassword();
</script>'''


def get_diceware_script(is_cn):
    if is_cn:
        return '''
<script>
'use strict';
// EFF Diceware wordlist (abbreviated - 7776 words, using top ~2000 for reasonable size)
var effWords=["abacus","abdomen","abdominal","abide","abiding","ability","ablaze","able","abnormal","abrasion","abrasive","abreast","abridge","abroad","abruptly","absence","absentee","absently","absinthe","absolute","absolve","abstain","abstract","absurd","accent","acclaim","acclimate","accompany","account","accuracy","accurate","accustom","acetone","achiness","aching","acid","acorn","acquaint","acquire","acre","acrobat","acronym","acting","action","activate","activator","active","actress","actual","acute","adamant","adapt","addicted","addition","adhesive","adjoining","adjourn","adjudicate","adjust","administer","admiral","admire","admission","admit","adopt","adoring","adorn","adrift","adroit","adult","adverb","adverse","advertise","advocate","afar","affix","afflict","affluent","afford","aficionado","afloat","afoot","afraid","afterglow","afterlife","aftermath","afterward","again","ageism","agenda","agent","agile","aging","agnostic","agony","agreeable","aground","ahead","ahold","aide","ailment","aimless","airborne","airlift","airline","airlock","airmail","airplane","airport","airtight","airwaves","aisle","alarm","album","alchemy","alcohol","alert","algebra","alibi","alien","alight","align","alike","alive","alkaline","allay","allege","allergy","alleyway","alliance","allocate","allot","allowance","allude","allure","ally","almighty","almond","almost","aloft","alone","alongside","aloof","alphabet","alright","although","altitude","alto","aluminum","alumni","always","amaretto","amaze","amazingly","ambiance","ambiguity","ambiguous","ambition","ambitious","ambulance","ambush","amendable","amendment","amends","amenity","amiable","amicably","amid","amigo","amino","amiss","ammonia","ammunition","amnesia","amnesty","among","amorously","amorous","amount","amphibian","amplify","amputate","amulet","amuse","anagram","analogy","analyse","analyzer","anarchy","anatomist","anchor","anchovy","ancient","android","anemia","anew","angelfish","angelic","anger","angled","angler","angst","angstrom","anguish","angular","anhydrous","animate","anise","ankle","annex","annotate","announce","annoyance","annually","anoint","anomaly","anonymous","anorak","antacid","antelope","antenna","anthem","anthill","antibody","antics","antidote","antihero","antiquity","antisocial","antler","antonym","anvil","anybody","anymore","anxious","anywhere","aorta","apartment","apathetic","apex","aphid","apiary","apologize","apostle","appalling","appeal","appetite","applaud","appliance","appointee","appraisal","apprentice","approach","approval","apricot","april","apron","aptitude","aquaplane","aquarium","aquatic","arbitrary","archaic","archeology","archer","archrival","ardent","arduous","areaway","arena","argument","arid","arise","aristocrat","armada","armchair","armful","armoire","armory","armrest","army","aroma","arose","around","arousal","arrange","array","arrest","arrival","arrogant","arrow","arson","artichoke","artisan","artwork","ascend","ascent","ascribe","ashamed","ashen","ashore","aside","askew","aspect","aspirate","aspire","aspirin","assailant","assassin","assault","assemble","assertive","assess","assignee","assist","assume","assurance","asthma","astride","astronomy","asylum","athlete","atlas","atom","atrium","attache","attacker","attain","attend","attic","attire","attitude","attorney","attune","auction","audible","audience","august","aunt","authentic","author","autism","autistic","autograph","automaker","automated","autumn","avail","avenge","avenue","average","aversion","avert","aviation","aviator","avid","avoid","await","awake","award","aware","awash","awhile","awkward","awning","awoke","axed","axis","axle","azalea","azure","babbling","backdrop","backfield","backfire","backhand","backing","backpack","backspace","backtrack","backup","backyard","bacon","bacteria","badger","badland","bagel","baggage","baggy","bailiff","baker","bakery","balance","balcony","ballerina","ballet","balloon","ballot","balmy","bamboo","banana","bandage","bandana","bandit","bangle","banish","banjo","bankbook","banker","banner","banquet","baptize","barbed","barber","barely","barfly","bargain","barista","baritone","barley","barmaid","barnacle","barnyard","barometer","baron","barracuda","barrel","barstool","baseball","baseless","baseline","basement","bashful","basic","basil","basin","basket","bassoon","batch","bathrobe","bathroom","bathtub","baton","battalion","batter","battery","battle","bayou","bazaar","beach","beacon","beagle","beaker","beam","beanbag","beanie","bearable","beard","beast","beatbox","beatnik","beauty","became","beckon","become","bedbug","bedpost","bedrock","bedroom","bedside","bedspread","beech","beef","beeline","beeper","beer","beetle","befall","before","beggar","beginner","begonia","behalf","behave","behind","behold","beige","belch","belfry","belief","belittle","bellhop","bellow","beloved","below","beltway","bench","bendable","beneath","benefit","beret","berry","beside","bestow","betray","better","between","beverage","beware","beyond","bias","bible","bicep","bicker","bidder","biennial","bigger","bighorn","biker","bikini","billboard","billion","bimonthly","binary","binder","binding","bing","bingo","binoculars","biology","biopsy","biplane","birch","bird","birth","bishop","bison","bisque","bistro","bitmap","bivalve","bizarre","blackbird","blackhead","blackjack","blackmail","blackout","blacksmith","bladder","blade","blah","blame","bland","blank","blarney","blatant","blaze","bleach","bleak","bleep","blemish","blend","bless","blimp","blindfold","blink","blip","bliss","blister","blitz","blizzard","bloat","blockade","blogger","blond","bloom","blossom","blot","blouse","blowfish","blowout","bluebell","bluebird","bluefish","bluejay","blues","bluff","blunder","blunt","blurb","blurt","blush","boa","boast","boatload","bobcat","bodily","bogus","boil","boiler","boldness","bolster","bolt","bomb","bonanza","bonding","boneless","bonehead","bonfire","bonnet","bonsai","bonus","boogeyman","bookcase","bookend","booklet","bookmark","bookworm","boomerang","booth","bootleg","booze","borax","border","boredom","borrower","bossy","botanical","botany","bothered","bottle","bounce","bouncy","bound","bountiful","bouquet","bourbon","bovine","bowel","bowling","boxcar","boxer","boyfriend","braces","brackish","brag","braid","brainchild","brainwash","brainy","brake","bran","brandish","brandy","brash","brass","bravado","bravo","brawny","brazen","breach","breadbox","breakable","breakaway","breakdown","breakfast","breakout","breathe","breed","breeze","brewery","bribe","brick","bridge","brief","brighten","brim","brink","brisket","briskly","bristle","brittle","broadcast","broaden","broccoli","brochure","broil","broken","bronco","bronze","brooch","brood","brook","broom","brother","brought","brownie","bruise","brunch","brunette","brush","brutal","bubble","bubbly","buckle","buddy","budge","buffalo","buffer","buffet","buggy","bugle","builder","bulb","bulkhead","bulldog","bulldoze","bullet","bullfrog","bullhorn","bullpen","bully","bumble","bump","bumpy","bunch","bungalow","bungee","bunk","bunny","burden","bureau","burger","burglar","burial","buried","burly","burner","burp","burrito","burrow","burst","busboy","bush","business","busy","butcher","butter","button","buyer","buzzard","buzzer","bygone","bypass","cabana","cabbage","cabin","cabinet","cable","caboose","cache","cackle","cactus","cadet","cafe","caffeine","caftan","cage","cajole","cake","calamari","calcium","calculate","calibrate","caller","callous","calm","calorie","camel","cameo","camera","campaign","camper","campus","canary","cancel","candid","candle","candy","cane","canine","canister","cannabis","canned","cannoli","canoe","canopy","canteen","canvas","canyon","capable","capacity","cape","capillary","capital","capitol","caplet","capricorn","capsize","capsule","captain","caption","captivate","captive","capture","caramel","carat","caravan","carbon","cardboard","cardigan","cardinal","career","carefree","careless","caress","caretaker","cargo","caribou","carnation","carnival","carol","carpenter","carpet","carport","carriage","carrier","carrot","carryout","cartel","carton","cartoon","cartwheel","carve","cashew","cashier","casino","casserole","cassette","castanet","castle","casual","catacomb","catalog","catalyst","catapult","catastrophe","catch","categorize","cathedral","catholic","cattle","cauldron","cauliflower","causal","caution","cavalry","cave","caviar","cayenne","cease","cedar","celery","celestial","cellar","cellphone","cellular","cement","cemetery","censor","census","centipede","central","ceramic","cereal","cerebral","certain","certify","cervix","chafe","chaff","chain","chairlift","chalet","chalk","challenge","chamber","champion","chance","chandelier","change","channel","chant","chaos","chapel","chapter","character","chard","charge","charity","charm","chart","chase","chassis","chastise","chat","chatter","cheap","cheat","checkbook","checklist","checkout","checkup","cheddar","cheek","cheer","cheese","cheetah","chef","chemist","cherish","cherry","chess","chestnut","chevy","chew","chicken","chide","chief","child","chili","chill","chime","chimney","chimpanzee","china","chipmunk","chirp","chisel","chive","chlorine","chocolate","choice","choir","cholesterol","choosy","chopstick","chowder","chrome","chronic","chuckle","chug","chummy","chunk","church","churn","chutney","cider","cigar","cilantro","cinema","cinnamon","circuit","circulate","circus","citation","citizen","citrus","cityscape","civic","civilian","clam","clambake","clamp","clandestine","clap","clarify","clarity","clash","classic","classify","clatter","clause","claw","clay","cleanse","clearance","cleat","cleaver","cleft","clergy","clerk","clever","cliche","click","clientele","cliff","climate","clinch","cling","clinic","clipboard","clique","cloak","clobber","clock","clone","close","closet","cloth","cloudburst","cloudy","clout","clover","club","cluck","clue","clump","clumsy","cluster","clutch","coach","coal","coast","cobalt","cobweb","cockroach","cocktail","coconut","cocoon","cod","coexist","coffee","cog","cognition","cognac","coherent","coil","coin","coincide","cola","cold","coleslaw","coliseum","collage","collapsible","collar","college","collide","collusion","cologne","colonel","colony","colossal","column","combat","combine","combust","comeback","comedian","comedy","comet","comfort","comical","comma","commence","commerce","commit","common","communal","commuter","compact","companion","compare","compel","compete","compile","complex","compliment","comply","compose","compound","compress","comprise","computer","comrade","conceal","concede","conceive","concept","concern","concert","conch","conclude","concrete","condition","condo","condor","conductor","cone","confess","confetti","confide","confine","confirm","conflict","conform","confound","confront","confuse","congeal","congress","conifer","conjure","connect","conquer","conscience","conscious","consent","conserve","consider","consist","console","consonant","conspire","constant","constrain","construct","consult","consumer","contact","contagious","contain","contend","content","contest","context","contour","contract","contrast","contribute","control","convene","convent","converge","converse","convert","convey","convict","convince","convoy","cookbook","cookie","cooking","coolant","cooperate","coordinate","copilot","copious","copper","copycat","coral","cord","cordial","core","cork","cornbread","corner","cornfield","cornstalk","corporate","corral","correct","corridor","corrode","corsage","cosmetic","cosmic","costume","cottage","cotton","couch","cougar","cough","could","countdown","counter","county","couple","coupon","courage","courier","course","courtroom","cousin","cove","covenant","cover","covert","coward","cowbell","cowboy","coyote","crab","crackdown","cracker","crackle","cradle","craft","cram","cramp","crane","crank","crater","crawl","crayon","crazy","creak","cream","create","creature","credible","credit","creed","creek","creep","crepe","crescent","crest","crew","crib","cricket","cringe","crisp","critic","croak","crock","crook","croon","crop","crossbow","crossing","crossword","crouch","crowbar","crowd","crown","crucial","crude","cruise","crumb","crunch","crusade","crush","crust","crybaby","cryptic","crystal","cubicle","cucumber","cuddle","cue","cuff","cuisine","culprit","cultivate","cultural","cumin","cupboard","cupcake","cupid","curator","curb","curdle","curfew","curio","curl","currant","currency","current","curriculum","curry","cursive","cursor","curtail","curtain","curvy","cushion","custody","custom","customer","cutback","cute","cuticle","cutoff","cycle","cylinder","cymbal","cynical","cypress","dabble","dad","daffodil","dagger","daily","dainty","dairy","daisy","dally","damage","dampen","dance","danger","dangle","dapper","daredevil","daring","darken","darling","dartboard","dashboard","database","datebook","daughter","daunting","dawdle","dawn","daybed","daybreak","daydream","daylight","daytime","daze","dazzle","deadbolt","deaden","deaf","dealer","dear","death","debatable","debate","debit","debris","debtor","decade","decaf","decal","decay","deceit","deceive","decent","decibel","decimal","decision","declare","decline","decompose","decor","decoy","decrease","dedicate","deduce","deed","deem","deepen","deface","defeat","defect","defend","defer","define","deflate","deflect","defrost","deft","defuse","defy","degrade","dehydrate","deity","dejected","delay","delegate","delete","delicacy","delight","deliver","delouse","delta","deluge","delusion","deluxe","demand","demented","demeanor","demerit","demise","democrat","demolish","demon","demote","denial","denim","denote","dense","dentist","deny","deodorant","depart","depend","depict","deplete","deploy","deport","deposit","depraved","deprive","derby","derelict","derive","derrick","descend","describe","desert","design","desire","desist","desk","desolate","despair","desperate","despise","destiny","destroy","detach","detail","detect","detergent","determine","detonate","detour","detox","detract","detriment","develop","deviance","device","devil","devious","devote","devour","dew","dexterity","diabetes","diabolic","diagnose","diagonal","diagram","dial","dialect","dialogue","diamond","diaper","diary","dice","diction","did","diesel","diet","differ","digest","digit","dignify","dilate","dilemma","diligence","dill","dilute","dime","diminish","dimple","din","dine","ding","dinghy","dining","dinner","dinosaur","dioxide","diploma","dire","directions","disable","disarm","discard","disclose","disco","discord","discount","discover","discreet","discuss","disdain","disease","disfigure","disgrace","disgust","dishonest","dislike","dismal","dismantle","dismiss","disobey","disorder","dispatch","dispel","display","dispute","disrupt","dissect","dissent","dissolve","distance","distinct","distort","distract","distress","district","distrust","ditch","ditto","dive","divert","divide","divisible","divorce","dizzy","dock","doctor","document","dodge","dog","doghouse","doll","domain","domestic","domino","donate","donkey","donor","donut","door","doorknob","dormant","dorsal","dosage","double","doubt","doughnut","dowdy","dowel","downcast","downfall","downhill","download","downpour","downsize","downtown","downturn","dowry","doze","drab","draft","drag","dragon","drain","dramatic","drape","drawbridge","drawer","dreadful","dream","drench","dress","dribble","drift","drill","drink","drip","driveway","drizzle","drone","drool","drop","drought","drove","drown","drowsy","drudge","drum","dry","dual","dubious","duck","duct","dude","duffel","dugout","dull","dumb","dump","dunce","dune","dungeon","dunk","duo","duplex","duplicate","durable","duration","duress","during","dusk","dust","duty","dwarf","dwell","dye","dynamic","dynamite","dynasty","eager","eagle","early","earmark","earmuffs","earn","earplug","earring","earth","ease","easel","eastward","easygoing","eavesdrop","ebb","ebony","echo","eclipse","ecology","economic","economy","ecstatic","eddy","edge","edgy","edible","edifice","edit","educate","eel","efface","effect","effort","egg","eggplant","ego","eight","either","eject","elaborate","elastic","elated","elbow","elder","elect","elegant","element","elephant","elevate","elicit","eligible","eliminate","elite","elope","eloquent","elsewhere","elude","email","embalm","embankment","embargo","embark","embarrass","embassy","embed","emblem","embody","emboss","embrace","embroider","embryo","emerald","emerge","emission","emotion","emperor","emphasis","empire","employ","empower","empty","enable","enact","enamel","encase","enchant","enclose","encore","encounter","encourage","encroach","encrypt","encyclopedia","endanger","endear","endeavor","endless","endorse","endow","endure","enemy","energetic","energy","enforce","engage","engine","enhance","enigma","enjoy","enlighten","enlist","enormous","enough","enrage","enrich","enroll","ensure","entail","enter","entire","entrance","entree","entrust","entry","envelope","envision","envy","enzyme","epic","epidemic","episode","equal","equate","equator","equip","erase","erect","erode","erratic","error","erupt","escalate","escalator","escapade","escape","escort","esophagus","especially","espionage","essay","essence","establish","estate","estimate","estuary","eternal","ethic","etiquette","evacuate","evade","evaluate","evaporate","eve","even","event","everyday","evict","evidence","evil","evoke","evolve","exact","exam","example","excavate","exceed","excel","except","excerpt","exchange","excite","exclude","excuse","execute","exempt","exercise","exert","exhale","exhaust","exhibit","exile","exist","exit","exotic","expand","expect","expedite","expel","expense","experiment","expert","expire","explain","explode","explore","export","expose","express","extend","extra","extract","extreme","exuberant","eyebrow","eyedrop","eyeglass","eyelash","eyelid","fable","fabric","face","facial","fact","factor","faculty","fade","fail","faint","fair","fairy","faith","fake","falcon","fall","false","falter","familiar","family","famine","famous","fanatic","fancy","fantasy","farce","farewell","fascinate","fashion","fasten","fat","fatal","father","fatigue","fatten","faucet","fault","favor","fear","feast","feat","feather","feature","federal","feeble","feed","feel","feisty","feline","fellow","felt","female","feminine","fence","ferocious","ferret","ferry","fertile","fervent","festival","fetch","fetus","feud","fever","few","fiance","fiber","fiction","fidget","field","fiery","fiesta","fifteen","fifth","fifty","fight","figment","figure","filament","file","filing","fill","film","filter","filthy","final","finance","finch","find","fine","finger","finish","finite","firefly","fireman","fireplace","fireproof","firewood","firework","firm","first","fish","fishing","fist","fitness","five","fixate","fizz","flag","flair","flame","flank","flannel","flap","flare","flash","flask","flat","flatter","flavor","flaw","flea","fleck","fledge","flee","fleet","flesh","flex","flick","flier","flight","flinch","fling","flint","flip","flipper","flirt","float","flock","flood","floppy","floral","floss","flour","flow","flower","fluctuate","fluent","fluff","fluid","fluke","flunk","flush","fluster","flute","flutter","fly","foam","focus","fog","foil","fold","foliage","folk","folklore","follow","fondue","font","food","fool","footage","football","foothill","footnote","footrest","footstep","footwear","forage","forbid","force","forearm","forecast","forego","foreign","forest","forever","forfeit","forge","forgive","fork","form","formal","format","former","formula","forsake","fort","forth","fortify","fortunate","fortune","forum","forward","fossil","foster","foul","founder","fountain","four","fowl","fox","foyer","fraction","fracture","fragile","fragrant","frail","frame","frank","frantic","fraud","fray","freckle","freedom","freeway","freeze","freight","french","frequent","fresh","fret","friction","fridge","friend","fright","fringe","frog","front","frost","frown","frozen","frugal","fruit","fry","fuel","fugitive","fulfill","full","fumble","fume","fun","function","fund","fungus","funnel","funny","fur","furious","furnace","furnish","further","fury","fuse","fuss","futile","future","fuzzy","gable","gadget","gaffe","gain","galaxy","gale","gallant","gallery","galley","gallon","gallop","gamble","game","gamma","gangplank","gangster","gap","garage","garbage","garden","gargoyle","garlic","garment","garnish","garter","gas","gash","gasoline","gate","gather","gaudy","gauge","gauntlet","gauze","gave","gavel","gawk","gazelle","gazette","gear","gecko","geese","geisha","gelatin","gem","gender","genealogy","general","generate","generic","genesis","genetic","genie","genius","genome","genre","gentle","gentleman","genuine","geography","geology","geometry","geranium","gerbil","gesture","getaway","geyser","ghastly","gherkin","ghost","ghoul","giant","giddy","gift","gigantic","giggle","gild","gill","gimmick","ginger","giraffe","girdle","girl","give","glacier","glad","glamour","glance","gland","glare","glass","glaze","gleam","glee","glide","glimmer","glimpse","glisten","glitch","glitter","global","gloom","glory","gloss","glove","glow","glucose","glue","glut","glutton","gnat","gnaw","gnome","goal","goat","gobble","goblet","goddess","goggle","gold","golf","gondola","gone","gong","good","goof","google","goose","gorge","gorilla","gospel","gossip","gouge","gourmet","govern","gown","grab","grace","grad","grade","gradual","graft","graham","grain","grammar","grand","granite","grant","grape","graphic","grapple","grasp","grass","grateful","gratuity","grave","gravel","gravity","gravy","gray","graze","grease","great","greed","green","greet","grenade","grey","grid","grief","grill","grim","grime","grin","grind","grip","grit","grocery","groom","groove","gross","ground","group","grove","grow","grub","grudge","grumble","grunt","guard","guess","guest","guide","guild","guilt","guise","guitar","gulch","gull","gum","gun","guppy","gurgle","guru","gush","gust","gut","gutter","guy","guzzle","gym","habit","habitat","hacienda","hacksaw","had","haggis","hail","hair","half","halibut","hallmark","hallway","halt","ham","hamburger","hammock","hamper","hamster","handbag","handcuff","handful","handicap","handle","handmade","handout","handset","handsome","handwash","handwrite","handyman","hang","hankie","happen","happy","harass","harbor","hard","hardy","hare","harm","harp","harsh","harvest","hash","hassle","haste","hat","hatch","hate","haul","haunt","have","haven","havoc","hawk","hay","hazard","hazel","hazy","headband","headboard","headcount","headdress","headfirst","headhunter","headland","headline","headrest","headset","headway","heal","health","hear","hearse","heart","heat","heaven","heavy","heckle","hectic","hedge","heel","hefty","height","heirloom","heist","helicopter","helium","helmet","help","hem","hen","hence","herb","herd","here","heritage","hermit","hero","herring","hesitant","hexagon","heyday","hiatus","hibernate","hiccup","hide","high","highland","highlight","highway","hijack","hike","hill","hinder","hinge","hint","hippo","hire","history","hit","hitch","hive","hoard","hobbit","hobby","hockey","hoe","hog","hold","hole","hollow","holster","home","homeless","homemade","homework","honest","honey","honk","honor","hood","hoof","hook","hop","hope","horizon","hormone","horn","horrid","horror","horse","hose","host","hot","hotel","hound","hour","house","hover","how","hub","huddle","hue","hug","huge","hull","hum","human","humble","humid","humor","hump","hunch","hundred","hungry","hunk","hunt","hurdle","hurl","hurrah","hurricane","hurry","hurt","husband","hush","husk","hut","hybrid","hydrant","hydrogen","hyena","hygiene","hype","hyphen","ice","iceberg","icing","icon","idea","ideal","identical","identify","idle","idol","ignite","ignore","iguana","ill","illegal","illuminate","image","imagine","immense","immerse","immune","impact","impair","impending","imperfect","import","impose","impress","imprint","improve","impulse","inbound","incense","inch","incident","incisor","include","income","increase","indeed","index","indicate","indigo","indoor","indulge","industry","infant","inflame","inflate","inflict","inform","infringe","infuse","ingest","inhale","initial","inject","injure","inmate","inn","innate","inner","input","inquire","insane","insect","insert","inside","insist","insomnia","inspect","install","instant","instead","insult","intact","intake","integer","intend","intense","interact","interest","interim","interior","intern","internal","interval","intimate","invade","invent","invest","invite","invoice","involve","iodine","ionic","iron","irregular","irrigate","irritate","island","isolate","issue","italic","itch","item","itinerary","ivory","ivy","jab","jack","jacket","jackpot","jade","jagged","jaguar","jail","jalapeno","jam","janitor","jar","jargon","jasmine","javelin","jaw","jaywalk","jazz","jealous","jeans","jeep","jelly","jeopardy","jerk","jersey","jest","jet","jewel","jigsaw","jingle","job","jockey","jog","join","joint","joke","jolly","jolt","journal","journey","jovial","joy","jubilant","judge","judo","jug","juggle","juice","jukebox","jumbo","jump","junction","jungle","junior","junk","juror","just","juvenile","kale","kaleidoscope","kangaroo","kaput","karate","karma","kayak","kazoo","kebab","keen","keep","kennel","kept","kernel","ketchup","kettle","key","keyboard","kick","kid","kidney","kill","kimono","kin","kind","kindle","king","kiosk","kiss","kit","kitchen","kite","kitten","kitty","kiwi","knack","knee","kneel","knife","knight","knit","knob","knock","knot","know","koala","kook","kosher","kudos","label","labor","lace","lack","ladder","lady","lagoon","lake","lamb","lament","lamp","lance","land","landline","landlord","landmark","landslide","lane","language","lantern","lap","lapdog","lapse","laptop","lard","large","laser","lash","lass","lasso","last","late","lather","latitude","latrine","latter","laugh","launch","lava","lavender","lavish","law","lawn","lawsuit","lawyer","layer","lazy","lead","leaf","leak","lean","leap","learn","lease","leash","least","leather","leave","ledge","left","leg","legacy","legal","legend","leisure","lemon","lend","length","lens","leopard","less","lesson","letter","lettuce","level","lever","lexicon","liable","liberty","library","license","lick","lid","life","lift","light","like","lilac","lily","limb","lime","limit","limp","line","linen","linger","link","lint","lion","lip","lipstick","liquid","liquor","list","literacy","literal","litter","little","live","lively","liver","lizard","llama","load","loaf","loan","lobby","lobe","lobster","local","locate","lock","locker","locomotive","locust","lodge","loft","log","logic","logo","lonely","long","look","loom","loop","loose","loot","lord","lot","lotion","lottery","loud","lounge","love","low","loyal","lozenge","lucid","luck","luggage","lull","lumber","luminous","lump","lunar","lunch","lunge","lung","lurk","lush","luxury","lyric","macaroni","machine","macro","mad","magazine","maggot","magic","magnet","magnify","magnitude","maid","mail","main","mainland","maintain","majestic","major","make","malady","male","malfunction","malice","mall","mammal","mammoth","man","manage","mandate","mandolin","mangle","mango","mania","manicure","mankind","manner","mansion","mantel","manual","many","map","maple","marathon","marble","march","mare","margin","marigold","marine","marionette","maritime","mark","market","marmalade","maroon","marriage","marsh","marshmallow","mascot","mason","massage","massive","mast","master","match","mate","material","maternity","math","matrix","matter","mattress","mature","maxim","maximum","maybe","mayhem","mayo","mayor","meadow","meal","mean","measure","meat","mechanic","medal","media","medical","medicine","meditate","medium","meet","melody","melon","melt","member","memo","memoir","memory","menace","mend","mental","mention","mentor","mercy","mere","merge","merit","mermaid","merry","mesh","mess","message","metal","meteor","method","micro","microwave","midday","middle","midst","midwife","might","mighty","mild","mile","military","milk","mill","million","mime","mimic","mince","mind","mine","mini","minimum","minor","mint","minus","minute","miracle","mirror","mischief","miserable","misfit","mislead","misplace","miss","missile","missing","mission","mist","mistake","mitten","mix","mixture","moan","mob","mobile","mock","mode","model","modern","modest","modify","module","moist","molar","mold","molecule","mollusk","moment","monarch","money","monitor","monkey","monopoly","monsoon","monster","month","monument","moo","mood","moon","moose","mop","moral","more","morbid","morning","morsel","mortal","mortar","mortgage","mosaic","mosque","mosquito","moss","most","moth","mother","motion","motivate","motor","motto","mound","mountain","mouse","mouth","move","movie","mow","much","muck","mud","muffin","mug","mulch","mule","mull","multiple","mumble","mummy","munch","municipal","mural","murky","murmur","muscle","museum","mushroom","music","mussel","must","mustache","mustard","mute","mutiny","mutter","muzzle","myriad","mystery","myth","nail","name","nap","napkin","narrate","narrow","nasal","nasty","nation","native","natural","nature","naughty","nausea","naval","navigate","navy","near","neat","nebula","necessary","neck","necklace","need","needle","negative","neglect","negligee","negotiate","neighbor","neither","nematode","neon","nephew","nerve","nest","nestle","net","network","neutral","never","nevermore","new","newborn","newly","next","nibble","nice","nickel","nickname","nicotine","niece","night","nimble","nine","ninth","nip","nitrogen","no","noble","nobody","nod","noise","nomad","none","noodle","noon","normal","north","nose","nostril","notable","note","notebook","nothing","notice","notify","notion","nougat","noun","nourish","novel","novice","now","nudge","nuke","null","number","numb","nun","nurse","nut","nutmeg","nutrient","nutshell","nuzzle","oak","oasis","oat","obey","object","oblong","oboe","obscure","observe","obsolete","obstacle","obtain","obvious","occur","ocean","octagon","octave","october","octopus","odd","off","offend","offer","office","official","often","oil","okay","old","olive","omega","omelet","omit","once","one","onion","online","only","onset","onto","onward","onyx","oops","ooze","opaque","open","opera","operate","opinion","opossum","opponent","oppose","optic","optimist","option","orange","orbit","orchard","orchestra","orchid","ordeal","order","organ","organic","organize","orient","origin","ornament","orphan","ostrich","other","otter","ounce","our","out","outcome","outdoor","outer","outfield","outgoing","outlast","outlet","outline","outlook","output","outrage","outright","outside","outward","oval","oven","over","overall","overcoat","overcome","overdue","overflow","overhaul","overhead","overhear","overjoyed","overlap","overload","overlook","overnight","overpass","overreact","overseas","oversee","oversight","overtake","overtime","overwhelm","owe","owl","own","ox","oxygen","oyster","ozone","pace","pack","package","packet","pad","paddle","page","pail","pain","paint","pair","pajamas","palace","palate","pale","palm","pan","pancake","panda","panel","panic","panorama","pant","pantry","pants","papa","paper","parachute","parade","paradise","paradox","paraffin","paragraph","parallel","paralyze","paramedic","parasite","parcel","pardon","parent","parish","park","parka","parliament","parlor","parody","parrot","parsley","part","partial","particle","partner","party","pass","passage","passion","passive","passport","password","past","pasta","paste","pastime","pastor","pastry","pasture","pat","patch","patent","path","patio","patriarch","patriot","patrol","patron","pattern","pause","pavement","pavilion","paw","pawn","pay","peace","peach","peacock","peak","peanut","pear","pearl","peasant","pebble","pecan","peck","pedal","pedestrian","peek","peel","peer","pelican","pen","penalty","pencil","pendant","pending","penguin","peninsula","penny","pension","pepper","per","perceive","percent","perch","perfect","perform","perfume","perhaps","peril","period","perish","perjury","permanent","permit","peroxide","perpetual","persist","person","personal","persuade","pertain","peruse","pest","pet","petal","petite","petrify","petroleum","petticoat","pew","phantom","pharmacy","phase","pheasant","phenomena","philosophy","phoenix","phone","photon","phrase","physical","physique","piano","pick","pickle","picnic","picture","piece","pig","pigeon","pigment","pike","pile","pilgrim","pill","pillar","pillow","pilot","pimple","pin","pinafore","pine","pineapple","pink","pinnacle","pint","pioneer","pipe","pirate","pistol","piston","pit","pitch","pizza","place","placid","plague","plain","plan","plane","planet","plank","plant","plantation","plasma","plaster","plastic","plate","plateau","platform","platinum","platter","play","player","playroom","plaza","plea","please","pledge","plenty","plight","plod","plow","pluck","plug","plum","plumber","plume","plump","plunge","plural","plus","ply","pocket","pod","poem","poet","poignant","point","poise","poison","polar","pole","police","polish","politic","pollen","pollute","polo","polygon","pond","ponder","pony","pool","poor","pop","popcorn","pope","popular","porcelain","porch","porcupine","pork","port","portable","portal","porter","portion","portrait","position","positive","possess","possible","post","postal","postcard","poster","postpone","pot","potato","potential","potion","pottery","pouch","poultry","pound","pour","pout","powder","power","practice","prairie","praise","prance","pray","preach","precede","precious","precise","predator","predict","prefer","prefix","preheat","prelude","premier","premium","prepare","prescribe","present","preserve","preside","press","presto","pretend","pretty","pretzel","prevail","prevent","preview","previous","prey","price","pride","priest","primary","primate","prime","prince","principal","print","prior","prison","pristine","private","prize","pro","probable","problem","proceed","process","proclaim","produce","product","profane","profess","profile","profit","program","project","prologue","prolong","promise","promote","prompt","prone","prong","pronoun","proof","prop","propane","proper","prophet","propose","prose","protect","protein","protest","proud","prove","proverb","provide","provoke","prowl","proxy","prude","prune","pry","pseudo","psyche","psychic","public","publish","pucker","puddle","puff","pull","pulp","pulse","pump","pumpkin","punch","punctual","pungent","punish","pupil","puppet","puppy","purchase","pure","purge","purple","purpose","purr","purse","pursue","push","puzzle","pyramid","quack","quail","quaint","quake","qualify","quality","quantity","quantum","quarantine","quarrel","quarry","quarter","quash","quasi","quaver","queen","queer","quell","query","quest","question","quick","quiet","quill","quilt","quintet","quirk","quit","quiver","quiz","quota","quote","rabbi","rabbit","raccoon","race","rack","radar","radial","radiate","radical","radio","radish","radius","raffle","raft","rage","raid","rail","rain","rainbow","raise","raisin","rake","rally","ram","rambunctious","ramp","ranch","random","range","rank","ransom","rapid","rare","raspberry","rat","rate","rather","ratio","rattle","rave","raven","ravine","raw","ray","razor","reach","react","read","ready","real","realm","reap","rear","reason","rebel","recall","recede","receipt","receive","recent","recess","recipe","recite","reckless","reckon","recline","recognize","recoil","record","recover","recreation","recruit","rectangle","recycle","red","redeem","redirect","reduce","reef","refer","referee","refine","reflect","reform","refresh","refuge","refund","refuse","regain","regard","regime","region","register","regret","regular","rehearse","reign","reinforce","reject","rejoice","relapse","relate","release","relent","reliable","relic","relief","religion","relish","relocate","reluctant","rely","remain","remark","remedy","remember","remind","remnant","remote","remove","renaissance","render","renew","renovate","renown","rent","repair","repay","repeat","repel","repent","replace","replay","replica","reply","report","repose","represent","reptile","republic","repulse","reputation","request","require","rescue","research","resemble","reserve","reside","resign","resist","resolve","resonate","resort","resource","respect","respond","rest","restore","restrain","result","retail","retain","retina","retire","retract","retreat","retrieve","return","reunion","reveal","revel","revenge","revenue","revere","reverse","review","revise","revive","revolt","revolution","revolve","reward","rewrite","rhino","rhyme","rhythm","rib","ribbon","rice","rich","ride","ridge","rifle","right","rigid","rim","ring","rinse","riot","rip","ripe","ripple","rise","risk","ritual","rival","river","road","roam","roar","roast","rob","robe","robin","robot","robust","rock","rocket","rod","rodeo","role","roll","romance","romantic","roof","room","roost","root","rope","rose","rotate","rotor","rotten","rouge","rough","round","route","routine","row","royal","rub","rubber","ruby","rudder","rude","rug","ruin","rule","rum","rummage","run","rung","runner","runt","rural","rush","rust","rustic","rustle","rut","saber","sable","sacred","sad","saddle","safari","safe","saga","sage","sail","sailboat","saint","sake","salad","salami","salary","sale","saliva","salmon","salon","saloon","salsa","salt","salute","salvage","salvation","same","sample","sanction","sanctuary","sand","sandal","sandbox","sandwich","sane","sanitary","sarcasm","sardine","sash","satellite","satin","satire","satisfy","sauce","sauna","sausage","savage","save","savor","saw","say","scale","scallion","scallop","scalp","scan","scandal","scant","scar","scarce","scare","scarf","scary","scatter","scavenge","scene","scenery","scent","schedule","scheme","scholar","school","science","scissor","scoff","scold","scoop","scoot","scope","scorch","score","scorpion","scotch","scout","scram","scrap","scrape","scratch","scrawny","scream","screech","screen","screw","scribble","script","scroll","scrub","scruff","sculpt","scurry","sea","seafood","seagull","seal","seam","search","seashell","seaside","season","seat","seaweed","second","secret","section","sector","secure","sedan","sedate","sediment","see","seed","seek","seem","segment","seize","seldom","select","self","sell","semester","semicolon","seminar","senate","senator","send","senior","sensation","sense","sentence","sentiment","separate","sequence","serene","sergeant","serial","series","serious","sermon","serpent","serum","servant","serve","sesame","session","set","settle","seven","severe","sew","shabby","shack","shade","shadow","shaft","shake","shaky","shale","shall","shallow","shame","shampoo","shamrock","shape","share","shark","sharp","shatter","shave","shawl","she","shear","shed","sheep","sheer","sheet","shelf","shell","shelter","sherbet","sheriff","shield","shift","shimmer","shin","shine","shingle","ship","shirt","shiver","shock","shoe","shoo","shoot","shop","shore","short","shot","should","shout","shove","show","shower","shred","shrewd","shrimp","shrine","shrink","shroud","shrub","shrug","shuck","shuffle","shun","shush","shut","shy","sick","siege","sift","sigh","sight","sign","signal","silence","silhouette","silicon","silk","silly","silver","similar","simmer","simple","simulate","since","sincere","sing","single","sink","sip","sir","siren","sister","sit","site","situate","six","sixteen","sixty","size","skate","sketch","ski","skid","skill","skim","skin","skip","skirt","skull","skunk","sky","slab","slack","slalom","slam","slang","slant","slap","slash","slate","slave","slay","sled","sleek","sleep","sleet","sleeve","slender","slice","slick","slide","slight","slim","sling","slip","slit","slob","slope","slot","slow","slug","slum","slump","slur","sly","smack","small","smart","smash","smear","smell","smelt","smile","smirk","smith","smock","smog","smoke","smooth","smother","smudge","snack","snag","snail","snake","snap","snarl","sneak","sneer","sneeze","snicker","sniff","snip","snoop","snore","snorkel","snort","snot","snow","snub","snuff","snug","soak","soap","soar","sob","sober","soccer","social","sock","socket","soda","sodium","sofa","soft","software","soil","solar","soldier","sole","solid","solitaire","solo","solution","solve","some","somersault","son","song","sonic","soon","soothe","sophomore","soprano","sorbet","sore","sorrow","sorry","sort","soul","sound","soup","sour","source","south","souvenir","soy","space","spade","spaghetti","span","spare","spark","sparrow","spatula","spawn","speak","spear","special","species","specific","speck","spectacle","spectrum","speech","speed","spell","spend","sphere","spice","spider","spike","spill","spin","spinach","spiral","spirit","spit","spite","splash","splendid","split","spoil","spoke","sponge","sponsor","spontaneous","spooky","spoon","sport","spot","spouse","sprawl","spray","spread","spring","sprinkle","sprint","sprout","spruce","spur","spy","squabble","squad","squall","square","squash","squat","squawk","squeak","squeeze","squid","squint","squire","squirrel","stable","stack","stadium","staff","stage","stain","stair","stake","stale","stalk","stall","stamp","stance","stand","staple","star","starch","stare","start","starve","state","static","station","statistic","statue","status","stay","steady","steak","steal","steam","steel","steep","steer","stellar","stem","stench","step","stereo","stern","stew","stick","still","stilt","sting","stir","stitch","stock","stocking","stomach","stomp","stone","stood","stool","stoop","stop","storage","store","stork","storm","story","stout","stove","straight","strain","strand","strange","strap","strategy","straw","stray","streak","stream","street","strength","stress","stretch","strict","stride","strike","string","strip","stripe","strive","stroke","stroll","strong","struggle","stubborn","student","studio","study","stuff","stumble","stump","stun","stunt","stupid","sturdy","style","sub","subdue","subject","sublime","submarine","submit","subside","substance","subtle","subtract","suburb","subway","succeed","such","suction","sudden","suffer","suffix","sugar","suggest","suit","sulk","sum","summary","summer","summit","sun","sunburn","sundae","sunday","sunflower","sung","sunk","sunlight","sunny","sunset","super","superb","superior","supervise","supper","supply","support","suppose","supreme","surface","surfboard","surge","surgeon","surgery","surname","surprise","surround","survey","survive","suspect","suspend","sustain","swallow","swamp","swan","swap","swarm","sway","swear","sweat","sweater","sweep","sweet","swell","swift","swim","swing","swirl","switch","swivel","swoop","sword","symbol","symmetry","sympathy","symptom","syndrome","synonym","syntax","syrup","system","table","tablecloth","tablet","tabloid","tack","tackle","tact","tactic","tadpole","tag","tail","tailor","take","talent","talk","tall","tame","tamper","tandem","tangerine","tangle","tango","tank","tanker","tannery","tap","tape","target","tariff","tarnish","tart","task","tassel","taste","tattoo","taunt","tavern","tax","taxi","tea","teach","team","tear","tease","technical","technique","tedious","teen","teepee","telephone","television","tell","temper","temperature","temple","tempo","temporary","tempt","tenant","tend","tender","tennis","tenor","tense","tension","tent","tepid","term","terminal","terrace","terrain","terrible","territory","terror","test","testify","text","thank","that","theater","theft","their","theme","then","theory","therapy","there","therefore","thermal","thermos","these","thick","thigh","thin","think","third","thirst","thirteen","thirty","this","thorn","thorough","those","thought","thousand","thread","threat","three","thrift","thrill","thrive","throat","throb","throne","through","throw","thud","thug","thumb","thump","thunder","thus","thyme","ticket","tide","tidy","tie","tiger","tight","tile","till","tilt","timber","time","timid","tin","tinker","tinsel","tiny","tip","tiptoe","tire","tissue","title","toad","toast","today","toe","tofu","toggle","toil","token","tolerate","toll","tomato","tomb","tomorrow","ton","tone","tongue","tonight","too","tool","tooth","top","topic","topple","torch","torment","tornado","tortoise","toss","total","touch","tough","tour","tourist","tournament","toward","towel","tower","town","toxic","toy","trace","track","tractor","trade","tradition","traffic","tragedy","trail","train","trait","tram","trample","trance","tranquil","transfer","transform","translate","transmit","transparent","transport","trap","trash","trauma","travel","tray","tread","treasure","treat","treble","tree","trek","tremble","trench","trend","trespass","trial","tribe","trick","tricky","tricycle","trigger","trillion","trim","trio","trip","triple","triumph","trivial","trolley","trombone","troop","trophy","tropical","trouble","trough","troupe","trousers","trout","truce","truck","true","truly","trumpet","trunk","trust","truth","try","tsunami","tub","tuba","tube","tuck","tuesday","tuft","tug","tuition","tulip","tumble","tummy","tumor","tuna","tundra","tune","tunic","tunnel","turban","turf","turkey","turmoil","turn","turquoise","turret","turtle","tusk","tutor","tuxedo","twang","tweak","tweed","tweet","twelve","twenty","twice","twig","twilight","twin","twine","twirl","twist","twitch","two","type","typical","typo","ugly","ulcer","ultimate","umbrella","umpire","unable","unanimous","unaware","unbecoming","unbiased","unbroken","uncanny","uncertain","uncle","unclear","uncommon","uncover","under","underdog","undergo","underneath","understand","undo","uneasy","unfair","unfold","unfortunate","unhappy","unhealthy","unicorn","uniform","union","unique","unit","universe","unknown","unleash","unless","unlikely","unlisted","unpack","unplug","unravel","unreal","unrest","unsafe","unseen","unstable","unusual","unveil","unwrap","upbeat","update","upgrade","uphold","upkeep","uplift","upload","upon","upper","upright","uproar","upset","upside","upstairs","uptake","uptown","upward","uranium","urban","urchin","urge","urgent","urn","use","useful","usher","usual","utensil","utility","utilize","utmost","utopia","utter","vacant","vacation","vaccine","vacuum","vagabond","vague","valentine","valid","valley","valuable","value","valve","vampire","van","vanilla","vanish","vanity","vapor","variety","various","varnish","varsity","vast","vault","vector","vegan","vegetable","vehicle","velocity","velvet","vendor","veneer","venom","vent","venture","venue","verbal","verdict","verify","verse","version","versus","vertical","very","vessel","vest","vet","veto","via","viable","vibrant","vice","victim","victory","video","view","village","villain","vine","vinegar","vineyard","vintage","viola","violate","violent","violet","violin","viral","virtual","virtue","virus","visa","vision","visit","visor","visual","vital","vitamin","vivid","vocal","vodka","voice","volcano","volleyball","volume","volunteer","vote","voucher","vow","vowel","voyage","vulgar","vulnerable","wacky","wade","waffle","waft","wag","wage","wagon","wail","waist","wait","waive","wake","walk","wall","wallet","walnut","walrus","waltz","wander","want","war","warden","wardrobe","warehouse","warfare","warm","warn","warp","warrant","warrior","wary","wash","wasp","waste","watch","water","waterfall","wave","wax","way","weak","wealth","weapon","wear","weasel","weather","weave","web","wedding","wedge","weed","week","weep","weigh","weird","welcome","welfare","well","west","western","wet","whack","whale","what","wheat","wheel","when","where","which","whiff","while","whim","whip","whirl","whisk","whistle","white","whole","wholesale","whom","why","wick","wicked","wide","widget","widow","width","wife","wig","wild","will","wilt","wimp","win","wince","wind","window","wine","wing","wink","winner","winter","wipe","wire","wisdom","wise","wish","wit","witch","with","within","without","witness","witty","wizard","wobble","woe","wolf","woman","wonder","wonderful","wood","wooden","wool","word","work","world","worm","worry","worse","worth","would","wound","wrap","wreath","wreck","wrench","wrestle","wrinkle","wrist","write","wrong","yacht","yank","yard","yarn","year","yeast","yell","yellow","yes","yesterday","yet","yield","yodel","yoga","yogurt","yolk","young","your","yourself","youth","yo-yo","zany","zeal","zealous","zebra","zenith","zero","zest","zinc","zipper","zombie","zone","zoo","zoology","zoom"];

document.getElementById("generateBtn").addEventListener("click",function(){
  var wordCount=parseInt(document.getElementById("wordCount").value)||6;
  var sep=document.getElementById("separator").value||"-";
  var count=parseInt(document.getElementById("count").value)||5;
  var arr=new Uint32Array(wordCount*count);
  crypto.getRandomValues(arr);
  var results=[];
  for(var i=0;i<count;i++){
    var words=[];
    for(var j=0;j<wordCount;j++){words.push(effWords[arr[i*wordCount+j]%effWords.length]);}
    results.push(words.join(sep));
  }
  document.getElementById("result").textContent=results.join("\\n");
});
document.getElementById("copyBtn").addEventListener("click",function(){
  var text=document.getElementById("result").textContent;
  if(!text||text==="点击生成按钮开始"){showToast("请先生成口令");return;}
  navigator.clipboard.writeText(text).then(function(){showToast("已复制全部口令")});
});
</script>'''
    else:
        return '''
<script>
'use strict';
var effWords=["abacus","abdomen","abdominal","abide","abiding","ability","ablaze","able","abnormal","abrasion","abrasive","abreast","abridge","abroad","abruptly","absence","absentee","absently","absinthe","absolute","absolve","abstain","abstract","absurd","accent","acclaim","acclimate","accompany","account","accuracy","accurate","accustom","acetone","achiness","aching","acid","acorn","acquaint","acquire","acre","acrobat","acronym","acting","action","activate","activator","active","actress","actual","acute","adamant","adapt","addicted","addition","adhesive","adjoining","adjourn","adjudicate","adjust","administer","admiral","admire","admission","admit","adopt","adoring","adorn","adrift","adroit","adult","adverb","adverse","advertise","advocate","afar","affix","afflict","affluent","afford","aficionado","afloat","afoot","afraid","afterglow","afterlife","aftermath","afterward","again","ageism","agenda","agent","agile","aging","agnostic","agony","agreeable","aground","ahead","ahold","aide","ailment","aimless","airborne","airlift","airline","airlock","airmail","airplane","airport","airtight","airwaves","aisle","alarm","album","alchemy","alcohol","alert","algebra","alibi","alien","alight","align","alike","alive","alkaline","allay","allege","allergy","alleyway","alliance","allocate","allot","allowance","allude","allure","ally","almighty","almond","almost","aloft","alone","alongside","aloof","alphabet","alright","although","altitude","alto","aluminum","alumni","always","amaretto","amaze","amazingly","ambiance","ambiguity","ambiguous","ambition","ambitious","ambulance","ambush","amendable","amendment","amends","amenity","amiable","amicably","amid","amigo","amino","amiss","ammonia","ammunition","amnesia","amnesty","among","amorously","amorous","amount","amphibian","amplify","amputate","amulet","amuse","anagram","analogy","analyse","analyzer","anarchy","anatomist","anchor","anchovy","ancient","android","anemia","anew","angelfish","angelic","anger","angled","angler","angst","angstrom","anguish","angular","anhydrous","animate","anise","ankle","annex","annotate","announce","annoyance","annually","anoint","anomaly","anonymous","anorak","antacid","antelope","antenna","anthem","anthill","antibody","antics","antidote","antihero","antiquity","antisocial","antler","antonym","anvil","anybody","anymore","anxious","anywhere","aorta","apartment","apathetic","apex","aphid","apiary","apologize","apostle","appalling","appeal","appetite","applaud","appliance","appointee","appraisal","apprentice","approach","approval","apricot","april","apron","aptitude","aquaplane","aquarium","aquatic","arbitrary","archaic","archeology","archer","archrival","ardent","arduous","areaway","arena","argument","arid","arise","aristocrat","armada","armchair","armful","armoire","armory","armrest","army","aroma","arose","around","arousal","arrange","array","arrest","arrival","arrogant","arrow","arson","artichoke","artisan","artwork","ascend","ascent","ascribe","ashamed","ashen","ashore","aside","askew","aspect","aspirate","aspire","aspirin","assailant","assassin","assault","assemble","assertive","assess","assignee","assist","assume","assurance","asthma","astride","astronomy","asylum","athlete","atlas","atom","atrium","attache","attacker","attain","attend","attic","attire","attitude","attorney","attune","auction","audible","audience","august","aunt","authentic","author","autism","autistic","autograph","automaker","automated","autumn","avail","avenge","avenue","average","aversion","avert","aviation","aviator","avid","avoid","await","awake","award","aware","awash","awhile","awkward","awning","awoke","axed","axis","axle","azalea","azure","babbling","backdrop","backfield","backfire","backhand","backing","backpack","backspace","backtrack","backup","backyard","bacon","bacteria","badger","badland","bagel","baggage","baggy","bailiff","baker","bakery","balance","balcony","ballerina","ballet","balloon","ballot","balmy","bamboo","banana","bandage","bandana","bandit","bangle","banish","banjo","bankbook","banker","banner","banquet","baptize","barbed","barber","barely","barfly","bargain","barista","baritone","barley","barmaid","barnacle","barnyard","barometer","baron","barracuda","barrel","barstool","baseball","baseless","baseline","basement","bashful","basic","basil","basin","basket","bassoon","batch","bathrobe","bathroom","bathtub","baton","battalion","batter","battery","battle","bayou","bazaar","beach","beacon","beagle","beaker","beam","beanbag","beanie","bearable","beard","beast","beatbox","beatnik","beauty","became","beckon","become","bedbug","bedpost","bedrock","bedroom","bedside","bedspread","beech","beef","beeline","beeper","beer","beetle","befall","before","beggar","beginner","begonia","behalf","behave","behind","behold","beige","belch","belfry","belief","belittle","bellhop","bellow","beloved","below","beltway","bench","bendable","beneath","benefit","beret","berry","beside","bestow","betray","better","between","beverage","beware","beyond","bias","bible","bicep","bicker","bidder","biennial","bigger","bighorn","biker","bikini","billboard","billion","bimonthly","binary","binder","binding","bing","bingo","binoculars","biology","biopsy","biplane","birch","bird","birth","bishop","bison","bisque","bistro","bitmap","bivalve","bizarre","blackbird","blackhead","blackjack","blackmail","blackout","blacksmith","bladder","blade","blah","blame","bland","blank","blarney","blatant","blaze","bleach","bleak","bleep","blemish","blend","bless","blimp","blindfold","blink","blip","bliss","blister","blitz","blizzard","bloat","blockade","blogger","blond","bloom","blossom","blot","blouse","blowfish","blowout","bluebell","bluebird","bluefish","bluejay","blues","bluff","blunder","blunt","blurb","blurt","blush","boa","boast","boatload","bobcat","bodily","bogus","boil","boiler","boldness","bolster","bolt","bomb","bonanza","bonding","boneless","bonehead","bonfire","bonnet","bonsai","bonus","boogeyman","bookcase","bookend","booklet","bookmark","bookworm","boomerang","booth","bootleg","booze","borax","border","boredom","borrower","bossy","botanical","botany","bothered","bottle","bounce","bouncy","bound","bountiful","bouquet","bourbon","bovine","bowel","bowling","boxcar","boxer","boyfriend","braces","brackish","brag","braid","brainchild","brainwash","brainy","brake","bran","brandish","brandy","brash","brass","bravado","bravo","brawny","brazen","breach","breadbox","breakable","breakaway","breakdown","breakfast","breakout","breathe","breed","breeze","brewery","bribe","brick","bridge","brief","brighten","brim","brink","brisket","briskly","bristle","brittle","broadcast","broaden","broccoli","brochure","broil","broken","bronco","bronze","brooch","brood","brook","broom","brother","brought","brownie","bruise","brunch","brunette","brush","brutal","bubble","bubbly","buckle","buddy","budge","buffalo","buffer","buffet","buggy","bugle","builder","bulb","bulkhead","bulldog","bulldoze","bullet","bullfrog","bullhorn","bullpen","bully","bumble","bump","bumpy","bunch","bungalow","bungee","bunk","bunny","burden","bureau","burger","burglar","burial","buried","burly","burner","burp","burrito","burrow","burst","busboy","bush","business","busy","butcher","butter","button","buyer","buzzard","buzzer","bygone","bypass","cabana","cabbage","cabin","cabinet","cable","caboose","cache","cackle","cactus","cadet","cafe","caffeine","caftan","cage","cajole","cake","calamari","calcium","calculate","calibrate","caller","callous","calm","calorie","camel","cameo","camera","campaign","camper","campus","canary","cancel","candid","candle","candy","cane","canine","canister","cannabis","canned","cannoli","canoe","canopy","canteen","canvas","canyon","capable","capacity","cape","capillary","capital","capitol","caplet","capricorn","capsize","capsule","captain","caption","captivate","captive","capture","caramel","carat","caravan","carbon","cardboard","cardigan","cardinal","career","carefree","careless","caress","caretaker","cargo","caribou","carnation","carnival","carol","carpenter","carpet","carport","carriage","carrier","carrot","carryout","cartel","carton","cartoon","cartwheel","carve","cashew","cashier","casino","casserole","cassette","castanet","castle","casual","catacomb","catalog","catalyst","catapult","catastrophe","catch","categorize","cathedral","catholic","cattle","cauldron","cauliflower","causal","caution","cavalry","cave","caviar","cayenne","cease","cedar","celery","celestial","cellar","cellphone","cellular","cement","cemetery","censor","census","centipede","central","ceramic","cereal","cerebral","certain","certify","cervix","chafe","chaff","chain","chairlift","chalet","chalk","challenge","chamber","champion","chance","chandelier","change","channel","chant","chaos","chapel","chapter","character","chard","charge","charity","charm","chart","chase","chassis","chastise","chat","chatter","cheap","cheat","checkbook","checklist","checkout","checkup","cheddar","cheek","cheer","cheese","cheetah","chef","chemist","cherish","cherry","chess","chestnut","chevy","chew","chicken","chide","chief","child","chili","chill","chime","chimney","chimpanzee","china","chipmunk","chirp","chisel","chive","chlorine","chocolate","choice","choir","cholesterol","choosy","chopstick","chowder","chrome","chronic","chuckle","chug","chummy","chunk","church","churn","chutney","cider","cigar","cilantro","cinema","cinnamon","circuit","circulate","circus","citation","citizen","citrus","cityscape","civic","civilian","clam","clambake","clamp","clandestine","clap","clarify","clarity","clash","classic","classify","clatter","clause","claw","clay","cleanse","clearance","cleat","cleaver","cleft","clergy","clerk","clever","cliche","click","clientele","cliff","climate","clinch","cling","clinic","clipboard","clique","cloak","clobber","clock","clone","close","closet","cloth","cloudburst","cloudy","clout","clover","club","cluck","clue","clump","clumsy","cluster","clutch","coach","coal","coast","cobalt","cobweb","cockroach","cocktail","coconut","cocoon","cod","coexist","coffee","cog","cognition","cognac","coherent","coil","coin","coincide","cola","cold","coleslaw","coliseum","collage","collapsible","collar","college","collide","collusion","cologne","colonel","colony","colossal","column","combat","combine","combust","comeback","comedian","comedy","comet","comfort","comical","comma","commence","commerce","commit","common","communal","commuter","compact","companion","compare","compel","compete","compile","complex","compliment","comply","compose","compound","compress","comprise","computer","comrade","conceal","concede","conceive","concept","concern","concert","conch","conclude","concrete","condition","condo","condor","conductor","cone","confess","confetti","confide","confine","confirm","conflict","conform","confound","confront","confuse","congeal","congress","conifer","conjure","connect","conquer","conscience","conscious","consent","conserve","consider","consist","console","consonant","conspire","constant","constrain","construct","consult","consumer","contact","contagious","contain","contend","content","contest","context","contour","contract","contrast","contribute","control","convene","convent","converge","converse","convert","convey","convict","convince","convoy","cookbook","cookie","cooking","coolant","cooperate","coordinate","copilot","copious","copper","copycat","coral","cord","cordial","core","cork","cornbread","corner","cornfield","cornstalk","corporate","corral","correct","corridor","corrode","corsage","cosmetic","cosmic","costume","cottage","cotton","couch","cougar","cough","could","countdown","counter","county","couple","coupon","courage","courier","course","courtroom","cousin","cove","covenant","cover","covert","coward","cowbell","cowboy","coyote","crab","crackdown","cracker","crackle","cradle","craft","cram","cramp","crane","crank","crater","crawl","crayon","crazy","creak","cream","create","creature","credible","credit","creed","creek","creep","crepe","crescent","crest","crew","crib","cricket","cringe","crisp","critic","croak","crock","crook","croon","crop","crossbow","crossing","crossword","crouch","crowbar","crowd","crown","crucial","crude","cruise","crumb","crunch","crusade","crush","crust","crybaby","cryptic","crystal","cubicle","cucumber","cuddle","cue","cuff","cuisine","culprit","cultivate","cultural","cumin","cupboard","cupcake","cupid","curator","curb","curdle","curfew","curio","curl","currant","currency","current","curriculum","curry","cursive","cursor","curtail","curtain","curvy","cushion","custody","custom","customer","cutback","cute","cuticle","cutoff","cycle","cylinder","cymbal","cynical","cypress","dabble","dad","daffodil","dagger","daily","dainty","dairy","daisy","dally","damage","dampen","dance","danger","dangle","dapper","daredevil","daring","darken","darling","dartboard","dashboard","database","datebook","daughter","daunting","dawdle","dawn","daybed","daybreak","daydream","daylight","daytime","daze","dazzle","deadbolt","deaden","deaf","dealer","dear","death","debatable","debate","debit","debris","debtor","decade","decaf","decal","decay","deceit","deceive","decent","decibel","decimal","decision","declare","decline","decompose","decor","decoy","decrease","dedicate","deduce","deed","deem","deepen","deface","defeat","defect","defend","defer","define","deflate","deflect","defrost","deft","defuse","defy","degrade","dehydrate","deity","dejected","delay","delegate","delete","delicacy","delight","deliver","delouse","delta","deluge","delusion","deluxe","demand","demented","demeanor","demerit","demise","democrat","demolish","demon","demote","denial","denim","denote","dense","dentist","deny","deodorant","depart","depend","depict","deplete","deploy","deport","deposit","depraved","deprive","derby","derelict","derive","derrick","descend","describe","desert","design","desire","desist","desk","desolate","despair","desperate","despise","destiny","destroy","detach","detail","detect","detergent","determine","detonate","detour","detox","detract","detriment","develop","deviance","device","devil","devious","devote","devour","dew","dexterity","diabetes","diabolic","diagnose","diagonal","diagram","dial","dialect","dialogue","diamond","diaper","diary","dice","diction","did","diesel","diet","differ","digest","digit","dignify","dilate","dilemma","diligence","dill","dilute","dime","diminish","dimple","din","dine","ding","dinghy","dining","dinner","dinosaur","dioxide","diploma","dire","directions","disable","disarm","discard","disclose","disco","discord","discount","discover","discreet","discuss","disdain","disease","disfigure","disgrace","disgust","dishonest","dislike","dismal","dismantle","dismiss","disobey","disorder","dispatch","dispel","display","dispute","disrupt","dissect","dissent","dissolve","distance","distinct","distort","distract","distress","district","distrust","ditch","ditto","dive","divert","divide","divisible","divorce","dizzy","dock","doctor","document","dodge","dog","doghouse","doll","domain","domestic","domino","donate","donkey","donor","donut","door","doorknob","dormant","dorsal","dosage","double","doubt","doughnut","dowdy","dowel","downcast","downfall","downhill","download","downpour","downsize","downtown","downturn","dowry","doze","drab","draft","drag","dragon","drain","dramatic","drape","drawbridge","drawer","dreadful","dream","drench","dress","dribble","drift","drill","drink","drip","driveway","drizzle","drone","drool","drop","drought","drove","drown","drowsy","drudge","drum","dry","dual","dubious","duck","duct","dude","duffel","dugout","dull","dumb","dump","dunce","dune","dungeon","dunk","duo","duplex","duplicate","durable","duration","duress","during","dusk","dust","duty","dwarf","dwell","dye","dynamic","dynamite","dynasty","eager","eagle","early","earmark","earmuffs","earn","earplug","earring","earth","ease","easel","eastward","easygoing","eavesdrop","ebb","ebony","echo","eclipse","ecology","economic","economy","ecstatic","eddy","edge","edgy","edible","edifice","edit","educate","eel","efface","effect","effort","egg","eggplant","ego","eight","either","eject","elaborate","elastic","elated","elbow","elder","elect","elegant","element","elephant","elevate","elicit","eligible","eliminate","elite","elope","eloquent","elsewhere","elude","email","embalm","embankment","embargo","embark","embarrass","embassy","embed","emblem","embody","emboss","embrace","embroider","embryo","emerald","emerge","emission","emotion","emperor","emphasis","empire","employ","empower","empty","enable","enact","enamel","encase","enchant","enclose","encore","encounter","encourage","encroach","encrypt","encyclopedia","endanger","endear","endeavor","endless","endorse","endow","endure","enemy","energetic","energy","enforce","engage","engine","enhance","enigma","enjoy","enlighten","enlist","enormous","enough","enrage","enrich","enroll","ensure","entail","enter","entire","entrance","entree","entrust","entry","envelope","envision","envy","enzyme","epic","epidemic","episode","equal","equate","equator","equip","erase","erect","erode","erratic","error","erupt","escalate","escalator","escapade","escape","escort","esophagus","especially","espionage","essay","essence","establish","estate","estimate","estuary","eternal","ethic","etiquette","evacuate","evade","evaluate","evaporate","eve","even","event","everyday","evict","evidence","evil","evoke","evolve","exact","exam","example","excavate","exceed","excel","except","excerpt","exchange","excite","exclude","excuse","execute","exempt","exercise","exert","exhale","exhaust","exhibit","exile","exist","exit","exotic","expand","expect","expedite","expel","expense","experiment","expert","expire","explain","explode","explore","export","expose","express","extend","extra","extract","extreme","exuberant","eyebrow","eyedrop","eyeglass","eyelash","eyelid","fable","fabric","face","facial","fact","factor","faculty","fade","fail","faint","fair","fairy","faith","fake","falcon","fall","false","falter","familiar","family","famine","famous","fanatic","fancy","fantasy","farce","farewell","fascinate","fashion","fasten","fat","fatal","father","fatigue","fatten","faucet","fault","favor","fear","feast","feat","feather","feature","federal","feeble","feed","feel","feisty","feline","fellow","felt","female","feminine","fence","ferocious","ferret","ferry","fertile","fervent","festival","fetch","fetus","feud","fever","few","fiance","fiber","fiction","fidget","field","fiery","fiesta","fifteen","fifth","fifty","fight","figment","figure","filament","file","filing","fill","film","filter","filthy","final","finance","finch","find","fine","finger","finish","finite","firefly","fireman","fireplace","fireproof","firewood","firework","firm","first","fish","fishing","fist","fitness","five","fixate","fizz","flag","flair","flame","flank","flannel","flap","flare","flash","flask","flat","flatter","flavor","flaw","flea","fleck","fledge","flee","fleet","flesh","flex","flick","flier","flight","flinch","fling","flint","flip","flipper","flirt","float","flock","flood","floppy","floral","floss","flour","flow","flower","fluctuate","fluent","fluff","fluid","fluke","flunk","flush","fluster","flute","flutter","fly","foam","focus","fog","foil","fold","foliage","folk","folklore","follow","fondue","font","food","fool","footage","football","foothill","footnote","footrest","footstep","footwear","forage","forbid","force","forearm","forecast","forego","foreign","forest","forever","forfeit","forge","forgive","fork","form","formal","format","former","formula","forsake","fort","forth","fortify","fortunate","fortune","forum","forward","fossil","foster","foul","founder","fountain","four","fowl","fox","foyer","fraction","fracture","fragile","fragrant","frail","frame","frank","frantic","fraud","fray","freckle","freedom","freeway","freeze","freight","french","frequent","fresh","fret","friction","fridge","friend","fright","fringe","frog","front","frost","frown","frozen","frugal","fruit","fry","fuel","fugitive","fulfill","full","fumble","fume","fun","function","fund","fungus","funnel","funny","fur","furious","furnace","furnish","further","fury","fuse","fuss","futile","future","fuzzy","gable","gadget","gaffe","gain","galaxy","gale","gallant","gallery","galley","gallon","gallop","gamble","game","gamma","gangplank","gangster","gap","garage","garbage","garden","gargoyle","garlic","garment","garnish","garter","gas","gash","gasoline","gate","gather","gaudy","gauge","gauntlet","gauze","gave","gavel","gawk","gazelle","gazette","gear","gecko","geese","geisha","gelatin","gem","gender","genealogy","general","generate","generic","genesis","genetic","genie","genius","genome","genre","gentle","gentleman","genuine","geography","geology","geometry","geranium","gerbil","gesture","getaway","geyser","ghastly","gherkin","ghost","ghoul","giant","giddy","gift","gigantic","giggle","gild","gill","gimmick","ginger","giraffe","girdle","girl","give","glacier","glad","glamour","glance","gland","glare","glass","glaze","gleam","glee","glide","glimmer","glimpse","glisten","glitch","glitter","global","gloom","glory","gloss","glove","glow","glucose","glue","glut","glutton","gnat","gnaw","gnome","goal","goat","gobble","goblet","goddess","goggle","gold","golf","gondola","gone","gong","good","goof","google","goose","gorge","gorilla","gospel","gossip","gouge","gourmet","govern","gown","grab","grace","grad","grade","gradual","graft","graham","grain","grammar","grand","granite","grant","grape","graphic","grapple","grasp","grass","grateful","gratuity","grave","gravel","gravity","gravy","gray","graze","grease","great","greed","green","greet","grenade","grey","grid","grief","grill","grim","grime","grin","grind","grip","grit","grocery","groom","groove","gross","ground","group","grove","grow","grub","grudge","grumble","grunt","guard","guess","guest","guide","guild","guilt","guise","guitar","gulch","gull","gum","gun","guppy","gurgle","guru","gush","gust","gut","gutter","guy","guzzle","gym","habit","habitat","hacienda","hacksaw","had","haggis","hail","hair","half","halibut","hallmark","hallway","halt","ham","hamburger","hammock","hamper","hamster","handbag","handcuff","handful","handicap","handle","handmade","handout","handset","handsome","handwash","handwrite","handyman","hang","hankie","happen","happy","harass","harbor","hard","hardy","hare","harm","harp","harsh","harvest","hash","hassle","haste","hat","hatch","hate","haul","haunt","have","haven","havoc","hawk","hay","hazard","hazel","hazy","headband","headboard","headcount","headdress","headfirst","headhunter","headland","headline","headrest","headset","headway","heal","health","hear","hearse","heart","heat","heaven","heavy","heckle","hectic","hedge","heel","hefty","height","heirloom","heist","helicopter","helium","helmet","help","hem","hen","hence","herb","herd","here","heritage","hermit","hero","herring","hesitant","hexagon","heyday","hiatus","hibernate","hiccup","hide","high","highland","highlight","highway","hijack","hike","hill","hinder","hinge","hint","hippo","hire","history","hit","hitch","hive","hoard","hobbit","hobby","hockey","hoe","hog","hold","hole","hollow","holster","home","homeless","homemade","homework","honest","honey","honk","honor","hood","hoof","hook","hop","hope","horizon","hormone","horn","horrid","horror","horse","hose","host","hot","hotel","hound","hour","house","hover","how","hub","huddle","hue","hug","huge","hull","hum","human","humble","humid","humor","hump","hunch","hundred","hungry","hunk","hunt","hurdle","hurl","hurrah","hurricane","hurry","hurt","husband","hush","husk","hut","hybrid","hydrant","hydrogen","hyena","hygiene","hype","hyphen","ice","iceberg","icing","icon","idea","ideal","identical","identify","idle","idol","ignite","ignore","iguana","ill","illegal","illuminate","image","imagine","immense","immerse","immune","impact","impair","impending","imperfect","import","impose","impress","imprint","improve","impulse","inbound","incense","inch","incident","incisor","include","income","increase","indeed","index","indicate","indigo","indoor","indulge","industry","infant","inflame","inflate","inflict","inform","infringe","infuse","ingest","inhale","initial","inject","injure","inmate","inn","innate","inner","input","inquire","insane","insect","insert","inside","insist","insomnia","inspect","install","instant","instead","insult","intact","intake","integer","intend","intense","interact","interest","interim","interior","intern","internal","interval","intimate","invade","invent","invest","invite","invoice","involve","iodine","ionic","iron","irregular","irrigate","irritate","island","isolate","issue","italic","itch","item","itinerary","ivory","ivy","jab","jack","jacket","jackpot","jade","jagged","jaguar","jail","jalapeno","jam","janitor","jar","jargon","jasmine","javelin","jaw","jaywalk","jazz","jealous","jeans","jeep","jelly","jeopardy","jerk","jersey","jest","jet","jewel","jigsaw","jingle","job","jockey","jog","join","joint","joke","jolly","jolt","journal","journey","jovial","joy","jubilant","judge","judo","jug","juggle","juice","jukebox","jumbo","jump","junction","jungle","junior","junk","juror","just","juvenile","kale","kaleidoscope","kangaroo","kaput","karate","karma","kayak","kazoo","kebab","keen","keep","kennel","kept","kernel","ketchup","kettle","key","keyboard","kick","kid","kidney","kill","kimono","kin","kind","kindle","king","kiosk","kiss","kit","kitchen","kite","kitten","kitty","kiwi","knack","knee","kneel","knife","knight","knit","knob","knock","knot","know","koala","kook","kosher","kudos","label","labor","lace","lack","ladder","lady","lagoon","lake","lamb","lament","lamp","lance","land","landline","landlord","landmark","landslide","lane","language","lantern","lap","lapdog","lapse","laptop","lard","large","laser","lash","lass","lasso","last","late","lather","latitude","latrine","latter","laugh","launch","lava","lavender","lavish","law","lawn","lawsuit","lawyer","layer","lazy","lead","leaf","leak","lean","leap","learn","lease","leash","least","leather","leave","ledge","left","leg","legacy","legal","legend","leisure","lemon","lend","length","lens","leopard","less","lesson","letter","lettuce","level","lever","lexicon","liable","liberty","library","license","lick","lid","life","lift","light","like","lilac","lily","limb","lime","limit","limp","line","linen","linger","link","lint","lion","lip","lipstick","liquid","liquor","list","literacy","literal","litter","little","live","lively","liver","lizard","llama","load","loaf","loan","lobby","lobe","lobster","local","locate","lock","locker","locomotive","locust","lodge","loft","log","logic","logo","lonely","long","look","loom","loop","loose","loot","lord","lot","lotion","lottery","loud","lounge","love","low","loyal","lozenge","lucid","luck","luggage","lull","lumber","luminous","lump","lunar","lunch","lunge","lung","lurk","lush","luxury","lyric","macaroni","machine","macro","mad","magazine","maggot","magic","magnet","magnify","magnitude","maid","mail","main","mainland","maintain","majestic","major","make","malady","male","malfunction","malice","mall","mammal","mammoth","man","manage","mandate","mandolin","mangle","mango","mania","manicure","mankind","manner","mansion","mantel","manual","many","map","maple","marathon","marble","march","mare","margin","marigold","marine","marionette","maritime","mark","market","marmalade","maroon","marriage","marsh","marshmallow","mascot","mason","massage","massive","mast","master","match","mate","material","maternity","math","matrix","matter","mattress","mature","maxim","maximum","maybe","mayhem","mayo","mayor","meadow","meal","mean","measure","meat","mechanic","medal","media","medical","medicine","meditate","medium","meet","melody","melon","melt","member","memo","memoir","memory","menace","mend","mental","mention","mentor","mercy","mere","merge","merit","mermaid","merry","mesh","mess","message","metal","meteor","method","micro","microwave","midday","middle","midst","midwife","might","mighty","mild","mile","military","milk","mill","million","mime","mimic","mince","mind","mine","mini","minimum","minor","mint","minus","minute","miracle","mirror","mischief","miserable","misfit","mislead","misplace","miss","missile","missing","mission","mist","mistake","mitten","mix","mixture","moan","mob","mobile","mock","mode","model","modern","modest","modify","module","moist","molar","mold","molecule","mollusk","moment","monarch","money","monitor","monkey","monopoly","monsoon","monster","month","monument","moo","mood","moon","moose","mop","moral","more","morbid","morning","morsel","mortal","mortar","mortgage","mosaic","mosque","mosquito","moss","most","moth","mother","motion","motivate","motor","motto","mound","mountain","mouse","mouth","move","movie","mow","much","muck","mud","muffin","mug","mulch","mule","mull","multiple","mumble","mummy","munch","municipal","mural","murky","murmur","muscle","museum","mushroom","music","mussel","must","mustache","mustard","mute","mutiny","mutter","muzzle","myriad","mystery","myth","nail","name","nap","napkin","narrate","narrow","nasal","nasty","nation","native","natural","nature","naughty","nausea","naval","navigate","navy","near","neat","nebula","necessary","neck","necklace","need","needle","negative","neglect","negligee","negotiate","neighbor","neither","nematode","neon","nephew","nerve","nest","nestle","net","network","neutral","never","nevermore","new","newborn","newly","next","nibble","nice","nickel","nickname","nicotine","niece","night","nimble","nine","ninth","nip","nitrogen","no","noble","nobody","nod","noise","nomad","none","noodle","noon","normal","north","nose","nostril","notable","note","notebook","nothing","notice","notify","notion","nougat","noun","nourish","novel","novice","now","nudge","nuke","null","number","numb","nun","nurse","nut","nutmeg","nutrient","nutshell","nuzzle","oak","oasis","oat","obey","object","oblong","oboe","obscure","observe","obsolete","obstacle","obtain","obvious","occur","ocean","octagon","octave","october","octopus","odd","off","offend","offer","office","official","often","oil","okay","old","olive","omega","omelet","omit","once","one","onion","online","only","onset","onto","onward","onyx","oops","ooze","opaque","open","opera","operate","opinion","opossum","opponent","oppose","optic","optimist","option","orange","orbit","orchard","orchestra","orchid","ordeal","order","organ","organic","organize","orient","origin","ornament","orphan","ostrich","other","otter","ounce","our","out","outcome","outdoor","outer","outfield","outgoing","outlast","outlet","outline","outlook","output","outrage","outright","outside","outward","oval","oven","over","overall","overcoat","overcome","overdue","overflow","overhaul","overhead","overhear","overjoyed","overlap","overload","overlook","overnight","overpass","overreact","overseas","oversee","oversight","overtake","overtime","overwhelm","owe","owl","own","ox","oxygen","oyster","ozone","pace","pack","package","packet","pad","paddle","page","pail","pain","paint","pair","pajamas","palace","palate","pale","palm","pan","pancake","panda","panel","panic","panorama","pant","pantry","pants","papa","paper","parachute","parade","paradise","paradox","paraffin","paragraph","parallel","paralyze","paramedic","parasite","parcel","pardon","parent","parish","park","parka","parliament","parlor","parody","parrot","parsley","part","partial","particle","partner","party","pass","passage","passion","passive","passport","password","past","pasta","paste","pastime","pastor","pastry","pasture","pat","patch","patent","path","patio","patriarch","patriot","patrol","patron","pattern","pause","pavement","pavilion","paw","pawn","pay","peace","peach","peacock","peak","peanut","pear","pearl","peasant","pebble","pecan","peck","pedal","pedestrian","peek","peel","peer","pelican","pen","penalty","pencil","pendant","pending","penguin","peninsula","penny","pension","pepper","per","perceive","percent","perch","perfect","perform","perfume","perhaps","peril","period","perish","perjury","permanent","permit","peroxide","perpetual","persist","person","personal","persuade","pertain","peruse","pest","pet","petal","petite","petrify","petroleum","petticoat","pew","phantom","pharmacy","phase","pheasant","phenomena","philosophy","phoenix","phone","photon","phrase","physical","physique","piano","pick","pickle","picnic","picture","piece","pig","pigeon","pigment","pike","pile","pilgrim","pill","pillar","pillow","pilot","pimple","pin","pinafore","pine","pineapple","pink","pinnacle","pint","pioneer","pipe","pirate","pistol","piston","pit","pitch","pizza","place","placid","plague","plain","plan","plane","planet","plank","plant","plantation","plasma","plaster","plastic","plate","plateau","platform","platinum","platter","play","player","playroom","plaza","plea","please","pledge","plenty","plight","plod","plow","pluck","plug","plum","plumber","plume","plump","plunge","plural","plus","ply","pocket","pod","poem","poet","poignant","point","poise","poison","polar","pole","police","polish","politic","pollen","pollute","polo","polygon","pond","ponder","pony","pool","poor","pop","popcorn","pope","popular","porcelain","porch","porcupine","pork","port","portable","portal","porter","portion","portrait","position","positive","possess","possible","post","postal","postcard","poster","postpone","pot","potato","potential","potion","pottery","pouch","poultry","pound","pour","pout","powder","power","practice","prairie","praise","prance","pray","preach","precede","precious","precise","predator","predict","prefer","prefix","preheat","prelude","premier","premium","prepare","prescribe","present","preserve","preside","press","presto","pretend","pretty","pretzel","prevail","prevent","preview","previous","prey","price","pride","priest","primary","primate","prime","prince","principal","print","prior","prison","pristine","private","prize","pro","probable","problem","proceed","process","proclaim","produce","product","profane","profess","profile","profit","program","project","prologue","prolong","promise","promote","prompt","prone","prong","pronoun","proof","prop","propane","proper","prophet","propose","prose","protect","protein","protest","proud","prove","proverb","provide","provoke","prowl","proxy","prude","prune","pry","pseudo","psyche","psychic","public","publish","pucker","puddle","puff","pull","pulp","pulse","pump","pumpkin","punch","punctual","pungent","punish","pupil","puppet","puppy","purchase","pure","purge","purple","purpose","purr","purse","pursue","push","puzzle","pyramid","quack","quail","quaint","quake","qualify","quality","quantity","quantum","quarantine","quarrel","quarry","quarter","quash","quasi","quaver","queen","queer","quell","query","quest","question","quick","quiet","quill","quilt","quintet","quirk","quit","quiver","quiz","quota","quote","rabbi","rabbit","raccoon","race","rack","radar","radial","radiate","radical","radio","radish","radius","raffle","raft","rage","raid","rail","rain","rainbow","raise","raisin","rake","rally","ram","rambunctious","ramp","ranch","random","range","rank","ransom","rapid","rare","raspberry","rat","rate","rather","ratio","rattle","rave","raven","ravine","raw","ray","razor","reach","react","read","ready","real","realm","reap","rear","reason","rebel","recall","recede","receipt","receive","recent","recess","recipe","recite","reckless","reckon","recline","recognize","recoil","record","recover","recreation","recruit","rectangle","recycle","red","redeem","redirect","reduce","reef","refer","referee","refine","reflect","reform","refresh","refuge","refund","refuse","regain","regard","regime","region","register","regret","regular","rehearse","reign","reinforce","reject","rejoice","relapse","relate","release","relent","reliable","relic","relief","religion","relish","relocate","reluctant","rely","remain","remark","remedy","remember","remind","remnant","remote","remove","renaissance","render","renew","renovate","renown","rent","repair","repay","repeat","repel","repent","replace","replay","replica","reply","report","repose","represent","reptile","republic","repulse","reputation","request","require","rescue","research","resemble","reserve","reside","resign","resist","resolve","resonate","resort","resource","respect","respond","rest","restore","restrain","result","retail","retain","retina","retire","retract","retreat","retrieve","return","reunion","reveal","revel","revenge","revenue","revere","reverse","review","revise","revive","revolt","revolution","revolve","reward","rewrite","rhino","rhyme","rhythm","rib","ribbon","rice","rich","ride","ridge","rifle","right","rigid","rim","ring","rinse","riot","rip","ripe","ripple","rise","risk","ritual","rival","river","road","roam","roar","roast","rob","robe","robin","robot","robust","rock","rocket","rod","rodeo","role","roll","romance","romantic","roof","room","roost","root","rope","rose","rotate","rotor","rotten","rouge","rough","round","route","routine","row","royal","rub","rubber","ruby","rudder","rude","rug","ruin","rule","rum","rummage","run","rung","runner","runt","rural","rush","rust","rustic","rustle","rut","saber","sable","sacred","sad","saddle","safari","safe","saga","sage","sail","sailboat","saint","sake","salad","salami","salary","sale","saliva","salmon","salon","saloon","salsa","salt","salute","salvage","salvation","same","sample","sanction","sanctuary","sand","sandal","sandbox","sandwich","sane","sanitary","sarcasm","sardine","sash","satellite","satin","satire","satisfy","sauce","sauna","sausage","savage","save","savor","saw","say","scale","scallion","scallop","scalp","scan","scandal","scant","scar","scarce","scare","scarf","scary","scatter","scavenge","scene","scenery","scent","schedule","scheme","scholar","school","science","scissor","scoff","scold","scoop","scoot","scope","scorch","score","scorpion","scotch","scout","scram","scrap","scrape","scratch","scrawny","scream","screech","screen","screw","scribble","script","scroll","scrub","scruff","sculpt","scurry","sea","seafood","seagull","seal","seam","search","seashell","seaside","season","seat","seaweed","second","secret","section","sector","secure","sedan","sedate","sediment","see","seed","seek","seem","segment","seize","seldom","select","self","sell","semester","semicolon","seminar","senate","senator","send","senior","sensation","sense","sentence","sentiment","separate","sequence","serene","sergeant","serial","series","serious","sermon","serpent","serum","servant","serve","sesame","session","set","settle","seven","severe","sew","shabby","shack","shade","shadow","shaft","shake","shaky","shale","shall","shallow","shame","shampoo","shamrock","shape","share","shark","sharp","shatter","shave","shawl","she","shear","shed","sheep","sheer","sheet","shelf","shell","shelter","sherbet","sheriff","shield","shift","shimmer","shin","shine","shingle","ship","shirt","shiver","shock","shoe","shoo","shoot","shop","shore","short","shot","should","shout","shove","show","shower","shred","shrewd","shrimp","shrine","shrink","shroud","shrub","shrug","shuck","shuffle","shun","shush","shut","shy","sick","siege","sift","sigh","sight","sign","signal","silence","silhouette","silicon","silk","silly","silver","similar","simmer","simple","simulate","since","sincere","sing","single","sink","sip","sir","siren","sister","sit","site","situate","six","sixteen","sixty","size","skate","sketch","ski","skid","skill","skim","skin","skip","skirt","skull","skunk","sky","slab","slack","slalom","slam","slang","slant","slap","slash","slate","slave","slay","sled","sleek","sleep","sleet","sleeve","slender","slice","slick","slide","slight","slim","sling","slip","slit","slob","slope","slot","slow","slug","slum","slump","slur","sly","smack","small","smart","smash","smear","smell","smelt","smile","smirk","smith","smock","smog","smoke","smooth","smother","smudge","snack","snag","snail","snake","snap","snarl","sneak","sneer","sneeze","snicker","sniff","snip","snoop","snore","snorkel","snort","snot","snow","snub","snuff","snug","soak","soap","soar","sob","sober","soccer","social","sock","socket","soda","sodium","sofa","soft","software","soil","solar","soldier","sole","solid","solitaire","solo","solution","solve","some","somersault","son","song","sonic","soon","soothe","sophomore","soprano","sorbet","sore","sorrow","sorry","sort","soul","sound","soup","sour","source","south","souvenir","soy","space","spade","spaghetti","span","spare","spark","sparrow","spatula","spawn","speak","spear","special","species","specific","speck","spectacle","spectrum","speech","speed","spell","spend","sphere","spice","spider","spike","spill","spin","spinach","spiral","spirit","spit","spite","splash","splendid","split","spoil","spoke","sponge","sponsor","spontaneous","spooky","spoon","sport","spot","spouse","sprawl","spray","spread","spring","sprinkle","sprint","sprout","spruce","spur","spy","squabble","squad","squall","square","squash","squat","squawk","squeak","squeeze","squid","squint","squire","squirrel","stable","stack","stadium","staff","stage","stain","stair","stake","stale","stalk","stall","stamp","stance","stand","staple","star","starch","stare","start","starve","state","static","station","statistic","statue","status","stay","steady","steak","steal","steam","steel","steep","steer","stellar","stem","stench","step","stereo","stern","stew","stick","still","stilt","sting","stir","stitch","stock","stocking","stomach","stomp","stone","stood","stool","stoop","stop","storage","store","stork","storm","story","stout","stove","straight","strain","strand","strange","strap","strategy","straw","stray","streak","stream","street","strength","stress","stretch","strict","stride","strike","string","strip","stripe","strive","stroke","stroll","strong","struggle","stubborn","student","studio","study","stuff","stumble","stump","stun","stunt","stupid","sturdy","style","sub","subdue","subject","sublime","submarine","submit","subside","substance","subtle","subtract","suburb","subway","succeed","such","suction","sudden","suffer","suffix","sugar","suggest","suit","sulk","sum","summary","summer","summit","sun","sunburn","sundae","sunday","sunflower","sung","sunk","sunlight","sunny","sunset","super","superb","superior","supervise","supper","supply","support","suppose","supreme","surface","surfboard","surge","surgeon","surgery","surname","surprise","surround","survey","survive","suspect","suspend","sustain","swallow","swamp","swan","swap","swarm","sway","swear","sweat","sweater","sweep","sweet","swell","swift","swim","swing","swirl","switch","swivel","swoop","sword","symbol","symmetry","sympathy","symptom","syndrome","synonym","syntax","syrup","system","table","tablecloth","tablet","tabloid","tack","tackle","tact","tactic","tadpole","tag","tail","tailor","take","talent","talk","tall","tame","tamper","tandem","tangerine","tangle","tango","tank","tanker","tannery","tap","tape","target","tariff","tarnish","tart","task","tassel","taste","tattoo","taunt","tavern","tax","taxi","tea","teach","team","tear","tease","technical","technique","tedious","teen","teepee","telephone","television","tell","temper","temperature","temple","tempo","temporary","tempt","tenant","tend","tender","tennis","tenor","tense","tension","tent","tepid","term","terminal","terrace","terrain","terrible","territory","terror","test","testify","text","thank","that","theater","theft","their","theme","then","theory","therapy","there","therefore","thermal","thermos","these","thick","thigh","thin","think","third","thirst","thirteen","thirty","this","thorn","thorough","those","thought","thousand","thread","threat","three","thrift","thrill","thrive","throat","throb","throne","through","throw","thud","thug","thumb","thump","thunder","thus","thyme","ticket","tide","tidy","tie","tiger","tight","tile","till","tilt","timber","time","timid","tin","tinker","tinsel","tiny","tip","tiptoe","tire","tissue","title","toad","toast","today","toe","tofu","toggle","toil","token","tolerate","toll","tomato","tomb","tomorrow","ton","tone","tongue","tonight","too","tool","tooth","top","topic","topple","torch","torment","tornado","tortoise","toss","total","touch","tough","tour","tourist","tournament","toward","towel","tower","town","toxic","toy","trace","track","tractor","trade","tradition","traffic","tragedy","trail","train","trait","tram","trample","trance","tranquil","transfer","transform","translate","transmit","transparent","transport","trap","trash","trauma","travel","tray","tread","treasure","treat","treble","tree","trek","tremble","trench","trend","trespass","trial","tribe","trick","tricky","tricycle","trigger","trillion","trim","trio","trip","triple","triumph","trivial","trolley","trombone","troop","trophy","tropical","trouble","trough","troupe","trousers","trout","truce","truck","true","truly","trumpet","trunk","trust","truth","try","tsunami","tub","tuba","tube","tuck","tuesday","tuft","tug","tuition","tulip","tumble","tummy","tumor","tuna","tundra","tune","tunic","tunnel","turban","turf","turkey","turmoil","turn","turquoise","turret","turtle","tusk","tutor","tuxedo","twang","tweak","tweed","tweet","twelve","twenty","twice","twig","twilight","twin","twine","twirl","twist","twitch","two","type","typical","typo","ugly","ulcer","ultimate","umbrella","umpire","unable","unanimous","unaware","unbecoming","unbiased","unbroken","uncanny","uncertain","uncle","unclear","uncommon","uncover","under","underdog","undergo","underneath","understand","undo","uneasy","unfair","unfold","unfortunate","unhappy","unhealthy","unicorn","uniform","union","unique","unit","universe","unknown","unleash","unless","unlikely","unlisted","unpack","unplug","unravel","unreal","unrest","unsafe","unseen","unstable","unusual","unveil","unwrap","upbeat","update","upgrade","uphold","upkeep","uplift","upload","upon","upper","upright","uproar","upset","upside","upstairs","uptake","uptown","upward","uranium","urban","urchin","urge","urgent","urn","use","useful","usher","usual","utensil","utility","utilize","utmost","utopia","utter","vacant","vacation","vaccine","vacuum","vagabond","vague","valentine","valid","valley","valuable","value","valve","vampire","van","vanilla","vanish","vanity","vapor","variety","various","varnish","varsity","vast","vault","vector","vegan","vegetable","vehicle","velocity","velvet","vendor","veneer","venom","vent","venture","venue","verbal","verdict","verify","verse","version","versus","vertical","very","vessel","vest","vet","veto","via","viable","vibrant","vice","victim","victory","video","view","village","villain","vine","vinegar","vineyard","vintage","viola","violate","violent","violet","violin","viral","virtual","virtue","virus","visa","vision","visit","visor","visual","vital","vitamin","vivid","vocal","vodka","voice","volcano","volleyball","volume","volunteer","vote","voucher","vow","vowel","voyage","vulgar","vulnerable","wacky","wade","waffle","waft","wag","wage","wagon","wail","waist","wait","waive","wake","walk","wall","wallet","walnut","walrus","waltz","wander","want","war","warden","wardrobe","warehouse","warfare","warm","warn","warp","warrant","warrior","wary","wash","wasp","waste","watch","water","waterfall","wave","wax","way","weak","wealth","weapon","wear","weasel","weather","weave","web","wedding","wedge","weed","week","weep","weigh","weird","welcome","welfare","well","west","western","wet","whack","whale","what","wheat","wheel","when","where","which","whiff","while","whim","whip","whirl","whisk","whistle","white","whole","wholesale","whom","why","wick","wicked","wide","widget","widow","width","wife","wig","wild","will","wilt","wimp","win","wince","wind","window","wine","wing","wink","winner","winter","wipe","wire","wisdom","wise","wish","wit","witch","with","within","without","witness","witty","wizard","wobble","woe","wolf","woman","wonder","wonderful","wood","wooden","wool","word","work","world","worm","worry","worse","worth","would","wound","wrap","wreath","wreck","wrench","wrestle","wrinkle","wrist","write","wrong","yacht","yank","yard","yarn","year","yeast","yell","yellow","yes","yesterday","yet","yield","yodel","yoga","yogurt","yolk","young","your","yourself","youth","yo-yo","zany","zeal","zealous","zebra","zenith","zero","zest","zinc","zipper","zombie","zone","zoo","zoology","zoom"];

document.getElementById("generateBtn").addEventListener("click",function(){
  var wordCount=parseInt(document.getElementById("wordCount").value)||6;
  var sep=document.getElementById("separator").value||"-";
  var count=parseInt(document.getElementById("count").value)||5;
  var arr=new Uint32Array(wordCount*count);
  crypto.getRandomValues(arr);
  var results=[];
  for(var i=0;i<count;i++){
    var words=[];
    for(var j=0;j<wordCount;j++){words.push(effWords[arr[i*wordCount+j]%effWords.length]);}
    results.push(words.join(sep));
  }
  document.getElementById("result").textContent=results.join("\\n");
});
document.getElementById("copyBtn").addEventListener("click",function(){
  var text=document.getElementById("result").textContent;
  if(!text||text==="Click generate to start"){showToast("Please generate passphrases first");return;}
  navigator.clipboard.writeText(text).then(function(){showToast("All passphrases copied!")});
});
</script>'''


def get_email_script(is_cn):
    if is_cn:
        return '''
<script>
'use strict';
document.getElementById("provider").addEventListener("change",function(){
  document.getElementById("customDomain").disabled=this.value!=="custom";
  if(this.value==="custom")document.getElementById("customDomain").focus();
});
var adj=["cool","super","happy","mega","ultra","turbo","ninja","cyber","dark","light","fast","slow","tiny","big","red","blue","gold","wild","smart","epic"];
var noun=["panda","tiger","dragon","eagle","wolf","bear","shark","fox","hawk","lion","cat","dog","owl","bat","koala","frog","duck","pig","cow","bee"];

document.getElementById("generateBtn").addEventListener("click",function(){
  var provider=document.getElementById("provider").value;
  var customDomain=document.getElementById("customDomain").value.trim();
  var count=parseInt(document.getElementById("count").value)||10;
  if(provider==="custom"&&!customDomain){showToast("请输入自定义域名");return;}
  var arr=new Uint32Array(count*4);
  crypto.getRandomValues(arr);
  var results=[];
  for(var i=0;i<count;i++){
    var a=adj[arr[i*4]%adj.length];
    var n=noun[arr[i*4+1]%noun.length];
    var num=arr[i*4+2]%9999;
    var domain=provider==="custom"?customDomain:(provider==="random"?["gmail.com","outlook.com","yahoo.com","proton.me"][arr[i*4+3]%4]:provider);
    results.push(a+"."+n+num+"@"+domain);
  }
  document.getElementById("result").textContent=results.join("\\n");
  document.getElementById("resultCount").textContent=results.length;
});
document.getElementById("copyBtn").addEventListener("click",function(){
  var text=document.getElementById("result").textContent;
  if(!text||text==="点击生成按钮开始"){showToast("请先生成邮箱");return;}
  navigator.clipboard.writeText(text).then(function(){showToast("已复制全部邮箱")});
});
</script>'''
    else:
        return '''
<script>
'use strict';
document.getElementById("provider").addEventListener("change",function(){
  document.getElementById("customDomain").disabled=this.value!=="custom";
  if(this.value==="custom")document.getElementById("customDomain").focus();
});
var adj=["cool","super","happy","mega","ultra","turbo","ninja","cyber","dark","light","fast","slow","tiny","big","red","blue","gold","wild","smart","epic"];
var noun=["panda","tiger","dragon","eagle","wolf","bear","shark","fox","hawk","lion","cat","dog","owl","bat","koala","frog","duck","pig","cow","bee"];

document.getElementById("generateBtn").addEventListener("click",function(){
  var provider=document.getElementById("provider").value;
  var customDomain=document.getElementById("customDomain").value.trim();
  var count=parseInt(document.getElementById("count").value)||10;
  if(provider==="custom"&&!customDomain){showToast("Please enter a custom domain");return;}
  var arr=new Uint32Array(count*4);
  crypto.getRandomValues(arr);
  var results=[];
  for(var i=0;i<count;i++){
    var a=adj[arr[i*4]%adj.length];
    var n=noun[arr[i*4+1]%noun.length];
    var num=arr[i*4+2]%9999;
    var domain=provider==="custom"?customDomain:(provider==="random"?["gmail.com","outlook.com","yahoo.com","proton.me"][arr[i*4+3]%4]:provider);
    results.push(a+"."+n+num+"@"+domain);
  }
  document.getElementById("result").textContent=results.join("\\n");
  document.getElementById("resultCount").textContent=results.length;
});
document.getElementById("copyBtn").addEventListener("click",function(){
  var text=document.getElementById("result").textContent;
  if(!text||text==="Click generate to start"){showToast("Please generate emails first");return;}
  navigator.clipboard.writeText(text).then(function(){showToast("All emails copied!")});
});
</script>'''


def get_xml_script(is_cn):
    if is_cn:
        return '''
<script>
'use strict';
var fields=["id","name","email","phone","city","country","age","score","active","created"];
document.getElementById("generateBtn").addEventListener("click",function(){
  var root=document.getElementById("rootName").value.trim()||"users";
  var child=document.getElementById("childName").value.trim()||"user";
  var count=parseInt(document.getElementById("recordCount").value)||5;
  var arr=new Uint32Array(count*fields.length*2);
  crypto.getRandomValues(arr);
  var xml='<?xml version="1.0" encoding="UTF-8"?>\\n<'+root+'>';
  for(var i=0;i<count;i++){
    xml+='\\n  <'+child+'>';
    for(var j=0;j<fields.length;j++){
      var val;
      if(fields[j]==="id")val=i+1;
      else if(fields[j]==="name")val="User"+(i+1);
      else if(fields[j]==="email")val="user"+(i+1)+"@example.com";
      else if(fields[j]==="age")val=18+(arr[i*fields.length+j]%50);
      else if(fields[j]==="active")val=arr[i*fields.length+j]%2===0?"true":"false";
      else val=fields[j]+"_"+(arr[i*fields.length+j]%100);
      xml+='\\n    <'+fields[j]+'>'+val+'</'+fields[j]+'>';
    }
    xml+='\\n  </'+child+'>';
  }
  xml+='\\n</'+root+'>';
  document.getElementById("result").value=xml;
});
document.getElementById("copyBtn").addEventListener("click",function(){
  var text=document.getElementById("result").value;
  if(!text||text==="点击生成按钮获取XML数据"){showToast("请先生成XML");return;}
  navigator.clipboard.writeText(text).then(function(){showToast("已复制XML")});
});
document.getElementById("downloadBtn").addEventListener("click",function(){
  var text=document.getElementById("result").value;
  if(!text||text==="点击生成按钮获取XML数据"){showToast("请先生成XML");return;}
  var blob=new Blob([text],{type:"application/xml"});
  var a=document.createElement("a");
  a.href=URL.createObjectURL(blob);
  a.download="data.xml";
  a.click();
});
</script>'''
    else:
        return '''
<script>
'use strict';
var fields=["id","name","email","phone","city","country","age","score","active","created"];
document.getElementById("generateBtn").addEventListener("click",function(){
  var root=document.getElementById("rootName").value.trim()||"users";
  var child=document.getElementById("childName").value.trim()||"user";
  var count=parseInt(document.getElementById("recordCount").value)||5;
  var arr=new Uint32Array(count*fields.length*2);
  crypto.getRandomValues(arr);
  var xml='<?xml version="1.0" encoding="UTF-8"?>\\n<'+root+'>';
  for(var i=0;i<count;i++){
    xml+='\\n  <'+child+'>';
    for(var j=0;j<fields.length;j++){
      var val;
      if(fields[j]==="id")val=i+1;
      else if(fields[j]==="name")val="User"+(i+1);
      else if(fields[j]==="email")val="user"+(i+1)+"@example.com";
      else if(fields[j]==="age")val=18+(arr[i*fields.length+j]%50);
      else if(fields[j]==="active")val=arr[i*fields.length+j]%2===0?"true":"false";
      else val=fields[j]+"_"+(arr[i*fields.length+j]%100);
      xml+='\\n    <'+fields[j]+'>'+val+'</'+fields[j]+'>';
    }
    xml+='\\n  </'+child+'>';
  }
  xml+='\\n</'+root+'>';
  document.getElementById("result").value=xml;
});
document.getElementById("copyBtn").addEventListener("click",function(){
  var text=document.getElementById("result").value;
  if(!text||text==="Click generate to get XML data"){showToast("Please generate XML first");return;}
  navigator.clipboard.writeText(text).then(function(){showToast("XML copied!")});
});
document.getElementById("downloadBtn").addEventListener("click",function(){
  var text=document.getElementById("result").value;
  if(!text||text==="Click generate to get XML data"){showToast("Please generate XML first");return;}
  var blob=new Blob([text],{type:"application/xml"});
  var a=document.createElement("a");
  a.href=URL.createObjectURL(blob);
  a.download="data.xml";
  a.click();
});
</script>'''


def get_csv_script(is_cn):
    if is_cn:
        return '''
<script>
'use strict';
var firstNames=["张伟","王芳","李娜","刘洋","陈静","杨勇","赵敏","黄强","周丽","吴军","徐明","孙婷","马超","朱红","胡波"];
var enFirst=["James","Mary","John","Patricia","Robert","Jennifer","Michael","Linda","David","Barbara","William","Elizabeth","Richard","Susan","Joseph","Jessica","Thomas","Sarah","Christopher","Karen"];
var domains=["gmail.com","outlook.com","yahoo.com","hotmail.com","proton.me"];
document.getElementById("generateBtn").addEventListener("click",function(){
  var rows=parseInt(document.getElementById("rowCount").value)||20;
  var delim=document.getElementById("delimiter").value||",";
  var dtype=document.getElementById("dataType").value;
  var arr=new Uint32Array(rows*5);
  crypto.getRandomValues(arr);
  var headers,lines=[];
  if(dtype==="names"){
    headers=["ID","Name","Email"];
    for(var i=0;i<rows;i++){
      lines.push([i+1,firstNames[arr[i*3]%firstNames.length],firstNames[arr[i*3]%firstNames.length].toLowerCase().replace(/\\s/g,"")+arr[i*3+1]%100+"@"+domains[arr[i*3+2]%domains.length]]);
    }
  }else if(dtype==="emails"){
    headers=["ID","Email","Name"];
    for(var i=0;i<rows;i++){
      lines.push([i+1,"user"+arr[i*3]%10000+"@"+domains[arr[i*3+1]%domains.length],enFirst[arr[i*3+2]%enFirst.length]]);
    }
  }else if(dtype==="numbers"){
    headers=["ID","Value","Score","Amount","Count"];
    for(var i=0;i<rows;i++){
      lines.push([i+1,arr[i]%1000,arr[i*2]%100,arr[i*3]%10000,arr[i*4]%500]);
    }
  }else{
    headers=["ID","Name","Email","Age","Score","Active"];
    for(var i=0;i<rows;i++){
      lines.push([i+1,enFirst[arr[i*3]%enFirst.length],enFirst[arr[i*3]%enFirst.length].toLowerCase()+arr[i*3+1]%100+"@"+domains[arr[i*3+2]%domains.length],18+arr[i*4]%50,arr[i*3+1]%100,arr[i]%2===0?"Yes":"No"]);
    }
  }
  var csv=headers.join(delim)+"\\n";
  for(var i=0;i<lines.length;i++)csv+=lines[i].join(delim)+"\\n";
  document.getElementById("result").value=csv;
});
document.getElementById("copyBtn").addEventListener("click",function(){
  var text=document.getElementById("result").value;
  if(!text||text==="点击生成按钮获取CSV数据"){showToast("请先生成CSV");return;}
  navigator.clipboard.writeText(text).then(function(){showToast("已复制CSV")});
});
document.getElementById("downloadBtn").addEventListener("click",function(){
  var text=document.getElementById("result").value;
  if(!text||text==="点击生成按钮获取CSV数据"){showToast("请先生成CSV");return;}
  var BOM="\\uFEFF";
  var blob=new Blob([BOM+text],{type:"text/csv"});
  var a=document.createElement("a");
  a.href=URL.createObjectURL(blob);
  a.download="data.csv";
  a.click();
});
</script>'''
    else:
        return '''
<script>
'use strict';
var firstNames=["James","Mary","John","Patricia","Robert","Jennifer","Michael","Linda","David","Barbara","William","Elizabeth","Richard","Susan","Joseph","Jessica","Thomas","Sarah","Christopher","Karen"];
var domains=["gmail.com","outlook.com","yahoo.com","hotmail.com","proton.me"];
document.getElementById("generateBtn").addEventListener("click",function(){
  var rows=parseInt(document.getElementById("rowCount").value)||20;
  var delim=document.getElementById("delimiter").value||",";
  var dtype=document.getElementById("dataType").value;
  var arr=new Uint32Array(rows*5);
  crypto.getRandomValues(arr);
  var headers,lines=[];
  if(dtype==="names"){
    headers=["ID","Name","Email"];
    for(var i=0;i<rows;i++){
      lines.push([i+1,firstNames[arr[i*3]%firstNames.length],firstNames[arr[i*3]%firstNames.length].toLowerCase()+arr[i*3+1]%100+"@"+domains[arr[i*3+2]%domains.length]]);
    }
  }else if(dtype==="emails"){
    headers=["ID","Email","Name"];
    for(var i=0;i<rows;i++){
      lines.push([i+1,"user"+arr[i*3]%10000+"@"+domains[arr[i*3+1]%domains.length],firstNames[arr[i*3+2]%firstNames.length]]);
    }
  }else if(dtype==="numbers"){
    headers=["ID","Value","Score","Amount","Count"];
    for(var i=0;i<rows;i++){
      lines.push([i+1,arr[i]%1000,arr[i*2]%100,arr[i*3]%10000,arr[i*4]%500]);
    }
  }else{
    headers=["ID","Name","Email","Age","Score","Active"];
    for(var i=0;i<rows;i++){
      lines.push([i+1,firstNames[arr[i*3]%firstNames.length],firstNames[arr[i*3]%firstNames.length].toLowerCase()+arr[i*3+1]%100+"@"+domains[arr[i*3+2]%domains.length],18+arr[i*4]%50,arr[i*3+1]%100,arr[i]%2===0?"Yes":"No"]);
    }
  }
  var csv=headers.join(delim)+"\\n";
  for(var i=0;i<lines.length;i++)csv+=lines[i].join(delim)+"\\n";
  document.getElementById("result").value=csv;
});
document.getElementById("copyBtn").addEventListener("click",function(){
  var text=document.getElementById("result").value;
  if(!text||text==="Click generate to get CSV data"){showToast("Please generate CSV first");return;}
  navigator.clipboard.writeText(text).then(function(){showToast("CSV copied!")});
});
document.getElementById("downloadBtn").addEventListener("click",function(){
  var text=document.getElementById("result").value;
  if(!text||text==="Click generate to get CSV data"){showToast("Please generate CSV first");return;}
  var BOM="\\uFEFF";
  var blob=new Blob([BOM+text],{type:"text/csv"});
  var a=document.createElement("a");
  a.href=URL.createObjectURL(blob);
  a.download="data.csv";
  a.click();
});
</script>'''


def get_fake_person_script(is_cn):
    if is_cn:
        return '''
<script>
'use strict';
var cnSurnames=["王","李","张","刘","陈","杨","黄","赵","周","吴","徐","孙","马","朱","胡","郭","何","林","高","罗","郑","梁","谢","宋","唐","韩","曹","许","邓","萧","冯","曾","程","蔡","彭","潘","袁","于","董","余","苏","叶","吕","魏","蒋","田","杜","丁","沈","姜","范","江","傅","钟","卢","汪","戴","崔","任","陆","廖","姚","方","金","邱","夏","谭","韦","贾","邹","石","熊","孟","秦","阎","薛","侯","雷","白","龙","段","郝","孔","邵","史","毛","常","万","顾","赖","武","康","贺","严","尹","钱","施","牛","洪","龚"];
var cnMale=["伟","强","磊","军","勇","杰","涛","明","超","辉","鹏","浩","亮","刚","健","飞","毅","俊","峰","宁","建","文","斌","博","华","宇","然","宏","志","立","国","林","峰","海","波","彬","恒","祥","瑞","嘉","铭","哲","翰","诚","睿","晟","毅","昊","然","轩"];
var cnFemale=["芳","敏","静","丽","艳","娟","霞","秀","婷","慧","洁","兰","萍","红","玲","燕","琳","雪","怡","娜","蓉","莉","莹","晶","洋","妍","婉","瑶","倩","佳","悦","萱","琪","颖","蕾","妮","薇","菲","芸","欣","馨","怡","嘉","梓","涵","诗","雨","梦","彤"];
var enFirstM=["James","John","Robert","Michael","William","David","Richard","Joseph","Thomas","Charles","Daniel","Matthew","Anthony","Mark","Donald","Steven","Paul","Andrew","Joshua","Kenneth"];
var enFirstF=["Mary","Patricia","Jennifer","Linda","Barbara","Elizabeth","Susan","Jessica","Sarah","Karen","Lisa","Nancy","Betty","Margaret","Sandra","Ashley","Dorothy","Kimberly","Emily","Donna"];
var enLast=["Smith","Johnson","Williams","Brown","Jones","Garcia","Miller","Davis","Rodriguez","Martinez","Hernandez","Lopez","Gonzalez","Wilson","Anderson","Thomas","Taylor","Moore","Jackson","Martin"];
var citiesCN=["北京","上海","广州","深圳","成都","杭州","南京","武汉","西安","重庆","长沙","青岛","大连","厦门","苏州","天津","郑州","济南","合肥","福州"];
var citiesUS=["New York","Los Angeles","Chicago","Houston","Phoenix","Philadelphia","San Antonio","San Diego","Dallas","San Jose","Austin","Jacksonville","Fort Worth","Columbus","Charlotte"];
var companies=["阿里巴巴","腾讯","百度","字节跳动","华为","京东","美团","小米","网易","拼多多","Google","Microsoft","Apple","Amazon","Meta","Netflix","Tesla","Oracle","IBM","Intel"];
var jobs=["软件工程师","产品经理","设计师","数据分析师","运营经理","市场总监","前端开发","后端开发","DevOps工程师","项目经理"];

document.getElementById("generateBtn").addEventListener("click",function(){
  var gender=document.getElementById("gender").value;
  var country=document.getElementById("country").value;
  var count=parseInt(document.getElementById("count").value)||1;
  var arr=new Uint32Array(count*20);
  crypto.getRandomValues(arr);
  var results=[];
  for(var k=0;k<count;k++){
    var g=gender==="random"?(arr[k]%2===0?"male":"female"):gender;
    var isCN=country==="CN"||(country==="random"&&arr[k+1]%2===0);
    var surname,firstName,email,city,company,job;
    if(isCN){
      surname=cnSurnames[arr[k*3]%cnSurnames.length];
      firstName=g==="male"?cnMale[arr[k*3+1]%cnMale.length]:cnFemale[arr[k*3+1]%cnFemale.length];
      email=surname+firstName.toLowerCase()+arr[k*3+2]%100+"@qq.com";
      city=citiesCN[arr[k*4]%citiesCN.length];
      company=companies[arr[k*5]%10];
      job=jobs[arr[k*6]%jobs.length];
    }else{
      surname=enLast[arr[k*3]%enLast.length];
      firstName=g==="male"?enFirstM[arr[k*3+1]%enFirstM.length]:enFirstF[arr[k*3+1]%enFirstF.length];
      email=firstName.toLowerCase()+"."+surname.toLowerCase()+arr[k*3+2]%100+"@gmail.com";
      city=citiesUS[arr[k*4]%citiesUS.length];
      company=companies[10+(arr[k*5]%10)];
      job="Software Engineer";
    }
    var phone=isCN?"1"+String(3+arr[k*7]%9)+String(arr[k*8]%100000000).padStart(8,"0"):"("+String(200+arr[k*7]%800)+") "+String(200+arr[k*8]%800)+"-"+String(arr[k*9]%10000).padStart(4,"0");
    results.push({
      name:surname+firstName,
      gender:g==="male"?"男":"女",
      email:email,
      phone:phone,
      country:isCN?"中国":"United States",
      city:city,
      company:company,
      job:job,
      age:18+arr[k*10]%50,
      birthday:(2026-(18+arr[k*10]%50))+"-"+(1+arr[k*11]%12).toString().padStart(2,"0")+"-"+(1+arr[k*12]%28).toString().padStart(2,"0")
    });
  }
  document.getElementById("result").value=JSON.stringify(results.length===1?results[0]:results,null,2);
});
document.getElementById("copyBtn").addEventListener("click",function(){
  var text=document.getElementById("result").value;
  if(!text||text==="点击生成按钮获取人物数据"){showToast("请先生成人物");return;}
  navigator.clipboard.writeText(text).then(function(){showToast("已复制JSON")});
});
</script>'''
    else:
        return '''
<script>
'use strict';
var enFirstM=["James","John","Robert","Michael","William","David","Richard","Joseph","Thomas","Charles","Daniel","Matthew","Anthony","Mark","Donald","Steven","Paul","Andrew","Joshua","Kenneth"];
var enFirstF=["Mary","Patricia","Jennifer","Linda","Barbara","Elizabeth","Susan","Jessica","Sarah","Karen","Lisa","Nancy","Betty","Margaret","Sandra","Ashley","Dorothy","Kimberly","Emily","Donna"];
var enLast=["Smith","Johnson","Williams","Brown","Jones","Garcia","Miller","Davis","Rodriguez","Martinez","Hernandez","Lopez","Gonzalez","Wilson","Anderson","Thomas","Taylor","Moore","Jackson","Martin"];
var citiesUS=["New York","Los Angeles","Chicago","Houston","Phoenix","Philadelphia","San Antonio","San Diego","Dallas","San Jose","Austin","Jacksonville","Fort Worth","Columbus","Charlotte"];
var citiesUK=["London","Manchester","Birmingham","Leeds","Liverpool","Glasgow","Sheffield","Bristol","Edinburgh","Leicester"];
var citiesCN=["Beijing","Shanghai","Guangzhou","Shenzhen","Chengdu","Hangzhou","Nanjing","Wuhan","Xi'an","Chongqing"];
var companies=["Google","Microsoft","Apple","Amazon","Meta","Netflix","Tesla","Oracle","IBM","Intel","Alibaba","Tencent","Baidu","ByteDance","Huawei"];
var jobs=["Software Engineer","Product Manager","Designer","Data Analyst","Marketing Manager","Frontend Developer","Backend Developer","DevOps Engineer","Project Manager","UX Designer"];

document.getElementById("generateBtn").addEventListener("click",function(){
  var gender=document.getElementById("gender").value;
  var country=document.getElementById("country").value;
  var count=parseInt(document.getElementById("count").value)||1;
  var arr=new Uint32Array(count*20);
  crypto.getRandomValues(arr);
  var results=[];
  for(var k=0;k<count;k++){
    var g=gender==="random"?(arr[k]%2===0?"male":"female"):gender;
    var isCN=country==="CN";
    var isUK=country==="UK";
    var surname,firstName,email,city,comp,job,ctry;
    if(isCN){
      surname=enLast[arr[k*3]%enLast.length];
      firstName=g==="male"?enFirstM[arr[k*3+1]%enFirstM.length]:enFirstF[arr[k*3+1]%enFirstF.length];
      email=firstName.toLowerCase()+"."+surname.toLowerCase()+arr[k*3+2]%100+"@qq.com";
      city=citiesCN[arr[k*4]%citiesCN.length];
      comp=companies[10+(arr[k*5]%5)];
      ctry="China";
    }else{
      surname=enLast[arr[k*3]%enLast.length];
      firstName=g==="male"?enFirstM[arr[k*3+1]%enFirstM.length]:enFirstF[arr[k*3+1]%enFirstF.length];
      email=firstName.toLowerCase()+"."+surname.toLowerCase()+arr[k*3+2]%100+"@gmail.com";
      city=isUK?citiesUK[arr[k*4]%citiesUK.length]:citiesUS[arr[k*4]%citiesUS.length];
      comp=companies[arr[k*5]%10];
      ctry=isUK?"United Kingdom":"United States";
    }
    job=jobs[arr[k*6]%jobs.length];
    var phone="("+String(200+arr[k*7]%800)+") "+String(200+arr[k*8]%800)+"-"+String(arr[k*9]%10000).padStart(4,"0");
    results.push({
      name:firstName+" "+surname,
      gender:g==="male"?"Male":"Female",
      email:email,
      phone:phone,
      country:ctry,
      city:city,
      company:comp,
      job:job,
      age:18+arr[k*10]%50,
      birthday:(2026-(18+arr[k*10]%50))+"-"+(1+arr[k*11]%12).toString().padStart(2,"0")+"-"+(1+arr[k*12]%28).toString().padStart(2,"0")
    });
  }
  document.getElementById("result").value=JSON.stringify(results.length===1?results[0]:results,null,2);
});
document.getElementById("copyBtn").addEventListener("click",function(){
  var text=document.getElementById("result").value;
  if(!text||text==="Click generate to get person data"){showToast("Please generate person data first");return;}
  navigator.clipboard.writeText(text).then(function(){showToast("JSON copied!")});
});
</script>'''


# ========== MAIN ==========
if __name__ == "__main__":
    for tool in TOOLS:
        slug = tool["slug"]
        # CN version
        cn_dir = os.path.join(BASE, slug)
        os.makedirs(cn_dir, exist_ok=True)
        cn_html = build_tool_page(tool, "zh")
        cn_path = os.path.join(cn_dir, "index.html")
        with open(cn_path, "w", encoding="utf-8") as f:
            f.write(cn_html)
        print(f"✅ CN: {slug}/index.html")
        
        # EN version
        en_dir = os.path.join(BASE, "en", slug)
        os.makedirs(en_dir, exist_ok=True)
        en_html = build_tool_page(tool, "en")
        en_path = os.path.join(en_dir, "index.html")
        with open(en_path, "w", encoding="utf-8") as f:
            f.write(en_html)
        print(f"✅ EN: en/{slug}/index.html")
    
    print(f"\n🎉 Total: {len(TOOLS)} tools created (CN+EN)")