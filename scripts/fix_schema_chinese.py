#!/usr/bin/env python3
"""Fix Schema Chinese in EN pages - 10 files"""
import re, glob, json

FIXES = {
    'en/extra-payment-calculator/index.html': {
        'old_schema_name': 'Extra Payment Calculator',
        'new_description': 'Free extra payment calculator. See how much interest and time you can save by paying extra on your monthly mortgage. Supports one-time and recurring extra payments.',
    },
    'en/hiking-time/index.html': {
        'new_description': 'Online hiking time calculator. Estimate hiking duration and calories burned based on distance, elevation gain, and difficulty level.',
    },
    'en/home-equity-calculator/index.html': {
        # Check actual
    },
    'en/metabolism-calculator/index.html': {
        'new_description': 'Online BMR calculator using the Mifflin-St Jeor equation. Estimate your daily calorie needs based on age, weight, height, and activity level.',
    },
    'en/web-performance-checker/index.html': {
        'new_description': 'Free online web performance checker. Analyze page size, resource count, image optimization, DOM complexity, and get actionable optimization recommendations. 100% client-side.',
    },
    'en/lead-conversion-rate-calculator/index.html': {
        'fix_duplicate_type': True,
    },
    'en/revenue-churn-calculator/index.html': {
        'fix_duplicate_type': True,
        'old_chinese_name': '📉 收入流失率计算器',
        'new_name': '📉 Revenue Churn Calculator',
    },
    'en/saas-mrr-calculator/index.html': {
        'fix_duplicate_type': True,
    },
    'en/startup-runway-calculator/index.html': {
        'fix_duplicate_type': True,
    },
    'en/viral-coefficient-calculator/index.html': {
        'fix_duplicate_type': True,
    },
}

def fix_duplicate_type_and_chinese(filepath, info):
    """Fix duplicate @type and remove Chinese from schema"""
    c = open(filepath, 'r', errors='ignore').read()
    orig = c
    
    # Pattern: schema block
    m = re.search(r'(<script type="application/ld\+json">)(.*?)(</script>)', c, re.DOTALL)
    if not m:
        return False
    
    schema_str = m.group(2)
    
    # Fix duplicate @type: remove the HowTo inline with SoftwareApplication
    # Pattern: "@type": "SoftwareApplication", "@type": "HowTo", "name": "...", "step": [...]
    # Replace: keep only SoftwareApplication, remove HowTo and its step array
    schema_str = re.sub(
        r',\s*"@type":\s*"HowTo",\s*"name":\s*"[^"]*",\s*"step":\s*\[[^\]]*\]',
        '',
        schema_str
    )
    
    # Fix Chinese name: replace Chinese name with English name
    if 'old_chinese_name' in info:
        schema_str = schema_str.replace(
            f'"name": "{info["old_chinese_name"]}"',
            f'"name": "{info["new_name"]}"'
        )
    
    # Also fix if there's any Chinese in the schema
    cn_char = re.compile(r'[\u4e00-\u9fff]')
    if cn_char.search(schema_str):
        # General: fix description with Chinese
        schema_str = re.sub(
            r'"description":\s*"[^"]*[\u4e00-\u9fff][^"]*"',
            lambda m: f'"description": "{info.get("new_description", "Online tool")}"',
            schema_str
        )
    
    c = c[:m.start(1)] + m.group(1) + schema_str + m.group(3) + c[m.end(3):]
    
    if c != orig:
        open(filepath, 'w').write(c)
        return True
    return False

def fix_description(filepath, info):
    """Fix Chinese in schema description"""
    c = open(filepath, 'r', errors='ignore').read()
    orig = c
    
    cn_char = re.compile(r'[\u4e00-\u9fff]')
    m = re.search(r'(<script type="application/ld\+json">)(.*?)(</script>)', c, re.DOTALL)
    if not m:
        return False
    
    schema_str = m.group(2)
    if cn_char.search(schema_str) and 'new_description' in info:
        # Replace description that has Chinese
        schema_str = re.sub(
            r'"description":\s*"[^"]*"',
            f'"description": "{info["new_description"]}"',
            schema_str
        )
        c = c[:m.start(1)] + m.group(1) + schema_str + m.group(3) + c[m.end(3):]
    
    if c != orig:
        open(filepath, 'w').write(c)
        return True
    return False

fixed = 0
for filepath, info in FIXES.items():
    if 'fix_duplicate_type' in info:
        if fix_duplicate_type_and_chinese(filepath, info):
            fixed += 1
            print(f'✅ Fixed dup type: {filepath}')
    elif 'new_description' in info:
        if fix_description(filepath, info):
            fixed += 1
            print(f'✅ Fixed desc: {filepath}')
    else:
        print(f'⚠️  Skipped: {filepath}')

print(f'\nTotal fixed: {fixed}')
