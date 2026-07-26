#!/usr/bin/env python3
"""
质量闭环检测脚本 v1.0
检测→修复→验证→再检测，循环直到零问题
每次运行输出：问题数、修复数、残留数
"""
import os, re, sys, json

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP = {'scripts','css','js','docs','quality','blog','en','.gsc-data','.git',
        'about','contact','terms','privacy','node_modules'}

def get_tools():
    tools = []
    for d in sorted(os.listdir(SITE)):
        if d in SKIP or d.startswith('.'): continue
        p = os.path.join(SITE, d, 'index.html')
        if os.path.isfile(p): tools.append(d)
    return tools

def get_en_tools():
    tools = []
    en_dir = os.path.join(SITE, 'en')
    for d in sorted(os.listdir(en_dir)):
        p = os.path.join(en_dir, d, 'index.html')
        if os.path.isfile(p): tools.append(d)
    return tools

CN_RE = re.compile(r'[\u4e00-\u9fff]')

# ============ 检测门 ============

def check_seo(path, lang, item):
    """门3: SEO标签完整性"""
    issues = []
    with open(path, 'r', encoding='utf-8', errors='ignore') as f: c = f.read()
    is_noindex = 'noindex' in c
    
    if not is_noindex:
        if 'rel="canonical"' not in c: issues.append('no_canonical')
        if 'og:image' not in c: issues.append('no_og_image')
        if 'twitter:card' not in c: issues.append('no_twitter_card')
        if 'hreflang' not in c: issues.append('no_hreflang')
        if 'meta name="robots"' not in c: issues.append('no_robots')
        if 'adsbygoogle' not in c: issues.append('no_adsense')
        if 'BreadcrumbList' not in c: issues.append('no_breadcrumb')
    
    if 'SoftwareApplication' not in c: issues.append('no_software_app')
    if 'favicon' not in c and 'rel="icon"' not in c: issues.append('no_favicon')
    
    # lang
    lm = re.search(r'lang="([^"]+)"', c)
    if lang == 'cn' and lm and lm.group(1) not in ('zh-CN','zh'):
        issues.append('lang_wrong')
    elif lang == 'en' and lm and lm.group(1) != 'en':
        issues.append('lang_wrong')
    
    # desc
    dm = re.search(r'<meta name="description" content="([^"]*)"', c)
    if not dm: issues.append('no_desc')
    elif not is_noindex:
        dl = len(dm.group(1))
        if dl < 50: issues.append('desc_short')
        elif dl > 160: issues.append('desc_long')
    
    # title
    tm = re.search(r'<title>([^<]+)</title>', c)
    if tm and len(tm.group(1)) > 60 and not is_noindex:
        issues.append('title_long')
    
    return issues

def check_structure(path, lang, item):
    """门4: HTML结构"""
    issues = []
    with open(path, 'r', encoding='utf-8', errors='ignore') as f: c = f.read()
    is_noindex = 'noindex' in c
    
    # h1
    h1c = c.count('<h1')
    if h1c == 0 and not is_noindex: issues.append('no_h1')
    elif h1c > 1: issues.append('multi_h1')
    
    # footer
    if '<footer' not in c and not is_noindex: issues.append('no_footer')
    
    # @media
    if '@media' not in c and not is_noindex: issues.append('no_media')
    
    # head闭合
    if '<head' in c and '</head>' not in c: issues.append('head_unclosed')
    
    # body闭合
    if '<body' in c and '</body>' not in c: issues.append('body_unclosed')
    
    return issues

def check_css(path, lang, item):
    """门5: CSS语法"""
    issues = []
    with open(path, 'r', encoding='utf-8', errors='ignore') as f: c = f.read()
    
    # 双花括号
    for m in re.finditer(r'<style[^>]*>(.*?)</style>', c, re.DOTALL):
        if '{{' in m.group(1):
            issues.append('double_brace_css')
            break
    
    return issues

def check_language(path, lang, item):
    """门6: 语言一致性"""
    issues = []
    with open(path, 'r', encoding='utf-8', errors='ignore') as f: c = f.read()
    
    if lang == 'en':
        # EN页面不应有中文
        if CN_RE.search(c): issues.append('chinese_in_en')
    else:
        # CN页面h1不应是纯英文
        h1m = re.search(r'<h1[^>]*>([^<]+)</h1>', c)
        if h1m and not CN_RE.search(h1m.group(1)):
            # 排除技术术语
            text = h1m.group(1).strip()
            if not re.match(r'^[A-Z0-9\s\-/()+.]+$', text):  # 纯技术名OK
                issues.append('h1_english_in_cn')
    
    return issues

def check_functionality(path, lang, item):
    """门7: 功能完整性"""
    issues = []
    with open(path, 'r', encoding='utf-8', errors='ignore') as f: c = f.read()
    is_noindex = 'noindex' in c
    
    if is_noindex: return issues
    
    has_func = 'function' in c or 'addEventListener' in c
    if not has_func:
        issues.append('empty_shell')
        return issues
    
    btns = len(re.findall(r'<button', c))
    inputs = len(re.findall(r'<input|<textarea|<select', c))
    if btns + inputs < 3:
        issues.append('low_interact')
    
    # 缺复制按钮但有输出区域
    has_output = bool(re.search(r'id="result|class="result|id="output', c))
    if has_output and 'copy' not in c.lower() and '复制' not in c:
        issues.append('no_copy_btn')
    
    return issues

def check_schema(path, lang, item):
    """门8: Schema质量"""
    issues = []
    with open(path, 'r', encoding='utf-8', errors='ignore') as f: c = f.read()
    
    for s in re.findall(r'<script type="application/ld\+json">(.*?)</script>', c, re.DOTALL):
        try: json.loads(s)
        except: issues.append('schema_invalid'); break
    
    return issues

# ============ 自动修复 ============

def auto_fix(path, lang, item, issues):
    """自动修复已知问题，返回(fixed_list, remaining_list)"""
    with open(path, 'r', encoding='utf-8', errors='ignore') as f: c = f.read()
    fixed = []
    remaining = []
    
    cn_url = f'https://free-toolbase.com/{item}/'
    en_url = f'https://free-toolbase.com/en/{item}/'
    OG = 'https://free-toolbase.com/og-image.svg'
    
    for issue in issues:
        if issue == 'double_brace_css':
            for m in re.finditer(r'(<style[^>]*>)(.*?)(</style>)', c, re.DOTALL):
                if '{{' in m.group(2):
                    c = c.replace(m.group(2), m.group(2).replace('{{','{').replace('}}','}'))
                    fixed.append(issue); break
            else: remaining.append(issue)
        
        elif issue == 'head_unclosed':
            # 在第一个<style>前插入</head><body>
            sp = c.find('<style')
            if sp > 0:
                c = c[:sp] + '</head>\n<body>\n' + c[sp:]
                if '</body>' not in c: c = c.rstrip() + '\n</body>\n</html>'
                fixed.append(issue)
            else: remaining.append(issue)
        
        elif issue == 'body_unclosed':
            c = c.rstrip() + '\n</body>\n</html>'
            fixed.append(issue)
        
        elif issue == 'no_og_image' and 'og:image' not in c:
            c = c.replace('</head>', f'<meta property="og:image" content="{OG}">\n</head>')
            fixed.append(issue)
        
        elif issue == 'no_twitter_card' and 'twitter:card' not in c:
            c = c.replace('</head>', '<meta name="twitter:card" content="summary_large_image">\n</head>')
            fixed.append(issue)
        
        elif issue == 'no_canonical' and 'rel="canonical"' not in c:
            url = en_url if lang=='en' else cn_url
            c = c.replace('</head>', f'<link rel="canonical" href="{url}">\n</head>')
            fixed.append(issue)
        
        elif issue == 'no_hreflang' and 'hreflang' not in c:
            hl = f'<link rel="alternate" hreflang="zh" href="{cn_url}">\n<link rel="alternate" hreflang="en" href="{en_url}">\n<link rel="alternate" hreflang="x-default" href="{cn_url if lang=="cn" else en_url}">'
            c = c.replace('</head>', hl + '\n</head>')
            fixed.append(issue)
        
        elif issue == 'no_robots' and 'meta name="robots"' not in c:
            c = c.replace('</head>', '<meta name="robots" content="index, follow">\n</head>')
            fixed.append(issue)
        
        elif issue == 'no_favicon' and 'favicon' not in c and 'rel="icon"' not in c:
            tag = '<link rel="icon" type="image/svg+xml" href="../favicon.svg">' if lang=='en' else '<link rel="icon" type="image/svg+xml" href="favicon.svg">'
            c = c.replace('</head>', tag + '\n</head>')
            fixed.append(issue)
        
        elif issue == 'no_footer' and '<footer' not in c:
            ft = '<footer style="border-top:1px solid rgba(148,163,184,.1);padding:24px 0;margin-top:32px;text-align:center;color:#64748b;font-size:.85rem"><a href="/en/" style="color:#64748b;margin:0 8px">Home</a> <a href="/en/privacy" style="color:#64748b;margin:0 8px">Privacy</a></footer>' if lang=='en' else '<footer style="border-top:1px solid rgba(148,163,184,.1);padding:24px 0;margin-top:32px;text-align:center;color:#64748b;font-size:.85rem"><a href="/" style="color:#64748b;margin:0 8px">首页</a> <a href="/privacy" style="color:#64748b;margin:0 8px">隐私政策</a></footer>'
            c = c.replace('</body>', ft + '\n</body>')
            fixed.append(issue)
        
        elif issue == 'no_media' and '@media' not in c and '</style>' in c:
            c = c.replace('</style>', '@media(max-width:640px){h1{font-size:1.2rem;word-break:break-word}.container{padding:0 12px}.btn{padding:8px 14px;font-size:.85rem}.panel{padding:16px}}\n</style>')
            fixed.append(issue)
        
        elif issue == 'no_h1' and not re.search(r'<h1', c):
            tm = re.search(r'<title>([^<]+?)(?:\s*[-|]\s*Free ToolBase)?</title>', c)
            tn = tm.group(1).strip() if tm else item.replace('-',' ').title()
            if '<main' in c:
                pos = c.find('>', c.find('<main')) + 1
                c = c[:pos] + f'\n<h1>{tn}</h1>' + c[pos:]
            elif '<body' in c:
                pos = c.find('>', c.find('<body')) + 1
                c = c[:pos] + f'\n<h1>{tn}</h1>' + c[pos:]
            fixed.append(issue)
        
        elif issue == 'multi_h1':
            h1s = [m.start() for m in re.finditer(r'<h1', c)]
            for pos in h1s[1:]: c = c[:pos] + '<h2' + c[pos+3:]
            for m in re.finditer(r'</h1>', c):
                pass
            closes = [m.start() for m in re.finditer(r'</h1>', c)]
            for pos in closes[1:]: c = c[:pos] + '</h2>' + c[pos+5:]
            fixed.append(issue)
        
        elif issue == 'desc_short':
            dm = re.search(r'<meta name="description" content="([^"]*)"', c)
            if dm and len(dm.group(1)) < 50:
                desc = dm.group(1)
                nd = desc.rstrip('。.') + ('，免费在线工具，无需注册' if lang=='cn' else '. Free online tool, no signup')
                if len(nd) > 160: nd = nd[:157]+'...'
                c = c.replace(f'content="{desc}"', f'content="{nd}"')
                fixed.append(issue)
            else: remaining.append(issue)
        
        elif issue == 'desc_long':
            dm = re.search(r'<meta name="description" content="([^"]*)"', c)
            if dm and len(dm.group(1)) > 160:
                desc = dm.group(1)
                c = c.replace(f'content="{desc}"', f'content="{desc[:157]}..."')
                fixed.append(issue)
            else: remaining.append(issue)
        
        elif issue == 'title_long':
            tm = re.search(r'<title>([^<]+)</title>', c)
            if tm and len(tm.group(1)) > 60:
                t = tm.group(1)
                nt = t.replace('Free Online ','').replace('Free ','')
                if len(nt)>60 and ' - Free ToolBase' in nt:
                    core = nt.replace(' - Free ToolBase','')
                    mx = 60 - len(' - Free ToolBase')
                    if len(core)>mx: core = core[:mx-1]+'…'
                    nt = core + ' - Free ToolBase'
                if nt!=t and len(nt)<=60:
                    c = c.replace(f'<title>{t}</title>', f'<title>{nt}</title>')
                    fixed.append(issue)
                else: remaining.append(issue)
            else: remaining.append(issue)
        
        elif issue == 'lang_wrong':
            correct = 'en' if lang=='en' else 'zh-CN'
            c = re.sub(r'lang="[^"]+"', f'lang="{correct}"', c, count=1)
            fixed.append(issue)
        
        elif issue == 'schema_invalid':
            for s in re.findall(r'(<script type="application/ld\+json">)(.*?)(</script>)', c, re.DOTALL):
                try: json.loads(s[1])
                except:
                    c = c.replace(s[0]+s[1]+s[2], '')
                    fixed.append(issue); break
        
        else:
            remaining.append(issue)
    
    if fixed:
        with open(path, 'w', encoding='utf-8') as f: f.write(c)
    
    return fixed, remaining

# ============ 主流程 ============

def run():
    all_issues = {}
    all_fixed = {}
    all_remaining = {}
    
    checks = [
        ('seo', check_seo),
        ('structure', check_structure),
        ('css', check_css),
        ('language', check_language),
        ('functionality', check_functionality),
        ('schema', check_schema),
    ]
    
    # CN
    for item in get_tools():
        path = os.path.join(SITE, item, 'index.html')
        issues = []
        for name, fn in checks:
            issues.extend(fn(path, 'cn', item))
        if issues:
            all_issues[f'cn:{item}'] = issues
            fixed, remaining = auto_fix(path, 'cn', item, issues)
            if fixed: all_fixed[f'cn:{item}'] = fixed
            if remaining: all_remaining[f'cn:{item}'] = remaining
    
    # EN
    for item in get_en_tools():
        path = os.path.join(SITE, 'en', item, 'index.html')
        issues = []
        for name, fn in checks:
            issues.extend(fn(path, 'en', item))
        if issues:
            all_issues[f'en:{item}'] = issues
            fixed, remaining = auto_fix(path, 'en', item, issues)
            if fixed: all_fixed[f'en:{item}'] = fixed
            if remaining: all_remaining[f'en:{item}'] = remaining
    
    # 统计
    total_issues = sum(len(v) for v in all_issues.values())
    total_fixed = sum(len(v) for v in all_fixed.values())
    total_remaining = sum(len(v) for v in all_remaining.values())
    
    # 按类型统计残留
    remaining_by_type = {}
    for issues in all_remaining.values():
        for i in issues:
            remaining_by_type[i] = remaining_by_type.get(i, 0) + 1
    
    print(f"扫描: {len(get_tools())} CN + {len(get_en_tools())} EN = {len(get_tools())+len(get_en_tools())} 页")
    print(f"问题: {total_issues}个")
    print(f"修复: {total_fixed}个")
    print(f"残留: {total_remaining}个")
    
    if remaining_by_type:
        print(f"\n残留问题分布:")
        for k, v in sorted(remaining_by_type.items(), key=lambda x:-x[1]):
            print(f"  {k}: {v}")
    
    # 输出JSON供cron读取
    result = {
        'total_issues': total_issues,
        'total_fixed': total_fixed,
        'total_remaining': total_remaining,
        'remaining_by_type': remaining_by_type,
        'remaining_pages': {k: v for k, v in all_remaining.items()},
    }
    
    out_path = os.path.join(SITE, 'quality', 'quality_loop_result.json')
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    return total_remaining

if __name__ == '__main__':
    remaining = run()
    sys.exit(0 if remaining == 0 else 1)
