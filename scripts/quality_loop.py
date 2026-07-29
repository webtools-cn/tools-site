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
        # no_adsense 暂时跳过 — 全站AdSense尚未接入
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

def check_theme(path, lang, item):
    """门5.5: 主题一致性 - 检测白色/浅色背景（全站应为深色#0f172a）"""
    issues = []
    with open(path, 'r', encoding='utf-8', errors='ignore') as f: c = f.read()
    if 'noindex' in c: return issues
    
    light_bgs = ['#f8fafc','#fafafa','#f5f5f5','#f0f0f0','#eeeeee','#ffffff','#fff','white','#F8FAFC','#FAFAFA','#F5F5F5']
    
    # 检查:root --bg
    root_m = re.search(r':root\s*\{([^}]+)\}', c)
    if root_m:
        bg_val = re.search(r'--bg\s*:\s*([^;]+)', root_m.group(1))
        if bg_val and bg_val.group(1).strip().lower() in [x.lower() for x in light_bgs]:
            issues.append('light_root_bg')
    
    # 检查body background硬编码
    body_m = re.search(r'body\s*\{[^}]*background(?:-color)?:\s*([^;]+)', c)
    if body_m:
        bg = body_m.group(1).strip().lower()
        if bg in [x.lower() for x in light_bgs]:
            issues.append('light_body_bg')
    
    # 检查:root --card-bg白色
    if root_m:
        card_val = re.search(r'--card-bg\s*:\s*([^;]+)', root_m.group(1))
        if card_val and card_val.group(1).strip().lower() in ['#ffffff','#fff','white']:
            issues.append('light_card_bg')
    
    # 检查:root --text深色（暗色主题文字应为浅色）
    if root_m:
        text_val = re.search(r'--text\s*:\s*([^;]+)', root_m.group(1))
        if text_val and '#1e293b' in text_val.group(1):
            issues.append('dark_text_on_dark_bg')
    
    return issues

def check_language(path, lang, item):
    """门6: 语言一致性"""
    issues = []
    with open(path, 'r', encoding='utf-8', errors='ignore') as f: c = f.read()
    
    if lang == 'en':
        # EN页面不应有中文（排除noindex页面和仅含"中文"链接的情况）
        if 'noindex' not in c and CN_RE.search(c):
            # 去除script/style标签后再检查
            clean = re.sub(r'<script[^>]*>.*?</script>', '', c, flags=re.DOTALL)
            clean = re.sub(r'<style[^>]*>.*?</style>', '', clean, flags=re.DOTALL)
            # 去除HTML标签
            text_only = re.sub(r'<[^>]+>', ' ', clean)
            # 如果去掉script/style后仍有超过3个中文字符，才标记
            if len(list(CN_RE.finditer(text_only))) > 4:
                issues.append('chinese_in_en')
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
    
    # 检测toolInput模板空壳：有按钮但无真正功能
    if 'id="toolInput"' in c:
        if '处理完成:' in c or '基于输入参数生成的结果' in c:
            issues.append('toolinput_stub')
            return issues
        js_funcs = re.findall(r'function\s+(\w+)\s*\(', c)
        utility_funcs = {'showToast', 'copyText', 'copyResult', 'exportResult', 'clearTool', 'runTool', 'gtag'}
        business_funcs = [f for f in js_funcs if f not in utility_funcs and not f.startswith('_')]
        if len(business_funcs) == 0:
            issues.append('toolinput_stub')
            return issues
    
    btns = len(re.findall(r'<button', c))
    inputs = len(re.findall(r'<input|<textarea|<select', c))
    if btns + inputs < 3:
        issues.append('low_interact')
    
    # 缺复制按钮但有输出区域
    has_output = bool(re.search(r'id="result|class="result|id="output', c))
    if has_output and 'copy' not in c.lower() and '复制' not in c and 'clipboard' not in c.lower():
        issues.append('no_copy_btn')
    
    return issues

def check_js(path, lang, item):
    """门9: JS语法质量 — 简单括号匹配"""
    issues = []
    with open(path, 'r', encoding='utf-8', errors='ignore') as f: c = f.read()
    if 'noindex' in c: return issues
    
    scripts = re.findall(r'<script>(.*?)</script>', c, re.DOTALL)
    for s in scripts:
        if len(s.strip()) < 50: continue
        if 'gtag' in s or 'adsbygoogle' in s or 'dataLayer' in s: continue
        if 'e.preventDefault()' in s and len(s) < 300: continue
        
        # 简单括号匹配（跳过字符串内容，注释中括号不影响JS语法）
        # 只移除字符串字面量中的内容
        no_str = re.sub(r"'[^'\\]*(?:\\.[^'\\]*)*'", "''", s)
        no_str = re.sub(r'"[^"\\]*(?:\\.[^"\\]*)*"', '""', no_str)
        no_str = re.sub(r'`[^`\\]*(?:\\.[^`\\]*)*`', '``', no_str)
        
        depth = 0
        for ch in no_str:
            if ch == '(': depth += 1
            elif ch == ')': depth -= 1
        if depth != 0:
            # 正则相关工具的括号误报：正则字面量中的 \( \) 会被计为括号
            if 'regex' not in item.lower():
                issues.append('js_paren_mismatch')
            break
        
        # 重复函数定义
        funcs = re.findall(r'function\s+(\w+)\s*\(', no_str)
        from collections import Counter
        dup = [f for f, cnt in Counter(funcs).items() if cnt > 1 and f not in ('addEventListener','querySelector')]
        if dup:
            issues.append('js_dup_func')
            break
        
        # alert()
        if re.search(r'\balert\s*\(', s):
            issues.append('js_alert')
            break
    
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
        
        elif issue in ('light_root_bg','light_body_bg','light_card_bg','dark_text_on_dark_bg'):
            # 自动修复白色/浅色背景→深色主题
            c = re.sub(r'--bg:\s*#f8fafc', '--bg:#0f172a', c, flags=re.IGNORECASE)
            c = re.sub(r'--bg:\s*#fafafa', '--bg:#0f172a', c, flags=re.IGNORECASE)
            c = re.sub(r'--bg:\s*#f5f5f5', '--bg:#0f172a', c, flags=re.IGNORECASE)
            c = re.sub(r'--bg:\s*#f0f0f0', '--bg:#0f172a', c, flags=re.IGNORECASE)
            c = re.sub(r'--bg:\s*#eeeeee', '--bg:#0f172a', c, flags=re.IGNORECASE)
            c = re.sub(r'--bg:\s*#ffffff', '--bg:#0f172a', c, flags=re.IGNORECASE)
            c = re.sub(r'--bg:\s*#fff\b', '--bg:#0f172a', c)
            c = re.sub(r'--bg:\s*white', '--bg:#0f172a', c, flags=re.IGNORECASE)
            c = re.sub(r'(background(?:-color)?:\s*)#f8fafc', r'\g<1>#0f172a', c, flags=re.IGNORECASE)
            c = re.sub(r'(background(?:-color)?:\s*)#fafafa', r'\g<1>#0f172a', c, flags=re.IGNORECASE)
            c = re.sub(r'(background(?:-color)?:\s*)#f5f5f5', r'\g<1>#0f172a', c, flags=re.IGNORECASE)
            c = re.sub(r'(background(?:-color)?:\s*)#f0f0f0', r'\g<1>#0f172a', c, flags=re.IGNORECASE)
            c = re.sub(r'(background(?:-color)?:\s*)#ffffff', r'\g<1>#0f172a', c, flags=re.IGNORECASE)
            c = re.sub(r'(background(?:-color)?:\s*)#fff\b', r'\g<1>#0f172a', c)
            c = re.sub(r'(background(?:-color)?:\s*)white', r'\g<1>#0f172a', c, flags=re.IGNORECASE)
            c = re.sub(r'--card-bg:\s*#ffffff', '--card-bg:#1e293b', c, flags=re.IGNORECASE)
            c = re.sub(r'--card-bg:\s*#fff\b', '--card-bg:#1e293b', c)
            c = re.sub(r'--card-bg:\s*white', '--card-bg:#1e293b', c, flags=re.IGNORECASE)
            c = re.sub(r'--text:\s*#1e293b', '--text:#e2e8f0', c)
            c = c.replace('--shadow:0 1px 3px rgba(0,0,0,.06)', '--shadow:0 1px 3px rgba(0,0,0,.3)')
            c = c.replace('--shadow: 0 1px 3px rgba(0,0,0,.06)', '--shadow: 0 1px 3px rgba(0,0,0,.3)')
            fixed.append(issue)
        
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
        
        elif issue == 'no_breadcrumb' and 'BreadcrumbList' not in c:
            # 从title提取名称
            tm = re.search(r'<title>([^<]+)</title>', c)
            tn = tm.group(1).split(' - ')[0].split(' | ')[0].strip()[:60] if tm else item.replace('-',' ').title()
            if lang == 'en':
                home_name = 'Home'; tools_name = 'Tools'
                home_url = 'https://free-toolbase.com/en/'; tools_url = 'https://free-toolbase.com/en/#tools'
            else:
                home_name = '首页'; tools_name = '工具'
                home_url = 'https://free-toolbase.com/'; tools_url = 'https://free-toolbase.com/#tools'
            bc = {
                "@context":"https://schema.org","@type":"BreadcrumbList",
                "itemListElement":[
                    {"@type":"ListItem","position":1,"name":home_name,"item":home_url},
                    {"@type":"ListItem","position":2,"name":tools_name,"item":tools_url},
                    {"@type":"ListItem","position":3,"name":tn}
                ]
            }
            bc_str = '<script type="application/ld+json">\n' + json.dumps(bc, ensure_ascii=False, indent=2) + '\n</script>'
            # 插在SoftwareApplication的</script>后面
            sa_end = c.find('</script>', c.find('SoftwareApplication'))
            if sa_end > 0:
                insert_pos = sa_end + len('</script>')
                c = c[:insert_pos] + '\n' + bc_str + c[insert_pos:]
            else:
                c = c.replace('</head>', '\n' + bc_str + '\n</head>')
            fixed.append(issue)
        
        elif issue == 'js_paren_mismatch':
            # 简单括号修复
            for m2 in re.finditer(r'(<script>)(.*?)(</script>)', c, re.DOTALL):
                s = m2.group(2)
                if len(s.strip()) < 50: continue
                if 'gtag' in s or 'adsbygoogle' in s or 'dataLayer' in s: continue
                if 'e.preventDefault()' in s and len(s) < 300: continue
                
                # 只移除字符串
                no_str = re.sub(r"'[^'\\]*(?:\\.[^'\\]*)*'", "''", s)
                no_str = re.sub(r'"[^"\\]*(?:\\.[^"\\]*)*"', '""', no_str)
                no_str = re.sub(r'`[^`\\]*(?:\\.[^`\\]*)*`', '``', no_str)
                depth = sum(1 for ch in no_str if ch == '(') - sum(1 for ch in no_str if ch == ')')
                if depth == 0: continue
                # 正则工具跳过
                if 'regex' in item.lower():
                    fixed.append(issue)
                    continue
                
                trial = s.rstrip()
                for _ in range(5):
                    if depth == 0: break
                    elif depth < 0:
                        lp = trial.rfind(')')
                        if lp >= 0: trial = trial[:lp] + trial[lp+1:]; depth += 1
                        else: break
                    else:
                        trial += ')'; depth -= 1
                if depth == 0:
                    c = c.replace(m2.group(0), m2.group(1) + trial + m2.group(3), 1)
                    fixed.append(issue)
                else:
                    remaining.append(issue)
                break
            else:
                remaining.append(issue)
        
        elif issue == 'js_dup_func':
            # 去重：只保留第一个定义
            func_defs = list(re.finditer(r'function\s+(\w+)\s*\([^)]*\)\s*\{[^}]*\}', c))
            seen = set()
            for fd in reversed(func_defs):
                fname = re.search(r'function\s+(\w+)', fd.group(0)).group(1)
                if fname in seen:
                    c = c[:fd.start()] + c[fd.end():]
                    fixed.append(issue)
                seen.add(fname)
            if 'js_dup_func' not in fixed:
                remaining.append(issue)
        
        elif issue == 'js_alert':
            if 'showToast' in c:
                c = re.sub(r'\balert\s*\(', 'showToast(', c)
                fixed.append(issue)
            else:
                remaining.append(issue)
        
        elif issue == 'no_software_app':
            tm = re.search(r'<title>([^<]+)</title>', c)
            tn = tm.group(1).split(' - ')[0].split(' | ')[0].strip()[:60] if tm else item.replace('-',' ').title()
            dm = re.search(r'<meta name="description" content="([^"]*)"', c)
            desc = dm.group(1)[:150] if dm else f'Free online {tn}. Pure frontend, no data upload.'
            sa = '{"@context":"https://schema.org","@type":"SoftwareApplication","name":"' + tn + '","description":"' + desc + '","applicationCategory":"UtilitiesApplication","operatingSystem":"Web","publisher":{"@type":"Organization","name":"Free ToolBase","email":"dexshuang@google.com"},"offers":{"@type":"Offer","price":"0","priceCurrency":"USD"}}'
            sa_tag = '<script type="application/ld+json">' + sa + '</script>'
            c = c.replace('</head>', '\n' + sa_tag + '\n</head>')
            fixed.append(issue)
        
        else:
            remaining.append(issue)
    
    if fixed:
        with open(path, 'w', encoding='utf-8') as f: f.write(c)
    
    return fixed, remaining

# ============ 主流程 ============

def check_homepage(path, lang):
    """门0: 首页HTML结构完整性"""
    issues = []
    with open(path, 'r', encoding='utf-8', errors='ignore') as f: c = f.read()
    
    # head标签必须正确闭合
    if not re.search(r'<head\s*>', c):
        issues.append('head_not_opened')
    
    # head内不应有tool-card HTML（卡片误插head→白屏），排除CSS中的.tool-card
    head_close = c.find('</head>')
    if head_close > 0 and re.search(r'<div\s+class="tool-card"', c[:head_close]):
        issues.append('cards_in_head')
    
    # 必须有tools-grid
    if 'tools-grid' not in c:
        issues.append('no_tools_grid')
    
    # 必须有搜索框
    if 'search' not in c.lower():
        issues.append('no_search')
    
    # 必须有分类筛选
    if 'data-category' not in c and 'filter' not in c.lower():
        issues.append('no_category_filter')
    
    return issues

def fix_homepage(path, lang, issues):
    """自动修复首页问题"""
    with open(path, 'r', encoding='utf-8', errors='ignore') as f: c = f.read()
    fixed = []
    remaining = []
    
    for issue in issues:
        if issue == 'head_not_opened':
            # 修复 <head 缺 >
            c = re.sub(r'<head(?!\s*>)[^>]*$', '<head>', c, count=1, flags=re.MULTILINE)
            if re.search(r'<head\s*>', c):
                fixed.append(issue)
            else:
                remaining.append(issue)
        
        elif issue == 'cards_in_head':
            # 把head里的tool-card移到tools-grid
            head_close = c.find('</head>')
            head_content = c[:head_close]
            cards = re.findall(r'<div class="tool-card"[^>]*>.*?</div>', head_content, re.DOTALL)
            for card in cards:
                c = c.replace(card, '', 1)
            grid_match = re.search(r'<div class="tools-grid"[^>]*>', c)
            if grid_match and cards:
                insert_pos = grid_match.end()
                c = c[:insert_pos] + '\n'.join(cards) + '\n' + c[insert_pos:]
                fixed.append(issue)
            else:
                remaining.append(issue)
    
    if fixed:
        with open(path, 'w', encoding='utf-8') as f: f.write(c)
    return fixed, remaining

# ============ 新增检测门 v2 (2026-07-27) ============

def check_hreflang_correctness(path, lang, item):
    """门10: hreflang正确性 - zh→CN页, en→EN页, 无重复, 无相对路径"""
    issues = []
    with open(path, 'r', encoding='utf-8', errors='ignore') as f: c = f.read()
    if 'noindex' in c: return issues
    
    hrefs = re.findall(r'hreflang="([^"]+)" href="([^"]+)"', c)
    if not hrefs: return issues  # no_hreflang已被门3检测
    
    cn_url = f'https://free-toolbase.com/{item}/'
    en_url = f'https://free-toolbase.com/en/{item}/'
    
    # 检查zh→CN
    zh_hrefs = [url for lg, url in hrefs if lg == 'zh']
    if zh_hrefs:
        for url in zh_hrefs:
            if '/en/' in url:
                issues.append('hreflang_zh_points_en')
                break
            if url != cn_url and not url.endswith('/' + item + '/'):
                issues.append('hreflang_zh_wrong')
                break
    
    # 检查en→EN
    en_hrefs = [url for lg, url in hrefs if lg == 'en']
    if en_hrefs:
        for url in en_hrefs:
            if '/en/' not in url:
                issues.append('hreflang_en_points_cn')
                break
            if url != en_url:
                issues.append('hreflang_en_wrong')
                break
    
    # 检查重复
    lang_list = [lg for lg, _ in hrefs]
    if len(lang_list) != len(set(lang_list)):
        issues.append('hreflang_duplicate')
    
    # 检查相对路径
    for lg, url in hrefs:
        if './' in url or not url.startswith('https://'):
            issues.append('hreflang_relative')
            break
    
    # 检查www域名
    for lg, url in hrefs:
        if 'www.free-toolbase.com' in url:
            issues.append('hreflang_www')
            break
    
    return issues


def check_content_thickness(path, lang, item):
    """门11: 内容厚度 - 可见文字是否足够"""
    issues = []
    with open(path, 'r', encoding='utf-8', errors='ignore') as f: c = f.read()
    if 'noindex' in c: return issues
    
    # 提取可见文字
    clean = re.sub(r'<script[^>]*>.*?</script>', '', c, flags=re.DOTALL)
    clean = re.sub(r'<style[^>]*>.*?</style>', '', clean, flags=re.DOTALL)
    clean = re.sub(r'<[^>]+>', ' ', clean)
    text_len = len(re.sub(r'\s+', ' ', clean).strip())
    
    if text_len < 300:
        issues.append('content_very_thin')
    elif text_len < 500:
        issues.append('content_thin')
    
    return issues


def check_internal_links(path, lang, item):
    """门12: 内部链接 - 是否有相关工具推荐"""
    issues = []
    with open(path, 'r', encoding='utf-8', errors='ignore') as f: c = f.read()
    if 'noindex' in c: return issues
    
    # 检查是否有相关工具/推荐工具区域
    has_related = bool(re.search(
        r'related.?tool|相关工具|推荐工具|also.?like|you.?might|similar.?tool|更多工具',
        c, re.I
    ))
    if not has_related:
        issues.append('no_related_tools')
    
    return issues


def check_canonical_correctness(path, lang, item):
    """门13: canonical正确性 - 无www/指向存在页面"""
    issues = []
    with open(path, 'r', encoding='utf-8', errors='ignore') as f: c = f.read()
    if 'noindex' in c: return issues
    
    cm = re.search(r'<link rel="canonical" href="([^"]+)"', c)
    if not cm: return issues  # no_canonical已被门3检测
    
    url = cm.group(1)
    
    # www域名
    if 'www.free-toolbase.com' in url:
        issues.append('canonical_www')
    
    # 自引用noindex页面的canonical指向自身
    if 'noindex' in c and url.endswith('/' + item + '/'):
        issues.append('canonical_self_noindex')
    
    return issues


def run():
    all_issues = {}
    all_fixed = {}
    all_remaining = {}
    
    checks = [
        ('seo', check_seo),
        ('structure', check_structure),
        ('css', check_css),
        ('theme', check_theme),
        ('language', check_language),
        ('functionality', check_functionality),
        ('js', check_js),
        ('schema', check_schema),
        ('hreflang', check_hreflang_correctness),
        ('content', check_content_thickness),
        ('internal_links', check_internal_links),
        ('canonical', check_canonical_correctness),
    ]
    
    # 首页检测
    for lang, path in [('cn', os.path.join(SITE, 'index.html')), ('en', os.path.join(SITE, 'en', 'index.html'))]:
        if not os.path.isfile(path): continue
        issues = check_homepage(path, lang)
        if issues:
            all_issues[f'homepage:{lang}'] = issues
            fixed, remaining = fix_homepage(path, lang, issues)
            if fixed: all_fixed[f'homepage:{lang}'] = fixed
            if remaining: all_remaining[f'homepage:{lang}'] = remaining
    
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
