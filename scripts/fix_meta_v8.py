#!/usr/bin/env python3
"""修复meta description v8 - 最终版：宽松前缀匹配+智能截断"""
import os, re, glob

def clean_name(name):
    """清除emoji"""
    name = re.sub(r'[^\u4e00-\u9fff\u3400-\u4dbfa-zA-Z0-9\s\-\.\(\)（）/+]', '', name)
    name = re.sub(r'\s+', ' ', name).strip()
    return name

def extract_info(filepath):
    """提取工具名+feature"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read(15000)
    
    # H1
    h1_match = re.search(r'<h1[^>]*>(.+?)</h1>', content)
    h1 = re.sub(r'<[^>]+>', '', h1_match.group(1)).strip() if h1_match else ''
    cn_name = clean_name(h1) if h1 else ''
    if not cn_name or len(cn_name) < 2:
        cn_name = os.path.basename(os.path.dirname(filepath)).replace('-', ' ')
    
    # Feature
    feature = ''
    paragraphs = re.findall(r'<p[^>]*>(.+?)</p>', content)
    for p in paragraphs:
        clean = re.sub(r'<[^>]+>', '', p).strip()
        if any(x in clean for x in ['首页', '›', '&rsaquo;', '&raquo;']):
            continue
        clean = re.sub(r'\s*[|｜]\s*无需注册.*$', '', clean)
        clean = re.sub(r'\s*🔒.*$', '', clean)
        if len(clean) < 25:
            continue
        if clean.startswith('{') or clean.startswith('function'):
            continue
        if any(kw in clean for kw in ['以下是', '第一步', '使用方法']):
            continue
        feature = clean
        break
    
    return cn_name, feature

def strip_feature_prefix(feature, cn_name):
    """去掉feature中重复的前缀（如"免费在线XXX工具，"）"""
    # 尝试多种模式
    patterns = [
        rf'^免费在线{re.escape(cn_name)}[工具]?\s*[，,、]\s*',
        rf'^免费在线[^，,、]{{0,15}}[工具]?\s*[，,、]\s*',
        rf'^{re.escape(cn_name)}[工具]?\s*[，,、]\s*',
        rf'^免费{re.escape(cn_name)}[工具]?\s*[，,、]\s*',
        rf'^在线{re.escape(cn_name)}[工具]?\s*[，,、]\s*',
    ]
    for pat in patterns:
        feature = re.sub(pat, '', feature)
    # 去掉尾随的SEO冗余
    feature = re.sub(r'\s*[|｜]\s*无需注册.*$', '', feature)
    feature = re.sub(r'\s*🔒\s*无需注册.*$', '', feature)
    feature = re.sub(r'\s*数据不上传.*$', '', feature)
    feature = re.sub(r'\s*纯前端.*$', '', feature)
    return feature.strip()

def gen_desc(cn_name, feature):
    """生成140-160描述"""
    prefix = f"免费在线{cn_name}工具"
    suffix = "。纯前端本地处理，数据不上传服务器，无需注册即可免费使用。"
    
    if feature and len(feature) >= 20:
        feat = strip_feature_prefix(feature, cn_name)
        
        if feat and len(feat) >= 10:
            # 计算budget
            base_len = len(prefix) + 1 + len(suffix)  # +1 = ，
            budget = 158 - base_len
            
            if budget > 20:
                # 截断到budget
                if len(feat) > budget:
                    # 找截断点
                    cut = feat[:budget].rfind('。')
                    if cut > budget * 0.5:
                        feat = feat[:cut+1]
                    else:
                        cut = feat[:budget].rfind('，')
                        if cut > budget * 0.3:
                            feat = feat[:cut] + '。'
                        else:
                            feat = feat[:budget-3] + '...'
                desc = f"{prefix}，{feat}{suffix}"
            else:
                desc = f"{prefix}，快速实用的{cn_name}解决方案{suffix}"
        else:
            desc = f"{prefix}，快速实用的{cn_name}解决方案{suffix}"
    else:
        desc = f"{prefix}，快速实用的{cn_name}解决方案，打开浏览器即可使用{suffix}"
    
    # 安全网
    if len(desc) < 100:
        desc = f"{prefix}，{cn_name}一站式在线解决方案{suffix}"
    if len(desc) > 160:
        cut = desc[:160].rfind('。')
        desc = desc[:cut+1] if cut > 100 else desc[:157] + '...'
    
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