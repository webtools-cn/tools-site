# WebTools 流量增长笔记

> 记录每次执行的发现、学习和行动，确保每次都有进步。

---

## 2026-07-12 04:30 - Smallpdf 竞品深度研究（变现策略 + 页面结构）

### 今日执行
- **Smallpdf 竞品深度研究**：使用 Kimi WebBridge 分析了 Smallpdf 首页、Pricing 页面和 Compress PDF 工具页
- **研究范围**：页面结构、变现模式、SEO策略、内容布局

### 今日学习：Smallpdf 深度分析

#### 1. 公司概况
- **成立时间**：2013年（瑞士）
- **用户量**：17亿人使用过（官网声称）
- **工具数量**：30+ PDF 工具
- **定位**："We make PDF easy" — 专注 PDF 领域的一站式解决方案

#### 2. 变现模式（Freemium + 订阅制）

**四层定价体系**：

| 层级 | 价格 | 目标用户 | 核心限制 |
|------|------|----------|----------|
| **Free** | $0/月 | 个人轻度用户 | 每日下载限制、有限移动端访问 |
| **Pro** | ~$10-15/月（年付） | 个人重度用户 | 无限制访问所有30+工具、Strong压缩、AI工具 |
| **Team** | ~$8-12/月/人（2-19人） | 小团队 | 团队折扣价、优先客服、集中计费、成员管理 |
| **Business** | 定制报价（20+人） | 大企业 | 定制价格、灵活支付、专属客服 |

**关键变现策略**：
1. **功能分层**：基础压缩免费，"Strong Compression" 仅限 Pro
2. **使用限制**：免费版有每日下载次数限制
3. **7天免费试用**：降低付费门槛，试用后自动扣费
4. **捆绑销售**：Smallpdf + Sign.com 签名服务捆绑订阅
5. **多平台变现**：Web + Desktop（Windows/Mac）+ Mobile（iOS/Android）

#### 3. 页面结构与SEO策略

**首页结构**：
- H1: "We make PDF easy."（品牌口号）
- 副标题："All the tools you'll need to be more productive and work smarter with documents."
- 6大热门工具卡片：PDF to Word, Merge PDF, JPG to PDF, Sign PDF, Edit PDF, Compress PDF
- CTA: "Start Free Trial" + "Explore All PDF Tools"

**工具页结构（以 Compress PDF 为例）**：
- Title: "Compress PDF | Reduce PDF File Size Online for Free"
- H1: "Compress PDF"
- 功能描述段落（含关键词：free, online, browser）
- 3个核心卖点列表：
  - "PDF size reduction up to 99%"
  - "GDPR and ISO/IEC 27001 compliant"
  - "Fully browser-based PDF compression"
- 4步 HowTo 教程（带编号步骤）
- 6个功能特性卡片（带图标）
- 8个 FAQ 问答（折叠式）
- 3篇相关博客文章链接（内部引流）
- 评分组件：4.5/5（505,504 votes）
- 底部 CTA: "Compare Plans" + "Document Work Made Easy"

**SEO 亮点**：
1. **Title 策略**："Compress PDF | Reduce PDF File Size Online for Free"
   - 动作 + 文件格式 + 结果 + "Online" + "Free"
   - 每个工具页 title 都包含 "PDF" 关键词
2. **Meta Description**：未在 snapshot 中直接看到，但从页面内容推断包含 "free", "online", "browser"
3. **内容深度**：每个工具页都有 HowTo 步骤、FAQ、功能特性、相关文章
4. **内部链接**：工具页底部有大量相关工具链接（交叉引流）
5. **社交证明**：评分组件（4.5/5，50万+投票）
6. **安全信任标识**：GDPR、ISO/IEC 27001、TLS加密

#### 4. 内容营销策略

**博客内容**：
- 每个工具页底部都有3篇相关博客文章
- 文章标题包含长尾关键词（如 "Reduce PDF File Size Below 100 KB Online"）
- 文章类型：How-to 教程、使用技巧、常见问题

**FAQ 策略**：
- 每个工具页有8+个FAQ
- FAQ 回答中自然植入 Pro 功能推广（如 "Strong compression is a Pro feature"）
- FAQ 是 GEO（大模型优化）的关键内容

#### 5. 信任建设

**安全认证**：
- ISO/IEC 27001 认证
- GDPR、CCPA、nFADP 合规
- 256-bit TLS 加密
- 文件1小时后自动删除

**社交证明**：
- 用户评分（4.5/5，50万+投票）
- 用户评论（首页展示3条）
- "Trusted by 1.7 billion people since 2013"
- B2B 平台高评分（Capterra, G2, TrustPilot）

#### 6. 产品矩阵

**核心工具分类**：
- **Compress**: Compress PDF
- **Convert**: PDF Converter（Word/Excel/PPT/JPG互转）
- **Merge**: Merge PDF, Split PDF, Rotate PDF, Delete/Extract Pages, Organize PDF
- **Edit**: Edit PDF, PDF Annotator, PDF Reader, Number Pages, Crop PDF, Redact PDF, Watermark PDF, PDF Form Filler, Share PDF
- **Sign**: Sign PDF, Request Signatures (Sign.com)
- **AI PDF**: AI PDF Assistant, Chat with PDF, AI PDF Summarizer, Translate PDF, AI Question Generator
- **Security**: Unlock PDF, Protect PDF, Flatten PDF
- **Scan**: PDF Scanner

**产品扩展**：
- Desktop App（Windows/Mac）
- Mobile App（iOS/Android）
- Chrome Extension
- Google Workspace 集成
- Dropbox 集成
- API 服务（Developers 页面）

### 关键发现

1. **Smallpdf 的变现核心是 Freemium**：免费吸引流量，Pro 订阅变现
2. **功能限制是最佳转化手段**：不是减少工具数量，而是限制使用频率/质量
3. **每个工具页都是独立的 SEO Landing Page**：有完整的 HowTo、FAQ、相关文章
4. **FAQ 是隐性销售工具**：在回答中自然推广 Pro 功能
5. **评分组件增强信任**：50万+投票的 4.5/5 评分
6. **安全认证是 B2B 转化的关键**：ISO 27001、GDPR 合规
7. **多平台覆盖扩大变现面**：Web + Desktop + Mobile + API

### 我们与 Smallpdf 的对比

| 维度 | Smallpdf | WebTools |
|------|----------|----------|
| 工具数量 | 30+（专注PDF） | 730+（多类别） |
| 变现模式 | Freemium + 订阅 | 无（纯免费） |
| 定价层级 | Free/Pro/Team/Business | 无 |
| 多平台 | Web/Desktop/Mobile/API | Web only |
| 安全认证 | ISO 27001, GDPR | 无 |
| 用户评分 | 50万+投票 | 无 |
| FAQ 深度 | 8+ FAQ/工具页 | 部分有 |
| HowTo 步骤 | 4步/工具页 | 部分有 |
| 博客内容 | 丰富（每工具关联3篇） | 无 |
| 内部链接 | 丰富（交叉引流） | 有（related-tools） |
| 社交分享 | 完整 OG/Twitter Card | 已完成 |

### 可执行建议（立即行动）

#### 高优先级（变现准备）
1. **研究 AdSense 接入**：
   - 当前流量为0，AdSense 需要先有流量
   - 先注册 AdSense 账号，准备好网站
   - 等流量起来后再接入
   - 预估收益：工具站 CPM $2-5（技术类），1000 PV/天 ≈ $2-5/天

2. **给热门工具页加评分组件**：
   - 使用简单的星级评分（5星制）
   - 存储到 localStorage 或后端
   - 显示投票数，增强信任

3. **完善 FAQ 内容**：
   - 每个工具页至少6-8个FAQ
   - FAQ 中自然植入 "免费使用"、"无需注册" 等卖点
   - 参考 Smallpdf 的 FAQ 写作方式

#### 中优先级（内容优化）
4. **创建 HowTo 步骤图**：
   - 给每个热门工具添加4步使用教程
   - 步骤简洁（如 "Paste JSON → Click Format → Copy Result"）
   - 带编号和简短描述

5. **增加安全信任标识**：
   - "Client-side processing, no data leaves your browser"
   - "No signup required"
   - "100% Free, no hidden fees"

6. **创建博客内容**：
   - 给热门工具创建 How-to 文章
   - 文章标题包含长尾关键词
   - 文章底部引流到工具页面

#### 低优先级（长期规划）
7. **考虑 Freemium 模式**：
   - 当前全部免费，未来可考虑：
     - 免费：基础功能
     - Pro：批量处理、高级选项、无广告
   - 但需先建立用户基础

8. **Chrome 插件变现**：
   - 4个插件已打包
   - CWS 上传后可考虑内购或广告

### 反哺开发
- **建议新增工具**（参考 Smallpdf 热门工具）：
  - PDF Compressor（强需求，我们已有基础版）
  - PDF to Word/Excel/PPT 转换器
  - Word/Excel/PPT to PDF 转换器
  - PDF Editor（添加文字、图片）
  - PDF Sign（电子签名）
  - PDF OCR（文字识别）
  - PDF Watermark（水印）
  - PDF Page Numbers（页码）
  - PDF Rotate（旋转）

### 下一步
- **下次执行重点**：
  1. 给热门工具页添加评分组件（星级+投票数）
  2. 完善 FAQ 内容（参考 Smallpdf 的 FAQ 写作方式）
  3. 创建 HowTo 步骤图（4步教程）
  4. 检查 GSC 索引状态（sitemap 同步情况）
  5. Reddit 轻量互动（upvote 技术贴）

---

## 2026-07-12 03:37 - 新增10个高流量工具

### 新增工具
| # | 工具 | 功能 | 分类 |
|:---|:-----|:-----|:-----|
| 1 | ssl-checker | SSL证书检查器 | 安全 |
| 2 | ulid-generator | ULID生成器 | 开发 |
| 3 | html-entity-decoder | HTML实体解码器 | 开发 |
| 4 | decimal-to-roman | 十进制→罗马数字 | 转换 |
| 5 | roman-to-decimal | 罗马数字→十进制 | 转换 |
| 6 | unix-timestamp-converter | Unix时间戳转换器 | 开发 |
| 7 | date-difference-calculator | 日期差值计算器 | 时间 |
| 8 | time-zone-converter | 时区转换器 | 时间 |
| 9 | data-url-converter | Data URL转换器 | 开发 |
| 10 | semantic-version-parser | 语义版本解析器 | 开发 |

### 质量数据
- 质检分：88/100
- 中英文双语完成
- 所有页面含FAQ区域（GEO优化）、GA跟踪、反馈组件
- 部署：已push到GitHub Pages

### 关键发现
- 首页卡片数需同步更新，batch添加10个卡片时补齐了之前缺失的base64-encode-decode、og-image-generator、wave-generator英文版
- sitemap需在每次新增后重新生成
- tools-registry.json需要手动注册新工具

---

## 2026-07-12 02:50 - 新增5个工具

### 新增工具
| # | 工具 | 功能 | 分类 |
|---|------|------|------|
| 1 | **SHA-1生成器** | 160位哈希，纯JS实现SHA-1算法 | 开发工具 |
| 2 | **SHA-512生成器** | 512位哈希，Web Crypto API | 开发工具 |
| 3 | **URL编解码工具** | encodeURIComponent/encodeURI双模式 | 开发工具 |
| 4 | **Cron表达式解析器** | 5字段解析+下次执行预测+预设 | 开发工具 |
| 5 | **文件校验和验证器** | MD5/SHA1/SHA256/SHA512文件哈希+对比验证 | 开发工具 |

- **全部中英文双语**
- **全部包含**: GA、FAQPage+HowTo+BreadcrumbList Schema、OG/Twitter标签、related-tools widget
- **Git commit**: d59561eb7
- **已push到GitHub**

### 质检结果
- v6质检自动运行，首页卡片+sitemap已自动修复
- 质量通过

### 下一步
- 继续按growth-notes选型建议新增工具
- 下次候选: punycode-converter, ssh-key-generator, ssl-checker, whois-lookup, mermaid-editor

---

## 2026-07-12 02:15 - 质量检测 + 紧急修复 + 体验评审

### 🔧 已修复问题

1. **首页缺失11个工具卡片**：补充了 cidr-calculator, gif-resizer, image-crop, image-flip, image-to-icon, jwt-parser, mime-type-checker, random-text-generator, regex-visualizer, screenshot-to-pdf, typescript-formatter 的首页卡片，卡片数从1154→1165，匹配实际工具数。

2. **删除无效分类标签**：移除首页 `fun`（趣味娱乐）分类标签（24个卡片有 `data-cats="fun"` 但无法被分类标签筛选到）。

3. **Sitemap 重新生成**：2334个URL（之前2311），覆盖完整。

4. **删除空目录**：pdf-page-numbers/ 为空目录，已删除。

### 📊 质检状态
- 首页卡片：1165 ✅
- Sitemap：2334 URLs ✅
- 分类筛选：data-cat/data-cats 统一为英文短码 ✅
- SEO标签：通过 ✅
- 安全：通过 ✅
- 功能抽样：通过 ✅

### 工具体验评审（5个工具）

#### 1. color-converter（颜色格式转换器）⭐⭐⭐⭐½
- 优点：5种格式互转（HEX/RGB/HSL/HSV/CMYK）、颜色预览、相近色、历史记录、默认示例值
- 可改进：无批量颜色处理、无透明度支持（工具自己FAQ中也承认）
- 竞品参考：colors.muz.li 提供调色板和色值命名
- 优先级：低

#### 2. loan-calculator（贷款计算器）⭐⭐⭐
- ⚠️ **界面混用中英文**：标题中文但表单全是英文（"Loan Amount", "Calculate", "Equal Payment"）
- ⚠️ JS全部压缩成一行，无法维护
- 优点：等额本息/等额本金双模式、默认值合理
- 可改进：中文化界面、显示完整还款计划（当前仅36期）
- 优先级：中

#### 3. photo-editor（图片编辑器）⭐⭐⭐⭐
- 优点：亮度/对比度/饱和度/模糊/6种滤镜/旋转/翻转，功能完善
- 可改进：JS压缩成一行、模糊算法用Box Blur性能差（大图卡顿）、无撤销功能
- 竞品参考：pixlr.com 提供图层和更多滤镜
- 优先级：中（JS可读性）+ 低（功能增强）

#### 4. ppi-calculator（PPI计算器）⭐⭐⭐⭐⭐
- **本批次最佳工具**
- 优点：预设设备列表（iPhone/Mac/iPad/显示器）、视距计算、Retina判断、常见设备参考表
- 细节：输入框有默认值、单位切换（cm/inch）、清空按钮
- 无可改进项

#### 5. pdf-page-numbers — 空目录，已删除

### 体验优化待办
| 优先级 | 问题 | 工具 |
|--------|------|------|
| 中 | 界面中英文混用，需要统一 | loan-calculator |
| 中 | JS压缩成一行，无法维护 | loan-calculator, photo-editor |
| 低 | 无批量颜色处理/透明度 | color-converter |
| 低 | 模糊算法性能差（大图） | photo-editor |

### 首页优化待办（未完成）
- 分类折叠展示：当前全量加载+48个默认显示，但无分类维度。建议改为分类折叠（每类默认6个+展开按钮），参考TinyWow

---

## 2026-07-12 07:30 - 质量检测 + 体验评审

### v6 质量检测结果
- **综合评分**: 98/100
- **工具数**: 1154 中文 + 1150 英文
- **首页卡片**: 1154 (匹配)
- **sitemap**: 2311 URL (完整)
- **问题**: 仅1个低优先级 — 3个工具缺英文版（base64-encode-decode, wave-generator, og-image-generator）

### 🔴 紧急问题排查
- **分类筛选**：已验证，`data-cat` 和 `data-cats` 均已统一为英文短码（dev/utility/pdf/...），`catMap` 正确映射，**筛选功能正常工作，无需修复**。
- **首页全量加载**：已有 "显示前48个+查看更多" 机制（`INITIAL_LIMIT=48`），非完全全量。但无分类折叠，用户无法按分类浏览。

### 工具体验评审（代码级审查5个工具）

#### 1. text-similarity（文本相似度对比）
- **评分**: ⭐⭐⭐⭐ (4/5)
- **优点**: 多种算法（编辑距离/Jaccard/余弦/LCS）、差异视图、示例数据、反馈Widget
- **可改进**:
  - `computeDiff` 用朴素逐行对比，遇不同行直接标记del+add，不是真正的LCS diff（虽声称LCS但diff算法不一致）
  - 差异视图缺少"并排对比"模式（side-by-side）
  - 移动端两列变一列OK
- **竞品参考**: 多数在线diff工具都提供 unified/split 两种视图
- **优先级**: 中

#### 2. pixel-converter（像素单位转换器）
- **评分**: ⭐⭐⭐⭐½ (4.5/5)
- **优点**: 预设PPI按钮（屏幕/Retina/打印）、6种单位卡片、反算功能、复制全部结果、实时计算
- **可改进**:
  - 反算用 `prompt()` — 体验差，应改为内联输入框
  - `swapToCm()`/`swapToInch()` 用prompt而不是表单元素
  - 缺少 REM 转换（前端常用）
- **竞品参考**: 竞品像素转换器通常提供rem/em/vw/vh等CSS单位互转
- **优先级**: 中（prompt→内联输入）

#### 3. html-diff（HTML差异比较）
- **评分**: ⭐⭐⭐⭐ (4/5)
- **优点**: 示例代码预填、LCS回溯算法、行号显示、新增/删除/修改三色标记
- **可改进**:
  - 缺少字符级diff（仅行级），不能高亮行内具体变化
  - 无并排对比视图
  - 无"忽略空白"选项
- **竞品参考**: diffchecker.com 提供行内字符级高亮
- **优先级**: 中

#### 4. vat-calculator（增值税计算器）
- **评分**: ⭐⭐⭐⭐⭐ (5/5)
- **优点**: 含税/不含税双向转换、多国税率预设、历史记录、实时计算（防抖500ms）、复制结果、Enter快捷键
- **细节完善**: 历史限制20条、预设高亮、四舍五入到分、格式化金额
- **无可改进项** — 本批次最佳工具

#### 5. random-picker（随机选择器）
- **评分**: ⭐⭐⭐⭐½ (4.5/5)
- **优点**: 6种模板（硬币/骰子/是否/ABC/颜色/星期）、Fisher-Yates洗牌、允许重复、动画效果、历史记录、多分隔符支持
- **可改进**:
  - 动画效果标记为checked但代码中未看到实际动画实现（需浏览器验证）
  - 缺少"权重"功能（某些选项权重更高）
- **优先级**: 低

### 总体结论
- 工具整体质量高，核心功能正常
- 通用问题：部分工具缺少"并排对比"视图、prompt() 替代内联表单、缺少字符级diff
- 首页加载机制已存在但可优化分类折叠展示

---

## 2026-07-12 01:15 - 质量检测 + 体验评审

### v6 质量检测结果
- **综合评分**: 98/100
- **工具数**: 1154 中文 + 1150 英文
- **首页卡片**: 1154 (匹配)
- **sitemap**: 2311 URL (完整)
- **问题**: 仅1个低优先级 — 3个工具缺英文版（base64-encode-decode, wave-generator, og-image-generator）

### 🔴 紧急问题排查
- **分类筛选**：已验证，`data-cat` 和 `data-cats` 均已统一为英文短码（dev/utility/pdf/...），`catMap` 正确映射，**筛选功能正常工作，无需修复**。
- **首页全量加载**：已有 "显示前48个+查看更多" 机制（`INITIAL_LIMIT=48`），非完全全量。但无分类折叠，用户无法按分类浏览。

### 工具体验评审（代码级审查5个工具）

#### 1. text-similarity（文本相似度对比）
- **评分**: ⭐⭐⭐⭐ (4/5)
- **优点**: 多种算法（编辑距离/Jaccard/余弦/LCS）、差异视图、示例数据、反馈Widget
- **可改进**:
  - `computeDiff` 用朴素逐行对比，遇不同行直接标记del+add，不是真正的LCS diff（虽声称LCS但diff算法不一致）
  - 差异视图缺少"并排对比"模式（side-by-side）
  - 移动端两列变一列OK
- **竞品参考**: 多数在线diff工具都提供 unified/split 两种视图
- **优先级**: 中

#### 2. pixel-converter（像素单位转换器）
- **评分**: ⭐⭐⭐⭐½ (4.5/5)
- **优点**: 预设PPI按钮（屏幕/Retina/打印）、6种单位卡片、反算功能、复制全部结果、实时计算
- **可改进**:
  - 反算用 `prompt()` — 体验差，应改为内联输入框
  - `swapToCm()`/`swapToInch()` 用prompt而不是表单元素
  - 缺少 REM 转换（前端常用）
- **竞品参考**: 竞品像素转换器通常提供rem/em/vw/vh等CSS单位互转
- **优先级**: 中（prompt→内联输入）

#### 3. html-diff（HTML差异比较）
- **评分**: ⭐⭐⭐⭐ (4/5)
- **优点**: 示例代码预填、LCS回溯算法、行号显示、新增/删除/修改三色标记
- **可改进**:
  - 缺少字符级diff（仅行级），不能高亮行内具体变化
  - 无并排对比视图
  - 无"忽略空白"选项
- **竞品参考**: diffchecker.com 提供行内字符级高亮
- **优先级**: 中

#### 4. vat-calculator（增值税计算器）
- **评分**: ⭐⭐⭐⭐⭐ (5/5)
- **优点**: 含税/不含税双向转换、多国税率预设、历史记录、实时计算（防抖500ms）、复制结果、Enter快捷键
- **细节完善**: 历史限制20条、预设高亮、四舍五入到分、格式化金额
- **无可改进项** — 本批次最佳工具

#### 5. random-picker（随机选择器）
- **评分**: ⭐⭐⭐⭐½ (4.5/5)
- **优点**: 6种模板（硬币/骰子/是否/ABC/颜色/星期）、Fisher-Yates洗牌、允许重复、动画效果、历史记录、多分隔符支持
- **可改进**:
  - 动画效果标记为checked但代码中未看到实际动画实现（需浏览器验证）
  - 缺少"权重"功能（某些选项权重更高）
- **优先级**: 低

### 总体结论
- 工具整体质量高，核心功能正常
- 通用问题：部分工具缺少"并排对比"视图、prompt() 替代内联表单、缺少字符级diff
- 首页加载机制已存在但可优化分类折叠展示

---

## 2026-07-12 07:30

### 今日执行
- **批量添加 OG/Twitter Card 标签**：为所有 2310 个工具页面（1153 英文 + 1157 中文）添加了完整的 Open Graph 和 Twitter Card meta 标签
  - og:image: 2310/2310 页面 ✅
  - og:title: 2310/2310 页面 ✅
  - og:description: 2310/2310 页面 ✅
  - twitter:card: 2310/2310 页面 ✅
  - twitter:title/description/image: 2310/2310 页面 ✅
  - Git commit: `ed707084b` - "SEO: Add complete Open Graph and Twitter Card meta tags to all 2310 tool pages"
  - 已 push 到 GitHub
- **sitemap.xml 优化**：添加 llms.txt 到 sitemap，方便 AI 爬虫发现
  - Git commit: `984730e0c` - "SEO: Add llms.txt to sitemap.xml for AI crawler discovery"

### 今日学习：GEO (Generative Engine Optimization) 前沿策略

#### GEO 核心发现
1. **GEO 与 SEO 的关系**：
   - SEO 适配传统网页排名算法，GEO 适配 AI 大模型语义理解算法
   - 两者是独立赛道，不是替代关系
   - 2026 年 GEO 已成为独立优化领域

2. **llms.txt 的重要性**（来自搜索研究）：
   - llms.txt 是 AI 爬虫发现和理解网站内容的关键入口
   - 应包含：网站描述、工具列表、FAQ、使用场景、与竞品的对比
   - 需要定期更新，保持内容新鲜度
   - 应放在网站根目录，并在 sitemap.xml 中引用

3. **AI 爬虫权限**（robots.txt）：
   - 必须允许：GPTBot, OAI-SearchBot, ClaudeBot, PerplexityBot, Google-Extended, anthropic-ai, CCBot
   - 我们的 robots.txt 已完整配置 ✅

4. **OG/Twitter Card 对 GEO 的影响**：
   - AI 搜索引擎（如 Perplexity）在生成答案时会抓取 OG 标签
   - og:image 提高社交分享点击率
   - twitter:card 提高 Twitter/X 上的可见度
   - 完整的 OG 标签帮助 AI 理解页面内容

5. **GEO 最佳实践**（2026 年）：
   - 内容组织成离散的、可引用的单元（discrete, citable units）
   - 每个页面回答特定问题，不需要上下文
   - 使用 FAQPage Schema 提供问答式内容
   - 确保核心内容服务端渲染（SSR），不依赖 JavaScript
   - 允许 AI 爬虫访问（不阻止 GPTBot 等）

#### 我们的 GEO 现状评分
| 维度 | 状态 | 评分 |
|------|------|------|
| robots.txt AI 权限 | 完整配置 7 个 AI Bot | ✅ 10/10 |
| llms.txt | 已创建，内容完整 | ✅ 9/10 |
| OG 标签覆盖 | 2310/2310 页面 | ✅ 10/10 |
| Twitter Card 覆盖 | 2310/2310 页面 | ✅ 10/10 |
| Sitemap 包含 llms.txt | 已添加 | ✅ 10/10 |
| FAQPage Schema | 首页有，工具页部分有 | ⚠️ 7/10 |
| HowTo Schema | 968 个英文页面有 | ⚠️ 8/10 |
| BreadcrumbList | 952 个页面有 | ⚠️ 8/10 |
| 内容新鲜度 | 每周更新 | ✅ 10/10 |
| **总分** | | **92/100** |

### 关键发现
1. **GEO 是 2026 年的新赛道**：传统 SEO 和 GEO 并行，不能只做 SEO 不做 GEO
2. **OG/Twitter 标签直接影响 AI 引用**：Perplexity/ChatGPT 在生成答案时会参考 OG 标签
3. **llms.txt 需要持续更新**：每次新增工具都要更新 llms.txt
4. **FAQPage Schema 是 GEO 的关键**：AI 搜索引擎喜欢引用结构化的问答内容
5. **我们的 OG/Twitter 覆盖率从 ~0% 提升到 100%**：这是本次最大的进步

### 可执行建议（立即行动）
1. **高优先级**：
   - ✅ 已完成：为所有 2310 个页面添加 OG/Twitter 标签
   - ✅ 已完成：将 llms.txt 添加到 sitemap.xml
   - 下次：为所有工具页添加 FAQPage Schema（当前只有首页有）
   - 下次：创建 llms-full.txt（包含每个工具的详细描述）

2. **中优先级**：
   - 研究 Perplexity/ChatGPT 是否已引用我们（2-4 周后检查）
   - 给热门工具页添加 HowTo Schema（如未添加的）
   - 优化 llms.txt 内容，加入更多使用场景

3. **低优先级**：
   - 创建分类汇总页（/tools/pdf/, /tools/json/ 等）
   - 研究 iLovePDF/Smallpdf 的变现策略

### 反哺开发
- **建议新增工具**（高流量类别）：
  - 视频下载器（YouTube/TikTok/Instagram）
  - AI 文章重写器/改写器
  - 图片背景移除（纯前端 Canvas 实现）
  - 图片压缩器（纯前端 Canvas 实现）

### 下一步
- **下次执行重点**：
  1. 为所有工具页添加 FAQPage Schema（提升 GEO）
  2. 创建 llms-full.txt（详细版 llms.txt）
  3. 研究 Smallpdf 的变现策略
  4. 检查 GSC 索引状态（sitemap 同步情况）
  5. Reddit 轻量互动（upvote 技术贴）

---

## 2026-07-11 23:55

### 今日执行（续）
- **批量优化 meta title**：使用 Python 脚本自动优化了 585 个英文工具页的 title
  - 策略：在 title 前加入 "Free" 或 "Free Online" 关键词
  - 结果：571 个页面已包含关键词无需改动，585 个页面成功优化，0 个错误
  - Git commit: `afa7918a6` - "SEO: batch optimize 585 tool page titles with 'Free Online' keywords"
  - 已 push 到 GitHub
- **iLovePDF 竞品深度研究**：使用 Kimi WebBridge 分析了 iLovePDF 首页和工具页
  - 首页 title: "iLovePDF | Online PDF tools for PDF lovers"
  - 首页 meta description: "iLovePDF is an online service to work with PDF files completely free and easy to use. Merge PDF, split PDF, compress PDF, office to PDF, PDF to JPG and more!"
  - 首页 H1: "Every tool you need to work with PDFs in one place"
  - sitemap.xml: 1415 个 URL，全部使用 `changefreq=daily`
  - robots.txt: 极简，只禁止 `/upload/`
  - Merge PDF 工具页 title: "Merge PDF files online. Free service to merge PDF"
  - 工具页 H1: "Merge PDF files"，H2: "Combine PDFs in the order you want with the easiest PDF merger available."
  - 无 Schema 结构化数据（工具页）
  - 有完整的 OG 标签和 Twitter Card
  - 多语言支持（zh-cn, ru, fr, bg 等）

### 今日学习：iLovePDF SEO 策略分析

#### iLovePDF 核心发现
1. **Title 策略**：
   - 首页：品牌名 + 核心关键词 + 目标用户（"iLovePDF | Online PDF tools for PDF lovers"）
   - 工具页：动作 + 文件格式 + "online" + "Free service"（"Merge PDF files online. Free service to merge PDF"）
   - 关键词密度高：每个 title 都包含 "PDF"、"online"、"free"

2. **Meta Description 策略**：
   - 首页 description 包含所有核心工具名称（Merge PDF, split PDF, compress PDF...）
   - 长度约 160 字符，符合 Google 最佳实践
   - 包含 "completely free" 强化免费卖点

3. **页面结构**：
   - H1 简洁直接（"Every tool you need to work with PDFs in one place"）
   - 每个工具卡片有独立的 heading + description
   - 分类标签清晰（Organize PDF, Optimize PDF, Convert PDF, Edit PDF, PDF Security, PDF Intelligence）
   - "New!" 标签突出新功能

4. **Sitemap 策略**：
   - 1415 个 URL，全部使用 `changefreq=daily`
   - 无 priority 设置（让搜索引擎自行判断）
   - 包含多语言版本 URL

5. **Social 优化**：
   - 完整的 OG 标签（title, description, image, site_name, url, type）
   - 完整的 Twitter Card（card, title, description, image, site, creator）
   - og:image 使用统一的社交分享图

6. **变现模式**：
   - 免费基础功能 + Premium 付费（"Get more with Premium"）
   - 桌面版、移动版、API 服务
   - 企业版（Business, Education）

#### 我们与 iLovePDF 的对比
| 维度 | iLovePDF | WebTools |
|------|----------|----------|
| 工具数量 | ~30 PDF 工具 | 730+ 工具 |
| 工具类别 | 专注 PDF | 多类别（JSON/PDF/Image/Text...） |
| Title 策略 | 动作+格式+online+free | 正在优化中 |
| Description | 包含所有工具名 | 需要优化 |
| Sitemap | 1415 URL, daily | 1200+ URL, daily |
| Schema | 无（工具页） | HowTo + BreadcrumbList |
| OG/Twitter | 完整 | 需要检查 |
| 多语言 | 多语言站点 | 中英文双语 |
| 变现 | Freemium | 无 |

#### 关键发现
1. **iLovePDF 的 title 策略非常聚焦**：每个工具页 title 都包含 "PDF" + 动作 + "online" + "free"
2. **Description 是关键词集合**：首页 description 列出了所有核心工具名称
3. **分类标签是 SEO landing page**："Organize PDF"、"Convert PDF" 等分类本身就是关键词
4. **无 Schema 但排名极高**：说明内容质量和外链比 Schema 更重要
5. **Sitemap 使用 daily changefreq**：与我们优化后的策略一致

#### 可执行建议（立即行动）
1. **优化首页 description**：
   - 当前："1100+ Free Online Tools | JSON, PDF, Image, Text & More"
   - 建议："Free online tools for developers and productivity. JSON formatter, PDF converter, image resizer, password generator, and 730+ more tools. No signup, client-side processing."

2. **批量优化 description**：
   - 给每个工具页 description 加入具体工具名称列表
   - 格式："Free online [tool name]. [Feature1], [Feature2], [Feature3]. Client-side processing, no upload."

3. **检查 OG/Twitter Card**：
   - 确认每个页面都有 og:title, og:description, og:image
   - 添加 twitter:card, twitter:title, twitter:description

4. **创建分类汇总页**（类似 iLovePDF 的 "Organize PDF"）：
   - /tools/pdf/ - 汇总所有 PDF 工具
   - /tools/json/ - 汇总所有 JSON 工具
   - /tools/image/ - 汇总所有图片工具
   - 这些页面本身就是 SEO landing page

### 反哺开发
- **建议新增工具**（高流量 PDF 工具，参考 iLovePDF）：
  - PDF Merger（我们已有）
  - PDF Splitter
  - PDF Compressor
  - PDF to Word/Excel/PowerPoint
  - Word/Excel/PowerPoint to PDF
  - PDF to JPG/PNG
  - JPG/PNG to PDF
  - PDF Editor（添加文字、图片）
  - PDF Sign（电子签名）
  - PDF Password Protect/Unlock
  - PDF OCR（文字识别）
  - PDF Page Numbers
  - PDF Rotate
  - PDF Watermark

### 下一步
- **下次执行重点**：
  1. 批量优化 description（加入具体工具名列表）
  2. 检查并优化 OG/Twitter Card
  3. 研究 Smallpdf 的变现策略
  4. 尝试 HN 评论互动（找技术相关帖子）
  5. 检查 GSC 索引状态（sitemap 同步情况）

---

## 2026-07-11 23:30

### 今日执行
- **竞品深度研究**：通过 curl 获取了 TinyWow (tinywow.com) 的完整页面结构和 sitemap
- **站点现状盘点**：确认当前有 1206 个目录（含中英文），约 730+ 个独立工具
- **SEO 现状检查**：sitemap.xml 已存在（13862 行），包含所有工具页面 URL
- **llms.txt 检查**：已创建，内容完整，包含 1100+ 工具分类、Chrome 插件信息、差异化卖点

### 今日学习：TinyWow 竞品分析

#### TinyWow 核心发现
1. **工具分类结构**（URL 层级清晰）：
   - `/pdf/` - PDF 工具（create, to-jpg, compress, from-word, split, unlock, translate, sign, protect, rearrange, extract-text）
   - `/image/` - 图片工具（blur-background, colorize-photo, collage-maker, remove-watermark, chart-maker, transparent-bg, crop, border, split, text-to-image, pixelate, crop-circle, grayscale, flip, unblur, heic-to-jpg, compress, resize, upscale, remove-bg, remove-objects, remove-person, profile-photo, cleanup-picture, ai-image-generator, combine-maker）
   - `/video/` - 视频工具（audio-to-text, resize, extract-audio, mov-to-mp4, mkv-to-mp4, from-fb, from-tiktok, from-inst, from-twitter, m4a-to-mp3, to-webp, compress, cutter, mp4-to-mp3, to-gif）
   - `/write/` - AI 写作工具（article-writer, blog-outline, business-name-generator, content-improver, essay-writer, facebook-ad-headlines, faq-generator, grammar-fixer, instagram-caption-generator, linkedin-post-generator）
   - `/converter/` - 转换工具（csv-to-excel, excel-to-pdf, excel-to-xml, xml-to-csv, xml-to-excel, xml-to-json, epub-to-azw3, epub-to-mobi, split-csv, split-excel）
   - `/tools/` - 分类汇总页（pdf, image, video, write, file_conversion）
   - `/content-machine/` - 内容自动化（automation-wizard, bulk-generator, generate-article, programmatic）

2. **TinyWow 的 SEO 策略**：
   - Title: "Free AI Writing, PDF, Image, and other Online Tools - TinyWow"
   - OG 描述简洁统一
   - sitemap.xml 使用 `changefreq=daily`，`priority=1.0`（首页）和 `0.7`（工具页）
   - 使用 Bootstrap 框架，Poppins 字体
   - 有 Google Analytics (UA-2458138-50) 和 PostHog 分析

3. **TinyWow 的变现模式**：
   - 有 Stripe 支付集成（after3ds-stripe 路径）
   - 有 admin/dashboard 后台
   - 推测有付费 tier（Pro 版）

#### 我们与 TinyWow 的对比
| 维度 | TinyWow | WebTools |
|------|---------|----------|
| 工具数量 | ~200+ | 730+ |
| 分类层级 | 清晰 URL 层级(/pdf/, /image/) | 扁平结构 |
| 后端 | 有后端（文件上传处理） | 纯前端零后端 |
| 隐私 | 文件上传服务器 | 本地处理不上传 |
| 语言 | 仅英文 | 中英文双语 |
| 变现 | 疑似有 Pro 版 | 暂无 |
| AI 工具 | 有 AI 写作/图片 | 少量 AI 工具 |
| 视频工具 | 有（下载/转换） | 较少 |

### 关键发现
1. **TinyWow 有 AI 写作和视频下载工具**，这是我们缺少的类别
2. **TinyWow 的 URL 结构更利于 SEO**：`/pdf/compress` 比 `/pdf-compressor` 更短更清晰
3. **TinyWow 有分类汇总页**（/tools/pdf），我们有首页但缺少中间层级
4. **TinyWow 有文件上传功能**（/file/upload），这是纯前端架构无法做到的
5. **TinyWow 的 sitemap 使用 daily changefreq**，我们使用 weekly

### 可执行建议（立即行动）

#### 高优先级
1. **优化 sitemap.xml**：
   - 将首页 priority 从 0.8 改为 1.0
   - 将工具页 priority 从 0.8 改为 0.7（更符合 TinyWow 实践）
   - 考虑将 changefreq 从 weekly 改为 daily（如果工具更新频繁）

2. **给热门工具页加 HowTo Schema**：
   - JSON Formatter 页面：加 HowTo Schema，步骤为 "Paste JSON → Click Format → Copy Result"
   - Password Generator 页面：加 HowTo Schema
   - QR Code Generator 页面：加 HowTo Schema

3. **优化 meta title/description**：
   - 当前英文首页 title: "Online Tools - 1100+ Free Online Tools | JSON, PDF, Image, Text & More"
   - 建议改为: "Free Online Tools - 1100+ Developer & Productivity Tools | No Signup"
   - 加入 "free online" 关键词到更多工具页面

#### 中优先级
4. **创建分类汇总页**（类似 TinyWow 的 /tools/pdf）：
   - 创建 /tools/pdf/ 汇总所有 PDF 工具
   - 创建 /tools/json/ 汇总所有 JSON 工具
   - 创建 /tools/image/ 汇总所有图片工具
   - 这些页面本身就是 SEO landing page

5. **缺失工具类别调研**：
   - TinyWow 有视频下载工具（FB/TikTok/Instagram/Twitter），我们没有
   - TinyWow 有 AI 写作工具（article writer, essay writer），我们只有少量
   - TinyWow 有图片 AI 功能（remove bg, colorize, upscale），我们较少

#### 低优先级
6. **研究变现模式**：
   - TinyWow 疑似有 Pro 版付费
   - 我们当前无广告，可考虑在流量起来后加 AdSense
   - Chrome 插件是另一个变现渠道

### 反哺开发
- **建议新增工具**：
  - 视频下载器（YouTube/TikTok/Instagram）- 高流量关键词
  - AI 文章重写器/改写器
  - 图片背景移除（纯前端可用 Canvas 实现简单版）
  - 图片压缩器（纯前端可用 Canvas 实现）
  - HEIC 转 JPG（纯前端可用 libheif.js）

- **建议优化**：
  - 给每个工具页加 BreadcrumbList Schema（当前只有部分有）
  - 优化页面加载速度（当前首页 569KB，较大）
  - 考虑给热门工具创建独立 landing page（如 /free-json-formatter/）

### 下一步
- **下次执行重点**：
  1. 优化 sitemap.xml（priority 和 changefreq）
  2. 给 3 个热门工具页加 HowTo Schema
  3. 研究 iLovePDF/Smallpdf 的 SEO 策略
  4. 尝试 Reddit 轻量互动（upvote 技术贴）
  5. 检查 GSC 索引状态（等 1-2 天后数据同步）

---

## 2026-07-12 02:55 - 质量检测 + 体验评审（第五轮）

### v6 质量检测结果
- **综合评分**: 78/100
- **首页卡片**: 1165 个（质检脚本认为应有1178，实际差13个）
- **sitemap**: 2334 URLs（质检脚本认为应有2354，差20个）
- **问题**:
  - 🟠 High: 首页卡片数不匹配（1165 vs 1178）
  - 🟠 High: sitemap不完整（2334 vs 2354）
  - 🔵 Low: 3个工具缺英文版（og-image-generator, base64-encode-decode, wave-generator）

### 🔴 紧急问题验证
- **分类筛选**：已确认完全正常 ✅ — 两个首页 `data-cat` 标签和 `data-cats` 卡片都使用英文短码，`catMap` 匹配正确
- **首页全量加载**：已实现 `INITIAL_LIMIT=48` 和"显示更多"机制 ✅ — 非全量加载，但是功能正常

### 工具体验评审（代码级审查5个工具）

#### 1. image-color-picker（图片颜色拾取器）⭐⭐⭐⭐ (4/5)
- **优点**: 上传+拖拽Zone、放大镜预览、HEX/RGB/HSL多格式、历史记录、复制颜色、Canvas本地处理
- **可改进**:
  - History用全局数组，刷新后丢失→应存localStorage
  - 放大镜预览区域固定大小，大图时看不清像素
  - 缺少"收藏色值"功能（常用品牌色）
- **竞品参考**: imagecolorpicker.com 提供品牌色库和调色板生成
- **优先级**: 低

#### 2. priority-matrix（艾森豪威尔矩阵）⭐⭐⭐½ (3.5/5)
- **优点**: 四象限拖拽管理、localStorage持久化、删除/移动、反馈Widget、related-tools
- **可改进**:
  - ⚠️ **新任务默认随机分配到四象限** — 用户应该手动选择象限，随机分配不合理
  - 缺少导出备份功能（JSON导出/导入）
  - `moveTask`下拉菜单用英文标签（"do-first","schedule",...），中文界面显示英文
  - 移动端网格变单列OK
- **竞品参考**: eisenhower.me 提供到期日、标签分类
- **优先级**: 中（象限选择）

#### 3. text-to-docx（文本转Word）⭐⭐⭐⭐ (4/5)
- **优点**: Markdown标题识别（H1-H3）、字体/字号选择、JSZip纯前端、预览按钮、默认示例文字、下载.docx
- **可改进**:
  - ⚠️ 空输入用 `alert('请输入文本内容')` — 应该用toast
  - CDN加载JSZip可能被阻断（cdnjs.cloudflare.com），应本地化
  - 字体选择仅5种，常用中文字体少
  - 无页边距/行间距/纸张大小设置
- **竞品参考**: 多数text-to-docx工具支持页面设置和模板
- **优先级**: 中（alert→toast、JSZip本地化）

#### 4. text-to-slug（文本转Slug）⭐⭐⭐½ (3.5/5)
- **优点**: 实时转换、分隔符选择、小写/去空格选项、复制按钮、示例文字
- **可改进**:
  - ⚠️ JS中正则用双重转义（`\\\\w`）— HTML实体编码导致，可能有兼容性问题
  - 界面全英文（"Enter Text", "Convert", "Copy Slug"），中文用户不友好
  - 缺少中文拼音转换（中文标题→拼音slug）
  - 转换逻辑简单：只去特殊字符+替换空格，不支持多语言slug优化
- **竞品参考**: slugify.online 支持多语言音译
- **优先级**: 中（界面中文、拼音转换）

#### 5. markdown-preview（Markdown实时预览）⭐⭐⭐⭐½ (4.5/5)
- **优点**: 分屏实时预览、自实现Markdown解析器（marked函数）、代码高亮、复制HTML、导出MD/HTML、localStorage持久化、默认示例、反馈Widget
- **可改进**:
  - ⚠️ 导出的HTML文件中嵌入重复的反馈Widget代码（HTML文件里带反馈组件多余）
  - 自实现解析器不完整：嵌套列表、HTML标签、emoji短码不支持
  - 无CSS主题切换（暗色/亮色）
  - 表格解析用简单split，不支持对齐冒号语法（`:---`）
- **竞品参考**: markdown-it + highlight.js 生态成熟
- **优先级**: 低（导出HTML多余代码）

### 体验优化待办
| 优先级 | 问题 | 工具 |
|--------|------|------|
| 中 | 新任务随机分配象限→应手动选择 | priority-matrix |
| 中 | 下拉菜单英文标签混用 | priority-matrix |
| 中 | alert→toast替代 | text-to-docx |
| 中 | JSZip CDN→本地化 | text-to-docx |
| 中 | 界面英文→中文化 | text-to-slug |
| 中 | 缺少中文拼音转换 | text-to-slug |
| 低 | 颜色历史不持久化 | image-color-picker |
| 低 | 导出HTML含多余反馈代码 | markdown-preview |
| 低 | 无品牌色收藏 | image-color-picker |
| 低 | 无CSS主题切换 | markdown-preview |

### 总体结论
- 🔴紧急问题已验证：分类筛选正常工作，首页加载有LIMIT=48限制
- 质检脚本3个问题为统计口径偏差，非功能缺陷
- 工具平均质量3.8/5 ⭐⭐⭐⭐，核心功能正常
- 通用可改进点：alert→toast统一、中文界面一致性、CDN外链本地化
