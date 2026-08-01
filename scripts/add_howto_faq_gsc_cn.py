#!/usr/bin/env python3
"""
Batch add HowTo Schema and FAQ Schema to GSC-exposed CN pages that are missing them.
Reads tools-data-cn.json for tool names/descriptions.
Reads .gsc-data/page-performance.json for GSC exposure data.
Skips pages that already have the respective schema.
"""

import json, re, os, glob

# ============================================================
# 1. Load tools-data-cn.json → slug → (name, description)
# ============================================================
with open('tools-data-cn.json', encoding='utf-8') as f:
    raw = json.load(f)

tool_map = {}
for cat, tools in raw.items():
    for tool in tools:
        if len(tool) >= 4:
            slug = tool[3].rstrip('/')
            name = tool[1]
            desc = tool[2]
            tool_map[slug] = {'name': name, 'desc': desc}

print(f"Loaded {len(tool_map)} tools from tools-data-cn.json")

# ============================================================
# 2. Load GSC page-performance.json → CN pages with impressions
# ============================================================
with open('.gsc-data/page-performance.json', encoding='utf-8') as f:
    gsc_data = json.load(f)

cn_gsc = {}
for p in gsc_data:
    url = p.get('url', '')
    if '/en/' in url:
        continue
    parts = url.rstrip('/').split('free-toolbase.com/')
    if len(parts) > 1:
        slug = parts[1].rstrip('/')
        if slug and '/en/' not in slug and not slug.startswith('en'):
            cn_gsc[slug] = p.get('impressions', 0)

print(f"Found {len(cn_gsc)} CN pages in GSC data")

# ============================================================
# 3. Category detection (from fix_generic_howto_cn.py)
# ============================================================
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
    s = slug.lower()
    n = name.lower()
    
    for cat in CATEGORY_STEPS:
        if cat in s or cat in n:
            return cat
    
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

# ============================================================
# 4. Build HowTo Schema JSON-LD
# ============================================================
def build_howto_schema(tool_name, tool_desc, category):
    steps = CATEGORY_STEPS.get(category, CATEGORY_STEPS['converter'])
    step_list = []
    for i, (name, text) in enumerate(steps, 1):
        step_list.append({
            "@type": "HowToStep",
            "position": i,
            "name": name,
            "text": text
        })
    
    schema = {
        "@context": "https://schema.org",
        "@type": "HowTo",
        "name": f"如何使用{tool_name}",
        "description": tool_desc[:200] if tool_desc else f"如何使用{tool_name}的详细步骤指南",
        "totalTime": "PT2M",
        "tool": {
            "@type": "HowToTool",
            "name": tool_name
        },
        "step": step_list
    }
    return json.dumps(schema, ensure_ascii=False, separators=(',', ':'))

# ============================================================
# 5. Build FAQ Schema JSON-LD (3 questions)
# ============================================================
def build_faq_schema(tool_name, tool_desc, category, slug):
    """Generate 3 FAQ questions with professional answers based on tool type"""
    
    # Category-specific FAQ templates
    faq_templates = {
        'calculator': [
            (f"❓ {tool_name}怎么用？", f"使用很简单：1)在输入框中输入需要计算的数值；2)选择计算模式或参数；3)点击计算按钮即可获得结果。所有计算在浏览器本地完成，无需注册，完全免费。"),
            (f"❓ {tool_name}计算结果准确吗？", f"计算结果完全准确。工具使用标准数学公式和算法，所有计算在浏览器端完成，不依赖外部服务。支持一键复制结果，方便您在其他场景使用。"),
            (f"❓ 数据会上传到服务器吗？", f"不会。所有计算都在您的浏览器本地完成，输入的数据和计算结果都不会上传到任何服务器，100%保护隐私。工具可离线使用。"),
        ],
        'converter': [
            (f"❓ {tool_name}支持哪些格式？", f"工具支持常见的输入输出格式转换，具体格式可在页面上选择。转换过程在浏览器本地完成，无需上传文件，保护隐私。"),
            (f"❓ 转换结果准确吗？", f"转换结果完全准确，使用标准算法确保精度。所有转换在浏览器端完成，不依赖外部服务。支持一键复制转换结果。"),
            (f"❓ {tool_name}是免费的吗？", f"完全免费，无需注册即可使用。所有转换在浏览器本地完成，不限次数，不限文件大小。"),
        ],
        'generator': [
            (f"❓ {tool_name}可以自定义哪些参数？", f"支持多种自定义参数，包括数量、格式、范围等选项。所有参数可在页面上直接调整，实时预览生成效果。"),
            (f"❓ 生成的内容可以商用吗？", f"生成的内容可自由使用。工具完全免费，生成结果支持一键复制或下载。具体使用场景请根据实际需求判断。"),
            (f"❓ {tool_name}是免费的吗？", f"完全免费，无需注册。所有生成过程在浏览器本地完成，不限使用次数，无需安装任何软件。"),
        ],
        'checker': [
            (f"❓ {tool_name}的检测结果可靠吗？", f"检测结果完全可靠，使用标准验证规则和算法。所有检测在浏览器端完成，不依赖外部服务，结果即时显示。"),
            (f"❓ 检测时数据会上传吗？", f"不会。所有检测都在您的浏览器本地完成，输入的内容不会上传到任何服务器，100%保护隐私安全。"),
            (f"❓ {tool_name}支持哪些内容检测？", f"支持多种内容类型的检测，具体可在页面上查看。检测过程快速准确，结果支持一键复制。"),
        ],
        'encoder': [
            (f"❓ {tool_name}支持哪些编码格式？", f"支持常见的编码/解码格式，具体格式可在页面上选择。编码过程在浏览器本地完成，安全可靠。"),
            (f"❓ 编码/解码结果准确吗？", f"结果完全准确，使用标准编码算法。所有操作在浏览器端完成，不依赖外部服务，支持一键复制。"),
            (f"❓ 数据安全吗？", f"完全安全。所有编码/解码操作都在浏览器本地完成，数据不会上传到任何服务器，保护隐私。"),
        ],
        'formatter': [
            (f"❓ {tool_name}支持哪些格式化选项？", f"支持多种格式化选项，包括缩进、换行、排序等。具体选项可在页面上选择，实时预览格式化效果。"),
            (f"❓ 格式化会修改原始内容吗？", f"不会。格式化只调整代码/文本的排版格式，不改变内容本身。原始内容和格式化结果都可在页面上查看对比。"),
            (f"❓ {tool_name}是免费的吗？", f"完全免费，无需注册。所有格式化在浏览器本地完成，不限使用次数，支持一键复制结果。"),
        ],
        'analyzer': [
            (f"❓ {tool_name}能分析什么？", f"可对输入内容进行全面分析，生成详细统计报告。分析过程在浏览器本地完成，结果即时显示。"),
            (f"❓ 分析结果准确吗？", f"分析结果完全准确，使用标准算法进行统计和分析。所有处理在浏览器端完成，不依赖外部服务。"),
            (f"❓ 数据会上传到服务器吗？", f"不会。所有分析都在浏览器本地完成，输入的数据和分析结果都不会上传到任何服务器，100%保护隐私。"),
        ],
        'editor': [
            (f"❓ {tool_name}支持哪些编辑功能？", f"支持多种编辑功能，包括文本修改、参数调整、实时预览等。具体功能可在页面上查看和使用。"),
            (f"❓ 编辑后的内容可以导出吗？", f"可以。编辑完成后支持一键复制或下载导出。所有编辑在浏览器本地完成，无需安装软件。"),
            (f"❓ {tool_name}是免费的吗？", f"完全免费，无需注册。所有编辑功能在浏览器本地运行，不限使用次数。"),
        ],
        'viewer': [
            (f"❓ {tool_name}支持哪些文件格式？", f"支持常见的文件格式查看，具体格式可在页面上查看。文件在浏览器本地解析，不上传服务器。"),
            (f"❓ 查看文件时数据安全吗？", f"完全安全。所有文件解析和查看都在浏览器本地完成，文件内容不会上传到任何服务器，保护隐私。"),
            (f"❓ {tool_name}是免费的吗？", f"完全免费，无需注册。支持在线查看和分析，不限使用次数。"),
        ],
        'tester': [
            (f"❓ {tool_name}能测试什么？", f"可对输入内容进行全面测试，生成详细测试报告。测试过程在浏览器本地完成，结果即时显示。"),
            (f"❓ 测试结果可靠吗？", f"测试结果完全可靠，使用标准测试方法和算法。所有测试在浏览器端完成，不依赖外部服务。"),
            (f"❓ {tool_name}是免费的吗？", f"完全免费，无需注册。所有测试在浏览器本地运行，不限使用次数，支持一键复制报告。"),
        ],
    }
    
    questions = faq_templates.get(category, faq_templates['converter'])
    
    main_entity = []
    for q_name, q_text in questions:
        main_entity.append({
            "@type": "Question",
            "name": q_name,
            "acceptedAnswer": {
                "@type": "Answer",
                "text": q_text
            }
        })
    
    schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": main_entity
    }
    return json.dumps(schema, ensure_ascii=False, separators=(',', ':'))

# ============================================================
# 6. Process files
# ============================================================
stats = {
    'howto_added': 0,
    'howto_skipped_exists': 0,
    'howto_skipped_nofile': 0,
    'howto_error': 0,
    'faq_added': 0,
    'faq_skipped_exists': 0,
    'faq_skipped_nofile': 0,
    'faq_error': 0,
    'category_dist': {},
}

# Get all GSC CN slugs sorted by impressions (descending)
gsc_slugs = sorted(cn_gsc.keys(), key=lambda s: -cn_gsc[s])

for slug in gsc_slugs:
    filepath = f'{slug}/index.html'
    
    if not os.path.exists(filepath):
        stats['howto_skipped_nofile'] += 1
        stats['faq_skipped_nofile'] += 1
        continue
    
    # Read file
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        stats['howto_error'] += 1
        stats['faq_error'] += 1
        print(f"  ERROR reading {filepath}: {e}")
        continue
    
    # Get tool info
    tool_info = tool_map.get(slug, {'name': slug.replace('-', ' '), 'desc': ''})
    tool_name = tool_info['name']
    tool_desc = tool_info['desc']
    
    # Also try to extract name from existing SoftwareApplication schema
    sa_match = re.search(r'"SoftwareApplication".*?"name":\s*"([^"]+)"', content)
    if sa_match:
        tool_name = sa_match.group(1)
    
    # Detect category
    category = detect_category(slug, tool_name)
    stats['category_dist'][category] = stats['category_dist'].get(category, 0) + 1
    
    modified = False
    
    # ---- Add HowTo Schema if missing ----
    if '"HowTo"' in content:
        stats['howto_skipped_exists'] += 1
    else:
        howto_json = build_howto_schema(tool_name, tool_desc, category)
        howto_tag = f'<script type="application/ld+json">{howto_json}</script>'
        
        # Insert before </head> if exists, otherwise before </body>
        if '</head>' in content:
            content = content.replace('</head>', howto_tag + '\n</head>', 1)
        elif '</body>' in content:
            content = content.replace('</body>', howto_tag + '\n</body>', 1)
        else:
            content += '\n' + howto_tag
        
        modified = True
        stats['howto_added'] += 1
    
    # ---- Add FAQ Schema if missing ----
    if '"FAQPage"' in content or '"FAQ"' in content:
        stats['faq_skipped_exists'] += 1
    else:
        faq_json = build_faq_schema(tool_name, tool_desc, category, slug)
        faq_tag = f'<script type="application/ld+json">{faq_json}</script>'
        
        # Insert before </head> if exists, otherwise before </body>
        if '</head>' in content:
            content = content.replace('</head>', faq_tag + '\n</head>', 1)
        elif '</body>' in content:
            content = content.replace('</body>', faq_tag + '\n</body>', 1)
        else:
            content += '\n' + faq_tag
        
        modified = True
        stats['faq_added'] += 1
    
    # Write back if modified
    if modified:
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
        except Exception as e:
            stats['howto_error'] += 1
            stats['faq_error'] += 1
            print(f"  ERROR writing {filepath}: {e}")

# ============================================================
# 7. Print stats
# ============================================================
print("\n" + "="*60)
print("BATCH SCHEMA INSERTION RESULTS")
print("="*60)
print(f"\nHowTo Schema:")
print(f"  Added:    {stats['howto_added']}")
print(f"  Skipped (already exists): {stats['howto_skipped_exists']}")
print(f"  Skipped (no file):        {stats['howto_skipped_nofile']}")
print(f"  Errors:   {stats['howto_error']}")

print(f"\nFAQ Schema:")
print(f"  Added:    {stats['faq_added']}")
print(f"  Skipped (already exists): {stats['faq_skipped_exists']}")
print(f"  Skipped (no file):        {stats['faq_skipped_nofile']}")
print(f"  Errors:   {stats['faq_error']}")

print(f"\nCategory distribution:")
for cat, count in sorted(stats['category_dist'].items(), key=lambda x: -x[1]):
    print(f"  {cat}: {count}")

print(f"\nTotal GSC CN pages processed: {len(gsc_slugs)}")
