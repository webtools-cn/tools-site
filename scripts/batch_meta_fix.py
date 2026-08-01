#!/usr/bin/env python3
"""
批量优化meta description v2：
- 清理emoji
- 避免"工具工具"
- 好描述做最小扩展
"""
import os, re, html, sys

ROOT = '/home/chison/tools-site'

def clean_emoji(text):
    """移除文本开头的emoji"""
    emoji_pattern = re.compile(
        "[\U0001F300-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF"
        "\U00002600-\U000027BF\U00002B50\U0001F600-\U0001F64F"
        "\U0001F680-\U0001F6FF\U0001F900-\U0001F9FF\U00002300-\U000023FF"
        "\U00002500-\U000025FF\U0000200D\U0000FE0F\U000020E3]", flags=re.UNICODE)
    # Only clean from start
    m = emoji_pattern.match(text.strip())
    if m:
        text = text[m.end():].strip()
    return text

def get_page_info(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        return None
    title_m = re.search(r'<title>(.+?)</title>', content)
    h1_m = re.search(r'<h1[^>]*>(.+?)</h1>', content)
    desc_m = re.search(r'<meta\s+name\s*=\s*[\"\']description[\"\']\s+content\s*=\s*[\"\'](.+?)[\"\']', content, flags=re.DOTALL | re.IGNORECASE)
    title = html.unescape(title_m.group(1).strip()) if title_m else ''
    h1 = html.unescape(h1_m.group(1).strip()) if h1_m else ''
    desc = html.unescape(desc_m.group(1).strip()) if desc_m else ''
    clean_title = re.sub(r'\s*[-|]\s*Free ToolBase\s*$', '', title).strip()
    clean_title = re.sub(r'\s*[-|]\s*已迁移\s*$', '', clean_title).strip()
    clean_h1 = clean_emoji(h1) if h1 else ''
    return {'content': content, 'title': title, 'clean_title': clean_title, 'h1': h1, 'clean_h1': clean_h1, 'desc': desc, 'desc_len': len(desc), 'filepath': filepath}

def generate_migrated_desc(tool_dir, target_tool):
    name = tool_dir.replace('-', ' ').title()
    target = target_tool.replace('-', ' ').title()
    return (f"{name}已升级迁移至新版{target}。新版提供更完善的{name}在线功能，支持更多格式选项和更好的用户体验，纯浏览器端本地处理保障数据安全。请访问新版{target}获得完整功能。无需注册下载，完全免费。")

def fix_page(filepath, new_desc):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        return False
    pattern = r'(<meta\s+name\s*=\s*[\"\']description[\"\']\s+content\s*=\s*[\"\'])(.+?)([\"\'])'
    new_content = re.sub(pattern, lambda m: m.group(1) + new_desc + m.group(3), content, count=1, flags=re.DOTALL | re.IGNORECASE)
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

def main():
    batch_size = 30
    start_idx = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    
    needs_fix = []
    for entry in sorted(os.listdir(ROOT)):
        if entry.startswith('.') or entry in ['en', 'tools', 'category', 'scripts', 'quality', '.gsc-data']:
            continue
        p = os.path.join(ROOT, entry, 'index.html')
        if not os.path.isfile(p):
            continue
        info = get_page_info(p)
        if not info or info['desc_len'] >= 100:
            continue
        is_mig = '已迁移' in info['title'] or '已迁移' in info['desc']
        target = None
        if is_mig:
            tm = re.search(r'已迁移至新版(.+?)[，,.\s]', info['desc'])
            if tm:
                target = tm.group(1).strip()
        needs_fix.append({'path': p, 'dir': entry, 'is_migrated': is_mig, 'target': target, 'desc': info['desc'], 'clean_h1': info['clean_h1'], 'desc_len': info['desc_len']})
    
    print(f"Total pages needing fix: {len(needs_fix)}")
    batch = needs_fix[start_idx:start_idx+batch_size]
    print(f"Processing batch at {start_idx}, size: {len(batch)}")
    
    fixed = 0
    for item in batch:
        if item['is_migrated'] and item['target']:
            new_desc = generate_migrated_desc(item['dir'], item['target'])
        else:
            # For normal pages with decent existing desc, just extend
            cur = item['desc'].rstrip('。.。')
            h1 = item['clean_h1']
            if len(cur) >= 70:
                # Good existing, extend minimally
                new_desc = cur + '。完全免费，无需注册下载，纯前端本地处理保障数据安全。'
            elif h1 and len(h1) > 3:
                new_desc = f"免费在线{h1}，快速高效完成{h1}相关任务。支持多种输入输出格式，操作简单直观，即开即用。纯浏览器端本地处理，数据绝不上传服务器，保障隐私安全。无需注册，完全免费。"
            else:
                new_desc = cur + '。完全免费，无需注册下载，纯前端本地处理。'
        
        dlen = len(new_desc)
        if dlen > 160:
            new_desc = new_desc[:157] + '...'
        elif dlen < 100:
            new_desc += '无需注册完全免费，纯前端本地处理数据安全保障隐私。'
        
        if fix_page(item['path'], new_desc):
            fixed += 1
            print(f"  OK [{item['desc_len']}->{len(new_desc)}] {item['dir']}")
        else:
            print(f"  FAIL {item['dir']}")
    
    print(f"\nFixed: {fixed}/{len(batch)} | Next: {start_idx+batch_size}")

if __name__ == '__main__':
    main()