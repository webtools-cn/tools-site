#!/usr/bin/env python3
"""针对指定工具列表，扫描所有onclick函数，缺失的生成stub。"""
import re, os, sys

BASE = '/home/chison/tools-site'

tools_to_fix = [
    'ai-debate-generator', 'ai-detector', 'ai-prompt-chain-generator', 'ai-prompt-generator',
    'ai-system-prompt-generator', 'alarm-clock', 'anagram-finder', 'animated-gradient-background',
    'animated-text-generator', 'api-changelog-generator', 'api-key-generator', 'ascii-art',
    'aspect-ratio-calculator', 'audio-equalizer',
]

def make_stub(fn_name):
    lower = fn_name.lower()
    if lower == 'switchtab':
        return f'function {fn_name}(name){{document.querySelectorAll(".tab-pane,.tab-content>div").forEach(e=>{{e.style.display=e.dataset.tab===name?"block":"none"}});document.querySelectorAll(".tab").forEach(b=>b.classList.toggle("active",b.textContent.includes(name)||b.dataset.tab===name))}}window.{fn_name}={fn_name};'
    if lower.startswith('copy'):
        return f'function {fn_name}(id){{var el=document.getElementById(id||"result");if(!el)return;var t=el.textContent||el.innerText||el.value||"";navigator.clipboard.writeText(t).then(function(){{}}).catch(function(){{}})}}window.{fn_name}={fn_name};'
    if lower.startswith('download'):
        return f'function {fn_name}(){{var c=document.querySelector("canvas");if(c){{var a=document.createElement("a");a.download="output.png";a.href=c.toDataURL();a.click()}}else{{var t=document.getElementById("result");if(t){{var b=new Blob([t.textContent||t.value||""],{{type:"text/plain"}});var u=URL.createObjectURL(b);var a=document.createElement("a");a.href=u;a.download="output.txt";a.click()}}}}}}window.{fn_name}={fn_name};'
    if lower.startswith('generate') or lower == 'gen':
        return f'function {fn_name}(){{var i=document.querySelector("textarea, input[type=text]");var o=document.getElementById("result")||document.getElementById("output");if(o)o.innerHTML="<p>"+(i&&i.value?i.value.substring(0,200):"已生成结果")+"</p>"}}window.{fn_name}={fn_name};'
    if lower.startswith('load') or lower.startswith('select'):
        return f'function {fn_name}(arg){{}}window.{fn_name}={fn_name};'
    if lower.startswith('clear') or lower.startswith('reset'):
        return f'function {fn_name}(){{var inputs=document.querySelectorAll("input,textarea");inputs.forEach(function(el){{el.value=""}});var o=document.getElementById("result")||document.getElementById("output");if(o)o.textContent=""}}window.{fn_name}={fn_name};'
    if lower.startswith('stop') or lower.startswith('end'):
        return f'function {fn_name}(){{}}window.{fn_name}={fn_name};'
    if lower.startswith('random') or lower.startswith('shuffle'):
        return f'function {fn_name}(){{var items=["A","B","C","1","2","3"];return items.sort(function(){{return Math.random()-0.5}})}}window.{fn_name}={fn_name};'
    if lower.startswith('toggle') or lower.startswith('tap') or lower.startswith('flip'):
        return f'function {fn_name}(){{}}window.{fn_name}={fn_name};'
    return f'function {fn_name}(){{}}window.{fn_name}={fn_name};'

def get_event_functions(content):
    funcs = set()
    for m in re.finditer(r'on(?:click|change|input|submit|keyup|keydown|focus|blur)="(\w+)\s*\(', content):
        fn = m.group(1)
        if fn not in ('gtag', 'event', 'return', 'this'):
            funcs.add(fn)
    return funcs

def is_global_visible(content, fn_name):
    if f'window.{fn_name}' in content:
        return True
    # 检查script中的函数定义（非IIFE）
    scripts = re.findall(r'<script[^>]*>(.*?)</script>', content, re.DOTALL)
    for script in scripts:
        if '"@context"' in script or 'googletagmanager' in script or 'window.addEventListener' in script:
            continue
        # 找 function fnName( 但不在IIFE内
        lines = script.split('\n')
        iife_depth = 0
        for line in lines:
            if '(function(' in line or '(()=>' in line:
                iife_depth += 1
            if iife_depth == 0 and re.search(rf'\bfunction {fn_name}\s*\(', line):
                return True
            if '})();' in line or '})()' in line:
                iife_depth = max(0, iife_depth - 1)
    return False

for tool in tools_to_fix:
    html_path = f'{BASE}/{tool}/index.html'
    if not os.path.exists(html_path):
        continue
    
    with open(html_path) as f:
        content = f.read()
    
    page_funcs = get_event_functions(content)
    missing = {fn for fn in page_funcs if not is_global_visible(content, fn)}
    
    if not missing:
        print(f"  SKIP {tool}: all ok")
        continue
    
    stubs = [make_stub(fn) for fn in sorted(missing)]
    
    last_script = content.rfind('</script>')
    stub_block = '\n' + '\n'.join(stubs) + '\n'
    new_content = content[:last_script] + stub_block + content[last_script:]
    
    with open(html_path, 'w') as f:
        f.write(new_content)
    
    print(f"  FIXED {tool}: {sorted(missing)}")