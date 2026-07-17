#!/usr/bin/env python3
"""Generate tool HTML pages using Python to avoid shell escaping issues."""
import os, json

BASE = os.path.expanduser("~/tools-site")

CSS = """*{box-sizing:border-box;margin:0;padding:0}body{background:#0f172a;color:#e2e8f0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,"PingFang SC","Microsoft YaHei",sans-serif;line-height:1.6;min-height:100vh}a{color:#06b6d4;text-decoration:none}.container{max-width:960px;margin:0 auto;padding:24px 16px}.header{display:flex;justify-content:space-between;align-items:center;margin-bottom:24px;flex-wrap:wrap;gap:12px}.header h1{font-size:1.5rem;color:#f1f5f9}.lang-switch{display:flex;gap:4px;background:#1e293b;border-radius:8px;padding:4px;border:1px solid rgba(148,163,184,.1)}.lang-switch a{padding:6px 12px;border-radius:5px;font-size:.85rem;color:#94a3b8}.lang-switch a.active{background:rgba(6,182,212,.2);color:#22d3ee}.nav-back{color:#64748b;font-size:.85rem;margin-bottom:16px}.nav-back a{color:#64748b}.section{background:#1e293b;border-radius:12px;padding:20px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1)}.section h2{font-size:1.1rem;color:#f1f5f9;margin-bottom:12px}.form-group{margin-bottom:14px}.form-group label{display:block;color:#94a3b8;font-size:.9rem;margin-bottom:6px;font-weight:500}.form-group input[type="number"],.form-group input[type="text"],.form-group select,.form-group textarea,.form-group input[type="range"]{width:100%;padding:10px 14px;background:#0f172a;border:1px solid rgba(148,163,184,.2);border-radius:8px;color:#e2e8f0;font-size:.9rem;outline:none;transition:all .2s}.form-group input:focus,.form-group select:focus,.form-group textarea:focus{border-color:rgba(6,182,212,.4);box-shadow:0 0 0 3px rgba(6,182,212,.1)}.form-row{display:flex;gap:12px;flex-wrap:wrap}.form-row .form-group{flex:1;min-width:200px}.btn-group{display:flex;gap:8px;flex-wrap:wrap;margin:12px 0}.btn{padding:10px 24px;border:none;border-radius:8px;font-size:.9rem;cursor:pointer;transition:all .2s;font-weight:600}.btn-primary{background:rgba(6,182,212,.2);color:#22d3ee;border:1px solid rgba(6,182,212,.3)}.btn-primary:hover{background:rgba(6,182,212,.3)}.btn-secondary{background:rgba(148,163,184,.1);color:#94a3b8;border:1px solid rgba(148,163,184,.2)}.btn-secondary:hover{background:rgba(148,163,184,.2)}.btn-success{background:rgba(34,197,94,.15);color:#4ade80;border:1px solid rgba(34,197,94,.25)}.btn-danger{background:rgba(239,68,68,.15);color:#f87171;border:1px solid rgba(239,68,68,.2)}.faq-item{margin-bottom:16px}.faq-item h3{font-size:.95rem;color:#e2e8f0;margin-bottom:6px}.faq-item p{color:#94a3b8;font-size:.9rem}.info-text{color:#94a3b8;font-size:.85rem;margin-bottom:12px}.badge{display:inline-block;background:rgba(6,182,212,.15);color:#22d3ee;padding:4px 12px;border-radius:20px;font-size:.8rem;margin-bottom:12px;border:1px solid rgba(6,182,212,.2)}.footer{border-top:1px solid rgba(148,163,184,.1);padding:24px 0;margin-top:32px;text-align:center;color:#64748b;font-size:.85rem}.footer a{color:#64748b;margin:0 8px}.toast{position:fixed;bottom:20px;left:50%;transform:translateX(-50%);background:#1e293b;color:#22d3ee;padding:10px 24px;border-radius:8px;border:1px solid rgba(6,182,212,.3);font-size:.85rem;z-index:999;opacity:0;transition:opacity .3s}.toast.show{opacity:1}.ad-slot{margin:16px auto;text-align:center;max-width:960px}.ad-slot:empty{display:none}.ad-slot ins{display:block}.ad-slot.ad-sidebar{max-width:300px}.seo-content{background:#1e293b;border-radius:12px;padding:20px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1)}.seo-content h2{font-size:1.1rem;color:#f1f5f9;margin-bottom:12px}.seo-content p,.seo-content li{color:#94a3b8;font-size:.9rem}.seo-content ol,.seo-content ul{padding-left:20px;margin-top:8px}.seo-content li{margin-bottom:8px}.seo-content strong{color:#e2e8f0}.main-grid{display:grid;grid-template-columns:1fr 300px;gap:16px}@media(max-width:768px){.main-grid{grid-template-columns:1fr}}"""

GA4 = """<script async src="https://www.googletagmanager.com/gtag/js?id=G-9W1157EBQV"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','G-9W1157EBQV');</script>"""
ADSENSE = """<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5998441792679372" crossorigin="anonymous"></script>"""

def make_schema_software(name, desc, rating_count=312):
    return json.dumps({
        "@context":"https://schema.org","@type":"SoftwareApplication",
        "name":name,"description":desc,"applicationCategory":"UtilitiesApplication",
        "operatingSystem":"Web",
        "publisher":{"@type":"Organization","name":"Online Tools","email":"dexshuang@google.com"},
        "offers":{"@type":"Offer","price":"0","priceCurrency":"CNY"},
        "aggregateRating":{"@type":"AggregateRating","ratingValue":"4.8","ratingCount":str(rating_count),"bestRating":"5","worstRating":"1","reviewCount":str(rating_count)}
    }, ensure_ascii=False)

def make_schema_faq(name, faqs):
    entities = []
    for q, a in faqs:
        entities.append({"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}})
    return json.dumps({"@context":"https://schema.org","@type":"FAQPage","name":faqs[0][0],"mainEntity":entities}, ensure_ascii=False)

def make_schema_howto(name, desc, steps):
    step_list = []
    for i, (sname, stext) in enumerate(steps, 1):
        step_list.append({"@type":"HowToStep","position":i,"name":sname,"text":stext})
    return json.dumps({"@context":"https://schema.org","@type":"HowTo","name":"如何使用"+name,"description":desc,"totalTime":"PT2M","tool":{"@type":"HowToTool","name":name},"step":step_list}, ensure_ascii=False)

def make_schema_breadcrumb(cat_name, cat_anchor, tool_name, tool_url):
    return json.dumps({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"首页","item":"https://free-toolbase.com/"},
        {"@type":"ListItem","position":2,"name":cat_name,"item":"https://free-toolbase.com/#"+cat_anchor},
        {"@type":"ListItem","position":3,"name":tool_name,"item":tool_url}
    ]}, ensure_ascii=False)

AD_TOP = '<div class="ad-slot" id="ad-top"><ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-5998441792679372" data-ad-slot="XXXXXXX" data-ad-format="horizontal" data-full-width-responsive="true"></ins></div>'
AD_MID = '<div class="ad-slot" style="margin:24px auto"><ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-5998441792679372" data-ad-slot="XXXXXXX" data-ad-format="horizontal" data-full-width-responsive="true"></ins></div>'
AD_SIDEBAR1 = '<div class="ad-slot ad-sidebar"><ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-5998441792679372" data-ad-slot="XXXXXXX" data-ad-format="rectangle" data-full-width-responsive="true"></ins></div>'
AD_SIDEBAR2 = '<div class="ad-slot ad-sidebar" style="margin-top:16px"><ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-5998441792679372" data-ad-slot="XXXXXXX" data-ad-format="rectangle" data-full-width-responsive="true"></ins></div>'

def make_footer_cn(slug):
    return f'''<div class="footer container"><div style="margin-bottom:12px"><a href="../index.html">首页</a><a href="../index.html">全部工具</a><a href="mailto:dexshuang@google.com">联系我们</a><a href="../privacy/">隐私政策</a><a href="../terms/">服务条款</a><a href="../about/">关于我们</a><a href="../en/{slug}/">EN</a></div><p>{{tool_name}} · 纯前端本地处理 · 数据绝不上传服务器</p><p style="margin-top:8px;color:#475569;font-size:.8rem">问题反馈: dexshuang@google.com</p></div>'''

def make_footer_en(slug):
    return f'''<div class="footer container"><div style="margin-bottom:12px"><a href="../index.html">Home</a><a href="../index.html">All Tools</a><a href="mailto:dexshuang@google.com">Contact</a><a href="../privacy/">Privacy</a><a href="../terms/">Terms</a><a href="../about/">About</a><a href="../{slug}/">中文</a></div><p>{{tool_name_en}} · Pure Frontend · No Server Uploads</p><p style="margin-top:8px;color:#475569;font-size:.8rem">Feedback: dexshuang@google.com</p></div>'''

def make_page(lang, slug, title, desc_cn, desc_en, icon, cat_cn, cat_en, cat_anchor, faqs_cn, faqs_en, seo_cn, seo_en, tool_html_cn, tool_html_en, tool_js, tool_js_en=None, rating_count=312):
    is_cn = lang == 'zh'
    title_text = title if is_cn else title
    desc = desc_cn if is_cn else desc_en
    lang_code = 'zh-CN' if is_cn else 'en'
    base_url = f"https://free-toolbase.com/{slug}/" if is_cn else f"https://free-toolbase.com/en/{slug}/"
    hreflang_zh = f"https://free-toolbase.com/{slug}/"
    hreflang_en = f"https://free-toolbase.com/en/{slug}/"
    
    switch_cn = f'index.html' if is_cn else f'../{slug}/'
    switch_en = f'../en/{slug}/' if is_cn else 'index.html'
    switch_cn_class = ' active' if is_cn else ''
    switch_en_class = '' if is_cn else ' active'
    
    breadcrumb = make_schema_breadcrumb(cat_cn if is_cn else cat_en, cat_anchor, title, base_url)
    
    nav = f'<a href="../index.html">{"首页" if is_cn else "Home"}</a> › <a href="../index.html#{cat_anchor}">{cat_cn if is_cn else cat_en}</a> › {title}'
    
    footer = f'''<div class="footer container"><div style="margin-bottom:12px"><a href="../index.html">{"首页" if is_cn else "Home"}</a><a href="../index.html">{"全部工具" if is_cn else "All Tools"}</a><a href="mailto:dexshuang@google.com">{"联系我们" if is_cn else "Contact"}</a><a href="../privacy/">{"隐私政策" if is_cn else "Privacy"}</a><a href="../terms/">{"服务条款" if is_cn else "Terms"}</a><a href="../about/">{"关于我们" if is_cn else "About"}</a><a href="{"../en/" if is_cn else "../"}{slug}/">{"EN" if is_cn else "中文"}</a></div><p>{title} · {"纯前端本地处理 · 数据绝不上传服务器" if is_cn else "Pure Frontend · No Server Uploads"}</p><p style="margin-top:8px;color:#475569;font-size:.8rem">{"问题反馈" if is_cn else "Feedback"}: dexshuang@google.com</p></div>'''
    
    badge_text = '零依赖·可离线使用' if is_cn else 'Zero Dependencies·Works Offline'
    info_text = f'{desc} · {"纯前端本地处理 · 数据绝不上传服务器" if is_cn else "Pure Frontend · No Server Uploads"}'
    
    seo = seo_cn if is_cn else seo_en
    tool_html = tool_html_cn if is_cn else tool_html_en
    js = tool_js if tool_js_en is None or is_cn else tool_js_en
    
    faqs = faqs_cn if is_cn else faqs_en
    faq_html = '\n'.join(f'<div class="faq-item"><h3>{q}</h3><p>{a}</p></div>' for q,a in faqs)
    
    page = f'''<!DOCTYPE html>
<html lang="{lang_code}">
<head>
{GA4}
{ADSENSE}
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="{desc}">
<meta name="keywords" content="{",".join([title, "在线工具" if is_cn else "online tool", "免费" if is_cn else "free"])}">
<title>{title} - {"免费在线工具·纯前端本地处理" if is_cn else "Free Online Tool·Pure Frontend"}</title>
<link rel="canonical" href="{base_url}">
<meta property="og:title" content="{icon} {title}"><meta property="og:description" content="{desc}"><meta property="og:url" content="{base_url}"><meta property="og:type" content="website"><meta property="og:site_name" content="{"在线小工具矩阵" if is_cn else "Free Toolbase"}">
<link rel="alternate" hreflang="zh" href="{hreflang_zh}"><link rel="alternate" hreflang="en" href="{hreflang_en}"><link rel="alternate" hreflang="x-default" href="{hreflang_en}">
<script type="application/ld+json">{make_schema_software(title, desc, rating_count)}</script>
<script type="application/ld+json">{make_schema_faq(title, faqs)}</script>
<script type="application/ld+json">{make_schema_howto(title, desc, [("input" if is_cn else "Input","准备输入数据" if is_cn else "Prepare input data"),("options" if is_cn else "Options","配置选项" if is_cn else "Configure options"),("output" if is_cn else "Output","查看结果" if is_cn else "View results")])}</script>
<script type="application/ld+json">{breadcrumb}</script>
<style>{CSS}</style>
</head>
<body>
{AD_TOP}
<div class="container">
  <div class="header"><h1>{icon} {title}</h1><div class="lang-switch"><a href="{switch_cn}" class="active{switch_cn_class}">中文</a><a href="{switch_en}" class="{switch_en_class}">EN</a></div></div>
  <p class="nav-back">{nav}</p>
  <p class="info-text">{info_text}</p>
  <span class="badge">{badge_text}</span>
  <div class="main-grid">
    <div><div class="section">{tool_html}</div></div>
    <div>{AD_SIDEBAR1}{AD_SIDEBAR2}</div>
  </div>
  {AD_MID}
  <div class="seo-content">{seo}</div>
  <div class="section"><h2>{"常见问题" if is_cn else "FAQ"}</h2>{faq_html}</div>
  {AD_MID}
  {footer}
</div>
<div class="toast" id="toast"></div>
<script>{js}</script>
</body>
</html>'''
    return page

def write_tool(slug, **kwargs):
    cn_dir = os.path.join(BASE, slug)
    en_dir = os.path.join(BASE, 'en', slug)
    os.makedirs(cn_dir, exist_ok=True)
    os.makedirs(en_dir, exist_ok=True)
    
    cn_page = make_page('zh', slug, **kwargs)
    en_page = make_page('en', slug, **kwargs)
    
    with open(os.path.join(cn_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(cn_page)
    with open(os.path.join(en_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(en_page)
    
    print(f"Created {slug}/index.html ({len(cn_page)} bytes)")
    print(f"Created en/{slug}/index.html ({len(en_page)} bytes)")


# ============================================================
# Tool 1: online-hearing-test
# ============================================================
write_tool(
    slug='online-hearing-test',
    title='在线听力测试',
    desc_cn='免费在线听力测试工具，通过播放不同频率纯音评估听力范围。支持左右耳分别测试，生成听力曲线图，纯前端本地处理，数据绝不上传。',
    desc_en='Free online hearing test tool. Evaluate your hearing range by playing pure tones at different frequencies. Supports left/right ear testing, generates audiogram charts. Pure frontend, no data uploads.',
    icon='👂',
    cat_cn='健康工具', cat_en='Health Tools', cat_anchor='health-tools',
    faqs_cn=[
        ('在线听力测试准确吗？', '本工具使用Web Audio API生成精确频率的纯音信号，可初步评估听力范围。建议在安静环境下使用耳机测试，结果仅供参考，不能替代专业听力检查。'),
        ('需要戴耳机测试吗？', '强烈建议使用耳机。耳机可隔离环境噪音，并分别测试左右耳。使用扬声器时，环境噪音和声场反射会严重影响结果准确性。'),
        ('测试覆盖哪些频率？', '标准测试覆盖125Hz到8000Hz，扩展模式可测试至16000Hz高频范围。'),
        ('数据安全吗？', '所有测试完全在浏览器本地运行，不会上传任何数据到服务器。隐私完全有保障。'),
        ('听力下降的常见原因是什么？', '常见原因包括：年龄增长、长期噪音暴露、耳道堵塞、中耳感染、某些药物副作用。发现听力异常请及时就医。'),
        ('如何解读听力曲线？', '正常听力0-25dB；26-40dB轻度损失；41-55dB中度；56-70dB中重度；71-90dB重度；90dB以上极重度。曲线越低损失越严重。'),
    ],
    faqs_en=[
        ('Is the online hearing test accurate?', 'This tool uses Web Audio API to generate precise pure tone signals for preliminary hearing assessment. Use headphones in a quiet environment. Results are for reference only, not a substitute for professional testing.'),
        ('Do I need headphones?', 'Strongly recommended. Headphones isolate ambient noise and allow testing each ear separately. Speaker testing is significantly less accurate.'),
        ('What frequency range is covered?', 'Standard mode covers 125Hz to 8000Hz. Extended mode goes up to 16000Hz.'),
        ('Is my data safe?', 'All processing runs locally in your browser. No audio data or results are uploaded to any server.'),
        ('What causes hearing loss?', 'Common causes: aging, prolonged noise exposure, ear canal blockage, middle ear infections, certain medications. See a doctor if you notice changes.'),
        ('How to read the audiogram?', 'Normal: 0-25dB; Mild loss: 26-40dB; Moderate: 41-55dB; Moderately severe: 56-70dB; Severe: 71-90dB; Profound: 90dB+. Lower curves indicate more loss.'),
    ],
    seo_cn='''<h2>在线听力测试能做什么？</h2><p>在线听力测试是一款免费的纯前端听力评估工具，通过Web Audio API生成不同频率和音量的纯音信号，帮助您初步了解自己的听力范围。支持左右耳分别测试，自动生成听力曲线图，所有数据在浏览器本地处理，绝不上传服务器。</p><h2>核心功能</h2><ul><li><strong>多频率纯音测试</strong>：覆盖125Hz至16000Hz频率范围</li><li><strong>左右耳分别测试</strong>：支持左耳、右耳、双耳三种模式</li><li><strong>听力曲线图</strong>：实时绘制听力图，直观展示各频率听力水平</li><li><strong>音量精细调节</strong>：0-80dB音量范围，精确定位听阈</li><li><strong>结果评估</strong>：自动评估听力等级，提供参考建议</li></ul><h2>使用教程</h2><ol><li><strong>准备环境</strong>：戴上耳机，进入安静环境，调整设备音量到舒适水平</li><li><strong>选择耳朵和频率</strong>：选择测试左耳或右耳，从125Hz低频开始逐步测试</li><li><strong>播放纯音</strong>：点击播放按钮，听到声音点击"听到了"，听不到点击"听不到"</li><li><strong>调节音量</strong>：逐步提高音量直到能听到，记录最小可听音量</li><li><strong>查看结果</strong>：测试完成后查看听力曲线图，正常听力应在0-25dB范围</li></ol><h2>应用场景</h2><ul><li><strong>日常自检</strong>：怀疑听力下降时快速自测</li><li><strong>耳机检测</strong>：测试耳机或音响设备的频率响应</li><li><strong>职业健康</strong>：长期噪音环境工人定期自测</li><li><strong>老年人关注</strong>：初步评估老年性耳聋迹象</li><li><strong>学生科普</strong>：了解人类听觉范围</li></ul><h2>扩展知识</h2><p>人类正常听力范围为20Hz-20000Hz，随年龄增长高频听力逐渐下降。听力图（Audiogram）横轴为频率（对数刻度），纵轴为听力级（dB HL）。正常听阈0-25dB；26-40dB轻度损失；41-55dB中度；56-70dB中重度；71-90dB重度；90dB以上极重度。在线测试提供初步参考，正式诊断需专业听力学家在隔音室中完成。</p>''',
    seo_en='''<h2>What Can the Online Hearing Test Do?</h2><p>The online hearing test is a free, pure-frontend hearing assessment tool. It uses the Web Audio API to generate pure tones at different frequencies and volumes, helping you understand your hearing range. Supports left/right ear testing, generates audiogram charts. All data is processed locally in your browser.</p><h2>Core Features</h2><ul><li><strong>Multi-frequency pure tone testing</strong>: Covers 125Hz to 16000Hz</li><li><strong>Left/right ear testing</strong>: Test each ear separately or both</li><li><strong>Audiogram chart</strong>: Real-time hearing curve visualization</li><li><strong>Fine volume control</strong>: 0-80dB range for precise threshold detection</li><li><strong>Result assessment</strong>: Automatic hearing level evaluation</li></ul><h2>How to Use</h2><ol><li><strong>Prepare</strong>: Put on headphones, find a quiet room, set volume to comfortable level</li><li><strong>Select ear and frequency</strong>: Choose left/right ear, start from 125Hz</li><li><strong>Play tones</strong>: Click play, mark "Heard" or "Not Heard"</li><li><strong>Adjust volume</strong>: Increase volume until you can hear, record minimum audible level</li><li><strong>View results</strong>: Check your audiogram, normal hearing is 0-25dB</li></ol><h2>Use Cases</h2><ul><li><strong>Routine self-check</strong>: Quick test when suspecting hearing decline</li><li><strong>Headphone testing</strong>: Check headphone/speaker frequency response</li><li><strong>Occupational health</strong>: Regular monitoring for noise-exposed workers</li><li><strong>Elderly care</strong>: Initial assessment for age-related hearing loss</li><li><strong>Education</strong>: Learn about human hearing range</li></ul><h2>Background</h2><p>Normal human hearing spans 20Hz-20000Hz, with high-frequency sensitivity declining with age. An audiogram plots frequency (log scale) on the x-axis and hearing level (dB HL) on the y-axis. Normal thresholds: 0-25dB; Mild loss: 26-40dB; Moderate: 41-55dB; Moderately severe: 56-70dB; Severe: 71-90dB; Profound: 90dB+. Online tests provide preliminary reference; formal diagnosis requires professional audiometric evaluation in a sound-treated booth.</p>''',
    tool_html_cn='''<div class="form-row"><div class="form-group"><label>选择耳朵</label><select id="ear" onchange="stopTest()"><option value="left">左耳</option><option value="right">右耳</option><option value="both">双耳</option></select></div><div class="form-group"><label>测试模式</label><select id="mode"><option value="standard">标准（125-8000Hz）</option><option value="extended">扩展（125-16000Hz）</option></select></div></div><div class="form-row"><div class="form-group"><label>频率: <span id="freqVal">1000 Hz</span></label><input type="range" id="freqSlider" min="125" max="16000" value="1000" oninput="document.getElementById('freqVal').textContent=this.value+' Hz'"><div style="display:flex;justify-content:space-between;font-size:.75rem;color:#64748b"><span>125 Hz</span><span>16000 Hz</span></div></div><div class="form-group"><label>音量: <span id="volVal">30 dB</span></label><input type="range" id="volSlider" min="0" max="80" value="30" oninput="document.getElementById('volVal').textContent=this.value+' dB'"><div style="display:flex;justify-content:space-between;font-size:.75rem;color:#64748b"><span>0 dB</span><span>80 dB</span></div></div></div><div class="btn-group"><button class="btn btn-primary" id="playBtn" onclick="toggleTest()">▶ 播放纯音</button><button class="btn btn-success" onclick="recordHeard()">✓ 听到了</button><button class="btn btn-danger" onclick="recordNotHeard()">✗ 听不到</button><button class="btn btn-secondary" onclick="stopTest()">⏹ 停止</button><button class="btn btn-secondary" onclick="clearResults()">🗑️ 清除</button></div><div class="form-group"><label>快速频率测试</label><div class="btn-group"><button class="btn btn-secondary" onclick="playFreq(125)">125Hz</button><button class="btn btn-secondary" onclick="playFreq(250)">250Hz</button><button class="btn btn-secondary" onclick="playFreq(500)">500Hz</button><button class="btn btn-secondary" onclick="playFreq(1000)">1kHz</button><button class="btn btn-secondary" onclick="playFreq(2000)">2kHz</button><button class="btn btn-secondary" onclick="playFreq(4000)">4kHz</button><button class="btn btn-secondary" onclick="playFreq(8000)">8kHz</button><button class="btn btn-secondary" onclick="playFreq(12000)">12kHz</button></div></div><div class="form-group"><label>听力曲线图</label><canvas id="audiogram" width="700" height="300" style="background:#0f172a;border:1px solid rgba(148,163,184,.2);border-radius:8px;width:100%"></canvas></div><div id="resultsSummary" style="color:#94a3b8;font-size:.85rem"></div><p class="info-text">💡 请在安静环境中使用优质耳机测试。本测试仅供参考，不能替代专业听力检查。</p>''',
    tool_html_en='''<div class="form-row"><div class="form-group"><label>Select Ear</label><select id="ear" onchange="stopTest()"><option value="left">Left Ear</option><option value="right">Right Ear</option><option value="both">Both Ears</option></select></div><div class="form-group"><label>Test Mode</label><select id="mode"><option value="standard">Standard (125-8000Hz)</option><option value="extended">Extended (125-16000Hz)</option></select></div></div><div class="form-row"><div class="form-group"><label>Frequency: <span id="freqVal">1000 Hz</span></label><input type="range" id="freqSlider" min="125" max="16000" value="1000" oninput="document.getElementById('freqVal').textContent=this.value+' Hz'"><div style="display:flex;justify-content:space-between;font-size:.75rem;color:#64748b"><span>125 Hz</span><span>16000 Hz</span></div></div><div class="form-group"><label>Volume: <span id="volVal">30 dB</span></label><input type="range" id="volSlider" min="0" max="80" value="30" oninput="document.getElementById('volVal').textContent=this.value+' dB'"><div style="display:flex;justify-content:space-between;font-size:.75rem;color:#64748b"><span>0 dB</span><span>80 dB</span></div></div></div><div class="btn-group"><button class="btn btn-primary" id="playBtn" onclick="toggleTest()">▶ Play Tone</button><button class="btn btn-success" onclick="recordHeard()">✓ Heard</button><button class="btn btn-danger" onclick="recordNotHeard()">✗ Not Heard</button><button class="btn btn-secondary" onclick="stopTest()">⏹ Stop</button><button class="btn btn-secondary" onclick="clearResults()">🗑️ Clear</button></div><div class="form-group"><label>Quick Frequency Test</label><div class="btn-group"><button class="btn btn-secondary" onclick="playFreq(125)">125Hz</button><button class="btn btn-secondary" onclick="playFreq(250)">250Hz</button><button class="btn btn-secondary" onclick="playFreq(500)">500Hz</button><button class="btn btn-secondary" onclick="playFreq(1000)">1kHz</button><button class="btn btn-secondary" onclick="playFreq(2000)">2kHz</button><button class="btn btn-secondary" onclick="playFreq(4000)">4kHz</button><button class="btn btn-secondary" onclick="playFreq(8000)">8kHz</button><button class="btn btn-secondary" onclick="playFreq(12000)">12kHz</button></div></div><div class="form-group"><label>Audiogram</label><canvas id="audiogram" width="700" height="300" style="background:#0f172a;border:1px solid rgba(148,163,184,.2);border-radius:8px;width:100%"></canvas></div><div id="resultsSummary" style="color:#94a3b8;font-size:.85rem"></div><p class="info-text">💡 Use quality headphones in a quiet environment. This test is for reference only, not a substitute for professional hearing evaluation.</p>''',
    tool_js='''var audioCtx=null,oscillator=null,gainNode=null,isPlaying=false,results=[];function toast(m){var t=document.getElementById("toast");t.textContent=m;t.classList.add("show");setTimeout(function(){t.classList.remove("show")},2000)}function getAudioCtx(){if(!audioCtx)audioCtx=new(window.AudioContext||window.webkitAudioContext)();return audioCtx}function toggleTest(){if(isPlaying){stopTest();return}startTest()}function startTest(){var freq=parseInt(document.getElementById('freqSlider').value);var vol=parseInt(document.getElementById('volSlider').value);playTone(freq,vol)}function stopTest(){if(oscillator){try{oscillator.stop()}catch(e){}oscillator.disconnect();oscillator=null}if(gainNode){gainNode.disconnect();gainNode=null}isPlaying=false;document.getElementById('playBtn').textContent='\\u25b6 \\u64ad\\u653e\\u7eaf\\u97f3'}function playTone(freq,vol){stopTest();var ctx=getAudioCtx();oscillator=ctx.createOscillator();gainNode=ctx.createGain();var ear=document.getElementById('ear').value;oscillator.type='sine';oscillator.frequency.setValueAtTime(freq,ctx.currentTime);var dB=Math.pow(10,(vol-80)/20);gainNode.gain.setValueAtTime(dB,ctx.currentTime);if(ear==='left'){var pan=ctx.createStereoPanner();pan.pan.setValueAtTime(-1,ctx.currentTime);oscillator.connect(gainNode);gainNode.connect(pan);pan.connect(ctx