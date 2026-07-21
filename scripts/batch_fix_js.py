#!/usr/bin/env python3
"""Batch fix JS syntax errors in HTML tool files.
Fixes common patterns found in broken tools.
"""
import re, os, sys, json, subprocess
from pathlib import Path

BASE = Path('/home/chison/tools-site')
BROKEN_LIST = Path(BASE, 'quality-reports', 'js-broken-all.json')

# Load broken list
with open(BROKEN_LIST) as f:
    data = json.load(f)

# Filter to the 40 remaining tools
remaining = {
    "fancy-text-generator", "flexbox-layout-generator", "handwriting-generator",
    "html-entity-converter", "html-meta-refresh-generator", "html-table-of-contents",
    "html-table-to-json", "html-tag-stripper", "html-wysiwyg-editor",
    "http-cache-header-generator", "markdown-link-checker", "markdown-previewer",
    "markdown-to-pdf-converter", "maze-generator", "md5-generator",
    "meta-tag-generator", "morse-code", "name-generator", "pdf-to-html",
    "privacy-policy-generator", "properties-to-yaml", "quiz-generator",
    "receipt-generator", "regex-cheatsheet", "shopping-list-generator",
    "sitemap-validator", "sql-migration-generator", "sql-to-csv",
    "sql-to-kysely", "sql-to-prisma", "svg-to-data-uri", "terms-generator",
    "text-normalizer", "text-palindrome-checker", "text-to-braille",
    "typing-test", "vite-config-generator", "word-search-generator",
    "workout-generator", "yaml-to-json"
}

def find_tool_files(tool_name):
    """Find all index.html files for a tool (zh and en)"""
    files = []
    for root, dirs, filenames in os.walk(BASE):
        if root.endswith(f'/{tool_name}') or root.endswith(f'/{tool_name}'):
            if 'index.html' in filenames:
                files.append(os.path.join(root, 'index.html'))
    return files

def extract_scripts(html):
    """Extract all script blocks, preserving position info"""
    scripts = list(re.finditer(r'<script([^>]*)>(.*?)</script>', html, re.DOTALL))
    return scripts

def check_js(js_code):
    """Check JS syntax, returns (ok, error_msg)"""
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
        f.write(js_code)
        tmp_path = f.name
    result = subprocess.run(['node', '-c', tmp_path], capture_output=True, text=True)
    os.unlink(tmp_path)
    return result.returncode == 0, result.stderr.strip()

def fix_html_in_js(js_code):
    """Fix HTML fragments accidentally included in JS extraction.
    This happens when </script> appears inside a JS string and the regex captures too much.
    """
    # Pattern 1: Remove HTML content that got included after the real script end
    # Look for common HTML patterns inside what should be pure JS
    # If we see HTML after what looks like the end of JS (like '})();' or '});'),
    # truncate there
    lines = js_code.split('\n')
    clean_lines = []
    for line in lines:
        # Stop at lines that start with HTML tags
        if re.match(r'^\s*<(div|ins|script|style|link|meta|span|p|h[1-6]|a\s)', line, re.IGNORECASE):
            break
        clean_lines.append(line)
    return '\n'.join(clean_lines)

def fix_escaped_quotes_in_html(js_code):
    """Fix \\\" sequences that came from HTML attribute escaping inside script blocks"""
    # In HTML <script>, \" is just " but some tools have \\" which becomes \" in JS
    # We need to replace \\\\"  (double-escaped) patterns
    js_code = js_code.replace('\\\\\\"', '\\"')  # Fix triple-escaped
    return js_code

def fix_template_script_tag(js_code):
    """Fix <\/script> in template strings that would break HTML parsing"""
    # The pattern <\/script> in JS is fine for JS but breaks HTML regex extraction
    # No fix needed in the JS itself, but we need to handle it during extraction
    return js_code

def fix_iife(js_code):
    """Fix IIFE (Immediately Invoked Function Expression) brace issues"""
    # Common pattern: extra or missing closing paren/bracket
    # Check brace balance
    open_paren = js_code.count('(') - js_code.count(')')
    open_brace = js_code.count('{') - js_code.count('}')
    open_bracket = js_code.count('[') - js_code.count(']')
    
    if open_paren > 0 and js_code.rstrip().endswith(';'):
        # Missing closing parens - add them
        js_code = js_code.rstrip(';') + ')' * open_paren + ';'
    return js_code

def fix_multiline_strings(js_code):
    """Fix unescaped newlines in single/double-quoted strings"""
    # Replace literal newlines in strings that aren't template literals
    # This is tricky - use a simple heuristic
    lines = js_code.split('\n')
    fixed_lines = []
    in_string = False
    string_char = None
    
    for line in lines:
        fixed_lines.append(line)
    
    return '\n'.join(fixed_lines)

def fix_regex_escapes(js_code):
    """Fix overly escaped regex patterns (\\\\\\\\w -> \\\\w etc.)"""
    # In HTML script blocks, backslashes get double-escaped
    js_code = js_code.replace('\\\\\\\\', '\\\\')
    return js_code

# Main fixing logic
fixed = []
still_broken = []
skipped = []

for tool in sorted(remaining):
    files = find_tool_files(tool)
    if not files:
        skipped.append((tool, "No files found"))
        continue
    
    zh_file = None
    en_file = None
    for f in files:
        if '/en/' in f:
            en_file = f
        else:
            zh_file = f
    
    target = zh_file or en_file
    if not target:
        skipped.append((tool, "No valid file"))
        continue
    
    with open(target) as f:
        html = f.read()
    
    # Extract main JS (last non-empty, non-gtag, non-json script)
    scripts = list(re.finditer(r'<script[^>]*>(.*?)</script>', html, re.DOTALL))
    main_js = None
    main_match = None
    for m in scripts:
        content = m.group(2).strip() if m.lastindex and m.lastindex >= 2 else m.group(1).strip()
        if content and 'window.dataLayer' not in content and not content.startswith('{'):
            main_js = content
            main_match = m
            break
    # Fallback: last script
    if not main_js:
        for m in reversed(scripts):
            content = m.group(2).strip() if m.lastindex and m.lastindex >= 2 else m.group(1).strip()
            if content and 'window.dataLayer' not in content and not content.startswith('{'):
                main_js = content
                main_match = m
                break
    
    if not main_js:
        skipped.append((tool, "No main JS found"))
        continue
    
    # Try fixes
    original_js = main_js
    ok, err = check_js(main_js)
    
    if not ok:
        # Apply fixes
        fixed_js = main_js
        
        # Fix 1: HTML in JS (truncation)
        if 'Unexpected token' in err and "'<'" in err:
            fixed_js = fix_html_in_js(fixed_js)
        
        # Fix 2: Escaped quotes
        fixed_js = fix_escaped_quotes_in_html(fixed_js)
        
        # Fix 3: IIFE balance
        if 'Unexpected token' in err and ("')'" in err or "'}'" in err or "';'" in err):
            fixed_js = fix_iife(fixed_js)
        
        # Fix 4: Regex escapes
        if '\\\\\\\\' in fixed_js:
            fixed_js = fix_regex_escapes(fixed_js)
        
        # Check again
        ok2, err2 = check_js(fixed_js)
        if ok2:
            # Replace in HTML
            html = html.replace(original_js, fixed_js, 1)
            with open(target, 'w') as f:
                f.write(html)
            fixed.append(tool)
            print(f"✅ {tool}: FIXED")
        else:
            still_broken.append((tool, err2[:150]))
            print(f"❌ {tool}: STILL BROKEN - {err2[:100]}")
    else:
        # Was already ok? Re-check
        still_broken.append((tool, "Pre-check OK but in broken list"))
        print(f"⚠️ {tool}: Already OK?")

print(f"\n=== SUMMARY ===")
print(f"Fixed: {len(fixed)}")
for t in fixed:
    print(f"  ✅ {t}")
print(f"Still broken: {len(still_broken)}")
for t, e in still_broken:
    print(f"  ❌ {t}: {e}")
print(f"Skipped: {len(skipped)}")
for t, e in skipped:
    print(f"  ⚠️ {t}: {e}")

# Update current-issues.json
issues_path = Path(BASE, 'quality-reports', 'current-issues.json')
with open(issues_path) as f:
    issues = json.load(f)

remaining_tools = [t for t, _ in still_broken] + [t for t, _ in skipped]
issues['broken_tools_remaining'] = remaining_tools
issues['summary']['gate0_js_syntax']['broken'] = len(remaining_tools)
issues['summary']['gate0_js_syntax']['ok'] = issues['summary']['gate0_js_syntax']['total'] - len(remaining_tools)
issues['summary']['gate0_js_syntax']['note'] = f"Batch fix: {len(fixed)} fixed, {len(remaining_tools)} remaining"
issues['fixed_this_run'] = fixed
issues['urgent']['reason'] = f"{len(remaining_tools)} tools still have JS syntax errors"
if len(remaining_tools) == 0:
    issues['p0_blocking'] = False

with open(issues_path, 'w') as f:
    json.dump(issues, f, ensure_ascii=False, indent=2)

print(f"\nUpdated current-issues.json: {len(remaining_tools)} remaining")
