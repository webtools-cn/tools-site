#!/usr/bin/env python3
"""给工具页添加复制按钮"""
import re, glob

FILES = [
    'fica-tax-calculator/index.html',
    'en/fica-tax-calculator/index.html',
    'freelancer-rate-calculator/index.html',
    'en/freelancer-rate-calculator/index.html',
    'hydration-tracker/index.html',
    'en/hydration-tracker/index.html',
]

for f in FILES:
    with open(f) as fh:
        content = fh.read()
    
    # 1. 在 btn-row 的 calculate 按钮后面加 copy 按钮
    # 中文版
    if '复制结果' not in content and 'Copy Results' not in content:
        # 找到按钮行，在清空/重置按钮前插入复制按钮
        if 'class="btn btn-primary"' in content:
            content = content.replace(
                '<button class="btn btn-outline" onclick="clearAll()"',
                '<button class="btn btn-outline" onclick="copyResults()">📋 复制结果</button>\n      <button class="btn btn-outline" onclick="clearAll()"'
            )
            content = content.replace(
                '<button class="btn btn-outline" onclick="resetAll()"',
                '<button class="btn btn-outline" onclick="copyResults()">📋 复制结果</button>\n      <button class="btn btn-outline" onclick="resetAll()"'
            )
    
    # 2. 对于英文版
    if 'Copy Results' not in content:
        content = content.replace(
            '<button class="btn btn-outline" onclick="clearAll()"',
            '<button class="btn btn-outline" onclick="copyResults()">📋 Copy Results</button>\n      <button class="btn btn-outline" onclick="clearAll()"'
        )
        content = content.replace(
            '<button class="btn btn-outline" onclick="resetAll()"',
            '<button class="btn btn-outline" onclick="copyResults()">📋 Copy Results</button>\n      <button class="btn btn-outline" onclick="resetAll()"'
        )
    
    # 3. 在 </script> 前添加 copyResults 函数
    copy_func = '''
function copyResults() {
  var res = document.getElementById('results');
  if (!res || res.style.display === 'none') { showToast('请先计算'); return; }
  var text = '';
  var items = res.querySelectorAll('.result-item');
  for (var i = 0; i < items.length; i++) {
    var label = items[i].querySelector('.label');
    var value = items[i].querySelector('.value');
    if (label && value) text += label.textContent + ': ' + value.textContent + '\\n';
  }
  if (!text) { text = res.textContent.trim(); }
  navigator.clipboard.writeText(text).then(function() { showToast('已复制'); }).catch(function() { showToast('复制失败'); });
}
'''
    if 'function copyResults' not in content:
        content = content.replace('</script>', copy_func + '\n</script>')
    
    with open(f, 'w') as fh:
        fh.write(content)
    
    has_copy = 'copyResults' in open(f).read()
    print(f'{f}: added_copy={has_copy}')

print('Done')