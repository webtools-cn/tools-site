# Firewood Cord Calculator - 需求文档

## 关键词分析
- "firewood cord calculator" — 月搜索量 ~18,000 (US)
- "cord of wood calculator" — 月搜索量 ~12,000
- "how much firewood do I need" — 月搜索量 ~8,000
- "firewood calculator" — 月搜索量 ~15,000
- 总计：~53,000/月，>1000 ✓

## 竞品分析
1. **InchCalculator** — cord计算+face cord换算，但无成本估算
2. **CalculatorPro** — 简单cord计算，无多单位
3. **Forestry.com guide** — 文章型，无交互计算

## 功能清单（差异化）
1. **多形状体积计算**：矩形堆/圆柱堆/任意尺寸堆
2. **Cord单位换算**：cord → face cord → rick → cubic feet → cubic meters
3. **成本估算**：输入每cord价格，计算总成本
4. **冬季需求估算**：根据房屋类型/取暖方式/气候带估算冬季所需cord数
5. **堆叠效率系数**：考虑木柴堆叠紧密程度（紧密堆叠60%实心 vs 松散堆叠40%）
6. **BTU热量对比**：不同木材种类的BTU输出对比表

## 用户场景覆盖
1. 想买firewood的用户，需要知道买多少cord → ✓ 体积计算+需求估算
2. 已有firewood堆，想知道是多少cord → ✓ 体积计算
3. 对比不同卖家的价格 → ✓ 成本估算
4. 了解不同木材的热值 → ✓ BTU对比表
5. 计算face cord和full cord换算 → ✓ 单位换算

## 差异化
- 竞品只有简单cord计算，本工具集成：体积计算+成本估算+冬季需求+BTU对比+堆叠系数
- 深色主题、中英双语
- 纯前端，无后端依赖
