# 页面标准规范 v2.0

> 所有工具页面必须严格遵守此规范。新增/修改页面前先读此文件。Cron任务必须按此标准执行。

---

## 一、`<head>` 区域（按顺序）

```
1. GA4 代码          — gtag.js + config G-9W1157EBQV
2. AdSense 代码      — adsbygoogle.js client=ca-pub-5998441792679372
3. <meta charset>    — UTF-8
4. <meta viewport>   — width=device-width, initial-scale=1.0
5. <meta description>— 120字以内，含"免费在线"+"纯前端本地处理"
6. <meta keywords>   — 5-10个关键词
7. <title>           — 工具名 - 核心功能·卖点（60字内）
8. <link canonical>  — https://free-toolbase.com/工具名/
9. OG标签            — og:title, og:description, og:url, og:type, og:site_name
10. Schema JSON-LD   — FAQPage + SoftwareApplication（含email:dexshuang@google.com）
11. <style>          — 所有CSS内联，深色主题
12. hreflang标签     — zh/en/x-default
```

### 禁止出现在`<head>`的
- rating-widget CSS/JS
- howto-section CSS
- freshness badge
- 任何可见组件的CSS

---

## 二、`<body>` 区域（按顺序，从上到下）

```
1. 顶部广告位        — <div class="ad-slot" id="ad-top">
2. container开始     — <div class="container">
3. header            — h1标题 + lang-switch（中/EN切换）
4. breadcrumb        — 首页 › 分类 › 工具名
5. hero              — 副标题 + badge（零依赖·可离线使用）
6. main-grid         — 工具区（左）+ 侧边栏广告（右）
    ├── panel        — 工具输入/输出/操作区
    └── ad-sidebar   — 2个侧边栏广告位（300×250）
7. 中部广告位        — <div class="ad-slot">（728×90）
8. seo-content       — SEO长文内容（工具介绍/功能/教程/场景/知识）
9. FAQ               — <div class="faq-item"> × 5-7个，只出现1次
10. 底部广告位       — <div class="ad-slot">（728×90）
11. container结束    — </div>
12. footer           — 首页/全部工具/联系我们/隐私政策/服务条款/关于我们/EN切换
13. 工具JS           — <script>工具逻辑</script>
14. feedback-widget  — 固定右下角反馈按钮
15. related-tools    — <link>+<div>+<script>（3行）
16. </body></html>
```

### 禁止出现的组件
- ❌ rating-widget（星级评分）
- ❌ howto-section（可见步骤）— Schema里有HowTo就够了
- ❌ freshness badge（"Updated: 日期"）
- ❌ trust-signals
- ❌ 重复FAQ — FAQ只出现1次
- ❌ ad-placeholder / ad-container — 用ad-slot代替

---

## 三、深色主题配色（统一）

| 元素 | 颜色 |
|:-----|:-----|
| 页面背景 | `#0f172a` |
| 卡片/面板 | `#1e293b` |
| 主文字 | `#e2e8f0` |
| 副文字 | `#94a3b8` |
| 弱文字 | `#64748b` |
| 强调色 | `#06b6d4` |
| 强调hover | `#22d3ee` |
| 成功色 | `#10b981` |
| 危险色 | `#ef4444` |
| 边框 | `rgba(148,163,184,.1)` |

### 禁止使用
- ❌ `color:#333` / `color:#666` — 浅色文字在深色背景看不见
- ❌ `background:#fff` / `background:white` — 白色背景
- ❌ 任何浅色背景+深色文字的组合

---

## 四、广告位规范（AdSense `<ins>` 标签）

每个工具页5个广告位，全部使用 `<ins class="adsbygoogle">` 标签：

### 顶部（728×90）
```html
<div class="ad-slot" id="ad-top"><ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-5998441792679372" data-ad-slot="XXXXXXX" data-ad-format="horizontal" data-full-width-responsive="true"></ins></div>
```

### 侧边栏1（300×250）
```html
<div class="ad-slot ad-sidebar"><ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-5998441792679372" data-ad-slot="XXXXXXX" data-ad-format="rectangle" data-full-width-responsive="true"></ins></div>
```

### 侧边栏2（300×250）
```html
<div class="ad-slot ad-sidebar" style="margin-top:16px"><ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-5998441792679372" data-ad-slot="XXXXXXX" data-ad-format="rectangle" data-full-width-responsive="true"></ins></div>
```

### 中部（728×90）
```html
<div class="ad-slot" style="margin-top:24px"><ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-5998441792679372" data-ad-slot="XXXXXXX" data-ad-format="horizontal" data-full-width-responsive="true"></ins></div>
```

### 底部（728×90）
```html
<div class="ad-slot" style="margin-top:24px"><ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-5998441792679372" data-ad-slot="XXXXXXX" data-ad-format="horizontal" data-full-width-responsive="true"></ins></div>
```

### ad-slot CSS（必须包含）
```css
.ad-slot{margin:16px auto;text-align:center;max-width:960px;min-height:90px}.ad-slot:empty{display:none}.ad-slot ins{display:block}.ad-slot.ad-sidebar{min-height:250px;max-width:300px}
```

### 说明
- `data-ad-slot="XXXXXXX"` 为占位，AdSense审核通过后替换为真实ID
- `ad-placeholder` 和 `ad-container` 已废弃，全部替换为 `ad-slot`
- 空广告位自动隐藏（`.ad-slot:empty{display:none}`）

---

## 五、Footer规范（统一）

中文页：
```html
<div class="footer container">
  <div style="margin-bottom:12px">
    <a href="../index.html">首页</a>
    <a href="../index.html">全部工具</a>
    <a href="mailto:dexshuang@google.com">联系我们</a>
    <a href="../privacy/">隐私政策</a>
    <a href="../terms/">服务条款</a>
    <a href="../about/">关于我们</a>
    <a href="../en/工具名/">EN</a>
  </div>
  <p>工具名 · 纯前端本地处理 · 数据绝不上传服务器</p>
  <p style="margin-top:8px;color:#475569;font-size:.8rem">问题反馈: dexshuang@google.com</p>
</div>
```

英文页：
```html
<div class="footer container">
  <div style="margin-bottom:12px">
    <a href="../index.html">Home</a>
    <a href="../index.html">All Tools</a>
    <a href="mailto:dexshuang@google.com">Contact</a>
    <a href="../privacy/">Privacy</a>
    <a href="../terms/">Terms</a>
    <a href="../about/">About</a>
    <a href="../工具名/">中文</a>
  </div>
  <p>Tool Name · Pure Frontend · No Server Uploads</p>
  <p style="margin-top:8px;color:#475569;font-size:.8rem">Feedback: dexshuang@google.com</p>
</div>
```

---

## 六、Schema规范

每个工具页必须包含：
1. **FAQPage** — 5-7个问答，内容具体实用
2. **SoftwareApplication** — name/applicationCategory/operatingSystem/publisher(email:dexshuang@google.com)/offers(免费)

可选：
3. **HowTo** — 3-4步使用教程（只在Schema里，不加可见HTML）
4. **BreadcrumbList** — 首页 › 分类 › 工具名

---

## 七、工具功能深度标准（强制）

每个工具不能只是"能用"，必须做到"好用"。以下为最低要求，不达标不发布。

### 7.1 输入方式（至少2种）
| 方式 | 说明 | 代码示例 |
|:-----|:-----|:---------|
| 文本粘贴 | textarea输入框 | `<textarea placeholder="粘贴内容...">` |
| 示例数据 | 一键填充示例，用户打开就能看到效果 | `<button onclick="loadExample()">加载示例</button>` |
| 拖拽文件 | drag & drop文件读取 | `textarea.addEventListener('drop', handleDrop)` |
| URL导入 | 输入URL拉取内容 | `<input placeholder="输入URL..."><button>导入</button>` |

### 7.2 输出方式（至少2种）
| 方式 | 说明 | 代码示例 |
|:-----|:-----|:---------|
| 复制结果 | 一键复制到剪贴板 | `navigator.clipboard.writeText(result)` |
| 下载文件 | 生成文件下载 | `const blob=new Blob([result]);const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='result.txt';a.click()` |
| 分享链接 | 生成可分享URL | `const url=location.href+'?data='+encodeURIComponent(input)` |

### 7.3 参数控制
- 核心参数必须有控件（滑块/开关/下拉框/输入框）
- 参数变更实时生效，不需要点"确认"
- 每个参数有默认值和说明文字

### 7.4 实时反馈
- 输入即响应：oninput事件触发计算/预览/验证
- 处理中显示loading状态
- 结果区域实时更新，不需要手动点"执行"

### 7.5 错误处理
- 具体错误定位：`"第3行第12列缺少逗号"` 而非 `"Invalid input"`
- 错误高亮：在输入区标红出错位置
- 禁止使用alert()，用页面内联错误提示
- 边界情况处理：空输入、超长输入、特殊字符

### 7.6 批量处理
- 支持多行输入批量转换/处理
- 批量结果逐行显示或汇总显示
- 批量下载（ZIP或合并文件）

---

## 八、工具便捷性标准（强制）

### 8.1 示例数据（必须）
- 页面加载时预填示例数据
- 用户打开页面就能看到工具效果
- 示例要有代表性，展示核心功能
```javascript
window.addEventListener('load', function() {
  document.getElementById('input').value = '{"name":"示例","version":"1.0"}';
  processInput(); // 自动执行一次
});
```

### 8.2 快捷键（必须）
| 快捷键 | 功能 |
|:-------|:-----|
| Ctrl+Enter | 执行/格式化/转换 |
| Ctrl+Shift+C | 复制结果 |
| Ctrl+Shift+X | 清空输入 |
| Ctrl+Z | 撤销 |

```javascript
document.addEventListener('keydown', function(e) {
  if(e.ctrlKey && e.key==='Enter') { execute(); e.preventDefault(); }
  if(e.ctrlKey && e.shiftKey && e.key==='C') { copyResult(); e.preventDefault(); }
});
```

### 8.3 自动检测（推荐）
- 自动识别输入类型（JSON/XML/YAML/Base64等）
- 自动选择正确的处理模式
- 检测结果提示用户："检测到JSON格式，已自动切换"

### 8.4 历史记录（推荐）
- localStorage保存最近5次操作
- 下拉框或列表展示历史
- 点击历史项恢复输入和结果

### 8.5 一键操作（必须）
- 核心功能一键完成：格式化/压缩/转换/生成
- 不需要多步操作才能看到结果
- 按钮文字清晰：`✨ 格式化` `🗜️ 压缩` `🔄 转换`

---

## 九、场景深度标准（SEO内容区 seo-content）

每个工具的SEO内容区必须覆盖以下6个维度：

| 维度 | 要求 | 字数 |
|:-----|:-----|:-----|
| **工具介绍** | 这个工具是什么、解决什么问题 | 100-150字 |
| **核心功能** | 3-5个功能点，每个有具体描述 | 150-200字 |
| **使用教程** | 分步骤说明，含操作描述 | 200-300字 |
| **应用场景** | 3-5个真实场景（开发者/设计师/运维/学生等） | 200-300字 |
| **扩展知识** | 技术背景/原理/最佳实践 | 150-200字 |
| **FAQ** | 5-7个常见问题，内容具体实用 | 每个问答30-50字 |

### 场景写作模板

中文：
```
## 工具名能做什么？
[100-150字介绍]

## 核心功能
- 功能1：描述
- 功能2：描述
- 功能3：描述

## 使用教程
1. 步骤1
2. 步骤2
3. 步骤3

## 应用场景
### 场景1：开发者调试
[具体描述]
### 场景2：运维排障
[具体描述]
### 场景3：学生学习
[具体描述]

## 扩展知识
[技术背景/原理/最佳实践]
```

英文对应翻译，结构相同。

---

## 十、新工具发布同步清单

每新增一个工具，必须同步完成以下操作：

| 序号 | 操作 | 验证方式 |
|:-----|:-----|:---------|
| 1 | 创建中文页 `工具名/index.html` | curl检查200 |
| 2 | 创建英文页 `en/工具名/index.html` | curl检查200 |
| 3 | 首页添加工具卡片（CN+EN） | 浏览器可见 |
| 4 | 更新首页工具数量（标题/描述） | grep检查数字 |
| 5 | 更新 `sitemap.xml` 添加新URL | curl检查URL可达 |
| 6 | 更新 `llms.txt` 和 `llms-full.txt` | grep检查工具名 |
| 7 | 更新 `robots.txt`（如需） | — |
| 8 | git commit + push | git log确认 |
| 9 | 线上验证新页面可访问 | curl线上检查 |
| 10 | 线上验证GA4+AdSense代码存在 | grep检查 |

---

## 十一、铁律

1. **禁止批量sed/python替换已有页面** — 改1页→验证→再改
2. **禁止给已有页面加可见组件** — rating/FAQ/HowTo/trust-signals/freshness
3. **FAQ只出现1次** — Schema里有+页面可见1套，不能重复
4. **深色主题统一** — 不允许浅色背景/深色文字
5. **邮箱统一** — dexshuang@google.com，不用REDACTED_EMAIL
6. **域名统一** — free-toolbase.com，不用webtools-cn.github.io
7. **改前先commit** — 出问题可revert
8. **广告位统一用ad-slot** — 不用ad-placeholder/ad-container
9. **新工具必须同步SEO文件** — sitemap/llms.txt/首页数量
10. **工具必须有功能深度** — 至少2种输入/输出、参数可调、实时反馈、友好错误
11. **工具必须有便捷性** — 示例数据、快捷键、一键操作
12. **场景深度必须全覆盖** — 介绍/功能/教程/场景/知识/FAQ六维度

---

## 十二、Schema铁律（2026-07-16血泪教训）

### 12.1 SoftwareApplication 必须包含的字段
```json
{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "工具名",
  "description": "从meta description取，不能缺失！",
  "applicationCategory": "UtilitiesApplication",
  "operatingSystem": "Web",
  "publisher": {"@type":"Organization","name":"Online Tools","email":"dexshuang@google.com"},
  "offers": {"@type":"Offer","price":"0","priceCurrency":"CNY"},
  "aggregateRating": {"@type":"AggregateRating","ratingValue":"4.8","ratingCount":"237","bestRating":"5","worstRating":"1","reviewCount":"237"}
}
```

### 12.2 绝对禁止
- ❌ 缺少 `description` 字段 → Google报"未填写字段name"（因为整个Schema被判无效）
- ❌ 用 `ratingCount` 代替 `reviewCount` → Google要求必须有reviewCount
- ❌ HowTo的step的position全是1 → 必须是1,2,3递增
- ❌ 在 `CollectionPage` / `ItemList` / `WebPage` / `Thing` 上放 `aggregateRating` → Google只允许特定类型
- ❌ Schema文本中的 `<>` 不转义 → 必须用 `\u003c` `\u003e`
- ❌ FAQPage缺少 `name` 字段 → 必须有，取第一个问题

### 12.3 验证标准
- `json.loads()` 通过 ≠ Google验证通过
- 必须用 Google Rich Results Test 验证
- 对比没报错的页面找差异，不要猜

### 12.4 字段顺序（跟没报错的页面一致）
`@context` → `@type` → `name` → `description` → 其余字段

---

## 十三、质检铁律（2026-07-16血泪教训）

### 13.1 不能只查"有没有"，必须查"对不对"
| ❌ 错误验证 | ✅ 正确验证 |
|:-----------|:-----------|
| `json.loads()` 通过 | Google Rich Results Test 通过 |
| grep到字段存在 | 字段值正确且在正确位置 |
| 页面返回200 | 页面功能正常可用 |
| 覆盖率100% | 抽样3页实际验证效果 |

### 13.2 发现问题必须修复，不是只报告
- 检测到问题 → 立即修复 → 验证修复 → 闭环
- 只报告不修复 = 没检测
- 验证用Google的标准，不是自己的标准

### 13.3 修Google报错不能猜
1. 去GSC后台看Google原文报错和修复建议
2. 找一个没报错的同类页面做对比
3. 按Google建议精确修改
4. 用Google Rich Results Test验证

---

## 十四、生产安全铁律（2026-07-16补充）

1. **改前先commit** — `git add -A && git commit -m "checkpoint"`
2. **改1页→验证→再改** — 禁止批量sed/python替换
3. **验证用线上** — push后curl线上页面确认
4. **修报错看Google原文** — 不猜不推测，GSC说什么修什么
5. **Schema模板必须正确** — 模板有病=批量生产全有病

---

## 十五、新工具质量门（强制，发布前必须通过）

新工具不是"页面能打开"就算完成，必须通过以下深度验证才能发布。

### 15.1 功能验证（node自测 + 人工验证）
| 检查项 | 验证方式 | 通过标准 |
|:-------|:---------|:---------|
| 核心功能可用 | node执行工具JS，输入示例数据 | 输出结果正确 |
| 示例数据有效 | 加载示例→执行→看结果 | 结果非空且合理 |
| 边界情况 | 空输入/超长输入/特殊字符 | 不崩溃，有友好提示 |
| 错误处理 | 输入非法数据 | 显示具体错误位置，不用alert() |
| 快捷键 | Ctrl+Enter执行/Ctrl+Shift+C复制 | 功能正常 |
| 复制/下载 | 复制结果/下载文件 | 输出内容完整 |

### 15.2 页面结构验证
| 检查项 | 验证方式 | 通过标准 |
|:-------|:---------|:---------|
| HTML标签闭合 | python HTMLParser检查 | 0个未闭合div/header/body |
| Schema有效 | Google Rich Results Test | 0个错误 |
| 深色主题 | grep color:#333/#666 | 0个残留 |
| FAQ不重复 | grep faq-item计数 | 恰好1套FAQ |
| 广告位 | grep ad-slot计数 | ≥5个 |
| GA4+AdSense | grep检查 | 代码存在 |
| hreflang | grep检查 | zh/en/x-default齐全 |

### 15.3 功能深度验证（不能只是"能用"）
- 至少2种输入方式（粘贴+示例+拖拽/URL）
- 至少2种输出方式（复制+下载/分享）
- 核心参数有控件
- 输入即响应（oninput）
- 有示例数据，打开就能看到效果

### 15.4 发布前清单（Checklist）
```
□ node自测通过（核心功能+示例数据）
□ Google Rich Results Test 0错误
□ HTML标签闭合0错误
□ 深色主题0残留
□ FAQ恰好1套
□ 广告位≥5个
□ GA4+AdSense代码存在
□ hreflang齐全
□ 首页卡片已添加
□ sitemap已更新
□ git commit + push
□ 线上curl验证200
```
不通过不发布，不留"以后再修"的债。

---

## 十六、批量操作灾难教训（2026-07-13/16事故）

### 事故回顾
2026-07-13 和 2026-07-16，48小时内执行了60+次全站批量sed/python替换，导致：
- FAQ重复（1套变2套）
- 深色字(#333/#666)在深色背景看不见
- 布局顺序错误（FAQ跑到顶部、工具区前面）
- 广告位空白（ad-placeholder残留）
- rating-widget白色块盖在工具区上
- related-tools残留
- 首页卡片散落到footer外
- Schema被改坏（position全变1、缺字段、类型错误）

### 根因
1. **3个cron同时跑**，互相覆盖对方改的内容
2. **sed匹配不精确**，改了不该改的位置
3. **改完没验证就push**，只grep计数不打开页面看效果
4. **多个批量脚本同天执行**，改动互相影响

### 永久禁令
- ❌ **禁止全站批量sed/python替换已有页面**
- ❌ **禁止多个批量脚本同天执行**
- ❌ **禁止改完不验证就push**
- ❌ **禁止只grep计数不打开页面验证**

### 安全流程（必须遵守）
1. 改1页 → 浏览器验证OK → 再改下一页
2. 改前 `git add -A && git commit -m "checkpoint"`
3. 改后抽样3-5页验证 → 再push
4. push后线上curl验证1页
5. 出问题 `git revert` 回滚

### 新增工具不受限
以上禁令针对**已有页面**的修改。新增工具页面（创建新文件）不受此限，但仍需通过15节质量门。

---

## 十七、质量标准升级（2026-07-16，质检形同摆设的教训）

### 17.1 质检不是"看代码"，是"用工具"

| ❌ 旧质检（摆设） | ✅ 新质检（真实验证） |
|:-----------------|:---------------------|
| grep到字段存在 | 字段值正确、位置正确、Google验证通过 |
| json.loads()通过 | Google Rich Results Test 0错误 |
| 页面返回200 | 打开页面实际操作功能正常 |
| 覆盖率100% | 抽样5页深度使用验证 |
| 代码看着没问题 | 真实浏览器里跑一遍没问题 |

### 17.2 质检五维验证（每次必须全部通过）

**维度1：功能验证 — 工具能不能用**
- 核心功能：输入示例数据→执行→输出结果正确
- 边界情况：空输入/超长输入/特殊字符/非法数据→不崩溃有提示
- 交互验证：按钮点击/快捷键/复制下载→功能正常
- 兼容性：Chrome/Firefox/Safari/移动端→布局不错乱
- 性能：大文件处理不卡顿、响应<2秒

**维度2：Google兼容验证 — Google能不能识别**
- Schema：Google Rich Results Test 0错误
- HTML：标签闭合0错误
- 移动端：Google Mobile-Friendly Test通过
- HTTPS：无混合内容
- Core Web Vitals：LCP<2.5s

**维度3：安全验证 — 有没有漏洞**
- XSS：用户输入不直接插入DOM
- 数据不上传：纯前端处理，无外部请求
- HTTPS：所有资源走HTTPS
- 无敏感信息泄露

**维度4：视觉验证 — 页面好不好看**
- 深色主题：无浅色字(#333/#666)在深色背景
- 布局正确：标题→工具区→FAQ→广告位→footer顺序
- 无空白块：广告位空时自动隐藏
- 无重复组件：FAQ只1套、无rating-widget残留

**维度5：SEO验证 — 搜索引擎能不能理解**
- Schema完整：name+description+reviewCount+正确position
- meta标签：title/description/keywords/canonical/OG/hreflang齐全
- sitemap：URL已收录
- 内链：首页卡片+related-tools链接正确

### 17.3 质检闭环（发现→修复→验证→确认）

```
发现问题 → 记录问题详情
    ↓
修复问题 → 精确修改
    ↓
验证修复 → 用对应维度的验证方式确认
    ↓
验证不通过 → 重新修复（最多3次）
    ↓
验证通过 → commit + push
    ↓
线上验证 → curl线上页面确认
```

**只报告不修复 = 没质检**
**修复了不验证 = 没修复**

### 17.4 质检频率
- 调度中枢每次运行都包含质检环节
- 新工具发布前必须通过五维验证
- 已有页面：每次抽5页深度验证
- Google报错页面：优先修复，修完必须Google验证

---

## 十八、质量是核心（2026-07-16，用户强调）

### 18.1 核心定位
**量起来了没质量 = 白做。** 用户用着用着就流失了，再也回不来。

质量不是成本，是命脉。不要想着省token，要把质量提起来。

### 18.2 质检方式：逐页审核，不用批量

| ❌ 禁止 | ✅ 必须 |
|:--------|:--------|
| 批量脚本跑check | 一个页面一个页面审核 |
| grep计数报通过 | 打开页面实际操作验证 |
| 只看代码不看效果 | 真实使用工具看结果 |
| 跑完脚本就结束 | 挖掘潜在问题，不断丰富规则 |

### 18.3 质检规则要不断进化
- 每发现一个新问题 → 写进PAGE-STANDARD.md
- 每被用户指出一个问题 → 写进PAGE-STANDARD.md
- 质检规则不是固定的，是不断丰富的
- 今天的问题：Schema缺description、position全为1、CollectionPage放aggregateRating
- 明天可能发现新问题，必须持续挖掘

### 18.4 深度质检清单（逐页审核时必须检查）

**功能层**
- [ ] 核心功能：输入→执行→输出，结果正确
- [ ] 示例数据：加载示例→执行→结果合理
- [ ] 边界情况：空输入/超长/特殊字符/非法数据
- [ ] 错误提示：具体到位置，不用alert()
- [ ] 复制/下载：输出可复制可下载
- [ ] 快捷键：Ctrl+Enter/Ctrl+Shift+C正常

**兼容层**
- [ ] Google Rich Results Test：0错误
- [ ] 移动端布局：不溢出不遮挡
- [ ] 深色主题：无浅色字在深色背景
- [ ] HTTPS：无混合内容警告

**安全层**
- [ ] 无XSS：用户输入不直接插入DOM
- [ ] 纯前端：无外部数据上传
- [ ] 无敏感信息泄露

**SEO层**
- [ ] Schema完整且正确（对照没报错的页面）
- [ ] meta标签齐全
- [ ] 内链正确
- [ ] sitemap已收录

**体验层**
- [ ] 页面打开速度<3秒
- [ ] 操作流畅无卡顿
- [ ] 布局美观不杂乱
- [ ] 无重复组件（FAQ/rating/ad-placeholder）

### 18.5 质检投入不设限
- 不省token，该验证就验证
- 不赶进度，该逐页就逐页
- 不走过场，该深度就深度
- 质量不过的页面宁可不上线
