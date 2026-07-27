#!/usr/bin/env python3
"""同步新工具到CN+EN首页，更新工具数量"""
import re, os, subprocess

# 脚本在~/tools-site/scripts目录下
base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 5个新工具：CN版卡片HTML
new_cards_cn = '''<div class="tool-card" data-category="金融计算器" data-name="货币市场收益计算器">
<a href="/money-market-calculator/">
<div class="tool-icon">💵</div>
<h3>货币市场收益计算器</h3>
<p>计算货币基金和Money Market账户预期收益</p>
</a>
</div>
<div class="tool-card" data-category="金融计算器" data-name="国债(T-Bill)收益计算器">
<a href="/treasury-bill-calculator/">
<div class="tool-icon">🏛️</div>
<h3>国债(T-Bill)收益计算器</h3>
<p>计算美国短期国库券(T-Bills)贴现收益率、实际年化收益</p>
</a>
</div>
<div class="tool-card" data-category="金融计算器" data-name="HSA vs FSA对比计算器">
<a href="/hsa-vs-fsa-calculator/">
<div class="tool-icon">🏥</div>
<h3>HSA vs FSA对比计算器</h3>
<p>对比美国健康储蓄账户(HSA)与弹性支出账户(FSA)税收优惠</p>
</a>
</div>
<div class="tool-card" data-category="金融计算器" data-name="定期vs终身寿险对比计算器">
<a href="/term-vs-whole-life-calculator/">
<div class="tool-icon">🛡️</div>
<h3>定期vs终身寿险对比计算器</h3>
<p>对比Term Life与Whole Life保费、现金价值与净成本</p>
</a>
</div>
<div class="tool-card" data-category="金融计算器" data-name="大额贷款(Jumbo Loan)计算器">
<a href="/jumbo-loan-calculator/">
<div class="tool-icon">🏘️</div>
<h3>大额贷款(Jumbo Loan)计算器</h3>
<p>超过FHFA限额的高额房贷月供计算，对比普通贷款差异</p>
</a>
</div>
'''

new_cards_en = '''<div class="tool-card" data-category="金融计算器" data-name="Money Market Yield Calculator">
<a href="/en/money-market-calculator/">
<div class="tool-icon">💵</div>
<h3>Money Market Yield Calculator</h3>
<p>Calculate expected returns for money market funds and accounts</p>
</a>
</div>
<div class="tool-card" data-category="金融计算器" data-name="Treasury Bill (T-Bill) Calculator">
<a href="/en/treasury-bill-calculator/">
<div class="tool-icon">🏛️</div>
<h3>Treasury Bill (T-Bill) Calculator</h3>
<p>Calculate discount yield and annualized return of US T-Bills</p>
</a>
</div>
<div class="tool-card" data-category="金融计算器" data-name="HSA vs FSA Comparison Calculator">
<a href="/en/hsa-vs-fsa-calculator/">
<div class="tool-icon">🏥</div>
<h3>HSA vs FSA Comparison Calculator</h3>
<p>Compare Health Savings Account vs Flexible Spending Account tax savings</p>
</a>
</div>
<div class="tool-card" data-category="金融计算器" data-name="Term vs Whole Life Insurance Calculator">
<a href="/en/term-vs-whole-life-calculator/">
<div class="tool-icon">🛡️</div>
<h3>Term vs Whole Life Insurance Calculator</h3>
<p>Compare Term Life and Whole Life premiums, cash value & net cost</p>
</a>
</div>
<div class="tool-card" data-category="金融计算器" data-name="Jumbo Loan Calculator">
<a href="/en/jumbo-loan-calculator/">
<div class="tool-icon">🏘️</div>
<h3>Jumbo Loan Calculator</h3>
<p>Calculate payments for mortgages exceeding FHFA conforming limits</p>
</a>
</div>
'''

# 处理CN首页
cn_path = os.path.join(base, 'index.html')
with open(cn_path, 'r') as f:
    cn = f.read()

# 插入新卡片在第一个金融计算器card之前
anchor = '<div class="tool-card" data-category="金融计算器" data-name="利率换算计算器">'
cn = cn.replace(anchor, new_cards_cn + anchor)

# 更新工具数量：3086→3091
cn = cn.replace('3086+', '3091+')

# 更新title中的数字
cn = re.sub(r'<title>在线小工具矩阵 - \d+\+免费在线工具集合', '<title>在线小工具矩阵 - 3091+免费在线工具集合', cn)

with open(cn_path, 'w') as f:
    f.write(cn)
print("CN首页已更新")

# 处理EN首页
en_path = os.path.join(base, 'en', 'index.html')
with open(en_path, 'r') as f:
    en = f.read()

# EN首页找第一个金融计算器card
anchor_en = '<div class="tool-card" data-category="金融计算器" data-name="'
# 找到第一个金融计算器
idx = en.find(anchor_en)
if idx > 0:
    # 找到这个完整的卡片开始
    en = en[:idx] + new_cards_en + en[idx:]

# 更新工具数量：3081→3086
en = en.replace('3081+', '3086+')

# 更新title中的数字
en = re.sub(r'Tools — PDF, Image, JSON, Text &amp; \d+\+ Developer Utili', 'Tools — PDF, Image, JSON, Text &amp; 3086+ Developer Utili', en)

with open(en_path, 'w') as f:
    f.write(en)
print("EN首页已更新")

print("Done!")
