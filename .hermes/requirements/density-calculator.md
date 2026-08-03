# 密度计算器 (Density Calculator) - 需求文档

## 1. 需求验证

### 用户是谁？
- **CN用户**: 初高中学生（物理/化学课），大学理工科学生，工程师，质量检测人员
- **EN用户**: Middle/high school students, college STEM students, engineers, quality control technicians

### 搜索量估计
- 关键词: "density calculator", "density formula calculator", "mass volume density"
- 估计总搜索量: 22,000+/月（英文），5,000+/月（中文）
- 竞品: calculatorsoup.com, omnicalculator.com, calculator.net

### 竞品分析
- 竞品1: CalculatorSoup - 功能全但界面老旧，有广告
- 竞品2: Omni Calculator - 界面好但过于复杂，加载慢
- 我们的优势: 界面简洁现代，三模式切换（密度/质量/体积），内置常见物质密度表，中英双语，无广告

### 前端可行性
- [x] 纯前端可实现
- [x] 无API依赖
- [x] 无CORS问题
- [x] 无数据隐私风险

## 2. 功能规格

### 核心功能
1. 三种计算模式：
   - 求密度 (ρ = m/V)
   - 求质量 (m = ρ × V)
   - 求体积 (V = m/ρ)
2. 单位选择：质量(kg/g/mg/lb/oz)、体积(m³/cm³/mL/L/gal)
3. 常见物质密度参考表（一键填充）
4. 结果自动换算显示多种单位

### 交互元素（≥3）
- 模式切换标签页
- 数值输入框 + 单位下拉选择
- 物质参考表（点击填充密度值）
- 计算结果展示区
- 复制结果按钮

### 技术方案
- 纯HTML/CSS/JS，无外部依赖
- CSS变量定义主题色
- 内置常见物质密度数据（约30种）
- 单位换算全部在JS中完成

## 3. EN版本差异
- 标题/描述/标签全部英文
- 物质名称用英文（如 "Water" 而非 "水"）
- 单位标签用英文（如 "Kilograms" 而非 "千克"）
- FAQ内容针对英文用户场景

## 4. 验收标准
- [x] 输入数据→输出正确
- [x] 布局正常、移动端375px不崩
- [x] EN版英文自然、无中文
- [x] 有Schema、无假评分、推荐相关
