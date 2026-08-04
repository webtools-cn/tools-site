# Siding Calculator 需求文档

## 1. 关键词分析
- **主关键词**: "siding calculator" — 月搜索量估计 8,000-12,000 (基于inchcalculator.com, calculator.net均有此工具，且为高频DIY/建筑工具)
- **次要关键词**: "vinyl siding calculator", "siding square footage calculator", "how much siding do I need", "siding estimator"
- **中文关键词**: "壁板计算器", "外墙板计算器", "挂板计算器"

## 2. 竞品分析
| 竞品 | URL | 功能 |
|:-----|:----|:-----|
| InchCalculator | inchcalculator.com/siding-calculator/ | 面积计算、浪费系数、方形/板条数量、成本估算 |
| Calculator.net | calculator.net/siding-calculator | 基础面积+浪费系数+成本 |
| HomeAdvisor | homeadvisor.com/cost/ | 成本估算导向，不计算材料 |

## 3. 功能清单
1. 输入墙面尺寸（长×高，多面墙）
2. 扣除门窗面积（可添加多个开口）
3. 三角形山墙面积计算（屋顶下斜面）
4. 浪费系数设置（默认10%）
5. 支持多种壁板类型（乙烯基/木质/纤维水泥/金属）
6. 按板条尺寸（宽×长）计算需要板条数
7. 按"方形"(10ft×10ft=100sqft)单位计算
8. 成本估算（材料单价+人工单价）
9. 公制/英制单位切换
10. SVG可视化墙面布局
11. 建筑规范提示

## 4. 用户场景
| 场景 | 覆盖率 |
|:-----|:-------|
| DIY户主估算全屋壁板用量 | ✓ |
| 承包商报价材料清单 | ✓ |
| 单面墙修补材料估算 | ✓ |
| 含山墙面复杂墙面计算 | ✓ |
| 不同材料成本对比 | ✓ |

覆盖率 > 90%

## 5. 差异化
- 竞品大多只支持单面墙或简单面积，本工具支持多面墙+多个门窗扣除+山墙面积
- SVG可视化墙面布局，直观显示
- 公制/英制双单位切换（竞品多数只有英制）
- 实时成本估算含材料+人工
- 支持自定义板条尺寸，不限预设

## 6. 技术方案
- 纯前端HTML+JS，零后端
- 深色主题 (--bg:#0f172a)
- SVG可视化
- 中英双语
