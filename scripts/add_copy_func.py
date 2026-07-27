#!/usr/bin/env python3
import re, os

FILES = [
    ('/home/chison/tools-site/raise-calculator/index.html', '✅ 已复制!'),
    ('/home/chison/tools-site/travel-budget-calculator/index.html', '✅ 已复制!'),
    ('/home/chison/tools-site/en/raise-calculator/index.html', '✅ Copied!'),
    ('/home/chison/tools-site/en/travel-budget-calculator/index.html', '✅ Copied!'),
]

COPY_JS_TEMPLATE = '''
function copyResult(){{
  var el=document.getElementById('resultSection');
  if(!el) return;
  var txt=el.innerText||el.textContent;
  navigator.clipboard.writeText(txt).then(function(){{
    showToast('{toast}');
  }}).catch(function(){{}});
}}
'''

for path, toast in FILES:
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        c = f.read()
    
    if 'function copyResult' in c:
        print(f"[SKIP] {path}: already has copyResult")
        continue
    
    copy_js = COPY_JS_TEMPLATE.format(toast=toast)
    
    # 在最后一个</script>前插入（在</body>之前的）
    last_script = c.rfind('</script>')
    if last_script > 0:
        c = c[:last_script] + copy_js + '\n' + c[last_script:]
    else:
        c = c.replace('</body>', '<script>' + copy_js + '\n</script>\n</body>')
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(c)
    print(f"[FIXED] {path}")

print("Done")
