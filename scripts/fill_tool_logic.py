#!/usr/bin/env python3
"""为5个新工具填充实际的交互功能"""
import os

BASE = os.path.expanduser("~/tools-site")

# ========= SPELL CHECKER =========
spell_js = """
(function() {
  'use strict';
  var commonWords = {
    'teh':'the', 'recieve':'receive', 'adress':'address', 'occured':'occurred',
    'untill':'until', 'tommorrow':'tomorrow', 'wich':'which', 'thier':'their',
    'alot':'a lot', 'definately':'definitely', 'seperate':'separate', 'goverment':'government',
    'occassion':'occasion', 'accomodate':'accommodate', 'neccessary':'necessary',
    'maintainance':'maintenance', 'reciept':'receipt', 'commitee':'committee',
    'embarass':'embarrass', 'concious':'conscious', 'independant':'independent',
    'begining':'beginning', 'wierd':'weird', 'buisness':'business',
    'calender':'calendar', 'cemetery':'cemetery', 'collegue':'colleague',
    'comittee':'committee', 'acheive':'achieve', 'arguement':'argument',
    'beleive':'believe', 'enviroment':'environment', 'experiance':'experience',
    'Febuary':'February', 'fourty':'forty', 'harrass':'harass',
    'immedately':'immediately', 'lisence':'license', 'neice':'niece',
    'occurence':'occurrence', 'pronounciation':'pronunciation', 'reccomend':'recommend',
    'relevent':'relevant', 'rythm':'rhythm', 'schedual':'schedule',
    'tendancy':'tendency', 'tommorow':'tomorrow', 'tounge':'tongue',
    'unfortunatly':'unfortunately', 'Wendesday':'Wednesday', 'writting':'writing'
  };
  var card = document.getElementById('app-card');
  card.innerHTML = '<h2>' + (document.documentElement.lang === 'zh-CN' ? '文本拼写检查' : 'Spell Check Text') + '</h2>' +
    '<textarea id="spellInput" rows="8" placeholder="' + (document.documentElement.lang === 'zh-CN' ? '输入或粘贴文本...' : 'Type or paste text here...') + '"></textarea>' +
    '<div style="margin-top:12px;display:flex;gap:8px;flex-wrap:wrap">' +
      '<button class="btn" id="checkBtn">' + (document.documentElement.lang === 'zh-CN' ? '🔍 检查拼写' : '🔍 Check Spelling') + '</button>' +
      '<button class="btn btn-secondary" id="clearBtn">' + (document.documentElement.lang === 'zh-CN' ? '清空' : 'Clear') + '</button>' +
      '<span id="resultBadge" style="margin-left:auto;font-size:.85rem;padding:6px 12px;border-radius:20px;display:none"></span>' +
    '</div>' +
    '<div id="spellOutput" class="output" style="line-height:2;min-height:80px"></div>';
  
  var input = document.getElementById('spellInput');
  var output = document.getElementById('spellOutput');
  var badge = document.getElementById('resultBadge');
  
  function checkSpelling() {
    var text = input.value.trim();
    if (!text) { output.innerHTML = '<span style="color:#94a3b8">' + (document.documentElement.lang === 'zh-CN' ? '请先输入文本' : 'Please enter some text first') + '</span>'; badge.style.display='none'; return; }
    var words = text.split(/(\\s+)/);
    var errors = 0;
    var result = words.map(function(w) {
      var lower = w.toLowerCase();
      if (commonWords[lower]) {
        errors++;
        return '<span style="background:#fee2e2;color:#dc2626;padding:2px 4px;border-radius:4px;cursor:pointer;text-decoration:underline wavy #ef4444" title="' + (document.documentElement.lang === 'zh-CN' ? '建议: ' : 'Suggestion: ') + commonWords[lower] + '" onclick="this.outerHTML=\\'' + commonWords[lower] + '\\'">' + w + '</span>';
      }
      return w;
    }).join('');
    output.innerHTML = result;
    if (errors === 0) {
      badge.style.display = 'inline-block';
      badge.style.background = '#dcfce7'; badge.style.color = '#166534';
      badge.textContent = document.documentElement.lang === 'zh-CN' ? '✅ 未发现拼写错误' : '✅ No spelling errors found';
    } else {
      badge.style.display = 'inline-block';
      badge.style.background = '#fee2e2'; badge.style.color = '#dc2626';
      badge.textContent = (document.documentElement.lang === 'zh-CN' ? '⚠️ 发现 ' : '⚠️ Found ') + errors + (document.documentElement.lang === 'zh-CN' ? ' 个拼写错误' : ' spelling error(s)');
    }
  }
  
  document.getElementById('checkBtn').onclick = checkSpelling;
  document.getElementById('clearBtn').onclick = function() { input.value = ''; output.innerHTML = ''; badge.style.display = 'none'; };
})();
"""

# ========= ACRONYM FINDER =========
acronym_js = """
(function() {
  'use strict';
  var acronyms = {
    'AI':'Artificial Intelligence|人工智能',
    'API':'Application Programming Interface|应用程序接口',
    'NASA':'National Aeronautics and Space Administration|美国国家航空航天局',
    'SEO':'Search Engine Optimization|搜索引擎优化',
    'HTML':'HyperText Markup Language|超文本标记语言',
    'CSS':'Cascading Style Sheets|层叠样式表',
    'JS':'JavaScript|JavaScript脚本语言',
    'JSON':'JavaScript Object Notation|JavaScript对象表示法',
    'XML':'eXtensible Markup Language|可扩展标记语言',
    'SQL':'Structured Query Language|结构化查询语言',
    'HTTP':'HyperText Transfer Protocol|超文本传输协议',
    'HTTPS':'HyperText Transfer Protocol Secure|安全超文本传输协议',
    'FTP':'File Transfer Protocol|文件传输协议',
    'SSH':'Secure Shell|安全外壳协议',
    'DNS':'Domain Name System|域名系统',
    'URL':'Uniform Resource Locator|统一资源定位符',
    'IP':'Internet Protocol|互联网协议',
    'TCP':'Transmission Control Protocol|传输控制协议',
    'UDP':'User Datagram Protocol|用户数据报协议',
    'VPN':'Virtual Private Network|虚拟专用网络',
    'LAN':'Local Area Network|局域网',
    'WAN':'Wide Area Network|广域网',
    'RAM':'Random Access Memory|随机存取存储器',
    'ROM':'Read-Only Memory|只读存储器',
    'CPU':'Central Processing Unit|中央处理器',
    'GPU':'Graphics Processing Unit|图形处理器',
    'SSD':'Solid State Drive|固态硬盘',
    'HDD':'Hard Disk Drive|机械硬盘',
    'USB':'Universal Serial Bus|通用串行总线',
    'OS':'Operating System|操作系统',
    'BIOS':'Basic Input/Output System|基本输入输出系统',
    'GUI':'Graphical User Interface|图形用户界面',
    'CLI':'Command Line Interface|命令行界面',
    'IDE':'Integrated Development Environment|集成开发环境',
    'SDK':'Software Development Kit|软件开发工具包',
    'MVP':'Minimum Viable Product|最小可行产品',
    'KPI':'Key Performance Indicator|关键绩效指标',
    'ROI':'Return on Investment|投资回报率',
    'CEO':'Chief Executive Officer|首席执行官',
    'CTO':'Chief Technology Officer|首席技术官',
    'CFO':'Chief Financial Officer|首席财务官',
    'HR':'Human Resources|人力资源',
    'R&D':'Research and Development|研发',
    'B2B':'Business to Business|企业对企业',
    'B2C':'Business to Consumer|企业对消费者',
    'IPO':'Initial Public Offering|首次公开募股',
    'GDP':'Gross Domestic Product|国内生产总值',
    'IMHO':'In My Humble Opinion|依我拙见',
    'FYI':'For Your Information|供你参考',
    'ASAP':'As Soon As Possible|尽快',
    'FAQ':'Frequently Asked Questions|常见问题',
    'ETA':'Estimated Time of Arrival|预计到达时间',
    'DIY':'Do It Yourself|自己动手',
    'BRB':'Be Right Back|马上回来',
    'LOL':'Laughing Out Loud|大笑',
    'OMG':'Oh My God|我的天啊',
    'BTW':'By The Way|顺便说一句',
    'TLDR':'Too Long; Didn\\'t Read|太长不看',
    'AFAIK':'As Far As I Know|据我所知',
    'IIRC':'If I Recall Correctly|如果我没记错',
    'IMO':'In My Opinion|依我看',
    'FOMO':'Fear Of Missing Out|错失恐惧症',
    'YOLO':'You Only Live Once|你只活一次',
    'TGIF':'Thank God It\\'s Friday|感谢上帝今天是周五',
    'POV':'Point Of View|视角',
    'NSFW':'Not Safe For Work|工作场所不宜',
    'TBA':'To Be Announced|待公布',
    'TBD':'To Be Determined|待定',
    'RSVP':'Répondez S\\'il Vous Plaît|请回复',
    'PS':'Post Scriptum|附言',
    'RIP':'Rest In Peace|安息',
    'AKA':'Also Known As|也被称为',
    'ETA':'Estimated Time of Arrival|预计到达时间',
    'GMT':'Greenwich Mean Time|格林尼治标准时间',
    'EST':'Eastern Standard Time|东部标准时间',
    'PST':'Pacific Standard Time|太平洋标准时间',
    'AM':'Ante Meridiem|上午',
    'PM':'Post Meridiem|下午',
    'BC':'Before Christ|公元前',
    'AD':'Anno Domini|公元',
    'CV':'Curriculum Vitae|简历',
    'ISBN':'International Standard Book Number|国际标准书号',
    'DOI':'Digital Object Identifier|数字对象标识符',
    'OCR':'Optical Character Recognition|光学字符识别',
    'NFC':'Near Field Communication|近场通信',
    'RFID':'Radio Frequency Identification|射频识别',
    'IoT':'Internet of Things|物联网',
    'AR':'Augmented Reality|增强现实',
    'VR':'Virtual Reality|虚拟现实',
    'ML':'Machine Learning|机器学习',
    'NLP':'Natural Language Processing|自然语言处理',
    'AGI':'Artificial General Intelligence|通用人工智能'
  };
  var isCN = document.documentElement.lang === 'zh-CN';
  var card = document.getElementById('app-card');
  card.innerHTML = '<h2>' + (isCN ? '缩写含义查询' : 'Acronym Lookup') + '</h2>' +
    '<div style="display:flex;gap:8px;margin-bottom:12px">' +
      '<input type="text" id="acronymInput" placeholder="' + (isCN ? '输入缩写，如 AI、NASA、SEO...' : 'Enter acronym, e.g. AI, NASA, SEO...') + '" style="flex:1;font-size:1.1rem">' +
      '<button class="btn" id="searchBtn">' + (isCN ? '查询' : 'Search') + '</button>' +
    '</div>' +
    '<div id="acronymResult" class="output"></div>' +
    '<div style="margin-top:12px;font-size:.8rem;color:var(--text-secondary)">' +
      (isCN ? '收录 ' : 'Database: ') + Object.keys(acronyms).length + (isCN ? ' 个常见缩写' : ' common acronyms') +
      '<br>' + (isCN ? '热门：' : 'Popular: ') + Object.keys(acronyms).slice(0,12).join(', ') +
    '</div>';
  
  document.getElementById('searchBtn').onclick = function() {
    var q = document.getElementById('acronymInput').value.trim().toUpperCase();
    var r = document.getElementById('acronymResult');
    if (!q) { r.innerHTML = '<span style="color:#94a3b8">' + (isCN ? '请输入缩写' : 'Please enter an acronym') + '</span>'; return; }
    if (acronyms[q]) {
      var parts = acronyms[q].split('|');
      r.innerHTML = '<div style="font-size:1.5rem;font-weight:700;color:var(--primary);margin-bottom:8px">' + q + '</div>' +
        '<div><strong>' + (isCN ? '全称：' : 'Full Form: ') + '</strong>' + parts[0] + '</div>' +
        '<div><strong>' + (isCN ? '中文释义：' : 'Meaning: ') + '</strong>' + parts[1] + '</div>';
    } else {
      r.innerHTML = '<span style="color:#f59e0b">' + (isCN ? '未找到 "{}" 的释义，尝试其他缩写'.replace('{}', q) : 'No result found for "{}". Try another acronym.'.replace('{}', q)) + '</span>';
    }
  };
  document.getElementById('acronymInput').onkeydown = function(e) { if (e.key === 'Enter') document.getElementById('searchBtn').click(); };
})();
"""

# ========= RANDOM JOKE =========
joke_js = """
(function() {
  'use strict';
  var isCN = document.documentElement.lang === 'zh-CN';
  var jokesCN = [
    {text:'程序员最讨厌康熙的哪个儿子？——胤禩，因为他是八阿哥(bug)。',cat:'programming'},
    {text:'为什么程序员分不清万圣节和圣诞节？——因为 Oct 31 == Dec 25！',cat:'programming'},
    {text:'一个SQL语句走进酒吧，看到两张表，它问："我能join你们吗？"',cat:'programming'},
    {text:'程序员："我要重构整个代码库。"项目经理："需要多久？"程序员："两周。这是三年前说的。"',cat:'programming'},
    {text:'产品经理："这个需求很简单。"程序员卒。',cat:'programming'},
    {text:'世界上有10种人，一种懂二进制，一种不懂。',cat:'programming'},
    {text:'为什么水在地球待了几十亿年却没有过期？因为它是流水。',cat:'cold'},
    {text:'什么东西越洗越脏？——水。',cat:'cold'},
    {text:'小明：为什么吸血鬼从来不攻击程序员？老师：因为他们讨厌阳光。小明：那为什么他们也不攻击网络工程师？老师：……',cat:'cold'},
    {text:'从前有个馒头，走着走着饿了就把自己吃了。',cat:'cold'},
    {text:'什么东西经常来，却从来不会真正到达？——明天。',cat:'riddle'},
    {text:'什么东西越热越爱出来？——汗。',cat:'riddle'},
    {text:'什么动物最没有方向感？——麋鹿（迷路）。',cat:'riddle'},
    {text:'什么东西越大越看不见？——黑暗。',cat:'riddle'},
    {text:'面试官："你简历上写你抗压能力很强？"应聘者："是的，我能在一天内打完一整季《狂飙》。"',cat:'life'},
    {text:'当代年轻人的四大谎言：我没事、我没钱、我很好、我明天就开始减肥。',cat:'life'},
    {text:'领导：这个项目还有多久完成？我：快了。领导：快了是多久？我：就是快了啊。',cat:'life'},
    {text:'公司团建的本质：花公司的钱，占用员工的私人时间，做领导喜欢的事。',cat:'life'},
    {text:'世界上最遥远的距离，不是生与死，而是从周一到周五。',cat:'life'},
    {text:'每天早上叫醒我的不是梦想，是闹钟响了八百遍之后的求生欲。',cat:'life'}
  ];
  var jokesEN = [
    {text:'Why do programmers prefer dark mode? Because light attracts bugs!',cat:'programming'},
    {text:'A SQL query walks into a bar, sees two tables, and asks: "May I join you?"',cat:'programming'},
    {text:'There are 10 types of people in the world: those who understand binary, and those who don\\'t.',cat:'programming'},
    {text:'Why do Java developers wear glasses? Because they don\\'t C#.',cat:'programming'},
    {text:'Debugging: Being the detective in a crime movie where you are also the murderer.',cat:'programming'},
    {text:'Why did the scarecrow win an award? Because he was outstanding in his field!',cat:'dad'},
    {text:'What do you call a fake noodle? An impasta!',cat:'dad'},
    {text:'I told my wife she was drawing her eyebrows too high. She looked surprised.',cat:'dad'},
    {text:'Why don\\'t scientists trust atoms? Because they make up everything!',cat:'dad'},
    {text:'Parallel lines have so much in common. It\\'s a shame they\\'ll never meet.',cat:'dad'},
    {text:'I\\'m reading a book on anti-gravity. It\\'s impossible to put down!',cat:'dad'},
    {text:'What do you call cheese that isn\\'t yours? Nacho cheese!',cat:'dad'},
    {text:'Knock knock. Who\\'s there? Lettuce. Lettuce who? Lettuce in, it\\'s cold out here!',cat:'knock'},
    {text:'Knock knock. Who\\'s there? Cow says. Cow says who? No, cow says moo!',cat:'knock'},
    {text:'Knock knock. Who\\'s there? Boo. Boo who? Don\\'t cry, it\\'s just a joke!',cat:'knock'},
    {text:'Why did the chicken join a band? Because it had the drumsticks!',cat:'pun'},
    {text:'I used to be a baker, but I couldn\\'t make enough dough.',cat:'pun'},
    {text:'The past, present, and future walked into a bar. It was tense.',cat:'pun'},
    {text:'I\\'m on a seafood diet. I see food and I eat it.',cat:'pun'},
    {text:'What did the ocean say to the beach? Nothing, it just waved.',cat:'pun'}
  ];
  var jokes = isCN ? jokesCN : jokesEN;
  var cats = [...new Set(jokes.map(function(j){return j.cat;}))];
  var catNames = isCN ? {'programming':'💻 程序员','cold':'❄️ 冷笑话','riddle':'🤔 脑筋急转弯','life':'😄 生活幽默','dad':'👨 老爸笑话','knock':'🚪 敲门笑话','pun':'🎭 双关语'} : {'programming':'💻 Programming','dad':'👨 Dad Jokes','knock':'🚪 Knock-Knock','pun':'🎭 Puns'};
  
  var card = document.getElementById('app-card');
  var filterHtml = cats.map(function(c){return '<button class="btn btn-secondary cat-btn" data-cat="'+c+'" style="font-size:.8rem;padding:6px 12px">'+catNames[c]+'</button>';}).join('');
  card.innerHTML = '<div id="jokeDisplay" class="output" style="font-size:1.1rem;line-height:1.8;min-height:100px;text-align:center;display:flex;align-items:center;justify-content:center">' +
      (isCN ? '👆 点击下方按钮获取随机笑话' : '👆 Click the button below to get a random joke') +
    '</div>' +
    '<div style="display:flex;gap:8px;margin-top:12px;flex-wrap:wrap;align-items:center">' +
      '<button class="btn" id="newJokeBtn" style="font-size:1rem">' + (isCN ? '😂 换一个笑话' : '😂 New Joke') + '</button>' +
      '<button class="btn btn-secondary" id="copyJokeBtn">' + (isCN ? '📋 复制' : '📋 Copy') + '</button>' +
    '</div>' +
    '<div style="margin-top:12px;display:flex;gap:6px;flex-wrap:wrap" id="catFilters">' + filterHtml + '</div>';
  
  var currentJoke = null;
  var activeCat = null;
  
  function getRandomJoke() {
    var pool = activeCat ? jokes.filter(function(j){return j.cat===activeCat;}) : jokes;
    var joke = pool[Math.floor(Math.random() * pool.length)];
    currentJoke = joke;
    document.getElementById('jokeDisplay').textContent = joke.text;
  }
  
  document.getElementById('newJokeBtn').onclick = getRandomJoke;
  document.getElementById('copyJokeBtn').onclick = function() {
    if (!currentJoke) { getRandomJoke(); return; }
    navigator.clipboard.writeText(currentJoke.text).then(function() {
      var t = document.getElementById('toast') || document.createElement('div');
      if (!t.id) { t.id='toast'; t.className='toast'; document.body.appendChild(t); }
      t.textContent = isCN ? '✅ 已复制到剪贴板' : '✅ Copied!';
      t.classList.add('show');
      setTimeout(function(){t.classList.remove('show');}, 2000);
    });
  };
  
  document.getElementById('catFilters').onclick = function(e) {
    if (e.target.classList.contains('cat-btn')) {
      var cat = e.target.dataset.cat;
      if (activeCat === cat) { activeCat = null; e.target.style.background='';e.target.style.color=''; }
      else { activeCat = cat; }
      document.querySelectorAll('.cat-btn').forEach(function(b){
        if (b.dataset.cat === activeCat) { b.style.background='var(--primary)'; b.style.color='#fff'; }
        else { b.style.background=''; b.style.color=''; }
      });
    }
  };
})();
"""

# ========= MONEY COUNTER =========
money_js = """
(function() {
  'use strict';
  var isCN = document.documentElement.lang === 'zh-CN';
  var currencies = {
    'CNY': {name:isCN?'人民币 (¥)':'Chinese Yuan (¥)', symbol:'¥', bills:[100,50,20,10,5,1], coins:[1,.5,.1], billNames:isCN?['100元','50元','20元','10元','5元','1元']:['¥100','¥50','¥20','¥10','¥5','¥1'], coinNames:isCN?['1元硬币','5角','1角']:['¥1 coin','50分','10分']},
    'USD': {name:isCN?'美元 ($)':'US Dollar ($)', symbol:'$', bills:[100,50,20,10,5,1], coins:[1,.25,.1,.05,.01], billNames:isCN?['$100','$50','$20','$10','$5','$1']:['$100','$50','$20','$10','$5','$1'], coinNames:isCN?['$1 coin','25¢','10¢','5¢','1¢']:['$1 coin','Quarter','Dime','Nickel','Penny']},
    'EUR': {name:isCN?'欧元 (€)':'Euro (€)', symbol:'€', bills:[500,200,100,50,20,10,5], coins:[2,1,.5,.2,.1,.05,.02,.01], billNames:isCN?['€500','€200','€100','€50','€20','€10','€5']:['€500','€200','€100','€50','€20','€10','€5'], coinNames:isCN?['€2','€1','50分','20分','10分','5分','2分','1分']:['€2','€1','50c','20c','10c','5c','2c','1c']},
    'GBP': {name:isCN?'英镑 (£)':'British Pound (£)', symbol:'£', bills:[50,20,10,5], coins:[2,1,.5,.2,.1,.05,.02,.01], billNames:isCN?['£50','£20','£10','£5']:['£50','£20','£10','£5'], coinNames:isCN?['£2','£1','50p','20p','10p','5p','2p','1p']:['£2','£1','50p','20p','10p','5p','2p','1p']},
    'JPY': {name:isCN?'日元 (¥)':'Japanese Yen (¥)', symbol:'¥', bills:[10000,5000,2000,1000], coins:[500,100,50,10,5,1], billNames:isCN?['¥10000','¥5000','¥2000','¥1000']:['¥10,000','¥5,000','¥2,000','¥1,000'], coinNames:isCN?['¥500','¥100','¥50','¥10','¥5','¥1']:['¥500','¥100','¥50','¥10','¥5','¥1']}
  };
  
  var card = document.getElementById('app-card');
  var opts = Object.keys(currencies).map(function(k){return '<option value="'+k+'">'+currencies[k].name+'</option>';}).join('');
  card.innerHTML = '<h2>' + (isCN ? '数钱计算器' : 'Money Counter') + '</h2>' +
    '<select id="currencySelect" style="margin-bottom:12px;font-size:1rem">'+opts+'</select>' +
    '<div id="denominations" style="display:grid;grid-template-columns:repeat(auto-fill,minmax(140px,1fr));gap:10px"></div>' +
    '<div style="margin-top:16px;padding:16px;background:linear-gradient(135deg,#4F46E5,#7C3AED);color:#fff;border-radius:12px;text-align:center">' +
      '<div style="font-size:.85rem;opacity:.9">'+(isCN?'总金额':'Total Amount')+'</div>' +
      '<div id="totalDisplay" style="font-size:2rem;font-weight:700">'+currencies['CNY'].symbol+'0.00</div>' +
    '</div>';
  
  function buildDenominations(curKey) {
    var cur = currencies[curKey];
    var html = '';
    cur.bills.forEach(function(v,i) {
      html += '<div style="background:#f8fafc;border:1px solid var(--border);border-radius:8px;padding:8px;text-align:center">' +
        '<div style="font-size:.75rem;color:var(--text-secondary);margin-bottom:4px">'+cur.billNames[i]+'</div>' +
        '<input type="number" min="0" value="0" data-val="'+v+'" data-type="bill" class="denom-input" style="width:100%;text-align:center;font-size:1rem;padding:6px">' +
      '</div>';
    });
    cur.coins.forEach(function(v,i) {
      html += '<div style="background:#fefce8;border:1px solid #fde68a;border-radius:8px;padding:8px;text-align:center">' +
        '<div style="font-size:.75rem;color:var(--text-secondary);margin-bottom:4px">'+cur.coinNames[i]+'</div>' +
        '<input type="number" min="0" value="0" data-val="'+v+'" data-type="coin" class="denom-input" style="width:100%;text-align:center;font-size:1rem;padding:6px">' +
      '</div>';
    });
    document.getElementById('denominations').innerHTML = html;
    attachListeners(cur);
  }
  
  function attachListeners(cur) {
    document.querySelectorAll('.denom-input').forEach(function(inp) {
      inp.oninput = function() {
        var total = 0;
        document.querySelectorAll('.denom-input').forEach(function(el) {
          total += (parseInt(el.value)||0) * parseFloat(el.dataset.val);
        });
        document.getElementById('totalDisplay').textContent = cur.symbol + total.toFixed(2);
      };
    });
  }
  
  document.getElementById('currencySelect').onchange = function() {
    buildDenominations(this.value);
  };
  buildDenominations('CNY');
})();
"""

# ========= INDENT FORMATTER =========
indent_js = """
(function() {
  'use strict';
  var isCN = document.documentElement.lang === 'zh-CN';
  var card = document.getElementById('app-card');
  card.innerHTML = '<h2>' + (isCN ? '代码缩进格式化' : 'Code Indent Formatter') + '</h2>' +
    '<textarea id="codeInput" rows="10" placeholder="' + (isCN ? '粘贴需要格式化的代码...' : 'Paste your code here...') + '" style="font-family:monospace;font-size:.85rem"></textarea>' +
    '<div style="display:flex;gap:8px;margin-top:12px;flex-wrap:wrap;align-items:center">' +
      '<select id="indentType" style="width:auto">' +
        '<option value="spaces2">' + (isCN ? '2个空格缩进' : '2 Spaces') + '</option>' +
        '<option value="spaces4" selected>' + (isCN ? '4个空格缩进' : '4 Spaces') + '</option>' +
        '<option value="spaces8">' + (isCN ? '8个空格缩进' : '8 Spaces') + '</option>' +
        '<option value="tab">' + (isCN ? 'Tab缩进' : 'Tab') + '</option>' +
      '</select>' +
      '<select id="srcIndent" style="width:auto">' +
        '<option value="auto">' + (isCN ? '自动检测来源缩进' : 'Auto Detect') + '</option>' +
        '<option value="spaces2">2 ' + (isCN ? '空格' : 'Spaces') + '</option>' +
        '<option value="spaces4">4 ' + (isCN ? '空格' : 'Spaces') + '</option>' +
        '<option value="tab">Tab</option>' +
      '</select>' +
      '<button class="btn" id="formatBtn">' + (isCN ? '✨ 格式化' : '✨ Format') + '</button>' +
      '<button class="btn btn-secondary" id="copyBtn">' + (isCN ? '📋 复制结果' : '📋 Copy') + '</button>' +
      '<button class="btn btn-secondary" id="clearBtn">' + (isCN ? '清空' : 'Clear') + '</button>' +
    '</div>' +
    '<textarea id="codeOutput" rows="10" readonly style="font-family:monospace;font-size:.85rem;margin-top:12px;background:#1e293b;color:#e2e8f0;border-color:#334155" placeholder="' + (isCN ? '格式化结果将显示在这里...' : 'Formatted output will appear here...') + '"></textarea>';
  
  function detectIndent(text) {
    var match = text.match(/^[ \\t]+/m);
    if (!match) return {type:'spaces',size:4};
    var ws = match[0];
    if (ws.includes('\\t') && !ws.includes(' ')) return {type:'tab',size:1};
    return {type:'spaces',size:ws.length};
  }
  
  function getIndentStr(size, isTab) {
    if (isTab) return '\\t';
    return ' '.repeat(size);
  }
  
  function formatCode(text, targetType, targetSize, srcIndent) {
    var lines = text.split('\\n');
    var src = srcIndent;
    if (src === 'auto') {
      var detected = detectIndent(text);
      src = detected.type === 'tab' ? 'tab' : 'spaces' + detected.size;
    }
    var srcIsTab = src === 'tab';
    var srcSize = srcIsTab ? 1 : parseInt(src.replace('spaces',''));
    var tgtIsTab = targetType === 'tab';
    var tgtSize = tgtIsTab ? 1 : targetSize;
    var tgtIndent = tgtIsTab ? '\\t' : ' '.repeat(targetSize);
    
    // 检测括号平衡来决定缩进级别
    var result = [];
    var indentLevel = 0;
    for (var i = 0; i < lines.length; i++) {
      var line = lines[i];
      // 计算当前行开头的空白
      var leadingWs = line.match(/^([ \\t]*)/)[0];
      var rest = line.slice(leadingWs.length);
      // 计算缩进级别
      var wsCount = 0;
      for (var j = 0; j < leadingWs.length; j++) {
        if (leadingWs[j] === '\\t') wsCount += srcSize;
        else wsCount++;
      }
      var level = Math.round(wsCount / srcSize);
      // 根据括号调整缩进
      var openBrackets = (rest.match(/[{(\\[]/g)||[]).length;
      var closeBrackets = (rest.match(/[})\\]]/g)||[]).length;
      // 检测闭合括号在行首的情况
      if (/^[})\\]]/.test(rest.trim())) level = Math.max(0, level - 1);
      
      var finalLevel = level;
      result.push(tgtIndent.repeat(finalLevel) + rest.trim());
      
      indentLevel += openBrackets - closeBrackets;
      if (indentLevel < 0) indentLevel = 0;
    }
    return result.join('\\n');
  }
  
  document.getElementById('formatBtn').onclick = function() {
    var input = document.getElementById('codeInput').value;
    if (!input.trim()) {
      alert(isCN ? '请先粘贴代码' : 'Please paste some code first');
      return;
    }
    var targetVal = document.getElementById('indentType').value;
    var targetIsTab = targetVal === 'tab';
    var targetSize = targetIsTab ? 1 : parseInt(targetVal.replace('spaces',''));
    var srcVal = document.getElementById('srcIndent').value;
    var formatted = formatCode(input, targetIsTab ? 'tab' : 'spaces', targetSize, srcVal);
    document.getElementById('codeOutput').value = formatted;
  };
  
  document.getElementById('copyBtn').onclick = function() {
    var out = document.getElementById('codeOutput').value;
    if (!out) { document.getElementById('formatBtn').click(); return; }
    navigator.clipboard.writeText(out).then(function() {
      var t = document.getElementById('toast') || document.createElement('div');
      if (!t.id) { t.id='toast'; t.className='toast'; document.body.appendChild(t); }
      t.textContent = isCN ? '✅ 已复制到剪贴板' : '✅ Copied!';
      t.classList.add('show');
      setTimeout(function(){t.classList.remove('show');}, 2000);
    });
  };
  document.getElementById('clearBtn').onclick = function() {
    document.getElementById('codeInput').value = '';
    document.getElementById('codeOutput').value = '';
  };
})();
"""

# Map slug -> js
tools_js = {
    'spell-checker': spell_js,
    'acronym-finder': acronym_js,
    'random-joke': joke_js,
    'money-counter': money_js,
    'indent-formatter': indent_js,
}

for slug, js in tools_js.items():
    for lang_dir in [os.path.join(BASE, slug), os.path.join(BASE, 'en', slug)]:
        fpath = os.path.join(lang_dir, 'index.html')
        with open(fpath, 'r') as f:
            content = f.read()
        # Replace placeholder <script> with real JS
        content = content.replace(
            "(function() {{\n  'use strict';\n}}());",
            js.strip()
        )
        with open(fpath, 'w') as f:
            f.write(content)
        print(f"✅ Updated JS: {fpath}")

print("\nAll 5 tools now have real functionality!")