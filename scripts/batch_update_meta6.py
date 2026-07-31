#!/usr/bin/env python3
"""Final push - add more to reach 140-160 for remaining pages."""
import re

ADDITIONS = {
    "backwards-text": ('结果。适合', '结果，同时显示字符数统计方便查看。适合'),
    "batch-rename": ('日常办公场景。', '日常办公场景，让繁琐的文件改名工作变得轻松高效。'),
    "business-card-maker": ('（经典白、商务蓝、极简黑等）自由切换。', '（经典白、商务蓝、极简黑、活力橙等）自由切换。'),
    "camera-recorder": ('多种场景。', '多种场景，录制后自动保存为WebM格式视频文件。'),
    "character-counter": ('SEO元描述长度检查等常用场景。', 'SEO元描述长度检查和微博/推特字数限制检测等常用场景。'),
    "compound-interest": ('等多种理财场景。', '等多种理财场景，帮你直观看到复利效应的长期力量。'),
    "cover-letter-generator": ('面试邀约率。', '面试邀约率，助你在求职竞争中脱颖而出。'),
    "credit-card-payoff": ('财务健康管理场景。', '财务健康管理场景，帮你早日摆脱信用卡债务负担。'),
    "csv-merger": ('跨部门报表整合等场景。', '跨部门报表整合和日志文件合并等常见数据处理场景。'),
    "csv-sorter": ('Excel导入前预处理等常用场景。', 'Excel导入前预处理和数据库批量导入等常见数据处理场景。'),
    "csv-transpose": ('矩阵数据可视化准备等数据处理场景。', '矩阵数据可视化准备和行列互换对比分析等数据处理场景。'),
    "date-add": ('（如1月31日加1个月自动适配2月天数）。', '（如1月31日加1个月自动适配为2月28日/29日）。'),
    "day-of-week-calculator": ('多种日常场景。', '多种日常场景，是查询任意日期星期的便捷实用工具。'),
    "day-of-week": ('等多种日常生活场景。', '等多种日常生活场景，附带日历视图让日期查询更加直观。'),
    "device-info": ('等实用场景。', '等实用场景，是排查浏览器兼容性问题的得力助手工具。'),
}

count = 0
for tool, (old_frag, new_frag) in ADDITIONS.items():
    filepath = f"{tool}/index.html"
    with open(filepath, 'r') as f:
        content = f.read()
    
    if old_frag not in content:
        print(f"  SKIP {tool}: old fragment not found")
        m = re.search(r'<meta name="description" content="([^"]+)"', content)
        if m:
            print(f"    Current ({len(m.group(1))}): ...{m.group(1)[-50:]}")
        continue
    
    content = content.replace(old_frag, new_frag, 1)
    
    with open(filepath, 'w') as f:
        f.write(content)
    
    m = re.search(r'<meta name="description" content="([^"]+)"', content)
    if m:
        new_len = len(m.group(1))
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