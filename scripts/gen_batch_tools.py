#!/usr/bin/env python3
"""批量生成剩余6个工具的中英文版"""
import os

BASE = '/home/chison/tools-site'
GA = '<script async src="https://www.googletagmanager.com/gtag/js?id=G-9W1157EBQV"></script>\n<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag(\'js\',new Date());gtag(\'config\',\'G-9W1157EBQV\');</script>'
ERR_HANDLER = '<script>window.addEventListener("error",function(e){if(e&&e.message===""){e.preventDefault();}});window.addEventListener("unhandledrejection",function(e){if(e&&e.reason&&e.reason.message===""){e.preventDefault();}});</script>'

CSS = '''<style>
*{box-sizing:border-box;margin:0;padding:0}
body{background:#0f172a;color:#e2e8f0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,{CN_FONT}sans-serif;line-height:1.6;min-height:100vh}
a{color:#06b6d4;text-decoration:none}
.container{max-width:800px;margin:0 auto;padding:24px 16px}
.header{display:flex;justify-content:space-between;align-items:center;margin-bottom:20px;flex-wrap:wrap;gap:12px}
.header h1{font-size:1.6rem;color:#f1f5f9}
.lang-switch{display:flex;gap:4px;background:#1e293b;border-radius:8px;padding:4px;border:1px solid rgba(148,163,184,.1)}
.lang-switch a{padding:6px 12px;border-radius:5px;font-size:.85rem;color:#94a3b8}
.lang-switch a.active{background:rgba(6,182,212,.2);color:#22d3ee}
.nav-back{color:#64748b;font-size:.85rem;margin-bottom:16px}
.panel{background:#1e293b;border-radius:12px;padding:20px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1)}
.panel-title{font-size:1.1rem;color:#f1f5f9;margin-bottom:14px;font-weight:600}
.btn{padding:8px 20px;border:none;border-radius:6px;font-size:.9rem;cursor:pointer;transition:all .2s}
.btn-primary{background:rgba(6,182,212,.2);color:#22d3ee;border:1px solid rgba(6,182,212,.3)}
.btn-primary:hover{background:rgba(6,182,212,.35);transform:translateY(-1px)}
.btn-secondary{background:rgba(148,163,184,.1);color:#94a3b8;border:1px solid rgba(148,163,184,.2)}
.btn-row{display:flex;gap:8px;flex-wrap:wrap;margin-top:12px}
textarea{width:100%;padding:12px;border:1px solid rgba(148,163,184,.2);border-radius:8px;background:#0f172a;color:#e2e8f0;font-size:.9rem;font-family:inherit;resize:vertical;min-height:80px;line-height:1.6}
textarea:focus{outline:none;border-color:#06b6d4}
input[type="number"],input[type="text"]{padding:10px 12px;border:1px solid rgba(148,163,184,.2);border-radius:8px;background:#0f172a;color:#e2e8f0;font-size:.9rem}
input:focus{outline:none;border-color:#06b6d4}
.output-box{padding:16px;background:#0f172a;border-radius:8px;border:1px solid rgba(148,163,184,.1);font-size:1.3rem;min-height:50px;word-break:break-all;color:#22d3ee}
.hero{margin-bottom:20px}
.hero p{color:#94a3b8;font-size:.95rem;line-height:1.7}
.badge{display:inline-block;padding:4px 12px;border-radius:20px;font-size:.75rem;font-weight:600;background:rgba(6,182,212,.1);color:#22d3ee;border:1px solid rgba(6,182,212,.2);margin-top:8px}
.toast{position:fixed;bottom:20px;left:50%;transform:translateX(-50%);background:#1e293b;color:#22d3ee;padding:10px 24px;border-radius:8px;border:1px solid rgba(6,182,212,.3);font-size:.85rem;z-index:999;opacity:0;transition:opacity .3s;pointer-events:none}
.toast.show{opacity:1}
.footer{border-top:1px solid rgba(148,163,184,.1);padding:24px 0;margin-top:48px;text-align:center;color:#64748b;font-size:.85rem}
.footer a{color:#64748b;margin:0 8px}
@media(max-width:640px){.header h1{font-size:1.3rem}}
</style>'''

def head(lang, slug, title_cn, title_en, desc_cn, desc_en, kw_cn, kw_en, app_cat='UtilitiesApplication'):
    cn = lang == 'zh-CN'
    lang_attr = 'zh-CN' if cn else 'en'
    font = '"PingFang SC","Microsoft YaHei",' if cn else ''
    title = title_cn if cn else title_en
    desc = desc_cn if cn else desc_en
    kw = kw_cn if cn else kw_en
    cn_url = f'https://free-toolbase.com/{slug}/'
    en_url = f'https://free-toolbase.com/en/{slug}/'
    canonical = cn_url if cn else en_url
    alt_zh = cn_url
    alt_en = en_url
    x_default = en_url
    app_name = title_cn if cn else title_en
    app_desc = desc_cn if cn else desc_en
    
    return f'''<!DOCTYPE html>
<html lang="{lang_attr}">
<head>
{GA}
{ERR_HANDLER}
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="{desc}">
<meta name="keywords" content="{kw}">
<title>{title} - Free ToolBase</title>
<link rel="canonical" href="{canonical}">
<meta property="og:title" content="{title} - Free ToolBase">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Free ToolBase">
<link rel="alternate" hreflang="zh" href="{alt_zh}">
<link rel="alternate" hreflang="en" href="{alt_en}">
<link rel="alternate" hreflang="x-default" href="{x_default}">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"SoftwareApplication","name":"{app_name}","description":"{app_desc}","applicationCategory":"{app_cat}","operatingSystem":"Web","publisher":{{"@type":"Organization","name":"Free ToolBase","email":"dexshuang@google.com"}},"offers":{{"@type":"Offer","price":"0","priceCurrency":"USD"}}}}</script>
{CSS.replace('{CN_FONT}', font)}'''

def body_start(lang, slug, h1_cn, h1_en, hero_cn, hero_en, badge_cn='🔒 纯前端 · 无数据上传', badge_en='🔒 Client-Side · No Data Upload'):
    cn = lang == 'zh-CN'
    h1 = h1_cn if cn else h1_en
    hero = hero_cn if cn else hero_en
    badge = badge_cn if cn else badge_en
    cn_active = ' class="active"' if cn else ''
    en_active = '' if cn else ' class="active"'
    home = '首页' if cn else 'Home'
    nav_name = h1_cn.split(' - ')[0] if cn else h1_en.split(' - ')[0]
    
    return f'''</head>
<body>
<div class="container">
<div class="header"><h1>{h1}</h1><div class="lang-switch"><a href="../{slug}/" {cn_active}>中文</a><a href="../en/{slug}/" {en_active}>EN</a></div></div>
<p class="nav-back"><a href="../index.html">{home}</a> &rsaquo; <a href="../#tools">Tools</a> &rsaquo; {nav_name}</p>
<div class="hero"><p>{hero} <span class="badge">{badge}</span></p></div>'''

def footer():
    return '''<div class="footer"><p>© 2026 Free ToolBase</p></div>
<div class="toast" id="toast"></div>
</div>'''

def toast_js():
    return '''<script>
function showToast(msg){
  var t=document.getElementById('toast');
  t.textContent=msg;t.classList.add('show');
  setTimeout(function(){t.classList.remove('show');},1500);
}
</script>'''

# ============= 工具1: regional-indicator-text =============
def regional_indicator(lang):
    cn = lang == 'zh-CN'
    slug = 'regional-indicator-text'
    h = head(lang, slug,
        '区域指示符文字生成器', 'Regional Indicator Text Generator',
        '免费在线区域指示符文字生成器。将英文字母转换为国旗表情符号对应的Unicode区域指示符字符(🇦🇧🇨)。',
        'Free online regional indicator text generator. Convert letters to flag emoji Unicode regional indicator symbols (🇦🇧🇨).',
        '区域指示符,国旗文字,Unicode文字,🇦🇧🇨,emoji文字,免费',
        'regional indicator,flag text,unicode text,🇦🇧🇨,emoji text,free')
    b = body_start(lang, slug,
        '🇦 Regional Indicator 区域指示符', '🇦 Regional Indicator Text',
        '将英文字母转换为区域指示符Unicode字符（🇦-🇿），广泛用于国旗表情和社交媒体风格文字。',
        'Convert letters to regional indicator symbols (🇦-🇿), widely used in flag emojis and social media styling.')
    js = '''<script>
var riMap={A:'🇦',B:'🇧',C:'🇨',D:'🇩',E:'🇪',F:'🇫',G:'🇬',H:'🇭',I:'🇮',J:'🇯',K:'🇰',L:'🇱',M:'🇲',N:'🇳',O:'🇴',P:'🇵',Q:'🇶',R:'🇷',S:'🇸',T:'🇹',U:'🇺',V:'🇻',W:'🇼',X:'🇽',Y:'🇾',Z:'🇿',a:'🇦',b:'🇧',c:'🇨',d:'🇩',e:'🇪',f:'🇫',g:'🇬',h:'🇭',i:'🇮',j:'🇯',k:'🇰',l:'🇱',m:'🇲',n:'🇳',o:'🇴',p:'🇵',q:'🇶',r:'🇷',s:'🇸',t:'🇹',u:'🇺',v:'🇻',w:'🇼',x:'🇽',y:'🇾',z:'🇿'};
function convert(text){return text.split('').map(function(c){return riMap[c]||c;}).join('');}
document.getElementById('input').addEventListener('input',function(){document.getElementById('output').textContent=convert(this.value);});
document.getElementById('convertBtn').addEventListener('click',function(){document.getElementById('output').textContent=convert(document.getElementById('input').value);showToast('''' + ('转换完成' if cn else 'Converted!') + ''');});
document.getElementById('copyBtn').addEventListener('click',function(){var t=document.getElementById('output').textContent;if(!t){showToast('''' + ('无内容可复制' if cn else 'Nothing to copy') + ''');return;}navigator.clipboard.writeText(t).then(function(){showToast('''' + ('已复制!' if cn else 'Copied!') + ''');});});
document.getElementById('clearBtn').addEventListener('click',function(){document.getElementById('input').value='';document.getElementById('output').textContent='';});
</script>'''
    panel_title = '✏️ 输入文字' if cn else '✏️ Input'
    placeholder = '输入英文字母，如 Hello' if cn else 'Enter English letters, e.g. Hello'
    btn_convert = '✨ 转换为区域指示符' if cn else '✨ Convert to Regional Indicators'
    btn_copy = '📋 复制结果' if cn else '📋 Copy'
    btn_clear = '🗑 清空' if cn else '🗑 Clear'
    output_label = '📝 输出' if cn else '📝 Output'
    
    content = h + b + f'''
<div class="panel">
  <div class="panel-title">{panel_title}</div>
  <textarea id="input" placeholder="{placeholder}"></textarea>
  <div class="btn-row">
    <button class="btn btn-primary" id="convertBtn">{btn_convert}</button>
    <button class="btn btn-secondary" id="copyBtn">{btn_copy}</button>
    <button class="btn btn-secondary" id="clearBtn">{btn_clear}</button>
  </div>
  <div class="panel-title" style="margin-top:14px">{output_label}</div>
  <div class="output-box" id="output"></div>
</div>''' + footer() + toast_js() + js + '\n</body>\n</html>'
    
    return content

# ============= 工具2: temperature-converter =============
def temperature_converter(lang):
    cn = lang == 'zh-CN'
    slug = 'temperature-converter'
    h = head(lang, slug,
        '温度单位换算器', 'Temperature Converter',
        '免费在线温度单位换算器。摄氏度、华氏度、开尔文三种温度单位互相转换，实时计算。',
        'Free online temperature converter. Convert between Celsius, Fahrenheit, and Kelvin in real time.',
        '温度换算,摄氏度,华氏度,开尔文,℃,℉,K,免费',
        'temperature converter,celsius,fahrenheit,kelvin,℃,℉,K,free')
    b = body_start(lang, slug,
        '🌡️ 温度单位换算器', '🌡️ Temperature Converter',
        '摄氏度(℃)、华氏度(℉)、开尔文(K)三种温度单位实时互转。输入任一温度即可自动计算其他两个。',
        'Convert between Celsius (°C), Fahrenheit (°F), and Kelvin (K) in real time. Enter any value to auto-calculate the others.')
    
    label_c = '摄氏度 (°C)' if cn else 'Celsius (°C)'
    label_f = '华氏度 (°F)' if cn else 'Fahrenheit (°F)'
    label_k = '开尔文 (K)' if cn else 'Kelvin (K)'
    btn_reset = '🔄 重置' if cn else '🔄 Reset'
    js = f'''<script>
var cEl=document.getElementById('celsius'),fEl=document.getElementById('fahrenheit'),kEl=document.getElementById('kelvin'),updating=false;
function cToOthers(v){{updating=true;fEl.value=(v*9/5+32).toFixed(2);kEl.value=(v+273.15).toFixed(2);updating=false;}}
function fToOthers(v){{updating=true;cEl.value=((v-32)*5/9).toFixed(2);kEl.value=((v-32)*5/9+273.15).toFixed(2);updating=false;}}
function kToOthers(v){{updating=true;cEl.value=(v-273.15).toFixed(2);fEl.value=((v-273.15)*9/5+32).toFixed(2);updating=false;}}
cEl.addEventListener('input',function(){{if(updating)return;var v=parseFloat(this.value);if(isNaN(v))return;cToOthers(v);}});
fEl.addEventListener('input',function(){{if(updating)return;var v=parseFloat(this.value);if(isNaN(v))return;fToOthers(v);}});
kEl.addEventListener('input',function(){{if(updating)return;var v=parseFloat(this.value);if(isNaN(v))return;kToOthers(v);}});
document.getElementById('resetBtn').addEventListener('click',function(){{cEl.value='';fEl.value='';kEl.value='';}});
</script>'''
    
    content = h + b + f'''
<div class="panel">
  <div class="panel-title">{label_c}</div>
  <input type="number" id="celsius" placeholder="0" step="any" style="width:100%">
  <div class="panel-title" style="margin-top:14px">{label_f}</div>
  <input type="number" id="fahrenheit" placeholder="32" step="any" style="width:100%">
  <div class="panel-title" style="margin-top:14px">{label_k}</div>
  <input type="number" id="kelvin" placeholder="273.15" step="any" style="width:100%">
  <div class="btn-row"><button class="btn btn-secondary" id="resetBtn">{btn_reset}</button></div>
</div>''' + footer() + toast_js() + js + '\n</body>\n</html>'
    
    return content

# ============= 工具3: reverse-bmi-calculator =============
def reverse_bmi(lang):
    cn = lang == 'zh-CN'
    slug = 'reverse-bmi-calculator'
    h = head(lang, slug,
        '目标体重反算器', 'Reverse BMI Calculator',
        '免费在线BMI反算器。输入身高和目标BMI值，自动计算对应的目标体重。支持公制和英制。',
        'Free online reverse BMI calculator. Enter your height and target BMI to find your goal weight. Supports metric and imperial.',
        'BMI反算,目标体重,BMI计算器,减肥目标,健康体重,免费',
        'reverse BMI,target weight,BMI calculator,goal weight,healthy weight,free')
    b = body_start(lang, slug,
        '⚖️ 目标体重反算器', '⚖️ Reverse BMI Calculator',
        '输入你的身高和目标BMI值，自动计算你需要达到的体重。帮助你设定科学的减肥或增重目标。',
        'Enter your height and target BMI to find your goal weight. Set realistic weight goals based on BMI standards.')
    
    label_height = '身高 (cm)' if cn else 'Height (cm)'
    label_bmi = '目标 BMI' if cn else 'Target BMI'
    label_weight = '目标体重 (kg)' if cn else 'Target Weight (kg)'
    btn_calc = '📐 计算目标体重' if cn else '📐 Calculate Goal Weight'
    result_text = '你的目标体重约为' if cn else 'Your target weight is approximately'
    ph_h = '例如: 170' if cn else 'e.g. 170'
    ph_b = '例如: 22' if cn else 'e.g. 22'
    
    js = f'''<script>
document.getElementById('calcBtn').addEventListener('click',function(){{
  var h=parseFloat(document.getElementById('height').value),b=parseFloat(document.getElementById('bmi').value);
  if(!h||!b){{showToast('{("请输入身高和目标BMI" if cn else "Please enter height and target BMI")}');return;}}
  var w=(b*h*h/10000).toFixed(1);
  document.getElementById('resultBox').textContent='{result_text} '+w+' kg';
}});
</script>'''
    
    content = h + b + f'''
<div class="panel">
  <div class="panel-title">{label_height}</div>
  <input type="number" id="height" placeholder="{ph_h}" step="any" style="width:100%">
  <div class="panel-title" style="margin-top:14px">{label_bmi}</div>
  <input type="number" id="bmi" placeholder="{ph_b}" step="any" style="width:100%">
  <div class="btn-row"><button class="btn btn-primary" id="calcBtn">{btn_calc}</button></div>
  <div class="panel-title" style="margin-top:14px">{label_weight}</div>
  <div class="output-box" id="resultBox" style="font-size:1.5rem;text-align:center">-- kg</div>
</div>
<div class="panel">
  <div class="panel-title">{('📊 BMI参考标准' if cn else '📊 BMI Reference')}</div>
  <div style="display:grid;grid-template-columns:repeat(2,1fr);gap:8px;font-size:.85rem">
    <div style="background:#0f172a;padding:8px 12px;border-radius:6px">{('偏瘦: < 18.5' if cn else 'Underweight: < 18.5')}</div>
    <div style="background:#0f172a;padding:8px 12px;border-radius:6px">{('正常: 18.5 - 24.9' if cn else 'Normal: 18.5 - 24.9')}</div>
    <div style="background:#0f172a;padding:8px 12px;border-radius:6px">{('超重: 25 - 29.9' if cn else 'Overweight: 25 - 29.9')}</div>
    <div style="background:#0f172a;padding:8px 12px;border-radius:6px">{('肥胖: ≥ 30' if cn else 'Obese: ≥ 30')}</div>
  </div>
</div>''' + footer() + toast_js() + js + '\n</body>\n</html>'
    
    return content

# ============= 工具4: ladder-reader =============
def ladder_reader(lang):
    cn = lang == 'zh-CN'
    slug = 'ladder-reader'
    h = head(lang, slug,
        '摸鱼阅读器', 'Stealth Reader',
        '免费在线摸鱼阅读器。将文本以单行滚动方式逐字显示，适合在办公场合悄悄阅读长文。',
        'Free online stealth reader. Display text one word at a time in a single line, perfect for reading at work without being noticed.',
        '摸鱼阅读,逐字阅读,快速阅读,办公阅读,隐身阅读,免费',
        'stealth reader,word reader,speed reading,office reading,privacy reader,free')
    b = body_start(lang, slug,
        '📖 摸鱼阅读器', '📖 Stealth Reader',
        '把长文粘贴进来，逐字滚动显示。适合在办公室悄悄阅读文章，看起来像在看代码或文档！',
        'Paste long text and read it word by word in a single scrolling line. Looks like you\'re reading code or documents!')
    
    label_input = '📝 粘贴文章' if cn else '📝 Paste Article'
    ph = '在此粘贴要阅读的文字...' if cn else 'Paste text to read here...'
    btn_start = '▶ 开始阅读' if cn else '▶ Start Reading'
    btn_pause = '⏸ 暂停' if cn else '⏸ Pause'
    btn_speed = '⚡ 加速' if cn else '⚡ Faster'
    btn_slow = '🐢 减速' if cn else '🐢 Slower'
    btn_prev = '⏪ 上一词' if cn else '⏪ Prev'
    btn_next = '⏩ 下一词' if cn else '⏩ Next'
    speed_label = '速度: ' if cn else 'Speed: '
    
    js = f'''<script>
var words=[],idx=0,speed=300,timer=null,running=false;
function updateDisplay(){{if(idx<words.length)document.getElementById('readerDisplay').textContent=words[idx];else{{pauseReader();document.getElementById('readerDisplay').textContent='{('阅读完成!' if cn else 'Done reading!')}';}}}}
function startReader(){{if(words.length===0){{var text=document.getElementById('inputText').value.trim();if(!text){{showToast('{('请先粘贴文字' if cn else 'Paste some text first')}');return;}}words=text.split(/\\s+/).filter(function(w){{return w.length>0;}});idx=0;}}running=true;timer=setInterval(function(){{idx++;updateDisplay();}},speed);document.getElementById('startBtn').style.display='none';document.getElementById('pauseBtn').style.display='';}}
function pauseReader(){{running=false;clearInterval(timer);document.getElementById('startBtn').style.display='';document.getElementById('pauseBtn').style.display='none';}}
document.getElementById('startBtn').addEventListener('click',startReader);
document.getElementById('pauseBtn').addEventListener('click',pauseReader);
document.getElementById('fasterBtn').addEventListener('click',function(){{speed=Math.max(50,speed-50);document.getElementById('speedLabel').textContent='{speed_label}'+speed+'ms';if(running){{pauseReader();startReader();}}}});
document.getElementById('slowerBtn').addEventListener('click',function(){{speed=Math.min(1000,speed+50);document.getElementById('speedLabel').textContent='{speed_label}'+speed+'ms';if(running){{pauseReader();startReader();}}}});
document.getElementById('prevBtn').addEventListener('click',function(){{if(idx>0){{idx--;updateDisplay();}}}});
document.getElementById('nextBtn').addEventListener('click',function(){{if(idx<words.length-1){{idx++;updateDisplay();}}}});
</script>'''
    
    content = h + b + f'''
<div class="panel">
  <div class="panel-title">{label_input}</div>
  <textarea id="inputText" placeholder="{ph}" style="min-height:100px"></textarea>
  <div class="panel" style="background:#0f172a;text-align:center;padding:20px;margin-top:12px">
    <div id="readerDisplay" style="font-size:1.8rem;color:#22d3ee;font-weight:700;min-height:60px;line-height:60px;word-break:break-all">{('等待开始...' if cn else 'Waiting to start...')}</div>
  </div>
  <div class="btn-row" style="justify-content:center">
    <button class="btn btn-primary" id="startBtn">{btn_start}</button>
    <button class="btn btn-primary" id="pauseBtn" style="display:none">{btn_pause}</button>
    <button class="btn btn-secondary" id="prevBtn">{btn_prev}</button>
    <button class="btn btn-secondary" id="nextBtn">{btn_next}</button>
  </div>
  <div class="btn-row" style="justify-content:center">
    <button class="btn btn-secondary" id="slowerBtn">{btn_slow}</button>
    <span id="speedLabel" style="color:#94a3b8;line-height:36px">{speed_label}300ms</span>
    <button class="btn btn-secondary" id="fasterBtn">{btn_speed}</button>
  </div>
</div>''' + footer() + toast_js() + js + '\n</body>\n</html>'
    
    return content

# ============= 工具5: html-entity-codec =============
def html_entity_codec(lang):
    cn = lang == 'zh-CN'
    slug = 'html-entity-codec'
    h = head(lang, slug,
        'HTML实体编解码器', 'HTML Entity Encoder/Decoder',
        '免费在线HTML实体编解码工具。一键将特殊字符编码为HTML实体或解码回原始字符。',
        'Free online HTML entity encoder/decoder. Encode special characters to HTML entities or decode them back instantly.',
        'HTML实体,HTML编码,HTML解码,实体转换,&amp;&lt;&gt;,免费',
        'html entity,html encode,html decode,entity converter,&amp;&lt;&gt;,free')
    b = body_start(lang, slug,
        '🔐 HTML实体编解码器', '🔐 HTML Entity Encoder/Decoder',
        'HTML实体编码与解码双向转换。将<>&"等特殊字符转为&amp;lt;&amp;gt;等实体，或反向解码。',
        'Encode and decode HTML entities. Convert special characters like <>&" to &amp;lt;&amp;gt; entities and back.')
    
    label_input = '✏️ 输入' if cn else '✏️ Input'
    ph_input = '输入文本或HTML实体...' if cn else 'Enter text or HTML entities...'
    btn_encode = '🔒 编码为实体' if cn else '🔒 Encode to Entities'
    btn_decode = '🔓 解码为字符' if cn else '🔓 Decode to Characters'
    btn_copy = '📋 复制结果' if cn else '📋 Copy'
    btn_clear = '🗑 清空' if cn else '🗑 Clear'
    label_output = '📝 输出' if cn else '📝 Output'
    
    js = f'''<script>
function encodeHTML(text){{var d=document.createElement('div');d.textContent=text;return d.innerHTML;}}
function decodeHTML(html){{var d=document.createElement('div');d.innerHTML=html;return d.textContent;}}
document.getElementById('encodeBtn').addEventListener('click',function(){{var input=document.getElementById('inputText').value;document.getElementById('outputBox').textContent=encodeHTML(input);showToast('{('编码完成' if cn else 'Encoded!')}');}});
document.getElementById('decodeBtn').addEventListener('click',function(){{var input=document.getElementById('inputText').value;document.getElementById('outputBox').textContent=decodeHTML(input);showToast('{('解码完成' if cn else 'Decoded!')}');}});
document.getElementById('copyBtn').addEventListener('click',function(){{var t=document.getElementById('outputBox').textContent;if(!t){{showToast('{('无内容' if cn else 'Nothing to copy')}');return;}}navigator.clipboard.writeText(t).then(function(){{showToast('{('已复制!' if cn else 'Copied!')}');}});}});
document.getElementById('clearBtn').addEventListener('click',function(){{document.getElementById('inputText').value='';document.getElementById('outputBox').textContent='';}});
document.getElementById('inputText').addEventListener('input',function(){{document.getElementById('outputBox').textContent=encodeHTML(this.value);}});
</script>'''
    
    content = h + b + f'''
<div class="panel">
  <div class="panel-title">{label_input}</div>
  <textarea id="inputText" placeholder="{ph_input}"></textarea>
  <div class="btn-row">
    <button class="btn btn-primary" id="encodeBtn">{btn_encode}</button>
    <button class="btn btn-primary" id="decodeBtn">{btn_decode}</button>
    <button class="btn btn-secondary" id="copyBtn">{btn_copy}</button>
    <button class="btn btn-secondary" id="clearBtn">{btn_clear}</button>
  </div>
  <div class="panel-title" style="margin-top:14px">{label_output}</div>
  <div class="output-box" id="outputBox" style="font-family:monospace;font-size:.95rem"></div>
</div>
<div class="panel">
  <div class="panel-title">{('📖 常见实体参考' if cn else '📖 Common Entities')}</div>
  <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(120px,1fr));gap:8px;font-size:.85rem;font-family:monospace">
    <div style="background:#0f172a;padding:6px 10px;border-radius:4px"><code style="color:#22d3ee">&amp;lt;</code> &lt;</div>
    <div style="background:#0f172a;padding:6px 10px;border-radius:4px"><code style="color:#22d3ee">&amp;gt;</code> &gt;</div>
    <div style="background:#0f172a;padding:6px 10px;border-radius:4px"><code style="color:#22d3ee">&amp;amp;</code> &amp;</div>
    <div style="background:#0f172a;padding:6px 10px;border-radius:4px"><code style="color:#22d3ee">&amp;quot;</code> &quot;</div>
    <div style="background:#0f172a;padding:6px 10px;border-radius:4px"><code style="color:#22d3ee">&amp;apos;</code> &apos;</div>
    <div style="background:#0f172a;padding:6px 10px;border-radius:4px"><code style="color:#22d3ee">&amp;nbsp;</code> (space)</div>
    <div style="background:#0f172a;padding:6px 10px;border-radius:4px"><code style="color:#22d3ee">&amp;copy;</code> &copy;</div>
    <div style="background:#0f172a;padding:6px 10px;border-radius:4px"><code style="color:#22d3ee">&amp;reg;</code> &reg;</div>
  </div>
</div>''' + footer() + toast_js() + js + '\n</body>\n</html>'
    
    return content


# 批量生成
tools = {
    'regional-indicator-text': regional_indicator,
    'temperature-converter': temperature_converter,
    'reverse-bmi-calculator': reverse_bmi,
    'ladder-reader': ladder_reader,
    'html-entity-codec': html_entity_codec,
}

for slug, func in tools.items():
    # CN
    cn_path = os.path.join(BASE, slug, 'index.html')
    cn_content = func('zh-CN')
    os.makedirs(os.path.dirname(cn_path), exist_ok=True)
    with open(cn_path, 'w') as f:
        f.write(cn_content)
    print(f'  CN {slug} done')
    
    # EN
    en_path = os.path.join(BASE, 'en', slug, 'index.html')
    en_content = func('en')
    os.makedirs(os.path.dirname(en_path), exist_ok=True)
    with open(en_path, 'w') as f:
        f.write(en_content)
    print(f'  EN {slug} done')

print('\nAll 5 tools generated (10 files total)!')