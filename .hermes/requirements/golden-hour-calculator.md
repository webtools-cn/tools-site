# Golden Hour Calculator - 需求文档

## 1. 市场分析
- **关键词**: golden hour calculator, blue hour calculator, sunrise sunset times, magic hour photography
- **月搜索量（估算）**: 20,000+（含长尾）
- **竞品**: PhotoPills($10.99), TPE(free), Golden-Hour.com(free基础), TimeAndDate.com(仅日出日落)
- **差异化**: 免费一站式，包含Golden Hour+Blue Hour+月相+可视化环形图

## 2. 功能清单
### 核心功能
1. **自动定位**: 浏览器GPS获取经纬度，fallback到IP定位
2. **手动定位**: 输入城市名或经纬度
3. **日期选择**: 日历选择任意日期
4. **24小时环形图**: Canvas绘制，显示：
   - 夜晚(深蓝) → 天文晨光(深紫) → 航海晨光(紫) → 民用晨光(浅紫)
   - 日出(橙线) → Golden Hour(金色弧) → 白天(浅蓝)
   - Golden Hour(金色弧) → 日落(橙线)
   - 民用暮光(浅紫) → 航海暮光(紫) → 天文暮光(深紫) → 夜晚(深蓝)
5. **时间表**: 文字列表显示精确时间
   - 日出时间
   - 日落时间
   - Morning Golden Hour (start-end)
   - Evening Golden Hour (start-end)
   - Morning Blue Hour (start-end)
   - Evening Blue Hour (start-end)
6. **月相信息**: 月相图标 + 月升月落时间
7. **太阳高度角**: 当前/选定时间的太阳高度角和方位角

### 可选功能
- 位置保存（localStorage）
- 分享链接（URL参数含坐标和日期）
- 推送提醒（浏览器通知）

## 3. 技术方案
- 纯前端HTML+JS+Canvas
- 天文算法: 自行实现基于NOAA Solar Calculator公式
  - 日出日落: Meeus算法
  - Golden Hour: 太阳在地平线下4°到地平线上6°
  - Blue Hour: 太阳在地平线下8°到地平线下4°
  - 月相: 基于儒略日计算
- GPS: navigator.geolocation API
- Canvas: 24小时环形图（donut chart变体）
- 深色主题: --bg:#0f172a

## 4. 页面设计
- 顶部: 标题 + 位置搜索栏 + 日期选择器
- 中间: Canvas环形时间图（直径~300px）
- 底部: 时间表（卡片式，两列布局）
- 响应式: 移动端单列

## 5. 竞品对比
| 功能 | Golden-Hour.com | PhotoPills | TPE | 我们 |
|------|:---:|:---:|:---:|:---:|
| Golden Hour | ✓ | ✓ | ✓ | ✓ |
| Blue Hour | ✗ | ✓ | ✓ | ✓ |
| 24h可视化 | ✗ | ✓ | ✓ | ✓ |
| 月相 | ✗ | ✓ | ✓ | ✓ |
| 免费 | ✓ | ✗ | 部分 | ✓ |
| 无需安装 | ✓ | ✗ | ✗ | ✓ |
| GPS定位 | ✗ | ✓ | ✓ | ✓ |