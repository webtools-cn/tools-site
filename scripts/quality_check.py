#!/usr/bin/env python3
"""
全站质量巡检脚本 - 每次cron运行前执行
检测：JSON完整性、深色字bug、假评分残留、空壳、EN中文、noindex、AdSense覆盖
输出：问题数量和具体文件列表
"""
import glob, json, re, os, sys

os.chdir('/home/chison/tools-site')
ERRORS = []

def err(cat, msg):
    ERRORS.append(f"[{cat}] {msg}")
    print(f"❌ [{cat}] {msg}")

def ok(cat, msg):
    print(f"✅ [{cat}] {msg}")

# 1. JSON vs 实际文件数
cn_json = json.load(open('tools-data-cn.json'))
en_json = json.load(open('tools-data-en.json'))
cn_json_slugs = set(item[3].rstrip('/') for items in cn_json.values() for item in items)
en_json_slugs = set(item[3].replace('/en/','').strip('/') for items in en_json.values() for item in items)
cn_file_slugs = set(f.split('/')[0] for f in glob.glob('*/index.html') if f!='index.html' and not f.startswith('en/'))
en_file_slugs = set(f.split('/')[1] for f in glob.glob('en/*/index.html'))
skip_dirs = {'css','js','scripts','quality','.gsc-data','.github'}
cn_file_slugs -= skip_dirs

cn_missing = cn_file_slugs - cn_json_slugs
en_missing = en_file_slugs - en_json_slugs
if cn_missing:
    err("JSON缺失", f"CN首页缺{len(cn_missing)}个工具(文件有但JSON无)")
else:
    ok("JSON完整性", f"CN: {len(cn_json_slugs)}/{len(cn_file_slugs)}")
if en_missing:
    err("JSON缺失", f"EN首页缺{len(en_missing)}个工具(文件有但JSON无)")
else:
    ok("JSON完整性", f"EN: {len(en_json_slugs)}/{len(en_file_slugs)}")

# 2. 深色字bug
cn_dark = [f.split('/')[0] for f in glob.glob('*/index.html') if f!='index.html' and not f.startswith('en/') and 'color:#1e293b' in open(f,'r',errors='ignore').read()]
en_dark = [f.split('/')[1] for f in glob.glob('en/*/index.html') if 'color:#1e293b' in open(f,'r',errors='ignore').read()]
if cn_dark or en_dark:
    err("深色字bug", f"CN={len(cn_dark)} EN={len(en_dark)} (color:#1e293b在深色背景上不可见)")
else:
    ok("深色字", "0")

# 3. 假评分残留
cn_rw = len([f for f in glob.glob('*/index.html') if f!='index.html' and not f.startswith('en/') and ('rating-widget' in open(f,'r',errors='ignore').read() or 'getConsistentRating' in open(f,'r',errors='ignore').read() or 'aggregateRating' in open(f,'r',errors='ignore').read())])
en_rw = len([f for f in glob.glob('en/*/index.html') if 'rating-widget' in open(f,'r',errors='ignore').read() or 'getConsistentRating' in open(f,'r',errors='ignore').read() or 'aggregateRating' in open(f,'r',errors='ignore').read()])
fake_slot = len([f for f in glob.glob('*/index.html')+glob.glob('en/*/index.html') if 'data-ad-slot="XXXXXXX"' in open(f,'r',errors='ignore').read()])
if cn_rw or en_rw or fake_slot:
    err("假评分", f"CN={cn_rw} EN={en_rw} 假slot={fake_slot}")
else:
    ok("假评分", "0残留")

# 4. AdSense覆盖
cn_ads = len([f for f in glob.glob('*/index.html') if 'ca-pub-5998441792679372' in open(f,'r',errors='ignore').read()])
en_ads = len([f for f in glob.glob('en/*/index.html') if 'ca-pub-5998441792679372' in open(f,'r',errors='ignore').read()])
cn_total = len([f for f in glob.glob('*/index.html') if f!='index.html' and not f.startswith('en/')])
en_total = len(glob.glob('en/*/index.html'))
if cn_ads < cn_total or en_ads < en_total:
    err("AdSense", f"CN={cn_ads}/{cn_total} EN={en_ads}/{en_total}")
else:
    ok("AdSense", f"CN={cn_ads}/{cn_total} EN={en_ads}/{en_total}")

# 5. EN中文残留（排除语言切换链接中的"中文"二字）
cn_char = re.compile(r'[\u4e00-\u9fff]')
en_cn_files = []
for f in glob.glob('en/*/index.html'):
    content = open(f,'r',errors='ignore').read()
    # 排除语言切换链接: <a ...>中文</a>
    content_clean = re.sub(r'<a[^>]*>\s*中文\s*</a>', '', content)
    # 排除lang-switch div: <div class="lang-switch">...中文...</div>
    content_clean = re.sub(r'<div[^>]*class="[^"]*lang-switch[^"]*"[^>]*>.*?</div>', '', content_clean, flags=re.DOTALL)
    if cn_char.search(content_clean):
        en_cn_files.append(f)
en_cn = len(en_cn_files)
if en_cn > 0:
    err("EN中文残留", f"{en_cn}页EN页面含中文(已排除语言切换链接)")
else:
    ok("EN中文", "0")

# 6. noindex
cn_ni = []
for f in glob.glob('*/index.html'):
    if f=='index.html' or f.startswith('en/'): continue
    c = open(f,'r',errors='ignore').read()
    # 排除option/select里的noindex(是工具功能选项，不是页面meta)
    c_clean = re.sub(r'<option[^>]*>.*?</option>', '', c, flags=re.DOTALL)
    c_clean = re.sub(r'<select[^>]*>.*?</select>', '', c_clean, flags=re.DOTALL)
    if 'noindex' in c_clean:
        cn_ni.append(f.split('/')[0])
en_ni = []
for f in glob.glob('en/*/index.html'):
    c = open(f,'r',errors='ignore').read()
    c_clean = re.sub(r'<option[^>]*>.*?</option>', '', c, flags=re.DOTALL)
    c_clean = re.sub(r'<select[^>]*>.*?</select>', '', c_clean, flags=re.DOTALL)
    if 'noindex' in c_clean:
        en_ni.append(f.split('/')[1])
if cn_ni or en_ni:
    err("noindex", f"CN={cn_ni} EN={en_ni}")
else:
    ok("noindex", "0")

# 7. 空壳辅助按钮（只统计函数体仅包含showToast的真正空壳）
cn_empty = 0
empty_pattern = re.compile(r'function\s+\w+\s*\([^)]*\)\s*\{\s*showToast\([\'"][^\'"]*[\'"]\)\s*;\s*\}')
for f in glob.glob('*/index.html'):
    if f=='index.html' or f.startswith('en/'):
        continue
    content = open(f,'r',errors='ignore').read()
    if empty_pattern.search(content):
        cn_empty += 1
if cn_empty > 0:
    err("空壳按钮", f"{cn_empty}页有纯showToast空壳函数(无明显业务逻辑)")
else:
    ok("空壳按钮", "0")

# 汇总
print(f"\n{'='*50}")
print(f"巡检结果: {len(ERRORS)} 个问题")
if ERRORS:
    for e in ERRORS:
        print(f"  {e}")
    sys.exit(1)
else:
    print("  全部通过 ✅")
    sys.exit(0)
