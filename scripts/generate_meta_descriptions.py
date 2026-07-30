#!/usr/bin/env python3
"""
智能meta description生成器 v2
策略：
1. 读取页面现有description
2. 如果已有不错内容但太短（<120），在后面补充分隔符+SEO尾句
3. 如果是模板化垃圾，从h1/title/content重新生成
4. 更新meta description + og:description + Schema description
"""
import glob, re, os, sys

def extract_page(filepath):
    """全面提取页面信息"""
    with open(filepath) as f:
        content = f.read()
    
    info = {}
    
    # 现有meta description
    m = re.search(r'<meta name="description" content="([^"]+)"', content)
    info['old_desc'] = m.group(1) if m else ''
    info['old_len'] = len(info['old_desc'])
    
    # title
    m = re.search(r'<title>(.*?)</title>', content)
    title = m.group(1).strip() if m else ''
    # 清理title
    title = re.sub(r'\s*[-|]\s*Free ToolBase.*$', '', title).strip()
    title = re.sub(r'\s*[-|]\s*在线小工具矩阵.*$', '', title).strip()
    info['title'] = title
    
    # h1
    m = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.DOTALL)
    h1 = re.sub(r'<[^>]+>', '', m.group(1)).strip() if m else ''
    info['h1'] = h1
    
    # 所有段落
    ps = re.findall(r'<p[^>]*>(.*?)</p>', content, re.DOTALL)
    paragraphs = []
    for p in ps:
        clean = re.sub(r'<[^>]+>', '', p).strip()
        if len(clean) > 20:
            paragraphs.append(clean)
    info['paragraphs'] = paragraphs
    
    # 特性列表
    items = re.findall(r'<li[^>]*>(.*?)</li>', content, re.DOTALL)
    features = []
    for i in items:
        clean = re.sub(r'<[^>]+>', '', i).strip()
        if len(clean) > 8 and not clean.startswith('{') and not clean.startswith('"') and 'schema.org' not in clean.lower():
            features.append(clean[:80])
    info['features'] = features[:5]
    
    return info

def is_template_desc(desc):
    """判断是否是模板化描述（实质内容占比很低）"""
    # 移除模板关键词后看剩余实质内容
    stripped = desc
    for word in ['免费在线', '无需注册', '浏览器本地处理', '纯前端处理', '数据不上传服务器', '保护隐私', '免费在线工具', '数据绝不上传', '即开即用']:
        stripped = stripped.replace(word, '')
    # 清理标点和空格
    stripped = re.sub(r'[\s，,。\.|、·！!]+', '', stripped)
    
    # 如果去掉模板词后剩余少于15个字符，说明是纯模板
    if len(stripped) < 15:
        return True
    return False

def generate_description(info, tool_name):
    """根据页面信息生成SEO描述（140-160字符）"""
    old = info['old_desc']
    first_p = info['paragraphs'][0] if info['paragraphs'] else ''
    features = info['features']
    
    # SEO后缀（通用）
    seo_suffix = '纯前端本地处理，数据不上传服务器，无需注册完全免费。'
    
    # 清理函数
    def clean_text(text):
        """移除模板后缀和冗余"""
        text = re.sub(r'\s*\|\s*无需注册.*$', '', text)
        text = re.sub(r'，免费在线工具.*$', '', text)
        text = re.sub(r'，无需注册\s*$', '', text)
        text = re.sub(r'\s*\|\s*Free ToolBase.*$', '', text)
        text = re.sub(r'，无需注册，无需注册\s*$', '', text)
        text = text.strip().rstrip('。.')
        return text
    
    # 工具显示名（去掉emoji和"免费在线"前缀）
    tool_display = re.sub(r'[\U0001F300-\U0001F9FF\u2600-\u27BF\u2B50\u2700-\u27BF\uFE0F\u200D]', '', info['h1']).strip()
    tool_display = tool_display.replace('免费在线', '').replace('免费', '').strip()
    
    # 策略1：已有不错的描述，扩展
    if not is_template_desc(old) and len(old) >= 40:
        base = clean_text(old)
        
        # 确保base足够长
        # 如果有features，追加features
        if features and len(base) < 120:
            feat_text = '、'.join([f.split('：')[0].split('—')[0].strip() for f in features[:2]])
            if feat_text:
                base = f'{base}，支持{feat_text}'
        
        # 如果base仍然太短，从h1补充
        if len(base) < 80 and tool_display and tool_display not in base:
            base = f'免费在线{tool_display}工具，{base}'
        
        if len(base) < 140:
            combined = base + '。' + seo_suffix
            if len(combined) <= 160:
                return combined
            else:
                short_suffix = '无需注册，纯前端本地处理。'
                combined = base + '。' + short_suffix
                return combined[:160]
        else:
            return base[:160]
    
    # 策略2：从第一段描述构建
    first_p_clean = clean_text(first_p) if first_p else ''
    if first_p_clean and len(first_p_clean) > 30:
        base = first_p_clean
        
        if not base.startswith('免费'):
            base = '免费在线' + base
        
        if len(base) < 140:
            combined = base + '。' + seo_suffix
            return combined[:160]
        else:
            return base[:160]
    
    # 策略3：从features构建
    if features:
        feat_list = [f.split('：')[0].split('—')[0].strip() for f in features[:4]]
        feat_text = '、'.join(feat_list)
        desc = f'免费在线{tool_display}工具，支持{feat_text}。纯前端本地处理，数据不上传，无需注册完全免费。'
        return desc[:160]
    
    # 策略4：从h1构建，如果还是太短就用old_desc
    desc = f'免费在线{tool_display}工具，纯前端本地处理，数据不上传服务器，无需注册下载，即开即用。'
    if len(desc) < 100:
        # 用旧描述+后缀
        base = clean_text(old) if old else tool_display
        desc = base + '。' + seo_suffix
    return desc[:160]

def update_page(filepath, new_desc):
    """更新页面meta description, og:description, schema description"""
    with open(filepath) as f:
        content = f.read()
    
    modified = False
    changes = []
    
    # 更新 meta description
    old_meta_match = re.search(r'<meta name="description" content="([^"]+)"', content)
    if old_meta_match and old_meta_match.group(1) != new_desc:
        content = content.replace(
            f'<meta name="description" content="{old_meta_match.group(1)}"',
            f'<meta name="description" content="{new_desc}"'
        )
        modified = True
        changes.append('meta')
    
    # 更新 og:description
    old_og_match = re.search(r'<meta property="og:description" content="([^"]+)"', content)
    if old_og_match and old_og_match.group(1) != new_desc:
        content = content.replace(
            f'<meta property="og:description" content="{old_og_match.group(1)}"',
            f'<meta property="og:description" content="{new_desc}"'
        )
        modified = True
        changes.append('og')
    
    # 更新 twitter:description
    old_tw_match = re.search(r'<meta name="twitter:description" content="([^"]+)"', content)
    if old_tw_match and old_tw_match.group(1) != new_desc:
        content = content.replace(
            f'<meta name="twitter:description" content="{old_tw_match.group(1)}"',
            f'<meta name="twitter:description" content="{new_desc}"'
        )
        modified = True
        changes.append('twitter')
    
    # 更新 Schema SoftwareApplication description
    old_schema = re.search(r'("SoftwareApplication"[^}]*"description"\s*:\s*)"([^"]+)"', content)
    if old_schema and old_schema.group(2) != new_desc:
        content = re.sub(
            r'("SoftwareApplication"[^}]*"description"\s*:\s*)"([^"]+)"',
            rf'\1"{new_desc}"',
            content,
            count=1
        )
        modified = True
        changes.append('schema')
    
    if modified:
        with open(filepath, 'w') as f:
            f.write(content)
    
    return modified, changes

def main():
    # 收集需要更新的页面
    pages = []
    for f in glob.glob('*/index.html'):
        tool = f.split('/')[0]
        
        # 跳过特殊目录
        if tool in ['en', 'css', 'js', 'scripts', 'quality', '.gsc-data', '404']:
            continue
        
        content = open(f).read()
        
        # 跳过迁移页面
        if 'meta http-equiv="refresh"' in content or '已迁移' in content:
            continue
        
        # 跳过没有实际工具内容的页面
        if not re.search(r'<h1[^>]*>', content):
            continue
        
        info = extract_page(f)
        if info['old_len'] < 120:
            pages.append((tool, f, info))
    
    # 按旧描述长度排序
    pages.sort(key=lambda x: x[2]['old_len'])
    
    print(f"Total tools with short meta: {len(pages)}")
    print(f"Processing first 20...\n")
    
    batch = pages[:20]
    updated = []
    
    for tool, filepath, info in batch:
        new_desc = generate_description(info, tool)
        new_len = len(new_desc)
        
        # 至少要比原来长，且>70
        if new_len < 70 or new_len <= info['old_len']:
            print(f"SKIP: {tool}: desc not good enough ({info['old_len']}→{new_len})")
            continue
        
        ok, changes = update_page(filepath, new_desc)
        if ok:
            updated.append((tool, info['old_len'], new_len))
            print(f"✓ {tool}: {info['old_len']}→{new_len} [{','.join(changes)}]")
            print(f"  {new_desc}")
        else:
            print(f"✗ {tool}: no change needed")
    
    print(f"\n=== Summary: {len(updated)} pages updated ===")

if __name__ == '__main__':
    main()