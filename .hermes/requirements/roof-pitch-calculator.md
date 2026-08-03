# Roof Pitch Calculator - 需求文档

## 1. 需求验证

### 用户是谁？
- **CN用户**: 建筑工人、装修师傅、自建房业主、建筑设计师。术语：屋顶坡度、屋面坡比、坡屋面
- **EN用户**: Roofers, DIY homeowners, contractors, architects. 术语: roof pitch, roof slope, rise/run ratio, pitch angle

### 搜索量估计
- 关键词: "roof pitch calculator" (~90K/month Google), "roof slope calculator" (~15K/month)
- 估计总搜索量: 100K+/month
- 竞品: calculator.net, omnicalculator.com, roofingcalc.com

### 竞品分析
- 竞品1 calculator.net: 功能全但UI老旧，广告多
- 竞品2 omnicalculator.com: 界面好但加载慢，有弹窗
- 我们的优势: 轻量纯前端、无广告干扰、双语支持、移动端友好

### 前端可行性
- [x] 纯前端可实现（三角函数计算）
- [x] 无API依赖
- [x] 无CORS问题
- [x] 无数据隐私风险

## 2. 功能规格

### 核心功能
1. 输入 Rise（垂直高度）和 Run（水平距离），自动计算 Pitch (X:12)、角度(°)、坡度(%)
2. 输入 Pitch (X:12)，反推 Rise、Run、角度、坡度
3. 输入角度(°)，反推所有其他值
4. 根据屋顶面积+坡度，计算实际屋面面积（考虑坡度系数）
5. 屋面板材数量估算（可选）

### 输入参数
- Rise (inches or cm)
- Run (inches or cm, = half of total span)
- Pitch (X:12 format)
- Angle (degrees)
- Roof footprint area (sq ft or m²)

### 输出
- Pitch ratio (X:12)
- Pitch angle (degrees)
- Pitch percentage (slope %)
- Rise value
- Run value
- Rafter length (hypotenuse)
- Roof area multiplier
- Actual roof surface area

### 单位
- 公制 (cm, m²) / 英制 (inches, sq ft) 可切换
