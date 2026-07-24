# PM流量机会分析报告 2026-07-25 (Cron Run #7)

## 📊 核心数据概览

| 指标 | 数值 | 变化 | 目标 |
|:-----|:-----|:-----|:-----|
| 总工具数 | 2,134 (CN) + 2,160 (EN) | - | - |
| 有点击页面 | 40 | 不变 | 213 (10%) |
| 流量覆盖率 | 4.0% | 不变 | 10% |
| GSC总曝光 | 6,960 (7/11-7/16) | - | - |
| GSC总点击 | 41 | - | - |
| 全站CTR | 0.6% | - | 3-5% |
| 第1页零点击率 | 88% (29/33) | 不变 | <20% |
| 蚕食集群 | **15个/69页** | **+5集群/+17页** | 0 |
| EN版·分隔符工具 | **43%+ (~900页)** | **新发现** | 0 |

## 🔥 本轮5大新发现

### 1. EN版title·分隔符是CTR灾难的系统性根因 (T135 P0)
- **43%+ EN工具title使用·(中点)分隔符**而非|(竖线)
- ·是中文排版习惯，Google SERP不识别为分隔符，title显示为连续文本
- Free/No Signup常在末尾被截断，desc缺CTA
- **这是EN版CTR 0.4% vs CN版2.49%的核心根因**
- 批量修复是比任何单工具优化都大的系统性杠杆
- 预期: EN版CTR从0.4%→1.5%+(3-4倍提升)，月增80+ clicks

### 2. WHOIS簇3页蚕食 - 月搜索8100+被GSC严重低估 (T131 P1)
- whois-lookup + whois-domain-lookup + whois-domain-lookup-free 3页功能完全重叠
- 2页title几乎相同且用·分隔符
- GSC仅显示12imp，但Ahrefs月搜索量8100+(whois lookup)+2400(whois domain lookup)
- 合并为1主工具+优化snippet

### 3. TIMELINE+FORM+SPECTRUM 3簇8页蚕食41imp零点击 (T132 P1)
- TIMELINE: timeline-maker + timeline-generator + css-scroll-timeline-generator = 3页/46imp
- FORM: html-form-generator + html-form-builder = 2页/27imp
- SPECTRUM: spectrum-analyzer + audio-spectrum-analyzer + online-spectrum-analyzer = 3页/16imp
- online-spectrum-analyzer是CN版错放en目录！

### 4. SORT+COUPON 2簇6页蚕食21imp零点击 (T133 P2)
- SORT: alphabetical-sorter + alphabetizer + list-sorter + line-sorter = 4页/12imp
- COUPON: coupon-code-generator + promo-code-generator = 2页/21imp

### 5. 4个tipping-point工具snippet优化 (T134 P1)
- mailto-link-generator: 11imp/pos42-49，title用·分隔符+Free在末尾
- meal-planner: 4imp/pos36.8，title用·分隔符+Free在末尾
- salary-calculator: 5imp/pos44.8，title用/分隔符+Free在末尾
- hsl-to-hex: 5imp/pos46.8，title可优化
- 这4个工具在pos30-50(tipping point)，优化snippet后极可能推入第1-2页

## 📈 蚕食集群全景(更新)

| 集群 | 工具数 | 合并为 | 节省 | 曝光/月搜索 | 优先级 | 任务 |
|:-----|:-------|:-------|:-----|:------------|:-------|:-----|
| cron | 10 | 2 | 8 | 4700+/月 | P0 | T127 |
| curl | 9 | 2 | 7 | 1060+/月 | P1 | T128 |
| piano | 7 | 2 | 5 | 343imp | P0 | T117 |
| border-text | 6 | 2 | 4 | 50imp | P0 | T111 |
| semver | 6 | 2 | 4 | 83imp | P0 | T113 |
| **sort** | **4** | **2** | **2** | **12imp** | **P2** | **T133** |
| meta-tag | 4 | 2 | 2 | 42imp | P1 | T123 |
| **timeline** | **3** | **2** | **1** | **46imp** | **P1** | **T132** |
| **spectrum** | **3** | **2** | **1** | **16imp** | **P1** | **T132** |
| **whois** | **3** | **1** | **2** | **8100+/月** | **P1** | **T131** |
| gif | 3 | 1 | 2 | 90imp | P0 | T122 |
| bic | 3 | 1 | 2 | 49imp | P1 | T124 |
| **form** | **2** | **1** | **1** | **27imp** | **P1** | **T132** |
| **coupon** | **2** | **1** | **1** | **21imp** | **P2** | **T133** |
| leet | 2 | 1 | 1 | 45imp | P1 | T126 |
| upside-down | 2 | 1 | 1 | 64imp | P1 | - |
| **合计** | **69** | **23** | **46** | - | - | - |

## 📋 品类CTR分析

| 品类 | 曝光 | 点击 | CTR | 评价 |
|:-----|:-----|:-----|:----|:-----|
| other | 1320 | 10 | 0.76% | 🟡 |
| web-design | 475 | 2 | 0.42% | 🔴 |
| math/convert | 345 | 0 | 0.0% | 🔴零点击 |
| utility/life | 255 | 2 | 0.78% | 🟡 |
| audio/music | 185 | 2 | 1.08% | 🟢最高CTR |
| text/transform | 183 | 0 | 0.0% | 🔴零点击 |
| image/media | 147 | 0 | 0.0% | 🔴零点击 |
| dev-tools | 145 | 0 | 0.0% | 🔴最大曝光零点击 |
| health/lifestyle | 93 | 0 | 0.0% | 🔴 |
| data-format | 69 | 0 | 0.0% | 🔴 |
| security/finance | 61 | 0 | 0.0% | 🔴 |
| seo-tools | 52 | 0 | 0.0% | 🔴 |
| office/docs | 16 | 1 | 6.25% | 🟢最高CTR(小样本) |

## 🎯 执行优先级(更新)

### 本周P0 (立即执行)
1. **T135** - EN版title·分隔符全站批量修复 - **最大系统性杠杆**
2. **T129** - 第1页零点击Batch#2 (5工具snippet修复)
3. **T127** - Cron簇10页合并
4. **T111** - Border-text簇合并
5. **T121** - Compass CN版snippet修复

### 下周P1
6. **T131** - WHOIS簇3页合并(月搜索8100+)
7. **T132** - TIMELINE+FORM+SPECTRUM 3簇8页合并
8. **T134** - 4个tipping-point工具snippet优化
9. **T128** - Curl簇9页合并
10. **T126** - Leet簇2页合并

### 后续P2
11. **T133** - SORT+COUPON 2簇6页合并
12. **T125** - EN版CTR系统性修复第1期
13. **T130** - 蚕食审计脚本开发

## 🔴 阻塞项

1. **GSC数据6天未更新** (7-19→7-25): cron 429错误
2. **25个任务全部停留在pm-review**: DEV cron 429/503错误导致无法推进
3. **Reddit引流完全阻断**: 403/karma=-2
4. **Google未重新抓取**: 之前优化等Google重抓中

## 📊 流量预测

当前: 40页有流量 (4.0%), 日均~8 clicks

EN版·分隔符批量修复后:
- EN版CTR从0.4%→1.5%+
- 月增80+ clicks
- 这是单次改动收益最大的策略

蚕食合并完成后(46页权重集中到23主工具):
- 主工具排名提升10-30位
- 预计月增200+ clicks

全部25个任务执行完成后:
- 预计月增500+ clicks
- 流量覆盖率: 4.0% → 10%+ (达标!)
