#!/usr/bin/env python3
"""批量添加10个新工具的首页卡片（中英文）+ 更新数字 + sitemap"""
import re, os

BASE = '/home/chison/tools-site'

# 10个新工具卡片数据 (格式: cn_name, en_name, cn_desc, en_desc, category, emoji, slug)
TOOLS = [
    ('REM↔PX转换器', 'REM↔PX Converter', '免费在线REM与PX双向转换器，支持自定义根字体大小，实时换算。前端开发必备。', 'Free online REM↔PX converter. Custom root font size, real-time conversion. Essential for frontend devs.', 'dev-tools', '📐', 'rem-to-pixel'),
    ('域名Typo生成器', 'Domain Typo Generator', '免费在线域名Typo生成器，输入域名自动生成键盘误触、遗漏字母等Typo变体。网络安全测试必备。', 'Free online domain typo generator. Generate keyboard slip, missing letter, and swapped letter variants from any domain.', 'security-tools', '⌨️', 'domain-typo-generator'),
    ('子网掩码计算器', 'Subnet Mask Calculator', '免费在线子网掩码计算器，输入IP/CIDR计算网络地址、广播地址、可用主机数。网络工程师必备。', 'Free online subnet mask calculator. Calculate network address, broadcast, usable hosts from IP/CIDR. Network engineer essential.', 'network-tools', '🌐', 'subnet-mask-calc'),
    ('API速率限制计算器', 'API Rate Limiter Calculator', '免费在线API速率限制计算器，分析固定窗口、令牌桶、滑动窗口策略。后端架构设计参考。', 'Free online API rate limiter calculator. Analyze fixed window, token bucket, sliding window strategies for backend design.', 'dev-tools', '⚡', 'api-rate-limiter-calc'),
    ('CSS优先级计算器', 'CSS Specificity Calculator', '免费在线CSS选择器优先级计算器，计算ID/Class/Element权重值。前端开发排错必备。', 'Free online CSS specificity calculator. Calculate ID/Class/Element weight for any selector. Frontend debugging essential.', 'dev-tools', '🎯', 'css-specificity-calc'),
    ('RSS转JSON转换器', 'RSS to JSON Converter', '免费在线RSS/Atom转JSON工具，粘贴XML自动解析为结构化JSON。数据集成必备。', 'Free online RSS/Atom to JSON converter. Paste XML, get structured JSON. Essential for data integration.', 'dev-tools', '📡', 'rss-to-json'),
    ('SQL差异对比', 'SQL Diff Compare', '免费在线SQL差异对比工具，逐行对比两个SQL版本。数据库迁移和Code Review必备。', 'Free online SQL diff tool. Compare two SQL versions line by line. Essential for DB migration and code review.', 'dev-tools', '🗄️', 'sql-diff'),
    ('假身份生成器', 'Fake Identity Generator', '免费在线假身份信息生成器，支持中/美/英/日多国格式。生成姓名/地址/电话/邮箱，测试数据必备。', 'Free online fake identity generator. Supports China/US/UK/Japan formats. Generate names, addresses, phones, emails for testing.', 'utility-tools', '🪪', 'fake-identity-generator'),
    ('CI/CD配置生成器', 'CI/CD Pipeline Generator', '免费在线CI/CD配置生成器，支持GitHub Actions/GitLab CI/Jenkins。可视化选择阶段，一键生成YAML。', 'Free online CI/CD pipeline config generator. Supports GitHub Actions, GitLab CI, Jenkins. Visual stage selector, one-click YAML.', 'dev-tools', '🚀', 'cicd-pipeline-generator'),
    ('HTML颜色解析器', 'HTML Color Parser', '免费在线颜色值解析器，支持HEX/RGB/HSL互转。实时预览色块，前端设计必备。', 'Free online color value parser. HEX/RGB/HSL conversion with live color preview. Essential for frontend design.', 'design-tools', '🎨', 'html-color-picker'),
]

# ==== CN首页处理 ====
cn_path = os.path.join(BASE, 'index.html')
with open(cn_path) as f:
    cn = f.read()

# 找最后一个tool-card在grid中的位置（在</div></div>闭合之前）
# 策略：找'代码缩进格式化'卡片后面的 </div></div>
marker = '代码缩进格式化'
idx = cn.rfind(marker)
if idx < 0:
    print('ERROR: 找不到CN首页标记位置')
else:
    # 从这往后找第一个 </div></div>
    after = cn[idx:]
    end_div = after.find('</div>')
    end_div2 = after.find('</div>', end_div+6)
    # 插入点在第二个</div>之后？不对，我们要在第一个</div>（卡片自身闭合）之后、第二个</div>（grid闭合）之前
    insert_pos = idx + end_div + 6  # 卡片自身</div>之后
    
    # 构建新卡片HTML
    cards_html = ''
    for cn_name, en_name, cn_desc, en_desc, cat, emoji, slug in TOOLS:
        cards_html += f'<div class="tool-card" data-cat="{cat}"><span class="tool-icon">{emoji}</span><span class="tool-name">{cn_name}</span><span class="tool-desc">{cn_desc}</span><a href="/{slug}/" class="btn">立即使用</a></div>\n'
    
    new_cn = cn[:insert_pos] + cards_html + cn[insert_pos:]
    with open(cn_path, 'w') as f:
        f.write(new_cn)
    print(f'CN首页: 插入10个卡片 OK')

# ==== EN首页处理 ====
en_path = os.path.join(BASE, 'en/index.html')
with open(en_path) as f:
    en = f.read()

# 找最后一个英文tool-card的位置
marker_en = 'Indent Formatter'  # 英文版最后一个工具可能是这个
idx_en = en.rfind(marker_en)
if idx_en < 0:
    # 尝试找 'code indent'
    idx_en = en.rfind('indent')
    if idx_en < 0:
        # 找倒数第二个 </div></div> 模式
        print('WARNING: 用备用方式定位EN首页')
        # 找 tools-grid 闭合
        grid_start = en.find('class="tools-grid"')
        after_grid = en[grid_start:]
        # 找连续两个</div>，中间没有<div（grid+外层容器闭合）
        import re as regex
        matches = list(regex.finditer(r'</div>\s*</div>\s*</div>', after_grid))
        if matches:
            last_close = matches[-1].start() + grid_start
            # 往前找最后一个卡片闭合
            before = en[:last_close]
            insert_pos_en = before.rfind('</div>') + 6
        else:
            print('ERROR: 找不到EN首页插入位置')
            insert_pos_en = -1
    else:
        after_en = en[idx_en:]
        end_div_en = after_en.find('</div>')
        insert_pos_en = idx_en + end_div_en + 6
else:
    after_en = en[idx_en:]
    end_div_en = after_en.find('</div>')
    insert_pos_en = idx_en + end_div_en + 6

if insert_pos_en > 0:
    # 构建英文卡片HTML
    en_cards_html = ''
    for cn_name, en_name, cn_desc, en_desc, cat, emoji, slug in TOOLS:
        en_cards_html += f'<div class="tool-card" data-cat="{cat}"><span class="tool-icon">{emoji}</span><span class="tool-name">{en_name}</span><span class="tool-desc">{en_desc}</span><a href="/en/{slug}/" class="btn">Use Now</a></div>\n'
    
    new_en = en[:insert_pos_en] + en_cards_html + en[insert_pos_en:]
    with open(en_path, 'w') as f:
        f.write(new_en)
    print(f'EN首页: 插入10个卡片 OK')
else:
    print('ERROR: EN首页插入失败')

print('\nDone!')