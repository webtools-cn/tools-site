#!/usr/bin/env python3
"""批量修复：添加AdSense代码 + 复制按钮"""
import re, os

SITE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(SITE)  # scripts -> root

ADSENSE_SCRIPT = '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5998441792679372" crossorigin="anonymous"></script>'
ADSENSE_AD_UNIT = '''<ins class="adsbygoogle"
     style="display:block"
     data-ad-client="ca-pub-5998441792679372"
     data-ad-slot="AUTO"
     data-ad-format="auto"
     data-full-width-responsive="true"></ins>
<script>(adsbygoogle = window.adsbygoogle || []).push({});</script>'''

def add_adsense(path):
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    original = content
    
    # Add AdSense script in head (before </head>)
    if 'pagead2.googlesyndication.com' not in content:
        content = content.replace('</head>', f'{ADSENSE_SCRIPT}\n</head>')
    
    # Add AdSense ad unit before footer
    if 'adsbygoogle' not in content or 'data-ad-slot' not in content:
        # Insert before <footer or before </body>
        if '<footer' in content:
            content = content.replace('<footer', f'{ADSENSE_AD_UNIT}\n<footer', 1)
        else:
            content = content.replace('</body>', f'{ADSENSE_AD_UNIT}\n</body>')
    
    if content != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def add_copy_btn(path):
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    original = content
    
    # Check if already has copy button
    if 'copyToClipboard' in content or 'navigator.clipboard' in content:
        return False
    
    # Find result panel and add copy button
    # Strategy: find the result panel's btn-group and add a copy button
    has_result_panel = 'result-panel' in content or 'id="result"' in content or 'class="result"' in content
    
    if not has_result_panel:
        return False
    
    # Add copy function JS before </script> that's inside <body>
    copy_js = '''
function copyResults() {
  const resultPanel = document.getElementById('result-panel');
  if (!resultPanel) return;
  const text = resultPanel.innerText.trim();
  if (!text) return;
  navigator.clipboard.writeText(text).then(() => {
    showToast('Copied!');
  }).catch(() => {
    showToast('Copy failed');
  });
}
function showToast(msg) {
  let t = document.getElementById('toast');
  if (!t) { t = document.createElement('div'); t.id = 'toast'; t.style.cssText = 'position:fixed;bottom:20px;left:50%;transform:translateX(-50%);background:#333;color:#fff;padding:8px 20px;border-radius:20px;font-size:.85rem;z-index:9999;transition:opacity .3s'; document.body.appendChild(t); }
  t.textContent = msg; t.style.opacity = '1';
  clearTimeout(t._tid); t._tid = setTimeout(() => { t.style.opacity = '0'; }, 2000);
}'''
    
    # Find the last </script> tag and add copy function before it
    # Find result panel's button group
    btn_group_pattern = r'(<div class="btn-group"[^>]*>.*?</div>)'
    btn_match = re.search(btn_group_pattern, content, re.DOTALL)
    
    if btn_match:
        # Check if near result-panel
        result_pos = content.find('result-panel')
        if result_pos > 0 and abs(result_pos - btn_match.start()) < 500:
            # Add copy button to btn-group
            old_btn_group = btn_match.group(1)
            new_btn_group = old_btn_group.rstrip('</div>') + '<button class="btn btn-success" onclick="copyResults()">📋 Copy</button></div>'
            content = content.replace(old_btn_group, new_btn_group)
    
    # Add toast CSS + copy JS
    if 'function copyResults' not in content:
        # Add before last </script>
        last_script = content.rfind('</script>')
        if last_script > 0:
            content = content[:last_script] + copy_js + '\n' + content[last_script:]
    
    if content != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    files = [
        'a1c-calculator/index.html',
        'calorie-deficit-calculator/index.html',
        'capital-gains-tax-calculator/index.html',
        'cholesterol-ratio-calculator/index.html',
        'self-employment-tax-calculator/index.html',
        'en/a1c-calculator/index.html',
        'en/calorie-deficit-calculator/index.html',
        'en/capital-gains-tax-calculator/index.html',
        'en/cholesterol-ratio-calculator/index.html',
        'en/self-employment-tax-calculator/index.html',
    ]
    
    adsense_fixed = 0
    copy_fixed = 0
    
    for f in files:
        path = os.path.join(SITE, f)
        if not os.path.exists(path):
            print(f"  SKIP: {f} not found")
            continue
        
        if add_adsense(path):
            adsense_fixed += 1
            print(f"  ✅ AdSense: {f}")
        
        if add_copy_btn(path):
            copy_fixed += 1
            print(f"  ✅ CopyBtn: {f}")
    
    print(f"\nAdSense fixed: {adsense_fixed}")
    print(f"CopyBtn fixed: {copy_fixed}")

if __name__ == '__main__':
    main()