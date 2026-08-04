# 债务还清计算器 (Debt Payoff Calculator) 需求文档

## 关键词分析
- **主关键词**: "debt payoff calculator" — 月搜索量估计 40K-100K（高搜索量金融工具）
- **次关键词**: "debt snowball calculator", "debt avalanche calculator", "debt repayment calculator"
- **中文关键词**: "债务还清计算器", "债务雪球计算器", "还款计划计算器"

## 竞品分析
1. **NerdWallet Debt Payoff Calculator** — 支持雪球/雪崩法，有可视化，但需要注册
2. **Bankrate Debt Payoff Calculator** — 基础计算，无策略对比
3. **Calculator.net Debt Payoff Calculator** — 支持多债务，无可视化对比

## 功能清单
1. ✅ 添加多笔债务（名称、余额、利率、最低还款额）
2. ✅ 选择还款策略：雪球法（先还小额）vs 雪崩法（先还高利率）
3. ✅ 输入每月可用的总还款金额
4. ✅ 计算每种策略的：总还款时间、总利息、总支付金额
5. ✅ 两种策略对比表
6. ✅ 逐月还款时间线（可视化进度条）
7. ✅ 添加/删除债务行
8. ✅ 导出还款计划（文本格式下载）

## 用户场景覆盖
1. 用户有多张信用卡债务 → 添加多笔，选策略对比 ✅
2. 用户有信用卡+学生贷款+车贷 → 混合债务类型 ✅
3. 用户想知道每月多还多少钱能省多少利息 → 调整月还款额 ✅
4. 用户想知道哪种策略更快还清 → 两种策略对比 ✅
5. 用户想看逐月还款计划 → 时间线展示 ✅

## 差异化
- **双策略对比**：大多数竞品只支持一种，我们同时展示两种策略的结果
- **可视化时间线**：逐月进度条，直观看到每笔债务何时还清
- **纯前端**：数据不上传，隐私安全
- **无注册**：直接使用

## 技术要求
- 纯前端 HTML+JS，无后端
- 深色主题：--bg:#0f172a --card-bg:#1e293b --text:#e2e8f0 --primary:#06b6d4
- 交互元素 ≥ 3
- Schema: SoftwareApplication + FAQ + Breadcrumb
- AdSense + GA 在 head
- 移动端 375px 不崩
