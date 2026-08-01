#!/usr/bin/env python3
"""
全站页面深度验证器 v1.0
模拟用户视角，逐页检查所有可见问题
输出：完整问题清单，按严重度排序
"""
import glob, re, json, os
from collections import defaultdict

os.chdir('/home/chison/tools-site')

cn_char = re.compile(r'[\u4e00-\u9fff]')

# ===== 检查函数 =====

def check_page(f, content):
    """对单个页面做全量检查，返回问题列表"""
    issues = []
    slug = f.replace('/index.html','').replace('index.html','(首页)')
    is_en = f.startswith('en/')
    is_home = slug in ['(首页)', 'en/(首页)']
    is_special = slug.replace('en/','') in ['privacy','privacy-policy','terms','terms-of-service','about','contact']
    
    # ===== 1. 功能层：页面能不能用 =====
    
    # 1.1 空壳函数
    if "showToast('功能已触发')" in content:
        issues.append(('L1-CRITICAL', 'empty_fn', "有空壳函数showToast('功能已触发')"))
    
    # 1.2 非工具页有Try It按钮
    if is_special and ('Try It' in content or 'tryIt' in content):
        issues.append(('L1-CRITICAL', 'wrong_template', f'非工具页({slug.replace("en/","")})用了工具模板'))
    
    # 1.3 文件上传按钮中文残留(EN页)
    if is_en and '未选择任何文件' in content:
        issues.append(('L1-HIGH', 'cn_in_ui', 'EN页面文件按钮显示"未选择任何文件"'))
    
    # 1.4 功能受限提示
    if 'cannot be implemented in the browser' in content or 'requires a server backend' in content:
        issues.append(('L1-MEDIUM', 'fake_tool', '工具声称无法在浏览器实现，是演示页面'))
    
    # ===== 2. 视觉层：用户看到什么 =====
    
    # 2.1 深色字
    if 'color:#1e293b' in content:
        issues.append(('L2-HIGH', 'dark_text', '深色背景上有深色文字#1e293b'))
    
    # 2.2 假评分
    if re.search(r'<span[^>]*>★[★½]*</span>\s*<span[^>]*>\d[\.\d]*</span>\s*<span[^>]*>\(\d+\)</span>', content):
        issues.append(('L2-CRITICAL', 'fake_rating', '有虚假评分widget'))
    
    # 2.3 底部乱码
    if 'Localprocess' in content or 'i.e.whenResult' in content or 'DatanotUploadserver' in content:
        issues.append(('L2-HIGH', 'broken_text', '底部有机翻乱码'))
    
    # 2.4 "AllToolsFreeusing"等机翻
    if 'AllToolsFreeusing' in content or 'Pure FrontendLocalprocess' in content:
        issues.append(('L2-HIGH', 'broken_text', '有机翻拼接文字'))
    
    # ===== 3. 语言层：EN页面语言纯度 =====
    
    if is_en and not is_home:
        # 3.1 提取所有可见文本中的中文（排除script/style/option）
        visible_lines = []
        in_script = False
        in_style = False
        for line in content.split('\n'):
            if '<script' in line and 'application/ld+json' not in line: in_script = True
            if '</script>' in line: in_script = False
            if '<style' in line: in_style = True
            if '</style>' in line: in_style = False
            if in_script or in_style: continue
            # 提取可见文本
            text = re.sub(r'<[^>]+>', ' ', line).strip()
            if not text: continue
            if not cn_char.search(text): continue
            # 排除"中文"链接
            if text.strip() == '中文': continue
            visible_lines.append(text)
        
        if visible_lines:
            # 分类：纯中文 vs 中英混合
            pure_cn_lines = []
            mixed_lines = []
            for text in visible_lines:
                has_en = bool(re.search(r'[a-zA-Z]{2,}', text))
                if has_en:
                    mixed_lines.append(text[:80])
                else:
                    pure_cn_lines.append(text[:80])
            
            if pure_cn_lines:
                # Filter false positives: if all CN text is just isolated "中文" (lang switch link residue)
                real_pure_cn = []
                for t in pure_cn_lines:
                    cn_only = re.sub(r'[^\u4e00-\u9fff]', '', t)
                    # Skip if it's just "中文" repeated (lang switch residue)
                    if re.match(r'^中文+$', cn_only):
                        continue
                    if len(cn_only) > 1:
                        real_pure_cn.append(t)
                if real_pure_cn:
                    issues.append(('L3-CRITICAL', 'en_pure_cn', f'EN页面有{len(real_pure_cn)}行纯中文'))
            if mixed_lines:
                issues.append(('L3-HIGH', 'en_mixed', f'EN页面有{len(mixed_lines)}行中英混合'))
    
    # ===== 4. SEO层：搜索引擎看到什么 =====
    
    # 4.1 缺AdSense
    if not is_home and 'ca-pub-5998441792679372' not in content:
        issues.append(('L4-MEDIUM', 'no_adsense', '缺少AdSense代码'))
    
    # 4.2 假slot
    if 'data-ad-slot="XXXXXXX"' in content:
        issues.append(('L4-CRITICAL', 'fake_slot', '有假ad-slot'))
    
    # 4.3 aggregateRating
    if 'aggregateRating' in content:
        issues.append(('L4-CRITICAL', 'aggregateRating', '有假aggregateRating'))
    
    # 4.4 rating-widget
    if 'rating-widget' in content or 'getConsistentRating' in content:
        issues.append(('L4-CRITICAL', 'rating_widget', '有rating-widget代码'))
    
    # 4.5 noindex
    c_clean = re.sub(r'<option[^>]*>.*?</option>', '', content, flags=re.DOTALL)
    if 'noindex' in c_clean and not is_home:
        issues.append(('L4-CRITICAL', 'noindex', '页面有noindex标签'))
    
    # 4.6 REPLACE_ME链接
    if 'REPLACE_ME' in content:
        issues.append(('L4-HIGH', 'broken_link', '有REPLACE_ME占位链接'))
    
    # 4.7 语言切换链接文字
    if is_en:
        # EN页面的CN链接应该写"中文"
        if re.search(r'<a[^>]*href="[^"]*"[^>]*>intext</a>', content):
            issues.append(('L4-HIGH', 'broken_lang_link', '语言切换链接显示"intext"而非"中文"'))
        if re.search(r'<a[^>]*href="[^"]*"[^>]*>Chinese</a>', content):
            issues.append(('L3-LOW', 'lang_link_style', '语言切换用"Chinese"而非"中文"'))
    
    # 4.8 Schema中中文(EN页)
    if is_en:
        schema_match = re.search(r'<script type="application/ld\+json">(.*?)</script>', content, re.DOTALL)
        if schema_match and cn_char.search(schema_match.group(1)):
            issues.append(('L4-MEDIUM', 'schema_cn', 'Schema中有中文'))
    
    # ===== 5. 结构层：页面完整性 =====
    
    # 5.1 缺footer
    if not is_home and '<footer' not in content and 'contentinfo' not in content:
        issues.append(('L5-LOW', 'no_footer', '页面缺少footer'))
    
    # 5.2 缺Schema
    if not is_home and not is_special and 'application/ld+json' not in content:
        issues.append(('L5-LOW', 'no_schema', '工具页缺少Schema'))
    
    # 5.3 相关工具推荐不相关
    if not is_home:
        related = re.findall(r'<a[^>]*href="[^"]*"[^>]*>([^<]*(?:Generator|Calculator|Converter|Editor|Checker|Encoder|Decoder|Formatter|Maker|Builder|Creator)[^<]*)</a>', content, re.I)
        # 检查是否都是通用推荐(Age Calculator, Body Shape, Complaint Letter等)
        generic = ['Age Calculator', 'Body Shape Calculator', 'Complaint Letter', 
                   'Acronym Generator', 'Add Watermark', 'Audio Crossfade',
                   'Hash Generator', 'Base64 Encoder', 'AES Encrypt', 'UUID Generator']
        if related and all(any(g in r for g in generic) for r in related):
            issues.append(('L5-MEDIUM', 'generic_related', '相关工具推荐全是通用占位，与当前工具无关'))
    
    return issues


# ===== 主流程 =====
all_files = glob.glob('*/index.html') + glob.glob('en/*/index.html')
print(f'扫描全站: {len(all_files)} 页\n')

all_issues = defaultdict(list)  # issue_type -> [slug, ...]
page_issues = {}  # slug -> [issues]

for f in all_files:
    c = open(f, 'r', errors='ignore').read()
    slug = f.replace('/index.html','').replace('index.html','(首页)')
    issues = check_page(f, c)
    if issues:
        page_issues[slug] = issues
        for level, itype, desc in issues:
            all_issues[itype].append(slug)

# ===== 输出 =====
print('=' * 60)
print('全站深度验证报告')
print('=' * 60)
print(f'总页面: {len(all_files)}')
print(f'有问题页面: {len(page_issues)}')
print(f'干净页面: {len(all_files) - len(page_issues)} ({(len(all_files)-len(page_issues))/len(all_files)*100:.1f}%)')
print()

# 按严重度排序
severity_order = {'CRITICAL': 0, 'HIGH': 1, 'MEDIUM': 2, 'LOW': 3}
sorted_issues = sorted(all_issues.items(), key=lambda x: severity_order.get(x[0].split('-')[-1] if '-' in x[0] else 'LOW', 9))

print('问题清单（按严重度）:')
print('-' * 60)
for itype, pages in sorted_issues:
    # 找到对应的level
    level = 'UNKNOWN'
    for slug, issues in page_issues.items():
        for l, t, d in issues:
            if t == itype:
                level = l
                break
        if level != 'UNKNOWN': break
    
    icon = {'CRITICAL':'🔴','HIGH':'🟠','MEDIUM':'🟡','LOW':'🟢'}.get(level.split('-')[-1], '⚪')
    print(f'{icon} [{level}] {itype}: {len(pages)} 页')
    if len(pages) <= 10:
        for p in pages:
            print(f'    - {p}')

print()
print('=' * 60)
print('问题总数统计:')
total = sum(len(v) for v in all_issues.values())
print(f'  总问题: {total}')
print(f'  涉及页面: {len(page_issues)}')
print(f'  问题类型: {len(all_issues)}')

# 保存详细报告
report = {
    'total_pages': len(all_files),
    'problem_pages': len(page_issues),
    'clean_pages': len(all_files) - len(page_issues),
    'issues': {itype: len(pages) for itype, pages in all_issues.items()},
    'pages': {slug: [(l,t,d) for l,t,d in issues] for slug, issues in page_issues.items()}
}
with open('quality/deep_audit_report.json', 'w') as f:
    json.dump(report, f, ensure_ascii=False, indent=2)
print(f'\n详细报告已保存: quality/deep_audit_report.json')
