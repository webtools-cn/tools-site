# 需求文档：利弊分析器 (Pros and Cons List Maker)

## 工具名称
pros-and-cons-list

## 搜索量验证
- "pros and cons list" 月搜索量 5000+
- "pros and cons maker" 月搜索量 2000+
- "pros and cons template" 月搜索量 8000+
- 竞品：proscons.com, tally.so, 各种简单工具
- 差异化：加权评分 + 可视化对比 + 导出功能

## 功能描述
在线利弊分析器，帮助用户列出某个决定的优势和劣势，支持：
1. 添加/删除/编辑优点和缺点条目
2. 为每条设置权重（重要性1-5星）
3. 自动计算总分对比
4. 可视化进度条显示利弊平衡
5. 导出为文本/图片
6. 支持多个选项对比

## 技术可行性
- 纯前端HTML+JS，零后端
- 无需API，无CORS问题
- localStorage保存数据
- Canvas导出图片

## 验收标准
- 功能：添加条目→设置权重→查看对比→导出
- 视觉：布局正常、移动端375px不崩
- 语言：EN英文自然、无中文
- SEO：有Schema、无假评分
