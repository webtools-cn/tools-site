#!/usr/bin/env python3
"""Analyze a tool's HTML to extract structure info needed for writing missing functions."""
import re, sys, json

def analyze_tool(tool_name):
    path = f'{tool_name}/index.html'
    html = open(path, errors='ignore').read()
    
    # Extract h1
    h1_match = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.DOTALL)
    h1 = re.sub(r'<[^>]+>', '', h1_match.group(1)).strip() if h1_match else ''
    
    # Extract meta description
    desc_match = re.search(r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']*)["\']', html)
    desc = desc_match.group(1) if desc_match else ''
    
    # Extract input fields with their ids and types
    inputs = re.findall(r'<input[^>]*\bid=["\']([^"\']+)["\'][^>]*>', html)
    selects = re.findall(r'<select[^>]*\bid=["\']([^"\']+)["\'][^>]*>', html)
    textareas = re.findall(r'<textarea[^>]*\bid=["\']([^"\']+)["\'][^>]*>', html)
    
    # Extract result/output areas
    results = re.findall(r'<(?:div|span|p|pre|code)[^>]*\bid=["\'](?:result|output|display|preview|canvas)[^"\']*["\'][^>]*>', html, re.IGNORECASE)
    result_ids = re.findall(r'\bid=["\']([^"\']*(?:result|output|display|preview|canvas)[^"\']*)["\']', html, re.IGNORECASE)
    
    # Extract onclick handlers
    onclicks = re.findall(r'onclick=["\']([^"\']+)["\']', html)
    
    # Extract oninput/onchange handlers
    oninputs = re.findall(r'on(?:input|change)=["\']([^"\']+)["\']', html)
    
    # Extract existing JS
    scripts = re.findall(r'<script>(.*?)</script>', html, re.DOTALL)
    js_parts = [s.strip() for s in scripts if s.strip() and 'dataLayer' not in s[:50] and 'gtag' not in s[:30] and 'application/ld+json' not in s[:30]]
    js = '\n'.join(js_parts)
    
    # Find defined functions
    fn_defs = set(re.findall(r'function\s+(\w+)\s*\(', js))
    
    # Find event-referenced functions
    events = re.findall(r'(?:onclick|oninput|onchange)\s*=\s*["\x27]([^"\x27]+)["\x27]', html)
    event_fns = set()
    for e in events:
        m = re.match(r'(\w+)\s*\(', e)
        if m and m.group(1) not in ('if','else','for','while','return','this','document','window','event','e','typeof','void','not','and','or','true','false','null','undefined'):
            event_fns.add(m.group(1))
    
    missing = sorted(event_fns - fn_defs)
    
    # Find stub functions (window.fn = window.fn || function(){})
    stubs = re.findall(r'window\.(\w+)\s*=\s*window\.\1\s*\|\|\s*function\s*\(\)\s*\{', js)
    
    # Find copyText helper
    has_copyText = 'function copyText' in js or 'function copyToClipboard' in js
    
    # Find the last script block position
    last_script_end = html.rfind('</script>')
    
    return {
        'tool': tool_name,
        'h1': h1,
        'desc': desc,
        'inputs': inputs,
        'selects': selects,
        'textareas': textareas,
        'result_ids': result_ids,
        'onclicks': onclicks[:10],
        'oninputs': oninputs[:10],
        'fn_defs': sorted(fn_defs),
        'missing': missing,
        'stubs': stubs,
        'has_copyText': has_copyText,
        'js_preview': js[:3000],
        'html_preview': html[:5000],
    }

if __name__ == '__main__':
    tool = sys.argv[1]
    info = analyze_tool(tool)
    print(json.dumps(info, ensure_ascii=False, indent=2))
