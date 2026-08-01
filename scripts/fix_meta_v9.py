#!/usr/bin/env python3
"""修复meta description v9 - 极简版：用feature核心+固定模板"""
import os, re, glob

def clean_name(name):
    """清除emoji和特殊符号"""
    name = re.sub(r'[^\u4e00-\u9fff\u3400-\u4dbfa-zA-Z0-9\s\-\.\(\)（）/+]', '', name)
    name = re.sub(r'\s+', ' ', name).strip()
    return name

def extract_info(filepath):
    """提取h1工具名+描述性内容"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read(15000)
    
    # H1 - 去emoji
    h1_match = re.search(r'<h1[^>]*>(.+?)</h1>', content)
    h1 = re.sub(r'<[^>]+>', '', h1_match.group(1)).strip() if h1_match else ''
    cn_name = clean_name(h1) if h1 else os.path.basename(os.path.dirname(filepath)).replace('-', ' ')
    if not cn_name or len(cn_name) < 2:
        cn_name = os.path.basename(os.path.dirname(filepath)).replace('-', ' ')
    
    # Feature - 第一个有意义的描述
    feature = ''
    paragraphs = re.findall(r'<p[^>]*>(.+?)</p>', content)
    for p in paragraphs:
        clean = re.sub(r'<[^>]+>', '', p).strip()
        if any(x in clean for x in ['首页', '›', '&rsaquo;', '&raquo;']):
            continue
        clean = re.sub(r'\s*[|｜]\s*无需注册.*$', '', clean)
        clean = re.sub(r'\s*🔒.*$', '', clean)
        clean = re.sub(r'\s*纯前端.*$', '', clean)
        clean = re.sub(r'\s*数据不.*$', '', clean)
        if len(clean) < 25:
            continue
        if clean.startswith('{') or clean.startswith('function') or clean.startswith('const'):
            continue
        if any(kw in clean for kw in ['以下是', '第一步', '使用方法', '如何使用', '详细指南']):
            continue
        feature = clean
        break
    
    return cn_name, feature

def gen_desc(cn_name, feature):
    """生成140-160字符精准描述"""
    # 去feature中的各种前缀
    core = feature if feature else ''
    # 去掉 "免费在线XXX工具，" 类前缀
    core = re.sub(r'^免费在线[^，,。]{0,30}[工具]?\s*[，,、。]\s*', '', core)
    core = re.sub(r'^免费[^，,。]{0,20}[工具]?\s*[，,、。]\s*', '', core)
    core = re.sub(r'^在线[^，,。]{0,20}[工具]?\s*[，,、。]\s*', '', core)
    core = re.sub(r'^'+re.escape(cn_name)+r'[工具]?\s*[，,、。]\s*', '', core)
    # 去掉尾随
    core = re.sub(r'\s*[|｜]\s*无需注册.*$', '', core)
    core = re.sub(r'\s*🔒.*$', '', core)
    core = core.strip()
    
    # 去"在线"冗余：如果cn_name已经包含"在线"，prefix不加
    has_online = '在线' in cn_name
    prefix = f"免费在线{cn_name}工具" if not has_online else f"免费{cn_name}工具"
    
    suffix = "。纯前端本地处理，数据不上传服务器，无需注册即可免费使用。"
    
    if core and len(core) >= 10:
        base_len = len(prefix) + 1 + len(suffix)
        budget = 158 - base_len
        if budget > 15:
            if len(core) > budget:
                cut = core[:budget].rfind('。')
                if cut > budget * 0.5:
                    core = core[:cut+1]
                else:
                    cut = core[:budget].rfind('，')
                    if cut > budget * 0.3:
                        core = core[:cut] + '。'
                    else:
                        core = core[:budget-3] + '...'
            desc = f"{prefix}，{core}{suffix}"
        else:
            desc = f"{prefix}，快速实用的{cn_name}解决方案{suffix}"
    else:
        desc = f"{prefix}，快速实用的{cn_name}解决方案，打开浏览器即可使用{suffix}"
    
    if len(desc) < 90:
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