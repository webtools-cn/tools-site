#!/usr/bin/env python3
"""只修复current-issues.json中48个broken工具"""
import subprocess, re, os, json

BROKEN = [
    "ai-fine-tuning-cost-calculator", "dns-record-comparator", "dockerfile-formatter",
    "dockerfile-linter", "fancy-text-generator", "flexbox-layout-generator",
    "handwriting-generator", "html-entity-converter", "html-meta-refresh-generator",
    "html-table-of-contents", "html-table-to-json", "html-tag-stripper",
    "html-wysiwyg-editor", "http-cache-header-generator", "line-chart-maker",
    "markdown-link-checker", "markdown-previewer", "markdown-to-pdf-converter",
    "maze-generator", "md5-generator", "meta-tag-generator", "morse-code",
    "name-generator", "pdf-to-html", "pie-chart-maker", "privacy-policy-generator",
    "properties-to-yaml", "quiz-generator", "receipt-generator",
    "regex-character-class-generator", "regex-cheatsheet", "shopping-list-generator",
    "sitemap-validator", "sql-migration-generator", "sql-to-csv", "sql-to-kysely",
    "sql-to-prisma", "svg-to-data-uri", "terms-generator", "text-diff-checker",
    "text-normalizer", "text-palindrome-checker", "text-to-braille", "typing-test",
    "vite-config-generator", "word-search-generator", "workout-generator",
    "yaml-to-json"
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
        return None, 'already_ok'
    
    orig = content
    new_content = content
    changed = False
    
    # Fix 1: </script> inside JS strings → <\/script>
    pat = re.compile(r'<script[^>]*>(.*?)</script>', re.DOTALL)
    
    def fix_script_tags(m):
        nonlocal changed
        attrs_match = re.match(r'<script([^>]*)>', m.group(0))
        sc = m.group(1)
        tag_start = attrs_match.group(0) if attrs_match else '<script>'
        # Skip JSON-LD
        if sc.strip().startswith('{') and ('@context' in sc or '"@type"' in sc):
            return m.group(0)
        new_sc = sc
        if '</script>' in sc:
            new_sc = sc.replace('</script>', '<\\/script>')
            changed = True
        if '</style>' in sc:
            new_sc = new_sc.replace('</style>', '<\\/style>')
            changed = True
        return tag_start + new_sc + '</script>'
    
    new_content = pat.sub(fix_script_tags, new_content)
    
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
    
    # Fix 3: unclosed string - missing closing quote before EOL (common AI error)
    # e.g., `text+='隐私政策` without closing quote
    def fix_unclosed(m):
        nonlocal changed
        sc = m.group(1)
        if sc.strip().startswith('{') and ('@context' in sc or '"@type"' in sc):
            return m.group(0)
        
        # Fix unclosed single-quoted strings
        new_sc = re.sub(
            r"(?<!=)'(?![\s,;:})\]\\)\[{}(!=&|])",
            lambda m2: m2.group(0),
            sc
        )
        
        # Fix: text+='xxx or text='xxx without closing '  
        new_sc = re.sub(r"(text\+?=['\"])([^'\"]*?)$", r"\1\2'", new_sc, flags=re.MULTILINE)
        if new_sc != sc:
            changed = True
            return '<script>' + new_sc + '</script>'
        return m.group(0)
    new_content = pat.sub(fix_unclosed, new_content)
    
    # Fix 4: Unicode escapes like \uXXXXX that are too long (should be \uXXXX)
    def fix_unicode(m):
        nonlocal changed
        sc = m.group(1)
        if sc.strip().startswith('{') and ('@context' in sc or '"@type"' in sc):
            return m.group(0)
        # Fix \u with more than 4 hex digits
        new_sc = re.sub(r'\\u([0-9a-fA-F]{5,})', lambda m2: '\\u' + m2.group(1)[:4], sc)
        if new_sc != sc:
            changed = True
            return '<script>' + new_sc + '</script>'
        return m.group(0)
    new_content = pat.sub(fix_unicode, new_content)
    
    # Fix 5: Duplicate variable declarations
    def fix_dup_decl(m):
        nonlocal changed
        sc = m.group(1)
        if sc.strip().startswith('{') and ('@context' in sc or '"@type"' in sc):
            return m.group(0)
        seen = set()
        new_lines = []
        for line in sc.split('\n'):
            m2 = re.match(r'\s*(?:var|let|const)\s+(\w+)', line)
            if m2 and m2.group(1) in seen:
                # Remove var/let/const prefix, keep rest
                line = re.sub(r'\b(?:var|let|const)\s+(' + re.escape(m2.group(1)) + r')', r'\1', line, 1)
                changed = True
            elif m2:
                seen.add(m2.group(1))
            new_lines.append(line)
        return '<script>' + '\n'.join(new_lines) + '</script>'
    new_content = pat.sub(fix_dup_decl, new_content)
    
    # Fix 6: Python ternary: "X" if condition else "Y" → condition?"X":"Y"
    def fix_py_ternary(m):
        nonlocal changed
        sc = m.group(1)
        if sc.strip().startswith('{') and ('@context' in sc or '"@type"' in sc):
            return m.group(0)
        new_sc = re.sub(r'"([^"]*)"\s+if\s+(\w[\w.]*)\s+else\s+"([^"]*)"', r'(\2?"\1":"\3")', sc)
        new_sc = re.sub(r"'([^']*)'\s+if\s+(\w[\w.]*)\s+else\s+'([^']*)'", r"(\2?'\1':'\3')", new_sc)
        if new_sc != sc:
            changed = True
            return '<script>' + new_sc + '</script>'
        return m.group(0)
    new_content = pat.sub(fix_py_ternary, new_content)
    
    # Fix 7: catch() => → catch(e) =>
    def fix_catch(m):
        nonlocal changed
        sc = m.group(1)
        if sc.strip().startswith('{') and ('@context' in sc or '"@type"' in sc):
            return m.group(0)
        new_sc = re.sub(r'catch\s*\(\s*\)\s*=>', 'catch(e)=>', sc)
        if new_sc != sc:
            changed = True
            return '<script>' + new_sc + '</script>'
        return m.group(0)
    new_content = pat.sub(fix_catch, new_content)
    
    # Fix 8: Invalid regex patterns
    def fix_regex(m):
        nonlocal changed
        sc = m.group(1)
        if sc.strip().startswith('{') and ('@context' in sc or '"@type"' in sc):
            return m.group(0)
        # Fix regex with stray characters like [a-z|
        new_sc = re.sub(r'\[a-zA-Z\|', '[a-zA-Z]|', sc)
        if new_sc != sc:
            changed = True
            return '<script>' + new_sc + '</script>'
        return m.group(0)
    new_content = pat.sub(fix_regex, new_content)
    
    if changed and new_content != orig:
        with open(html_path, 'w') as f:
            f.write(new_content)
        new_js, _ = extract_js(html_path)
        ok2, err2 = check_js(new_js)
        if ok2:
            return True, 'fixed'
        else:
            # Revert
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
            if info == 'already_ok':
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
