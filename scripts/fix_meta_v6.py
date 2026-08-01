#!/usr/bin/env python3
"""修复meta description v6 - 智能feature截断版"""
import os, re, glob

def clean_name(name):
    """清除emoji，只保留中英文数字"""
    name = re.sub(r'[^\u4e00-\u9fff\u3400-\u4dbfa-zA-Z0-9\s\-\.\(\)（）/]', '', name)
    name = re.sub(r'\s+', ' ', name).strip()
    return name

def smart_truncate(text, max_len):
    """智能截断中文文本到max_len以内"""
    if len(text) <= max_len:
        return text
    # 优先在句号处截断
    cut = text[:max_len].rfind('。')
    if cut > max_len * 0.6:
        return text[:cut+1]
    # 其次在逗号处
    cut = text[:max_len].rfind('，')
    if cut > max_len * 0.5:
        return text[:cut] + '。'
    # 最后硬截断
    return text[:max_len-3] + '...'

def extract_info(filepath):
    """提取工具名+功能描述"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read(15000)
    
    # 工具名
    h1_match = re.search(r'<h1[^>]*>(.+?)</h1>', content)
    h1 = re.sub(r'<[^>]+>', '', h1_match.group(1)).strip() if h1_match else ''
    h1_clean = clean_name(h1)
    
    # 去除h1中可能多余的前缀后缀
    cn_name = h1_clean
    # 去掉开头的"免费"/"在线"
    cn_name = re.sub(r'^(免费|在线)\s*', '', cn_name)
    
    if not cn_name or len(cn_name) < 2:
        title_match = re.search(r'<title>(.+?)(?:\s*[-|]\s*Free ToolBase)', content)
        if title_match:
            title = clean_name(title_match.group(1))
            title = re.sub(r'^(免费在线|在线|免费)\s*', '', title)
            cn_name = title
        if not cn_name or len(cn_name) < 2:
            cn_name = os.path.basename(os.path.dirname(filepath)).replace('-', ' ')
    
    # 功能描述：找第一个高质量的描述性段落
    best_feature = ''
    
    # 策略：遍历所有<p>，找最佳的那个
    paragraphs = re.findall(r'<p[^>]*>(.+?)</p>', content)
    for p in paragraphs:
        clean = re.sub(r'<[^>]+>', '', p).strip()
        
        # 过滤噪音
        if any(x in clean for x in ['首页', '›', '&rsaquo;', '&raquo;']):
            continue
        if len(clean) < 15:
            continue
        if clean.startswith('{') or clean.startswith('function') or clean.startswith('const') or clean.startswith('import'):
            continue
        if any(kw in clean for kw in ['以下是详细的使用', '以下是使用', '第一步', '步骤', '点击按钮', '使用方法']):
            continue
        # 跳过纯链接/纯英文短句
        if re.match(r'^[\(\)\d\s\.\-,:;!?]+$', clean):
            continue
        
        # 清理SEO尾缀
        clean = re.sub(r'\s*[|｜]\s*无需注册[^。]*', '', clean)
        
        # 这是好的候选
        best_feature = clean
        break
    
    return cn_name, best_feature

def gen_desc(cn_name, feature):
    """生成精准description"""
    if not cn_name:
        cn_name = '工具'
    
    prefix = f"免费在线{cn_name}工具"
    
    if feature and len(feature) >= 15:
        # 去掉重复前缀
        feature = re.sub(r'^免费在线' + re.escape(cn_name) + r'[，,、]\s*', '', feature)
        feature = re.sub(r'^免费在线', '', feature)
        # 去掉尾随的"纯前端"等
        feature = re.sub(r'[，,]\s*纯前端[^。]*$', '', feature)
        feature = re.sub(r'[，,]\s*数据不[^。]*$', '', feature)
        
        suffix = "。纯前端本地处理，数据不上传服务器，无需注册即可免费使用。"
        budget = 158 - len(prefix) - len(suffix)
        
        if budget > 10:
            feat_trimmed = smart_truncate(feature, budget)
            desc = f"{prefix}，{feat_trimmed}{suffix}"
        else:
            desc = f"{prefix}，快速便捷的{cn_name}解决方案。{suffix}"
    else:
        desc = f"{prefix}，快速便捷的{cn_name}解决方案，打开浏览器即可使用。纯前端本地处理，保障数据安全，无需注册完全免费。"
    
    # 最终确保140-160
    if len(desc) < 120:
        desc = f"{prefix}，{cn_name}一站式在线解决方案。纯前端本地处理，数据不上传服务器，无需注册即可免费使用。"
    
    if len(desc) > 160:
        cut = desc[:160].rfind('。')
        desc = desc[:cut+1] if cut > 120 else desc[:157] + '...'
    
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
    
    # 修复条件
    needs_fix = ('...' in old_desc and old_len < 100) or (old_len < 100 and '...' not in old_desc)
    if not needs_fix and old_len >= 100:
        return False, "ok"
    
    cn_name, feature = extract_info(filepath)
    new_desc = gen_desc(cn_name, feature)
    
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
