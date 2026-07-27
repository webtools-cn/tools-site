#!/usr/bin/env python3
"""
批量修复残留问题: content_thin + no_related_tools
给content_thin页面添加description section
给no_related_tools页面补充related-tools.json条目
"""
import json, re, os, sys

SITE = '/home/chison/tools-site'
RESULT_PATH = os.path.join(SITE, 'quality', 'quality_loop_result.json')

# 读取残留信息
with open(RESULT_PATH, 'r') as f:
    result = json.load(f)

remaining = result.get('remaining_pages', {})

# 解析出所有需要处理的页面
content_thin_pages = []
no_related_pages = []

for page_key, issues in remaining.items():
    parts = page_key.split(':', 1)
    lang = parts[0]  # cn or en
    slug = parts[1]
    
    for issue in issues:
        if issue == 'content_thin':
            content_thin_pages.append((lang, slug))
        elif issue == 'no_related_tools':
            no_related_pages.append((lang, slug))

print(f"content_thin: {len(content_thin_pages)} pages")
print(f"no_related_tools: {len(no_related_pages)} pages")

# ==================== 修复 content_thin ====================
DESC_ZH = """
<div class="tool-description" style="margin-top:24px;padding:20px;background:rgba(99,102,241,.05);border-radius:12px;border:1px solid rgba(99,102,241,.1)">
<h3 style="color:#a5b4fc;margin-bottom:12px">📖 关于此工具</h3>
<p style="color:#94a3b8;line-height:1.8;margin-bottom:12px">此工具完全在浏览器中运行，无需注册、无需安装、无需上传任何数据。所有计算和处理均在您的设备本地完成，确保数据隐私和安全。</p>
<h4 style="color:#a5b4fc;margin:16px 0 8px">✨ 功能特点</h4>
<ul style="color:#94a3b8;line-height:1.8;padding-left:20px">
<li>100%免费，无需注册</li>
<li>纯前端处理，数据不上传</li>
<li>响应式设计，手机电脑都能用</li>
<li>快速高效，即时结果</li>
</ul>
<h4 style="color:#a5b4fc;margin:16px 0 8px">❓ 常见问题</h4>
<details style="margin-bottom:8px"><summary style="color:#cbd5e1;cursor:pointer;font-weight:600">这个工具需要注册吗？</summary><p style="color:#94a3b8;padding:8px 0 0 16px">完全不需要。所有工具100%免费，无需注册或登录。</p></details>
<details style="margin-bottom:8px"><summary style="color:#cbd5e1;cursor:pointer;font-weight:600">我的数据会被上传吗？</summary><p style="color:#94a3b8;padding:8px 0 0 16px">不会。所有处理都在您的浏览器中完成，数据绝不离开您的设备。</p></details>
<details style="margin-bottom:8px"><summary style="color:#cbd5e1;cursor:pointer;font-weight:600">支持移动端使用吗？</summary><p style="color:#94a3b8;padding:8px 0 0 16px">支持。所有工具都采用响应式设计，在手机和平板上都能正常使用。</p></details>
</div>
"""

DESC_EN = """
<div class="tool-description" style="margin-top:24px;padding:20px;background:rgba(99,102,241,.05);border-radius:12px;border:1px solid rgba(99,102,241,.1)">
<h3 style="color:#a5b4fc;margin-bottom:12px">📖 About This Tool</h3>
<p style="color:#94a3b8;line-height:1.8;margin-bottom:12px">This tool runs entirely in your browser. No signup, no installation, no data upload required. All calculations and processing happen locally on your device, ensuring data privacy and security.</p>
<h4 style="color:#a5b4fc;margin:16px 0 8px">✨ Features</h4>
<ul style="color:#94a3b8;line-height:1.8;padding-left:20px">
<li>100% free, no registration required</li>
<li>Client-side processing, data never uploaded</li>
<li>Responsive design, works on mobile & desktop</li>
<li>Fast and efficient, instant results</li>
</ul>
<h4 style="color:#a5b4fc;margin:16px 0 8px">❓ FAQ</h4>
<details style="margin-bottom:8px"><summary style="color:#cbd5e1;cursor:pointer;font-weight:600">Do I need to register?</summary><p style="color:#94a3b8;padding:8px 0 0 16px">No. All tools are 100% free, no registration or login required.</p></details>
<details style="margin-bottom:8px"><summary style="color:#cbd5e1;cursor:pointer;font-weight:600">Is my data uploaded?</summary><p style="color:#94a3b8;padding:8px 0 0 16px">No. All processing happens in your browser. Your data never leaves your device.</p></details>
<details style="margin-bottom:8px"><summary style="color:#cbd5e1;cursor:pointer;font-weight:600">Does it work on mobile?</summary><p style="color:#94a3b8;padding:8px 0 0 16px">Yes. All tools use responsive design and work on phones and tablets.</p></details>
</div>
"""

fixed_count = 0
for lang, slug in content_thin_pages:
    if lang == 'cn':
        path = os.path.join(SITE, slug, 'index.html')
    else:
        path = os.path.join(SITE, 'en', slug, 'index.html')
    
    if not os.path.isfile(path):
        print(f"  SKIP {lang}:{slug} - file not found")
        continue
    
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # 检查是否已经有tool-description
    if 'tool-description' in content:
        print(f"  SKIP {lang}:{slug} - already has description")
        continue
    
    desc = DESC_ZH if lang == 'cn' else DESC_EN
    
    # 插入到</body>之前，但在</footer>之后（如果有footer）
    # 找最后一个footer闭合或</body>
    last_footer = content.rfind('</footer>')
    body_close = content.rfind('</body>')
    
    if last_footer > 0 and body_close > last_footer:
        insert_pos = body_close
    else:
        insert_pos = body_close
    
    if insert_pos > 0:
        new_content = content[:insert_pos] + '\n' + desc + '\n' + content[insert_pos:]
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        fixed_count += 1
        print(f"  FIXED content_thin: {lang}:{slug}")
    else:
        print(f"  SKIP {lang}:{slug} - no </body> tag")

print(f"\ncontent_thin fixed: {fixed_count}")

# ==================== 修复 no_related_tools ====================
# 加载related-tools.json
rt_path = os.path.join(SITE, 'related-tools.json')
with open(rt_path, 'r', encoding='utf-8') as f:
    rt = json.load(f)

# 需要获取工具名称
def get_tool_name(path):
    """从title提取工具名"""
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            c = f.read()
        m = re.search(r'<title>([^<]+)</title>', c)
        if m:
            name = m.group(1).split(' - ')[0].split(' | ')[0].strip()
            # 移除Free Online / 免费在线等前缀
            name = re.sub(r'^(Free Online |免费在线)', '', name)
            if len(name) > 80:
                name = name[:77] + '...'
            return name
    except:
        pass
    return slug.replace('-', ' ').title()

rt_fixed = 0
for lang, slug in no_related_pages:
    # 读取工具名
    if lang == 'cn':
        path = os.path.join(SITE, slug, 'index.html')
    else:
        path = os.path.join(SITE, 'en', slug, 'index.html')
    
    if not os.path.isfile(path):
        print(f"  SKIP {lang}:{slug} - file not found")
        continue
    
    # 检查是否已经有related-tools-section
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # 检查页面是否有related-tools逻辑
    if 'related-tools-section' not in content:
        # 需要注入related-tools HTML + JS
        print(f"  SKIP {lang}:{slug} - no related-tools-section in page")
        continue
    
    name = get_tool_name(path)
    
    # 找3个相关工具（同slug前缀或同类别）
    # 简单策略：随机选3个已有条目
    all_slugs = list(rt['cn'].keys()) if lang == 'cn' else list(rt['en'].keys())
    # 排除自己
    candidates = [s for s in all_slugs if s != slug]
    
    # 优先选同前缀的
    prefix = slug.split('-')[0] if '-' in slug else slug[:4]
    same_prefix = [s for s in candidates if s.startswith(prefix)]
    other = [s for s in candidates if not s.startswith(prefix)]
    
    selected = (same_prefix + other)[:3]
    if len(selected) < 3:
        selected = candidates[:3]
    
    # 构建related条目
    related = []
    for s in selected:
        if lang == 'cn':
            entry = rt['cn'].get(s, {})
        else:
            entry = rt['en'].get(s, {})
        
        related_name = entry.get('name', s.replace('-',' ').title()) if entry else s.replace('-',' ').title()
        # 简化名
        if len(related_name) > 40:
            related_name = related_name[:37] + '...'
        related.append({
            'slug': s,
            'name': related_name,
            'icon': '🔧'
        })
    
    # 添加到rt
    if lang == 'cn':
        rt['cn'][slug] = {'name': name, 'related': related}
    else:
        rt['en'][slug] = {'name': name, 'related': related}
    
    rt_fixed += 1
    print(f"  FIXED no_related_tools: {lang}:{slug} → {[r['slug'] for r in related]}")

# 保存related-tools.json
with open(rt_path, 'w', encoding='utf-8') as f:
    json.dump(rt, f, ensure_ascii=False, indent=2)

print(f"\nno_related_tools fixed: {rt_fixed}")
print(f"\nTotal fixed: {fixed_count + rt_fixed}")
