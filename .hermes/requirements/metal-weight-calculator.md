# 金属重量计算器 (Metal Weight Calculator) - 需求文档

## 1. 需求验证

### 用户是谁？
- **CN用户**: 机械加工、金属制造、钢结构工程师、五金采购员，需要根据金属型材尺寸快速估算重量
- **EN用户**: Metal fabricators, machinists, engineers, purchasing managers, DIY makers who need to estimate metal weight from dimensions

### 搜索量估计
- 关键词: "metal weight calculator", "steel weight calculator", "aluminum weight calculator"
- 估计总搜索量: 30,000+/月 (metal weight calculator ~12K, steel weight calculator ~8K, aluminum weight ~5K)
- 竞品: omnicalculator.com, giessereilexikon.com, calculatorsoup.com, goodcalculators.com

### 竞品分析
- 竞品1: omnicalculator.com/metal-weight — 支持多种型材，但界面复杂、广告多
- 竞品2: goodcalculators.com/metal-weight-calculator — 仅支持基本形状，无材质对比
- 竞品3: calculatorsoup.com — 仅支持钢板，型材种类少
- 我们的优势: 深色主题、支持7种型材×12种金属材质、实时计算、批量件数计算、公制/英制切换

### 前端可行性
- [x] 纯前端可实现（重量 = 体积 × 密度，纯数学计算）
- [x] 无API依赖
- [x] 无CORS问题
- [x] 无数据隐私风险

## 2. 功能规格

### 核心功能
1. 选择金属材质（钢、不锈钢、铝、铜、黄铜、青铜、锌、铅、钛、铸铁、镁、银）
2. 选择型材形状（圆棒、方棒、六角棒、圆管、方管、钢板/板材、角钢）
3. 输入尺寸参数，自动计算单件重量和总重量
4. 输入件数计算总重量
5. 公制(mm) / 英制(inch) 单位切换

### 交互元素（≥3）
- 材质下拉选择
- 型材形状选择
- 尺寸输入框（根据形状动态变化）
- 件数输入
- 单位制切换
- 重置按钮
- 复制结果按钮

### 技术方案
- 密度表硬编码在JS中（g/cm³）
- 体积公式按形状计算
- 重量 = 体积 × 密度 × 件数
- 公制: mm输入 → cm³体积 → g重量 → kg
- 英制: inch输入 → in³体积 → lb重量

## 3. EN版本差异
- 标题/description/FAQ全部英文
- 单位: 英制模式显示 lb/ft
- 材质名: Steel, Stainless Steel, Aluminum, Copper, Brass, Bronze, Zinc, Lead, Titanium, Cast Iron, Magnesium, Silver

## 4. 验收标准
- [x] 输入数据→输出正确（手工验证：钢圆棒直径50mm长1000mm = 15.4kg）
- [x] 布局正常、移动端375px不崩
- [x] EN版英文自然、无中文
- [x] 有Schema(SoftwareApplication+FAQ+Breadcrumb+HowTo)、无假评分、推荐相关
