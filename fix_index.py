#!/usr/bin/env python3
"""Fix index.html: remove duplicate cards, add missing tools.
Uses line-based approach for reliability."""
import re, os

INDEX = "/opt/project/index.html"
EN_INDEX = "/opt/project/en/index.html"

def find_tool_card_blocks(content):
    """Find all tool-card blocks with their href."""
    blocks = []
    pattern = re.compile(r'(<div class="tool-card" data-cats="[^"]*">.*?</div>\s*)(?=<div class="tool-card"|\s*</div>|\s*$)', re.DOTALL)
    
    for m in pattern.finditer(content):
        block = m.group(1)
        # Extract href
        href_m = re.search(r'href="([^"]+)/">', block)
        if href_m:
            href = href_m.group(1)
            # Normalize (remove ../ prefix)
            href_clean = href.replace('../', '')
            blocks.append((m.start(), m.end(), block, href_clean))
    
    return blocks

def add_tool_card(content, insert_after_pos, card_html):
    """Add a card after the given position."""
    return content[:insert_after_pos] + "\n" + card_html + content[insert_after_pos:]

# ============================================================
# Fix index.html
# ============================================================
with open(INDEX) as f:
    content = f.read()

original = content

# First, let's just find duplicates by looking at hrefs
href_positions = {}
for m in re.finditer(r'href="([^"]+)/">立即使用</a>', content):
    href = m.group(1)
    if href not in href_positions:
        href_positions[href] = []
    href_positions[href].append(m.start())

duplicate_hrefs = {k: v for k, v in href_positions.items() if len(v) > 1}
print(f"Found {len(duplicate_hrefs)} duplicate tools")

# For each duplicate, remove all but the first occurrence
removed_count = 0
for href, positions in sorted(duplicate_hrefs.items()):
    # Keep the first occurrence, remove the rest
    for pos in sorted(positions[1:], reverse=True):  # Remove from end to start
        # Find the tool-card div that contains this href
        card_start = content.rfind('<div class="tool-card"', 0, pos)
        if card_start < 0:
            continue
        
        # Find where this card ends - look for the next tool-card or a closing pattern
        # Cards are separated by newlines. The card pattern is:
        # <div class="tool-card" ...>
        #   ... <a href=".../">立即使用</a>
        # </div>
        # Followed by either another card or other content
        
        # Find the closing </div> of this card
        # Since cards can contain nested divs (from tool-meta), count div nesting
        search_start = card_start
        depth = 0
        card_end = -1
        for i in range(card_start, min(card_start + 2000, len(content))):
            if content[i:i+5] == '<div ' or content[i:i+4] == '<div>':
                depth += 1
            elif content[i:i+6] == '</div>':
                depth -= 1
                if depth == 0:
                    card_end = i + 6
                    break
        
        if card_end < 0:
            continue
        
        # Remove the card
        # Also remove preceding whitespace/newline
        while card_start > 0 and content[card_start-1] in ' \n\r\t':
            card_start -= 1
        
        content = content[:card_start] + content[card_end:]
        removed_count += 1
        print(f"  Removed duplicate '{href}'")

print(f"\nTotal cards removed: {removed_count}")

# Now add missing tool cards
# Find insertion point - before the </div> that closes tools-grid
tools_grid_end = content.find('</div>', content.find('class="tools-grid"'))
# Actually find the end of tools-grid by looking for the closing </div> after the last card
last_card_pos = content.rfind('<div class="tool-card"')
if last_card_pos > 0:
    # Find end of this card
    search_start = last_card_pos
    depth = 0
    for i in range(last_card_pos, min(last_card_pos + 2000, len(content))):
        if content[i:i+5] == '<div ' or content[i:i+4] == '<div>':
            depth += 1
        elif content[i:i+6] == '</div>':
            depth -= 1
            if depth == 0:
                insert_pos = i + 6
                break
    else:
        insert_pos = len(content)
else:
    insert_pos = len(content)

# Missing tools that already have HTML pages
missing = [
    {
        "href": "heatmap-generator",
        "cats": "设计工具",
        "icon": "🗺️",
        "title": "热力图生成器 · Heatmap Generator",
        "desc": "免费在线热力图生成器，将数据矩阵可视化为彩色热力图。支持多种配色方案、自定义数据标签、高清PNG导出。纯前端本地生成，数据不上传服务器。适合数据分析、可视化报告和学术研究。",
        "tags": "设计工具"
    },
    {
        "href": "http-request-builder",
        "cats": "开发者工具",
        "icon": "🌐",
        "title": "HTTP请求生成器 · HTTP Request Builder",
        "desc": "免费在线HTTP请求测试工具，支持GET/POST/PUT/DELETE/PATCH等请求方法。自定义请求头、请求体、查询参数，实时查看响应状态码、响应头和响应体。纯前端本地处理，适合API调试。",
        "tags": "开发者工具"
    },
    {
        "href": "http-status-codes",
        "cats": "开发者工具",
        "icon": "📋",
        "title": "HTTP状态码查询 · HTTP Status Codes",
        "desc": "免费在线HTTP状态码查询工具，完整收录1xx-5xx状态码。支持分类浏览和关键词搜索，每个状态码附详细说明和常见场景。适合Web开发者日常调试参考。",
        "tags": "开发者工具"
    },
    {
        "href": "http-to-curl",
        "cats": "开发者工具",
        "icon": "🔧",
        "title": "HTTP转cURL命令 · HTTP to cURL",
        "desc": "免费在线HTTP请求转cURL命令生成器，支持GET/POST/PUT/DELETE等7种方法。填写URL、请求头和请求体，一键生成cURL命令并复制。纯前端处理，数据不上传服务器。",
        "tags": "开发者工具"
    }
]

# Build cards
new_cards = ""
for t in missing:
    card = f"""    <div class="tool-card" data-cats="{t['cats']}">
      <div class="icon">{t['icon']}</div>
      <h3>{t['title']}</h3>
      <p>{t['desc']}</p>
      <div class="tool-meta"><span>{t['tags']}</span><span class="new-tag">NEW</span></div>
      <a href="{t['href']}/">立即使用</a>
    </div>"""
    new_cards += card + "\n"

content = content[:insert_pos] + "\n" + new_cards + content[insert_pos:]

# Save
with open(INDEX, 'w') as f:
    f.write(content)

print(f"\nAdded {len(missing)} new tool cards")
print(f"Original size: {len(original)} bytes -> {len(content)} bytes")

# Verify
hrefs = re.findall(r'href="([^"]+)/">立即使用</a>', content)
from collections import Counter
dupes = {k:v for k,v in Counter(hrefs).items() if v > 1}
cn_dirs = set(d for d in os.listdir("/opt/project") if os.path.isdir(os.path.join("/opt/project", d)) and not d.startswith('.') and d not in ['en', 'chrome-extension', 'quality-reports', 'libs', 'assets'])
index_tools = set(hrefs)
missing_still = sorted(cn_dirs - index_tools)
print(f"\nVerification:")
print(f"  Tool links in index: {len(hrefs)}")
print(f"  Unique tools: {len(set(hrefs))}")
print(f"  CN dirs: {len(cn_dirs)}")
print(f"  Remaining duplicates: {dupes}")
print(f"  Still missing from index (excluding pycache/blog): {[m for m in missing_still if not m.startswith('__') and m != 'blog']}")
