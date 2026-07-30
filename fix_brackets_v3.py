#!/usr/bin/env python3
"""
Pattern-aware JS bracket fixer.
Instead of blindly adding/removing brackets, this identifies common JS patterns
where brackets are missing/extra and fixes them contextually.

Common patterns:
1. func(args; → func(args);  (missing ) before ;)
2. .forEach(x => expr; → .forEach(x => expr);  (missing ) before ;)
3. .then(() => expr; → .then(() => expr);  (missing ) before ;)
4. setTimeout(() => {stmt}, 1000; → setTimeout(() => {stmt}, 1000);  (missing ) before ;)
5. if(cond{ → if(cond){  (missing ) before {)
6. function(} → function(){}  (missing ) and content)
7. Extra ); at end of IIFE
8. setTimeout((=>expr, 1000); → setTimeout(()=>expr, 1000);  (arrow function syntax error)
"""

import re
import os
import subprocess
import sys
import tempfile
import shutil

def extract_js_from_html(html):
    """Extract JS code from <script> tags."""
    results = []
    pattern = re.compile(r'<script>(.*?)</script>', re.DOTALL)
    for match in pattern.finditer(html):
        js = match.group(1)
        stripped = js.strip()
        if not stripped:
            continue
        if 'dataLayer' in stripped[:50] or 'gtag' in stripped[:30] or 'application/ld+json' in stripped[:30]:
            continue
        js_start = match.start() + len('<script>')
        js_end = match.end() - len('</script>')
        results.append((js_start, js_end, js))
    return results

def validate_js(js):
    """Validate JS with node --check."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
        f.write(js)
        temp_path = f.name
    
    try:
        result = subprocess.run(['node', '--check', temp_path], capture_output=True, text=True, timeout=10)
        return result.returncode == 0, result.stderr
    finally:
        os.unlink(temp_path)

def fix_common_patterns(js):
    """Fix common JS bracket error patterns."""
    original = js
    
    # Pattern: setTimeout/setInterval with arrow function missing closing paren
    # setTimeout(() => { ... }, 1000; → setTimeout(() => { ... }, 1000);
    # Also: setTimeout((=>expr, 1000); → setTimeout(()=>expr, 1000);
    
    # Pattern: (=>  should be ()=>
    js = re.sub(r'\(=>', '()=>', js)
    
    # Pattern: function call missing closing paren before semicolon
    # e.g., .forEach(x => expr; → .forEach(x => expr);
    # e.g., .then(() => expr; → .then(() => expr);
    # e.g., .map(x => expr; → .map(x => expr);
    # e.g., .filter(x => expr; → .filter(x => expr);
    
    # Fix: arrow callback missing ) before ;
    # Pattern: => something; where something doesn't contain ( but should end with );
    # This is tricky - we need to find where the arrow callback's enclosing function call ends
    
    # Pattern: .method(args; → .method(args);
    # Look for patterns where a function call's arguments end with ; but no )
    # We need to track parenthesis depth
    
    # Let's do a more sophisticated line-by-line fix
    lines = js.split('\n')
    new_lines = []
    
    for line in lines:
        new_line = fix_line(line)
        new_lines.append(new_line)
    
    js = '\n'.join(new_lines)
    
    # Additional pattern fixes
    # Pattern: if/while/for condition missing closing paren before {
    # e.g., if(cond{ → if(cond){
    js = re.sub(r'\b(if|while|for|switch)\s*\(([^{]*)\{', r'\1(\2){', js)
    
    # Pattern: catch without try (missing try{)
    # e.g., }catch(e){ → try{...}catch(e){ - this is complex, skip for now
    
    # Pattern: Extra ); at end of IIFE or script
    # Count and remove trailing extra );
    
    return js

def fix_line(line):
    """Fix bracket issues in a single line of JS."""
    # Skip lines that are just strings or comments
    stripped = line.strip()
    if stripped.startswith('//') or stripped.startswith('/*') or stripped.startswith('*'):
        return line
    
    # Pattern: function call ending with ; but missing )
    # Track paren depth and find where ) should be added
    result = fix_line_parens(line)
    
    return result

def fix_line_parens(line):
    """Fix parenthesis issues in a line."""
    # Find all ( and ) positions, ignoring strings and comments
    chars = list(line)
    in_string = False
    string_char = None
    paren_stack = []  # positions of unmatched (
    extra_close_parens = []  # positions of extra )
    
    i = 0
    while i < len(chars):
        ch = chars[i]
        
        # Handle string literals
        if not in_string and ch in ('"', "'", '`'):
            in_string = True
            string_char = ch
            i += 1
            continue
        
        if in_string:
            if ch == '\\':
                i += 2
                continue
            if ch == string_char:
                in_string = False
                string_char = None
            i += 1
            continue
        
        # Handle comments
        if ch == '/' and i+1 < len(chars):
            if chars[i+1] == '/':
                break  # Rest of line is comment
            # Skip regex for now
        
        if ch == '(':
            paren_stack.append(i)
        elif ch == ')':
            if paren_stack:
                paren_stack.pop()
            else:
                extra_close_parens.append(i)
        
        i += 1
    
    # If there are unmatched ( and the line ends with ; or {, we need to add )
    if paren_stack and not in_string:
        # Check if line ends with ; or {
        rstripped = line.rstrip()
        if rstripped.endswith(';'):
            # Add ) before the ;
            # But we need to figure out how many ) to add
            # Count how many ( are unmatched
            num_missing = len(paren_stack)
            # Add ) before the final ;
            line = rstripped[:-1] + ')' * num_missing + ';'
            # Preserve trailing whitespace
        elif rstripped.endswith('{'):
            # Add ) before the {
            num_missing = len(paren_stack)
            line = rstripped[:-1] + ')' * num_missing + '{'
        elif rstripped.endswith(','):
            # Might be in a function call with multiple args
            # e.g., setTimeout(() => { ... }, 1000,
            # Don't add ) here, it might be correct
            pass
    
    # Remove extra ) - but be very careful
    # Only remove if they're clearly extra (e.g., )); at end where only one ) is needed)
    # For now, don't remove extra ) in line-by-line mode - handle separately
    
    return line

def fix_js_smart(js):
    """
    Smart JS bracket fixer that uses multiple strategies.
    """
    # Strategy 1: Fix common patterns
    js = fix_common_patterns(js)
    
    # Strategy 2: Fix (=> to ()=>
    js = re.sub(r'\(=>', '()=>', js)
    
    # Strategy 3: Fix missing ) before ; on lines
    # Already done in fix_common_patterns via fix_line
    
    # Strategy 4: Fix specific patterns
    # .forEach/.map/.filter/.then/.catch arrow callback missing )
    # Pattern: .method(arrow_func; → .method(arrow_func);
    
    # Strategy 5: Fix IIFE issues
    # (function(){...})(); is correct
    # (function(){...})); has extra )
    # (function(){...}() has missing )
    
    return js

def fix_file_interactive(filepath):
    """
    Fix a file by reading it, applying fixes, and validating.
    If validation fails, try more specific fixes based on the error message.
    """
    print(f"\n{'='*60}")
    print(f"Processing: {filepath}")
    
    with open(filepath, 'r', errors='ignore') as f:
        html = f.read()
    
    js_blocks = extract_js_from_html(html)
    if not js_blocks:
        print("  No JS found")
        return False
    
    full_js = '\n'.join(js for _, _, js in js_blocks)
    paren_diff = full_js.count('(') - full_js.count(')')
    brace_diff = full_js.count('{') - full_js.count('}')
    
    if abs(paren_diff) <= 3 and abs(brace_diff) <= 2:
        # Still validate - might have other syntax errors
        valid, error = validate_js(full_js)
        if valid:
            print(f"  Already valid: paren={paren_diff} brace={brace_diff}")
            return False
        else:
            print(f"  Balanced but invalid: {error.strip()[:100]}")
    
    print(f"  Before: paren_diff={paren_diff} brace_diff={brace_diff}")
    
    # Apply fixes to each script block
    modified_html = html
    offset = 0
    
    for js_start, js_end, js_content in js_blocks:
        fixed_js = fix_js_smart(js_content)
        
        if fixed_js != js_content:
            actual_start = js_start + offset
            actual_end = js_end + offset
            modified_html = modified_html[:actual_start] + fixed_js + modified_html[actual_end:]
            offset += len(fixed_js) - len(js_content)
    
    # Validate
    new_js_blocks = extract_js_from_html(modified_html)
    new_full_js = '\n'.join(js for _, _, js in new_js_blocks)
    new_paren_diff = new_full_js.count('(') - new_full_js.count(')')
    new_brace_diff = new_full_js.count('{') - new_full_js.count('}')
    print(f"  After pattern fix: paren_diff={new_paren_diff} brace_diff={new_brace_diff}")
    
    valid, error = validate_js(new_full_js)
    if valid:
        print(f"  ✅ node --check passed")
        with open(filepath, 'w') as f:
            f.write(modified_html)
        return True
    
    print(f"  ❌ Still invalid: {error.strip()[:200]}")
    
    # Try iterative targeted fixes based on error messages
    max_retries = 20
    for retry in range(max_retries):
        error_line = None
        error_type = None
        
        # Parse error message
        err_match = re.search(r':(\d+)\n(.+?)(?:\n|$)', error)
        if err_match:
            error_line = int(err_match.group(1))
            error_msg = err_match.group(2).strip()
        
        if not error_line:
            break
        
        # Get the problematic line
        js_lines = new_full_js.split('\n')
        if error_line > len(js_lines):
            break
        
        problem_line = js_lines[error_line - 1]
        print(f"  Retry {retry+1}: Line {error_line}: {problem_line[:80]}")
        print(f"  Error: {error_msg[:100]}")
        
        # Apply targeted fix based on error type
        fixed = False
        
        if 'missing )' in error_msg:
            # Find where ) should be added
            # Look at the line and find unmatched (
            fixed_js_content = add_missing_close_paren_at_line(new_full_js, error_line)
            if fixed_js_content != new_full_js:
                new_full_js = fixed_js_content
                fixed = True
        
        elif 'Unexpected token' in error_msg:
            # Various causes
            if "Unexpected token ')'" in error_msg:
                # Extra ) - remove it
                fixed_js_content = remove_extra_close_paren_at_line(new_full_js, error_line)
                if fixed_js_content != new_full_js:
                    new_full_js = fixed_js_content
                    fixed = True
            elif "Unexpected token '}'" in error_msg:
                # Extra } or missing {
                fixed_js_content = remove_extra_close_brace_at_line(new_full_js, error_line)
                if fixed_js_content != new_full_js:
                    new_full_js = fixed_js_content
                    fixed = True
            elif "Unexpected token 'catch'" in error_msg:
                # Missing try block
                fixed_js_content = fix_missing_try(new_full_js, error_line)
                if fixed_js_content != new_full_js:
                    new_full_js = fixed_js_content
                    fixed = True
            elif "Unexpected token 'else'" in error_msg:
                # Missing } before else
                fixed_js_content = fix_else_without_brace(new_full_js, error_line)
                if fixed_js_content != new_full_js:
                    new_full_js = fixed_js_content
                    fixed = True
            elif "Unexpected token ';'" in error_msg:
                # Could be many things - often missing ) or (
                fixed_js_content = fix_unexpected_semicolon(new_full_js, error_line)
                if fixed_js_content != new_full_js:
                    new_full_js = fixed_js_content
                    fixed = True
            elif "Unexpected token '=>'" in error_msg:
                # (=> should be ()=>
                fixed_js_content = fix_arrow_function(new_full_js, error_line)
                if fixed_js_content != new_full_js:
                    new_full_js = fixed_js_content
                    fixed = True
            elif "Unexpected token '{'" in error_msg:
                # Missing ) before {
                fixed_js_content = add_close_paren_before_brace(new_full_js, error_line)
                if fixed_js_content != new_full_js:
                    new_full_js = fixed_js_content
                    fixed = True
        
        elif 'Invalid regular expression' in error_msg:
            # Fix regex - missing ) in regex pattern
            fixed_js_content = fix_regex(new_full_js, error_line)
            if fixed_js_content != new_full_js:
                new_full_js = fixed_js_content
                fixed = True
        
        elif 'Missing catch or finally' in error_msg:
            fixed_js_content = fix_missing_catch(new_full_js, error_line)
            if fixed_js_content != new_full_js:
                new_full_js = fixed_js_content
                fixed = True
        
        if not fixed:
            print(f"  Could not auto-fix, stopping retries")
            break
        
        # Re-validate
        valid, error = validate_js(new_full_js)
        if valid:
            print(f"  ✅ node --check passed after {retry+1} retries")
            # Write back to HTML
            # Reconstruct HTML with fixed JS
            modified_html = reconstruct_html(html, js_blocks, new_full_js)
            with open(filepath, 'w') as f:
                f.write(modified_html)
            return True
        
        new_paren_diff = new_full_js.count('(') - new_full_js.count(')')
        new_brace_diff = new_full_js.count('{') - new_full_js.count('}')
        print(f"  After retry: paren_diff={new_paren_diff} brace_diff={new_brace_diff}")
    
    # Failed - rollback
    print(f"  ❌ Could not fix after all retries")
    return False

def reconstruct_html(original_html, original_js_blocks, fixed_full_js):
    """Reconstruct HTML with fixed JS, preserving non-JS content."""
    # Simple approach: replace each script block
    # Split fixed_full_js by the same number of blocks
    # This is tricky because the blocks might have changed size
    # Instead, just replace the entire content between first <script> and last </script>
    
    # Find all script blocks
    pattern = re.compile(r'(<script>)(.*?)(</script>)', re.DOTALL)
    blocks = list(pattern.finditer(original_html))
    
    # Filter to JS blocks only (not analytics)
    js_block_indices = []
    for i, match in enumerate(blocks):
        js = match.group(2).strip()
        if not js:
            continue
        if 'dataLayer' in js[:50] or 'gtag' in js[:30] or 'application/ld+json' in js[:30]:
            continue
        js_block_indices.append(i)
    
    if len(js_block_indices) == 1:
        # Simple case - just replace the one block
        idx = js_block_indices[0]
        match = blocks[idx]
        return original_html[:match.start()] + '<script>' + fixed_full_js + '</script>' + original_html[match.end():]
    
    # Multiple blocks - need to split fixed_full_js
    # For now, put everything in the first JS block and empty the rest
    # This is a simplification that might not work for all cases
    result = original_html
    offset = 0
    first = True
    for idx in js_block_indices:
        match = blocks[idx]
        start = match.start() + offset
        end = match.end() + offset
        if first:
            replacement = '<script>' + fixed_full_js + '</script>'
            first = False
        else:
            replacement = '<script></script>'
        result = result[:start] + replacement + result[end:]
        offset += len(replacement) - len(match.group(0))
    
    return result

# Targeted fix functions

def add_missing_close_paren_at_line(js, line_num):
    """Add missing ) at the specified line."""
    lines = js.split('\n')
    if line_num < 1 or line_num > len(lines):
        return js
    
    line = lines[line_num - 1]
    
    # Find where ) should be added
    # Track paren depth in this line
    depth = 0
    in_string = False
    string_char = None
    last_open_pos = -1
    
    for i, ch in enumerate(line):
        if not in_string and ch in ('"', "'", '`'):
            in_string = True
            string_char = ch
            continue
        if in_string:
            if ch == '\\': continue
            if ch == string_char:
                in_string = False
            continue
        if ch == '(':
            depth += 1
            last_open_pos = i
        elif ch == ')':
            depth -= 1
    
    if depth > 0:
        # Add ) before the ; at end of line, or at end
        rstripped = line.rstrip()
        if rstripped.endswith(';'):
            line = rstripped[:-1] + ')' * depth + ';'
        elif rstripped.endswith('{'):
            line = rstripped[:-1] + ')' * depth + '{'
        else:
            line = rstripped + ')' * depth
        lines[line_num - 1] = line
    
    return '\n'.join(lines)

def remove_extra_close_paren_at_line(js, line_num):
    """Remove extra ) at the specified line."""
    lines = js.split('\n')
    if line_num < 1 or line_num > len(lines):
        return js
    
    line = lines[line_num - 1]
    
    # Find the position of the extra ) indicated by the error
    # The error usually points to the position with ^
    # Simple approach: find the first ) that doesn't have a matching ( on this line
    # or remove one ) from the line
    
    # Count parens
    depth = 0
    in_string = False
    string_char = None
    extra_positions = []
    
    for i, ch in enumerate(line):
        if not in_string and ch in ('"', "'", '`'):
            in_string = True
            string_char = ch
            continue
        if in_string:
            if ch == '\\': continue
            if ch == string_char:
                in_string = False
            continue
        if ch == '(':
            depth += 1
        elif ch == ')':
            depth -= 1
            if depth < 0:
                extra_positions.append(i)
                depth = 0  # Reset to avoid counting cascading extras
    
    if extra_positions:
        # Remove the first extra )
        pos = extra_positions[0]
        line = line[:pos] + line[pos+1:]
        lines[line_num - 1] = line
    
    return '\n'.join(lines)

def remove_extra_close_brace_at_line(js, line_num):
    """Remove extra } at the specified line."""
    lines = js.split('\n')
    if line_num < 1 or line_num > len(lines):
        return js
    
    line = lines[line_num - 1]
    
    # Find and remove extra }
    # Simple: remove one } from the line
    idx = line.find('}')
    if idx >= 0:
        line = line[:idx] + line[idx+1:]
        lines[line_num - 1] = line
    
    return '\n'.join(lines)

def fix_missing_try(js, line_num):
    """Fix catch without try by adding try{."""
    lines = js.split('\n')
    if line_num < 1 or line_num > len(lines):
        return js
    
    # Find the catch line
    line = lines[line_num - 1]
    
    # Look for pattern: }catch(e){
    # Need to find the matching } and add try{ before it
    # Simple approach: find the previous } and add try{ before the block
    
    # Find the start of the try block by looking backwards for matching {
    brace_depth = 0
    start_line = line_num - 1
    
    for i in range(line_num - 2, -1, -1):
        l = lines[i]
        for ch in reversed(l):
            if ch == '}':
                brace_depth += 1
            elif ch == '{':
                brace_depth -= 1
                if brace_depth < 0:
                    start_line = i
                    break
        if brace_depth < 0:
            break
    
    # Add try before the { on start_line
    if start_line >= 0:
        l = lines[start_line]
        brace_pos = l.rfind('{')
        if brace_pos >= 0:
            lines[start_line] = l[:brace_pos] + 'try{' + l[brace_pos+1:]
    
    return '\n'.join(lines)

def fix_else_without_brace(js, line_num):
    """Fix else without closing } before it."""
    lines = js.split('\n')
    if line_num < 1 or line_num > len(lines):
        return js
    
    # Add } before else
    line = lines[line_num - 1]
    # Pattern: else{ → }else{
    if line.strip().startswith('else'):
        lines[line_num - 1] = '}' + line
    
    return '\n'.join(lines)

def fix_unexpected_semicolon(js, line_num):
    """Fix unexpected ; - often caused by missing ) or (."""
    lines = js.split('\n')
    if line_num < 1 or line_num > len(lines):
        return js
    
    line = lines[line_num - 1]
    
    # Common pattern: setTimeout((=>expr, 1000); → setTimeout(()=>expr, 1000);
    # Or: loadExample(; → loadExample();
    # Or: showAll(; → showAll();
    
    # Pattern: function call with just (; 
    line = re.sub(r'(\w+)\(\;', r'\1();', line)
    
    # Pattern: (=> should be ()=>
    line = re.sub(r'\(=>', '()=>', line)
    
    lines[line_num - 1] = line
    return '\n'.join(lines)

def fix_arrow_function(js, line_num):
    """Fix (=> to ()=>."""
    lines = js.split('\n')
    if line_num < 1 or line_num > len(lines):
        return js
    
    line = lines[line_num - 1]
    line = re.sub(r'\(=>', '()=>', line)
    lines[line_num - 1] = line
    return '\n'.join(lines)

def add_close_paren_before_brace(js, line_num):
    """Add ) before { when missing."""
    lines = js.split('\n')
    if line_num < 1 or line_num > len(lines):
        return js
    
    line = lines[line_num - 1]
    # Pattern: if(cond{ → if(cond){
    # Find { and check if ( is unmatched before it
    brace_pos = line.find('{')
    if brace_pos >= 0:
        # Count parens before {
        before_brace = line[:brace_pos]
        depth = 0
        in_string = False
        string_char = None
        for ch in before_brace:
            if not in_string and ch in ('"', "'", '`'):
                in_string = True
                string_char = ch
                continue
            if in_string:
                if ch == string_char:
                    in_string = False
                continue
            if ch == '(': depth += 1
            elif ch == ')': depth -= 1
        
        if depth > 0:
            line = line[:brace_pos] + ')' * depth + line[brace_pos:]
            lines[line_num - 1] = line
    
    return '\n'.join(lines)

def fix_regex(js, line_num):
    """Fix invalid regex - missing ) in pattern."""
    lines = js.split('\n')
    if line_num < 1 or line_num > len(lines):
        return js
    
    line = lines[line_num - 1]
    
    # Find regex pattern and add missing )
    # Pattern: /pattern/flags where pattern has unmatched (
    # Find /.../ patterns
    regex_match = re.search(r'/([^/\n]*)/([gimsuy]*)', line)
    if regex_match:
        pattern = regex_match.group(1)
        flags = regex_match.group(2)
        # Count ( and ) in pattern, ignoring \(
        clean_pattern = re.sub(r'\\.', '', pattern)
        opens = clean_pattern.count('(') - clean_pattern.count(')')
        if opens > 0:
            # Add missing ) before the closing /
            new_pattern = pattern + ')' * opens
            old_regex = '/' + pattern + '/' + flags
            new_regex = '/' + new_pattern + '/' + flags
            line = line.replace(old_regex, new_regex, 1)
            lines[line_num - 1] = line
    
    return '\n'.join(lines)

def fix_missing_catch(js, line_num):
    """Fix try without catch/finally."""
    lines = js.split('\n')
    if line_num < 1 or line_num > len(lines):
        return js
    
    # Add }catch(e){} after the try block
    line = lines[line_num - 1]
    if line.strip() == '}':
        lines[line_num - 1] = '}catch(e){}'
    
    return '\n'.join(lines)

# Main execution
result = subprocess.run(['python3', '-c', """
import re, glob
for f in sorted(glob.glob('*/index.html')) + sorted(glob.glob('en/*/index.html')):
    html = open(f, errors='ignore').read()
    scripts = re.findall(r'<script>(.*?)</script>', html, re.DOTALL)
    js_parts = [s.strip() for s in scripts if s.strip() and 'dataLayer' not in s[:50] and 'gtag' not in s[:30] and 'application/ld+json' not in s[:30]]
    if not js_parts: continue
    js = chr(10).join(js_parts)
    opens = js.count('(') - js.count(')')
    brace_diff = js.count('{') - js.count('}')
    if abs(opens) > 3 or abs(brace_diff) > 2:
        if not (js.rstrip().endswith(')();') and js.count(')();') > 1):
            print(f'{f}: paren={opens} brace={brace_diff}')
"""], capture_output=True, text=True, cwd='/home/chison/tools-site')

files_to_fix = []
for line in result.stdout.strip().split('\n'):
    if ':' in line:
        filepath = line.split(':')[0]
        files_to_fix.append(filepath)

print(f"Found {len(files_to_fix)} files to fix")

fixed_count = 0
failed_count = 0
failed_files = []

for filepath in files_to_fix:
    try:
        if fix_file_interactive(filepath):
            fixed_count += 1
        else:
            # Rollback
            subprocess.run(['git', 'checkout', '--', filepath], cwd='/home/chison/tools-site', capture_output=True)
            failed_count += 1
            failed_files.append(filepath)
    except Exception as e:
        print(f"  ❌ Error: {e}")
        subprocess.run(['git', 'checkout', '--', filepath], cwd='/home/chison/tools-site', capture_output=True)
        failed_count += 1
        failed_files.append(filepath)

print(f"\n{'='*60}")
print(f"Summary: Fixed={fixed_count}, Failed={failed_count}, Total={len(files_to_fix)}")
if failed_files:
    print(f"Failed files:")
    for f in failed_files:
        print(f"  {f}")
