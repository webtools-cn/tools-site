#!/usr/bin/env python3
"""快速生成计算器工具 — 输入规格 → 自动输出 CN+EN 两个 HTML"""
import json, os, sys

def gen_tool(slug, cn_name, en_name, cn_desc, en_desc, inputs_cn, inputs_en, calc_js):
    """生成一个计算器工具
    
    inputs_cn: [(label, placeholder), ...]
    inputs_en: [(label, placeholder), ...]
    calc_js: JS计算逻辑 (使用变量 a,b,c,... 对应v1,v2,v3,...)
    """
    os.makedirs(slug, exist_ok=True)
    os.makedirs(f'en/{slug}', exist_ok=True)
    
    # 生成input HTML
    cn_inputs = ''
    en_inputs = ''
    for i, ((cnl, cnp), (enl, enp)) in enumerate(zip(inputs_cn, inputs_en)):
        vid = f'v{i+1}'
        cn_inputs += f'<div class="form-group"><label>{cnl}</label><input type="number" id="{vid}" placeholder="{cnp}" step="any"></div>\n'
        en_inputs += f'<div class="form-group"><label>{enl}</label><input type="number" id="{vid}" placeholder="{enp}" step="any"></div>\n'
    
    # 读取模板
    with open('scripts/template.html', encoding='utf-8') as f:
        tpl = f.read()
    
    # CN版
    cn_html = tpl.replace('SLUG', slug)
    cn_html = cn_html.replace('TOOL_NAME_CN', cn_name)
    cn_html = cn_html.replace('TOOL_DESC_CN_SEO', cn_desc[:160])
    cn_html = cn_html.replace('TOOL_DESC_CN_SHORT', cn_desc[:80])
    cn_html = cn_html.replace('PERCENTAGE_CALC', cn_name)
    cn_html = cn_html.replace('PERCENTAGE_DESC_CN', cn_desc)
    cn_html = cn_html.replace('PERCENTAGE_LABEL2', '')
    cn_html = cn_html.replace('PERCENTAGE_PH2', '')
    cn_html = cn_html.replace('PERCENTAGE_LABEL', inputs_cn[0][0])
    cn_html = cn_html.replace('PERCENTAGE_PH', inputs_cn[0][1])
    cn_html = cn_html.replace('<!-- PERCENTAGE_LOGIC -->', calc_js)
    # 动态替换inputs — 使用INPUTS_PLACEHOLDER
    cn_html = cn_html.replace('<!-- INPUTS_PLACEHOLDER -->', cn_inputs.rstrip())
    # 替换SEO占位符
    cn_html = cn_html.replace('TOOL_SEO_INTRO_CN', f'{cn_name}是一款免费在线工具，{cn_desc}。支持手机和电脑，所有计算在浏览器本地完成，数据安全不上传。')
    cn_html = cn_html.replace('TOOL_STEP1_CN', f'输入第一个参数')
    cn_html = cn_html.replace('TOOL_STEP2_CN', f'输入第二个参数')
    cn_html = cn_html.replace('TOOL_STEP3_CN', f'点击"计算"按钮查看结果')
    cn_html = cn_html.replace('FAQ_PLACEHOLDER_CN', f'<h3>这个工具准确吗？</h3><p>计算公式基于标准数学公式，结果精确可靠。</p><h3>需要下载吗？</h3><p>完全不需要，打开网页即可使用，纯前端计算。</p>')
    cn_html = cn_html.replace('FAQ_CN_JSON', f'[{{"@type":"Question","name":"这个工具准确吗？","acceptedAnswer":{{"@type":"Answer","text":"计算公式基于标准数学公式，结果精确可靠。"}}}},{{"@type":"Question","name":"需要下载吗？","acceptedAnswer":{{"@type":"Answer","text":"完全不需要，打开网页即可使用，纯前端计算。"}}}}]')
    
    with open(f'{slug}/index.html', 'w', encoding='utf-8') as f:
        f.write(cn_html)
    
    # EN版
    en_html = tpl.replace('SLUG', slug)
    en_html = en_html.replace('lang="zh-CN"', 'lang="en"')
    en_html = en_html.replace('PERCENTAGE_CALC', en_name)
    en_html = en_html.replace('PERCENTAGE_DESC_CN', en_desc)
    en_html = en_html.replace('🧮 计算', '🧮 Calculate')
    en_html = en_html.replace('请输入有效数值', 'Please enter valid numbers')
    en_html = en_html.replace('所有计算在浏览器本地完成', 'All calculations run locally in your browser')
    en_html = en_html.replace('首页', 'Home')
    en_html = en_html.replace('PERCENTAGE_LABEL', inputs_en[0][0])
    en_html = en_html.replace('PERCENTAGE_PH', inputs_en[0][1])
    en_html = en_html.replace(
        'href="/"> Free ToolBase',
        'href="/en/"> Free ToolBase'
    )
    en_html = en_html.replace(
        'href="/en/SLUG/">English',
        'href="/SLUG/">中文'
    )
    en_html = en_html.replace('<!-- INPUTS_PLACEHOLDER -->', en_inputs.rstrip())
    # 修复canonical
    en_html = en_html.replace(
        'href="https://free-toolbase.com/SLUG/"',
        'href="https://free-toolbase.com/en/SLUG/"'
    )
    en_html = en_html.replace(
        'href="https://free-toolbase.com/' + slug + '/"',
        'href="https://free-toolbase.com/en/' + slug + '/"'
    )
    # 修复alternate
    en_html = en_html.replace(
        'href="https://free-toolbase.com/SLUG/" />',
        'href="https://free-toolbase.com/SLUG/" />',
    )
    en_html = en_html.replace('<!-- PERCENTAGE_LOGIC -->', calc_js)
    
    with open(f'en/{slug}/index.html', 'w', encoding='utf-8') as f:
        f.write(en_html)
    
    # 注册JSON
    for lang, jf, name, desc in [('cn', 'tools-data-cn.json', cn_name, cn_desc), ('en', 'tools-data-en.json', en_name, en_desc)]:
        with open(jf) as f:
            data = json.load(f)
        data['calc-tools'].append(['📐', name, desc, f'{slug}/'])
        with open(jf, 'w') as f:
            json.dump(data, f, ensure_ascii=False)
    
    # sitemap
    with open('sitemap.xml') as f:
        sm = f.read()
    # CN URL
    if f'/{slug}/' not in sm:
        sm = sm.replace('</urlset>', f'  <url><loc>https://free-toolbase.com/{slug}/</loc><changefreq>monthly</changefreq></url>\n</urlset>')
    # EN URL
    if f'/en/{slug}/' not in sm:
        sm = sm.replace('</urlset>', f'  <url><loc>https://free-toolbase.com/en/{slug}/</loc><changefreq>monthly</changefreq></url>\n</urlset>')
    with open('sitemap.xml', 'w') as f:
        f.write(sm)
    
    print(f'✅ {slug}: {cn_name} (CN+EN+JSON+sitemap)')

# ====== 批量生成 ======
TOOLS = [
    {
        'slug': 'percentage-change-calculator',
        'cn_name': '百分比变化计算器',
        'en_name': 'Percentage Change Calculator',
        'cn_desc': '计算数值从旧值到新值的百分比变化幅度',
        'en_desc': 'Calculate the percentage change from an old value to a new value',
        'inputs_cn': [('旧值', '如: 100'), ('新值', '如: 120')],
        'inputs_en': [('Old Value', 'e.g. 100'), ('New Value', 'e.g. 120')],
        'calc_js': 'var ch=((b-a)/a)*100;document.getElementById("rv").textContent=ch.toFixed(2)+"%";document.getElementById("result").style.display="block"',
    },
    {
        'slug': 'paint-coverage-calculator',
        'cn_name': '油漆用量计算器',
        'en_name': 'Paint Coverage Calculator',
        'cn_desc': '根据墙面面积计算所需油漆用量',
        'en_desc': 'Calculate paint needed based on wall area',
        'inputs_cn': [('墙面总面积(m²)', '如: 50'), ('每升覆盖面积(m²)', '如: 10')],
        'inputs_en': [('Total Wall Area (m²)', 'e.g. 50'), ('Coverage per Liter (m²)', 'e.g. 10')],
        'calc_js': 'var g=a/b;document.getElementById("rv").innerHTML="需要 <b>"+g.toFixed(1)+" 升</b> 油漆<br>≈ "+(Math.ceil(g*10)/10).toFixed(1)+" 升 (冗余10%)";document.getElementById("result").style.display="block"',
    },
    {
        'slug': 'amortization-calculator',
        'cn_name': '等额本息还款计算器',
        'en_name': 'Amortization Calculator',
        'cn_desc': '计算等额本息贷款的月供和总利息',
        'en_desc': 'Calculate monthly payment and total interest for amortized loans',
        'inputs_cn': [('贷款总额(元)', '如: 1000000'), ('年利率(%)', '如: 4.5'), ('贷款年数', '如: 30')],
        'inputs_en': [('Loan Amount ($)', 'e.g. 100000'), ('Annual Rate (%)', 'e.g. 4.5'), ('Years', 'e.g. 30')],
        'calc_js': 'var c=parseFloat(document.getElementById("v3").value);var mr=a/100/12;var n=c*12;var mp=mr===0?a/n:a*mr*Math.pow(1+mr,n)/(Math.pow(1+mr,n)-1);var ti=mp*n-a;document.getElementById("rv").innerHTML="月供: <b>"+mp.toFixed(2)+"</b><br>总利息: <b>"+ti.toFixed(2)+"</b><br>还款总额: <b>"+(a+ti).toFixed(2)+"</b>";document.getElementById("result").style.display="block"',
    },
]

for t in TOOLS:
    gen_tool(**t)

print(f'\n生成了 {len(TOOLS)} 个工具')
