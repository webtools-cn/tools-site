#!/usr/bin/env python3
"""Fix meta - auto truncate long descriptions to 150 chars at word boundary."""
import os

fixes = {
    './en/mermaid-editor/index.html': None,
    './en/image-color-extractor/index.html': None,
    './en/gif-resizer/index.html': None,
    './en/svg-to-jsx-converter/index.html': None,
    './en/days-between-dates/index.html': None,
    './en/text-deduplicate/index.html': None,
    './en/css-gradient-text-generator/index.html': None,
    './en/text-animation-generator/index.html': None,
    './en/compliment-generator/index.html': None,
    './en/daily-affirmation-generator/index.html': None,
    './en/word-search-generator/index.html': None,
    './en/jwt-generator/index.html': None,
    './en/text-to-html/index.html': None,
    './en/device-mockup/index.html': None,
    './en/text-formatter/index.html': None,
    './en/mesh-gradient-generator/index.html': None,
    './en/jwt-debugger/index.html': None,
    './en/wav-to-mp3/index.html': None,
    './en/data-storage-converter/index.html': None,
    './en/vite-config-generator/index.html': None,
    './en/css-grid-template-areas/index.html': None,
    './en/http-status-codes/index.html': None,
    './en/color-inverter/index.html': None,
    './en/color-blender/index.html': None,
    './en/dummy-json-generator/index.html': None,
    './en/regex-visualizer/index.html': None,
    './en/pastebin/index.html': None,
    './en/syllable-counter/index.html': None,
    './en/pdf-bookmark/index.html': None,
    './en/css-text-outline-generator/index.html': None,
    './en/url-redirect-checker/index.html': None,
    './en/resignation-letter-generator/index.html': None,
    './en/js-deobfuscator/index.html': None,
    './en/url-encoder-decoder/index.html': None,
    './css-skeleton-loader-generator/index.html': None,
    './phone-link-generator/index.html': None,
    './canvas-painter/index.html': None,
    './text-reverse/index.html': None,
    './resignation-letter-generator/index.html': None,
    './time-duration-calculator/index.html': None,
}

def truncate_desc(desc, max_len=155):
    """Truncate description at last space before max_len chars, add period if needed."""
    if len(desc) <= max_len:
        return desc
    truncated = desc[:max_len]
    last_space = truncated.rfind(' ')
    if last_space > 100:  # Don't cut too short
        return truncated[:last_space] + '.'
    return truncated[:max_len] + '.'

fixed = 0
errors = []

for filepath in fixes:
    if not os.path.exists(filepath):
        errors.append(f'MISSING: {filepath}')
        continue
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    for i, line in enumerate(content.split('\n')):
        if 'name="description"' in line:
            idx = line.find('content="')
            if idx < 0:
                continue
            start = idx + 9
            end = line.find('"', start)
            old_val = line[start:end]
            old_len = len(old_val)
            
            if 100 <= old_len <= 160:
                print(f'  SKIP (OK): {filepath} ({old_len})')
                break
            
            new_val = truncate_desc(old_val)
            new_len = len(new_val)
            
            new_line = line[:start] + new_val + line[end:]
            lines = content.split('\n')
            lines[i] = new_line
            
            with open(filepath, 'w') as f:
                f.write('\n'.join(lines))
            
            print(f'✓ {filepath}: {old_len}→{new_len}')
            fixed += 1
            break

print(f'\nFixed: {fixed}, Errors: {len(errors)}')
for e in errors:
    print(f'  ✗ {e}')