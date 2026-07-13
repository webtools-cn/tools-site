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

## 七、工具深度与场景深度标准

### 7.1 工具功能深度
每个工具不能只是"能用"，必须做到"好用"：

| 维度 | 要求 | 示例 |
|:-----|:-----|:-----|
| **输入方式** | 至少2种输入方式 | JSON格式化：粘贴+拖拽文件+URL导入 |
| **输出方式** | 至少2种输出方式 | 复制+下载+分享链接 |
| **参数控制** | 核心参数可调 | 密码生成器：长度/字符集/排除字符 |
| **实时反馈** | 输入即响应 | 实时预览/实时计算/实时验证 |
| **错误处理** | 友好错误提示 | "第3行第12列缺少逗号"而非"Invalid input" |
| **批量处理** | 支持批量操作 | 批量转换/批量压缩/批量生成 |
| **历史记录** | 保留最近操作 | localStorage存储最近5次操作 |

### 7.2 场景深度（SEO内容区 seo-content）
每个工具的SEO内容区必须覆盖以下场景维度：

| 场景维度 | 要求 | 字数 |
|:---------|:-----|:-----|
| **工具介绍** | 这个工具是什么、解决什么问题 | 100-150字 |
| **核心功能** | 列举3-5个核心功能点 | 150-200字 |
| **使用教程** | 分步骤说明如何使用 | 200-300字 |
| **应用场景** | 3-5个真实使用场景（开发者/设计师/运维/学生等） | 200-300字 |
| **扩展知识** | 相关技术背景/原理/最佳实践 | 150-200字 |
| **FAQ** | 5-7个常见问题，内容具体实用 | 每个问答30-50字 |

### 7.3 场景写作模板

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

## 八、新工具发布同步清单

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

## 九、铁律

1. **禁止批量sed/python替换已有页面** — 改1页→验证→再改
2. **禁止给已有页面加可见组件** — rating/FAQ/HowTo/trust-signals/freshness
3. **FAQ只出现1次** — Schema里有+页面可见1套，不能重复
4. **深色主题统一** — 不允许浅色背景/深色文字
5. **邮箱统一** — dexshuang@google.com，不用REDACTED_EMAIL
6. **域名统一** — free-toolbase.com，不用webtools-cn.github.io
7. **改前先commit** — 出问题可revert
8. **广告位统一用ad-slot** — 不用ad-placeholder/ad-container
9. **新工具必须同步SEO文件** — sitemap/llms.txt/首页数量
10. **工具必须有功能深度** — 不能只是"能用"，必须"好用"
