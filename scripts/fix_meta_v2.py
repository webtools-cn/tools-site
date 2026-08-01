#!/usr/bin/env python3
"""修复meta description: 截断的+过短(<100字符)的非迁移页，生成中文精准描述"""
import os, re, glob

def extract_cn_name_and_features(filepath):
    """从页面提取中文名称和功能"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read(15000)
    
    # title中提取 - 格式: "XXX - Free ToolBase" 或 "XXX - 免费在线工具 | Free ToolBase"
    title_match = re.search(r'<title>(.+?)\s*[-|]\s*Free ToolBase', content)
    title = title_match.group(1).strip() if title_match else ''
    # 清理title中的"免费在线"等前缀
    title = re.sub(r'^(免费在线|在线|免费)\s*', '', title)
    
    # h1提取
    h1_match = re.search(r'<h1[^>]*>(.+?)</h1>', content)
    h1 = re.sub(r'<[^>]+>', '', h1_match.group(1)).strip() if h1_match else ''
    
    # 从title提取纯中文
    cn_name = title if title else h1
    # 去emoji
    cn_name = re.sub(r'[\U0001F300-\U0001F9FF\u2600-\u27BF\u2B50\u2700-\u27BF\uFE0F\u200D]', '', cn_name).strip()
    
    # 提取功能特征 - 从h1后的第一段描述性<p>
    features = []
    paragraphs = re.findall(r'<p[^>]*>(.+?)</p>', content)
    for p in paragraphs:
        clean = re.sub(r'<[^>]+>', '', p).strip()
        # 跳过太短/太长的/JSON/代码
        if 10 < len(clean) < 80 and '{' not in clean and 'function' not in clean:
            features.append(clean)
            if len(features) >= 2:
                break
    
    # 从h2提取
    if not features:
        h2_matches = re.findall(r'<h2[^>]*>(.+?)</h2>', content)
        for h2 in h2_matches[:3]:
            clean = re.sub(r'<[^>]+>', '', h2).strip()
            if clean and len(clean) < 30:
                features.append(clean)
    
    return cn_name, h1, features

def gen_desc(cn_name, h1, features):
    """生成140-160字符的中文description"""
    # 工具中文名
    if not cn_name or len(cn_name) < 2:
        cn_name = h1 if h1 else '工具'
    
    # 构建功能描述
    if features:
        feature_text = '支持' + '、'.join(features[:3])
    else:
        feature_text = h1 if h1 and len(h1) > 5 else ''
    
    # 组装
    desc = f"免费在线{cn_name}工具。{feature_text}。纯前端本地处理，数据不上传服务器，无需注册完全免费。"
    
    # 如果太短（features为空），用备选方案
    if len(desc) < 110:
        # 从页面找更多信息
        desc = f"免费在线{cn_name}工具，快速便捷的{cn_name}解决方案。纯前端本地处理，保护您的数据隐私，数据不上传服务器，无需注册即可免费使用。"
    
    # 确保140-160
    if len(desc) < 120:
        desc = f"免费在线{cn_name}工具，{cn_name}一站式解决方案。纯前端本地处理，数据不上传服务器，无需注册完全免费，打开浏览器即可使用。"
    
    # 截断
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
    
    # 跳过迁移页
    if '已迁移' in old_desc or '迁移至' in old_desc:
        return False, "migrated"
    
    # 只修复截断的或过短的
    needs_fix = ('...' in old_desc and old_len < 100) or (old_len < 100 and '...' not in old_desc)
    if not needs_fix and old_len >= 100:
        return False, "ok"
    
    cn_name, h1, features = extract_cn_name_and_features(filepath)
    new_desc = gen_desc(cn_name, h1, features)
    
    if len(new_desc) < 100:
        new_desc = f"免费在线{cn_name}工具，简单高效的{cn_name}在线解决方案。纯前端本地处理，保障数据安全，无需下载注册，打开浏览器即可免费使用。"
    
    if len(new_desc) > 160:
        new_desc = new_desc[:157] + '...'
    
    # 如果新旧一致就不改
    if new_desc == old_desc:
        return False, "same"
    
    new_meta = f'{old_match.group(1)}{new_desc}{old_match.group(3)}'
    content = content[:old_match.start()] + new_meta + content[old_match.end():]
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True, f"[{old_len}\u2192{len(new_desc)}]"

def main():
    base_dir = '/home/chison/tools-site'
    count = 0
    skipped_migrated = 0
    skipped_ok = 0
    
    for f in sorted(glob.glob(f'{base_dir}/*/index.html')):
        if '/en/' in f or '/scripts/' in f:
            continue
        
        success, msg = fix_file(f)
        if success:
            count += 1
            print(f'OK {os.path.basename(os.path.dirname(f))} {msg}')
        elif msg == 'migrated':
            skipped_migrated += 1
        elif msg == 'ok':
            skipped_ok += 1
    
    print(f'\nTotal fixed: {count}')
    print(f'Skipped (migrated): {skipped_migrated}')
    print(f'Skipped (already ok): {skipped_ok}')

if __name__ == '__main__':
    main()
