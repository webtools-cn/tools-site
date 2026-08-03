# Insulation Calculator - 需求文档

## 1. 需求验证

### 用户是谁？
- **CN用户**: 装修工人、自建房业主、节能改造工程人员，计算房屋保温层所需保温棉/保温板面积、厚度对应的R值和包数
- **EN用户**: DIY homeowners, insulation contractors, energy auditors calculating batt/roll insulation coverage, R-value requirements, and number of bags/batts needed

### 搜索量估计
- 关键词: "insulation calculator", "r-value calculator", "how much insulation do I need"
- 估计总搜索量: 30,000+/月（英文为主）
- 竞品: calculator.net, inchcalculator.com, homedepot.com insulation calculator

### 竞品分析
- 竞品1: calculator.net - 功能全但界面老旧，无R值对比
- 竞品2: inchcalculator.com - 有面积计算但缺多区域汇总
- 我们的优势: 支持多区域汇总、R值计算、公制英制切换、包数估算、浪费率设置

### 前端可行性
- [x] 纯前端可实现
- [x] 无API依赖
- [x] 无CORS问题
- [x] 无数据隐私风险

## 2. 功能规格

### 核心功能
1. 输入墙体/天花板/地面面积，选择保温材料类型和R值，计算所需保温材料覆盖面积和包数
2. 支持矩形和L型区域面积计算
3. 支持浪费率设置（默认10%）
4. 公制/英制单位切换
5. 多区域汇总

### 交互元素（≥3）
- 面积输入（长×宽自动计算 or 直接输入面积）
- 保温材料类型选择（Fiberglass batt, Mineral wool, Spray foam, Rigid foam等）
- R值选择/自定义
- 浪费率输入
- 单价输入（可选）
- 计算结果输出（面积、包数、成本）
- 多区域添加

### 技术方案
- 纯前端HTML+CSS+JS
- CSS变量暗色主题，与站点一致
- Schema.org SoftwareApplication + FAQPage

## 3. EN版本差异
- 英文用自然语言描述，非直译
- 英文版默认英制单位
- 术语用美国建筑业标准用语

## 4. 验收标准
- [x] 输入数据→输出正确
- [x] 布局正常、移动端375px不崩
- [x] EN版英文自然、无中文
- [x] 有Schema、无假评分、推荐相关
