# GSC/Bing 问题清单 (2026-08-02)

## P0: Failing URLs (49个)
首页和工具页在Google索引中失败：
- https://free-toolbase.com/ (首页)
- tax-calculator, checksum-calculator, business-days-calculator
- mac-address-lookup, vin-decoder, unicode-lookup
- token-estimator, sql-explainer, reaction-test
- gpa-calculator, compound-interest-calculator
- running-pace-calculator, metronome-online
- speed-test, wifi-password-generator
- en/backwards-text, en/website-status-checker
- 等30+个其他URL

## P0: Meta Description太短
- CN 1820页 50-120字符（需扩写到120-160）
- EN 692页偏短

## P1: Robots标签问题 (4页)
- speed-test: 有index,follow但功能不可用 → 加noindex或替代方案
- wifi-password-generator: 有index,follow → 检查功能是否正常
- en/backwards-text: 缺robots标签 → 加index,follow
- en/website-status-checker: 缺robots标签且功能不可用 → 加noindex

## P1: 浅色背景 (52 CN + 53 EN)
需改为#0f172a深色主题

## P1: 空壳工具 (62个)
核心函数是stub，只输出"Generated at "+时间戳

## P1: EN含中文 (2362个)
EN页面可见内容有中文字符

## P2: 外链不足
缺少高质量域名反链，需Reddit/HN引流

## AI搜索流量TOP10
| 查询 | 引用次数 | 引用份额 | 工具 |
|:-----|:--------:|:--------:|:-----|
| 工作日计算器在线 | 1540 | 30.6% | business-days-calculator |
| online clock full screen | 208 | 13.6% | online-clock |
| 日期计算器在线 | 194 | 29.4% | date-calculator |
| random address | 142 | 12.9% | random-address-generator |
| subnet divider | 126 | 26.9% | subnet-calculator |
| big clock on screen | 103 | 15.0% | online-clock |
| random us address | 92 | 12.7% | random-address-generator |
| 工作日计算器 | 68 | 1.0% | business-days-calculator |
| 文本反转 | 67 | 31.8% | text-reverser |
| 工时计算 | 62 | 10.3% | hours-calculator |
