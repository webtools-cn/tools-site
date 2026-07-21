#!/usr/bin/env python3
"""终极修复脚本 - 打开每个文件直接看JS内容，做针对性修复"""
import subprocess, re, os

def check_js_in_file(path):
    with open(path) as f: c = f.read()
    scripts = re.findall(r'<script>(.*?)</script>', c, re.DOTALL)
    js = '\n'.join(s.strip() for s in scripts if s.strip() and not (s.strip().startswith('{') and ('@context' in s or '"@type"' in s)))
    if not js: return True, '', c
    r = subprocess.run(['node','-c','-'], input=js, capture_output=True, text=True, timeout=5)
    return r.returncode == 0, r.stderr.strip(), c

def fix_tool(tool):
    path = f'{tool}/index.html'
    if not os.path.exists(path): return 'NO_FILE'
    
    ok, err, content = check_js_in_file(path)
    if ok: return 'OK'
    
    orig = content
    
    # Strategy: extract the last <script> block (main JS), 
    # fix it by wrapping innerHTML/outerHTML values in template literals,
    # and reinsert
    
    # Find all script blocks
    script_blocks = list(re.finditer(r'(<script[^>]*>)(.*?)(</script>)', content, re.DOTALL))
    
    # Identify the main JS block (largest non-JSON-LD, non-GA script)
    main_idx = -1
    main_size = 0
    for i, m in enumerate(script_blocks):
        tag = m.group(1)
        body = m.group(2).strip()
        if 'src=' in tag or 'application/ld+json' in tag:
            continue
        if body.startswith('{') and ('@context' in body or '"@type"' in body):
            continue
        if 'window.dataLayer' in body or 'gtag' in body:
            continue
        if len(body) > main_size:
            main_size = len(body)
            main_idx = i
    
    if main_idx < 0:
        return 'NO_MAIN_JS'
    
    m = script_blocks[main_idx]
    if m is None:
        return 'NO_SCRIPT_MATCH'
    js_body = m.group(2)
    
    # Fix 1: Convert single-quoted multi-line innerHTML strings to template literals
    # Pattern: app.innerHTML='<div...' or x.innerHTML='<html>...
    # These often span logical lines with unescaped content
    fixed_js = js_body
    
    # Fix innerHTML='...  with potential HTML inside  
    # Check if innerHTML contains unescaped HTML that's breaking JS
    if "innerHTML='" in fixed_js:
        # Replace innerHTML='...' patterns with template literals
        # Very conservative: only fix when the string clearly contains HTML tags
        fixed_js = re.sub(
            r"(\w+\.innerHTML\s*=\s*)'([^']*<(?:div|html|head|body|style|span|table|tr|td|h\d|p|br|a\s|img|input|form|select|option)[^']*)'",
            r"\1`\2`",
            fixed_js
        )
    
    # Fix 2: document.write('... → document.write(`...`)
    fixed_js = re.sub(
        r"(win\.document\.write\()'([^']*<html[^']*)'",
        r"\1`\2`",
        fixed_js
    )
    fixed_js = re.sub(
        r"(document\.write\()'([^']*<html[^']*)'",
        r"\1`\2`",
        fixed_js
    )
    
    # Fix 3: textContent='... with HTML → use template literal
    fixed_js = re.sub(
        r"(\.textContent\s*=\s*)'([^']*<(?:head|meta|link|title)[^']*)'",
        r"\1`\2`",
        fixed_js
    )
    
    # Fix 4: Catch unclosed single quotes in multi-line string building
    # text+='...\n pattern (actual newline in source)
    fixed_js = re.sub(
        r"(\+=\s*)'([^'\n]*?)\n(?!\+|\))",
        r"\1`\2`\n",
        fixed_js
    )
    
    # Fix 5: var text='...\n without closing
    fixed_js = re.sub(
        r"(\btext\s*=\s*)'([^'\n]*?)\n\s*';",
        r"\1`\2`;",
        fixed_js
    )
    
    # Fix 6: Duplicate let/const declarations within the same script
    seen_decls = {}
    lines = fixed_js.split('\n')
    new_lines = []
    for line in lines:
        m = re.match(r'(\s*)(let|const|var)\s+(\w+)', line)
        if m:
            indent, kw, name = m.group(1), m.group(2), m.group(3)
            if name in seen_decls:
                line = indent + name + line[m.end():]
            else:
                seen_decls[name] = True
        new_lines.append(line)
    fixed_js = '\n'.join(new_lines)
    
    # Fix 7: catch()=> → catch(e)=>
    fixed_js = re.sub(r'catch\s*\(\s*\)\s*=>', 'catch(e)=>', fixed_js)
    
    # Fix 8: })(); → }());  (IIFE fix)
    if '})();' in fixed_js and '}());' not in fixed_js:
        fixed_js = fixed_js.replace('})();', '}());')
    
    if fixed_js == js_body:
        return f'NO_FIX_APPLIED: {err[:80]}'
    
    # Debug
    if m is None:
        return f'BUG: m is None at line 129, main_idx={main_idx}, n_blocks={len(script_blocks)}'
    
    # Rebuild content
    new_content = content[:m.start(2)] + fixed_js + content[m.end(2):]
    
    with open(path, 'w') as f: f.write(new_content)
    ok2, err2, _ = check_js_in_file(path)
    if ok2:
        return 'FIXED'
    else:
        with open(path, 'w') as f: f.write(orig)
        return f'REVERTED: {err2[:100]}'

BROKEN = ['ai-fine-tuning-cost-calculator','dns-record-comparator','dockerfile-formatter',
    'dockerfile-linter','fancy-text-generator','flexbox-layout-generator',
    'handwriting-generator','html-entity-converter','html-meta-refresh-generator',
    'html-table-of-contents','html-table-to-json','html-tag-stripper',
    'html-wysiwyg-editor','http-cache-header-generator',
    'markdown-link-checker','markdown-previewer','markdown-to-pdf-converter',
    'maze-generator','md5-generator','meta-tag-generator','morse-code',
    'name-generator','pdf-to-html',
    'privacy-policy-generator','properties-to-yaml','quiz-generator','receipt-generator',
    'regex-cheatsheet','shopping-list-generator',
    'sitemap-validator','sql-migration-generator','sql-to-csv','sql-to-kysely',
    'sql-to-prisma','svg-to-data-uri','terms-generator',
    'text-normalizer','text-palindrome-checker','text-to-braille','typing-test',
    'vite-config-generator','word-search-generator','workout-generator','yaml-to-json']

results = {'FIXED':[], 'OK':[], 'REVERTED':[], 'OTHER':[]}
for tool in BROKEN:
    r = fix_tool(tool)
    if r == 'FIXED': results['FIXED'].append(tool)
    elif r == 'OK': results['OK'].append(tool)
    elif r.startswith('REVERTED'): results['REVERTED'].append((tool, r))
    else: results['OTHER'].append((tool, r))

print(f"\n=== RESULTS ===")
print(f"FIXED: {len(results['FIXED'])}")
for t in results['FIXED']: print(f'  ✅ {t}')
print(f"\nAlready OK: {len(results['OK'])}")
for t in results['OK']: print(f'  ⏭️ {t}')
print(f"\nREVERTED: {len(results['REVERTED'])}")
for t, why in results['REVERTED']: print(f'  ❌ {t}: {why[:120]}')
print(f"\nOTHER: {len(results['OTHER'])}")
for t, why in results['OTHER']: print(f'  ⚠️ {t}: {why[:120]}')
