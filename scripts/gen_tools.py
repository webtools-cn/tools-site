#!/usr/bin/env python3
"""Generate 10 tools: pig-latin-translator, sip-calculator, chess-timer, pixel-to-em, em-to-px, lottery-generator, yes-no, flip-text, bubble-text, bold-text-generator"""

import os

BASE = '/home/chison/tools-site'

GA = '''<script async src="https://www.googletagmanager.com/gtag/js?id=G-9W1157EBQV"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','G-9W1157EBQV');</script>
<script>window.addEventListener("error",function(e){if(e&&e.message===""){e.preventDefault();}});window.addEventListener("unhandledrejection",function(e){if(e&&e.reason&&e.reason.message===""){e.preventDefault();}});</script>'''

# Shared CSS (uses {{ }} to escape f-string braces)
CSS = '''*{{box-sizing:border-box;margin:0;padding:0}}
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
textarea,input,select{{background:#0f172a;border:1px solid rgba(148,163,184,.2);border-radius:6px;padding:8px 12px;color:#e2e8f0;font-size:.85rem;outline:none;font-family:inherit;width:100%}}
textarea:focus,input:focus,select:focus{{border-color:rgba(6,182,212,.5)}}
.btn{{padding:8px 20px;border:none;border-radius:6px;font-size:.85rem;cursor:pointer;transition:all .2s;display:inline-flex;align-items:center;gap:4px}}
.btn-primary{{background:rgba(6,182,212,.2);color:#22d3ee;border:1px solid rgba(6,182,212,.3)}}
.btn-primary:hover{{background:rgba(6,182,212,.3)}}
.btn-secondary{{background:rgba(148,163,184,.1);color:#94a3b8;border:1px solid rgba(148,163,184,.2)}}
.btn-secondary:hover{{background:rgba(148,163,184,.2)}}
.tool-section{{background:#1e293b;border-radius:12px;padding:20px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1)}}
.tool-section h2{{font-size:1.1rem;color:#f1f5f9;margin-bottom:12px}}
.result-output{{background:#0f172a;border-radius:8px;padding:16px;color:#e2e8f0;font-size:.85rem;overflow-x:auto;max-height:400px;white-space:pre-wrap;word-break:break-all;margin-bottom:12px;font-family:ui-monospace,SFMono-Regular,Consolas,monospace}}
.result-actions{{display:flex;gap:8px;flex-wrap:wrap}}
.faq-item{{margin-bottom:16px}}
.faq-item h3{{font-size:.95rem;color:#e2e8f0;margin-bottom:6px}}
.faq-item p{{color:#94a3b8;font-size:.9rem}}
.footer{{border-top:1px solid rgba(148,163,184,.1);padding:24px 0;margin-top:32px;text-align:center;color:#64748b;font-size:.85rem}}
.footer a{{color:#64748b;margin:0 8px}}
.toast{{position:fixed;bottom:20px;left:50%;transform:translateX(-50%);background:#1e293b;color:#22d3ee;padding:10px 24px;border-radius:8px;border:1px solid rgba(6,182,212,.3);font-size:.85rem;z-index:999;opacity:0;transition:opacity .3s}}
.toast.show{{opacity:1}}
.hero{{margin-bottom:16px}}
.hero p{{color:#94a3b8;font-size:.95rem;margin-bottom:8px}}
.badge{{display:inline-block;background:rgba(6,182,212,.15);color:#22d3ee;padding:2px 8px;border-radius:4px;font-size:.8rem;margin-right:6px}}
.main-grid{{display:grid;grid-template-columns:1fr 300px;gap:16px}}
@media(max-width:768px){{.main-grid{{grid-template-columns:1fr}}.header h1{{font-size:1.3rem}}}}
.seo-content{{color:#475569;font-size:.85rem;margin-top:24px}}
.seo-content h3{{color:#64748b;font-size:1rem;margin-bottom:8px}}
.stat-row{{display:flex;gap:24px;flex-wrap:wrap}}
.stat-item{{text-align:center}}
.stat-value{{color:#22d3ee;font-weight:700;font-size:1.2rem}}
.stat-label{{color:#94a3b8;font-size:.8rem}}
@media(max-width:640px){{h1{{font-size:1.2rem;word-break:break-word}}}}'''

SEO_TAIL = '''<meta property="og:image" content="https://free-toolbase.com/og-image.svg">
<meta name="twitter:image" content="https://free-toolbase.com/og-image.svg">
<meta name="twitter:card" content="summary_large_image">
<meta name="robots" content="index, follow">
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5998441792679372" crossorigin="anonymous"></script>'''

ADSENSE_BLOCK = '''<ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-5998441792679372" data-ad-slot="auto" data-ad-format="auto" data-full-width-responsive="true"></ins>
<script>(adsbygoogle = window.adsbygoogle || []).push({});</script>'''

def cn_footer(slug, cn_name):
    return f'''{ADSENSE_BLOCK}
<footer class="footer container">
<div style="margin-bottom:12px"><a href="../index.html">首页</a><a href="../index.html">全部工具</a><a href="../privacy/">隐私政策</a><a href="../terms/">服务条款</a><a href="../about/">关于我们</a><a href="../en/{slug}/">EN</a></div>
<p>{cn_name} | 无需注册 · 数据绝不上传服务器</p>
<p style="margin-top:8px;color:#475569;font-size:.8rem">问题反馈: dexshuang@google.com</p>
</footer>
<div class="toast" id="toast"></div>'''

def en_footer(slug, en_name):
    return f'''{ADSENSE_BLOCK}
<footer class="footer container">
<div style="margin-bottom:12px"><a href="../index.html">Home</a><a href="../index.html">All Tools</a><a href="../privacy/">Privacy</a><a href="../terms/">Terms</a><a href="../about/">About</a><a href="../{slug}/">中文</a></div>
<p>{en_name} | No signup · Data never leaves your device</p>
<p style="margin-top:8px;color:#475569;font-size:.8rem">Feedback: dexshuang@google.com</p>
</footer>
<div class="toast" id="toast"></div>'''

def make_page(slug, cn_name, en_name, cn_desc, en_desc, cn_title, en_title,
              cn_hero, en_hero, cn_badges, en_badges, cn_seo, en_seo,
              body_cn, body_en, js, lang='cn'):
    name = cn_name if lang == 'cn' else en_name
    title = cn_title if lang == 'cn' else en_title
    desc = cn_desc if lang == 'cn' else en_desc
    hero = cn_hero if lang == 'cn' else en_hero
    badges = cn_badges if lang == 'cn' else en_badges
    seo = cn_seo if lang == 'cn' else en_seo
    body = body_cn if lang == 'cn' else body_en
    lang_attr = 'zh-CN' if lang == 'cn' else 'en'
    hreflang_self = 'zh' if lang == 'cn' else 'en'
    hreflang_other = 'en' if lang == 'cn' else 'zh'
    self_url = f'{slug}/' if lang == 'cn' else f'en/{slug}/'
    other_url = f'en/{slug}/' if lang == 'cn' else f'{slug}/'
    xdefault = f'en/{slug}/'
    canon = f'https://free-toolbase.com/{self_url}'
    home_label = '首页' if lang == 'cn' else 'Home'
    tools_label = '工具' if lang == 'cn' else 'Tools'
    home_url = '../' if lang == 'cn' else '../'
    footer = cn_footer(slug, cn_name) if lang == 'cn' else en_footer(slug, en_name)

    breadcrumb_name1 = home_label
    breadcrumb_name2 = tools_label
    breadcrumb_item1 = f'https://free-toolbase.com/{"en/" if lang=="en" else ""}'
    breadcrumb_item2 = f'https://free-toolbase.com/{"en/" if lang=="en" else ""}#tools'

    # seo heading (first sentence)
    seo_heading = seo.split('。')[0].split('.')[0]

    page = f'''<!DOCTYPE html>
<html lang="{lang_attr}">
<head>
{GA}
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="{desc}">
<title>{title}</title>
<link rel="canonical" href="{canon}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canon}">
<meta property="og:type" content="website">
<link rel="alternate" hreflang="{hreflang_self}" href="https://free-toolbase.com/{self_url}">
<link rel="alternate" hreflang="{hreflang_other}" href="https://free-toolbase.com/{other_url}">
<link rel="alternate" hreflang="x-default" href="https://free-toolbase.com/{xdefault}">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"SoftwareApplication","name":"{name}","description":"{desc}","applicationCategory":"UtilitiesApplication","operatingSystem":"Web","offers":{{"@type":"Offer","price":"0","priceCurrency":"USD"}}}}</script>
<style>{CSS}</style>
{SEO_TAIL}
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"{breadcrumb_name1}","item":"{breadcrumb_item1}"}},{{"@type":"ListItem","position":2,"name":"{breadcrumb_name2}","item":"{breadcrumb_item2}"}},{{"@type":"ListItem","position":3,"name":"{name}","item":"{canon}"}}]}}</script>
</head>
<body>
<div class="container">
<div class="header"><h1>{name}</h1>
<div class="lang-switch">{'<a href="index.html" class="active">中文</a><a href="../en/'+slug+'/">EN</a>' if lang=='cn' else '<a href="../'+slug+'/">中文</a><a href="index.html" class="active">EN</a>'}</div>
</div>
<p class="nav-back"><a href="{home_url}index.html">{home_label}</a> &rsaquo; <a href="{home_url}index.html#tools">{tools_label}</a> &rsaquo; {name}</p>
<div class="hero"><p>{hero}</p>{badges}</div>
<div class="main-grid"><div>
{body}
</div></div>
<div class="seo-content"><h3>{seo_heading}</h3><p>{seo}</p></div>
</div>
{footer}
</body></html>'''

    return page

# ============ TOOLS DATA ============

tools = []

# 1. Pig Latin
tools.append({
    'slug': 'pig-latin-translator',
    'cn_name': '🐷 猪拉丁语翻译器', 'en_name': '🐷 Pig Latin Translator',
    'cn_desc': '将英文文本转换为猪拉丁语（Pig Latin）。输入英文句子，自动输出猪拉丁语版本。',
    'en_desc': 'Convert English text to Pig Latin. Enter English sentences and get the Pig Latin version automatically.',
    'cn_title': '猪拉丁语翻译器 - Free ToolBase', 'en_title': 'Pig Latin Translator - Free ToolBase',
    'cn_hero': '免费在线猪拉丁语翻译器，将英文文本转换为Pig Latin。支持实时转换，一键复制。无需注册，数据不上传服务器。',
    'en_hero': 'Free online Pig Latin Translator. Convert English text to Pig Latin instantly. No signup required, all processing done locally.',
    'cn_badges': '<span class="badge">实时转换</span><span class="badge">零依赖</span><span class="badge">隐私安全</span>',
    'en_badges': '<span class="badge">Real-time</span><span class="badge">Zero-dependency</span><span class="badge">Private</span>',
    'cn_seo': '猪拉丁语（Pig Latin）是一种英语文字游戏，起源于19世纪末的美国儿童游戏。规则：以元音开头的单词加way，以辅音开头的单词将辅音移到末尾加ay。',
    'en_seo': 'Pig Latin is an English word game that originated as a children game in late 19th century America. Rules: words starting with vowels get "way", consonants move to end + "ay".',
    'body_cn': '''<div class="tool-section"><h2>输入英文文本</h2><textarea id="inputText" placeholder="输入英文句子，例如: Hello World..." style="min-height:120px"></textarea></div>
<div class="tool-section"><h2>猪拉丁语结果</h2><div class="result-output" id="resultOutput">等待输入...</div><div class="result-actions"><button class="btn btn-primary" onclick="convertPigLatin()">🐷 立即使用</button><button class="btn btn-secondary" onclick="copyResult()">📋 复制结果</button><button class="btn btn-secondary" onclick="clearAll()">🗑️ 清空</button></div></div>
<div class="tool-section"><h2>❓ 什么是猪拉丁语？</h2><div class="faq-item"><h3>猪拉丁语的规则是什么？</h3><p>以元音(a/e/i/o/u)开头的单词加"way"，以辅音开头的单词将辅音移到末尾加"ay"。例如"hello"→"ellohay"，"apple"→"appleway"。</p></div></div>''',
    'body_en': '''<div class="tool-section"><h2>Enter English Text</h2><textarea id="inputText" placeholder="Enter English sentences, e.g. Hello World..." style="min-height:120px"></textarea></div>
<div class="tool-section"><h2>Pig Latin Result</h2><div class="result-output" id="resultOutput">Waiting for input...</div><div class="result-actions"><button class="btn btn-primary" onclick="convertPigLatin()">🐷 Use Now</button><button class="btn btn-secondary" onclick="copyResult()">📋 Copy</button><button class="btn btn-secondary" onclick="clearAll()">🗑️ Clear</button></div></div>
<div class="tool-section"><h2>❓ What is Pig Latin?</h2><div class="faq-item"><h3>What are the rules?</h3><p>Words starting with vowels (a/e/i/o/u) get "way" appended. Words starting with consonants move the consonant cluster to the end + "ay". E.g. "hello"→"ellohay", "apple"→"appleway".</p></div></div>''',
    'js': '''<script>
function getVowels(){return new Set(['a','e','i','o','u','A','E','I','O','U']);}
function pigLatinWord(word){
  if(!word||!/[a-zA-Z]/.test(word))return word;
  var v=getVowels();
  if(v.has(word[0]))return word+'way';
  var i=0;
  while(i<word.length&&!v.has(word[i])&&/[a-zA-Z]/.test(word[i]))i++;
  if(i>=word.length)return word+'ay';
  return word.slice(i)+word.slice(0,i)+'ay';
}
function convertPigLatin(){
  var input=document.getElementById('inputText').value.trim();
  if(!input){document.getElementById('resultOutput').textContent='EMPTY';return;}
  var words=input.split(/\\s+/);
  document.getElementById('resultOutput').textContent=words.map(pigLatinWord).join(' ');
}
function copyResult(){
  var t=document.getElementById('resultOutput').textContent;
  if(!t||t==='EMPTY')return;
  navigator.clipboard.writeText(t).then(function(){showToast('COPIED');});
}
function clearAll(){document.getElementById('inputText').value='';document.getElementById('resultOutput').textContent='EMPTY';}
function showToast(m){var t=document.getElementById('toast');t.textContent=m;t.classList.add('show');setTimeout(function(){t.classList.remove('show');},2000);}
document.getElementById('inputText').addEventListener('input',convertPigLatin);
</script>''',
    'cn_empty': '等待输入...', 'cn_copied': '已复制!',
    'en_empty': 'Waiting for input...', 'en_copied': 'Copied!',
})

# 2. SIP Calculator
tools.append({
    'slug': 'sip-calculator',
    'cn_name': '💰 SIP投资计算器', 'en_name': '💰 SIP Investment Calculator',
    'cn_desc': '计算定期定额投资(SIP)的预期收益。输入月投金额、年化收益率和投资年限，查看最终价值和总收益。',
    'en_desc': 'Calculate expected returns from Systematic Investment Plan. Enter monthly amount, annual rate, and duration to see final value.',
    'cn_title': 'SIP投资计算器 - Free ToolBase', 'en_title': 'SIP Investment Calculator - Free ToolBase',
    'cn_hero': '免费在线SIP投资计算器，计算定期定额投资的复利收益。输入月投金额、年化收益率和投资年限，查看最终价值、总投入和总收益。支持图表可视化。',
    'en_hero': 'Free online SIP Investment Calculator. Calculate compound returns from regular investments. Enter monthly amount, annual rate, and duration to see final value and total gains.',
    'cn_badges': '<span class="badge">复利计算</span><span class="badge">图表可视化</span><span class="badge">隐私安全</span>',
    'en_badges': '<span class="badge">Compound</span><span class="badge">Charts</span><span class="badge">Private</span>',
    'cn_seo': 'SIP（定期定额投资）通过每月固定投入、利用复利效应实现财富增长。本工具计算预期收益并提供可视化图表。',
    'en_seo': 'SIP (Systematic Investment Plan) uses fixed monthly contributions and compound interest. This tool calculates expected returns with visual charts.',
    'body_cn': '''<div class="tool-section"><h2>投资参数</h2><div style="display:flex;gap:12px;flex-wrap:wrap;margin-bottom:12px"><div style="flex:1;min-width:180px"><label style="color:#94a3b8;font-size:.85rem">月投金额 (¥)</label><input type="number" id="monthlyAmount" value="5000" min="100" step="100"></div><div style="flex:1;min-width:180px"><label style="color:#94a3b8;font-size:.85rem">年化收益率 (%)</label><input type="number" id="annualRate" value="12" min="0" step="0.1"></div><div style="flex:1;min-width:180px"><label style="color:#94a3b8;font-size:.85rem">投资年限</label><input type="number" id="years" value="10" min="1" step="1"></div></div><button class="btn btn-primary" onclick="calculateSIP()">💰 立即使用</button></div>
<div class="tool-section"><h2>计算结果</h2><div class="stat-row" style="margin-bottom:12px"><div class="stat-item"><div class="stat-value" id="totalInvestment">¥0</div><div class="stat-label">总投入</div></div><div class="stat-item"><div class="stat-value" id="finalValue">¥0</div><div class="stat-label">最终价值</div></div><div class="stat-item"><div class="stat-value" id="totalGain">¥0</div><div class="stat-label">总收益</div></div><div class="stat-item"><div class="stat-value" id="roi">0%</div><div class="stat-label">收益率</div></div></div><canvas id="growthChart" style="width:100%;max-height:300px"></canvas></div>''',
    'body_en': '''<div class="tool-section"><h2>Parameters</h2><div style="display:flex;gap:12px;flex-wrap:wrap;margin-bottom:12px"><div style="flex:1;min-width:180px"><label style="color:#94a3b8;font-size:.85rem">Monthly Amount ($)</label><input type="number" id="monthlyAmount" value="500" min="10" step="10"></div><div style="flex:1;min-width:180px"><label style="color:#94a3b8;font-size:.85rem">Annual Return (%)</label><input type="number" id="annualRate" value="12" min="0" step="0.1"></div><div style="flex:1;min-width:180px"><label style="color:#94a3b8;font-size:.85rem">Years</label><input type="number" id="years" value="10" min="1" step="1"></div></div><button class="btn btn-primary" onclick="calculateSIP()">💰 Use Now</button></div>
<div class="tool-section"><h2>Results</h2><div class="stat-row" style="margin-bottom:12px"><div class="stat-item"><div class="stat-value" id="totalInvestment">$0</div><div class="stat-label">Total Invested</div></div><div class="stat-item"><div class="stat-value" id="finalValue">$0</div><div class="stat-label">Final Value</div></div><div class="stat-item"><div class="stat-value" id="totalGain">$0</div><div class="stat-label">Total Gain</div></div><div class="stat-item"><div class="stat-value" id="roi">0%</div><div class="stat-label">ROI</div></div></div><canvas id="growthChart" style="width:100%;max-height:300px"></canvas></div>''',
    'js': '''<script>
function calculateSIP(){
  var monthly=parseFloat(document.getElementById('monthlyAmount').value)||5000;
  var rate=parseFloat(document.getElementById('annualRate').value)||12;
  var yrs=parseInt(document.getElementById('years').value)||10;
  var mr=rate/100/12,months=yrs*12,fv=0,labels=[],data=[];
  for(var i=1;i<=months;i++){fv=(fv+monthly)*(1+mr);if(i%12===0||i===months){labels.push('Y'+Math.floor(i/12));data.push(Math.round(fv));}}
  var ti=monthly*months,gain=fv-ti,roiPct=ti>0?(gain/ti*100):0;
  document.getElementById('totalInvestment').textContent='$'+ti.toLocaleString();
  document.getElementById('finalValue').textContent='$'+Math.round(fv).toLocaleString();
  document.getElementById('totalGain').textContent='$'+Math.round(gain).toLocaleString();
  document.getElementById('roi').textContent=roiPct.toFixed(1)+'%';
  drawChart(labels,data);
}
function drawChart(labels,data){
  var canvas=document.getElementById('growthChart'),ctx=canvas.getContext('2d');
  var dpr=window.devicePixelRatio||1,rect=canvas.parentElement.getBoundingClientRect();
  canvas.width=rect.width*dpr;canvas.height=300*dpr;canvas.style.width=rect.width+'px';canvas.style.height='300px';ctx.scale(dpr,dpr);
  var w=rect.width-60,h=240,ox=50,oy=20,maxVal=Math.max.apply(null,data)*1.1||1;
  ctx.clearRect(0,0,w+60,h+40);
  ctx.strokeStyle='rgba(148,163,184,.2)';ctx.lineWidth=1;
  for(var i=0;i<=4;i++){var y=oy+h-h*i/4;ctx.beginPath();ctx.moveTo(ox,y);ctx.lineTo(ox+w,y);ctx.stroke();ctx.fillStyle='#64748b';ctx.font='11px sans-serif';ctx.fillText('$'+(maxVal*i/4/1000).toFixed(0)+'K',2,y+4);}
  labels.forEach(function(l,i){ctx.fillStyle='#64748b';ctx.font='11px sans-serif';ctx.fillText(l,ox+i*(w/(labels.length-1||1))-10,oy+h+20);});
  ctx.beginPath();ctx.strokeStyle='#22d3ee';ctx.lineWidth=2;
  data.forEach(function(d,i){var x=ox+i*(w/(data.length-1||1)),y=oy+h-(d/maxVal)*h;if(i===0)ctx.moveTo(x,y);else ctx.lineTo(x,y);});ctx.stroke();
  ctx.fillStyle='rgba(6,182,212,.2)';
  data.forEach(function(d,i){var x=ox+i*(w/(data.length-1||1)),y=oy+h-(d/maxVal)*h;ctx.beginPath();ctx.arc(x,y,4,0,Math.PI*2);ctx.fill();ctx.stroke();});
}
window.addEventListener('load',calculateSIP);
['monthlyAmount','annualRate','years'].forEach(function(id){document.getElementById(id).addEventListener('input',calculateSIP);});
</script>''',
    'cn_empty': '', 'cn_copied': '', 'en_empty': '', 'en_copied': '',
})

# 3. Chess Timer
tools.append({
    'slug': 'chess-timer',
    'cn_name': '♟️ 国际象棋计时器', 'en_name': '♟️ Chess Timer',
    'cn_desc': '双人国际象棋计时器，支持自定义时间和加秒。双方轮流计时，到时间为零自动提示。',
    'en_desc': 'Two-player chess clock with customizable time and increment. Alternating timer with automatic timeout alert.',
    'cn_title': '国际象棋计时器 - Free ToolBase', 'en_title': 'Chess Timer - Free ToolBase',
    'cn_hero': '免费在线国际象棋计时器，模拟真实棋钟。支持自定义初始时间、加秒设置，双人轮流计时。适合国际象棋、围棋等需要计时的对弈。',
    'en_hero': 'Free online Chess Timer simulating a real chess clock. Customizable initial time and increment. Perfect for chess, Go, and other timed games.',
    'cn_badges': '<span class="badge">双人计时</span><span class="badge">加秒模式</span><span class="badge">音效提示</span>',
    'en_badges': '<span class="badge">Two-player</span><span class="badge">Increment</span><span class="badge">Alert</span>',
    'cn_seo': '国际象棋计时器模拟真实棋钟，双方轮流计时。支持自定义初始时间和加秒，多种预设模式。适用于国际象棋、围棋等需要计时的对弈活动。',
    'en_seo': 'Chess timer simulating a real chess clock with alternating timing. Customizable initial time and increment, multiple presets. Perfect for chess, Go, and other timed games.',
    'body_cn': '''<div class="tool-section"><h2>时间设置</h2><div style="display:flex;gap:12px;flex-wrap:wrap;margin-bottom:12px"><div style="flex:1;min-width:150px"><label style="color:#94a3b8;font-size:.85rem">初始时间(分钟)</label><input type="number" id="initMinutes" value="5" min="1" step="1"></div><div style="flex:1;min-width:150px"><label style="color:#94a3b8;font-size:.85rem">加秒(秒)</label><input type="number" id="increment" value="3" min="0" step="1"></div><div style="flex:1;min-width:150px"><label style="color:#94a3b8;font-size:.85rem">预设</label><select id="preset" onchange="applyPreset()"><option value="">自定义</option><option value="1,0">子弹 1+0</option><option value="3,0">闪电 3+0</option><option value="3,2">快棋 3+2</option><option value="5,3">常用 5+3</option><option value="10,0">快速 10+0</option><option value="10,5">10+5</option><option value="15,10">标准 15+10</option></select></div></div></div>
<div class="tool-section"><h2>计时器</h2><div style="display:flex;gap:16px;flex-wrap:wrap"><div style="flex:1;text-align:center;padding:24px;background:#0f172a;border-radius:12px;border:3px solid rgba(6,182,212,.3);cursor:pointer" id="player1Box" onclick="switchTurn(0)"><div style="font-size:.9rem;color:#94a3b8;margin-bottom:8px">⚪ 玩家1 (白方)</div><div style="font-size:3rem;font-weight:700;color:#22d3ee;font-family:monospace" id="timer1">5:00</div><div style="color:#94a3b8;font-size:.8rem;margin-top:4px">点击计时</div></div><div style="flex:1;text-align:center;padding:24px;background:#0f172a;border-radius:12px;border:3px solid rgba(148,163,184,.1);cursor:pointer" id="player2Box" onclick="switchTurn(1)"><div style="font-size:.9rem;color:#94a3b8;margin-bottom:8px">⚫ 玩家2 (黑方)</div><div style="font-size:3rem;font-weight:700;color:#94a3b8;font-family:monospace" id="timer2">5:00</div><div style="color:#94a3b8;font-size:.8rem;margin-top:4px">等待中</div></div></div><div class="result-actions" style="margin-top:12px"><button class="btn btn-primary" onclick="startTimer()">▶ 开始</button><button class="btn btn-secondary" onclick="pauseTimer()">⏸ 暂停</button><button class="btn btn-secondary" onclick="resetTimer()">🔄 重置</button></div></div>''',
    'body_en': '''<div class="tool-section"><h2>Time Settings</h2><div style="display:flex;gap:12px;flex-wrap:wrap;margin-bottom:12px"><div style="flex:1;min-width:150px"><label style="color:#94a3b8;font-size:.85rem">Initial Time (min)</label><input type="number" id="initMinutes" value="5" min="1" step="1"></div><div style="flex:1;min-width:150px"><label style="color:#94a3b8;font-size:.85rem">Increment (sec)</label><input type="number" id="increment" value="3" min="0" step="1"></div><div style="flex:1;min-width:150px"><label style="color:#94a3b8;font-size:.85rem">Preset</label><select id="preset" onchange="applyPreset()"><option value="">Custom</option><option value="1,0">Bullet 1+0</option><option value="3,0">Blitz 3+0</option><option value="3,2">Blitz 3+2</option><option value="5,3">Rapid 5+3</option><option value="10,0">Rapid 10+0</option><option value="10,5">10+5</option><option value="15,10">Standard 15+10</option></select></div></div></div>
<div class="tool-section"><h2>Clock</h2><div style="display:flex;gap:16px;flex-wrap:wrap"><div style="flex:1;text-align:center;padding:24px;background:#0f172a;border-radius:12px;border:3px solid rgba(6,182,212,.3);cursor:pointer" id="player1Box" onclick="switchTurn(0)"><div style="font-size:.9rem;color:#94a3b8;margin-bottom:8px">⚪ Player 1 (White)</div><div style="font-size:3rem;font-weight:700;color:#22d3ee;font-family:monospace" id="timer1">5:00</div><div style="color:#94a3b8;font-size:.8rem;margin-top:4px">Click to time</div></div><div style="flex:1;text-align:center;padding:24px;background:#0f172a;border-radius:12px;border:3px solid rgba(148,163,184,.1);cursor:pointer" id="player2Box" onclick="switchTurn(1)"><div style="font-size:.9rem;color:#94a3b8;margin-bottom:8px">⚫ Player 2 (Black)</div><div style="font-size:3rem;font-weight:700;color:#94a3b8;font-family:monospace" id="timer2">5:00</div><div style="color:#94a3b8;font-size:.8rem;margin-top:4px">Waiting</div></div></div><div class="result-actions" style="margin-top:12px"><button class="btn btn-primary" onclick="startTimer()">▶ Start</button><button class="btn btn-secondary" onclick="pauseTimer()">⏸ Pause</button><button class="btn btn-secondary" onclick="resetTimer()">🔄 Reset</button></div></div>''',
    'js': '''<script>
var timers=[300,300],incr=[3,3],active=-1,intervalId=null,paused=false;
function fmt(s){var m=Math.floor(s/60),sec=s%60;return m+':'+(sec<10?'0':'')+sec;}
function updateDisplay(){
  document.getElementById('timer1').textContent=fmt(timers[0]);
  document.getElementById('timer2').textContent=fmt(timers[1]);
  var b1=document.getElementById('player1Box'),b2=document.getElementById('player2Box');
  if(active===0){b1.style.borderColor='rgba(6,182,212,.6)';b2.style.borderColor='rgba(148,163,184,.1)';}
  else if(active===1){b2.style.borderColor='rgba(6,182,212,.6)';b1.style.borderColor='rgba(148,163,184,.1)';}
  else{b1.style.borderColor='rgba(148,163,184,.1)';b2.style.borderColor='rgba(148,163,184,.1)';}
  if(timers[0]<=0){document.getElementById('timer1').textContent='超时!';document.getElementById('timer1').style.color='#f87171';}
  if(timers[1]<=0){document.getElementById('timer2').textContent='超时!';document.getElementById('timer2').style.color='#f87171';}
}
function switchTurn(player){
  if(paused||active===player)return;
  if(active>=0)timers[active]+=incr[active];
  active=player;updateDisplay();
  if(!intervalId)startInterval();
}
function startInterval(){
  clearInterval(intervalId);
  intervalId=setInterval(function(){
    if(active<0||paused)return;
    timers[active]--;
    if(timers[active]<=0){timers[active]=0;updateDisplay();clearInterval(intervalId);intervalId=null;}
    updateDisplay();
  },1000);
}
function startTimer(){if(active<0){active=0;updateDisplay();startInterval();}else{paused=false;startInterval();}}
function pauseTimer(){paused=true;if(intervalId){clearInterval(intervalId);intervalId=null;}}
function resetTimer(){
  clearInterval(intervalId);intervalId=null;active=-1;paused=false;
  timers[0]=parseInt(document.getElementById('initMinutes').value)*60;
  timers[1]=parseInt(document.getElementById('initMinutes').value)*60;
  incr=[parseInt(document.getElementById('increment').value),parseInt(document.getElementById('increment').value)];
  document.getElementById('timer1').style.color='#22d3ee';document.getElementById('timer2').style.color='#94a3b8';
  updateDisplay();
}
function applyPreset(){var v=document.getElementById('preset').value;if(!v)return;var p=v.split(',');document.getElementById('initMinutes').value=p[0];document.getElementById('increment').value=p[1];resetTimer();}
updateDisplay();
</script>''',
    'cn_empty': '', 'cn_copied': '', 'en_empty': '', 'en_copied': '',
})

# 4. PX to EM
tools.append({
    'slug': 'pixel-to-em',
    'cn_name': '📐 PX转EM转换器', 'en_name': '📐 PX to EM Converter',
    'cn_desc': '将像素(PX)值转换为EM单位。输入像素值和基准字号，自动计算对应的EM值。',
    'en_desc': 'Convert pixel (PX) values to EM units. Enter pixel value and base font size to get the corresponding EM value.',
    'cn_title': 'PX转EM转换器 - Free ToolBase', 'en_title': 'PX to EM Converter - Free ToolBase',
    'cn_hero': '免费在线PX转EM转换器，帮助前端开发者将像素值转换为响应式EM单位。支持自定义基准字号，查看常用对照表。',
    'en_hero': 'Free online PX to EM converter for frontend developers. Convert pixel values to responsive EM units. Custom base size and common reference table.',
    'cn_badges': '<span class="badge">前端必备</span><span class="badge">批量转换</span><span class="badge">对照表</span>',
    'en_badges': '<span class="badge">Frontend</span><span class="badge">Batch</span><span class="badge">Table</span>',
    'cn_seo': 'PX到EM转换是前端开发常见需求。EM是相对单位，相对于父元素字号。本工具帮助开发者快速将像素值转换为EM。',
    'en_seo': 'PX to EM conversion is a common need in frontend development. EM is a relative unit based on parent font size. This tool helps developers quickly convert pixel values to EM.',
    'body_cn': '''<div class="tool-section"><h2>转换参数</h2><div style="display:flex;gap:12px;flex-wrap:wrap;margin-bottom:12px"><div style="flex:1;min-width:180px"><label style="color:#94a3b8;font-size:.85rem">像素值 (PX)</label><input type="number" id="pxValue" value="16" step="0.1"></div><div style="flex:1;min-width:180px"><label style="color:#94a3b8;font-size:.85rem">基准字号 (PX)</label><input type="number" id="baseSize" value="16" step="1"></div></div></div><div class="tool-section"><h2>转换结果</h2><div class="result-output" id="resultOutput" style="font-size:1.5rem;text-align:center">1em</div><div style="color:#94a3b8;font-size:.85rem;text-align:center;margin-bottom:8px">公式: PX ÷ 基准字号 = EM</div></div><div class="tool-section"><h2>常用对照表 (基准16px)</h2><div style="display:flex;flex-wrap:wrap;gap:4px" id="refTable"></div></div>''',
    'body_en': '''<div class="tool-section"><h2>Conversion Parameters</h2><div style="display:flex;gap:12px;flex-wrap:wrap;margin-bottom:12px"><div style="flex:1;min-width:180px"><label style="color:#94a3b8;font-size:.85rem">Pixel Value (PX)</label><input type="number" id="pxValue" value="16" step="0.1"></div><div style="flex:1;min-width:180px"><label style="color:#94a3b8;font-size:.85rem">Base Font Size (PX)</label><input type="number" id="baseSize" value="16" step="1"></div></div></div><div class="tool-section"><h2>Result</h2><div class="result-output" id="resultOutput" style="font-size:1.5rem;text-align:center">1em</div><div style="color:#94a3b8;font-size:.85rem;text-align:center;margin-bottom:8px">Formula: PX ÷ Base Size = EM</div></div><div class="tool-section"><h2>Common Reference (Base 16px)</h2><div style="display:flex;flex-wrap:wrap;gap:4px" id="refTable"></div></div>''',
    'js': '''<script>
function convertPxToEm(){
  var px=parseFloat(document.getElementById('pxValue').value)||16;
  var base=parseFloat(document.getElementById('baseSize').value)||16;
  if(base<=0)base=16;
  document.getElementById('resultOutput').textContent=(px/base).toFixed(4)+'em';
}
function buildRefTable(){
  var base=parseFloat(document.getElementById('baseSize').value)||16;
  var h='';
  [1,2,4,6,8,10,12,14,16,18,20,24,28,32,36,40,48,56,64,72,80,96].forEach(function(px){
    h+='<span style="display:inline-block;padding:4px 8px;background:#0f172a;border-radius:4px;margin:2px;font-size:.8rem;color:#94a3b8">'+px+'px = <span style="color:#22d3ee">'+(px/base).toFixed(4)+'em</span></span>';
  });
  document.getElementById('refTable').innerHTML=h;
}
document.getElementById('pxValue').addEventListener('input',convertPxToEm);
document.getElementById('baseSize').addEventListener('input',function(){convertPxToEm();buildRefTable();});
convertPxToEm();buildRefTable();
</script>''',
    'cn_empty': '', 'cn_copied': '', 'en_empty': '', 'en_copied': '',
})

# 5. EM to PX
tools.append({
    'slug': 'em-to-px',
    'cn_name': '📏 EM转PX转换器', 'en_name': '📏 EM to PX Converter',
    'cn_desc': '将EM单位转换为像素(PX)值。输入EM值和基准字号，自动计算对应的像素值。',
    'en_desc': 'Convert EM units to pixel (PX) values. Enter EM value and base font size to get the corresponding pixel value.',
    'cn_title': 'EM转PX转换器 - Free ToolBase', 'en_title': 'EM to PX Converter - Free ToolBase',
    'cn_hero': '免费在线EM转PX转换器，将EM单位转换为像素值。支持自定义基准字号。前端开发必备工具。',
    'en_hero': 'Free online EM to PX converter. Convert EM units to pixel values. Custom base font size. Essential tool for frontend developers.',
    'cn_badges': '<span class="badge">前端必备</span><span class="badge">精准快速</span><span class="badge">对照表</span>',
    'en_badges': '<span class="badge">Frontend</span><span class="badge">Precise</span><span class="badge">Table</span>',
    'cn_seo': 'EM到PX转换将相对单位转换为绝对像素值。在CSS中，1em等于当前元素的字号大小。本工具帮助前端开发者快速将EM值转换为像素。',
    'en_seo': 'EM to PX conversion turns relative units into absolute pixel values. In CSS, 1em equals the current font size. This tool helps frontend developers convert EM values to pixels.',
    'body_cn': '''<div class="tool-section"><h2>转换参数</h2><div style="display:flex;gap:12px;flex-wrap:wrap;margin-bottom:12px"><div style="flex:1;min-width:180px"><label style="color:#94a3b8;font-size:.85rem">EM值</label><input type="number" id="emValue" value="1" step="0.01"></div><div style="flex:1;min-width:180px"><label style="color:#94a3b8;font-size:.85rem">基准字号 (PX)</label><input type="number" id="baseSize" value="16" step="1"></div></div></div><div class="tool-section"><h2>转换结果</h2><div class="result-output" id="resultOutput" style="font-size:1.5rem;text-align:center">16px</div><div style="color:#94a3b8;font-size:.85rem;text-align:center;margin-bottom:8px">公式: EM × 基准字号 = PX</div></div><div class="tool-section"><h2>常用对照表 (基准16px)</h2><div style="display:flex;flex-wrap:wrap;gap:4px" id="refTable"></div></div>''',
    'body_en': '''<div class="tool-section"><h2>Conversion Parameters</h2><div style="display:flex;gap:12px;flex-wrap:wrap;margin-bottom:12px"><div style="flex:1;min-width:180px"><label style="color:#94a3b8;font-size:.85rem">EM Value</label><input type="number" id="emValue" value="1" step="0.01"></div><div style="flex:1;min-width:180px"><label style="color:#94a3b8;font-size:.85rem">Base Font Size (PX)</label><input type="number" id="baseSize" value="16" step="1"></div></div></div><div class="tool-section"><h2>Result</h2><div class="result-output" id="resultOutput" style="font-size:1.5rem;text-align:center">16px</div><div style="color:#94a3b8;font-size:.85rem;text-align:center;margin-bottom:8px">Formula: EM × Base Size = PX</div></div><div class="tool-section"><h2>Common Reference (Base 16px)</h2><div style="display:flex;flex-wrap:wrap;gap:4px" id="refTable"></div></div>''',
    'js': '''<script>
function convertEmToPx(){
  var em=parseFloat(document.getElementById('emValue').value)||1;
  var base=parseFloat(document.getElementById('baseSize').value)||16;
  document.getElementById('resultOutput').textContent=(em*base).toFixed(1)+'px';
}
function buildRefTable(){
  var base=parseFloat(document.getElementById('baseSize').value)||16;
  var h='';
  [0.125,0.25,0.375,0.5,0.625,0.75,0.875,1,1.125,1.25,1.5,1.75,2,2.5,3,4,5,6].forEach(function(em){
    h+='<span style="display:inline-block;padding:4px 8px;background:#0f172a;border-radius:4px;margin:2px;font-size:.8rem;color:#94a3b8">'+em+'em = <span style="color:#22d3ee">'+(em*base).toFixed(0)+'px</span></span>';
  });
  document.getElementById('refTable').innerHTML=h;
}
document.getElementById('emValue').addEventListener('input',convertEmToPx);
document.getElementById('baseSize').addEventListener('input',function(){convertEmToPx();buildRefTable();});
convertEmToPx();buildRefTable();
</script>''',
    'cn_empty': '', 'cn_copied': '', 'en_empty': '', 'en_copied': '',
})

# ============ GENERATE ============

for t in tools:
    slug = t['slug']
    js_cn = t['js'].replace('EMPTY', t.get('cn_empty','')).replace('COPIED', t.get('cn_copied',''))
    js_en = t['js'].replace('EMPTY', t.get('en_empty','')).replace('COPIED', t.get('en_copied',''))
    
    # Build HTML (without JS first)
    cn_html = make_page(slug, t['cn_name'], t['en_name'], t['cn_desc'], t['en_desc'], t['cn_title'], t['en_title'],
                       t['cn_hero'], t['en_hero'], t['cn_badges'], t['en_badges'], t['cn_seo'], t['en_seo'],
                       t['body_cn'], t['body_en'], js_cn, lang='cn')
    en_html = make_page(slug, t['cn_name'], t['en_name'], t['cn_desc'], t['en_desc'], t['cn_title'], t['en_title'],
                       t['cn_hero'], t['en_hero'], t['cn_badges'], t['en_badges'], t['cn_seo'], t['en_seo'],
                       t['body_cn'], t['body_en'], js_en, lang='en')

    # Inject JS before </body></html>
    cn_html = cn_html.replace('</body></html>', js_cn + '\n</body></html>')
    en_html = en_html.replace('</body></html>', js_en + '\n</body></html>')

    os.makedirs(f'{BASE}/{slug}', exist_ok=True)
    os.makedirs(f'{BASE}/en/{slug}', exist_ok=True)
    with open(f'{BASE}/{slug}/index.html', 'w') as f: f.write(cn_html)
    with open(f'{BASE}/en/{slug}/index.html', 'w') as f: f.write(en_html)
    print(f'✅ {slug} ({len(cn_html)} bytes CN, {len(en_html)} bytes EN)')

print(f'\n🎉 生成了 {len(tools)} 个工具')