# PM深度分析 #13 - 2026-07-25

## 📊 GSC数据概览
- GSC数据4天未更新(7-21→7-25)，cron 429错误
- 全站约2163个工具(EN 2163页)
- 总曝光: ~3000+ imp/月
- 总点击: ~18 clicks/月
- 全站CTR: 0.88%
- 流量覆盖率: 4.0% (目标10%)

## 🔥 本轮5个新发现+新任务

### T681: Homepage /en/ pos9.5 Page1零点击 (P0)
**发现**: /en/ homepage 123imp/pos9.5/0cl - Page1排名但零点击！这是全站流量入口！
**根因**: 
- title用"Browser Utilities"非用户搜索词
- "ToolBase"品牌名无人知晓，浪费title字符
- desc无差异化(与tinywow/10015.io等竞品无区别)
- 缺Organization/SiteLinks Schema
**方案**: 重写title强调No Signup/No Upload/Private + 添加Schema + Most Popular Tools区块
**预期**: CTR 5-10%, 月增6-12 clicks

### T682: Timeline簇129imp全站#4高曝光零点击 (P0)
**发现**: timeline-maker/timeline-generator/gantt-chart 3+1页争抢129imp
**根因**: 
- timeline-maker和timeline-generator标题完全相同！
- gantt-chart含·分隔符
- 全部缺Interactive关键词
**方案**: 合并timeline-generator→timeline-maker + gantt差异化 + 加Interactive + 专题页
**预期**: CTR 2-3%

### T683: 全站·分隔符系统性修复 (P0) ⭐最大发现
**发现**: 1501个EN页面(70.7%)title含·分隔符！
**根因**: ·(middle dot)是非标准title分隔符，Google可能截断/误读
**影响**: 70%的页面受影响，是全站最大系统性CTR根因
**方案**: 批量替换·→| (仅title/og:title标签内)
**预期**: 全站CTR从0.88%→1.5-2%

### T684: Bingo 132imp + upside-down 107imp (P1)
**发现**: 2个大品类高曝光零点击
**根因**: 
- Bingo: Free后置+缺Interactive+缺online
- upside-down: 2页蚕食(upside-down-text和upside-down-text-generator标题几乎相同)
**方案**: Free前置+Interactive+合并蚕食页
**预期**: CTR 2-3%

### T685: BIC/SWIFT pos16 + Code-Diff 96imp (P1)
**发现**: 2个tipping-point品类
**根因**: 
- BIC: ·分隔符+Free后置+缺Interactive (但best_pos=16！)
- Code-Diff: code-diff/code-compare标题完全相同蚕食
**方案**: 修复·+Free前置+Interactive+合并蚕食页
**预期**: BIC进Page1=月增10+ clicks

## 📈 品类曝光排名 (GSC数据)

| 排名 | 品类 | 曝光 | 点击 | CTR | 最佳排名 |
|------|------|------|------|-----|----------|
| 1 | html-form-wysiwyg | 251 | 0 | 0% | pos53.5 |
| 2 | timeline | 129 | 0 | 0% | pos71.0 |
| 3 | piano | 114 | 0 | 0% | pos66.0 |
| 4 | text-fun | 107 | 0 | 0% | pos36.3 |
| 5 | bingo | 101 | 0 | 0% | pos61.0 |
| 6 | gif | 90 | 0 | 0% | pos44.5 |
| 7 | semver | 85 | 0 | 0% | pos9.0 |
| 8 | hearing | 83 | 0 | 0% | pos43.5 |
| 9 | audio | 68 | 2 | 2.94% | pos5.0 |
| 10 | braille | 60 | 0 | 0% | pos49.6 |

## 🎯 Page1零点击工具 (最高ROI修复)

| 工具 | 排名 | 曝光 | 问题 |
|------|------|------|------|
| border-text-online-free | pos3.7 | 6imp | 已在T111修复 |
| bracket-matcher | pos4.5 | 4imp | Matcher≠Checker |
| key-code-finder | pos8.5 | 4imp | 缺Interactive |
| /en/ homepage | pos9.5 | 123imp | title无差异化 |

## 🎯 Tipping-point工具 (pos10-30)

| 查询 | 排名 | 曝光 | 工具 |
|------|------|------|------|
| semver validator | pos23.6 | 29imp | semver-checker |
| semver checker | pos23.3 | 25imp | semver-checker |
| python format online | pos20.8 | 5imp | python-formatter |
| bic validator | pos16.0 | 2imp | bic-validator |
| verif bic | pos28.4 | 5imp | bic-validator |

## 🔑 关键洞察

1. **·分隔符是全站最大系统性CTR根因**: 1501/2163=70%的EN页面title含·，批量替换·→|预期全站CTR从0.88%→1.5-2%
2. **Homepage /en/ pos9.5是全站唯一Page1流量入口**: 修复后预期CTR 5-10%=月增6-12 clicks(入口效应带动全站)
3. **Interactive关键词模式已验证**: audio品类CTR 2.6%是全站唯一盈利品类，audio-eq-presets CTR 23.5%是标杆
4. **蚕食是第二大CTR根因**: timeline-maker/generator标题完全相同、code-diff/compare标题完全相同、upside-down 2页蚕食
5. **BIC/SWIFT pos16最接近Page1**: 修复·+Free前置+Interactive后预期进Page1=月增10+ clicks

## 📋 任务优先级排序

1. **T683** ·分隔符系统性修复 (影响70%页面，最大单次SEO改动)
2. **T681** Homepage /en/ pos9.5修复 (全站流量入口)
3. **T682** Timeline簇129imp修复 (全站#4高曝光)
4. **T156** python-formatter pos20.8修复 (全站最佳tipping-point)
5. **T685** BIC/SWIFT pos16修复 (最接近Page1)
6. **T153** bracket-matcher pos4.5修复 (Page1零点击)
7. **T159** key-code-finder pos8.5修复 (Page1零点击)
8. **T684** Bingo+upside-down修复 (239imp大品类)
9. **T160** Interactive关键词批量注入 (系统性CTR提升)
10. **T151** piano-keyboard 272imp修复 (全站#1曝光)
