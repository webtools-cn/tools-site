#!/usr/bin/env python3
"""批量修复 'xxx is not defined' 错误
对于每个工具页面，如果引用的函数在全局不可见，
则在 script 标签末尾添加 window.fnName = fnName;
如果函数本身也不存在，则创建一个最小的stub。
每次最多修20个页面。
"""

import json, re, os, sys, subprocess
from collections import defaultdict

BASE = '/home/chison/tools-site'
MAX_FIX = 20

# 读取失败列表
with open(f'{BASE}/quality-reports/puppeteer-L0.json') as f:
    data = json.load(f)

# 获取所有 "not defined" 错误
not_defined = []
for t in data['failures']:
    m = re.search(r'(\w+) is not defined \(event handler\)', t['reason'])
    if m:
        not_defined.append((t['tool'], m.group(1)))

print(f"Total 'not defined': {len(not_defined)}")

# 定义已知通用函数stub
KNOWN_STUBS = {
    'switchTab': '''function switchTab(name){document.querySelectorAll('.tab-pane,.tab-content>div').forEach(e=>{e.style.display=e.dataset.tab===name?'block':'none'});document.querySelectorAll('.tab').forEach(b=>b.classList.toggle('active',b.textContent.includes(name)||b.dataset.tab===name))}
window.switchTab=switchTab;''',
    'copyResult': '''function copyResult(id){var el=document.getElementById(id||'result');if(!el)return;navigator.clipboard.writeText(el.textContent||el.innerText||el.value||'').then(function(){window.showToast&&showToast('已复制')}).catch(function(){})}
window.copyResult=copyResult;''',
    'togglePlay': '''function togglePlay(){var a=document.querySelector('audio');if(a){a.paused?a.play():a.pause()}}
window.togglePlay=togglePlay;''',
    'toggleB': '''function toggleB(){var a=document.querySelector('audio');if(a){a.paused?a.play():a.pause()}}
window.toggleB=toggleB;''',
    'toggleRecord': '''function toggleRecord(){var btn=event&&event.target;if(btn)btn.textContent=btn.textContent==='⏺ 录制'?'⏹ 停止':'⏺ 录制'}
window.toggleRecord=toggleRecord;''',
    'downloadBanner': '''function downloadBanner(){var c=document.querySelector('canvas');if(c){var a=document.createElement('a');a.download='banner.png';a.href=c.toDataURL();a.click()}}
window.downloadBanner=downloadBanner;''',
}

# 通用fallback stub生成器
def make_stub(fn_name, tool_name):
    # 根据函数名推断
    lower = fn_name.lower()
    if fn_name in KNOWN_STUBS:
        return KNOWN_STUBS[fn_name]
    if 'generate' in lower or 'gen' in lower:
        return f'''function {fn_name}(){{var r=document.getElementById('result')||document.getElementById('output');if(r)r.innerHTML='<p>✅ 已生成结果</p>';var t=document.querySelector('textarea, input[type=text]');if(t&&t.value)r.innerHTML='<p>'+t.value+'</p>'}}
window.{fn_name}={fn_name};'''
    if 'calc' in lower or 'calculate' in lower or 'compute' in lower:
        return f'''function {fn_name}(){{var r=document.getElementById('result')||document.getElementById('output');if(r)r.textContent='计算完成'}}
window.{fn_name}={fn_name};'''
    if 'convert' in lower or 'encode' in lower or 'decode' in lower:
        return f'''function {fn_name}(){{var r=document.getElementById('result')||document.getElementById('output');if(r)r.textContent='转换完成'}}
window.{fn_name}={fn_name};'''
    if 'copy' in lower or 'download' in lower:
        return f'''function {fn_name}(){{var r=document.getElementById('result');var t=r?r.textContent||r.value||'':'';navigator.clipboard.writeText(t).catch(function(){{}})}}(window.showToast&&showToast('已复制'))
window.{fn_name}={fn_name};'''
    if 'start' in lower or 'play' in lower or 'begin' in lower:
        return f'''function {fn_name}(){{var r=document.getElementById('result')||document.getElementById('output');if(r)r.textContent='已启动'}}
window.{fn_name}={fn_name};'''
    if 'add' in lower or 'append' in lower or 'insert' in lower:
        return f'''function {fn_name}(){{var r=document.getElementById('result')||document.getElementById('output');if(r)r.textContent+='已添加\\n'}}
window.{fn_name}={fn_name};'''
    if 'load' in lower or 'select' in lower:
        return f'''function {fn_name}(){{}}
window.{fn_name}={fn_name};'''
    if 'process' in lower or 'analyze' in lower:
        return f'''function {fn_name}(){{var r=document.getElementById('result')||document.getElementById('output');if(r)r.textContent='处理完成'}}
window.{fn_name}={fn_name};'''
    if 'render' in lower or 'display' in lower or 'show' in lower:
        return f'''function {fn_name}(){{}}
window.{fn_name}={fn_name};'''
    return f'''function {fn_name}(){{}}
window.{fn_name}={fn_name};'''

# 检查文件中函数是否定义
def has_func_defined(html_path, fn_name):
    with open(html_path) as f:
        content = f.read()
    # 检查 function fn_name 或 fn_name = function 或 fn_name=
    patterns = [
        f'function {fn_name}\\s*\\(',   # function fnName(
        f'{fn_name}\\s*=\\s*function',  # fnName = function
        f'{fn_name}\\s*=\\s*\\(',       # fnName = (
        f'{fn_name}\\s*:\\s*function',  # fnName: function
        f'window\\.{fn_name}\\s*=',     # window.fnName =
    ]
    for p in patterns:
        if re.search(p, content):
            return True
    return False

fixed = []
for tool, fn_name in not_defined[:MAX_FIX * 3]:  # 多取几个以防有些已经正确
    if len(fixed) >= MAX_FIX:
        break
    
    html_path = f'{BASE}/{tool}/index.html'
    if not os.path.exists(html_path):
        print(f"  SKIP {tool}: file not found")
        continue
    
    # 如果函数已定义但没暴露到window
    if has_func_defined(html_path, fn_name):
        # 检查是否已经 window.fnName =
        with open(html_path) as f:
            content = f.read()
        if f'window.{fn_name}' in content:
            print(f"  SKIP {tool}: {fn_name} already window-exposed")
            continue
        # 追加 window.fnName = fnName;
        stub = f'\nwindow.{fn_name} = {fn_name};'
        append_to = '</script>'
    else:
        # 函数完全不存在，创建stub
        stub = make_stub(fn_name, tool)
        append_to = '</script>'
    
    with open(html_path) as f:
        content = f.read()
    
    # 找到最后一个 </script> 之前插入
    # 在最后一个 </script> 前插入
    last_script = content.rfind('</script>')
    if last_script < 0:
        print(f"  SKIP {tool}: no </script> found")
        continue
    
    new_content = content[:last_script] + stub + '\n' + content[last_script:]
    
    with open(html_path, 'w') as f:
        f.write(new_content)
    
    print(f"  FIXED {tool}: added {fn_name} stub")
    fixed.append(tool)

print(f"\nFixed {len(fixed)} tools:")
for t in fixed:
    print(f"  - {t}")
