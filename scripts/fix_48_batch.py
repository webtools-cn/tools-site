#!/usr/bin/env python3
"""只对48个broken工具运行batch修复"""
import subprocess, re, os

BROKEN = [
    "ai-fine-tuning-cost-calculator","dns-record-comparator","dockerfile-formatter",
    "dockerfile-linter","fancy-text-generator","flexbox-layout-generator",
    "handwriting-generator","html-entity-converter","html-meta-refresh-generator",
    "html-table-of-contents","html-table-to-json","html-tag-stripper",
    "html-wysiwyg-editor","http-cache-header-generator","line-chart-maker",
    "markdown-link-checker","markdown-previewer","markdown-to-pdf-converter",
    "maze-generator","md5-generator","meta-tag-generator","morse-code",
    "name-generator","pdf-to-html","pie-chart-maker","privacy-policy-generator",
    "properties-to-yaml","quiz-generator","receipt-generator",
    "regex-character-class-generator","regex-cheatsheet","shopping-list-generator",
    "sitemap-validator","sql-migration-generator","sql-to-csv","sql-to-kysely",
    "sql-to-prisma","svg-to-data-uri","terms-generator","text-diff-checker",
    "text-normalizer","text-palindrome-checker","text-to-braille","typing-test",
    "vite-config-generator","word-search-generator","workout-generator","yaml-to-json"
]

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
    
    orig = content
    new_content = content
    changed = False
    
    pat = re.compile(r'<script>(.*?)</script>', re.DOTALL)
    
    # Fix 1: </style> and </script> in JS strings → escaped
    def fix_html_in_js(m):
        nonlocal changed
        sc = m.group(1)
        if sc.strip().startswith('{') and ('@context' in sc or '"@type"' in sc):
            return m.group(0)
        new_sc = sc
        if '</style>' in new_sc:
            new_sc = new_sc.replace('</style>', '<\\/style>')
            changed = True
        if '</script>' in new_sc:
            new_sc = new_sc.replace('</script>', '<\\/script>')
            changed = True
        return '<script>' + new_sc + '</script>'
    
    new_content = pat.sub(fix_html_in_js, new_content)
    
    # Fix 2: &nbsp; in JS → space
    def fix_nbsp(m):
        nonlocal changed
        sc = m.group(1)
        if sc.strip().startswith('{') and ('@context' in sc or '"@type"' in sc):
            return m.group(0)
        if '&nbsp;' in sc:
            changed = True
            return '<script>' + sc.replace('&nbsp;', ' ') + '</script>'
        return m.group(0)
    new_content = pat.sub(fix_nbsp, new_content)
    
    # Fix 3: Duplicate var/let/const declarations
    def fix_duplicates(m):
        nonlocal changed
        sc = m.group(1)
        if sc.strip().startswith('{') and ('@context' in sc or '"@type"' in sc):
            return m.group(0)
        seen = set()
        lines = sc.split('\n')
        new_lines = []
        for line in lines:
            m2 = re.match(r'(\s*)(?:let|const|var)\s+(\w+)', line)
            if m2:
                name = m2.group(2)
                if name in seen:
                    line = m2.group(1) + name + line[m2.end():]
                    changed = True
                else:
                    seen.add(name)
            new_lines.append(line)
        return '<script>' + '\n'.join(new_lines) + '</script>'
    new_content = pat.sub(fix_duplicates, new_content)
    
    # Fix 4: Python-style ternary: "X" if Y else "Z" → Y?"X":"Z"
    def fix_py_ternary(m):
        nonlocal changed
        sc = m.group(1)
        if sc.strip().startswith('{') and ('@context' in sc or '"@type"' in sc):
            return m.group(0)
        fixed = re.sub(r'"([^"]*)"\s+if\s+(\w[\w.]*)\s+else\s+"([^"]*)"', r'(\2?"\1":"\3")', sc)
        fixed = re.sub(r"'([^']*)'\s+if\s+(\w[\w.]*)\s+else\s+'([^']*)'", r"(\2?'\1':'\3')", fixed)
        if fixed != sc:
            changed = True
            return '<script>' + fixed + '</script>'
        return m.group(0)
    new_content = pat.sub(fix_py_ternary, new_content)
    
    # Fix 5: Unclosed single-quoted strings spanning lines
    # Pattern: text='xxx\n or text+='xxx\n without closing quote
    def fix_unclosed_strings(m):
        nonlocal changed
        sc = m.group(1)
        if sc.strip().startswith('{') and ('@context' in sc or '"@type"' in sc):
            return m.group(0)
        
        # Fix: var text='xxx\n' → var text='xxx\\n'
        fixed = re.sub(r"(=\s*)'([^']*?)\n'", r"\1'\2\\n'", sc)
        # Fix: text+='xxx\n' → text+='xxx\\n'
        fixed = re.sub(r"(\+=\s*)'([^']*?)\n'", r"\1'\2\\n'", fixed)
        if fixed != sc:
            changed = True
            return '<script>' + fixed + '</script>'
        return m.group(0)
    new_content = pat.sub(fix_unclosed_strings, new_content)
    
    # Fix 6: catch()=> → catch(e)=>
    def fix_catch(m):
        nonlocal changed
        sc = m.group(1)
        if sc.strip().startswith('{') and ('@context' in sc or '"@type"' in sc):
            return m.group(0)
        fixed = re.sub(r'catch\s*\(\s*\)\s*=>', 'catch(e)=>', sc)
        if fixed != sc:
            changed = True
            return '<script>' + fixed + '</script>'
        return m.group(0)
    new_content = pat.sub(fix_catch, new_content)
    
    # Fix 7: })(→ }) → }()
    # Already handled by simpler replacement below
    
    # Fix 8: html+='<!DOCTYPE → innerHTML issues
    # Skip - too complex for regex
    
    if changed and new_content != orig:
        with open(html_path, 'w') as f:
            f.write(new_content)
        new_js, _ = extract_js(html_path)
        ok2, err2 = check_js(new_js)
        if ok2:
            return True, 'fixed'
        else:
            with open(html_path, 'w') as f:
                f.write(orig)
            return False, f'still_broken: {err2[:100]}'
    
    return False, f'unfixable: {err[:100]}'

if __name__ == '__main__':
    fixed = []
    still = []
    already = []
    
    for tool in BROKEN:
        result, info = fix_tool(tool)
        if result is None:
            if info == 'ok':
                already.append(tool)
            continue
        if result:
            fixed.append(tool)
        else:
            still.append((tool, info))
    
    print(f"\n=== RESULTS ===")
    print(f"Already OK: {len(already)}")
    for t in already: print(f"  ⏭️ {t}")
    print(f"\nFixed: {len(fixed)}")
    for t in fixed: print(f"  ✅ {t}")
    print(f"\nStill broken: {len(still)}")
    for t, why in still: print(f"  ❌ {t}: {why}")