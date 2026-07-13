# 页面标准规范 v1.0

> 所有工具页面必须严格遵守此规范。新增/修改页面前先读此文件。

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
1. 顶部广告位        — <div class="ad-placeholder" id="ad-top">
2. container开始     — <div class="container">
3. header            — h1标题 + lang-switch（中/EN切换）
4. breadcrumb        — 首页 › 分类 › 工具名
5. hero              — 副标题 + badge（零依赖·可离线使用）
6. main-grid         — 工具区（左）+ 侧边栏广告（右）
    ├── panel        — 工具输入/输出/操作区
    └── ad-sidebar   — 2个侧边栏广告位（300×250）
7. 中部广告位        — <div class="ad-placeholder">（728×90）
8. seo-content       — SEO长文内容（工具介绍/功能/教程/场景/知识）
9. FAQ               — <div class="faq-item"> × 5-7个，只出现1次
10. 底部广告位       — <div class="ad-placeholder">（728×90）
11. container结束    — </div>
12. footer           — 首页/全部工具/联系我们/隐私政策/服务条款/关于我们/EN切换
13. 工具JS           — <script>工具逻辑</script>
14. feedback-widget  — 固定右下角反馈按钮
15. related-tools    — <link>+<div>+<script>（3行）
16. </body></html>
```

### 禁止出现的组件
- ❌ rating-widget（星级评分）— 之前批量加的，已删除
- ❌ howto-section（可见步骤）— Schema里有HowTo就够了
- ❌ freshness badge（"Updated: 日期"）— 不需要
- ❌ trust-signals — 不需要
- ❌ 重复FAQ — FAQ只出现1次
- ❌ ad-container — 用ad-placeholder代替

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

## 四、广告位规范

| 位置 | ID | 尺寸 | 代码 |
|:-----|:---|:-----|:-----|
| 顶部 | ad-top | 728×90 | `<div class="ad-placeholder" id="ad-top">广告位 - 顶部Banner (728×90)</div>` |
| 侧边栏1 | — | 300×250 | `<div class="ad-placeholder ad-sidebar">广告位 - 侧边栏1 (300×250)</div>` |
| 侧边栏2 | — | 300×250 | `<div class="ad-placeholder ad-sidebar" style="margin-top:16px">广告位 - 侧边栏2 (300×250)</div>` |
| 中部 | — | 728×90 | `<div class="ad-placeholder" style="margin-top:24px">广告位 - 中部 (728×90)</div>` |
| 底部 | — | 728×90 | `<div class="ad-placeholder" style="margin-top:24px">广告位 - 底部 (728×90)</div>` |

AdSense审核通过后，ad-placeholder替换为`<ins class="adsbygoogle">`，ad-slot填入真实ID。

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

## 七、铁律

1. **禁止批量sed/python替换已有页面** — 改1页→验证→再改
2. **禁止给已有页面加可见组件** — rating/FAQ/HowTo/trust-signals/freshness
3. **FAQ只出现1次** — Schema里有+页面可见1套，不能重复
4. **深色主题统一** — 不允许浅色背景/深色文字
5. **邮箱统一** — dexshuang@google.com，不用REDACTED_EMAIL
6. **域名统一** — free-toolbase.com，不用webtools-cn.github.io
7. **改前先commit** — 出问题可revert
