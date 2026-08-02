# RAL Color Converter - 需求文档

## 1. 需求验证

### 用户是谁？
- **CN用户**: 工业设计师、油漆工、制造业采购人员，需要将RAL色号转换为HEX/RGB用于数字设计
- **EN用户**: European/US industrial designers, painters, architects needing RAL-to-digital conversion

### 搜索量估计
- 关键词: "RAL color converter", "RAL to HEX", "RAL to RGB", "RAL color chart"
- 估计总搜索量: 25K-35K/月
- 竞品: ralcolor.com, ralcolors.com, ralchart.com

### 竞品分析
- ralcolor.com: 颜色全但UI老旧，广告多
- ralcolors.com: 颜色数据准确但加载慢
- 我们的优势: 纯前端快速加载，中英双语，同时支持搜索和浏览

### 前端可行性
- [x] 纯前端可实现（静态颜色数据）
- [x] 无API依赖
- [x] 无CORS问题
- [x] 无数据隐私风险

## 2. 功能规格

### 核心功能
1. RAL Classic颜色列表展示（约213种颜色），可搜索/筛选
2. 点击任意颜色显示详细信息：RAL编号、英文名、中文名、HEX、RGB、CMYK
3. RAL编号搜索、颜色名称搜索
4. 复制颜色代码（HEX/RGB）

### 交互元素（≥3）
- 搜索框（按RAL编号或名称搜索）
- 颜色网格（点击选择）
- 复制按钮（HEX、RGB、CMYK各自复制）
- 颜色分类筛选（黄/橙/红/紫/蓝/绿/灰/棕/白黑）

### 技术方案
- RAL Classic颜色数据静态内置（约213种）
- 每个颜色：RAL编号、英文名、中文名、HEX、RGB、CMYK
- Vanilla JS实现搜索、筛选、复制功能
- CSS Grid展示颜色卡片

## 3. EN版本差异
- 颜色名称使用英文官方名称
- UI文本全部英文
- 搜索支持英文颜色名

## 4. 验收标准
- [x] 输入RAL编号→显示对应颜色和代码
- [x] 颜色搜索正常工作
- [x] 布局正常、移动端375px不崩
- [x] EN版英文自然、无中文
- [x] 有Schema、无假评分