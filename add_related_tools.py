#!/usr/bin/env python3
"""Build related-tools.json from tools-registry.json and add related-tools section to all tool pages."""
import os, re, json

def load_registry():
    with open('tools-registry.json', 'r', errors='ignore') as f:
        return json.load(f)

def build_related_json(registry):
    """Build related-tools.json with same-category recommendations."""
    tools = registry.get('tools', [])
    
    # Build category map
    cat_map = {}  # category -> list of tools
    tool_map = {}  # slug -> tool info
    
    for t in tools:
        slug = t.get('slug', '')
        if not slug:
            continue
        cat = t.get('category', 'other')
        icon = t.get('icon', '🔧')
        
        # CN name
        cn_name = t.get('name', slug.replace('-', ' ').title())
        
        # EN name - try to get from seo.h1 or title
        en_name = slug.replace('-', ' ').title()
        seo = t.get('seo', {})
        if seo.get('h1'):
            en_name = seo['h1']
        
        tool_info = {
            'slug': slug,
            'name_cn': cn_name,
            'name_en': en_name,
            'icon': icon,
            'category': cat
        }
        
        tool_map[slug] = tool_info
        if cat not in cat_map:
            cat_map[cat] = []
        cat_map[cat].append(tool_info)
    
    # Build related-tools data
    en_data = {}
    cn_data = {}
    
    for slug, info in tool_map.items():
        cat = info['category']
        same_cat = [t for t in cat_map.get(cat, []) if t['slug'] != slug]
        
        # Pick up to 6 related tools from same category
        related = same_cat[:6]
        
        if related:
            en_data[slug] = {
                'name': info['name_en'],
                'related': [{'slug': r['slug'], 'name': r['name_en'], 'icon': r['icon']} for r in related]
            }
            cn_data[slug] = {
                'name': info['name_cn'],
                'related': [{'slug': r['slug'], 'name': r['name_cn'], 'icon': r['icon']} for r in related]
            }
    
    return {'en': en_data, 'cn': cn_data}

def add_related_tools_section(page_dir, is_en=True):
    """Add related-tools section (HTML container + JS) to a page."""
    filepath = os.path.join(page_dir, 'index.html')
    if not os.path.exists(filepath):
        return False
    
    with open(filepath, 'r', errors='ignore') as f:
        content = f.read()
    
    changed = False
    
    # Add CSS link if missing
    if 'related-tools.css' not in content:
        content = content.replace('</head>', '<link rel="stylesheet" href="https://free-toolbase.com/related-tools.css">\n</head>', 1)
        changed = True
    
    # Add HTML container if missing
    if 'id="related-tools-section"' not in content:
        # Insert before </body> or before the last script
        section_html = '\n<div class="related-tools-section" id="related-tools-section"><div class="related-tools-loading">Loading related tools...</div></div>\n'
        # Insert before </body>
        content = content.replace('</body>', section_html + '</body>', 1)
        changed = True
    
    # Add JS if missing
    if 'related-tools.js' not in content:
        # Add inline JS instead of external file for reliability
        js_code = '''<script>
(function() {
  'use strict';
  var s = document.getElementById('related-tools-section');
  if (!s) return;
  var p = window.location.pathname;
  var en = p.indexOf('/en/') !== -1;
  p = p.replace(/\\/en\\//g, '/');
  var slug = p.split('/').filter(Boolean).pop() || '';
  if (!slug) { s.innerHTML = ''; return; }
  var depth = en ? '../../' : '../';
  var u = depth + 'related-tools.json';
  fetch(u).then(function(r) {
    if (!r.ok) throw new Error('not found');
    return r.json();
  }).then(function(d) {
    var data = en ? d.en : d.cn;
    var t = data[slug];
    if (!t || !t.related || !t.related.length) { s.innerHTML = ''; return; }
    var h = '<div class="related-tools-inner"><h3 class="related-tools-title">'
      + (en ? '🔗 You May Also Like' : '🔗 相关工具推荐')
      + '</h3><div class="related-tools-grid">';
    t.related.forEach(function(r) {
      var link = en ? '../../en/' + r.slug + '/' : '../' + r.slug + '/';
      h += '<a href="' + link + '" class="related-tool-card">'
        + '<span class="related-tool-icon">' + (r.icon || '🔧') + '</span>'
        + '<span class="related-tool-name">' + r.name + '</span></a>';
    });
    h += '</div></div>';
    s.innerHTML = h;
  }).catch(function() { s.innerHTML = ''; });
})();
</script>'''
        content = content.replace('</body>', js_code + '\n</body>', 1)
        changed = True
    
    if changed:
        with open(filepath, 'w', errors='ignore') as f:
            f.write(content)
    
    return changed

def main():
    # Step 1: Build related-tools.json
    print("Building related-tools.json...")
    registry = load_registry()
    related_data = build_related_json(registry)
    
    with open('related-tools.json', 'w', encoding='utf-8') as f:
        json.dump(related_data, f, ensure_ascii=False, indent=2)
    
    en_count = len(related_data['en'])
    cn_count = len(related_data['cn'])
    print(f"  EN entries: {en_count}, CN entries: {cn_count}")
    
    # Step 2: Add related-tools section to all EN tool pages
    print("\nAdding related-tools section to EN pages...")
    en_fixed = 0
    for root, dirs, files in os.walk('en'):
        if 'index.html' in files:
            if '/tools/' in root or '/category/' in root or root == 'en':
                continue
            if add_related_tools_section(root, is_en=True):
                en_fixed += 1
    print(f"  EN pages fixed: {en_fixed}")
    
    # Step 3: Add related-tools section to all CN tool pages
    print("\nAdding related-tools section to CN pages...")
    cn_fixed = 0
    for root, dirs, files in os.walk('.'):
        if 'index.html' in files and '/en/' not in root and root != '.':
            parts = root.split('/')
            if len(parts) > 2 and parts[1] in ('tools', 'category'):
                continue
            if parts[0] == 'en':
                continue
            if add_related_tools_section(root, is_en=False):
                cn_fixed += 1
    print(f"  CN pages fixed: {cn_fixed}")
    
    print(f"\nTotal pages fixed: {en_fixed + cn_fixed}")

if __name__ == '__main__':
    main()
