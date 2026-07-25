#!/usr/bin/env python3
"""批量生成10个工具（中文+英文）+ 同步首页卡片"""

import os, re

BASE = '/home/chison/tools-site'

# 10个工具定义
TOOLS = [
    {
        "slug": "pig-latin-translator",
        "cn_name": "🐷 猪拉丁语翻译器",
        "en_name": "🐷 Pig Latin Translator",
        "cn_desc": "将英文文本转换为猪拉丁语（Pig Latin）。输入英文句子，自动输出猪拉丁语版本。",
        "en_desc": "Convert English text to Pig Latin. Enter English sentences and get the Pig Latin version automatically.",
        "cn_title": "猪拉丁语翻译器 - Free ToolBase",
        "en_title": "Pig Latin Translator - Free ToolBase",
        "category": "text-tools",
        "cn_icon": "🐷",
        "en_icon": "🐷",
        "cn_hero": "免费在线猪拉丁语翻译器，将英文文本转换为Pig Latin。支持实时转换，一键复制。无需注册，数据不上传服务器。",
        "en_hero": "Free online Pig Latin Translator. Convert English text to Pig Latin instantly. No signup required, all processing done locally.",
        "cn_badges": "实时转换 零依赖 隐私安全",
        "en_badges": "Real-time Zero-dependency Private",
    },
    {
        "slug": "sip-calculator",
        "cn_name": "💰 SIP投资计算器",
        "en_name": "💰 SIP Investment Calculator",
        "cn_desc": "计算定期定额投资(SIP)的预期收益。输入月投金额、年化收益率和投资年限，查看最终价值和总收益。",
        "en_desc": "Calculate expected returns from Systematic Investment Plan (SIP). Enter monthly amount, annual return rate, and years to see final value.",
        "cn_title": "SIP投资计算器 - Free ToolBase",
        "en_title": "SIP Investment Calculator - Free ToolBase",
        "category": "finance-tools",
        "cn_icon": "💰",
        "en_icon": "💰",
        "cn_hero": "免费在线SIP投资计算器，计算定期定额投资的复利收益。输入月投金额、年化收益率和投资年限，查看最终价值、总投入和总收益。支持图表可视化。",
        "en_hero": "Free online SIP Investment Calculator. Calculate compound returns from regular investments. Enter monthly amount, annual rate, and duration to see final value and total gains.",
        "cn_badges": "复利计算 图表可视化 隐私安全",
        "en_badges": "Compound Interest Charts Private",
    },
    {
        "slug": "chess-timer",
        "cn_name": "♟️ 国际象棋计时器",
        "en_name": "♟️ Chess Timer",
        "cn_desc": "双人国际象棋计时器，支持自定义时间和加秒。双方轮流计时，到时间为零自动提示。",
        "en_desc": "Two-player chess clock with customizable time and increment. Alternating timer with automatic timeout alert.",
        "cn_title": "国际象棋计时器 - Free ToolBase",
        "en_title": "Chess Timer - Free ToolBase",
        "category": "game-tools",
        "cn_icon": "♟️",
        "en_icon": "♟️",
        "cn_hero": "免费在线国际象棋计时器，模拟真实棋钟。支持自定义初始时间、加秒设置，双人轮流计时。适合国际象棋、围棋等需要计时的对弈。",
        "en_hero": "Free online Chess Timer simulating a real chess clock. Customizable initial time and increment. Perfect for chess, Go, and other timed games.",
        "cn_badges": "双人计时 加秒模式 音效提示",
        "en_badges": "Two-player Increment Sound Alert",
    },
    {
        "slug": "pixel-to-em",
        "cn_name": "📐 PX转EM转换器",
        "en_name": "📐 PX to EM Converter",
        "cn_desc": "将像素(PX)值转换为EM单位。输入像素值和基准字号，自动计算对应的EM值。",
        "en_desc": "Convert pixel (PX) values to EM units. Enter pixel value and base font size to get the corresponding EM value.",
        "cn_title": "PX转EM转换器 - Free ToolBase",
        "en_title": "PX to EM Converter - Free ToolBase",
        "category": "dev-tools",
        "cn_icon": "📐",
        "en_icon": "📐",
        "cn_hero": "免费在线PX转EM转换器，帮助前端开发者将像素值转换为响应式EM单位。支持自定义基准字号，批量转换，查看常用对照表。",
        "en_hero": "Free online PX to EM converter for frontend developers. Convert pixel values to responsive EM units. Custom base size, batch conversion, and common reference table.",
        "cn_badges": "前端必备 批量转换 对照表",
        "en_badges": "Frontend Batch Table",
    },
    {
        "slug": "em-to-px",
        "cn_name": "📏 EM转PX转换器",
        "en_name": "📏 EM to PX Converter",
        "cn_desc": "将EM单位转换为像素(PX)值。输入EM值和基准字号，自动计算对应的像素值。",
        "en_desc": "Convert EM units to pixel (PX) values. Enter EM value and base font size to get the corresponding pixel value.",
        "cn_title": "EM转PX转换器 - Free ToolBase",
        "en_title": "EM to PX Converter - Free ToolBase",
        "category": "dev-tools",
        "cn_icon": "📏",
        "en_icon": "📏",
        "cn_hero": "免费在线EM转PX转换器，将EM单位转换为像素值。支持自定义基准字号，批量转换。前端开发必备工具。",
        "en_hero": "Free online EM to PX converter. Convert EM units to pixel values. Custom base font size, batch conversion. Essential tool for frontend developers.",
        "cn_badges": "前端必备 批量转换 精准快速",
        "en_badges": "Frontend Batch Precise",
    },
    {
        "slug": "lottery-generator",
        "cn_name": "🎰 彩票号码生成器",
        "en_name": "🎰 Lottery Number Generator",
        "cn_desc": "随机生成彩票号码，支持双色球、大乐透等多种玩法。一键生成机选号码。",
        "en_desc": "Randomly generate lottery numbers for various lottery games. One-click random number generation.",
        "cn_title": "彩票号码生成器 - Free ToolBase",
        "en_title": "Lottery Number Generator - Free ToolBase",
        "category": "fun-tools",
        "cn_icon": "🎰",
        "en_icon": "🎰",
        "cn_hero": "免费在线彩票号码生成器，随机生成中国和美国常见彩票号码。支持双色球、大乐透、Powerball、Mega Millions等玩法。纯随机算法。",
        "en_hero": "Free online Lottery Number Generator. Randomly generate numbers for popular lotteries including Powerball, Mega Millions, EuroMillions. Pure random algorithm.",
        "cn_badges": "多玩法 真随机 一键生成",
        "en_badges": "Multi-game Random One-click",
    },
    {
        "slug": "yes-no",
        "cn_name": "🎯 是/否决策器",
        "en_name": "🎯 Yes or No Decision Maker",
        "cn_desc": "随机生成是或否的决策答案。适用于快速做决定的场景，附带趣味动画效果。",
        "en_desc": "Randomly generate yes or no decisions. Perfect for quick decision making with fun animation effects.",
        "cn_title": "是/否决策器 - Free ToolBase",
        "en_title": "Yes or No Decision Maker - Free ToolBase",
        "category": "fun-tools",
        "cn_icon": "🎯",
        "en_icon": "🎯",
        "cn_hero": "免费在线是/否决策器，当你犹豫不决时帮你做决定。点击按钮即可获得随机'是'或'否'答案，附带趣味动画。适合日常小决策。",
        "en_hero": "Free online Yes or No Decision Maker. Get a random yes or no answer when you can't decide. Fun animation included. Perfect for everyday small decisions.",
        "cn_badges": "趣味动画 纯随机 一秒决策",
        "en_badges": "Fun Animation Random Quick",
    },
    {
        "slug": "flip-text",
        "cn_name": "🪞 文字翻转器",
        "en_name": "🪞 Flip Text Generator",
        "cn_desc": "将文字水平翻转或上下颠倒。支持镜像翻转、倒置翻转和反向翻转三种模式。",
        "en_desc": "Flip text horizontally or upside down. Supports mirror flip, upside-down flip, and reverse flip modes.",
        "cn_title": "文字翻转器 - Free ToolBase",
        "en_title": "Flip Text Generator - Free ToolBase",
        "category": "text-tools",
        "cn_icon": "🪞",
        "en_icon": "🪞",
        "cn_hero": "免费在线文字翻转器，将普通文字转换为镜像、倒置或反向版本。支持三种翻转模式，用于创意设计、社交媒体和趣味玩法。",
        "en_hero": "Free online Flip Text Generator. Convert normal text to mirrored, upside-down, or reversed versions. Three flip modes for creative design, social media, and fun.",
        "cn_badges": "三种模式 实时预览 一键复制",
        "en_badges": "3 Modes Real-time Copy",
    },
    {
        "slug": "bubble-text",
        "cn_name": "🫧 泡泡文字生成器",
        "en_name": "🫧 Bubble Text Generator",
        "cn_desc": "将普通文字转换为圆圈/泡泡包围的装饰性文字。适合社交媒体和创意设计。",
        "en_desc": "Convert plain text to decorative bubble/circle-enclosed text. Perfect for social media and creative designs.",
        "cn_title": "泡泡文字生成器 - Free ToolBase",
        "en_title": "Bubble Text Generator - Free ToolBase",
        "category": "text-tools",
        "cn_icon": "🫧",
        "en_icon": "🫧",
        "cn_hero": "免费在线泡泡文字生成器，将普通文字转换为圆圈包围的可爱泡泡文字。支持大小写字母和数字转换，适合社交媒体昵称、创意设计和趣味玩法。",
        "en_hero": "Free online Bubble Text Generator. Convert plain text to cute bubble-style text with circles. Supports letters and numbers. Perfect for social media nicknames and creative designs.",
        "cn_badges": "可爱风格 社交必备 一键复制",
        "en_badges": "Cute Style Social Ready Copy",
    },
    {
        "slug": "bold-text-generator",
        "cn_name": "💪 粗体文字生成器",
        "en_name": "💪 Bold Text Generator",
        "cn_desc": "将普通文字转换为Unicode粗体、斜体、花体等装饰风格。支持多种文字风格转换。",
        "en_desc": "Convert plain text to Unicode bold, italic, cursive, and other decorative styles. Multiple text style conversions.",
        "cn_title": "粗体文字生成器 - Free ToolBase",
        "en_title": "Bold Text Generator - Free ToolBase",
        "category": "text-tools",
        "cn_icon": "💪",
        "en_icon": "💪",
        "cn_hero": "免费在线粗体文字生成器，将普通文字转换为多种Unicode装饰风格。支持粗体、斜体、粗斜体、花体、双线体、等宽体等，适合社交媒体和创意设计。",
        "en_hero": "Free online Bold Text Generator. Convert plain text to various Unicode decorative styles including bold, italic, bold-italic, script, double-struck, monospace. Perfect for social media.",
        "cn_badges": "多种风格 实时预览 一键复制",
        "en_badges": "Multi-style Real-time Copy",
    },
]

# 中英文Unicode映射
BOLD = dict(zip("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789", "𝐀𝐁𝐂𝐃𝐄𝐅𝐆𝐇𝐈𝐉𝐊𝐋𝐌𝐍𝐎𝐏𝐐𝐑𝐒𝐓𝐔𝐕𝐖𝐗𝐘𝐙𝐚𝐛𝐜𝐝𝐞𝐟𝐠𝐡𝐢𝐣𝐤𝐥𝐦𝐧𝐨𝐩𝐪𝐫𝐬𝐭𝐮𝐯𝐰𝐱𝐲𝐳𝟎𝟏𝟐𝟑𝟒𝟓𝟔𝟕𝟖𝟗"))
ITALIC = dict(zip("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz", "𝐴𝐵𝐶𝐷𝐸𝐹𝐺𝐻𝐼𝐽𝐾𝐿𝑀𝑁𝑂𝑃𝑄𝑅𝑆𝑇𝑈𝑉𝑊𝑋𝑌𝑍𝑎𝑏𝑐𝑑𝑒𝑓𝑔ℎ𝑖𝑗𝑘𝑙𝑚𝑛𝑜𝑝𝑞𝑟𝑠𝑡𝑢𝑣𝑤𝑥𝑦𝑧"))
BOLD_ITALIC = dict(zip("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz", "𝑨𝑩𝑪𝑫𝑬𝑭𝑮𝑯𝑰𝑱𝑲𝑳𝑴𝑵𝑶𝑷𝑸𝑹𝑺𝑻𝑼𝑽𝑾𝑿𝒀𝒁𝒂𝒃𝒄𝒅𝒆𝒇𝒈𝒉𝒊𝒋𝒌𝒍𝒎𝒏𝒐𝒑𝒒𝒓𝒔𝒕𝒖𝒗𝒘𝒙𝒚𝒛"))
SCRIPT = dict(zip("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz", "𝒜ℬ𝒞𝒟ℰℱ𝒢ℋℐ𝒥𝒦ℒℳ𝒩𝒪𝒫𝒬ℛ𝒮𝒯𝒰𝒱𝒲𝒳𝒴𝒵𝒶𝒷𝒸𝒹ℯ𝒻ℊ𝒽𝒾𝒿𝓀𝓁𝓂𝓃ℴ𝓅𝓆𝓇𝓈𝓉𝓊𝓋𝓌𝓍𝓎𝓏"))
DOUBLE_STRUCK = dict(zip("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789", "𝔸𝔹ℂ𝔻𝔼𝔽𝔾ℍ𝕀𝕁𝕂𝕃𝕄ℕ𝕆ℙℚℝ𝕊𝕋𝕌𝕍𝕎𝕏𝕐ℤ𝕒𝕓𝕔𝕕𝕖𝕗𝕘𝕙𝕚𝕛𝕜𝕝𝕞𝕟𝕠𝕡𝕢𝕣𝕤𝕥𝕦𝕧𝕨𝕩𝕪𝕫𝟘𝟙𝟚𝟛𝟜𝟝𝟞𝟟𝟠𝟡"))
MONOSPACE = dict(zip("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789", "𝙰𝙱𝙲𝙳𝙴𝙵𝙶𝙷𝙸𝙹𝙺𝙻𝙼𝙽𝙾𝙿𝚀𝚁𝚂𝚃𝚄𝚅𝚆𝚇𝚈𝚉𝚊𝚋𝚌𝚍𝚎𝚏𝚐𝚑𝚒𝚓𝚔𝚕𝚖𝚗𝚘𝚙𝚚𝚛𝚜𝚝𝚞𝚟𝚠𝚡𝚢𝚣𝟶𝟷𝟸𝟹𝟺𝟻𝟼𝟽𝟾𝟿"))
SANS_BOLD = dict(zip("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789", "𝗔𝗕𝗖𝗗𝗘𝗙𝗚𝗛𝗜𝗝𝗞𝗟𝗠𝗡𝗢𝗣𝗤𝗥𝗦𝗧𝗨𝗩𝗪𝗫𝗬𝗭𝗮𝗯𝗰𝗱𝗲𝗳𝗴𝗵𝗶𝗷𝗸𝗹𝗺𝗻𝗼𝗽𝗾𝗿𝘀𝘁𝘂𝘃𝘄𝘅𝘆𝘇𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵"))
SANS_ITALIC = dict(zip("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz", "𝘈𝘉𝘊𝘋𝘌𝘍𝘎𝘏𝘐𝘑𝘒𝘓𝘔𝘕𝘖𝘗𝘘𝘙𝘚𝘛𝘜𝘝𝘞𝘟𝘠𝘡𝘢𝘣𝘤𝘥𝘦𝘧𝘨𝘩𝘪𝘫𝘬𝘭𝘮𝘯𝘰𝘱𝘲𝘳𝘴𝘵𝘶𝘷𝘸𝘹𝘺𝘻"))
SANS_BOLD_ITALIC = dict(zip("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz", "𝘼𝘽𝘾𝘿𝙀𝙁𝙂𝙃𝙄𝙅𝙆𝙇𝙈𝙉𝙊𝙋𝙌𝙍𝙎𝙏𝙐𝙑𝙒𝙓𝙔𝙕𝙖𝙗𝙘𝙙𝙚𝙛𝙜𝙝𝙞𝙟𝙠𝙡𝙢𝙣𝙤𝙥𝙦𝙧𝙨𝙩𝙪𝙫𝙬𝙭𝙮𝙯"))

# 翻转文字映射
FLIP_MAP = str.maketrans(
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.!?()[]{}",
    "ɐqɔpǝɟƃɥᴉɾʞlɯuodbɹsʇnʌʍxʎz∀𐐒ƆᗡƎℲ⅁HIſ⋊⅂WNOԀΌᴚS⊥∩ΛMX⅄Z0⇂↋45689¡¿)(][}{"
)
MIRROR_MAP = str.maketrans(
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "ɒdɔbɘʇǫʜiįʞlmnoqpɿƨƚuvwxyzAdↃbƎꟻGHI\uff8c\uff8aLMИO\uff8a\uff90ЯƧTUVWXYZ"
)
REVERSE_MAP = None  # just reverse

# 泡泡文字映射
BUBBLE_MAP = dict(zip(
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789",
    "ⒶⒷⒸⒹⒺⒻⒼⒽⒾⒿⓀⓁⓂⓃⓄⓅⓆⓇⓈⓉⓊⓋⓌⓍⓎⓏⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩ⓪①②③④⑤⑥⑦⑧⑨"
))

# 猪拉丁语规则
def pig_latin(text):
    vowels = set('aeiouAEIOU')
    words = text.split()
    result = []
    for word in words:
        if not word.isalpha():
            result.append(word)
            continue
        if word[0] in vowels:
            result.append(word + 'way')
        else:
            i = 0
            while i < len(word) and word[i] not in vowels:
                i += 1
            if i == len(word):
                result.append(word + 'ay')
            else:
                result.append(word[i:] + word[:i] + 'ay')
    return ' '.join(result)

# 模板
TEMPLATE_CN = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-9W1157EBQV"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-9W1157EBQV');</script>
<script>window.addEventListener("error",function(e){{if(e&&e.message===""){{e.preventDefault();}}}});window.addEventListener("unhandledrejection",function(e){{if(e&&e.reason&&e.reason.message===""){{e.preventDefault();}}}});</script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="{cn_desc}">
<meta name="keywords" content="{cn_keywords}">
<title>{cn_title}</title>
<link rel="canonical" href="https://free-toolbase.com/{slug}/">
<meta property="og:title" content="{cn_og_title}">
<meta property="og:description" content="{cn_desc}">
<meta property="og:url" content="https://free-toolbase.com/{slug}/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Free ToolBase">
<link rel="alternate" hreflang="zh" href="https://free-toolbase.com/{slug}/">
<link rel="alternate" hreflang="en" href="https://free-toolbase.com/en/{slug}/">
<link rel="alternate" hreflang="x-default" href="https://free-toolbase.com/en/{slug}/">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"SoftwareApplication","name":"{cn_name_noemoji}","description":"{cn_desc}","applicationCategory":"UtilitiesApplication","operatingSystem":"Web","offers":{{"@type":"Offer","price":"0","priceCurrency":"USD"}}}}</script>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#0f172a;color:#e2e8f0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,"PingFang SC","Microsoft YaHei",sans-serif;line-height:1.6;min-height:100vh}}
a{{color:#06b6d4;text-decoration:none}}
.container{{max-width:900px;margin:0 auto;padding:24px 16px}}
.header{{display:flex;justify-content:space-between;align-items:center;margin-bottom:24px;flex-wrap:wrap;gap:12px}}
.header h1{{font-size:1.6rem;color:#f1f5f9}}
.lang-switch{{display:flex;gap:4px;background:#1e293b;border-radius:8px;padding:4px;border:1px solid rgba(148,163,184,.1)}}
.lang-switch a{{padding:6px 12px;border-radius:5px;font-size:.85rem;color:#94a3b8}}
.lang-switch a.active{{background:rgba(6,182,212,.2);color:#22d3ee}}
.nav-back{{color:#64748b;font-size:.85rem;margin-bottom:16px}}
.nav-back a{{color:#64748b}}
.nav-back a:hover{{color:#94a3b8}}
textarea,input,select{{background:#0f172a;border:1px solid rgba(148,163,184,.2);border-radius:6px;padding:8px 12px;color:#e2e8f0;font-size:.85rem;outline:none;font-family:inherit;width:100%}}
textarea:focus,input:focus,select:focus{{border-color:rgba(6,182,212,.5)}}
.btn{{padding:8px 20px;border:none;border-radius:6px;font-size:.85rem;cursor:pointer;transition:all .2s;display:inline-flex;align-items:center;gap:4px}}
.btn-primary{{background:rgba(6,182,212,.2);color:#22d3ee;border:1px solid rgba(6,182,212,.3)}}
.btn-primary:hover{{background:rgba(6,182,212,.3)}}
.btn-secondary{{background:rgba(148,163,184,.1);color:#94a3b8;border:1px solid rgba(148,163,184,.2)}}
.btn-secondary:hover{{background:rgba(148,163,184,.2)}}
.tool-section{{background:#1e293b;border-radius:12px;padding:20px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1)}}
.tool-section h2{{font-size:1.1rem;color:#f1f5f9;margin-bottom:12px}}
.tool-section p{{color:#94a3b8;font-size:.9rem;margin-bottom:8px}}
.result-output{{background:#0f172a;border-radius:8px;padding:16px;color:#e2e8f0;font-size:.85rem;overflow-x:auto;max-height:400px;white-space:pre-wrap;word-break:break-all;margin-bottom:12px;font-family:ui-monospace,SFMono-Regular,Consolas,monospace}}
.result-actions{{display:flex;gap:8px;flex-wrap:wrap}}
.faq-item{{margin-bottom:16px}}
.faq-item h3{{font-size:.95rem;color:#e2e8f0;margin-bottom:6px}}
.faq-item p{{color:#94a3b8;font-size:.9rem}}
.footer{{border-top:1px solid rgba(148,163,184,.1);padding:24px 0;margin-top:32px;text-align:center;color:#64748b;font-size:.85rem}}
.footer a{{color:#64748b;margin:0 8px}}
.footer a:hover{{color:#94a3b8}}
.toast{{position:fixed;bottom:20px;left:50%;transform:translateX(-50%);background:#1e293b;color:#22d3ee;padding:10px 24px;border-radius:8px;border:1px solid rgba(6,182,212,.3);font-size:.85rem;z-index:999;opacity:0;transition:opacity .3s}}
.toast.show{{opacity:1}}
.hero{{margin-bottom:16px}}
.hero p{{color:#94a3b8;font-size:.95rem;margin-bottom:8px}}
.badge{{display:inline-block;background:rgba(6,182,212,.15);color:#22d3ee;padding:2px 8px;border-radius:4px;font-size:.8rem;margin-right:6px}}
.main-grid{{display:grid;grid-template-columns:1fr 300px;gap:16px}}
@media(max-width:768px){{.main-grid{{grid-template-columns:1fr}}.header h1{{font-size:1.3rem}}.btn{{padding:6px 14px;font-size:.8rem}}}}
.ad-slot{{margin:0 auto;text-align:center;max-width:960px;min-height:90px;background:rgba(148,163,184,.05);border-radius:8px}}
.ad-slot.ad-sidebar{{min-height:250px;max-width:300px}}
.seo-content{{color:#475569;font-size:.85rem;margin-top:24px}}
.seo-content h3{{color:#64748b;font-size:1rem;margin-bottom:8px}}
@media(max-width:640px){{h1{{font-size:1.2rem;word-break:break-word}}}}
.stat-row{{display:flex;gap:24px;flex-wrap:wrap}}
.stat-item{{text-align:center}}
.stat-value{{color:#22d3ee;font-weight:700;font-size:1.2rem}}
.stat-label{{color:#94a3b8;font-size:.8rem}}
</style>
<meta property="og:image" content="https://free-toolbase.com/og-image.svg">
<meta name="twitter:image" content="https://free-toolbase.com/og-image.svg">
<meta name="twitter:card" content="summary_large_image">
<meta name="robots" content="index, follow">
<link rel="icon" type="image/svg+xml" href="favicon.svg">
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5998441792679372" crossorigin="anonymous"></script>
<script type="application/ld+json">{{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{{"@type": "ListItem", "position": 1, "name": "首页", "item": "https://free-toolbase.com/"}}, {{"@type": "ListItem", "position": 2, "name": "工具", "item": "https://free-toolbase.com/#tools"}}, {{"@type": "ListItem", "position": 3, "name": "{cn_name_noemoji}", "item": "https://free-toolbase.com/{slug}/"}}]}}</script>
</head>
<body>
<div class="container">
<div class="header"><h1>{cn_icon} {cn_name_noemoji}</h1><div class="lang-switch"><a href="index.html" class="active">中文</a><a href="../en/{slug}/">EN</a></div></div>
<p class="nav-back"><a href="../index.html">首页</a> &rsaquo; <a href="../index.html#tools">工具</a> &rsaquo; {cn_name_noemoji}</p>
<div class="hero"><p>{cn_hero}</p><span class="badge">{cn_badges_withpipe}</span></div>
<div class="main-grid"><div>
{BODY_CN}
</div></div>
<div class="seo-content"><h3>关于{cn_name_noemoji}</h3><p>{cn_seo_text}</p></div>
</div>
<div>
<!-- AdSense -->
<ins class="adsbygoogle"
     style="display:block"
     data-ad-client="ca-pub-5998441792679372"
     data-ad-slot="auto"
     data-ad-format="auto"
     data-full-width-responsive="true"></ins>
<script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
<footer class="footer container">
<div style="margin-bottom:12px">
<a href="../index.html">首页</a>
<a href="../index.html">全部工具</a>
<a href="../privacy/">隐私政策</a>
<a href="../terms/">服务条款</a>
<a href="../about/">关于我们</a>
<a href="../en/{slug}/">EN</a>
</div>
<p>{cn_name_noemoji} | 无需注册 · 数据绝不上传服务器</p>
<p style="margin-top:8px;color:#475569;font-size:.8rem">问题反馈: dexshuang@google.com</p>
</footer>
<div class="toast" id="toast"></div>
</body>
</html>'''

TEMPLATE_EN = '''<!DOCTYPE html>
<html lang="en">
<head>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-9W1157EBQV"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-9W1157EBQV');</script>
<script>window.addEventListener("error",function(e){{if(e&&e.message===""){{e.preventDefault();}}}});window.addEventListener("unhandledrejection",function(e){{if(e&&e.reason&&e.reason.message===""){{e.preventDefault();}}}});</script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="{en_desc}">
<meta name="keywords" content="{en_keywords}">
<title>{en_title}</title>
<link rel="canonical" href="https://free-toolbase.com/en/{slug}/">
<meta property="og:title" content="{en_og_title}">
<meta property="og:description" content="{en_desc}">
<meta property="og:url" content="https://free-toolbase.com/en/{slug}/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Free ToolBase">
<link rel="alternate" hreflang="en" href="https://free-toolbase.com/en/{slug}/">
<link rel="alternate" hreflang="zh" href="https://free-toolbase.com/{slug}/">
<link rel="alternate" hreflang="x-default" href="https://free-toolbase.com/en/{slug}/">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"SoftwareApplication","name":"{en_name_noemoji}","description":"{en_desc}","applicationCategory":"UtilitiesApplication","operatingSystem":"Web","offers":{{"@type":"Offer","price":"0","priceCurrency":"USD"}}}}</script>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#0f172a;color:#e2e8f0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;line-height:1.6;min-height:100vh}}
a{{color:#06b6d4;text-decoration:none}}
.container{{max-width:900px;margin:0 auto;padding:24px 16px}}
.header{{display:flex;justify-content:space-between;align-items:center;margin-bottom:24px;flex-wrap:wrap;gap:12px}}
.header h1{{font-size:1.6rem;color:#f1f5f9}}
.lang-switch{{display:flex;gap:4px;background:#1e293b;border-radius:8px;padding:4px;border:1px solid rgba(148,163,184,.1)}}
.lang-switch a{{padding:6px 12px;border-radius:5px;font-size:.85rem;color:#94a3b8}}
.lang-switch a.active{{background:rgba(6,182,212,.2);color:#22d3ee}}
.nav-back{{color:#64748b;font-size:.85rem;margin-bottom:16px}}
.nav-back a{{color:#64748b}}
.nav-back a:hover{{color:#94a3b8}}
textarea,input,select{{background:#0f172a;border:1px solid rgba(148,163,184,.2);border-radius:6px;padding:8px 12px;color:#e2e8f0;font-size:.85rem;outline:none;font-family:inherit;width:100%}}
textarea:focus,input:focus,select:focus{{border-color:rgba(6,182,212,.5)}}
.btn{{padding:8px 20px;border:none;border-radius:6px;font-size:.85rem;cursor:pointer;transition:all .2s;display:inline-flex;align-items:center;gap:4px}}
.btn-primary{{background:rgba(6,182,212,.2);color:#22d3ee;border:1px solid rgba(6,182,212,.3)}}
.btn-primary:hover{{background:rgba(6,182,212,.3)}}
.btn-secondary{{background:rgba(148,163,184,.1);color:#94a3b8;border:1px solid rgba(148,163,184,.2)}}
.btn-secondary:hover{{background:rgba(148,163,184,.2)}}
.tool-section{{background:#1e293b;border-radius:12px;padding:20px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1)}}
.tool-section h2{{font-size:1.1rem;color:#f1f5f9;margin-bottom:12px}}
.tool-section p{{color:#94a3b8;font-size:.9rem;margin-bottom:8px}}
.result-output{{background:#0f172a;border-radius:8px;padding:16px;color:#e2e8f0;font-size:.85rem;overflow-x:auto;max-height:400px;white-space:pre-wrap;word-break:break-all;margin-bottom:12px;font-family:ui-monospace,SFMono-Regular,Consolas,monospace}}
.result-actions{{display:flex;gap:8px;flex-wrap:wrap}}
.faq-item{{margin-bottom:16px}}
.faq-item h3{{font-size:.95rem;color:#e2e8f0;margin-bottom:6px}}
.faq-item p{{color:#94a3b8;font-size:.9rem}}
.footer{{border-top:1px solid rgba(148,163,184,.1);padding:24px 0;margin-top:32px;text-align:center;color:#64748b;font-size:.85rem}}
.footer a{{color:#64748b;margin:0 8px}}
.footer a:hover{{color:#94a3b8}}
.toast{{position:fixed;bottom:20px;left:50%;transform:translateX(-50%);background:#1e293b;color:#22d3ee;padding:10px 24px;border-radius:8px;border:1px solid rgba(6,182,212,.3);font-size:.85rem;z-index:999;opacity:0;transition:opacity .3s}}
.toast.show{{opacity:1}}
.hero{{margin-bottom:16px}}
.hero p{{color:#94a3b8;font-size:.95rem;margin-bottom:8px}}
.badge{{display:inline-block;background:rgba(6,182,212,.15);color:#22d3ee;padding:2px 8px;border-radius:4px;font-size:.8rem;margin-right:6px}}
.main-grid{{display:grid;grid-template-columns:1fr 300px;gap:16px}}
@media(max-width:768px){{.main-grid{{grid-template-columns:1fr}}.header h1{{font-size:1.3rem}}.btn{{padding:6px 14px;font-size:.8rem}}}}
.ad-slot{{margin:0 auto;text-align:center;max-width:960px;min-height:90px;background:rgba(148,163,184,.05);border-radius:8px}}
.ad-slot.ad-sidebar{{min-height:250px;max-width:300px}}
.seo-content{{color:#475569;font-size:.85rem;margin-top:24px}}
.seo-content h3{{color:#64748b;font-size:1rem;margin-bottom:8px}}
.stat-row{{display:flex;gap:24px;flex-wrap:wrap}}
.stat-item{{text-align:center}}
.stat-value{{color:#22d3ee;font-weight:700;font-size:1.2rem}}
.stat-label{{color:#94a3b8;font-size:.8rem}}
@media(max-width:640px){{h1{{font-size:1.2rem;word-break:break-word}}}}
</style>
<meta property="og:image" content="https://free-toolbase.com/og-image.svg">
<meta name="twitter:image" content="https://free-toolbase.com/og-image.svg">
<meta name="twitter:card" content="summary_large_image">
<meta name="robots" content="index, follow">
<link rel="icon" type="image/svg+xml" href="favicon.svg">
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5998441792679372" crossorigin="anonymous"></script>
<script type="application/ld+json">{{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{{"@type": "ListItem", "position": 1, "name": "Home", "item": "https://free-toolbase.com/en/"}}, {{"@type": "ListItem", "position": 2, "name": "Tools", "item": "https://free-toolbase.com/en/#tools"}}, {{"@type": "ListItem", "position": 3, "name": "{en_name_noemoji}", "item": "https://free-toolbase.com/en/{slug}/"}}]}}</script>
</head>
<body>
<div class="container">
<div class="header"><h1>{en_icon} {en_name_noemoji}</h1><div class="lang-switch"><a href="../{slug}/">中文</a><a href="index.html" class="active">EN</a></div></div>
<p class="nav-back"><a href="../index.html">Home</a> &rsaquo; <a href="../index.html#tools">Tools</a> &rsaquo; {en_name_noemoji}</p>
<div class="hero"><p>{en_hero}</p><span class="badge">{en_badges_withpipe}</span></div>
<div class="main-grid"><div>
{BODY_EN}
</div></div>
<div class="seo-content"><h3>About {en_name_noemoji}</h3><p>{en_seo_text}</p></div>
</div>
<div>
<!-- AdSense -->
<ins class="adsbygoogle"
     style="display:block"
     data-ad-client="ca-pub-5998441792679372"
     data-ad-slot="auto"
     data-ad-format="auto"
     data-full-width-responsive="true"></ins>
<script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
<footer class="footer container">
<div style="margin-bottom:12px">
<a href="../index.html">Home</a>
<a href="../index.html">All Tools</a>
<a href="../privacy/">Privacy</a>
<a href="../terms/">Terms</a>
<a href="../about/">About</a>
<a href="../{slug}/">中文</a>
</div>
<p>{en_name_noemoji} | No signup · Data never leaves your device</p>
<p style="margin-top:8px;color:#475569;font-size:.8rem">Feedback: dexshuang@google.com</p>
</footer>
<div class="toast" id="toast"></div>
</body>
</html>'''

def build_tool_bodies():
    """Return dict of slug -> (body_cn, body_en, seo_cn, seo_en)"""
    bodies = {}

    # 1. pig-latin-translator
    bodies['pig-latin-translator'] = (
        '''<div class="tool-section">
  <h2>输入英文文本</h2>
  <textarea id="inputText" placeholder="输入英文句子，例如: Hello World..." style="min-height:120px"></textarea>
</div>
<div class="tool-section">
  <h2>猪拉丁语结果</h2>
  <div class="result-output" id="resultOutput">等待输入...</div>
  <div class="result-actions">
    <button class="btn btn-primary" onclick="convertPigLatin()">🐷 转换</button>
    <button class="btn btn-secondary" onclick="copyResult()">📋 复制结果</button>
    <button class="btn btn-secondary" onclick="clearAll()">🗑️ 清空</button>
  </div>
</div>
<div class="tool-section">
  <h2>❓ 什么是猪拉丁语？</h2>
  <div class="faq-item"><h3>猪拉丁语的规则是什么？</h3><p>猪拉丁语(Pig Latin)是一种英语文字游戏。规则：以元音开头的单词加"way"，以辅音开头的单词将辅音移到末尾加"ay"。例如"hello"→"ellohay"，"apple"→"appleway"。</p></div>
</div>
<script>
function getVowels(){{return new Set(['a','e','i','o','u','A','E','I','O','U']);}}
function pigLatinWord(word){{
  if(!word||!/[a-zA-Z]/.test(word))return word;
  var vowels=getVowels();
  if(vowels.has(word[0]))return word+'way';
  var i=0;
  while(i<word.length&&!vowels.has(word[i])&&/[a-zA-Z]/.test(word[i]))i++;
  if(i>=word.length)return word+'ay';
  return word.slice(i)+word.slice(0,i)+'ay';
}}
function convertPigLatin(){{
  var input=document.getElementById('inputText').value.trim();
  if(!input){{document.getElementById('resultOutput').textContent='请先输入英文文本';return;}}
  var words=input.split(/\\s+/);
  var result=words.map(pigLatinWord).join(' ');
  document.getElementById('resultOutput').textContent=result;
}}
function copyResult(){{
  var text=document.getElementById('resultOutput').textContent;
  if(!text||text==='等待输入...')return;
  navigator.clipboard.writeText(text).then(function(){{showToast('已复制!');}});
}}
function clearAll(){{document.getElementById('inputText').value='';document.getElementById('resultOutput').textContent='等待输入...';}}
function showToast(msg){{var t=document.getElementById('toast');t.textContent=msg;t.classList.add('show');setTimeout(function(){{t.classList.remove('show');}},2000);}}
document.getElementById('inputText').addEventListener('input',convertPigLatin);
</script>''',
        '''<div class="tool-section">
  <h2>Enter English Text</h2>
  <textarea id="inputText" placeholder="Enter English sentences, e.g. Hello World..." style="min-height:120px"></textarea>
</div>
<div class="tool-section">
  <h2>Pig Latin Result</h2>
  <div class="result-output" id="resultOutput">Waiting for input...</div>
  <div class="result-actions">
    <button class="btn btn-primary" onclick="convertPigLatin()">🐷 Convert</button>
    <button class="btn btn-secondary" onclick="copyResult()">📋 Copy</button>
    <button class="btn btn-secondary" onclick="clearAll()">🗑️ Clear</button>
  </div>
</div>
<div class="tool-section">
  <h2>❓ What is Pig Latin?</h2>
  <div class="faq-item"><h3>What are the rules of Pig Latin?</h3><p>Pig Latin is an English word game. Rules: words starting with vowels get "way" appended, words starting with consonants move the consonant cluster to the end and add "ay". E.g., "hello"→"ellohay", "apple"→"appleway".</p></div>
</div>
<script>
function getVowels(){{return new Set(['a','e','i','o','u','A','E','I','O','U']);}}
function pigLatinWord(word){{
  if(!word||!/[a-zA-Z]/.test(word))return word;
  var vowels=getVowels();
  if(vowels.has(word[0]))return word+'way';
  var i=0;
  while(i<word.length&&!vowels.has(word[i])&&/[a-zA-Z]/.test(word[i]))i++;
  if(i>=word.length)return word+'ay';
  return word.slice(i)+word.slice(0,i)+'ay';
}}
function convertPigLatin(){{
  var input=document.getElementById('inputText').value.trim();
  if(!input){{document.getElementById('resultOutput').textContent='Please enter English text first';return;}}
  var words=input.split(/\\s+/);
  var result=words.map(pigLatinWord).join(' ');
  document.getElementById('resultOutput').textContent=result;
}}
function copyResult(){{
  var text=document.getElementById('resultOutput').textContent;
  if(!text||text==='Waiting for input...')return;
  navigator.clipboard.writeText(text).then(function(){{showToast('Copied!');}});
}}
function clearAll(){{document.getElementById('inputText').value='';document.getElementById('resultOutput').textContent='Waiting for input...';}}
function showToast(msg){{var t=document.getElementById('toast');t.textContent=msg;t.classList.add('show');setTimeout(function(){{t.classList.remove('show');}},2000);}}
document.getElementById('inputText').addEventListener('input',convertPigLatin);
</script>''',
        '猪拉丁语（Pig Latin）是一种英语文字游戏，起源于19世纪末的美国儿童游戏。规则简单：以元音开头的单词加"way"，以辅音开头的单词将辅音移到末尾加"ay"。本工具实时转换，输入英文即出结果。',
        'Pig Latin is an English word game that originated as a children\'s game in late 19th century America. Simple rules: words starting with vowels get "way", consonants move to end + "ay". This tool converts in real-time.'
    )

    # 2. sip-calculator
    bodies['sip-calculator'] = (
        '''<div class="tool-section">
  <h2>投资参数</h2>
  <div style="display:flex;gap:12px;flex-wrap:wrap;margin-bottom:12px">
    <div style="flex:1;min-width:180px"><label style="color:#94a3b8;font-size:.85rem">月投金额 (¥)</label><input type="number" id="monthlyAmount" value="5000" min="100" step="100"></div>
    <div style="flex:1;min-width:180px"><label style="color:#94a3b8;font-size:.85rem">年化收益率 (%)</label><input type="number" id="annualRate" value="12" min="0" step="0.1"></div>
    <div style="flex:1;min-width:180px"><label style="color:#94a3b8;font-size:.85rem">投资年限</label><input type="number" id="years" value="10" min="1" step="1"></div>
  </div>
  <button class="btn btn-primary" onclick="calculateSIP()">💰 计算收益</button>
</div>
<div class="tool-section">
  <h2>计算结果</h2>
  <div class="stat-row" style="margin-bottom:12px">
    <div class="stat-item"><div class="stat-value" id="totalInvestment">¥0</div><div class="stat-label">总投入</div></div>
    <div class="stat-item"><div class="stat-value" id="finalValue">¥0</div><div class="stat-label">最终价值</div></div>
    <div class="stat-item"><div class="stat-value" id="totalGain">¥0</div><div class="stat-label">总收益</div></div>
    <div class="stat-item"><div class="stat-value" id="roi">0%</div><div class="stat-label">收益率</div></div>
  </div>
  <canvas id="growthChart" style="width:100%;max-height:300px"></canvas>
</div>
<script>
function calculateSIP(){{
  var monthly=parseFloat(document.getElementById('monthlyAmount').value)||5000;
  var rate=parseFloat(document.getElementById('annualRate').value)||12;
  var yrs=parseInt(document.getElementById('years').value)||10;
  var monthlyRate=rate/100/12;
  var months=yrs*12;
  var futureValue=0;
  var labels=[],data=[];
  for(var i=1;i<=months;i++){{
    futureValue=(futureValue+monthly)*(1+monthlyRate);
    if(i%12===0||i===months){{labels.push(Math.floor(i/12)+'年');data.push(Math.round(futureValue));}}
  }}
  var totalInvested=monthly*months;
  var gain=futureValue-totalInvested;
  var roiPct=totalInvested>0?(gain/totalInvested*100):0;
  document.getElementById('totalInvestment').textContent='¥'+totalInvested.toLocaleString();
  document.getElementById('finalValue').textContent='¥'+Math.round(futureValue).toLocaleString();
  document.getElementById('totalGain').textContent='¥'+Math.round(gain).toLocaleString();
  document.getElementById('roi').textContent=roiPct.toFixed(1)+'%';
  drawChart(labels,data);
}}
function drawChart(labels,data){{
  var canvas=document.getElementById('growthChart');
  var ctx=canvas.getContext('2d');
  var dpr=window.devicePixelRatio||1;
  var rect=canvas.parentElement.getBoundingClientRect();
  canvas.width=rect.width*dpr;
  canvas.height=300*dpr;
  canvas.style.width=rect.width+'px';
  canvas.style.height='300px';
  ctx.scale(dpr,dpr);
  var w=rect.width-60,h=240,ox=50,oy=20,maxVal=Math.max.apply(null,data)*1.1;
  ctx.clearRect(0,0,w+60,h+40);
  ctx.strokeStyle='rgba(148,163,184,.2)';ctx.lineWidth=1;
  for(var i=0;i<=4;i++){{var y=oy+h-h*i/4;ctx.beginPath();ctx.moveTo(ox,y);ctx.lineTo(ox+w,y);ctx.stroke();ctx.fillStyle='#64748b';ctx.font='11px sans-serif';ctx.fillText('¥'+(maxVal*i/4/10000).toFixed(0)+'万',2,y+4);}}
  labels.forEach(function(l,i){{ctx.fillStyle='#64748b';ctx.font='11px sans-serif';ctx.fillText(l,ox+i*(w/(labels.length-1||1))-10,oy+h+20);}});
  ctx.beginPath();ctx.strokeStyle='#22d3ee';ctx.lineWidth=2;
  data.forEach(function(d,i){{var x=ox+i*(w/(data.length-1||1));var y=oy+h-(d/maxVal)*h;if(i===0)ctx.moveTo(x,y);else ctx.lineTo(x,y);}});
  ctx.stroke();
  ctx.fillStyle='rgba(6,182,212,.2)';
  data.forEach(function(d,i){{var x=ox+i*(w/(data.length-1||1));var y=oy+h-(d/maxVal)*h;ctx.beginPath();ctx.arc(x,y,4,0,Math.PI*2);ctx.fill();ctx.stroke();}});
}}
window.addEventListener('load',calculateSIP);
['monthlyAmount','annualRate','years'].forEach(function(id){{document.getElementById(id).addEventListener('input',calculateSIP);}});
</script>''',
        '''<div class="tool-section">
  <h2>Investment Parameters</h2>
  <div style="display:flex;gap:12px;flex-wrap:wrap;margin-bottom:12px">
    <div style="flex:1;min-width:180px"><label style="color:#94a3b8;font-size:.85rem">Monthly Amount ($)</label><input type="number" id="monthlyAmount" value="500" min="10" step="10"></div>
    <div style="flex:1;min-width:180px"><label style="color:#94a3b8;font-size:.85rem">Annual Return (%)</label><input type="number" id="annualRate" value="12" min="0" step="0.1"></div>
    <div style="flex:1;min-width:180px"><label style="color:#94a3b8;font-size:.85rem">Years</label><input type="number" id="years" value="10" min="1" step="1"></div>
  </div>
  <button class="btn btn-primary" onclick="calculateSIP()">💰 Calculate</button>
</div>
<div class="tool-section">
  <h2>Results</h2>
  <div class="stat-row" style="margin-bottom:12px">
    <div class="stat-item"><div class="stat-value" id="totalInvestment">$0</div><div class="stat-label">Total Invested</div></div>
    <div class="stat-item"><div class="stat-value" id="finalValue">$0</div><div class="stat-label">Final Value</div></div>
    <div class="stat-item"><div class="stat-value" id="totalGain">$0</div><div class="stat-label">Total Gain</div></div>
    <div class="stat-item"><div class="stat-value" id="roi">0%</div><div class="stat-label">ROI</div></div>
  </div>
  <canvas id="growthChart" style="width:100%;max-height:300px"></canvas>
</div>
<script>
function calculateSIP(){{
  var monthly=parseFloat(document.getElementById('monthlyAmount').value)||500;
  var rate=parseFloat(document.getElementById('annualRate').value)||12;
  var yrs=parseInt(document.getElementById('years').value)||10;
  var monthlyRate=rate/100/12;
  var months=yrs*12;
  var futureValue=0;
  var labels=[],data=[];
  for(var i=1;i<=months;i++){{
    futureValue=(futureValue+monthly)*(1+monthlyRate);
    if(i%12===0||i===months){{labels.push('Yr '+Math.floor(i/12));data.push(Math.round(futureValue));}}
  }}
  var totalInvested=monthly*months;
  var gain=futureValue-totalInvested;
  var roiPct=totalInvested>0?(gain/totalInvested*100):0;
  document.getElementById('totalInvestment').textContent='$'+totalInvested.toLocaleString();
  document.getElementById('finalValue').textContent='$'+Math.round(futureValue).toLocaleString();
  document.getElementById('totalGain').textContent='$'+Math.round(gain).toLocaleString();
  document.getElementById('roi').textContent=roiPct.toFixed(1)+'%';
  drawChart(labels,data);
}}
function drawChart(labels,data){{
  var canvas=document.getElementById('growthChart');
  var ctx=canvas.getContext('2d');
  var dpr=window.devicePixelRatio||1;
  var rect=canvas.parentElement.getBoundingClientRect();
  canvas.width=rect.width*dpr;
  canvas.height=300*dpr;
  canvas.style.width=rect.width+'px';
  canvas.style.height='300px';
  ctx.scale(dpr,dpr);
  var w=rect.width-60,h=240,ox=50,oy=20,maxVal=Math.max.apply(null,data)*1.1;
  ctx.clearRect(0,0,w+60,h+40);
  ctx.strokeStyle='rgba(148,163,184,.2)';ctx.lineWidth=1;
  for(var i=0;i<=4;i++){{var y=oy+h-h*i/4;ctx.beginPath();ctx.moveTo(ox,y);ctx.lineTo(ox+w,y);ctx.stroke();ctx.fillStyle='#64748b';ctx.font='11px sans-serif';ctx.fillText('$'+(maxVal*i/4/1000).toFixed(0)+'K',2,y+4);}}
  labels.forEach(function(l,i){{ctx.fillStyle='#64748b';ctx.font='11px sans-serif';ctx.fillText(l,ox+i*(w/(labels.length-1||1))-10,oy+h+20);}});
  ctx.beginPath();ctx.strokeStyle='#22d3ee';ctx.lineWidth=2;
  data.forEach(function(d,i){{var x=ox+i*(w/(data.length-1||1));var y=oy+h-(d/maxVal)*h;if(i===0)ctx.moveTo(x,y);else ctx.lineTo(x,y);}});
  ctx.stroke();
  ctx.fillStyle='rgba(6,182,212,.2)';
  data.forEach(function(d,i){{var x=ox+i*(w/(data.length-1||1));var y=oy+h-(d/maxVal)*h;ctx.beginPath();ctx.arc(x,y,4,0,Math.PI*2);ctx.fill();ctx.stroke();}});
}}
window.addEventListener('load',calculateSIP);
['monthlyAmount','annualRate','years'].forEach(function(id){{document.getElementById(id).addEventListener('input',calculateSIP);}});
</script>''',
        'SIP（Systematic Investment Plan，定期定额投资）是一种长期投资策略，通过每月固定投入、利用复利效应实现财富增长。本工具帮助您计算SIP投资的预期收益。',
        'SIP (Systematic Investment Plan) is a long-term investment strategy using fixed monthly contributions and compound interest. This tool helps you calculate expected SIP returns.'
    )

    # 3. chess-timer
    bodies['chess-timer'] = (
        '''<div class="tool-section">
  <h2>时间设置</h2>
  <div style="display:flex;gap:12px;flex-wrap:wrap;margin-bottom:12px">
    <div style="flex:1;min-width:150px"><label style="color:#94a3b8;font-size:.85rem">初始时间(分钟)</label><input type="number" id="initMinutes" value="5" min="1" step="1"></div>
    <div style="flex:1;min-width:150px"><label style="color:#94a3b8;font-size:.85rem">加秒(秒)</label><input type="number" id="increment" value="3" min="0" step="1"></div>
    <div style="flex:1;min-width:150px"><label style="color:#94a3b8;font-size:.85rem">预设</label><select id="preset" onchange="applyPreset()"><option value="">自定义</option><option value="1,0">子弹 1+0</option><option value="3,0">闪电 3+0</option><option value="3,2">快棋 3+2</option><option value="5,3">常用 5+3</option><option value="10,0">快速 10+0</option><option value="10,5">10+5</option><option value="15,10">标准 15+10</option><option value="30,0">慢棋 30+0</option></select></div>
  </div>
</div>
<div class="tool-section">
  <h2>计时器</h2>
  <div style="display:flex;gap:16px;flex-wrap:wrap">
    <div style="flex:1;text-align:center;padding:24px;background:#0f172a;border-radius:12px;border:3px solid rgba(6,182,212,.3);cursor:pointer" id="player1Box" onclick="switchTurn(0)">
      <div style="font-size:.9rem;color:#94a3b8;margin-bottom:8px">⚪ 玩家1 (白方)</div>
      <div style="font-size:3rem;font-weight:700;color:#22d3ee;font-family:monospace" id="timer1">5:00</div>
      <div style="color:#94a3b8;font-size:.8rem;margin-top:4px">点击计时</div>
    </div>
    <div style="flex:1;text-align:center;padding:24px;background:#0f172a;border-radius:12px;border:3px solid rgba(148,163,184,.1);cursor:pointer" id="player2Box" onclick="switchTurn(1)">
      <div style="font-size:.9rem;color:#94a3b8;margin-bottom:8px">⚫ 玩家2 (黑方)</div>
      <div style="font-size:3rem;font-weight:700;color:#94a3b8;font-family:monospace" id="timer2">5:00</div>
      <div style="color:#94a3b8;font-size:.8rem;margin-top:4px">等待中</div>
    </div>
  </div>
  <div class="result-actions" style="margin-top:12px">
    <button class="btn btn-primary" onclick="startTimer()">▶ 开始</button>
    <button class="btn btn-secondary" onclick="pauseTimer()">⏸ 暂停</button>
    <button class="btn btn-secondary" onclick="resetTimer()">🔄 重置</button>
  </div>
</div>
<script>
var timers=[300,300],incr=[3,3],active=-1,intervalId=null,paused=false;
function formatTime(s){{var m=Math.floor(s/60),sec=s%60;return m+':'+(sec<10?'0':'')+sec;}}
function updateDisplay(){{
  document.getElementById('timer1').textContent=formatTime(timers[0]);
  document.getElementById('timer2').textContent=formatTime(timers[1]);
  var b1=document.getElementById('player1Box'),b2=document.getElementById('player2Box');
  if(active===0){{b1.style.borderColor='rgba(6,182,212,.6)';b2.style.borderColor='rgba(148,163,184,.1)';b1.querySelector('div:last-child').textContent='计时中...';b2.querySelector('div:last-child').textContent='等待中';}}
  else if(active===1){{b2.style.borderColor='rgba(6,182,212,.6)';b1.style.borderColor='rgba(148,163,184,.1)';b2.querySelector('div:last-child').textContent='计时中...';b1.querySelector('div:last-child').textContent='等待中';}}
  else{{b1.style.borderColor='rgba(148,163,184,.1)';b2.style.borderColor='rgba(148,163,184,.1)';b1.querySelector('div:last-child').textContent='点击计时';b2.querySelector('div:last-child').textContent='等待中';}}
  if(timers[0]<=0){{document.getElementById('timer1').textContent='超时!';document.getElementById('timer1').style.color='#f87171';}}
  if(timers[2]<=0){{document.getElementById('timer2').textContent='超时!';document.getElementById('timer2').style.color='#f87171';}}
}}
function switchTurn(player){{
  if(paused||active===player)return;
  if(active>=0)timers[active]+=incr[active];
  active=player;updateDisplay();
  if(!intervalId)startInterval();
}}
function startInterval(){{
  clearInterval(intervalId);
  intervalId=setInterval(function(){{
    if(active<0||paused)return;
    timers[active]--;
    if(timers[active]<=0){{timers[active]=0;updateDisplay();clearInterval(intervalId);intervalId=null;}}
    updateDisplay();
  }},1000);
}}
function startTimer(){{if(active<0){{active=0;updateDisplay();startInterval();}}else{{paused=false;startInterval();}}}}
function pauseTimer(){{paused=true;if(intervalId){{clearInterval(intervalId);intervalId=null;}}}}
function resetTimer(){{
  clearInterval(intervalId);intervalId=null;active=-1;paused=false;
  timers[0]=parseInt(document.getElementById('initMinutes').value)*60;
  timers[1]=parseInt(document.getElementById('initMinutes').value)*60;
  incr=[parseInt(document.getElementById('increment').value),parseInt(document.getElementById('increment').value)];
  document.getElementById('timer1').style.color='#22d3ee';document.getElementById('timer2').style.color='#94a3b8';
  updateDisplay();
}}
function applyPreset(){{
  var val=document.getElementById('preset').value;
  if(!val)return;
  var parts=val.split(',');
  document.getElementById('initMinutes').value=parts[0];
  document.getElementById('increment').value=parts[1];
  resetTimer();
}}
updateDisplay();
</script>''',
        '''<div class="tool-section">
  <h2>Time Settings</h2>
  <div style="display:flex;gap:12px;flex-wrap:wrap;margin-bottom:12px">
    <div style="flex:1;min-width:150px"><label style="color:#94a3b8;font-size:.85rem">Initial Time (min)</label><input type="number" id="initMinutes" value="5" min="1" step="1"></div>
    <div style="flex:1;min-width:150px"><label style="color:#94a3b8;font-size:.85rem">Increment (sec)</label><input type="number" id="increment" value="3" min="0" step="1"></div>
    <div style="flex:1;min-width:150px"><label style="color:#94a3b8;font-size:.85rem">Preset</label><select id="preset" onchange="applyPreset()"><option value="">Custom</option><option value="1,0">Bullet 1+0</option><option value="3,0">Blitz 3+0</option><option value="3,2">Blitz 3+2</option><option value="5,3">Rapid 5+3</option><option value="10,0">Rapid 10+0</option><option value="10,5">10+5</option><option value="15,10">Standard 15+10</option><option value="30,0">Classical 30+0</option></select></div>
  </div>
</div>
<div class="tool-section">
  <h2>Clock</h2>
  <div style="display:flex;gap:16px;flex-wrap:wrap">
    <div style="flex:1;text-align:center;padding:24px;background:#0f172a;border-radius:12px;border:3px solid rgba(6,182,212,.3);cursor:pointer" id="player1Box" onclick="switchTurn(0)">
      <div style="font-size:.9rem;color:#94a3b8;margin-bottom:8px">⚪ Player 1 (White)</div>
      <div style="font-size:3rem;font-weight:700;color:#22d3ee;font-family:monospace" id="timer1">5:00</div>
      <div style="color:#94a3b8;font-size:.8rem;margin-top:4px">Click to time</div>
    </div>
    <div style="flex:1;text-align:center;padding:24px;background:#0f172a;border-radius:12px;border:3px solid rgba(148,163,184,.1);cursor:pointer" id="player2Box" onclick="switchTurn(1)">
      <div style="font-size:.9rem;color:#94a3b8;margin-bottom:8px">⚫ Player 2 (Black)</div>
      <div style="font-size:3rem;font-weight:700;color:#94a3b8;font-family:monospace" id="timer2">5:00</div>
      <div style="color:#94a3b8;font-size:.8rem;margin-top:4px">Waiting</div>
    </div>
  </div>
  <div class="result-actions" style="margin-top:12px">
    <button class="btn btn-primary" onclick="startTimer()">▶ Start</button>
    <button class="btn btn-secondary" onclick="pauseTimer()">⏸ Pause</button>
    <button class="btn btn-secondary" onclick="resetTimer()">🔄 Reset</button>
  </div>
</div>
<script>
var timers=[300,300],incr=[3,3],active=-1,intervalId=null,paused=false;
function formatTime(s){{var m=Math.floor(s/60),sec=s%60;return m+':'+(sec<10?'0':'')+sec;}}
function updateDisplay(){{
  document.getElementById('timer1').textContent=formatTime(timers[0]);
  document.getElementById('timer2').textContent=formatTime(timers[1]);
  var b1=document.getElementById('player1Box'),b2=document.getElementById('player2Box');
  if(active===0){{b1.style.borderColor='rgba(6,182,212,.6)';b2.style.borderColor='rgba(148,163,184,.1)';b1.querySelector('div:last-child').textContent='Running...';b2.querySelector('div:last-child').textContent='Waiting';}}
  else if(active===1){{b2.style.borderColor='rgba(6,182,212,.6)';b1.style.borderColor='rgba(148,163,184,.1)';b2.querySelector('div:last-child').textContent='Running...';b1.querySelector('div:last-child').textContent='Waiting';}}
  else{{b1.style.borderColor='rgba(148,163,184,.1)';b2.style.borderColor='rgba(148,163,184,.1)';b1.querySelector('div:last-child').textContent='Click to time';b2.querySelector('div:last-child').textContent='Waiting';}}
  if(timers[0]<=0){{document.getElementById('timer1').textContent='Time Out!';document.getElementById('timer1').style.color='#f87171';}}
  if(timers[1]<=0){{document.getElementById('timer2').textContent='Time Out!';document.getElementById('timer2').style.color='#f87171';}}
}}
function switchTurn(player){{
  if(paused||active===player)return;
  if(active>=0)timers[active]+=incr[active];
  active=player;updateDisplay();
  if(!intervalId)startInterval();
}}
function startInterval(){{
  clearInterval(intervalId);
  intervalId=setInterval(function(){{
    if(active<0||paused)return;
    timers[active]--;
    if(timers[active]<=0){{timers[active]=0;updateDisplay();clearInterval(intervalId);intervalId=null;}}
    updateDisplay();
  }},1000);
}}
function startTimer(){{if(active<0){{active=0;updateDisplay();startInterval();}}else{{paused=false;startInterval();}}}}
function pauseTimer(){{paused=true;if(intervalId){{clearInterval(intervalId);intervalId=null;}}}}
function resetTimer(){{
  clearInterval(intervalId);intervalId=null;active=-1;paused=false;
  timers[0]=parseInt(document.getElementById('initMinutes').value)*60;
  timers[1]=parseInt(document.getElementById('initMinutes').value)*60;
  incr=[parseInt(document.getElementById('increment').value),parseInt(document.getElementById('increment').value)];
  document.getElementById('timer1').style.color='#22d3ee';document.getElementById('timer2').style.color='#94a3b8';
  updateDisplay();
}}
function applyPreset(){{
  var val=document.getElementById('preset').value;
  if(!val)return;
  var parts=val.split(',');
  document.getElementById('initMinutes').value=parts[0];
  document.getElementById('increment').value=parts[1];
  resetTimer();
}}
updateDisplay();
</script>''',
        '国际象棋计时器模拟真实棋钟，双方轮流计时。支持自定义初始时间和加秒，多种预设模式。适用于国际象棋、围棋等需要计时的对弈活动。',
        'Chess timer simulating a real chess clock with alternating timing. Customizable initial time and increment, multiple presets. Perfect for chess, Go, and other timed games.'
    )

    # 4. pixel-to-em
    bodies['pixel-to-em'] = (
        '''<div class="tool-section">
  <h2>转换参数</h2>
  <div style="display:flex;gap:12px;flex-wrap:wrap;margin-bottom:12px">
    <div style="flex:1;min-width:180px"><label style="color:#94a3b8;font-size:.85rem">像素值 (PX)</label><input type="number" id="pxValue" value="16" step="0.1"></div>
    <div style="flex:1;min-width:180px"><label style="color:#94a3b8;font-size:.85rem">基准字号 (PX)</label><input type="number" id="baseSize" value="16" step="1"></div>
  </div>
</div>
<div class="tool-section">
  <h2>转换结果</h2>
  <div class="result-output" id="resultOutput" style="font-size:1.5rem;text-align:center">1em</div>
  <div style="color:#94a3b8;font-size:.85rem;text-align:center;margin-bottom:8px">公式: PX ÷ 基准字号 = EM</div>
</div>
<div class="tool-section">
  <h2>常用对照表 (基准16px)</h2>
  <div style="display:flex;flex-wrap:wrap;gap:4px" id="refTable"></div>
</div>
<script>
function convertPxToEm(){{
  var px=parseFloat(document.getElementById('pxValue').value)||16;
  var base=parseFloat(document.getElementById('baseSize').value)||16;
  if(base<=0)base=16;
  var em=px/base;
  document.getElementById('resultOutput').textContent=em.toFixed(4)+'em';
}}
function buildRefTable(){{
  var base=parseFloat(document.getElementById('baseSize').value)||16;
  var html='';
  [1,2,4,6,8,10,12,14,16,18,20,24,28,32,36,40,48,56,64,72,80,96].forEach(function(px){{
    html+='<span style="display:inline-block;padding:4px 8px;background:#0f172a;border-radius:4px;margin:2px;font-size:.8rem;color:#94a3b8">'+px+'px = <span style="color:#22d3ee">'+(px/base).toFixed(4)+'em</span></span>';
  }});
  document.getElementById('refTable').innerHTML=html;
}}
document.getElementById('pxValue').addEventListener('input',function(){{convertPxToEm();}});
document.getElementById('baseSize').addEventListener('input',function(){{convertPxToEm();buildRefTable();}});
convertPxToEm();buildRefTable();
</script>''',
        '''<div class="tool-section">
  <h2>Conversion Parameters</h2>
  <div style="display:flex;gap:12px;flex-wrap:wrap;margin-bottom:12px">
    <div style="flex:1;min-width:180px"><label style="color:#94a3b8;font-size:.85rem">Pixel Value (PX)</label><input type="number" id="pxValue" value="16" step="0.1"></div>
    <div style="flex:1;min-width:180px"><label style="color:#94a3b8;font-size:.85rem">Base Font Size (PX)</label><input type="number" id="baseSize" value="16" step="1"></div>
  </div>
</div>
<div class="tool-section">
  <h2>Result</h2>
  <div class="result-output" id="resultOutput" style="font-size:1.5rem;text-align:center">1em</div>
  <div style="color:#94a3b8;font-size:.85rem;text-align:center;margin-bottom:8px">Formula: PX ÷ Base Size = EM</div>
</div>
<div class="tool-section">
  <h2>Common Reference (Base 16px)</h2>
  <div style="display:flex;flex-wrap:wrap;gap:4px" id="refTable"></div>
</div>
<script>
function convertPxToEm(){{
  var px=parseFloat(document.getElementById('pxValue').value)||16;
  var base=parseFloat(document.getElementById('baseSize').value)||16;
  if(base<=0)base=16;
  var em=px/base;
  document.getElementById('resultOutput').textContent=em.toFixed(4)+'em';
}}
function buildRefTable(){{
  var base=parseFloat(document.getElementById('baseSize').value)||16;
  var html='';
  [1,2,4,6,8,10,12,14,16,18,20,24,28,32,36,40,48,56,64,72,80,96].forEach(function(px){{
    html+='<span style="display:inline-block;padding:4px 8px;background:#0f172a;border-radius:4px;margin:2px;font-size:.8rem;color:#94a3b8">'+px+'px = <span style="color:#22d3ee">'+(px/base).toFixed(4)+'em</span></span>';
  }});
  document.getElementById('refTable').innerHTML=html;
}}
document.getElementById('pxValue').addEventListener('input',function(){{convertPxToEm();}});
document.getElementById('baseSize').addEventListener('input',function(){{convertPxToEm();buildRefTable();}});
convertPxToEm();buildRefTable();
</script>''',
        'PX到EM转换是前端开发中的常见需求。EM是相对单位，相对于父元素的字号。本工具帮助开发者快速将像素值转换为EM，支持自定义基准字号。',
        'PX to EM conversion is a common need in frontend development. EM is a relative unit based on parent font size. This tool helps developers quickly convert pixel values to EM with customizable base size.'
    )

    # 5. em-to-px
    bodies['em-to-px'] = (
        '''<div class="tool-section">
  <h2>转换参数</h2>
  <div style="display:flex;gap:12px;flex-wrap:wrap;margin-bottom:12px">
    <div style="flex:1;min-width:180px"><label style="color:#94a3b8;font-size:.85rem">EM值</label><input type="number" id="emValue" value="1" step="0.01"></div>
    <div style="flex:1;min-width:180px"><label style="color:#94a3b8;font-size:.85rem">基准字号 (PX)</label><input type="number" id="baseSize" value="16" step="1"></div>
  </div>
</div>
<div class="tool-section">
  <h2>转换结果</h2>
  <div class="result-output" id="resultOutput" style="font-size:1.5rem;text-align:center">16px</div>
  <div style="color:#94a3b8;font-size:.85rem;text-align:center;margin-bottom:8px">公式: EM × 基准字号 = PX</div>
</div>
<div class="tool-section">
  <h2>常用对照表 (基准16px)</h2>
  <div style="display:flex;flex-wrap:wrap;gap:4px" id="refTable"></div>
</div>
<script>
function convertEmToPx(){{
  var em=parseFloat(document.getElementById('emValue').value)||1;
  var base=parseFloat(document.getElementById('baseSize').value)||16;
  var px=em*base;
  document.getElementById('resultOutput').textContent=px.toFixed(1)+'px';
}}
function buildRefTable(){{
  var base=parseFloat(document.getElementById('baseSize').value)||16;
  var html='';
  [0.125,0.25,0.375,0.5,0.625,0.75,0.875,1,1.125,1.25,1.5,1.75,2,2.5,3,4,5,6].forEach(function(em){{
    html+='<span style="display:inline-block;padding:4px 8px;background:#0f172a;border-radius:4px;margin:2px;font-size:.8rem;color:#94a3b8">'+em+'em = <span style="color:#22d3ee">'+(em*base).toFixed(0)+'px</span></span>';
  }});
  document.getElementById('refTable').innerHTML=html;
}}
document.getElementById('emValue').addEventListener('input',function(){{convertEmToPx();}});
document.getElementById('baseSize').addEventListener('input',function(){{convertEmToPx();buildRefTable();}});
convertEmToPx();buildRefTable();
</script>''',
        '''<div class="tool-section">
  <h2>Conversion Parameters</h2>
  <div style="display:flex;gap:12px;flex-wrap:wrap;margin-bottom:12px">
    <div style="flex:1;min-width:180px"><label style="color:#94a3b8;font-size:.85rem">EM Value</label><input type="number" id="emValue" value="1" step="0.01"></div>
    <div style="flex:1;min-width:180px"><label style="color:#94a3b8;font-size:.85rem">Base Font Size (PX)</label><input type="number" id="baseSize" value="16" step="1"></div>
  </div>
</div>
<div class="tool-section">
  <h2>Result</h2>
  <div class="result-output" id="resultOutput" style="font-size:1.5rem;text-align:center">16px</div>
  <div style="color:#94a3b8;font-size:.85rem;text-align:center;margin-bottom:8px">Formula: EM × Base Size = PX</div>
</div>
<div class="tool-section">
  <h2>Common Reference (Base 16px)</h2>
  <div style="display:flex;flex-wrap:wrap;gap:4px" id="refTable"></div>
</div>
<script>
function convertEmToPx(){{
  var em=parseFloat(document.getElementById('emValue').value)||1;
  var base=parseFloat(document.getElementById('baseSize').value)||16;
  var px=em*base;
  document.getElementById('resultOutput').textContent=px.toFixed(1)+'px';
}}
function buildRefTable(){{
  var base=parseFloat(document.getElementById('baseSize').value)||16;
  var html='';
  [0.125,0.25,0.375,0.5,0.625,0.75,0.875,1,1.125,1.25,1.5,1.75,2,2.5,3,4,5,6].forEach(function(em){{
    html+='<span style="display:inline-block;padding:4px 8px;background:#0f172a;border-radius:4px;margin:2px;font-size:.8rem;color:#94a3b8">'+em+'em = <span style="color:#22d3ee">'+(em*base).toFixed(0)+'px</span></span>';
  }});
  document.getElementById('refTable').innerHTML=html;
}}
document.getElementById('emValue').addEventListener('input',function(){{convertEmToPx();}});
document.getElementById('baseSize').addEventListener('input',function(){{convertEmToPx();buildRefTable();}});
convertEmToPx();buildRefTable();
</script>''',
        'EM到PX转换将相对单位转换为绝对像素值。在CSS中，1em等于当前元素的字号大小。本工具帮助前端开发者快速将EM值转换为对应的像素值。',
        'EM to PX conversion turns relative units into absolute pixel values. In CSS, 1em equals the current font size. This tool helps frontend developers quickly convert EM values to pixels.'
    )

    # 6. lottery-generator
    bodies['lottery-generator'] = (
        '''<div class="tool-section">
  <h2>选择玩法</h2>
  <select id="lotteryType" onchange="generateNumbers()" style="margin-bottom:12px">
    <option value="ssq">双色球 (6红+1蓝)</option>
    <option value="dlt">大乐透 (5前+2后)</option>
    <option value="pb">Powerball (5白+1红)</option>
    <option value="mm">Mega Millions (5白+1金)</option>
    <option value="eu">EuroMillions (5主+2星)</option>
    <option value="6d">6位数字</option>
  </select>
  <button class="btn btn-primary" onclick="generateNumbers()">🎰 随机生成</button>
</div>
<div class="tool-section">
  <h2>生成的号码</h2>
  <div class="result-output" id="resultOutput" style="font-size:1.8rem;text-align:center;letter-spacing:8px">点击生成</div>
  <div class="result-actions">
    <button class="btn btn-primary" onclick="copyResult()">📋 复制号码</button>
    <button class="btn btn-secondary" onclick="generateNumbers()">🔄 再生成一组</button>
  </div>
</div>
<script>
function rand(min,max){{return Math.floor(Math.random()*(max-min+1))+min;}}
function pickUnique(count,min,max){{
  var arr=[];
  while(arr.length<count){{var n=rand(min,max);if(arr.indexOf(n)===-1)arr.push(n);}}
  return arr.sort(function(a,b){{return a-b;}});
}}
function generateNumbers(){{
  var type=document.getElementById('lotteryType').value;
  var result='';
  if(type==='ssq'){{var red=pickUnique(6,1,33);var blue=rand(1,16);result='🔴 '+red.join(' ')+'  🔵 '+blue;}}
  else if(type==='dlt'){{var front=pickUnique(5,1,35);var back=pickUnique(2,1,12);result='⚪ '+front.join(' ')+'  🟡 '+back.join(' ');}}
  else if(type==='pb'){{var white=pickUnique(5,1,69);var red=rand(1,26);result='⚪ '+white.join(' ')+'  🔴 '+red;}}
  else if(type==='mm'){{var w=pickUnique(5,1,70);var g=rand(1,25);result='⚪ '+w.join(' ')+'  🟡 '+g;}}
  else if(type==='eu'){{var m=pickUnique(5,1,50);var s=pickUnique(2,1,12);result='⚪ '+m.join(' ')+'  ⭐ '+s.join(' ');}}
  else if(type==='6d'){{result=rand(0,9)+''+rand(0,9)+''+rand(0,9)+''+rand(0,9)+''+rand(0,9)+''+rand(0,9);}}
  document.getElementById('resultOutput').textContent=result;
}}
function copyResult(){{
  var text=document.getElementById('resultOutput').textContent;
  if(text==='点击生成')return;
  navigator.clipboard.writeText(text).then(function(){{showToast('已复制!');}});
}}
function showToast(msg){{var t=document.getElementById('toast');t.textContent=msg;t.classList.add('show');setTimeout(function(){{t.classList.remove('show');}},2000);}}
generateNumbers();
</script>''',
        '''<div class="tool-section">
  <h2>Select Game</h2>
  <select id="lotteryType" onchange="generateNumbers()" style="margin-bottom:12px">
    <option value="pb">Powerball (5 white + 1 red)</option>
    <option value="mm">Mega Millions (5 white + 1 gold)</option>
    <option value="eu">EuroMillions (5 main + 2 stars)</option>
    <option value="ssq">Double Color Ball (6 red + 1 blue)</option>
    <option value="dlt">Super Lotto (5 front + 2 back)</option>
    <option value="6d">6-Digit</option>
  </select>
  <button class="btn btn-primary" onclick="generateNumbers()">🎰 Generate</button>
</div>
<div class="tool-section">
  <h2>Your Numbers</h2>
  <div class="result-output" id="resultOutput" style="font-size:1.8rem;text-align:center;letter-spacing:8px">Click to generate</div>
  <div class="result-actions">
    <button class="btn btn-primary" onclick="copyResult()">📋 Copy</button>
    <button class="btn btn-secondary" onclick="generateNumbers()">🔄 Generate Again</button>
  </div>
</div>
<script>
function rand(min,max){{return Math.floor(Math.random()*(max-min+1))+min;}}
function pickUnique(count,min,max){{
  var arr=[];
  while(arr.length<count){{var n=rand(min,max);if(arr.indexOf(n)===-1)arr.push(n);}}
  return arr.sort(function(a,b){{return a-b;}});
}}
function generateNumbers(){{
  var type=document.getElementById('lotteryType').value;
  var result='';
  if(type==='pb'){{var white=pickUnique(5,1,69);var red=rand(1,26);result='⚪ '+white.join(' ')+'  🔴 '+red;}}
  else if(type==='mm'){{var w=pickUnique(5,1,70);var g=rand(1,25);result='⚪ '+w.join(' ')+'  🟡 '+g;}}
  else if(type==='eu'){{var m=pickUnique(5,1,50);var s=pickUnique(2,1,12);result='⚪ '+m.join(' ')+'  ⭐ '+s.join(' ');}}
  else if(type==='ssq'){{var red=pickUnique(6,1,33);var blue=rand(1,16);result='🔴 '+red.join(' ')+'  🔵 '+blue;}}
  else if(type==='dlt'){{var front=pickUnique(5,1,35);var back=pickUnique(2,1,12);result='⚪ '+front.join(' ')+'  🟡 '+back.join(' ');}}
  else if(type==='6d'){{result=rand(0,9)+''+rand(0,9)+''+rand(0,9)+''+rand(0,9)+''+rand(0,9)+''+rand(0,9);}}
  document.getElementById('resultOutput').textContent=result;
}}
function copyResult(){{
  var text=document.getElementById('resultOutput').textContent;
  if(text==='Click to generate')return;
  navigator.clipboard.writeText(text).then(function(){{showToast('Copied!');}});
}}
function showToast(msg){{var t=document.getElementById('toast');t.textContent=msg;t.classList.add('show');setTimeout(function(){{t.classList.remove('show');}},2000);}}
generateNumbers();
</script>''',
        '彩票号码生成器使用真随机算法生成彩票号码。本工具仅供娱乐，不保证中奖。支持双色球、大乐透、Powerball、Mega Millions、EuroMillions等多种玩法。',
        'Lottery number generator uses pure random algorithm to generate numbers. For entertainment only, no winning guarantee. Supports Powerball, Mega Millions, EuroMillions, and more.'
    )

    # 7. yes-no
    bodies['yes-no'] = (
        '''<div class="tool-section" style="text-align:center">
  <h2>心里默念你的问题...</h2>
  <div class="result-output" id="resultOutput" style="font-size:4rem;text-align:center;min-height:120px;display:flex;align-items:center;justify-content:center;color:#22d3ee">❓</div>
  <button class="btn btn-primary" onclick="decide()" style="font-size:1.2rem;padding:16px 40px">🎯 帮我决定!</button>
  <div class="result-actions" style="margin-top:12px;justify-content:center">
    <button class="btn btn-secondary" onclick="copyResult()">📋 复制答案</button>
  </div>
  <div style="margin-top:12px;color:#64748b;font-size:.8rem">已做决定 <span id="decideCount">0</span> 次</div>
</div>
<script>
var count=0;
var answers=['✅ 是!','❌ 否!','🤔 也许吧','👍 当然可以','👎 不建议','⭐ 肯定行','💤 再等等','🔥 就现在!','🌈 顺其自然','🎯 放手去做','🌙 明天再问','🦋 换个角度想'];
function decide(){{
  var answer=answers[Math.floor(Math.random()*answers.length)];
  var el=document.getElementById('resultOutput');
  el.textContent=answer;
  el.style.transform='scale(1.3)';
  setTimeout(function(){{el.style.transform='scale(1)';}},200);
  count++;
  document.getElementById('decideCount').textContent=count;
}}
function copyResult(){{
  var text=document.getElementById('resultOutput').textContent;
  if(text==='❓')return;
  navigator.clipboard.writeText(text).then(function(){{showToast('已复制!');}});
}}
function showToast(msg){{var t=document.getElementById('toast');t.textContent=msg;t.classList.add('show');setTimeout(function(){{t.classList.remove('show');}},2000);}}
</script>''',
        '''<div class="tool-section" style="text-align:center">
  <h2>Ask your question in your mind...</h2>
  <div class="result-output" id="resultOutput" style="font-size:4rem;text-align:center;min-height:120px;display:flex;align-items:center;justify-content:center;color:#22d3ee">❓</div>
  <button class="btn btn-primary" onclick="decide()" style="font-size:1.2rem;padding:16px 40px">🎯 Decide for Me!</button>
  <div class="result-actions" style="margin-top:12px;justify-content:center">
    <button class="btn btn-secondary" onclick="copyResult()">📋 Copy Answer</button>
  </div>
  <div style="margin-top:12px;color:#64748b;font-size:.8rem">Decisions made: <span id="decideCount">0</span></div>
</div>
<script>
var count=0;
var answers=['✅ Yes!','❌ No!','🤔 Maybe','👍 Definitely','👎 Not recommended','⭐ Absolutely','💤 Wait a bit','🔥 Now is the time!','🌈 Go with the flow','🎯 Just do it','🌙 Ask again tomorrow','🦋 Think differently'];
function decide(){{
  var answer=answers[Math.floor(Math.random()*answers.length)];
  var el=document.getElementById('resultOutput');
  el.textContent=answer;
  el.style.transform='scale(1.3)';
  setTimeout(function(){{el.style.transform='scale(1)';}},200);
  count++;
  document.getElementById('decideCount').textContent=count;
}}
function copyResult(){{
  var text=document.getElementById('resultOutput').textContent;
  if(text==='❓')return;
  navigator.clipboard.writeText(text).then(function(){{showToast('Copied!');}});
}}
function showToast(msg){{var t=document.getElementById('toast');t.textContent=msg;t.classList.add('show');setTimeout(function(){{t.classList.remove('show');}},2000);}}
</script>''',
        '是/否决策器帮助你快速做出小决定。当面对日常小选择犹豫不决时，点击按钮获得随机答案。纯娱乐工具，重要决策请理性判断。',
        'Yes/No Decision Maker helps you make quick small decisions. Click to get a random answer when you can\'t decide on everyday choices. For entertainment only.'
    )

    # 8. flip-text
    bodies['flip-text'] = (
        '''<div class="tool-section">
  <h2>输入文字</h2>
  <textarea id="inputText" placeholder="输入要翻转的文字..." style="min-height:100px"></textarea>
</div>
<div class="tool-section">
  <h2>翻转模式</h2>
  <div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:12px">
    <button class="btn btn-primary" onclick="flipText('upside')" id="btnUpside">🙃 上下颠倒</button>
    <button class="btn btn-secondary" onclick="flipText('mirror')" id="btnMirror">🪞 镜像翻转</button>
    <button class="btn btn-secondary" onclick="flipText('reverse')" id="btnReverse">↔️ 反向翻转</button>
  </div>
</div>
<div class="tool-section">
  <h2>翻转结果</h2>
  <div class="result-output" id="resultOutput" style="font-size:1.3rem">等待输入...</div>
  <div class="result-actions">
    <button class="btn btn-primary" onclick="copyResult()">📋 复制结果</button>
    <button class="btn btn-secondary" onclick="clearAll()">🗑️ 清空</button>
  </div>
</div>
<script>
var flipMap={{'{':'}','}':'{','[':']',']':'[','(':')',')':'(','<':'>','>':'<','.':'˙',',':'ʻ','!':'¡','?':'¿','&':'⅋','_':'‾','\"':'„',\"'\":',',a:'ɐ',b:'q',c:'ɔ',d:'p',e:'ǝ',f:'ɟ',g:'ƃ',h:'ɥ',i:'ᴉ',j:'ɾ',k:'ʞ',l:'l',m:'ɯ',n:'u',o:'o',p:'d',q:'b',r:'ɹ',s:'s',t:'ʇ',u:'n',v:'ʌ',w:'ʍ',x:'x',y:'ʎ',z:'z',A:'∀',B:'𐐒',C:'Ɔ',D:'ᗡ',E:'Ǝ',F:'Ⅎ',G:'⅁',H:'H',I:'I',J:'ſ',K:'⋊',L:'⅂',M:'W',N:'N',O:'O',P:'Ԁ',Q:'Ό',R:'ᴚ',S:'S',T:'⊥',U:'∩',V:'Λ',W:'M',X:'X',Y:'⅄',Z:'Z','0':'0','1':'⇂','2':'↋','3':'3','4':'4','5':'5','6':'9','7':'7','8':'8','9':'6'}};
function flipText(mode){{
  var input=document.getElementById('inputText').value;
  if(!input){{document.getElementById('resultOutput').textContent='请先输入文字';return;}}
  var result='';
  if(mode==='upside')result=input.split('').reverse().map(function(c){{return flipMap[c]||c;}}).join('');
  else if(mode==='mirror')result=input.split('').map(function(c){{return flipMap[c]||c;}}).reverse().join('');
  else if(mode==='reverse')result=input.split('').reverse().join('');
  document.getElementById('resultOutput').textContent=result;
  document.querySelectorAll('[id^=btn]').forEach(function(b){{b.className='btn btn-secondary';}});
  document.getElementById('btn'+mode.charAt(0).toUpperCase()+mode.slice(1)).className='btn btn-primary';
}}
function copyResult(){{
  var text=document.getElementById('resultOutput').textContent;
  if(!text||text==='等待输入...')return;
  navigator.clipboard.writeText(text).then(function(){{showToast('已复制!');}});
}}
function clearAll(){{document.getElementById('inputText').value='';document.getElementById('resultOutput').textContent='等待输入...';}}
function showToast(msg){{var t=document.getElementById('toast');t.textContent=msg;t.classList.add('show');setTimeout(function(){{t.classList.remove('show');}},2000);}}
document.getElementById('inputText').addEventListener('input',function(){{if(document.querySelector('.btn-primary[id^=btn]'))flipText(document.querySelector('.btn-primary[id^=btn]').id.replace('btn','').toLowerCase());}});
</script>''',
        '''<div class="tool-section">
  <h2>Enter Text</h2>
  <textarea id="inputText" placeholder="Enter text to flip..." style="min-height:100px"></textarea>
</div>
<div class="tool-section">
  <h2>Flip Mode</h2>
  <div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:12px">
    <button class="btn btn-primary" onclick="flipText('upside')" id="btnUpside">🙃 Upside Down</button>
    <button class="btn btn-secondary" onclick="flipText('mirror')" id="btnMirror">🪞 Mirror</button>
    <button class="btn btn-secondary" onclick="flipText('reverse')" id="btnReverse">↔️ Reverse</button>
  </div>
</div>
<div class="tool-section">
  <h2>Result</h2>
  <div class="result-output" id="resultOutput" style="font-size:1.3rem">Waiting for input...</div>
  <div class="result-actions">
    <button class="btn btn-primary" onclick="copyResult()">📋 Copy</button>
    <button class="btn btn-secondary" onclick="clearAll()">🗑️ Clear</button>
  </div>
</div>
<script>
var flipMap={{'{':'}','}':'{','[':']',']':'[','(':')',')':'(','<':'>','>':'<','.':'˙',',':'ʻ','!':'¡','?':'¿','&':'⅋','_':'‾','\"':'„',\"'\":',',a:'ɐ',b:'q',c:'ɔ',d:'p',e:'ǝ',f:'ɟ',g:'ƃ',h:'ɥ',i:'ᴉ',j:'ɾ',k:'ʞ',l:'l',m:'ɯ',n:'u',o:'o',p:'d',q:'b',r:'ɹ',s:'s',t:'ʇ',u:'n',v:'ʌ',w:'ʍ',x:'x',y:'ʎ',z:'z',A:'∀',B:'𐐒',C:'Ɔ',D:'ᗡ',E:'Ǝ',F:'Ⅎ',G:'⅁',H:'H',I:'I',J:'ſ',K:'⋊',L:'⅂',M:'W',N:'N',O:'O',P:'Ԁ',Q:'Ό',R:'ᴚ',S:'S',T:'⊥',U:'∩',V:'Λ',W:'M',X:'X',Y:'⅄',Z:'Z','0':'0','1':'⇂','2':'↋','3':'3','4':'4','5':'5','6':'9','7':'7','8':'8','9':'6'}};
function flipText(mode){{
  var input=document.getElementById('inputText').value;
  if(!input){{document.getElementById('resultOutput').textContent='Please enter text first';return;}}
  var result='';
  if(mode==='upside')result=input.split('').reverse().map(function(c){{return flipMap[c]||c;}}).join('');
  else if(mode==='mirror')result=input.split('').map(function(c){{return flipMap[c]||c;}}).reverse().join('');
  else if(mode==='reverse')result=input.split('').reverse().join('');
  document.getElementById('resultOutput').textContent=result;
  document.querySelectorAll('[id^=btn]').forEach(function(b){{b.className='btn btn-secondary';}});
  document.getElementById('btn'+mode.charAt(0).toUpperCase()+mode.slice(1)).className='btn btn-primary';
}}
function copyResult(){{
  var text=document.getElementById('resultOutput').textContent;
  if(!text||text==='Waiting for input...')return;
  navigator.clipboard.writeText(text).then(function(){{showToast('Copied!');}});
}}
function clearAll(){{document.getElementById('inputText').value='';document.getElementById('resultOutput').textContent='Waiting for input...';}}
function showToast(msg){{var t=document.getElementById('toast');t.textContent=msg;t.classList.add('show');setTimeout(function(){{t.classList.remove('show');}},2000);}}
document.getElementById('inputText').addEventListener('input',function(){{if(document.querySelector('.btn-primary[id^=btn]'))flipText(document.querySelector('.btn-primary[id^=btn]').id.replace('btn','').toLowerCase());}});
</script>''',
        '文字翻转器支持三种翻转模式：上下颠倒（每个字符映射为颠倒版本）、镜像翻转（颠倒后整体反转）、反向翻转（纯字符串反转）。适用于创意设计、社交媒体趣味玩法。',
        'Flip Text Generator supports three modes: upside down (each char mapped to inverted version), mirror (upside down + reverse), and reverse (pure string reversal). Great for creative design and social media.'
    )

    # 9. bubble-text
    bodies['bubble-text'] = (
        '''<div class="tool-section">
  <h2>输入文字</h2>
  <textarea id="inputText" placeholder="输入要转换的文字..." style="min-height:100px"></textarea>
</div>
<div class="tool-section">
  <h2>泡泡文字结果</h2>
  <div class="result-output" id="resultOutput" style="font-size:1.5rem;letter-spacing:2px">等待输入...</div>
  <div class="result-actions">
    <button class="btn btn-primary" onclick="convertBubble()">🫧 转换</button>
    <button class="btn btn-secondary" onclick="copyResult()">📋 复制结果</button>
    <button class="btn btn-secondary" onclick="clearAll()">🗑️ 清空</button>
  </div>
</div>
<div class="tool-section">
  <h2>示例</h2>
  <p style="font-size:1.3rem">Hello → Ⓗⓔⓛⓛⓞ</p>
  <p style="font-size:1.3rem">123 → ①②③</p>
</div>
<script>
var bubbleMap={{A:'Ⓐ',B:'Ⓑ',C:'Ⓒ',D:'Ⓓ',E:'Ⓔ',F:'Ⓕ',G:'Ⓖ',H:'Ⓗ',I:'Ⓘ',J:'Ⓙ',K:'Ⓚ',L:'Ⓛ',M:'Ⓜ',N:'Ⓝ',O:'Ⓞ',P:'Ⓟ',Q:'Ⓠ',R:'Ⓡ',S:'Ⓢ',T:'Ⓣ',U:'Ⓤ',V:'Ⓥ',W:'Ⓦ',X:'Ⓧ',Y:'Ⓨ',Z:'Ⓩ',a:'ⓐ',b:'ⓑ',c:'ⓒ',d:'ⓓ',e:'ⓔ',f:'ⓕ',g:'ⓖ',h:'ⓗ',i:'ⓘ',j:'ⓙ',k:'ⓚ',l:'ⓛ',m:'ⓜ',n:'ⓝ',o:'ⓞ',p:'ⓟ',q:'ⓠ',r:'ⓡ',s:'ⓢ',t:'ⓣ',u:'ⓤ',v:'ⓥ',w:'ⓦ',x:'ⓧ',y:'ⓨ',z:'ⓩ','0':'⓪','1':'①','2':'②','3':'③','4':'④','5':'⑤','6':'⑥','7':'⑦','8':'⑧','9':'⑨'}};
function convertBubble(){{
  var input=document.getElementById('inputText').value;
  if(!input){{document.getElementById('resultOutput').textContent='请先输入文字';return;}}
  var result=input.split('').map(function(c){{return bubbleMap[c]||c;}}).join('');
  document.getElementById('resultOutput').textContent=result;
}}
function copyResult(){{
  var text=document.getElementById('resultOutput').textContent;
  if(!text||text==='等待输入...')return;
  navigator.clipboard.writeText(text).then(function(){{showToast('已复制!');}});
}}
function clearAll(){{document.getElementById('inputText').value='';document.getElementById('resultOutput').textContent='等待输入...';}}
function showToast(msg){{var t=document.getElementById('toast');t.textContent=msg;t.classList.add('show');setTimeout(function(){{t.classList.remove('show');}},2000);}}
document.getElementById('inputText').addEventListener('input',convertBubble);
</script>''',
        '''<div class="tool-section">
  <h2>Enter Text</h2>
  <textarea id="inputText" placeholder="Enter text to convert..." style="min-height:100px"></textarea>
</div>
<div class="tool-section">
  <h2>Bubble Text Result</h2>
  <div class="result-output" id="resultOutput" style="font-size:1.5rem;letter-spacing:2px">Waiting for input...</div>
  <div class="result-actions">
    <button class="btn btn-primary" onclick="convertBubble()">🫧 Convert</button>
    <button class="btn btn-secondary" onclick="copyResult()">📋 Copy</button>
    <button class="btn btn-secondary" onclick="clearAll()">🗑️ Clear</button>
  </div>
</div>
<div class="tool-section">
  <h2>Example</h2>
  <p style="font-size:1.3rem">Hello → Ⓗⓔⓛⓛⓞ</p>
  <p style="font-size:1.3rem">123 → ①②③</p>
</div>
<script>
var bubbleMap={{A:'Ⓐ',B:'Ⓑ',C:'Ⓒ',D:'Ⓓ',E:'Ⓔ',F:'Ⓕ',G:'Ⓖ',H:'Ⓗ',I:'Ⓘ',J:'Ⓙ',K:'Ⓚ',L:'Ⓛ',M:'Ⓜ',N:'Ⓝ',O:'Ⓞ',P:'Ⓟ',Q:'Ⓠ',R:'Ⓡ',S:'Ⓢ',T:'Ⓣ',U:'Ⓤ',V:'Ⓥ',W:'Ⓦ',X:'Ⓧ',Y:'Ⓨ',Z:'Ⓩ',a:'ⓐ',b:'ⓑ',c:'ⓒ',d:'ⓓ',e:'ⓔ',f:'ⓕ',g:'ⓖ',h:'ⓗ',i:'ⓘ',j:'ⓙ',k:'ⓚ',l:'ⓛ',m:'ⓜ',n:'ⓝ',o:'ⓞ',p:'ⓟ',q:'ⓠ',r:'ⓡ',s:'ⓢ',t:'ⓣ',u:'ⓤ',v:'ⓥ',w:'ⓦ',x:'ⓧ',y:'ⓨ',z:'ⓩ','0':'⓪','1':'①','2':'②','3':'③','4':'④','5':'⑤','6':'⑥','7':'⑦','8':'⑧','9':'⑨'}};
function convertBubble(){{
  var input=document.getElementById('inputText').value;
  if(!input){{document.getElementById('resultOutput').textContent='Please enter text first';return;}}
  var result=input.split('').map(function(c){{return bubbleMap[c]||c;}}).join('');
  document.getElementById('resultOutput').textContent=result;
}}
function copyResult(){{
  var text=document.getElementById('resultOutput').textContent;
  if(!text||text==='Waiting for input...')return;
  navigator.clipboard.writeText(text).then(function(){{showToast('Copied!');}});
}}
function clearAll(){{document.getElementById('inputText').value='';document.getElementById('resultOutput').textContent='Waiting for input...';}}
function showToast(msg){{var t=document.getElementById('toast');t.textContent=msg;t.classList.add('show');setTimeout(function(){{t.classList.remove('show');}},2000);}}
document.getElementById('inputText').addEventListener('input',convertBubble);
</script>''',
        '泡泡文字生成器将普通文字转换为圆圈包围的装饰文字（Enclosed Alphanumerics）。每个字母和数字被Unicode圆圈字符替换，适合社交媒体昵称、创意设计和趣味玩法。',
        'Bubble Text Generator converts plain text to circle-enclosed decorative text (Enclosed Alphanumerics). Each letter and number is replaced with a Unicode circled character. Perfect for social media nicknames.'
    )

    # 10. bold-text-generator
    bodies['bold-text-generator'] = (
        '''<div class="tool-section">
  <h2>输入文字</h2>
  <textarea id="inputText" placeholder="输入要转换的文字..." style="min-height:80px"></textarea>
</div>
<div class="tool-section">
  <h2>选择风格</h2>
  <div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:12px">
    <button class="btn btn-primary" onclick="convertStyle('bold')" id="btnBold">𝐁 粗体</button>
    <button class="btn btn-secondary" onclick="convertStyle('italic')" id="btnItalic">𝐼 斜体</button>
    <button class="btn btn-secondary" onclick="convertStyle('boldItalic')" id="btnBoldItalic">𝑩 粗斜体</button>
    <button class="btn btn-secondary" onclick="convertStyle('script')" id="btnScript">𝒮 花体</button>
    <button class="btn btn-secondary" onclick="convertStyle('double')" id="btnDouble">𝔻 双线体</button>
    <button class="btn btn-secondary" onclick="convertStyle('mono')" id="btnMono">𝙼 等宽体</button>
    <button class="btn btn-secondary" onclick="convertStyle('sans')" id="btnSans">𝗔 无衬线粗</button>
    <button class="btn btn-secondary" onclick="convertStyle('sansItalic')" id="btnSansItalic">𝘈 无衬线斜</button>
    <button class="btn btn-secondary" onclick="convertStyle('sansBoldItalic')" id="btnSansBoldItalic">𝘼 无衬线粗斜</button>
  </div>
</div>
<div class="tool-section">
  <h2>转换结果</h2>
  <div class="result-output" id="resultOutput" style="font-size:1.5rem">等待输入...</div>
  <div class="result-actions">
    <button class="btn btn-primary" onclick="copyResult()">📋 复制结果</button>
    <button class="btn btn-secondary" onclick="clearAll()">🗑️ 清空</button>
  </div>
</div>
<div class="tool-section">
  <h2>效果预览</h2>
  <div class="result-output" id="preview" style="font-size:1.2rem">The quick brown fox jumps over the lazy dog.</div>
  <p style="color:#94a3b8;font-size:.8rem">点击上方按钮预览对应风格</p>
</div>
<script>
var maps={{\nbold:{{A:'𝐀',B:'𝐁',C:'𝐂',D:'𝐃',E:'𝐄',F:'𝐅',G:'𝐆',H:'𝐇',I:'𝐈',J:'𝐉',K:'𝐊',L:'𝐋',M:'𝐌',N:'𝐍',O:'𝐎',P:'𝐏',Q:'𝐐',R:'𝐑',S:'𝐒',T:'𝐓',U:'𝐔',V:'𝐕',W:'𝐖',X:'𝐗',Y:'𝐘',Z:'𝐙',a:'𝐚',b:'𝐛',c:'𝐜',d:'𝐝',e:'𝐞',f:'𝐟',g:'𝐠',h:'𝐡',i:'𝐢',j:'𝐣',k:'𝐤',l:'𝐥',m:'𝐦',n:'𝐧',o:'𝐨',p:'𝐩',q:'𝐪',r:'𝐫',s:'𝐬',t:'𝐭',u:'𝐮',v:'𝐯',w:'𝐰',x:'𝐱',y:'𝐲',z:'𝐳','0':'𝟎','1':'𝟏','2':'𝟐','3':'𝟑','4':'𝟒','5':'𝟓','6':'𝟔','7':'𝟕','8':'𝟖','9':'𝟗'}},
italic:{{A:'𝐴',B:'𝐵',C:'𝐶',D:'𝐷',E:'𝐸',F:'𝐹',G:'𝐺',H:'𝐻',I:'𝐼',J:'𝐽',K:'𝐾',L:'𝐿',M:'𝑀',N:'𝑁',O:'𝑂',P:'𝑃',Q:'𝑄',R:'𝑅',S:'𝑆',T:'𝑇',U:'𝑈',V:'𝑉',W:'𝑊',X:'𝑋',Y:'𝑌',Z:'𝑍',a:'𝑎',b:'𝑏',c:'𝑐',d:'𝑑',e:'𝑒',f:'𝑓',g:'𝑔',h:'ℎ',i:'𝑖',j:'𝑗',k:'𝑘',l:'𝑙',m:'𝑚',n:'𝑛',o:'𝑜',p:'𝑝',q:'𝑞',r:'𝑟',s:'𝑠',t:'𝑡',u:'𝑢',v:'𝑣',w:'𝑤',x:'𝑥',y:'𝑦',z:'𝑧'}},
boldItalic:{{A:'𝑨',B:'𝑩',C:'𝑪',D:'𝑫',E:'𝑬',F:'𝑭',G:'𝑮',H:'𝑯',I:'𝑰',J:'𝑱',K:'𝑲',L:'𝑳',M:'𝑴',N:'𝑵',O:'𝑶',P:'𝑷',Q:'𝑸',R:'𝑹',S:'𝑺',T:'𝑻',U:'𝑼',V:'𝑽',W:'𝑾',X:'𝑿',Y:'𝒀',Z:'𝒁',a:'𝒂',b:'𝒃',c:'𝒄',d:'𝒅',e:'𝒆',f:'𝒇',g:'𝒈',h:'𝒉',i:'𝒊',j:'𝒋',k:'𝒌',l:'𝒍',m:'𝒎',n:'𝒏',o:'𝒐',p:'𝒑',q:'𝒒',r:'𝒓',s:'𝒔',t:'𝒕',u:'𝒖',v:'𝒗',w:'𝒘',x:'𝒙',y:'𝒚',z:'𝒛'}},
script:{{A:'𝒜',B:'ℬ',C:'𝒞',D:'𝒟',E:'ℰ',F:'ℱ',G:'𝒢',H:'ℋ',I:'ℐ',J:'𝒥',K:'𝒦',L:'ℒ',M:'ℳ',N:'𝒩',O:'𝒪',P:'𝒫',Q:'𝒬',R:'ℛ',S:'𝒮',T:'𝒯',U:'𝒰',V:'𝒱',W:'𝒲',X:'𝒳',Y:'𝒴',Z:'𝒵',a:'𝒶',b:'𝒷',c:'𝒸',d:'𝒹',e:'ℯ',f:'𝒻',g:'ℊ',h:'𝒽',i:'𝒾',j:'𝒿',k:'𝓀',l:'𝓁',m:'𝓂',n:'𝓃',o:'ℴ',p:'𝓅',q:'𝓆',r:'𝓇',s:'𝓈',t:'𝓉',u:'𝓊',v:'𝓋',w:'𝓌',x:'𝓍',y:'𝓎',z:'𝓏'}},
double:{{A:'𝔸',B:'𝔹',C:'ℂ',D:'𝔻',E:'𝔼',F:'𝔽',G:'𝔾',H:'ℍ',I:'𝕀',J:'𝕁',K:'𝕂',L:'𝕃',M:'𝕄',N:'ℕ',O:'𝕆',P:'ℙ',Q:'ℚ',R:'ℝ',S:'𝕊',T:'𝕋',U:'𝕌',V:'𝕍',W:'𝕎',X:'𝕏',Y:'𝕐',Z:'ℤ',a:'𝕒',b:'𝕓',c:'𝕔',d:'𝕕',e:'𝕖',f:'𝕗',g:'𝕘',h:'𝕙',i:'𝕚',j:'𝕛',k:'𝕜',l:'𝕝',m:'𝕞',n:'𝕟',o:'𝕠',p:'𝕡',q:'𝕢',r:'𝕣',s:'𝕤',t:'𝕥',u:'𝕦',v:'𝕧',w:'𝕨',x:'𝕩',y:'𝕪',z:'𝕫','0':'𝟘','1':'𝟙','2':'𝟚','3':'𝟛','4':'𝟜','5':'𝟝','6':'𝟞','7':'𝟟','8':'𝟠','9':'𝟡'}},
mono:{{A:'𝙰',B:'𝙱',C:'𝙲',D:'𝙳',E:'𝙴',F:'𝙵',G:'𝙶',H:'𝙷',I:'𝙸',J:'𝙹',K:'𝙺',L:'𝙻',M:'𝙼',N:'𝙽',O:'𝙾',P:'𝙿',Q:'𝚀',R:'𝚁',S:'𝚂',T:'𝚃',U:'𝚄',V:'𝚅',W:'𝚆',X:'𝚇',Y:'𝚈',Z:'𝚉',a:'𝚊',b:'𝚋',c:'𝚌',d:'𝚍',e:'𝚎',f:'𝚏',g:'𝚐',h:'𝚑',i:'𝚒',j:'𝚓',k:'𝚔',l:'𝚕',m:'𝚖',n:'𝚗',o:'𝚘',p:'𝚙',q:'𝚚',r:'𝚛',s:'𝚜',t:'𝚝',u:'𝚞',v:'𝚟',w:'𝚠',x:'𝚡',y:'𝚢',z:'𝚣','0':'𝟶','1':'𝟷','2':'𝟸','3':'𝟹','4':'𝟺','5':'𝟻','6':'𝟼','7':'𝟽','8':'𝟾','9':'𝟿'}},
sans:{{A:'𝗔',B:'𝗕',C:'𝗖',D:'𝗗',E:'𝗘',F:'𝗙',G:'𝗚',H:'𝗛',I:'𝗜',J:'𝗝',K:'𝗞',L:'𝗟',M:'𝗠',N:'𝗡',O:'𝗢',P:'𝗣',Q:'𝗤',R:'𝗥',S:'𝗦',T:'𝗧',U:'𝗨',V:'𝗩',W:'𝗪',X:'𝗫',Y:'𝗬',Z:'𝗭',a:'𝗮',b:'𝗯',c:'𝗰',d:'𝗱',e:'𝗲',f:'𝗳',g:'𝗴',h:'𝗵',i:'𝗶',j:'𝗷',k:'𝗸',l:'𝗹',m:'𝗺',n:'𝗻',o:'𝗼',p:'𝗽',q:'𝗾',r:'𝗿',s:'𝘀',t:'𝘁',u:'𝘂',v:'𝘃',w:'𝘄',x:'𝘅',y:'𝘆',z:'𝘇','0':'𝟬','1':'𝟭','2':'𝟮','3':'𝟯','4':'𝟰','5':'𝟱','6':'𝟲','7':'𝟳','8':'𝟴','9':'𝟵'}},
sansItalic:{{A:'𝘈',B:'𝘉',C:'𝘊',D:'𝘋',E:'𝘌',F:'𝘍',G:'𝘎',H:'𝘏',I:'𝘐',J:'𝘑',K:'𝘒',L:'𝘓',M:'𝘔',N:'𝘕',O:'𝘖',P:'𝘗',Q:'𝘘',R:'𝘙',S:'𝘚',T:'𝘛',U:'𝘜',V:'𝘝',W:'𝘞',X:'𝘟',Y:'𝘠',Z:'𝘡',a:'𝘢',b:'𝘣',c:'𝘤',d:'𝘥',e:'𝘦',f:'𝘧',g:'𝘨',h:'𝘩',i:'𝘪',j:'𝘫',k:'𝘬',l:'𝘭',m:'𝘮',n:'𝘯',o:'𝘰',p:'𝘱',q:'𝘲',r:'𝘳',s:'𝘴',t:'𝘵',u:'𝘶',v:'𝘷',w:'𝘸',x:'𝘹',y:'𝘺',z:'𝘻'}},
sansBoldItalic:{{A:'𝘼',B:'𝘽',C:'𝘾',D:'𝘿',E:'𝙀',F:'𝙁',G:'𝙂',H:'𝙃',I:'𝙄',J:'𝙅',K:'𝙆',L:'𝙇',M:'𝙈',N:'𝙉',O:'𝙊',P:'𝙋',Q:'𝙌',R:'𝙍',S:'𝙎',T:'𝙏',U:'𝙐',V:'𝙑',W:'𝙒',X:'𝙓',Y:'𝙔',Z:'𝙕',a:'𝙖',b:'𝙗',c:'𝙘',d:'𝙙',e:'𝙚',f:'𝙛',g:'𝙜',h:'𝙝',i:'𝙞',j:'𝙟',k:'𝙠',l:'𝙡',m:'𝙢',n:'𝙣',o:'𝙤',p:'𝙥',q:'𝙦',r:'𝙧',s:'𝙨',t:'𝙩',u:'𝙪',v:'𝙫',w:'𝙬',x:'𝙭',y:'𝙮',z:'𝙯'}}}};
var currentStyle='bold';
function convertStyle(style){{
  currentStyle=style;
  var input=document.getElementById('inputText').value;
  if(!input)return;
  var map=maps[style];
  var result=input.split('').map(function(c){{return map[c]||c;}}).join('');
  document.getElementById('resultOutput').textContent=result;
  var preview='The quick brown fox jumps over the lazy dog.';
  document.getElementById('preview').textContent=preview.split('').map(function(c){{return map[c]||c;}}).join('');
  document.querySelectorAll('[id^=btn]').forEach(function(b){{b.className='btn btn-secondary';}});
  var id='btn'+style.charAt(0).toUpperCase()+style.slice(1);
  if(style==='boldItalic')id='btnBoldItalic';
  else if(style==='sansItalic')id='btnSansItalic';
  else if(style==='sansBoldItalic')id='btnSansBoldItalic';
  document.getElementById(id).className='btn btn-primary';
}}
function copyResult(){{
  var text=document.getElementById('resultOutput').textContent;
  if(!text||text==='等待输入...')return;
  navigator.clipboard.writeText(text).then(function(){{showToast('已复制!');}});
}}
function clearAll(){{document.getElementById('inputText').value='';document.getElementById('resultOutput').textContent='等待输入...';}}
function showToast(msg){{var t=document.getElementById('toast');t.textContent=msg;t.classList.add('show');setTimeout(function(){{t.classList.remove('show');}},2000);}}
document.getElementById('inputText').addEventListener('input',function(){{convertStyle(currentStyle);}});
</script>''',
        '''<div class="tool-section">
  <h2>Enter Text</h2>
  <textarea id="inputText" placeholder="Enter text to convert..." style="min-height:80px"></textarea>
</div>
<div class="tool-section">
  <h2>Select Style</h2>
  <div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:12px">
    <button class="btn btn-primary" onclick="convertStyle('bold')" id="btnBold">𝐁 Bold</button>
    <button class="btn btn-secondary" onclick="convertStyle('italic')" id="btnItalic">𝐼 Italic</button>
    <button class="btn btn-secondary" onclick="convertStyle('boldItalic')" id="btnBoldItalic">𝑩 Bold Italic</button>
    <button class="btn btn-secondary" onclick="convertStyle('script')" id="btnScript">𝒮 Script</button>
    <button class="btn btn-secondary" onclick="convertStyle('double')" id="btnDouble">𝔻 Double</button>
    <button class="btn btn-secondary" onclick="convertStyle('mono')" id="btnMono">𝙼 Mono</button>
    <button class="btn btn-secondary" onclick="convertStyle('sans')" id="btnSans">𝗔 Sans Bold</button>
    <button class="btn btn-secondary" onclick="convertStyle('sansItalic')" id="btnSansItalic">𝘈 Sans Italic</button>
    <button class="btn btn-secondary" onclick="convertStyle('sansBoldItalic')" id="btnSansBoldItalic">𝘼 Sans Bold Italic</button>
  </div>
</div>
<div class="tool-section">
  <h2>Result</h2>
  <div class="result-output" id="resultOutput" style="font-size:1.5rem">Waiting for input...</div>
  <div class="result-actions">
    <button class="btn btn-primary" onclick="copyResult()">📋 Copy</button>
    <button class="btn btn-secondary" onclick="clearAll()">🗑️ Clear</button>
  </div>
</div>
<div class="tool-section">
  <h2>Preview</h2>
  <div class="result-output" id="preview" style="font-size:1.2rem">The quick brown fox jumps over the lazy dog.</div>
  <p style="color:#94a3b8;font-size:.8rem">Click a style above to preview</p>
</div>
<script>
var maps={{\nbold:{{A:'𝐀',B:'𝐁',C:'𝐂',D:'𝐃',E:'𝐄',F:'𝐅',G:'𝐆',H:'𝐇',I:'𝐈',J:'𝐉',K:'𝐊',L:'𝐋',M:'𝐌',N:'𝐍',O:'𝐎',P:'𝐏',Q:'𝐐',R:'𝐑',S:'𝐒',T:'𝐓',U:'𝐔',V:'𝐕',W:'𝐖',X:'𝐗',Y:'𝐘',Z:'𝐙',a:'𝐚',b:'𝐛',c:'𝐜',d:'𝐝',e:'𝐞',f:'𝐟',g:'𝐠',h:'𝐡',i:'𝐢',j:'𝐣',k:'𝐤',l:'𝐥',m:'𝐦',n:'𝐧',o:'𝐨',p:'𝐩',q:'𝐪',r:'𝐫',s:'𝐬',t:'𝐭',u:'𝐮',v:'𝐯',w:'𝐰',x:'𝐱',y:'𝐲',z:'𝐳','0':'𝟎','1':'𝟏','2':'𝟐','3':'𝟑','4':'𝟒','5':'𝟓','6':'𝟔','7':'𝟕','8':'𝟖','9':'𝟗'}},
italic:{{A:'𝐴',B:'𝐵',C:'𝐶',D:'𝐷',E:'𝐸',F:'𝐹',G:'𝐺',H:'𝐻',I:'𝐼',J:'𝐽',K:'𝐾',L:'𝐿',M:'𝑀',N:'𝑁',O:'𝑂',P:'𝑃',Q:'𝑄',R:'𝑅',S:'𝑆',T:'𝑇',U:'𝑈',V:'𝑉',W:'𝑊',X:'𝑋',Y:'𝑌',Z:'𝑍',a:'𝑎',b:'𝑏',c:'𝑐',d:'𝑑',e:'𝑒',f:'𝑓',g:'𝑔',h:'ℎ',i:'𝑖',j:'𝑗',k:'𝑘',l:'𝑙',m:'𝑚',n:'𝑛',o:'𝑜',p:'𝑝',q:'𝑞',r:'𝑟',s:'𝑠',t:'𝑡',u:'𝑢',v:'𝑣',w:'𝑤',x:'𝑥',y:'𝑦',z:'𝑧'}},
boldItalic:{{A:'𝑨',B:'𝑩',C:'𝑪',D:'𝑫',E:'𝑬',F:'𝑭',G:'𝑮',H:'𝑯',I:'𝑰',J:'𝑱',K:'𝑲',L:'𝑳',M:'𝑴',N:'𝑵',O:'𝑶',P:'𝑷',Q:'𝑸',R:'𝑹',S:'𝑺',T:'𝑻',U:'𝑼',V:'𝑽',W:'𝑾',X:'𝑿',Y:'𝒀',Z:'𝒁',a:'𝒂',b:'𝒃',c:'𝒄',d:'𝒅',e:'𝒆',f:'𝒇',g:'𝒈',h:'𝒉',i:'𝒊',j:'𝒋',k:'𝒌',l:'𝒍',m:'𝒎',n:'𝒏',o:'𝒐',p:'𝒑',q:'𝒒',r:'𝒓',s:'𝒔',t:'𝒕',u:'𝒖',v:'𝒗',w:'𝒘',x:'𝒙',y:'𝒚',z:'𝒛'}},
script:{{A:'𝒜',B:'ℬ',C:'𝒞',D:'𝒟',E:'ℰ',F:'ℱ',G:'𝒢',H:'ℋ',I:'ℐ',J:'𝒥',K:'𝒦',L:'ℒ',M:'ℳ',N:'𝒩',O:'𝒪',P:'𝒫',Q:'𝒬',R:'ℛ',S:'𝒮',T:'𝒯',U:'𝒰',V:'𝒱',W:'𝒲',X:'𝒳',Y:'𝒴',Z:'𝒵',a:'𝒶',b:'𝒷',c:'𝒸',d:'𝒹',e:'ℯ',f:'𝒻',g:'ℊ',h:'𝒽',i:'𝒾',j:'𝒿',k:'𝓀',l:'𝓁',m:'𝓂',n:'𝓃',o:'ℴ',p:'𝓅',q:'𝓆',r:'𝓇',s:'𝓈',t:'𝓉',u:'𝓊',v:'𝓋',w:'𝓌',x:'𝓍',y:'𝓎',z:'𝓏'}},
double:{{A:'𝔸',B:'𝔹',C:'ℂ',D:'𝔻',E:'𝔼',F:'𝔽',G:'𝔾',H:'ℍ',I:'𝕀',J:'𝕁',K:'𝕂',L:'𝕃',M:'𝕄',N:'ℕ',O:'𝕆',P:'ℙ',Q:'ℚ',R:'ℝ',S:'𝕊',T:'𝕋',U:'𝕌',V:'𝕍',W:'𝕎',X:'𝕏',Y:'𝕐',Z:'ℤ',a:'𝕒',b:'𝕓',c:'𝕔',d:'𝕕',e:'𝕖',f:'𝕗',g:'𝕘',h:'𝕙',i:'𝕚',j:'𝕛',k:'𝕜',l:'𝕝',m:'𝕞',n:'𝕟',o:'𝕠',p:'𝕡',q:'𝕢',r:'𝕣',s:'𝕤',t:'𝕥',u:'𝕦',v:'𝕧',w:'𝕨',x:'𝕩',y:'𝕪',z:'𝕫','0':'𝟘','1':'𝟙','2':'𝟚','3':'𝟛','4':'𝟜','5':'𝟝','6':'𝟞','7':'𝟟','8':'𝟠','9':'𝟡'}},
mono:{{A:'𝙰',B:'𝙱',C:'𝙲',D:'𝙳',E:'𝙴',F:'𝙵',G:'𝙶',H:'𝙷',I:'𝙸',J:'𝙹',K:'𝙺',L:'𝙻',M:'𝙼',N:'𝙽',O:'𝙾',P:'𝙿',Q:'𝚀',R:'𝚁',S:'𝚂',T:'𝚃',U:'𝚄',V:'𝚅',W:'𝚆',X:'𝚇',Y:'𝚈',Z:'𝚉',a:'𝚊',b:'𝚋',c:'𝚌',d:'𝚍',e:'𝚎',f:'𝚏',g:'𝚐',h:'𝚑',i:'𝚒',j:'𝚓',k:'𝚔',l:'𝚕',m:'𝚖',n:'𝚗',o:'𝚘',p:'𝚙',q:'𝚚',r:'𝚛',s:'𝚜',t:'𝚝',u:'𝚞',v:'𝚟',w:'𝚠',x:'𝚡',y:'𝚢',z:'𝚣','0':'𝟶','1':'𝟷','2':'𝟸','3':'𝟹','4':'𝟺','5':'𝟻','6':'𝟼','7':'𝟽','8':'𝟾','9':'𝟿'}},
sans:{{A:'𝗔',B:'𝗕',C:'𝗖',D:'𝗗',E:'𝗘',F:'𝗙',G:'𝗚',H:'𝗛',I:'𝗜',J:'𝗝',K:'𝗞',L:'𝗟',M:'𝗠',N:'𝗡',O:'𝗢',P:'𝗣',Q:'𝗤',R:'𝗥',S:'𝗦',T:'𝗧',U:'𝗨',V:'𝗩',W:'𝗪',X:'𝗫',Y:'𝗬',Z:'𝗭',a:'𝗮',b:'𝗯',c:'𝗰',d:'𝗱',e:'𝗲',f:'𝗳',g:'𝗴',h:'𝗵',i:'𝗶',j:'𝗷',k:'𝗸',l:'𝗹',m:'𝗺',n:'𝗻',o:'𝗼',p:'𝗽',q:'𝗾',r:'𝗿',s:'𝘀',t:'𝘁',u:'𝘂',v:'𝘃',w:'𝘄',x:'𝘅',y:'𝘆',z:'𝘇','0':'𝟬','1':'𝟭','2':'𝟮','3':'𝟯','4':'𝟰','5':'𝟱','6':'𝟲','7':'𝟳','8':'𝟴','9':'𝟵'}},
sansItalic:{{A:'𝘈',B:'𝘉',C:'𝘊',D:'𝘋',E:'𝘌',F:'𝘍',G:'𝘎',H:'𝘏',I:'𝘐',J:'𝘑',K:'𝘒',L:'𝘓',M:'𝘔',N:'𝘕',O:'𝘖',P:'𝘗',Q:'𝘘',R:'𝘙',S:'𝘚',T:'𝘛',U:'𝘜',V:'𝘝',W:'𝘞',X:'𝘟',Y:'𝘠',Z:'𝘡',a:'𝘢',b:'𝘣',c:'𝘤',d:'𝘥',e:'𝘦',f:'𝘧',g:'𝘨',h:'𝘩',i:'𝘪',j:'𝘫',k:'𝘬',l:'𝘭',m:'𝘮',n:'𝘯',o:'𝘰',p:'𝘱',q:'𝘲',r:'𝘳',s:'𝘴',t:'𝘵',u:'𝘶',v:'𝘷',w:'𝘸',x:'𝘹',y:'𝘺',z:'𝘻'}},
sansBoldItalic:{{A:'𝘼',B:'𝘽',C:'𝘾',D:'𝘿',E:'𝙀',F:'𝙁',G:'𝙂',H:'𝙃',I:'𝙄',J:'𝙅',K:'𝙆',L:'𝙇',M:'𝙈',N:'𝙉',O:'𝙊',P:'𝙋',Q:'𝙌',R:'𝙍',S:'𝙎',T:'𝙏',U:'𝙐',V:'𝙑',W:'𝙒',X:'𝙓',Y:'𝙔',Z:'𝙕',a:'𝙖',b:'𝙗',c:'𝙘',d:'𝙙',e:'𝙚',f:'𝙛',g:'𝙜',h:'𝙝',i:'𝙞',j:'𝙟',k:'𝙠',l:'𝙡',m:'𝙢',n:'𝙣',o:'𝙤',p:'𝙥',q:'𝙦',r:'𝙧',s:'𝙨',t:'𝙩',u:'𝙪',v:'𝙫',w:'𝙬',x:'𝙭',y:'𝙮',z:'𝙯'}}}};
var currentStyle='bold';
function convertStyle(style){{
  currentStyle=style;
  var input=document.getElementById('inputText').value;
  if(!input)return;
  var map=maps[style];
  var result=input.split('').map(function(c){{return map[c]||c;}}).join('');
  document.getElementById('resultOutput').textContent=result;
  var preview='The quick brown fox jumps over the lazy dog.';
  document.getElementById('preview').textContent=preview.split('').map(function(c){{return map[c]||c;}}).join('');
  document.querySelectorAll('[id^=btn]').forEach(function(b){{b.className='btn btn-secondary';}});
  var id='btn'+style.charAt(0).toUpperCase()+style.slice(1);
  if(style==='boldItalic')id='btnBoldItalic';
  else if(style==='sansItalic')id='btnSansItalic';
  else if(style==='sansBoldItalic')id='btnSansBoldItalic';
  document.getElementById(id).className='btn btn-primary';
}}
function copyResult(){{
  var text=document.getElementById('resultOutput').textContent;
  if(!text||text==='Waiting for input...')return;
  navigator.clipboard.writeText(text).then(function(){{showToast('Copied!');}});
}}
function clearAll(){{document.getElementById('inputText').value='';document.getElementById('resultOutput').textContent='Waiting for input...';}}
function showToast(msg){{var t=document.getElementById('toast');t.textContent=msg;t.classList.add('show');setTimeout(function(){{t.classList.remove('show');}},2000);}}
document.getElementById('inputText').addEventListener('input',function(){{convertStyle(currentStyle);}});
</script>''',
        'Unicode粗体文字使用数学字母符号区块的字符，而非CSS样式。这意味着在任何平台（包括不支持富文本的地方）都能显示粗体等装饰效果。本工具支持9种Unicode风格转换。',
        'Unicode bold text uses characters from the Mathematical Alphanumeric Symbols block rather than CSS styling. This means decorative text displays on any platform including those without rich text support. Supports 9 Unicode styles.'
    )

    return bodies

def gen_all():
    bodies = build_tool_bodies()
    for tool in TOOLS:
        slug = tool['slug']
        cn_name_noemoji = tool['cn_name'].split(' ', 1)[-1] if ' ' in tool['cn_name'] else tool['cn_name']
        en_name_noemoji = tool['en_name'].split(' ', 1)[-1] if ' ' in tool['en_name'] else tool['en_name']
        
        body_cn, body_en, seo_cn, seo_en = bodies[slug]
        
        cn_badges_list = tool['cn_badges'].split()
        en_badges_list = tool['en_badges'].split()
        
        cn_badges_withpipe = '</span><span class="badge">'.join(cn_badges_list)
        en_badges_withpipe = '</span><span class="badge">'.join(en_badges_list)
        
        cn_keywords = f"在线{tool['cn_name_noemoji']},{slug},{tool['category']},在线工具,免费"
        en_keywords = f"online {slug},{slug},{tool['category']},free online tool"
        
        cn_og_title = tool['cn_title']
        en_og_title = tool['en_title']
        
        # CN page
        cn_page = TEMPLATE_CN.format(
            slug=slug,
            cn_desc=tool['cn_desc'],
            cn_title=tool['cn_title'],
            cn_icon=tool['cn_icon'],
            cn_name_noemoji=cn_name_noemoji,
            cn_hero=tool['cn_hero'],
            cn_badges_withpipe=cn_badges_withpipe,
            cn_keywords=cn_keywords,
            cn_og_title=cn_og_title,
            cn_seo_text=seo_cn,
            BODY_CN=body_cn,
        )
        
        # EN page
        en_page = TEMPLATE_EN.format(
            slug=slug,
            en_desc=tool['en_desc'],
            en_title=tool['en_title'],
            en_icon=tool['en_icon'],
            en_name_noemoji=en_name_noemoji,
            en_hero=tool['en_hero'],
            en_badges_withpipe=en_badges_withpipe,
            en_keywords=en_keywords,
            en_og_title=en_og_title,
            en_seo_text=seo_en,
            BODY_EN=body_en,
        )
        
        # Create dirs and write
        os.makedirs(f'{BASE}/{slug}', exist_ok=True)
        os.makedirs(f'{BASE}/en/{slug}', exist_ok=True)
        
        with open(f'{BASE}/{slug}/index.html', 'w') as f:
            f.write(cn_page)
        with open(f'{BASE}/en/{slug}/index.html', 'w') as f:
            f.write(en_page)
        
        print(f'✅ {slug} (CN + EN)')

if __name__ == '__main__':
    gen_all()
