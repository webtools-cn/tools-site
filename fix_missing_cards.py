#!/usr/bin/env python3
"""Auto-generate missing tool cards and insert into index.html"""
import os, re

# Read existing index
with open('index.html') as f:
    content = f.read()

# Find all existing card slugs
card_slugs = set()
for m in re.finditer(r'<a href="([^"]+)/"', content):
    slug = m.group(1).strip()
    if slug and not (slug.startswith('http://') or slug.startswith('https://')) and slug != 'en':
        card_slugs.add(slug)

# Get all tool dirs (exclude non-tool dirs)
EXCLUDE = {'en','chrome-extension','quality-reports','libs','assets','css','js','images','scripts','blog'}
dirs = [d for d in os.listdir('.') if os.path.isdir(d) and not d.startswith('.') and d not in EXCLUDE]

missing = [d for d in dirs if d not in card_slugs]
print(f'Missing cards: {len(missing)}')

# Category classification
def classify(d, tool_html=''):
    d_lower = d.lower()
    if 'json' in d_lower or 'http' in d_lower or 'webhook' in d_lower or 'regex' in d_lower or 'port' in d_lower or 'hash' in d_lower or 'lint' in d_lower or 'base64' in d_lower or 'protobuf' in d_lower or 'curl' in d_lower or 'css' in d_lower or 'html' in d_lower or 'tailwind' in d_lower or 'react' in d_lower or 'xml' in d_lower or 'yaml' in d_lower:
        return 'dev'
    if 'pdf' in d_lower:
        return 'pdf'
    if any(x in d_lower for x in ['image','jpg','png','webp','gif','heic','bmp','tiff','avif','svg','remove-bg','round-corners','upscale']):
        return 'image'
    if any(x in d_lower for x in ['text','sentence','rewriter','title-case','progress-bar','speed-reading','reading']):
        return 'text'
    if any(x in d_lower for x in ['color','hex','hsl','pantone','gradient','neon','banner','3d','mesh','palette']):
        return 'design'
    if any(x in d_lower for x in ['audio','binaural','drum','chord','converter']):
        return 'media'
    if any(x in d_lower for x in ['chess','sudoku','crossword','emoji','generator','gif-creator']):
        return 'creative'
    if any(x in d_lower for x in ['calculator','csv','convert']):
        return 'calc'
    return 'utility'

# Category icons
CAT_ICONS = {
    'dev': '💻', 'utility': '🔧', 'pdf': '📄', 'image': '🖼️',
    'design': '🎨', 'text': '📝', 'office': '📊', 'security': '🔒',
    'creative': '✨', 'calc': '🧮', 'media': '🎵', 'health': '💪',
    'math': '📐', 'fun': '🎮'
}
CAT_LABELS = {
    'dev': '开发工具', 'utility': '实用工具', 'pdf': 'PDF工具', 'image': '图片工具',
    'design': '设计工具', 'text': '文字工具', 'office': '办公工具', 'security': '安全工具',
    'creative': '创意工具', 'calc': '计算工具', 'media': '媒体工具', 'health': '健康工具',
    'math': '数学工具', 'fun': '趣味工具'
}

EMOJI_FALLBACKS = ['🔧','📌','⚡','🛠️','📎','🔗','💡','🎯','📦','🔮','⭐','🔥','💎','🚀','🎪','🎲','📋','🧩','🔌','🎛️','📡','🗺️','🪄','📯','🎼','🖲️','🔬','📐','🧪','⚙️']

new_cards = []
for i, d in enumerate(sorted(missing)):
    idx_path = os.path.join(d, 'index.html')
    title = d.replace('-', ' ').title()
    desc = ''
    emoji = EMOJI_FALLBACKS[i % len(EMOJI_FALLBACKS)]
    
    if os.path.exists(idx_path):
        with open(idx_path) as f:
            th = f.read()
        # Title - prefer og:title then <title>
        tm = re.search(r'<meta property="og:title" content="([^"]+)"', th)
        if not tm:
            tm = re.search(r'<title>(.*?)</title>', th)
        if tm:
            t = tm.group(1)
            t = re.sub(r'\s*[-|·]\s*.*', '', t).strip()
            t = re.sub(r'免费在线\s*', '', t).strip()
            if t and len(t) > 1:
                title = t
        
        # Description
        dm = re.search(r'<meta name="description" content="([^"]+)"', th)
        if not dm:
            dm = re.search(r'<meta property="og:description" content="([^"]+)"', th)
        if dm:
            desc = dm.group(1)[:200]
        
        # Try to get icon from tool html
        em_m = re.search(r'<div class="icon">(.)</div>', th)
        if em_m:
            emoji = em_m.group(1)
    
    cat = classify(d)
    
    card = f'''    <div class="tool-card" data-cats="{cat}">
      <div class="icon">{emoji}</div>
      <h3>{title}</h3>
      <p>{desc}</p>
      <div class="tool-meta"><span>{CAT_LABELS[cat]}</span></div>
      <a href="{d}/">立即使用</a>
    </div>'''
    new_cards.append(card)

# Insert cards before showMoreWrap
insert_pos = content.find('<div id="showMoreWrap"')
if insert_pos < 0:
    insert_pos = content.find('</div>\n  <div class="no-results"')

new_cards_str = '\n'.join(new_cards) + '\n  '
new_content = content[:insert_pos] + new_cards_str + content[insert_pos:]

with open('index.html', 'w') as f:
    f.write(new_content)

print(f'Added {len(new_cards)} cards to index.html')

# Also update the meta description count
import re
card_count = len(re.findall(r'data-cats=', new_content))
print(f'Total cards now: {card_count}')
