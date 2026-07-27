#!/usr/bin/env python3
"""
修复 no_related_tools 页面：注入 related-tools-section HTML + JS
修复 content_thin 跳过页：检查是否有足够的可见文字
"""
import json, re, os, sys

SITE = '/home/chison/tools-site'
RESULT_PATH = os.path.join(SITE, 'quality', 'quality_loop_result.json')

with open(RESULT_PATH, 'r') as f:
    result = json.load(f)

remaining = result.get('remaining_pages', {})

# 需要注入related-tools-section的页面
no_related_pages = []
for page_key, issues in remaining.items():
    if 'no_related_tools' in issues:
        parts = page_key.split(':', 1)
        lang = parts[0]
        slug = parts[1]
        no_related_pages.append((lang, slug))

# RELATED_TOOLS_SECTION模板
RELATED_ZH = """
<!-- Related Tools Section -->
<div id="related-tools-section" style="margin-top:32px"></div>
<style>
.related-tools-inner{max-width:900px;margin:0 auto;padding:0 16px}
.related-tools-title{color:#a5b4fc;margin-bottom:16px;font-size:1.1rem}
.related-tools-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:12px}
.related-tool-card{display:flex;align-items:center;gap:8px;padding:12px 16px;background:rgba(99,102,241,.06);border:1px solid rgba(99,102,241,.12);border-radius:8px;text-decoration:none;color:#cbd5e1;transition:all .2s;font-size:.9rem}
.related-tool-card:hover{background:rgba(99,102,241,.12);border-color:rgba(99,102,241,.25);transform:translateY(-1px)}
.related-tool-icon{font-size:1.2rem}
.related-tool-name{flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
</style>
<script>
(function(){
  var s = document.getElementById('related-tools-section');
  if (!s) return;
  var p = window.location.pathname;
  var en = p.indexOf('/en/') !== -1;
  p = p.replace(/\/en\//g, '/');
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
</script>
"""

RELATED_EN = """
<!-- Related Tools Section -->
<div id="related-tools-section" style="margin-top:32px"></div>
<style>
.related-tools-inner{max-width:900px;margin:0 auto;padding:0 16px}
.related-tools-title{color:#a5b4fc;margin-bottom:16px;font-size:1.1rem}
.related-tools-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:12px}
.related-tool-card{display:flex;align-items:center;gap:8px;padding:12px 16px;background:rgba(99,102,241,.06);border:1px solid rgba(99,102,241,.12);border-radius:8px;text-decoration:none;color:#cbd5e1;transition:all .2s;font-size:.9rem}
.related-tool-card:hover{background:rgba(99,102,241,.12);border-color:rgba(99,102,241,.25);transform:translateY(-1px)}
.related-tool-icon{font-size:1.2rem}
.related-tool-name{flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
</style>
<script>
(function(){
  var s = document.getElementById('related-tools-section');
  if (!s) return;
  var p = window.location.pathname;
  var en = p.indexOf('/en/') !== -1;
  p = p.replace(/\/en\//g, '/');
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
</script>
"""

# 注入related-tools-section
fixed_related = 0
for lang, slug in no_related_pages:
    if lang == 'cn':
        path = os.path.join(SITE, slug, 'index.html')
    else:
        path = os.path.join(SITE, 'en', slug, 'index.html')
    
    if not os.path.isfile(path):
        print(f"  SKIP {lang}:{slug} - file not found")
        continue
    
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    if 'related-tools-section' in content:
        print(f"  SKIP {lang}:{slug} - already has related-tools-section")
        continue
    
    related_html = RELATED_ZH if lang == 'cn' else RELATED_EN
    
    # 插入到</body>之前
    body_close = content.rfind('</body>')
    if body_close > 0:
        new_content = content[:body_close] + '\n' + related_html + '\n' + content[body_close:]
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        fixed_related += 1
        print(f"  FIXED related: {lang}:{slug}")
    else:
        print(f"  SKIP {lang}:{slug} - no </body>")

print(f"\nrelated-tools-section injected: {fixed_related}")

# 现在更新related-tools.json，为这些页面添加条目
# 加载
rt_path = os.path.join(SITE, 'related-tools.json')
with open(rt_path, 'r', encoding='utf-8') as f:
    rt = json.load(f)

def get_tool_name(path):
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            c = f.read()
        m = re.search(r'<title>([^<]+)</title>', c)
        if m:
            name = m.group(1).split(' - ')[0].split(' | ')[0].strip()
            name = re.sub(r'^(Free Online |免费在线)', '', name)
            if len(name) > 80:
                name = name[:77] + '...'
            return name
    except:
        pass
    return slug.replace('-', ' ').title()

rt_fixed = 0
for lang, slug in no_related_pages:
    if lang == 'cn':
        path = os.path.join(SITE, slug, 'index.html')
    else:
        path = os.path.join(SITE, 'en', slug, 'index.html')
    
    name = get_tool_name(path)
    
    # 选3个相关工具
    all_slugs = list(rt['cn'].keys()) if lang == 'cn' else list(rt['en'].keys())
    candidates = [s for s in all_slugs if s != slug]
    
    prefix = slug.split('-')[0] if '-' in slug else slug[:4]
    same_prefix = [s for s in candidates if s.startswith(prefix)]
    other = [s for s in candidates if not s.startswith(prefix)]
    
    selected = (same_prefix + other)[:3]
    if len(selected) < 3:
        selected = candidates[:3]
    
    related = []
    for s in selected:
        if lang == 'cn':
            entry = rt['cn'].get(s, {})
        else:
            entry = rt['en'].get(s, {})
        
        related_name = entry.get('name', s.replace('-',' ').title()) if entry else s.replace('-',' ').title()
        if len(related_name) > 40:
            related_name = related_name[:37] + '...'
        related.append({
            'slug': s,
            'name': related_name,
            'icon': '🔧'
        })
    
    if lang == 'cn':
        rt['cn'][slug] = {'name': name, 'related': related}
    else:
        rt['en'][slug] = {'name': name, 'related': related}
    
    rt_fixed += 1
    print(f"  ADDED to rt.json: {lang}:{slug} → {[r['slug'] for r in related]}")

with open(rt_path, 'w', encoding='utf-8') as f:
    json.dump(rt, f, ensure_ascii=False, indent=2)

print(f"\nrelated-tools.json entries added: {rt_fixed}")
print(f"\nTotal: {fixed_related} page injections + {rt_fixed} json entries")