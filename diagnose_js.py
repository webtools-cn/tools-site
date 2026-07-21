#!/usr/bin/env python3
"""诊断每个文件的精确问题"""
import os, re, tempfile, subprocess, json

BASE = os.path.expanduser("~/tools-site")

def verify_js(js_text):
    if not js_text.strip(): return True, ''
    with tempfile.NamedTemporaryFile(suffix='.js', mode='w', delete=False) as f:
        f.write(js_text); name = f.name
    r = subprocess.run(['node', '-c', name], capture_output=True, text=True)
    os.unlink(name)
    return r.returncode == 0, r.stderr.strip()

def extract_js_blocks(html):
    blocks = []
    for m in re.finditer(r'<script([^>]*)>(.*?)</script>', html, re.S):
        attrs = m.group(1)
        body = m.group(2)
        if 'src=' in attrs.lower() or 'application/ld+json' in attrs:
            continue
        blocks.append((m.start(2), m.end(2), body))
    return blocks

def diagnose(html_path):
    with open(html_path) as f: html = f.read()
    blocks = extract_js_blocks(html)
    all_js = '\n'.join(b[2].strip() for b in blocks)
    ok, err = verify_js(all_js)
    if ok: return 'ok'
    
    # 分类错误
    if 'Invalid or unexpected token' in err:
        return 'newline_in_string'
    if 'Unexpected token' in err:
        if "'}'" in err or "')'" in err:
            return 'iife_balance'
        return 'unexpected_token'
    if 'Unexpected end of input' in err:
        return 'eof'
    if 'Invalid regular expression flags' in err:
        return 'regex_flags'
    if 'missing )' in err:
        return 'missing_paren'
    return f'other: {err[:80]}'

broken = [
    "fancy-text-generator","html-entity-converter","html-meta-refresh-generator",
    "html-table-to-json","html-wysiwyg-editor","http-cache-header-generator",
    "markdown-previewer","markdown-to-pdf-converter","maze-generator",
    "md5-generator","meta-tag-generator","pdf-to-html","properties-to-yaml",
    "quiz-generator","receipt-generator","regex-cheatsheet","shopping-list-generator",
    "sitemap-validator","sql-migration-generator","sql-to-csv",
    "word-search-generator","workout-generator"
]

for tool in broken:
    p = os.path.join(BASE, tool, 'index.html')
    if os.path.exists(p):
        d = diagnose(p)
        print(f"[{tool}] {d}")
    else:
        print(f"[{tool}] MISSING")