#!/usr/bin/env python3
"""Fix calc() function for 8 new calculator tools (CN + EN = 16 files)
Fixes:
1. SELECT elements: use el.value (string) instead of parseFloat
2. text inputs (time-duration): use el.value (string) instead of parseFloat
3. Add DOM update at end: rv.textContent=r + result.style.display='block'
4. EN pages: translate Chinese output text to English
"""
import re, os

TOOLS = {
    'time-duration-calc': {
        'cn_calc': '''function calc(){
  var v1el=document.getElementById('v1'),a=v1el.value;
  var v2el=document.getElementById('v2'),b=v2el?v2el.value:'';
  if(!a||!b){show('请输入有效时间');return}
  var s=a.split(':');var e=b.split(':');
  if(s.length<2||e.length<2){show('请输入HH:MM格式');return}
  var sm=parseInt(s[0])*60+parseInt(s[1]);var em=parseInt(e[0])*60+parseInt(e[1]);
  if(em<sm)em+=1440;
  var diff=em-sm;var h=Math.floor(diff/60);var m=diff%60;
  var r=h+'小时'+m+'分钟';
  document.getElementById('rv').textContent=r;
  document.getElementById('result').style.display='block';
}''',
        'en_calc': '''function calc(){
  var v1el=document.getElementById('v1'),a=v1el.value;
  var v2el=document.getElementById('v2'),b=v2el?v2el.value:'';
  if(!a||!b){show('Please enter valid time');return}
  var s=a.split(':');var e=b.split(':');
  if(s.length<2||e.length<2){show('Please use HH:MM format');return}
  var sm=parseInt(s[0])*60+parseInt(s[1]);var em=parseInt(e[0])*60+parseInt(e[1]);
  if(em<sm)em+=1440;
  var diff=em-sm;var h=Math.floor(diff/60);var m=diff%60;
  var r=h+' hours '+m+' minutes';
  document.getElementById('rv').textContent=r;
  document.getElementById('result').style.display='block';
}''',
    },
    'oz-to-ml-calc': {
        'cn_calc': '''function calc(){
  var v1el=document.getElementById('v1'),a=parseFloat(v1el.value)||0;
  var v2el=document.getElementById('v2'),b=v2el?v2el.value:'';
  if(isNaN(a)||!v1el.value){show('请输入有效数值');return}
  var result=b=='盎司→毫升'||b=='oz → ml'?a*29.5735:a/29.5735;
  var unit=b=='盎司→毫升'||b=='oz → ml'?'毫升':'盎司';
  var r=parseFloat(result.toFixed(2))+' '+unit;
  document.getElementById('rv').textContent=r;
  document.getElementById('result').style.display='block';
}''',
        'en_calc': '''function calc(){
  var v1el=document.getElementById('v1'),a=parseFloat(v1el.value)||0;
  var v2el=document.getElementById('v2'),b=v2el?v2el.value:'';
  if(isNaN(a)||!v1el.value){show('Please enter a valid number');return}
  var result=b=='盎司→毫升'||b=='oz → ml'?a*29.5735:a/29.5735;
  var unit=b=='盎司→毫升'||b=='oz → ml'?'ml':'oz';
  var r=parseFloat(result.toFixed(2))+' '+unit;
  document.getElementById('rv').textContent=r;
  document.getElementById('result').style.display='block';
}''',
    },
    'lbs-to-kg-calc': {
        'cn_calc': '''function calc(){
  var v1el=document.getElementById('v1'),a=parseFloat(v1el.value)||0;
  var v2el=document.getElementById('v2'),b=v2el?v2el.value:'';
  if(isNaN(a)||!v1el.value){show('请输入有效数值');return}
  var result=b=='磅→千克'||b=='lbs → kg'?a*0.453592:a/0.453592;
  var unit=b=='磅→千克'||b=='lbs → kg'?'千克':'磅';
  var r=parseFloat(result.toFixed(2))+' '+unit;
  document.getElementById('rv').textContent=r;
  document.getElementById('result').style.display='block';
}''',
        'en_calc': '''function calc(){
  var v1el=document.getElementById('v1'),a=parseFloat(v1el.value)||0;
  var v2el=document.getElementById('v2'),b=v2el?v2el.value:'';
  if(isNaN(a)||!v1el.value){show('Please enter a valid number');return}
  var result=b=='磅→千克'||b=='lbs → kg'?a*0.453592:a/0.453592;
  var unit=b=='磅→千克'||b=='lbs → kg'?'kg':'lbs';
  var r=parseFloat(result.toFixed(2))+' '+unit;
  document.getElementById('rv').textContent=r;
  document.getElementById('result').style.display='block';
}''',
    },
    'celsius-to-fahrenheit': {
        'cn_calc': '''function calc(){
  var v1el=document.getElementById('v1'),a=parseFloat(v1el.value)||0;
  var v2el=document.getElementById('v2'),b=v2el?v2el.value:'';
  if(isNaN(a)||!v1el.value){show('请输入有效数值');return}
  var result=b=='摄氏→华氏'||b=='°C → °F'?a*9/5+32:(a-32)*5/9;
  var unit=b=='摄氏→华氏'||b=='°C → °F'?'°F':'°C';
  var r=parseFloat(result.toFixed(1))+' '+unit;
  document.getElementById('rv').textContent=r;
  document.getElementById('result').style.display='block';
}''',
        'en_calc': '''function calc(){
  var v1el=document.getElementById('v1'),a=parseFloat(v1el.value)||0;
  var v2el=document.getElementById('v2'),b=v2el?v2el.value:'';
  if(isNaN(a)||!v1el.value){show('Please enter a valid number');return}
  var result=b=='摄氏→华氏'||b=='°C → °F'?a*9/5+32:(a-32)*5/9;
  var unit=b=='摄氏→华氏'||b=='°C → °F'?'°F':'°C';
  var r=parseFloat(result.toFixed(1))+' '+unit;
  document.getElementById('rv').textContent=r;
  document.getElementById('result').style.display='block';
}''',
    },
    'gpa-calculator-4': {
        'cn_calc': '''function calc(){
  var a=parseFloat(document.getElementById('v1').value)||0;
  var b=parseFloat(document.getElementById('v2').value)||0;
  var c=parseFloat(document.getElementById('v3').value)||0;
  var d=parseFloat(document.getElementById('v4').value)||0;
  var e=parseFloat(document.getElementById('v5').value)||0;
  var f=parseFloat(document.getElementById('v6').value)||0;
  if(isNaN(a)||isNaN(b)){show('请输入有效数值');return}
  function toGP(s){if(s>=90)return 4;if(s>=85)return 3.7;if(s>=82)return 3.3;if(s>=78)return 3;if(s>=75)return 2.7;if(s>=72)return 2.3;if(s>=68)return 2;if(s>=64)return 1.5;if(s>=60)return 1;return 0;}
  var totalP=a*toGP(b)+c*toGP(d)+e*toGP(f);
  var totalC=a+c+e;
  var gpa=totalC>0?totalP/totalC:0;
  var r='GPA: '+gpa.toFixed(2)+' (加权平均)';
  document.getElementById('rv').textContent=r;
  document.getElementById('result').style.display='block';
}''',
        'en_calc': '''function calc(){
  var a=parseFloat(document.getElementById('v1').value)||0;
  var b=parseFloat(document.getElementById('v2').value)||0;
  var c=parseFloat(document.getElementById('v3').value)||0;
  var d=parseFloat(document.getElementById('v4').value)||0;
  var e=parseFloat(document.getElementById('v5').value)||0;
  var f=parseFloat(document.getElementById('v6').value)||0;
  if(isNaN(a)||isNaN(b)){show('Please enter valid numbers');return}
  function toGP(s){if(s>=90)return 4;if(s>=85)return 3.7;if(s>=82)return 3.3;if(s>=78)return 3;if(s>=75)return 2.7;if(s>=72)return 2.3;if(s>=68)return 2;if(s>=64)return 1.5;if(s>=60)return 1;return 0;}
  var totalP=a*toGP(b)+c*toGP(d)+e*toGP(f);
  var totalC=a+c+e;
  var gpa=totalC>0?totalP/totalC:0;
  var r='GPA: '+gpa.toFixed(2)+' (weighted average)';
  document.getElementById('rv').textContent=r;
  document.getElementById('result').style.display='block';
}''',
    },
    'acre-to-sqm-calc': {
        'cn_calc': '''function calc(){
  var v1el=document.getElementById('v1'),a=parseFloat(v1el.value)||0;
  var v2el=document.getElementById('v2'),b=v2el?v2el.value:'';
  if(isNaN(a)||!v1el.value){show('请输入有效数值');return}
  var result=b=='英亩→平方米'||b=='acres → m²'?a*4046.86:a/4046.86;
  var unit=b=='英亩→平方米'||b=='acres → m²'?'平方米':'英亩';
  var r=parseFloat(result.toFixed(2))+' '+unit;
  document.getElementById('rv').textContent=r;
  document.getElementById('result').style.display='block';
}''',
        'en_calc': '''function calc(){
  var v1el=document.getElementById('v1'),a=parseFloat(v1el.value)||0;
  var v2el=document.getElementById('v2'),b=v2el?v2el.value:'';
  if(isNaN(a)||!v1el.value){show('Please enter a valid number');return}
  var result=b=='英亩→平方米'||b=='acres → m²'?a*4046.86:a/4046.86;
  var unit=b=='英亩→平方米'||b=='acres → m²'?'m²':'acres';
  var r=parseFloat(result.toFixed(2))+' '+unit;
  document.getElementById('rv').textContent=r;
  document.getElementById('result').style.display='block';
}''',
    },
    'gallon-to-liter-calc': {
        'cn_calc': '''function calc(){
  var v1el=document.getElementById('v1'),a=parseFloat(v1el.value)||0;
  var v2el=document.getElementById('v2'),b=v2el?v2el.value:'';
  if(isNaN(a)||!v1el.value){show('请输入有效数值');return}
  var result=b=='加仑→升'||b=='gal → L'?a*3.78541:a/3.78541;
  var unit=b=='加仑→升'||b=='gal → L'?'升':'加仑';
  var r=parseFloat(result.toFixed(2))+' '+unit;
  document.getElementById('rv').textContent=r;
  document.getElementById('result').style.display='block';
}''',
        'en_calc': '''function calc(){
  var v1el=document.getElementById('v1'),a=parseFloat(v1el.value)||0;
  var v2el=document.getElementById('v2'),b=v2el?v2el.value:'';
  if(isNaN(a)||!v1el.value){show('Please enter a valid number');return}
  var result=b=='加仑→升'||b=='gal → L'?a*3.78541:a/3.78541;
  var unit=b=='加仑→升'||b=='gal → L'?'L':'gal';
  var r=parseFloat(result.toFixed(2))+' '+unit;
  document.getElementById('rv').textContent=r;
  document.getElementById('result').style.display='block';
}''',
    },
    'calorie-burn-calc': {
        'cn_calc': '''function calc(){
  var v1el=document.getElementById('v1'),a=parseFloat(v1el.value)||0;
  var v2el=document.getElementById('v2'),b=v2el?parseFloat(v2el.value)||0:0;
  var v3el=document.getElementById('v3'),c=v3el?v3el.value:'';
  if(isNaN(a)||!v1el.value){show('请输入有效数值');return}
  var mets={'跑步':8,'游泳':7,'骑行':6,'走路':3,'跳绳':10,'Running':8,'Swimming':7,'Cycling':6,'Walking':3,'Jump Rope':10};
  var met=mets[c]||5;
  var cal=met*a*b/60;
  var r='约消耗 '+Math.round(cal)+' 千卡';
  document.getElementById('rv').textContent=r;
  document.getElementById('result').style.display='block';
}''',
        'en_calc': '''function calc(){
  var v1el=document.getElementById('v1'),a=parseFloat(v1el.value)||0;
  var v2el=document.getElementById('v2'),b=v2el?parseFloat(v2el.value)||0:0;
  var v3el=document.getElementById('v3'),c=v3el?v3el.value:'';
  if(isNaN(a)||!v1el.value){show('Please enter a valid number');return}
  var mets={'跑步':8,'游泳':7,'骑行':6,'走路':3,'跳绳':10,'Running':8,'Swimming':7,'Cycling':6,'Walking':3,'Jump Rope':10};
  var met=mets[c]||5;
  var cal=met*a*b/60;
  var r='Approximately '+Math.round(cal)+' kcal burned';
  document.getElementById('rv').textContent=r;
  document.getElementById('result').style.display='block';
}''',
    },
}

# Fix placeholder steps too
PLACEHOLDER_FIXES = {
    'time-duration-calc': {
        'cn': [('输入第一个参数', '输入开始时间，例如 09:00'), ('输入第二个参数', '输入结束时间，例如 17:30')],
        'en': [('Enter the first parameter', 'Enter start time, e.g. 09:00'), ('Enter the second parameter', 'Enter end time, e.g. 17:30')],
    },
    'oz-to-ml-calc': {
        'cn': [('输入第一个参数', '输入盎司数值'), ('输入第二个参数', '选择转换方向')],
        'en': [('Enter the first parameter', 'Enter the value in ounces'), ('Enter the second parameter', 'Select conversion direction')],
    },
    'lbs-to-kg-calc': {
        'cn': [('输入第一个参数', '输入磅数值'), ('输入第二个参数', '选择转换方向')],
        'en': [('Enter the first parameter', 'Enter the value in pounds'), ('Enter the second parameter', 'Select conversion direction')],
    },
    'celsius-to-fahrenheit': {
        'cn': [('输入第一个参数', '输入要转换的温度值'), ('输入第二个参数', '选择转换方向（摄氏→华氏或华氏→摄氏）')],
        'en': [('Enter the first parameter', 'Enter the temperature value to convert'), ('Enter the second parameter', 'Select conversion direction (°C → °F or °F → °C)')],
    },
    'gpa-calculator-4': {
        'cn': [('输入第一个参数', '输入第一门课的学分和成绩'), ('输入第二个参数', '输入第二门课的学分和成绩'), ('输入第三个参数', '点击"计算"按钮查看GPA')],
        'en': [('Enter the first parameter', 'Enter credits and score for course 1'), ('Enter the second parameter', 'Enter credits and score for course 2'), ('Enter the third parameter', 'Click "Calculate" to see your GPA')],
    },
    'acre-to-sqm-calc': {
        'cn': [('输入第一个参数', '输入英亩数值'), ('输入第二个参数', '选择转换方向')],
        'en': [('Enter the first parameter', 'Enter the value in acres'), ('Enter the second parameter', 'Select conversion direction')],
    },
    'gallon-to-liter-calc': {
        'cn': [('输入第一个参数', '输入加仑数值'), ('输入第二个参数', '选择转换方向')],
        'en': [('Enter the first parameter', 'Enter the value in gallons'), ('Enter the second parameter', 'Select conversion direction')],
    },
    'calorie-burn-calc': {
        'cn': [('输入第一个参数', '输入体重（公斤）'), ('输入第二个参数', '输入运动时长（分钟）'), ('输入第三个参数', '选择运动类型，点击"计算"按钮')],
        'en': [('Enter the first parameter', 'Enter your weight in kg'), ('Enter the second parameter', 'Enter exercise duration in minutes'), ('Enter the third parameter', 'Select exercise type and click "Calculate"')],
    },
}

base = '/home/chison/tools-site'
fixed = 0

for tool, calcs in TOOLS.items():
    for lang, calc_func in [('cn', calcs['cn_calc']), ('en', calcs['en_calc'])]:
        if lang == 'cn':
            fpath = os.path.join(base, tool, 'index.html')
        else:
            fpath = os.path.join(base, 'en', tool, 'index.html')
        
        if not os.path.exists(fpath):
            print(f"SKIP (not found): {fpath}")
            continue
        
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace calc() function
        # Match from 'function calc(){' to the closing '}' at same indentation level
        pattern = r'function calc\(\)\{[\s\S]*?\n\}'
        new_content = re.sub(pattern, calc_func.replace('\\', '\\\\'), content, count=1)
        
        if new_content == content:
            print(f"WARN: calc() not replaced in {fpath}")
        else:
            content = new_content
            fixed += 1
        
        # Fix placeholder steps
        if tool in PLACEHOLDER_FIXES:
            fixes = PLACEHOLDER_FIXES[tool].get(lang, [])
            for old, new in fixes:
                if old in content:
                    content = content.replace(old, new)
        
        # For EN pages, also fix footer Chinese and copyright Chinese
        if lang == 'en':
            # Fix footer links
            content = content.replace('联系我们', 'Contact Us')
            content = content.replace('隐私政策', 'Privacy Policy')
            content = content.replace('服务条款', 'Terms of Service')
            content = content.replace('关于我们', 'About Us')
            content = content.replace('首页', 'Home')
            # Fix copyright
            content = content.replace('所有计算在浏览器本地完成，数据不上传服务器', 'All calculations run locally in your browser, data never leaves your device')
            content = content.replace('数据不上传服务器', 'data never leaves your device')
        
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"FIXED: {fpath}")

print(f"\nTotal files fixed: {fixed}")
