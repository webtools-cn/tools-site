#!/usr/bin/env python3
"""Batch fix meta descriptions - v4: full line replacement."""
import os, re

# Map: file_path -> new_description  
# Uses full line match to avoid partial matches
fixes = [
    # (filepath, new_description)
    ('./en/ohms-law-calculator/index.html',
     "Free Ohm's Law calculator — calculate voltage, current, resistance, and power using V=IR and P=VI formulas. Supports all units (volts, amps, ohms, watts). Instant results for electronics study, circuit design, and electrical engineering. No sign-up."),
    ('./jensen-alpha-calculator/index.html',
     "免费在线Jensen's Alpha计算器，输入投资组合收益率、无风险利率、市场收益率和Beta值，一键计算詹森阿尔法指标。衡量投资组合超越CAPM理论预期收益的超额表现，支持风险调整后收益评估，基金经理选股能力评价核心工具。"),
    ('./en/jensen-alpha-calculator/index.html',
     "Free Jensen's Alpha calculator — measure your portfolio's risk-adjusted excess return vs CAPM. Enter portfolio return, risk-free rate, market return, and beta to calculate alpha. Essential for evaluating fund manager performance and investment skill. No sign-up."),
    ('./en/conways-game-of-life/index.html',
     "Free Conway's Game of Life simulator — run John Conway's classic cellular automaton in your browser. Click to seed cells, then watch patterns evolve with play/pause/speed controls. Includes famous patterns like gliders, oscillators, and spaceships. No sign-up."),
    ('./en/cat-age-calculator/index.html',
     "Free cat age calculator — convert your cat's age to human years with the most accurate formula. Cats age differently: the first year equals 15 human years, the second adds 9, then 4 per year. Understand your cat's life stage from kitten to senior. No sign-up."),
    ('./en/chronotype-quiz/index.html',
     "Free chronotype quiz — discover your sleep animal type (bear, wolf, lion, or dolphin) based on Dr. Breus' chronotype theory. 12 questions about energy peaks, sleep habits, and productivity patterns. Optimize your daily schedule around your natural rhythm."),
    ('./en/online-compass/index.html',
     "Free online compass — uses your phone's magnetometer for accurate real-time direction finding. Shows degrees, cardinal directions (N/S/E/W), and GPS coordinates. Works offline, perfect for hiking, camping, and navigation. No app install needed, just open in browser."),
    ('./en/cat-calorie-calculator/index.html',
     "Free cat calorie calculator — determine your cat's daily calorie needs based on weight, age, activity level, and body condition score. Uses veterinary-standard RER/MER formulas. Supports weight loss, maintenance, and kitten growth plans. No sign-up required."),
    ('./en/child-height-predictor/index.html',
     "Free child height predictor — estimate your child's adult height using mid-parental method and bone age data. Enter parent heights and child's current measurements to get a predicted range. Based on pediatric growth formulas used by doctors. No sign-up."),
    ('./en/college-savings-calculator/index.html',
     "Free college savings calculator — plan your child's education fund with inflation-adjusted projections. Enter current savings, monthly contribution, years until enrollment, and expected tuition costs. Compare 529 plan scenarios. No sign-up required."),
    ('./en/graham-number-calculator/index.html',
     "Free Graham Number calculator — based on Benjamin Graham's value investing formula (√22.5 × EPS × BVPS). Enter earnings per share and book value to find a stock's fair value. Essential tool for value investors following Graham and Buffett principles."),
    ('./en/car-depreciation-calculator/index.html',
     "Free car depreciation calculator — estimate your vehicle's value over time using straight-line and declining balance methods. Enter purchase price, age, and annual mileage. See year-by-year depreciation curves and total cost of ownership. No sign-up."),
    ('./en/dog-calorie-calculator/index.html',
     "Free dog calorie calculator — determine your dog's daily calorie needs by breed size, weight, age, activity level, and body condition. Uses veterinary RER/MER formulas. Supports weight loss, maintenance, and active/working dog diets. No sign-up required."),
    ('./en/business-valuation-calculator/index.html',
     "Free business valuation calculator — estimate your company's worth using DCF, revenue multiple, and asset-based methods. Enter revenue, profit, growth rate, and industry multipliers. Useful for M&A, fundraising, and exit planning. No sign-up required."),
    ('./en/voice-to-text/index.html',
     "Free voice-to-text tool — convert speech to text using your browser's built-in speech recognition API. Supports English and 50+ languages with real-time transcription. Copy, download, or edit results. Works offline in Chrome. No sign-up, 100% private."),
    ('./en/robots-txt-generator/index.html',
     "Free Robots.txt Generator — visually build and generate your website's robots.txt file. Select which bots to allow or disallow, set crawl delays, and add sitemap URLs. Perfect for SEO optimization and controlling search engine crawling. No sign-up."),
    ('./en/url-redirect-checker/index.html',
     "Free online URL redirect checker — trace HTTP redirect chains showing each hop with status codes (301, 302, 307), response headers, and final destination. Debug SEO redirect issues, verify canonical URLs, and audit redirect loops. No sign-up required."),
    ('./en/gratitude-journal/index.html',
     "Free gratitude journal — practice daily positive thinking. Write three things you're grateful for each day with prompts and mood tracking. All entries stored locally in your browser for complete privacy. Build a lasting gratitude habit. No sign-up."),
    ('./syllable-counter/index.html',
     "免费在线音节计数器，自动统计英文文本中每个单词的音节数，计算总音节、平均音节和Flesch可读性分数。支持实时统计、词频排序和CSV导出，浏览器本地处理保障隐私。适用于英文写作、SEO内容优化和语言学习场景。"),
    ('./en/purchasing-power-calculator/index.html',
     "Free purchasing power calculator — calculate how inflation erodes your money's value over time using CPI data. Compare historical purchasing power across decades and project future value. Essential for retirement planning and salary negotiations. No sign-up."),
    ('./en/id-photo-cropper/index.html',
     "Free online ID photo cropper — crop and resize photos for passport, visa, driver's license, and ID cards. Supports standard sizes for 50+ countries with background color replacement (white, blue, red). All processing done locally, no upload. No sign-up."),
    ('./en/baby-weight-percentile/index.html',
     "Free baby weight percentile calculator — based on WHO growth standards for infants 0-36 months. Enter your baby's weight, age, and gender to see percentile ranking and growth chart. Used by pediatricians worldwide to track healthy development. No sign-up."),
    ('./resignation-letter-generator/index.html',
     "免费在线辞职信生成器，填写姓名、职位、日期等基本信息即可生成专业辞职信。支持正式、友好、简短三种模板，一键复制到剪贴板或下载PDF。纯前端本地处理，数据不上传服务器，无需注册完全免费。"),
    ('./en/metabolic-age-calculator/index.html',
     "Free metabolic age calculator — estimate your body's biological age by comparing your BMR to age-group averages. Enter weight, height, age, and activity level to see if you're metabolically younger or older than your chronological age. No sign-up."),
    ('./time-duration-calculator/index.html',
     "免费在线时间时长计算器，轻松计算两个时间点之间的天数、小时、分钟和秒差。支持跨天计算、夜班工时统计、日期差值对比和时间加减运算。结果以多单位展示，纯前端本地处理，无需注册，打开即用。"),

    # === LONG pages (>160 chars) truncate ===
    ('./en/mermaid-editor/index.html',
     "Free Mermaid diagram editor — create flowcharts, sequence diagrams, Gantt charts, class diagrams, and more with text-based syntax. Live preview and SVG/PNG export. No sign-up required, runs entirely in your browser."),
    ('./en/image-color-extractor/index.html',
     "Free image color extractor — upload any image to extract dominant colors, accent tones, and a full palette in HEX/RGB. Supports PNG, JPG, WebP. All processing is client-side for privacy. No sign-up required."),
    ('./en/gif-resizer/index.html',
     "Free GIF resizer — resize animated GIFs with proportional scaling, custom dimensions, and preset sizes (emoji, avatar, sticker). Frame-by-frame re-rendering preserves all animation. 100% client-side processing. No sign-up required."),
    ('./en/svg-to-jsx-converter/index.html',
     "Free SVG to React JSX converter — transform SVG code into React JSX with proper attribute conversion (class→className, stroke-width→strokeWidth), self-closing tags, and TypeScript support. One-click copy. No sign-up."),
    ('./en/days-between-dates/index.html',
     "Free days between dates calculator — find exact days, weeks, months, and years between any two dates. Also calculate what date falls N days before/after a given date. Supports calendar and business days. No sign-up required."),
    ('./en/text-deduplicate/index.html',
     "Free text deduplication tool — remove duplicate lines or words with case-sensitive/insensitive options. Real-time stats: original count, duplicates found, unique lines remaining. One-click copy results. No sign-up required."),
    ('./en/css-gradient-text-generator/index.html',
     "Free CSS gradient text generator — create stunning gradient text effects with linear/radial gradients, 2-6 color stops, and adjustable angles. Live preview and one-click CSS copy. No sign-up required."),
    ('./en/text-animation-generator/index.html',
     "Free text animation generator — create CSS text animations including typewriter, neon glow, gradient flow, wave bounce, and 3D rotation. Live preview and one-click copy CSS + HTML code. No sign-up required."),
    ('./en/compliment-generator/index.html',
     "Free compliment generator — generate thoughtful compliments across 6 categories: personality, appearance, talent, encouragement, friendship, and romance. 100+ hand-picked compliments with copy buttons. No sign-up required."),
    ('./en/daily-affirmation-generator/index.html',
     "Free daily affirmation generator — generate positive self-affirmation cards to boost optimism and confidence. Customize, save favorites, and build a morning routine. All data stored locally for privacy. No sign-up required."),
    ('./en/word-search-generator/index.html',
     "Free word search generator — create custom printable word search puzzles from your word list. Multiple grid sizes and difficulty levels. Words hidden horizontally, vertically, and diagonally. Perfect for teachers and parents. No sign-up."),
    ('./en/jwt-generator/index.html',
     "Free JWT token generator — create signed JSON Web Tokens for API auth, OAuth 2.0, and microservices. Supports HS256/HS384/HS512 with customizable payload, expiration, and claims. All generation is client-side for security. No sign-up."),
    ('./en/text-to-html/index.html',
     "Free text to HTML converter — paste plain text and instantly get clean, formatted HTML code. Auto-handles paragraph tags, line breaks, and special character escaping. One-click copy. Perfect for content editors. No sign-up."),
    ('./en/device-mockup/index.html',
     "Free device mockup generator — place screenshots into realistic phone, tablet, laptop, and desktop frames. Supports iPhone, Android, iPad, MacBook models with customizable backgrounds. Create professional product showcase images. No sign-up."),
    ('./en/text-formatter/index.html',
     "Free text formatter — auto-add spaces between CJK and English, remove blank lines, normalize punctuation, add paragraph numbering, and convert full-width/half-width characters. Perfect for article typesetting. No sign-up required."),
    ('./en/mesh-gradient-generator/index.html',
     "Free mesh gradient generator — create stunning multi-color mesh gradients with a visual editor. Drag to adjust 4-6 color anchor points with independent colors and opacity. Live preview and CSS export. Perfect for hero sections. No sign-up."),
    ('./en/jwt-debugger/index.html',
     "Free JWT debugger — decode and inspect JWT header, payload, and signature in your browser. Supports HS256, RS256 with optional signature verification. Base64 decode and JSON pretty-print for easy debugging. No sign-up required."),
    ('./en/wav-to-mp3/index.html',
     "Free WAV to MP3 converter — convert WAV audio to compressed MP3 with adjustable bitrate (64-320kbps). Batch conversion with pure frontend processing, your files never leave your browser. Perfect for reducing audio file sizes. No sign-up."),
    ('./en/data-storage-converter/index.html',
     "Free data storage converter — convert between bytes, KB, MB, GB, TB, PB with both SI (1000) and IEC (1024) standards. Perfect for developers calculating file sizes and comparing drive capacities. Instant results. No sign-up."),
    ('./en/vite-config-generator/index.html',
     "Free Vite config generator — visually build vite.config.js/ts for React, Vue, Svelte, and more. Configure path aliases, plugins, dev proxy, and build options with live preview. One-click copy. No sign-up required."),
    ('./en/css-grid-template-areas/index.html',
     "Free CSS Grid template areas generator — visually design CSS Grid layouts by dragging and resizing named areas. Live preview and instant CSS grid-template-areas code generation. Perfect for frontend developers. No sign-up required."),
    ('./en/http-status-codes/index.html',
     "Free HTTP status codes reference — complete guide to all 1xx-5xx status codes with explanations, common causes, and troubleshooting tips. Essential quick reference for web developers, API designers, and system administrators. No sign-up."),
    ('./en/color-inverter/index.html',
     "Free image color inverter — upload any image and instantly invert colors for a negative/X-ray effect. Supports JPG, PNG, GIF, BMP with live preview and download. All processing is client-side for privacy. No sign-up required."),
    ('./en/color-blender/index.html',
     "Free color blender — mix two colors at any ratio (0-100%) to generate midtones and gradient swatches. Supports HEX/RGB with live preview. Ideal for UI color schemes and CSS gradient generation. No sign-up required."),
    ('./en/dummy-json-generator/index.html',
     "Free dummy JSON generator — create mock JSON with customizable field types, array length, and nesting depth. Generate realistic test data for API development and frontend prototyping. All data generated locally. No sign-up required."),
    ('./en/regex-visualizer/index.html',
     "Free regex visualizer — convert regular expressions into interactive railroad diagrams with syntax highlighting, match testing, and group explanations. Browse common regex templates for quick reference. No sign-up required."),
    ('./en/pastebin/index.html',
     "Free pastebin — paste text and generate shareable links instantly. Syntax highlighting for 30+ languages, line numbers, one-click copy. All client-side processing, your data never leaves your browser. No sign-up required."),
    ('./en/syllable-counter/index.html',
     "Free syllable counter — count syllables in English text, calculate Flesch Reading Ease score, and analyze word-level syllable distribution. Real-time analysis, word frequency sorting, and CSV export. Browser-based for privacy. No sign-up."),
    ('./en/pdf-bookmark/index.html',
     "Free PDF bookmark editor — add, edit, and manage PDF bookmarks directly in your browser. Create hierarchical bookmarks and download the updated file. All processing is client-side with pdf-lib. No file uploads, no sign-up required."),
    ('./en/css-text-outline-generator/index.html',
     "Free CSS text outline generator — customize text-stroke width, color, and shadow effects with live preview. One-click copy CSS for web titles, banners, and logo typography. No sign-up required."),
]

fixed = 0
errors = []

for filepath, new_desc in fixes:
    if not os.path.exists(filepath):
        errors.append(f'MISSING FILE: {filepath}')
        continue
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Find the meta description line's full old content attribute value
    pattern = r'(<meta\s+name=["\']description["\']\s+content=["\'])([^"\']+)(["\'])'
    m = re.search(pattern, content)
    
    if not m:
        errors.append(f'NO META DESC FOUND: {filepath}')
        continue
    
    old_val = m.group(2)
    old_len = len(old_val)
    new_len = len(new_desc)
    
    # Skip if already matches
    if old_val == new_desc:
        print(f'  SKIP (match): {filepath}')
        continue
    
    # Replace only the content value
    before = content[:m.start(2)]
    after = content[m.end(2):]
    new_content = before + new_desc + after
    
    # Verify
    verify_m = re.search(r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']+)["\']', new_content, re.IGNORECASE)
    verified_len = len(verify_m.group(1)) if verify_m else 0
    
    if verified_len != new_len:
        errors.append(f'VERIFY MISMATCH (expected {new_len} got {verified_len}): {filepath}')
        print(f'  DEBUG: expected={new_len}, got={verified_len}, file shows old_len={old_len}')
        continue
    
    with open(filepath, 'w') as f:
        f.write(new_content)
    
    print(f'✓ {filepath}: {old_len}→{new_len} chars')
    fixed += 1

print(f'\nFixed: {fixed}, Errors: {len(errors)}')
for e in errors:
    print(f'  ✗ {e}')