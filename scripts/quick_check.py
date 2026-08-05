#!/usr/bin/env python3
"""Quick check: JS syntax + theme colors for a list of tools."""
import re, subprocess, tempfile, os, sys

tools = sys.argv[1:]

def check_js(filepath):
    content = open(filepath).read()
    scripts = []
    for match in re.finditer(r'<script([^>]*)>(.*?)</script>', content, re.DOTALL):
        attrs = match.group(1)
        body = match.group(2).strip()
        if not body:
            continue
        if 'application/ld+json' in attrs:
            continue
        if body.startswith('{') and '"@context"' in body[:100]:
            continue
        scripts.append(body)
    errors = []
    for s in scripts:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
            f.write(s)
            fname = f.name
        result = subprocess.run(['node', '-c', fname], capture_output=True, text=True)
        os.unlink(fname)
        if result.returncode != 0:
            err_line = result.stderr.strip().split('\n')[0][:150]
            errors.append(err_line)
    return len(scripts), errors

def check_theme(filepath):
    content = open(filepath).read()
    issues = []
    # Check for light backgrounds
    light_bgs = re.findall(r'(?:background|bg)\s*:\s*(#fff|#ffffff|#f8fafc|#f8f9fa|#faf8f5|#fdf2f8)\b', content, re.IGNORECASE)
    if light_bgs:
        issues.append(f"Light bg: {light_bgs[:3]}")
    # Check :root variables
    root_match = re.search(r':root\s*\{([^}]+)\}', content)
    if root_match:
        root = root_match.group(1)
        if '--bg' in root:
            bg_match = re.search(r'--bg\s*:\s*([^;]+)', root)
            if bg_match and '#0f172a' not in bg_match.group(1):
                issues.append(f"--bg={bg_match.group(1).strip()}")
        if '--card-bg' in root:
            card_match = re.search(r'--card-bg\s*:\s*([^;]+)', root)
            if card_match and '#1e293b' not in card_match.group(1):
                issues.append(f"--card-bg={card_match.group(1).strip()}")
    else:
        issues.append("No :root found")
    return issues

def check_en_chinese(filepath):
    """Check if EN page has Chinese characters (excluding schema/ld+json)."""
    content = open(filepath).read()
    # Remove ld+json blocks
    content_clean = re.sub(r'<script\s+type="application/ld\+json">.*?</script>', '', content, flags=re.DOTALL)
    # Remove HTML comments
    content_clean = re.sub(r'<!--.*?-->', '', content_clean, flags=re.DOTALL)
    # Find Chinese characters
    chinese = re.findall(r'[\u4e00-\u9fff]+', content_clean)
    return chinese[:10]

for tool in tools:
    print(f"\n{'='*60}")
    print(f"TOOL: {tool}")
    print(f"{'='*60}")
    for lang_label, path in [("CN", f"{tool}/index.html"), ("EN", f"en/{tool}/index.html")]:
        if not os.path.exists(path):
            print(f"  [{lang_label}] FILE NOT FOUND: {path}")
            continue
        # JS check
        n_blocks, js_errors = check_js(path)
        if js_errors:
            for e in js_errors:
                print(f"  [{lang_label}] JS ERROR: {e}")
        else:
            print(f"  [{lang_label}] JS OK ({n_blocks} blocks)")
        # Theme check
        theme_issues = check_theme(path)
        if theme_issues:
            for t in theme_issues:
                print(f"  [{lang_label}] THEME: {t}")
        else:
            print(f"  [{lang_label}] Theme OK")
        # EN Chinese check
        if lang_label == "EN":
            chinese = check_en_chinese(path)
            if chinese:
                print(f"  [{lang_label}] CHINESE FOUND: {chinese[:5]}")
            else:
                print(f"  [{lang_label}] No Chinese (OK)")
