#!/usr/bin/env python3
"""Batch fix Chinese residues in EN pages: JS comments + Schema HowTo steps + mixed descriptions"""
import re, glob, os

def fix_js_comment(content):
    """Replace Chinese JS comments with English equivalents"""
    replacements = [
        ('// === 重写的函数实现 ===', '// === Implementation ==='),
        ('// 重写的函数实现', '// Implementation'),
        ('/* 重写的函数实现 */', '/* Implementation */'),
        ("'功能已触发'", "'Feature triggered'"),  # 部分页面用单引号
        ('"功能已触发"', '"Feature triggered"'),
        ('功能已触发', 'Feature triggered'),
        ("'已重置'", "'Reset'"),
        ('"已重置"', '"Reset"'),
        ("'已加载示例'", "'Sample loaded'"),
        ('"已加载示例"', '"Sample loaded"'),
        ("'没有可复制的结果'", "'Nothing to copy'"),
        ('"没有可复制的结果"', '"Nothing to copy"'),
        ("'已下载'", "'Downloaded'"),
        ('"已下载"', '"Downloaded"'),
    ]
    for old, new in replacements:
        content = content.replace(old, new)
    return content

def fix_schema_howto_steps(content):
    """Fix Chinese text in Schema.org HowTo steps"""
    # Common patterns: "text":"...中文..."
    cn_char = re.compile(r'[\u4e00-\u9fff]')
    
    # Find schema blocks
    schema_pattern = re.compile(r'(<script type="application/ld\+json">)(.*?)(</script>)', re.DOTALL)
    
    def fix_schema(m):
        schema = m.group(2)
        if not cn_char.search(schema):
            return m.group(0)
        
        # Fix step texts with Chinese
        def fix_step_text(sm):
            text = sm.group(1)
            # Common mixed Chinese patterns
            fixes = {
                '第': lambda t: t.replace('第', '').replace('years', 'years'),
            }
            # Remove all Chinese chars from step text
            cleaned = cn_char.sub('', text)
            # Clean up whitespace
            cleaned = re.sub(r'\s+', ' ', cleaned).strip()
            if not cleaned:
                cleaned = 'Follow the instructions'
            return f'"text":"{cleaned}"'
        
        schema = re.sub(r'"text":"([^"]*)"', fix_step_text, schema)
        
        # Fix name fields with Chinese
        def fix_name(sm):
            name = sm.group(1)
            cleaned = cn_char.sub('', name).strip()
            if not cleaned:
                cleaned = 'Step'
            return f'"name":"{cleaned}"'
        
        schema = re.sub(r'"name":"([^"]*[\u4e00-\u9fff][^"]*)"', fix_name, schema)
        
        # Fix description with Chinese
        def fix_desc(sm):
            desc = sm.group(1)
            cleaned = cn_char.sub('', desc).strip()
            if not cleaned:
                cleaned = 'Online tool'
            return f'"description":"{cleaned}"'
        
        schema = re.sub(r'"description":"([^"]*[\u4e00-\u9fff][^"]*)"', fix_desc, schema)
        
        return m.group(1) + schema + m.group(3)
    
    content = schema_pattern.sub(fix_schema, content)
    return content

def fix_mixed_descriptions(content):
    """Fix mixed Chinese-English descriptions in meta tags and visible text"""
    cn_char = re.compile(r'[\u4e00-\u9fff]')
    
    # Fix meta description
    def fix_meta(m):
        desc = m.group(1)
        if cn_char.search(desc):
            cleaned = cn_char.sub('', desc)
            cleaned = re.sub(r'\s+', ' ', cleaned).strip()
            if not cleaned:
                cleaned = 'Free online tool'
            return f'<meta name="description" content="{cleaned}">'
        return m.group(0)
    
    content = re.sub(r'<meta name="description" content="([^"]*)"', fix_meta, content)
    
    # Fix og:description
    content = re.sub(
        r'<meta property="og:description" content="([^"]*[\u4e00-\u9fff][^"]*)"',
        lambda m: f'<meta property="og:description" content="{cn_char.sub("", m.group(1)).strip()}"',
        content
    )
    
    return content

def fix_visible_chinese(content):
    """Fix visible Chinese text in EN pages (not in script/style tags)"""
    cn_char = re.compile(r'[\u4e00-\u9fff]')
    
    # Remove script and style blocks before checking visible content
    def has_visible_chinese(text):
        # Remove script and style blocks
        clean = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL)
        clean = re.sub(r'<style[^>]*>.*?</style>', '', clean, flags=re.DOTALL)
        return cn_char.search(clean) is not None
    
    return content  # Too complex to auto-fix visible text, skip for now

def fix_file(filepath):
    """Fix a single EN page"""
    try:
        content = open(filepath, 'r', errors='ignore').read()
        original = content
        
        # Apply fixes
        content = fix_js_comment(content)
        content = fix_schema_howto_steps(content)
        content = fix_mixed_descriptions(content)
        
        if content != original:
            open(filepath, 'w').write(content)
            return True
        return False
    except Exception as e:
        print(f'Error fixing {filepath}: {e}')
        return False

def main():
    en_files = sorted(glob.glob('en/*/index.html'))
    
    # First pass: identify files with issues
    cn_char = re.compile(r'[\u4e00-\u9fff]')
    issue_files = []
    for f in en_files:
        c = open(f, 'r', errors='ignore').read()
        # Exclude lang-switch 中文
        c_clean = re.sub(r'<a[^>]*href="[^"]*">中文</a>', '', c)
        if cn_char.search(c_clean):
            issue_files.append(f)
    
    print(f'Files with Chinese issues: {len(issue_files)}')
    
    fixed = 0
    for f in issue_files[:50]:  # Process first 50 this round
        if fix_file(f):
            fixed += 1
            if fixed <= 10:
                print(f'✅ Fixed: {f}')
    
    print(f'\nFixed {fixed}/{min(50, len(issue_files))} files')
    
    # Verify remaining
    remaining = 0
    for f in en_files:
        c = open(f, 'r', errors='ignore').read()
        c_clean = re.sub(r'<a[^>]*href="[^"]*">中文</a>', '', c)
        if cn_char.search(c_clean):
            remaining += 1
    
    print(f'Remaining after fix: {remaining}')

if __name__ == '__main__':
    main()