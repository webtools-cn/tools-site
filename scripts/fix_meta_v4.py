#!/usr/bin/env python3
"""修复meta description v4 - 精准中文工具名+去重功能描述"""
import os, re, glob

def clean_name(name):
    """彻底清除emoji和特殊符号"""
    # 移除emoji (包括组合emoji)
    name = re.sub(r'[\U0001F300-\U0001F9FF\u2600-\u27BF\u2B50\u2700-\u27BF\uFE0F\u200D\ufe0f️]', '', name)
    # 移除特殊符号但保留中文标点
    name = re.sub(r'[★☆✦✧♡♥♦♣♠◉◎◈◆◇▪▫●○]', '', name)
    # 清理多余空格和标点
    name = re.sub(r'\s+', ' ', name).strip()
    name = re.sub(r'^[·•·,，、\s]+', '', name)
    return name

def extract_info(filepath):
    """提取中文工具名+去重功能"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read(15000)
    
    # --- 工具名 ---
    h1_match = re.search(r'<h1[^>]*>(.+?)</h1>', content)
    h1 = re.sub(r'<[^>]+>', '', h1_match.group(1)).strip() if h1_match else ''
    h1_clean = clean_name(h1)
    
    title_match = re.search(r'<title>(.+?)(?:\s*[-|]\s*Free ToolBase)', content)
    title = title_match.group(1).strip() if title_match else ''
    title = re.sub(r'^(免费在线|在线|免费)\s*', '', title)
    title_clean = clean_name(title)
    
    cn_name = h1_clean if len(h1_clean) > 2 and len(h1_clean) < 30 else title_clean
    if not cn_name or len(cn_name) < 2:
        # fallback: 用目录名
        cn_name = os.path.basename(os.path.dirname(filepath)).replace('-', ' ')
    
    # --- 功能特征（去重）---
    features = []
    seen = set()
    
    paragraphs = re.findall(r'<p[^>]*>(.+?)</p>', content)
    for p in paragraphs:
        clean = re.sub(r'<[^>]+>', '', p).strip()
        # 跳过噪音
        if any(x in clean for x in ['首页', '›', '&rsaquo;', '&raquo;']):
            continue
        clean = re.sub(r'\s*\|\s*无需注册[^。]*', '', clean)
        clean = re.sub(r'\s*🔒.*', '', clean)
        if len(clean) < 15 or len(clean) > 100:
            continue
        if clean.startswith('{') or clean.startswith('function'):
            continue
        
        # 去重（前20字符作为指纹）
        fp = clean[:20]
        if fp in seen:
            continue
        seen.add(fp)
        features.append(clean)
        if len(features) >= 2:
            break
    
    return cn_name, features

def gen_desc(cn_name, features):
    """生成140-160字符精准description"""
    if not cn_name:
        cn_name = '工具'
    
    if features and len(features) >= 1:
        # 取第一个好的feature作为核心描述
        main_feat = features[0]
        # 截断feature到合适长度，留出空间给固定文案
        max_feat_len = 160 - len(f"免费在线{cn_name}工具，。纯前端本地处理，数据不上传服务器，无需注册即可免费使用。")
        if len(main_feat) > max_feat_len:
            # 在句号处截断
            cut = main_feat[:max_feat_len].rfind('。')
            if cut > 30:
                main_feat = main_feat[:cut+1]
            else:
                main_feat = main_feat[:max_feat_len-3] + '...'
        
        desc = f"免费在线{cn_name}工具，{main_feat}。纯前端本地处理，数据不上传服务器，无需注册即可免费使用。"
    else:
        desc = f"免费在线{cn_name}工具，简单高效的{cn_name}解决方案，打开浏览器即可使用。纯前端本地处理，保障数据安全，无需注册完全免费。"
    
    # 最后调整长度
    if len(desc) > 160:
        last_period = desc[:160].rfind('。')
        if last_period > 120:
            desc = desc[:last_period+1]
        else:
            desc = desc[:157].rstrip() + '...'
    
    if len(desc) < 120:
        desc = f"免费在线{cn_name}工具，简单高效的{cn_name}在线解决方案。纯前端本地处理，数据不上传服务器，无需注册即可免费使用，打开浏览器随时访问。"
    
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
    
    return True, f"[{old_len}→{len(new_desc)}] {new_desc[:80]}..."

def main():
    base_dir = '/home/chison/tools-site'
    count = 0
    skipped_migrated = 0
    
    for f in sorted(glob.glob(f'{base_dir}/*/index.html')):
        if '/en/' in f or '/scripts/' in f:
            continue
        success, msg = fix_file(f)
        if success:
            count += 1
            if count <= 10 or count % 100 == 0:
                print(f'OK {os.path.basename(os.path.dirname(f)):40s} {msg}')
        elif msg == 'migrated':
            skipped_migrated += 1
    
    print(f'\nTotal fixed: {count}')
    print(f'Skipped migrated: {skipped_migrated}')

if __name__ == '__main__':
    main()