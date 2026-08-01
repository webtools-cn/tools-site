#!/usr/bin/env python3
"""修复meta description v7 - 简版：直接用h1作工具名，feature去前缀后拼接"""
import os, re, glob

def clean_name(name):
    """只清除emoji和特殊符号"""
    name = re.sub(r'[^\u4e00-\u9fff\u3400-\u4dbfa-zA-Z0-9\s\-\.\(\)（）/]', '', name)
    name = re.sub(r'\s+', ' ', name).strip()
    return name

def extract_info(filepath):
    """提取h1工具名和功能feature"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read(15000)
    
    # H1
    h1_match = re.search(r'<h1[^>]*>(.+?)</h1>', content)
    h1 = re.sub(r'<[^>]+>', '', h1_match.group(1)).strip() if h1_match else ''
    cn_name = clean_name(h1) if h1 else ''
    if not cn_name or len(cn_name) < 2:
        cn_name = os.path.basename(os.path.dirname(filepath)).replace('-', ' ')
    
    # Feature: 第一个有意义的描述性<p>
    feature = ''
    paragraphs = re.findall(r'<p[^>]*>(.+?)</p>', content)
    for p in paragraphs:
        clean = re.sub(r'<[^>]+>', '', p).strip()
        
        # 过滤
        if any(x in clean for x in ['首页', '›', '&rsaquo;', '&raquo;']):
            continue
        clean = re.sub(r'\s*[|｜]\s*无需注册[^。]*', '', clean)
        if len(clean) < 20:
            continue
        if clean.startswith('{') or clean.startswith('function'):
            continue
        if any(kw in clean for kw in ['以下是', '第一步', '使用方法']):
            continue
        
        feature = clean
        break
    
    return cn_name, feature

def gen_desc(cn_name, feature):
    """生成描述"""
    prefix = f"免费在线{cn_name}工具"
    suffix = "。纯前端本地处理，数据不上传服务器，无需注册即可免费使用。"
    
    if feature and len(feature) >= 20:
        # 去前缀重复
        feat = feature
        # 去掉 "免费在线XXX工具，" 类重复
        feat = re.sub(r'^免费在线' + re.escape(cn_name) + r'[工具]?[，,、]\s*', '', feat)
        feat = re.sub(r'^免费在线[^，]{0,20}[工具]?[，,、]\s*', '', feat)
        # 去掉尾随SEO冗余
        feat = re.sub(r'[，,]\s*无需注册[^。]*$', '', feat)
        feat = re.sub(r'[，,]\s*数据不[^。]*$', '', feat)
        
        # 计算可用空间
        base_len = len(prefix) + 1 + len(suffix)  # +1 for ，
        budget = 158 - base_len
        
        if budget > 15 and len(feat) > 0:
            # 截断feature
            if len(feat) > budget:
                cut = feat[:budget].rfind('。')
                if cut > budget * 0.5:
                    feat = feat[:cut+1]
                else:
                    cut = feat[:budget].rfind('，')
                    if cut > budget * 0.4:
                        feat = feat[:cut] + '。'
                    else:
                        feat = feat[:budget-3] + '...'
            desc = f"{prefix}，{feat}{suffix}"
        else:
            desc = f"{prefix}，快速便捷的{cn_name}解决方案{suffix}"
    else:
        desc = f"{prefix}，快速便捷的{cn_name}解决方案，打开浏览器即可使用{suffix}"
    
    # 最终微调
    if len(desc) < 110:
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
