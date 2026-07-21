#!/usr/bin/env python3
"""自动修复工具JS常见语法错误"""
import subprocess, re, sys, os

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
    return '\n'.join(js_parts) if js_parts else ''

def check_js(js):
    r = subprocess.run(['node', '-c', '-'], input=js, capture_output=True, text=True, timeout=5)
    return r.returncode == 0, r.stderr.strip()

def fix_tool(tool_dir):
    html_path = f'{tool_dir}/index.html'
    if not os.path.exists(html_path):
        return None
    
    with open(html_path) as f:
        content = f.read()
    
    js = extract_js(html_path)
    if not js:
        return None
    
    ok, err = check_js(js)
    if ok:
        return 'ok'
    
    original_err = err
    
    # Strategy 1: Fix catch{e=>{...}} → catch(e){...}
    new_content = content
    new_content = re.sub(r'catch\s*\{\s*e\s*=>\s*\{', 'catch(e){', new_content)
    
    # Strategy 2: Fix missing closing brace at end of script
    # Count { and } in each script block
    for script_match in list(re.finditer(r'<script>(.*?)</script>', new_content, re.DOTALL)):
        script_content = script_match.group(1)
        if script_content.strip().startswith('{') and ('@context' in script_content or '"@type"' in script_content):
            continue
        opens = script_content.count('{')
        closes = script_content.count('}')
        diff = opens - closes
        if diff > 0 and diff <= 3:
            # Add missing } before </script>
            new_content = new_content.replace(
                script_content + '</script>',
                script_content + ('}' * diff) + '\n</script>'
            )
        elif diff < 0 and diff >= -3:
            # Remove extra } at end
            # Find last few } and remove |diff| of them
            last_script_end = script_content.rstrip()
            for _ in range(abs(diff)):
                if last_script_end.endswith('}'):
                    last_script_end = last_script_end[:-1]
            new_content = new_content.replace(
                script_content,
                last_script_end,
                1  # only replace first occurrence
            )
    
    # Strategy 3: Fix missing ) after argument list
    # Often caused by: function call with missing closing paren
    for script_match in list(re.finditer(r'<script>(.*?)</script>', new_content, re.DOTALL)):
        script_content = script_match.group(1)
        if script_content.strip().startswith('{') and ('@context' in script_content or '"@type"' in script_content):
            continue
        opens = script_content.count('(')
        closes = script_content.count(')')
        diff = opens - closes
        if diff > 0 and diff <= 3:
            # Add missing ) before </script>
            new_content = new_content.replace(
                script_content + '</script>',
                script_content + (')' * diff) + '\n</script>'
            )
    
    # Write and verify
    if new_content != content:
        with open(html_path, 'w') as f:
            f.write(new_content)
        new_js = extract_js(html_path)
        ok2, err2 = check_js(new_js)
        if ok2:
            return 'fixed'
        else:
            # Revert
            with open(html_path, 'w') as f:
                f.write(content)
            return f'still_broken: {err2.split(chr(10))[0][:80]}'
    
    return f'unfixable: {original_err.split(chr(10))[0][:80]}'

if __name__ == '__main__':
    SKIP = {'_gen','__pycache__','en','libs','js','css','scripts','tools',
            '.git','data','about','blog','privacy-policy','terms-of-service','category',
            'calc','design','dev','fun','health','image','math','media','network',
            'office','pdf','security','seo','text','utility'}
    
    results = {'fixed': [], 'ok': [], 'still_broken': [], 'unfixable': [], 'skipped': []}
    
    for d in sorted(os.listdir('.')):
        if not os.path.isdir(d) or d in SKIP or d.startswith('.'): continue
        f = f'{d}/index.html'
        if not os.path.exists(f): continue
        result = fix_tool(d)
        if result is None:
            continue
        if result == 'ok':
            continue
        if result == 'fixed':
            results['fixed'].append(d)
        elif result.startswith('still_broken'):
            results['still_broken'].append((d, result))
        elif result.startswith('unfixable'):
            results['unfixable'].append((d, result))
    
    print(f"Fixed: {len(results['fixed'])}")
    for t in results['fixed']:
        print(f"  ✅ {t}")
    print(f"\nStill broken: {len(results['still_broken'])}")
    for t, e in results['still_broken']:
        print(f"  ❌ {t}: {e}")
    print(f"\nUnfixable (needs manual): {len(results['unfixable'])}")
    for t, e in results['unfixable'][:20]:
        print(f"  ⚠️ {t}: {e}")
