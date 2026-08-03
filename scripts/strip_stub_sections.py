#!/usr/bin/env python3
# Batch remove trailing stub sections that shadow good implementations.
# Strategy: for each CN file, find '=== 重写的函数实现 ===' marker; if EVERY
# post-marker `function NAME(` is also assigned via `window.NAME=function` BEFORE
# the marker, then the post-marker section is a duplicate/stub override -> remove
# from marker line up to (but not including) the closing </script>.
# EN files: marker '=== Implementation ===' with same logic.
import re, os, sys, shutil

CN_MARKERS = ['=== 重写的函数实现 ===', '=== 重写实现 ===']
EN_MARKERS = ['=== Implementation ===']

def find_marker(html, markers):
    for mk in markers:
        i = html.find(mk)
        if i != -1:
            return i
    return -1

def covered_by_window_assigns(pre, post):
    win_assigns = set(re.findall(r'window\.(\w+)\s*=\s*function', pre))
    fn_decls = set(re.findall(r'function\s+(\w+)\s*\(', post))
    return fn_decls, fn_decls <= win_assigns

def strip_stub_section(path, markers, dry=False):
    html = open(path, encoding='utf-8').read()
    mpos = find_marker(html, markers)
    if mpos == -1:
        return ('no-marker', 0)
    # find the line start of the marker comment
    line_start = html.rfind('\n', 0, mpos) + 1
    pre = html[:line_start]
    post = html[line_start:]
    fn_decls, covered = covered_by_window_assigns(pre, post)
    if not covered:
        return ('not-covered', len(fn_decls))
    # find closing script tag after marker
    close = html.find('</script>', mpos)
    if close == -1:
        return ('no-close', len(fn_decls))
    new_html = pre + html[close:]
    if not dry:
        shutil.copy2(path, path + '.bak')
        open(path, 'w', encoding='utf-8').write(new_html)
    return ('stripped', len(fn_decls))

if __name__ == '__main__':
    dry = '--dry' in sys.argv
    targets = [
        ('caddyfile-generator/index.html', CN_MARKERS),
        ('cidr-to-ip-range/index.html', CN_MARKERS),
        ('env-to-json/index.html', CN_MARKERS),
        ('haproxy-config-generator/index.html', CN_MARKERS),
        ('html-table-to-markdown/index.html', CN_MARKERS),
        ('http-cache-header-generator/index.html', CN_MARKERS),
        ('kubernetes-yaml-generator/index.html', CN_MARKERS),
        ('string-case-converter/index.html', CN_MARKERS),
        ('tailwind-spacing-generator/index.html', CN_MARKERS),
        ('typescript-utility-types/index.html', CN_MARKERS),
        ('unicode-range-generator/index.html', CN_MARKERS),
        ('yaml-to-dotenv/index.html', CN_MARKERS),
        ('en/caddyfile-generator/index.html', EN_MARKERS),
        ('en/cidr-to-ip-range/index.html', EN_MARKERS),
        ('en/env-to-json/index.html', EN_MARKERS),
        ('en/haproxy-config-generator/index.html', EN_MARKERS),
        ('en/html-table-to-markdown/index.html', EN_MARKERS),
        ('en/http-cache-header-generator/index.html', EN_MARKERS),
        ('en/kubernetes-yaml-generator/index.html', EN_MARKERS),
        ('en/string-case-converter/index.html', EN_MARKERS),
        ('en/tailwind-spacing-generator/index.html', EN_MARKERS),
        ('en/typescript-utility-types/index.html', EN_MARKERS),
        ('en/unicode-range-generator/index.html', EN_MARKERS),
        ('en/yaml-to-dotenv/index.html', EN_MARKERS),
    ]
    for path, markers in targets:
        if not os.path.isfile(path):
            print(f'{path}: MISSING')
            continue
        status, n = strip_stub_section(path, markers, dry=dry)
        print(f'{path}: {status} ({n} fns)')
