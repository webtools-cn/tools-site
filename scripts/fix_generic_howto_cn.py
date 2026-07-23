#!/usr/bin/env python3
"""
T041: Replace generic HowTo Schema with tool-specific content for CN tools.
Generic pattern: "准备输入/配置选项/查看结果" + "输入或粘贴需要处理的数据/根据需要调整参数设置/获取处理后的输出结果"
Replace with category-specific steps that describe actual tool usage.
"""
import re, glob, json, sys

# Category-specific step templates (CN)
CATEGORY_STEPS = {
    'calculator': [
        ('输入数据', '在输入框中输入需要计算的数值'),
        ('选择选项', '根据需要选择计算模式或参数'),
        ('点击计算', '点击计算按钮获取结果'),
        ('查看结果', '查看计算结果，支持一键复制'),
    ],
    'converter': [
        ('输入内容', '在输入框中输入或粘贴需要转换的内容'),
        ('选择格式', '选择源格式和目标格式'),
        ('执行转换', '点击转换按钮进行格式转换'),
        ('复制结果', '查看转换结果并一键复制'),
    ],
    'generator': [
        ('设置参数', '配置生成参数（数量、格式、范围等）'),
        ('点击生成', '点击生成按钮创建内容'),
        ('预览结果', '查看生成的结果'),
        ('复制或下载', '一键复制结果或下载为文件'),
    ],
    'checker': [
        ('输入内容', '在输入框中输入需要检查的内容'),
        ('点击检查', '点击检查按钮开始检测'),
        ('查看结果', '查看检查结果和详细报告'),
        ('复制报告', '一键复制检查报告'),
    ],
    'encoder': [
        ('输入内容', '在输入框中输入或粘贴需要编码/解码的内容'),
        ('选择方向', '选择编码或解码操作'),
        ('执行操作', '点击按钮执行编码或解码'),
        ('复制结果', '查看结果并一键复制'),
    ],
    'formatter': [
        ('输入内容', '在输入框中粘贴需要格式化的代码或文本'),
        ('选择格式', '选择格式化选项（缩进、换行等）'),
        ('点击格式化', '点击按钮执行格式化'),
        ('复制结果', '查看格式化结果并一键复制'),
    ],
    'analyzer': [
        ('输入内容', '在输入框中输入或粘贴需要分析的内容'),
        ('点击分析', '点击分析按钮开始处理'),
        ('查看报告', '查看分析结果和详细统计'),
        ('复制结果', '一键复制分析结果'),
    ],
    'editor': [
        ('输入内容', '在编辑器中输入或粘贴内容'),
        ('编辑修改', '使用工具栏或快捷键编辑内容'),
        ('实时预览', '在预览区查看编辑效果'),
        ('导出结果', '复制或下载编辑后的内容'),
    ],
    'viewer': [
        ('上传文件', '点击上传或拖拽文件到指定区域'),
        ('查看内容', '浏览文件内容和详细信息'),
        ('分析数据', '查看自动生成的分析报告'),
        ('导出结果', '复制或下载分析结果'),
    ],
    'tester': [
        ('准备测试', '输入测试参数或上传测试文件'),
        ('开始测试', '点击开始按钮执行测试'),
        ('查看结果', '查看测试结果和详细数据'),
        ('复制报告', '一键复制测试报告'),
    ],
}

def detect_category(slug, name):
    """Detect tool category from slug and name"""
    s = slug.lower()
    n = name.lower()
    
    # Direct category matches
    for cat in ['calculator', 'converter', 'generator', 'checker', 'encoder', 'formatter', 'analyzer', 'editor', 'viewer', 'tester']:
        if cat in s or cat in n:
            return cat
    
    # Additional patterns
    if any(w in s for w in ['calc', 'compute', 'count']):
        return 'calculator'
    if any(w in s for w in ['convert', 'transform', 'translate']):
        return 'converter'
    if any(w in s for w in ['generate', 'create', 'make', 'builder']):
        return 'generator'
    if any(w in s for w in ['check', 'verify', 'validate', 'detect']):
        return 'checker'
    if any(w in s for w in ['encode', 'decode', 'encrypt', 'decrypt', 'hash']):
        return 'encoder'
    if any(w in s for w in ['format', 'beautify', 'minify', 'pretty']):
        return 'formatter'
    if any(w in s for w in ['analyz', 'inspect', 'monitor']):
        return 'analyzer'
    if any(w in s for w in ['edit', 'modify', 'design']):
        return 'editor'
    if any(w in s for w in ['view', 'render', 'display', 'visual']):
        return 'viewer'
    if any(w in s for w in ['test', 'benchmark', 'measure', 'speed']):
        return 'tester'
    if any(w in s for w in ['sort', 'filter', 'search', 'find']):
        return 'analyzer'
    if any(w in s for w in ['compare', 'diff']):
        return 'analyzer'
    if any(w in s for w in ['random', 'shuffle']):
        return 'generator'
    if any(w in s for w in ['play', 'player', 'recorder', 'record']):
        return 'editor'
    if any(w in s for w in ['download', 'export', 'import']):
        return 'converter'
    if any(w in s for w in ['color', 'gradient', 'shadow', 'border', 'animation']):
        return 'generator'
    if any(w in s for w in ['extract', 'split', 'merge', 'join', 'combine']):
        return 'converter'
    if any(w in s for w in ['compress', 'decompress', 'zip']):
        return 'converter'
    if any(w in s for w in ['remove', 'delete', 'clean', 'strip']):
        return 'formatter'
    if any(w in s for w in ['scan', 'lookup', 'query']):
        return 'checker'
    if any(w in s for w in ['draw', 'paint', 'sketch']):
        return 'editor'
    if any(w in s for w in ['schedule', 'plan', 'organize']):
        return 'generator'
    if any(w in s for w in ['log', 'trace', 'debug']):
        return 'viewer'
    
    return 'converter'  # default fallback

def build_howto_steps_json(tool_name, category):
    """Build HowTo step JSON array for a given tool and category"""
    steps = CATEGORY_STEPS.get(category, CATEGORY_STEPS['converter'])
    step_objects = []
    for i, (name, text) in enumerate(steps, 1):
        step_objects.append(
            f'{{"@type": "HowToStep", "position": {i}, "name": "{name}", "text": "{text}"}}'
        )
    return '[' + ', '.join(step_objects) + ']'

def process_file(filepath):
    """Process a single CN file to replace generic HowTo with specific content"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if this file has the generic HowTo pattern
    if '输入或粘贴需要处理的数据' not in content:
        return False
    
    # Extract tool name from HowTo schema
    name_match = re.search(r'"HowTo".*?"name":\s*"如何使用([^"]+)"', content)
    if name_match:
        tool_name = name_match.group(1)
    else:
        # Fallback: get from SoftwareApplication
        sa_match = re.search(r'"SoftwareApplication".*?"name":\s*"([^"]+)"', content)
        if sa_match:
            tool_name = sa_match.group(1)
        else:
            tool_name = filepath.split('/')[0].replace('-', ' ')
    
    # Detect category
    slug = filepath.split('/')[0]
    category = detect_category(slug, tool_name)
    
    # Build new step JSON
    new_steps = build_howto_steps_json(tool_name, category)
    
    # Replace the generic step array
    # Pattern 1: "准备输入" (1863 files)
    old_pattern1 = '"step": [{"@type": "HowToStep", "position": 1, "name": "准备输入", "text": "输入或粘贴需要处理的数据"}, {"@type": "HowToStep", "position": 2, "name": "配置选项", "text": "根据需要调整参数设置"}, {"@type": "HowToStep", "position": 3, "name": "查看结果", "text": "获取处理后的输出结果"}]'
    
    # Pattern 2: "输入数据" (2 files)
    old_pattern2 = '"step": [{"@type": "HowToStep", "position": 1, "name": "输入数据", "text": "输入或粘贴需要处理的数据"}, {"@type": "HowToStep", "position": 2, "name": "配置选项", "text": "根据需要调整参数设置"}, {"@type": "HowToStep", "position": 3, "name": "查看结果", "text": "获取处理后的输出结果"}]'
    
    if old_pattern1 in content:
        content = content.replace(old_pattern1, '"step": ' + new_steps)
    elif old_pattern2 in content:
        content = content.replace(old_pattern2, '"step": ' + new_steps)
    else:
        # Try regex for any variation
        old_regex = r'"step":\s*\[\{"@type":\s*"HowToStep",\s*"position":\s*1,\s*"name":\s*"(?:准备输入|输入数据)",\s*"text":\s*"输入或粘贴需要处理的数据"\},\s*\{"@type":\s*"HowToStep",\s*"position":\s*2,\s*"name":\s*"配置选项",\s*"text":\s*"根据需要调整参数设置"\},\s*\{"@type":\s*"HowToStep",\s*"position":\s*3,\s*"name":\s*"查看结果",\s*"text":\s*"获取处理后的输出结果"\}\]'
        content = re.sub(old_regex, '"step": ' + new_steps, content)
    
    # Also update the HowTo description to be more specific
    old_desc = f'"description": "{tool_name}的使用步骤"'
    new_desc = f'"description": "如何使用{tool_name}的详细步骤指南"'
    if old_desc in content:
        content = content.replace(old_desc, new_desc)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

def main():
    # Process all CN files
    processed = 0
    errors = 0
    categories = {}
    
    for f in sorted(glob.glob('*/index.html')):
        if f.startswith('en/'): continue
        try:
            if process_file(f):
                processed += 1
                slug = f.split('/')[0]
                # Detect category for stats
                with open(f) as fh:
                    c = fh.read()
                name_match = re.search(r'"HowTo".*?"name":\s*"如何使用([^"]+)"', c)
                tool_name = name_match.group(1) if name_match else slug
                cat = detect_category(slug, tool_name)
                categories[cat] = categories.get(cat, 0) + 1
        except Exception as e:
            errors += 1
            print(f'Error processing {f}: {e}', file=sys.stderr)
    
    print(f'Processed: {processed}')
    print(f'Errors: {errors}')
    print(f'Category distribution:')
    for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
        print(f'  {cat}: {count}')

if __name__ == '__main__':
    main()
