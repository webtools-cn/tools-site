#!/usr/bin/env python3
"""终极JS修复：用acorn定位错误，然后尝试自动修复"""
import subprocess, re, os, json, sys

def extract_js_from_html(html_path):
    with open(html_path) as f:
        content = f.read()
    scripts = re.findall(r'<script>(.*?)</script>', content, re.DOTALL)
    js_parts = []
    for s in scripts:
        s = s.strip()
        if not s: continue
        if s.startswith('{') and ('@context' in s or '"@type"' in s): continue
        js_parts.append(s)
    return '\n'.join(js_parts) if js_parts else '', content

def check_js(js):
    r = subprocess.run(['node', '-c', '-'], input=js, capture_output=True, text=True, timeout=5)
    return r.returncode == 0, r.stderr.strip()

def try_fix_js(js, tool_name):
    """尝试多种修复策略"""
    fixed = js
    
    # Strategy 1: Fix HTML closing tags in strings
    for tag in ['style', 'script', 'div', 'table', 'html', 'head', 'body', 'a', 'p', 'tr', 'td', 'th', 'ul', 'ol', 'li', 'span', 'IfModule', 'FilesMatch', 'VirtualHost', 'Directory', 'Location', 'Proxy']:
        fixed = fixed.replace(f'</{tag}>', f'<\\/{tag}>')
    
    # Strategy 2: Fix &nbsp; &amp; etc
    fixed = fixed.replace('&nbsp;', ' ')
    fixed = fixed.replace('&amp;', '&')
    fixed = fixed.replace('&lt;', '<')
    fixed = fixed.replace('&gt;', '>')
    fixed = fixed.replace('&quot;', '"')
    
    # Strategy 3: Fix Python ternary
    fixed = re.sub(r'"([^"]+)"\s+if\s+(\w+)\s+else\s+"([^"]+)"', r'(\2?"\1":"\3")', fixed)
    fixed = re.sub(r"'([^']+)'\s+if\s+(\w+)\s+else\s+'([^']+)'", r"(\2?'\1':'\3')", fixed)
    
    # Strategy 4: Fix duplicate const/let declarations
    for kw in ['const', 'let']:
        names = re.findall(rf'{kw}\s+(\w+)\s*=', fixed)
        seen = set()
        for name in names:
            if name in seen:
                # Replace second occurrence
                fixed = re.sub(rf'{kw}\s+{re.escape(name)}\s*=', f'{name} =', fixed, 1)
            seen.add(name)
    
    # Strategy 5: Fix unquoted object properties with spaces/Chinese
    # {Gunning Fog指数: → {"Gunning Fog指数":
    fixed = re.sub(r'\{([A-Z][a-z]+\s[A-Za-z\u4e00-\u9fff\u0080-\uffff]+):', r'{"\1":', fixed)
    # {年级 +Math → {"年级" +Math  -- no, this is different
    
    # Strategy 6: Fix single-quoted strings containing apostrophes
    # 'Don't' → "Don't"
    # Find patterns like 'word'word' and replace outer quotes
    fixed = re.sub(r"'([^']*)'([^':;,)\]}=\s])", lambda m: '"' + m.group(1) + '"' + m.group(2) if "'" in m.group(1) else m.group(0), fixed)
    
    # Strategy 7: Fix broken regex - common pattern /[!\"#$%&\'()*+,\\-./:;<=>?@[\\]^_`{|}~]/
    # Replace with properly escaped version
    fixed = re.sub(r'/\[!\\\\"#\$%&\'\(\)\*\+,\\\\\\-\./:;<=>\?@\[\\\\\]\^_`\{\\|\}~\]/g?', r'/[!"#$%&\'()*+,\\-./:;<=>?@[\\]^_`{|}~]/g', fixed)
    
    # Strategy 8: Fix 'double declining' as object key
    fixed = fixed.replace("double declining:", '"double declining":')
    fixed = fixed.replace("'double declining':", '"double declining":')
    
    # Strategy 9: Fix broken ternary like ==='sqlite'?'sqlite':'sqlite';
    # This is actually valid JS but wrong logic - skip
    
    # Strategy 10: Fix </ in template literals that break HTML parsing
    # Already handled by Strategy 1
    
    return fixed

def apply_fix_to_html(content, old_js, new_js):
    """Replace JS in HTML content"""
    # Find the script block containing old_js and replace
    if old_js in content:
        return content.replace(old_js, new_js, 1)
    return content

SKIP = {'_gen','__pycache__','en','libs','js','css','scripts','tools',
        '.git','data','about','blog','privacy-policy','terms-of-service','category',
        'calc','design','dev','fun','health','image','math','media','network',
        'office','pdf','security','seo','text','utility'}

fixed_total = 0
still_broken = []

for d in sorted(os.listdir('.')):
    if not os.path.isdir(d) or d in SKIP or d.startswith('.'): continue
    f = f'{d}/index.html'
    if not os.path.exists(f): continue
    
    js, content = extract_js_from_html(f)
    if not js: continue
    ok, err = check_js(js)
    if ok: continue
    
    # Try fixing
    fixed_js = try_fix_js(js, d)
    if fixed_js == js:
        still_broken.append(d)
        continue
    
    # Apply fix to HTML
    new_content = content
    # Replace each script block
    scripts = list(re.finditer(r'<script>(.*?)</script>', content, re.DOTALL))
    for m in reversed(scripts):
        sc = m.group(1).strip()
        if not sc: continue
        if sc.startswith('{') and ('@context' in sc or '"@type"' in sc): continue
        fixed_sc = try_fix_js(sc, d)
        if fixed_sc != sc:
            new_content = new_content[:m.start()] + '<script>' + fixed_sc + '</script>' + new_content[m.end():]
    
    if new_content != content:
        with open(f, 'w') as fh:
            fh.write(new_content)
        new_js, _ = extract_js_from_html(f)
        ok2, err2 = check_js(new_js)
        if ok2:
            fixed_total += 1
            print(f'✅ {d}')
        else:
            with open(f, 'w') as fh:
                fh.write(content)
            still_broken.append(d)
    else:
        still_broken.append(d)

print(f'\nFixed: {fixed_total}')
print(f'Still broken: {len(still_broken)}')
for t in still_broken:
    print(f'  ❌ {t}')
