# Wire Size Calculator (电线尺寸计算器) 需求文档

## 一、关键词分析
- **主关键词**: "wire size calculator" — 预估月搜索量 15K-30K（全球）
- **次关键词**: "wire gauge calculator", "AWG calculator", "electrical wire size calculator", "cable size calculator"
- **中文关键词**: "电线尺寸计算器", "导线截面积计算", "电缆选型计算器"
- **竞争度**: 中等（有计算器站点但大多功能单一）

## 二、竞品分析
1. **calculatorsoup.com** — 只算电压降，不推荐AWG规格
2. **omnicalculator.com** — 功能较全但界面复杂，加载慢
3. **southwire.com** — 厂商站，偏宣传
4. **electricaltechnology.org** — 有表格但交互差

## 三、功能清单
1. ✅ 根据电流(A) + 电压(V) + 距离(ft/m) + 电压降百分比(%) → 推荐AWG规格
2. ✅ 支持铜线/铝线选择
3. ✅ 支持单相/三相电路
4. ✅ 显示推荐线径的：AWG号、直径(mm)、截面积(mm²)、电阻(Ω/km)
5. ✅ 电压降计算结果
6. ✅ NEC标准载流量参考表
7. ✅ 同时推荐满足载流量和电压降两个条件的最小AWG
8. ✅ 公制/英制单位切换

## 四、用户场景
1. 电工/DIY爱好者布线时确定电线规格 — 80%
2. 工程师设计电路时快速验证 — 10%
3. 学生学习电气工程 — 10%

## 五、差异化
- **双条件验证**: 同时检查载流量(ampacity)和电压降(voltage drop)，取更大值
- **NEC标准数据**: 内置完整NEC Table 310.16载流量数据
- **AWG↔mm²对照**: 双标准显示（美国AWG + 国际mm²）
- **无广告干扰的计算体验**: 纯前端，即时结果

## 六、技术方案
- 纯前端JS，NEC AWG数据表内置
- 公式: VD = 2 × L × I × R / 1000（单相）, VD = √3 × L × I × R / 1000（三相）
- R = 电阻率(Ω/km) × 长度(km)
- 铜电阻率: 0.0175 Ω·mm²/m, 铝: 0.0282 Ω·mm²/m
