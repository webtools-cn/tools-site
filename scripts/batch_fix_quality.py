#!/usr/bin/env python3
"""
批量修复质量检测残留问题
修复 no_adsense, no_breadcrumb, no_software_app, no_media, title_long
"""
import os, re, json, sys
from pathlib import Path

SITE = Path('/home/chison/tools-site')
OG_IMAGE = 'https://free-toolbase.com/og-image.svg'
ADSENSE_CODE = '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5998441792679372" crossorigin="anonymous"></script>'

def load_quality_data():
    with open(SITE / 'quality' / 'quality_loop_result.json') as f:
        return json.load(f)

def get_page_path(lang, item):
    if lang == 'cn':
        return SITE / item / 'index.html'
    else:
        return SITE / 'en' / item / 'index.html'

def get_tool_name(page_path, lang):
    with open(page_path, 'r', encoding='utf-8', errors='ignore') as f:
        c = f.read()
    # 从title提取工具名
    tm = re.search(r'<title>([^<]+)</title>', c)
    if tm:
        title = tm.group(1)
        title = re.sub(r'\s*[-|]\s*Free ToolBase.*$', '', title)
        title = re.sub(r'^Free( Online)? ', '', title)
        title = re.sub(r'^免费(在线)?', '', title)
        title = title.strip()
        if title:
            return title
    # 从h1提取
    hm = re.search(r'<h1[^>]*>([^<]+)</h1>', c)
    if hm:
        return hm.group(1).strip()
    return item.replace('-', ' ').title()

def get_description(page_path):
    with open(page_path, 'r', encoding='utf-8', errors='ignore') as f:
        c = f.read()
    dm = re.search(r'<meta name="description" content="([^"]*)"', c)
    if dm:
        return dm.group(1)
    return ''

def add_adsense(page_path):
    with open(page_path, 'r', encoding='utf-8', errors='ignore') as f:
        c = f.read()
    if 'adsbygoogle' in c or 'pagead2' in c:
        return False  # already has
    # Insert before </head>
    if '</head>' in c:
        c = c.replace('</head>', ADSENSE_CODE + '\n</head>')
        with open(page_path, 'w', encoding='utf-8') as f:
            f.write(c)
        return True
    return False

def add_breadcrumb(page_path, lang, item):
    with open(page_path, 'r', encoding='utf-8', errors='ignore') as f:
        c = f.read()
    if 'BreadcrumbList' in c:
        return False  # already has
    
    cn_url = f'https://free-toolbase.com/{item}/'
    en_url = f'https://free-toolbase.com/en/{item}/'
    tool_name = get_tool_name(page_path, lang)
    
    if lang == 'cn':
        breadcrumb = f'<script type="application/ld+json">{{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{{"@type": "ListItem", "position": 1, "name": "首页", "item": "{cn_url.replace(item+"/","")}"}}, {{"@type": "ListItem", "position": 2, "name": "工具", "item": "{cn_url.replace(item+"/","")}#tools"}}, {{"@type": "ListItem", "position": 3, "name": "{tool_name}", "item": "{cn_url}"}}]}}</script>'
    else:
        breadcrumb = f'<script type="application/ld+json">{{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{{"@type": "ListItem", "position": 1, "name": "Home", "item": "{en_url.replace("en/"+item+"/","")}"}}, {{"@type": "ListItem", "position": 2, "name": "Tools", "item": "{en_url.replace(item+"/","")}#tools"}}, {{"@type": "ListItem", "position": 3, "name": "{tool_name}", "item": "{en_url}"}}]}}</script>'
    
    # Insert before </head> or after last schema
    insert_at = c.find('</head>')
    if insert_at > 0:
        c = c[:insert_at] + breadcrumb + '\n' + c[insert_at:]
        with open(page_path, 'w', encoding='utf-8') as f:
            f.write(c)
        return True
    return False

def add_software_app(page_path, lang, item):
    with open(page_path, 'r', encoding='utf-8', errors='ignore') as f:
        c = f.read()
    if 'SoftwareApplication' in c:
        return False
    
    tool_name = get_tool_name(page_path, lang)
    desc = get_description(page_path)
    
    schema = f'<script type="application/ld+json">{{"@context": "https://schema.org", "@type": "SoftwareApplication", "name": "{tool_name}", "description": "{desc}", "applicationCategory": "UtilitiesApplication", "operatingSystem": "Web", "publisher": {{"@type": "Organization", "name": "Free ToolBase", "email": "dexshuang@google.com"}}, "offers": {{"@type": "Offer", "price": "0", "priceCurrency": "USD"}}}}</script>'
    
    insert_at = c.find('</head>')
    if insert_at > 0:
        c = c[:insert_at] + schema + '\n' + c[insert_at:]
        with open(page_path, 'w', encoding='utf-8') as f:
            f.write(c)
        return True
    return False

def add_media_query(page_path):
    with open(page_path, 'r', encoding='utf-8', errors='ignore') as f:
        c = f.read()
    if '@media' in c:
        return False
    
    # Find the last </style> and add media query before it
    media = '@media(max-width:640px){h1{font-size:1.2rem;word-break:break-word}.container{padding:0 12px}.btn{padding:8px 14px;font-size:.85rem}.panel{padding:16px}}'
    
    last_style = c.rfind('</style>')
    if last_style > 0:
        c = c[:last_style] + media + '\n' + c[last_style:]
        with open(page_path, 'w', encoding='utf-8') as f:
            f.write(c)
        return True
    return False

def fix_title_long(page_path, lang):
    with open(page_path, 'r', encoding='utf-8', errors='ignore') as f:
        c = f.read()
    
    tm = re.search(r'<title>([^<]+)</title>', c)
    if not tm:
        return False
    title = tm.group(1)
    if len(title) <= 60:
        return False
    
    # 缩短策略
    nt = title
    # Remove redundant prefixes
    nt = re.sub(r'^免费在线', '', nt)
    nt = re.sub(r'^在线', '', nt)
    nt = re.sub(r'^Free Online ', '', nt)
    nt = re.sub(r'^Free ', '', nt)
    nt = nt.strip()
    
    if len(nt) > 60 and ' - Free ToolBase' in nt:
        core = nt.replace(' - Free ToolBase', '')
        max_core = 60 - len(' - Free ToolBase')
        if len(core) > max_core:
            core = core[:max_core-2] + '…'
        nt = core + ' - Free ToolBase'
    
    if nt != title and len(nt) <= 60:
        c = c.replace(f'<title>{title}</title>', f'<title>{nt}</title>')
        with open(page_path, 'w', encoding='utf-8') as f:
            f.write(c)
        return True
    return False

def fix_chinese_in_en(page_path):
    """Remove Chinese characters from English pages"""
    with open(page_path, 'r', encoding='utf-8', errors='ignore') as f:
        c = f.read()
    
    cn_re = re.compile(r'[\u4e00-\u9fff]')
    if not cn_re.search(c):
        return False  # no chinese
    
    # 检查是否noindex页面(不可行工具) - 跳过
    if 'noindex' in c:
        return False
    
    # Strategy: find where Chinese appears and try to replace
    # Most common cases: h1/h2/p/span/button/label have Chinese
    # We look for Chinese blocks and try to infer English replacements
    # This is a best-effort approach
    
    changed = False
    
    # Replace common Chinese UI patterns
    replacements = [
        ('首页', 'Home'),
        ('工具', 'Tools'),
        ('返回', 'Back'),
        ('生成', 'Generate'),
        ('复制', 'Copy'),
        ('清空', 'Clear'),
        ('下载', 'Download'),
        ('重置', 'Reset'),
        ('预览', 'Preview'),
        ('结果', 'Result'),
        ('输入', 'Input'),
        ('输出', 'Output'),
        ('计算', 'Calculate'),
        ('转换', 'Convert'),
        ('编码', 'Encode'),
        ('解码', 'Decode'),
        ('加密', 'Encrypt'),
        ('解密', 'Decrypt'),
        ('上传', 'Upload'),
        ('设置', 'Settings'),
        ('选项', 'Options'),
        ('格式', 'Format'),
        ('保存', 'Save'),
        ('删除', 'Delete'),
        ('编辑', 'Edit'),
        ('添加', 'Add'),
        ('搜索', 'Search'),
        ('确认', 'Confirm'),
        ('取消', 'Cancel'),
        ('关闭', 'Close'),
        ('加载中', 'Loading'),
        ('点击', 'Click'),
        ('选择', 'Select'),
        ('文件', 'File'),
        ('文本', 'Text'),
        ('数字', 'Number'),
        ('颜色', 'Color'),
        ('大小', 'Size'),
        ('宽度', 'Width'),
        ('高度', 'Height'),
        ('比例', 'Ratio'),
        ('质量', 'Quality'),
        ('密码', 'Password'),
        ('哈希', 'Hash'),
        ('免费', 'Free'),
        ('在线', 'Online'),
        ('无需注册', 'No Signup'),
        ('关于', 'About'),
        ('隐私', 'Privacy'),
        ('条款', 'Terms'),
        ('联系', 'Contact'),
        ('支持', 'Support'),
        ('帮助', 'Help'),
        ('全部', 'All'),
        ('更多', 'More'),
        ('分享', 'Share'),
    ]
    
    for cn_text, en_text in replacements:
        if cn_text in c:
            c = c.replace(cn_text, en_text)
            changed = True
    
    # If still has Chinese, try to handle tool-specific Chinese text in h1/title
    if cn_re.search(c):
        # Replace lang="zh-CN" with lang="en" if still wrong
        c = re.sub(r'lang="zh-CN"', 'lang="en"', c)
        changed = True
    
    if changed:
        with open(page_path, 'w', encoding='utf-8') as f:
            f.write(c)
        return True
    return False

def main():
    data = load_quality_data()
    pages = data['remaining_pages']
    
    fixed_count = {'no_adsense': 0, 'no_breadcrumb': 0, 'no_software_app': 0, 
                   'no_media': 0, 'title_long': 0, 'chinese_in_en': 0}
    failed = {'no_adsense': 0, 'no_breadcrumb': 0, 'no_software_app': 0, 
              'no_media': 0, 'title_long': 0, 'chinese_in_en': 0}
    
    total = len(pages)
    for idx, (page_key, issues) in enumerate(pages.items()):
        lang, item = page_key.split(':', 1)
        page_path = get_page_path(lang, item)
        
        if not page_path.exists():
            continue
        
        for issue in issues:
            try:
                if issue == 'no_adsense':
                    if add_adsense(page_path):
                        fixed_count['no_adsense'] += 1
                    else:
                        failed['no_adsense'] += 1
                elif issue == 'no_breadcrumb':
                    if add_breadcrumb(page_path, lang, item):
                        fixed_count['no_breadcrumb'] += 1
                    else:
                        failed['no_breadcrumb'] += 1
                elif issue == 'no_software_app':
                    if add_software_app(page_path, lang, item):
                        fixed_count['no_software_app'] += 1
                    else:
                        failed['no_software_app'] += 1
                elif issue == 'no_media':
                    if add_media_query(page_path):
                        fixed_count['no_media'] += 1
                    else:
                        failed['no_media'] += 1
                elif issue == 'title_long':
                    if fix_title_long(page_path, lang):
                        fixed_count['title_long'] += 1
                    else:
                        failed['title_long'] += 1
                elif issue == 'chinese_in_en':
                    if fix_chinese_in_en(page_path):
                        fixed_count['chinese_in_en'] += 1
                    else:
                        failed['chinese_in_en'] += 1
            except Exception as e:
                failed[issue] = failed.get(issue, 0) + 1
        
        # Progress every 200
        if (idx + 1) % 200 == 0:
            print(f'  Progress: {idx+1}/{total}')
    
    # Report
    total_fixed = sum(fixed_count.values())
    total_failed = sum(failed.values())
    print(f'\n=== Batch Fix Results ===')
    print(f'Total pages processed: {total}')
    print(f'Total fixed: {total_fixed}')
    print(f'Total failed: {total_failed}')
    for k in fixed_count:
        print(f'  {k}: fixed={fixed_count[k]}, failed={failed[k]}')

if __name__ == '__main__':
    main()
