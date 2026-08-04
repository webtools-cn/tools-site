# MPG Calculator - 需求文档

## 1. 需求验证

### 用户是谁？
- **CN用户**: 需要将MPG换算为L/100km的车主、进口车买家、自驾游规划者
- **EN用户**: 美国车主计算车辆燃油效率(MPG)、比较车辆油耗、规划出行油费

### 搜索量估计
- 关键词: "mpg calculator", "gas mileage calculator", "fuel efficiency calculator"
- 估计总搜索量: 500,000+/月 (美国市场为主)
- 竞品: calculator.net, omnicalculator.com, fuel-economy.gov

### 竞品分析
- 竞品1: calculator.net MPG calculator — 功能全但界面老旧
- 竞品2: omnicalculator.com — 界面好但广告多
- 我们的优势: 暗色主题现代UI、支持MPG↔L/100km双向换算、无需注册、移动端友好

### 前端可行性
- [x] 纯前端可实现
- [x] 无API依赖
- [x] 无CORS问题
- [x] 无数据隐私风险

## 2. 功能规格

### 核心功能
1. 输入行驶距离(英里/公里)和消耗燃油(加仑/升)，计算MPG
2. 输入MPG和距离，计算所需燃油量和油费
3. MPG ↔ L/100km 双向换算

### 交互元素（≥3）
- 距离输入 + 单位选择
- 燃油量输入 + 单位选择  
- 油价输入(可选)
- 结果自动计算显示
- MPG↔L/100km 换算表

### 技术方案
- 纯JS数学计算
- 1 MPG = 235.215 L/100km (换算公式)
- 1 US gallon = 3.78541 L, 1 mile = 1.60934 km

## 3. EN版本差异
- 英文界面，美国习惯单位(gallon/mile)为主
- 英文FAQ和说明
- 英文Schema

## 4. 验收标准
- [ ] 输入数据→输出正确
- [ ] 布局正常、移动端375px不崩
- [ ] EN版英文自然、无中文
- [ ] 有Schema、无假评分、推荐相关
