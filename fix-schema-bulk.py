#!/usr/bin/env python3
"""
Fix Schema issues across all tool pages:
1. Remove invalid "name" field from aggregateRating
2. Clean SoftwareApplication name (remove emoji, multi-line content)
3. Remove emoji from BreadcrumbList names
"""

import re, json, os

def remove_emoji(text):
    """Remove emoji and zero-width joiner characters from text"""
    result = []
    for ch in text:
        cp = ord(ch)
        if cp in (0xFE0F, 0x200D):  # variation selector, ZWJ
            continue
        if 0x1F000 <= cp <= 0x1FAFF:  # emoji
            continue
        if 0x2600 <= cp <= 0x27BF:  # misc symbols
            continue
        if 0x2B50 <= cp <= 0x2B55:  # stars, circles
            continue
        if cp == 0x00A9 or cp == 0x00AE:  # copyright, registered
            continue
        if 0x2300 <= cp <= 0x23FF:  # misc technical
            continue
        if 0x25A0 <= cp <= 0x25FF:  # geometric shapes
            continue
        if 0x20D0 <= cp <= 0x20FF:  # combining diacritical marks for symbols
            continue
        if 0x1F900 <= cp <= 0x1F9FF:  # supplemental symbols
            continue
        result.append(ch)
    return ''.join(result).strip()

def clean_sa_name(name):
    """Clean SoftwareApplication name"""
    name = name.split('\n')[0].strip()
    name = remove_emoji(name)
    name = re.sub(r'\s+', ' ', name).strip()
    return name

def fix_page(path):
    """Fix a single page. Returns (changed, fixes_list)"""
    with open(path) as f:
        html = f.read()
    
    original_html = html
    fixes = []
    
    # Find all JSON-LD blocks
    ld_scripts = list(re.finditer(r'<script type="application/ld\+json">(.*?)</script>', html, re.DOTALL))
    
    for m in ld_scripts:
        raw = m.group(1)
        try:
            d = json.loads(raw)
        except json.JSONDecodeError:
            continue
        
        # Handle array of schemas
        if isinstance(d, list):
            schemas = d
        else:
            schemas = [d]
        
        all_changed = False
        all_fixes = []
        new_schemas = []
        
        for d in schemas:
            changed = False
            t = d.get('@type', '')
            
            # Fix 1: Remove "name" from aggregateRating
            if 'aggregateRating' in d:
                ar = d['aggregateRating']
                if 'name' in ar:
                    del ar['name']
                    changed = True
                    all_fixes.append(f'removed name from aggregateRating in {t}')
            
            # Fix 2: Clean SoftwareApplication name
            if t == 'SoftwareApplication' and 'name' in d:
                old_name = d['name']
                new_name = clean_sa_name(old_name)
                if new_name != old_name:
                    d['name'] = new_name
                    changed = True
                    all_fixes.append(f'cleaned SA name: "{old_name[:30]}" -> "{new_name}"')
            
            # Fix 3: Clean BreadcrumbList names
            if t == 'BreadcrumbList':
                if 'name' in d:
                    old_name = d['name']
                    new_name = remove_emoji(old_name)
                    new_name = re.sub(r'\s+', ' ', new_name).strip()
                    if new_name != old_name:
                        d['name'] = new_name
                        changed = True
                        all_fixes.append(f'cleaned BL name: "{old_name}" -> "{new_name}"')
                for item in d.get('itemListElement', []):
                    if 'name' in item:
                        old_name = item['name']
                        new_name = remove_emoji(old_name)
                        new_name = re.sub(r'\s+', ' ', new_name).strip()
                        if new_name != old_name:
                            item['name'] = new_name
                            changed = True
                            all_fixes.append(f'cleaned BL item name: "{old_name}" -> "{new_name}"')
            
            # Fix 4: Clean FAQPage name
            if t == 'FAQPage' and 'name' in d:
                old_name = d['name']
                new_name = remove_emoji(old_name)
                new_name = re.sub(r'\s+', ' ', new_name).strip()
                if new_name != old_name:
                    d['name'] = new_name
                    changed = True
                    all_fixes.append(f'cleaned FAQ name')
            
            # Fix 5: Clean HowTo name
            if t == 'HowTo' and 'name' in d:
                old_name = d['name']
                new_name = remove_emoji(old_name)
                new_name = re.sub(r'\s+', ' ', new_name).strip()
                if new_name != old_name:
                    d['name'] = new_name
                    changed = True
                    all_fixes.append(f'cleaned HowTo name')
            
            if changed:
                all_changed = True
            
            new_schemas.append(d)
        
        if all_changed:
            # Re-serialize
            if isinstance(json.loads(raw), list):
                new_json = json.dumps(new_schemas, ensure_ascii=False, indent=2)
            else:
                new_json = json.dumps(new_schemas[0], ensure_ascii=False, indent=2)
            new_json = new_json.replace('<', '\\u003c').replace('>', '\\u003e')
            new_block = f'<script type="application/ld+json">{new_json}</script>'
            html = html.replace(m.group(0), new_block, 1)
            fixes = all_fixes
    
    if html != original_html:
        with open(path, 'w') as f:
            f.write(html)
        return True, fixes
    return False, []

# Run the fix
total_fixed = 0
all_fixes = []

for root, dirs, files in os.walk('.'):
    if '.git' in root:
        continue
    for fname in files:
        if fname != 'index.html':
            continue
        path = os.path.join(root, fname)
        changed, fixes = fix_page(path)
        if changed:
            total_fixed += 1
            all_fixes.extend(fixes)

print(f'Fixed {total_fixed} pages')
print(f'Total fixes applied: {len(all_fixes)}')

# Summary
fix_types = {}
for f in all_fixes:
    key = f.split(':')[0] if ':' in f else f
    fix_types[key] = fix_types.get(key, 0) + 1

print('\nFix summary:')
for k, v in sorted(fix_types.items(), key=lambda x: -x[1]):
    print(f'  {k}: {v}')
