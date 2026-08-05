#!/usr/bin/env python3
"""Fix calc() function in new tool pages: 
1. Remove duplicate const declarations
2. Replace return with DOM update + display:block
3. Fix EN Chinese text残留
"""
import re, os

BASE = "/home/chison/tools-site"

# Define fixes for each tool: (cn_file, en_file, cn_calc_body, en_calc_body)
# Each calc_body is the JS code that goes between the validation check and the closing brace

tools = {
    "warehouse-capacity-calculator": {
        "cn": '''  var v4el=document.getElementById('v4');var d=v4el?v4el.value:'1';
  var area=a, aisle=b, palletArea=c;
  var layers=v4el?parseInt(d):1;
  if(palletArea<=0||layers<=0){show('请输入有效数值');return}
  var usable=area*(1-aisle/100);
  var perLayer=Math.floor(usable/palletArea);
  var total=perLayer*layers;
  document.getElementById('rv').textContent=total+' 托盘';
  document.getElementById('rd').textContent='每层 '+perLayer+' 托盘 × '+layers+' 层 | 可用面积 '+usable.toFixed(1)+'m²';
  document.getElementById('result').style.display='block';''',
        "en": '''  var v4el=document.getElementById('v4');var d=v4el?v4el.value:'1';
  var area=a, aisle=b, palletArea=c;
  var layers=v4el?parseInt(d):1;
  if(palletArea<=0||layers<=0){show('Please enter valid numbers');return}
  var usable=area*(1-aisle/100);
  var perLayer=Math.floor(usable/palletArea);
  var total=perLayer*layers;
  document.getElementById('rv').textContent=total+' pallets';
  document.getElementById('rd').textContent=perLayer+' pallets/layer × '+layers+' layers | Usable area '+usable.toFixed(1)+'m²';
  document.getElementById('result').style.display='block';''',
    },
    "fence-cost-calculator": {
        "cn": '''  var v4el=document.getElementById('v4');var d=v4el?v4el.value:'0';
  var length=a, material=c, labor=v4el?parseFloat(d):0;
  var total=length*(material+labor);
  document.getElementById('rv').textContent='¥'+total.toFixed(2);
  document.getElementById('rd').textContent='长度 '+length+'m × (材料¥'+material.toFixed(2)+'/m + 人工¥'+labor.toFixed(2)+'/m)';
  document.getElementById('result').style.display='block';''',
        "en": '''  var v4el=document.getElementById('v4');var d=v4el?v4el.value:'0';
  var length=a, material=c, labor=v4el?parseFloat(d):0;
  var total=length*(material+labor);
  document.getElementById('rv').textContent='$'+total.toFixed(2);
  document.getElementById('rd').textContent='Length '+length+'m × (Material $'+material.toFixed(2)+'/m + Labor $'+labor.toFixed(2)+'/m)';
  document.getElementById('result').style.display='block';''',
    },
    "postage-calculator": {
        "cn": '''  var wt=a, dist=b, method=c;
  var base=5;
  var rate=[0.5,1.2,3.0][method-1]||0.5;
  var cost=base+wt*rate*dist*0.1;
  var final=Math.max(5,cost);
  var methods=['标准','加急','特快'];
  document.getElementById('rv').textContent='¥'+final.toFixed(2);
  document.getElementById('rd').textContent=methods[Math.min(method-1,2)]+' | '+wt+'kg × '+dist+'km | 基础费¥5';
  document.getElementById('result').style.display='block';''',
        "en": '''  var wt=a, dist=b, method=c;
  var base=5;
  var rate=[0.5,1.2,3.0][method-1]||0.5;
  var cost=base+wt*rate*dist*0.1;
  var final=Math.max(5,cost);
  var methods=['Standard','Express','Priority'];
  document.getElementById('rv').textContent='$'+final.toFixed(2);
  document.getElementById('rd').textContent=methods[Math.min(method-1,2)]+' | '+wt+'kg × '+dist+'km | Base $5';
  document.getElementById('result').style.display='block';''',
    },
    "recipe-scaler-calculator": {
        "cn": '''  var v4el=document.getElementById('v4');var d=v4el?v4el.value:'配料';
  var orig=a, target=b, amount=c, name=d;
  var ratio=target/orig;
  var scaled=amount*ratio;
  document.getElementById('rv').textContent=scaled.toFixed(1)+' g';
  document.getElementById('rd').textContent=name+': '+amount+'g → '+scaled.toFixed(1)+'g (系数 '+ratio.toFixed(2)+'×)';
  document.getElementById('result').style.display='block';''',
        "en": '''  var v4el=document.getElementById('v4');var d=v4el?v4el.value:'Ingredient';
  var orig=a, target=b, amount=c, name=d;
  var ratio=target/orig;
  var scaled=amount*ratio;
  document.getElementById('rv').textContent=scaled.toFixed(1)+' g';
  document.getElementById('rd').textContent=name+': '+amount+'g → '+scaled.toFixed(1)+'g (Factor '+ratio.toFixed(2)+'×)';
  document.getElementById('result').style.display='block';''',
    },
    "celsius-to-kelvin": {
        "cn": '''  var celsius=a;
  var k=celsius+273.15;
  document.getElementById('rv').textContent=k.toFixed(2)+' K';
  document.getElementById('rd').textContent=celsius+'°C + 273.15 = '+k.toFixed(2)+' K';
  document.getElementById('result').style.display='block';''',
        "en": '''  var celsius=a;
  var k=celsius+273.15;
  document.getElementById('rv').textContent=k.toFixed(2)+' K';
  document.getElementById('rd').textContent=celsius+'°C + 273.15 = '+k.toFixed(2)+' K';
  document.getElementById('result').style.display='block';''',
    },
    "fahrenheit-to-kelvin": {
        "cn": '''  var f=a;
  var k=(f-32)*5/9+273.15;
  document.getElementById('rv').textContent=k.toFixed(2)+' K';
  document.getElementById('rd').textContent='('+f+'°F - 32) × 5/9 + 273.15 = '+k.toFixed(2)+' K';
  document.getElementById('result').style.display='block';''',
        "en": '''  var f=a;
  var k=(f-32)*5/9+273.15;
  document.getElementById('rv').textContent=k.toFixed(2)+' K';
  document.getElementById('rd').textContent='('+f+'°F - 32) × 5/9 + 273.15 = '+k.toFixed(2)+' K';
  document.getElementById('result').style.display='block';''',
    },
    "kelvin-to-fahrenheit": {
        "cn": '''  var k=a;
  var f=(k-273.15)*9/5+32;
  document.getElementById('rv').textContent=f.toFixed(2)+' °F';
  document.getElementById('rd').textContent='('+k+'K - 273.15) × 9/5 + 32 = '+f.toFixed(2)+' °F';
  document.getElementById('result').style.display='block';''',
        "en": '''  var k=a;
  var f=(k-273.15)*9/5+32;
  document.getElementById('rv').textContent=f.toFixed(2)+' °F';
  document.getElementById('rd').textContent='('+k+'K - 273.15) × 9/5 + 32 = '+f.toFixed(2)+' °F';
  document.getElementById('result').style.display='block';''',
    },
    "hexagon-area-calculator": {
        "cn": '''  var s=a;
  var area=(3*Math.sqrt(3)/2)*s*s;
  document.getElementById('rv').textContent=area.toFixed(4)+' m²';
  document.getElementById('rd').textContent='(3√3/2) × '+s+'² = '+area.toFixed(4)+' m²';
  document.getElementById('result').style.display='block';''',
        "en": '''  var s=a;
  var area=(3*Math.sqrt(3)/2)*s*s;
  document.getElementById('rv').textContent=area.toFixed(4)+' m²';
  document.getElementById('rd').textContent='(3√3/2) × '+s+'² = '+area.toFixed(4)+' m²';
  document.getElementById('result').style.display='block';''',
    },
    "ellipse-area-calculator": {
        "cn": '''  var aa=a, bb=b;
  var area=Math.PI*aa*bb;
  document.getElementById('rv').textContent=area.toFixed(4)+' m²';
  document.getElementById('rd').textContent='π × '+aa+' × '+bb+' = '+area.toFixed(4)+' m²';
  document.getElementById('result').style.display='block';''',
        "en": '''  var aa=a, bb=b;
  var area=Math.PI*aa*bb;
  document.getElementById('rv').textContent=area.toFixed(4)+' m²';
  document.getElementById('rd').textContent='π × '+aa+' × '+bb+' = '+area.toFixed(4)+' m²';
  document.getElementById('result').style.display='block';''',
    },
}

fixed = 0
for tool, fix in tools.items():
    for lang in ["cn", "en"]:
        if lang == "cn":
            fpath = os.path.join(BASE, tool, "index.html")
        else:
            fpath = os.path.join(BASE, "en", tool, "index.html")
        
        if not os.path.exists(fpath):
            print(f"SKIP (not found): {fpath}")
            continue
        
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find the calc function and replace the body after the validation check
        # Pattern: from "if(isNaN..." line to the closing "}"
        old_pattern = r"(if\(isNaN\(a\)\|\|isNaN\(b\)\|\|\(v3el&&isNaN\(c\)\)\)\{show\([^}]+\);return\}\n)(  const .+?\n})(\n})"
        
        replacement = r"\1" + fix[lang] + r"\n}"
        
        new_content = re.sub(old_pattern, replacement, content, flags=re.DOTALL)
        
        if new_content != content:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"FIXED: {fpath}")
            fixed += 1
        else:
            # Try alternate pattern - the return line might be on same line as const
            old_pattern2 = r"(if\(isNaN\(a\)\|\|isNaN\(b\)\|\|\(v3el&&isNaN\(c\)\)\)\{show\([^}]+\);return\}\n)(.+?)(\n})"
            new_content2 = re.sub(old_pattern2, replacement, content, flags=re.DOTALL)
            if new_content2 != content:
                with open(fpath, 'w', encoding='utf-8') as f:
                    f.write(new_content2)
                print(f"FIXED (alt): {fpath}")
                fixed += 1
            else:
                print(f"NO MATCH: {fpath}")

print(f"\nTotal fixed: {fixed}")
