#!/usr/bin/env python3
"""
SEO Meta Description优化脚本
目标：将<100字符的meta description扩展到140-160字符
策略：提取工具信息 + 场景关键词 + 用户痛点
"""
import re, os, glob, sys

def extract_info(content):
    """从页面提取工具信息"""
    info = {}
    
    # Title
    m = re.search(r'<title>(.*?)</title>', content)
    if m:
        raw = re.sub(r'\s*[-–|]\s*Free ToolBase.*$', '', m.group(1)).strip()
        raw = re.sub(r'\s*\|.*$', '', raw).strip()
        raw = re.sub(r'\s*[-–]\s*$', '', raw).strip()
        # Remove "免费在线" prefix
        raw = re.sub(r'^免费在线\s*', '', raw)
        raw = re.sub(r'^免费\s*', '', raw)
        info['title'] = raw
    
    # H1
    m = re.search(r'<h1[^>]*>(.*?)</h1>', content)
    if m:
        h1 = re.sub(r'<[^>]+>', '', m.group(1)).strip()
        # Remove emoji
        h1 = re.sub(r'[\U0001F300-\U0001F9FF\u2600-\u27BF\u2B50\u2700-\u27BF]', '', h1).strip()
        info['h1'] = h1
    
    # Hero paragraph
    m = re.search(r'class="hero"[^>]*>.*?<p>(.*?)</p>', content, re.DOTALL)
    if m:
        hero = re.sub(r'<[^>]+>', '', m.group(1)).strip()
        # Remove "| 无需注册 ..." suffix
        hero = re.sub(r'\s*\|.*$', '', hero).strip()
        info['hero'] = hero
    
    # Existing meta
    m = re.search(r'<meta name="description" content="([^"]+)"', content)
    if m:
        info['old_meta'] = m.group(1)
        info['old_len'] = len(m.group(1))
    
    # Keywords
    m = re.search(r'<meta name="keywords" content="([^"]+)"', content)
    if m:
        info['keywords'] = m.group(1)
    
    return info

def generate_meta(info):
    """生成140-160字符的精准meta description"""
    tool_name = info.get('title', '')
    if not tool_name or len(tool_name) < 3:
        tool_name = info.get('h1', '在线工具')
    
    # 获取功能描述 - 用old_meta作为基底，它已经是最精简的
    old_meta = info.get('old_meta', '')
    
    # 清理尾部冗余
    base_desc = old_meta.strip().rstrip('。，.!！?？')
    base_desc = re.sub(r'，\s*免费在线工具\s*，?\s*无需注册\s*$', '', base_desc)
    base_desc = re.sub(r'，\s*免费在线工具\s*$', '', base_desc)
    base_desc = re.sub(r'。\s*免费在线工具\s*，?\s*无需注册\s*$', '', base_desc)
    
    # 如果base_desc已经很好了，只需要补充到140-160
    if 140 <= len(base_desc) <= 160:
        return base_desc
    
    target_min, target_max = 140, 160
    
    # 计算需要补充多少字符
    remaining = target_min - len(base_desc)
    
    if remaining <= 0:
        # 已经足够长，直接返回
        return base_desc[:157] + '。' if len(base_desc) > 160 else base_desc
    
    # 场景后缀库（高质量、含搜索词的）
    tool_type_suffixes = {
        '计算器': [
            '基于标准公式算法实时计算，结果精准可靠。支持自定义参数灵活配置，免费在线工具无需注册，适合个人理财规划和企业财务分析使用。',
            '输入数值立即得出结果，清晰展示详细计算步骤和推导过程。支持多种参数组合模式，满足不同场景的使用需求。',
            '操作简单直观，自动校验输入格式并提示错误。计算结果支持一键复制导出，数据不上传服务器保障用户隐私安全。',
        ],
        '生成器': [
            '可视化配置参数，实时预览生成效果。支持一键复制代码或导出，前端开发和设计效率神器。',
            '丰富的自定义选项，所见即所得操作体验。生成的代码即拿即用，纯前端处理零延迟。',
            '智能识别输入自动生成，支持多种格式输出。无需注册安装，打开浏览器即可使用。',
        ],
        '转换器': [
            '快速完成格式互转，支持拖拽上传和批量处理。纯浏览器端本地转换，文件数据安全有保障。',
            '精准转换保留原始内容和结构，支持多种输入输出格式。无需安装软件，免费在线使用。',
            '一键转换秒出结果，支持大文件和大数据量处理。所有计算在本地完成，不经过任何服务器。',
        ],
        '查看器': [
            '清晰直观的数据展示，支持多种视图模式切换。无需下载安装，打开网页即可查看分析。',
            '智能解析自动识别格式，信息展示层次分明。纯前端渲染保障数据安全，免费无需注册。',
        ],
        '编辑器': [
            '所见即所得编辑体验，支持语法高亮和自动补全。提供代码校验和格式化功能，提升开发效率。',
            '实时编辑即时反馈，支持多语言语法高亮。纯前端处理数据不上传，开发者日常必备工具。',
        ],
        '工具': [
            '简洁高效的操作流程，无需注册即开即用。纯前端本地处理保障数据安全，免费在线使用。',
            '解决特定问题的实用利器，无需下载安装任何软件。数据不出浏览器，保护用户隐私安全。',
            '在线处理即时反馈，操作流程简单直观。所有数据在浏览器本地处理，安全可靠无需注册。',
        ],
        '增强器': [
            '一键操作快速完成处理，实时预览效果并支持参数调节。纯浏览器端本地运算，文件数据安全保障，无需下载注册。',
        ],
        '可视化': [
            '上传即生成清晰可视化效果，支持多种显示模式和自定义样式。纯前端渲染处理，数据安全无需注册。',
        ],
        '压缩': [
            '高效压缩算法快速处理，支持多级压缩率调节。纯前端本地运算，文件不经过任何服务器。',
        ],
        '编码': [
            '支持多种编码格式互转，实时输入即时转换。纯浏览器端执行保障数据安全，开发者必备工具。',
        ],
        '解码': [
            '快速解码还原原始内容，支持标准编码格式。所有运算在浏览器本地完成，数据零上传。',
        ],
        '加密': [
            '浏览器端本地加密运算，支持多种加密算法和密钥格式。数据绝不上传服务器，保障信息安全。',
        ],
        '提取器': [
            '智能识别精准提取目标信息，支持批量数据输入。处理速度快，结果格式统一便于后续使用。',
        ],
        '查询': [
            '快速查询秒级返回结果，数据来源权威准确。界面简洁操作方便，免费无需注册。',
        ],
        '分析': [
            '深度数据分析功能，自动生成可视化报表。支持数据导入导出，适合学术研究和商业决策。',
        ],
        '制作': [
            '轻松创建专业品质内容，提供丰富模板和自定义选项。输出格式通用，易于分享和使用。',
        ],
    }
    
    # 找匹配的后缀 - 优先匹配更具体的类型
    matched_suffixes = []
    # 优先顺序：工具类型关键词按优先级排列
    priority_keywords = ['计算器','生成器','转换器','编辑器','查看器','可视化','增强器','压缩','编码','解码','加密','提取器','制作','分析','查询','工具']
    for kw in priority_keywords:
        if kw in tool_name or kw in base_desc:
            matched_suffixes.extend(tool_type_suffixes.get(kw, []))
            break  # 取第一个匹配的，避免混合
    
    if not matched_suffixes:
        matched_suffixes = tool_type_suffixes.get('工具', ['简洁高效的操作流程，无需注册即开即用。'])
    
    # 选一个最合适长度的后缀
    best_suffix = None
    for suffix in matched_suffixes:
        new_len = len(base_desc) + 1 + len(suffix)  # +1 for separator
        if 140 <= new_len <= 160:
            best_suffix = suffix
            break
        elif new_len < 140 and (best_suffix is None or len(suffix) > len(best_suffix)):
            best_suffix = suffix
    
    if best_suffix is None:
        best_suffix = matched_suffixes[0]
    
    # 如果最佳后缀+base_desc仍不够140，使用通用长后缀
    if len(base_desc) + len(best_suffix) < 138:
        # base太短，用超长通用后缀
        best_suffix = '功能实用操作简单，无需注册安装即开即用。所有处理在浏览器本地完成，数据绝不上传服务器，免费在线工具安全可靠。'
    
    # 选择分隔符
    if base_desc.endswith('。') or best_suffix.startswith('。'):
        meta = f"{base_desc}{best_suffix}"
    else:
        meta = f"{base_desc}。{best_suffix}"
    
    # 最终长度检查 - 循环直到>=140（最多一次）
    if len(meta) < 140:
        if len(meta) < 135:
            meta += '，无需注册安装即开即用，纯前端处理保障数据安全'
        elif '无需注册' not in meta[-20:]:
            meta += '，无需注册安装即开即用'
        else:
            meta += '，纯前端处理保障数据安全'
    if len(meta) < 140:
        meta += '。'  # still short, pad
    elif len(meta) > 160:
        # 太长，在最后一个句号处截断
        cut = meta[:158]
        last_period = max(cut.rfind('。'), cut.rfind('，'))
        if last_period > 130:
            meta = meta[:last_period] + '。'
        else:
            meta = cut.rstrip('，。') + '。'
    
    return meta

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true', help='Preview only, no changes')
    parser.add_argument('--limit', type=int, default=30, help='Max pages to process')
    args = parser.parse_args()
    
    base_dir = '/home/chison/tools-site'
    os.chdir(base_dir)
    
    files = []
    for f in sorted(glob.glob('*/index.html')):
        dirname = os.path.dirname(f)
        if dirname.startswith('en/'):
            continue
        with open(f) as fh:
            content = fh.read()
        if '已迁移' in content:
            continue
        m = re.search(r'<meta name="description" content="([^"]+)"', content)
        if m and len(m.group(1)) < 100:
            files.append(dirname)
    
    print(f"Found {len(files)} pages with short meta (<100 chars)")
    
    if args.dry_run:
        print("=== DRY RUN MODE ===\n")
    
    success_count = 0
    skipped_count = 0
    modified_files = []
    
    for p in files[:args.limit]:
        fpath = f'{p}/index.html'
        with open(fpath) as f:
            content = f.read()
        info = extract_info(content)
        new_meta = generate_meta(info)
        
        old_meta = info.get('old_meta', '')
        old_len = info.get('old_len', 0)
        new_len = len(new_meta)
        
        if new_len < 140 or new_len > 160:
            print(f"SKIP {p}: length out of range ({new_len})")
            skipped_count += 1
            continue
        
        if args.dry_run:
            print(f"\n{p}:")
            print(f"  Old ({old_len}): {old_meta}")
            print(f"  New ({new_len}): {new_meta}")
            success_count += 1
            continue
        
        # Replace meta description, og:description, and JSON-LD description
        # 1. meta description
        new_content = content.replace(
            f'<meta name="description" content="{old_meta}">',
            f'<meta name="description" content="{new_meta}">',
            1
        )
        # 2. og:description (use same content)
        new_content = re.sub(
            r'<meta property="og:description" content="[^"]*"',
            f'<meta property="og:description" content="{new_meta}"',
            new_content,
            count=1
        )
        # 3. JSON-LD SoftwareApplication description
        new_content = re.sub(
            r'"description":"[^"]*"(,"applicationCategory")',
            f'"description":"{new_meta}"\\1',
            new_content,
            count=1
        )
        
        with open(fpath, 'w') as f:
            f.write(new_content)
        
        modified_files.append(p)
        success_count += 1
    
    print(f"\n=== SUMMARY ===")
    print(f"Processed: {len(files[:args.limit])}")
    print(f"Modified: {success_count - skipped_count}")
    print(f"Skipped: {skipped_count}")
    
    if modified_files and not args.dry_run:
        print(f"\nModified files: {modified_files[:10]}...")
    
    return files

if __name__ == '__main__':
    files = main()
