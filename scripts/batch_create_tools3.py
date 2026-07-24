#!/usr/bin/env python3
"""批量创建10个新工具（中英文双语）"""

import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = [
    {
        "slug": "tint-image",
        "name_zh": "图片色调调整",
        "name_en": "Image Tint Tool",
        "desc_zh": "在线图片色调调整工具，支持上传图片并应用色彩滤镜。可调整色相、饱和度、亮度，实时预览效果。无需上传服务器，本地处理保护隐私。",
        "desc_en": "Free online image tint tool. Upload an image and apply color filters. Adjust hue, saturation, brightness with live preview. All processing done locally, no upload required.",
        "hero_zh": "上传图片，拖动滑块调整色调、饱和度、亮度。支持多种预设滤镜效果。所有处理在浏览器本地完成，保护隐私安全。",
        "hero_en": "Upload an image, drag sliders to adjust hue, saturation, and brightness. Multiple preset filter effects available. All processing done locally in your browser.",
    },
    {
        "slug": "terms-of-service-generator",
        "name_zh": "服务条款生成器",
        "name_en": "Terms of Service Generator",
        "desc_zh": "免费在线服务条款/使用协议生成器。选择网站类型填写基本信息，一键生成专业的服务条款文档。适用于网站、App、SaaS等。",
        "desc_en": "Free online Terms of Service generator. Select your website type, fill in basic info, and generate a professional TOS document. Suitable for websites, apps, and SaaS.",
        "hero_zh": "选择您的业务类型，填写基本信息，即可生成专业服务条款。支持网站、移动应用、SaaS平台等场景。生成内容仅供参考，建议咨询法律专业人士。",
        "hero_en": "Select your business type, fill in basic info, and generate professional terms of service. Supports websites, mobile apps, and SaaS platforms. Generated content is for reference only.",
    },
    {
        "slug": "recipe-analyzer",
        "name_zh": "食谱营养分析器",
        "name_en": "Recipe Nutrition Analyzer",
        "desc_zh": "免费在线食谱营养分析工具。输入食材和用量，计算总热量、蛋白质、脂肪、碳水等营养成分。支持自定义食材数据库，适合健身和饮食管理。",
        "desc_en": "Free online recipe nutrition analyzer. Enter ingredients and amounts to calculate total calories, protein, fat, carbs, and more. Supports custom ingredient database.",
        "hero_zh": "输入食谱的食材和用量，自动计算营养成分。支持热量、蛋白质、脂肪、碳水化合物、纤维等关键指标分析。适合健身爱好者、营养师和家庭烹饪。",
        "hero_en": "Enter recipe ingredients and amounts to auto-calculate nutrition facts. Supports calories, protein, fat, carbs, fiber and key metrics. Ideal for fitness enthusiasts and home cooking.",
    },
    {
        "slug": "nutrition-analyzer",
        "name_zh": "食物营养成分查询",
        "name_en": "Food Nutrition Lookup",
        "desc_zh": "免费在线食物营养成分查询工具。搜索常见食物查看详细营养数据，包括热量、蛋白质、脂肪、碳水、维生素和矿物质含量。数据来源于权威营养数据库。",
        "desc_en": "Free online food nutrition lookup tool. Search common foods to view detailed nutrition data including calories, protein, fat, carbs, vitamins and minerals. Data from authoritative sources.",
        "hero_zh": "搜索或选择食物名称，查看详细营养成分表。包含热量、宏量营养素、维生素、矿物质等完整数据。支持中英文食物搜索，数据持续更新。",
        "hero_en": "Search or select food items to view detailed nutrition facts. Includes calories, macronutrients, vitamins, minerals and more. Supports both Chinese and English food search.",
    },
    {
        "slug": "gradient-extractor",
        "name_zh": "渐变色提取器",
        "name_en": "Gradient Extractor",
        "desc_zh": "免费在线渐变色提取工具。从图片中智能提取主色调和渐变色方案，生成CSS渐变代码。支持线性渐变和径向渐变，一键复制CSS代码。",
        "desc_en": "Free online gradient extractor. Intelligently extract dominant colors and gradient schemes from images, generating CSS gradient code. Supports linear and radial gradients.",
        "hero_zh": "上传一张图片，自动提取主色调并生成渐变色方案。支持多种渐变方向和类型，一键复制CSS代码到项目中。适合设计师和前端开发者。",
        "hero_en": "Upload an image to auto-extract dominant colors and generate gradient schemes. Supports multiple gradient directions and types. Copy CSS code with one click.",
    },
    {
        "slug": "font-pair",
        "name_zh": "字体搭配推荐器",
        "name_en": "Font Pairing Generator",
        "desc_zh": "免费在线字体搭配推荐工具。浏览精选的Google Fonts字体搭配方案，支持标题+正文组合预览。可自定义文字内容实时查看效果，适合网页设计。",
        "desc_en": "Free online font pairing tool. Browse curated Google Fonts pairings with heading + body text preview. Customize text content to preview in real-time. Perfect for web design.",
        "hero_zh": "浏览精选字体搭配方案，实时预览标题和正文效果。支持中英文常用字体组合，可自定义预览文字。点击即可复制CSS引用代码。",
        "hero_en": "Browse curated font pairings with real-time heading and body text preview. Supports popular Chinese and English font combinations. Click to copy CSS import code.",
    },
    {
        "slug": "audio-cutter",
        "name_zh": "在线音频剪切器",
        "name_en": "Online Audio Cutter",
        "desc_zh": "免费在线音频剪切工具。上传音频文件，设置起止时间精确剪切。支持MP3、WAV、OGG等格式。所有处理在浏览器本地完成，无需上传服务器。",
        "desc_en": "Free online audio cutter. Upload audio files, set start/end times to precisely trim. Supports MP3, WAV, OGG formats. All processing done locally in your browser.",
        "hero_zh": "上传音频文件，拖动时间轴设置剪切范围。支持精确到秒的剪切控制，可试听选区效果。处理后直接下载，无需上传到服务器。",
        "hero_en": "Upload an audio file, drag the timeline to set trim range. Supports precise second-level trimming with preview. Download directly after processing, no server upload needed.",
    },
    {
        "slug": "video-cutter",
        "name_zh": "在线视频剪切器",
        "name_en": "Online Video Cutter",
        "desc_zh": "免费在线视频剪切工具。上传视频文件，设置起止时间快速裁剪。支持MP4、WebM、MOV等格式。本地处理不传服务器，安全快速。",
        "desc_en": "Free online video cutter. Upload video files, set start/end times to quickly trim. Supports MP4, WebM, MOV formats. Local processing, no server upload, safe and fast.",
        "hero_zh": "上传视频文件，拖动时间轴设置裁剪范围。支持精确到帧的剪切控制，可预览选区。处理后直接下载，所有操作在浏览器本地完成。",
        "hero_en": "Upload a video file, drag the timeline to set trim range. Supports frame-accurate trimming with preview. Download directly, all operations done locally in browser.",
    },
    {
        "slug": "unit-converter-advanced",
        "name_zh": "高级单位换算器",
        "name_en": "Advanced Unit Converter",
        "desc_zh": "免费在线高级单位换算工具。支持长度、重量、温度、面积、体积、速度、压力、能量、功率、数据存储等20+类别。界面简洁，实时换算。",
        "desc_en": "Free online advanced unit converter. Supports 20+ categories including length, weight, temperature, area, volume, speed, pressure, energy, power, data storage. Clean interface, real-time conversion.",
        "hero_zh": "选择单位类别，输入数值即可实时换算。覆盖长度、重量、温度、面积、体积、速度、压力、能量、功率、数据存储等20+类别，200+单位。",
        "hero_en": "Select a category, enter a value for real-time conversion. Covers 20+ categories including length, weight, temperature, area, volume, speed, pressure, energy, power, data storage, 200+ units.",
    },
    {
        "slug": "image-censor",
        "name_zh": "图片马赛克工具",
        "name_en": "Image Censor Tool",
        "desc_zh": "免费在线图片马赛克/模糊工具。在图片上拖动选择区域添加马赛克或模糊效果。支持调节马赛克大小和模糊强度。本地处理，保护隐私。",
        "desc_en": "Free online image mosaic/blur tool. Drag to select areas on an image and apply mosaic or blur effects. Adjustable mosaic size and blur intensity. Local processing, privacy protected.",
        "hero_zh": "上传图片，拖动鼠标选择需要打码的区域。支持马赛克和模糊两种效果，可调节强度。所有处理在浏览器本地完成，不上传服务器。",
        "hero_en": "Upload an image, drag to select areas to censor. Supports mosaic and blur effects with adjustable intensity. All processing done locally in your browser.",
    },
]

def escape_js(s):
    return s.replace('\\', '\\\\').replace("'", "\\'").replace('\n', '\\n')

def make_html(tool, lang='zh'):
    is_zh = lang == 'zh'
    slug = tool['slug']
    name = tool['name_zh'] if is_zh else tool['name_en']
    desc = tool['desc_zh'] if is_zh else tool['desc_en']
    hero = tool['hero_zh'] if is_zh else tool['hero_en']
    lang_code = 'zh-CN' if is_zh else 'en'
    og_locale = 'zh_CN' if is_zh else 'en_US'
    canon = f'https://free-toolbase.com/{slug}/' if is_zh else f'https://free-toolbase.com/en/{slug}/'
    alt_zh = f'https://free-toolbase.com/{slug}/'
    alt_en = f'https://free-toolbase.com/en/{slug}/'
    alt_href = alt_en if is_zh else alt_zh
    alt_lang = 'en' if is_zh else 'zh'
    home_link = '../index.html' if is_zh else '../../index.html'
    home_text = '首页' if is_zh else 'Home'
    tools_text = '工具' if is_zh else 'Tools'
    en_link = f'../en/{slug}/' if is_zh else f'index.html'
    zh_link = '../index.html' if is_zh else f'../../{slug}/index.html'
    
    title_full = f'{name} - Free ToolBase'
    kw = '工具,在线工具,免费' if is_zh else 'tool,online tool,free'
    
    # Features text
    if is_zh:
        feature_title = '功能说明'
        feature_lines = [
            desc,
            '所有处理在浏览器本地完成，无需上传文件到服务器。',
            '完全免费，无需注册或登录，即开即用。',
        ]
        faq_title = '常见问题'
        faq = [
            ('文件安全吗？', '所有处理在浏览器本地完成，文件不会上传到任何服务器，请放心使用。'),
            ('需要注册吗？', '完全不需要注册或登录，打开即可使用。'),
            ('移动端能用吗？', '完美适配手机和平板等移动设备，随时随地使用。'),
            ('支持哪些格式？', '支持主流格式，具体支持范围请参考工具页面的说明。'),
        ]
        privacy_text = '隐私政策'
        terms_text = '服务条款'
        copyright_text = '© 2026 Free ToolBase'
    else:
        feature_title = 'Features'
        feature_lines = [
            desc,
            'All processing is done locally in your browser — no files are uploaded to any server.',
            'Completely free, no registration or login required. Ready to use instantly.',
        ]
        faq_title = 'FAQ'
        faq = [
            ('Is my file safe?', 'All processing is done locally in your browser. Files are never uploaded to any server.'),
            ('Do I need to register?', 'No registration or login required. Just open and use.'),
            ('Does it work on mobile?', 'Fully responsive — works perfectly on phones and tablets.'),
            ('What formats are supported?', 'Common formats are supported. See the tool page for specific details.'),
        ]
        privacy_text = 'Privacy'
        terms_text = 'Terms'
        copyright_text = '© 2026 Free ToolBase'

    features_html = ''.join(f'<p>{line}</p>' for line in feature_lines)
    faq_html = ''.join(f'<div class="faq-item"><h3>{q}</h3><p>{a}</p></div>' for q, a in faq)

    html = f'''<!DOCTYPE html>
<html lang="{lang_code}">
<head>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-9W1157EBQV"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-9W1157EBQV');</script>
<script>window.addEventListener("error",function(e){{if(e&&e.message===""){{e.preventDefault();}}}});window.addEventListener("unhandledrejection",function(e){{if(e&&e.reason&&e.reason.message===""){{e.preventDefault();}}}});</script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="{desc}">
<meta name="keywords" content="{kw}">
<title>{title_full}</title>
<link rel="canonical" href="{canon}">
<meta property="og:title" content="{title_full}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canon}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Free ToolBase">
<meta property="og:locale" content="{og_locale}">
<link rel="alternate" hreflang="zh" href="{alt_zh}">
<link rel="alternate" hreflang="en" href="{alt_en}">
<link rel="alternate" hreflang="x-default" href="{alt_en}">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"SoftwareApplication","name":"{escape_js(name)}","description":"{escape_js(desc)}","applicationCategory":"UtilitiesApplication","operatingSystem":"Web","publisher":{{"@type":"Organization","name":"Free ToolBase","email":"dexshuang@google.com"}},"offers":{{"@type":"Offer","price":"0","priceCurrency":"USD"}}}}</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"HowTo","name":"{escape_js('如何使用' + name if is_zh else 'How to use ' + name)}","description":"{escape_js('使用' + name + '的详细步骤指南' if is_zh else 'Step-by-step guide for using ' + name)}","totalTime":"PT2M","tool":{{"@type":"HowToTool","name":"{escape_js(name)}"}},"step":[{{"@type":"HowToStep","position":1,"name":"{escape_js('输入数据' if is_zh else 'Enter data')}","text":"{escape_js('在输入框中输入需要处理的数据' if is_zh else 'Enter the data to process in the input field')}"}},{{"@type":"HowToStep","position":2,"name":"{escape_js('选择选项' if is_zh else 'Select options')}","text":"{escape_js('根据需要选择处理模式或参数' if is_zh else 'Choose processing mode or parameters as needed')}"}},{{"@type":"HowToStep","position":3,"name":"{escape_js('执行操作' if is_zh else 'Execute')}","text":"{escape_js('点击执行按钮获取结果' if is_zh else 'Click the execute button to get results')}"}},{{"@type":"HowToStep","position":4,"name":"{escape_js('查看结果' if is_zh else 'View results')}","text":"{escape_js('查看处理结果，支持一键复制或下载' if is_zh else 'View results with one-click copy or download')}"}}]}}</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"{escape_js('首页' if is_zh else 'Home')}","item":"{escape_js('https://free-toolbase.com/')}"}},{{"@type":"ListItem","position":2,"name":"{escape_js('工具' if is_zh else 'Tools')}","item":"{escape_js('https://free-toolbase.com/#tools')}"}},{{"@type":"ListItem","position":3,"name":"{escape_js(name)}","item":"{escape_js(canon)}"}}]}}</script>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#0f172a;color:#e2e8f0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,"PingFang SC","Microsoft YaHei",sans-serif;line-height:1.6;min-height:100vh}}
a{{color:#06b6d4;text-decoration:none}}
.container{{max-width:800px;margin:0 auto;padding:24px 16px}}
.header{{display:flex;justify-content:space-between;align-items:center;margin-bottom:24px;flex-wrap:wrap;gap:12px}}
.header h1{{font-size:1.6rem;color:#f1f5f9}}
.lang-switch{{display:flex;gap:4px;background:#1e293b;border-radius:8px;padding:4px;border:1px solid rgba(148,163,184,.1)}}
.lang-switch a{{padding:6px 12px;border-radius:5px;font-size:.85rem;color:#94a3b8}}
.lang-switch a.active{{background:rgba(6,182,212,.2);color:#22d3ee}}
.nav-back{{color:#64748b;font-size:.85rem;margin-bottom:16px}}
.nav-back a{{color:#64748b}}
.nav-back a:hover{{color:#94a3b8}}
.input-section{{background:#1e293b;border-radius:12px;padding:20px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1)}}
.input-section h2{{font-size:1.1rem;color:#f1f5f9;margin-bottom:12px}}
label{{display:block;font-size:.9rem;color:#94a3b8;margin-bottom:6px}}
input[type="text"],input[type="number"],input[type="file"],select,textarea{{width:100%;padding:12px;background:#0f172a;color:#e2e8f0;border:1px solid rgba(148,163,184,.2);border-radius:8px;font-size:1rem;outline:none;font-family:inherit}}
input:focus,select:focus,textarea:focus{{border-color:rgba(6,182,212,.5)}}
input[type="range"]{{width:100%;accent-color:#06b6d4}}
textarea{{min-height:100px;resize:vertical}}
.btn-row{{display:flex;gap:8px;flex-wrap:wrap;margin-top:16px}}
.btn{{padding:10px 24px;border:none;border-radius:6px;font-size:.9rem;cursor:pointer;transition:all .2s;font-weight:600}}
.btn-primary{{background:rgba(6,182,212,.2);color:#22d3ee;border:1px solid rgba(6,182,212,.3)}}
.btn-primary:hover{{background:rgba(6,182,212,.3)}}
.btn-secondary{{background:rgba(148,163,184,.1);color:#94a3b8;border:1px solid rgba(148,163,184,.2)}}
.btn-secondary:hover{{background:rgba(148,163,184,.2)}}
.btn-danger{{background:rgba(239,68,68,.15);color:#f87171;border:1px solid rgba(239,68,68,.2)}}
.btn-danger:hover{{background:rgba(239,68,68,.25)}}
.btn-success{{background:rgba(34,197,94,.15);color:#4ade80;border:1px solid rgba(34,197,94,.2)}}
.btn-success:hover{{background:rgba(34,197,94,.25)}}
.result-section{{background:#1e293b;border-radius:12px;padding:20px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1);display:none}}
.result-section.show{{display:block}}
.result-section h2{{font-size:1.1rem;color:#f1f5f9;margin-bottom:16px}}
.result-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px}}
.result-card{{background:#0f172a;border-radius:8px;padding:16px;border:1px solid rgba(148,163,184,.1)}}
.result-card .label{{font-size:.8rem;color:#94a3b8;margin-bottom:4px}}
.result-card .value{{font-size:1.5rem;color:#22d3ee;font-weight:600}}
.result-card .sub{{font-size:.8rem;color:#64748b;margin-top:4px}}
.info-section{{background:#1e293b;border-radius:12px;padding:20px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1)}}
.info-section h2{{font-size:1.1rem;color:#f1f5f9;margin-bottom:12px}}
.info-section p,.info-section li{{color:#94a3b8;font-size:.9rem;margin-bottom:8px}}
.info-section ul{{padding-left:20px}}
.info-section h3{{font-size:1rem;color:#e2e8f0;margin:16px 0 8px}}
.faq-item{{margin-bottom:12px;padding:12px;background:#0f172a;border-radius:8px;border:1px solid rgba(148,163,184,.1)}}
.faq-item h3{{font-size:.95rem;color:#e2e8f0;margin-bottom:6px}}
.faq-item p{{color:#94a3b8;font-size:.85rem}}
.form-row{{display:flex;gap:12px;flex-wrap:wrap}}
.form-row .form-group{{flex:1;min-width:150px}}
.form-group{{margin-bottom:12px}}
.footer{{border-top:1px solid rgba(148,163,184,.1);padding:24px 0;margin-top:48px;text-align:center;color:#64748b;font-size:.85rem}}
.footer a{{color:#06b6d4}}
.hero{{margin-bottom:16px;color:#94a3b8;font-size:.95rem}}
.hero p{{margin-bottom:4px}}
.badge{{display:inline-block;background:rgba(6,182,212,.15);color:#22d3ee;padding:4px 12px;border-radius:20px;font-size:.8rem;margin-bottom:16px}}
.ad-slot{{margin:16px auto;text-align:center;max-width:960px;min-height:90px;background:rgba(148,163,184,.05);border-radius:8px}}
.ad-slot:empty{{display:none}}
.preview-area{{background:#0f172a;border-radius:8px;padding:16px;text-align:center;min-height:100px;display:flex;align-items:center;justify-content:center;margin-top:12px;border:1px dashed rgba(148,163,184,.2)}}
.slider-group{{margin-bottom:12px}}
.slider-group .range-label{{display:flex;justify-content:space-between;font-size:.85rem;color:#94a3b8;margin-bottom:4px}}
canvas{{max-width:100%;border-radius:8px}}
@media(max-width:640px){{.header{{flex-direction:column;align-items:flex-start}}.result-grid{{grid-template-columns:1fr}}.form-row{{flex-direction:column}}.form-row .form-group{{min-width:100%}}}}
.toast{{position:fixed;bottom:24px;left:50%;transform:translateX(-50%);background:#1e293b;color:#e2e8f0;padding:12px 24px;border-radius:8px;font-size:.9rem;border:1px solid rgba(148,163,184,.15);opacity:0;transition:opacity .3s;pointer-events:none;z-index:999}}
.toast.show{{opacity:1}}
</style>
</head>
<body>
<div class="container">
<div class="header"><h1>{name}</h1><div class="lang-switch"><a href="{zh_link}" class="{'active' if is_zh else ''}">中文</a><a href="{en_link}" class="{'' if is_zh else 'active'}">EN</a></div></div>
<p class="nav-back"><a href="{home_link}">{home_text}</a> &rsaquo; <a href="{home_link}#tools">{tools_text}</a> &rsaquo; {name}</p>
<div class="hero"><p>{hero}</p><span class="badge">{'零依赖·可离线使用' if is_zh else 'No dependencies · Works offline'}</span></div>

<!-- TOOL-SPECIFIC CONTENT PLACEHOLDER -->

<div class="info-section">
<h2>{feature_title}</h2>
{features_html}
<h3>{faq_title}</h3>
{faq_html}
</div>
<div class="footer"><p>{copyright_text} | <a href="{'../privacy/' if is_zh else '../../privacy/'}">{privacy_text}</a> | <a href="{'../terms/' if is_zh else '../../terms/'}">{terms_text}</a></p></div>
</div>
<div class="toast" id="toast"></div>
<script>
function showToast(msg){{var t=document.getElementById('toast');t.textContent=msg;t.classList.add('show');setTimeout(function(){{t.classList.remove('show')}},2000)}}
</script>
</body>
</html>'''
    return html


def main():
    for tool in TOOLS:
        slug = tool['slug']
        # 中文版
        zh_dir = os.path.join(BASE, slug)
        os.makedirs(zh_dir, exist_ok=True)
        zh_path = os.path.join(zh_dir, 'index.html')
        with open(zh_path, 'w', encoding='utf-8') as f:
            f.write(make_html(tool, 'zh'))
        print(f'Created: {slug}/index.html (zh)')
        
        # 英文版
        en_dir = os.path.join(BASE, 'en', slug)
        os.makedirs(en_dir, exist_ok=True)
        en_path = os.path.join(en_dir, 'index.html')
        with open(en_path, 'w', encoding='utf-8') as f:
            f.write(make_html(tool, 'en'))
        print(f'Created: en/{slug}/index.html (en)')

if __name__ == '__main__':
    main()