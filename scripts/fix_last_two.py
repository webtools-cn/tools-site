#!/usr/bin/env python3
"""给最后2个content_thin页面补充FAQ块"""
import os, re

SITE = '/home/chison/tools-site'

for tool, faq in [
    ('expense-split-calculator', '''
<div style="margin:1.5rem 0;padding:1rem;background:#eff6ff;border-radius:8px;">
<h3 style="margin-top:0;color:#1d4ed8;">❓ 费用分摊常见问题</h3>
<p style="color:#475569;line-height:1.8;"><strong>问：如何处理有人不参与某笔消费？</strong><br>答：可使用按项目分摊模式，只为参与该项目的成员分配费用。</p>
<p style="color:#475569;line-height:1.8;"><strong>问：能否处理多次消费合并分摊？</strong><br>答：可以，每次添加一笔消费，所有消费自动汇总后统一分摊。</p>
<p style="color:#475569;line-height:1.8;"><strong>问：计算结果是否包含税费？</strong><br>答：税费已包含在输入的总金额中，系统按您输入的金额直接计算。</p>
</div>'''),
    ('roi-calculator-rental', '''
<div style="margin:1.5rem 0;padding:1rem;background:#eff6ff;border-radius:8px;">
<h3 style="margin-top:0;color:#1d4ed8;">❓ 出租回报率常见问题</h3>
<p style="color:#475569;line-height:1.8;"><strong>问：租金回报率高就是好投资吗？</strong><br>答：不一定，还需考虑房产升值潜力、地段、空置率等综合因素。</p>
<p style="color:#475569;line-height:1.8;"><strong>问：应该用年租金除以什么价格？</strong><br>答：建议使用含税费和装修的总投入成本，更能反映真实回报。</p>
<p style="color:#475569;line-height:1.8;"><strong>问：净收益率和毛收益率有什么区别？</strong><br>答：净收益率扣除了物业费、维修费等持有成本，更能反映实际到手收益。</p>
</div>'''),
]:
    path = os.path.join(SITE, tool, 'index.html')
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()
    
    if faq.strip() in c:
        continue
    
    if 'related-tools' in c:
        idx = c.find('related-tools')
        section_end = c.find('</section>', idx)
        c = c[:section_end + len('</section>')] + '\n' + faq + c[section_end + len('</section>'):]
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(c)
    
    # verify
    clean = re.sub(r'<script[^>]*>.*?</script>', '', c, flags=re.DOTALL)
    clean = re.sub(r'<style[^>]*>.*?</style>', '', clean, flags=re.DOTALL)
    clean = re.sub(r'<[^>]+>', ' ', clean)
    text_len = len(re.sub(r'\s+', ' ', clean).strip())
    status = '✅' if text_len >= 500 else '❌'
    print(f'{status} {tool}: {text_len} chars')