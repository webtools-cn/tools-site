#!/usr/bin/env python3
"""批量移除EN工具h1中的emoji"""
import os, re, sys

SITE_DIR = '/home/chison/tools-site'

# emoji范围
EMOJI_PATTERN = re.compile(
    '[\U0001F300-\U0001F9FF'  # Misc Symbols, Emoticons
    '\u2600-\u27BF'            # Misc symbols
    '\u2B50'                   # Star
    '\u2702-\u27B0'           # Dingbats
    '\u24C2-\U0001F251'       # Enclosed chars
    '\uFE0F'                   # Variation selector
    '\u200D'                   # Zero-width joiner
    '\U0001F600-\U0001F64F'   # Emoticons
    '\U0001F680-\U0001F6FF'   # Transport
    '\U0001F1E0-\U0001F1FF'   # Flags
    ']')

def fix_h1_emoji(content):
    """移除h1开头的emoji"""
    def replacer(m):
        h1_content = m.group(1)
        # 移除开头的emoji+空格
        cleaned = EMOJI_PATTERN.sub('', h1_content).strip()
        # 如果清空了，保留原样
        if not cleaned:
            return m.group(0)
        # 确保没有多余空格
        cleaned = re.sub(r'\s+', ' ', cleaned)
        return f'<h1>{cleaned}</h1>'
    
    new_content = re.sub(r'<h1[^>]*>(.*?)</h1>', replacer, content)
    return new_content

def main():
    files_to_fix = sys.argv[1:] if len(sys.argv) > 1 else None
    
    if files_to_fix:
        # 指定文件列表
        tools = [f for f in files_to_fix]
    else:
        # 默认：高曝光工具
        tools = [
            'piano-keyboard', 'html-form-generator', 'html-wysiwyg-editor',
            'timeline-maker', 'bingo-card-generator', 'hearing-test',
            'recipe-nutrition-analyzer', 'semver-checker', 'gif-to-video-converter',
            'upside-down-text', 'credit-card-generator', 'mailto-link-generator',
            'online-piano', 'website-status-checker', 'leet-speak-converter',
            'braille-translator', 'text-to-braille', 'bic-validator',
            'hex-to-ascii', 'triangle-calculator', 'gantt-chart',
            'meta-tag-analyzer', 'ip-range-calculator', 'vision-test',
            'semantic-version-parser', 'code-compare', 'coupon-code-generator',
            'video-compress', 'shipping-calculator', 'height-converter',
            'digital-clock', 'timeline-generator', 'alphabetizer',
            'aes-encrypt-decrypt', 'syllable-counter', 'cidr-to-ip-range',
            'image-tint-effect', 'audio-spectrum-analyzer', 'gif-creator',
            'image-to-icon', 'terms-generator', 'whois-lookup',
            'percentage-difference-calculator', 'excel-to-html',
            'audio-equalizer', 'gif-to-mp4', 'beat-maker', 'json-to-php-array',
            # 加上Page1零点击的
            'bracket-matcher', 'key-code-finder', 'gitattributes-generator',
            'html-image-map-generator', 'gradient-border-animation', 'compass',
            'border-text-generator', 'css-border-image-generator', 'semver-validator',
        ]
    
    fixed = 0
    skipped = 0
    for tool in tools:
        path = os.path.join(SITE_DIR, 'en', tool, 'index.html')
        if not os.path.exists(path):
            print(f'MISS: en/{tool}/index.html')
            skipped += 1
            continue
        
        with open(path) as f:
            content = f.read()
        
        # 检查h1是否有emoji
        h1_match = re.search(r'<h1[^>]*>(.*?)</h1>', content)
        if not h1_match:
            skipped += 1
            continue
        
        h1_text = h1_match.group(1)
        if not EMOJI_PATTERN.search(h1_text):
            skipped += 1
            continue
        
        new_content = fix_h1_emoji(content)
        if new_content != content:
            with open(path, 'w') as f:
                f.write(new_content)
            new_h1 = re.search(r'<h1[^>]*>(.*?)</h1>', new_content).group(1)[:60]
            print(f'FIX: en/{tool}/index.html: "{h1_text[:50]}" -> "{new_h1}"')
            fixed += 1
        else:
            skipped += 1
    
    print(f'\nDone! Fixed: {fixed}, Skipped: {skipped}')

if __name__ == '__main__':
    main()
