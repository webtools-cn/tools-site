#!/usr/bin/env python3
"""给5个CN工具页补充info-box（FAQ + 使用说明），解决content_thin/very_thin"""
import os, re

BASE = '/home/chison/tools-site'

INFO_BOXES = {
    'cat-age-calculator': '''<div class="info-box">
      <h2>📖 猫咪年龄换算规则</h2>
      <ul>
        <li><strong>第1年</strong> = 人类15岁（快速成长期，完成疫苗接种）</li>
        <li><strong>第2年</strong> = 人类24岁（相当于+9岁，性成熟期）</li>
        <li><strong>第3年起</strong> = 每年+4岁（成年稳定期）</li>
        <li>室内猫平均寿命12-18年（人类64-88岁），室外猫寿命较短约5-8年</li>
        <li>猫咪6个月≈人类10岁，1岁≈15岁，2岁≈24岁</li>
      </ul>
    </div>
    <div class="info-box">
      <h2>❓ 常见问题</h2>
      <p><strong>Q: 为什么猫咪第1年等于人类15岁？</strong></p>
      <p>A: 猫咪在第一年内经历幼猫到青少年的快速发育，骨骼和器官成熟速度远超人类。研究显示猫咪1岁时生理成熟度接近人类15岁。</p>
      <p><strong>Q: 不同品种的猫寿命有差异吗？</strong></p>
      <p>A: 有。暹罗猫、缅甸猫等东方品种平均寿命较长（15-20年），而波斯猫等扁脸品种平均12-15年。混血猫通常更健康长寿。</p>
    </div>''',

    'cocktail-recipe-generator': '''<div class="info-box">
      <h2>📖 鸡尾酒基酒知识</h2>
      <ul>
        <li><strong>伏特加</strong>：无色无味，最百搭的基酒，适合Mojito、Cosmopolitan等</li>
        <li><strong>金酒</strong>：杜松子风味，清新草本香，代表：Martini、Gin Tonic</li>
        <li><strong>朗姆酒</strong>：甘蔗酿造，甜润，分白朗姆和黑朗姆，代表：Daiquiri、Mojito</li>
        <li><strong>龙舌兰</strong>：墨西哥特产，植物香气，代表：Margarita、Tequila Sunrise</li>
        <li><strong>威士忌</strong>：谷物酿造，醇厚复杂，代表：Old Fashioned、Manhattan</li>
        <li><strong>白兰地</strong>：葡萄蒸馏，优雅果香，代表：Sidecar、Alexander</li>
      </ul>
    </div>
    <div class="info-box">
      <h2>❓ 常见问题</h2>
      <p><strong>Q: 初学者适合从哪款鸡尾酒开始？</strong></p>
      <p>A: 推荐Mojito（莫吉托）和Gin Tonic（金汤力），配料简单、容错率高、口感清爽易接受。</p>
      <p><strong>Q: 没有专业调酒工具怎么办？</strong></p>
      <p>A: 可用带盖水杯代替摇酒壶，筷子代替搅拌棒，普通杯子即可。关键是比例和冰块要充足。</p>
    </div>''',

    'coffee-ratio-calculator': '''<div class="info-box">
      <h2>📖 咖啡冲泡比例指南</h2>
      <ul>
        <li><strong>手冲咖啡</strong>：粉水比 1:15-1:17（如15g粉配225-255ml水），口感均衡</li>
        <li><strong>法压壶</strong>：粉水比 1:12-1:15，粗研磨，浸泡4分钟</li>
        <li><strong>意式浓缩</strong>：粉水比 1:2-1:3（18g粉出36-54ml浓缩液）</li>
        <li><strong>冷萃咖啡</strong>：粉水比 1:4-1:8（浓缩液），冷藏浸泡12-24小时后稀释饮用</li>
        <li><strong>摩卡壶</strong>：粉水比 1:5-1:7，中细研磨，小火加热</li>
      </ul>
    </div>
    <div class="info-box">
      <h2>❓ 常见问题</h2>
      <p><strong>Q: 为什么同样的比例味道不一样？</strong></p>
      <p>A: 咖啡风味还受研磨度、水温（推荐90-96°C）、萃取时间和咖啡豆新鲜度影响。建议每次只调整一个变量。</p>
      <p><strong>Q: SCA金杯标准是什么？</strong></p>
      <p>A: SCA（精品咖啡协会）推荐粉水比1:15-1:18，萃取率18-22%，浓度1.15-1.35%，这个范围内口感最佳。</p>
    </div>''',

    'currency-bill-counter': '''<div class="info-box">
      <h2>📖 人民币面值知识</h2>
      <ul>
        <li><strong>第五套人民币</strong>：面值有100元、50元、20元、10元、5元、1元纸币，以及1元、5角、1角硬币</li>
        <li><strong>100元纸币</strong>：红色，正面毛泽东头像，背面人民大会堂</li>
        <li><strong>50元纸币</strong>：绿色，正面毛泽东头像，背面布达拉宫</li>
        <li><strong>20元纸币</strong>：棕色，正面毛泽东头像，背面桂林山水</li>
        <li><strong>10元纸币</strong>：蓝黑色，正面毛泽东头像，背面长江三峡</li>
        <li><strong>5元纸币</strong>：紫色，正面毛泽东头像，背面泰山</li>
        <li><strong>1元纸币</strong>：橄榄绿，正面毛泽东头像，背面西湖三潭印月</li>
      </ul>
    </div>
    <div class="info-box">
      <h2>❓ 常见问题</h2>
      <p><strong>Q: 如何快速点钞？</strong></p>
      <p>A: 银行常用手法有单指单张、多指多张和扇面点钞。日常使用按面值分类后逐叠计数最快。</p>
      <p><strong>Q: 硬币怎么计算最方便？</strong></p>
      <p>A: 建议先将硬币按面值分类，每10枚叠一摞，然后计数摞数乘以面值。1元硬币100枚正好100元。</p>
    </div>''',

    'ingredient-substitute-finder': '''<div class="info-box">
      <h2>📖 常用食材替代指南</h2>
      <ul>
        <li><strong>鸡蛋替代</strong>：1个鸡蛋 = 1/4杯苹果泥 或 1汤匙亚麻籽粉+3汤匙水（适合烘焙）</li>
        <li><strong>黄油替代</strong>：1杯黄油 = 1杯椰子油 或 3/4杯植物油（烘焙中可减量）</li>
        <li><strong>牛奶替代</strong>：1杯牛奶 = 1杯豆浆/杏仁奶/燕麦奶（烹饪和烘焙均可）</li>
        <li><strong>面粉替代</strong>：1杯中筋面粉 = 1杯全麦面粉（口感略粗）或 7/8杯米粉（无麸质）</li>
        <li><strong>糖替代</strong>：1杯白糖 = 3/4杯蜂蜜（减液体）或 1杯椰子糖（低GI）</li>
        <li><strong>奶油替代</strong>：1杯奶油 = 1杯椰奶（冷藏后取凝固部分）或 1杯希腊酸奶</li>
      </ul>
    </div>
    <div class="info-box">
      <h2>❓ 常见问题</h2>
      <p><strong>Q: 食材替代会影响口感吗？</strong></p>
      <p>A: 会有些许差异。一般来说，同类替代（如不同植物油之间）影响较小，跨类替代（如用苹果泥替代鸡蛋）会改变质地和风味。</p>
      <p><strong>Q: 什么情况下不建议替代？</strong></p>
      <p>A: 对结构要求严格的烘焙（如马卡龙、舒芙蕾）不建议大幅替代。普通家常菜和简易烘焙替代空间较大。</p>
    </div>''',
}

fixed = 0
for tool, info_html in INFO_BOXES.items():
    fpath = os.path.join(BASE, tool, 'index.html')
    with open(fpath) as f:
        content = f.read()
    
    # 检查是否已有info-box（已有的跳过）
    if content.count('class="info-box"') >= 2:
        print(f"⏭️  {tool} — 已有info-box")
        continue
    
    # 在</main>之前插入info-box（放在已有info-box之后或main末尾）
    # 找到最后一个info-box后面或</main>前面
    if 'class="info-box"' in content:
        # 在最后一个info-box的</div>之后插入新info-box
        last_info_end = content.rfind('class="info-box"')
        # 找到该div的结束位置
        depth = 0
        pos = last_info_end
        for i in range(pos, len(content)):
            if content[i:i+6] == '<div c' or content[i:i+5] == '<div>':
                # 找对应</div>
                pass
        # 简化：直接在</main>前插入
        content = content.replace('</main>', f'\n{info_html}\n</main>')
    else:
        # 没有任何info-box，在</main>前插入
        content = content.replace('</main>', f'\n{info_html}\n</main>')
    
    with open(fpath, 'w') as f:
        f.write(content)
    fixed += 1
    print(f"✅ {tool} — 已添加info-box")

print(f"\n共修复: {fixed}个")