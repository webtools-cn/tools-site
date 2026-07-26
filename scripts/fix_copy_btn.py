#!/usr/bin/env python3
"""
智能修复 no_copy_btn 问题
策略：在页面JS末尾注入通用复制功能，为每个结果区域添加复制按钮
"""
import json, os, re, sys

SITE = '/home/chison/tools-site'

# 通用复制按钮CSS + JS（注入到页面末尾</body>前）
COPY_CSS = '''
.copy-btn{display:inline-flex;align-items:center;gap:4px;padding:6px 12px;background:rgba(6,182,212,.1);color:#22d3ee;border:1px solid rgba(6,182,212,.25);border-radius:6px;cursor:pointer;font-size:.8rem;transition:all .2s;margin-left:8px;vertical-align:top}
.copy-btn:hover{background:rgba(6,182,212,.25)}
.copy-btn.copied{background:rgba(34,197,94,.15);color:#22c55e;border-color:rgba(34,197,94,.3)}
'''

COPY_JS_TEMPLATE = '''
<script>
(function(){
  // 为所有result区域添加复制按钮
  var processed = new Set();
  function addCopyBtns(){
    var results = document.querySelectorAll('[id*="result"],[id*="Result"],[id*="output"],[id*="Output"],[class*="result"],[class*="output"]');
    results.forEach(function(el){
      if(processed.has(el)) return;
      if(el.querySelector('.copy-btn')) return;
      if(el.tagName==='INPUT'||el.tagName==='TEXTAREA'||el.tagName==='SELECT') return;
      if(el.children.length===0 && el.textContent.trim().length<5) return;
      var btn = document.createElement('button');
      btn.className = 'copy-btn';
      btn.innerHTML = '📋 复制';
      btn.title = '复制结果';
      btn.onclick = function(e){
        e.stopPropagation();
        var text = el.textContent || el.value || '';
        if(el.tagName==='INPUT'||el.tagName==='TEXTAREA') text = el.value;
        navigator.clipboard.writeText(text.trim()).then(function(){
          btn.innerHTML = '✅ 已复制';
          btn.classList.add('copied');
          setTimeout(function(){btn.innerHTML='📋 复制';btn.classList.remove('copied');},2000);
        }).catch(function(){
          var ta = document.createElement('textarea');
          ta.value = text.trim();
          ta.style.position='fixed';ta.style.opacity='0';
          document.body.appendChild(ta);
          ta.select();
          document.execCommand('copy');
          document.body.removeChild(ta);
          btn.innerHTML = '✅ 已复制';
          btn.classList.add('copied');
          setTimeout(function(){btn.innerHTML='📋 复制';btn.classList.remove('copied');},2000);
        });
      };
      el.appendChild(btn);
      processed.add(el);
    });
  }
  // Run initially
  addCopyBtns();
  // Re-run after button clicks (most tools update results on click)
  document.addEventListener('click', function(){setTimeout(addCopyBtns,100);});
  // Observe DOM changes
  if(window.MutationObserver){
    var obs = new MutationObserver(function(){addCopyBtns();});
    obs.observe(document.body,{childList:true,subtree:true});
  }
})();
</script>
'''

def fix_page(path):
    """为单个页面添加复制功能"""
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        c = f.read()
    
    # 已经有复制功能的跳过
    if 'navigator.clipboard' in c or 'document.execCommand(\'copy\')' in c:
        return False
    if '.copy-btn' in c:
        return False
    if '📋' in c and ('复制' in c or 'copy' in c.lower()):
        return False
    
    changed = False
    
    # 1. 添加复制按钮CSS (在最后一个</style>前)
    if '.copy-btn' not in c:
        last_style = c.rfind('</style>')
        if last_style > 0:
            c = c[:last_style] + COPY_CSS + '\n' + c[last_style:]
            changed = True
    
    # 2. 添加复制JS (在</body>前)
    if 'addCopyBtns' not in c:
        body_close = c.rfind('</body>')
        if body_close > 0:
            c = c[:body_close] + COPY_JS_TEMPLATE + '\n' + c[body_close:]
            changed = True
    
    if changed:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(c)
        return True
    return False


def main():
    # Load quality data
    with open(os.path.join(SITE, 'quality', 'quality_loop_result.json')) as f:
        data = json.load(f)
    
    pages = data['remaining_pages']
    
    # Filter only no_copy_btn pages
    target = [(k,v) for k,v in pages.items() if 'no_copy_btn' in v]
    print(f'Target pages with no_copy_btn: {len(target)}')
    
    fixed = 0
    skipped = 0
    errors = 0
    
    for idx, (page_key, issues) in enumerate(target):
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
        
        if (idx + 1) % 100 == 0:
            print(f'  Progress: {idx+1}/{len(target)}')
    
    print(f'\n=== no_copy_btn Fix Results ===')
    print(f'Total: {len(target)}')
    print(f'Fixed: {fixed}')
    print(f'Skipped (already fixed/no change): {skipped}')
    print(f'Errors: {errors}')

if __name__ == '__main__':
    main()