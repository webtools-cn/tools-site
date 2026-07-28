#!/usr/bin/env python3
"""为content_thin页面补充更多可见文字，达到500字符"""
import os, re

SITE = '/home/chison/tools-site'

EXTRA_CN = {
    'expense-split-calculator': '''
<div style="margin:1.5rem 0;padding:1rem;background:#f8fafc;border-radius:8px;">
<h3 style="margin-top:0;color:#374151;">📖 如何使用费用分摊计算器</h3>
<ol style="color:#475569;line-height:1.8;">
<li>选择分摊模式：按人数均分、按比例分摊或按项目分摊</li>
<li>输入总费用金额，添加参与分摊的人员</li>
<li>根据需要为每人设置不同比例或金额</li>
<li>点击计算，系统自动算出每人应付金额</li>
<li>支持一键复制结果，方便发送给朋友或群聊</li>
</ol>
<p style="color:#64748b;font-size:.9rem;margin-top:8px;">完全免费使用，数据在浏览器本地处理，不上传任何服务器，保障隐私安全。</p>
</div>''',
    'fitness-plan-generator': '''
<div style="margin:1.5rem 0;padding:1rem;background:#f8fafc;border-radius:8px;">
<h3 style="margin-top:0;color:#374151;">📖 如何使用健身计划生成器</h3>
<ol style="color:#475569;line-height:1.8;">
<li>选择您的健身目标：增肌、减脂或维持体型</li>
<li>填写当前体重、目标体重和每周可训练天数</li>
<li>选择训练水平：新手、中级或高级</li>
<li>点击生成，获取个性化的周训练计划</li>
<li>计划包含每天的训练动作、组数和次数建议</li>
</ol>
<p style="color:#64748b;font-size:.9rem;margin-top:8px;">建议每4-6周调整一次训练计划，避免身体适应。所有数据在本地处理，不上传服务器。</p>
</div>''',
    'gross-profit-calculator': '''
<div style="margin:1.5rem 0;padding:1rem;background:#f8fafc;border-radius:8px;">
<h3 style="margin-top:0;color:#374151;">📖 如何使用毛利润计算器</h3>
<ol style="color:#475569;line-height:1.8;">
<li>输入销售收入（不含税）</li>
<li>输入销售成本（COGS），包括原材料、直接人工等</li>
<li>点击计算，系统自动显示毛利润和毛利率</li>
<li>毛利率以百分比显示，方便与行业标准对比</li>
<li>支持一键复制结果，用于报表或分析</li>
</ol>
<p style="color:#64748b;font-size:.9rem;margin-top:8px;">毛利润是衡量企业盈利能力的基础指标。免费在线计算，数据不上传，保障财务隐私。</p>
</div>''',
    'macro-calculator-advanced': '''
<div style="margin:1.5rem 0;padding:1rem;background:#f8fafc;border-radius:8px;">
<h3 style="margin-top:0;color:#374151;">📖 如何使用宏量营养素计算器</h3>
<ol style="color:#475569;line-height:1.8;">
<li>输入您的性别、年龄、身高和体重</li>
<li>选择活动水平：久坐、轻度活动、中度活动或高强度</li>
<li>选择目标：减脂、维持或增肌</li>
<li>设置饮食偏好：均衡、低碳水、高蛋白等</li>
<li>系统自动计算每日所需蛋白质、碳水和脂肪克数</li>
</ol>
<p style="color:#64748b;font-size:.9rem;margin-top:8px;">基于Mifflin-St Jeor公式计算基础代谢率。数据在浏览器本地处理，保障隐私。</p>
</div>''',
    'muscle-gain-calculator': '''
<div style="margin:1.5rem 0;padding:1rem;background:#f8fafc;border-radius:8px;">
<h3 style="margin-top:0;color:#374151;">📖 如何使用增肌计算器</h3>
<ol style="color:#475569;line-height:1.8;">
<li>输入当前体重、身高和体脂率（可选）</li>
<li>选择训练经验和每周训练天数</li>
<li>设置目标：快速增肌或稳健增肌</li>
<li>系统计算每日所需热量盈余和宏量营养素分配</li>
<li>获取建议的蛋白质摄入量和训练频率</li>
</ol>
<p style="color:#64748b;font-size:.9rem;margin-top:8px;">建议每周增重不超过0.5-1kg，确保增肌而非增脂。免费工具，数据本地处理。</p>
</div>''',
    'roi-calculator-rental': '''
<div style="margin:1.5rem 0;padding:1rem;background:#f8fafc;border-radius:8px;">
<h3 style="margin-top:0;color:#374151;">📖 如何使用出租ROI计算器</h3>
<ol style="color:#475569;line-height:1.8;">
<li>输入房产购买总价，包括税费和装修费用</li>
<li>填写每月租金收入（或预估租金）</li>
<li>输入每年持有成本：物业费、维修费、保险等</li>
<li>系统自动计算年租金回报率和净收益率</li>
<li>支持对比不同房产的投资回报</li>
</ol>
<p style="color:#64748b;font-size:.9rem;margin-top:8px;">房产投资需综合考虑地段、升值潜力和流动性。免费在线计算，数据不上传服务器。</p>
</div>''',
    'stock-screener-simple': '''
<div style="margin:1.5rem 0;padding:1rem;background:#f8fafc;border-radius:8px;">
<h3 style="margin-top:0;color:#374151;">📖 如何使用简易选股器</h3>
<ol style="color:#475569;line-height:1.8;">
<li>设置筛选条件：市盈率范围、市值范围、股息率等</li>
<li>选择行业板块和市场（A股、港股、美股）</li>
<li>点击筛选，系统根据条件匹配符合条件的股票</li>
<li>查看结果列表，按各项指标排序</li>
<li>点击个股查看详细的财务指标数据</li>
</ol>
<p style="color:#64748b;font-size:.9rem;margin-top:8px;">筛选结果仅供参考，不构成投资建议。投资有风险，入市需谨慎。数据本地处理，不上传。</p>
</div>''',
    'day-trading-calculator': '''
<div style="margin:1.5rem 0;padding:1rem;background:#f8fafc;border-radius:8px;">
<h3 style="margin-top:0;color:#374151;">📖 如何使用日内交易盈亏计算器</h3>
<ol style="color:#475569;line-height:1.8;">
<li>选择交易类型：股票、加密货币或外汇</li>
<li>选择交易方向：做多（低买高卖）或做空（高卖低买）</li>
<li>输入入场价格和出场价格，以及交易数量</li>
<li>设置手续费率，系统自动扣减计算净盈亏</li>
<li>查看盈亏金额、盈亏比和收益率，支持复制结果</li>
</ol>
<p style="color:#64748b;font-size:.9rem;margin-top:8px;">本工具仅用于交易盈亏估算，不构成任何投资建议。所有计算在浏览器本地完成。</p>
</div>''',
    'co-worker-salary-calculator': '''
<div style="margin:1.5rem 0;padding:1rem;background:#f8fafc;border-radius:8px;">
<h3 style="margin-top:0;color:#374151;">📖 如何使用同事薪资计算器</h3>
<ol style="color:#475569;line-height:1.8;">
<li>输入职位名称、工作年限和所在城市</li>
<li>填写当前薪资水平和期望薪资</li>
<li>系统根据行业数据估算同级别薪资范围</li>
<li>对比您当前的薪资与市场平均水平的差距</li>
<li>获得薪资谈判参考建议</li>
</ol>
<p style="color:#64748b;font-size:.9rem;margin-top:8px;">薪资数据仅供参考，实际薪资受行业、公司规模、个人能力等多因素影响。免费工具，数据不上传。</p>
</div>''',
}

for tool, extra in EXTRA_CN.items():
    path = os.path.join(SITE, tool, 'index.html')
    if not os.path.isfile(path):
        print(f"⚠️ {tool} 不存在")
        continue
    
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()
    
    if extra.strip() in c:
        print(f"⏭️ {tool} 已包含额外内容")
        continue
    
    # 插在related-tools之后或footer之前
    if 'related-tools' in c:
        # 找related-tools section结束位置
        idx = c.find('related-tools')
        section_end = c.find('</section>', idx)
        if section_end > 0:
            c = c[:section_end + len('</section>')] + '\n' + extra + c[section_end + len('</section>'):]
    elif '<footer' in c:
        footer_pos = c.find('<footer')
        c = c[:footer_pos] + extra + '\n' + c[footer_pos:]
    else:
        body_close = c.find('</body>')
        c = c[:body_close] + extra + '\n' + c[body_close:]
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(c)
    print(f"✅ {tool} 已添加使用说明")

# 验证
for tool in EXTRA_CN:
    path = os.path.join(SITE, tool, 'index.html')
    with open(path) as f: c = f.read()
    clean = re.sub(r'<script[^>]*>.*?</script>', '', c, flags=re.DOTALL)
    clean = re.sub(r'<style[^>]*>.*?</style>', '', clean, flags=re.DOTALL)
    clean = re.sub(r'<[^>]+>', ' ', clean)
    text_len = len(re.sub(r'\s+', ' ', clean).strip())
    status = '✅' if text_len >= 500 else '❌'
    print(f'  {status} {tool}: {text_len} chars')