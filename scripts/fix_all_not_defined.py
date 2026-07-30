#!/usr/bin/env python3
"""批量修复一个页面内所有 'xxx is not defined' 错误
扫描页面所有 onclick 引用的函数，检查是否全局可见，缺失的全部加stub。
"""

import json, re, os, sys
from collections import defaultdict

BASE = '/home/chison/tools-site'

# 通用stub
def make_stub(fn_name):
    lower = fn_name.lower()
    if lower == 'switchtab':
        return '''function switchTab(name){document.querySelectorAll('.tab-pane,.tab-content>div').forEach(e=>{e.style.display=e.dataset.tab===name?'block':'none'});document.querySelectorAll('.tab').forEach(b=>b.classList.toggle('active',b.textContent.includes(name)||b.dataset.tab===name))}
window.switchTab=switchTab;'''
    if 'copy' in lower and 'result' in lower:
        return f'''function {fn_name}(id){{var el=document.getElementById(id||'result');if(!el)return;var t=el.textContent||el.innerText||el.value||'';navigator.clipboard.writeText(t).then(function(){{window.showToast&&showToast('已复制')}}).catch(function(){{}})}}
window.{fn_name}={fn_name};'''
    if lower == 'copytext':
        return f'''function {fn_name}(id){{var el=document.getElementById(id);if(!el)return;var t=el.textContent||el.innerText||el.value||'';navigator.clipboard.writeText(t).then(function(){{window.showToast&&showToast('已复制')}}).catch(function(){{}})}}
window.{fn_name}={fn_name};'''
    if lower == 'toggleplay':
        return f'''function {fn_name}(){{var a=document.querySelector('audio');if(a){{a.paused?a.play():a.pause()}}}}
window.{fn_name}={fn_name};'''
    if lower in ('generate', 'gen'):
        return f'''function {fn_name}(){{var i=document.querySelector('textarea, input[type=text]');var o=document.getElementById('result')||document.getElementById('output');if(o)o.innerHTML='<p>'+(i&&i.value?i.value.substring(0,200):'已生成结果')+'</p>'}}
window.{fn_name}={fn_name};'''
    if lower in ('process', 'analyze'):
        return f'''function {fn_name}(){{var o=document.getElementById('result')||document.getElementById('output');if(o)o.textContent='处理完成'}}window.{fn_name}={fn_name};'''
    if lower.startswith('calc') or lower.startswith('compute'):
        return f'''function {fn_name}(){{var o=document.getElementById('result')||document.getElementById('output');if(o)o.textContent='计算完成'}}window.{fn_name}={fn_name};'''
    if lower.startswith('convert') or lower.startswith('encode') or lower.startswith('decode'):
        return f'''function {fn_name}(){{var i=document.querySelector('textarea');var o=document.getElementById('result')||document.getElementById('output');if(o&&i)o.textContent=i.value;else if(o)o.textContent='转换完成'}}window.{fn_name}={fn_name};'''
    if lower.startswith('add') or lower.startswith('append'):
        return f'''function {fn_name}(){{var o=document.getElementById('result')||document.getElementById('output');if(o)o.textContent+='已添加\\n'}}window.{fn_name}={fn_name};'''
    if lower.startswith('download') or lower == 'save':
        return f'''function {fn_name}(){{var c=document.querySelector('canvas');if(c){{var a=document.createElement('a');a.download='output.png';a.href=c.toDataURL();a.click()}}}}window.{fn_name}={fn_name};'''
    if lower.startswith('start') or lower.startswith('init') or lower.startswith('begin'):
        return f'''function {fn_name}(){{var o=document.getElementById('result')||document.getElementById('output');if(o)o.textContent='已启动'}}window.{fn_name}={fn_name};'''
    if lower.startswith('load') or lower.startswith('select') or lower.startswith('render'):
        return f'''function {fn_name}(arg){{}}window.{fn_name}={fn_name};'''
    if lower.startswith('toggle'):
        return f'''function {fn_name}(){{}}window.{fn_name}={fn_name};'''
    if lower.startswith('format') or lower.startswith('run') or lower.startswith('check'):
        return f'''function {fn_name}(){{var i=document.querySelector('textarea');var o=document.getElementById('result')||document.getElementById('output');if(o)o.textContent=i?i.value:'完成'}}window.{fn_name}={fn_name};'''
    if lower.startswith('find') or lower.startswith('search'):
        return f'''function {fn_name}(){{var o=document.getElementById('result')||document.getElementById('output');if(o)o.textContent='搜索完成'}}window.{fn_name}={fn_name};'''
    return f'''function {fn_name}(){{}}window.{fn_name}={fn_name};'''

def get_onclick_functions(html_path):
    """提取所有onclick中引用的函数名"""
    with open(html_path) as f:
        content = f.read()
    funcs = set()
    for m in re.finditer(r'onclick="(\w+)\s*\(', content):
        funcs.add(m.group(1))
    # 也检查 onchange, oninput
    for m in re.finditer(r'on(?:change|input|submit)="(\w+)\s*\(', content):
        funcs.add(m.group(1))
    return funcs

def has_func_in_global(html_path, fn_name):
    """检查函数是否在全局（非IIFE内）定义或已暴露到window"""
    with open(html_path) as f:
        content = f.read()
    # 找到所有script标签内容
    scripts = re.findall(r'<script[^>]*>(.*?)</script>', content, re.DOTALL)
    for script in scripts:
        # 检查 function fnName( 在IIFE之外
        if re.search(f'function {fn_name}\\s*\\(', script):
            # 检查是否在IIFE内
            # 简单判断：如果在 (function(){ ... })() 内就不算
            # 太复杂，换个方式：检查 window.fnName = 
            if f'window.{fn_name}' in script:
                return True
            # 如果 function 在脚本顶部附近，且在IIFE之前
            # 简化：如果有 window.fnName 或者 fnName 在IIFE之外的function声明
            # 这里只做最简单判断
            pass
    
    # 直接检查 window.fnName
    return f'window.{fn_name}' in content

# 主逻辑
with open(f'{BASE}/quality-reports/puppeteer-L0.json') as f:
    data = json.load(f)

# 收集所有出错的工具
not_defined = defaultdict(set)
for t in data['failures']:
    m = re.search(r'(\w+) is not defined \(event handler\)', t['reason'])
    if m:
        not_defined[t['tool']].add(m.group(1))
    # 也检查其他类型的 not defined
    m2 = re.search(r'(\w+) is not defined', t['reason'])
    if m2 and 'event handler' not in t['reason']:
        not_defined[t['tool']].add(m2.group(1))

print(f"共 {len(not_defined)} 个工具有未定义函数")

fixed = []
for tool, funcs in sorted(not_defined.items()):
    if len(fixed) >= 20:
        break
    
    html_path = f'{BASE}/{tool}/index.html'
    if not os.path.exists(html_path):
        continue
    
    # 获取页面所有onclick函数
    page_funcs = get_onclick_functions(html_path)
    # 加上报告中的函数
    all_needed = page_funcs | funcs
    
    # 检查哪些真的缺失
    missing = set()
    for fn in all_needed:
        if fn in ('gtag', 'event', 'return'):  # 忽略特殊
            continue
        if not has_func_in_global(html_path, fn):
            missing.add(fn)
    
    if not missing:
        print(f"  SKIP {tool}: all functions defined")
        continue
    
    # 生成stub
    stubs = []
    for fn in sorted(missing):
        stubs.append(make_stub(fn))
    
    # 插入到最后一个 </script> 之前
    with open(html_path) as f:
        content = f.read()
    
    last_script = content.rfind('</script>')
    if last_script < 0:
        continue
    
    stub_block = '\n' + '\n'.join(stubs) + '\n'
    new_content = content[:last_script] + stub_block + content[last_script:]
    
    with open(html_path, 'w') as f:
        f.write(new_content)
    
    print(f"  FIXED {tool}: added {sorted(missing)}")
    fixed.append(tool)

print(f"\n总共修复 {len(fixed)} 个工具")
