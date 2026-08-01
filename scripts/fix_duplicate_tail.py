#!/usr/bin/env python3
"""
Production fix: Remove duplicate tail phrases from meta descriptions.
Keeps the first unique occurrence of content, removes all duplicates after.
Targets: eliminate repetition, keep length 100-160 where possible.
"""
import re, sys

FULL_TAIL = '纯前端本地处理，数据不上传服务器，无需注册完全免费'

def deduplicate_desc(desc):
    """Remove duplicate phrases intelligently."""
    # Split description into sentences/clauses
    # Find where the tail repetition starts
    first_tail = desc.find(FULL_TAIL)
    if first_tail == -1:
        return desc
    
    # Count occurrences
    count = desc.count(FULL_TAIL)
    if count <= 1:
        return desc
    
    # Get content before the second occurrence
    second_tail = desc.find(FULL_TAIL, first_tail + len(FULL_TAIL))
    if second_tail == -1:
        return desc
    
    # Content between first and second tail
    between = desc[first_tail + len(FULL_TAIL):second_tail].strip('。，, .；')
    
    # Build clean version: prefix + between (if meaningful) + one tail
    prefix = desc[:first_tail].rstrip('。，, .；')
    
    # If between has meaningful unique content (not just junk), keep it
    if between and len(between) > 5 and between not in ['纯前端本地处理', '数据不上传', '无需注册', '完全免费', '免费']:
        # Only keep if it's not already in prefix
        if between not in prefix:
            prefix = prefix + '。' + between
    
    # Clean prefix: remove any partial tail fragments
    for fragment in ['纯前端本地处理', '数据不上传服务器', '无需注册完全免费', '纯前端', '数据不上传']:
        # Remove trailing fragment if prefix ends with it
        if prefix.endswith(fragment):
            prefix = prefix[:-len(fragment)].rstrip('。，, .；')
    
    result = prefix + '。' + FULL_TAIL + '。'
    
    # Clean up double punctuation
    result = result.replace('。。', '。').replace('，，', '，')
    
    # If too long, trim
    if len(result) > 160:
        max_prefix = 155 - len(FULL_TAIL)
        prefix = prefix[:max_prefix]
        for sep in ['。', '，', '、', ' ']:
            pos = prefix.rfind(sep)
            if pos > 50:
                prefix = prefix[:pos]
                break
        result = prefix + '。' + FULL_TAIL + '。'
    
    return result

def fix_file(filepath):
    with open(filepath) as f:
        content = f.read()
    m = re.search(r'(<meta name="description" content=")([^"]+)(")', content)
    if not m:
        return False
    desc = m.group(2)
    if desc.count(FULL_TAIL) <= 1:
        return False
    new_desc = deduplicate_desc(desc)
    if new_desc == desc:
        return False
    new_content = content[:m.start(2)] + new_desc + content[m.end(2):]
    with open(filepath, 'w') as f:
        f.write(new_content)
    return True, len(desc), len(new_desc)

if __name__ == '__main__':
    files = sys.argv[1:]
    count = 0
    for f in files:
        result = fix_file(f)
        if result:
            ok, old_len, new_len = result
            print(f'  {f}: {old_len} -> {new_len} chars')
            count += 1
    print(f'Fixed: {count}/{len(files)}')