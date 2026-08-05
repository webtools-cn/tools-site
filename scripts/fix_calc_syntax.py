#!/usr/bin/env python3
"""修复8个新计算器工具的JS语法错误。
问题：calc()函数里 var a 和 let a 重复声明 + v1/v2/v3/result 裸引用
修复：删除前4行var声明+isNaN验证，保留let行但用getElementById包装，result也用getElementById
"""
import re, os

TOOLS = [
    'paint-needed-calculator',
    'paper-size-calculator', 
    'mix-ratio-calculator',
    'coffee-cost-calculator',
    'ramp-slope-calculator',
    'carpet-cost-calculator',
    'soil-volume-calculator',
    'event-budget-calculator',
]

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 匹配整个calc函数
    # 模式: function calc(){\n  var a=...\n  var b=...\n  var v3el=...\n  var c=...\n  if(isNaN...\n  let a=...\n}
    pattern = r'function calc\(\)\{\n  var a=parseFloat\(document\.getElementById\(\'v1\'\)\.value\);\n  var b=parseFloat\(document\.getElementById\(\'v2\'\)\.value\);\n  var v3el=document\.getElementById\(\'v3\'\);\n  var c=v3el\?parseFloat\(v3el\.value\):0;\n  if\(isNaN\(a\)\|\|isNaN\(b\)\|\|\(v3el&&isNaN\(c\)\)\)\{show\([^)]+\);return\}\n  (let a=.+?)\n\}'
    
    m = re.search(pattern, content, re.DOTALL)
    if not m:
        print(f"  SKIP: pattern not found in {filepath}")
        return False
    
    calc_logic = m.group(1)  # let a=... 那一行
    
    # 修复 calc_logic:
    # 1. v1.value → document.getElementById('v1').value
    # 2. v2.value → document.getElementById('v2').value  
    # 3. v3.value → document.getElementById('v3').value
    # 4. result.textContent → (function(){var r=document.getElementById('result');r.style.display='block';var rv=document.getElementById('rv');rv.textContent=
    # 但这太复杂了。更简单：直接替换result.textContent为正确的调用
    
    # 替换裸引用
    calc_logic = calc_logic.replace("v1.value", "document.getElementById('v1').value")
    calc_logic = calc_logic.replace("v2.value", "document.getElementById('v2').value")
    calc_logic = calc_logic.replace("v3.value", "document.getElementById('v3').value")
    
    # result.textContent= → var __r=document.getElementById('result');__r.style.display='block';document.getElementById('rv').textContent=
    # 但可能有多次result.textContent调用，需要处理
    # 实际上每行只有2次: 一次设置"请输入完整参数"，一次设置结果
    # 方案：把 result.textContent=X 替换为 __setResult(X)
    
    calc_logic = calc_logic.replace("result.textContent=", "__setResult(")
    # 现在需要找到对应的赋值结束位置。result.textContent="xxx";return 变成 __setResult("xxx");return
    # result.textContent=...; return → __setResult(...); return
    # 但 __setResult( 后面需要加 )
    
    # 这个方法太脆弱，改用更直接的方式
    # 直接重写整个calc函数
    
    return False  # 先用另一个方法

# 更直接的方法：直接替换整个calc函数体
def fix_file_v2(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取 let a= 那一行的计算逻辑
    pattern = r'function calc\(\)\{\n  var a=parseFloat\(document\.getElementById\(\'v1\'\)\.value\);\n  var b=parseFloat\(document\.getElementById\(\'v2\'\)\.value\);\n  var v3el=document\.getElementById\(\'v3\'\);\n  var c=v3el\?parseFloat\(v3el\.value\):0;\n  if\(isNaN\(a\)\|\|isNaN\(b\)\|\|\(v3el&&isNaN\(c\)\)\)\{show\(([^)]+)\);return\}\n  (let a=.+?)\n\}'
    
    m = re.search(pattern, content, re.DOTALL)
    if not m:
        print(f"  SKIP: pattern not found in {filepath}")
        return False
    
    show_msg = m.group(1)  # '请输入有效数值' 或 'Please enter valid numbers'
    calc_line = m.group(2)  # let a=... 计算逻辑
    
    # 修复裸引用
    calc_line = calc_line.replace("v1.value", "document.getElementById('v1').value")
    calc_line = calc_line.replace("v2.value", "document.getElementById('v2').value")
    calc_line = calc_line.replace("v3.value", "document.getElementById('v3').value")
    
    # 修复 result.textContent → 正确的DOM操作
    # 分两种情况：
    # 1. result.textContent="请输入完整参数";return  → show('请输入完整参数');return  
    # 2. result.textContent=计算结果  → 设置rv和rd
    
    # 把 result.textContent="xxx";return 替换为 show("xxx");return
    calc_line = re.sub(r'result\.textContent=("(?:[^"\\]|\\.)*");return', r'show(\1);return', calc_line)
    
    # 把剩余的 result.textContent= 替换为正确的DOM更新
    # 找到最后一个 result.textContent= 的值
    # 它后面通常是整个表达式的结尾
    if 'result.textContent=' in calc_line:
        # 把 result.textContent=X 替换为 
        # var __r=document.getElementById('result');__r.style.display='block';document.getElementById('rv').textContent=X
        calc_line = re.sub(
            r'result\.textContent=(.+)$',
            r"var __r=document.getElementById('result');__r.style.display='block';document.getElementById('rv').textContent=\1",
            calc_line
        )
    
    # 构建新的calc函数
    new_func = f"""function calc(){{
  {calc_line}
}}"""
    
    # 替换旧的calc函数
    old_func_pattern = r'function calc\(\)\{[\s\S]*?\n\}'
    new_content = re.sub(old_func_pattern, new_func, content, count=1)
    
    if new_content == content:
        print(f"  SKIP: replacement failed in {filepath}")
        return False
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"  FIXED: {filepath}")
    return True

fixed = 0
for tool in TOOLS:
    print(f"\n=== {tool} ===")
    for path in [f'{tool}/index.html', f'en/{tool}/index.html']:
        if os.path.exists(path):
            if fix_file_v2(path):
                fixed += 1

print(f"\n\nTotal fixed: {fixed}/16")
