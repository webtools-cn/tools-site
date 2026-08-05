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
        'slug': 'roi-calculator',
        'cn_name': 'ROI计算器',
        'en_name': 'ROI Calculator',
        'cn_desc': '输入投资金额和收益金额，计算投资回报率(ROI)',
        'en_desc': 'Calculate Return on Investment (ROI) with investment amount and returns',
        'inputs_cn': [('投资金额(元)', '如: 10000'), ('收益金额(元)', '如: 15000')],
        'inputs_en': [('Investment ($)', 'e.g. 10000'), ('Return ($)', 'e.g. 15000')],
        'calc_js': 'var roi=(b-a)/a*100;document.getElementById("rv").innerHTML="ROI: <b>"+roi.toFixed(2)+"%</b><br>净收益: <b>"+(b-a).toFixed(2)+"</b><br>"+(roi>=0?"✅ 盈利":"❌ 亏损");document.getElementById("result").style.display="block"',
    },
    {
        'slug': 'compound-interest-calculator',
        'cn_name': '复利计算器',
        'en_name': 'Compound Interest Calculator',
        'cn_desc': '输入本金、年利率和投资年限，计算复利终值和总收益',
        'en_desc': 'Calculate compound interest future value with principal, annual rate and years',
        'inputs_cn': [('本金(元)', '如: 10000'), ('年利率(%)', '如: 5'), ('投资年限', '如: 10')],
        'inputs_en': [('Principal ($)', 'e.g. 10000'), ('Annual Rate (%)', 'e.g. 5'), ('Years', 'e.g. 10')],
        'calc_js': 'var r=b/100;var fv=a*Math.pow(1+r,c);document.getElementById("rv").innerHTML="复利终值: <b>"+fv.toFixed(2)+"</b><br>总收益: <b>"+(fv-a).toFixed(2)+"</b><br>增长倍数: <b>"+(fv/a).toFixed(2)+"×</b>";document.getElementById("result").style.display="block"',
    },
    {
        'slug': 'rectangle-area-calculator',
        'cn_name': '矩形面积计算器',
        'en_name': 'Rectangle Area Calculator',
        'cn_desc': '输入矩形的长和宽，计算面积和周长',
        'en_desc': 'Calculate rectangle area and perimeter with length and width',
        'inputs_cn': [('长度(m)', '如: 5'), ('宽度(m)', '如: 3')],
        'inputs_en': [('Length (m)', 'e.g. 5'), ('Width (m)', 'e.g. 3')],
        'calc_js': 'var area=a*b;var peri=2*(a+b);document.getElementById("rv").innerHTML="面积: <b>"+area.toFixed(2)+" m²</b><br>周长: <b>"+peri.toFixed(2)+" m</b><br>对角线: <b>"+Math.sqrt(a*a+b*b).toFixed(2)+" m</b>";document.getElementById("result").style.display="block"',
    },
    {
        'slug': 'cylinder-volume-calculator',
        'cn_name': '圆柱体积计算器',
        'en_name': 'Cylinder Volume Calculator',
        'cn_desc': '输入圆柱的底面半径和高度，计算体积和表面积',
        'en_desc': 'Calculate cylinder volume and surface area with radius and height',
        'inputs_cn': [('半径(m)', '如: 2'), ('高度(m)', '如: 5')],
        'inputs_en': [('Radius (m)', 'e.g. 2'), ('Height (m)', 'e.g. 5')],
        'calc_js': 'var vol=Math.PI*a*a*b;var sa=2*Math.PI*a*(a+b);document.getElementById("rv").innerHTML="体积: <b>"+vol.toFixed(2)+" m³</b><br>表面积: <b>"+sa.toFixed(2)+" m²</b><br>侧面积: <b>"+(2*Math.PI*a*b).toFixed(2)+" m²</b>";document.getElementById("result").style.display="block"',
    },
    {
        'slug': 'loan-emi-calculator',
        'cn_name': '贷款月供计算器',
        'en_name': 'Loan EMI Calculator',
        'cn_desc': '输入贷款金额、年利率和期限，计算等额本息的每月还款额',
        'en_desc': 'Calculate monthly EMI payment with loan amount, annual rate and tenure',
        'inputs_cn': [('贷款金额(元)', '如: 500000'), ('年利率(%)', '如: 4.5'), ('贷款期限(年)', '如: 20')],
        'inputs_en': [('Loan Amount ($)', 'e.g. 500000'), ('Annual Rate (%)', 'e.g. 4.5'), ('Tenure (Years)', 'e.g. 20')],
        'calc_js': 'var mr=b/100/12;var n=c*12;var emi=a*mr*Math.pow(1+mr,n)/(Math.pow(1+mr,n)-1);document.getElementById("rv").innerHTML="月供: <b>"+emi.toFixed(2)+"</b><br>总还款: <b>"+(emi*n).toFixed(2)+"</b><br>总利息: <b>"+(emi*n-a).toFixed(2)+"</b>";document.getElementById("result").style.display="block"',
    },
    {
        'slug': 'gpa-calculator',
        'cn_name': 'GPA计算器',
        'en_name': 'GPA Calculator',
        'cn_desc': '输入课程分数和学分，计算加权平均绩点(GPA)',
        'en_desc': 'Calculate weighted GPA with course scores and credits',
        'inputs_cn': [('课程1分数', '如: 85'), ('课程1学分', '如: 3'), ('课程2分数', '如: 90'), ('课程2学分', '如: 4')],
        'inputs_en': [('Course 1 Score', 'e.g. 85'), ('Course 1 Credit', 'e.g. 3'), ('Course 2 Score', 'e.g. 90'), ('Course 2 Credit', 'e.g. 4')],
        'calc_js': 'function g(x){return x>=90?4:x>=80?3:x>=70?2:x>=60?1:0}var w1=g(a)*b;var w2=g(c)*d;var gpa=(w1+w2)/(b+d);document.getElementById("rv").innerHTML="加权GPA: <b>"+gpa.toFixed(2)+" / 4.0</b><br>课程1绩点: <b>"+g(a)+"</b><br>课程2绩点: <b>"+g(c)+"</b>";document.getElementById("result").style.display="block"',
    },
    {
        'slug': 'btu-cooling-calculator',
        'cn_name': 'BTU制冷量计算器',
        'en_name': 'BTU Cooling Calculator',
        'cn_desc': '输入房间面积和类型，计算所需的制冷量(BTU)',
        'en_desc': 'Calculate required BTU cooling capacity based on room area and type',
        'inputs_cn': [('房间面积(m²)', '如: 25'), ('层高(m)', '如: 2.8')],
        'inputs_en': [('Room Area (m²)', 'e.g. 25'), ('Ceiling Height (m)', 'e.g. 2.8')],
        'calc_js': 'var vol=a*b;var btu=vol*40*3.41;var hp=btu/12000;document.getElementById("rv").innerHTML="房间体积: <b>"+vol.toFixed(1)+" m³</b><br>所需BTU: <b>"+Math.round(btu)+"</b><br>≈ <b>"+hp.toFixed(1)+" 匹</b>空调";document.getElementById("result").style.display="block"',
    },
    {
        'slug': 'temperature-converter-calculator',
        'cn_name': '温度换算器',
        'en_name': 'Temperature Converter',
        'cn_desc': '输入摄氏温度，一键换算华氏度和开尔文',
        'en_desc': 'Convert Celsius to Fahrenheit and Kelvin instantly',
        'inputs_cn': [('摄氏温度(°C)', '如: 25')],
        'inputs_en': [('Celsius (°C)', 'e.g. 25')],
        'calc_js': 'var f=a*9/5+32;var k=a+273.15;document.getElementById("rv").innerHTML="℉ 华氏度: <b>"+f.toFixed(1)+"°F</b><br>K 开尔文: <b>"+k.toFixed(2)+"K</b>";document.getElementById("result").style.display="block"',
    },
    {
        'slug': 'km-to-miles-converter',
        'cn_name': '公里英里换算器',
        'en_name': 'Kilometers to Miles Converter',
        'cn_desc': '输入公里数，一键换算成英里、米和英尺',
        'en_desc': 'Convert kilometers to miles, meters and feet instantly',
        'inputs_cn': [('公里(km)', '如: 10')],
        'inputs_en': [('Kilometers (km)', 'e.g. 10')],
        'calc_js': 'var miles=a*0.621371;var meters=a*1000;var feet=a*3280.84;document.getElementById("rv").innerHTML="英里: <b>"+miles.toFixed(2)+" mi</b><br>米: <b>"+meters.toFixed(0)+" m</b><br>英尺: <b>"+feet.toFixed(0)+" ft</b>";document.getElementById("result").style.display="block"',
    },
    {
        'slug': 'inch-to-cm-converter',
        'cn_name': '英寸厘米换算器',
        'en_name': 'Inches to CM Converter',
        'cn_desc': '输入英寸数，一键换算成厘米、毫米和米',
        'en_desc': 'Convert inches to centimeters, millimeters and meters instantly',
        'inputs_cn': [('英寸(in)', '如: 12')],
        'inputs_en': [('Inches (in)', 'e.g. 12')],
        'calc_js': 'var cm=a*2.54;var mm=a*25.4;var m=a*0.0254;document.getElementById("rv").innerHTML="厘米: <b>"+cm.toFixed(2)+" cm</b><br>毫米: <b>"+mm.toFixed(1)+" mm</b><br>米: <b>"+m.toFixed(4)+" m</b>";document.getElementById("result").style.display="block"',
    },
]

for t in TOOLS:
    gen_tool(**t)

print(f'\n生成了 {len(TOOLS)} 个工具')
