#!/usr/bin/env python3
"""修复 no_related_tools: 为页面添加相关工具推荐section"""
import os, re, json

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 手动映射相关工具
RELATED_MAP = {
    '1rm-calculator': ['bmi-calculator', 'pace-calculator', 'metabolism-calculator'],
    'ebay-fee-calculator': ['paypal-fee-calculator', 'profit-margin-calculator', 'markup-calculator'],
    'hiking-time': ['pace-calculator', 'watch-size-calculator', 'sleep-cycles-calculator'],
    'metabolism-calculator': ['calorie-tracker', 'bmi-calculator', 'pace-calculator'],
    'paypal-fee-calculator': ['ebay-fee-calculator', 'profit-margin-calculator', 'commission-calculator'],
    'paraphraser': ['word-counter', 'text-analyzer', 'smart-quotes-converter'],
}

def tool_display_name(tool):
    """生成友好的显示名"""
    name = tool.replace('-', ' ').title()
    return name

def add_related_tools(path, tool_name):
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    if 'related-tools' in content or 'Related Tools' in content:
        return None
    
    related = RELATED_MAP.get(tool_name, [])
    if not related:
        return None
    
    section = '\n  <section class="card" style="margin-top:24px">\n    <h2 style="font-size:20px;margin-bottom:16px">Related Tools</h2>\n    <div style="display:flex;flex-wrap:wrap;gap:10px">\n'
    for t in related:
        section += f'      <a href="../{t}/index.html" style="display:inline-block;padding:8px 16px;background:var(--bg);border:1px solid var(--border);border-radius:20px;text-decoration:none;color:var(--text);font-size:14px;transition:all .2s">{tool_display_name(t)}</a>\n'
    section += '    </div>\n  </section>\n'
    
    # Insert before </main>
    content = content.replace('</main>', section + '</main>', 1)
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    return f'+related-tools ({len(related)} tools)'

def main():
    for key, issues in [('cn:1rm-calculator', ['js_alert','no_related_tools']),
                         ('cn:ebay-fee-calculator', ['js_alert','no_related_tools']),
                         ('cn:hiking-time', ['js_alert','no_related_tools']),
                         ('cn:metabolism-calculator', ['js_alert','no_related_tools']),
                         ('cn:paypal-fee-calculator', ['js_alert','no_related_tools']),
                         ('en:1rm-calculator', ['chinese_in_en','js_alert','no_related_tools']),
                         ('en:ebay-fee-calculator', ['chinese_in_en','js_alert','no_related_tools']),
                         ('en:hiking-time', ['js_alert','no_related_tools']),
                         ('en:metabolism-calculator', ['js_alert','no_related_tools']),
                         ('en:paypal-fee-calculator', ['chinese_in_en','js_alert','no_related_tools']),
                         ('en:paraphraser', ['no_related_tools'])]:
        lang, tool = key.split(':', 1)
        if lang == 'cn':
            path = os.path.join(SITE, tool, 'index.html')
        else:
            path = os.path.join(SITE, 'en', tool, 'index.html')
        
        if not os.path.exists(path):
            continue
        
        result = add_related_tools(path, tool)
        if result:
            print(f'✅ {key}: {result}')

if __name__ == '__main__':
    main()
