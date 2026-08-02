# Percentage Calculator - 需求文档

## 1. 需求验证

### 用户是谁？
- **CN用户**: 学生、财务人员、购物者（算折扣）、上班族（算涨薪幅度）
- **EN用户**: Students, shoppers (sales discounts), finance workers, tip calculators, data analysts

### 搜索量估计
- 关键词: percentage calculator, percent calculator, discount calculator, percentage change, tip calculator, percentage of, what is X% of Y
- 估计总搜索量: 50万+/月 (全球)
- 竞品: calculator.net, omnicalculator.com, calculatorsoup.com, rapidtables.com

### 竞品分析
- calculator.net: 功能全但UI老旧，广告多
- omnicalculator.com: 功能好但加载慢，太多JS
- rapidtables.com: 简洁但功能单一
- 我们的优势: 极速加载、干净UI、一个页面覆盖多种百分比计算、移动端优先

### 前端可行性
- [x] 纯前端可实现
- [x] 无API依赖
- [x] 无CORS问题
- [x] 无数据隐私风险

## 2. 功能规格

### 核心功能（5合1）
1. **X is what % of Y** - 占比计算（最常见的搜索）
2. **What is X% of Y** - 百分比值计算
3. **% increase/decrease** - 百分比变化（涨跌幅）
4. **Discount calculator** - 折扣计算（原价→折后价）
5. **Tip calculator** - 小费计算（EN版特色）

### 交互元素（≥3）
- 数字输入框 x 多个
- 百分比滑块
- 实时结果显示
- 一键复制结果
- 预设场景按钮（如10%/20%/50%快速选择）

### 技术方案
- 纯JS计算，无依赖
- CSS变量主题
- 响应式布局
- 实时计算（输入即出结果）
- 历史记录（localStorage保存最近计算）

## 3. EN版本差异
- Tip calculator 仅EN版有（CN无小费文化）
- EN版默认$符号，CN版默认¥符号
- EN版折扣用 "XX% OFF" 标签，CN版用 "打X折"

## 4. 验收标准
- [x] 输入数据→输出正确
- [x] 布局正常、移动端375px不崩
- [x] EN版英文自然、无中文
- [x] 有Schema、无假评分