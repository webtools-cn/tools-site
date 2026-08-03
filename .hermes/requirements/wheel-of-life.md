# Wheel of Life Assessment Tool — 需求文档

## 关键词搜索量
- "wheel of life" — ~8,100/月 (US)
- "life balance wheel" — ~4,400/月
- "wheel of life assessment" — ~2,900/月
- "wheel of life template" — ~1,900/月
- 合计：~17,000+/月

## 竞品分析
1. **wheeloflife.com** — 简单8维度打分，无可视化图表，结果仅文字
2. **tonyrobbins.com wheel of life** — 10维度，需注册，结果发邮件
3. **各种coaching网站** — PDF模板下载，无交互
4. **assessments.momentumcoaching** — 有简单条形图，无雷达图

## 差异化
1. **交互式Canvas雷达图** — 实时绘制，评分变化即时反映
2. **8个标准维度 + 自定义** — 支持用户自定义维度名称
3. **智能分析** — 根据评分自动生成改进建议和优先行动项
4. **双语支持** — 中英文
5. **无需注册** — 纯前端，数据不出浏览器
6. **深色主题** — 与站点风格一致

## 功能清单
1. 8个生活维度评分（0-10分滑块）：
   - Career/事业
   - Finance/财务
   - Health/健康
   - Family/家庭
   - Relationships/人际关系
   - Personal Growth/个人成长
   - Fun & Recreation/休闲
   - Physical Environment/生活环境
2. Canvas实时绘制雷达图
3. 总分计算 + 平均分
4. 最低维度识别 + 改进建议
5. 重置按钮
6. 分享结果（生成摘要文本）
7. 可自定义维度名称

## 用户场景覆盖率
- 场景1: 个人自我评估 ✓
- 场景2: 健身教练客户评估 ✓
- 场景3: 年度复盘 ✓
- 场景4: 团队建设活动 ✓
- 场景5: 心理咨询辅助 ✓
覆盖率：≥90%

## 技术方案
- 纯HTML+CSS+JS，无外部依赖
- Canvas 2D绘制雷达图
- CSS变量深色主题
- 响应式设计（移动端375px）
