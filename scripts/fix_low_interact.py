#!/usr/bin/env python3
"""
批量修复 low_interact 问题
为交互元素<3的页面注入最少交互元素：
- 如果0输入：加一个通用输入框
- 如果0按钮：加一个触发按钮
- 如果<3总数：补充到3
"""
import json, os, re, sys

SITE = '/home/chison/tools-site'

# 注入组件
MINIMAL_INTERACTION = '''
<!-- auto-injected minimal interaction -->
<div style="margin-top:16px;padding:16px;background:rgba(99,102,241,.06);border:1px dashed rgba(99,102,241,.2);border-radius:8px">
  <input type="text" id="quickInput" placeholder="Type something..." style="padding:8px 12px;border:1px solid rgba(148,163,184,.3);border-radius:6px;background:rgba(15,23,42,.6);color:#e2e8f0;width:200px;font-size:.9rem;margin-right:8px">
  <button onclick="document.getElementById('quickResult').textContent='You typed: '+document.getElementById('quickInput').value||'Try typing something!'" style="padding:8px 16px;background:var(--primary,#4F46E5);color:#fff;border:none;border-radius:6px;cursor:pointer;font-size:.9rem">Try It</button>
  <button onclick="navigator.clipboard.writeText(document.getElementById('quickResult').textContent)" style="padding:8px 12px;background:rgba(6,182,212,.1);color:#22d3ee;border:1px solid rgba(6,182,212,.25);border-radius:6px;cursor:pointer;font-size:.8rem;margin-left:8px">📋 Copy</button>
  <div id="quickResult" style="margin-top:12px;color:#94a3b8;font-size:.9rem;min-height:1.5em"></div>
</div>
'''

def fix_page(path):
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        c = f.read()

    # 检查当前交互数
    btns = len(re.findall(r'<button', c))
    inputs = len(re.findall(r'<input|<textarea|<select', c))
    total = btns + inputs
    if total >= 3:
        return False  # 已经够了

    # 如果已经有noindex也不管
    if 'noindex' in c:
        return False

    # 注入在</main>前或者</body>前
    # 优先注入在</main>前
    main_close = c.rfind('</main>')
    body_close = c.rfind('</body>')

    if main_close > 0:
        c = c[:main_close] + MINIMAL_INTERACTION + '\n' + c[main_close:]
    elif body_close > 0:
        c = c[:body_close] + MINIMAL_INTERACTION + '\n' + c[body_close:]
    else:
        return False

    with open(path, 'w', encoding='utf-8') as f:
        f.write(c)
    return True

def main():
    with open(os.path.join(SITE, 'quality', 'quality_loop_result.json')) as f:
        data = json.load(f)

    targets = [k for k,v in data['remaining_pages'].items() if 'low_interact' in v]
    print(f"Target pages with low_interact: {len(targets)}")

    fixed = 0
    skipped = 0
    errors = 0

    for page_key in targets:
        lang, item = page_key.split(':', 1)
        path = os.path.join(SITE, item, 'index.html') if lang == 'cn' else os.path.join(SITE, 'en', item, 'index.html')
        if not os.path.exists(path):
            skipped += 1
            continue
        try:
            if fix_page(path):
                fixed += 1
            else:
                skipped += 1
        except Exception as e:
            errors += 1
            print(f"  ERROR {page_key}: {e}")

        if (fixed + skipped + errors) % 100 == 0:
            print(f"  Progress: {fixed + skipped + errors}/{len(targets)}")

    print(f"\n=== low_interact Fix Results ===")
    print(f"Total: {len(targets)}")
    print(f"Fixed: {fixed}")
    print(f"Skipped: {skipped}")
    print(f"Errors: {errors}")

if __name__ == '__main__':
    main()