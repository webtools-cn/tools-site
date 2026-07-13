#!/usr/bin/env python3
"""Add related-tools HTML container + JS to all tool pages that lack them. Simple and reliable."""
import os

def fix_page(filepath, is_en):
    with open(filepath, 'r', errors='ignore') as f:
        content = f.read()
    
    changed = False
    
    # Add CSS link if missing
    if 'related-tools.css' not in content:
        content = content.replace('</head>', '<link rel="stylesheet" href="https://free-toolbase.com/related-tools.css">\n</head>', 1)
        changed = True
    
    # Add HTML container if missing
    if 'id="related-tools-section"' not in content:
        section_html = '\n<div class="related-tools-section" id="related-tools-section"><div class="related-tools-loading">Loading related tools...</div></div>\n'
        content = content.replace('</body>', section_html + '</body>', 1)
        changed = True
    
    # Add JS if missing (check for the fetch to related-tools.json)
    if 'related-tools.json' not in content:
        js_code = '''<script>
(function(){var s=document.getElementById('related-tools-section');if(!s)return;var p=window.location.pathname;var en=p.indexOf('/en/')!==-1;p=p.replace(/\\/en\\//g,'/');var slug=p.split('/').filter(Boolean).pop()||'';if(!slug){s.innerHTML='';return;}var depth=en?'../../':'../';fetch(depth+'related-tools.json').then(function(r){if(!r.ok)throw new Error('');return r.json();}).then(function(d){var data=en?d.en:d.cn;var t=data[slug];if(!t||!t.related||!t.related.length){s.innerHTML='';return;}var h='<div class="related-tools-inner"><h3 class="related-tools-title">'+(en?'🔗 You May Also Like':'🔗 相关工具推荐')+'</h3><div class="related-tools-grid">';t.related.forEach(function(r){var link=en?'../../en/'+r.slug+'/':'../'+r.slug+'/';h+='<a href="'+link+'" class="related-tool-card"><span class="related-tool-icon">'+(r.icon||'🔧')+'</span><span class="related-tool-name">'+r.name+'</span></a>';});h+='</div></div>';s.innerHTML=h;}).catch(function(){s.innerHTML='';});})();
</script>'''
        content = content.replace('</body>', js_code + '\n</body>', 1)
        changed = True
    
    if changed:
        with open(filepath, 'w', errors='ignore') as f:
            f.write(content)
    return changed

fixed = 0

# EN pages
for root, dirs, files in os.walk('en'):
    if 'index.html' in files:
        if '/tools/' in root or '/category/' in root or root == 'en':
            continue
        if fix_page(os.path.join(root, 'index.html'), True):
            fixed += 1

# CN pages
for root, dirs, files in os.walk('.'):
    if 'index.html' in files and '/en/' not in root and root != '.':
        parts = root.split('/')
        if len(parts) > 2 and parts[1] in ('tools', 'category'):
            continue
        if parts[0] == 'en':
            continue
        if fix_page(os.path.join(root, 'index.html'), False):
            fixed += 1

print(f"Fixed {fixed} pages")
