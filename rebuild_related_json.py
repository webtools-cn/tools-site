#!/usr/bin/env python3
"""Rebuild related-tools.json with correct EN names from actual page titles."""
import os, re, json

def load_registry():
    with open('tools-registry.json', 'r', errors='ignore') as f:
        return json.load(f)

def get_en_name_from_page(slug):
    """Extract English name from the EN page title."""
    filepath = os.path.join('en', slug, 'index.html')
    if not os.path.exists(filepath):
        return slug.replace('-', ' ').title()
    with open(filepath, 'r', errors='ignore') as f:
        content = f.read()
    # Try to get from <h1>
    h1_match = re.search(r'<h1[^>]*>([^<]+)</h1>', content)
    if h1_match:
        return h1_match.group(1).strip()
    # Fallback to title
    title_match = re.search(r'<title>([^<]+)</title>', content)
    if title_match:
        title = title_match.group(1)
        # Remove common suffixes
        for sep in [' - ', ' | ', ' · ']:
            if sep in title:
                title = title.split(sep)[0]
        return title.strip()
    return slug.replace('-', ' ').title()

def get_cn_name_from_page(slug):
    """Extract Chinese name from the CN page title."""
    filepath = os.path.join(slug, 'index.html')
    if not os.path.exists(filepath):
        return slug.replace('-', ' ').title()
    with open(filepath, 'r', errors='ignore') as f:
        content = f.read()
    h1_match = re.search(r'<h1[^>]*>([^<]+)</h1>', content)
    if h1_match:
        return h1_match.group(1).strip()
    title_match = re.search(r'<title>([^<]+)</title>', content)
    if title_match:
        title = title_match.group(1)
        for sep in [' - ', ' | ', ' · ']:
            if sep in title:
                title = title.split(sep)[0]
        return title.strip()
    return slug.replace('-', ' ').title()

def build_related_json(registry):
    """Build related-tools.json with correct EN/CN names."""
    tools = registry.get('tools', [])
    
    # Build category map
    cat_map = {}
    tool_slugs_by_cat = {}
    
    for t in tools:
        slug = t.get('slug', '')
        if not slug:
            continue
        cat = t.get('category', 'other')
        icon = t.get('icon', '🔧')
        
        if cat not in tool_slugs_by_cat:
            tool_slugs_by_cat[cat] = []
        tool_slugs_by_cat[cat].append({'slug': slug, 'icon': icon})
    
    # Build data with correct names
    en_data = {}
    cn_data = {}
    
    all_slugs = [t.get('slug', '') for t in tools if t.get('slug')]
    
    # Process in batches for efficiency
    en_names = {}
    cn_names = {}
    
    print("Extracting EN names from pages...")
    for slug in all_slugs:
        en_names[slug] = get_en_name_from_page(slug)
    
    print("Extracting CN names from pages...")
    for slug in all_slugs:
        cn_names[slug] = get_cn_name_from_page(slug)
    
    print("Building related data...")
    for t in tools:
        slug = t.get('slug', '')
        if not slug:
            continue
        cat = t.get('category', 'other')
        icon = t.get('icon', '🔧')
        
        same_cat = [s for s in tool_slugs_by_cat.get(cat, []) if s['slug'] != slug]
        related = same_cat[:6]
        
        if related:
            en_data[slug] = {
                'name': en_names.get(slug, slug.replace('-', ' ').title()),
                'related': [{'slug': r['slug'], 'name': en_names.get(r['slug'], r['slug'].replace('-', ' ').title()), 'icon': r['icon']} for r in related]
            }
            cn_data[slug] = {
                'name': cn_names.get(slug, slug.replace('-', ' ').title()),
                'related': [{'slug': r['slug'], 'name': cn_names.get(r['slug'], r['slug'].replace('-', ' ').title()), 'icon': r['icon']} for r in related]
            }
    
    return {'en': en_data, 'cn': cn_data}

def main():
    print("Loading registry...")
    registry = load_registry()
    
    print("Building related-tools.json...")
    related_data = build_related_json(registry)
    
    with open('related-tools.json', 'w', encoding='utf-8') as f:
        json.dump(related_data, f, ensure_ascii=False, indent=2)
    
    en_count = len(related_data['en'])
    cn_count = len(related_data['cn'])
    print(f"Done! EN entries: {en_count}, CN entries: {cn_count}")
    
    # Verify a few
    for slug in ['password-generator', 'json-formatter', 'cron-generator']:
        if slug in related_data['en']:
            entry = related_data['en'][slug]
            print(f"  EN {slug}: name='{entry['name']}', related_count={len(entry['related'])}")
            if entry['related']:
                print(f"    first: {entry['related'][0]}")

if __name__ == '__main__':
    main()
