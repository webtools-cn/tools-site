# 溶液稀释计算器 (Solution Dilution Calculator) - 需求文档

## 1. 需求验证

### 用户是谁？
- **CN用户**: 实验室研究员、学生（高中/大学化学/生物课）、质检人员、医药配制人员
- **EN用户**: Lab technicians, chemistry/biology students, pharmacists, homebrewers, DIY cleaner makers

### 搜索量估计
- 关键词: "dilution calculator", "solution dilution calculator", "C1V1 C2V2 calculator", "稀释计算器"
- 估计总搜索量: "dilution calculator" ~40K/月 (EN), "稀释计算" ~5K/月 (CN), C1V1相关长尾~10K/月
- 竞品: OmniCalculator, Sigma-Aldrich, Tocris, EndMemo

### 竞品分析
- 竞品1 (OmniCalculator dilution): 功能全UI好 / 广告多、加载慢
- 竞品2 (Sigma-Aldrich): 权威 / 界面老旧、只有一种模式
- 竞品3 (Tocris): 简洁 / 只支持molarity、无mass模式
- 我们的优势: 三种模式(浓度稀释/摩尔稀释/质量稀释)、纯前端秒开、中英双语、移动端友好

### 前端可行性
- [x] 纯前端可实现（纯数学公式 C1V1=C2V2）
- [x] 无API依赖
- [x] 无CORS问题
- [x] 无数据隐私风险

## 2. 功能规格

### 核心功能
1. **浓度稀释模式**: C1×V1 = C2×V2，输入任意3个值求第4个
2. **摩尔浓度稀释**: M1×V1 = M2×V2，支持mol/L和mmol/L
3. **质量/体积稀释**: 计算需要加多少溶剂
4. **稀释倍数计算**: 显示稀释比（如1:10）
5. **单位转换**: mL/L、g/mg、mol/mmol

### 交互元素（≥3）
- 输入框（C1, V1, C2, V2 四个值，留空一个自动计算）
- 单位下拉选择
- 计算按钮
- 结果显示（含稀释倍数、需添加溶剂量）
- 快速示例按钮

### 技术方案
- 纯JS数学计算，C1V1=C2V2 公式
- 留空的字段自动计算
- 实时验证输入

## 3. EN版本差异
- 英文术语: "Stock concentration", "Final concentration", "Stock volume", "Final volume"
- 示例用英文场景: "Dilute 5M NaCl to 500mL of 0.5M solution"
- 无中文残留

## 4. 验收标准
- [x] 输入数据→输出正确
- [x] 布局正常、移动端375px不崩
- [x] EN版英文自然、无中文
- [x] 有Schema、无假评分、推荐相关
