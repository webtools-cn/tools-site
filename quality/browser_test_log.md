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
