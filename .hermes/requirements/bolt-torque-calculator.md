# Bolt Torque Calculator - 需求文档

## 1. 需求验证

### 用户是谁？
- **CN用户**: 机械工程师、装配工人、设备维修人员，需要计算螺栓拧紧扭矩以确保连接可靠
- **EN用户**: Mechanical engineers, maintenance technicians, assembly workers who need to calculate proper bolt tightening torque

### 搜索量估计
- 关键词: "bolt torque calculator", "torque calculator"
- 估计总搜索量: ~15000/月 (EN), ~3000/月 (CN)
- 竞品: engineersedge.com, boltscience.com, engineeringtoolbox.com

### 竞品分析
- 竞品1: engineersedge.com — 功能全但UI老旧，移动端不友好
- 竞品2: boltscience.com — 专业但需注册才能用部分功能
- 竞品3: engineeringtoolbox.com — 简单但只有基本公式
- 我们的优势: 现代UI、移动端友好、无需注册、中英双语、支持公制/英制切换、批量计算

### 前端可行性
- [x] 纯前端可实现（T = K × D × F 公式纯数学）
- [x] 无API依赖
- [x] 无CORS问题
- [x] 无数据隐私风险

## 2. 功能规格

### 核心功能
1. 输入螺栓直径、目标夹紧力、螺母系数(K)→计算所需扭矩
2. 输入扭矩→反算夹紧力
3. 支持公制(mm/N·m)和英制(in/lbf·ft)单位切换
4. 内置常见螺母系数参考表（干燥钢-钢=0.20, 润滑=0.15等）
5. 内置常见螺栓等级的保证载荷参考
6. 批量计算模式：输入多个螺栓规格一次计算

### 交互元素（≥3）
- 螺栓直径输入 + 单位选择
- 夹紧力/扭矩输入 + 模式切换（正算/反算）
- 螺母系数选择（下拉+自定义）
- 实时计算结果输出
- 批量表格输入

### 技术方案
- T = K × D × F (Torque = Nut Factor × Bolt Diameter × Clamp Force)
- 单位转换：1 N·m = 0.737562 lbf·ft, 1 mm = 0.0393701 in
- 纯JS数学计算，Canvas/无外部依赖

## 3. EN版本差异
- 英文使用 "Bolt Torque Calculator" 标题
- 螺母系数参考表用英文术语
- 单位用 imperial/metric 表述

## 4. 验收标准
- [ ] 输入数据→输出正确（验证公式 T=K×D×F）
- [ ] 布局正常、移动端375px不崩
- [ ] EN版英文自然、无中文
- [ ] 有Schema、无假评分
