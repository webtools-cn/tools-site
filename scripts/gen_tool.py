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
        'slug': 'weight-loss-calorie-calculator',
        'cn_name': '减重热量缺口计算器',
        'en_name': 'Weight Loss Calorie Calculator',
        'cn_desc': '根据目标减重公斤数和天数计算每日所需热量缺口',
        'en_desc': 'Calculate daily calorie deficit needed based on target weight loss and timeline',
        'inputs_cn': [('目标减重(kg)', '如: 5'), ('计划天数', '如: 30')],
        'inputs_en': [('Target Weight Loss (kg)', 'e.g. 5'), ('Planned Days', 'e.g. 30')],
        'calc_js': 'var total=a*7700;var daily=total/b;document.getElementById("rv").innerHTML="总需消耗: <b>"+total.toFixed(0)+" kcal</b><br>每日缺口: <b>"+daily.toFixed(0)+" kcal/天</b><br>≈ 减少 <b>"+(daily/500).toFixed(1)+" 碗米饭</b>";document.getElementById("result").style.display="block"',
    },
    {
        'slug': 'water-bill-calculator',
        'cn_name': '水费计算器',
        'en_name': 'Water Bill Calculator',
        'cn_desc': '根据用水量、水价和排污费计算月度水费',
        'en_desc': 'Calculate monthly water bill based on usage, unit price and sewage fee',
        'inputs_cn': [('月用水量(吨)', '如: 20'), ('水价(元/吨)', '如: 3.5'), ('排污费(元/吨)', '如: 1.4')],
        'inputs_en': [('Monthly Usage (tons)', 'e.g. 20'), ('Water Rate ($/ton)', 'e.g. 3.5'), ('Sewage Fee ($/ton)', 'e.g. 1.4')],
        'calc_js': 'var wc=a*b;var sc=a*c;var total=wc+sc;document.getElementById("rv").innerHTML="水费: <b>"+wc.toFixed(2)+"</b><br>排污费: <b>"+sc.toFixed(2)+"</b><br>合计: <b>"+total.toFixed(2)+"</b>";document.getElementById("result").style.display="block"',
    },
    {
        'slug': 'gas-bill-calculator',
        'cn_name': '燃气费计算器',
        'en_name': 'Gas Bill Calculator',
        'cn_desc': '根据用气量和阶梯气价计算月度燃气费用',
        'en_desc': 'Calculate monthly gas bill based on usage and tiered pricing',
        'inputs_cn': [('月用气量(m³)', '如: 30'), ('气价(元/m³)', '如: 2.8')],
        'inputs_en': [('Monthly Usage (m³)', 'e.g. 30'), ('Gas Rate ($/m³)', 'e.g. 2.8')],
        'calc_js': 'var total=a*b;document.getElementById("rv").innerHTML="月燃气费: <b>"+total.toFixed(2)+"</b><br>年预估: <b>"+(total*12).toFixed(2)+"</b>";document.getElementById("result").style.display="block"',
    },
    {
        'slug': 'monthly-salary-calculator',
        'cn_name': '月薪计算器',
        'en_name': 'Monthly Salary Calculator',
        'cn_desc': '输入税前年收入计算扣除五险一金后的月薪',
        'en_desc': 'Calculate monthly take-home pay from annual gross salary after deductions',
        'inputs_cn': [('税前年收入(元)', '如: 200000'), ('社保公积金比例(%)', '如: 22')],
        'inputs_en': [('Annual Gross Salary ($)', 'e.g. 50000'), ('Deduction Rate (%)', 'e.g. 22')],
        'calc_js': 'var monthly=a/12;var deduct=monthly*b/100;var net=monthly-deduct;document.getElementById("rv").innerHTML="税前月薪: <b>"+monthly.toFixed(2)+"</b><br>月扣除: <b>"+deduct.toFixed(2)+"</b><br>税后月薪: <b>"+net.toFixed(2)+"</b>";document.getElementById("result").style.display="block"',
    },
    {
        'slug': 'packaging-cost-calculator',
        'cn_name': '包装成本计算器',
        'en_name': 'Packaging Cost Calculator',
        'cn_desc': '根据包装材料单价和数量计算产品包装的单个成本',
        'en_desc': 'Calculate per-unit packaging cost from material price and quantity',
        'inputs_cn': [('包装材料总价(元)', '如: 5000'), ('产品数量(个)', '如: 1000')],
        'inputs_en': [('Total Material Cost ($)', 'e.g. 5000'), ('Product Quantity', 'e.g. 1000')],
        'calc_js': 'var per=a/b;document.getElementById("rv").innerHTML="单个包装成本: <b>"+per.toFixed(2)+"</b><br>每100个成本: <b>"+(per*100).toFixed(2)+"</b>";document.getElementById("result").style.display="block"',
    },
]

for t in TOOLS:
    gen_tool(**t)

print(f'\n生成了 {len(TOOLS)} 个工具')
