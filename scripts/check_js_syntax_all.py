#!/usr/bin/env python3
"""Check all tool pages for JS syntax errors - fast batch mode"""
import os, re, subprocess, tempfile, sys

TOOLS_ROOT = '/home/chison/tools-site'
NOT_TOOLS = {'about','blog','privacy','terms','contact'}
SKIP = {'en','assets','scripts','quality','css','js','images','node_modules','.git','.github','fonts','libs','vendor','dist','build','.gsc-data','quality-reports'}

def extract_js(filepath):
    with open(filepath) as f:
        h = f.read()
    pattern = r'<script(?![^>]*\bsrc=)(?![^>]*type=["\']application/ld\+json)(?![^>]*type=["\']application/json)>(.*?)</script>'
    scripts = re.findall(pattern, h, re.DOTALL)
    main_scripts = []
    for s in scripts:
        s = s.strip()
        if not s:
            continue
        if s.startswith('window.dataLayer'):
            continue
        if s.startswith('window.addEventListener("error"') or s.startswith("window.addEventListener('error'"):
            continue
        if s.startswith('window.addEventListener("unhandledrejection"') or s.startswith("window.addEventListener('unhandledrejection'"):
            continue
        main_scripts.append(s)
    if not main_scripts:
        return None
    return '\n'.join(main_scripts)

# Collect all tools
tools = []
dirs = sorted(d for d in os.listdir(TOOLS_ROOT) 
              if os.path.isdir(os.path.join(TOOLS_ROOT, d)) 
              and d not in NOT_TOOLS|SKIP 
              and os.path.exists(os.path.join(TOOLS_ROOT, d, 'index.html')))
for name in dirs:
    tools.append((f'CN/{name}', f'{TOOLS_ROOT}/{name}/index.html'))

en_dirs = sorted(d for d in os.listdir(f'{TOOLS_ROOT}/en') 
                 if os.path.isdir(os.path.join(TOOLS_ROOT, 'en', d)) 
                 and d not in NOT_TOOLS|SKIP
                 and os.path.exists(os.path.join(TOOLS_ROOT, 'en', d, 'index.html')))
for name in en_dirs:
    tools.append((f'EN/{name}', f'{TOOLS_ROOT}/en/{name}/index.html'))

print(f'Total tools to check: {len(tools)}', file=sys.stderr)

# Write all JS to a single file with markers, then check
# Actually, better: write each to a temp file and batch-check
import json
results = []
batch_size = 50
for i in range(0, len(tools), batch_size):
    batch = tools[i:i+batch_size]
    # Create a single JS file with try-catch wrappers
    js_parts = []
    tool_map = {}
    for j, (tool_name, filepath) in enumerate(batch):
        js = extract_js(filepath)
        if js is None:
            continue
        # Wrap in a function to isolate syntax errors
        wrapped = f'// TOOL:{tool_name}\n{js}\n// END:{tool_name}\n'
        js_parts.append(wrapped)
        tool_map[j] = tool_name
    
    if not js_parts:
        continue
    
    # Write each tool's JS separately and check
    for j, (tool_name, filepath) in enumerate(batch):
        js = extract_js(filepath)
        if js is None:
            continue
        tmppath = f'/tmp/jscheck_{i+j}.js'
        with open(tmppath, 'w') as f:
            f.write(js)
        result = subprocess.run(['node', '--check', tmppath], capture_output=True, text=True, timeout=3)
        os.unlink(tmppath)
        if result.returncode != 0:
            err = result.stderr.strip()
            err_line = err.split('\n')[-1] if '\n' in err else err
            results.append(f'{tool_name}: {err_line}')
    
    if (i + batch_size) % 500 == 0:
        print(f'  Checked {i+batch_size} tools...', file=sys.stderr, flush=True)

print(f'Total tools checked: {len(tools)}')
print(f'Broken JS: {len(results)}')
for r in results:
    print(f'  {r}')
