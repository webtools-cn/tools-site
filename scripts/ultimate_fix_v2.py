#!/usr/bin/env python3
"""终极修复v2 - 逐个修复JS语法错误"""
import subprocess, re, os

def extract_main_js(content):
    """Extract main JS block for syntax check"""
    scripts = re.findall(r'<script>(.*?)</script>', content, re.DOTALL)
    parts = []
    for s in scripts:
        s = s.strip()
        if not s: continue
        if s.startswith('{') and ('@context' in s or '"@type"' in s): continue
        parts.append(s)
    return '\n'.join(parts) if parts else ''

def check_syntax(js):
    if not js: return True, ''
    r = subprocess.run(['node','-c','-'], input=js, capture_output=True, text=True, timeout=5)
    return r.returncode == 0, r.stderr.strip()

def get_main_script_block(content):
    """Find the largest non-GA, non-JSON-LD script block"""
    blocks = list(re.finditer(r'(<script[^>]*>)(.*?)(</script>)', content, re.DOTALL))
    best = None
    best_size = 0
    for m in blocks:
        tag = m.group(1)
        body = m.group(2).strip()
        if 'src=' in tag or 'application/ld+json' in tag: continue
        if body.startswith('{') and ('@context' in body or '"@type"' in body): continue
        if 'window.dataLayer' in body or 'gtag' in body: continue
        if len(body) > best_size:
            best_size = len(body)
            best = m
    return best

def fix_tool(tool):
    path = f'{tool}/index.html'
    if not os.path.exists(path):
        return 'NO_FILE'
    
    with open(path) as f: content = f.read()
    js = extract_main_js(content)
    ok, err = check_syntax(js)
    if ok:
        return 'OK'
    
    m = get_main_script_block(content)
    if m is None:
        return 'NO_MAIN_BLOCK'
    
    orig_js = m.group(2)
    fixed_js = orig_js
    changed = False
    
    # Fix 1: innerHTML='...<tag>...' → innerHTML=`...<tag>...`
    if "innerHTML='" in fixed_js:
        new_js = re.sub(
            r"(\w+\.innerHTML\s*=\s*)'([^']*<(?:div|html|head|body|style|span|table|tr|td|h[1-6]|p\b|br\b|a\s|img|input|form|select|option|svg|canvas|iframe|ul|ol|li|pre|code|strong|em|b\b|i\b)[^']*)'",
            r"\1`\2`",
            fixed_js
        )
        if new_js != fixed_js:
            fixed_js = new_js
            changed = True
    
    # Fix 2: document.write('...<html...') → document.write(`...<html...`)
    new_js = re.sub(r"(win\.)?document\.write\('([^']*<html[^']*)'\)", r"document.write(`\2`)", fixed_js)
    if new_js != fixed_js:
        fixed_js = new_js
        changed = True
    
    # Fix 3: textContent = '...<tag>...' → textContent = `...<tag>...`
    new_js = re.sub(
        r"(\.textContent\s*=\s*)'([^']*<(?:head|meta|link|title|style)[^']*)'",
        r"\1`\2`",
        fixed_js
    )
    if new_js != fixed_js:
        fixed_js = new_js
        changed = True
    
    # Fix 4: Duplicate let/const/var declarations
    lines = fixed_js.split('\n')
    seen = set()
    new_lines = []
    for line in lines:
        m2 = re.match(r'(\s*)(let|const|var)\s+(\w+)', line)
        if m2:
            indent, kw, name = m2.group(1), m2.group(2), m2.group(3)
            if name in seen:
                line = indent + name + line[m2.end():]
                changed = True
            else:
                seen.add(name)
        new_lines.append(line)
    fixed_js = '\n'.join(new_lines)
    
    # Fix 5: })(); → }());
    if '})();' in fixed_js and '}());' not in fixed_js:
        fixed_js = fixed_js.replace('})();', '}());')
        changed = True
    
    # Fix 6: catch()=> → catch(e)=>
    new_js = re.sub(r'catch\s*\(\s*\)\s*=>', 'catch(e)=>', fixed_js)
    if new_js != fixed_js:
        fixed_js = new_js
        changed = True
    
    # Fix 7: '3 || '3' → '3' || '3'
    if "'3 || '3'" in fixed_js:
        fixed_js = fixed_js.replace("'3 || '3'", "'3' || '3'")
        changed = True
    
    # Fix 8: ':''; → '':'';  (Python empty string in JS)
    if "':'';" in fixed_js:
        fixed_js = fixed_js.replace("':'';", "'':'';")
        changed = True
    
    if not changed:
        return f'NO_FIX: {err[:80]}'
    
    # Apply fix
    new_content = content[:m.start(2)] + fixed_js + content[m.end(2):]
    with open(path, 'w') as f: f.write(new_content)
    
    # Verify
    with open(path) as f: verify_content = f.read()
    verify_js = extract_main_js(verify_content)
    ok2, err2 = check_syntax(verify_js)
    if ok2:
        return 'FIXED'
    else:
        # Revert
        with open(path, 'w') as f: f.write(content)
        return f'REVERTED: {err2[:80]}'

BROKEN = [
    'ai-fine-tuning-cost-calculator','dns-record-comparator','dockerfile-formatter',
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
    'vite-config-generator','word-search-generator','workout-generator','yaml-to-json'
]

results = {'FIXED':[], 'OK':[], 'NO_FIX':[], 'REVERTED':[], 'ERROR':[]}
for tool in BROKEN:
    try:
        r = fix_tool(tool)
        if r == 'FIXED': results['FIXED'].append(tool)
        elif r == 'OK': results['OK'].append(tool)
        elif r.startswith('REVERTED'): results['REVERTED'].append((tool, r))
        elif r.startswith('NO_FIX'): results['NO_FIX'].append((tool, r))
        else: results['ERROR'].append((tool, r))
    except Exception as e:
        results['ERROR'].append((tool, str(e)))

print(f"\n=== RESULTS ===")
print(f"FIXED: {len(results['FIXED'])}")
for t in results['FIXED']: print(f'  ✅ {t}')
print(f"\nOK: {len(results['OK'])}")
for t in results['OK']: print(f'  ⏭️ {t}')
print(f"\nREVERTED: {len(results['REVERTED'])}")
for t, why in results['REVERTED']: print(f'  ❌ {t}')
print(f"\nNO_FIX: {len(results['NO_FIX'])}")
for t, why in results['NO_FIX']: print(f'  ⚠️ {t}')
print(f"\nERROR: {len(results['ERROR'])}")
for t, why in results['ERROR']: print(f'  💥 {t}: {why}')