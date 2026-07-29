#!/usr/bin/env python3
"""修复未定义CSS变量：给引用了var(--xxx)但没有:root定义的页面补上变量声明"""
import re, glob, os

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

var_map = {
    'card-bg': '#1e293b', 'shadow': '0 1px 3px rgba(0,0,0,.3)',
    'primary-hover': 'rgba(6,182,212,.3)', 'primary-light': 'rgba(6,182,212,.15)',
    'surface': '#1e293b', 'surface2': '#334155', 'text2': '#94a3b8',
    'text-light': '#94a3b8', 'text-muted': '#64748b', 'accent': '#06b6d4',
    'muted': '#64748b', 'sub': '#94a3b8', 'error': '#EF4444', 'danger': '#EF4444',
    'warning': '#F59E0B', 'green': '#10B981', 'red': '#EF4444', 'yellow': '#F59E0B',
    'cyan': '#06b6d4', 'hover': 'rgba(6,182,212,.3)', 'primary2': '#0891b2',
    'bg-card': '#1e293b', 'font-size-3xl': '1.875rem', 'font-size-base': '1rem',
    'font-size-sm': '0.875rem', 'test': '#10B981',
}

fixed = 0
for f in glob.glob(os.path.join(SITE, '*/index.html')) + glob.glob(os.path.join(SITE, 'en/*/index.html')):
    with open(f) as fh:
        c = fh.read()
    
    var_refs = set(re.findall(r'var\(--([^)]+)\)', c))
    if not var_refs:
        continue
    
    all_defined = set()
    for root_m in re.finditer(r':root\s*\{([^}]+)\}', c):
        for vm in re.finditer(r'--([\w-]+)\s*:', root_m.group(1)):
            all_defined.add(vm.group(1))
    for style_m in re.finditer(r'<style[^>]*>(.*?)</style>', c, re.DOTALL):
        for vm in re.finditer(r'--([\w-]+)\s*:', style_m.group(1)):
            all_defined.add(vm.group(1))
    
    undefined = var_refs - all_defined
    if not undefined:
        continue
    
    need_add = {v: var_map.get(v, '#94a3b8') for v in undefined if v in var_map}
    if not need_add:
        continue
    
    new_vars = ''.join(f'--{k}:{v};' for k, v in need_add.items())
    
    if ':root{' in c or ':root {' in c:
        c = re.sub(r'(:root\s*\{)', r'\g<1>' + new_vars, c)
    else:
        c = c.replace('<style>', '<style>:root{' + new_vars + '}', 1)
    
    with open(f, 'w') as fh:
        fh.write(c)
    fixed += 1

print(f"修复: {fixed} 个页面（补全未定义CSS变量）")
