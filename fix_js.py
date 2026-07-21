#!/usr/bin/env python3
"""Fix JS syntax errors in tool HTML files by extracting, checking, and applying fixes."""
import subprocess
import re
import sys
import os

TOOLS = [
    "apache-config-generator", "api-response-mocker", "bar-chart-maker",
    "bic-checker", "business-name-generator", "character-frequency",
    "code-diff", "color-namer", "cron-expression-parser",
    "css-hover-animation-effects", "css-hover-effects",
    "css-keyframe-animation-generator", "css-to-js", "csv-to-sql",
    "curl-to-python", "daily-affirmation-generator", "dns-record-comparator",
    "dockerfile-formatter", "dockerfile-linter", "editorconfig-generator"
]

BASE = "/home/chison/tools-site"

def extract_js(tool):
    """Extract JS from HTML file."""
    path = f"{BASE}/{tool}/index.html"
    result = subprocess.run(
        ["python3", f"{BASE}/scripts/extract_js.py", path],
        capture_output=True, text=True
    )
    tmp = f"/tmp/{tool}.js"
    with open(tmp, 'w') as f:
        f.write(result.stdout)
    return tmp

def check_js(tmp_path):
    """Check JS syntax with node -c."""
    result = subprocess.run(
        ["node", "-c", tmp_path],
        capture_output=True, text=True
    )
    return result.returncode, result.stderr

def get_error_info(stderr):
    """Parse node error to get line number and error type."""
    m = re.search(r':(\d+)\n.*SyntaxError: (.+)', stderr)
    if m:
        return int(m.group(1)), m.group(2)
    return None, None

def read_html(tool):
    path = f"{BASE}/{tool}/index.html"
    with open(path, 'r') as f:
        return f.read()

def write_html(tool, content):
    path = f"{BASE}/{tool}/index.html"
    with open(path, 'w') as f:
        f.write(content)

def verify(tool):
    tmp = extract_js(tool)
    rc, err = check_js(tmp)
    return rc == 0, err

# Process each tool
results = {}
for tool in TOOLS:
    print(f"\n{'='*60}")
    print(f"Processing: {tool}")
    
    # Extract and check
    tmp = extract_js(tool)
    rc, err = check_js(tmp)
    if rc == 0:
        print(f"  Already OK!")
        results[tool] = "OK"
        continue
    
    line_no, error_type = get_error_info(err)
    print(f"  Error at line {line_no}: {error_type}")
    
    # Read the extracted JS to see the problematic line
    with open(tmp, 'r') as f:
        js_lines = f.readlines()
    if line_no and line_no <= len(js_lines):
        print(f"  JS line: {js_lines[line_no-1][:120]}...")
    
    # Read the HTML
    html = read_html(tool)
    
    # Try automated fixes based on error type
    fixed = False
    
    if tool == "apache-config-generator":
        # Invalid regular expression flags - regex in template literal
        # The issue is proxyUrl.replace(/^https?:\/\/... inside a template literal
        # Need to escape the backslashes properly or use a different approach
        old = "proxyUrl.replace(/^https?:\\\\/\\\\//,'')"
        new = "proxyUrl.replace(/^https?:[\\\\/\\\\/]/,'')"
        if old in html:
            html = html.replace(old, new)
            write_html(tool, html)
            ok, e = verify(tool)
            if ok:
                print(f"  FIXED!")
                results[tool] = "FIXED"
                fixed = True
            else:
                print(f"  Still broken: {e}")
                # Revert and try different fix
                html = html.replace(new, old)
    
    if not fixed and tool == "apache-config-generator":
        # Try replacing the entire problematic section with simpler code
        old = """if(proxyWs)cfg+=`  RewriteEngine On\\n  RewriteCond %{HTTP:Upgrade} =websocket [NC]\\n  RewriteRule /(.*) ws://${proxyUrl.replace(/^https?:\\\\/\\\\//,'')}/$1 [P,L]\\n`;"""
        new = """if(proxyWs){var _pUrl=proxyUrl.replace(/^https?:\\/\\//,'');cfg+=`  RewriteEngine On\\n  RewriteCond %{HTTP:Upgrade} =websocket [NC]\\n  RewriteRule /(.*) ws://${_pUrl}/$1 [P,L]\\n`;}"""
        if old in html:
            html = html.replace(old, new)
            write_html(tool, html)
            ok, e = verify(tool)
            if ok:
                print(f"  FIXED with approach 2!")
                results[tool] = "FIXED"
                fixed = True
            else:
                print(f"  Still broken: {e}")
    
    if not fixed:
        print(f"  NEEDS MANUAL FIX")
        results[tool] = f"MANUAL: {error_type}"

print(f"\n\n{'='*60}")
print("SUMMARY:")
for tool, status in results.items():
    print(f"  {tool}: {status}")
