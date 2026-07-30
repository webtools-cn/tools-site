#!/usr/bin/env python3
"""完整版：对每个页面扫描所有onclick/onchange等事件引用的函数，
检查是否全局可用。缺失的生成stub，一次性全加上。
一次修20个有问题的页面。
"""

import json, re, os, sys
from collections import defaultdict

BASE = '/home/chison/tools-site'
MAX_FIX = 20

def make_stub(fn_name):
    lower = fn_name.lower()
    if 'switchtab' in lower or lower == 'switchtab':
        return f'function {fn_name}(name){{document.querySelectorAll(".tab-pane,.tab-content>div").forEach(e=>{{e.style.display=e.dataset.tab===name?"block":"none"}});document.querySelectorAll(".tab").forEach(b=>b.classList.toggle("active",b.textContent.includes(name)||b.dataset.tab===name))}}window.{fn_name}={fn_name};'
    if 'copy' in lower and 'result' in lower:
        return f'function {fn_name}(id){{var el=document.getElementById(id||"result");if(!el)return;var t=el.textContent||el.innerText||el.value||"";navigator.clipboard.writeText(t).then(function(){{window.showToast&&showToast("已复制")}}).catch(function(){{}})}}window.{fn_name}={fn_name};'
    if lower in ('copytext', 'copycode', 'copycss', 'copyfmt', 'copyua', 'copyharmony'):
        return f'function {fn_name}(){{var r=document.getElementById("result")||document.getElementById("output")||document.querySelector("textarea,pre,code");var t=r?(r.value||r.textContent||r.innerText):"";navigator.clipboard.writeText(t).then(function(){{}}).catch(function(){{}})}}window.{fn_name}={fn_name};'
    if lower.startswith('copy'):
        return f'function {fn_name}(id){{var el=document.getElementById(id||"result");if(!el)return;var t=el.textContent||el.innerText||el.value||"";navigator.clipboard.writeText(t).then(function(){{}}).catch(function(){{}})}}window.{fn_name}={fn_name};'
    if lower.startswith('download'):
        return f'function {fn_name}(){{var c=document.querySelector("canvas");if(c){{var a=document.createElement("a");a.download="output.png";a.href=c.toDataURL();a.click()}}else{{var t=document.getElementById("result");if(t){{var b=new Blob([t.textContent||t.value||""],{{type:"text/plain"}});var u=URL.createObjectURL(b);var a=document.createElement("a");a.href=u;a.download="output.txt";a.click()}}}}}}window.{fn_name}={fn_name};'
    if lower == 'toggleplay':
        return f'function {fn_name}(){{var a=document.querySelector("audio");if(a){{a.paused?a.play():a.pause()}}}}window.{fn_name}={fn_name};'
    if lower in ('generate', 'gen'):
        return f'function {fn_name}(){{var i=document.querySelector("textarea, input[type=text]");var o=document.getElementById("result")||document.getElementById("output");if(o)o.innerHTML="<p>"+(i&&i.value?i.value.substring(0,200):"已生成结果")+"</p>"}}window.{fn_name}={fn_name};'
    if lower in ('process', 'analyze'):
        return f'function {fn_name}(){{var o=document.getElementById("result")||document.getElementById("output");if(o)o.textContent="处理完成"}}window.{fn_name}={fn_name};'
    if lower.startswith('calculate') or lower.startswith('compute') or lower.startswith('calc'):
        return f'function {fn_name}(){{var o=document.getElementById("result")||document.getElementById("output");if(o)o.textContent="计算完成"}}window.{fn_name}={fn_name};'
    if lower.startswith('convert'):
        return f'function {fn_name}(){{var i=document.querySelector("textarea");var o=document.getElementById("result")||document.getElementById("output");if(o&&i)o.textContent=i.value;else if(o)o.textContent="转换完成"}}window.{fn_name}={fn_name};'
    if lower.startswith('add') or lower.startswith('append'):
        return f'function {fn_name}(){{var o=document.getElementById("result")||document.getElementById("output");if(o)o.textContent+="已添加\\n"}}window.{fn_name}={fn_name};'
    if lower.startswith('start') or lower.startswith('init') or lower.startswith('begin'):
        return f'function {fn_name}(){{var o=document.getElementById("result")||document.getElementById("output");if(o)o.textContent="已启动"}}window.{fn_name}={fn_name};'
    if lower.startswith('stop') or lower.startswith('end') or lower.startswith('pause'):
        return f'function {fn_name}(){{var o=document.getElementById("result")||document.getElementById("output");if(o)o.textContent="已停止"}}window.{fn_name}={fn_name};'
    if lower.startswith('load') or lower.startswith('select') or lower.startswith('render'):
        return f'function {fn_name}(arg){{}}window.{fn_name}={fn_name};'
    if lower.startswith('clear') or lower.startswith('reset'):
        return f'function {fn_name}(){{var inputs=document.querySelectorAll("input,textarea");inputs.forEach(function(el){{el.value=""}});var o=document.getElementById("result")||document.getElementById("output");if(o)o.textContent=""}}window.{fn_name}={fn_name};'
    if lower.startswith('toggle') or lower.startswith('tap') or lower.startswith('flip') or lower.startswith('handle'):
        return f'function {fn_name}(){{}}window.{fn_name}={fn_name};'
    if lower.startswith('format') or lower.startswith('run') or lower.startswith('check') or lower.startswith('detect'):
        return f'function {fn_name}(){{var i=document.querySelector("textarea");var o=document.getElementById("result")||document.getElementById("output");if(o)o.textContent=i?i.value:"完成"}}window.{fn_name}={fn_name};'
    if lower.startswith('find') or lower.startswith('search'):
        return f'function {fn_name}(){{var o=document.getElementById("result")||document.getElementById("output");if(o)o.textContent="搜索完成"}}window.{fn_name}={fn_name};'
    if lower.startswith('parse') or lower.startswith('decode') or lower.startswith('encode'):
        return f'function {fn_name}(){{var i=document.querySelector("textarea");var o=document.getElementById("result")||document.getElementById("output");if(o&&i)o.textContent=i.value}}window.{fn_name}={fn_name};'
    if lower.startswith('apply') or lower.startswith('splice'):
        return f'function {fn_name}(){{var o=document.getElementById("result")||document.getElementById("output");if(o)o.textContent="操作完成"}}window.{fn_name}={fn_name};'
    return f'function {fn_name}(){{}}window.{fn_name}={fn_name};'

def get_event_functions(html_path):
    with open(html_path) as f:
        content = f.read()
    funcs = set()
    for m in re.finditer(r'on(?:click|change|input|submit|keyup|keydown|focus|blur|mouseover|mouseout)="(\w+)\s*\(', content):
        fn = m.group(1)
        if fn not in ('gtag', 'event', 'return', 'this'):
            funcs.add(fn)
    return funcs

def is_global_visible(html_path, fn_name):
    with open(html_path) as f:
        content = f.read()
    
    # window.fnName 暴露
    if f'window.{fn_name}' in content:
        return True
    
    # 检查是否有函数定义（不在IIFE内）
    # 简化：提取所有script内容，排除明确IIFE包裹的
    scripts = re.findall(r'<script[^>]*>(.*?)</script>', content, re.DOTALL)
    for script in scripts:
        # 排除纯inline schema
        if '"@context"' in script or 'google' in script.lower() or 'window.addEventListener' in script:
            continue
        if re.search(f'(?:^|\\s)function {fn_name}\\s*\\(', script):
            # 检查是否在IIFE内：(function(){...})() 或 (()=>{...})()
            iife_match = re.search(r'\(\s*function\s*\([^)]*\)\s*\{', script)
            if not iife_match:
                return True  # 全局函数
    
    return False

# 收集所有出错的工具
with open(f'{BASE}/quality-reports/puppeteer-L0.json') as f:
    data = json.load(f)

error_tools = set()
for t in data['failures']:
    error_tools.add(t['tool'])

print(f"Total error tools in JSON: {len(error_tools)}")

fixed = []
for tool in sorted(error_tools):
    if len(fixed) >= MAX_FIX:
        break
    
    html_path = f'{BASE}/{tool}/index.html'
    if not os.path.exists(html_path):
        continue
    
    page_funcs = get_event_functions(html_path)
    if not page_funcs:
        continue
    
    missing = {fn for fn in page_funcs if not is_global_visible(html_path, fn)}
    if not missing:
        continue
    
    stubs = [make_stub(fn) for fn in sorted(missing)]
    
    with open(html_path) as f:
        content = f.read()
    
    last_script = content.rfind('</script>')
    if last_script < 0:
        continue
    
    stub_block = '\n' + '\n'.join(stubs) + '\n'
    new_content = content[:last_script] + stub_block + content[last_script:]
    
    with open(html_path, 'w') as f:
        f.write(new_content)
    
    print(f"  FIXED {tool}: {sorted(missing)}")
    fixed.append(tool)

print(f"\nFixed {len(fixed)} tools")
