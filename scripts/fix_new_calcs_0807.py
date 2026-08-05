#!/usr/bin/env python3
"""Fix 8 new calculator tools: resultEl undefined, v1/v2 misuse, EN Chinese output, placeholder text."""
import re, os

TOOLS = {
    'bird-age-calculator': {
        'cn_js': '''function calc(){
  var a=parseFloat(document.getElementById('v1').value);
  var v3el=document.getElementById('v3');
  var c=v3el?parseFloat(v3el.value):0;
  if(isNaN(a)){show('请输入有效数值');return}
  var resultEl=document.getElementById('result');
  var species=document.getElementById('v2').value;
  var ratio;
  if(species==='parrot'||species==='macaw'||species==='cockatoo'){ratio=6.5}
  else if(species==='canary'||species==='finch'){ratio=8}
  else if(species==='pigeon'||species==='dove'){ratio=5}
  else if(species==='budgie'||species==='cockatiel'){ratio=7}
  else{ratio=6}
  var humanAge=Math.round(a*ratio);
  resultEl.innerHTML='<div style="text-align:center;"><p>相当于人类年龄: <strong>'+humanAge+' 岁</strong></p><p style="color:#94a3b8;font-size:0.85rem;">换算比: 1鸟年 = '+ratio+'人类年</p></div>';
  resultEl.style.display='block';
}''',
        'en_js': '''function calc(){
  var a=parseFloat(document.getElementById('v1').value);
  var v3el=document.getElementById('v3');
  var c=v3el?parseFloat(v3el.value):0;
  if(isNaN(a)){show('Please enter valid numbers');return}
  var resultEl=document.getElementById('result');
  var species=document.getElementById('v2').value;
  var ratio;
  if(species==='parrot'||species==='macaw'||species==='cockatoo'){ratio=6.5}
  else if(species==='canary'||species==='finch'){ratio=8}
  else if(species==='pigeon'||species==='dove'){ratio=5}
  else if(species==='budgie'||species==='cockatiel'){ratio=7}
  else{ratio=6}
  var humanAge=Math.round(a*ratio);
  resultEl.innerHTML='<div style="text-align:center;"><p>Human equivalent age: <strong>'+humanAge+' years old</strong></p><p style="color:#94a3b8;font-size:0.85rem;">Ratio: 1 bird year = '+ratio+' human years</p></div>';
  resultEl.style.display='block';
}''',
        'cn_input_fix': True,  # species needs select instead of number input
    },
    'brew-ratio-calculator': {
        'cn_js': '''function calc(){
  var a=parseFloat(document.getElementById('v1').value);
  var b=parseFloat(document.getElementById('v2').value);
  if(isNaN(a)||isNaN(b)){show('请输入有效数值');return}
  var resultEl=document.getElementById('result');
  var ratio=b/a;
  var style='';
  if(ratio<15)style='偏浓，适合意式/摩卡壶';
  else if(ratio<17)style='标准，适合手冲/美式';
  else if(ratio<19)style='偏淡，适合法压/冷萃';
  else style='很淡，适合大杯冰美式';
  resultEl.innerHTML='<div style="text-align:center;"><p>粉水比: <strong>1:'+ratio.toFixed(1)+'</strong></p><p>口感: <strong>'+style+'</strong></p><p style="color:#94a3b8;font-size:0.85rem;">黄金杯标准: 1:15 ~ 1:18</p></div>';
  resultEl.style.display='block';
}''',
        'en_js': '''function calc(){
  var a=parseFloat(document.getElementById('v1').value);
  var b=parseFloat(document.getElementById('v2').value);
  if(isNaN(a)||isNaN(b)){show('Please enter valid numbers');return}
  var resultEl=document.getElementById('result');
  var ratio=b/a;
  var style='';
  if(ratio<15)style='Strong, for espresso/moka pot';
  else if(ratio<17)style='Standard, for pour-over/Americano';
  else if(ratio<19)style='Mild, for French press/cold brew';
  else style='Very mild, for large iced Americano';
  resultEl.innerHTML='<div style="text-align:center;"><p>Brew Ratio: <strong>1:'+ratio.toFixed(1)+'</strong></p><p>Taste: <strong>'+style+'</strong></p><p style="color:#94a3b8;font-size:0.85rem;">Golden cup standard: 1:15 ~ 1:18</p></div>';
  resultEl.style.display='block';
}''',
    },
    'decking-calculator': {
        'cn_js': '''function calc(){
  var a=parseFloat(document.getElementById('v1').value);
  var b=parseFloat(document.getElementById('v2').value);
  if(isNaN(a)||isNaN(b)){show('请输入有效数值');return}
  var resultEl=document.getElementById('result');
  var needed=Math.ceil(a/b);
  var withWaste=Math.ceil(needed*1.1);
  resultEl.innerHTML='<div style="text-align:center;"><p>精确需要: <strong>'+needed+' 块</strong></p><p>含10%损耗: <strong>'+withWaste+' 块</strong></p><p style="color:#94a3b8;font-size:0.85rem;">建议按含损耗数量采购</p></div>';
  resultEl.style.display='block';
}''',
        'en_js': '''function calc(){
  var a=parseFloat(document.getElementById('v1').value);
  var b=parseFloat(document.getElementById('v2').value);
  if(isNaN(a)||isNaN(b)){show('Please enter valid numbers');return}
  var resultEl=document.getElementById('result');
  var needed=Math.ceil(a/b);
  var withWaste=Math.ceil(needed*1.1);
  resultEl.innerHTML='<div style="text-align:center;"><p>Exact needed: <strong>'+needed+' boards</strong></p><p>With 10% waste: <strong>'+withWaste+' boards</strong></p><p style="color:#94a3b8;font-size:0.85rem;">Recommended to purchase with waste allowance</p></div>';
  resultEl.style.display='block';
}''',
    },
    'electricity-bill-calculator': {
        'cn_js': '''function calc(){
  var a=parseFloat(document.getElementById('v1').value);
  var b=parseFloat(document.getElementById('v2').value);
  if(isNaN(a)||isNaN(b)){show('请输入有效数值');return}
  var resultEl=document.getElementById('result');
  var dailyCost=a*b;
  var monthlyCost=dailyCost*30;
  var yearlyCost=dailyCost*365;
  resultEl.innerHTML='<div style="text-align:center;"><p>每日电费: <strong>¥'+dailyCost.toFixed(2)+'</strong></p><p>每月电费: <strong>¥'+monthlyCost.toFixed(2)+'</strong></p><p>每年电费: <strong>¥'+yearlyCost.toFixed(2)+'</strong></p></div>';
  resultEl.style.display='block';
}''',
        'en_js': '''function calc(){
  var a=parseFloat(document.getElementById('v1').value);
  var b=parseFloat(document.getElementById('v2').value);
  if(isNaN(a)||isNaN(b)){show('Please enter valid numbers');return}
  var resultEl=document.getElementById('result');
  var dailyCost=a*b;
  var monthlyCost=dailyCost*30;
  var yearlyCost=dailyCost*365;
  resultEl.innerHTML='<div style="text-align:center;"><p>Daily cost: <strong>$'+dailyCost.toFixed(2)+'</strong></p><p>Monthly cost: <strong>$'+monthlyCost.toFixed(2)+'</strong></p><p>Yearly cost: <strong>$'+yearlyCost.toFixed(2)+'</strong></p></div>';
  resultEl.style.display='block';
}''',
    },
    'employee-cost-calculator': {
        'cn_js': '''function calc(){
  var a=parseFloat(document.getElementById('v1').value);
  var b=parseFloat(document.getElementById('v2').value);
  if(isNaN(a)||isNaN(b)){show('请输入有效数值');return}
  var resultEl=document.getElementById('result');
  var annualSalary=a*12;
  var annualBenefits=annualSalary*b/100;
  var total=annualSalary+annualBenefits;
  resultEl.innerHTML='<div style="text-align:center;"><p>年薪: <strong>¥'+annualSalary.toLocaleString()+'</strong></p><p>福利/社保: <strong>¥'+annualBenefits.toLocaleString()+'</strong></p><p style="font-size:1.2rem;">年度总成本: <strong>¥'+total.toLocaleString()+'</strong></p></div>';
  resultEl.style.display='block';
}''',
        'en_js': '''function calc(){
  var a=parseFloat(document.getElementById('v1').value);
  var b=parseFloat(document.getElementById('v2').value);
  if(isNaN(a)||isNaN(b)){show('Please enter valid numbers');return}
  var resultEl=document.getElementById('result');
  var annualSalary=a*12;
  var annualBenefits=annualSalary*b/100;
  var total=annualSalary+annualBenefits;
  resultEl.innerHTML='<div style="text-align:center;"><p>Annual salary: <strong>$'+annualSalary.toLocaleString()+'</strong></p><p>Benefits/insurance: <strong>$'+annualBenefits.toLocaleString()+'</strong></p><p style="font-size:1.2rem;">Total annual cost: <strong>$'+total.toLocaleString()+'</strong></p></div>';
  resultEl.style.display='block';
}''',
    },
    'fish-tank-volume-calculator': {
        'cn_js': '''function calc(){
  var a=parseFloat(document.getElementById('v1').value);
  var b=parseFloat(document.getElementById('v2').value);
  var v3el=document.getElementById('v3');
  var c=v3el?parseFloat(v3el.value):0;
  if(isNaN(a)||isNaN(b)||(v3el&&isNaN(c))){show('请输入有效数值');return}
  var resultEl=document.getElementById('result');
  var volCm3=a*b*c;
  var volL=volCm3/1000;
  var volGal=volL*0.2642;
  var volUkGal=volL*0.22;
  resultEl.innerHTML='<div style="text-align:center;"><p>容积: <strong>'+volL.toFixed(1)+' 升</strong></p><p>= <strong>'+volGal.toFixed(1)+' 美制加仑</strong></p><p>= <strong>'+volUkGal.toFixed(1)+' 英制加仑</strong></p><p style="color:#94a3b8;font-size:0.85rem;">建议养鱼: 1cm鱼/升水</p></div>';
  resultEl.style.display='block';
}''',
        'en_js': '''function calc(){
  var a=parseFloat(document.getElementById('v1').value);
  var b=parseFloat(document.getElementById('v2').value);
  var v3el=document.getElementById('v3');
  var c=v3el?parseFloat(v3el.value):0;
  if(isNaN(a)||isNaN(b)||(v3el&&isNaN(c))){show('Please enter valid numbers');return}
  var resultEl=document.getElementById('result');
  var volCm3=a*b*c;
  var volL=volCm3/1000;
  var volGal=volL*0.2642;
  var volUkGal=volL*0.22;
  resultEl.innerHTML='<div style="text-align:center;"><p>Volume: <strong>'+volL.toFixed(1)+' liters</strong></p><p>= <strong>'+volGal.toFixed(1)+' US gallons</strong></p><p>= <strong>'+volUkGal.toFixed(1)+' UK gallons</strong></p><p style="color:#94a3b8;font-size:0.85rem;">Recommended: 1cm fish per liter of water</p></div>';
  resultEl.style.display='block';
}''',
    },
    'golf-handicap-calculator': {
        'cn_js': '''function calc(){
  var a=parseFloat(document.getElementById('v1').value);
  var b=parseFloat(document.getElementById('v2').value);
  var v3el=document.getElementById('v3');
  var c=v3el?parseFloat(v3el.value):0;
  if(isNaN(a)||isNaN(b)||(v3el&&isNaN(c))){show('请输入有效数值');return}
  var resultEl=document.getElementById('result');
  var rating=b||72;
  var slope=c||113;
  var diff=(a-rating)*113/slope;
  var handicap=diff*0.96;
  resultEl.innerHTML='<div style="text-align:center;"><p>差值与标准杆: <strong>'+(diff>=0?'+':'')+diff.toFixed(1)+'</strong></p><p>差点指数: <strong>'+handicap.toFixed(1)+'</strong></p><p style="color:#94a3b8;font-size:0.85rem;">公式: (杆数-难度)×113÷坡度×0.96</p></div>';
  resultEl.style.display='block';
}''',
        'en_js': '''function calc(){
  var a=parseFloat(document.getElementById('v1').value);
  var b=parseFloat(document.getElementById('v2').value);
  var v3el=document.getElementById('v3');
  var c=v3el?parseFloat(v3el.value):0;
  if(isNaN(a)||isNaN(b)||(v3el&&isNaN(c))){show('Please enter valid numbers');return}
  var resultEl=document.getElementById('result');
  var rating=b||72;
  var slope=c||113;
  var diff=(a-rating)*113/slope;
  var handicap=diff*0.96;
  resultEl.innerHTML='<div style="text-align:center;"><p>Differential: <strong>'+(diff>=0?'+':'')+diff.toFixed(1)+'</strong></p><p>Handicap index: <strong>'+handicap.toFixed(1)+'</strong></p><p style="color:#94a3b8;font-size:0.85rem;">Formula: (score-rating)×113÷slope×0.96</p></div>';
  resultEl.style.display='block';
}''',
    },
    'swim-pace-calculator': {
        'cn_js': '''function calc(){
  var a=parseFloat(document.getElementById('v1').value);
  var b=parseFloat(document.getElementById('v2').value);
  if(isNaN(a)||isNaN(b)){show('请输入有效数值');return}
  var resultEl=document.getElementById('result');
  var pacePer100m=(b*60)/(a/100);
  var paceMin=Math.floor(pacePer100m/60);
  var paceSec=Math.round(pacePer100m%60);
  var speed=a/1000/(b/60);
  resultEl.innerHTML='<div style="text-align:center;"><p>每100米配速: <strong>'+paceMin+'\\''+String(paceSec).padStart(2,'0')+\\"</strong></p><p>速度: <strong>'+speed.toFixed(2)+' km/h</strong></p><p>总距离: <strong>'+(a/1000).toFixed(2)+' km</strong></p></div>';
  resultEl.style.display='block';
}''',
        'en_js': '''function calc(){
  var a=parseFloat(document.getElementById('v1').value);
  var b=parseFloat(document.getElementById('v2').value);
  if(isNaN(a)||isNaN(b)){show('Please enter valid numbers');return}
  var resultEl=document.getElementById('result');
  var pacePer100m=(b*60)/(a/100);
  var paceMin=Math.floor(pacePer100m/60);
  var paceSec=Math.round(pacePer100m%60);
  var speed=a/1000/(b/60);
  resultEl.innerHTML='<div style="text-align:center;"><p>Pace per 100m: <strong>'+paceMin+'\\''+String(paceSec).padStart(2,'0')+\\"</strong></p><p>Speed: <strong>'+speed.toFixed(2)+' km/h</strong></p><p>Total distance: <strong>'+(a/1000).toFixed(2)+' km</strong></p></div>';
  resultEl.style.display='block';
}''',
    },
}

# "如何使用" steps for each tool (CN)
HOWTO_CN = {
    'bird-age-calculator': '<li>输入鸟的实际年龄（年）</li>\n  <li>选择鸟类品种（鹦鹉/金丝雀/鸽子等）</li>\n  <li>点击"计算"按钮查看人类等效年龄</li>',
    'brew-ratio-calculator': '<li>输入咖啡豆重量（克）</li>\n  <li>输入水量（毫升）</li>\n  <li>点击"计算"按钮查看粉水比和口感建议</li>',
    'decking-calculator': '<li>输入露台总面积（平方米）</li>\n  <li>输入单块地板面积（平方米）</li>\n  <li>点击"计算"按钮查看所需地板数量</li>',
    'electricity-bill-calculator': '<li>输入每日用电量（kWh）</li>\n  <li>输入电价（元/kWh）</li>\n  <li>点击"计算"按钮查看日/月/年电费</li>',
    'employee-cost-calculator': '<li>输入员工月薪（元）</li>\n  <li>输入社保福利比例（%）</li>\n  <li>点击"计算"按钮查看年度总人力成本</li>',
    'fish-tank-volume-calculator': '<li>输入鱼缸长度（厘米）</li>\n  <li>输入鱼缸宽度和高度（厘米）</li>\n  <li>点击"计算"按钮查看水体体积</li>',
    'golf-handicap-calculator': '<li>输入平均杆数</li>\n  <li>输入球场难度Rating和坡度Slope</li>\n  <li>点击"计算"按钮查看差点指数</li>',
    'swim-pace-calculator': '<li>输入游泳距离（米）</li>\n  <li>输入完成时间（分钟）</li>\n  <li>点击"计算"按钮查看配速和速度</li>',
}

# "How to use" steps for each tool (EN)
HOWTO_EN = {
    'bird-age-calculator': '<li>Enter the bird\'s actual age (years)</li>\n  <li>Select the bird species (parrot/canary/pigeon etc.)</li>\n  <li>Click "Calculate" to see the human equivalent age</li>',
    'brew-ratio-calculator': '<li>Enter coffee grounds weight (grams)</li>\n  <li>Enter water amount (ml)</li>\n  <li>Click "Calculate" to see brew ratio and taste</li>',
    'decking-calculator': '<li>Enter total deck area (m²)</li>\n  <li>Enter single board area (m²)</li>\n  <li>Click "Calculate" to see required board count</li>',
    'electricity-bill-calculator': '<li>Enter daily electricity usage (kWh)</li>\n  <li>Enter electricity rate ($/kWh)</li>\n  <li>Click "Calculate" to see daily/monthly/yearly cost</li>',
    'employee-cost-calculator': '<li>Enter monthly salary ($)</li>\n  <li>Enter benefits/insurance rate (%)</li>\n  <li>Click "Calculate" to see total annual cost</li>',
    'fish-tank-volume-calculator': '<li>Enter tank length (cm)</li>\n  <li>Enter tank width and height (cm)</li>\n  <li>Click "Calculate" to see water volume</li>',
    'golf-handicap-calculator': '<li>Enter average score</li>\n  <li>Enter course Rating and Slope</li>\n  <li>Click "Calculate" to see handicap index</li>',
    'swim-pace-calculator': '<li>Enter swimming distance (meters)</li>\n  <li>Enter completion time (minutes)</li>\n  <li>Click "Calculate" to see pace and speed</li>',
}

# bird-age species select HTML
BIRD_SPECIES_CN = '''<div class="form-group"><label>品种</label><select id="v2"><option value="parrot">鹦鹉</option><option value="canary">金丝雀</option><option value="pigeon">鸽子</option><option value="budgie">虎皮鹦鹉</option><option value="cockatiel">鸡尾鹦鹉</option><option value="macaw">金刚鹦鹉</option><option value="cockatoo">巴丹鹦鹉</option><option value="finch">雀类</option><option value="dove">斑鸠</option><option value="other">其他</option></select></div>'''
BIRD_SPECIES_EN = '''<div class="form-group"><label>Species</label><select id="v2"><option value="parrot">Parrot</option><option value="canary">Canary</option><option value="pigeon">Pigeon</option><option value="budgie">Budgie</option><option value="cockatiel">Cockatiel</option><option value="macaw">Macaw</option><option value="cockatoo">Cockatoo</option><option value="finch">Finch</option><option value="dove">Dove</option><option value="other">Other</option></select></div>'''

PLACEHOLDER_CN_RE = re.compile(r'<li>输入第一个参数</li>\s*<li>输入第二个参数</li>\s*<li>点击"计算"按钮查看结果</li>')
PLACEHOLDER_EN_RE = re.compile(r'<li>Enter the first parameter</li>\s*<li>Enter the second parameter</li>\s*<li>Click "Calculate" to see the result</li>')

def fix_js(content, new_js):
    """Replace the calc() function body with the fixed version."""
    # Match from 'function calc(){' to the closing '}' before 'function show'
    pattern = re.compile(r'function calc\(\)\{.*?\n\}(?=\nfunction show)', re.DOTALL)
    result = pattern.sub(new_js, content, count=1)
    return result

def fix_file(filepath, tool_name, is_en):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    tool = TOOLS[tool_name]
    new_js = tool['en_js'] if is_en else tool['cn_js']
    
    # 1. Fix JS
    content = fix_js(content, new_js)
    
    # 2. Fix "如何使用" placeholder
    if is_en:
        howto = HOWTO_EN[tool_name]
        content = PLACEHOLDER_EN_RE.sub(howto, content)
        # Also try CN placeholder in EN pages (some EN pages have CN placeholder)
        content = PLACEHOLDER_CN_RE.sub(howto, content)
    else:
        howto = HOWTO_CN[tool_name]
        content = PLACEHOLDER_CN_RE.sub(howto, content)
    
    # 3. bird-age: replace number input with select for species
    if tool_name == 'bird-age-calculator':
        species_html = BIRD_SPECIES_EN if is_en else BIRD_SPECIES_CN
        # Match the species form-group (v2 input that's type=number)
        content = re.sub(
            r'<div class="form-group"><label>[^<]*</label><input type="number" id="v2"[^>]*></div>',
            species_html,
            content,
            count=1
        )
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

# Process all 8 tools, CN + EN
fixed = []
for tool_name in TOOLS:
    for prefix, is_en in [('', False), ('en/', True)]:
        filepath = os.path.join(prefix + tool_name, 'index.html')
        if os.path.exists(filepath):
            if fix_file(filepath, tool_name, is_en):
                fixed.append(filepath)
                print(f"  ✅ Fixed: {filepath}")
            else:
                print(f"  ⚠️ No changes: {filepath}")
        else:
            print(f"  ❌ Not found: {filepath}")

print(f"\nTotal fixed: {len(fixed)} files")
