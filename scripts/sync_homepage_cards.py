#!/usr/bin/env python3
"""同步首页卡片 - 为10个新工具添加中英文首页卡片"""
import re

BASE = '/home/chison/tools-site'

# 10个新工具
new_tools = [
    ('dns-lookup-tool', 'developer-tools', '🌐', 'DNS记录查询', '在线查询域名DNS记录，支持A/AAAA/CNAME/MX/NS/TXT类型', 'DNS Lookup Tool', 'Query DNS records online, supports A/AAAA/CNAME/MX/NS/TXT types'),
    ('robots-txt-parser', 'seo-tools', '🤖', 'Robots.txt解析器', '在线解析robots.txt，可视化Allow/Disallow规则，测试URL爬取权限', 'Robots.txt Parser', 'Parse robots.txt online, visualize Allow/Disallow rules, test URL crawlability'),
    ('kubernetes-yaml-validator', 'developer-tools', '☸️', 'K8s YAML验证器', '在线验证Kubernetes YAML配置，检查Deployment/Service/Pod格式', 'K8s YAML Validator', 'Validate Kubernetes YAML configs, check Deployment/Service/Pod format'),
    ('word-counter-online', 'text-tools', '📝', '在线字数统计', '统计文本字数/字符/行数/段落，中英文混合计数，阅读时间估算', 'Word Counter Online', 'Count words/chars/lines/paragraphs, CJK-aware, reading time estimation'),
    ('icalendar-generator', 'utility', '📅', 'iCalendar生成器', '在线生成.ics日历文件，支持Google Calendar/Outlook导入', 'iCalendar Generator', 'Generate .ics calendar files, import to Google Calendar/Outlook'),
    ('svg-to-css', 'developer-tools', '🎯', 'SVG转CSS背景', '将SVG转换为CSS background-image的data URI，优化压缩', 'SVG to CSS Background', 'Convert SVG to CSS background-image data URI, optimized'),
    ('traceroute-online', 'developer-tools', '🛤️', '在线路由追踪', '可视化路由追踪，查看数据包经过的网络节点和延迟', 'Traceroute Online', 'Visual traceroute, see network hops and latency times'),
    ('port-checker', 'developer-tools', '🔌', '端口检测工具', '在线检测端口开放状态，支持常见端口列表快速扫描', 'Port Checker', 'Check port status online, common ports list quick scan'),
    ('content-security-policy-generator', 'seo-tools', '🛡️', 'CSP策略生成器', '在线生成Content-Security-Policy，可视化配置防XSS策略', 'CSP Generator', 'Generate Content-Security-Policy, visually configure XSS protection'),
    ('ssl-certificate-checker', 'seo-tools', '🔒', 'SSL证书检查器', '在线检查SSL/TLS证书详情，颁发者/有效期/加密算法', 'SSL Certificate Checker', 'Check SSL/TLS certificate details, issuer/validity/encryption'),
]

# 生成CN卡片
cn_cards = []
en_cards = []
for tool_id, cat, icon, cn_name, cn_desc, en_name, en_desc in new_tools:
    cn_card = f'<div class="tool-card" data-cat="{cat}"><span class="tool-icon">{icon}</span><span class="tool-name">{cn_name}</span><span class="tool-desc">{cn_desc}</span><a href="{tool_id}/" class="btn">立即使用</a></div>'
    en_card = f'<div class="tool-card" data-cat="{cat}"><span class="tool-icon">{icon}</span><span class="tool-name">{en_name}</span><span class="tool-desc">{en_desc}</span><a href="/en/{tool_id}/" class="btn">Use Now</a></div>'
    cn_cards.append(cn_card)
    en_cards.append(en_card)

# 插入到CN首页 - 找到 tools-grid 闭合前
with open(f'{BASE}/index.html', 'r') as f:
    cn_content = f.read()

# 找 tools-grid 的结束位置
# 用 tools-grid 的最后一个闭合 </div>
import re
grid_start = cn_content.find('class="tools-grid"')
# 从grid_start开始找闭合的</div>
depth = 0
i = grid_start
while i < len(cn_content):
    if cn_content[i:i+4] == '<div':
        depth += 1
        i += 4
    elif cn_content[i:i+5] == '</div':
        depth -= 1
        if depth == 0:
            grid_end = i
            break
        i += 5
    else:
        i += 1

cn_new = cn_content[:grid_end] + '\n' + '\n'.join(cn_cards) + '\n' + cn_content[grid_end:]

with open(f'{BASE}/index.html', 'w') as f:
    f.write(cn_new)
print(f'CN首页: 已插入 {len(cn_cards)} 个卡片')

# 插入到EN首页
with open(f'{BASE}/en/index.html', 'r') as f:
    en_content = f.read()

grid_start = en_content.find('class="tools-grid"')
depth = 0
i = grid_start
while i < len(en_content):
    if en_content[i:i+4] == '<div':
        depth += 1
        i += 4
    elif en_content[i:i+5] == '</div':
        depth -= 1
        if depth == 0:
            grid_end = i
            break
        i += 5
    else:
        i += 1

en_new = en_content[:grid_end] + '\n' + '\n'.join(en_cards) + '\n' + en_content[grid_end:]

with open(f'{BASE}/en/index.html', 'w') as f:
    f.write(en_new)
print(f'EN首页: 已插入 {len(en_cards)} 个卡片')

# 验证
cn_count = en_new.count('tool-card')
# 重新读取验证
with open(f'{BASE}/index.html') as f:
    cn_count = f.read().count('tool-card')
with open(f'{BASE}/en/index.html') as f:
    en_count = f.read().count('tool-card')
print(f'CN卡片: {cn_count}, EN卡片: {en_count}')
if cn_count == en_count:
    print('✅ 首页卡片数一致')
else:
    print(f'❌ 不一致！差{abs(cn_count-en_count)}张')