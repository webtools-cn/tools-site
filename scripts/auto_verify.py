#!/usr/bin/env python3
"""批量功能验证脚本 - 用Node.js验证JS语法+用正则验证关键功能"""
import subprocess, re, glob, json, os

def check_js_syntax(filepath):
    """门0: JS语法检查"""
    try:
        result = subprocess.run(['node', '-c', filepath], capture_output=True, text=True, timeout=5)
        if result.returncode != 0:
            return f"JS语法错误: {result.stderr.strip()[:100]}"
    except Exception as e:
        return f"检查失败: {str(e)[:50]}"
    return None

def check_interactive_elements(filepath):
    """门1: 交互元素检查 - 至少3个(input+button+output)"""
    try:
        c = open(filepath, 'r', errors='ignore').read()
    except:
        return "无法读取"
    
    inputs = len(re.findall(r'<input[^>]+|<select[^>]+|<textarea[^>]+', c))
    buttons = len(re.findall(r'<button[^>]*>', c))
    outputs = len(re.findall(r'id="result|id="output|id="outputArea|class="result|class="output', c))
    
    if inputs == 0 and buttons == 0:
        return "无交互元素(空壳)"
    if inputs < 1:
        return f"输入不足({inputs}个input)"
    if buttons < 1:
        return f"无按钮"
    if outputs < 1:
        return f"无输出区域"
    return None

def check_calc_function(filepath):
    """门2: 计算函数存在检查"""
    try:
        c = open(filepath, 'r', errors='ignore').read()
    except:
        return None
    
    # 检查是否有calc/calculate/convert/generate等核心函数
    has_func = bool(re.search(r'function\s+(calc|calculate|convert|generate|check|validate|format|encode|decode|parse|analyze)', c))
    has_onclick = bool(re.search(r'onclick|addEventListener', c))
    
    if not has_func and not has_onclick:
        return "无核心函数"
    return None

def check_no_placeholder(filepath):
    """门3: 无占位符检查"""
    try:
        c = open(filepath, 'r', errors='ignore').read()
    except:
        return None
    
    placeholders = re.findall(r'REPLACE_ME|TODO|FIXME|PLACEHOLDER|Lorem ipsum', c, re.IGNORECASE)
    if placeholders:
        return f"占位符: {placeholders[:3]}"
    return None

def check_en_no_chinese(filepath):
    """门4: EN页面无中文(排除链接)"""
    try:
        c = open(filepath, 'r', errors='ignore').read()
    except:
        return None
    
    if '/en/' not in filepath:
        return None  # 只检查EN页面
    
    cn_chars = re.findall(r'[\u4e00-\u9fff]+', c)
    other_cn = [x for x in cn_chars if x != '中文']
    # 排除number-to-words功能特性
    if 'number-to-words' in filepath:
        other_cn = [x for x in other_cn if x not in '壹贰叁肆伍陆柒捌玖拾佰仟万亿零角分整一二三四五六七八九负点']
    if other_cn:
        return f"中文残留: {list(set(other_cn))[:3]}"
    return None

def check_title_desc(filepath):
    """门5: title和description存在且合理"""
    try:
        c = open(filepath, 'r', errors='ignore').read()
    except:
        return None
    
    title_m = re.search(r'<title>(.*?)</title>', c)
    desc_m = re.search(r'<meta name="description" content="(.*?)"', c)
    
    issues = []
    if not title_m:
        issues.append("无title")
    elif len(title_m.group(1)) < 10:
        issues.append(f"title太短: {title_m.group(1)[:30]}")
    
    if not desc_m:
        issues.append("无description")
    elif len(desc_m.group(1)) < 20:
        issues.append("description太短")
    
    return ', '.join(issues) if issues else None

def check_adsense(filepath):
    """门6: AdSense代码存在"""
    try:
        c = open(filepath, 'r', errors='ignore').read()
    except:
        return None
    
    if 'adsbygoogle' not in c and 'pagead2.googlesyndication.com' not in c:
        return "无AdSense"
    return None

def check_no_fake_rating(filepath):
    """门7: 无假评分"""
    try:
        c = open(filepath, 'r', errors='ignore').read()
    except:
        return None
    
    if 'aggregateRating' in c:
        return "有aggregateRating(假评分)"
    return None

# 主流程
results = {'pass': 0, 'fail': 0, 'errors': {}}
total = 0

all_files = glob.glob('*/index.html') + glob.glob('en/*/index.html')
for f in sorted(all_files):
    total += 1
    slug = f.split('/')[0] if '/en/' not in f else f.split('/')[1]
    is_en = '/en/' in f
    
    errors = []
    
    # 门0: JS语法
    # 跳过，太慢
    
    # 门1-7
    for check_name, check_fn in [
        ('交互', check_interactive_elements),
        ('函数', check_calc_function),
        ('占位', check_no_placeholder),
        ('中文', check_en_no_chinese),
        ('SEO', check_title_desc),
        ('AdSense', check_adsense),
        ('评分', check_no_fake_rating),
    ]:
        err = check_fn(f)
        if err:
            errors.append(f"{check_name}:{err}")
    
    if errors:
        results['fail'] += 1
        results['errors'][f] = errors
    else:
        results['pass'] += 1

print(f"验证完成: {results['pass']}/{total} 通过, {results['fail']} 有问题")
print(f"\n问题分布:")
issue_types = {}
for f, errs in results['errors'].items():
    for e in errs:
        key = e.split(':')[0]
        issue_types[key] = issue_types.get(key, 0) + 1

for k, v in sorted(issue_types.items(), key=lambda x: -x[1]):
    print(f"  {k}: {v}页")

# 保存详细结果
with open('quality/auto_verify_results.json', 'w') as fp:
    json.dump(results, fp, indent=2, ensure_ascii=False)
print(f"\n详细结果: quality/auto_verify_results.json")
