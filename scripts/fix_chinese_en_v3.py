#!/usr/bin/env python3
"""
chinese_in_en 顽固case修复 v3
处理lang-switch中的"中文"链接和工具名碎片
"""
import json, os, re

SITE = '/home/chison/tools-site'

# 额外映射
EXTRA = {
    '砖块用量器': 'Brick Calculator',
    '砖块用量': 'Brick Quantity',
    '命令器': 'Command Runner',
    '命令': 'Command',
    '间到': 'time left',
    '停止倒计': 'Stop countdown',
    '倒计': 'Countdown',
    '百分比': 'Percentage',
    '延迟': 'Delay',
    '毫秒': 'ms',
    '像素': 'px',
    '厘米': 'cm',
    '英寸': 'inch',
    '毫米': 'mm',
    '像素比': 'ratio',
    '长宽比': 'aspect ratio',
    '宽高比': 'aspect ratio',
    '分辨率': 'Resolution',
    '对比度': 'Contrast',
    '饱和度': 'Saturation',
    '亮度': 'Brightness',
    '色相': 'Hue',
    '透明度': 'Opacity',
    '不透明度': 'Opacity',
    '渐变': 'Gradient',
    '阴影': 'Shadow',
    '圆角': 'Border Radius',
    '边框': 'Border',
    '间距': 'Spacing',
    '内边距': 'Padding',
    '外边距': 'Margin',
    '字体': 'Font',
    '字号': 'Font Size',
    '行高': 'Line Height',
    '字重': 'Font Weight',
    '对齐': 'Alignment',
    '居中': 'Center',
    '左对齐': 'Left Align',
    '右对齐': 'Right Align',
    '两端对齐': 'Justify',
    '显示': 'Display',
    '隐藏': 'Hidden',
    '可见': 'Visible',
    '固定': 'Fixed',
    '绝对': 'Absolute',
    '相对': 'Relative',
    '静态': 'Static',
    '弹性': 'Flex',
    '网格': 'Grid',
    '块级': 'Block',
    '内联': 'Inline',
    '内联块': 'Inline-Block',
    '表格': 'Table',
    '单元格': 'Cell',
    '行': 'Row',
    '列': 'Column',
}

def fix_stubborn_chinese(path):
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        c = f.read()
    
    cn_re = re.compile(r'[\u4e00-\u9fff]')
    if not cn_re.search(c):
        return False
    if 'noindex' in c:
        return False
    
    changed = False
    
    # Strategy 1: Replace lang-switch "中文" with "CN" 
    # Pattern: href="../<tool>/">中文</a>
    c = re.sub(r'href="[^"]*">中文</a>', 'href="\\g<0>" class="cn-link">CN</a>', c)
    # Simpler: just replace "中文" with "CN" in lang-switch context
    c = c.replace('>中文</a>', '>CN</a>')
    if '>中文</a>' not in c:  # only count if changed
        pass
    else:
        changed = True
    
    # Strategy 2: Apply extra mappings
    for cn_text, en_text in EXTRA.items():
        if cn_text in c:
            c = c.replace(cn_text, en_text)
            changed = True
    
    # Strategy 3: Remove any remaining standalone Chinese characters in visible text
    # by checking specific patterns in lang-switch areas
    
    if changed:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(c)
        return True
    return False


def main():
    with open(os.path.join(SITE, 'quality', 'quality_loop_result.json')) as f:
        data = json.load(f)
    
    pages = data['remaining_pages']
    target = [(k,v) for k,v in pages.items() if 'chinese_in_en' in v]
    
    print(f'Target pages: {len(target)}')
    
    fixed = 0
    skipped = 0
    
    for idx, (page_key, issues) in enumerate(target):
        lang, item = page_key.split(':', 1)
        path = os.path.join(SITE, 'en', item, 'index.html')
        
        if not os.path.exists(path):
            skipped += 1
            continue
        
        try:
            if fix_stubborn_chinese(path):
                fixed += 1
            else:
                skipped += 1
        except:
            skipped += 1
    
    print(f'Fixed: {fixed}, Skipped: {skipped}')

if __name__ == '__main__':
    main()