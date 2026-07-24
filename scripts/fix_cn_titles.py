#!/usr/bin/env python3
"""
Fix CN tool page titles: Replace generic '工具名 - 免费在线工具|纯前端本地处理' 
with SEO-optimized titles based on EN version descriptions.

Strategy: 
1. Read CN title, extract tool name
2. Read EN title for the same tool, extract keywords
3. Generate CN title: '免费{工具名} - {核心功能} | 无需注册'
4. Fallback: Extract meaningful description from meta description
"""

import glob, re, os, json

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIXES = []

def clean_name(name):
    """Clean tool name for use in title"""
    name = name.strip()
    # Remove leading '在线'
    name = re.sub(r'^在线', '', name)
    # Remove trailing suffixes
    name = re.sub(r'(工具|生成器|转换器|检查器|计算器|编辑器|查找器|提取器|解析器|验证器)$', '', name)
    return name.strip()

def load_en_title(tool_dir):
    """Get EN version title for reference"""
    en_path = os.path.join(BASE, 'en', tool_dir, 'index.html')
    if not os.path.exists(en_path):
        return None
    with open(en_path) as f:
        content = f.read()
    m = re.search(r'<title>(.*?)</title>', content, re.DOTALL)
    if m:
        return m.group(1).strip()
    return None

def load_cn_desc(tool_dir):
    """Get CN meta description"""
    cn_path = os.path.join(BASE, tool_dir, 'index.html')
    if not os.path.exists(cn_path):
        return None
    with open(cn_path) as f:
        content = f.read()
    m = re.search(r'<meta name="description" content="(.*?)">', content)
    if m:
        return m.group(1)
    return None

def derive_cn_title(tool_dir, current_title, en_title, cn_desc):
    """Derive a proper Chinese SEO title"""
    # Extract tool name from current title (before ' - ')
    name_part = current_title.split(' - ')[0].strip()
    # Remove leading '免费' if already present to avoid doubling
    name_part = re.sub(r'^免费', '', name_part)
    clean = clean_name(name_part)
    
    # Extract core functionality from EN title
    core_func = ''
    if en_title:
        # Clean EN title of boilerplate
        en_clean = en_title
        for phrase in ['Free ', 'Online ', ' | No Signup', ' | No signup', ' | Free ToolBase', ' | ToolBase', 
                       'Pure Frontend', ' | Pure Frontend', 'Free Online Tool', 'Free Online']:
            en_clean = en_clean.replace(phrase, '')
        en_clean = en_clean.strip()
        # Remove leading/trailing separators
        en_clean = en_clean.strip('|').strip('-').strip()
        
        # Extract benefit part from EN title
        parts = en_clean.split(' - ')
        if len(parts) > 1:
            core_func = parts[-1].strip()
        else:
            # Try from description
            pass
    
    # If EN-derived is empty or too generic, try from CN description
    if not core_func or len(core_func) < 5 or core_func.lower() in ['tool', 'tools', 'online tool']:
        if cn_desc:
            cn_desc_clean = cn_desc.replace('免费', '').replace('在线', '').strip()
            # Get meaningful first ~20 chars
            core_func = cn_desc_clean[:25].rstrip('，。！？,.:;')
    
    # Last resort fallback
    if not core_func or len(core_func) < 5:
        core_func = f'在线{clean}工具'
    
    # Ensure core_func isn't too long
    if len(core_func) > 40:
        core_func = core_func[:40]
    
    return f'免费{name_part} - {core_func} | 无需注册'

def fix_file(path, new_title, old_title):
    """Update title in file"""
    with open(path) as f:
        content = f.read()
    
    # Update <title>
    content = content.replace(f'<title>{old_title}</title>', f'<title>{new_title}</title>', 1)
    
    # Update og:title if it matches old pattern
    old_og = re.escape(old_title).replace(r'\ ', r'\s*')
    og_pattern = re.compile(r'<meta property="og:title" content="[^"]*">')
    # Only update og:title if it looks generic
    og_match = og_pattern.search(content)
    if og_match:
        og_content = og_match.group()
        if '免费在线工具' in og_content or old_title.split(' - ')[0].replace('免费','').strip() in og_content:
            content = content.replace(og_content, f'<meta property="og:title" content="{new_title}">', 1)
    
    with open(path, 'w') as f:
        f.write(content)
    
    return True

def main():
    total = 0
    fixed = 0
    skipped = 0
    errors = []
    
    for cn_path in sorted(glob.glob(os.path.join(BASE, '*', 'index.html'))):
        # Skip en/ and root index.html and directories that aren't tool pages
        rel = os.path.relpath(cn_path, BASE)
        if rel.startswith('en/') or rel == 'index.html':
            continue
        if rel.startswith('scripts/') or rel.startswith('css/') or rel.startswith('js/') or rel.startswith('quality/'):
            continue
        if rel.startswith('.'):
            continue
        
        tool_dir = os.path.basename(os.path.dirname(cn_path))
        
        with open(cn_path) as f:
            content = f.read()
        
        m = re.search(r'<title>(.*?)</title>', content, re.DOTALL)
        if not m:
            continue
        
        current_title = m.group(1).strip()
        total += 1
        
        # Only fix pages with the generic pattern
        if '免费在线工具|纯前端本地处理' in current_title or '免费在线工具|' in current_title:
            en_title = load_en_title(tool_dir)
            cn_desc = load_cn_desc(tool_dir)
            new_title = derive_cn_title(tool_dir, current_title, en_title, cn_desc)
            
            if new_title and new_title != current_title:
                try:
                    fix_file(cn_path, new_title, current_title)
                    fixed += 1
                    FIXES.append({'tool': tool_dir, 'old': current_title, 'new': new_title})
                    if fixed <= 10:  # Show first 10 changes
                        print(f'  ✓ {tool_dir}')
                        print(f'    Old: {current_title}')
                        print(f'    New: {new_title}')
                except Exception as e:
                    errors.append((tool_dir, str(e)))
                    skipped += 1
            else:
                skipped += 1
        else:
            skipped += 1
    
    print(f'\nTotal CN pages scanned: {total}')
    print(f'Fixed: {fixed}')
    print(f'Skipped: {skipped}')
    print(f'Errors: {len(errors)}')
    
    # Save report
    report_path = os.path.join(BASE, 'quality', 'cn_title_fixes.json')
    with open(report_path, 'w') as f:
        json.dump({'total': total, 'fixed': fixed, 'skipped': skipped, 'fixes': FIXES, 'errors': errors}, 
                  f, ensure_ascii=False, indent=2)
    print(f'Report saved to {report_path}')

if __name__ == '__main__':
    main()
