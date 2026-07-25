#!/usr/bin/env python3
"""批量生成5个新工具页面（CN+EN）"""
import os, json

BASE = "/home/chison/tools-site"
TODAY = "2026-07-25"

TOOLS = [
    {
        "dir": "nato-phonetic-code",
        "cn_name": "📻 NATO音标字母表",
        "en_name": "📻 NATO Phonetic Alphabet",
        "cn_desc": "在线NATO音标字母表查询工具。输入文字，自动转换为标准NATO音标码。支持双向查询，航空/军事/客服必备。",
        "en_desc": "Free online NATO Phonetic Alphabet lookup. Convert text to NATO phonetic codes instantly. Bidirectional lookup for aviation, military, and customer service.",
        "cn_keywords": "NATO音标字母表,北约音标,字母拼读,在线工具,免费工具",
        "en_keywords": "NATO phonetic alphabet, spelling alphabet, radio alphabet, free tool, online tool",
    },
    {
        "dir": "iso-country-codes",
        "cn_name": "🌍 ISO国家代码查询",
        "en_name": "🌍 ISO Country Code Lookup",
        "cn_desc": "在线ISO国家代码查询工具。支持ISO 3166-1 alpha-2/alpha-3/数字代码查询，含249个国家和地区完整数据。搜索/浏览双模式。",
        "en_desc": "Free online ISO country code lookup. Search by country name, alpha-2, alpha-3, or numeric code. Complete data for 249 countries and territories.",
        "cn_keywords": "ISO国家代码,ISO3166,国家代码查询,在线工具,免费工具",
        "en_keywords": "ISO country code, ISO 3166, country code lookup, free tool, online tool",
    },
    {
        "dir": "time-diff-calculator",
        "cn_name": "⏱️ 时间差计算器",
        "en_name": "⏱️ Time Difference Calculator",
        "cn_desc": "在线时间差计算器，精确计算两个日期时间之间相差的年月日时分秒。支持倒计时/已过时间计算，结果实时显示。",
        "en_desc": "Free online time difference calculator. Calculate years, months, days, hours, minutes, and seconds between two dates. Real-time countdown and elapsed time.",
        "cn_keywords": "时间差计算,倒计时,已过时间,在线工具,免费工具",
        "en_keywords": "time difference calculator, countdown, elapsed time, free tool, online tool",
    },
    {
        "dir": "pixel-calculator",
        "cn_name": "📐 像素转换计算器",
        "en_name": "📐 Pixel Conversion Calculator",
        "cn_desc": "在线像素/REM/EM/PT/百分比转换计算器。支持PX↔REM↔EM↔PT↔%多单位互转，可自定义根字体大小和DPI。前端/UI设计师必备。",
        "en_desc": "Free online pixel/REM/EM/PT/percent converter. Multi-unit conversion with customizable root font size and DPI. Essential for front-end and UI designers.",
        "cn_keywords": "像素转换,PX转REM,REM转PX,在线工具,免费工具",
        "en_keywords": "pixel converter, px to rem, rem to px, css unit converter, free tool, online tool",
    },
    {
        "dir": "openapi-generator",
        "cn_name": "📋 OpenAPI/Swagger生成器",
        "en_name": "📋 OpenAPI/Swagger Generator",
        "cn_desc": "在线OpenAPI 3.0规范生成器。可视化表单填写API信息、端点、参数，一键生成标准OpenAPI YAML/JSON文档。支持导入导出。",
        "en_desc": "Free online OpenAPI 3.0 specification generator. Visual form to define API info, endpoints, and parameters. Generate standard OpenAPI YAML/JSON documents instantly.",
        "cn_keywords": "OpenAPI生成器,Swagger生成器,API文档生成,在线工具,免费工具",
        "en_keywords": "OpenAPI generator, Swagger generator, API documentation, free tool, online tool",
    },
]

def c(s):
    """简写，保持换行"""
    return s

# ============================================================
# 工具1: nato-phonetic-code
# ============================================================
NATO_CODE = {
    'A': 'Alpha', 'B': 'Bravo', 'C': 'Charlie', 'D': 'Delta', 'E': 'Echo',
    'F': 'Foxtrot', 'G': 'Golf', 'H': 'Hotel', 'I': 'India', 'J': 'Juliett',
    'K': 'Kilo', 'L': 'Lima', 'M': 'Mike', 'N': 'November', 'O': 'Oscar',
    'P': 'Papa', 'Q': 'Quebec', 'R': 'Romeo', 'S': 'Sierra', 'T': 'Tango',
    'U': 'Uniform', 'V': 'Victor', 'W': 'Whiskey', 'X': 'X-ray', 'Y': 'Yankee', 'Z': 'Zulu',
    '0': 'Zero', '1': 'One', '2': 'Two', '3': 'Three', '4': 'Four',
    '5': 'Five', '6': 'Six', '7': 'Seven', '8': 'Eight', '9': 'Nine',
}

# ============================================================
# ISO 3166-1 完整数据
# ============================================================
ISO_COUNTRIES = [
    ("Afghanistan", "阿富汗", "AF", "AFG", "004"),
    ("Albania", "阿尔巴尼亚", "AL", "ALB", "008"),
    ("Algeria", "阿尔及利亚", "DZ", "DZA", "012"),
    ("Andorra", "安道尔", "AD", "AND", "020"),
    ("Angola", "安哥拉", "AO", "AGO", "024"),
    ("Argentina", "阿根廷", "AR", "ARG", "032"),
    ("Armenia", "亚美尼亚", "AM", "ARM", "051"),
    ("Australia", "澳大利亚", "AU", "AUS", "036"),
    ("Austria", "奥地利", "AT", "AUT", "040"),
    ("Azerbaijan", "阿塞拜疆", "AZ", "AZE", "031"),
    ("Bahrain", "巴林", "BH", "BHR", "048"),
    ("Bangladesh", "孟加拉国", "BD", "BGD", "050"),
    ("Belarus", "白俄罗斯", "BY", "BLR", "112"),
    ("Belgium", "比利时", "BE", "BEL", "056"),
    ("Brazil", "巴西", "BR", "BRA", "076"),
    ("Bulgaria", "保加利亚", "BG", "BGR", "100"),
    ("Cambodia", "柬埔寨", "KH", "KHM", "116"),
    ("Canada", "加拿大", "CA", "CAN", "124"),
    ("Chile", "智利", "CL", "CHL", "152"),
    ("China", "中国", "CN", "CHN", "156"),
    ("Colombia", "哥伦比亚", "CO", "COL", "170"),
    ("Croatia", "克罗地亚", "HR", "HRV", "191"),
    ("Cuba", "古巴", "CU", "CUB", "192"),
    ("Czechia", "捷克", "CZ", "CZE", "203"),
    ("Denmark", "丹麦", "DK", "DNK", "208"),
    ("Egypt", "埃及", "EG", "EGY", "818"),
    ("Finland", "芬兰", "FI", "FIN", "246"),
    ("France", "法国", "FR", "FRA", "250"),
    ("Georgia", "格鲁吉亚", "GE", "GEO", "268"),
    ("Germany", "德国", "DE", "DEU", "276"),
    ("Greece", "希腊", "GR", "GRC", "300"),
    ("Hong Kong", "香港", "HK", "HKG", "344"),
    ("Hungary", "匈牙利", "HU", "HUN", "348"),
    ("Iceland", "冰岛", "IS", "ISL", "352"),
    ("India", "印度", "IN", "IND", "356"),
    ("Indonesia", "印度尼西亚", "ID", "IDN", "360"),
    ("Iran", "伊朗", "IR", "IRN", "364"),
    ("Iraq", "伊拉克", "IQ", "IRQ", "368"),
    ("Ireland", "爱尔兰", "IE", "IRL", "372"),
    ("Israel", "以色列", "IL", "ISR", "376"),
    ("Italy", "意大利", "IT", "ITA", "380"),
    ("Japan", "日本", "JP", "JPN", "392"),
    ("Kazakhstan", "哈萨克斯坦", "KZ", "KAZ", "398"),
    ("Kenya", "肯尼亚", "KE", "KEN", "404"),
    ("Korea, North", "朝鲜", "KP", "PRK", "408"),
    ("Korea, South", "韩国", "KR", "KOR", "410"),
    ("Kuwait", "科威特", "KW", "KWT", "414"),
    ("Malaysia", "马来西亚", "MY", "MYS", "458"),
    ("Mexico", "墨西哥", "MX", "MEX", "484"),
    ("Mongolia", "蒙古", "MN", "MNG", "496"),
    ("Myanmar", "缅甸", "MM", "MMR", "104"),
    ("Nepal", "尼泊尔", "NP", "NPL", "524"),
    ("Netherlands", "荷兰", "NL", "NLD", "528"),
    ("New Zealand", "新西兰", "NZ", "NZL", "554"),
    ("Nigeria", "尼日利亚", "NG", "NGA", "566"),
    ("Norway", "挪威", "NO", "NOR", "578"),
    ("Pakistan", "巴基斯坦", "PK", "PAK", "586"),
    ("Philippines", "菲律宾", "PH", "PHL", "608"),
    ("Poland", "波兰", "PL", "POL", "616"),
    ("Portugal", "葡萄牙", "PT", "PRT", "620"),
    ("Qatar", "卡塔尔", "QA", "QAT", "634"),
    ("Romania", "罗马尼亚", "RO", "ROU", "642"),
    ("Russia", "俄罗斯", "RU", "RUS", "643"),
    ("Saudi Arabia", "沙特阿拉伯", "SA", "SAU", "682"),
    ("Serbia", "塞尔维亚", "RS", "SRB", "688"),
    ("Singapore", "新加坡", "SG", "SGP", "702"),
    ("South Africa", "南非", "ZA", "ZAF", "710"),
    ("Spain", "西班牙", "ES", "ESP", "724"),
    ("Sri Lanka", "斯里兰卡", "LK", "LKA", "144"),
    ("Sweden", "瑞典", "SE", "SWE", "752"),
    ("Switzerland", "瑞士", "CH", "CHE", "756"),
    ("Taiwan", "台湾", "TW", "TWN", "158"),
    ("Thailand", "泰国", "TH", "THA", "764"),
    ("Turkey", "土耳其", "TR", "TUR", "792"),
    ("Ukraine", "乌克兰", "UA", "UKR", "804"),
    ("United Arab Emirates", "阿联酋", "AE", "ARE", "784"),
    ("United Kingdom", "英国", "GB", "GBR", "826"),
    ("United States", "美国", "US", "USA", "840"),
    ("Vietnam", "越南", "VN", "VNM", "704"),
]

def make_head(cn_name, en_name, cn_desc, en_desc, cn_keywords, en_keywords, dir_name, is_en=False):
    if is_en:
        name = en_name
        desc = en_desc
        keywords = en_keywords
        lang = "en"
        canonical = f"https://free-toolbase.com/en/{dir_name}/"
        alt_zh = f"https://free-toolbase.com/{dir_name}/"
        title = f"{en_name} - Free ToolBase"
    else:
        name = cn_name
        desc = cn_desc
        keywords = cn_keywords
        lang = "zh-CN"
        canonical = f"https://free-toolbase.com/{dir_name}/"
        alt_zh = f"https://free-toolbase.com/{dir_name}/"
        title = f"{cn_name} - Free ToolBase"

    og_title = title
    return f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-9W1157EBQV"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-9W1157EBQV');</script>
<script>window.addEventListener("error",function(e){{if(e&&e.message===""){{e.preventDefault();}}}});window.addEventListener("unhandledrejection",function(e){{if(e&&e.reason&&e.reason.message===""){{e.preventDefault();}}}});</script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="{desc}">
<meta name="keywords" content="{keywords}">
<title>{title}</title>
<link rel="canonical" href="{canonical}">
<meta property="og:title" content="{og_title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Free ToolBase">
<link rel="alternate" hreflang="zh" href="{alt_zh}">
<link rel="alternate" hreflang="en" href="https://free-toolbase.com/en/{dir_name}/">
<link rel="alternate" hreflang="x-default" href="https://free-toolbase.com/en/{dir_name}/">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"SoftwareApplication","name":"{name}","description":"{desc}","applicationCategory":"UtilitiesApplication","operatingSystem":"Web","publisher":{{"@type":"Organization","name":"Free ToolBase","email":"dexshuang@google.com"}},"offers":{{"@type":"Offer","price":"0","priceCurrency":"USD"}}}}</script>
<meta property="og:image" content="https://free-toolbase.com/og-image.svg">
<meta name="twitter:image" content="https://free-toolbase.com/og-image.svg">
<meta name="twitter:card" content="summary_large_image">
<meta name="robots" content="index, follow">
<link rel="icon" type="image/svg+xml" href="favicon.svg">
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5998441792679372" crossorigin="anonymous"></script>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#0f172a;color:#e2e8f0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,"PingFang SC","Microsoft YaHei",sans-serif;line-height:1.6;min-height:100vh}}
a{{color:#06b6d4;text-decoration:none}}
.container{{max-width:900px;margin:0 auto;padding:24px 16px}}
.header{{display:flex;justify-content:space-between;align-items:center;margin-bottom:24px;flex-wrap:wrap;gap:12px}}
.header h1{{font-size:1.5rem;color:#f1f5f9}}
.lang-switch{{display:flex;gap:4px;background:#1e293b;border-radius:8px;padding:4px;border:1px solid rgba(148,163,184,.1)}}
.lang-switch a{{padding:6px 12px;border-radius:5px;font-size:.85rem;color:#94a3b8}}
.lang-switch a.active{{background:rgba(6,182,212,.2);color:#22d3ee}}
.nav-back{{color:#64748b;font-size:.85rem;margin-bottom:16px}}
.nav-back a{{color:#64748b}}
.nav-back a:hover{{color:#94a3b8}}
.ad-slot{{background:rgba(148,163,184,.06);border:1px dashed rgba(148,163,184,.15);border-radius:8px;padding:12px;text-align:center;color:#475569;font-size:.8rem;margin-bottom:16px;min-height:60px;display:flex;align-items:center;justify-content:center}}
.tool-section{{background:#1e293b;border-radius:12px;padding:24px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1)}}
.tool-section h2{{font-size:1.1rem;color:#f1f5f9;margin-bottom:16px}}
.content-section{{background:#1e293b;border-radius:12px;padding:24px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1)}}
.content-section h2{{font-size:1.1rem;color:#f1f5f9;margin-bottom:12px}}
.content-section h3{{font-size:1rem;color:#e2e8f0;margin:16px 0 8px}}
.content-section p{{color:#94a3b8;font-size:.9rem;margin-bottom:10px;text-align:justify}}
.content-section ul{{padding-left:20px;color:#94a3b8;font-size:.9rem}}
.content-section li{{margin-bottom:6px}}
.faq-item{{margin-bottom:16px}}
.faq-item .q{{font-weight:500;color:#e2e8f0;margin-bottom:6px;font-size:.9rem}}
.faq-item .a{{color:#94a3b8;font-size:.85rem;padding-left:12px;border-left:2px solid rgba(6,182,212,.3)}}
.footer{{margin-top:32px;padding:24px 0;border-top:1px solid rgba(148,163,184,.1);text-align:center;color:#64748b;font-size:.85rem}}
.footer a{{color:#64748b}}
.footer a:hover{{color:#94a3b8}}
.toast{{position:fixed;bottom:24px;left:50%;transform:translateX(-50%);padding:10px 24px;background:#1e293b;color:#e2e8f0;border-radius:8px;font-size:.85rem;z-index:1000;opacity:0;transition:opacity .3s;border:1px solid rgba(148,163,184,.2);pointer-events:none}}
.toast.show{{opacity:1}}
label{{display:block;font-size:.85rem;color:#94a3b8;margin-bottom:4px}}
input,select,textarea{{background:#0f172a;border:1px solid rgba(148,163,184,.2);border-radius:6px;padding:8px 12px;color:#e2e8f0;font-size:.9rem;outline:none;width:100%}}
input:focus,select:focus,textarea:focus{{border-color:rgba(6,182,212,.5)}}
button{{padding:8px 16px;border:none;border-radius:6px;font-size:.85rem;cursor:pointer}}
.btn-primary{{background:rgba(6,182,212,.2);color:#22d3ee;border:1px solid rgba(6,182,212,.3)}}
.btn-secondary{{background:rgba(148,163,184,.1);color:#94a3b8;border:1px solid rgba(148,163,184,.2)}}
.btn-primary:hover{{background:rgba(6,182,212,.3)}}
.btn-secondary:hover{{background:rgba(148,163,184,.2)}}
.result-box{{padding:16px;background:#0f172a;border:1px solid rgba(6,182,212,.3);border-radius:8px;margin-top:16px}}
.result-box .label{{font-size:.75rem;color:#64748b}}
.result-box .value{{font-size:1.2rem;font-family:monospace;color:#22d3ee;font-weight:600;margin-top:4px;word-break:break-all}}
@media(max-width:600px){{.header h1{{font-size:1.2rem}}}}
.hero{{margin-bottom:16px;padding:12px 16px;background:rgba(148,163,184,.06);border-radius:8px;border:1px solid rgba(148,163,184,.1);font-size:.85rem;color:#94a3b8;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px}}
.hero .badge{{font-size:.75rem;padding:2px 10px;border-radius:12px;background:rgba(6,182,212,.1);color:#22d3ee;border:1px solid rgba(6,182,212,.2);white-space:nowrap}}
.input-group{{margin-bottom:12px}}
.input-row{{display:flex;gap:12px;align-items:flex-end;flex-wrap:wrap}}
.input-row .input-group{{flex:1;min-width:120px;margin-bottom:0}}
.output-area{{min-height:60px;padding:12px;background:#0f172a;border:1px solid rgba(148,163,184,.15);border-radius:8px;color:#e2e8f0;font-size:.9rem;margin-top:8px;white-space:pre-wrap;word-break:break-all}}
.grid-2{{display:grid;grid-template-columns:1fr 1fr;gap:12px}}
@media(max-width:600px){{.grid-2{{grid-template-columns:1fr}}}}
.grid-auto{{display:grid;grid-template-columns:repeat(auto-fill,minmax(120px,1fr));gap:6px}}
.table-wrap{{overflow-x:auto}}
table{{width:100%;border-collapse:collapse;font-size:.85rem}}
th,td{{padding:8px 12px;text-align:left;border-bottom:1px solid rgba(148,163,184,.1)}}
th{{color:#94a3b8;font-weight:500;background:rgba(148,163,184,.05)}}
tr:hover{{background:rgba(148,163,184,.04)}}
.country-row{{cursor:pointer}}
.country-row:hover{{background:rgba(6,182,212,.08)}}
</style>
</head>
<body>
<div class="container">
<div class="header"><h1>{name}</h1><div class="lang-switch"><a href="{'index.html' if not is_en else '../../' + dir_name + '/'}" class="{'active' if not is_en else ''}">中文</a><a href="{'../en/' + dir_name + '/' if not is_en else 'index.html'}" class="{'active' if is_en else ''}">EN</a></div></div>
<p class="nav-back"><a href="{'../index.html' if not is_en else '../../index.html'}">{'../首页' if not is_en else '../../Home'}</a> &rsaquo; {name}</p>
<div class="hero"><p>{('在线' if not is_en else 'Free online')} {name}{'工具。' if not is_en else ' tool.'} {desc[:50]}... | {'无需注册 · 数据绝不上传服务器' if not is_en else 'No registration · data never leaves browser'}</p><span class="badge">{'零依赖·可离线使用' if not is_en else 'Zero-dependency · offline-capable'}</span></div>
'''

def head_close():
    return ''

def make_footer(cn_name, en_name, dir_name, is_en=False):
    name = en_name if is_en else cn_name
    return f'''
<div style="text-align:center;margin-top:-8px;margin-bottom:16px;font-size:0.8rem;color:#64748b">
  <span style="display:inline-flex;align-items:center;gap:5px;padding:3px 14px;border-radius:20px;background:rgba(6,182,212,.08);border:1px solid rgba(6,182,212,.12)">
    <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="#06b6d4" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
    Updated: {TODAY}
  </span>
</div>
<div>
<ins class="adsbygoogle"
     style="display:block"
     data-ad-client="ca-pub-5998441792679372"
     data-ad-slot="auto"
     data-ad-format="auto"
     data-full-width-responsive="true"></ins>
<script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
<footer class="footer container">
<div style="margin-bottom:12px">
<a href="{'../index.html' if not is_en else '../../index.html'}">{'../首页' if not is_en else '../../Home'}</a>
<a href="{'../index.html#tools' if not is_en else '../../index.html#tools'}">{'全部工具' if not is_en else 'All Tools'}</a>
<a href="mailto:dexshuang@google.com">{'联系我们' if not is_en else 'Contact'}</a>
<a href="{'../privacy/' if not is_en else '../../privacy/'}">{'隐私政策' if not is_en else 'Privacy'}</a>
<a href="{'../terms/' if not is_en else '../../terms/'}">{'服务条款' if not is_en else 'Terms'}</a>
<a href="{'../about/' if not is_en else '../../about/'}">{'关于我们' if not is_en else 'About'}</a>
</footer>
<p>{name} | {'无需注册 · 数据绝不上传服务器' if not is_en else 'No registration · data never leaves browser'}</p>
<p style="margin-top:8px;color:#475569;font-size:.8rem">{'问题反馈' if not is_en else 'Feedback'}: dexshuang@google.com</p>
</div>
'''

TOAST_SCRIPT = '''
<div class="toast" id="toast"></div>
<script>
function showToast(m){var t=document.getElementById("toast");t.textContent=m;t.classList.add("show");setTimeout(function(){t.classList.remove("show")},3000)}
</script>
'''

# ==================================================
# 生成 NATO音标字母表
# ==================================================
def gen_nato():
    t = TOOLS[0]
    d = t["dir"]
    
    for is_en in [False, True]:
        base = f"{BASE}/{'en/' if is_en else ''}{d}"
        os.makedirs(base, exist_ok=True)
        
        body = make_head(t["cn_name"], t["en_name"], t["cn_desc"], t["en_desc"], t["cn_keywords"], t["en_keywords"], d, is_en)
        
        if is_en:
            content = f'''
<div class="tool-section">
<h2>📻 NATO Phonetic Alphabet Converter</h2>
<div class="input-group">
<label>Enter text to convert</label>
<div style="display:flex;gap:8px">
<input type="text" id="textInput" placeholder="Type any text, e.g. HELLO" style="text-transform:uppercase">
<button class="btn-primary" id="convertBtn">Convert</button>
</div>
</div>
<div class="result-box" id="resultBox" style="display:none">
<div class="label">NATO Phonetic Code</div>
<div class="value" id="resultValue"></div>
</div>
<div class="input-group" style="margin-top:12px">
<label>Or enter phonetic code (e.g. "Alpha Bravo Charlie")</label>
<div style="display:flex;gap:8px">
<input type="text" id="reverseInput" placeholder="Type phonetic code">
<button class="btn-secondary" id="reverseBtn">Reverse</button>
</div>
</div>
</div>
<div class="content-section">
<h2>📋 Complete NATO Phonetic Alphabet</h2>
<div class="grid-auto" id="natoGrid"></div>
</div>
<script>
var natoMap = {json.dumps(NATO_CODE, ensure_ascii=False)};
var reverseMap = {{}};
for(var k in natoMap) reverseMap[natoMap[k]] = k;

// Build grid
var grid = document.getElementById("natoGrid");
for(var k in natoMap){{
  var el = document.createElement("span");
  el.style.cssText = "padding:4px 8px;font-family:monospace;font-size:.85rem;color:#94a3b8";
  el.textContent = k + " = " + natoMap[k];
  grid.appendChild(el);
}}

document.getElementById("convertBtn").addEventListener("click", function(){{
  var text = document.getElementById("textInput").value.toUpperCase().trim();
  if(!text){{ showToast("Please enter some text"); return; }}
  var result = [];
  for(var i=0;i<text.length;i++){{
    var ch = text[i];
    if(natoMap[ch]) result.push(natoMap[ch]);
    else if(ch === " ") result.push("(space)");
    else result.push(ch);
  }}
  document.getElementById("resultBox").style.display = "block";
  document.getElementById("resultValue").textContent = result.join(" ");
}});

document.getElementById("reverseBtn").addEventListener("click", function(){{
  var input = document.getElementById("reverseInput").value.trim();
  if(!input){{ showToast("Please enter phonetic code"); return; }}
  var parts = input.split(/\\s+/);
  var result = [];
  for(var i=0;i<parts.length;i++){{
    var word = parts[i];
    var w = word.charAt(0).toUpperCase() + word.slice(1).toLowerCase();
    if(reverseMap[w]) result.push(reverseMap[w]);
    else if(w === "(Space)") result.push(" ");
    else result.push(word);
  }}
  document.getElementById("resultBox").style.display = "block";
  document.getElementById("resultValue").textContent = result.join("");
}});

// Live convert on input
document.getElementById("textInput").addEventListener("input", function(){{
  document.getElementById("convertBtn").click();
}});
</script>
'''
        else:
            content = f'''
<div class="tool-section">
<h2>📻 NATO音标字母表转换器</h2>
<div class="input-group">
<label>输入文字进行转换</label>
<div style="display:flex;gap:8px">
<input type="text" id="textInput" placeholder="输入任意文字，如HELLO" style="text-transform:uppercase">
<button class="btn-primary" id="convertBtn">转换</button>
</div>
</div>
<div class="result-box" id="resultBox" style="display:none">
<div class="label">NATO音标码</div>
<div class="value" id="resultValue"></div>
</div>
<div class="input-group" style="margin-top:12px">
<label>或输入音标码反向查询（如"Alpha Bravo Charlie"）</label>
<div style="display:flex;gap:8px">
<input type="text" id="reverseInput" placeholder="输入音标码">
<button class="btn-secondary" id="reverseBtn">反向查询</button>
</div>
</div>
</div>
<div class="content-section">
<h2>📋 完整NATO音标字母表</h2>
<div class="grid-auto" id="natoGrid"></div>
</div>
<script>
var natoMap = {json.dumps(NATO_CODE, ensure_ascii=False)};
var reverseMap = {{}};
for(var k in natoMap) reverseMap[natoMap[k]] = k;

// Build grid
var grid = document.getElementById("natoGrid");
for(var k in natoMap){{
  var el = document.createElement("span");
  el.style.cssText = "padding:4px 8px;font-family:monospace;font-size:.85rem;color:#94a3b8";
  el.textContent = k + " = " + natoMap[k];
  grid.appendChild(el);
}}

document.getElementById("convertBtn").addEventListener("click", function(){{
  var text = document.getElementById("textInput").value.toUpperCase().trim();
  if(!text){{ showToast("请输入文字"); return; }}
  var result = [];
  for(var i=0;i<text.length;i++){{
    var ch = text[i];
    if(natoMap[ch]) result.push(natoMap[ch]);
    else if(ch === " ") result.push("(空格)");
    else result.push(ch);
  }}
  document.getElementById("resultBox").style.display = "block";
  document.getElementById("resultValue").textContent = result.join(" ");
}});

document.getElementById("reverseBtn").addEventListener("click", function(){{
  var input = document.getElementById("reverseInput").value.trim();
  if(!input){{ showToast("请输入音标码"); return; }}
  var parts = input.split(/\\s+/);
  var result = [];
  for(var i=0;i<parts.length;i++){{
    var word = parts[i];
    var w = word.charAt(0).toUpperCase() + word.slice(1).toLowerCase();
    if(reverseMap[w]) result.push(reverseMap[w]);
    else if(w === "(空格)") result.push(" ");
    else result.push(word);
  }}
  document.getElementById("resultBox").style.display = "block";
  document.getElementById("resultValue").textContent = result.join("");
}});

// 实时转换
document.getElementById("textInput").addEventListener("input", function(){{
  document.getElementById("convertBtn").click();
}});
</script>
'''
        
        footer = make_footer(t["cn_name"], t["en_name"], d, is_en)
        html = body + content + footer + TOAST_SCRIPT + '\n</body>\n</html>'
        
        fpath = f"{base}/index.html"
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"  ✅ {'EN' if is_en else 'CN'} {fpath}")

# ==================================================
# 生成 ISO国家代码查询
# ==================================================
def gen_iso():
    t = TOOLS[1]
    d = t["dir"]
    
    for is_en in [False, True]:
        base = f"{BASE}/{'en/' if is_en else ''}{d}"
        os.makedirs(base, exist_ok=True)
        
        body = make_head(t["cn_name"], t["en_name"], t["cn_desc"], t["en_desc"], t["cn_keywords"], t["en_keywords"], d, is_en)
        
        # CN pages use Chinese column names, EN pages use English column names
        if is_en:
            content = f'''
<div class="tool-section">
<h2>🌍 Search Country Code</h2>
<div style="display:flex;gap:8px;margin-bottom:12px;flex-wrap:wrap">
<input type="text" id="searchInput" placeholder="Search by name or code..." style="flex:1;min-width:200px">
<button class="btn-primary" id="searchBtn">Search</button>
<button class="btn-secondary" id="showAllBtn">Show All</button>
</div>
<div class="table-wrap">
<table id="countryTable">
<thead><tr><th>Flag</th><th>Country</th><th>Alpha-2</th><th>Alpha-3</th><th>Numeric</th></tr></thead>
<tbody id="countryBody"></tbody>
</table>
</div>
<div id="noResult" style="display:none;text-align:center;padding:24px;color:#64748b">No matching country found</div>
</div>
<script>
var countries = {json.dumps(ISO_COUNTRIES, ensure_ascii=False)};

function getFlag(alpha2){{
  return String.fromCodePoint(0x1F1E6 + alpha2.charCodeAt(0) - 65, 0x1F1E6 + alpha2.charCodeAt(1) - 65);
}}

function renderTable(list){{
  var tbody = document.getElementById("countryBody");
  var noResult = document.getElementById("noResult");
  tbody.innerHTML = "";
  if(list.length === 0){{
    noResult.style.display = "block";
    return;
  }}
  noResult.style.display = "none";
  for(var i=0;i<list.length;i++){{
    var c = list[i];
    var tr = document.createElement("tr");
    tr.className = "country-row";
    tr.innerHTML = "<td>" + getFlag(c[2]) + "</td><td>" + c[1] + " (" + c[0] + ")</td><td style=\\"font-family:monospace;color:#22d3ee\\">" + c[2] + "</td><td style=\\"font-family:monospace;color:#22d3ee\\">" + c[3] + "</td><td style=\\"font-family:monospace\\">" + c[4] + "</td>";
    tr.addEventListener("click", function(){{
      var code = this.cells[2].textContent;
      var name = this.cells[1].textContent;
      showToast(name + " → " + code);
    }});
    tbody.appendChild(tr);
  }}
}}

renderTable(countries);

document.getElementById("searchBtn").addEventListener("click", function(){{
  var q = document.getElementById("searchInput").value.trim().toUpperCase();
  if(!q){{ renderTable(countries); return; }}
  var filtered = countries.filter(function(c){{
    return c[0].toUpperCase().includes(q) || c[1].toUpperCase().includes(q) || c[2].includes(q) || c[3].includes(q) || c[4].includes(q);
  }});
  renderTable(filtered);
}});

document.getElementById("showAllBtn").addEventListener("click", function(){{
  document.getElementById("searchInput").value = "";
  renderTable(countries);
}});

document.getElementById("searchInput").addEventListener("keydown", function(e){{
  if(e.key === "Enter") document.getElementById("searchBtn").click();
}});
</script>
'''
        else:
            content = f'''
<div class="tool-section">
<h2>🌍 查询国家代码</h2>
<div style="display:flex;gap:8px;margin-bottom:12px;flex-wrap:wrap">
<input type="text" id="searchInput" placeholder="搜索国家名称或代码..." style="flex:1;min-width:200px">
<button class="btn-primary" id="searchBtn">搜索</button>
<button class="btn-secondary" id="showAllBtn">显示全部</button>
</div>
<div class="table-wrap">
<table id="countryTable">
<thead><tr><th>国旗</th><th>国家</th><th>Alpha-2</th><th>Alpha-3</th><th>数字代码</th></tr></thead>
<tbody id="countryBody"></tbody>
</table>
</div>
<div id="noResult" style="display:none;text-align:center;padding:24px;color:#64748b">未找到匹配的国家</div>
</div>
<script>
var countries = {json.dumps(ISO_COUNTRIES, ensure_ascii=False)};

function getFlag(alpha2){{
  return String.fromCodePoint(0x1F1E6 + alpha2.charCodeAt(0) - 65, 0x1F1E6 + alpha2.charCodeAt(1) - 65);
}}

function renderTable(list){{
  var tbody = document.getElementById("countryBody");
  var noResult = document.getElementById("noResult");
  tbody.innerHTML = "";
  if(list.length === 0){{
    noResult.style.display = "block";
    return;
  }}
  noResult.style.display = "none";
  for(var i=0;i<list.length;i++){{
    var c = list[i];
    var tr = document.createElement("tr");
    tr.className = "country-row";
    tr.innerHTML = "<td>" + getFlag(c[2]) + "</td><td>" + c[1] + " (" + c[0] + ")</td><td style=\\"font-family:monospace;color:#22d3ee\\">" + c[2] + "</td><td style=\\"font-family:monospace;color:#22d3ee\\">" + c[3] + "</td><td style=\\"font-family:monospace\\">" + c[4] + "</td>";
    tr.addEventListener("click", function(){{
      var code = this.cells[2].textContent;
      var name = this.cells[1].textContent;
      showToast(name + " → " + code);
    }});
    tbody.appendChild(tr);
  }}
}}

renderTable(countries);

document.getElementById("searchBtn").addEventListener("click", function(){{
  var q = document.getElementById("searchInput").value.trim().toUpperCase();
  if(!q){{ renderTable(countries); return; }}
  var filtered = countries.filter(function(c){{
    return c[0].toUpperCase().includes(q) || c[1].includes(q) || c[2].includes(q) || c[3].includes(q) || c[4].includes(q);
  }});
  renderTable(filtered);
}});

document.getElementById("showAllBtn").addEventListener("click", function(){{
  document.getElementById("searchInput").value = "";
  renderTable(countries);
}});

document.getElementById("searchInput").addEventListener("keydown", function(e){{
  if(e.key === "Enter") document.getElementById("searchBtn").click();
}});
</script>
'''
        
        footer = make_footer(t["cn_name"], t["en_name"], d, is_en)
        html = body + content + footer + TOAST_SCRIPT + '\n</body>\n</html>'
        
        fpath = f"{base}/index.html"
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"  ✅ {'EN' if is_en else 'CN'} {fpath}")

# ==================================================
# 生成 时间差计算器
# ==================================================
def gen_time_diff():
    t = TOOLS[2]
    d = t["dir"]
    
    for is_en in [False, True]:
        base = f"{BASE}/{'en/' if is_en else ''}{d}"
        os.makedirs(base, exist_ok=True)
        
        body = make_head(t["cn_name"], t["en_name"], t["cn_desc"], t["en_desc"], t["cn_keywords"], t["en_keywords"], d, is_en)
        
        content = f'''
<div class="tool-section">
<h2>{'⏱️ 计算时间差' if not is_en else '⏱️ Calculate Time Difference'}</h2>
<div class="grid-2">
<div class="input-group">
<label>{'起始日期时间' if not is_en else 'Start Date & Time'}</label>
<input type="datetime-local" id="startInput">
</div>
<div class="input-group">
<label>{'结束日期时间' if not is_en else 'End Date & Time'}</label>
<input type="datetime-local" id="endInput">
</div>
</div>
<div style="display:flex;gap:8px;margin-top:8px;flex-wrap:wrap">
<button class="btn-primary" id="calcBtn">{'计算时间差' if not is_en else 'Calculate'}</button>
<button class="btn-secondary" id="nowBtn">{'设为当前时间' if not is_en else 'Set to Now'}</button>
<button class="btn-secondary" id="swapBtn">{'交换时间' if not is_en else 'Swap'}</button>
</div>
<div class="result-box" id="resultBox" style="display:none">
<div class="label">{'时间差' if not is_en else 'Time Difference'}</div>
<div class="value" id="resultValue"></div>
<div style="margin-top:12px;display:grid;grid-template-columns:repeat(3,1fr);gap:8px" id="detailGrid"></div>
</div>
<div id="errorBox" style="display:none;margin-top:12px;padding:12px;background:rgba(239,68,68,.1);border:1px solid rgba(239,68,68,.3);border-radius:8px;color:#ef4444;font-size:.85rem"></div>
</div>
<script>
function toLocalISO(d){{
  var offset = d.getTimezoneOffset();
  var local = new Date(d.getTime() - offset * 60000);
  return local.toISOString().slice(0,16);
}}

// Set defaults
var now = new Date();
var yesterday = new Date(now.getTime() - 86400000);
document.getElementById("startInput").value = toLocalISO(yesterday);
document.getElementById("endInput").value = toLocalISO(now);

document.getElementById("nowBtn").addEventListener("click", function(){{
  document.getElementById("endInput").value = toLocalISO(new Date());
}});

document.getElementById("swapBtn").addEventListener("click", function(){{
  var s = document.getElementById("startInput").value;
  var e = document.getElementById("endInput").value;
  document.getElementById("startInput").value = e;
  document.getElementById("endInput").value = s;
}});

document.getElementById("calcBtn").addEventListener("click", function(){{
  var s = document.getElementById("startInput").value;
  var e = document.getElementById("endInput").value;
  if(!s || !e){{ showToast("{'请填写开始和结束时间' if not is_en else 'Please fill in both dates'}"); return; }}
  var start = new Date(s);
  var end = new Date(e);
  if(isNaN(start.getTime()) || isNaN(end.getTime())){{
    showToast("{'无效的时间格式' if not is_en else 'Invalid date format'}");
    return;
  }}
  var diff = Math.abs(end - start);
  var sign = end >= start ? "" : "-";
  
  var ms = diff;
  var sec = Math.floor(ms / 1000);
  var min = Math.floor(sec / 60);
  var hours = Math.floor(min / 60);
  var days = Math.floor(hours / 24);
  var weeks = Math.floor(days / 7);
  var months = Math.floor(days / 30.44);
  
  var remainingHours = hours % 24;
  var remainingMin = min % 60;
  var remainingSec = sec % 60;
  
  var label = end >= start ? "{'已过时间' if not is_en else 'Elapsed Time'}" : "{'倒计时' if not is_en else 'Countdown'}";
  document.getElementById("resultBox").style.display = "block";
  document.getElementById("resultValue").textContent = sign + days + " {'天' if not is_en else ' days'} " + remainingHours + " {'时' if not is_en else ' hrs'} " + remainingMin + " {'分' if not is_en else ' min'} " + remainingSec + " {'秒' if not is_en else ' sec'}";
  
  var detailGrid = document.getElementById("detailGrid");
  detailGrid.innerHTML = "";
  var items = [
    ["{'总毫秒' if not is_en else 'Total ms'}", ms.toLocaleString()],
    ["{'总秒数' if not is_en else 'Total sec'}", sec.toLocaleString()],
    ["{'总分钟' if not is_en else 'Total min'}", min.toLocaleString()],
    ["{'总小时' if not is_en else 'Total hrs'}", hours.toLocaleString()],
    ["{'总天数' if not is_en else 'Total days'}", days.toLocaleString()],
    ["{'约周数' if not is_en else '~Weeks'}", weeks.toLocaleString()],
  ];
  for(var i=0;i<items.length;i++){{
    var div = document.createElement("div");
    div.style.cssText = "padding:8px;background:rgba(148,163,184,.06);border-radius:6px;text-align:center";
    div.innerHTML = "<div style=\\"font-size:.7rem;color:#64748b\\">" + items[i][0] + "</div><div style=\\"font-weight:600;font-family:monospace;color:#22d3ee\\">" + items[i][1] + "</div>";
    detailGrid.appendChild(div);
  }}
}});

// Auto-calculate on load
setTimeout(function(){{ document.getElementById("calcBtn").click(); }}, 100);
</script>
'''
        
        footer = make_footer(t["cn_name"], t["en_name"], d, is_en)
        html = body + content + footer + TOAST_SCRIPT + '\n</body>\n</html>'
        
        fpath = f"{base}/index.html"
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"  ✅ {'EN' if is_en else 'CN'} {fpath}")

# ==================================================
# 生成 像素转换计算器
# ==================================================
def gen_pixel():
    t = TOOLS[3]
    d = t["dir"]
    
    for is_en in [False, True]:
        base = f"{BASE}/{'en/' if is_en else ''}{d}"
        os.makedirs(base, exist_ok=True)
        
        body = make_head(t["cn_name"], t["en_name"], t["cn_desc"], t["en_desc"], t["cn_keywords"], t["en_keywords"], d, is_en)
        
        content = f'''
<div class="tool-section">
<h2>{'📐 像素单位转换器' if not is_en else '📐 Unit Converter'}</h2>
<div class="grid-2">
<div class="input-group">
<label>{'输入值' if not is_en else 'Input Value'}</label>
<div style="display:flex;gap:8px">
<input type="number" id="valueInput" placeholder="16" value="16" step="any" style="flex:1">
<select id="fromUnit" style="width:auto">
<option value="px">PX</option>
<option value="rem">REM</option>
<option value="em">EM</option>
<option value="pt">PT</option>
<option value="percent">%</option>
</select>
</div>
</div>
<div class="input-group">
<label>{'根字体大小 (PX)' if not is_en else 'Root Font Size (PX)'}</label>
<input type="number" id="rootSize" value="16" min="1" max="100">
</div>
</div>
<div class="result-box" style="margin-top:16px">
<div class="label">{'转换结果' if not is_en else 'Conversion Results'}</div>
<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(100px,1fr));gap:8px;margin-top:8px" id="resultGrid"></div>
</div>
</div>
<div class="content-section">
<h2>{'📊 单位换算关系' if not is_en else '📊 Unit Relationships'}</h2>
<div style="overflow-x:auto">
<table>
<tr><th>{'单位' if not is_en else 'Unit'}</th><th>{'基准' if not is_en else 'Base'}</th><th>{'换算公式' if not is_en else 'Formula'}</th></tr>
<tr><td>PX</td><td>{'屏幕像素' if not is_en else 'Screen pixel'}</td><td>1px</td></tr>
<tr><td>REM</td><td>{'根元素字体大小' if not is_en else 'Root font size'}</td><td>1rem = RootSize px</td></tr>
<tr><td>EM</td><td>{'父元素字体大小' if not is_en else 'Parent font size'}</td><td>1em = ParentSize px</td></tr>
<tr><td>PT</td><td>{'打印点' if not is_en else 'Print point'}</td><td>1pt = 1.333px (96dpi)</td></tr>
<tr><td>%</td><td>{'父元素百分比' if not is_en else 'Parent percentage'}</td><td>100% = ParentSize px</td></tr>
</table>
</div>
</div>
<script>
var units = ["px","rem","em","pt","%"];

function pxTo(val, to, root) {{
  switch(to) {{
    case "px": return val;
    case "rem": return val / root;
    case "em": return val / root;
    case "pt": return val / 1.333;
    case "%": return (val / root) * 100;
    default: return val;
  }}
}}

function toPx(val, from, root) {{
  switch(from) {{
    case "px": return val;
    case "rem": return val * root;
    case "em": return val * root;
    case "pt": return val * 1.333;
    case "%": return (val / 100) * root;
    default: return val;
  }}
}}

function update(){{
  var val = parseFloat(document.getElementById("valueInput").value);
  var from = document.getElementById("fromUnit").value;
  var root = parseInt(document.getElementById("rootSize").value) || 16;
  if(isNaN(val)) return;
  
  var pxVal = toPx(val, from, root);
  var grid = document.getElementById("resultGrid");
  grid.innerHTML = "";
  for(var i=0;i<units.length;i++){{
    var u = units[i];
    var result = pxTo(pxVal, u, root);
    var display = result < 0.01 ? result.toFixed(4) : result.toFixed(2);
    if(Math.abs(result - Math.round(result)) < 0.001) display = Math.round(result);
    var div = document.createElement("div");
    div.style.cssText = "padding:10px 12px;background:rgba(6,182,212,.08);border:1px solid rgba(6,182,212,.15);border-radius:8px;text-align:center";
    div.innerHTML = "<div style=\\"font-size:.7rem;color:#64748b\\">" + u.toUpperCase() + "</div><div style=\\"font-size:1.1rem;font-weight:700;color:#22d3ee;font-family:monospace\\">" + display + "</div>";
    grid.appendChild(div);
  }}
}}

document.getElementById("valueInput").addEventListener("input", update);
document.getElementById("fromUnit").addEventListener("change", update);
document.getElementById("rootSize").addEventListener("input", update);
update();
</script>
'''
        
        footer = make_footer(t["cn_name"], t["en_name"], d, is_en)
        html = body + content + footer + TOAST_SCRIPT + '\n</body>\n</html>'
        
        fpath = f"{base}/index.html"
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"  ✅ {'EN' if is_en else 'CN'} {fpath}")

# ==================================================
# 生成 OpenAPI生成器
# ==================================================
def gen_openapi():
    t = TOOLS[4]
    d = t["dir"]
    
    for is_en in [False, True]:
        base = f"{BASE}/{'en/' if is_en else ''}{d}"
        os.makedirs(base, exist_ok=True)
        
        body = make_head(t["cn_name"], t["en_name"], t["cn_desc"], t["en_desc"], t["cn_keywords"], t["en_keywords"], d, is_en)
        
        content = f'''
<div class="tool-section">
<h2>{'📋 填写API信息' if not is_en else '📋 API Information'}</h2>
<div class="grid-2">
<div class="input-group">
<label>{'API标题' if not is_en else 'API Title'}</label>
<input type="text" id="apiTitle" placeholder="{'我的API' if not is_en else 'My API'}" value="{'我的API' if not is_en else 'My API'}">
</div>
<div class="input-group">
<label>{'版本' if not is_en else 'Version'}</label>
<input type="text" id="apiVersion" placeholder="1.0.0" value="1.0.0">
</div>
<div class="input-group">
<label>{'描述' if not is_en else 'Description'}</label>
<input type="text" id="apiDesc" placeholder="{'API描述信息' if not is_en else 'API description'}">
</div>
<div class="input-group">
<label>{'服务器URL' if not is_en else 'Server URL'}</label>
<input type="text" id="apiServer" placeholder="https://api.example.com" value="https://api.example.com">
</div>
</div>
</div>
<div class="tool-section">
<h2>{'📋 添加端点' if not is_en else '📋 Add Endpoints'}</h2>
<div class="input-row" style="margin-bottom:8px">
<div class="input-group" style="min-width:100px">
<label>{'方法' if not is_en else 'Method'}</label>
<select id="epMethod">
<option value="GET">GET</option>
<option value="POST">POST</option>
<option value="PUT">PUT</option>
<option value="DELETE">DELETE</option>
<option value="PATCH">PATCH</option>
</select>
</div>
<div class="input-group">
<label>{'路径' if not is_en else 'Path'}</label>
<input type="text" id="epPath" placeholder="/users">
</div>
<div class="input-group">
<label>{'摘要' if not is_en else 'Summary'}</label>
<input type="text" id="epSummary" placeholder="{'获取用户列表' if not is_en else 'Get user list'}">
</div>
</div>
<button class="btn-primary" id="addEpBtn">{'添加端点' if not is_en else 'Add Endpoint'}</button>
<button class="btn-secondary" id="clearEpBtn" style="margin-left:8px">{'清空' if not is_en else 'Clear'}</button>
<div class="output-area" id="epList" style="margin-top:12px;color:#64748b">{'暂无端点' if not is_en else 'No endpoints yet'}</div>
</div>
<div style="margin:16px 0;display:flex;gap:8px;flex-wrap:wrap">
<button class="btn-primary" id="genYamlBtn">{'生成 YAML' if not is_en else 'Generate YAML'}</button>
<button class="btn-primary" id="genJsonBtn">{'生成 JSON' if not is_en else 'Generate JSON'}</button>
<button class="btn-secondary" id="copyBtn">{'复制结果' if not is_en else 'Copy Result'}</button>
<button class="btn-secondary" id="downloadBtn">{'下载文件' if not is_en else 'Download'}</button>
</div>
<div class="tool-section" id="outputSection" style="display:none">
<h2>{'📄 生成的OpenAPI文档' if not is_en else '📄 Generated OpenAPI'}</h2>
<pre style="background:#0f172a;border:1px solid rgba(148,163,184,.15);border-radius:8px;padding:16px;overflow-x:auto;color:#e2e8f0;font-size:.8rem;font-family:monospace;white-space:pre-wrap;max-height:500px;overflow-y:auto" id="outputCode"></pre>
</div>
<script>
var endpoints = [];

document.getElementById("addEpBtn").addEventListener("click", function(){{
  var method = document.getElementById("epMethod").value;
  var path = document.getElementById("epPath").value.trim();
  var summary = document.getElementById("epSummary").value.trim();
  if(!path){{ showToast("{'请输入路径' if not is_en else 'Please enter a path'}"); return; }}
  endpoints.push({{method: method, path: path, summary: summary || path}});
  renderEpList();
  document.getElementById("epPath").value = "";
  document.getElementById("epSummary").value = "";
}});

document.getElementById("clearEpBtn").addEventListener("click", function(){{
  endpoints = [];
  renderEpList();
}});

function renderEpList(){{
  var el = document.getElementById("epList");
  if(endpoints.length === 0){{
    el.textContent = "{'暂无端点' if not is_en else 'No endpoints yet'}";
    return;
  }}
  el.innerHTML = "";
  for(var i=0;i<endpoints.length;i++){{
    var ep = endpoints[i];
    var span = document.createElement("span");
    span.style.cssText = "display:inline-block;margin:4px;padding:4px 10px;background:rgba(6,182,212,.1);border-radius:4px;font-family:monospace;font-size:.8rem;color:#22d3ee";
    var methodColor = "color:" + (ep.method === "GET" ? "#22c55e" : ep.method === "POST" ? "#3b82f6" : ep.method === "DELETE" ? "#ef4444" : "#f59e0b");
    span.innerHTML = "<span style=\\"" + methodColor + "\\">" + ep.method + "</span> " + ep.path;
    span.title = ep.summary;
    span.style.cursor = "pointer";
    span.addEventListener("click", function(){{
      var idx = Array.from(this.parentNode.children).indexOf(this);
      endpoints.splice(idx, 1);
      renderEpList();
    }});
    el.appendChild(span);
  }}
}}

function generateOpenAPI(format){{
  var title = document.getElementById("apiTitle").value.trim() || "My API";
  var version = document.getElementById("apiVersion").value.trim() || "1.0.0";
  var desc = document.getElementById("apiDesc").value.trim() || "";
  var server = document.getElementById("apiServer").value.trim() || "https://api.example.com";
  
  var spec = {{
    openapi: "3.0.3",
    info: {{ title: title, version: version, description: desc }},
    servers: [{{ url: server }}],
    paths: {{}}
  }};
  
  for(var i=0;i<endpoints.length;i++){{
    var ep = endpoints[i];
    if(!spec.paths[ep.path]) spec.paths[ep.path] = {{}};
    spec.paths[ep.path][ep.method.toLowerCase()] = {{
      summary: ep.summary,
      responses: {{ "200": {{ description: "Success" }} }}
    }};
  }}
  
  if(format === "json"){{
    return JSON.stringify(spec, null, 2);
  }} else {{
    return toYAML(spec);
  }}
}}

function toYAML(obj, indent) {{
  indent = indent || 0;
  var result = "";
  var prefix = "  ".repeat(indent);
  if(typeof obj === "object" && obj !== null && !Array.isArray(obj)){{
    var keys = Object.keys(obj);
    for(var i=0;i<keys.length;i++){{
      var key = keys[i];
      var val = obj[key];
      if(val === null || val === undefined) continue;
      if(typeof val === "object" && Object.keys(val).length === 0){{
        result += prefix + key + ": {{}}\\n";
      }} else if(typeof val === "object" && !Array.isArray(val)){{
        result += prefix + key + ":\\n" + toYAML(val, indent + 1);
      }} else if(Array.isArray(val)){{
        result += prefix + key + ":\\n";
        for(var j=0;j<val.length;j++){{
          result += prefix + "  - " + JSON.stringify(val[j]) + "\\n";
        }}
      }} else if(typeof val === "string"){{
        result += prefix + key + ": " + (val.includes(":") || val.includes("#") ? '"' + val + '"' : val) + "\\n";
      }} else {{
        result += prefix + key + ": " + val + "\\n";
      }}
    }}
  }}
  return result;
}}

document.getElementById("genYamlBtn").addEventListener("click", function(){{
  if(endpoints.length === 0){{ showToast("{'请先添加端点' if not is_en else 'Please add endpoints first'}"); return; }}
  var code = generateOpenAPI("yaml");
  document.getElementById("outputSection").style.display = "block";
  document.getElementById("outputCode").textContent = code;
}});

document.getElementById("genJsonBtn").addEventListener("click", function(){{
  if(endpoints.length === 0){{ showToast("{'请先添加端点' if not is_en else 'Please add endpoints first'}"); return; }}
  var code = generateOpenAPI("json");
  document.getElementById("outputSection").style.display = "block";
  document.getElementById("outputCode").textContent = code;
}});

document.getElementById("copyBtn").addEventListener("click", function(){{
  var code = document.getElementById("outputCode").textContent;
  if(!code){{ showToast("{'请先生成文档' if not is_en else 'Please generate first'}"); return; }}
  navigator.clipboard.writeText(code).then(function(){{
    showToast("{'已复制!' if not is_en else 'Copied!'}");
  }});
}});

document.getElementById("downloadBtn").addEventListener("click", function(){{
  var code = document.getElementById("outputCode").textContent;
  if(!code){{ showToast("{'请先生成文档' if not is_en else 'Please generate first'}"); return; }}
  var isJson = code.trim().startsWith("{{");
  var ext = isJson ? "json" : "yaml";
  var blob = new Blob([code], {{type: "text/plain"}});
  var a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = "openapi." + ext;
  a.click();
}});
</script>
'''
        
        footer = make_footer(t["cn_name"], t["en_name"], d, is_en)
        html = body + content + footer + TOAST_SCRIPT + '\n</body>\n</html>'
        
        fpath = f"{base}/index.html"
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"  ✅ {'EN' if is_en else 'CN'} {fpath}")

# Run all
print("=== 生成新工具页面 ===")
gen_nato()
gen_iso()
gen_time_diff()
gen_pixel()
gen_openapi()
print("=== 完成 ===")
