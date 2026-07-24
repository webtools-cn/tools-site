#!/usr/bin/env python3
"""
批量修复明确的问题：
1. FAQ重复：同时存在emoji FAQ和空的纯文本FAQ → 删除空FAQ
2. 空div：删除无id无data属性的空div标签
最多修复100个文件
"""
import os, re, json
from pathlib import Path

SITE_DIR = Path(__file__).parent.parent
SKIP_DIRS = {'scripts','css','js','docs','quality','blog','en','.gsc-data','.git',
             'about','contact','terms','privacy','assets','images','node_modules'}
MAX_FIX = 100

def get_tool_dirs():
    dirs = []
    for d in sorted(SITE_DIR.iterdir()):
        if d.name in SKIP_DIRS or d.name.startswith('.'): continue
        if not d.is_dir(): continue
        if (d / 'index.html').exists():
            dirs.append(d.name)
    return dirs

def fix_faq_duplicate(html):
    """
    修复真正的FAQ重复：emoji FAQ h2 + 空/几乎空的纯文本FAQ h2。
    删除空的纯文本FAQ区块（只有h2没有内容的section/div）。
    """
    # 找所有h2
    h2s = list(re.finditer(r'<h2[^>]*>(.*?)</h2>', html, re.DOTALL))
    
    # 分类
    emoji_faq_h2s = []  # ❓常见问题 / 📖常见问题 等
    plain_faq_h2s = []  # 常见问题 / FAQ 不带emoji
    
    for m in h2s:
        text = m.group(1).strip()
        if re.search(r'^[❓📖ℹ️💡🔍📚❔]\s*(常见问题|FAQ)', text):
            emoji_faq_h2s.append(m)
        elif re.match(r'^\s*(常见问题|FAQ|Frequently Asked Questions)\s*$', text):
            plain_faq_h2s.append(m)
    
    if not emoji_faq_h2s or not plain_faq_h2s:
        return html, 0
    
    changes = 0
    for plain in plain_faq_h2s:
        # 检查这个plain FAQ h2所在的区块是否为空
        # 向前找最近的<section或<div class="section/faq/card"
        pos = plain.start()
        before = html[:pos]
        
        # 找区块起始标签
        sec_start = pos
        for pattern in [r'<section[^>]*>', r'<div[^>]*class="[^"]*(?:section|faq|card|info)[^"]*"[^>]*>']:
            matches = list(re.finditer(pattern, before, re.IGNORECASE))
            if matches:
                sec_start = matches[-1].start()
                break
        
        # 从区块起始到h2之间的内容
        pre_content = html[sec_start:pos]
        # 找h2之后到区块结束之间的内容
        after = html[plain.end():]
        
        # 检查h2后面是否几乎为空（只有空白或很少内容就到下一个标签或区块结束）
        # 往前找</section>或</div>闭合
        depth = len(re.findall(r'<(?:section|div)[^>]*>', pre_content, re.IGNORECASE))
        depth -= len(re.findall(r'</(?:section|div)>', pre_content, re.IGNORECASE))
        depth += 1  # h2所在的区块
        
        sec_end = plain.end()
        for m in re.finditer(r'</?(?:section|div)[^>]*>', after, re.IGNORECASE):
            tag = m.group()
            if tag.startswith('</'):
                depth -= 1
            else:
                depth += 1
            if depth <= 0:
                sec_end = plain.end() + m.end()
                break
        
        # 提取h2到区块结束之间的内容
        between = html[plain.end():sec_end].strip()
        # 如果之间只有空白或很短的文本（<20字符），认为是空FAQ
        if len(between) < 20:
            removed = html[sec_start:sec_end]
            if len(removed) < 3000:  # 安全检查
                html = html[:sec_start] + html[sec_end:]
                changes += 1
    
    return html, changes

def fix_empty_divs(html):
    """删除无意义的空div（无id、无data-属性）"""
    def should_remove(m):
        attrs = m.group(1)
        if re.search(r'\bid\s*=', attrs, re.IGNORECASE):
            return False
        if re.search(r'\bdata-', attrs, re.IGNORECASE):
            return False
        # 检查是否有class
        if not re.search(r'\bclass\s*=', attrs, re.IGNORECASE):
            return True
        # 有class但检查是不是语义化class
        cls_match = re.search(r'class\s*=\s*"([^"]*)"', attrs, re.IGNORECASE)
        if cls_match:
            cls = cls_match.group(1).strip()
            # 保留有明确用途的class
            if cls in ('toast', 'modal', 'overlay', 'spinner', 'loader', 'tooltip', 'popup'):
                return False
        return True
    
    new_html, n = re.subn(
        r'<div([^>]*)>\s*</div>',
        lambda m: '' if should_remove(m) else m.group(0),
        html, flags=re.IGNORECASE
    )
    return new_html, n

def main():
    tools = get_tool_dirs()
    print(f"扫描 {len(tools)} 个工具目录...")
    
    stats = {'faq_fixed': 0, 'div_fixed': 0, 'total_files': 0}
    fixed_files = []
    
    for tool in tools:
        if stats['total_files'] >= MAX_FIX:
            print(f"已达上限 {MAX_FIX}，停止")
            break
        
        path = SITE_DIR / tool / 'index.html'
        with open(path, 'r', encoding='utf-8') as f:
            html = f.read()
        
        original = html
        file_changes = []
        
        # 1. FAQ重复修复
        html, n = fix_faq_duplicate(html)
        if n:
            stats['faq_fixed'] += n
            file_changes.append(f'FAQ-{n}')
        
        # 2. 空div清理
        html, n = fix_empty_divs(html)
        if n:
            stats['div_fixed'] += n
            file_changes.append(f'DIV-{n}')
        
        if html != original:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(html)
            stats['total_files'] += 1
            fixed_files.append(f"{tool}: {', '.join(file_changes)}")
    
    print(f"\n=== 批量修复完成 ===")
    print(f"修复文件数: {stats['total_files']}")
    print(f"  FAQ重复: {stats['faq_fixed']} 处")
    print(f"  空div: {stats['div_fixed']} 处")
    
    if fixed_files:
        print("\n修复详情（前20条）:")
        for f in fixed_files[:20]:
            print(f"  {f}")
        if len(fixed_files) > 20:
            print(f"  ... 还有 {len(fixed_files)-20} 个")
    
    result = {'stats': stats, 'fixed': fixed_files}
    with open(SITE_DIR / 'quality' / 'batch_fix_result.json', 'w') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

if __name__ == '__main__':
    main()