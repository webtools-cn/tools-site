#!/usr/bin/env python3
"""
批量优化英文工具页的 meta title，加入 "Free Online" 关键词
策略：
- 标题前加 "Free Online"（如果两者都缺）
- 标题前加 "Free"（如果缺 free 但有 online）
- 在标题中插入 "Online"（如果缺 online 但有 free）
- 保持标题长度在 60 字符以内（Google 显示限制）
"""

import os
import re
import glob
from pathlib import Path

EN_DIR = Path("/home/chison/tools-site/en")

def analyze_title(title):
    """分析 title 的关键词覆盖情况"""
    title_lower = title.lower()
    has_free = "free" in title_lower
    has_online = "online" in title_lower
    return has_free, has_online

def optimize_title(title, tool_name=""):
    """智能优化 title"""
    has_free, has_online = analyze_title(title)
    
    if has_free and has_online:
        return None  # 不需要优化
    
    # 清理 title（去掉已有的前缀模式）
    clean_title = title.strip()
    
    if not has_free and not has_online:
        # 两者都缺 → 前加 "Free Online"
        new_title = f"Free Online {clean_title}"
    elif not has_free:
        # 缺 free 但有 online → 前加 "Free"
        new_title = f"Free {clean_title}"
    else:
        # 缺 online 但有 free → 在合适位置插入 "Online"
        # 策略：如果标题以工具名开头，在工具名后加 "Online"
        new_title = f"Free Online {clean_title.replace('Free ', '')}"
    
    # 截断到 60 字符以内（Google 显示限制）
    if len(new_title) > 60:
        new_title = new_title[:57] + "..."
    
    return new_title

def process_file(filepath):
    """处理单个 HTML 文件"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return False, f"Read error: {e}"
    
    # 查找 title 标签
    title_match = re.search(r'<title>([^<]*)</title>', content, re.IGNORECASE)
    if not title_match:
        return False, "No title tag found"
    
    old_title = title_match.group(1)
    new_title = optimize_title(old_title)
    
    if new_title is None:
        return False, "Already optimized"
    
    # 替换 title
    new_content = content.replace(f"<title>{old_title}</title>", f"<title>{new_title}</title>", 1)
    
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True, f"'{old_title}' → '{new_title}'"
    except Exception as e:
        return False, f"Write error: {e}"

def main():
    stats = {
        "total": 0,
        "optimized": 0,
        "already_ok": 0,
        "errors": 0,
    }
    
    # 找到所有英文工具页的 index.html
    html_files = sorted(EN_DIR.glob("*/index.html"))
    
    print(f"Found {len(html_files)} HTML files to process")
    print("=" * 80)
    
    for filepath in html_files:
        stats["total"] += 1
        success, msg = process_file(filepath)
        
        if success:
            stats["optimized"] += 1
            tool_dir = filepath.parent.name
            print(f"[OPT] {tool_dir}: {msg}")
        elif "Already optimized" in msg:
            stats["already_ok"] += 1
        else:
            stats["errors"] += 1
            tool_dir = filepath.parent.name
            print(f"[ERR] {tool_dir}: {msg}")
    
    print("=" * 80)
    print(f"Total: {stats['total']}")
    print(f"Optimized: {stats['optimized']}")
    print(f"Already OK: {stats['already_ok']}")
    print(f"Errors: {stats['errors']}")

if __name__ == "__main__":
    main()
