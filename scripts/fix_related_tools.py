#!/usr/bin/env python3
"""批量修复不相关推荐 - 用同类工具替换占位推荐"""
import os, re, json

# Load tools data to find related tools by category
with open('tools-data-cn.json', 'r', errors='ignore') as f:
    tools_data = json.load(f)

# Build category map: slug -> category
slug_to_cat = {}
cat_to_slugs = {}
for cat, tools in tools_data.items():
    cat_to_slugs[cat] = []
    for t in tools:
        if len(t) < 4: continue
        slug = t[3].strip('/').split('/')[-1] if t[3] else ''
        if slug:
            slug_to_cat[slug] = cat
            cat_to_slugs[cat].append(slug)

# Generic placeholder recommendations to replace
PLACEHOLDER_RECS = ['年龄计算器', '体型计算器', '投诉信生成器']

cn_fixed = 0
en_fixed = 0

def get_related_tools(slug, count=3):
    """Get related tools from same category"""
    cat = slug_to_cat.get(slug, '')
    if not cat: return []
    same_cat = [s for s in cat_to_slugs.get(cat, []) if s != slug]
    if len(same_cat) >= count:
        return same_cat[:count]
    # If not enough in same category, add from adjacent categories
    return same_cat

# Fix CN pages
for d in sorted(os.listdir('.')):
    p = os.path.join(d, 'index.html')
    if not os.path.isfile(p) or d == 'en': continue
    c = open(p, 'r', errors='ignore').read()
    
    # Check if has placeholder recommendations
    has_placeholder = any(gr in c for gr in PLACEHOLDER_RECS)
    if not has_placeholder: continue
    
    # Find related tools section
    related_m = re.search(r'(相关工具推荐.*?</div>)', c, re.DOTALL)
    if not related_m: continue
    
    # Get replacement tools
    related = get_related_tools(d, 3)
    if not related: continue
    
    # Build new related tools HTML
    new_links = []
    for r_slug in related:
        r_name = r_slug.replace('-', ' ').title()
        # Try to get actual name from tools data
        for cat, tools in tools_data.items():
            for t in tools:
                if len(t) < 4: continue
                if t[3].strip('/').split('/')[-1] == r_slug:
                    r_name = t[1]
                    break
        new_links.append(f'<a href="../{r_slug}/" style="color:#06b6d4;text-decoration:none;font-size:14px;display:block;padding:6px 0">{r_name}</a>')
    
    # Replace the entire related tools div content
    old_section = related_m.group(1)
    new_section = f'<h2 style="color:#e2e8f0;font-size:18px;margin-bottom:12px">🔗 相关工具推荐</h2>\n  ' + '\n  '.join(new_links) + '\n</div>'
    
    # Find the container div and replace
    c = c.replace(old_section, new_section, 1)
    open(p, 'w', encoding='utf-8', errors='ignore').write(c)
    cn_fixed += 1

# Fix EN pages
PLACEHOLDER_RECS_EN = ['Age Calculator', 'Body Shape Calculator', 'Complaint Letter Generator']
for d in sorted(os.listdir('en')):
    p = os.path.join('en', d, 'index.html')
    if not os.path.isfile(p): continue
    c = open(p, 'r', errors='ignore').read()
    
    has_placeholder = any(gr in c for gr in PLACEHOLDER_RECS_EN)
    if not has_placeholder: continue
    
    related_m = re.search(r'(You May Also Like.*?</div>)', c, re.DOTALL)
    if not related_m: continue
    
    related = get_related_tools(d, 3)
    if not related: continue
    
    new_links = []
    for r_slug in related:
        r_name = r_slug.replace('-', ' ').title()
        new_links.append(f'<a href="../{r_slug}/" style="color:#06b6d4;text-decoration:none;font-size:14px;display:block;padding:6px 0">{r_name}</a>')
    
    old_section = related_m.group(1)
    new_section = f'<h3 style="color:#e2e8f0;font-size:18px;margin-bottom:12px">🔗 You May Also Like</h3>\n  ' + '\n  '.join(new_links) + '\n</div>'
    
    c = c.replace(old_section, new_section, 1)
    open(p, 'w', encoding='utf-8', errors='ignore').write(c)
    en_fixed += 1

print(f"CN related fixed: {cn_fixed}")
print(f"EN related fixed: {en_fixed}")
print(f"Total: {cn_fixed + en_fixed}")
