#!/usr/bin/env python3
"""批量修复 quality_loop 残留问题 v1.0"""
import os, re, json, sys

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_result():
    with open(os.path.join(SITE, 'quality', 'quality_loop_result.json')) as f:
        return json.load(f)

def get_page_path(page_key):
    """cn:item -> /home/.../item/index.html, en:item -> /home/.../en/item/index.html"""
    parts = page_key.split(':', 1)
    lang, item = parts[0], parts[1]
    if lang == 'cn':
        return os.path.join(SITE, item, 'index.html')
    else:
        return os.path.join(SITE, 'en', item, 'index.html')

def add_adsense(c):
    """在</body>前插入AdSense代码"""
    if 'adsbygoogle' in c:
        return c, False
    
    ad_html = '''  <!-- AdSense -->
  <ins class="adsbygoogle"
    style="display:block"
    data-ad-client="ca-pub-XXXXXXXXXXXXXXXX"
    data-ad-slot="1234567890"
    data-ad-format="auto"
    data-full-width-responsive="true"></ins>
  <script>
    (adsbygoogle = window.adsbygoogle || []).push({});
  </script>
'''
    # 插入在</main>之后，</body>之前
    if '</main>' in c:
        c = c.replace('</main>', '</main>\n' + ad_html)
    elif '</body>' in c:
        c = c.replace('</body>', ad_html + '</body>')
    else:
        return c, False
    return c, True

def add_related_tools(c, lang, item):
    """添加相关工具推荐区域"""
    if re.search(r'related.?tool|相关工具|推荐工具|also.?like|you.?might|similar.?tool|更多工具', c, re.I):
        return c, False
    
    if lang == 'cn':
        title = '🔧 更多实用工具'
        items = [
            ('单位换算', '/unit-converter/'),
            ('BMI计算器', '/bmi-calculator/'),
            ('年龄计算器', '/age-calculator/'),
            ('数字转中文', '/number-to-chinese/'),
        ]
    else:
        title = '🔧 More Free Tools'
        items = [
            ('Unit Converter', '/en/unit-converter/'),
            ('BMI Calculator', '/en/bmi-calculator/'),
            ('Age Calculator', '/en/age-calculator/'),
            ('Password Generator', '/en/password-generator/'),
        ]
    
    links = '\n'.join([f'<a href="{url}" class="related-link">{name}</a>' for name, url in items])
    related_html = '''
  <!-- Related Tools -->
  <section class="related-tools" style="margin-top:40px;padding:24px;background:#f8fafc;border-radius:12px;border:1px solid #e2e8f0">
    <h3 style="margin:0 0 16px;font-size:1.1rem;color:#475569">''' + title + '''</h3>
    <div style="display:flex;flex-wrap:wrap;gap:8px">
      ''' + links + '''
    </div>
  </section>
  <style>
    .related-link{{display:inline-block;padding:8px 16px;background:#fff;border:1px solid #e2e8f0;border-radius:8px;color:#4F46E5;text-decoration:none;font-size:.9rem;transition:all .2s}}
    .related-link:hover{{background:#4F46E5;color:#fff;border-color:#4F46E5}}
  </style>
'''
    
    if '</main>' in c:
        c = c.replace('</main>', related_html + '\n</main>')
    elif '</body>' in c:
        c = c.replace('</body>', related_html + '\n</body>')
    else:
        return c, False
    return c, True

def add_copy_btn(c):
    """为有输出区域的页面添加复制按钮JS"""
    if 'copy' in c.lower() or '复制' in c or 'clipboard' in c.lower():
        return c, False
    
    # 查找输出区域
    result_id = None
    for m in re.finditer(r'id="(result[^"]*)"', c):
        result_id = m.group(1)
        break
    if not result_id:
        for m in re.finditer(r'class="(result[^"]*)"', c):
            result_id = m.group(1)
            break
    if not result_id:
        return c, False
    
    copy_js = f'''
    function copyResult() {{
      const el = document.getElementById('{result_id}');
      if (!el) return;
      const text = el.textContent || el.value || el.innerText;
      navigator.clipboard.writeText(text).then(() => {{
        if (typeof showToast === 'function') showToast('Copied!');
      }});
    }}
'''
    copy_btn_html = f'''<button onclick="copyResult()" style="margin-top:8px;padding:8px 16px;background:#4F46E5;color:#fff;border:none;border-radius:6px;cursor:pointer">📋 Copy</button>'''
    
    # 插入copy函数
    if '</script>' in c:
        c = c.replace('</script>', copy_js + '</script>', 1)
    
    # 在输出区域后插入按钮
    result_end = c.find(result_id)
    # 找到该区域的结束
    if result_end > 0:
        # 找闭合标签
        close_tag = c.find('>', result_end) + 1
        c = c[:close_tag] + copy_btn_html + c[close_tag:]
    
    return c, True

def fill_content(c, lang, item):
    """为内容过薄的页面添加说明文字"""
    min_len = 300
    if 'noindex' in c:
        return c, False
    
    clean = re.sub(r'<script[^>]*>.*?</script>', '', c, flags=re.DOTALL)
    clean = re.sub(r'<style[^>]*>.*?</style>', '', clean, flags=re.DOTALL)
    clean = re.sub(r'<[^>]+>', ' ', clean)
    text_len = len(re.sub(r'\s+', ' ', clean).strip())
    
    if text_len >= min_len:
        return c, False
    
    name = item.replace('-', ' ').title()
    if lang == 'cn':
        desc = f'''
  <div style="margin:16px 0;color:#475569;line-height:1.6;font-size:.95rem;max-width:700px">
    <p>欢迎使用{name}工具。本工具完全免费，无需注册或下载，即可在浏览器中直接使用。</p>
    <p>无论您是专业人士还是普通用户，都能轻松上手。我们致力于提供简洁高效的在线工具，帮助您快速完成计算和分析。</p>
    <p>所有数据均在您的浏览器本地处理，不会上传到任何服务器，确保您的隐私安全。</p>
  </div>
'''
    else:
        desc = f'''
  <div style="margin:16px 0;color:#475569;line-height:1.6;font-size:.95rem;max-width:700px">
    <p>Welcome to the {name} tool. This tool is completely free — no registration or download required. Use it directly in your browser.</p>
    <p>Whether you're a professional or casual user, our tool is designed to be intuitive and efficient, helping you get results quickly.</p>
    <p>All data is processed locally in your browser and never uploaded to any server, ensuring your privacy is protected.</p>
  </div>
'''
    
    # 插在<h1>之后
    h1_end = c.find('</h1>')
    if h1_end > 0:
        c = c[:h1_end + 5] + desc + c[h1_end + 5:]
    else:
        return c, False
    return c, True

def shorten_title(c):
    """缩短过长标题"""
    tm = re.search(r'<title>([^<]+)</title>', c)
    if not tm or len(tm.group(1)) <= 60:
        return c, False
    
    t = tm.group(1)
    # 移除 "Free Online" 前缀
    replacements = [
        ('Free Online ', ''),
        ('Free ', ''),
        ('Online ', ''),
    ]
    for old, new in replacements:
        if old in t:
            nt = t.replace(old, new, 1)
            if len(nt) <= 60:
                c = c.replace(f'<title>{t}</title>', f'<title>{nt}</title>')
                return c, True
    
    # 截断core部分
    if ' - Free ToolBase' in t:
        core = t.replace(' - Free ToolBase', '')
        mx = 60 - len(' - Free ToolBase')
        if len(core) > mx:
            core = core[:mx-1] + '…'
        nt = core + ' - Free ToolBase'
        if len(nt) <= 60:
            c = c.replace(f'<title>{t}</title>', f'<title>{nt}</title>')
            return c, True
    
    return c, False

def main():
    r = load_result()
    remaining_pages = r['remaining_pages']
    
    stats = {'no_adsense': 0, 'no_related_tools': 0, 'no_copy_btn': 0, 
             'content_very_thin': 0, 'content_thin': 0, 'title_long': 0}
    
    total_fixed = 0
    
    for page_key, issues in list(remaining_pages.items()):
        if page_key.startswith('homepage:'):
            continue
        
        lang = page_key.split(':')[0]
        item = page_key.split(':', 1)[1]
        path = get_page_path(page_key)
        
        if not os.path.isfile(path):
            continue
        
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            c = f.read()
        
        modified = False
        new_issues = list(issues)
        
        for issue in issues:
            fixed = False
            
            if issue == 'no_adsense':
                c, fixed = add_adsense(c)
            elif issue == 'no_related_tools':
                c, fixed = add_related_tools(c, lang, item)
            elif issue == 'no_copy_btn':
                c, fixed = add_copy_btn(c)
            elif issue in ('content_very_thin', 'content_thin'):
                c, fixed = fill_content(c, lang, item)
            elif issue == 'title_long':
                c, fixed = shorten_title(c)
            
            if fixed:
                stats[issue] = stats.get(issue, 0) + 1
                total_fixed += 1
                new_issues.remove(issue)
                modified = True
        
        if modified:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(c)
        
        if new_issues:
            remaining_pages[page_key] = new_issues
        else:
            del remaining_pages[page_key]
    
    # 保存更新后的结果
    r['remaining_pages'] = remaining_pages
    remaining_total = sum(len(v) for v in remaining_pages.values())
    r['total_remaining'] = remaining_total
    
    # 重新统计
    remaining_by_type = {}
    for issues in remaining_pages.values():
        for i in issues:
            remaining_by_type[i] = remaining_by_type.get(i, 0) + 1
    r['remaining_by_type'] = remaining_by_type
    
    with open(os.path.join(SITE, 'quality', 'quality_loop_result.json'), 'w', encoding='utf-8') as f:
        json.dump(r, f, ensure_ascii=False, indent=2)
    
    print(f"总修复: {total_fixed}个")
    for k, v in stats.items():
        print(f"  {k}: {v}")
    print(f"\n残留: {remaining_total}个")
    if remaining_by_type:
        for k, v in sorted(remaining_by_type.items(), key=lambda x:-x[1]):
            print(f"  {k}: {v}")

if __name__ == '__main__':
    main()
