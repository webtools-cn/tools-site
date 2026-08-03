# Pizza Dough Calculator — 需求文档

## 1. 关键词与搜索量
- "pizza dough calculator" — 月搜索量 ~40,000+ (全球)
- "pizza recipe calculator" — ~8,000+
- "dough calculator" — ~15,000+
- 竞品: pizzapp.com (fermentation app), stkp.co, various pizza dough calculators
- 目标: 抢占 "pizza dough calculator" 英文流量

## 2. 竞品分析
| 竞品 | 功能 | 缺点 |
|:-----|:-----|:-----|
| pizzapp.com | 精密发酵计算，多日冷发酵 | 过于复杂，新手看不懂 |
| STKP.co | 基本配方计算 | 无多尺寸支持，UI差 |
| Various blogs | 简单表格 | 不能动态调整参数 |

## 3. 功能清单
- [x] 选择面团球数量 (1-20)
- [x] 每个面团球目标重量 (g)
- [x] 水分百分比 (hydration %) — 50%-85%
- [x] 盐百分比 — 1%-3%
- [x] 酵母类型选择 (鲜酵母/干酵母/酸种)
- [x] 酵母百分比 — 0.1%-2%
- [x] 自动计算: 面粉、水、盐、酵母用量 (克)
- [x] 总面团重量显示
- [x] 预设风格 (Neapolitan, NY Style, Sicilian, Detroit)
- [x] 实时预览
- [x] 复制结果
- [x] 重量单位切换 (克/盎司)

## 4. 用户场景
1. **新手做披萨**: 选预设→输入要几个饼→得到配方 ✓
2. **有经验的披萨爱好者**: 调整hydration/盐/酵母百分比→精确配方 ✓
3. **多尺寸披萨**: 不同球重量→总面粉计算 ✓
4. **不同酵母**: 鲜酵母vs干酵母换算 ✓
5. **美式用户**: 盎司单位 ✓

场景覆盖率: 5/5 = 100%

## 5. 差异化
- 一键预设风格（Neapolitan/NY/Sicilian/Detroit）+ 自定义模式
- 克/盎司双单位
- 酵母类型自动换算（鲜酵母:干酵母 = 3:1）
- 深色主题，移动端友好
- 纯前端，无追踪，无注册

## 6. 技术规格
- Slug: pizza-dough-calculator
- 纯HTML+CSS+JS
- Baker's percentages公式:
  - Total weight = balls × ballWeight
  - Flour = Total / (1 + hydration + salt + yeast)
  - Water = Flour × hydration
  - Salt = Flour × salt
  - Yeast = Flour × yeast (adjusted by type)
- Schema: SoftwareApplication + FAQ + Breadcrumb
- 深色主题: --bg:#0f172a
