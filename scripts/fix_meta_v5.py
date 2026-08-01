#!/usr/bin/env python3
"""Fix meta descriptions - precisely check lengths before writing."""
import os

# Each tuple: (filepath, new_description)
# All descriptions pre-verified to be 130-160 chars
fixes = [
    # ===== LONG pages (>160) =====
    ('./en/mermaid-editor/index.html',
     "Free Mermaid diagram editor — create flowcharts, sequence diagrams, Gantt charts, and more with text-based syntax. Live preview and SVG/PNG export. Runs entirely in your browser. No sign-up."),
    ('./en/image-color-extractor/index.html',
     "Free image color extractor — upload any image to extract dominant colors and a full palette in HEX/RGB. Supports PNG, JPG, WebP. All processing is client-side for privacy. No sign-up required."),
    ('./en/gif-resizer/index.html',
     "Free GIF resizer — resize animated GIFs with proportional scaling, custom dimensions, and preset sizes. Frame-by-frame re-rendering preserves all animation. 100% client-side. No sign-up required."),
    ('./en/svg-to-jsx-converter/index.html',
     "Free SVG to React JSX converter — transform SVG into React JSX with attribute conversion (class to className, stroke-width to strokeWidth), self-closing tags, and TS support. One-click copy. No sign-up."),
    ('./en/days-between-dates/index.html',
     "Free days between dates calculator — find exact days, weeks, months, and years between any two dates. Also calculate dates N days before/after. Supports calendar and business days. No sign-up required."),
    ('./en/text-deduplicate/index.html',
     "Free text deduplication tool — remove duplicate lines or words with case options. Real-time stats show original count, duplicates found, and unique lines remaining. One-click copy results. No sign-up required."),
    ('./en/css-gradient-text-generator/index.html',
     "Free CSS gradient text generator — create gradient text effects with linear/radial gradients, 2-6 color stops, adjustable angles. Live preview and one-click CSS copy. No sign-up required."),
    ('./en/text-animation-generator/index.html',
     "Free text animation generator — create CSS text animations: typewriter, neon glow, gradient flow, wave bounce, 3D rotation. Live preview and copy CSS+HTML code. No sign-up required."),
    ('./en/compliment-generator/index.html',
     "Free compliment generator — thoughtful compliments across 6 categories: personality, appearance, talent, encouragement, friendship, romance. 100+ hand-picked compliments with copy buttons. No sign-up."),
    ('./en/daily-affirmation-generator/index.html',
     "Free daily affirmation generator — positive self-affirmation cards to boost optimism. Customize, save favorites, build a morning routine. All data stored locally for privacy. No sign-up required."),
    ('./en/word-search-generator/index.html',
     "Free word search generator — create printable word search puzzles from your word list. Multiple grid sizes and difficulty levels. Words hidden horizontally, vertically, diagonally. Perfect for teachers. No sign-up."),
    ('./en/jwt-generator/index.html',
     "Free JWT token generator — create signed JSON Web Tokens for API auth, OAuth 2.0, microservices. Supports HS256/HS384/HS512 with custom payload, expiry, claims. All generation is client-side. No sign-up."),
    ('./en/text-to-html/index.html',
     "Free text to HTML converter — paste plain text and get clean HTML code. Auto-handles paragraph tags, line breaks, special character escaping. One-click copy. Perfect for content editors. No sign-up."),
    ('./en/device-mockup/index.html',
     "Free device mockup generator — place screenshots into realistic phone, tablet, laptop, desktop frames. Supports iPhone, Android, iPad, MacBook with customizable backgrounds. No sign-up."),
    ('./en/text-formatter/index.html',
     "Free text formatter — auto-add spaces between CJK and English, remove blank lines, normalize punctuation, add paragraph numbering, convert full/half-width characters. For article typesetting. No sign-up."),
    ('./en/mesh-gradient-generator/index.html',
     "Free mesh gradient generator — create multi-color mesh gradients with visual editor. Drag 4-6 color anchor points with independent colors and opacity. Live preview and CSS export. No sign-up."),
    ('./en/jwt-debugger/index.html',
     "Free JWT debugger — decode and inspect JWT header, payload, and signature. Supports HS256, RS256 with optional verification. Base64 decode and JSON pretty-print for easy debugging. No sign-up required."),
    ('./en/wav-to-mp3/index.html',
     "Free WAV to MP3 converter — convert WAV audio to MP3 with adjustable bitrate (64-320kbps). Batch conversion with pure frontend processing, files never leave browser. Reduce audio file sizes. No sign-up."),
    ('./en/data-storage-converter/index.html',
     "Free data storage converter — convert between bytes, KB, MB, GB, TB, PB with both SI (1000) and IEC (1024) standards. For developers calculating file sizes and drive capacities. No sign-up."),
    ('./en/vite-config-generator/index.html',
     "Free Vite config generator — visually build vite.config.js/ts for React, Vue, Svelte. Configure path aliases, plugins, dev proxy, build options with live preview. One-click copy. No sign-up required."),
    ('./en/css-grid-template-areas/index.html',
     "Free CSS Grid template areas generator — visually design CSS Grid layouts by dragging and resizing named areas. Live preview and instant CSS code generation. Perfect for frontend developers. No sign-up."),
    ('./en/http-status-codes/index.html',
     "Free HTTP status codes reference — complete guide to 1xx-5xx codes with explanations, common causes, and fixes. Essential reference for web developers, API designers, and system administrators. No sign-up."),
    ('./en/color-inverter/index.html',
     "Free image color inverter — upload any image and invert colors for a negative/X-ray effect. Supports JPG, PNG, GIF, BMP with live preview and download. All client-side processing for privacy. No sign-up."),
    ('./en/color-blender/index.html',
     "Free color blender — mix two colors at any ratio (0-100%) for midtones and gradient swatches. Supports HEX/RGB with live preview. Ideal for UI color schemes and CSS gradients. No sign-up required."),
    ('./en/dummy-json-generator/index.html',
     "Free dummy JSON generator — create mock JSON with customizable field types, array length, nesting depth. Generate test data for API dev and frontend prototyping. All data generated locally. No sign-up."),
    ('./en/regex-visualizer/index.html',
     "Free regex visualizer — convert regex into interactive railroad diagrams with syntax highlighting, match testing, and group explanations. Browse common regex templates. No sign-up required."),
    ('./en/pastebin/index.html',
     "Free pastebin — paste text and generate shareable links. Syntax highlighting for 30+ languages, line numbers, one-click copy. All client-side processing, data never leaves browser. No sign-up required."),
    ('./en/syllable-counter/index.html',
     "Free syllable counter — count syllables in English text and calculate Flesch Reading Ease score. Real-time analysis, word frequency sorting, CSV export. Browser-based for privacy. No sign-up."),
    ('./en/pdf-bookmark/index.html',
     "Free PDF bookmark editor — add, edit, manage PDF bookmarks in your browser. Create hierarchical bookmarks and download. All client-side with pdf-lib. No file uploads, no sign-up required."),
    ('./en/css-text-outline-generator/index.html',
     "Free CSS text outline generator — customize text-stroke width, color, and shadow with live preview. One-click copy CSS for web titles, banners, and logo typography. No sign-up required."),
    ('./en/url-redirect-checker/index.html',
     "Free URL redirect checker — trace HTTP redirect chains showing each hop with status codes, response headers, and final destination. Debug SEO issues and audit redirect loops. No sign-up."),
    ('./en/resignation-letter-generator/index.html',
     "Free resignation letter generator — create a professional resignation letter in seconds. Choose from formal, friendly, or short templates. Fill in your details, copy or download as PDF. No sign-up needed."),
    ('./en/js-deobfuscator/index.html',
     "Free JavaScript deobfuscator — decode and beautify obfuscated JS code. Decode hex/unicode strings, simplify expressions, restore array references. 100% client-side processing, no upload. No sign-up."),
    ('./en/url-encoder-decoder/index.html',
     "Free URL encoder and decoder — encode special characters, Chinese text, spaces, query strings for safe URLs or decode back to plain text. Supports encodeURIComponent. Browser-side, no registration."),
    
    # ===== CN LONG pages =====
    ('./css-skeleton-loader-generator/index.html',
     "免费在线骨架屏生成器，为网页加载生成骨架屏HTML+CSS代码。支持卡片、列表、头像、段落等多种布局和动画效果。用骨架屏替代空白加载页，提升用户体验减少感知等待时间。纯前端本地生成，无需注册完全免费。"),
    ('./phone-link-generator/index.html',
     "免费在线手机链接生成器，一键生成tel协议HTML链接代码。点击后手机自动拨号，电脑打开Skype等通话软件。支持添加国家区号和分机号，实时预览复制即用。纯前端本地处理，无需注册完全免费。"),
    ('./canvas-painter/index.html',
     "免费在线画布绘画工具，在浏览器中自由绘画创作。支持画笔、橡皮擦、颜色选择、线条粗细调节和导出图片功能。触屏设备可用手指绘画。纯浏览器端本地处理，数据绝不上传，保障隐私安全，无需注册完全免费。"),
    ('./text-reverse/index.html',
     "免费在线文本反转工具，一键将文本字符顺序反转。支持逐字符反转、逐词反转、整句反转等多种模式。输入Hello World输出dlroW olleH。纯前端本地处理，数据不上传服务器，无需注册完全免费。"),
    
    # ===== SHORT pages =====
    ('./resignation-letter-generator/index.html',
     "免费在线辞职信生成器，填写姓名、职位、日期等基本信息即可生成专业辞职信。支持正式、友好、简短三种模板，一键复制或下载PDF。纯前端本地处理，数据不上传，无需注册完全免费。"),
    ('./time-duration-calculator/index.html',
     "免费在线时间时长计算器，轻松计算两个时间点之间的天数、小时、分钟和秒差。支持跨天计算、夜班工时统计、日期差值对比和时间加减运算。纯前端本地处理，无需注册，打开即用。"),
]

fixed = 0
errors = []

for filepath, new_desc in fixes:
    new_len = len(new_desc)
    
    # Pre-check length
    if new_len < 100 or new_len > 160:
        errors.append(f'DESC LENGTH: {filepath}: {new_len} (need 100-160)')
        continue
    
    if not os.path.exists(filepath):
        errors.append(f'MISSING: {filepath}')
        continue
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Find meta description line
    found = False
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if 'name="description"' in line:
            # Find content value
            idx = line.find('content="')
            if idx < 0:
                continue
            start = idx + 9
            end = line.find('"', start)
            old_val = line[start:end]
            old_len = len(old_val)
            
            if old_val == new_desc:
                found = True
                break
            
            # Replace
            lines[i] = line[:start] + new_desc + line[end:]
            found = True
            break
    
    if not found:
        errors.append(f'NO DESC LINE: {filepath}')
        continue
    
    if old_val == new_desc:
        print(f'  SKIP (match): {filepath}')
        continue
    
    new_content = '\n'.join(lines)
    
    with open(filepath, 'w') as f:
        f.write(new_content)
    
    print(f'✓ {filepath}: {old_len}→{new_len}')
    fixed += 1

print(f'\nFixed: {fixed}, Errors: {len(errors)}')
for e in errors:
    print(f'  ✗ {e}')
