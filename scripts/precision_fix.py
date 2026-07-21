#!/usr/bin/env python3
"""精确修复67个broken工具JS"""
import subprocess, re, os

def check(f):
    with open(f) as fh: c = fh.read()
    scripts = re.findall(r'<script>(.*?)</script>', c, re.DOTALL)
    js = '\n'.join(s.strip() for s in scripts if s.strip() and not (s.strip().startswith('{') and ('@context' in s or '"@type"' in s)))
    if not js: return True, ''
    r = subprocess.run(['node', '-c', '-'], input=js, capture_output=True, text=True, timeout=5)
    return r.returncode == 0, r.stderr.strip()

def fix_file(f, rules):
    """Apply find→replace rules, verify, revert on fail"""
    with open(f) as fh: orig = fh.read()
    content = orig
    for old, new in rules:
        content = content.replace(old, new)
    if content == orig:
        return False
    with open(f, 'w') as fh: fh.write(content)
    ok, _ = check(f)
    if ok:
        return True
    with open(f, 'w') as fh: fh.write(orig)
    return False

results = []

# === 1. 重复变量声明 (6个工具) ===
for tool, var in [
    ('bar-chart-maker', 'chartColors'), ('bar-chart-maker', 'chartBorders'),
    ('bar-chart-maker', 'chartData'),
    ('radar-chart-maker', 'defaultDims'), ('radar-chart-maker', 'defaultColors'),
    ('scatter-plot-maker', 'seriesList'), ('scatter-plot-maker', 'defaultSeries'),
    ('scatter-plot-maker', 'defaultBorders'), ('scatter-plot-maker', 'defaultColors'),
    ('piano-keyboard', 'showKeyLabels'), ('piano-keyboard', 'audioCtx'),
    ('piano-keyboard', 'sustainOn'), ('piano-keyboard', 'isMouseDown'),
]:
    f = f'{tool}/index.html'
    with open(f) as fh: c = fh.read()
    first = True
    modified = False
    for m in list(re.finditer(rf'(?:let|const|var)\s+{re.escape(var)}\s*=', c)):
        if not first:
            c = c[:m.start()] + f'{var} =' + c[m.end():]
            modified = True
        first = False
    if modified:
        with open(f, 'w') as fh: fh.write(c)
        ok, _ = check(f)
        results.append((tool, var, ok))

# === 2. HTML标签在JS字符串中(8个) ===
for tool, tags in [
    ('curl-converter', ['<br>', '<div', '<p>']),
    ('curl-to-python', ['<div', '</div>']),
    ('line-chart-maker', ['</div>']),
    ('pie-chart-maker', ['</div>']),
    ('html-table-of-contents', ['<div', '</div>']),
    ('html-wysiwyg-editor', ['<!DOCTYPE html>']),
    ('sql-to-csv', ['<div', '</div>']),
    ('html-to-docx', ['<div', '</div>']),
]:
    f = f'{tool}/index.html'
    with open(f) as fh: c = fh.read()
    # Wrap whole JS in template literal approach won't work.
    # Just skip - these need JS extraction first, not in-script fixes
    
# === 3. 字符串内未转义引号/特殊字符 ===
fixes_simple = {
    'api-response-mocker': [
        ('"message\":\"请求参数验证失败\",details:[{field:"email",message":"邮箱格式不正确"}', '"message":"请求参数验证失败","details":[{"field":"email","message":"邮箱格式不正确"}'),
    ],
    'daily-planner': [
        ("""onchange=\"toggleTask('' + timeStr + '',""", 'onchange="toggleTask(\\\'' + timeStr + '\\\','),
    ],
    'regex-character-class-generator': [
        ("'3 || '3'", "'3' || '3'"),
    ],
    'yes-no-generator': [
        ("Don't", "Don\\x27t"),
    ],
    'text-diff-checker': [
        ('style=\\"\\"+SS+\\"\\"', 'style=\\"'+SS+'\\"'),
    ],
    'morse-code': [
        ("==='点击转换查看结果'", "==='点击转换查看结果'"),
    ],
    'privacy-policy-generator': [
        ("text+='隐私政策", "text+='隐私政策'"),
    ],
    'terms-generator': [
        ("text='服务条款", "text='服务条款'"),
    ],
}

for tool, rules in fixes_simple.items():
    f = f'{tool}/index.html'
    if os.path.exists(f):
        ok = fix_file(f, rules)
        results.append((tool, 'simple', ok))

# === 4. Python三元表达式 ===
for tool in ['json-to-python']:
    f = f'{tool}/index.html'
    with open(f) as fh: c = fh.read()
    c = re.sub(r'"(\w+)"\s+if\s+(\w+)\s+else\s+"(\w+)"', r'(\2?"\1":"\3")', c)
    with open(f, 'w') as fh: fh.write(c)
    ok, _ = check(f)
    results.append((tool, 'py_ternary', ok))

# === 5. catch语法 ===
for tool in ['morse-code']:
    f = f'{tool}/index.html'
    with open(f) as fh: c = fh.read()
    c = re.sub(r'catch\s*\(?\)?\s*=>\s*\{', 'catch(e){', c)
    with open(f, 'w') as fh: fh.write(c)
    ok, _ = check(f)
    results.append((tool, 'catch', ok))

# === 6. 多余}); → } ===
for tool in ['sitemap-validator']:
    f = f'{tool}/index.html'
    with open(f) as fh: c = fh.read()
    c = c.replace('})();', '}());')
    with open(f, 'w') as fh: fh.write(c)
    ok, _ = check(f)
    results.append((tool, 'iife', ok))

# Print results
ok = [r for r in results if r[2]]
fail = [r for r in results if not r[2]]
print(f'Fixed: {len(ok)}, Failed: {len(fail)}')
for t, why, s in sorted(ok): print(f'  ✅ {t} ({why})')
for t, why, s in sorted(fail): print(f'  ❌ {t} ({why})')
