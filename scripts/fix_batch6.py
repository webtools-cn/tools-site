#!/usr/bin/env python3
"""Fix batch 6: 5 new tools (cylinder-volume/date-duration/morse-translator/ohms-law/resistor-color-decoder)"""
import re, os

TOOLS = {
    'cylinder-volume-calc': {
        'cn_steps': '<li>在"底面半径"输入框中输入圆柱底面的半径值</li>\n  <li>在"高度"输入框中输入圆柱的高度值</li>\n  <li>点击"计算"按钮，即可获得圆柱体积',
        'en_steps': '<li>Enter the base radius of the cylinder in the "Radius" field</li>\n  <li>Enter the height of the cylinder in the "Height" field</li>\n  <li>Click "Calculate" to get the cylinder volume',
        'en_calc_fixes': [
            ("v.toFixed(2)+' 立方单位'", "v.toFixed(2)+' cubic units'"),
            ("'底面积: '+(Math.PI*a*a).toFixed(2)+' 平方单位'", "'Base area: '+(Math.PI*a*a).toFixed(2)+' sq units'"),
        ],
        'en_show_fixes': [
            ("show('电阻不能为0')", "show('Resistance cannot be 0')"),
        ],
    },
    'date-duration-calc': {
        'cn_steps': '<li>在"开始日期"输入框中输入起始日期（格式：YYYY-MM-DD）</li>\n  <li>在"结束日期"输入框中输入截止日期（格式：YYYY-MM-DD）</li>\n  <li>点击"计算"按钮，即可获得两个日期之间的天数、周数和月数',
        'en_steps': '<li>Enter the start date in the "Start Date" field (format: YYYY-MM-DD)</li>\n  <li>Enter the end date in the "End Date" field (format: YYYY-MM-DD)</li>\n  <li>Click "Calculate" to get the duration in days, weeks, and months',
        'en_calc_fixes': [
            ("show('请输入有效日期(YYYY-MM-DD)')", "show('Please enter valid dates (YYYY-MM-DD)')"),
            ("days+' 天'", "days+' days'"),
            ("'约 '+weeks+' 周 / '+months+' 月'", "'≈ '+weeks+' weeks / '+months+' months'"),
        ],
    },
    'morse-translator': {
        'cn_steps': '<li>在"输入文本"框中输入要转换的内容</li>\n  <li>在"模式"框中输入 text2morse（文字转摩斯）或 morse2text（摩斯转文字）</li>\n  <li>点击"计算"按钮，即可获得转换结果',
        'en_steps': '<li>Enter the text or Morse code in the "Input" field</li>\n  <li>Enter "text2morse" or "morse2text" in the "Mode" field</li>\n  <li>Click "Calculate" to get the converted result',
        'en_calc_fixes': [
            ("show('请输入内容')", "show('Please enter input text')"),
            ("'解密完成'", "'Decryption complete'"),
            ("'编码完成'", "'Encoding complete'"),
        ],
    },
    'ohms-law-calc': {
        'cn_steps': '<li>在"电压(V)"输入框中输入电压值</li>\n  <li>在"电阻(Ω)"输入框中输入电阻值</li>\n  <li>点击"计算"按钮，即可获得电流和功率',
        'en_steps': '<li>Enter the voltage value in the "Voltage (V)" field</li>\n  <li>Enter the resistance value in the "Resistance (Ω)" field</li>\n  <li>Click "Calculate" to get the current and power',
        'en_calc_fixes': [
            ("show('电阻不能为0')", "show('Resistance cannot be 0')"),
            ("'功率: '+p.toFixed(2)+' W'", "'Power: '+p.toFixed(2)+' W'"),
        ],
    },
    'resistor-color-decoder': {
        'cn_steps': '<li>在"色环1"框中输入第一个色环颜色（如：红）</li>\n  <li>在"色环2"框中输入第二个色环颜色（如：黑）</li>\n  <li>在"乘数"框中输入乘数色环颜色，点击"计算"按钮获得电阻值',
        'en_steps': '<li>Enter the first band color in "Band 1" (e.g., red)</li>\n  <li>Enter the second band color in "Band 2" (e.g., black)</li>\n  <li>Enter the multiplier color in "Multiplier" and click "Calculate"',
        'en_calc_fixes': [
            ("show('输入颜色名称: 黑棕红橙黄绿蓝紫灰白(或英文)')", "show('Enter color name: black/brown/red/orange/yellow/green/blue/violet/grey/white')"),
            ("'原始值: '+(v1*10+v2)*Math.pow(10,vm)+' Ω'", "'Raw value: '+(v1*10+v2)*Math.pow(10,vm)+' Ω'"),
        ],
    },
}

# Common EN footer/copyright fixes
EN_FOOTER_OLD = """    <a href="mailto:dexshuang@google.com">联系我们</a>
    <a href="../privacy/">隐私政策</a>
    <a href="../terms/">服务条款</a>
    <a href="../about/">关于我们</a>"""
EN_FOOTER_NEW = """    <a href="mailto:dexshuang@google.com">Contact Us</a>
    <a href="../privacy/">Privacy Policy</a>
    <a href="../terms/">Terms of Service</a>
    <a href="../about/">About Us</a>"""

EN_COPYRIGHT_OLD = "，数据不上传服务器"
EN_COPYRIGHT_NEW = ", data never leaves your device"

# Common placeholder steps
CN_STEPS_OLD = """<li>输入第一个参数</li>
  <li>输入第二个参数</li>
  <li>点击"计算"按钮查看结果</li>"""
EN_STEPS_OLD = """<li>Enter the first parameter</li>
  <li>Enter the second parameter</li>
  <li>Click "Calculate" to see the result</li>"""

os.chdir('/home/chison/tools-site')

for tool, fixes in TOOLS.items():
    # === Fix CN ===
    cn_path = f'{tool}/index.html'
    with open(cn_path, 'r') as f:
        cn = f.read()
    
    # Fix placeholder steps
    cn_new_steps = f'<li>{fixes["cn_steps"]}</li>' if False else fixes['cn_steps']
    # The steps are inside <ol>...</ol>, need to replace the 3 <li> lines
    cn = cn.replace(CN_STEPS_OLD, fixes['cn_steps'] + '</li>')
    # Actually let's be more careful - replace the whole 3-line block
    cn_old_steps_block = '<li>输入第一个参数</li>\n  <li>输入第二个参数</li>\n  <li>点击"计算"按钮查看结果</li>'
    cn_new_steps_block = fixes['cn_steps']
    cn = cn.replace(cn_old_steps_block, cn_new_steps_block)
    
    with open(cn_path, 'w') as f:
        f.write(cn)
    print(f"✅ CN {tool}: steps fixed")
    
    # === Fix EN ===
    en_path = f'en/{tool}/index.html'
    with open(en_path, 'r') as f:
        en = f.read()
    
    # Fix footer
    en = en.replace(EN_FOOTER_OLD, EN_FOOTER_NEW)
    
    # Fix copyright
    en = en.replace(EN_COPYRIGHT_OLD, EN_COPYRIGHT_NEW)
    
    # Fix placeholder steps
    en_old_steps_block = '<li>Enter the first parameter</li>\n  <li>Enter the second parameter</li>\n  <li>Click "Calculate" to see the result</li>'
    en = en.replace(en_old_steps_block, fixes['en_steps'])
    
    # Fix lang-switch link (should point to CN version, not EN)
    en = en.replace(f'href="/en/{tool}/">English', f'href="/{tool}/">中文')
    
    # Fix hreflang (zh should point to CN URL)
    en = en.replace(
        f'<link rel="alternate" hreflang="zh" href="https://free-toolbase.com/en/{tool}/">',
        f'<link rel="alternate" hreflang="zh" href="https://free-toolbase.com/{tool}/">'
    )
    
    # Fix calc() Chinese output
    for old, new in fixes.get('en_calc_fixes', []):
        en = en.replace(old, new)
    
    with open(en_path, 'w') as f:
        f.write(en)
    print(f"✅ EN {tool}: footer+copyright+steps+lang-switch+hreflang+calc fixed")

print("\n✅ All 10 files fixed!")
