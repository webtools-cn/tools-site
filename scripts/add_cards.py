#!/usr/bin/env python3
"""在首页添加新工具卡片"""
import os

BASE = "/home/chison/tools-site"

CARDS = [
    {
        "slug": "virtual-piano-keyboard",
        "category": "fun-tools",
        "cn": '<div class="tool-card" data-category="fun-tools"><span class="tool-icon">🎹</span><span class="tool-name">虚拟钢琴键盘</span><span class="tool-desc">在线弹钢琴，鼠标/键盘演奏，支持录制回放</span><a href="/virtual-piano-keyboard/" class="btn">立即使用</a></div>',
        "en": '<div class="tool-card" data-category="fun-tools"><span class="tool-name">Virtual Piano Keyboard</span><span class="tool-desc">Play piano online with mouse/keyboard, record and playback</span><a href="/en/virtual-piano-keyboard/" class="btn">Use Now</a></div>',
    },
    {
        "slug": "neumorphic-css",
        "category": "design-tools",
        "cn": '<div class="tool-card" data-category="design-tools"><span class="tool-icon">🎨</span><span class="tool-name">Neumorphic CSS 生成器</span><span class="tool-desc">可视化生成新拟态风格CSS，实时预览一键复制</span><a href="/neumorphic-css/" class="btn">立即使用</a></div>',
        "en": '<div class="tool-card" data-category="design-tools"><span class="tool-name">Neumorphic CSS Generator</span><span class="tool-desc">Visual Soft UI CSS generator with real-time preview and copy</span><a href="/en/neumorphic-css/" class="btn">Use Now</a></div>',
    },
    {
        "slug": "bricks-calculator",
        "category": "calc-tools",
        "cn": '<div class="tool-card" data-category="calc-tools"><span class="tool-icon">🧱</span><span class="tool-name">砖块用量计算器</span><span class="tool-desc">输入墙体尺寸和砖块规格，自动计算所需砖数</span><a href="/bricks-calculator/" class="btn">立即使用</a></div>',
        "en": '<div class="tool-card" data-category="calc-tools"><span class="tool-name">Brick Calculator</span><span class="tool-desc">Calculate bricks needed from wall dimensions and specs</span><a href="/en/bricks-calculator/" class="btn">Use Now</a></div>',
    },
    {
        "slug": "website-uptime-checker",
        "category": "network-tools",
        "cn": '<div class="tool-card" data-category="network-tools"><span class="tool-icon">🔍</span><span class="tool-name">网站在线检测器</span><span class="tool-desc">检测任意网站是否可访问，显示状态码和响应时间</span><a href="/website-uptime-checker/" class="btn">立即使用</a></div>',
        "en": '<div class="tool-card" data-category="network-tools"><span class="tool-name">Website Uptime Checker</span><span class="tool-desc">Check if any website is online, show status code and response time</span><a href="/en/website-uptime-checker/" class="btn">Use Now</a></div>',
    },
    {
        "slug": "jwt-token-generator",
        "category": "security-tools",
        "cn": '<div class="tool-card" data-category="security-tools"><span class="tool-icon">🔐</span><span class="tool-name">JWT 令牌生成器</span><span class="tool-desc">可视化编辑Header/Payload，生成标准JWT Token</span><a href="/jwt-token-generator/" class="btn">立即使用</a></div>',
        "en": '<div class="tool-card" data-category="security-tools"><span class="tool-name">JWT Token Generator</span><span class="tool-desc">Edit Header/Payload visually, generate standard JWT tokens</span><a href="/en/jwt-token-generator/" class="btn">Use Now</a></div>',
    },
    {
        "slug": "swift-bic-validation",
        "category": "finance-tools",
        "cn": '<div class="tool-card" data-category="finance-tools"><span class="tool-icon">🏦</span><span class="tool-name">SWIFT/BIC 代码验证器</span><span class="tool-desc">验证BIC代码格式，解析银行代码、国家代码和分行代码</span><a href="/swift-bic-validation/" class="btn">立即使用</a></div>',
        "en": '<div class="tool-card" data-category="finance-tools"><span class="tool-name">SWIFT/BIC Code Validator</span><span class="tool-desc">Validate BIC format, parse bank/country/location/branch codes</span><a href="/en/swift-bic-validation/" class="btn">Use Now</a></div>',
    },
    {
        "slug": "ip-address-range-calculator",
        "category": "network-tools",
        "cn": '<div class="tool-card" data-category="network-tools"><span class="tool-icon">🌐</span><span class="tool-name">IP地址范围计算器</span><span class="tool-desc">CIDR子网计算：网络地址/广播地址/可用IP/主机数</span><a href="/ip-address-range-calculator/" class="btn">立即使用</a></div>',
        "en": '<div class="tool-card" data-category="network-tools"><span class="tool-name">IP Address Range Calculator</span><span class="tool-desc">CIDR subnet calc: network/broadcast/usable IPs/host count</span><a href="/en/ip-address-range-calculator/" class="btn">Use Now</a></div>',
    },
    {
        "slug": "color-contrast-analyzer",
        "category": "design-tools",
        "cn": '<div class="tool-card" data-category="design-tools"><span class="tool-icon">🎯</span><span class="tool-name">WCAG 颜色对比度分析器</span><span class="tool-desc">分析前景/背景色对比度，评估AA/AAA合规性</span><a href="/color-contrast-analyzer/" class="btn">立即使用</a></div>',
        "en": '<div class="tool-card" data-category="design-tools"><span class="tool-name">WCAG Color Contrast Analyzer</span><span class="tool-desc">Analyze fg/bg contrast ratio, evaluate AA/AAA compliance</span><a href="/en/color-contrast-analyzer/" class="btn">Use Now</a></div>',
    },
    {
        "slug": "docker-run-generator",
        "category": "dev-tools",
        "cn": '<div class="tool-card" data-category="dev-tools"><span class="tool-icon">🐳</span><span class="tool-name">Docker Run 命令生成器</span><span class="tool-desc">可视化配置端口/卷/环境变量，一键生成docker run命令</span><a href="/docker-run-generator/" class="btn">立即使用</a></div>',
        "en": '<div class="tool-card" data-category="dev-tools"><span class="tool-name">Docker Run Command Generator</span><span class="tool-desc">Visually configure ports/volumes/env vars, generate docker run</span><a href="/en/docker-run-generator/" class="btn">Use Now</a></div>',
    },
    {
        "slug": "cron-sandbox",
        "category": "dev-tools",
        "cn": '<div class="tool-card" data-category="dev-tools"><span class="tool-icon">⏰</span><span class="tool-name">Cron 表达式测试沙盒</span><span class="tool-desc">输入Cron表达式，查看人类可读描述和未来执行时间</span><a href="/cron-sandbox/" class="btn">立即使用</a></div>',
        "en": '<div class="tool-card" data-category="dev-tools"><span class="tool-name">Cron Expression Sandbox</span><span class="tool-desc">Enter cron expression, see human-readable description and next runs</span><a href="/en/cron-sandbox/" class="btn">Use Now</a></div>',
    },
]

# 更新CN首页
cn_path = os.path.join(BASE, "index.html")
with open(cn_path, "r") as f:
    cn_lines = f.readlines()

# 找到 tools-grid 所在行号
tools_grid_line = None
for i, line in enumerate(cn_lines):
    if '<div class="tools-grid"' in line:
        tools_grid_line = i
        break

if tools_grid_line is None:
    print("ERROR: tools-grid not found in CN index")
    exit(1)

# 在 tools-grid 下一行插入所有新卡片
cn_cards_html = "\n".join([c["cn"] for c in CARDS]) + "\n"
cn_lines.insert(tools_grid_line + 1, cn_cards_html)

with open(cn_path, "w") as f:
    f.writelines(cn_lines)
print(f"CN: 插入{len(CARDS)}张卡片在第{tools_grid_line+1}行")

# 更新EN首页
en_path = os.path.join(BASE, "en/index.html")
with open(en_path, "r") as f:
    en_lines = f.readlines()

tools_grid_line = None
for i, line in enumerate(en_lines):
    if '<div class="tools-grid"' in line:
        tools_grid_line = i
        break

if tools_grid_line is None:
    print("ERROR: tools-grid not found in EN index")
    exit(1)

en_cards_html = "\n".join([c["en"] for c in CARDS]) + "\n"
en_lines.insert(tools_grid_line + 1, en_cards_html)

with open(en_path, "w") as f:
    f.writelines(en_lines)
print(f"EN: 插入{len(CARDS)}张卡片在第{tools_grid_line+1}行")
