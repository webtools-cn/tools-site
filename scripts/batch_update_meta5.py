#!/usr/bin/env python3
"""Final fixes to push all descriptions to 140-160 range."""
import re

ADDITIONS = {
    "avif-to-jpg": ('JPG格式。纯浏览器', 'JPG格式，解决AVIF在旧设备上无法显示的兼容问题。纯浏览器'),
    "backwards-text": ('对比三种翻转模式。', '对比三种翻转模式，每种模式实时显示结果。'),
    "batch-rename": ('开发运维和项目管理场景。', '开发运维和项目管理等日常办公场景。'),
    "bmp-to-png": ('画质清晰无损。纯', '画质清晰无损。支持拖拽上传图片文件，转换速度极快。纯'),
    "business-card-maker": ('专业配色模板自由切换。', '专业配色模板（经典白、商务蓝、极简黑等）自由切换。'),
    "camera-recorder": ('面试练习场景。', '面试练习、产品演示和视频会议录制等多种场景。'),
    "character-counter": ('翻译字数估算等场景。', '翻译字数估算和SEO元描述长度检查等常用场景。'),
    "compound-interest": ('长期投资回报预测场景。', '长期投资回报预测和储蓄目标规划等多种理财场景。'),
    "cover-letter-generator": ('提升求职效率。', '提升求职效率和面试邀约率。'),
    "credit-card-payoff": ('还款计划制定场景。', '还款计划制定和财务健康管理场景。'),
    "csv-merger": ('多源数据统一处理场景。', '多源数据统一处理和跨部门报表整合等场景。'),
    "csv-sorter": ('数据分析预处理等场景。', '数据分析和Excel导入前预处理等常用场景。'),
    "csv-transpose": ('报表重构等场景。', '报表重构和矩阵数据可视化准备等数据处理场景。'),
    "date-add": ('自动处理月末边界情况。', '自动处理月末边界情况（如1月31日加1个月自动适配2月天数）。'),
    "day-of-week-calculator": ('生日星期推算场景。', '生日星期推算和重要日期确认等多种日常场景。'),
    "day-of-week": ('纪念日推算场景。', '纪念日推算和节日规划等多种日常生活场景。'),
    "device-info": ('设备兼容性检测场景。', '设备兼容性检测和系统信息快速查看等实用场景。'),
    "auto-loan-calculator": ('，结果精准可靠。', '。此外还支持等额本金对比、提前还款计算和购车预算规划功能。'),
}

count = 0
for tool, (old_frag, new_frag) in ADDITIONS.items():
    filepath = f"{tool}/index.html"
    with open(filepath, 'r') as f:
        content = f.read()
    
    if old_frag not in content:
        print(f"  SKIP {tool}: old fragment not found")
        # Try finding current meta
        m = re.search(r'<meta name="description" content="([^"]+)"', content)
        if m:
            print(f"    Current: {m.group(1)[:100]}")
        continue
    
    content = content.replace(old_frag, new_frag, 1)
    
    with open(filepath, 'w') as f:
        f.write(content)
    
    m = re.search(r'<meta name="description" content="([^"]+)"', content)
    if m:
        new_len = len(m.group(1))
        # Update og:description and schema
        new_desc = m.group(1)
        og_pattern = r'<meta property="og:description" content="[^"]*">'
        og_replacement = f'<meta property="og:description" content="{new_desc}">'
        content2 = re.sub(og_pattern, og_replacement, content)
        schema_pattern = r'"description":\s*"[^"]*"'
        schema_replacement = f'"description": "{new_desc}"'
        content2 = re.sub(schema_pattern, schema_replacement, content2, count=1)
        with open(filepath, 'w') as f:
            f.write(content2)
        
        status = "✅" if 140 <= new_len <= 160 else "⚠️"
        print(f"  {status} {tool}: {new_len} chars")
        count += 1

print(f"\nTotal: {count}")