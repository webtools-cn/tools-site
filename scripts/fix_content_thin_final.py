#!/usr/bin/env python3
"""修复最后4个content_thin残留 - 补充FAQ区域增加厚度"""
import re, os

BASE = '/home/chison/tools-site'

FAQ_CONTENT = {
    'basis-point-calculator': '''<section class="info-section" style="margin-top:24px;padding:16px;background:#f8fafc;border-radius:8px;border:1px solid #e2e8f0">
<h2 style="font-size:1.1rem;color:#334155;margin-top:0">❓ 常见问题</h2>
<h3 style="font-size:.95rem;color:#475569;margin:12px 0 4px">基点和百分比怎么换算？</h3>
<p style="color:#64748b;font-size:.85rem;line-height:1.5;margin:0 0 12px">1基点 = 0.01%。例如25个基点 = 0.25%。将百分比乘以100即可得到基点数。</p>
<h3 style="font-size:.95rem;color:#475569;margin:12px 0 4px">什么时候用基点？</h3>
<p style="color:#64748b;font-size:.85rem;line-height:1.5;margin:0">央行利率调整、债券收益率变动、贷款利差、基金管理费率等场景通常使用基点表示，避免小数混淆。</p>
</section>''',
    'breakeven-analysis-calculator': '''<section class="info-section" style="margin-top:24px;padding:16px;background:#f8fafc;border-radius:8px;border:1px solid #e2e8f0">
<h2 style="font-size:1.1rem;color:#334155;margin-top:0">❓ 常见问题</h2>
<h3 style="font-size:.95rem;color:#475569;margin:12px 0 4px">盈亏平衡点公式是什么？</h3>
<p style="color:#64748b;font-size:.85rem;line-height:1.5;margin:0 0 12px">盈亏平衡点 = 固定成本 ÷ (单价 - 单位变动成本)。结果是需要销售的单位数量。</p>
<h3 style="font-size:.95rem;color:#475569;margin:12px 0 4px">盈亏平衡分析有什么用？</h3>
<p style="color:#64748b;font-size:.85rem;line-height:1.5;margin:0">帮助企业确定最低销售量、制定定价策略、评估成本结构合理性，是商业计划书的必备分析。</p>
</section>''',
    'how-much-house-can-i-afford': '''<section class="info-section" style="margin-top:24px;padding:16px;background:#f8fafc;border-radius:8px;border:1px solid #e2e8f0">
<h2 style="font-size:1.1rem;color:#334155;margin-top:0">❓ 常见问题</h2>
<h3 style="font-size:.95rem;color:#475569;margin:12px 0 4px">买房需要准备多少首付？</h3>
<p style="color:#64748b;font-size:.85rem;line-height:1.5;margin:0 0 12px">国内首套房首付比例通常20%-30%，二套房30%-60%。首付越高，月供越低。</p>
<h3 style="font-size:.95rem;color:#475569;margin:12px 0 4px">月供占收入多少合适？</h3>
<p style="color:#64748b;font-size:.85rem;line-height:1.5;margin:0">一般建议月供不超过家庭月收入的30%-40%。银行审批通常要求月供不超过收入的50%。</p>
</section>''',
    'pregnancy-week-calculator': '''<section class="info-section" style="margin-top:24px;padding:16px;background:#f8fafc;border-radius:8px;border:1px solid #e2e8f0">
<h2 style="font-size:1.1rem;color:#334155;margin-top:0">❓ 常见问题</h2>
<h3 style="font-size:.95rem;color:#475569;margin:12px 0 4px">预产期怎么算？</h3>
<p style="color:#64748b;font-size:.85rem;line-height:1.5;margin:0 0 12px">预产期 = 末次月经日期 + 280天（40周）。这是Naegele法则的标准计算方法。</p>
<h3 style="font-size:.95rem;color:#475569;margin:12px 0 4px">孕周和怀孕周数一样吗？</h3>
<p style="color:#64748b;font-size:.85rem;line-height:1.5;margin:0">孕周从末次月经第一天算起，比实际受孕时间早约2周。这是医学标准计算方法，B超会根据胎儿大小进行调整。</p>
</section>''',
}

fixed_count = 0
for tool, faq_html in FAQ_CONTENT.items():
    fpath = os.path.join(BASE, tool, 'index.html')
    with open(fpath, 'r') as f:
        content = f.read()
    
    if '常见问题' in content:
        print(f"⏭️  {tool}: FAQ已存在")
        continue
    
    # 插入到第一个info-section的</section>之后
    first_section_end = content.find('</section>')
    if first_section_end > 0:
        content = content[:first_section_end + len('</section>')] + '\n' + faq_html + content[first_section_end + len('</section>'):]
    else:
        content = content.replace('</main>', faq_html + '\n</main>')
    
    with open(fpath, 'w') as f:
        f.write(content)
    
    # 验证
    clean = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL)
    clean = re.sub(r'<style[^>]*>.*?</style>', '', clean, flags=re.DOTALL)
    clean = re.sub(r'<[^>]+>', ' ', clean)
    text_len = len(re.sub(r'\s+', ' ', clean).strip())
    print(f"✅ {tool}: {text_len} 字符")
    fixed_count += 1

print(f"\n修复: {fixed_count} 个页面")