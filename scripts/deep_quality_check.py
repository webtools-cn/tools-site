#!/usr/bin/env python3
"""全站深度质检 - 覆盖SEO+功能+视觉，不只是语法检查"""
import os, re, sys, subprocess, json
from datetime import datetime

ERRORS = []
WARNINGS = []
OKS = []

def err(cat, msg): ERRORS.append(f"[CRITICAL] {cat}: {msg}")
def warn(cat, msg): WARNINGS.append(f"[WARN] {cat}: {msg}")
def ok(cat, msg): OKS.append(f"[OK] {cat}: {msg}")

# ===== 1. Meta Description 检查 =====
short_desc_cn = 0
short_desc_en = 0
good_desc_cn = 0
good_desc_en = 0
no_desc = 0

for d in sorted(os.listdir('.')):
    p = os.path.join(d, 'index.html')
    if not os.path.isfile(p) or d == 'en': continue
    c = open(p, 'r', errors='ignore').read()
    m = re.search(r'<meta name="description" content="([^"]*)"', c)
    if not m:
        no_desc += 1
    else:
        l = len(m.group(1))
        if l < 100:
            short_desc_cn += 1
        elif l <= 160:
            good_desc_cn += 1

for d in sorted(os.listdir('en')):
    p = os.path.join('en', d, 'index.html')
    if not os.path.isfile(p): continue
    c = open(p, 'r', errors='ignore').read()
    m = re.search(r'<meta name="description" content="([^"]*)"', c)
    if not m:
        no_desc += 1
    else:
        l = len(m.group(1))
        if l < 100:
            short_desc_en += 1
        elif l <= 160:
            good_desc_en += 1

if short_desc_cn > 0 or short_desc_en > 0:
    err("Meta Description", f"CN {short_desc_cn}页偏短(<100字符), EN {short_desc_en}页偏短. 合格: CN {good_desc_cn}, EN {good_desc_en}")
else:
    ok("Meta Description", f"CN {good_desc_cn}页合格, EN {good_desc_en}页合格")

# ===== 2. 浅色背景检查 =====
light_bg = 0
for d in sorted(os.listdir('.')):
    p = os.path.join(d, 'index.html')
    if not os.path.isfile(p) or d == 'en': continue
    c = open(p, 'r', errors='ignore').read()
    style_m = re.search(r'<style>(.*?)</style>', c, re.DOTALL)
    if not style_m: continue
    style = style_m.group(1)
    # 去除 @media print 块（打印时白底是正常的）
    style_no_print = re.sub(r'@media\s+print\s*\{.*?\}', '', style, flags=re.DOTALL)
    # 只检查 body 或 html 选择器的背景色
    if re.search(r'(?:^|\})(?![^{]*@media\s+print)\s*(?:body|html)\s*\{[^}]*background[^:]*:\s*#(fff|ffffff|f8f9fa|fafafa|f5f5f5|eee|eeeeee)\b', style_no_print, re.I):
        light_bg += 1

if light_bg > 0:
    err("浅色背景", f"{light_bg}个CN页面有浅色背景(#fff等), 必须改为#0f172a")
else:
    ok("浅色背景", "0")

# ===== 3. 空壳工具检查 =====
stub_count = 0
stub_list = []
for d in sorted(os.listdir('.')):
    p = os.path.join(d, 'index.html')
    if not os.path.isfile(p) or d == 'en': continue
    c = open(p, 'r', errors='ignore').read()
    if 'Generated at ' in c and len(c) < 15000:
        stub_count += 1
        if len(stub_list) < 10:
            stub_list.append(d)

if stub_count > 0:
    err("空壳工具", f"{stub_count}个工具是stub(只输出时间戳): {', '.join(stub_list)}{'...' if stub_count > 10 else ''}")
else:
    ok("空壳工具", "0")

# ===== 4. EN页面含中文 =====
en_chinese = 0
for d in sorted(os.listdir('en')):
    p = os.path.join('en', d, 'index.html')
    if not os.path.isfile(p): continue
    c = open(p, 'r', errors='ignore').read()
    visible = re.sub(r'<script[^>]*>.*?</script>', '', c, flags=re.DOTALL)
    if re.search(r'[\u4e00-\u9fff]', visible):
        en_chinese += 1

if en_chinese > 0:
    warn("EN中文", f"{en_chinese}个EN页面含中文字符")
else:
    ok("EN中文", "0")

# ===== 5. Robots标签检查 =====
no_robots = 0
has_noindex = 0
for d in sorted(os.listdir('.')):
    p = os.path.join(d, 'index.html')
    if not os.path.isfile(p) or d == 'en': continue
    c = open(p, 'r', errors='ignore').read()
    if 'noindex' in c.lower():
        has_noindex += 1
    elif '<meta name="robots"' not in c:
        no_robots += 1

if no_robots > 0:
    warn("Robots标签", f"{no_robots}个CN页面缺robots标签")
else:
    ok("Robots标签", f"0缺, {has_noindex}个noindex")

# ===== 6. GA覆盖检查 =====
cn_no_ga = 0
en_no_ga = 0
for d in sorted(os.listdir('.')):
    p = os.path.join(d, 'index.html')
    if not os.path.isfile(p) or d == 'en': continue
    if 'googletagmanager' not in open(p,'r',errors='ignore').read():
        cn_no_ga += 1

for d in sorted(os.listdir('en')):
    p = os.path.join('en', d, 'index.html')
    if not os.path.isfile(p): continue
    if 'googletagmanager' not in open(p,'r',errors='ignore').read():
        en_no_ga += 1

if cn_no_ga > 0 or en_no_ga > 0:
    err("GA覆盖", f"CN {cn_no_ga}页缺GA, EN {en_no_ga}页缺GA")
else:
    ok("GA覆盖", "全站覆盖")

# ===== 7. 假评分检查 =====
fake_rating = 0
for d in sorted(os.listdir('.')):
    p = os.path.join(d, 'index.html')
    if not os.path.isfile(p) or d == 'en': continue
    if 'aggregateRating' in open(p,'r',errors='ignore').read():
        fake_rating += 1

if fake_rating > 0:
    err("假评分", f"{fake_rating}个页面有aggregateRating(会被Google降权)")
else:
    ok("假评分", "0")

# ===== 8. Title中英混杂检查(辅助页面) =====
bad_title = []
for page in ['privacy', 'terms', 'about', 'contact']:
    p = f'{page}/index.html'
    if not os.path.isfile(p): continue
    c = open(p, 'r', errors='ignore').read()
    m = re.search(r'<title>([^<]+)</title>', c)
    if m:
        t = m.group(1)
        has_cn = bool(re.search(r'[\u4e00-\u9fff]', t))
        has_en_word = bool(re.search(r'[A-Z][a-z]{2,}', t))
        if has_cn and has_en_word and 'Free ToolBase' not in t:
            bad_title.append(f'{page}: {t}')

if bad_title:
    err("Title混杂", f"辅助页面title中英混杂: {bad_title}")
else:
    ok("Title混杂", "0")

# ===== 9. Footer完整性检查(抽样) =====
bad_footer = 0
sampled = 0
for d in sorted(os.listdir('.')):
    p = os.path.join(d, 'index.html')
    if not os.path.isfile(p) or d == 'en': continue
    c = open(p, 'r', errors='ignore').read()
    # Check if footer has at least 4 links (home + privacy + terms + about)
    footer_m = re.search(r'<footer[^>]*>(.*?)</footer>', c, re.DOTALL)
    if not footer_m:
        # Check contentinfo role
        footer_m = re.search(r'role="contentinfo"[^>]*>(.*?)</(?:div|footer|section)', c, re.DOTALL)
    if footer_m:
        links = re.findall(r'<a[^>]*>', footer_m.group(1))
        if len(links) < 4:
            bad_footer += 1
            if bad_footer <= 5:
                print(f"  残缺footer: {d} (只有{len(links)}个链接)")
    sampled += 1
    if sampled >= 100: break  # Sample 100 pages

if bad_footer > 0:
    warn("Footer残缺", f"抽样100页中{bad_footer}页footer链接<4个(缺首页/隐私/条款/关于等)")
else:
    ok("Footer残缺", f"抽样{sampled}页均OK")

# ===== 10. 相关推荐相关性检查(抽样) =====
bad_related = 0
related_sampled = 0
for d in sorted(os.listdir('.')):
    p = os.path.join(d, 'index.html')
    if not os.path.isfile(p) or d == 'en': continue
    c = open(p, 'r', errors='ignore').read()
    # Find related tools section
    related_m = re.search(r'相关工具推荐.*?</div>', c, re.DOTALL)
    if not related_m: continue
    related_text = related_m.group(0)
    # Check for generic/placeholder recommendations
    # If related tools contain words completely unrelated to the tool category
    # Simple heuristic: check if "年龄计算器" appears in non-age tools, etc.
    generic_recs = ['年龄计算器', '体型计算器', '投诉信生成器', 'Age Calculator', 'Body Shape Calculator']
    for gr in generic_recs:
        if gr in related_text:
            bad_related += 1
            if bad_related <= 5:
                print(f"  不相关推荐: {d} 包含'{gr}'")
            break
    related_sampled += 1
    if related_sampled >= 100: break

if bad_related > 0:
    warn("相关推荐不相关", f"抽样100页中{bad_related}页有通用占位推荐(年龄/体型/投诉信等)")
else:
    ok("相关推荐", f"抽样{related_sampled}页均相关")

# ===== 汇总 =====
print(f"\n{'='*60}")
print(f"深度质检报告 {datetime.now().strftime('%Y-%m-%d %H:%M')}")
print(f"{'='*60}")
print(f"\n🔴 CRITICAL ({len(ERRORS)}):")
for e in ERRORS: print(f"  {e}")
print(f"\n🟡 WARN ({len(WARNINGS)}):")
for w in WARNINGS: print(f"  {w}")
print(f"\n🟢 OK ({len(OKS)}):")
for o in OKS: print(f"  {o}")
print(f"\n{'='*60}")
print(f"总问题: {len(ERRORS)} CRITICAL + {len(WARNINGS)} WARN")
if ERRORS:
    sys.exit(1)
else:
    print("全部通过 ✅")
    sys.exit(0)
