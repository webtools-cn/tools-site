#!/usr/bin/env python3
"""修复meta description v5 - 最终版：精准emoji清洗 + 智能feature提取"""
import os, re, glob

def clean_name(name):
    """彻底清除emoji和特殊符号，保留中英文"""
    name = re.sub(r'[^\u4e00-\u9fff\u3400-\u4dbfa-zA-Z0-9\s\-\.\(\)（）/]', '', name)
    name = re.sub(r'\s+', ' ', name).strip()
    return name

def extract_info(filepath):
    """提取中文工具名+功能（去重、去噪音）"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read(15000)
    
    # --- 工具名：从h1提取 ---
    h1_match = re.search(r'<h1[^>]*>(.+?)</h1>', content)
    h1 = re.sub(r'<[^>]+>', '', h1_match.group(1)).strip() if h1_match else ''
    h1_clean = clean_name(h1)
    
    # 备选：title
    if not h1_clean or len(h1_clean) < 2:
        title_match = re.search(r'<title>(.+?)(?:\s*[-|]\s*Free ToolBase)', content)
        title = title_match.group(1).strip() if title_match else ''
        title = re.sub(r'^(免费在线|在线|免费)\s*', '', title)
        title_clean = clean_name(title)
        cn_name = title_clean if title_clean and len(title_clean) > 2 else os.path.basename(os.path.dirname(filepath)).replace('-', ' ')
    else:
        cn_name = h1_clean
    
    # --- 功能特征 ---
    features = []
    seen = set()
    
    # 策略：只取描述工具功能的<p>，过滤噪音
    paragraphs = re.findall(r'<p[^>]*>(.+?)</p>', content)
    for p in paragraphs:
        clean = re.sub(r'<[^>]+>', '', p).strip()
        
        # 过滤噪音段落
        if any(x in clean for x in ['首页', '›', '&rsaquo;', '&raquo;', '&raquo']):
            continue
        # 去掉"无需注册"等SEO尾缀
        clean = re.sub(r'\s*[|｜]\s*无需注册[^。]*', '', clean)
        clean = re.sub(r'\s*🔒.*', '', clean)
        clean = re.sub(r'\s*-\s*$', '', clean)
        
        # 长度范围：20-130字符（放宽上限）
        if len(clean) < 20 or len(clean) > 130:
            continue
        # 跳过代码/JSON
        if clean.startswith('{') or clean.startswith('function') or clean.startswith('const '):
            continue
        # 跳过纯英文噪点
        if re.match(r'^[A-Za-z0-9\s\.\-_]+$', clean) and len(clean) < 30:
            continue
        # 跳过"如何使用"等教程性内容
        if any(kw in clean for kw in ['以下是详细的使用', '以下是使用', '点此', '点击按钮', '第一步']):
            continue
        
        fp = clean[:25]
        if fp in seen:
            continue
        seen.add(fp)
        features.append(clean)
        if len(features) >= 2:
            break
    
    return cn_name, features

def gen_desc(cn_name, features):
    """生成高质量140-160字符description"""
    if not cn_name:
        cn_name = '工具'
    
    if features:
        # 取最佳feature
        main_feat = features[0]
        # 去掉可能的"免费在线XXX工具，"前缀避免重复
        main_feat = re.sub(r'^免费在线' + re.escape(cn_name) + r'[，,]\s*', '', main_feat)
        # 去掉尾随的纯前端本地处理等（会在模板里统一加）
        main_feat = re.sub(r'[，,]?\s*纯前端本地[^，。]*[，。]?\s*$', '', main_feat)
        main_feat = re.sub(r'[，,]?\s*数据不[^，。]*[，。]?\s*$', '', main_feat)
        
        if len(main_feat) < 15:
            # feature被清洗过度了，用第二个
            if len(features) > 1:
                main_feat = features[1]
                main_feat = re.sub(r'^免费在线' + re.escape(cn_name) + r'[，,]\s*', '', main_feat)
        
        # 控制总长度
        prefix = f"免费在线{cn_name}工具，"
        suffix = "。纯前端本地处理，数据不上传服务器，无需注册即可免费使用。"
        budget = 160 - len(prefix) - len(suffix)
        
        if len(main_feat) > budget:
            # 截断到句号
            cut = main_feat[:budget].rfind('。')
            if cut > 20:
                main_feat = main_feat[:cut+1]
            elif budget > 30:
                main_feat = main_feat[:budget-3] + '...'
            else:
                main_feat = main_feat[:budget]
        
        desc = f"{prefix}{main_feat}{suffix}"
    else:
        desc = f"免费在线{cn_name}工具，简单高效的{cn_name}解决方案，打开浏览器即可使用。纯前端本地处理，保障数据安全，无需注册完全免费。"
    
    # 最终调整
    if len(desc) < 120:
        desc = f"免费在线{cn_name}工具，实用的{cn_name}在线解决方案。纯前端本地处理，数据不上传服务器，无需注册即可免费使用。"
    
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
    
    # 修复条件：截断的 或 过短（<100字符）
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
    
    return True, f"[{old_len}→{len(new_desc)}]"

def main():
    base_dir = '/home/chison/tools-site'
    count = 0
    
    for f in sorted(glob.glob(f'{base_dir}/*/index.html')):
        if '/en/' in f or '/scripts/' in f:
            continue
        success, msg = fix_file(f)
        if success:
            count += 1
    
    print(f'Total fixed: {count}')
    return count

if __name__ == '__main__':
    main()
