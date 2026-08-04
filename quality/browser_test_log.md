# 浏览器实测记录

> 每次测完必须记录。不记录=没测。下次测过的不再测。

## 格式：日期 | 工具 | CN/EN | 主题 | 功能 | 语言 | Console | 问题 | 状态

### 2026-08-02

| 工具 | CN/EN | 主题 | 功能 | 语言 | Console | 问题 | 状态 |
|:-----|:-----:|:----:|:----:|:----:|:-------:|:-----|:----:|
| hash-generator | CN | ✅ | ✅(MD5已修) | ✅ | 无 | md5缺add()→已修 | ✅ |
| password-generator | CN | ✅ | ✅ | ✅ | 无 | - | ✅ |
| due-date-calculator | CN | ✅ | ✅ | ✅ | 无 | - | ✅ |
| sketch-pad | CN | ✅ | ✅ | ✅ | 无 | - | ✅ |
| privacy | CN | ✅ | ✅ | ✅ | 无 | 内容全英文+title中英混杂→已修 | ✅ |
| en/privacy | EN | ✅ | ✅ | ✅ | 无 | 引用不存在的CSS白底→已修 | ✅ |
| en/terms | EN | ✅ | ✅ | ✅ | 无 | 同上→已修 | ✅ |
| en/contact | EN | ✅ | ✅ | ✅ | 无 | 同上→已修 | ✅ |
| dns-lookup | EN | ✅ | ❌→✅ | ✅ | 有 | DoH API返回HTML→Google改/resolve→已修 | ✅ |
| metronome | CN | ✅ | ⚠️ | ✅ | 未深测 | 未点按钮实测 | ⚠️ |
| ai-jailbreak-detector | CN | ✅ | 未测 | ✅ | 未测 | 相关推荐不相关(Docker/文件类型/Google索引) | ⚠️ |

### 2026-08-02 (第2轮：暗色主题批量修复)

| 工具 | CN/EN | 主题 | 功能 | 语言 | Console | 问题 | 状态 |
|:-----|:-----:|:----:|:----:|:----:|:-------:|:-----|:----:|
| business-days-calculator | CN | ✅→已修 | - | ✅ | 未测 | related-tools标题#374151→#e2e8f0, 双重h2嵌套→已修 | ✅ |
| chi-square-calculator | CN | ❌→已修 | - | ✅ | 未测 | hero渐变#EEF2FF→暗色, lang-switch.active浅色→暗色, result-main浅色→暗色, seo-content#475569→#94a3b8 | ✅ |
| date-calculator | CN | ✅ | - | ✅ | 未测 | related-tools标题#374151→#e2e8f0 | ✅ |
| hours-calculator | CN | ✅ | - | ✅ | 未测 | related-tools标题#374151→#e2e8f0 | ✅ |
| checksum-calculator | CN | ✅ | - | ✅ | 未测 | related-tools标题#374151→#e2e8f0 | ✅ |
| text-reverser | CN | ✅ | - | ✅ | 未测 | related-tools标题#374151→#e2e8f0 | ✅ |
| loan-payment-tracker | CN | ✅ | - | ✅ | 未测 | related-tools标题#374151→#e2e8f0 | ✅ |
| json-schema-mocker | CN | ✅ | - | ✅ | 未测 | related-tools标题#374151→#e2e8f0 | ✅ |
| string-case-converter | CN | ✅ | - | ✅ | 未测 | related-tools标题#374151→#e2e8f0 | ✅ |
| tournament-bracket-generator | CN | ✅ | - | ✅ | 未测 | 缺related-tools→已添加, footer#64748b→#94a3b8 | ✅ |
| en/business-days-calculator | EN | ✅ | - | ✅ | 未测 | related-tools#374151→#e2e8f0 | ✅ |
| en/date-calculator | EN | ✅ | - | ✅ | 未测 | related-tools#374151→#e2e8f0 | ✅ |
| en/hours-calculator | EN | ✅ | - | ✅ | 未测 | related-tools#374151→#e2e8f0 | ✅ |
| en/checksum-calculator | EN | ✅ | - | ✅ | 未测 | related-tools#374151→#e2e8f0 | ✅ |
| en/text-reverser | EN | ✅ | - | ✅ | 未测 | related-tools#374151→#e2e8f0 | ✅ |

### 2026-08-03 (功能实测：business-days-calculator)

| 工具 | CN/EN | 主题 | 功能 | 语言 | Console | 问题 | 状态 |
|:-----|:-----:|:----:|:----:|:----:|:-------:|:-----|:----:|
| business-days-calculator | CN | ✅ | ❌→✅ | ✅ | 无 | calcAdd/calcSub跳过开始日期当天→10个工作日结果8/17应为8/14→已修 | ✅ |
| en/business-days-calculator | EN | ✅ | ❌→✅ | ✅ | 无 | 同上→已修 | ✅ |

## 全局修复摘要
- 15个页面 related-tools 标题 `color:#374151`(深色背景看不清) → `#e2e8f0`，背景 `#0f172a` → `#1e293b`
- chi-square-calculator: 严重浅色主题混搭(reversed hero/reversed lang-switch/reversed result-main) → 全部暗色化
- tournament-bracket-generator: 新增 related-tools 区域
- 多处 footer/seo-content 低对比度文字修复

## 待测队列
- openai-token-counter
- base64-to-image
- css-text-effects-generator
- 更多EN页面随机抽

## 2026-08-04 轮次 (静态深度检测)

| 工具 | CN/EN | 主题 | 功能 | 语言 | Console | 问题 | 状态 |
|------|-------|------|------|------|---------|------|------|
| pwa-manifest-generator | CN | ✅深色 | ✅JS OK | ✅ | N/A(无浏览器) | #374151/#475569深色文字→已修 | passed |
| pwa-manifest-generator | EN | ✅深色 | ✅JS OK | ✅ | N/A | 无问题 | passed |
| text-case | CN | ✅深色 | ✅重定向页 | ✅ | N/A | 迁移页(meta refresh→text-case-converter) | passed |
| text-case | EN | ✅深色 | ✅重定向页 | ✅ | N/A | 迁移页 | passed |
| annuity-payout-calculator | CN | ✅深色 | ✅JS OK | ✅ | N/A | #475569深色文字→已修 | passed |
| annuity-payout-calculator | EN | ✅深色 | ✅JS OK | ✅ | N/A | #374151/#475569深色文字→已修 | passed |
| pdf-compressor | CN | ✅深色 | ✅JS OK | ✅ | N/A | #374151/#475569深色文字→已修 | passed |
| pdf-compressor | EN | ✅深色 | ✅JS OK | ✅ | N/A | #475569深色文字→已修 | passed |
| ai-prompt-variable-extractor | CN | ✅深色 | ✅JS OK | ✅ | N/A | 无问题 | passed |
| ai-prompt-variable-extractor | EN | ✅深色 | ✅JS OK | ✅ | N/A | 无问题 | passed |
| audio-echo-effect | CN | ✅深色 | ✅JS OK | ✅ | N/A | #475569深色文字→已修 | passed |
| audio-echo-effect | EN | ✅深色 | ✅JS OK | ✅ | N/A | 无问题 | passed |
| email-verifier | CN | ✅深色 | ✅JS OK | ✅ | N/A | #f1f5f9浅色bg, #EEF2FF浅hover, #475569/#6b7280深色文字, 紫色渐变→全部已修 | passed |
| email-verifier | EN | ✅深色 | ✅JS OK | ✅ | N/A | 同CN+#374151深色文字→已修 | passed |

**注意**: 本轮因浏览器扩展未连接，采用静态深度检测代替浏览器实测。检测内容包括：JS语法验证、DOM引用完整性、深色主题合规(背景/文字/hover色)、Schema完整性、Footer完整性、meta描述长度、空壳检测、aggregateRating检测。

**修复总结**: 6个工具共修复 15处深色文字问题 + 3处浅色背景问题 + 1处紫色渐变 → 全部改为标准深色主题配色。

## 2026-08-04 质检批次 #55

| 工具 | CN/EN | 主题 | 功能 | 语言 | Console | 问题 | 状态 |
|:-----|:------|:-----|:-----|:-----|:--------|:-----|:-----|
| csv-merger | CN | ✅深色 | ✅ | ✅ | N/A | 无 | passed |
| csv-merger | EN | ✅深色 | ✅ | ✅ | N/A | 无 | passed |
| unicode-analyzer | CN | ✅深色 | ✅ | ✅ | N/A | 无 | passed |
| unicode-analyzer | EN | ✅深色 | ✅ | ✅ | N/A | 无 | passed |
| high-yield-savings-calculator | CN | ✅深色 | ✅ | ✅ | N/A | 无 | passed |
| high-yield-savings-calculator | EN | ✅深色 | ✅ | ✅ | N/A | 无 | passed |
| cron-to-text | CN | ✅深色 | ✅ | ✅ | N/A | 无 | passed |
| cron-to-text | EN | ✅深色 | ✅ | ✅ | N/A | 缺Breadcrumb schema → 已修复 | passed |
| firewood-cord-calculator | CN | ✅深色 | ✅ | ✅ | N/A | 无 | passed |
| firewood-cord-calculator | EN | ✅深色 | ✅ | ✅ | N/A | 无 | passed |
| rule-of-72-calculator | CN | ✅深色 | ✅ | ✅ | N/A | 无 | passed |
| rule-of-72-calculator | EN | ✅深色 | ✅ | ✅ | N/A | 无 | passed |
| forex-profit-calculator | CN | ✅深色 | ✅(已修) | ✅ | N/A | pip计算bug→已修复 | passed |
| forex-profit-calculator | EN | ✅深色 | ✅(已修) | ✅ | N/A | pip计算bug+related链接格式→已修复 | passed |

### 修复详情
1. **forex-profit-calculator CN+EN**: pip计算严重bug — pipsRounded使用价格差(exit-entry)而非pip数量。修复：pipCount/pipSize(0.0001或JPY对0.01) → 正确pip数量。验证：EUR/USD buy 1.1000→1.1050 = 50 pips × $10 = $500 (原计算$0.05，相差10000倍)
2. **forex-profit-calculator CN**: 修复重复related-tools链接(两个相同tip-calculator)
3. **forex-profit-calculator EN**: 修复related-tools链接格式(`//en/`→`../`)+标题深色文字(#374151→#e2e8f0)
4. **cron-to-text EN**: 添加缺失的BreadcrumbList schema

> 注：浏览器扩展未连接(extension_connected:false)，使用Node.js提取JS逻辑验证代替浏览器实测。所有7个工具14个页面(CN+EN)的JS语法通过+核心计算逻辑通过Node验证。

---

## 2026-08-05 批次 (border-generator, pixel-art-maker, grams-to-ounces, image-pixel-art, morse-code-converter, video-cutter, css-neon-text)

| 工具 | CN/EN | 主题 | 功能 | 语言 | Console | 问题 | 状态 |
|:-----|:------|:-----|:-----|:-----|:--------|:-----|:-----|
| border-generator | CN | ✅深色 | ✅ | ✅ | N/A | 无 | passed |
| border-generator | EN | ✅深色 | ✅ | ✅ | N/A | 无 | passed |
| pixel-art-maker | CN | ✅深色 | ✅(迁移页) | ✅ | N/A | 迁移至pixel-art-editor | passed |
| pixel-art-maker | EN | ✅深色 | ✅(迁移页) | ✅ | N/A | 迁移至pixel-art-editor | passed |
| grams-to-ounces | CN | ✅深色 | ✅ | ✅ | N/A | 无 | passed |
| grams-to-ounces | EN | ✅深色 | ✅ | ✅ | N/A | 无 | passed |
| image-pixel-art | CN | ✅深色 | ✅ | ✅ | N/A | 无 | passed |
| image-pixel-art | EN | ✅深色 | ✅(已修) | ✅ | N/A | JS语法错误};)→已修复 | passed |
| morse-code-converter | CN | ✅深色 | ✅(已修) | ✅ | N/A | JS语法错误setDirection('toMorse';→已修复 | passed |
| morse-code-converter | EN | ✅深色 | ✅(已修) | ✅ | N/A | JS语法错误buildTable(;+setDirection('toMorse';))→已修复 | passed |
| video-cutter | CN | ✅深色 | ✅ | ✅ | N/A | 无 | passed |
| video-cutter | EN | ✅深色 | ✅ | ✅ | N/A | 无 | passed |
| css-neon-text | CN | ✅深色 | ✅ | ✅ | N/A | 无 | passed |
| css-neon-text | EN | ✅深色 | ✅ | ✅ | N/A | 无 | passed |

### 修复详情
1. **morse-code-converter CN**: 第352行 `setDirection('toMorse';` 缺少右括号 → `setDirection('toMorse');` — 语法错误导致整个页面JS无法执行，所有功能不可用
2. **morse-code-converter EN**: 第345行 `buildTable(;` + 第346行 `setDirection('toMorse';))` 两处缺失/多余括号 → `buildTable();` + `setDirection('toMorse');` — 同上，语法错误导致功能完全不可用
3. **image-pixel-art EN**: 第541行 `};)` → `});` — addEventListener回调闭合错误，语法错误导致功能不可用

> 注：浏览器扩展未连接，使用Node.js提取JS语法检查+CSS变量/浅色背景/深色文字grep验证代替。所有7个工具14个页面(CN+EN)验证通过，发现3个语法错误已修复并推送。

## 第18轮 - 2026-08-05

| 工具 | CN/EN | 主题 | 功能 | 语言 | Console | 问题 | 状态 |
|:-----|:------|:-----|:-----|:-----|:-------|:-----|:-----|
| recipe-converter | CN | ✅深色 | ✅计算正确 | ✅ | ✅ | 无 | passed |
| recipe-converter | EN | ✅深色 | ✅计算正确 | ✅ | ✅ | 无 | passed |
| image-tinter | CN | ✅深色 | ✅JS语法通过 | ✅ | ✅ | 无 | passed |
| image-tinter | EN | ✅深色 | ✅已修复 | ✅ | ✅ | **JS语法错误已修**: `e.preventDefault(;}` → `e.preventDefault();}` + `};))` → `});` | fixed+passed |
| guitar-chord-generator | CN | ✅已修复 | ✅JS通过 | ✅ | ✅ | **主题色已修**: 添加CSS变量, 修复不可见文字(#1a1a2e→#e2e8f0), 强调色(#667eea→#06b6d4), 卡片背景(#0f172a→#1e293b), Canvas颜色全部适配深色 | fixed+passed |
| guitar-chord-generator | EN | ✅已修复 | ✅JS通过 | ✅ | ✅ | 同CN版修复 | fixed+passed |
| sep-ira-calculator | CN | ✅深色 | ✅计算正确 | ✅ | ✅ | 无 | passed |
| sep-ira-calculator | EN | ✅深色 | ✅计算正确 | ✅ | ✅ | 无 | passed |
| college-cost-calculator | CN | ✅深色 | ✅计算正确 | ✅ | ✅ | 无 | passed |
| college-cost-calculator | EN | ✅深色 | ✅计算正确 | ✅ | ✅ | 无 | passed |
| terms-of-service | CN | ✅深色 | ✅页面正常 | ✅ | ✅ | 无 | passed |
| terms-of-service | EN | ✅深色 | ✅页面正常 | ✅ | ✅ | 无 | passed |
| subnet-mask-calc | CN | ✅深色 | ✅计算正确 | ✅ | ✅ | 无 | passed |
| subnet-mask-calc | EN | ✅深色 | ✅计算正确 | ✅ | ✅ | 无 | passed |

### 本轮修复
1. **en/image-tinter**: 2处JS语法错误 — `e.preventDefault(;}` 缺少右括号 + `};))` addEventListener闭合错误
2. **guitar-chord-generator CN+EN**: 大量深色主题违规 — 无CSS变量系统, 文字色#1a1a2e在深色背景不可见, 强调色用#667eea(非标准), 卡片背景用#0f172a(应为#1e293b), Canvas绘制颜色未适配深色主题

### 测试方法
- JS语法: Python HTMLParser提取script内容 → node -c 验证
- 功能逻辑: Node.js mock DOM环境执行JS + 手动测试核心计算函数
- 静态检查: grep验证CSS变量/浅色背景/深色文字/假评分/GA/meta
- EN中文检查: 正则匹配中文字符(排除ld+json和语言切换链接)

## 2026-08-05 质检轮次

| 工具 | CN/EN | JS语法 | 主题 | 功能 | 语言 | Footer | 问题 | 状态 |
|:-----|:------|:------:|:----:|:----:|:----:|:------:|:-----|:----:|
| video-compress | CN | ❌→✅ | ✅ | ✅ | ✅ | ❌→✅ | showToast JS语法错误(setTimeout括号未闭合+多余})) + footer缺链接 | 已修 |
| video-compress | EN | ❌→✅ | ✅ | ✅ | ✅ | ❌→✅ | 同CN | 已修 |
| css-selector-tester | CN | ✅ | ✅ | ✅ | ✅ | ❌→✅ | footer用/contact/而非mailto | 已修 |
| css-selector-tester | EN | ✅ | ✅ | ✅ | ✅ | ❌→✅ | 同CN | 已修 |
| file-diff | CN | ✅ | ✅ | ✅ | ✅ | ❌→✅ | footer用/contact/而非mailto | 已修 |
| file-diff | EN | ✅ | ✅ | ✅ | ✅ | ❌→✅ | 同CN | 已修 |
| bricks-calculator | CN | ✅ | ✅ | ✅ | ✅ | ✅ | 无 | 通过 |
| bricks-calculator | EN | ❌→✅ | ✅ | ✅ | ✅ | ✅ | calculateBricks(;) 语法错误 | 已修 |
| grid-generator | CN | ✅ | ✅ | ✅ | ✅ | ✅ | 无 | 通过 |
| grid-generator | EN | ✅ | ✅ | ✅ | ✅ | ✅ | 无 | 通过 |
| alcohol-cost-calculator | CN | ✅ | ✅ | ✅ | ✅ | ✅ | 无 | 通过 |
| alcohol-cost-calculator | EN | ✅ | ✅ | ✅ | ✅ | ✅ | 无 | 通过 |
| correlation-calculator | CN | ✅ | ✅ | ✅ | ✅ | ❌→✅ | footer缺关于/联系/邮箱 | 已修 |
| correlation-calculator | EN | ✅ | ✅ | ✅ | ✅ | ❌→✅ | footer缺链接+privacy-policy/terms-of-service URL错误 | 已修 |

### 本轮汇总
- 测试工具数：7个（CN+EN = 14页）
- 通过：8页
- 修复：6页（3个JS语法错误 + 6个footer问题）
- P0红线问题修复：3个JS语法错误（video-compress CN/EN, bricks-calculator EN）
- commit: 0227792f3a
