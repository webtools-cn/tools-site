#!/usr/bin/env python3
"""智能JS自动修复 - 针对常见生成器错误模式"""
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

def get_error_info(err):
    """提取错误行号和类型"""
    line_match = re.search(r'\[stdin\]:(\d+)', err)
    line_no = int(line_match.group(1)) if line_match else 0
    if 'Invalid or unexpected token' in err:
        return line_no, 'invalid_token'
    elif "Unexpected token ')'" in err:
        return line_no, 'extra_paren'
    elif 'missing ) after argument list' in err:
        return line_no, 'missing_paren'
    elif 'Unexpected string' in err:
        return line_no, 'unexpected_string'
    elif "Unexpected token '<'" in err:
        return line_no, 'html_in_js'
    elif 'Invalid regular expression' in err:
        return line_no, 'bad_regex'
    elif 'Unexpected end of input' in err:
        return line_no, 'unclosed'
    elif "Unexpected token '{'" in err:
        return line_no, 'unexpected_brace'
    elif "Unexpected token ';'" in err:
        return line_no, 'unexpected_semi'
    elif "Unexpected identifier" in err:
        return line_no, 'unexpected_ident'
    elif "Unexpected number" in err:
        return line_no, 'unexpected_number'
    elif "Unexpected token 'if'" in err or "Unexpected token 'catch'" in err:
        return line_no, 'missing_brace'
    else:
        return line_no, 'other'

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
    
    line_no, err_type = get_error_info(err)
    new_content = content
    
    # === Fix strategies ===
    
    # Strategy 1: Fix catch{e=>{...}} → catch(e){...}
    new_content = re.sub(r'catch\s*\{\s*e\s*=>\s*\{', 'catch(e){', new_content)
    
    # Strategy 2: Fix unclosed strings with HTML - replace single-quoted strings containing HTML with backtick
    # Pattern: html: '...<tag>...' or similar
    if err_type in ('invalid_token', 'html_in_js', 'unexpected_string'):
        # Find single-quoted strings that span multiple lines and contain HTML
        # Replace '...' with `...` for long strings
        def replace_long_single_quotes(m):
            s = m.group(0)
            if len(s) > 100 and '<' in s and '>' in s:
                # Replace with backtick
                inner = s[1:-1]  # remove surrounding quotes
                # Unescape any \' inside
                inner = inner.replace("\\'", "'")
                return '`' + inner + '`'
            return s
        
        # This is risky for short strings, only apply to clearly broken ones
        # Instead, find the specific line and fix it
        pass
    
    # Strategy 3: Fix missing closing braces/parens at end of script blocks
    for script_match in list(re.finditer(r'<script>(.*?)</script>', new_content, re.DOTALL)):
        script_content = script_match.group(1)
        if script_content.strip().startswith('{') and ('@context' in script_content or '"@type"' in script_content):
            continue
        
        opens_b = script_content.count('{')
        closes_b = script_content.count('}')
        diff_b = opens_b - closes_b
        
        opens_p = script_content.count('(')
        closes_p = script_content.count(')')
        diff_p = opens_p - closes_p
        
        # Add missing braces/parens
        if diff_b > 0 and diff_b <= 5:
            new_content = new_content.replace(
                script_content + '</script>',
                script_content + ('}' * diff_b) + '\n</script>',
                1
            )
        if diff_p > 0 and diff_p <= 5:
            new_content = new_content.replace(
                script_content + '</script>',
                script_content + (')' * diff_p) + '\n</script>',
                1
            )
    
    # Strategy 4: Fix duplicate showToast declarations
    # Keep only the last occurrence
    showToast_pattern = r'function\s+showToast\s*\([^)]*\)\s*\{[^}]*\}'
    matches = list(re.finditer(showToast_pattern, new_content))
    if len(matches) > 1:
        # Keep last, remove others
        for m in matches[:-1]:
            new_content = new_content[:m.start()] + new_content[m.end():]
    
    # Strategy 5: Fix duplicate copyText declarations
    copyText_pattern = r'function\s+copyText\s*\([^)]*\)\s*\{[^}]*\}'
    matches = list(re.finditer(copyText_pattern, new_content))
    if len(matches) > 1:
        for m in matches[:-1]:
            new_content = new_content[:m.start()] + new_content[m.end():]
    
    # Write and verify
    if new_content != content:
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
            return False, f'still_broken: {err_type}'
    
    return False, f'unfixable: {err_type}'

if __name__ == '__main__':
    SKIP = {'_gen','__pycache__','en','libs','js','css','scripts','tools',
            '.git','data','about','blog','privacy-policy','terms-of-service','category',
            'calc','design','dev','fun','health','image','math','media','network',
            'office','pdf','security','seo','text','utility'}
    
    fixed = []
    still_broken = []
    unfixable = []
    
    for d in sorted(os.listdir('.')):
        if not os.path.isdir(d) or d in SKIP or d.startswith('.'): continue
        f = f'{d}/index.html'
        if not os.path.exists(f): continue
        
        result, info = fix_tool(d)
        if result is None:
            continue
        if result:
            fixed.append(d)
        elif 'still_broken' in info:
            still_broken.append(d)
        else:
            unfixable.append((d, info))
    
    print(f"Auto-fixed: {len(fixed)}")
    for t in fixed:
        print(f"  ✅ {t}")
    print(f"\nStill broken (auto-fix didn't help): {len(still_broken)}")
    for t in still_broken:
        print(f"  ❌ {t}")
    print(f"\nUnfixable: {len(unfixable)}")
    for t, e in unfixable[:20]:
        print(f"  ⚠️ {t}: {e}")
