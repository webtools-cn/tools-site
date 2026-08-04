# Retaining Wall Calculator 需求文档

## 1. 关键词分析
- **主关键词**: "retaining wall calculator" — 月搜索量估计 12,000+ (基于竞品inchcalculator.com, calculator.net均有此工具)
- **次要关键词**: "retaining wall blocks calculator", "retaining wall material calculator", "how many blocks for retaining wall"
- **中文关键词**: "挡土墙计算器", "挡土墙材料计算"

## 2. 竞品分析
| 竞品 | URL | 功能 |
|:-----|:----|:-----|
| InchCalculator | inchcalculator.com/retaining-wall-calculator/ | 块数计算、碎石回填、沙子计算、成本估算 |
| Calculator.net | calculator.net/retaining-wall-calculator | 基础块数+面积 |
| Omnicalculator | omnicalculator.com/construction/retaining-wall | 块数、成本、多种块型 |

## 3. 功能清单
1. 输入墙长、墙高
2. 选择块材类型（标准砌块、景观块、互锁块）或自定义块尺寸
3. 计算所需块数（含损耗率）
4. 计算墙面积和体积
5. 计算碎石/砾石回填量（墙后排水层）
6. 计算沙子/基底材料量
7. 成本估算（块材单价+碎石+沙子）
8. 公制/英制单位切换
9. SVG可视化墙体布局
10. 建筑规范提示（墙高超过120cm建议工程师设计）

## 4. 用户场景
| 场景 | 覆盖率 |
|:-----|:-------|
| DIY户主建花园挡土墙 | ✓ |
| 景观承包商估算材料 | ✓ |
| 确定需要多少块景观砖 | ✓ |
| 估算挡土墙项目成本 | ✓ |
| 计算排水碎石用量 | ✓ |

覆盖率：100%

## 5. 差异化
- 竞品大多只算块数，本工具增加：
  1. 碎石排水层计算（挡土墙关键需求）
  2. SVG可视化布局
  3. 沙子基底计算
  4. 建筑规范安全提示
  5. 多种块材预设+自定义
  6. 中英双语

## 6. 技术方案
- 纯前端HTML+JS+CSS
- 深色主题 (--bg:#0f172a)
- SVG可视化
- 无外部依赖
