#!/usr/bin/env python3
"""修复所有 page 中 schema JSON 的 description 与 meta description 不一致的问题。
处理两种JSON格式：script标签中的JSON-LD和行内JSON。"""
import re, os, glob

def fix_schema_descriptions(html_content, meta_desc):
    """将HTML内容中所有JSON description字段替换为meta_desc（正确处理转义）"""
    
    # 策略：找到所有 <script type="application/ld+json"> 块，替换其中的 description
    def replace_in_script_block(match):
        block = match.group(0)
        # 在JSON块内，替换 "description": "..."  为  "description": "meta_desc转义版"
        # 需要：把meta_desc中的 " 转成 \" , \ 转成 \\
        escaped = meta_desc.replace('\\', '\\\\').replace('"', '\\"')
        # 匹配 "description": "任意非空内容"
        block = re.sub(
            r'"description"\s*:\s*"(?:[^"\\]|\\.)*"',
            f'"description": "{escaped}"',
            block
        )
        return block
    
    html_content = re.sub(
        r'<script type="application/ld\+json">.*?</script>',
        replace_in_script_block,
        html_content,
        flags=re.DOTALL
    )
    
    return html_content

count = 0
for path in sorted(glob.glob('*/index.html')):
    c = open(path).read()
    if 'meta http-equiv="refresh"' in c:
        continue
    
    mm = re.search(r'<meta name="description" content="([^"]+)"', c)
    if not mm:
        continue
    meta_desc = mm.group(1)
    
    fixed = fix_schema_descriptions(c, meta_desc)
    
    if fixed != c:
        # 验证修复后的一致性
        # 从fixed中提取schema description验证
        sm = re.search(r'<script type="application/ld\+json">.*?</script>', fixed, re.DOTALL)
        if sm:
            sblock = sm.group(0)
            sd = re.search(r'"description"\s*:\s*"((?:[^"\\]|\\.)*)"', sblock)
            if sd:
                schema_desc = sd.group(1).replace('\\"', '"').replace('\\\\', '\\')
                if schema_desc == meta_desc:
                    open(path, 'w').write(fixed)
                    count += 1
                else:
                    print(f'SKIP {path}: schema desc still differs after fix')
                    continue
            else:
                # 可能只有一个description字段被匹配
                open(path, 'w').write(fixed)
                count += 1
        else:
            open(path, 'w').write(fixed)
            count += 1

print(f'Total schema desc synced: {count}')