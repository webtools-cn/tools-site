#!/usr/bin/env python3
"""批量修复 no_copy_btn 残留问题"""
import re, os

tools = [
    'breath-holding-timer',
    'ketogenic-diet-calculator',
    'tabata-timer',
]

def fix_page(path, tool_name, lang):
    """给工具页添加复制按钮"""
    with open(path, 'r') as f:
        c = f.read()
    
    # 检查是否已有copyBtn
    if 'copyBtn' in c or 'copyResult' in c:
        print(f'  SKIP {path}: already has copy')
        return False
    
    # 找到 result-section 的结束 </div> (在info-section之前或有结束标签)
    # 策略：在 result-section 内添加复制按钮，放在h2后面或grid后面
    
    # 找到 resultSection 区域
    m = re.search(r'(<div class="result-section"[^>]*id="resultSection"[^>]*>)(.*?)(</div>\s*(?:<div class="info-section|</main>))', c, re.DOTALL)
    if not m:
        print(f'  SKIP {path}: no resultSection found')
        return False
    
    prefix = m.group(1)
    body = m.group(2)
    suffix = m.group(3)
    
    # 在 result-section 内的 h2 后面插入复制按钮
    copy_btn_html = '''\n  <div style="display:flex;gap:8px;align-items:center;margin-bottom:12px;">
    <button class="btn btn-secondary" id="copyBtn" style="font-size:.85rem;padding:6px 14px;">📋 复制结果</button>
  </div>\n'''
    
    # 在 h2 后面插入
    h2_match = re.search(r'(<h2>[^<]+</h2>)', body)
    if h2_match:
        new_body = body[:h2_match.end()] + copy_btn_html + body[h2_match.end():]
    else:
        new_body = copy_btn_html + body
    
    new_section = prefix + new_body + suffix
    c = c.replace(m.group(0), new_section)
    
    # 添加 toast 组件（如果还没有）
    if 'id="toast"' not in c:
        toast_html = '''\n<div id="toast" style="display:none;position:fixed;bottom:20px;left:50%;transform:translateX(-50%);background:#22d3ee;color:#0f172a;padding:10px 24px;border-radius:8px;font-size:.9rem;z-index:9999;transition:all .3s;"></div>\n'''
        c = c.replace('</body>', toast_html + '\n</body>')
    
    # 添加 copyResult 函数（如果还没有）
    if 'function copyResult' not in c:
        # 根据不同工具生成合适的复制内容
        if tool_name == 'ketogenic-diet-calculator':
            copy_fn = '''
function copyResult(){
  const lines=['=== 生酮饮食计算结果 ===',
    'TDEE: '+$('tdeeDisplay').textContent,
    '目标热量: '+$('targetCalDisplay').textContent,
    '脂肪: '+$('fatGrams').textContent+'g ('+$('fatCal').textContent+')',
    '蛋白质: '+$('proteinGrams').textContent+'g ('+$('proteinCal').textContent+')',
    '碳水: '+$('carbsGrams').textContent+'g ('+$('carbsCal').textContent+')'];
  navigator.clipboard.writeText(lines.join('\\n')).then(()=>showToast('✅ 已复制到剪贴板')).catch(()=>showToast('复制失败'))
}
function showToast(msg){const t=$('toast');t.textContent=msg;t.style.display='block';setTimeout(()=>t.style.display='none',2000)}
'''
        elif tool_name == 'breath-holding-timer':
            copy_fn = '''
function copyResult(){
  const lines=['=== 憋气计时器结果 ===',
    '最佳成绩: '+($('bestTime')?$('bestTime').textContent:'N/A')];
  navigator.clipboard.writeText(lines.join('\\n')).then(()=>showToast('✅ 已复制到剪贴板')).catch(()=>showToast('复制失败'))
}
function showToast(msg){const t=$('toast');t.textContent=msg;t.style.display='block';setTimeout(()=>t.style.display='none',2000)}
'''
        elif tool_name == 'tabata-timer':
            copy_fn = '''
function copyResult(){
  const lines=['=== Tabata计时器结果 ===',
    '已完成轮数: '+($('roundDisplay')?$('roundDisplay').textContent:'N/A'),
    '剩余时间: '+($('timeDisplay')?$('timeDisplay').textContent:'N/A')];
  navigator.clipboard.writeText(lines.join('\\n')).then(()=>showToast('✅ 已复制到剪贴板')).catch(()=>showToast('复制失败'))
}
function showToast(msg){const t=$('toast');t.textContent=msg;t.style.display='block';setTimeout(()=>t.style.display='none',2000)}
'''
        
        # 找到合适位置插入 copyResult 函数
        # 在现有的 showToast 后面或 script 标签的后面
        if 'function showToast' in c:
            c = c.replace('function showToast(msg){', copy_fn.strip() + '\n\nfunction showToast(msg){')
        else:
            # 在 </script> 之前插入
            c = c.replace('</script>', copy_fn + '\n</script>')
    
    # 绑定事件
    if "$('copyBtn')" not in c and "copyBtn" not in c.split('addEventListener')[1] if 'addEventListener' in c else True:
        event_binding = "\n$('copyBtn').addEventListener('click',copyResult);"
        c = c.replace('</script>', event_binding + '\n</script>')
    
    with open(path, 'w') as f:
        f.write(c)
    
    print(f'  FIXED {path}')
    return True

def $(id):
    return f"document.getElementById('{id}')"

total = 0
for tool in tools:
    for lang_dir, lang in [('', 'cn'), ('en/', 'en')]:
        path = f'{lang_dir}{tool}/index.html'
        if os.path.exists(path):
            if fix_page(path, tool, lang):
                total += 1

print(f'\n共修复 {total} 个页面')
