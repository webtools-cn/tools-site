#!/usr/bin/env python3
"""Fix JS syntax errors in tool HTML files - optimized version.
Strategy: 
1. Use fast counting to detect errors per-block
2. Fix each block independently (never merge blocks)
3. Validate with node --check only after fixing
4. Rollback if validation fails
"""
import re, os, subprocess, sys, tempfile
from glob import glob as find_files

def validate_js(js_code):
    """Validate JS syntax using node --check with temp file."""
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
            f.write(js_code)
            tmpfile = f.name
        result = subprocess.run(
            ['node', '--check', tmpfile],
            capture_output=True, timeout=10
        )
        os.unlink(tmpfile)
        return result.returncode == 0, result.stderr.decode('utf-8', errors='ignore')
    except Exception as e:
        try: os.unlink(tmpfile)
        except: pass
        return False, str(e)

def parse_node_error(err_text):
    """Parse node error to get line, col, and message."""
    lines = err_text.strip().split('\n')
    line_num = 0
    col_num = 0
    error_msg = ''
    
    if lines:
        match = re.match(r'.*?:(\d+):(\d+)', lines[0])
        if match:
            line_num = int(match.group(1))
            col_num = int(match.group(2))
    
    for line in lines:
        if 'SyntaxError' in line:
            error_msg = line.strip()
            break
    
    return line_num, col_num, error_msg

def fix_block(js):
    """Try to fix a single JS block. Returns (fixed_js, success, message)."""
    # Check if already valid
    ok, err = validate_js(js)
    if ok:
        return js, True, "Already valid"
    
    original = js
    
    for attempt in range(15):
        err_info = validate_js(js)
        if err_info[0]:
            return js, True, f"Fixed after {attempt+1} attempts"
        
        line_num, col_num, error_msg = parse_node_error(err_info[1])
        
        if 'Unexpected end of input' in error_msg:
            # Missing closing brackets
            paren_diff = js.count('(') - js.count(')')
            brace_diff = js.count('{') - js.count('}')
            
            additions = ''
            if brace_diff > 0:
                additions += '}' * brace_diff
            if paren_diff > 0:
                additions += ')' * paren_diff
            
            if additions:
                js = js.rstrip() + '\n' + additions + '\n'
                continue
            else:
                # No obvious missing brackets - might be a string literal issue
                break
        
        elif 'missing )' in error_msg:
            # Missing closing paren - add it
            lines_list = js.split('\n')
            if 1 <= line_num <= len(lines_list):
                line = lines_list[line_num - 1]
                # Find the last ; on the line and add ) before it
                last_semi = line.rfind(';')
                if last_semi > 0:
                    before_semi = line[:last_semi]
                    open_count = before_semi.count('(') - before_semi.count(')')
                    if open_count > 0:
                        new_line = line[:last_semi] + ')' * open_count + line[last_semi:]
                        lines_list[line_num - 1] = new_line
                        js = '\n'.join(lines_list)
                        continue
            break
        
        elif 'Unexpected token' in error_msg:
            token_match = re.search(r"Unexpected token '(.+?)'", error_msg)
            if not token_match:
                token_match = re.search(r"Unexpected token (\S+)", error_msg)
            token = token_match.group(1) if token_match else ''
            
            lines_list = js.split('\n')
            if 1 <= line_num <= len(lines_list):
                line = lines_list[line_num - 1]
                
                if token == ')' and col_num > 0:
                    # Extra ) - remove it
                    idx = col_num - 1
                    if idx < len(line) and line[idx] == ')':
                        line = line[:idx] + line[idx+1:]
                        lines_list[line_num - 1] = line
                        js = '\n'.join(lines_list)
                        continue
                
                elif token == '}' and col_num > 0:
                    # Extra } - remove it
                    idx = col_num - 1
                    if idx < len(line) and line[idx] == '}':
                        line = line[:idx] + line[idx+1:]
                        lines_list[line_num - 1] = line
                        js = '\n'.join(lines_list)
                        continue
                
                elif token == ';':
                    # Often from )(; or }(; pattern - should be )(); or })();
                    if col_num > 0:
                        before = line[:col_num-1].rstrip()
                        if before.endswith(')(') or before.endswith('}('):
                            # Add missing ) before ;
                            line = line[:col_num-1] + ')' + line[col_num-1:]
                            lines_list[line_num - 1] = line
                            js = '\n'.join(lines_list)
                            continue
                        elif before.endswith(')') or before.endswith('}'):
                            # Misplaced ; - remove it
                            line = line[:col_num-1] + line[col_num:]
                            lines_list[line_num - 1] = line
                            js = '\n'.join(lines_list)
                            continue
                
                elif token == '<':
                    # Likely HTML tag leaked into JS - skip this block
                    break
            
            break
        
        elif 'Unexpected identifier' in error_msg:
            # Complex structural issue - skip
            break
        
        elif 'catch' in error_msg.lower():
            # Missing try block - complex, skip
            break
        
        else:
            break
    
    # Final validation
    ok, err = validate_js(js)
    if ok:
        return js, True, "Fixed"
    
    return original, False, f"Unfixable: {error_msg[:80]}"

def fix_file(filepath):
    """Fix a single HTML file's JS errors."""
    html = open(filepath, errors='ignore').read()
    
    # Find all script blocks
    script_pattern = re.compile(r'(<script>)(.*?)(</script>)', re.DOTALL)
    matches = list(script_pattern.finditer(html))
    
    # Identify JS blocks (not analytics/ld+json)
    js_blocks = []
    for m in matches:
        content = m.group(2).strip()
        if content and 'dataLayer' not in content[:50] and 'gtag' not in content[:30] and 'application/ld+json' not in content[:30]:
            # Quick check: does this block have balance issues?
            paren_diff = content.count('(') - content.count(')')
            brace_diff = content.count('{') - content.count('}')
            # Also check for )(; pattern
            has_broken_iife = bool(re.search(r'\}\(\;', content))
            if abs(paren_diff) > 0 or abs(brace_diff) > 0 or has_broken_iife:
                js_blocks.append({
                    'start': m.start(),
                    'end': m.end(),
                    'open_tag': m.group(1),
                    'content': content,
                    'close_tag': m.group(3),
                    'full_match': m.group(0)
                })
    
    if not js_blocks:
        return False, "No fixable blocks"
    
    # Fix each block
    new_html = html
    any_fixed = False
    messages = []
    
    for block in reversed(js_blocks):
        fixed_js, success, msg = fix_block(block['content'])
        if success and fixed_js != block['content']:
            new_full = f"{block['open_tag']}\n{fixed_js}\n{block['close_tag']}"
            before = new_html[:block['start']]
            after = new_html[block['end']:]
            new_html = before + new_full + after
            any_fixed = True
            messages.append(msg)
    
    if any_fixed:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_html)
        return True, "; ".join(messages)
    
    return False, "No changes made"

def main():
    os.chdir('/home/chison/tools-site')
    
    # Find files with JS errors using fast counting
    error_files = []
    for f in sorted(find_files('*/index.html')) + sorted(find_files('en/*/index.html')):
        html = open(f, errors='ignore').read()
        scripts = re.findall(r'<script>(.*?)</script>', html, re.DOTALL)
        js_parts = [s.strip() for s in scripts if s.strip() and 'dataLayer' not in s[:50] and 'gtag' not in s[:30] and 'application/ld+json' not in s[:30]]
        if not js_parts: continue
        
        has_error = False
        for part in js_parts:
            paren_diff = part.count('(') - part.count(')')
            brace_diff = part.count('{') - part.count('}')
            has_broken_iife = bool(re.search(r'\}\(\;', part))
            if abs(paren_diff) > 0 or abs(brace_diff) > 0 or has_broken_iife:
                has_error = True
                break
        
        if has_error:
            error_files.append(f)
    
    print(f"Found {len(error_files)} files with potentially fixable JS blocks")
    
    fixed = 0
    failed = 0
    failed_files = []
    
    for filepath in error_files:
        success, msg = fix_file(filepath)
        if success:
            fixed += 1
            print(f"✓ {filepath}")
        else:
            failed += 1
            failed_files.append(filepath)
            print(f"✗ {filepath}")
    
    print(f"\n=== Summary ===")
    print(f"Fixed: {fixed}")
    print(f"Failed: {failed}")

if __name__ == '__main__':
    main()
