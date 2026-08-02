# HTML表格生成器 — 需求文档

## 1. 关键词分析
- 关键词：`html table generator`, `online table creator`, `html表格生成器`
- 估算月搜索量：~15K-30K（英文为主，"html table generator"是开发者常用搜索）
- 竞品：htmltable.com, rapidtables.com, tablesgenerator.com

## 2. 竞品分析
| 竞品 | 优势 | 劣势 |
|:-----|:-----|:-----|
| htmltable.com | 简洁 | 功能少、无样式自定义 |
| rapidtables.com | 功能多 | 广告多、UI老旧 |
| tablesgenerator.com | LaTeX支持 | 体验差、弹窗多 |

## 3. 差异化
- **深色主题**：开发者友好的暗色界面（竞品都是浅色）
- **实时双向同步**：表格编辑↔HTML代码实时互转（竞品大多是单向）
- **单元格合并**：可视化选择区域合并（竞品需要手动输colspan/rowspan）
- **样式预设**：5种预设表格样式一键切换
- **无广告干扰**：干净体验（竞品全是广告）

## 4. 用户场景
1. 开发者快速生成HTML表格代码 → 粘贴到项目中
2. 内容创作者制作文章中的表格 → 导出HTML
3. Markdown用户需要HTML兼容表格 → 生成代码
4. 初学者学习HTML表格语法 → 可视化理解

## 5. 功能清单
- ✅ 行列数设置（滑块+输入框）
- ✅ 可视化网格编辑（点击编辑单元格内容）
- ✅ 单元格合并（拖选区域→合并/拆分）
- ✅ 表头行设置（勾选第一行是否为th）
- ✅ 5种预设样式切换（简洁/条纹/边框/暗色/紧凑）
- ✅ 实时HTML代码预览
- ✅ 一键复制HTML代码
- ✅ 导入/导出CSV数据
- ✅ 响应式（移动端可用）

## 6. 技术方案
- 纯HTML+CSS+JS，零依赖
- Canvas/table渲染双模（编辑用table，预览用渲染）
- 深色主题：#0f172a背景
- 所有操作在浏览器本地完成

## 7. SEO标题
- CN: HTML表格生成器 - 在线可视化表格编辑器 | Free ToolBase
- EN: HTML Table Generator - Visual Table Builder Online | Free ToolBase