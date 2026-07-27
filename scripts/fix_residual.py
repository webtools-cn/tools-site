#!/usr/bin/env python3
"""批量修复残留问题：no_adsense, title_long, chinese_in_en, no_copy_btn"""
import re
import os

BASE = '/home/chison/tools-site'

# AdSense 代码块
ADSENSE_SCRIPT = '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5998441792679372" crossorigin="anonymous"></script>'
ADSENSE_CSS = '.ad-slot{margin:0 auto;text-align:center;max-width:960px}.ad-slot:not(:has(ins[frame])){display:none}.ad-slot:empty{display:none}.ad-slot ins{display:block}'
ADSENSE_HTML = '<div class="ad-slot"><ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-5998441792679372" data-ad-slot="1381158794" data-ad-format="auto" data-full-width-responsive="true"></ins></div>'

# COPY_BTN 模板
COPY_BTN_HTML = '<button class="copy-btn" onclick="copyResult()" title="复制结果">📋 复制</button>'
COPY_BTN_JS = '''
function copyResult() {
  const result = document.getElementById('result');
  if (!result || !result.textContent.trim()) return;
  navigator.clipboard.writeText(result.textContent.trim()).then(() => {
    const btn = document.querySelector('.copy-btn');
    if (btn) { btn.textContent = '✅ 已复制'; setTimeout(() => { btn.textContent = '📋 复制'; }, 1500); }
  }).catch(() => {});
}
'''

# 需要修复的页面
PAGES = {
    'ai-content-idea-generator': {'needs': ['no_adsense'], 'lang': 'cn'},
    'hdl-cholesterol-calculator': {'needs': ['no_adsense'], 'lang': 'cn'},
    'startup-name-generator': {'needs': ['no_adsense'], 'lang': 'cn'},
    'web-performance-checker': {'needs': ['no_adsense'], 'lang': 'cn'},
    'kpi-calculator': {'needs': ['no_adsense'], 'lang': 'cn'},
    'debt-snowflake-calculator': {'needs': ['no_copy_btn'], 'lang': 'cn'},
    'medicare-premium-calculator': {'needs': ['no_copy_btn'], 'lang': 'cn'},
    'en/ai-content-idea-generator': {'needs': ['no_adsense'], 'lang': 'en'},
    'en/hdl-cholesterol-calculator': {'needs': ['no_adsense'], 'lang': 'en'},
    'en/startup-name-generator': {'needs': ['no_adsense'], 'lang': 'en'},
    'en/web-performance-checker': {'needs': ['no_adsense'], 'lang': 'en'},
    'en/kpi-calculator': {'needs': ['no_adsense', 'chinese_in_en'], 'lang': 'en'},
    'en/medicare-premium-calculator': {'needs': ['no_copy_btn'], 'lang': 'en'},
    'en/xirr-calculator': {'needs': [], 'lang': 'en'},  # title_long only
}

# CN→EN翻译映射
CN_TO_EN = {
    '计算器': 'Calculator',
    '输入': 'Input',
    '和实际值': 'and Actual Value',
    '可选填入去年同期值做同比分析': 'Optionally enter last year values for YoY analysis',
    '点击计算按钮获取': 'Click Calculate to get',
    '同比变化': 'YoY Change',
    '查看': 'View',
    '和详细分析': 'and detailed analysis',
    '支持一键复制': 'Supports one-click copy',
    '中文': 'Chinese',
    '实际': 'Actual',
    '目标': 'Target',
    '同': 'Same',
    '本期': 'Current Period',
    '去年同期': 'Last Year Same Period',
}


def fix_no_adsense(path):
    """在页面中插入AdSense代码"""
    with open(path, 'r') as f:
        content = f.read()
    
    if 'adsbygoogle' in content:
        print(f"  [skip] {path} already has adsense")
        return False
    
    modified = False
    
    # 1. 在</head>前插入adsense script
    if ADSENSE_SCRIPT not in content:
        content = content.replace('</head>', f'{ADSENSE_SCRIPT}\n</head>')
        modified = True
        print(f"  [+] adsense script added")
    
    # 2. 在CSS末尾添加ad-slot样式
    if '.ad-slot' not in content:
        # 找到最后一个</style>前插入
        last_style = content.rfind('</style>')
        if last_style > 0:
            content = content[:last_style] + ADSENSE_CSS + '\n' + content[last_style:]
            print(f"  [+] adsense CSS added")
        modified = True
    
    # 3. 在<main>之后插入adsense slot
    if 'ad-slot' not in content:
        # 在第一个<main>标签后面插入
        main_match = re.search(r'<main[^>]*>', content)
        if main_match:
            insert_pos = main_match.end()
            content = content[:insert_pos] + '\n' + ADSENSE_HTML + '\n' + content[insert_pos:]
            print(f"  [+] adsense slot added")
        modified = True
    
    if modified:
        with open(path, 'w') as f:
            f.write(content)
    return modified


def fix_title_short(path):
    """缩短title到60字符以内"""
    with open(path, 'r') as f:
        content = f.read()
    
    title_match = re.search(r'<title>(.*?)</title>', content)
    if not title_match:
        return False
    
    old_title = title_match.group(1)
    # 去掉重复的部分（如 "KPI Calculator - KPI Calculator"）
    # 策略：保留描述性部分，去掉"Free Online"等前缀
    new_title = old_title
    # 常见模式修复
    if 'Free Online ' in new_title and len(new_title) > 60:
        new_title = new_title.replace('Free Online ', 'Free ')
    if len(new_title) > 65:
        # 去掉最后面的管道前缀
        new_title = re.sub(r'\s*\|\s*No Signup$', '', new_title)
        new_title += ' | No Signup'
    if len(new_title) > 65:
        new_title = new_title[:60]
    
    if new_title != old_title:
        content = content.replace(f'<title>{old_title}</title>', f'<title>{new_title}</title>')
        with open(path, 'w') as f:
            f.write(content)
        print(f"  [!] title: {old_title[:50]}... -> {new_title[:50]}...")
        return True
    return False


def fix_chinese_in_en(path):
    """替换EN页面中的中文字符"""
    with open(path, 'r') as f:
        content = f.read()
    
    # 找所有中文
    cn_chars = re.findall(r'[\u4e00-\u9fff]+', content)
    if not cn_chars:
        return False
    
    print(f"  [CN] found: {cn_chars[:10]}")
    modified = False
    for cn in sorted(set(cn_chars), key=len, reverse=True):
        if cn in CN_TO_EN:
            content = content.replace(cn, CN_TO_EN[cn])
            print(f"  [+] {cn} -> {CN_TO_EN[cn]}")
            modified = True
    
    if modified:
        with open(path, 'w') as f:
            f.write(content)
    return modified


def fix_no_copy_btn(path):
    """添加复制按钮"""
    with open(path, 'r') as f:
        content = f.read()
    
    if 'copy-btn' in content or 'copyResult' in content:
        print(f"  [skip] {path} already has copy button")
        return False
    
    modified = False
    
    # 在result/输出区域附近添加复制按钮
    # 查找输出区域常见的模式
    result_patterns = [
        r'(<div[^>]*id="result"[^>]*>)',
        r'(<div[^>]*class="[^"]*result[^"]*"[^>]*>)',
        r'(<div[^>]*id="output"[^>]*>)',
    ]
    
    for pattern in result_patterns:
        match = re.search(pattern, content)
        if match:
            insert_pos = match.end()
            content = content[:insert_pos] + '\n' + COPY_BTN_HTML + '\n' + content[insert_pos:]
            modified = True
            print(f"  [+] copy button added after result div")
            break
    
    if not modified:
        # 找不到result div，在</main>前插入
        main_end = content.rfind('</main>')
        if main_end > 0:
            content = content[:main_end] + COPY_BTN_HTML + '\n' + content[main_end:]
            modified = True
            print(f"  [+] copy button added before </main>")
    
    # 添加copy JS函数
    if 'function copyResult' not in content and modified:
        script_end = content.rfind('</script>')
        if script_end > 0:
            content = content[:script_end] + COPY_BTN_JS + '\n' + content[script_end:]
            print(f"  [+] copy JS function added")
    
    if modified:
        with open(path, 'w') as f:
            f.write(content)
    return modified


def main():
    fixed_count = 0
    for page, info in PAGES.items():
        path = os.path.join(BASE, page, 'index.html')
        if not os.path.exists(path):
            print(f"[MISS] {path}")
            continue
        
        print(f"\n=== {page} ===")
        page_fixed = False
        
        for need in info['needs']:
            if need == 'no_adsense':
                if fix_no_adsense(path):
                    page_fixed = True
            elif need == 'chinese_in_en':
                if fix_chinese_in_en(path):
                    page_fixed = True
            elif need == 'no_copy_btn':
                if fix_no_copy_btn(path):
                    page_fixed = True
        
        if page_fixed:
            fixed_count += 1
    
    print(f"\n\n总计修复: {fixed_count} 个页面")
    return fixed_count


if __name__ == '__main__':
    main()
