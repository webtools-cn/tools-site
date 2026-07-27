#!/usr/bin/env python3
"""批量修复残留问题：no_adsense, no_copy_btn, title_long"""
import re
import os
import sys

BASE = "/home/chison/tools-site"

ADSENSE_CODE = '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5998441792679372" crossorigin="anonymous"></script>'

COPY_BTN_JS = """
function copyResult(selector) {
  const el = document.querySelector(selector);
  if (!el) return;
  const text = el.textContent || el.value || el.innerText || '';
  navigator.clipboard.writeText(text.trim()).then(function() {
    showToast('已复制到剪贴板');
  }).catch(function() { showToast('复制失败'); });
}
function showToast(msg) {
  let t = document.querySelector('.toast');
  if (!t) { t = document.createElement('div'); t.className = 'toast'; document.body.appendChild(t); }
  t.textContent = msg; t.classList.add('show');
  setTimeout(function(){ t.classList.remove('show'); }, 2000);
}
"""

COPY_BTN_STYLE = """
.copy-btn{background:rgba(6,182,212,.15);color:#22d3ee;border:1px solid rgba(6,182,212,.3);padding:6px 12px;border-radius:6px;cursor:pointer;font-size:.8rem;transition:all .2s;white-space:nowrap}.copy-btn:hover{background:rgba(6,182,212,.25)}
.toast{position:fixed;bottom:20px;left:50%;transform:translateX(-50%);background:#1e293b;color:#22d3ee;padding:10px 24px;border-radius:8px;border:1px solid rgba(6,182,212,.3);font-size:.85rem;z-index:999;opacity:0;transition:opacity .3s;pointer-events:none}.toast.show{opacity:1}
"""

TOO_LONG_TITLES = {
    "bench-press-calculator": "卧推1RM计算器 - 最大重量测算 · 力量等级评估",
    "caffeine-half-life-calculator": "咖啡因半衰期计算器 - 摄入量与代谢追踪",
    "confidence-interval-calculator": "置信区间计算器 - 在线统计分析工具",
    "cost-per-click-calculator": "CPC点击成本计算器 - 在线广告预算分析",
    "monte-carlo-simulator": "蒙特卡洛模拟器 - 在线概率统计分析",
}

def add_adsense(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    if 'pagead2.googlesyndication.com' in content:
        return False
    
    # Insert after the last <link rel="alternate" or after hreflang
    marker = '<link rel="alternate" hreflang="x-default"'
    if marker in content:
        idx = content.index(marker)
        # find end of this line
        end = content.index('>', idx) + 1
        new_content = content[:end] + '\n' + ADSENSE_CODE + content[end:]
    else:
        # Fallback: insert before first <style>
        style_pos = content.index('<style>')
        new_content = content[:style_pos] + ADSENSE_CODE + '\n' + content[style_pos:]
    
    with open(filepath, 'w') as f:
        f.write(new_content)
    return True

def add_copy_btn(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    
    if 'function copyResult' in content and 'navigator.clipboard' in content:
        return False
    
    modified = False
    
    # Add CSS for copy button if missing
    if '.copy-btn{' not in content:
        # Insert before </style>
        style_end = content.index('</style>')
        # Insert after the last CSS rule before </style>
        insert_pos = style_end
        content = content[:insert_pos] + COPY_BTN_STYLE + content[insert_pos:]
        modified = True
    
    # Add JS functions if missing
    if 'function copyResult' not in content:
        # Insert before </body>
        body_end = content.index('</body>')
        content = content[:body_end] + '<script>' + COPY_BTN_JS + '</script>\n' + content[body_end:]
        modified = True
    
    if modified:
        with open(filepath, 'w') as f:
            f.write(content)
    return modified

def fix_title_length(filepath, tool_name):
    with open(filepath, 'r') as f:
        content = f.read()
    
    new_title = TOO_LONG_TITLES.get(tool_name)
    if not new_title:
        return False
    
    new_full = f'<title>免费在线{new_title} | 无需注册</title>'
    
    # Replace title
    old_title_match = re.search(r'<title>.*?</title>', content)
    if not old_title_match:
        return False
    
    old_title = old_title_match.group()
    if len(old_title) <= 60:
        return False
    
    content = content.replace(old_title, new_full)
    
    # Also fix og:title
    old_og = re.search(r'<meta property="og:title" content=".*?">', content)
    if old_og:
        og_new = f'<meta property="og:title" content="免费在线{new_title} | 无需注册">'
        content = content.replace(old_og.group(), og_new)
    
    with open(filepath, 'w') as f:
        f.write(content)
    return True

def main():
    no_adsense_files = [
        "cap-table-calculator", "epf-calculator", "esop-calculator",
        "fertility-calculator", "fixed-deposit-calculator", "retirement-nest-egg-calculator"
    ]
    
    no_copy_files = [
        "bench-press-calculator", "caffeine-half-life-calculator",
        "confidence-interval-calculator", "cost-per-click-calculator",
        "monte-carlo-simulator"
    ]
    
    fixed = []
    
    # Fix no_adsense
    for name in no_adsense_files:
        for suffix, lang in [("/index.html", "cn"), ("/en/index.html", "en")]:
            fp = os.path.join(BASE, name.replace(f"/en/", "/")) if lang == "cn" else os.path.join(BASE, "en", name, "index.html")
            if lang == "cn":
                fp = os.path.join(BASE, name, "index.html")
            else:
                fp = os.path.join(BASE, "en", name, "index.html")
            if add_adsense(fp):
                fixed.append(f"+adsense {lang}:{name}")
    
    # Fix no_copy_btn
    for name in no_copy_files:
        for suffix, lang in [("", "cn"), ("/en/", "en")]:
            if lang == "cn":
                fp = os.path.join(BASE, name, "index.html")
            else:
                fp = os.path.join(BASE, "en", name, "index.html")
            if add_copy_btn(fp):
                fixed.append(f"+copy_btn {lang}:{name}")
    
    # Fix title_long (only EN pages)
    for name in TOO_LONG_TITLES:
        fp = os.path.join(BASE, "en", name, "index.html")
        if fix_title_length(fp, name):
            fixed.append(f"+title_fix en:{name}")
    
    print(f"修复完成: {len(fixed)} 项")
    for f in fixed:
        print(f"  {f}")

if __name__ == '__main__':
    main()
