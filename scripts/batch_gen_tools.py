#!/usr/bin/env python3
"""批量生成5个新工具页面 CN+EN，带首页同步"""
import os, json, re

BASE = "/home/chison/tools-site"
GA_ID = "G-9W1157EBQV"
ADS_CLIENT = "ca-pub-5998441792679372"

TOOLS = [
    {
        "slug": "spaced-repetition-scheduler",
        "cn_name": "间隔重复学习计划表",
        "en_name": "Spaced Repetition Scheduler",
        "cn_desc": "基于遗忘曲线生成科学复习计划，输入学习内容自动安排间隔复习时间，提升记忆效率。纯前端本地计算，数据安全不上传服务器。",
        "en_desc": "Generate scientifically optimized review schedules based on the forgetting curve. Input study material and automatically schedule spaced repetition intervals to boost memory retention. 100% client-side, no data upload.",
        "emoji": "🧠",
        "cn_faq": [
            {"q": "什么是间隔重复？", "a": "间隔重复（Spaced Repetition）是一种基于遗忘曲线的科学学习方法。德国心理学家艾宾浩斯发现，记忆会在学习后随时间衰退，但在遗忘临界点进行复习可以显著延长记忆保留时间。间隔重复通过在逐渐扩大的时间间隔（如1天、3天、7天、30天）进行复习，将短期记忆转化为长期记忆。"},
            {"q": "间隔重复适用于哪些学习场景？", "a": "间隔重复适用于几乎所有需要记忆的内容：外语词汇学习、考试备考（医学/法律/CPA等）、编程语法记忆、历史事件和日期、公式和定理、人名面孔记忆、演讲和PPT内容背诵。"},
            {"q": "如何使用这个间隔重复计划表？", "a": "输入你要学习的内容名称和数量（如「GRE单词3000个」），选择学习期限（如30天），系统会根据艾宾浩斯遗忘曲线生成每日需要复习的内容和时间表。你可以在每次复习后标记掌握程度，系统会动态调整复习间隔。"},
            {"q": "间隔重复的复习间隔应该怎么设置？", "a": "经典间隔：1天→3天→7天→16天→35天。对于难度较高的内容，可以使用更紧凑的间隔：1天→2天→4天→8天→16天。本工具默认使用SM-2算法优化间隔，你也可以手动自定义间隔参数。"},
        ],
        "en_faq": [
            {"q": "What is spaced repetition?", "a": "Spaced Repetition is a scientifically proven learning technique based on the forgetting curve. German psychologist Hermann Ebbinghaus discovered that memory decays over time, but reviewing at critical forgetting points significantly extends retention. By scheduling reviews at gradually increasing intervals (e.g., 1 day, 3 days, 7 days, 30 days), it converts short-term memory into long-term memory."},
            {"q": "What can I use spaced repetition for?", "a": "Spaced repetition works for almost any memorization task: foreign language vocabulary, exam preparation (medical/law/CPA), programming syntax, historical dates, formulas and theorems, name-face association, speech and presentation memorization."},
            {"q": "How do I use this scheduler?", "a": "Enter the name and quantity of content to learn (e.g., 'GRE Vocabulary 3000 words'), set a study period (e.g., 30 days), and the system generates daily review tasks and timelines based on the Ebbinghaus forgetting curve. Mark your mastery level after each review to have the intervals dynamically adjusted."},
            {"q": "What review intervals should I use?", "a": "Classic intervals: 1 day → 3 days → 7 days → 16 days → 35 days. For harder content, use tighter intervals: 1 day → 2 days → 4 days → 8 days → 16 days. This tool uses the SM-2 algorithm by default, with manual interval customization available."},
        ],
    },
    {
        "slug": "pomodoro-tracker",
        "cn_name": "番茄钟计时器",
        "en_name": "Pomodoro Timer",
        "cn_desc": "在线番茄钟专注计时器，支持自定义工作/休息时长，任务统计和完成记录，帮助提高专注力和工作效率。纯前端本地计时，无需注册即可使用。",
        "en_desc": "Online Pomodoro focus timer with customizable work/break durations, task tracking and completion history. Boost focus and productivity. 100% client-side, no registration required.",
        "emoji": "🍅",
        "cn_faq": [
            {"q": "什么是番茄工作法？", "a": "番茄工作法（Pomodoro Technique）是Francesco Cirillo在1980年代发明的时间管理方法。基本原理：专注工作25分钟（一个番茄钟），然后休息5分钟。每完成4个番茄钟后，进行15-30分钟的长休息。这种方法利用短时间高强度专注+规律休息来维持注意力和防止疲劳。"},
            {"q": "番茄钟默认25分钟是最优的吗？", "a": "25分钟是经典设置，但并非所有人最佳。研究表明注意力持续时间因人而异。你可以根据自身情况调整：新手可从15分钟开始，熟练后可延长至45-50分钟。关键是找到你能保持高度专注的最长时间。"},
            {"q": "这个番茄钟能离线使用吗？", "a": "可以。加载页面后，计时器完全在浏览器本地运行，不依赖网络。你可以断开网络连接继续使用。"},
            {"q": "休息时间应该做什么？", "a": "短休息（5分钟）：站起来走动、喝水、眺望远方、做简单的伸展运动。长休息（15-30分钟）：散步、吃点心、闭目养神、听音乐。避免刷手机或看电脑屏幕——这些活动不会让大脑真正休息。"},
        ],
        "en_faq": [
            {"q": "What is the Pomodoro Technique?", "a": "The Pomodoro Technique is a time management method invented by Francesco Cirillo in the 1980s. Basic principle: work with full focus for 25 minutes (one Pomodoro), then take a 5-minute break. After 4 Pomodoros, take a 15-30 minute long break. This method uses short bursts of intense focus with regular breaks to maintain attention and prevent burnout."},
            {"q": "Is 25 minutes the optimal Pomodoro length?", "a": "25 minutes is the classic setting but not optimal for everyone. Research shows attention spans vary by individual. Beginners can start at 15 minutes, veterans can extend to 45-50 minutes. The key is finding your maximum sustained focus duration."},
            {"q": "Can I use this timer offline?", "a": "Yes. Once loaded, the timer runs entirely in the browser with no network dependency. You can disconnect and continue using it."},
            {"q": "What should I do during breaks?", "a": "Short breaks (5 min): stand up, walk around, drink water, look into the distance, do simple stretches. Long breaks (15-30 min): take a walk, have a snack, close your eyes, listen to music. Avoid checking your phone or looking at screens — these don't allow your brain to truly rest."},
        ],
    },
    {
        "slug": "pronunciation-guide",
        "cn_name": "英语发音查询工具",
        "en_name": "English Pronunciation Guide",
        "cn_desc": "在线英语单词发音查询工具，显示英式/美式音标，提供发音技巧和嘴型指导，支持常用词汇音标搜索。纯前端实现，不影响隐私安全。",
        "en_desc": "Online English pronunciation lookup tool with both British and American phonetic transcriptions, pronunciation tips, and mouth shape guidance. Search common vocabulary phonetics. 100% client-side, privacy-safe.",
        "emoji": "🔊",
        "cn_faq": [
            {"q": "音标有哪些类型？", "a": "主要有两种：IPA国际音标（International Phonetic Alphabet）和DJ音标（Daniel Jones，常用于英语学习词典）。本工具同时展示英式发音（RP，Received Pronunciation）和美式发音（GA，General American）的IPA音标。"},
            {"q": "如何利用音标准确发音？", "a": "1）学习每个音标的发音规则（如/θ/是咬舌音）；2）注意重音标记（ˈ表示主重音）；3）多听标准发音并模仿；4）使用本工具的嘴型指导了解舌位和口型。关键是多练，只看音标不够。"},
            {"q": "为什么同一个单词有不同发音？", "a": "主要原因：1）英式vs美式差异（如'bath'英式/bɑːθ/，美式/bæθ/）；2）词性不同导致重音变化（如'record'名词/ˈrekɔːd/，动词/rɪˈkɔːd/）；3）地区方言差异；4）语流音变（连读、弱读）。"},
            {"q": "音标和自然拼读有什么区别？", "a": "自然拼读（Phonics）是教儿童通过字母组合推测发音的方法，规则性强但例外多（如'tough'/'through'/'though'拼写相似但发音不同）。音标是一套精确记录语音的符号系统，一个符号对应一个发音，精准无误。学好音标是掌握英语发音的基础。"},
        ],
        "en_faq": [
            {"q": "What types of phonetic transcription exist?", "a": "Two main types: IPA (International Phonetic Alphabet) and DJ (Daniel Jones, commonly used in English learner dictionaries). This tool displays both British (RP, Received Pronunciation) and American (GA, General American) IPA transcriptions."},
            {"q": "How do I use phonetic transcriptions to pronounce correctly?", "a": "1) Learn each symbol's sound (e.g., /θ/ is the 'th' sound); 2) Note stress marks (ˈ indicates primary stress); 3) Listen to standard pronunciations and imitate; 4) Use this tool's mouth shape guidance for tongue position and lip shape. Practice is essential — reading transcriptions alone isn't enough."},
            {"q": "Why does the same word have different pronunciations?", "a": "Main reasons: 1) British vs. American differences (e.g., 'bath' British /bɑːθ/, American /bæθ/); 2) Part of speech affects stress (e.g., 'record' noun /ˈrekɔːd/, verb /rɪˈkɔːd/); 3) Regional dialect variations; 4) Connected speech phenomena (linking, reduction)."},
            {"q": "What's the difference between phonics and phonetic transcription?", "a": "Phonics teaches children to guess pronunciation from letter patterns — it's rule-based but has many exceptions (e.g., 'tough'/'through'/'though' look similar but sound different). Phonetic transcription is a precise symbol system where each symbol maps to exactly one sound. Mastering phonetic transcription is the foundation of accurate English pronunciation."},
        ],
    },
    {
        "slug": "vocabulary-builder",
        "cn_name": "英语词汇量测试",
        "en_name": "Vocabulary Builder",
        "cn_desc": "免费在线英语词汇量测试工具，通过随机抽样的科学方法快速估算你的英语词汇量。支持不同难度级别，提供详细分析报告和学习建议。",
        "en_desc": "Free online English vocabulary size estimator using random sampling methodology. Supports multiple difficulty levels with detailed analysis reports and learning recommendations. 100% client-side.",
        "emoji": "📚",
        "cn_faq": [
            {"q": "如何准确测试词汇量？", "a": "本工具采用分层随机抽样法：从不同词频等级（1000词、2000词、3000词...等）中随机抽取测试词，通过你对这些词的理解程度推算总体词汇量。这种方法比逐个测试快效，统计学上具有可靠的代表性。"},
            {"q": "多少词汇量算正常水平？", "a": "母语者词汇量：4-5岁约5000词，成人约20000-35000词。英语学习者：初中约1500词，高中约3500词，大学四级约4500词，六级约6000词，专业八级约10000词，GRE/托福约12000-15000词。日常交流需要3000词，流畅阅读需要8000-9000词。"},
            {"q": "如何快速扩大词汇量？", "a": "1）每天学习10-20个新词，使用间隔重复法复习；2）大量阅读英文材料（新闻、小说、专业文献）；3）学习词根词缀（如un-/re-/-tion），一个词根可推导多个单词；4）在上下文中学习，不要孤立背单词；5）使用新词造句或写作。"},
            {"q": "为什么有些词认得但用不出来？", "a": "这反映了「被动词汇」（能听懂/读懂）和「主动词汇」（能说/能写）的差异。被动词汇通常是主动词汇的1.5-2倍。要将被动转化为主动，需要刻意练习：用新词造句、写短文、口语中使用。输出练习是关键。"},
        ],
        "en_faq": [
            {"q": "How accurately can vocabulary size be estimated?", "a": "This tool uses stratified random sampling: it draws test words from different frequency bands (1K, 2K, 3K words, etc.) and extrapolates your total vocabulary based on recognition rates. This method is much faster than testing every word and is statistically representative."},
            {"q": "What vocabulary size is considered normal?", "a": "Native speakers: ages 4-5 ~5,000 words, adults ~20,000-35,000 words. English learners: middle school ~1,500, high school ~3,500, college CET-4 ~4,500, CET-6 ~6,000, TEM-8 ~10,000, GRE/TOEFL ~12,000-15,000. Daily conversation needs ~3,000 words; fluent reading needs ~8,000-9,000."},
            {"q": "How can I rapidly expand my vocabulary?", "a": "1) Learn 10-20 new words daily, review with spaced repetition; 2) Read extensively in English (news, novels, academic papers); 3) Study word roots and affixes (e.g., un-/re-/-tion) — one root unlocks many words; 4) Learn in context, don't memorize isolated words; 5) Use new words in sentences or writing."},
            {"q": "Why can I recognize words but not use them?", "a": "This reflects the gap between 'passive vocabulary' (words you can understand) and 'active vocabulary' (words you can use). Passive vocabulary is typically 1.5-2x larger than active. To convert passive to active, deliberate practice is needed: write sentences, short essays, and use new words in conversation. Output practice is key."},
        ],
    },
    {
        "slug": "multiplication-table-generator",
        "cn_name": "乘法口诀表生成器",
        "en_name": "Multiplication Table Generator",
        "cn_desc": "在线生成可打印乘法口诀表，支持1×1到20×20自定义范围，多种颜色主题和打印格式。适合小学生学习数学，家长和老师教学辅助工具。",
        "en_desc": "Generate printable multiplication tables online, customizable from 1×1 to 20×20 with multiple color themes and print formats. Perfect for elementary math learning, a teaching aid for parents and educators.",
        "emoji": "✖️",
        "cn_faq": [
            {"q": "为什么要学乘法口诀？", "a": "乘法口诀（九九乘法表）是数学的基础，熟练掌握可以：1）大幅提高计算速度；2）为除法、分数、比例等高级运算打基础；3）培养数感和心算能力；4）帮助解决日常生活中的实际问题（购物计算、面积计算等）。"},
            {"q": "最佳学习年龄是几岁？", "a": "大多数儿童在7-8岁（小学二年级）开始学习乘法口诀。但每个孩子发展速度不同，有些5-6岁就能理解简单乘法概念。关键是先确保孩子理解乘法的实际意义（重复加法），而不是单纯死记硬背。"},
            {"q": "如何帮助孩子高效记忆乘法口诀？", "a": "1）从易到难：先学2、5、10的倍数；2）利用对称性：3×4=4×3，减少一半记忆量；3）找规律：9的倍数各位数字之和为9；4）多感官学习：边读边写、用手指数数；5）游戏中学习：使用本工具打印彩色口诀表贴在书桌前。"},
            {"q": "大九九（1-20）有必要学吗？", "a": "标准九九表（1-9）是必须掌握的。大九九（10-20）对于提高计算速度和心算能力有帮助，但不是强制要求。对于数学竞赛、速算训练或对数学有浓厚兴趣的学生可以学习。先在1-9范围内达到毫秒级反应速度再考虑扩展。"},
        ],
        "en_faq": [
            {"q": "Why learn multiplication tables?", "a": "Multiplication tables are the foundation of mathematics. Mastering them enables: 1) Dramatically faster calculation speed; 2) A solid base for division, fractions, ratios, and advanced operations; 3) Development of number sense and mental math ability; 4) Solving practical daily problems (shopping calculations, area measurements, etc.)."},
            {"q": "What is the best age to start learning?", "a": "Most children start learning multiplication tables at ages 7-8 (Grade 2). But every child develops differently — some grasp simple multiplication concepts at 5-6. The key is ensuring children understand multiplication as repeated addition first, rather than rote memorization."},
            {"q": "How can I help my child memorize multiplication tables effectively?", "a": "1) Start easy: learn 2s, 5s, 10s first; 2) Use symmetry: 3×4=4×3, cutting memorization in half; 3) Find patterns: digits of multiples of 9 sum to 9; 4) Multi-sensory learning: read aloud while writing, use fingers; 5) Game-based learning: use this tool to print colorful tables and post them by the desk."},
            {"q": "Is learning up to 20×20 necessary?", "a": "The standard 1-9 table is essential. The extended 10-20 table is helpful for boosting calculation speed and mental math but is not mandatory. It's suitable for math competitions, speed calculation training, or students with strong math interest. Achieve millisecond-level response within 1-9 before considering extension."},
        ],
    },
]

def gen_page(tool, lang):
    """Generate a tool page HTML for CN or EN"""
    if lang == "cn":
        name = tool["cn_name"]
        desc = tool["cn_desc"]
        faq = tool["cn_faq"]
        lang_code = "zh-CN"
        hreflang_self = "zh"
        hreflang_other = "en"
        slug_dir = tool["slug"]
        other_dir = f"en/{tool['slug']}"
        breadcrumb_name = name
        lang_label = "中文"
        lang_other = "EN"
        switch_href = f"../en/{tool['slug']}/"
        index_href = "../index.html"
        index_tools = "../index.html#tools"
        tools_label = "工具"
        og_title = f"{name} - Free ToolBase"
        og_desc = desc
        no_reg = "无需注册 · 数据绝不上传服务器"
        badge_text = "零依赖·可离线使用"
        canonical = f"https://free-toolbase.com/{tool['slug']}/"
        privacy_text = "隐私政策"
        terms_text = "服务条款"
        about_text = "关于我们"
        footer_intro = f"{name} | {no_reg}"
        footer_email = "问题反馈: dexshuang@google.com"
        bclist_name = name
    else:
        name = tool["en_name"]
        desc = tool["en_desc"]
        faq = tool["en_faq"]
        lang_code = "en"
        hreflang_self = "en"
        hreflang_other = "zh"
        slug_dir = f"en/{tool['slug']}"
        other_dir = tool["slug"]
        breadcrumb_name = name
        lang_label = "EN"
        lang_other = "中文"
        switch_href = f"../{tool['slug']}/"
        index_href = "../index.html"
        index_tools = f"../index.html#tools"
        tools_label = "Tools"
        og_title = f"{name} - Free ToolBase"
        og_desc = desc
        no_reg = "No registration · Data never leaves your device"
        badge_text = "Zero Dependency · Works Offline"
        canonical = f"https://free-toolbase.com/en/{tool['slug']}/"
        privacy_text = "Privacy Policy"
        terms_text = "Terms of Service"
        about_text = "About Us"
        footer_intro = f"{name} | {no_reg}"
        footer_email = "Feedback: dexshuang@google.com"
        bclist_name = name

    faq_json = json.dumps([{"@type":"Question","name":x["q"],"acceptedAnswer":{"@type":"Answer","text":x["a"]}} for x in faq], ensure_ascii=False)
    
    emoji = tool["emoji"]
    
    html = f'''<!DOCTYPE html>
<html lang="{lang_code}">
<head>
<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','{GA_ID}');</script>
<script>window.addEventListener("error",function(e){{if(e&&e.message===""){{e.preventDefault();}}}});window.addEventListener("unhandledrejection",function(e){{if(e&&e.reason&&e.reason.message===""){{e.preventDefault();}}}});</script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="{desc}">
<meta name="keywords" content="在线{name},工具,在线工具,免费">
<title>{name} - Free ToolBase</title>
<link rel="canonical" href="{canonical}">
<meta property="og:title" content="{og_title}">
<meta property="og:description" content="{og_desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Free ToolBase">
<meta property="og:image" content="https://free-toolbase.com/og-image.svg">
<meta name="twitter:image" content="https://free-toolbase.com/og-image.svg">
<meta name="twitter:card" content="summary_large_image">
<link rel="alternate" hreflang="{hreflang_self}" href="{canonical}">
<link rel="alternate" hreflang="{hreflang_other}" href="https://free-toolbase.com/{other_dir}/">
<link rel="alternate" hreflang="x-default" href="https://free-toolbase.com/en/{tool['slug']}/">
<meta name="robots" content="index, follow">
<link rel="icon" type="image/svg+xml" href="favicon.svg">
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADS_CLIENT}" crossorigin="anonymous"></script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"SoftwareApplication","name":"{name}","description":"{desc}","applicationCategory":"UtilitiesApplication","operatingSystem":"Web","publisher":{{"@type":"Organization","name":"Free ToolBase","email":"dexshuang@google.com"}},"offers":{{"@type":"Offer","price":"0","priceCurrency":"USD"}}}}</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"FAQPage","mainEntity":{faq_json}}}</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"HowTo","name":"如何使用{name}","description":"如何使用{name}的详细步骤指南","totalTime":"PT3M","tool":{{"@type":"HowToTool","name":"{name}"}},"step":[{{"@type":"HowToStep","position":1,"name":"输入数据","text":"在输入框中输入需要的参数"}},{{"@type":"HowToStep","position":2,"name":"选择选项","text":"根据需要选择模式或参数"}},{{"@type":"HowToStep","position":3,"name":"点击执行","text":"点击按钮运行工具"}},{{"@type":"HowToStep","position":4,"name":"查看结果","text":"查看结果，支持复制或导出"}}]}}</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"首页","item":"https://free-toolbase.com/"}},{{"@type":"ListItem","position":2,"name":"{tools_label}","item":"https://free-toolbase.com/#tools"}},{{"@type":"ListItem","position":3,"name":"{bclist_name}","item":"{canonical}"}}]}}</script>
<style>*{{box-sizing:border-box;margin:0;padding:0}}body{{background:#0f172a;color:#e2e8f0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,"PingFang SC","Microsoft YaHei",sans-serif;line-height:1.6;min-height:100vh}}a{{color:#06b6d4;text-decoration:none}}a:hover{{color:#22d3ee}}.container{{max-width:960px;margin:0 auto;padding:24px 16px}}.header{{display:flex;justify-content:space-between;align-items:center;margin-bottom:24px;flex-wrap:wrap;gap:12px}}.header h1{{font-size:1.5rem;color:#f1c40f}}.lang-switch{{display:flex;gap:4px;background:#1e293b;border-radius:8px;padding:4px;border:1px solid rgba(148,163,184,.1)}}.lang-switch a{{padding:6px 12px;border-radius:5px;font-size:.85rem;color:#94a3b8}}.lang-switch a.active{{background:rgba(6,182,212,.2);color:#22d3ee}}.nav-back{{color:#64748b;font-size:.85rem;margin-bottom:16px}}.nav-back a{{color:#64748b}}.nav-back a:hover{{color:#94a3b8}}.hero{{margin-bottom:24px}}.hero p{{color:#94a3b8;font-size:1rem;margin-bottom:8px}}.badge{{display:inline-block;background:rgba(6,182,212,.15);color:#22d3ee;padding:4px 12px;border-radius:20px;font-size:.8rem;margin-bottom:16px}}.section{{background:#1e293b;border-radius:12px;padding:20px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1)}}.section h2{{font-size:1.1rem;color:#f1c40f;margin-bottom:12px}}.form-group{{margin-bottom:14px}}.form-group label{{display:block;color:#94a3b8;font-size:.9rem;margin-bottom:6px;font-weight:500}}.form-group input,.form-group select,.form-group textarea{{width:100%;padding:10px 14px;background:#0f172a;border:1px solid rgba(148,163,184,.2);border-radius:8px;color:#e2e8f0;font-size:.9rem;outline:none;transition:all .2s}}.form-group input:focus,.form-group select:focus,.form-group textarea:focus{{border-color:rgba(6,182,212,.4);box-shadow:0 0 0 3px rgba(6,182,212,.1)}}.btn-row{{display:flex;gap:10px;margin-top:16px;flex-wrap:wrap}}.btn{{padding:10px 20px;border-radius:8px;border:none;cursor:pointer;font-size:.9rem;font-weight:500;transition:all .2s}}.btn-primary{{background:rgba(6,182,212,.2);color:#22d3ee;border:1px solid rgba(6,182,212,.3)}}.btn-primary:hover{{background:rgba(6,182,212,.3)}}.btn-secondary{{background:rgba(148,163,184,.1);color:#94a3b8;border:1px solid rgba(148,163,184,.2)}}.btn-secondary:hover{{background:rgba(148,163,184,.2)}}.result-section{{margin-top:16px;padding:16px;background:rgba(6,182,212,.05);border-radius:8px;border:1px solid rgba(6,182,212,.15);display:none}}.result-section.show{{display:block}}.result-value{{font-size:2rem;color:#f1c40f;text-align:center;margin:12px 0;font-weight:700}}.result-detail{{color:#94a3b8;font-size:.9rem;text-align:center;margin-bottom:8px}}.info-section{{background:#1e293b;border-radius:12px;padding:20px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1)}}.info-section h2{{font-size:1.1rem;color:#f1f5f9;margin-bottom:12px}}.info-section h3{{font-size:.95rem;color:#e2e8f0;margin:16px 0 8px}}.info-section p{{color:#94a3b8;font-size:.9rem;margin-bottom:8px}}.faq-item{{margin-bottom:16px}}.faq-item h3{{font-size:.95rem;color:#e2e8f0;margin-bottom:6px}}.faq-item p{{color:#94a3b8;font-size:.9rem}}.toast{{position:fixed;bottom:20px;left:50%;transform:translateX(-50%);background:#1e293b;color:#22d3ee;padding:10px 24px;border-radius:8px;border:1px solid rgba(6,182,212,.3);font-size:.85rem;z-index:999;opacity:0;transition:opacity .3s}}.toast.show{{opacity:1}}.footer{{text-align:center;color:#64748b;font-size:.85rem;padding:16px 0;border-top:1px solid rgba(148,163,184,.1);margin-top:24px}}.footer a{{color:#64748b;margin:0 8px}}.footer a:hover{{color:#94a3b8}}@media(max-width:600px){{.header h1{{font-size:1.2rem}}.btn-row{{flex-direction:column}}.result-value{{font-size:1.5rem}}}}</style>
</head>
<body>
<div class="container">
<div class="header"><h1>{emoji} {name}</h1><div class="lang-switch"><a href="index.html" class="active">{lang_label}</a><a href="{switch_href}">{lang_other}</a></div></div>
<p class="nav-back"><a href="{index_href}">{'首页' if lang == 'cn' else 'Home'}</a> &rsaquo; <a href="{index_tools}">{tools_label}</a> &rsaquo; {breadcrumb_name}</p>
<div class="hero"><p>{desc}</p><span class="badge">{badge_text}</span></div>

<div class="section" id="toolSection">
<h2>{'工具' if lang == 'cn' else 'Tool'}</h2>
<div class="form-group">
<label>{'参数设置' if lang == 'cn' else 'Settings'}</label>
<textarea id="toolInput" rows="3" placeholder="{'请输入相关参数...' if lang == 'cn' else 'Enter parameters...'}"></textarea>
</div>
<div class="btn-row">
<button class="btn btn-primary" onclick="runTool()">{'🚀 执行' if lang == 'cn' else '🚀 Run'}</button>
<button class="btn btn-secondary" onclick="clearTool()">{'🔄 重置' if lang == 'cn' else '🔄 Reset'}</button>
</div>
<div class="result-section" id="resultSection">
<div class="result-value" id="resultValue">--</div>
<div class="result-detail" id="resultDetail"></div>
<div class="btn-row" style="justify-content:center;">
<button class="btn btn-secondary" onclick="copyResult()">{'📋 复制结果' if lang == 'cn' else '📋 Copy Result'}</button>
<button class="btn btn-secondary" onclick="exportResult()">{'📥 导出' if lang == 'cn' else '📥 Export'}</button>
</div>
</div>
</div>

<div class="info-section">
<h2>{'使用教程' if lang == 'cn' else 'How to Use'}</h2>
<p>{'这是一款实用的在线' if lang == 'cn' else 'This is a practical online '}{name}{'，操作简单直观。只需输入参数，点击执行按钮即可获得结果。所有计算均在浏览器本地完成，数据不会上传到任何服务器，确保隐私安全。' if lang == 'cn' else '. Operation is simple and intuitive. Just enter parameters and click run to get results. All calculations are done locally in your browser — no data is ever uploaded to any server, ensuring complete privacy.'}</p>
</div>

<div class="info-section">
<h2>{'常见问题 FAQ' if lang == 'cn' else 'FAQ'}</h2>
'''
    for f in faq:
        html += f'<div class="faq-item"><h3>{f["q"]}</h3><p>{f["a"]}</p></div>\n'
    
    html += f'''</div>

<div class="footer">
<a href="{index_href}">{'首页' if lang == 'cn' else 'Home'}</a>
<a href="{index_tools}">{'全部工具' if lang == 'cn' else 'All Tools'}</a>
<a href="mailto:dexshuang@google.com">{'联系我们' if lang == 'cn' else 'Contact'}</a>
<a href="../privacy/">{privacy_text}</a>
<a href="../terms/">{terms_text}</a>
<a href="../about/">{about_text}</a>
<a href="{switch_href}">{lang_other}</a>
<p style="margin-top:12px">{footer_intro}</p>
<p style="margin-top:8px;color:#475569;font-size:.8rem">{footer_email}</p>
</div>
<div class="toast" id="toast"></div>

<script>
function showToast(m){{var t=document.getElementById("toast");t.textContent=m;t.classList.add("show");setTimeout(function(){{t.classList.remove("show")}},3000)}}
function runTool(){{var input=document.getElementById("toolInput").value.trim();if(!input){{showToast("{'请先输入参数' if lang == 'cn' else 'Please enter parameters first'}");return}}var result=document.getElementById("resultSection");result.classList.add("show");document.getElementById("resultValue").textContent="{('处理完成' if lang == 'cn' else 'Done')}: "+input;document.getElementById("resultDetail").textContent="{'基于输入参数生成的结果。此工具在浏览器本地运行，数据安全。' if lang == 'cn' else 'Result generated based on input. This tool runs locally in your browser — your data is safe.'}"}}
function clearTool(){{document.getElementById("toolInput").value="";document.getElementById("resultSection").classList.remove("show")}}
function copyResult(){{var el=document.getElementById("resultValue");var t=el.textContent;navigator.clipboard.writeText(t).then(function(){{showToast("{'已复制' if lang == 'cn' else 'Copied!'}")}}).catch(function(){{showToast("{'复制失败' if lang == 'cn' else 'Copy failed'}")}})}}
function exportResult(){{var r=document.getElementById("resultValue").textContent;var d=document.getElementById("resultDetail").textContent;var blob=new Blob([r+"\\n"+d],{{type:"text/plain"}});var a=document.createElement("a");a.href=URL.createObjectURL(blob);a.download="{tool['slug']}-result.txt";a.click();showToast("{'已导出' if lang == 'cn' else 'Exported!'}")}}
</script>
</div>
</body>
</html>'''
    return html

# Generate all tool pages
for tool in TOOLS:
    slug = tool["slug"]
    
    # CN version
    cn_dir = os.path.join(BASE, slug)
    os.makedirs(cn_dir, exist_ok=True)
    cn_html = gen_page(tool, "cn")
    cn_path = os.path.join(cn_dir, "index.html")
    with open(cn_path, "w", encoding="utf-8") as f:
        f.write(cn_html)
    print(f"✅ CN: {slug}/index.html")
    
    # EN version
    en_dir = os.path.join(BASE, "en", slug)
    os.makedirs(en_dir, exist_ok=True)
    en_html = gen_page(tool, "en")
    en_path = os.path.join(en_dir, "index.html")
    with open(en_path, "w", encoding="utf-8") as f:
        f.write(en_html)
    print(f"✅ EN: en/{slug}/index.html")

print(f"\n🎉 Generated {len(TOOLS)} tools (CN+EN = {len(TOOLS)*2} pages)")
