# 订阅费用计算器 - 需求文档

## 1. 需求验证

### 用户是谁？
- **CN用户**: 有多个订阅服务（视频/音乐/云盘等）的人，想知道总花费
- **EN用户**: People with Netflix/Spotify/Amazon Prime etc, tracking total subscription spend

### 搜索量估计
- 关键词: subscription cost calculator, subscription tracker
- 估计总搜索量: 5000+/月
- 竞品: 多数是App，网页版少且功能简单

### 竞品分析
- 竞品1: 各种App - 需下载注册
- 我们的优势: 纯前端无需注册，预设常见订阅服务，支持自定义

### 前端可行性
- [x] 纯前端可实现
- [x] 无API依赖
- [x] 无CORS问题

## 2. 功能规格

### 核心功能
1. 添加订阅项（名称/月费/年费/计费周期）
2. 预设常见服务快捷添加（Netflix/Spotify/iCloud等）
3. 汇总：月总支出/年总支出/日均支出，可视化占比

### 交互元素（≥3）
- 添加订阅按钮+表单
- 订阅列表（可编辑/删除）
- 汇总结果卡片+饼图

## 3. 验收标准
- [ ] 添加/删除订阅→汇总正确
- [ ] 布局正常、移动端不崩
- [ ] EN版英文自然
- [ ] 有Schema
