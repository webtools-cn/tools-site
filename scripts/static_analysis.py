#!/usr/bin/env python3
"""
全站JS静态分析 - 检测语法错误、未定义函数、DOM null等问题
替代Puppeteer（因Chrome在kernel 7.0上崩溃无法运行）
"""
import re, os, subprocess, json
from datetime import datetime
from collections import defaultdict

SKIP = {'_gen','__pycache__','en','libs','js','css','scripts','tools',
        '.git','data','about','blog','privacy-policy','terms-of-service','category'}

results = {
    'syntax_errors': [],
    'undefined_functions': [],
    'dom_null_risk': [],
    'missing_h1': [],
    'missing_interaction': [],
    'no_js': [],
}
pass_count = 0
total = 0

def extract_scripts(html_path):
    with open(html_path) as f:
        content = f.read()
    scripts = list(re.finditer(r'<script([^>]*)>(.*?)</script>', content, re.DOTALL))
    inline_scripts = []
    for m in scripts:
        attrs = m.group(1)
        body = m.group(2).strip()
        if 'application/ld+json' in attrs or 'src=' in attrs or not body:
            continue
        inline_scripts.append(body)
    return content, inline_scripts

def check_syntax(tool_name, scripts):
    """Check each script with node -c"""
    errors = []
    for i, js in enumerate(scripts):
        r = subprocess.run(['node', '-c'], input=js, capture_output=True, text=True, timeout=5)
        if r.returncode != 0:
            err = r.stderr.strip()
            for line in err.split('\n'):
                if 'SyntaxError' in line:
                    errors.append(f'Script#{i}: {line.strip()[:120]}')
                    break
    return errors

def check_undefined_functions(tool_name, scripts):
    """Check for functions called but not defined"""
    issues = []
    for i, js in enumerate(scripts):
        # Find all function calls: xxx(...) that look like named functions
        calls = set(re.findall(r'(?<![.\"\'])([a-zA-Z_$][\w$]*)\(', js))
        # Find function definitions
        defs = set(re.findall(r'function\s+([a-zA-Z_$][\w$]*)', js))
        defs.update(re.findall(r'(?:const|let|var)\s+([a-zA-Z_$][\w$]*)\s*=\s*(?:async\s*)?\(', js))
        defs.update(re.findall(r'(?:const|let|var)\s+([a-zA-Z_$][\w$]*)\s*=\s*function', js))
        # Common builtins
        builtins = {'console','document','window','Math','JSON','Array','Object','String',
                     'Number','Boolean','Date','RegExp','Error','Promise','Set','Map',
                     'parseInt','parseFloat','isNaN','isFinite','eval','encodeURIComponent',
                     'decodeURIComponent','encodeURI','decodeURI','setTimeout','setInterval',
                     'clearTimeout','clearInterval','alert','confirm','prompt','fetch',
                     'navigator','location','history','localStorage','sessionStorage',
                     'addEventListener','removeEventListener','querySelector','querySelectorAll',
                     'getElementById','getElementsByClassName','getElementsByTagName',
                     'createElement','createTextNode','appendChild','removeChild',
                     'classList','innerHTML','textContent','value','style',
                     'split','join','map','filter','reduce','forEach','push','pop',
                     'trim','toLowerCase','toUpperCase','replace','match','indexOf',
                     'includes','startsWith','endsWith','slice','substring','substr',
                     'toString','toFixed','toPrecision','length','charAt','charCodeAt',
                     'fromCharCode','keys','values','entries','has','get','set','delete',
                     'then','catch','finally','async','await','new','this','return',
                     'if','else','for','while','do','switch','case','break','continue',
                     'try','catch','throw','typeof','instanceof','in','of','null','undefined',
                     'true','false','import','export','default','class','extends','super',
                     'require','module','process','Intl','Proxy','Reflect','Symbol',
                     'WeakMap','WeakSet','ArrayBuffer','DataView','Float32Array','Float64Array',
                     'Int8Array','Int16Array','Int32Array','Uint8Array','Uint16Array','Uint32Array',
                     'Uint8ClampedArray','BigInt64Array','BigUint64Array','atob','btoa',
                     'requestAnimationFrame','cancelAnimationFrame','getComputedStyle',
                     'matchMedia','CustomEvent','Event','MouseEvent','KeyboardEvent',
                     'FocusEvent','InputEvent','ClipboardEvent','DragEvent','PointerEvent',
                     'WheelEvent','TouchEvent','Blob','File','FileReader','FileList',
                     'FormData','URL','URLSearchParams','Headers','Request','Response',
                     'AbortController','AbortSignal','TextEncoder','TextDecoder',
                     'crypto','structuredClone','queueMicrotask','reportError',
                     'performance','ResizeObserver','IntersectionObserver','MutationObserver',
                     'scrollTo','scrollBy','getBoundingClientRect','focus','blur','click',
                     'preventDefault','stopPropagation','stopImmediatePropagation',
                     'open','close','print','postMessage','getSelection',
                     'showToast','copyToClipboard','copyResult','toggleTheme','switchTab',
                     'debounce','throttle','formatNumber','formatBytes','formatDate',
                     'escapeHtml','unescapeHtml','generateId','getRandomInt','clamp',
                     'showNotification','hideNotification','showModal','hideModal',
                     'downloadFile','readFile','uploadFile','validateEmail','validateUrl',
                     'truncateText','capitalizeFirst','camelToKebab','kebabToCamel',
                     'isMobile','isDarkMode','getQueryParam','setQueryParam',
                     'showTab','resetForm','clearOutput','togglePassword',
                     'handleInput','handleSubmit','handleClick','handleChange',
                     'init','main','setup','render','update','calculate','convert',
                     'encode','decode','encrypt','decrypt','hash','compress','decompress',
                     'format','parse','validate','generate','transform','analyze',
                     'toast','toggle','switchTheme','switchLang','copy',
                     'navigator.clipboard.writeText','document.execCommand',
                     'document.querySelector','document.getElementById',
                     'document.createElement','document.body.appendChild',
                     'window.open','window.location','window.navigator',
                     'console.log','console.error','console.warn','console.info',
                     'Math.random','Math.floor','Math.ceil','Math.round','Math.abs',
                     'Math.max','Math.min','Math.pow','Math.sqrt','Math.PI',
                     'JSON.parse','JSON.stringify','Object.keys','Object.values',
                     'Object.entries','Object.assign','Array.from','Array.isArray',
                     'String.fromCharCode','parseInt','parseFloat',
                     'crypto.subtle.digest','crypto.getRandomValues',
                     'performance.now','Intl.DateTimeFormat','Intl.NumberFormat',
                     'ClipboardItem','navigator.clipboard',
                     # Common DOM element IDs used as global references
                     'input','output','result','fileInput','dropZone',
                     # IIFE patterns
                     'window','document','globalThis','self',
                     # Common jQuery-like patterns
                     '$','jQuery'}
        undefined = calls - defs - builtins
        # Filter false positives
        real_undefined = set()
        for fn in undefined:
            if len(fn) <= 1 or fn[0].isupper() and fn not in js.split('function ' + fn):
                continue
            # Check if it looks like a real function call (not an HTML element ref)
            if re.search(rf'\b{re.escape(fn)}\s*\(', js):
                # Check it's not defined via window.fn = 
                if not re.search(rf'window\.{re.escape(fn)}\s*=', js) and \
                   not re.search(rf'this\.{re.escape(fn)}\s*=', js):
                    real_undefined.add(fn)
        if real_undefined:
            issues.append(f'Script#{i}: {", ".join(sorted(real_undefined)[:5])}')
    return issues

def check_dom_null(tool_name, html_content, scripts):
    """Check for DOM access without null checks"""
    issues = []
    for i, js in enumerate(scripts):
        # Find getElementById/querySelector calls
        dom_gets = re.findall(r'(?:getElementById|querySelector|querySelectorAll)\s*\(\s*[\'\"]([^\'\"]+)[\'\"]', js)
        for el_id in dom_gets[:10]:
            # Check if there's a null check for this element
            null_check_patterns = [
                rf'if\s*\(\s*{re.escape(el_id)}\s*\)',
                rf'if\s*\(\s*!\s*{re.escape(el_id)}\s*\)',
                rf'{re.escape(el_id)}\s*\?\s*\.',
                rf'{re.escape(el_id)}\s*&&',
                rf'if\s*\(\s*.*{re.escape(el_id)}.*\s*===\s*null',
                rf'if\s*\(\s*.*{re.escape(el_id)}.*\s*!==\s*null',
                rf'{re.escape(el_id)}\s*!=\s*null',
            ]
            has_check = any(re.search(p, js) for p in null_check_patterns)
            if not has_check and el_id not in js.replace(el_id, '', 1):  # not just a string literal
                # Check if it's accessed directly after querySelector
                direct_access = re.search(rf'querySelector.*{re.escape(el_id)}.*\.', js)
                if direct_access:
                    issues.append(f'Script#{i}: {el_id} accessed without null check')
    return issues[:5]

def check_missing_h1(tool_name, html_content):
    if '<h1' not in html_content.lower():
        return ['Missing <h1>']
    return []

def check_missing_interaction(tool_name, html_content):
    """Check for minimal interaction elements"""
    inputs = len(re.findall(r'<(?:input|textarea|select)\s', html_content, re.I))
    buttons = len(re.findall(r'<(?:button|input\s+type=[\"\']submit)', html_content, re.I))
    if inputs + buttons < 2:
        return [f'Low interaction: {inputs} inputs + {buttons} buttons']
    return []

# Main
tool_dirs = sorted([d for d in os.listdir('.') if os.path.isdir(d) and d not in SKIP and not d.startswith('.')])

for d in tool_dirs:
    html_path = os.path.join(d, 'index.html')
    if not os.path.exists(html_path):
        continue
    total += 1
    try:
        html_content, scripts = extract_scripts(html_path)
        if not scripts:
            results['no_js'].append(d)
            continue
        
        # Syntax check
        syntax_errors = check_syntax(d, scripts)
        if syntax_errors:
            results['syntax_errors'].append({'tool': d, 'errors': syntax_errors})
            continue  # Skip other checks if syntax is broken
        
        # Undefined function check
        undefined = check_undefined_functions(d, scripts)
        if undefined:
            results['undefined_functions'].append({'tool': d, 'errors': undefined})
        
        # DOM null check
        dom_issues = check_dom_null(d, html_content, scripts)
        if dom_issues:
            results['dom_null_risk'].append({'tool': d, 'errors': dom_issues})
        
        # Missing h1
        h1_issues = check_missing_h1(d, html_content)
        if h1_issues:
            results['missing_h1'].append({'tool': d, 'errors': h1_issues})
        
        # Interaction check
        int_issues = check_missing_interaction(d, html_content)
        if int_issues:
            results['missing_interaction'].append({'tool': d, 'errors': int_issues})
        
        pass_count += 1
    except Exception as e:
        print(f'Error processing {d}: {e}')

# Build report
total_issues = sum(len(v) for v in results.values())
report = {
    'timestamp': datetime.now().isoformat(),
    'type': 'static_analysis',
    'total': total,
    'pass': total - total_issues,
    'issues': {
        'syntax_errors': len(results['syntax_errors']),
        'undefined_functions': len(results['undefined_functions']),
        'dom_null_risk': len(results['dom_null_risk']),
        'missing_h1': len(results['missing_h1']),
        'missing_interaction': len(results['missing_interaction']),
        'no_js': len(results['no_js']),
    },
    'details': {k: v[:50] for k, v in results.items() if v}
}

os.makedirs('quality-reports', exist_ok=True)
fname = f"quality-reports/static-analysis-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
with open(fname, 'w') as f:
    json.dump(report, f, indent=2, ensure_ascii=False)

print(f'Total: {total}')
print(f'Pass: {report["pass"]}')
for k, v in report['issues'].items():
    if v:
        print(f'  {k}: {v}')
print(f'Report: {fname}')