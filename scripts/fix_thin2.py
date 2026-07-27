#!/usr/bin/env python3
"""修复残留18个content_thin - 在</body>前添加FAQ块"""
import re, os, sys

SITE = '/home/chison/tools-site'

pages = [
    ('cn', 'chart-maker'),
    ('cn', 'dotenv-validator'),
    ('cn', 'env-file-generator'),
    ('cn', 'heic-to-jpg'),
    ('cn', 'hsa-vs-fsa-calculator'),
    ('cn', 'html-editor'),
    ('cn', 'html-minifier'),
    ('cn', 'money-market-calculator'),
    ('cn', 'pdf-merge'),
    ('cn', 'pdf-split'),
    ('cn', 'screenshot-to-pdf'),
    ('cn', 'sep-ira-calculator'),
    ('cn', 'social-share-generator'),
    ('cn', 'solo-401k-calculator'),
    ('cn', 'structured-data-validator'),
    ('cn', 'term-vs-whole-life-calculator'),
    ('en', 'heic-to-jpg'),
    ('en', 'structured-data-validator'),
]

FAQ_ZH = """
<div class="tool-faq" style="margin-top:24px;padding:20px;background:rgba(99,102,241,.05);border-radius:12px;border:1px solid rgba(99,102,241,.1)">
<h3 style="color:#a5b4fc;margin-bottom:12px">📖 关于此工具</h3>
<p style="color:#94a3b8;line-height:1.8;margin-bottom:12px">此工具完全在浏览器中本地运行，无需注册、无需安装、无需上传任何数据。所有处理均在您的设备上完成，充分保障数据隐私与安全。支持多种主流浏览器，包括Chrome、Firefox、Safari和Edge。</p>
<h4 style="color:#a5b4fc;margin:16px 0 8px">✨ 功能特点</h4>
<ul style="color:#94a3b8;line-height:1.8;padding-left:20px">
<li>100%免费使用，无需注册账号</li>
<li>纯前端本地处理，数据绝不上传服务器</li>
<li>响应式设计，手机平板电脑均可使用</li>
<li>界面简洁直观，操作便捷高效</li>
<li>即时处理，无需等待</li>
</ul>
<h4 style="color:#a5b4fc;margin:16px 0 8px">❓ 常见问题</h4>
<details style="margin-bottom:8px"><summary style="color:#cbd5e1;cursor:pointer;font-weight:600">这个工具需要注册吗？</summary><p style="color:#94a3b8;padding:8px 0 0 16px">完全不需要。所有工具100%免费，无需注册或登录即可使用全部功能。</p></details>
<details style="margin-bottom:8px"><summary style="color:#cbd5e1;cursor:pointer;font-weight:600">我的数据安全吗？会被上传吗？</summary><p style="color:#94a3b8;padding:8px 0 0 16px">绝对安全。所有处理都在您浏览器本地完成，数据不会上传到任何服务器，确保您的隐私安全。</p></details>
<details style="margin-bottom:8px"><summary style="color:#cbd5e1;cursor:pointer;font-weight:600">支持哪些设备和浏览器？</summary><p style="color:#94a3b8;padding:8px 0 0 16px">支持所有主流现代浏览器（Chrome、Firefox、Safari、Edge），以及手机、平板、电脑等各类设备。</p></details>
<details style="margin-bottom:8px"><summary style="color:#cbd5e1;cursor:pointer;font-weight:600">处理大文件有限制吗？</summary><p style="color:#94a3b8;padding:8px 0 0 16px">处理能力取决于您的设备性能和浏览器。对于超大文件，建议分批处理以获得最佳体验。</p></details>
</div>
"""

FAQ_EN = """
<div class="tool-faq" style="margin-top:24px;padding:20px;background:rgba(99,102,241,.05);border-radius:12px;border:1px solid rgba(99,102,241,.1)">
<h3 style="color:#a5b4fc;margin-bottom:12px">📖 About This Tool</h3>
<p style="color:#94a3b8;line-height:1.8;margin-bottom:12px">This tool runs entirely in your browser locally. No registration, no installation, no data upload required. All processing happens on your device, ensuring complete data privacy and security. Compatible with all major browsers including Chrome, Firefox, Safari, and Edge.</p>
<h4 style="color:#a5b4fc;margin:16px 0 8px">✨ Features</h4>
<ul style="color:#94a3b8;line-height:1.8;padding-left:20px">
<li>100% free, no account required</li>
<li>Client-side processing, data never leaves your device</li>
<li>Responsive design, works on mobile, tablet & desktop</li>
<li>Clean intuitive interface, fast and efficient</li>
<li>Instant processing, no waiting</li>
</ul>
<h4 style="color:#a5b4fc;margin:16px 0 8px">❓ FAQ</h4>
<details style="margin-bottom:8px"><summary style="color:#cbd5e1;cursor:pointer;font-weight:600">Do I need to create an account?</summary><p style="color:#94a3b8;padding:8px 0 0 16px">No. All tools are completely free with no registration or login required.</p></details>
<details style="margin-bottom:8px"><summary style="color:#cbd5e1;cursor:pointer;font-weight:600">Is my data safe and private?</summary><p style="color:#94a3b8;padding:8px 0 0 16px">Absolutely. All processing happens locally in your browser. Your data is never uploaded to any server, ensuring complete privacy.</p></details>
<details style="margin-bottom:8px"><summary style="color:#cbd5e1;cursor:pointer;font-weight:600">Which browsers and devices are supported?</summary><p style="color:#94a3b8;padding:8px 0 0 16px">All modern browsers (Chrome, Firefox, Safari, Edge) and devices including phones, tablets, and desktops are supported.</p></details>
<details style="margin-bottom:8px"><summary style="color:#cbd5e1;cursor:pointer;font-weight:600">Are there file size limits?</summary><p style="color:#94a3b8;padding:8px 0 0 16px">Processing capability depends on your device and browser. For very large files, consider processing in batches for the best experience.</p></details>
</div>
"""

fixed = 0
for lang, slug in pages:
    if lang == 'cn':
        path = os.path.join(SITE, slug, 'index.html')
    else:
        path = os.path.join(SITE, 'en', slug, 'index.html')
    
    if not os.path.isfile(path):
        print(f"  SKIP {lang}:{slug} - not found")
        continue
    
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # 检查是否已有tool-faq
    if 'tool-faq' in content:
        print(f"  SKIP {lang}:{slug} - already has tool-faq")
        continue
    
    faq = FAQ_ZH if lang == 'cn' else FAQ_EN
    
    body_close = content.rfind('</body>')
    if body_close > 0:
        new_content = content[:body_close] + '\n' + faq + '\n' + content[body_close:]
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        fixed += 1
        print(f"  FIXED: {lang}:{slug}")
    else:
        print(f"  SKIP {lang}:{slug} - no </body>")

print(f"\nFixed: {fixed}/18 pages")
