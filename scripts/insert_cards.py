#!/usr/bin/env python3
"""插入5个新工具卡片到CN和EN首页"""
import re

BASE = "/home/chison/tools-site"

# CN首页卡片
CN_CARDS = """<div class="tool-card" data-category="dev-tools"><span class="tool-icon">📐</span><span class="tool-name">流程图生成器</span><span class="tool-desc">手绘风格在线流程图，拖拽节点创建流程图、思维导图，支持矩形/菱形/圆形节点。</span><a href="/diagram-generator/" class="btn">立即使用</a></div>
<div class="tool-card" data-category="fun-tools"><span class="tool-icon">😀</span><span class="tool-name">文字转Emoji</span><span class="tool-desc">将普通文字转换为表情符号，支持字母/单词映射，让文字更有趣。</span><a href="/emojify/" class="btn">立即使用</a></div>
<div class="tool-card" data-category="fun-tools"><span class="tool-icon">✨</span><span class="tool-name">花体字生成器</span><span class="tool-desc">12种Unicode字体风格转换：粗体、斜体、手写体、花体、双线体等，一键复制。</span><a href="/font-generator/" class="btn">立即使用</a></div>
<div class="tool-card" data-category="seo-tools"><span class="tool-icon">🔗</span><span class="tool-name">UTM参数构建器</span><span class="tool-desc">可视化生成带UTM追踪参数的URL，支持GA/百度统计，营销人员必备。</span><a href="/utm-builder/" class="btn">立即使用</a></div>
<div class="tool-card" data-category="finance-tools"><span class="tool-icon">🚗</span><span class="tool-name">车贷计算器</span><span class="tool-desc">计算汽车贷款月供、总利息和还款总额，支持等额本息和等额本金两种方式。</span><a href="/car-loan-calculator/" class="btn">立即使用</a></div>"""

# EN首页卡片
EN_CARDS = """<div class="tool-card" data-category="dev-tools"><span class="tool-icon">📐</span><span class="tool-name">Flowchart Generator</span><span class="tool-desc">Hand-drawn style online flowchart, drag & drop nodes, mind maps, org charts.</span><a href="/en/diagram-generator/" class="btn">Use Now</a></div>
<div class="tool-card" data-category="fun-tools"><span class="tool-icon">😀</span><span class="tool-name">Text to Emoji</span><span class="tool-desc">Convert plain text into fun emoji symbols. Letter and word mapping support.</span><a href="/en/emojify/" class="btn">Use Now</a></div>
<div class="tool-card" data-category="fun-tools"><span class="tool-icon">✨</span><span class="tool-name">Font Generator</span><span class="tool-desc">12 Unicode font styles: bold, italic, script, fraktur, double-struck, and more.</span><a href="/en/font-generator/" class="btn">Use Now</a></div>
<div class="tool-card" data-category="seo-tools"><span class="tool-icon">🔗</span><span class="tool-name">UTM Builder</span><span class="tool-desc">Visually generate URLs with UTM tracking parameters for GA and campaign tracking.</span><a href="/en/utm-builder/" class="btn">Use Now</a></div>
<div class="tool-card" data-category="finance-tools"><span class="tool-icon">🚗</span><span class="tool-name">Car Loan Calculator</span><span class="tool-desc">Calculate monthly payments, total interest, and total cost for auto loans.</span><a href="/en/car-loan-calculator/" class="btn">Use Now</a></div>"""

# 插入CN
anchor_cn = '<div class="tool-card" data-category="dev-tools"><span class="tool-icon">📋</span><span class="tool-name">OpenAPI生成器</span>'
with open(f"{BASE}/index.html", "r") as f:
    content_cn = f.read()
# 在OpenAPI生成器卡片后面插入
pos = content_cn.find(anchor_cn)
if pos >= 0:
    end_of_card = content_cn.index("</div>", content_cn.index("</a>", pos)) + 6
    new_cn = content_cn[:end_of_card] + "\n" + CN_CARDS + content_cn[end_of_card:]
    with open(f"{BASE}/index.html", "w") as f:
        f.write(new_cn)
    print("✅ CN首页卡片已插入")
else:
    print("❌ CN首页未找到锚点")

# 插入EN
anchor_en = '<div class="tool-card" data-category="dev-tools"><span class="tool-icon">📋</span><span class="tool-name">OpenAPI Generator</span>'
with open(f"{BASE}/en/index.html", "r") as f:
    content_en = f.read()
pos = content_en.find(anchor_en)
if pos >= 0:
    end_of_card = content_en.index("</div>", content_en.index("</a>", pos)) + 6
    new_en = content_en[:end_of_card] + "\n" + EN_CARDS + content_en[end_of_card:]
    with open(f"{BASE}/en/index.html", "w") as f:
        f.write(new_en)
    print("✅ EN首页卡片已插入")
else:
    print("❌ EN首页未找到锚点")

# 更新工具数量
# CN: "2694个免费工具" → "2699个免费工具"
# EN: "2694+免费在线工具" → "2699+免费在线工具"
for path, patterns in [
    (f"{BASE}/index.html", [("2694个免费工具", "2699个免费工具"), ("2694+免费在线工具", "2699+免费在线工具")]),
    (f"{BASE}/en/index.html", [("2694 free online tools", "2699 free online tools"), ("2694+ free online tools", "2699+ free online tools"), ("2694+ browser-based utilities", "2699+ browser-based utilities")])
]:
    with open(path, "r") as f:
        c = f.read()
    for old, new in patterns:
        c = c.replace(old, new)
    with open(path, "w") as f:
        f.write(c)
    print(f"✅ {path} 数字已更新")

print("\n验证:")
print(f"CN卡片: {new_cn.count('tool-card')}")
print(f"EN卡片: {new_en.count('tool-card')}")