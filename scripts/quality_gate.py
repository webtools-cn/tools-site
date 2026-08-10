#!/usr/bin/env python3
"""质量门 v2：push 前全站检测（结构/footer位置/FAQ重复/JS语法/中文/meta/字数/首页一致性）
用法: python3 scripts/quality_gate.py [--fix]
退出码: 0=通过 1=有严重问题
"""
import re, os, glob, sys, subprocess, json

FIX = '--fix' in sys.argv
skip = {'index.html', 'en/index.html'}
pages = [p for p in glob.glob('*/index.html') + glob.glob('en/*/index.html') if p not in skip and os.path.isfile(p)]
pages += ['index.html', 'en/index.html']

def visible_text(h):
    s = re.sub(r'<script.*?</script>', '', h, flags=re.S | re.I)
    s = re.sub(r'<style.*?</style>', '', s, flags=re.S | re.I)
    s = re.sub(r'<[^>]+>', ' ', s)
    return re.sub(r'\s+', ' ', s).strip()

def check_js_blocks_batch(codes):
    """批量JS语法检查：一次node调用"""
    if not codes: return []
    tmp = '/tmp/qg_js.js'
    js = "const codes = " + json.dumps(codes) + ";\n"
    js += "const out = [];\nfor (const c of codes) { try { new Function(c); out.push(true); } catch(e) { out.push(false); } }\n"
    js += "process.stdout.write(JSON.stringify(out));"
    open(tmp, 'w').write(js)
    try:
        r = subprocess.run(['node', tmp], capture_output=True, text=True, timeout=180)
        return json.loads(r.stdout)
    except Exception:
        return [False] * len(codes)

issues = {'struct': [], 'footer_pos': [], 'faq_dup': [], 'js_syntax': [], 'cn_in_en': [], 'meta_short': [], 'thin': [], 'dup': [], 'home_num': []}

# 0. 批量JS语法检查
all_js_codes = []
for p in pages:
    try:
        h = open(p, encoding='utf-8', errors='ignore').read()
    except: continue
    for m in re.finditer(r'<script[^>]*>([\s\S]*?)</script>', h, re.S):
        code = m.group(1).strip()
        if code and '"@context"' not in code[:100] and re.search(r'function (calc|calculate|run|generate|convert|process|handle|go|build|start|submit)', code):
            all_js_codes.append((p, code))
print(f"JS块检查: {len(all_js_codes)} 个...", file=sys.stderr)
js_results = check_js_blocks_batch([c for _, c in all_js_codes])
for (p, code), ok in zip(all_js_codes, js_results):
    if not ok:
        issues['js_syntax'].append((p, code[:40]))

# 1-5. 结构/footer/FAQ/EN中文/meta/薄页
for p in pages:
    try:
        h = open(p, encoding='utf-8', errors='ignore').read()
    except: continue
    s = re.sub(r'<script.*?</script>', '', h, flags=re.S | re.I)
    s = re.sub(r'<style.*?</style>', '', s, flags=re.S | re.I)

    # 1. 结构平衡
    for tag in ['div', 'main', 'footer', 'section']:
        o = len(re.findall(r'<' + tag + r'[\s>]', s))
        c = s.count('</' + tag + '>')
        if o != c:
            issues['struct'].append((p, tag, o, c))

    # 2. footer 位置
    fs = s.find('<footer')
    if fs >= 0:
        fe = s.find('</footer>', fs)
        if fe >= 0:
            rest = s[fe+9:]
            visible_tags = re.findall(r'<(h2|h3|p|div class="info-section"|ul|table)[\s>]', rest)
            rest_text = re.sub(r'<[^>]+>', '', rest).strip()
            if len(rest_text) > 50 or len(visible_tags) >= 2:
                issues['footer_pos'].append((p, len(rest_text), visible_tags[:4]))

    # 2b. FAQ 重复
    faq_h2 = re.findall(r'<h2[^>]*>(❓[^<]*)</h2>', s)
    if len(faq_h2) >= 2:
        issues['faq_dup'].append((p, faq_h2))

    # 3. EN中文
    txt = visible_text(h)
    if p.startswith('en/'):
        body = re.sub(r'<a[^>]*>中文</a>', '', s)
        cn = [x for x in re.findall(r'[\u4e00-\u9fff]{2,}', body) if x != '中文']
        if cn:
            issues['cn_in_en'].append((p, cn[:3]))

    # 4. meta
    m = re.search(r'name="description"\s+content="([^"]*)"', h)
    if m and len(m.group(1)) < 50:
        issues['meta_short'].append((p, len(m.group(1))))

    # 5. 薄页
    if '已迁移' not in h and 'http-equiv="refresh"' not in h.lower() and len(txt) < 500:
        issues['thin'].append((p, len(txt)))

# 6. 首页数字一致性
try:
    cn_data = json.load(open('tools-data-cn.json', encoding='utf-8'))
    en_data = json.load(open('tools-data-en.json', encoding='utf-8'))
    real_cn = sum(len(v) for v in cn_data.values())
    real_en = sum(len(v) for v in en_data.values())
    for hp, real in [('index.html', real_cn), ('en/index.html', real_en)]:
        h = open(hp, encoding='utf-8', errors='ignore').read()
        m = re.search(r'id="statTools">(\d+)\+?</span>', h)
        if m:
            shown = int(m.group(1))
            if abs(shown - real) > 50:
                issues['home_num'].append((hp, shown, real))
        m2 = re.search(r'id="statCats">(\d+)</span>', h)
        if m2:
            shown_cats = int(m2.group(1))
            real_cats = len(cn_data) if hp == 'index.html' else len(en_data)
            if shown_cats != real_cats:
                issues['home_num'].append((hp + ' cats', shown_cats, real_cats))
except Exception as e:
    issues['home_num'].append(('json', str(e)))

# 7. 雷同度
templates = [
    '该工具完全在本地运行，您的数据不会上传到服务器，保障隐私安全',
    '该工具完全在浏览器端运行，无需安装任何软件，无需注册账号，打开网页即可使用',
    '所有输入数据仅在本地处理，不会上传到任何服务器，确保您的隐私安全',
    'No installation, no registration, just open and use',
    'All processing happens locally in your browser',
    'All processing is done locally',
]
dup_count = {t: 0 for t in templates}
for p in pages:
    h = open(p, encoding='utf-8', errors='ignore').read()
    t = visible_text(h)
    for tmpl in templates:
        if tmpl in t:
            dup_count[tmpl] += 1

print('=' * 55)
print('质量门 v2 报告')
print('=' * 55)
sections = [
    ('结构不平衡', 'struct'), ('footer位置错', 'footer_pos'), ('FAQ重复', 'faq_dup'),
    ('JS语法失败', 'js_syntax'), ('EN含中文', 'cn_in_en'), ('meta<50', 'meta_short'),
    ('薄页<500', 'thin'), ('首页数字不一致', 'home_num'),
]
total = 0
for label, key in sections:
    v = issues[key]
    total += len(v)
    print(f'{label}: {len(v)}')
    for item in v[:8]:
        print(f'  {item}')
print('雷同模板句:')
for t, n in dup_count.items():
    if n > 10:
        print(f'  [{n}页] {t[:40]}')
total_dup = sum(1 for n in dup_count.values() if n > 10)
print('=' * 55)
print(f'严重问题: {total} 个页面问题 + {total_dup} 类雷同')
sys.exit(1 if total > 0 else 0)
