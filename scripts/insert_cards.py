#!/usr/bin/env python3
"""在CN和EN首页插入新工具卡片"""
import re

BASE = "/home/chison/tools-site"

CN_CARDS = """<div class="tool-card" data-category="image-tools"><span class="tool-icon">🎞️</span><span class="tool-name">GIF倒放工具</span><span class="tool-desc">上传GIF即可一键反转播放顺序</span><a href="/gif-reverse/" class="btn">立即使用</a></div>
<div class="tool-card" data-category="image-tools"><span class="tool-icon">⏩</span><span class="tool-name">GIF速度调节器</span><span class="tool-desc">在线调节GIF播放速度，支持0.25x到4x变速</span><a href="/gif-speed-changer/" class="btn">立即使用</a></div>
<div class="tool-card" data-category="dev-tools"><span class="tool-icon">🖼️</span><span class="tool-name">SVG在线预览编辑器</span><span class="tool-desc">粘贴SVG代码实时渲染，支持缩放查看</span><a href="/svg-viewer/" class="btn">立即使用</a></div>
<div class="tool-card" data-category="dev-tools"><span class="tool-icon">🛡️</span><span class="tool-name">安全响应头检测器</span><span class="tool-desc">在线检测网站CSP/HSTS等安全响应头配置</span><a href="/security-headers-checker/" class="btn">立即使用</a></div>
<div class="tool-card" data-category="design-tools"><span class="tool-icon">🎨</span><span class="tool-name">HSL颜色选择器</span><span class="tool-desc">可视化调节色相/饱和度/亮度，实时预览CSS色值</span><a href="/hsl-color-picker/" class="btn">立即使用</a></div>
<div class="tool-card" data-category="dev-tools"><span class="tool-icon">📄</span><span class="tool-name">XML在线查看器</span><span class="tool-desc">粘贴XML代码自动美化高亮，树形结构展示</span><a href="/xml-viewer/" class="btn">立即使用</a></div>
<div class="tool-card" data-category="text-tools"><span class="tool-icon">🔍</span><span class="tool-name">文本去重工具</span><span class="tool-desc">按行去重或整体去重，支持保留/移除重复项</span><a href="/text-deduplicator/" class="btn">立即使用</a></div>
<div class="tool-card" data-category="fun-tools"><span class="tool-icon">🎯</span><span class="tool-name">决策转盘</span><span class="tool-desc">自定义选项列表，旋转转盘随机选择</span><a href="/decision-wheel/" class="btn">立即使用</a></div>
<div class="tool-card" data-category="fun-tools"><span class="tool-icon">🎲</span><span class="tool-name">骰子模拟器</span><span class="tool-desc">支持D4-D100多面骰和多骰同掷，含历史记录</span><a href="/dice-roll-simulator/" class="btn">立即使用</a></div>
<div class="tool-card" data-category="text-tools"><span class="tool-icon">📋</span><span class="tool-name">剪贴板格式化工具</span><span class="tool-desc">一键粘贴自动去空格、格式化大小写、清理特殊字符</span><a href="/clipboard-formatter/" class="btn">立即使用</a></div>"""

EN_CARDS = """<div class="tool-card" data-category="image-tools"><span class="tool-icon">🎞️</span><span class="tool-name">GIF Reverse Tool</span><span class="tool-desc">Upload GIF and reverse playback instantly</span><a href="/en/gif-reverse/" class="btn">Use Now</a></div>
<div class="tool-card" data-category="image-tools"><span class="tool-icon">⏩</span><span class="tool-name">GIF Speed Changer</span><span class="tool-desc">Adjust GIF playback speed from 0.25x to 4x</span><a href="/en/gif-speed-changer/" class="btn">Use Now</a></div>
<div class="tool-card" data-category="dev-tools"><span class="tool-icon">🖼️</span><span class="tool-name">SVG Online Viewer</span><span class="tool-desc">Paste SVG code for real-time rendering with zoom</span><a href="/en/svg-viewer/" class="btn">Use Now</a></div>
<div class="tool-card" data-category="dev-tools"><span class="tool-icon">🛡️</span><span class="tool-name">Security Headers Checker</span><span class="tool-desc">Check CSP, HSTS and security headers online</span><a href="/en/security-headers-checker/" class="btn">Use Now</a></div>
<div class="tool-card" data-category="design-tools"><span class="tool-icon">🎨</span><span class="tool-name">HSL Color Picker</span><span class="tool-desc">Visual HSL adjustment with real-time CSS preview</span><a href="/en/hsl-color-picker/" class="btn">Use Now</a></div>
<div class="tool-card" data-category="dev-tools"><span class="tool-icon">📄</span><span class="tool-name">XML Online Viewer</span><span class="tool-desc">Paste XML for auto-beautify with syntax highlighting</span><a href="/en/xml-viewer/" class="btn">Use Now</a></div>
<div class="tool-card" data-category="text-tools"><span class="tool-icon">🔍</span><span class="tool-name">Text Deduplicator</span><span class="tool-desc">Remove duplicate lines with multiple modes</span><a href="/en/text-deduplicator/" class="btn">Use Now</a></div>
<div class="tool-card" data-category="fun-tools"><span class="tool-icon">🎯</span><span class="tool-name">Decision Wheel</span><span class="tool-desc">Customize options and spin the wheel randomly</span><a href="/en/decision-wheel/" class="btn">Use Now</a></div>
<div class="tool-card" data-category="fun-tools"><span class="tool-icon">🎲</span><span class="tool-name">Dice Roll Simulator</span><span class="tool-desc">Multi-sided dice with history tracking</span><a href="/en/dice-roll-simulator/" class="btn">Use Now</a></div>
<div class="tool-card" data-category="text-tools"><span class="tool-icon">📋</span><span class="tool-name">Clipboard Formatter</span><span class="tool-desc">One-click paste and auto-clean text formatting</span><a href="/en/clipboard-formatter/" class="btn">Use Now</a></div>"""

# Insert into CN index.html
with open(f"{BASE}/index.html") as f:
    cn = f.read()
# Find insertion point: last tool-card before <script>
# Look for the pattern: last </div>\n\n<script>
cn = cn.replace('\n\n<script>\n// Make tool cards clickable', '\n' + CN_CARDS + '\n\n<script>\n// Make tool cards clickable')
with open(f"{BASE}/index.html", "w") as f:
    f.write(cn)

# Insert into EN index.html
with open(f"{BASE}/en/index.html") as f:
    en = f.read()
en = en.replace('\n\n<script>\n// Make tool cards clickable', '\n' + EN_CARDS + '\n\n<script>\n// Make tool cards clickable')
with open(f"{BASE}/en/index.html", "w") as f:
    f.write(en)

# Verify
cn_cards = cn.count('class="tool-card"')
en_cards = en.count('class="tool-card"')
print(f"CN卡片: {cn_cards}")
print(f"EN卡片: {en_cards}")
print(f"一致: {cn_cards == en_cards}")

# Update tool count numbers
import re
actual = str(cn_cards)
cn_updated = re.sub(r'\d+个免费工具', f'{actual}个免费工具', cn)
cn_updated = re.sub(r'\d+\+免费在线工具', f'{actual}+免费在线工具', cn_updated)
en_updated = re.sub(r'\d+\+ free online tools', f'{actual}+ free online tools', en)
en_updated = re.sub(r'\d+\+ browser-based utilities', f'{actual}+ browser-based utilities', en_updated)

with open(f"{BASE}/index.html", "w") as f:
    f.write(cn_updated)
with open(f"{BASE}/en/index.html", "w") as f:
    f.write(en_updated)

print(f"✅ 首页卡片已更新: {actual}")