# Flashcard Generator · 需求文档

## 1. 关键词搜索量分析
- "flashcard generator" — ~5,000-10,000 月搜索量（估算）
- "flashcard maker" — ~8,000-15,000 月搜索量（估算）  
- "free flashcard maker" — ~3,000-5,000 月搜索量（估算）
- "online flashcards" — ~10,000-20,000 月搜索量（估算）
- "printable flashcards" — ~3,000-5,000 月搜索量（估算）
- "study flashcards" — ~3,000-5,000 月搜索量（估算）
- 中文"闪卡生成器"/"记忆卡片" — ~500-1,500 月搜索量（估算）

**结论：英文搜索量远超中文，月搜索量合计 ≥ 30,000。通过。**

## 2. 竞品分析

| 竞品 | 优势 | 劣势 |
|:-----|:-----|:-----|
| Quizlet | 市场份额最大，社区内容丰富 | 需要注册，功能臃肿，有广告 |
| Anki | 间隔重复算法，适合长期记忆 | 界面老旧，学习成本高，需下载 |
| Flashcards World | 现代UI，FSRS算法 | 需要注册，有付费墙 |
| Cram.com | 简单直接 | 需要注册，广告多 |
| GoConqr | 多格式支持 | 注册墙，功能复杂 |

## 3. 差异化定位

| 我们 | 竞品 |
|:-----|:-----|
| **零注册**，打开即用 | 几乎全要注册 |
| **纯本地存储**（localStorage） | 需要云端账号 |
| **支持打印**（A4/Letter） | 大多不支持 |
| **深色主题**，现代UI | 大多是浅色老式UI |
| **双语言界面**（中/EN） | 大多仅英文 |
| **无需下载**，纯浏览器 | Anki等需安装 |
| **可导出JSON**备份 | 通常锁在平台内 |

## 4. 用户场景（覆盖率 ≥ 80%）
1. ✅ 学生考前复习：输入术语-定义对，翻转自测
2. ✅ 语言学习：单词-翻译，正面单词反面释义
3. ✅ 教师备课：批量创建卡片，打印分发
4. ✅ 面试准备：问题-答案模式
5. ✅ 医学/法学：概念记忆
6. ✅ 家长辅导孩子：制作学习卡片
7. ✅ 演讲准备：关键点记忆
8. ✅ 旅行语言速成：常用短语记忆

## 5. 核心功能清单
### MVP（必须）
- 添加卡片：正面/反面文本
- 卡片翻转动画（CSS 3D transform）
- 上一张/下一张导航
- 随机打乱模式
- 全部展开视图
- 删除/编辑卡片
- 本地存储（localStorage自动保存）
- 打印模式（A4布局4-6张/页）
- 导出JSON
- 导入JSON
- 卡片计数和进度

### Nice-to-have（后续迭代）
- 标签/分类
- Markdown支持
- 搜索过滤
- 统计（正确率）
- CSV导入

## 6. 技术方案
- HTML5 + CSS3 + Vanilla JS
- CSS 3D transform 翻转效果
- localStorage 持久化
- Web Share API（可选）
- 打印CSS @media print
- 深色主题：--bg:#0f172a，--card-bg:#1e293b

## 7. 页面结构
```
flashcard-generator/
├── index.html          # CN版
en/flashcard-generator/
└── index.html          # EN版
```

## 8. Schema标记
- SoftwareApplication
- FAQ（如何使用/是否免费/如何打印/数据安全）
- BreadcrumbList
- HowTo（如何使用闪卡学习）
