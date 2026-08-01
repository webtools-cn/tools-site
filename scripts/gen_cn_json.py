#!/usr/bin/env python3
"""重新生成完整的tools-data-cn.json，覆盖所有CN工具页"""
import glob, json, re, os

os.chdir('/home/chison/tools-site')

# 分类关键词映射
CAT_MAP = {
    'json': 'dev-tools', 'base64': 'dev-tools', 'base32': 'dev-tools', 'base58': 'dev-tools', 'base85': 'dev-tools',
    'encode': 'dev-tools', 'decode': 'dev-tools', 'hash': 'dev-tools', 'encrypt': 'dev-tools', 'decrypt': 'dev-tools',
    'regex': 'dev-tools', 'cron': 'dev-tools', 'sql': 'dev-tools', 'html': 'dev-tools', 'css': 'dev-tools',
    'javascript': 'dev-tools', 'js-': 'dev-tools', 'api': 'dev-tools', 'jwt': 'dev-tools', 'url': 'dev-tools',
    'unicode': 'dev-tools', 'ascii': 'dev-tools', 'utf': 'dev-tools', 'binary': 'dev-tools', 'hex': 'dev-tools',
    'uuid': 'dev-tools', 'lorem': 'dev-tools', 'code': 'dev-tools', 'git': 'dev-tools', 'diff': 'dev-tools',
    'markdown': 'dev-tools', 'yaml': 'dev-tools', 'toml': 'dev-tools', 'xml': 'dev-tools', 'csv': 'dev-tools',
    'color': 'color-tools', 'gradient': 'color-tools', 'palette': 'color-tools', 'cmyk': 'color-tools',
    'rgb': 'color-tools', 'hsl': 'color-tools', 'pantone': 'color-tools',
    'image': 'image-tools', 'img': 'image-tools', 'photo': 'image-tools', 'picture': 'image-tools',
    'png': 'image-tools', 'jpg': 'image-tools', 'jpeg': 'image-tools', 'webp': 'image-tools',
    'svg': 'image-tools', 'gif': 'image-tools', 'ico': 'image-tools', 'favicon': 'image-tools',
    'watermark': 'image-tools', 'resize': 'image-tools', 'crop': 'image-tools', 'compress': 'image-tools',
    'screenshot': 'image-tools', 'qr': 'image-tools', 'barcode': 'image-tools',
    'pdf': 'pdf-tools', 'text': 'text-tools', 'word': 'text-tools', 'char': 'text-tools',
    'string': 'text-tools', 'case': 'text-tools', 'slug': 'text-tools', 'pinyin': 'text-tools',
    'translate': 'text-tools', 'spell': 'text-tools', 'grammar': 'text-tools',
    'calc': 'calc-tools', 'calculator': 'calc-tools', 'convert': 'conv-tools', 'converter': 'conv-tools',
    'math': 'math-tools', 'number': 'math-tools', 'fraction': 'math-tools', 'percentage': 'math-tools',
    'roman': 'math-tools', 'prime': 'math-tools', 'fibonacci': 'math-tools',
    'password': 'security-tools', 'token': 'security-tools', 'ssl': 'security-tools', 'cert': 'security-tools',
    'firewall': 'security-tools', 'vpn': 'security-tools', '2fa': 'security-tools',
    'audio': 'audio-tools', 'mp3': 'audio-tools', 'wav': 'audio-tools', 'midi': 'audio-tools',
    'video': 'video-tools', 'mp4': 'video-tools', 'gif-': 'video-tools',
    'finance': 'finance-tools', 'tax': 'finance-tools', 'invest': 'finance-tools', 'loan': 'finance-tools',
    'mortgage': 'finance-tools', 'interest': 'finance-tools', 'stock': 'finance-tools',
    'crypto': 'finance-tools', 'bitcoin': 'finance-tools', '401k': 'finance-tools', 'ira': 'finance-tools',
    'roi': 'finance-tools', 'compound': 'finance-tools', 'salary': 'finance-tools', 'tip': 'finance-tools',
    'health': 'health-tools', 'bmi': 'health-tools', 'calorie': 'health-tools', 'heart': 'health-tools',
    'blood': 'health-tools', 'pregnancy': 'health-tools', 'body': 'health-tools',
    'seo': 'seo-tools', 'meta': 'seo-tools', 'sitemap': 'seo-tools', 'robots': 'seo-tools',
    'redirect': 'seo-tools', 'canonical': 'seo-tools', 'open-graph': 'seo-tools',
    'dns': 'network-tools', 'ip': 'network-tools', 'ping': 'network-tools', 'port': 'network-tools',
    'speed': 'network-tools', 'whois': 'network-tools', 'domain': 'network-tools', 'ssl-check': 'network-tools',
    'generator': 'gen-tools', 'random': 'gen-tools', 'name': 'gen-tools', 'fake': 'gen-tools',
    'mock': 'gen-tools', 'avatar': 'gen-tools', 'logo': 'gen-tools', 'banner': 'gen-tools',
    'badge': 'gen-tools', 'certificate': 'gen-tools', 'invoice': 'gen-tools', 'resume': 'gen-tools',
    'letter': 'gen-tools', 'email': 'gen-tools', 'signature': 'gen-tools',
    'design': 'design-tools', 'figma': 'design-tools', 'shadow': 'design-tools', 'border': 'design-tools',
    'animation': 'design-tools', 'bezier': 'design-tools', 'mesh': 'design-tools',
    'age': 'life-tools', 'date': 'life-tools', 'time': 'life-tools', 'countdown': 'life-tools',
    'timer': 'life-tools', 'stopwatch': 'life-tools', 'alarm': 'life-tools', 'calendar': 'life-tools',
    'weather': 'life-tools', 'unit': 'life-tools', 'temperature': 'life-tools', 'weight': 'life-tools',
    'kitchen': 'kitchen-tools', 'recipe': 'kitchen-tools', 'cooking': 'kitchen-tools', 'bake': 'kitchen-tools',
    'travel': 'travel-tools', 'flight': 'travel-tools', 'distance': 'travel-tools', 'timezone': 'travel-tools',
    'currency': 'travel-tools', 'jetlag': 'travel-tools',
    'sport': 'sports-tools', 'fitness': 'sports-tools', 'workout': 'sports-tools', 'run': 'sports-tools',
    'study': 'study-tools', 'flashcard': 'study-tools', 'quiz': 'study-tools', 'note': 'study-tools',
    'pomodoro': 'productivity-tools', 'todo': 'productivity-tools', 'task': 'productivity-tools',
    'habit': 'productivity-tools', 'focus': 'productivity-tools', 'journal': 'productivity-tools',
    'decision': 'productivity-tools', 'brainstorm': 'productivity-tools',
    'fun': 'fun-tools', 'game': 'fun-tools', '2048': 'fun-tools', 'dice': 'fun-tools',
    'coin': 'fun-tools', 'wheel': 'fun-tools', 'meme': 'fun-tools', 'joke': 'fun-tools',
    'business': 'business-tools', 'contract': 'business-tools', 'nda': 'business-tools',
    'office': 'office-tools', 'doc': 'office-tools', 'spreadsheet': 'office-tools', 'slide': 'office-tools',
    'science': 'science-tools', 'physics': 'science-tools', 'chemistry': 'science-tools',
    'education': 'education-tools', 'learn': 'education-tools', 'teach': 'education-tools',
}

CAT_ICONS = {
    'dev-tools': '💻', 'utility-tools': '🔧', 'finance-tools': '💰', 'text-tools': '📝',
    'design-tools': '🎨', 'health-tools': '❤️', 'image-tools': '🖼️', 'calc-tools': '🧮',
    'media-tools': '🎬', 'fun-tools': '🎮', 'office-tools': '📊', 'pdf-tools': '📄',
    'math-tools': '📐', 'security-tools': '🔒', 'creative-tools': '🎭', 'network-tools': '🌐',
    'life-tools': '🏠', 'seo-tools': '🔍', 'productivity-tools': '⏱️', 'conv-tools': '🔄',
    'audio-tools': '🎵', 'business-tools': '💼', 'converter-tools': '🔄', 'gen-tools': '⚙️',
    'developer-tools': '💻', 'travel-tools': '✈️', 'education-tools': '📚', 'kitchen-tools': '🍳',
    'css-tools': '🎨', 'color-tools': '🎨', 'sports-tools': '⚽', 'study-tools': '📖',
    'science-tools': '🔬', 'video-tools': '🎥', 'data-tools': '📊', 'generator-tools': '⚙️',
    'new-tools': '🆕', 'check-tools': '✅',
}

def get_cat(slug):
    """根据slug推断分类"""
    slug_lower = slug.lower()
    for key, cat in CAT_MAP.items():
        if key in slug_lower:
            return cat
    return 'utility-tools'

def extract_info(filepath, slug):
    """从HTML提取工具信息"""
    try:
        content = open(filepath, 'r', encoding='utf-8', errors='ignore').read()
    except:
        return None
    
    # 提取title
    title_match = re.search(r'<title>([^<]+)</title>', content)
    title = title_match.group(1).strip() if title_match else slug.replace('-', ' ').title()
    # 去掉 " - Free ToolBase" 等后缀
    title = re.sub(r'\s*[-|–]\s*(Free ToolBase|在线小工具|免费在线工具).*$', '', title)
    
    # 提取description
    desc_match = re.search(r'<meta\s+name="description"\s+content="([^"]+)"', content)
    desc = desc_match.group(1).strip() if desc_match else ''
    # 截取到40字符
    if len(desc) > 40:
        desc = desc[:37] + '...'
    
    if not desc:
        desc = title[:40] if len(title) > 40 else title
    
    # 提取分类（从Schema或页面内容）
    cat_match = re.search(r'"applicationCategory":\s*"([^"]+)"', content)
    if cat_match:
        app_cat = cat_match.group(1).lower()
        if 'developer' in app_cat: cat = 'dev-tools'
        elif 'utilit' in app_cat: cat = 'utility-tools'
        elif 'financ' in app_cat: cat = 'finance-tools'
        elif 'design' in app_cat: cat = 'design-tools'
        elif 'health' in app_cat: cat = 'health-tools'
        elif 'educat' in app_cat: cat = 'education-tools'
        elif 'busines' in app_cat: cat = 'business-tools'
        elif 'product' in app_cat: cat = 'productivity-tools'
        else: cat = get_cat(slug)
    else:
        cat = get_cat(slug)
    
    icon = CAT_ICONS.get(cat, '📁')
    href = slug + '/'
    
    return [icon, title, desc, href]

# 扫描所有CN工具页
data = {}
skipped = 0
for f in sorted(glob.glob('*/index.html')):
    if f == 'index.html' or f.startswith('en/'):
        continue
    slug = f.replace('/index.html', '')
    # 跳过非工具页
    if slug in ('css', 'js', 'scripts', 'quality', '.git', '.gsc-data', '.github'):
        skipped += 1
        continue
    
    info = extract_info(f, slug)
    if not info:
        skipped += 1
        continue
    
    cat = get_cat(slug)
    if cat not in data:
        data[cat] = []
    data[cat].append(info)

# 按每个分类内工具数排序
total = sum(len(v) for v in data.values())
print(f'生成CN JSON: {total} 个工具, {len(data)} 个分类, 跳过 {skipped}')

# 保存
with open('tools-data-cn.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f'已保存 tools-data-cn.json')
