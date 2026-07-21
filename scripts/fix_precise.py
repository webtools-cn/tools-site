#!/usr/bin/env python3
"""精确逐个修复 - 对每个工具打开文件直接改"""
import subprocess, re, os

def check_js(path):
    with open(path) as f: c = f.read()
    scripts = re.findall(r'<script>(.*?)</script>', c, re.DOTALL)
    js = '\n'.join(s.strip() for s in scripts if s.strip() and not (s.strip().startswith('{') and ('@context' in s or '"@type"' in s)))
    if not js: return True, ''
    r = subprocess.run(['node','-c','-'], input=js, capture_output=True, text=True, timeout=5)
    return r.returncode == 0, r.stderr.strip()

def fix_by_replace(tool, replacements):
    """对文件做精确替换，每项(old_str, new_str)"""
    path = f'{tool}/index.html'
    if not os.path.exists(path): return 'NO_FILE'
    ok, _ = check_js(path)
    if ok: return 'ALREADY_OK'
    
    with open(path) as f: orig = f.read()
    content = orig
    for old, new in replacements:
        content = content.replace(old, new)
    
    if content == orig: return 'NO_MATCH'
    
    with open(path, 'w') as f: f.write(content)
    ok2, err2 = check_js(path)
    if ok2: return 'FIXED'
    # Revert
    with open(path, 'w') as f: f.write(orig)
    return f'REVERTED: {err2[:80]}'

results = {}

# === Group 1: })(); → }()); ===
for tool in ['sitemap-validator','html-wysiwyg-editor','markdown-previewer','text-to-braille']:
    r = fix_by_replace(tool, [('})();', '}());')])
    results[tool] = r

# === Group 2: convert();})(); → convert();}()); ===
for tool in ['text-to-braille']:
    r = fix_by_replace(tool, [('convert();})();', 'convert();}());')])
    if r == 'FIXED': results[tool] = r

# === Group 3: Duplicate let declarations ===
for tool, var_name in [('line-chart-maker','chartColors'),('pie-chart-maker','chartColors')]:
    path = f'{tool}/index.html'
    if not os.path.exists(path): continue
    with open(path) as f: content = f.read()
    # Find second occurrence of "let chartColors" and remove "let "
    pattern = f'let {var_name} ='
    first = content.find(pattern)
    second = content.find(pattern, first + 1)
    if second > 0:
        new_content = content[:second] + f'{var_name} =' + content[second + len(pattern):]
        with open(path, 'w') as f: f.write(new_content)
        ok, _ = check_js(path)
        if ok:
            results[tool] = 'FIXED'
        else:
            with open(path, 'w') as f: f.write(content)
            results[tool] = 'REVERTED'
    else:
        results[tool] = 'NO_SECOND_OCCURRENCE'

# === Group 4: '3 || '3' → '3' || '3' ===
for tool in ['regex-character-class-generator']:
    r = fix_by_replace(tool, [("'3 || '3'", "'3' || '3'")])
    results[tool] = r

# === Group 5: ':''; → '':''; ===
for tool in ['sql-migration-generator','sql-to-kysely']:
    r = fix_by_replace(tool, [("':'';", "'':'';"), (",'':'';", ",'':'';")])
    results[tool] = r

# === Group 6: sql-to-prisma: 'postgresql'?'postgresql'==='sqlite' → fix ===
# The error: dialect==='postgresql'?'postgresql'==='sqlite' 
# Should be: dialect==='postgresql'?'postgresql':dialect==='sqlite'?'sqlite'
for tool in ['sql-to-prisma']:
    path = f'{tool}/index.html'
    if not os.path.exists(path): continue
    with open(path) as f: content = f.read()
    # Find the broken ternary chain
    old_pat = "dialect==='postgresql'?'postgresql'==='sqlite'?'sqlite':'mysql'"
    new_pat = "dialect==='postgresql'?'postgresql':dialect==='sqlite'?'sqlite':'mysql'"
    if old_pat in content:
        new_content = content.replace(old_pat, new_pat)
        with open(path, 'w') as f: f.write(new_content)
        ok, _ = check_js(path)
        if ok:
            results[tool] = 'FIXED'
        else:
            with open(path, 'w') as f: f.write(content)
            results[tool] = 'REVERTED'
    else:
        results[tool] = 'NO_MATCH'

# === Group 7: terms-generator & privacy-policy-generator: unclosed strings ===
# These have text+='xxx\n pattern where \n is actual newline in source, not escape
# Need to convert to template literals
for tool in ['terms-generator','privacy-policy-generator']:
    path = f'{tool}/index.html'
    if not os.path.exists(path): continue
    with open(path) as f: orig = f.read()
    content = orig
    
    # Fix pattern: text='xxx\n' where the next line starts with ' or text
    # Convert: var text='xxx\n';text+='yyy\n';text+='zzz' → var text=`xxx\nyyy\nzzz`;
    # But this is very specific to each tool. Let's try a different approach:
    # Find the script block containing text generation, and rewrite it
    
    # Pattern: text='...  followed by multiple text+='... lines  
    # All with unclosed single-quoted strings
    # Convert to one big template literal
    
    # Find: var text='...\n';text+='...\n';...text+='...';
    # Replace with: var text = `...\n...\n...`;
    
    # Match the full text building pattern
    def rebuild_text_var(script_content):
        # Find: var text='FIRST'; or text='FIRST'; 
        # Followed by: text+='SECOND'; text+='THIRD'; ...
        # Convert all to one template literal
        lines = script_content.split('\n')
        result = []
        collecting = False
        text_parts = []
        text_var_name = None
        start_line = -1
        end_line = -1
        
        for i, line in enumerate(lines):
            stripped = line.strip()
            if not collecting:
                m = re.match(r"(?:var\s+)?(text)\s*=\s*'([^']*)';?", stripped)
                if m:
                    text_var_name = m.group(1)
                    text_parts = [m.group(2)]
                    collecting = True
                    start_line = i
                    continue
            
            if collecting:
                m = re.match(rf"{text_var_name}\s*\+=\s*'([^']*)';?", stripped)
                if m:
                    text_parts.append(m.group(1))
                    end_line = i
                    continue
                else:
                    # End of text building
                    # Build the replacement
                    full_text = '\\n'.join(text_parts)
                    replacement = f'var {text_var_name} = `{full_text}`;'
                    result.append(replacement)
                    result.append(stripped)  # current non-matching line
                    collecting = False
                    continue
            
            result.append(line)
        
        # Handle case where collecting goes to end
        if collecting:
            full_text = '\\n'.join(text_parts)
            replacement = f'var {text_var_name} = `{full_text}`;'
            # Replace from start_line to end_line
            before = lines[:start_line]
            after = lines[end_line+1:]
            return '\n'.join(before + [replacement] + after)
        
        return '\n'.join(result)
    
    # Apply to script blocks
    def fix_text_script(m):
        sc = m.group(1)
        if sc.strip().startswith('{') and ('@context' in sc or '"@type"' in sc):
            return m.group(0)
        fixed = rebuild_text_var(sc)
        return '<script>' + fixed + '</script>'
    
    new_content = re.sub(r'<script>(.*?)</script>', fix_text_script, content, flags=re.DOTALL)
    
    if new_content != orig:
        with open(path, 'w') as f: f.write(new_content)
        ok, err = check_js(path)
        if ok:
            results[tool] = 'FIXED'
        else:
            with open(path, 'w') as f: f.write(orig)
            results[tool] = f'REVERTED: {err[:80]}'
    else:
        results[tool] = 'NO_MATCH'

# === Group 8: markdown-link-checker - statusNames with emoji in single quotes ===
# Already fixed? Let me check by running syntax check
for tool in ['markdown-link-checker']:
    path = f'{tool}/index.html'
    with open(path) as f: content = f.read()
    # The error is about unclosed string - check if emoji inside single quotes breaks it
    # Try: const statusNames={ok:'...' ... → template literal or escape
    # Actually this might just need proper quoting
    ok, err = check_js(path)
    if ok:
        results[tool] = 'ALREADY_OK'
    else:
        results[tool] = f'SKIP: {err[:80]}'

# Print
print("=== RESULTS ===")
fixed_count = sum(1 for v in results.values() if v == 'FIXED')
ok_count = sum(1 for v in results.values() if v == 'ALREADY_OK')
reverted = [(k,v) for k,v in results.items() if v.startswith('REVERTED')]
other = [(k,v) for k,v in results.items() if v not in ('FIXED','ALREADY_OK') and not v.startswith('REVERTED')]

print(f"\nFIXED ({fixed_count}):")
for k,v in results.items():
    if v == 'FIXED': print(f'  ✅ {k}')
print(f"\nALREADY OK ({ok_count}):")
for k,v in results.items():
    if v == 'ALREADY_OK': print(f'  ⏭️ {k}')
print(f"\nREVERTED ({len(reverted)}):")
for k,v in reverted: print(f'  ❌ {k}: {v}')
print(f"\nOTHER ({len(other)}):")
for k,v in other: print(f'  ⚠️ {k}: {v}')