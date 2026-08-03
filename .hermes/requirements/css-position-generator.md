# CSS Position Generator 需求文档

## 工具名称
css-position-generator

## 关键词分析
- "css position" — 月搜索量约 30,000+（Google全球）
- "position absolute relative" — 月搜索量约 12,000+
- "css position generator" — 月搜索量约 3,000+
- "position sticky" — 月搜索量约 8,000+
- 目标关键词：css position generator, css position visualizer

## 竞品分析
1. **W3Schools CSS Position** — 仅教程文字，无可视化交互
2. **CSS-Tricks position** — 文章型，无可视化工具
3. **MDN position** — 文档型，有简单demo但不可配置
4. **一些小型online tools** — 功能简单，只能展示一种定位

## 功能清单
1. 五种position模式可视化：static/relative/absolute/fixed/sticky
2. 可配置 top/right/bottom/left 偏移值（滑块+数字输入）
3. 可配置 z-index
4. 可视化容器（父元素）和定位元素（子元素）
5. 实时CSS代码生成（带语法高亮）
6. 一键复制CSS代码
7. 预设场景：居中定位、固定导航栏、sticky header、绝对定位覆盖
8. 可切换父容器 position（relative/absolute/fixed）来演示定位上下文
9. 暗色主题，符合站点规范

## 用户场景
1. 前端开发者学习CSS position五种模式 — 覆盖率100%
2. 开发者需要快速生成position CSS代码 — 覆盖率100%
3. 开发者需要理解absolute相对哪个父元素定位 — 覆盖率100%
4. 开发者需要测试sticky/fixed效果 — 覆盖率100%
5. 开发者需要理解z-index层叠 — 覆盖率80%

## 差异化
1. **可视化交互**：不是纯文本教程，而是可拖拽/可配置的实时可视化
2. **父容器position切换**：大多数工具只能展示一种，本工具可切换父容器position来演示定位上下文
3. **预设场景**：一键加载常见用例（居中、固定导航、sticky header等）
4. **深色主题**：与站点整体风格一致
5. **代码实时生成**：所见即所得的CSS代码输出

## 覆盖率评估
≥80%，可以开发。
