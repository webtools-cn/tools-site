#!/usr/bin/env python3
"""快速生成计算器工具 — 输入规格 → 自动输出 CN+EN 两个 HTML"""
import json, os, sys

def gen_tool(slug, cn_name, en_name, cn_desc, en_desc, inputs_cn, inputs_en, calc_js):
    """生成一个计算器工具
    
    inputs_cn: [(label, placeholder), ...]
    inputs_en: [(label, placeholder), ...]
    calc_js: JS计算逻辑 (使用变量 a,b,c,... 对应v1,v2,v3,...)
    """
    # 重复检查：如果CN文件已存在，跳过
    if os.path.exists(f'{slug}/index.html'):
        print(f'⏭️ 跳过已存在: {slug}')
        return
    
    os.makedirs(slug, exist_ok=True)
    os.makedirs(f'en/{slug}', exist_ok=True)
    
    # 生成input HTML - 支持select类型: tuple可带第三个元素 'select:选项1,选项2,...'
    cn_inputs = ''
    en_inputs = ''
    for i, (cn_tuple, en_tuple) in enumerate(zip(inputs_cn, inputs_en)):
        vid = f'v{i+1}'
        cn_extra = cn_tuple[2] if len(cn_tuple) > 2 else ''
        en_extra = en_tuple[2] if len(en_tuple) > 2 else ''
        
        if cn_extra.startswith('select:'):
            opts = cn_extra[7:].split(',')
            cn_inputs += f'<div class="form-group"><label>{cn_tuple[0]}</label><select id="{vid}">'
            for o in opts:
                cn_inputs += f'<option value="{o.strip()}">{o.strip()}</option>'
            cn_inputs += '</select></div>\n'
        else:
            cn_inputs += f'<div class="form-group"><label>{cn_tuple[0]}</label><input type="number" id="{vid}" placeholder="{cn_tuple[1]}" step="any"></div>\n'
        
        if en_extra.startswith('select:'):
            opts = en_extra[7:].split(',')
            en_inputs += f'<div class="form-group"><label>{en_tuple[0]}</label><select id="{vid}">'
            for o in opts:
                en_inputs += f'<option value="{o.strip()}">{o.strip()}</option>'
            en_inputs += '</select></div>\n'
        else:
            en_inputs += f'<div class="form-group"><label>{en_tuple[0]}</label><input type="number" id="{vid}" placeholder="{en_tuple[1]}" step="any"></div>\n'
    
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
    cn_html = cn_html.replace('<!-- PERCENTAGE_LOGIC -->', 'var v1=a,v2=b,v3=c,v4=d;' + calc_js)
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
    en_html = en_html.replace('TOOL_NAME_CN', en_name)
    en_html = en_html.replace('TOOL_DESC_CN_SEO', en_desc[:160])
    en_html = en_html.replace('TOOL_DESC_CN_SHORT', en_desc[:80])
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
    en_html = en_html.replace('<!-- PERCENTAGE_LOGIC -->', 'var v1=a,v2=b,v3=c,v4=d;' + calc_js)
    en_html = en_html.replace('TOOL_SEO_INTRO_CN', f'{en_name} is a free online tool. {en_desc} Works on mobile and desktop, all calculations run locally in your browser for privacy.')
    en_html = en_html.replace('TOOL_STEP1_CN', 'Enter the first parameter')
    en_html = en_html.replace('TOOL_STEP2_CN', 'Enter the second parameter')
    en_html = en_html.replace('TOOL_STEP3_CN', 'Click "Calculate" to see the result')
    en_html = en_html.replace('FAQ_PLACEHOLDER_CN', '<h3>Is this tool accurate?</h3><p>Calculations use standard formulas for reliable results.</p><h3>Do I need to download anything?</h3><p>No, it runs entirely in your browser. No downloads needed.</p>')
    en_html = en_html.replace('FAQ_CN_JSON', '[{"@type":"Question","name":"Is this tool accurate?","acceptedAnswer":{"@type":"Answer","text":"Calculations use standard formulas for reliable results."}},{"@type":"Question","name":"Do I need to download anything?","acceptedAnswer":{"@type":"Answer","text":"No, it runs entirely in your browser. No downloads needed."}}]')
    en_html = en_html.replace('关于 ', 'About ')
    en_html = en_html.replace('如何使用', 'How to Use')
    
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
# 在此添加新工具配置，格式见 gen_tool() 参数
TOOLS = [
]

for t in TOOLS:
    gen_tool(**t)

print(f'\n生成了 {len(TOOLS)} 个工具')
