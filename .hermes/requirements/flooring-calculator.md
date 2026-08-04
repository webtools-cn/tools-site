# Flooring Calculator 需求文档

## 1. 关键词分析
- **主关键词**: "flooring calculator" — 月搜索量估计 15,000+ (calculator.net, inchcalculator.com均有此工具，属高频装修计算器)
- **次要关键词**: "how much flooring do i need", "flooring cost calculator", "laminate flooring calculator", "vinyl plank calculator"
- **中文关键词**: "地板计算器", "地板用量计算", "铺地板计算"

## 2. 竞品分析
| 竞品 | URL | 功能 |
|:-----|:----|:-----|
| Calculator.net | calculator.net/flooring-calculator.html | 房间面积、废料率、箱数、成本 |
| InchCalculator | inchcalculator.com/flooring-calculator/ | 面积、片数、箱数、废料、成本 |
| OmniCalculator | omnicalculator.com/construction/flooring | 多房间、多地板类型、废料、成本 |

## 3. 功能清单
1. 输入房间尺寸（长×宽），支持添加多个房间
2. 选择地板类型（硬木/复合板/瓷砖/卷材/SPC）
3. 输入地板规格（单片长×宽 或 每箱覆盖面积）
4. 废料率调整（5%-20%，默认10%）
5. 计算总面积
6. 计算所需片数/箱数（含废料）
7. 成本估算（单价+总价）
8. 公制/英制单位切换
9. SVG可视化房间+地板布局
10. 安装提示（方向建议、过渡条等）

## 4. 用户场景
| 场景 | 覆盖率 |
|:-----|:-------|
| DIY户主计算客厅需要多少箱复合地板 | ✓ |
| 承包商估算多房间地板材料 | ✓ |
| 计算瓷砖铺设所需片数 | ✓ |
| 估算地板项目总成本 | ✓ |
| 计算含废料的实际采购量 | ✓ |

覆盖率：100%

## 5. 差异化
- 竞品大多只算面积+箱数，本工具增加：
  1. 多房间支持（逐个添加，汇总）
  2. 按片计算（输入单片尺寸，算总片数）+ 按箱计算（输入每箱面积）
  3. SVG可视化地板铺设方向示意
  4. 安装专业提示（铺设方向、过渡条、防潮层等）
  5. 5种地板类型预设
  6. 中英双语

## 6. 技术方案
- 纯前端HTML+JS+CSS
- 深色主题 (--bg:#0f172a)
- SVG可视化
- 无外部依赖
