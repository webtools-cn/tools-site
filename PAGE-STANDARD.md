# 工具站页面标准规范 v1.0

> 所有新工具页面和页面修改必须严格遵守此规范。违反此规范的修改将被质检打回。

---

## 一、页面布局顺序（从上到下）

```
1. <head> — meta/GA4/AdSense/Schema/hreflang
2. <body>
3.   <div class="container">
4.     <div class="header"> — h1标题 + lang-switch语言切换
5.     <div class="breadcrumb"> — 面包屑导航
6.     <div class="hero"> — 一句话描述 + badge
7.     <div class="main-grid"> — 工具区（用户来用的核心功能）
8.     <div class="seo-content"> — SEO深度内容（可选）
9.     <div class="faq-section"> — FAQ常见问题
10.    <div class="footer container"> — 页脚
11.  </body>
```

**铁律：工具区(main-grid)必须在第一屏可见！**
- ❌ 禁止在工具区前面放评分/FAQ/广告/信任信号/使用步骤
- ❌ 禁止在工具区前面放任何GEO组件
- ✅ 评分/信任信号/使用步骤放在工具区后面、footer前面

---

## 二、深色主题配色（强制统一）

| 元素 | 颜色 | 用途 |
|:-----|:-----|:-----|
| 页面背景 | `#0f172a` | body背景 |
| 卡片/面板 | `#1e293b` | panel/card/faq-section背景 |
| 主文字 | `#f1f5f9` | h1/h2/h3/正文 |
| 次要文字 | `#94a3b8` | 描述/说明/FAQ答案 |
| 辅助文字 | `#64748b` | footer/小字 |
| 强调色 | `#06b6d4` | 按钮/链接/高亮 |
| 强调亮色 | `#22d3ee` | hover/active |
| 边框 | `rgba(148,163,184,.1)` | 卡片/面板边框 |
| 输入框背景 | `#0f172a` | textarea/input背景 |

**禁止使用的颜色：**
- ❌ `#fff` / `#f8f9fa` / `#f1f5f9` — 不能做背景（在深色页面上是白色块）
- ❌ `#333` / `#666` / `#1a1a2e` — 不能做文字（在深色背景上看不见）
- ❌ `#e2e8f0` — 不能做边框（太亮）

---

## 三、头部(header)标准

```html
<div class="header">
  <h1>工具名称</h1>
  <div class="lang-switch">
    <a href="../tool-name/" class="active">中文</a>
    <a href="../en/tool-name/">EN</a>
  </div>
</div>
```

- h1只放工具名称，不放评分/广告/其他
- lang-switch紧跟h1右侧

---

## 四、面包屑(breadcrumb)标准

```html
<div class="breadcrumb">
  <a href="../index.html">首页</a> › <a href="../index.html">分类名</a> › 工具名
</div>
```

---

## 五、工具区(main-grid)标准

- 工具区是页面核心，必须第一屏可见
- 左右两栏：`grid-template-columns: 1fr 300px`（PC端）
- 移动端单栏：`@media(max-width:900px) { grid-template-columns: 1fr }`
- 右侧栏预留给广告（ad-slot审核通过后启用）

---

## 六、SEO内容区(seo-content)标准

- 放在工具区后面
- 包含：工具介绍、功能列表、使用教程、应用场景
- 深色主题：h2用`#f1f5f9`，p用`#94a3b8`

---

## 七、FAQ区(faq-section)标准

```html
<div class="faq-section">
  <h2>常见问题 (FAQ)</h2>
  <div class="faq-item">
    <h3>问题</h3>
    <p>答案</p>
  </div>
  <!-- 3-5个问答 -->
</div>
```

- 放在seo-content后面、footer前面
- **只出现1次**，禁止重复
- 深色主题：背景`#1e293b`，h3用`#f1f5f9`，p用`#94a3b8`
- ❌ 禁止浅色背景(`#fff`/`#f8f9fa`)
- ❌ 禁止深色文字(`#333`/`#666`)

---

## 八、评分组件标准

- 放在FAQ后面、footer前面
- 深色主题：背景`#1e293b`，边框`rgba(148,163,184,.15)`
- 文字颜色：评分数字`#f1f5f9`，评分人数`#94a3b8`
- ❌ 禁止浅色背景(`#f8fafc`/`linear-gradient`)
- ❌ 禁止放在工具区前面

---

## 九、信任信号标准

- 精简为一行：`🔒 本地处理 · ✅ 完全免费 · ⚡ 即时结果`
- 放在工具区后面，不占大块空间
- ❌ 禁止放在工具区前面

---

## 十、使用步骤(howto-steps)标准

- 放在FAQ前面、seo-content后面
- 深色主题配色
- ❌ 禁止放在工具区前面

---

## 十一、广告位标准

- 只在footer前放1个广告位
- 空广告位必须隐藏：`.ad-container:empty{display:none}`
- 广告位容器：`max-height:0;overflow:hidden`（审核通过后改回来）
- ❌ 禁止在工具区前面放广告
- ❌ 禁止空广告位显示大块空白

---

## 十二、Footer标准

```html
<div class="footer container">
  <div style="margin-bottom:12px">
    <a href="../index.html">首页</a>
    <a href="mailto:dexshuang@google.com">联系我们</a>
    <a href="../privacy/">隐私政策</a>
    <a href="../terms/">服务条款</a>
    <a href="../about/">关于我们</a>
  </div>
  <p>工具名 · 纯前端本地处理 · 数据绝不上传服务器</p>
  <p style="margin-top:8px;color:#475569;font-size:.8rem">问题反馈: dexshuang@google.com</p>
</div>
```

- 邮箱统一用 `dexshuang@google.com`
- 隐私政策链接：`../privacy/`（不是privacy-policy/）
- 服务条款链接：`../terms/`（不是terms-of-service/）
- 关于我们链接：`../about/`

---

## 十三、Head区必含项

```html
<head>
  <!-- GA4 -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-9W1157EBQV"></script>
  <script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag("js",new Date());gtag("config","G-9W1157EBQV");</script>
  
  <!-- AdSense -->
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5998441792679372" crossorigin="anonymous"></script>
  
  <!-- Meta -->
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>工具名 - 免费在线工具 | free-toolbase.com</title>
  <meta name="description" content="描述">
  <link rel="canonical" href="https://free-toolbase.com/tool-name/">
  
  <!-- OG -->
  <meta property="og:title" content="工具名">
  <meta property="og:description" content="描述">
  <meta property="og:url" content="https://free-toolbase.com/tool-name/">
  <meta property="og:type" content="website">
  
  <!-- hreflang -->
  <link rel="alternate" hreflang="zh" href="https://free-toolbase.com/tool-name/">
  <link rel="alternate" hreflang="en" href="https://free-toolbase.com/en/tool-name/">
  <link rel="alternate" hreflang="x-default" href="https://free-toolbase.com/en/tool-name/">
  
  <!-- Schema: FAQPage + BreadcrumbList -->
  <script type="application/ld+json">...</script>
</head>
```

---

## 十四、禁止事项清单

1. ❌ 禁止在工具区前面放评分/FAQ/广告/信任信号/使用步骤
2. ❌ 禁止浅色背景(#fff/#f8fafc)在深色页面上
3. ❌ 禁止深色文字(#333/#666)在深色背景上
4. ❌ 禁止FAQ重复出现两次
5. ❌ 禁止空广告位显示大块空白
6. ❌ 禁止related-tools.css外部引用
7. ❌ 禁止第二套<style>覆盖第一套样式
8. ❌ 禁止邮箱用REDACTED_EMAIL
9. ❌ 禁止隐私政策链接用privacy-policy/（用../privacy/）
10. ❌ 禁止服务条款链接用terms-of-service/（用../terms/）
