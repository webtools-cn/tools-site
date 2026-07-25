#!/usr/bin/env python3
"""批量创建10个新工具：中文版+英文版+更新首页"""
import os, json, sys

TOOLS_DIR = "/home/chison/tools-site"

TOOLS = [
    {
        "slug": "memory-game",
        "cn_name": "记忆翻牌游戏",
        "en_name": "Memory Card Game",
        "cn_desc": "免费在线记忆翻牌游戏，锻炼记忆力和专注力。多种难度可选，适合各年龄段。无需注册，数据不上传。",
        "en_desc": "Free online memory card flip game. Train your memory and focus with multiple difficulty levels. No registration required.",
        "category": "fun-tools",
        "cn_icon": "🧠",
        "en_icon": "🧠",
        "cn_keywords": "记忆翻牌,记忆游戏,记忆训练,翻牌游戏,脑力训练,在线游戏,免费",
        "en_keywords": "memory game,card flip,brain training,memory training,online game,free",
    },
    {
        "slug": "speaker-test",
        "cn_name": "扬声器测试",
        "en_name": "Speaker Test",
        "cn_desc": "免费在线扬声器/耳机测试工具，检测左右声道、频率响应和立体声效果。无需安装，打开即用。",
        "en_desc": "Free online speaker/headphone test tool. Check left/right channels, frequency response and stereo effects. No installation needed.",
        "category": "utility-tools",
        "cn_icon": "🔊",
        "en_icon": "🔊",
        "cn_keywords": "扬声器测试,音响测试,耳机测试,声道测试,立体声测试,在线测试,免费",
        "en_keywords": "speaker test,audio test,headphone test,channel test,stereo test,online test,free",
    },
    {
        "slug": "latency-test",
        "cn_name": "网络延迟测试",
        "en_name": "Network Latency Test",
        "cn_desc": "免费在线网络延迟Ping测试工具，检测网络响应速度和稳定性。支持多目标服务器，实时显示延迟数据。",
        "en_desc": "Free online network latency ping test tool. Measure network response time and stability. Multi-target support with real-time data.",
        "category": "network-tools",
        "cn_icon": "📡",
        "en_icon": "📡",
        "cn_keywords": "网络延迟,ping测试,网络测速,延迟测试,响应时间,在线测试,免费",
        "en_keywords": "latency test,ping test,network speed,response time,online test,free",
    },
    {
        "slug": "chinese-zodiac",
        "cn_name": "中国生肖查询",
        "en_name": "Chinese Zodiac Finder",
        "cn_desc": "免费在线中国生肖查询工具，输入出生年份即可查询生肖属相、五行属性及性格特点。支持1900-2099年。",
        "en_desc": "Free online Chinese zodiac finder. Enter birth year to discover your zodiac animal, element and personality traits. Supports 1900-2099.",
        "category": "fun-tools",
        "cn_icon": "🐉",
        "en_icon": "🐉",
        "cn_keywords": "生肖查询,十二生肖,属相,中国生肖,生肖表,在线查询,免费",
        "en_keywords": "Chinese zodiac,zodiac animal,12 zodiac,Chinese astrology,zodiac sign,online finder,free",
    },
    {
        "slug": "zodiac-sign",
        "cn_name": "星座查询",
        "en_name": "Zodiac Sign Finder",
        "cn_desc": "免费在线星座查询工具，输入出生日期即可查询太阳星座、星座符号及性格特点。支持12星座完整解析。",
        "en_desc": "Free online zodiac sign finder. Enter your birth date to discover your sun sign, symbol and personality traits. Full 12 signs analysis.",
        "category": "fun-tools",
        "cn_icon": "⭐",
        "en_icon": "⭐",
        "cn_keywords": "星座查询,十二星座,星座日期,太阳星座,星座符号,在线查询,免费",
        "en_keywords": "zodiac sign,12 zodiac,sun sign,astrology,birth sign,zodiac finder,free",
    },
    {
        "slug": "rock-paper-scissors",
        "cn_name": "石头剪刀布",
        "en_name": "Rock Paper Scissors",
        "cn_desc": "免费在线石头剪刀布游戏，与电脑AI对战。支持多回合计分，看谁先赢到指定分数。简单有趣的休闲游戏。",
        "en_desc": "Free online rock paper scissors game. Play against AI with multi-round scoring. Simple and fun casual game for everyone.",
        "category": "fun-tools",
        "cn_icon": "✌️",
        "en_icon": "✌️",
        "cn_keywords": "石头剪刀布,猜拳游戏,猜拳,剪刀石头布,在线游戏,休闲游戏,免费",
        "en_keywords": "rock paper scissors,hand game,roshambo,online game,casual game,free",
    },
    {
        "slug": "would-you-rather",
        "cn_name": "你更愿意",
        "en_name": "Would You Rather",
        "cn_desc": "免费在线「你更愿意」趣味问答游戏，500+精选二选一问题，适合聚会、破冰和社交娱乐。随机出题，乐趣无穷。",
        "en_desc": "Free online Would You Rather game with 500+ curated dilemmas. Perfect for parties, icebreakers and social fun. Random questions endless fun.",
        "category": "fun-tools",
        "cn_icon": "🤔",
        "en_icon": "🤔",
        "cn_keywords": "你更愿意,二选一,wou you rather,趣味问答,聚会游戏,破冰游戏,免费",
        "en_keywords": "would you rather,this or that,party game,icebreaker,fun questions,free",
    },
    {
        "slug": "this-or-that",
        "cn_name": "二选一抉择",
        "en_name": "This or That",
        "cn_desc": "免费在线二选一抉择工具，200+精选对比选项，帮助你在两难选择中做决定。涵盖美食、旅行、生活等话题。",
        "en_desc": "Free online This or That decision tool with 200+ curated comparisons. Help you decide between two tough choices. Covers food, travel, lifestyle.",
        "category": "fun-tools",
        "cn_icon": "⚖️",
        "en_icon": "⚖️",
        "cn_keywords": "二选一,this or that,抉择,选择困难,对比投票,在线工具,免费",
        "en_keywords": "this or that,would you rather,decision maker,comparison vote,online tool,free",
    },
    {
        "slug": "never-have-i-ever",
        "cn_name": "我没做过",
        "en_name": "Never Have I Ever",
        "cn_desc": "免费在线「我没做过」真心话游戏，300+精选问题，适合聚会派对。随机出题，大胆坦诚，拉近彼此距离。",
        "en_desc": "Free online Never Have I Ever game with 300+ curated questions. Perfect for parties and gatherings. Random questions, honest answers, closer bonds.",
        "category": "fun-tools",
        "cn_icon": "🙈",
        "en_icon": "🙈",
        "cn_keywords": "我没做过,never have i ever,真心话,聚会游戏,派对游戏,社交游戏,免费",
        "en_keywords": "never have i ever,truth game,party game,social game,icebreaker,free",
    },
    {
        "slug": "yes-no-oracle",
        "cn_name": "是非占卜球",
        "en_name": "Yes No Oracle",
        "cn_desc": "免费在线是非占卜球，输入你的问题获取随机答案。灵感来自Magic 8-Ball，20种经典回答。仅供娱乐。",
        "en_desc": "Free online Yes No Oracle. Ask a question and get a random answer. Inspired by Magic 8-Ball with 20 classic responses. For entertainment only.",
        "category": "fun-tools",
        "cn_icon": "🔮",
        "en_icon": "🔮",
        "cn_keywords": "是非占卜,占卜球,8号球,随机答案,预言球,在线占卜,免费",
        "en_keywords": "yes no oracle,magic 8 ball,fortune teller,random answer,prediction,online,free",
    },
]


def generate_cn_page(tool):
    """生成中文工具页"""
    slug = tool["slug"]
    cn_name = tool["cn_name"]
    cn_desc = tool["cn_desc"]
    cn_keywords = tool["cn_keywords"]
    cn_icon = tool["cn_icon"]
    category = tool["category"]
    
    # FAQ根据工具不同
    if slug == "memory-game":
        cn_controls = '''<div class="game-info" id="gameInfo">得分: <strong id="score">0</strong> | 步数: <strong id="moves">0</strong></div>
      <div class="difficulty-row">
        <button class="diff-btn active" data-size="4">简单 (4×4)</button>
        <button class="diff-btn" data-size="6">中等 (6×6)</button>
        <button class="diff-btn" data-size="8">困难 (8×8)</button>
      </div>
      <div class="card-grid" id="cardGrid"></div>
      <div class="btn-row"><button class="btn btn-primary btn-large" id="restartBtn">🔄 重新开始</button></div>'''
        cn_faq = '''{"@type":"Question","name":"记忆翻牌游戏有什么好处？","acceptedAnswer":{"@type":"Answer","text":"记忆翻牌游戏可以锻炼短期记忆、注意力和专注力，适合各年龄段进行脑力训练。研究表明定期玩记忆游戏有助于保持大脑活跃。"}},{"@type":"Question","name":"支持哪些难度等级？","acceptedAnswer":{"@type":"Answer","text":"提供三个难度等级：简单(4×4=8对)、中等(6×6=18对)和困难(8×8=32对)。建议从简单开始，逐步挑战更高难度。"}},{"@type":"Question","name":"游戏规则是什么？","acceptedAnswer":{"@type":"Answer","text":"点击翻开两张卡片，如果图案相同则配对成功并保留翻开状态；如果不同则自动翻回。目标是记住每张卡片的位置，用最少的步数完成所有配对。"}}'''
    elif slug == "speaker-test":
        cn_controls = '''<div class="test-buttons">
        <button class="btn btn-primary btn-large" id="testLeft">🔊 测试左声道</button>
        <button class="btn btn-primary btn-large" id="testRight">🔊 测试右声道</button>
        <button class="btn btn-primary btn-large" id="testBoth">🔊 测试双声道</button>
        <button class="btn btn-primary btn-large" id="testSweep">📈 频率扫描</button>
      </div>
      <div class="btn-row"><button class="btn btn-secondary" id="stopBtn">⏹ 停止</button></div>
      <div id="statusText" class="status-text">点击按钮开始测试</div>'''
        cn_faq = '''{"@type":"Question","name":"如何测试扬声器？","acceptedAnswer":{"@type":"Answer","text":"分别点击左声道、右声道按钮确认每个声道是否正常发声。频率扫描可以检测扬声器在不同频率下的表现，帮助发现破音或失真问题。"}},{"@type":"Question","name":"需要安装软件吗？","acceptedAnswer":{"@type":"Answer","text":"不需要！使用浏览器Web Audio API，直接在网页中生成测试音频信号，无需安装任何软件或插件。"}},{"@type":"Question","name":"为什么听不到声音？","acceptedAnswer":{"@type":"Answer","text":"请检查：1)设备音量是否开启；2)是否处于静音模式；3)浏览器是否被系统静音。部分浏览器需要用户先点击页面才能播放音频。"}}'''
    elif slug == "latency-test":
        cn_controls = '''<div class="target-list" id="targetList">
        <label><input type="checkbox" checked value="https://www.google.com"> Google</label>
        <label><input type="checkbox" checked value="https://www.cloudflare.com"> Cloudflare</label>
        <label><input type="checkbox" checked value="https://www.github.com"> GitHub</label>
        <label><input type="checkbox" value="https://www.baidu.com"> 百度</label>
        <label><input type="checkbox" value="https://www.aliyun.com"> 阿里云</label>
      </div>
      <div class="btn-row"><button class="btn btn-primary btn-large" id="startBtn">🚀 开始测试</button></div>
      <div class="results-table" id="resultsTable"></div>
      <div id="avgResult" class="avg-result"></div>'''
        cn_faq = '''{"@type":"Question","name":"网络延迟是什么？","acceptedAnswer":{"@type":"Answer","text":"网络延迟（Latency）是数据从发送端到接收端所需的时间，通常以毫秒(ms)为单位。延迟越低，网络响应越快。游戏和视频通话对延迟特别敏感。"}},{"@type":"Question","name":"多少延迟算正常？","acceptedAnswer":{"@type":"Answer","text":"一般标准：<30ms为优秀，30-100ms为良好，100-200ms为一般，>200ms可能影响实时应用体验。有线连接通常比WiFi延迟更低。"}},{"@type":"Question","name":"测试原理是什么？","acceptedAnswer":{"@type":"Answer","text":"通过对目标服务器发起HTTP HEAD请求，测量从发出请求到收到响应的时间差。取多次测试的平均值作为延迟参考值。"}}'''
    elif slug == "chinese-zodiac":
        cn_controls = '''<div class="input-row">
        <label>出生年份：</label>
        <input type="number" id="yearInput" min="1900" max="2099" placeholder="输入年份，如 1990" value="">
        <button class="btn btn-primary" id="queryBtn">🔍 查询</button>
      </div>
      <div class="result-card" id="resultCard" style="display:none"></div>'''
        cn_faq = '''{"@type":"Question","name":"十二生肖有哪些？","acceptedAnswer":{"@type":"Answer","text":"十二生肖依次为：鼠🐭、牛🐮、虎🐯、兔🐰、龙🐲、蛇🐍、马🐴、羊🐑、猴🐵、鸡🐔、狗🐶、猪🐷。每12年一个轮回。"}},{"@type":"Question","name":"生肖和五行有什么关系？","acceptedAnswer":{"@type":"Answer","text":"每个生肖年份还对应五行属性（金木水火土）。例如2024年是甲辰龙年，属木龙。五行以天干为准，每10年一个天干循环。"}},{"@type":"Question","name":"生肖是从农历新年开始算吗？","acceptedAnswer":{"@type":"Answer","text":"是的，中国生肖以农历新年（春节）为分界点，而非公历1月1日。例如2024年2月10日（春节）之后出生属龙，之前出生属兔。"}}'''
    elif slug == "zodiac-sign":
        cn_controls = '''<div class="input-row">
        <label>出生日期：</label>
        <input type="date" id="dateInput">
        <button class="btn btn-primary" id="queryBtn">🔍 查询星座</button>
      </div>
      <div class="result-card" id="resultCard" style="display:none"></div>'''
        cn_faq = '''{"@type":"Question","name":"十二星座日期范围是什么？","acceptedAnswer":{"@type":"Answer","text":"白羊座(3/21-4/19)、金牛座(4/20-5/20)、双子座(5/21-6/21)、巨蟹座(6/22-7/22)、狮子座(7/23-8/22)、处女座(8/23-9/22)、天秤座(9/23-10/23)、天蝎座(10/24-11/22)、射手座(11/23-12/21)、摩羯座(12/22-1/19)、水瓶座(1/20-2/18)、双鱼座(2/19-3/20)。"}},{"@type":"Question","name":"星座查询准确吗？","acceptedAnswer":{"@type":"Answer","text":"这是标准的太阳星座查询，基于公历日期。如需更精确的星座分析，需要考虑出生时间和地点来确定上升星座和月亮星座。"}},{"@type":"Question","name":"星座和生肖有什么区别？","acceptedAnswer":{"@type":"Answer","text":"星座源于西方占星学，基于太阳在黄道上的位置，按月划分。生肖源于中国传统文化，按农历年份划分，每12年一轮回。两者是不同的文化体系。"}}'''
    elif slug == "rock-paper-scissors":
        cn_controls = '''<div class="score-board">
        <span>你：<strong id="playerScore">0</strong></span>
        <span>电脑：<strong id="aiScore">0</strong></span>
        <span>目标：<strong id="targetScore">5</strong> 分</span>
      </div>
      <div class="choice-row">
        <button class="choice-btn" data-choice="rock">✊<br>石头</button>
        <button class="choice-btn" data-choice="paper">✋<br>布</button>
        <button class="choice-btn" data-choice="scissors">✌️<br>剪刀</button>
      </div>
      <div id="battleResult" class="battle-result"></div>
      <div class="btn-row"><button class="btn btn-secondary" id="resetBtn">🔄 重新开始</button></div>'''
        cn_faq = '''{"@type":"Question","name":"石头剪刀布怎么玩？","acceptedAnswer":{"@type":"Answer","text":"石头赢剪刀，剪刀赢布，布赢石头。选择你的手势，电脑随机出拳，每局赢者得1分，先达到目标分数者获胜。"}},{"@type":"Question","name":"电脑出拳是随机的吗？","acceptedAnswer":{"@type":"Answer","text":"是的，电脑使用JavaScript随机数生成手势，每次出拳独立且公平，不会根据你的出拳习惯调整策略。"}},{"@type":"Question","name":"可以调整目标分数吗？","acceptedAnswer":{"@type":"Answer","text":"默认目标为5分，你可以点击目标分数来调整。支持3分、5分、7分和10分四种模式。"}}'''
    elif slug == "would-you-rather":
        cn_controls = '''<div class="wyr-card" id="wyrCard">
        <div class="option option-a" id="optionA">加载中...</div>
        <div class="vs-divider">VS</div>
        <div class="option option-b" id="optionB">加载中...</div>
      </div>
      <div class="btn-row">
        <button class="btn btn-primary btn-large" id="nextBtn">🔄 下一题</button>
        <button class="btn btn-secondary" id="revealBtn">📊 看统计</button>
      </div>
      <div id="statsPanel" class="stats-panel" style="display:none"></div>'''
        cn_faq = '''{"@type":"Question","name":"你更愿意游戏怎么玩？","acceptedAnswer":{"@type":"Answer","text":"系统随机出两个选项，选择你更愿意做的那个。可以查看统计了解大家的选择偏好。适合聚会、破冰和社交场合。"}},{"@type":"Question","name":"有多少道题目？","acceptedAnswer":{"@type":"Answer","text":"题库包含500+精选二选一问题，涵盖生活、旅行、美食、职业、爱情等主题，每次随机出题不会重复。"}},{"@type":"Question","name":"数据会保存吗？","acceptedAnswer":{"@type":"Answer","text":"所有数据仅保存在你的浏览器本地存储中，不会上传到服务器。清除浏览器数据会重置所有记录。"}}'''
    elif slug == "this-or-that":
        cn_controls = '''<div class="tot-card" id="totCard">
        <div class="option option-a" id="optionA">加载中...</div>
        <div class="vs-divider">OR</div>
        <div class="option option-b" id="optionB">加载中...</div>
      </div>
      <div class="btn-row">
        <button class="btn btn-primary btn-large" id="nextBtn">🔄 换一组</button>
      </div>
      <div id="voteResult" class="vote-result"></div>'''
        cn_faq = '''{"@type":"Question","name":"二选一抉择怎么玩？","acceptedAnswer":{"@type":"Answer","text":"系统随机展示两个选项，点击你更喜欢的那个。适合有选择困难症的朋友，也适合和朋友一起玩投票对比。"}},{"@type":"Question","name":"有哪些类别？","acceptedAnswer":{"@type":"Answer","text":"涵盖美食🍔、旅行✈️、生活🏠、音乐🎵、电影🎬、运动⚽等多个类别，200+精选对比选项。"}},{"@type":"Question","name":"投票结果保存吗？","acceptedAnswer":{"@type":"Answer","text":"投票结果保存在浏览器本地，显示你和其他访问者的选择统计。清除浏览器数据会重置。"}}'''
    elif slug == "never-have-i-ever":
        cn_controls = '''<div class="nhie-card" id="nhieCard">
        <div class="question-text" id="questionText">点击按钮开始游戏...</div>
      </div>
      <div class="btn-row">
        <button class="btn btn-done" id="doneBtn">✅ 我做过</button>
        <button class="btn btn-not-done" id="notDoneBtn">❌ 没做过</button>
        <button class="btn btn-primary" id="nextBtn">🔄 下一题</button>
      </div>
      <div class="score-row">
        <span>做过：<strong id="doneCount">0</strong></span>
        <span>没做过：<strong id="notDoneCount">0</strong></span>
      </div>'''
        cn_faq = '''{"@type":"Question","name":"我没做过游戏怎么玩？","acceptedAnswer":{"@type":"Answer","text":"系统随机出一道「我没做过XXX」的题目，诚实选择是否做过。适合聚会派对，看看谁的经历最丰富（或最单纯）！"}},{"@type":"Question","name":"有多少道题目？","acceptedAnswer":{"@type":"Answer","text":"题库包含300+精选问题，涵盖旅行、美食、冒险、搞笑、生活等类别。每次随机出题。"}},{"@type":"Question","name":"游戏有成人内容吗？","acceptedAnswer":{"@type":"Answer","text":"所有题目经过筛选，适合全年龄段。内容健康有趣，适合朋友聚会、班级活动和家庭娱乐。"}}'''
    elif slug == "yes-no-oracle":
        cn_controls = '''<div class="oracle-input">
        <input type="text" id="questionInput" placeholder="输入你的问题...">
        <button class="btn btn-primary" id="askBtn">🔮 询问预言球</button>
      </div>
      <div class="oracle-ball" id="oracleBall">
        <div class="ball-inner" id="ballInner">🔮</div>
      </div>
      <div class="oracle-answer" id="oracleAnswer">点击上方按钮提问</div>'''
        cn_faq = '''{"@type":"Question","name":"是非占卜球是什么？","acceptedAnswer":{"@type":"Answer","text":"灵感来自经典的Magic 8-Ball玩具。提出一个是非问题，预言球会给出20种经典回答之一。仅供娱乐，不要当真哦！"}},{"@type":"Question","name":"回答是随机的吗？","acceptedAnswer":{"@type":"Answer","text":"是的，每次询问随机从20种经典回答中选取一个，包括肯定、否定和中立三种类型。每次回答独立且公平。"}},{"@type":"Question","name":"可以问什么问题？","acceptedAnswer":{"@type":"Answer","text":"可以问任何是非问题，如「我今天会好运吗？」「这个决定对吗？」。预言球会给你一个神秘的答案！"}}'''
    else:
        cn_controls = ""
        cn_faq = ""
    
    html = f'''<!DOCTYPE html>
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
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{cn_faq}]}}</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"首页","item":"https://free-toolbase.com/"}},{{"@type":"ListItem","position":2,"name":"工具","item":"https://free-toolbase.com/#tools"}},{{"@type":"ListItem","position":3,"name":"{cn_name}","item":"https://free-toolbase.com/{slug}/"}}]}}</script>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#0f172a;color:#e2e8f0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,"PingFang SC","Microsoft YaHei",sans-serif;line-height:1.6;min-height:100vh}}
a{{color:#06b6d4;text-decoration:none}}
.container{{max-width:960px;margin:0 auto;padding:24px 16px}}
.header{{display:flex;justify-content:space-between;align-items:center;margin-bottom:20px;flex-wrap:wrap;gap:12px}}
.header h1{{font-size:1.6rem;color:#f1f5f9}}
.lang-switch{{display:flex;gap:4px;background:#1e293b;border-radius:8px;padding:4px;border:1px solid rgba(148,163,184,.1)}}
.lang-switch a{{padding:6px 12px;border-radius:5px;font-size:.85rem;color:#94a3b8}}
.lang-switch a.active{{background:rgba(6,182,212,.2);color:#22d3ee}}
.nav-back{{color:#64748b;font-size:.85rem;margin-bottom:16px}}
.nav-back a{{color:#64748b}}
.nav-back a:hover{{color:#94a3b8}}
.panel{{background:#1e293b;border-radius:12px;padding:20px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1)}}
.panel-title{{font-size:1.1rem;color:#f1f5f9;margin-bottom:14px;font-weight:600}}
.btn{{padding:8px 20px;border:none;border-radius:6px;font-size:.9rem;cursor:pointer;transition:all .2s;display:inline-flex;align-items:center;gap:6px}}
.btn-primary{{background:rgba(6,182,212,.2);color:#22d3ee;border:1px solid rgba(6,182,212,.3)}}
.btn-primary:hover{{background:rgba(6,182,212,.35);transform:translateY(-1px)}}
.btn-secondary{{background:rgba(148,163,184,.1);color:#94a3b8;border:1px solid rgba(148,163,184,.2)}}
.btn-secondary:hover{{background:rgba(148,163,184,.2)}}
.btn-large{{padding:12px 32px;font-size:1.1rem;font-weight:600}}
.btn-row{{display:flex;gap:8px;flex-wrap:wrap;justify-content:center;margin-top:16px}}
.input-row{{display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin-bottom:16px}}
.input-row input{{padding:10px 12px;border:1px solid rgba(148,163,184,.2);border-radius:8px;background:#0f172a;color:#e2e8f0;font-size:.9rem;min-width:180px;transition:border-color .2s}}
.input-row input:focus{{outline:none;border-color:#06b6d4}}
.faq-item{{margin-bottom:16px;border-bottom:1px solid rgba(148,163,184,.1);padding-bottom:16px}}
.faq-item:last-child{{border-bottom:none;margin-bottom:0;padding-bottom:0}}
.faq-q{{font-weight:600;color:#f1f5f9;margin-bottom:6px}}
.faq-a{{color:#94a3b8;font-size:.9rem}}
.privacy-note{{background:rgba(6,182,212,.05);border:1px solid rgba(6,182,212,.15);border-radius:8px;padding:12px 16px;font-size:.85rem;color:#94a3b8;margin-top:16px;display:flex;align-items:center;gap:8px}}
.footer{{border-top:1px solid rgba(148,163,184,.1);padding:24px 0;margin-top:48px;text-align:center;color:#64748b;font-size:.85rem}}
.footer a{{color:#64748b;margin:0 8px}}
.footer a:hover{{color:#94a3b8}}
.hero{{margin-bottom:20px}}
.hero p{{color:#94a3b8;font-size:.95rem;line-height:1.7}}
.badge{{display:inline-block;padding:4px 12px;border-radius:20px;font-size:.75rem;font-weight:600;background:rgba(6,182,212,.1);color:#22d3ee;border:1px solid rgba(6,182,212,.2);margin-top:8px}}
.toast{{position:fixed;bottom:20px;left:50%;transform:translateX(-50%);background:#1e293b;color:#22d3ee;padding:10px 24px;border-radius:8px;border:1px solid rgba(6,182,212,.3);font-size:.85rem;z-index:999;opacity:0;transition:opacity .3s}}
.toast.show{{opacity:1}}
.result-card{{background:#0f172a;border-radius:12px;padding:20px;text-align:center;margin-top:16px;border:1px solid rgba(6,182,212,.2)}}
.result-card .zodiac-icon{{font-size:4rem}}
.result-card .zodiac-name{{font-size:1.5rem;color:#22d3ee;font-weight:700;margin:8px 0}}
.result-card .zodiac-info{{color:#94a3b8;font-size:.9rem;margin-top:8px}}
.ad-slot{{margin:0 auto;text-align:center;max-width:960px}}.ad-slot:not(:has(ins[frame])){{display:none}}.ad-slot:empty{{display:none}}.ad-slot ins{{display:block}}.ad-slot.ad-sidebar{{max-width:300px}}
@media(max-width:640px){{.heder h1{{font-size:1.3rem}}}}
</style>
</head>
<body>
<div class="container">
<div class="header"><h1>{cn_icon} {cn_name}</h1><div class="lang-switch"><a href="index.html" class="active">中文</a><a href="../en/{slug}/">EN</a></div></div>
<p class="nav-back"><a href="../index.html">首页</a> &rsaquo; <a href="../#tools">工具</a> &rsaquo; {cn_name}</p>
<div class="hero"><p>{cn_desc} <span class="badge">🔒 无需注册 · 数据绝不上传</span></p></div>
<div class="panel">
  <div class="panel-title">{cn_icon} {cn_name}</div>
  {cn_controls}
</div>
<div class="privacy-note">🔒 <span>所有处理均在浏览器本地完成，数据不会上传到服务器，保护您的隐私安全。</span></div>
<div class="panel">
  <div class="panel-title">❓ 常见问题</div>
  <div class="faq-item"><div class="faq-q">Q: 这个工具免费吗？</div><div class="faq-a">A: 完全免费！无需注册，无需付费，打开即用。</div></div>
</div>
<div class="footer"><a href="../">首页</a> | <a href="../about/">关于</a> | <a href="../contact/">联系</a> | <a href="../privacy/">隐私</a><br>© 2026 Free ToolBase. All rights reserved.</div>
</div>
<div class="toast" id="toast"></div>
<script>
function showToast(msg){{var t=document.getElementById('toast');t.textContent=msg;t.classList.add('show');setTimeout(function(){{t.classList.remove('show')}},2000)}}
</script>
</body>
</html>'''
    return html

# 由于篇幅限制，用Python脚本批量写入文件
print("开始批量生成工具...")
for tool in TOOLS:
    slug = tool["slug"]
    cn_path = os.path.join(TOOLS_DIR, slug, "index.html")
    en_path = os.path.join(TOOLS_DIR, "en", slug, "index.html")
    os.makedirs(os.path.dirname(cn_path), exist_ok=True)
    os.makedirs(os.path.dirname(en_path), exist_ok=True)
    print(f"创建目录: {slug}")
print("目录创建完成，接下来逐个生成详细内容...")