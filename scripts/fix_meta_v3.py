#!/usr/bin/env python3
"""修复meta description v3 - 精准提取工具名+功能描述"""
import os, re, glob

def extract_info(filepath):
    """从页面提取中文工具名和功能"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read(15000)
    
    # --- 提取工具名 ---
    # 优先从h1提取（最准确）
    h1_match = re.search(r'<h1[^>]*>(.+?)</h1>', content)
    h1 = re.sub(r'<[^>]+>', '', h1_match.group(1)).strip() if h1_match else ''
    # 去emoji
    h1_clean = re.sub(r'[\U0001F300-\U0001F9FF\u2600-\u27BF\u2B50\u2700-\u27BF\uFE0F\u200D\ufe0f️]', '', h1).strip()
    
    # 从title备选
    title_match = re.search(r'<title>(.+?)(?:\s*[-|]\s*Free ToolBase)', content)
    title = title_match.group(1).strip() if title_match else ''
    title = re.sub(r'^(免费在线|在线|免费)\s*', '', title)
    title_clean = re.sub(r'[\U0001F300-\U0001F9FF\u2600-\u27BF\u2B50\u2700-\u27BF\uFE0F\u200D\ufe0f️]', '', title).strip()
    
    cn_name = h1_clean if len(h1_clean) > 2 else title_clean
    
    # --- 提取功能特征 ---
    features = []
    
    # 方法1：找描述性<p>（跳过面包屑、页码、JSON）
    paragraphs = re.findall(r'<p[^>]*>(.+?)</p>', content)
    for p in paragraphs:
        clean = re.sub(r'<[^>]+>', '', p).strip()
        clean = re.sub(r'\s*\|\s*无需注册[^。]*', '', clean)
        # 跳过面包屑、emoji开头的装饰段落
        if any(x in clean for x in ['首页', '›', '&rsaquo;', '&raquo;']):
            continue
        if len(clean) < 15 or len(clean) > 120:
            continue
        if clean.startswith('{') or clean.startswith('function'):
            continue
        features.append(clean)
        if len(features) >= 3:
            break
    
    # 方法2：从h2提取
    if not features:
        h2_matches = re.findall(r'<h2[^>]*>(.+?)</h2>', content)
        for h2 in h2_matches[:3]:
            clean = re.sub(r'<[^>]+>', '', h2).strip()
            if clean and len(clean) < 40 and not any(x in clean for x in ['首页', 'FAQ']):
                features.append(clean)
    
    return cn_name, features

def gen_desc(cn_name, features):
    """生成140-160字符的中文description"""
    if not cn_name or len(cn_name) < 1:
        cn_name = '工具'
    
    if features:
        # 拼接功能
        feature_text = '、'.join(features[:2])
        # 去除冗余前缀
        feature_text = re.sub(r'^免费在线'+cn_name+r'工具[，,]\s*', '', feature_text)
        if len(feature_text) < 10:
            feature_text = features[0] if features[0] else ''
        
        desc = f"免费在线{cn_name}工具，{feature_text}。纯前端本地处理，数据不上传服务器，无需注册即可免费使用。"
    else:
        desc = f"免费在线{cn_name}工具，快速便捷的{cn_name}解决方案，打开浏览器即可使用。纯前端本地处理，保障数据安全，无需注册完全免费。"
    
    # 确保140-160
    if len(desc) < 120:
        desc = f"免费在线{cn_name}工具，简单高效的{cn_name}在线解决方案。纯前端本地处理，数据不上传服务器，无需注册即可免费使用，打开浏览器随时访问。"
    
    # 截断到160
    if len(desc) > 160:
        last_period = desc[:160].rfind('。')
        if last_period > 120:
            desc = desc[:last_period+1]
        else:
            desc = desc[:157].rstrip() + '...'
    
    return desc.strip()

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    old_match = re.search(r'(<meta\s+name=[\"\']description[\"\']\s+content=[\"\'])(.+?)([\"\'])', content, re.IGNORECASE)
    if not old_match:
        return False, "no meta"
    
    old_desc = old_match.group(2)
    old_len = len(old_desc)
    
    if '已迁移' in old_desc or '迁移至' in old_desc:
        return False, "migrated"
    
    needs_fix = ('...' in old_desc and old_len < 100) or (old_len < 100 and '...' not in old_desc)
    if not needs_fix and old_len >= 100:
        return False, "ok"
    
    cn_name, features = extract_info(filepath)
    new_desc = gen_desc(cn_name, features)
    
    if new_desc == old_desc:
        return False, "same"
    
    new_meta = f'{old_match.group(1)}{new_desc}{old_match.group(3)}'
    content = content[:old_match.start()] + new_meta + content[old_match.end():]
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True, f"[{old_len}\u2192{len(new_desc)}] {new_desc[:60]}..."

def main():
    base_dir = '/home/chison/tools-site'
    count = 0
    
    for f in sorted(glob.glob(f'{base_dir}/*/index.html')):
        if '/en/' in f or '/scripts/' in f:
            continue
        success, msg = fix_file(f)
        if success:
            count += 1
            if count <= 15 or count % 50 == 0:
                print(f'OK {os.path.basename(os.path.dirname(f)):40s} {msg}')
    
    print(f'\nTotal fixed: {count}')

if __name__ == '__main__':
    main()
