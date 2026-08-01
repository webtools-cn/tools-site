#!/usr/bin/env python3
"""修复截断的meta description（含"..."且<100字符的非迁移页）"""
import os, re, glob, sys

def get_tool_features(filepath):
    """从页面内容提取工具功能特征"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read(8000)
    
    # 找h1
    h1_match = re.search(r'<h1[^>]*>(.+?)</h1>', content)
    h1 = re.sub(r'<[^>]+>', '', h1_match.group(1)) if h1_match else ''
    
    # 找功能描述 - 在<h2>或<p>中
    features = []
    h2_matches = re.findall(r'<h2[^>]*>(.+?)</h2>', content)
    for h2 in h2_matches[:3]:
        clean = re.sub(r'<[^>]+>', '', h2).strip()
        if clean and len(clean) < 30:
            features.append(clean)
    
    # 如果h2不够，找功能相关段落
    if len(features) < 2:
        p_matches = re.findall(r'<p[^>]*>(.+?)</p>', content)
        for p in p_matches[:5]:
            clean = re.sub(r'<[^>]+>', '', p).strip()
            if clean and len(clean) > 10 and len(clean) < 60:
                features.append(clean)
    
    return h1, features

def generate_description(tool_name, features_str, h1):
    """生成140-160字符的精准中文description"""
    base = f"免费在线{tool_name}工具"
    
    if features_str and len(features_str) > 3:
        desc = f"{base}，{features_str}。纯前端本地处理，数据不上传服务器，无需注册完全免费。"
    else:
        desc = f"{base}。{h1}。纯前端本地处理，数据不上传服务器，无需注册完全免费。"
    
    if len(desc) < 110:
        desc = f"{base}。无需下载安装，打开浏览器即可使用，数据不上传服务器，无需注册完全免费。"
    
    # 截断到160字符
    if len(desc) > 160:
        last_period = desc[:160].rfind('。')
        if last_period > 120:
            desc = desc[:last_period+1]
        else:
            desc = desc[:157].rstrip() + '...'
    
    return desc.strip()

def fix_file(filepath):
    """修复单个文件的meta description"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    old_match = re.search(r'(<meta\s+name=[\"\']description[\"\']\s+content=[\"\'])(.+?)([\"\'])', content, re.IGNORECASE)
    if not old_match:
        return False, "no meta"
    
    old_desc = old_match.group(2)
    old_len = len(old_desc)
    
    if '...' not in old_desc or old_len >= 100:
        return False, "skip"
    if '已迁移' in old_desc or '迁移至' in old_desc:
        return False, "migrated"
    
    tool_dir = os.path.dirname(filepath)
    tool_name = os.path.basename(tool_dir).replace('-', ' ').title()
    
    h1, features = get_tool_features(filepath)
    features_str = '支持' + '、'.join(features[:4]) if features else h1
    
    new_desc = generate_description(tool_name, features_str, h1)
    
    if len(new_desc) < 100:
        new_desc = f"免费在线{tool_name}工具，{features_str}。纯前端本地处理，数据不上传服务器，无需注册即可使用。"
    
    if len(new_desc) > 160:
        new_desc = new_desc[:157] + '...'
    
    new_meta = f'{old_match.group(1)}{new_desc}{old_match.group(3)}'
    content = content[:old_match.start()] + new_meta + content[old_match.end():]
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True, f"[{old_len}\u2192{len(new_desc)}]"

def main():
    base_dir = '/home/chison/tools-site'
    count = 0
    
    for f in sorted(glob.glob(f'{base_dir}/*/index.html')):
        if '/en/' in f or '/scripts/' in f:
            continue
        
        success, msg = fix_file(f)
        if success:
            count += 1
            print(f'OK {os.path.basename(os.path.dirname(f))} {msg}')
    
    print(f'\nTotal fixed: {count}')
    return count

if __name__ == '__main__':
    main()
