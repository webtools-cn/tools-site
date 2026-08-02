# Natural Language Date Parser - 需求文档

## 1. 需求验证

### 用户是谁？
- 开发者：快速解析自然语言日期，得到timestamp/ISO格式
- 普通用户：想知道"下周五"是什么日期、"2周前"是哪天
- 国际化用户：不同时区的日期解析

### 搜索量估计
- 关键词: "date calculator", "days from now", "what date is 30 days from today", "natural language date parser", "date to timestamp"
- 竞品关键词: "what date will it be in 3 weeks", "date duration calculator"
- 估计全球月搜索量: 100万+（包含各类日期计算）

### 竞品分析
- timeanddate.com: 功能全但UI老旧，广告多
- calculator.net/date-calculator: 功能有限
- 我们的优势: 自然语言输入 + 实时预览 + 多种输出格式 + 极简UI

### 前端可行性
- [x] 纯前端可实现
- [x] 无API依赖
- [x] 无CORS问题
- [x] 无数据隐私风险

## 2. 功能规格

### 核心功能
1. **自然语言输入**: 支持 "today", "tomorrow", "next Friday", "2 weeks from now", "3 months ago" 等
2. **相对日期计算**: "X days/weeks/months/years from now/ago"
3. **精确日期输出**: 自动显示 ISO 8601, Unix timestamp, 可读格式
4. **日期差计算**: "days between date1 and date2"
5. **倒计时**: 到目标日期的天数/小时

### 交互元素（≥5）
- 文本输入框（自然语言）
- 实时解析结果展示区
- 多格式输出切换（ISO / Timestamp / Human）
- 快捷预设按钮（Today, Tomorrow, Next Week, 30 days）
- 复制按钮（一键复制各格式）

### 技术方案
- 纯JS日期解析，基于原生Date API
- 自定义NLP微型解析器（正则+规则）
- 深色主题
- 响应式布局
- 实时解析（输入即出结果）

## 3. 差异化
- 支持中英文混合自然语言（"下周五"、"next Friday"）
- 多格式一键输出
- 比竞品更快的响应（纯前端，无服务器往返）
- 移动端优化

## 4. 验收标准
- [ ] 输入数据→输出正确
- [ ] 布局正常、移动端375px不崩
- [ ] EN版英文自然、无中文
- [ ] 有Schema、无假评分
- [ ] 交互元素≥3
- [ ] 浏览器实测通过