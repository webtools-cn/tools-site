#!/usr/bin/env python3
"""精准逐个修复48个broken工具 - 打开文件直接定位问题行"""
import subprocess, re, os

def check_js_file(html_path):
    with open(html_path) as f: c = f.read()
    scripts = re.findall(r'<script>(.*?)</script>', c, re.DOTALL)
    js = '\n'.join(s.strip() for s in scripts if s.strip() and not (s.strip().startswith('{') and ('@context' in s or '"@type"' in s)))
    if not js: return True, ''
    r = subprocess.run(['node','-c','-'], input=js, capture_output=True, text=True, timeout=5)
    return r.returncode == 0, r.stderr.strip()

def read_script_content(html_path):
    with open(html_path) as f: return f.read()

def fix_tool(tool):
    path = f'{tool}/index.html'
    if not os.path.exists(path): return 'NO_FILE'
    
    ok, err = check_js_file(path)
    if ok: return 'OK'
    
    content = read_script_content(path)
    orig = content
    
    # === FIX 1: unclosed single-quoted strings (16 tools) ===
    # Pattern: textContent = '... \n or text+='...\n without closing quote
    # Replace with backtick template literals where the string spans content
    content = re.sub(
        r"textContent\s*=\s*'([^']*?)$",
        r"textContent = `\1`",
        content, flags=re.MULTILINE
    )
    content = re.sub(
        r"innerHTML\s*=\s*'([^']*?)$",
        r"innerHTML = `\1`",
        content, flags=re.MULTILINE
    )
    
    # Fix: text+='xxx\n → text+=`xxx\n`
    content = re.sub(
        r"(text\s*\+=\s*)'([^'\n]*?)\n",
        r"\1`\2\n",
        content
    )
    
    # Fix: text='xxx\n → text=`xxx\n`  
    content = re.sub(
        r"(text\s*=\s*)'([^'\n]*?)\n",
        r"\1`\2\n`",
        content
    )
    
    # Fix: document.write('... → document.write(`...`
    content = re.sub(
        r"(win\.document\.write\()'([^']*?)\n",
        r"\1`\2\n",
        content
    )
    
    # Fix: html+='... → html+=`...`
    content = re.sub(
        r"(html\s*\+=\s*)'([^'\n]*?)\n",
        r"\1`\2\n",
        content
    )
    
    # Fix: innerHTML='... → innerHTML=`...`
    content = re.sub(
        r"(innerHTML\s*=\s*)'([^'\n]*?)\n",
        r"\1`\2\n",
        content
    )
    
    # === FIX 2: duplicate declarations ===
    # Fix: let chartColors = ... (second occurrence) → chartColors = ...
    dup_vars = {}
    def fix_dup_in_script(m):
        nonlocal dup_vars
        sc = m.group(1)
        if sc.strip().startswith('{') and ('@context' in sc or '"@type"' in sc):
            return m.group(0)
        lines = sc.split('\n')
        seen = set()
        new_lines = []
        for line in lines:
            m2 = re.match(r'(\s*)(?:let|const|var)\s+(\w+)', line)
            if m2 and m2.group(2) in seen:
                line = m2.group(1) + m2.group(2) + line[m2.end():]
            elif m2:
                seen.add(m2.group(2))
            new_lines.append(line)
        return '<script>' + '\n'.join(new_lines) + '</script>'
    
    content = re.sub(r'<script>(.*?)</script>', fix_dup_in_script, content, flags=re.DOTALL)
    
    # === FIX 3: })() → }()) ===
    content = content.replace('})();', '}());')
    
    # === FIX 4: convert();})(); → convert();}()); ===
    content = content.replace('convert();})();', 'convert();}());')
    
    # === FIX 5: regex-character-class: '3 || '3' → '3' || '3' ===
    content = content.replace("'3 || '3'", "'3' || '3'")
    
    # === FIX 6: text-diff-checker: style=""+SS+"" → style="'+SS+'" ===
    content = re.sub(r'style=""\+(\w+)\+""', r"style=\"'+\1+'\"", content)
    
    # === FIX 7: sql-migration: ':'' → '':'' ===
    content = content.replace("':'';", "'':'';")
    
    # === FIX 8: unicode escape \u with >4 digits ===
    content = re.sub(r'\\u([0-9a-fA-F]{5,})', lambda m: '\\u' + m.group(1)[:4], content)
    
    if content != orig:
        with open(path, 'w') as f: f.write(content)
        ok2, err2 = check_js_file(path)
        if ok2:
            return 'FIXED'
        else:
            with open(path, 'w') as f: f.write(orig)
            return f'REVERTED: {err2[:80]}'
    return f'NO_CHANGE: {err[:80]}'

BROKEN = [
    'ai-fine-tuning-cost-calculator','dns-record-comparator','dockerfile-formatter',
    'dockerfile-linter','fancy-text-generator','flexbox-layout-generator',
    'handwriting-generator','html-entity-converter','html-meta-refresh-generator',
    'html-table-of-contents','html-table-to-json','html-tag-stripper',
    'html-wysiwyg-editor','http-cache-header-generator','line-chart-maker',
    'markdown-link-checker','markdown-previewer','markdown-to-pdf-converter',
    'maze-generator','md5-generator','meta-tag-generator','morse-code',
    'name-generator','pdf-to-html','pie-chart-maker','privacy-policy-generator',
    'properties-to-yaml','quiz-generator','receipt-generator',
    'regex-character-class-generator','regex-cheatsheet','shopping-list-generator',
    'sitemap-validator','sql-migration-generator','sql-to-csv','sql-to-kysely',
    'sql-to-prisma','svg-to-data-uri','terms-generator','text-diff-checker',
    'text-normalizer','text-palindrome-checker','text-to-braille','typing-test',
    'vite-config-generator','word-search-generator','workout-generator','yaml-to-json'
]

results = {'FIXED':[], 'OK':[], 'REVERTED':[], 'NO_CHANGE':[], 'NO_FILE':[]}
for tool in BROKEN:
    r = fix_tool(tool)
    if r == 'FIXED': results['FIXED'].append(tool)
    elif r == 'OK': results['OK'].append(tool)
    elif r.startswith('REVERTED'): results['REVERTED'].append((tool, r))
    elif r.startswith('NO_CHANGE'): results['NO_CHANGE'].append((tool, r))
    else: results['NO_FILE'].append(tool)

print('=== RESULTS ===')
print(f"FIXED: {len(results['FIXED'])}")
for t in results['FIXED']: print(f'  ✅ {t}')
print(f"\nAlready OK: {len(results['OK'])}")
print(f"\nREVERTED (fix broke something): {len(results['REVERTED'])}")
for t, why in results['REVERTED']: print(f'  ❌ {t}: {why}')
print(f"\nNO_CHANGE (pattern not matched): {len(results['NO_CHANGE'])}")
for t, why in results['NO_CHANGE'][:10]: print(f'  ⚠️ {t}: {why}')
if len(results['NO_CHANGE']) > 10: 
    extra = len(results['NO_CHANGE']) - 10
    print(f'  ... and {extra} more')