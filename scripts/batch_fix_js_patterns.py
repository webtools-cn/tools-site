#!/usr/bin/env python3
"""批量修复JS常见错误模式 - 针对AI生成工具的典型问题"""
import subprocess, re, os, sys

def extract_js(html_path):
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

def fix_tool(tool_dir):
    html_path = f'{tool_dir}/index.html'
    if not os.path.exists(html_path):
        return None, 'no_file'
    
    js, content = extract_js(html_path)
    if not js:
        return None, 'no_js'
    
    ok, err = check_js(js)
    if ok:
        return None, 'ok'
    
    new_content = content
    changed = False
    
    # Fix 1: </style> in JS strings → <\/style>
    if '</style>' in new_content:
        # Only replace within script blocks
        def fix_style_in_script(m):
            sc = m.group(1)
            if sc.strip().startswith('{') and ('@context' in sc or '"@type"' in sc):
                return m.group(0)
            if '</style>' in sc:
                changed_flag = True
                return '<script>' + sc.replace('</style>', '<\\/style>') + '</script>'
            return m.group(0)
        new_content = re.sub(r'<script>(.*?)</script>', fix_style_in_script, new_content, flags=re.DOTALL)
        if new_content != content:
            changed = True
    
    # Fix 2: </script> in JS strings → <\/script>
    if '</script>' in new_content and new_content != content:
        # Already handled by regex, skip
        pass
    
    # Fix 3: &nbsp; in JS → space
    if '&nbsp;' in new_content:
        def fix_nbsp_in_script(m):
            sc = m.group(1)
            if sc.strip().startswith('{') and ('@context' in sc or '"@type"' in sc):
                return m.group(0)
            if '&nbsp;' in sc:
                return '<script>' + sc.replace('&nbsp;', ' ') + '</script>'
            return m.group(0)
        old = new_content
        new_content = re.sub(r'<script>(.*?)</script>', fix_nbsp_in_script, new_content, flags=re.DOTALL)
        if new_content != old:
            changed = True
    
    # Fix 4: Duplicate variable declarations (Identifier already declared)
    # Find duplicate var/let/const declarations in same script block
    def fix_duplicates(m):
        sc = m.group(1)
        if sc.strip().startswith('{') and ('@context' in sc or '"@type"' in sc):
            return m.group(0)
        # Find duplicate var declarations
        decls = re.findall(r'(var|let|const)\s+(\w+)\s*=', sc)
        seen = {}
        for typ, name in decls:
            key = name
            if key in seen:
                # Replace second occurrence's var/let/const with empty
                sc = re.sub(r'(var|let|const)\s+' + re.escape(name) + r'\s*=', name + ' =', sc, 1)
            else:
                seen[key] = True
        return '<script>' + sc + '</script>'
    old = new_content
    new_content = re.sub(r'<script>(.*?)</script>', fix_duplicates, new_content, flags=re.DOTALL)
    if new_content != old:
        changed = True
    
    # Fix 5: Python-style if/else in JS (e.g., "value" if condition else "other")
    # Replace: X if Y else Z → Y ? X : Z
    def fix_python_ifelse(m):
        sc = m.group(1)
        if sc.strip().startswith('{') and ('@context' in sc or '"@type"' in sc):
            return m.group(0)
        # Pattern: "string" if variable else "string2"
        fixed = re.sub(r'"([^"]+)"\s+if\s+(\w+)\s+else\s+"([^"]+)"', r'(\2?"\1":"\3")', sc)
        fixed = re.sub(r"'([^']+)'\s+if\s+(\w+)\s+else\s+'([^']+)'", r"(\2?'\1':'\3')", fixed)
        if fixed != sc:
            return '<script>' + fixed + '</script>'
        return m.group(0)
    old = new_content
    new_content = re.sub(r'<script>(.*?)</script>', fix_python_ifelse, new_content, flags=re.DOTALL)
    if new_content != old:
        changed = True
    
    # Fix 6: Object property names with spaces/special chars not quoted
    # e.g., {Gunning Fog指数: 8} → {"Gunning Fog指数": 8}
    def fix_unquoted_props(m):
        sc = m.group(1)
        if sc.strip().startswith('{') and ('@context' in sc or '"@type"' in sc):
            return m.group(0)
        # Match {ChineseOrSpecialKey: value} patterns
        fixed = re.sub(r'\{([^\w"\'`{\[][\w\u4e00-\u9fff\s]+):', r'{"\1":', sc)
        if fixed != sc:
            return '<script>' + fixed + '</script>'
        return m.group(0)
    old = new_content
    new_content = re.sub(r'<script>(.*?)</script>', fix_unquoted_props, new_content, flags=re.DOTALL)
    if new_content != old:
        changed = True
    
    # Fix 7: Don't/apostrophes in single-quoted strings
    # e.g., 'Don't' → "Don't" or 'Don\'t'
    def fix_apostrophes(m):
        sc = m.group(1)
        if sc.strip().startswith('{') and ('@context' in sc or '"@type"' in sc):
            return m.group(0)
        # Replace 'Don't' style with "Don't"
        fixed = re.sub(r"'([^']*)'([^':;,)\]}=\s])", lambda m: '"' + m.group(1) + '"' + m.group(2) if "'" in m.group(1) else m.group(0), sc)
        if fixed != sc:
            return '<script>' + fixed + '</script>'
        return m.group(0)
    
    if changed or new_content != content:
        with open(html_path, 'w') as f:
            f.write(new_content)
        new_js, _ = extract_js(html_path)
        ok2, err2 = check_js(new_js)
        if ok2:
            return True, 'fixed'
        else:
            # Revert
            with open(html_path, 'w') as f:
                f.write(content)
            return False, f'still_broken_after_fix'
    
    return False, 'no_applicable_fix'

if __name__ == '__main__':
    SKIP = {'_gen','__pycache__','en','libs','js','css','scripts','tools',
            '.git','data','about','blog','privacy-policy','terms-of-service','category',
            'calc','design','dev','fun','health','image','math','media','network',
            'office','pdf','security','seo','text','utility'}
    
    fixed = []
    still_broken = []
    
    for d in sorted(os.listdir('.')):
        if not os.path.isdir(d) or d in SKIP or d.startswith('.'): continue
        f = f'{d}/index.html'
        if not os.path.exists(f): continue
        
        result, info = fix_tool(d)
        if result is None:
            continue
        if result:
            fixed.append(d)
        else:
            still_broken.append(d)
    
    print(f"Fixed: {len(fixed)}")
    for t in fixed:
        print(f"  ✅ {t}")
    print(f"\nStill broken: {len(still_broken)}")
    for t in still_broken:
        print(f"  ❌ {t}")
